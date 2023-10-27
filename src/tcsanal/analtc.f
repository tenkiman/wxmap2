      subroutine analtc(ua,va,nt,iunito,iunitd,iunitp)

      common /const/ pi,deg2rad,rad2deg,ms2kt,m2ft

      integer ni, nj, maxtc, numvar, maxhr, dtau, maxhour
      integer iflg
      real dlat,dlon,rearth

      parameter (ni=360,nj=181,nk=2,ntcf=13,ntcs=12)
      parameter(dlat=1.0,dlon=1.0,rearth=6363*1e3)

      parameter(dphi=10.0)
      parameter(dr=10.0,rmax=1000.0,dt=12.0,speed=dr/dt)

      real tclat,tclon,tcstruct,modvmax,modrmax

      include 'params.h'

      common /struct/ 
     $     tclat(ntcf),tclon(ntcf),tcstruct(ntcs)

      integer nr,nphi

C         
C         run time malloc of arrays
C         

      real, save, allocatable ::  uc(:,:),vc(:,:),spd(:,:),r(:),phi(:)
      real, save, allocatable ::  ur(:,:),vr(:,:),lat(:),lon(:)
      real, save, allocatable ::  ucb(:,:),vcb(:,:),scb(:,:),dum1(:,:),dum2(:,:)
      real, save, allocatable ::  vtcngp(:),vtcngpb(:,:)

      integer, save, allocatable ::  nb(:)

      real ua(ni,nj,nk),va(ni,nj,nk)

      character id*8,quadname*5

      logical shem


      nr=nint(rmax/dr)+1
      nphi=nint(360.0/dphi)
      nq=5

      allocate (uc(nr,nphi),stat=iflag)
      allocate (vc(nr,nphi),stat=iflag)
      allocate (spd(nr,nphi),stat=iflag)
      allocate (r(nr))
      allocate (phi(nphi))
      allocate (ur(nr,nphi))
      allocate (vr(nr,nphi))
      allocate (lat(nphi))
      allocate (lon(nphi))
      allocate (ucb(nr,nq))
      allocate (vcb(nr,nq))
      allocate (scb(nr,nq))
      allocate (dum1(ni,nj))
      allocate (dum2(ni,nj))
      allocate (vtcngp(nr))
      allocate (vtcngpb(nr,nq))

      allocate (nb(nq))

      call constants(1)

      npos=nt

      curtclat=tclat(npos)
      curtclon=tclon(npos)

      shem=.false.
      if(curtclat.lt.0.0) shem=.true.


      if(verb) then
        print*,' analyze ',curtclat,curtclon,npos,iunito
        print*,' xy      ',xtc,ytc,irc
      endif

      write(*,'(a,i2,2x,f6.1,1x,f6.1)') 
     $     'analtc (n,lat,lon): ',npos,curtclat,curtclon

      call clltxy(curtclat,curtclon,xtc,ytc,irc)

      call load32(ua,dum1,levwind,ni,nj,nk)
      call load32(va,dum2,levwind,ni,nj,nk)

      rt=0.0
      nl=1
      iflag=1

      nobs=0

      do i=1,nr

        do j=1,nq

          ucb(i,j)=0.0
          vcb(i,j)=0.0
          scb(i,j)=0.0
          nb(j)=0

        end do

        do j=1,nphi

          r(i)=(i-1)*dr
          phi(j)=(j-1)*dphi

          if(i.eq.1) then
            lat(j)=curtclat
            lon(j)=curtclon
            distance=0.0
          else
            distance=dr
          endif

          call rumltlg(phi(j),distance,lat(j),lon(j),rlat1,rlon1)

          rphi=phi(j)*deg2rad

          call clltxy(lat(j),lon(j),x,y,irc)

          call bssl5(x,y,dum1,ni,nj,ur(i,j))
          call bssl5(x,y,dum2,ni,nj,vr(i,j))

          theta=atan2(ur(i,j),vr(i,j))
          spd(i,j)=rmag(ur(i,j),vr(i,j))
C         
C         boundary condition
C
          if(r(i).eq.0.0) spd(i,j)=0.0

          dangle=(rphi-theta)
          rhemfac=1.0
          if(shem) rhemfac=-1.0

          vc(i,j)=rhemfac*spd(i,j)*sin(dangle)
          uc(i,j)=rhemfac*spd(i,j)*cos(dangle)

          if(((phi(j).eq.0.0).or.(phi(j).eq.90.0).or.(phi(j).eq.180.0).or.(phi(j).eq.270.0))
     $         .and.verb) then
            write(*,'(2i4,2x,13f7.1)') 
     $           i,j,r(i),lat(j),lon(j),rmag(ur(i,j),vr(i,j)),
     $           ur(i,j),vr(i,j),phi(j),theta*rad2deg,dangle*rad2deg,
     $           uc(i,j),vc(i,j),rmag(uc(i,j),vc(i,j))
          end if

          call sumquad(ucb,vcb,nb,uc(i,j),vc(i,j),i,1,nr,nq)

          if(phi(j).ge.0.0.and.phi(j).lt.90.0) 
     $         call sumquad(ucb,vcb,nb,uc(i,j),vc(i,j),i,2,nr,nq)
          if(phi(j).ge.90.0.and.phi(j).lt.180.0) 
     $         call sumquad(ucb,vcb,nb,uc(i,j),vc(i,j),i,3,nr,nq)
          if(phi(j).ge.180.0.and.phi(j).lt.270.0) 
     $         call sumquad(ucb,vcb,nb,uc(i,j),vc(i,j),i,4,nr,nq)
          if(phi(j).ge.270.0.and.phi(j).lt.360.0) 
     $         call sumquad(ucb,vcb,nb,uc(i,j),vc(i,j),i,5,nr,nq)

          lat(j)=rlat1
          lon(j)=rlon1


          nobs=nobs+1
          
          write(id,'(i7)') nobs
          write(iunito) id,lat(j),lon(j),rt,nl,iflag
          write(iunito) r(i),vc(i,j),uc(i,j),ur(i,j),vr(i,j)

        end do

        do j=1,nq
          ucb(i,j)=ucb(i,j)/nb(j)
          vcb(i,j)=vcb(i,j)/nb(j)
          scb(i,j)=rmag(ucb(i,j),vcb(i,j))
        end do

        if(verb) then
          write(*,'(i3,2x,f6.1,2(1x,f8.2),2x,f8.2,2x,4(f8.2,1x))') 
     $         i,r(i),vcb(i,1),ucb(i,1),(scb(i,j),j=1,nq)
        endif

      end do

C         
C         write out end of time record
C         
      write(id,'(i7,a1)') -999,'\0'
      rlon=0.0
      rlat=0.0
      rt=0.0
      nlev=0
      write(iunito) id,curtclat,curtclon,rt,nlev,iflag

Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
C         
C         calc NOGAPS TC bogus profile from  mean r50 r30 
C
Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

      rad30=0.0
      do i=3,6
        rad30=rad30+tcstruct(i)
      end do
      rad30=rad30*0.25

      rad50=0.0
      do i=7,10
        rad50=rad50+tcstruct(i)
      end do
      rad50=rad50*0.25

      vmax=tcstruct(1)

      call ngptcbog(rad50,rad30,vmax,r,vtcngp,nr,
     $     rmaxngp,alphangp)
      
      if(verb) then
        print*,'SSSS ',vmax,rad50,rad30
        do i=1,nr
          write(*,'(f6.1,1x,f6.1)') r(i),vtcngp(i)
        end do
      endif

      do j=1,nq
        do i=1,nr
          vtcngpb(i,j)=vtcngp(i)
        end do
      end do

Caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
C         
C         calc structure parameters along each radial
C         
Caaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa


      tau=(nt-1)*dt

      if(nt.eq.1) then
        write(iunitd,'(a,2x,f4.1,a,f4.1)')
     $       'TC struct spdcrit = ',spdcrit,' and vcrit = ',vcrit

        write(iunitd,'(a,2x,f4.1,a,f6.3)')
     $       'NOGAPS TC bogus profile rmax = ',rmaxngp,' and alpha = ',alpha

        write(iunitd,'(a)')
     $       'Tau   Quad   Rinner  Router  Rvcrit   Varea  Rarea    Vmax   Rmax'

        write(*,'(a)')
     $       'Tau   Quad   Rinner  Router  Rvcrit   Varea  Rarea    Vmax   Rmax'

      else
        write(iunitd,'(a)') ' '
      endif

      do j=1,nq
        
        rinner=-999.0
        router=-999.0

        do i=1,nr

          wind=spd(i,j)
          wind=scb(i,j)
          if((wind.ge.spdcrit).and.(rinner.lt.0.0)) then
            rinner=r(i)
          endif

          if((wind.le.spdcrit).and.(rinner.gt.0.0).and.(router.lt.0.0)) then
            router=r(i)
          endif

        enddo

        rtcmin=-999.0

        do i=nr,1,-1
          vwind=vc(i,j)
          vwind=vcb(i,j)
          if((vc(i,j).gt.vcrit).and.(rtcmin.lt.0.0)) then
            rtcmin=r(i)
          endif
        end do

        if((router.lt.0.0).and.(rinner.gt.0.0)) router=r(nr)

        vsum=0.0
        asum=0.0
        modvmax=-999.0
        modrmax=-999.0

        do i=1,nr
          
          wind=spd(i,j)
          wind=scb(i,j)
          if(wind.gt.modvmax) then
            modvmax=wind
            modrmax=r(i)
          endif
          
          if(r(i).ge.rinner.and.r(i).le.router) then
            vsum=vsum+wind*r(i)*dr
            asum=asum+r(i)*dr
          endif

        enddo

        vbar=-999.0

        if(asum.gt.0.0) then
          vbar=vsum/asum
        endif

        if(verb) then
          write(*,'(a,4(f6.1,1x),2x,2(e13.5,1x),2x,f6.1,1x,f6.1)')
     $         'RRR parms: ',phi(j),rinner,router,rtcmin,vsum,asum,
     $         vbar,sqrt(asum)
        endif


        if(j.eq.1) quadname=' all ' 
        if(j.eq.2) quadname=' NEQ ' 
        if(j.eq.3) quadname=' SEQ ' 
        if(j.eq.4) quadname=' SWQ '
        if(j.eq.5) quadname=' NWQ '

        sqrtasum=-999.0
        if(asum.eq.0.0) asum=-999.0
        if(asum.gt.0.0) sqrtasum=sqrt(asum)

        write(iunitd,'(i3.3,2x,a,2x,8(f6.1,2x))')
     $       int(tau),quadname,rinner,router,rtcmin,vbar,sqrtasum,
     $       modvmax,modrmax

        write(*,'(i3.3,2x,a,2x,8(f6.1,2x))')
     $       int(tau),quadname,rinner,router,rtcmin,vbar,sqrtasum,
     $       modvmax,modrmax

      end do

         
C         
C         output the wind profiles :: mean and four quadrants for grads display        
C         

      write(iunitp) vcb
      write(iunitp) ucb
      write(iunitp) scb
      write(iunitp) vtcngpb

      deallocate (uc,stat=iflag)
      deallocate (vc,stat=iflag)
      deallocate (spd,stat=iflag)
      deallocate (r,stat=iflag)
      deallocate (phi,stat=iflag)
      deallocate (ur,stat=iflag)
      deallocate (vr,stat=iflag)
      deallocate (lat,stat=iflag)
      deallocate (lon,stat=iflag)
      deallocate (ucb,stat=iflag)
      deallocate (vcb,stat=iflag)
      deallocate (scb,stat=iflag)
      deallocate (dum1,stat=iflag)
      deallocate (dum2,stat=iflag)
      deallocate (vtcngp,stat=iflag)
      deallocate (vtcngpb,stat=iflag)

      deallocate (nb,stat=iflag)

      return
      end


      subroutine sumquad(uc,vc,nb,u,v,i,j,nr,nq)
      dimension uc(nr,nq),vc(nr,nq),nb(nq)
      uc(i,j)=uc(i,j)+u
      vc(i,j)=vc(i,j)+v
      nb(j)=nb(j)+1
      return
      end
          
      

      function rmag(u,v)
      rmag=sqrt(u*u+v*v)
      return
      end

