      subroutine spcgto(ipn,jdtg,itauf,phip,upres,vpres,psout,lmaxp)
C
C.............................START PROLOGUE............................
C
C SCCS IDENTIFICATION:  @(#)spcgto.f	1.1 1/12/94
C                       23:29:13 /home/library/nogaps/src/sub/tbog/SCCS/s.spcgto.f
C
C CONFIGURATION IDENTIFICATION:
C
C MODULE NAME:  spcgto
C
C DESCRIPTION:
C
C COPYRIGHT:  (c) 1994 FLENUMMETOCCEN
C             U.S. GOVERNMENT DOMAIN
C             ALL RIGHTS RESERVED
C
C CONTRACT NUMBER AND TITLE:
C
C REFERENCES:
C
C CLASSIFICATION:  Unclassified
C
C RESTRICTIONS:
C
C COMPUTER/OPERATING SYSTEM DEPENDENCIES:
C
C LIBRARIES OF RESIDENCE: /a/ops/lib/libtbog159.a
C
C USAGE: call spcgto(ipn,jdtg,itauf,phip,upres,vpres,psout,lmaxp)
C
C PARAMETERS:
C      Name            Type         Usage            Description
C   ----------      ----------     -------  ----------------------------
C
C COMMON BLOCKS:
C
C
C      Block      Name     Type    Usage              Notes
C     --------  --------   ----    ------   ------------------------
C
C FILES:
C      Name        Unit    Type    Attribute  Usage       Description
C   ----------     ----  --------  --------- -------  ------------------
C
C
C DATA BASES:
C      Name             Table        Usage            Description
C   ----------     --------------  ---------   -------------------------
C
C NON-FILE INPUT/OUTPUT:
C    Name         Type        Usage             Description
C  --------      -------      ------   ------------------------------
C
C ERROR CONDITIONS:
C        CONDITION                 ACTION
C    -----------------        ----------------------------
C
C
C
C ADDITIONAL COMMENTS:
C
C.................MAINTENANCE SECTION................................
C
C MODULES CALLED:
C         Name           Description
C        -------     ----------------------
C
C LOCAL VARIABLES AND 
C          STRUCTURES:
C
C
C         Name      Type                 Description
C        ------     ----       ----------------------------------
C
C METHOD:
C
C INCLUDE FILES:
C      Name                           Description
C   ---------------    -------------------------------------------------
C
C COMPILER DEPENDENCIES: FORTRAN 77
C
C COMPILE OPTIONS:
C
C MAKEFILE: /a/ops/met/nogaps/src/sub/tbog/tbog159lib.mak
C
C RECORD OF CHANGES:
C <<CHANGE NOTICE>> version 1.0 (12 Jan 1994) -- Pauley, R.
C   Initial installation under configuration management.
C
C..............................END PROLOGUE.............................
C
c
      include 'cnstnt.h'
c
c
      dimension phip(imjm,lmaxp),upres(imjm,lmaxp),vpres(imjm,lmaxp)
      dimension pslout(lmaxp),psout(lmaxp),vten(lm+1)
     x,     slp(imjm)
c
      dimension vornow(mlmax,2,lm),divnow(mlmax,2,lm)
     *, temnow(mlmax,2,lm),shnow(mlmax,2,lm),plnow(mlmax,2)
c
      dimension ut(imjm,lm),vt(imjm,lm),tt(imjm,lm),sht(imjm,lm)
     *, pt(imjm),ts(imjm),philm(imjm),onocos(imjm)
      dimension phat(imjm,2),pk2(imjm,lm),pk(imjm,lm),phi(imjm,lm+1)
     *, plog(imjm,lm+1),sgeo(imjm),tsave(imjm),tmp(imjm),pdiff(imjm)
     *, gw(imjm),gt(imjm),sr(imjm),ptrn(imjm)
     *, phisuf(imjm),hold(imjm),filth(mlmax),filval(jtrun)
     *, poly(mlmax,jm/2),dpoly(mlmax,jm/2)
c
      common/ fftcom/ trigs(1280),ifax(19),rtsort,rtfft
c
      logical found
c
      character*16 lrec
      character*8 ipdto,jdtg
      character*48 pc3grd,pshist,psttrp,pshccn,c3grid,trpfil,shist,hccn
      data rad/6.371e6/
      data gascon/287.04/
      data cpnew/1004.64/
      data grav/9.80665/
c
      capa=1./3.5
      capap1=1.0+capa
      ptop=1.0
      pok=1000.0**capa
      radsq=rad*rad
c
c  find approximate mid-point vertical index to be used in computing
c  mean temperature for reduction to sea level pressure.
c
      msg= 1
c
c
      found=.false.
      itauf= 99999
c
      do 115 kk=1,2
c
c  look for verifying fcst on backfil
c
      call chlen(pstdir(kk),lendir)
      if(lendir.eq.0) then
      pc3grd='pc3grd'
      pshist='pshist'
      psttrp='psttrp'
      pshccn='pshccn'
      else
      pc3grd=pstdir(kk)(1:lendir)//'pc3grd'
      pshist=pstdir(kk)(1:lendir)//'pshist'
      psttrp=pstdir(kk)(1:lendir)//'psttrp'
      pshccn=pstdir(kk)(1:lendir)//'pshccn'
      endif
      iptau= 6*kk
c
      call nfread(pc3grd,msg,2,1,1,imjm,sgeo,iptau,ipdtg,istat)
      call nfread(pc3grd,msg,2,3,1,imjm,gt,iptau,ipdtg,istat)
      call nfread(pc3grd,msg,2,6,1,imjm,gw,iptau,ipdtg,istat)
      call nfread(pc3grd,msg,2,8,1,imjm,sr,iptau,ipdtg,istat)
c
      if(istat.eq.0) then
c
      call dtgfix(ipdtg,ipdto,iptau)
c
      print 100, iptau,ipdto,jdtg
  100 format(' backup fgtau=',i2,' verifying dtg=',a8
     *,' current dtg=',a8)
c
      if(ipdto.eq.jdtg) then
c
      itx= -1
      call nfread(psttrp,msg,2,1,1,imjm,pdiff,itx,ipdtg,istat)
      call nfread(psttrp,msg,2,2,1,imjm,tsave,itx,ipdtg,istat)
      call nfread(psttrp,msg,2,3,1,imjm,tmp,itx,ipdtg,istat)
c
      call nfread(pshist,msg,2,1,lm,idim2,vornow,iptau,ipdtg,istat)
      l2= 1+lm
      call nfread(pshist,msg,2,l2,lm,idim2,divnow,iptau,ipdtg,istat)
      l3= l2+lm
      call nfread(pshist,msg,2,l3,lm,idim2,temnow,iptau,ipdtg,istat)
      l4= l3+lm
      call nfread(pshist,msg,2,l4,lm,idim2,shnow,iptau,ipdtg,istat)
      l5= l4+lm
      call nfread(pshist,msg,2,l5,1,idim2,plnow,iptau,ipdtg,istat)
c
      call nfread(pshccn,msg,0,1,1,lccn,ccn,itx,ipdtg,istat)
c
      found=.true.
      itauf= iptau
      go to 116
      endif
      endif
c
c  look for verifying fcst on specfil
c
      iptau=6*kk
      call chlen(hstdir,lendir)
      if(lendir.gt.0) then
      c3grid=hstdir(1:lendir)//'c3grid'
      trpfil=hstdir(1:lendir)//'trpfil'
      shist=hstdir(1:lendir)//'shist'
      hccn=hstdir(1:lendir)//'hccn'
      else
      c3grid='c3grid'
      trpfil='trpfil'
      shist='shist'
      hccn='hccn'
      endif
      call nfread(c3grid,msg,2,1,1,imjm,sgeo,iptau,ipdtg,istat)
      call nfread(c3grid,msg,2,3,1,imjm,gt,iptau,ipdtg,istat)
      call nfread(c3grid,msg,2,6,1,imjm,gw,iptau,ipdtg,istat)
      call nfread(c3grid,msg,2,8,1,imjm,sr,iptau,ipdtg,istat)
c
      if(istat.eq.0) then
c
      call dtgfix(ipdtg,ipdto,iptau)
c
      print 110, iptau,ipdto,jdtg
  110 format(' primary fgtau=',i2,' verifying dtg=',a8
     *,' current dtg=',a8)
c
      if(ipdto.eq.jdtg) then
c
      itx= -1
      call nfread(trpfil,msg,2,1,1,imjm,pdiff,itx,ipdtg,istat)
      call nfread(trpfil,msg,2,2,1,imjm,tsave,itx,ipdtg,istat)
      call nfread(trpfil,msg,2,3,1,imjm,tmp,itx,ipdtg,istat)
c
      call nfread(shist,msg,2,1,lm,idim2,vornow,iptau,ipdtg,istat)
      l2= 1+lm
      call nfread(shist,msg,2,l2,lm,idim2,divnow,iptau,ipdtg,istat)
      l3= l2+lm
      call nfread(shist,msg,2,l3,lm,idim2,temnow,iptau,ipdtg,istat)
      l4= l3+lm
      call nfread(shist,msg,2,l4,lm,idim2,shnow,iptau,ipdtg,istat)
      l5= l4+lm
      call nfread(shist,msg,2,l5,1,idim2,plnow,iptau,ipdtg,istat)
c
      call nfread(hccn,msg,0,1,1,lccn,ccn,itx,ipdtg,istat)
c
      found= .true.
      itauf= iptau
      go to 116
      endif
      endif
      ipdto= '99999999'
  115 continue
  116 continue
c
      if(.not.found) return
      print 9898,capa,capap1,ptop,pok,radsq
 9898 format(2x,5e13.5)
      r500= 100.0
      do 130 k=1,lm
      lmid= k
      pxx= asig(k+1)+bsig(k+1)*1000.0
      if(pxx.gt.r500) go to 131
  130 continue
  131 continue
c
      call sortml(jtrun,mlmax,msort,lsort,mlsort)
c
      do 150 ml=1,mlmax
      rl= lsort(ml)
      rm= msort(ml)-1
      rlm= rl-1.0
      if(msort(ml).eq.1) rm= 0.0
      if(lsort(ml).eq.1) rlm= 0.0
      eps4(ml)= rl*rlm/radsq
      cim(ml)= rm
  150 continue
c
      call gausl3(jm,-1.0,1.0,weight,sinl)
CDIR$ IVDEP
      do 155 j=1,jm/2
      sinl(jm+1-j)= -sinl(j)
      weight(jm+1-j)= weight(j)
      ocos(j)= 1.0/(1.0-sinl(j)*sinl(j))
      ocos(jm+1-j)= ocos(j)
      cosl(j)= 1.0/sqrt(ocos(j))
      cosl(jm+1-j)= cosl(j)
  155 continue
      ij=0
      do 156 j=1,jm
      do 156 i=1,im
      ij=ij+1
      onocos(ij)=ocos(j)
  156 continue
c
c  initialize fft parameters
c
      call fftfax(im,ifax,trigs)
c
ccc      rtfft= 0.0
      rtsort= 0.0
c
c  compute legendre polynomials
c
      do 258 j=1,jm/2
      call lgndr(jtrun,mlmax,mlsort,poly(1,j),dpoly(1,j),sinl(j))
  258 continue
c
c  transform spectral history fields to grid point fields
c
c  temperature
c
cmic$ do all autoscope
cmic$1 shared(im,jm,lm,mlmax,poly,tt,sht,temnow,shnow)
cmic$1 private(k)
      do 10 k=1,lm
      call transr(im,jm,mlmax,poly,temnow(1,1,k),tt(1,k),0,0,0)
   10 continue
c
c  terrain pressure
c
      call transr(im,jm,mlmax,poly,plnow,pt,0,0,0)
c
      kbotm= 1
      ktop= 2
      tem1= 0.0
      if(ptop.gt.0.0) tem1= ptop**capap1
      tem= 1.0/pok
      tem1= tem*tem1
      do 215 i=1,imjm
      phat(i,ktop)= asig(2)+bsig(2)*pt(i)
      pk2(i,1)= tem*phat(i,ktop)**capa
  215 continue
      do 225 i=1,imjm
      pk(i,1)= (phat(i,ktop)*pk2(i,1)-tem1)
     * /(capap1*(dasig(1)+dbsig(1)*pt(i)))
  225 continue
      tem= 1.0/pok
      do 280 k=2,lm
      do 170 i=1,imjm
      phat(i,kbotm)= asig(k+1)+bsig(k+1)*pt(i)
      pk2(i,k)= tem*phat(i,kbotm)**capa
  170 continue
      do 180 i=1,imjm
      pk(i,k)= (phat(i,kbotm)*pk2(i,k)-pk2(i,k-1)*phat(i,ktop))
     * /(capap1*(dasig(k)+dbsig(k)*pt(i)))
  180 continue
      ktop= kbotm
      kbotm= 3-ktop
  280 continue
c
      do 287 k=1,lmaxp
      pslout(k)= log(psout(k))
  287 continue
c
c  hydrostatic equation
c
      do 405 l=1,lmm1
      do 405 i=1,imjm
      phi(i,l)= tt(i,l+1)*(pk(i,l+1)-pk2(i,l))+tt(i,l)
     * *(pk2(i,l)-pk(i,l))
  405 continue
c
      ograv=1.0/grav
      do 402 i=1,imjm
      phi(i,lm) = sgeo(i)+cpnew*tt(i,lm)*(pk2(i,lm)-pk(i,lm))
      phi(i,lm)=phi(i,lm)*ograv
      ts(i)=tt(i,lm)*pk2(i,lm)
      ptrn(i)=pt(i)+ptop
  402 continue
      temx=cpnew*ograv
c
      do 409 l = lmm1,1,-1
      do 408 i=1,imjm
  408 phi(i,l)=phi(i,l+1)+phi(i,l)*temx
  409 continue
c
      call qpnh(pdiff,'specoi  fg pdiff',1,1,im,jm)
      call qpnh(tsave,'specoi  fg tsave',1,1,im,jm)
      call qpnh(tmp,'specoi  fg t1000',1,1,im,jm)
c
c
      p0= 1000.0
      dkapa= 3.5
      temx= log(p0)
      do 330 i=1,imjm*lm
      plog(i,1)= temx+dkapa*log(pk(i,1))
  330 continue
c
c
c deltp is the initial difference between the sea level pressure
c and the terrain pressure.
c
c
c  add pdiff to terrain pressure to get forecast sea level pressure
c  compute correction to pdiff due to change in temperature in
c  bottom half of atmosphere during forecast
c
      fac= 6.5e-4
      temx= 1.0/(gascon*log(10.0))
      ocp= 1.0/cpnew
c
c  compute t1000 from deep layer thickness change and adiabatically
c  from bottom model level pressure.
c  we constrain the 1000 mb temperature to be between isothermal
c  and adiabatic w.r.t. the bottom model level temperature
c
      do 40 i=1,imjm
      spab= tt(i,lm)*pk(i,lm)
      rwork= tmp(i)+temx*(grav*phi(i,lmid)-sgeo(i))-tsave(i)
      spal= spab+ocp*sgeo(i)
      rwork= max(spab,min(spal,rwork))
c
c  adjust pdiff due to change in subterrain temperature
c
      spal= rwork-tmp(i)
      tmp(i)= rwork
      rwork= sgeo(i)*(pt(i)+pdiff(i))/(gascon*tmp(i)**2)
      pdiff(i)= pdiff(i)-spal*rwork
      slp(i)= pt(i)+pdiff(i)
   40 continue
c
c  spectral transform filter of slp
c
c  determine filter to be applied to first-guess fields
c
      pie=2.0*asin(1.0)
      do 605 j=1,jtrun
      if(j.ge.17.and.j.le.23) then
      arg=(j-16)*pie/8.
      filval(j)=.5+.5*cos(arg)
      else
        if(j.ge.24) then
        filval(j)=0.
        else
        filval(j)=1.
        endif
      endif
  605 continue
      do 606 ml=1,mlmax
      n= lsort(ml)
      filth(ml)=filval(n)
  606 continue
      print 603
  603 format(/2x,'  filter weights  '/)
      print 602,(filval(i),i=1,jtrun)
  602 format(2x,5e13.5)
c
c  filter sea-level pressure field
c
c     call tranrs(0,im,jm,mlmax,poly,weight,slp,plnow)
c
c     do 13 ml=2,mlmax
c     plnow(ml,1)=plnow(ml,1)*filth(ml)
c     plnow(ml,2)=plnow(ml,2)*filth(ml)
c  13 continue
c
c     call transr(im,jm,mlmax,poly,plnow,slp,0,0,0)
c
c  laplacian smoothing of slp under high terrain
c
      call tranrs(0,im,jm,mlmax,poly,weight,slp,plnow)
c
      do 14 ml=1,mlmax
      plnow(ml,1)= plnow(ml,1)*eps4(ml)
      plnow(ml,2)= plnow(ml,2)*eps4(ml)
   14 continue
c
      call transr(im,jm,mlmax,poly,plnow,hold,0,0,0)
c
      tem=(2.5e10*(48.0/jtrun)**2)/50000.
      do 5 i=1,imjm
      spab= tem*sgeo(i)
      if(sgeo(i).lt.1000.0) spab= 0.0
      slp(i)= slp(i)-hold(i)*spab
    5 continue
c
c  compute height of 1000 mb from slp and 1000mb temp
c
      p608= 0.608
      fac= 1088.0
      temx= 0.001
      do 47 i=1,imjm
      phi(i,lm+1)= ograv*(gascon*tmp(i)*log(temx*slp(i))-fac)
      plog(i,lm+1)= pslout(lmaxp)
      hold(i)= pt(i)+ptop
   47 continue
c
      call geostd(imjm,hold,phisuf)
c
      do 48 i=1,imjm
      spab= log(hold(i))
      if((plog(i,lm).lt.pslout(lmaxp))
     * .and.(spab.gt.pslout(lmaxp))) then
      plog(i,lm+1)= spab
      phi(i,lm+1)= ograv*sgeo(i)-phisuf(i)
      endif
c
      if(plog(i,lm).ge.pslout(lmaxp)) plog(i,lm+1)=plog(i,lm)+temx
   48 continue
      do 49 i=1,imjm
      philm(i)=phi(i,lm)
   49 continue
c
c  convert geopotentials to d-values at sigma pressures
c
      do 11 k=1,lm
c
      do 88 i=1,imjm
      hold(i)= p0*sqrt(pk(i,k))*pk(i,k)*pk(i,k)*pk(i,k)
   88 continue
c
      call geostd(imjm,hold,phisuf)
c
      do 11 i=1,imjm
      phi(i,k)= phi(i,k)-phisuf(i)
   11 continue
c
      do 12 i=1,imjm
      if(plog(i,lm).ge.pslout(lmaxp)) phi(i,lm+1)=phi(i,lm)
   12 continue
c
      do 16 k=1,lm+1
      vten(k)= 1.0
   16 continue
c
c  store unfiltered heights in phip
c
      call s2ptrp(im,jm,lm,lmaxp,phi,phi(1,lm+1),plog,phip,pslout
     *,vten)
c
c  filter geopotential height fields on pressure levels
c
cmic$ do all autoscope
cmic$1 shared(im,jm,lmaxp,mlmax,poly,weight,phip,temnow,filth)
cmic$1 private(ml,k)
      do 600 k=1,lmaxp
      call tranrs(0,im,jm,mlmax,poly,weight,phip(1,k),temnow(1,1,k))
c
      do 601 ml=2,mlmax
      temnow(ml,1,k)=temnow(ml,1,k)*filth(ml)
      temnow(ml,2,k)=temnow(ml,2,k)*filth(ml)
  601 continue
c
      call transr(im,jm,mlmax,poly,temnow(1,1,k),phip(1,k),0,0,0)
  600 continue
c
c  get wind fields from vorticity and divergence
c
c **************************************************************
c
c
cmic$ do all autoscope
cmic$1 shared(im,jm,lm,mlmax,radsq,ocos,eps4,cim,poly,dpoly)
cmic$1 shared(divnow,vornow,ut,vt,filth)
cmic$1 private(ml,k)
      do 199 k=1,lm
c
c  filter divergence and vorticity fields on sigma surfaces
c  prior to determination of smoothed minus unsmoothed
c  first-guess u- and v-wind fields
c
c     do 305 ml=2,mlmax
c     divnow(ml,1,k)=divnow(ml,1,k)*filth(ml)
c     divnow(ml,2,k)=divnow(ml,2,k)*filth(ml)
c     vornow(ml,1,k)=vornow(ml,1,k)*filth(ml)
c     vornow(ml,2,k)=vornow(ml,2,k)*filth(ml)
c 305 continue
c
      call tranuv(im,jm,mlmax,radsq,ocos,eps4,cim
     *, poly,dpoly,vornow(1,1,k),divnow(1,1,k),ut(1,k),vt(1,k))
  199 continue
c
c  interpolate u- component of wind to constant pressure surfaces
c
      call s2ptrp(im,jm,lm,lmaxp,ut,ut(1,lm),plog,upres,pslout,vten)
c
c  interpolate v- component of wind to constant pressure surfaces
c
      call s2ptrp(im,jm,lm,lmaxp,vt,vt(1,lm),plog,vpres,pslout,vten)
c
c  filter u-wind field on pressure levels
c
cmic$ do all autoscope
cmic$1 shared(im,jm,lmaxp,mlmax,poly,weight)
cmic$1 shared(temnow,upres,filth)
cmic$1 private(ml,k)
      do 610 k=1,lmaxp
      call tranrs(0,im,jm,mlmax,poly,weight,upres(1,k),temnow(1,1,k))
c
      do 611 ml=2,mlmax
      temnow(ml,1,k)=temnow(ml,1,k)*filth(ml)
      temnow(ml,2,k)=temnow(ml,2,k)*filth(ml)
  611 continue
c
      call transr(im,jm,mlmax,poly,temnow(1,1,k),upres(1,k),0,0,0)
  610 continue
c
c  filter v-wind field on pressure levels
c
cmic$ do all autoscope
cmic$1 shared(im,jm,lmaxp,mlmax,poly,weight)
cmic$1 shared(temnow,vpres,filth)
cmic$1 private(ml,k)
      do 620 k=1,lmaxp
      call tranrs(0,im,jm,mlmax,poly,weight,vpres(1,k),temnow(1,1,k))
c
      do 621 ml=2,mlmax
      temnow(ml,1,k)=temnow(ml,1,k)*filth(ml)
      temnow(ml,2,k)=temnow(ml,2,k)*filth(ml)
  621 continue
c
      call transr(im,jm,mlmax,poly,temnow(1,1,k),vpres(1,k),0,0,0)
  620 continue
c ******************************************************************
c
c remove cosine latitude - earth radius weighting from winds
c
      do 410 j=1,jm
      ii= (j-1)*im
      temr= rad/cosl(j)
      do 410 i=1,im
      hold(i+ii)= temr
  410 continue
c
      do 420 k=1,lmaxp
      do 420 i=1,imjm
      upres(i,k)= upres(i,k)*hold(i)
      vpres(i,k)= vpres(i,k)*hold(i)
  420 continue
c
c  print section
c
      if(ipn.eq.0) return
c
      do 510 k=1,lmaxp
      ipp= psout(k)
      write(lrec,800) ipp,itauf,jdtg
  800 format('ht',i4,i2,a8)
      call qpnh(phip(1,k),lrec,1,1,im,jm)
      if(ipn.gt.1) call qprnth(phip(1,k),lrec,1,1,im,jm)
  510 continue
c
      do 520 k=1,lmaxp
      ipp= psout(k)
      write(lrec,820) ipp,itauf,jdtg
  820 format('ut',i4,i2,a8)
      call qpnh(upres(1,k),lrec,1,1,im,jm)
      if(ipn.gt.1) call qprnth(upres(1,k),lrec,1,1,im,jm)
  520 continue
c
      do 530 k=1,lmaxp
      ipp= psout(k)
      write(lrec,840) ipp,itauf,jdtg
  840 format('vt',i4,i2,a8)
      call qpnh(vpres(1,k),lrec,1,1,im,jm)
      if(ipn.gt.1) call qprnth(vpres(1,k),lrec,1,1,im,jm)
  530 continue
c
      write(lrec,860) itauf,jdtg
  860 format('slp',3x,i2,a8)
      call qpnh(slp,lrec,1,1,im,jm)
      if(ipn.gt.1) then
      do 865 i=1,imjm
      hold(i)= slp(i)-1000.0
  865 continue
      call qprnth(hold,lrec,1,1,im,jm)
      endif
c
c
      return
      end
