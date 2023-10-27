c
c ++++BEGIN SECONDARY EYEWALL FORMATION INDEX (p-SEF) MODULE++++
c
c Jim Kossin (NOAA/NCDC), 2010
c
c Updated June 17, 2010 by JK for cosmetic output changes
c
      subroutine psef_driver(luout,stname,tcfid,ioper,iyr,ilmon,ilday,
     .                       iltime,xfeat_plus,iflag_feat,iflag_feat_ir)
      dimension xfeat_plus(12,4),ipsef(4),iflag_feat(4),ipdferr(4)
      dimension ipsefv(4)
      dimension xfeat_t(12)
      character*10 stname
      character*8 tcfid
      character*10 cpsef(4),cpsefv(4)
c

      do i=1,4 ! initialize pdf-read error flag
         ipdferr(i)=0
      enddo

c If the IR00 predictors are in the lsdiag file, then the IRRP1.dat file 
c should be available.

      if (iflag_feat_ir.eq.0) then ! IR00 is available
         call calc_pc4(pc4,ipc4_fail) ! try to calculate pc4
         if (ipc4_fail.eq.0) then ! pc4 is available. execute full 12-feature model
            do itim=1,4         ! loop in forecast time 0,12,24,36h
               if (xfeat_plus(1,itim) .lt. 65.) then
                  ipsef(itim)=0 ! storm is not a hurricane. zero probability.
                  ipsefv(itim)=0
               elseif (xfeat_plus(12,itim) .le. 0.) then 
                  ipsef(itim)=0 ! storm center is over land. zero probability.
                  ipsefv(itim)=0
               elseif (iflag_feat(itim).eq.1) then ! missing lsdiag feature(s). flag.
                  ipsef(itim)=111
               else
                  do ifeat=1,11 ! loop in model feature
                     xfeat_t(ifeat)=xfeat_plus(ifeat,itim)
                  enddo
                  xfeat_t(12)=pc4
                  nfeat=12
                  ipsef(itim)=
     .             anint(100.*postp2(xfeat_t,nfeat,ioper,iferr)) ! call model function
                  ipdferr(itim)=iferr
                  ipsefv(itim)=
     .             anint(100.*postp2v(xfeat_t,nfeat,ioper,iferr))
               endif
            enddo

         else                   ! no pc4. execute reduced model (11 features)

            do itim=1,4         ! loop in forecast time 0,12,24,36h
               if (xfeat_plus(1,itim) .lt. 65.) then
                  ipsef(itim)=0 ! storm is not a hurricane
                  ipsefv(itim)=0
               elseif (xfeat_plus(12,itim) .le. 0.) then 
                  ipsef(itim)=0 ! storm center is over land
                  ipsefv(itim)=0
               elseif (iflag_feat(itim).eq.1) then ! missing lsdiag feature(s)
                  ipsef(itim)=111
               else
                  do ifeat=1,11 ! loop in feature
                     xfeat_t(ifeat)=xfeat_plus(ifeat,itim)
                  enddo
                  nfeat=11
                  ipsef(itim)=
     .             anint(100.*postp2(xfeat_t,nfeat,ioper,iferr)) ! call model function
                  ipdferr(itim)=iferr
                  ipsefv(itim)=
     .             anint(100.*postp2v(xfeat_t,nfeat,ioper,iferr))
               endif
            enddo
         endif

      else                      ! no IR. execute reduced model (9 features)

         do itim=1,4            ! loop in forecast time 0,12,24,36h
            if (xfeat_plus(1,itim) .lt. 65.) then
               ipsef(itim)=0    ! storm is not a hurricane
               ipsefv(itim)=0
            elseif (xfeat_plus(12,itim) .le. 0.) then 
               ipsef(itim)=0  ! storm center is over land
               ipsefv(itim)=0
            elseif (iflag_feat(itim).eq.1) then ! missing lsdiag feature(s)
               ipsef(itim)=111
            else
               do ifeat=1,9     ! loop in feature
                  xfeat_t(ifeat)=xfeat_plus(ifeat,itim)
               enddo
               nfeat=9
               ipsef(itim)=
     .          anint(100.*postp2(xfeat_t,nfeat,ioper,iferr)) ! call model function
               ipdferr(itim)=iferr
               ipsefv(itim)=
     .          anint(100.*postp2v(xfeat_t,nfeat,ioper,iferr))
            endif
         enddo
      endif

c
c output p-SEF model result to ships.txt file
c
      write(luout,600) tcfid,stname,ilmon,ilday,
     +                 iyr,iltime

  600 format(/,'**',1x,
     + 'PROBLTY OF AT LEAST 1 SCNDRY EYEWL FORMTN EVENT',
     +     1x,a8,1x,a10,
     +     1x,i2.2,'/',i2.2,'/',i4.4,2x,i2.2,' UTC **')
c
c cumulative probability for climo
c
      do i=1,4
         dum=1.
         do j=1,i
            dum=dum*(1.-float(ipsefv(j))/100.)
         enddo
         idum=anint((1.-dum)*100.)
         write(cpsefv(i),200) ipsefv(i),'(',idum,')'
      enddo

      do i=1,4
         dum=1.
         do j=1,i
            dum=dum*(1.-float(ipsef(j))/100.)
         enddo
         idum=anint((1.-dum)*100.)
         write(cpsef(i),200) ipsef(i),'(',idum,')'
      enddo
c
c over-write if there were data issues
c
      do i=1,4
         if (ipsef(i).eq.111 .or. ipdferr(i).eq.1) then
            do j=4,i,-1
               cpsef(j)=' ERR'
            enddo
         endif
      enddo

 200  format(i3,a1,i3,a1)

      write(luout,510)
 510  format('TIME(HR)',3x,'0-12',2x,'12-24(0-24)',2x,
     .     '24-36(0-36)',2x,'36-48(0-48)')

      write(luout,516) cpsefv(1),(cpsefv(i),i=2,4)

      if (iflag_feat_ir.eq.1) then ! reduced model output, no IR
         write(luout,512) (cpsef(i),i=1,4)
      elseif (ipc4_fail.eq.1) then ! reduced model output, no pc4
         write(luout,513) (cpsef(i),i=1,4)
      else
         write(luout,514) (cpsef(i),i=1,4) ! full model output. no caution.
      endif

 512  format('PROB(%)',4x,a3,4x,3(a10,3x),
     .       'IR UNAVAIL...MODEL SKILL DEGRADED')
 513  format('PROB(%)',4x,a3,4x,3(a10,3x),
     .       'PC4 UNAVAIL...MODEL SKILL DEGRADED')

 514  format('PROB(%)',4x,a3,4x,3(a10,3x),
     .       '<-- FULL MODEL PROB (RAN NORMALLY)')
 516  format('CLIMO(%)',3x,a3,4x,3(a10,3x),
     .       '<-- PROB BASED ON INTENSITY ONLY')

      return
      end

c   This is the naive Bayesian probabilistic model of 
c   Kossin and Sitkowski (MWR, 2009) for the NATL
c
      function postp2(xfeat,nfeat,ioper,iferr)
c Jim Kossin (NOAA/NCDC), 2009
      real xfeat(12)
      real x1(12,100),x2(12,100),p1(12,100),p2(12,100)
      real x1s(100),x2s(100),p1s(100),p2s(100)
      character *256 coef_location,fname
      data prior2 /.1211/ ! prior probability of SEF

c read class-conditional PDFs for each feature 

      iferr=0
      if (ioper .eq. 1) then
         call getenv("SHIPS_COEF",coef_location)
         fname =trim( coef_location ) // 'pdfs.dat'
         open(unit=10,file=fname,status='old',err=333)
      else
         open(unit=10,file='pdfs.dat',status='old',err=333)
      endif
      read(10,*,err=333) x1
      read(10,*,err=333) x2
      read(10,*,err=333) p1
      read(10,*,err=333) p2
      close(10)
      goto 334
 333  iferr=1
 334  continue

      prior1=1.-prior2 ! prior probability of non-SEF

      prod1=1.
      prod2=1.
      do ifeat=1,nfeat
         do ix=1,100
            x1s(ix)=x1(ifeat,ix)
            x2s(ix)=x2(ifeat,ix)
            p1s(ix)=p1(ifeat,ix)
            p2s(ix)=p2(ifeat,ix)
         enddo

         call straddle(xfeat(ifeat),x1s,ib1,ib2)
         dx1=abs(x1s(ib1)-x1s(ib2))
         prob=0.5*(p1s(ib1)+p1s(ib2))*dx1 ! integrate under PDF (trapezoidal)
         prod1=prod1*prob ! naive assumption

         call straddle(xfeat(ifeat),x2s,ib1,ib2)
         dx2=abs(x2s(ib1)-x2s(ib2))
         prob=0.5*(p2s(ib1)+p2s(ib2))*dx2
         prod2=prod2*prob

      enddo
      den=prior1*prod1+prior2*prod2
      postp2=(prior2/den)*prod2
      return
      end


c   naive Bayesian probabilistic model with Vmax as sole feature 

      function postp2v(xfeat,nfeat,ioper,iferr)
c Jim Kossin (NOAA/NCDC), 2009
      real xfeat(12)
      real x1(12,100),x2(12,100),p1(12,100),p2(12,100)
      real x1s(100),x2s(100),p1s(100),p2s(100)
      character *256 coef_location,fname
      data prior2 /.1211/ ! prior probability of SEF

c read class-conditional PDFs for each feature 

      iferr=0
      if (ioper .eq. 1) then
         call getenv("SHIPS_COEF",coef_location)
         fname =trim( coef_location ) // 'pdfs.dat'
         open(unit=10,file=fname,status='old',err=333)
      else
         open(unit=10,file='pdfs.dat',status='old',err=333)
      endif
      read(10,*,err=333) x1
      read(10,*,err=333) x2
      read(10,*,err=333) p1
      read(10,*,err=333) p2
      close(10)
      goto 334
 333  iferr=1
 334  continue

      prior1=1.-prior2 ! prior probability of non-SEF

      prod1=1.
      prod2=1.
      ifeat=1 ! Vmax feature
      do ix=1,100
         x1s(ix)=x1(ifeat,ix)
         x2s(ix)=x2(ifeat,ix)
         p1s(ix)=p1(ifeat,ix)
         p2s(ix)=p2(ifeat,ix)
      enddo

      call straddle(xfeat(ifeat),x1s,ib1,ib2)
      dx1=abs(x1s(ib1)-x1s(ib2))
      prob=0.5*(p1s(ib1)+p1s(ib2))*dx1 ! integrate under PDF (trapezoidal)
      prod1=prod1*prob          ! naive assumption

      call straddle(xfeat(ifeat),x2s,ib1,ib2)
      dx2=abs(x2s(ib1)-x2s(ib2))
      prob=0.5*(p2s(ib1)+p2s(ib2))*dx2
      prod2=prod2*prob

      den=prior1*prod1+prior2*prod2
      postp2v=(prior2/den)*prod2
      return
      end

c*******************************************
      subroutine straddle(val,vec,imin1,imin2)
c Jim Kossin (NOAA/NCDC), 2009
      real vec(100)
      n=100
      do i=1,2
         xmin1=99.e22
         xmin2=99.e22
         do j=1,100
            dis=abs(val-vec(j))
            if(vec(j) .le. val .and. dis .lt. xmin1) then
               xmin1=dis
               imin1=j
            endif
            if(vec(j) .gt. val .and. dis .lt. xmin2) then
               xmin2=dis
               imin2=j
            endif
         enddo
      enddo
      xlolim=vec(1)
      xuplim=vec(n)
      if(val .le. xlolim) then
         imin1=1
         imin2=2
      endif
      if(val .ge. xuplim) then
         imin1=n-1
         imin2=n
      endif
      return
      end
*****************************************************
      subroutine calc_pc4(pc4feat,ipc4_fail)
c Jim Kossin (NOAA/NCDC), 2009
      dimension rad(75),tbav(75)

      icnt=0
      open(unit=10,file='IRRP1.dat',status='old',err=30)
      do ir=1,75
         read(unit=10,fmt=222,end=30,err=30) rad(ir),tbav(ir)
         icnt=icnt+1
      enddo
 30   close(10)
 222  format(f6.1,1x,f6.2)

      do ir=1,75
         tbav(ir)=tbav(ir)-273.15
      enddo

      ipc4_fail=0
      if (icnt.lt.75) then
         ipc4_fail=1
      else
         pc4feat=pc4(rad,tbav)
      endif
      return
      end

c234567**1*********2*********3*********4*********5*********6*********7**
c
c Jim Kossin, NOAA/NCDC
c August 2009
c
c Function to calculate the 4th principal component associated with 
c an azimuthally-averaged IR brightness temperature (Tb) profile.
c The input Tb profile is 4 km resolution from 2 to 298 km out from
c storm center. The Tb profile is remapped onto a 10 km resolution 
c profile from 5 to 295 km using cubic spline interpolation. Then the
c profile is standardized at each radius, and projected onto the 4th
c EOF. The mean Tb profile, its standard deviation, and the 4th EOF
c were calculated using the 1997-2006 training data, and are read in
c as data files.

      function pc4(rad,tbprof)
      real rad(75),tbprof(75),y2a(75)
      real radi(30),eof4(30),tbav(30),tbsd(30)

      data radi /5,15,25,35,45,55,65,75,85,95,105,115,125,
     &           135,145,155,165,175,185,195,205,215,225,
     &           235,245,255,265,275,285,295/

      data tbav /-4.6483963e+01,-4.8303877e+01,-5.0960344e+01,
     &           -5.3559282e+01,-5.4983187e+01,-5.5491269e+01,
     &           -5.5363386e+01,-5.4807094e+01,-5.3829697e+01,
     &           -5.2720925e+01,-5.1489467e+01,-5.0104190e+01,
     &           -4.8661542e+01,-4.7176361e+01,-4.5687971e+01,
     &           -4.4074049e+01,-4.2459080e+01,-4.0858517e+01,
     &           -3.9171911e+01,-3.7508266e+01,-3.5869062e+01,
     &           -3.4317544e+01,-3.2619275e+01,-3.1008600e+01,
     &           -2.9471016e+01,-2.7917769e+01,-2.6391870e+01,
     &           -2.4947670e+01,-2.3606550e+01,-2.2161592e+01/

      data tbsd /2.8106663e+01,2.5422448e+01,2.2410103e+01,
     &           2.0173125e+01,1.8848620e+01,1.8095025e+01,
     &           1.7604715e+01,1.7277687e+01,1.7006015e+01,
     &           1.6777955e+01,1.6601845e+01,1.6407054e+01,
     &           1.6246333e+01,1.6106714e+01,1.5970024e+01,
     &           1.5836675e+01,1.5744422e+01,1.5679081e+01,
     &           1.5631427e+01,1.5597248e+01,1.5583210e+01,
     &           1.5573351e+01,1.5528258e+01,1.5511065e+01,
     &           1.5462713e+01,1.5420461e+01,1.5362908e+01,
     &           1.5273803e+01,1.5209599e+01,1.5097766e+01/

      data eof4 /3.5805491e-01,2.7637137e-01,1.1243732e-01,
     &          -6.8450638e-02,-1.9367073e-01,-2.5279508e-01,
     &          -2.6304075e-01,-2.3712233e-01,-1.9122983e-01,
     &          -1.3043134e-01,-6.3082689e-02,7.2187760e-03,
     &           7.2455619e-02,1.2957592e-01,1.7241220e-01,
     &           2.0660705e-01,2.2513236e-01,2.2539544e-01,
     &           2.1466190e-01,1.8938416e-01,1.5203351e-01,
     &           1.0252932e-01,4.6256525e-02,-1.1234203e-02,
     &          -6.4770702e-02,-1.1469455e-01,-1.5635822e-01,
     &          -1.9082514e-01,-2.1533300e-01,-2.3512818e-01/

c prepare derivative vectors for cubic spline interpolation
      call spline(rad,tbprof,75,1.e30,1.e30,y2a)

c project standardized interpolated Tb profile onto 4th EOF to get
c the 4th PC
      pc4=0.
      do i=1,30
         call splint(rad,tbprof,y2a,75,radi(i),dum)
         pc4=pc4+eof4(i)*(dum-tbav(i))/tbsd(i)
      enddo
      return
      end

c234567**1*********2*********3*********4*********5*********6*********7**
      SUBROUTINE SPLINE(X,Y,N,YP1,YPN,Y2)
c      implicit real*8(a-h)
c      implicit real*8(o-z)
      PARAMETER (NMAX=500)
      DIMENSION X(N),Y(N),Y2(N),U(NMAX)
      IF (YP1.GT..99e30) THEN
        Y2(1)=0.
        U(1)=0.
      ELSE
        Y2(1)=-0.5
        U(1)=(3./(X(2)-X(1)))*((Y(2)-Y(1))/(X(2)-X(1))-YP1)
      ENDIF
      DO 11 I=2,N-1
        SIG=(X(I)-X(I-1))/(X(I+1)-X(I-1))
        P=SIG*Y2(I-1)+2.
        Y2(I)=(SIG-1.)/P
        U(I)=(6.*((Y(I+1)-Y(I))/(X(I+1)-X(I))-(Y(I)-Y(I-1))
     *      /(X(I)-X(I-1)))/(X(I+1)-X(I-1))-SIG*U(I-1))/P
11    CONTINUE
      IF (YPN.GT..99e30) THEN
        QN=0.
        UN=0.
      ELSE
        QN=0.5
        UN=(3./(X(N)-X(N-1)))*(YPN-(Y(N)-Y(N-1))/(X(N)-X(N-1)))
      ENDIF
      Y2(N)=(UN-QN*U(N-1))/(QN*Y2(N-1)+1.)
      DO 12 K=N-1,1,-1
        Y2(K)=Y2(K)*Y2(K+1)+U(K)
12    CONTINUE
      RETURN
      END

c234567**1*********2*********3*********4*********5*********6*********7**
      SUBROUTINE SPLINT(XA,YA,Y2A,N,X,Y)
c      implicit real*8(a-h)
c      implicit real*8(o-z)
      DIMENSION XA(N),YA(N),Y2A(N)
      KLO=1
      KHI=N
1     IF (KHI-KLO.GT.1) THEN
        K=(KHI+KLO)/2
        IF(XA(K).GT.X)THEN
          KHI=K
        ELSE
          KLO=K
        ENDIF
      GOTO 1
      ENDIF
      H=XA(KHI)-XA(KLO)
      IF (H.EQ.0.) PAUSE 'Bad XA input.'
      A=(XA(KHI)-X)/H
      B=(X-XA(KLO))/H
      Y=A*YA(KLO)+B*YA(KHI)+
     *      ((A**3-A)*Y2A(KLO)+(B**3-B)*Y2A(KHI))*(H**2)/6.
      RETURN
      END
