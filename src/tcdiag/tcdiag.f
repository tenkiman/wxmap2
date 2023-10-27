      subroutine tcdiag(mx,my,mp,us,vs,ps,rlon,rlat,slat,slon,rmiss,
     +                  outfile)
      integer :: nx,ny,np
c       ++ Basic model fields and coordinates
      dimension us(mx,my,mp),vs(mx,my,mp),ps(mx,my,mp)

c       ++Cylindrical grid variables (Note: mpl must be .ge. mp)
      parameter (mr=150,mt=16,mpl=1)
      dimension r(0:mr),theta(0:mt)
      dimension xrt(0:mr,0:mt),yrt(0:mr,0:mt)
      dimension sinth(0:mt),costh(0:mt)
c
c       ++Arrays for interpolating fields to the cylindrical grid
      dimension uc(0:mr,0:mt,0:mpl),vc(0:mr,0:mt,0:mpl)
      dimension urc(0:mr,0:mt,0:mpl),vtc(0:mr,0:mt,0:mpl),
     +          wc(0:mr,0:mt,0:mpl), pc(0:mr,0:mt,0:mpl)
      dimension urca(0:mr,0:mpl),vtca(0:mr,0:mpl),wca(0:mr,0:mpl),
     +          pca(0:mr,0:mpl)
c
      dimension usc(0:mr,0:mt,mpl),vsc(0:mr,0:mt,mpl),
     +          psc(0:mr,0:mt,mpl)
      character(len=*) outfile

c
c     Set defaults
      ierr = 0
      nx = mx
      ny = my
      np = mp
c
c     ** Begin specification of diagnostic calculation parameters

c        ++ Cylindrical grid parameters (r0, dr in km, dtheta (dt) in deg, +x axis is east)
c           nr,nt = number of radial and azimuthal grid intervals.
c           Note: dr should be .le. model grid spacing, radial domain should extend to at
c                 least 1000 km.
         nr=150
         nt=8
         r0=0.0
         dr=10.0
         dt=360.0/float(nt)
c
c     ** End specification of diagnostic calculation parameters
c
c     Specify physical and numerical constants
      pi = 3.14159265
      dtr = pi/180.0
      cctk = 273.15
      cmtk = 1.944
c
c     Calculate cylindrical grid info (r in km, theta in deg, +x axis is east)
      call cgcal(mr,mt,nr,nt,dr,dt,r0,dtr,r,theta,xrt,yrt,sinth,costh)
c
c     Calculate parameters to convert between lat/lon and storm-centered
c     cylindrical grid. These must be recalculated if storm center is moved.
      call gridcon(mx,my,nx,ny,rlon,rlat,slon,slat,dtr,
     +             dlon,dlat,dx,dy,glon1,glat1,xg1,yg1)
c
c     Interpolate 2D model fields to cylindrical grid
!      call lltocg2(us,usc,mx,my,nx,ny,mr,mt,nr,nt,
!     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
!      call lltocg2(vs,vsc,mx,my,nx,ny,mr,mt,nr,nt,
!     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(us,usc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(vs,vsc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(ps,psc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)

c
c     Calculate radial and tangential winds
      call uvtort(usc,vsc,sinth,costh,mr,mt,mp,nr,nt,np,urc,vtc,rmiss)
c
c     Azimuthally average radial and tangential winds
!      call azavg3(urc,urca,mr,mt,1,nr,nt,1,rmiss)
      call azavg3(vtc,vtca,mr,mt,1,nr,nt,1,rmiss)
      call wndspd(urc,vtc,wc,mr,mt,mp,nr,nt,np,rmiss)
      call azavg3(wc,wca,mr,mt,mp,nr,nt,np,rmiss)
      call azavg3(psc,pca,mr,mt,mp,nr,nt,np,rmiss)

      open(unit=3, file=outfile, form='formatted', action='write',
     +     status='unknown')
      do i=0,nr
          if ( wca(i,0) .ne. rmiss ) then

              write(3,*) r(i), ',' , wca(i,0), ',' , vtca(i,0), ',' ,
     +                  pca(i,0)
          end if
      end do
      end


