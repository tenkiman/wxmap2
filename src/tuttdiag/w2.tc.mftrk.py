#!/usr/bin/env python

from WxMAP2 import *
W2=W2()

import GA
from AD import AdeckBaseDir

from tc2 import TcData,TcAdecksLocalDir,getHemis

import TCw2 as TC
import atcf

from TCdiag import tcdiagModels

from M2 import setModel2




class MfTrkAreaNhem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=0.0,
                 latN=80.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)

        self.latS=latS
        self.latN=latN

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

        self.latS=latS
        self.latN=latN

        self.setGrid(dx,dy)


class MfTrkAreaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=60.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)

        self.latS=latS
        self.latN=latN

        self.setGrid(dx,dy)




class mfTracker(f77GridOutput):


    remethod='ba'
    remethod='bl'
    remethod='' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine
    
    rexopt='linear'
    reyopt='linear'
    
    def __init__(self,model,dtg,
                 area=None,
                 taus=None,
                 vars=None,
                 doregrid=1,
                 tdir='mftrk',
                 doLogger=0,
                 Quiet=1,
                 verb=0,
                 doByTau=0,
                 version=1.0,
                 adecksource='wxmap2',
                 ):

        self.model=model
        self.dtg=dtg
        self.area=area
        self.taus=taus
        self.vars=vars
        self.doregrid=doregrid
        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.dpaths={}
        self.sstdpath=None
        self.areaname=None
        self.verb=verb
        self.doByTau=doByTau
        self.version=version
        self.adecksource=adecksource

        # -- get m2 object with model details
        #
        self.m2=setModel2(model)
        
        # -- abspath tdir set here
        #
        self.setCtl(tdir=tdir)
        self.initVars()
        self.initNgtrkVars()

        self.setTCs()

        self.setNgtrkOutput()
        if(area == None): self.setGrid()
        self.setOutput()

    def setTCs(self,ropt='',override=0):

        self.tD=TcData(verb=self.verb)
        self.ngtrp=self.tD.Carq2Ngtrp(self.dtg)
        MF.WriteList2File(self.ngtrp,self.ngpath,verb=2)

        (self.istmids,self.btcs)=self.tD.getDtg(self.dtg)

        
    def setGrid(self,ropt='',override=0):

        self.hemigrid=getHemis(self.istmids)
        if(self.hemigrid == 'nhem'):  aa=MfTrkAreaNhem()
        if(self.hemigrid == 'shem'):  aa=MfTrkAreaShem()
        if(self.hemigrid == 'global'):  aa=MfTrkAreaGlobal()

        self.area=aa

        # override to test with more general code
        #
        #self.area=W2areaGlobal()
        
        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None

        

        

    def initVars(self,undef=1e20):
        
        if(self.area == None): self.area=W2areaGlobal()


        pslvar='1.0'
        if(hasattr(self.m2,'modelpslvar')): pslvar=self.m2.modelpslvar

        pslfact=pslvar.replace('psl*','')
           
        if(self.vars == None): self.vars=['uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                                          'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                                          'vrt925:(hcurl(ua,va)*1e5):925:-999:-999:rel vort 925 [*1e5 /s]',
###                                          'vrt850:(hcurl(ua,va)*1e5):925:-999:-999:rel vort 925 [*1e5 /s]',
                                          'psl:(psl*%s):((psl(t-TM1)*TFM1)*%s + (psl(t+TP1)*TFP1)*%s):0:-999:-999:psl [mb]'%(pslfact,pslfact,pslfact),
                                          ]


        self.undef=undef
        
        if(self.taus == None):
            self.btau=0
            self.etau=144
            self.dtau=6
            self.tunits='hr'
            self.taus=range(self.btau,self.etau+1,self.dtau)


    def runTracker(self,ropt='',override=0):

        copt='-S'
        copt=''
        cmd1="%s %s %s %s %s %s %s"%(self.tracker,self.ngpath,self.mpath,self.nopath,self.ndpath,self.nfpath,copt)
        mf.runcmd(cmd1,ropt)



    def initNgtrkVars(self):

        self.oadir=self.tdir
        
        self.localadirs={}
        
        # -- trackers paths
        self.ngpath="%s/ngtrk.ngtrp.txt"%(self.tdir)
        self.ndpath="%s/ngtrk.diag.txt"%(self.tdir)
        self.nfpath="%s/ngtrk.mfdiag.txt"%(self.tdir)
        self.nopath="%s/ngtrk.out.txt"%(self.tdir)

        # -- tracker app
        #
        self.tracker='%s/ngtrkN.x'%(CL.pydir)


        # -- atcf
        
        amodel=self.model
        #if(w2.IsModel2(model)): amodel=model[0:3]

        if(amodel == 'rtfimy'):
            adeckname='f8cy'
            adecknum=99

        elif(amodel == 'rtfim'):
            adeckname='f8c'
            adecknum=99

        else:
            adeckname=atcf.ModelNametoAdeckName[amodel]
            adecknum=atcf.ModelNametoAdeckNum[amodel]

        self.amodel=amodel
        self.adeckname=adeckname
        self.adecknum=adecknum


    def setNgtrkOutput(self):

        self.adeckatcfpaths={}
        self.adeckatcfpathLocals={}

        for stmid in self.istmids:
            print 'stmid: ',stmid
            year=dtg[0:4]
            self.localadirs[stmid]="%s/%s"%(TcAdecksLocalDir,year)
            mf.ChkDir(self.localadirs[stmid],'mk')

            versionId="v%03.0f"%(self.version*10.0)
            adeckatcfpath="%s/%s.%s.%s.%s.%s"%(self.oadir,self.adecksource,versionId,self.amodel,self.dtg,stmid)
            adeckatcfpathLocal="%s/%s.%s.%s.%s.%s"%(self.localadirs[stmid],self.adecksource,versionId,self.amodel,self.dtg,stmid)
            #
            # --- create symbolic link between local ngp2 and ngp wxmap adeck ... nhc feed missing tau0
            #
            if(self.amodel == 'ngp2'):
                adeckatcfpathalias="%s/wxmap.%s.%s.%s"%(self.oadir,self.amodel[0:3],self.dtg,stmid)
            else:
                adeckatcfpathalias=''

            if(adeckatcfpathalias != ''):
                cmd="ln -s %s %s"%(adeckatcfpath,adeckatcfpathalias)
                mf.runcmd(cmd,'')

            if(verb >= 0):
                print 'AAAA:      adeckatcfpath: ',adeckatcfpath
                print 'AAAA: adeckatcfpathLocal: ',adeckatcfpathLocal

            self.adeckatcfpaths[stmid]=adeckatcfpath
            self.adeckatcfpathLocals[stmid]=adeckatcfpathLocal


    def lsAdecks(self):

        print 'GGG ',self.hemigrid
        for stmid in self.istmids:

            siz=MF.GetPathSiz(self.adeckatcfpathLocals[stmid])
            if(siz != None):
                print 'sss ',siz,self.adeckatcfpathLocals[stmid]



        


    def ngtrk2Adeck(self,
                    verb=0,
                    biascorrvmax=0):


        ntcfs={}

        otdir=self.tdir

        ngtrktrackpath=self.nopath
        ngtrkdiagmfpath=self.nfpath
        ngtrkngtrppath=self.ngpath

        #----------------------------------------------------------------------
        # read in ngtrk ngtrp and diag 
        #----------------------------------------------------------------------

        (stmdatang,stmidsng,stmvmaxmf,stmidsmf)=self.ParseNgtrkNgtrpDiagCards(ngtrkngtrppath,ngtrkdiagmfpath)

        #----------------------------------------------------------------------
        # read in ngtrk track
        #----------------------------------------------------------------------

        (stmids,stmdata,stmtaus)=self.ParseNgtrkTrackCards(ngtrktrackpath)

        pmin=0
        r34ne=0
        r34se=0
        r34sw=0
        r34nw=0

        for stmid in stmids:

            print 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqq ',stmid
            for istmid in self.istmids:
                if(stmid.upper() == istmid.split('.')[0].upper()):
                    stmidFull=istmid
                    print 'qqq ',stmidFull,istmid
                
        

            # -- open adeck file
            #

            aatcf=open(self.adeckatcfpaths[stmidFull],'w')

            stmnum=stmid[0:2]
            basin1=stmid[2:]
            basin2=TC.Basin1toBasin2[basin1]

            if(verb): print 'SSS ',stmid,basin1,basin2,self.adeckname,self.adecknum

            vmaxbias=int(stmdatang[stmid,'tcvmax']) - int(stmvmaxmf[stmid,0,'vmax'])

            vmax0=stmvmaxmf[stmid,0,'vmax']

            ntcfcst=0


            if(len(stmtaus[stmid]) == 0):
                ntcfs[stmid]=0
                continue
                
            print
            for itau in stmtaus[stmid]:

                try:
                    (rlatfc,rlonfc,rdirfc,rspdfc,rcnf)=stmdata[stmid,itau,'fcst']
                    (clat,clon,ilat,ilon,hemns,hemew)=TC.Rlatlon2Clatlon(rlatfc,rlonfc)
                    vmax=stmvmaxmf[stmid,itau,'vmax']
                    dvmax=stmvmaxmf[stmid,itau,'dvmax']
                    ntcfcst=ntcfcst+1

                except:
                    continue

                try:
                    pmin=stmvmaxmf[stmid,itau,'pmin']
                    if(pmin > 1050.0): pmin=0.
                except:
                    continue


                if(biascorrvmax):
                    #
                    # bias correct vmax forecast
                    #

                    vmaxadd=vmax
                    if(dvmax != -999):
                        vmaxadd=vmax0 + vmax0*dvmax

                        vmaxcorr=vmaxadd+vmaxbias

                    #
                    # round to nearest 5 kt
                    #

                    vmaxcorr=int(float(vmaxcorr)/5.0 + 0.5)*5

                else:
                    vmaxadd=0.0
                    vmaxcorr=vmax

                if(verb):
                    print "VVV %6.1f %7.3f %6.1f %3d"%(vmax0,dvmax,vmaxadd,vmaxcorr)
                    print 'FFF %03d  %6.1f  %7.1f :: %6.1f %6.1f'%(itau,rlatfc,rlonfc,rdirfc,rspdfc)
                    print "FFF %03d %03d%1s %04d%1s"%(itau,ilat,hemns,ilon,hemew)

                acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,self.dtg,self.adecknum,self.adeckname,itau)
                # 20030428 -- make more atcf friendly
                adum=0 
                acard1=" %3d%1s, %4d%1s, %3d, %4.0f,   ,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                        (ilat,hemns,ilon,hemew,vmaxcorr,pmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

                acard=acard0+acard1
                print 'AAA %s'%(acard)
                acard=acard+'\n'

                aatcf.writelines(acard)

            aatcf.close()

            cmd="cp %s %s"%(self.adeckatcfpaths[stmidFull],self.adeckatcfpathLocals[stmidFull])
            mf.runcmd(cmd)

            ntcfs[stmid]=ntcfcst

        #
        # add lower case stmid to ntcfs
        #

        for stmid in stmids:
            stmlow=stmid
            ntcfs[stmlow]=ntcfs[stmid]
            print 'NNNNNNNNNNNNNN ntcfs: ',stmlow,' ',ntcfs[stmid]

        return(ntcfs,stmids,stmdata,stmidsng,stmdatang)



    def ParseHeadMFdiag(self,n,cards,verb=0):

        tt=cards[n].split()
        type=tt[0]
        rtau=float(tt[2])
        stm=tt[4]
        rlon0=float(tt[5])
        rlat0=float(tt[6])
        if(verb): print 'mm1 ',cards[n],len(cards),type,rtau,stm,rlat0,rlon0

        n=n+1
        tt=cards[n].split()

        npts=int(tt[0])+int(tt[1])

        if(verb): print 'mm2 ',npts

        return(n,stm,rtau,rlat0,rlon0,type,npts)


    def ParseExtremaMFdiag(self,n,cards,rlat0,rlon0,npts,getmax=1,verb=0):

        # mf 20090401 -- changed format of the mf diag output from ngtrk.x
        #

        disttau=-999.0
        
        if(getmax):
            maxtau=-999.0
        else:
            maxtau=1e20

        for nn in range(0,npts):
            n=n+1
            try:
                tt=cards[n].split()
                doparse=1
            except:
                doparse=0

            if(doparse):
                dist=float(tt[1])
                rlon=float(tt[2])
                rlat=float(tt[3])
                rmax=float(tt[4])

                if(getmax and rmax>maxtau):
                    maxtau=rmax
                    disttau=dist
                if(not(getmax) and rmax<maxtau):
                    maxtau=rmax
                    disttau=dist

            if(verb):
                print cards[n][:-1]
                print "%s :: %6.2f %6.2f %6.2f %6.2f"%('mm3 ',rlat,rlon,rmax,dist)

        n=n+1

        return(n,maxtau,disttau)


    def ParseNgtrkTrackCards(self,ngtrkpath,verb=0):

        o=open(ngtrkpath)
        cards=o.readlines()
        o.close()

        ncards=len(cards)

        n=0
        tt=cards[n].split()
        nstm=int(tt[0])

        stmids=[]
        stmdata={}
        stmtaus={}

        n=n+1

        for i in range(0,nstm):
            tt=cards[n].split()
            stmid=tt[0]
            stmtaus[stmid]=[]
            stmids.append(stmid)
            n=n+1

        # next card is blank, skip 2 because we started at 1 vice 0

        n=n+2

        while(n < ncards):

            tt=cards[n].split()
            tau=tt[0]

            if(tau == '***'):
                stm=tt[1]
                rlatcarq=float(tt[2])
                rloncarq=float(tt[3])
                itau=0

                stmdata[stm,itau,'carq']=(rlatcarq,rloncarq)

            elif(tau.find('FIN') >= 0 or tau.find('LOS') >= 0):
                print 'done/lost'

            else:
                stm=tt[1]
                rlat=tt[2]
                rlon=tt[3]
                rdir=tt[4]
                rspd=tt[5]
                rcnf="%s %s %s"%(tt[6],tt[7],tt[8])
                itau=int(tau)
                rlatfc=float(rlat)
                rlonfc=float(rlon)

                if(verb): print 'nnn ',itau,stm,rlat,rlon,rdir,rspd,rcnf
                if(rlatfc > 90.0):
                    n=n+1
                    continue            

                rdirfc=float(rdir)
                rspdfc=float(rspd)

                stmdata[stm,itau,'fcst']=(rlatfc,rlonfc,rdirfc,rspdfc,rcnf)

                
                try:
                    stmtaus[stm].append(itau)
                except:
                    stmtaus[stm]=[]
                    stmtaus[stm].append(itau)

            n=n+1

        return(stmids,stmdata,stmtaus)



    def ParseNgtrkNgtrpDiagCards(self,ngtrkngtrppath,ngtrkdiagmfpath,verb=0):


        #----------------------------------------------------------------------
        # parse the ngtrp file
        #----------------------------------------------------------------------

        stmdatang={}
        stmidsng=[]
        stmvmaxmf={}
        stmidsmf=[]

        print 'pppppppppppp ',ngtrkngtrppath
        o=open(ngtrkngtrppath)
        cards=o.readlines()
        o.close()

        ncards=len(cards)

        n=1
        while(n < ncards):

            tt=cards[n].split()

            (tcrlat,tcrlon,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(tt[0],tt[1])

            stmid=tt[3]+tt[4]
            tcvmax=int(tt[2])
            tcdir=float(tt[7])*0.1
            tcspd=float(tt[8])*0.1
            tcr34=float(tt[5])
            tcr50=float(tt[6])

            stmidsng.append(stmid)

            stmdatang[stmid,'tcvmax']=tcvmax
            stmdatang[stmid,'tcdir']=tcdir
            stmdatang[stmid,'tcspd']=tcspd
            stmdatang[stmid,'tcr34']=tcr34
            stmdatang[stmid,'tcr50']=tcr50
            stmdatang[stmid,'tcrlat']=tcrlat
            stmdatang[stmid,'tcrlon']=tcrlon

            n=n+1

        #----------------------------------------------------------------------
        # parse the mf diag file from ngtrk.x
        #----------------------------------------------------------------------

        o=open(ngtrkdiagmfpath)
        cards=o.readlines()
        o.close()

        ncards=len(cards)
        if(verb): print 'NNN ncards ',ncards,ngtrkdiagmfpath

        n=0
        while(n < ncards):

            (n,stm,rtau,rlat0,rlon0,type,npts)=self.ParseHeadMFdiag(n,cards,verb=0)
            stmidsmf.append(stm)
            if(verb): print 'EXTRMA n: ',n,maxtau,disttau,type,stm,rlat0,rlon0

            if(type == 'PSL'):
                (n,maxtau,disttau)=self.ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts,getmax=0,verb=0)
                tau=int(rtau)
                stmvmaxmf[stm,tau,'pmin']=maxtau
                stmvmaxmf[stm,tau,'pmindist']=disttau

            elif(type == 'SPD'):
                (n,maxtau,disttau)=self.ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts,getmax=1)
                tau=int(rtau)
                stmvmaxmf[stm,tau,'vmax']=maxtau
                stmvmaxmf[stm,tau,'dist']=disttau

            else:
                (n,maxtau,disttau)=self.ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts,getmax=1)




        if(len(stmidsmf) == 0):
            rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)

        stmidsmf=mf.uniq(stmidsmf)

        dtau=self.dtau
        etau=self.etau
        btau=self.btau

        for stm in stmidsmf:

            for tau in range(btau,etau+1,dtau):

                try:
                    vmax=stmvmaxmf[stm,tau,'vmax']
                    dist=stmvmaxmf[stm,tau,'dist']
                    if(tau >= dtau):
                        taumdtau=tau-dtau
                        dvmax=stmvmaxmf[stm,tau,'vmax']-stmvmaxmf[stm,0,'vmax']
                        dvmax=dvmax/stmvmaxmf[stm,0,'vmax']
                    elif(tau == 0):
                        dvmax=0.0
                    stmvmaxmf[stm,tau,'dvmax']=dvmax

                    if(verb): print 'TTTT %s :: %03d  %6.1f  %7.1f  %7.3f'%(stm,tau,vmax,dist,dvmax)

                except:

                    stmvmaxmf[stm,tau,'vmax']=-999
                    stmvmaxmf[stm,tau,'dist']=-999
                    stmvmaxmf[stm,tau,'dvmax']=-999
                    if(verb): print 'TTTT(except) %s :: %03d  %6.1f  %7.1f  %7.3f'%(stm,tau,vmax,dist,dvmax)

                    test=1

        rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)
        return(rc)


    def SetBestNgtrkTrack(self,dtg,model,
        stmids1,stmdata1,stmtaus1,stmdatang1,stmidsng1,stmvmaxmf1,stmidsmf1,
        stmids2,stmdata2,stmtaus2,stmdatang2,stmidsng2,stmvmaxmf2,stmidsmf2,
        ipemax=200.0,ipeclose=60.0,tdratiomin=70.0,sqrlmax=40.0,fnldistratiomax=30.0,
        ):

        """ made redundant by ngtrkN.x which is more fault tolerant and stable by using the mass field (psl) as part of a three fix consensus 
        
        """

        def bestrule(model):
            #
            # 0 -- use algorithm
            # 1 -- always select sfc wind
            # 2 -- always select 850 vort

            rule=0
            if(model == 'fim8'):
                rule=2
                rule=0
            return(rule)


        def xequator(stmdata,stmid,taus):

            isshem=TC.IsShemBasinStm(stmid)
            isxeq=0
            for tau in taus:
                flat=stmdata[stmid,tau,'fcst'][0]
                if(flat > -88.0 and flat < 88.0):
                    if(isshem and flat > 0.0): isxeq=1
                    if(not(isshem) and flat < 0.0): isxeq=1

            return(isxeq)



        stmids=[]
        stmdata={}
        stmtaus={}

        stmdatang={}
        stmidsng=[]
        stmvmaxmf={}
        stmidsmf=[]

        for stmid in stmids1:

            tcvmax=stmdatang1[stmid,'tcvmax']
            tcdir=stmdatang1[stmid,'tcdir']
            tcspd=stmdatang1[stmid,'tcspd']

            try:
                taus1=stmtaus1[stmid]
            except:
                taus1=[]

            try:
                taus2=stmtaus2[stmid]
            except:
                taus2=[]


            nt1=len(taus1)
            nt2=len(taus2)

            print
            print 'BBBB',dtg,' Best trker: ',stmid,' tcdir/tcspd: ',tcdir,tcspd

            ntest=0

            if( nt1 > 0 and nt2 == 0 ):
                best=1
                if(xequator(stmdata1,stmid,taus1)): best=0

            elif(nt1 == 0 and nt2 > 0):
                best=2
                if(xequator(stmdata2,stmid,taus2)): best=0

            elif( nt1 > 0 and nt2 > 0 ):

                if(nt2 > nt1):
                    ataus=taus2
                else:
                    ataus=taus1

                totdist1=0.0
                totdist2=0.0

                for k in range(0,len(ataus)):

                    tau=ataus[k]
                    taup=ataus[k-1]

                    if(tau == 0):

                        clat1=stmdata1[stmid,tau,'carq'][0]
                        clon1=stmdata1[stmid,tau,'carq'][1]

                        try:
                            flat10=stmdata1[stmid,tau,'fcst'][0]
                            flon10=stmdata1[stmid,tau,'fcst'][1]
                            ipe1=TC.gc_dist(clat1,clon1,flat10,flon10)
                        except:
                            flon10=999.
                            flat10=99.
                            ipe1=999.

                        try:
                            flat20=stmdata2[stmid,tau,'fcst'][0]
                            flon20=stmdata2[stmid,tau,'fcst'][1]
                            ipe2=TC.gc_dist(clat1,clon1,flat20,flon20)
                        except:
                            flat20=99.
                            flon20=999.
                            ipe2=999.

                        fdist12=TC.gc_dist(flat10,flon10,flat20,flon20)
                        print 'BBBB',dtg,' ipe CARQ: ',clat1,clon1,' 1: %5.1f %6.1f ipe: %4.1f '%(flat10,flon10,ipe1),\
                              ' 2: %5.1f %6.1f ipe: %4.1f '%(flat20,flon20,ipe2),' fdist12: %4.1f'%(fdist12)


                    try:
                        flat1f=stmdata1[stmid,tau,'fcst'][0]
                        flon1f=stmdata1[stmid,tau,'fcst'][1]

                        if(k > 0):
                            flat1fp=stmdata1[stmid,taup,'fcst'][0]
                            flon1fp=stmdata1[stmid,taup,'fcst'][1]
                            totdist1=totdist1+TC.gc_dist(flat1f,flon1f,flat1fp,flon1fp)

                        spd1f=stmdata1[stmid,tau,'fcst'][3]

                    except:
                        flat1f=-99.
                        flon1f=-999.
                        spd1f=-99.

                    try:
                        flat2f=stmdata2[stmid,tau,'fcst'][0]
                        flon2f=stmdata2[stmid,tau,'fcst'][1]

                        if(k > 0):
                            flat2fp=stmdata2[stmid,taup,'fcst'][0]
                            flon2fp=stmdata2[stmid,taup,'fcst'][1]
                            totdist2=totdist2+TC.gc_dist(flat2f,flon2f,flat2fp,flon2fp)
                        spd2f=stmdata2[stmid,tau,'fcst'][3]

                    except:
                        flat2f=-99.
                        flon2f=-999.
                        spd2f=-99.



                    fdist12=-999.
                    if(TC.chklat(flat1f) and TC.chklat(flat2f)):
                        fdist12=TC.gc_dist(flat1f,flon1f,flat2f,flon2f)
                    print 'ffff: %03d'%(tau),' 1: %5.1f %6.1f %4.1f '%(flat1f,flon1f,spd1f),' 2: %5.1f %6.1f %4.1f '%(flat2f,flon2f,spd2f),\
                          ' fdist12: %5.1f'%(fdist12)

                #
                # find distance from initial postion to final positions
                #

                flat1fnl=stmdata1[stmid,taus1[-1],'fcst'][0]
                flon1fnl=stmdata1[stmid,taus1[-1],'fcst'][1]
                i2fdist1=TC.gc_dist(flat10,flon10,flat1fnl,flon1fnl)

                #
                # persistence forecast
                #
                (flat1pers,flon1pers)=TC.rumltlg(tcdir,tcspd,taus1[-1],flat10,flon10)

                flat2fnl=stmdata2[stmid,taus2[-1],'fcst'][0]
                flon2fnl=stmdata2[stmid,taus2[-1],'fcst'][1]
                i2fdist2=TC.gc_dist(flat20,flon20,flat2fnl,flon2fnl)
                (flat2pers,flon2pers)=TC.rumltlg(tcdir,tcspd,taus2[-1],flat20,flon20)

                if(flat2pers == None or flat1pers == None):
                    #
                    # case where TC goes over the poles...
                    #
                    f2f2perdist=None
                    f12f2dist=None
                    f1f2perdist=None
                else:

                    #
                    # distance from final 1 and 2 points
                    #
                    f2f2perdist=TC.gc_dist(flat2fnl,flon2fnl,flat2pers,flon2pers)
                    f12f2dist=TC.gc_dist(flat1fnl,flon1fnl,flat2fnl,flon2fnl)

                    #
                    # distance between final and persistence points
                    #
                    f1f2perdist=TC.gc_dist(flat1fnl,flon1fnl,flat1pers,flon1pers)

                #
                # normalize all distacnce to per time step 12 h
                #
                #if(nt1 >= 2):
                #   totdist1=totdist1/(nt1-1)
                #   i2fdist1=i2fdist1/(nt1-1)
                #if(nt2 >= 2):
                #   totdist2=totdist2/(nt2-1)
                #   i2fdist2=i2fdist2/(nt2-1)

                #
                # squirely ratio =  distance from tau=0 to tau=final / total distance, if small the the storm did a lot of motion to go nowhere
                #
                sqrly1=sqrly2=-999.

                if(totdist1 > 0.0):
                   sqrly1=(i2fdist1/totdist1)*100.0

                if(totdist2 > 0.0):
                   sqrly2=(i2fdist2/totdist2)*100.0

                print 'BBBB',dtg,' select nt1/ipe1: %d %3.0f'%(nt1,ipe1),' nt2/ipe2: %d %3.0f'%(nt2,ipe2),' ipemax: ',ipemax,' ipeclose: ',ipeclose
                print 'BBBB',dtg,'    totdist1: %6.0f'%(totdist1),'  totdist2: %6.0f'%(totdist2)
                print 'BBBB',dtg,'    i2fdist1: %6.0f'%(i2fdist1),'  i2fdist2: %6.0f'%(i2fdist2)
                print 'BBBB',dtg,'    sqrly1/2: %3.0f  %3.0f'%(sqrly1,sqrly2)

                #print 'BBBB',dtg,' f1f2perdist: %6.0f'%(f1f2perdist),flat10,flon10,flat1pers,flon1pers
                #print 'BBBB',dtg,' f2f2perdist: %6.0f'%(f2f2perdist)

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # selection rules:
                #
                # 1) take longest (tau) track if ipe <= ipemax
                #

                ipe1test=(ipe1 <= ipemax)
                ipe2test=(ipe2 <= ipemax)

                ipe1closetest=(ipe1 <= ipeclose)
                ipe2closetest=(ipe2 <= ipeclose)

                ipetest=0
                if(nt1 > nt2 and ipe1test):
                    best=1
                    ntest=1

                elif(nt2 > nt1 and ipe2test):
                    best=2
                    ntest=1

                #
                # if one track fails the ipemax test, just go with the one that passes
                #
                elif(ipe2test and not(ipe1test)):
                    best=2
                    ntest=22

                elif(not(ipe2test) and ipe1test):
                    best=1
                    ntest=11

                #
                # both failed...
                #
                elif(not(ipe2test) and not(ipe1test)):
                    best=0
                    ntest=99

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 2) if lengths =, go for lower ipe
                #
                elif(nt1 == nt2):

                    if(ipe1 <= ipe2):
                        best=1
                    else:
                        best=2

                    ipetest=1

                    #
                    # go with the sfc if both are less than ipeclose (60 nm)
                    #

                    if(best == 2 and ipe1 < ipeclose):
                        ipetest=3
                        best=1

                    ntest=2
                    print 'BBBB',dtg,' nt1=nt2 ipetest: %d  best: %d'%(ipetest,best)

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 3) check length of track...if one track much shorter/longer than the other
                #    then use longer, unless ipe is very good
                #

                disttest=0
                tdratio=-999.0
                if(totdist1 <= totdist2 and totdist2 > 0.0):
                    tdratio=(totdist1/totdist2)*100.0
                    if(tdratio < tdratiomin and not(ipe1closetest)):
                        best=2
                        disttest=2
                        ntest=3
                elif(totdist1 > 0.0):
                    tdratio=(totdist2/totdist1)*100.0
                    if(tdratio < tdratiomin and not(ipe2closetest) ):
                        best=1
                        disttest=1
                        ntest=3
                else:
                    distest=-1
                    best=1
                    ntest=3

                fnldisttest=0
                fnldstratio=-999.0


                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 4) now check squirlyness -- tracks that are long but go near initial position -- go for the less squirly
                #

                sqrltest=0
                dsqrl=sqrly1-sqrly2

                print 'BBBB',dtg,'      dsqrl: %4.0f'%(dsqrl)

                if(abs(dsqrl) > sqrlmax):
                    if(dsqrl > 0.0):
                        sqrltest=2
                        best=1
                        ntest=4
                    elif(dsqrl < 0.0):
                        sqrltest=1
                        best=2
                        ntest=4

                    print 'BBBBSSSQQQRRRLLLYYY setting best by squirelyness: disttest: ',disttest,' dsqrl: %4.0f'%(dsqrl),' best: ',best

                print 'BBBB',dtg,'       ntest: ',ntest,' ipetest: ',ipetest,' best= ',best
                print 'BBBB',dtg,'    disttest: ',disttest," tdratio: %3.0f"%(tdratio),' best= ',best


                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 5) check a big difference between the trackers, go with sfc
                #

                totdist12=totdist1+totdist2
                if(totdist12 > 0.0 and f12f2dist != None):
                    fnldistratio=(f12f2dist/totdist12*0.5)*100.0
                else:
                    fnldistratio=0.0
                    f12f2dist=-999.

                print 'BBBB',dtg,'   f12f2dist: %6.0f  fnldistratio: %3.0f fnldistratiomax: %3.0f'%(f12f2dist,fnldistratio,fnldistratiomax),\
                      ' disttest: ',disttest,' sqrltest: ',sqrltest
                if(totdist2 > 0.0 and totdist1 > 0.0 and disttest == 0 and sqrltest == 0 and fnldistratio > fnldistratiomax):
                    best=1
                    fnldisttest=0
                    ntest=5
                    print 'BBBBFFFNNNLLDDDRATIO   f12f2dist: %6.0f  fnldistratio: %3.0f  fnldisttest: %d'%(f12f2dist,fnldistratio,fnldisttest)

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 6) cross equator
                #

                if(best == 1 and xequator(stmdata1,stmid,taus1)):
                    best=2
                    ntest=6
                    print 'BBBBB',dtg,' XXXXXXXXXEEEEEEEEEEEEEQQQQQQQQQQQQQQQ track 1, set best=2'
                if(best == 2 and xequator(stmdata2,stmid,taus2)):
                    best=1
                    ntest=6
                    print 'BBBBB',dtg,' XXXXXXXXXEEEEEEEEEEEEEQQQQQQQQQQQQQQQ track 2, set best=1'


            else:

                #
                # no positions -- total failure of tracker
                #

                best=0
                ntest=0

            if(bestrule(model) > 0):
                best=bestrule(model)
                ntest="override by model: %s"%(model)

            print 'BBBB %s%s'%(dtg,'BBBBBBBBBBBBBBBBBBBB---> '),stmid,' best: ',best,' ntest: ',ntest

            if(best > 0):
                stmids.append(stmid)
                stmidsng.append(stmid)
                stmidsmf.append(stmid)

            if(best == 0):


                stmidsng.append(stmid)
                stmdatang[stmid,'tcvmax']=stmdatang1[stmid,'tcvmax']
                stmdatang[stmid,'tcdir']=stmdatang1[stmid,'tcdir']
                stmdatang[stmid,'tcspd']=stmdatang1[stmid,'tcspd']
                stmdatang[stmid,'tcr34']=stmdatang1[stmid,'tcr34']
                stmdatang[stmid,'tcr50']=stmdatang1[stmid,'tcr50']
                stmdatang[stmid,'tcrlat']=stmdatang1[stmid,'tcrlat']
                stmdatang[stmid,'tcrlon']=stmdatang1[stmid,'tcrlon']

            elif(best == 1):

                stmdata[stmid,0,'carq']=stmdata1[stmid,0,'carq']

                for tau in taus1:
                    stmdata[stmid,tau,'fcst']=stmdata1[stmid,tau,'fcst']
                    stmvmaxmf[stmid,tau,'vmax']=stmvmaxmf1[stmid,tau,'vmax']
                    stmvmaxmf[stmid,tau,'dist']=stmvmaxmf1[stmid,tau,'dist']
                    stmvmaxmf[stmid,tau,'dvmax']=stmvmaxmf1[stmid,tau,'dvmax']

                stmtaus[stmid]=taus1

                stmdatang[stmid,'tcvmax']=stmdatang1[stmid,'tcvmax']
                stmdatang[stmid,'tcdir']=stmdatang1[stmid,'tcdir']
                stmdatang[stmid,'tcspd']=stmdatang1[stmid,'tcspd']
                stmdatang[stmid,'tcr34']=stmdatang1[stmid,'tcr34']
                stmdatang[stmid,'tcr50']=stmdatang1[stmid,'tcr50']
                stmdatang[stmid,'tcrlat']=stmdatang1[stmid,'tcrlat']
                stmdatang[stmid,'tcrlon']=stmdatang1[stmid,'tcrlon']


            elif(best == 2):

                stmdata[stmid,0,'carq']=stmdata2[stmid,0,'carq']
                for tau in taus2:
                    stmdata[stmid,tau,'fcst']=stmdata2[stmid,tau,'fcst']
                    stmvmaxmf[stmid,tau,'vmax']=stmvmaxmf2[stmid,tau,'vmax']
                    stmvmaxmf[stmid,tau,'dist']=stmvmaxmf2[stmid,tau,'dist']
                    stmvmaxmf[stmid,tau,'dvmax']=stmvmaxmf2[stmid,tau,'dvmax']

                stmtaus[stmid]=taus2

                stmdatang[stmid,'tcvmax']=stmdatang2[stmid,'tcvmax']
                stmdatang[stmid,'tcdir']=stmdatang2[stmid,'tcdir']
                stmdatang[stmid,'tcspd']=stmdatang2[stmid,'tcspd']
                stmdatang[stmid,'tcr34']=stmdatang2[stmid,'tcr34']
                stmdatang[stmid,'tcr50']=stmdatang2[stmid,'tcr50']
                stmdatang[stmid,'tcrlat']=stmdatang2[stmid,'tcrlat']
                stmdatang[stmid,'tcrlon']=stmdatang2[stmid,'tcrlon']


        rc=(stmids,stmdata,stmtaus,stmdatang,stmidsng,stmvmaxmf,stmidsmf)

        return(rc)



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgs'],
            2:['modelopt',  """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'dols':['l',0,1,'1 - list'],
            'doKlean':['K',0,1,'0 - ! clean up .dat files'],
            'dotrkonly':['T',0,1,'1 - run only in tracker mode'],

            }

        self.purpose='''
purpose -- parse and create adeck card data shelves'''
        self.examples='''
%s test
'''


#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

dowindow=0
gaopt='-g 1024x768'

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


dtgs=mf.dtg_dtgopt_prc(dtgopt)

models=modelopt.split(',')

if(len(models) > 1 or modelopt == 'all' or len(dtgs) > 1):

    if(modelopt == 'all'): models=tcdiagModels

    for dtg in dtgs:
        for model in models:
            cmd="%s %s %s"%(CL.pypath,dtg,model)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt,lsopt='q')

    sys.exit()

else:
    model=modelopt


ctlpath=None

MF.sTimer('all')

for dtg in dtgs:

    MF.sTimer('dtg')
    MF.sTimer('mfT')
    mfT=mfTracker(model,dtg,verb=verb)
    MF.dTimer('mfT')

    if(dols): mfT.lsAdecks() ; continue
    
    MF.sTimer('fldinput')
    if( not(MF.ChkPath(mfT.nopath)) or override ):
        mfT.makeFldInput(override=override)
    MF.dTimer('fldinput')

    MF.sTimer('trk')
    mfT.runTracker(override=override)
    MF.dTimer('trk')

    MF.sTimer('adeck')
    mfT.ngtrk2Adeck(verb=verb)
    MF.dTimer('adeck')

    if(not(doKlean)): mfT.clean()
    
    MF.dTimer('dtg')

MF.dTimer('all')
    

