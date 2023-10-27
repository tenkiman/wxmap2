      MODULE ships_util
c-----7---------------------------------------------------------------72
c     This module contains the widely used constants in SHIPS and both
c      basic and SHIPS-related utility procedures.
c
c     Parameters:
c        rmiss, imiss
c     SHIPS procedures:
c        subroutine dlmw(plev,dw,ml)
c        subroutine stndz(p,z,t,theta)
c        subroutine tspdcal(tlat,tlon,ttime,mft,rmissval,cx,cy,cmag)
c     Utility procedures:
c      math/stat-
c        subroutine gaussj(a,n,np,b,m,mp)
c        subroutine moment(data1,n,ave,adev,sdev,var,skew,curt)
c        subroutine patch(f,rmissval,mft)
c        subroutine patchi(f,rmissval,mft)
c      coordinate conversion-
c        subroutine ctorh(x,y,r,theta)
c        subroutine rhtoc(r,thetah,x,y)
c        subroutine lltoxy(olon,olat,colat,tlon,tlat,xtem,ytem)
c        subroutine xytoll(olon,olat,colat,xtem,ytem,tlon,tlat)
c        subroutine llintp(f1,slon1,slat1,dlon1,dlat1,im1,jm1,i1,j1,
c                          f2,slon2,slat2,dlon2,dlat2,im2,jm2,i2,j2,
c                          izp,ierr)
c      time-
c        subroutine jdate(iyr,imon,iday,jday)
c        subroutine chartointmon(charmon,intmon)
c        subroutine tdiff(iy2,im2,id2,it2,iy1,im1,id1,it1,idelt)
c        subroutine yr2to4(iyr2,iyr4)
c      misc-
c        subroutine upcase(string,nchar)
c
c     Created:  15 Jul 2010 by Kate Musgrave
c     Modified: 16 Jul 2010 (KM) -general code update to Fortran 90
c               29 Oct 2010 (KM) -added subroutine patchi
c                                -modified subroutine patch
c-----7---------------------------------------------------------------72
c 
      IMPLICIT NONE
c 
      !the integer and real versions of missing data
c***      integer, parameter :: imiss = 9999
c***      real, parameter :: rmiss = 9999.
c 
      !physical constants and conversion factors
c 
c***      private, real, parameter :: pi = 3.14159265                                                    
c***      private, real, parameter :: dtr = pi/180.0                                                     
c                                                                        
c***      private, real, parameter :: dtk = 111.1                                                        
c                                                                        
c***      private, real, parameter :: erad = 6371.0                                                      
c***      private, real, parameter :: erot = 7.292E-5                                                    
c 
      CONTAINS
c
c***********************************************************************
c***********************************************************************
c
c     SHIPS utility procedures
c
c***********************************************************************
c 
c-----7---------------------------------------------------------------72
c     subroutine dlmw
c-----7---------------------------------------------------------------72
      SUBROUTINE dlmw(plev,dw,ml)
c     This subroutine calculates the deep-layer mean weights for a
c     given array of pressure levels.
c 
c     Input:
c       plev        - 1-D array containing the pressure levels (mb)
c       ml          - The number of pressure levels
c 
c     Output:
c       dw          - The weights for a mass-weighted average
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: ml
      real, dimension(ml), intent(in) :: plev
      real, dimension(ml), intent(out) :: dw
c 
      !list local variables
      real :: pdeep
      integer :: k      !counter
c 
      if (ml .eq. 1) then            !one pressure level
         dw(1) = 1.0
      else                           !more than one pressure level
         pdeep = plev(ml) - plev(1)
c 
         dw( 1) = 0.5*(plev(2)-plev(1))/pdeep
         dw(ml) = 0.5*(plev(ml)-plev(ml-1))/pdeep
c 
         if (ml .ne. 2) then         !if more than two pressure levels
            do k=2,ml-1
               dw(k) = 0.5*(plev(k+1)-plev(k-1))/pdeep
            enddo
         endif
c 
      endif
c 
      return
      END SUBROUTINE dlmw
c 
c-----7---------------------------------------------------------------72
c     subroutine stndz
c-----7---------------------------------------------------------------72
      SUBROUTINE stndz(p,z,t,theta)
c     This routine calculates the standard height z (m) from the
c     pressure p (mb). The temperature t (K) and potential temperature
c     theta (K) at p are also calculated.
c 
      IMPLICIT NONE
c 
      !list calling variables
      real, intent(in) :: p              !pressure (mb)
      real, intent(out) :: z             !standard height (m)
      real, intent(out) :: t             !temperature (K)
      real, intent(out) :: theta         !potential temperature (K)
c 
      !list local parameters and variables
      real, parameter :: g   = 9.80665
      real, parameter :: r   = 287.05
      real, parameter :: cp  = 1004.0
      real, parameter :: b   = 0.0065
      real, parameter :: p0  = 1013.25
      real, parameter :: t0  = 288.15
      real, parameter :: p00 = 1000.0
      real, parameter :: p1  = 226.32
      real, parameter :: t1  = 216.65
      real, parameter :: z1  = 11000.0
c 
      real :: cap, a
c 
      cap = r/cp
      a   = r*b/g
c  
      if (p .ge. p1) then
         z = (t0/b)*(1.0 - (p/p0)**a)
         t = t0 - b*z
      else
         z = z1 + (r*t1/g)*alog(p1/p)
         t = t1
      endif
c 
      theta = t*( (p00/p)**cap )
c 
      return
      END SUBROUTINE stndz
c 
c-----7---------------------------------------------------------------72
c     subroutine tspdcal
c-----7---------------------------------------------------------------72
      SUBROUTINE tspdcal(tlat,tlon,ttime,mft,rmissval,cx,cy,cmag)
c     This routine calculates the components of the storm
c     motion (cx,cy) in knots, given the lat/lon as a function
c     of time. Centered or one-sided differences are used as a appropriate.
c     Missing lat/lon points (equal to rmissval) are accounted for. 
c
c     This routine assumes lat is in degree N
c                          lon is in degree W positive
c     
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: mft        !maximum index value
      real, intent(in) ::    rmissval   !real missing value default
      real, dimension(-2:mft), intent(in) ::  tlat, tlon, ttime
                                        !lat, lon, time series
      real, dimension(-2:mft), intent(out) :: cx, cy, cmag
                                        !storm motion components, total
c
      !list local variables
      integer, parameter :: itmx=500 !max array size
      real, dimension(-3:itmx) :: ttlat, ttlon   !temp lat/lon arrays
      real ::    dtr, dtnmi          !conversion factors
      integer :: k                   !loop counter
      integer :: im, i0, ip, icode   !missing value flags
      real ::    dlat, dlon, dt      !change in lat, lon, time
      real ::    alat, cfac          !intermediate calculations
c
c     Check to make sure mft is not too big
      if (mft .gt. itmx) then
         write(6,*) 'mft too large in routine tspdcal, increase itmx'
         stop
      endif
c
c     Initialize variables to missing
      do k=-2,mft
         cx(k) =   rmissval
         cy(k) =   rmissval
         cmag(k) = rmissval
      enddo
c 
      do k=-3,itmx
         ttlat(k) = rmissval
         ttlon(k) = rmissval
      enddo     
c 
      dtnmi = 60.0
      dtr   = 3.14159/180.0
c 
      do k=-2,mft
         ttlat(k) =  tlat(k)
         ttlon(k) = -tlon(k)
      enddo
c 
      do 99 k=-2,mft
         im=0
         i0=0
         ip=0
         if (ttlat(k-1) .lt. rmissval) im=1
         if (ttlat(k  ) .lt. rmissval) i0=1
         if (ttlat(k+1) .lt. rmissval) ip=1
c 
         icode = ip + 10*i0 + 100*im
c 
         if (icode .eq. 101 .or. icode .eq. 111) then
c           Use centered differences
            dlat =     (ttlat(k+1)-ttlat(k-1))
            dlon =     (ttlon(k+1)-ttlon(k-1))
            dt   =     (ttime(k+1)-ttime(k-1))
            alat = 0.5*(ttlat(k+1)+ttlat(k-1))
            cfac = cos(dtr*alat)
c 
            cy(k) =      dtnmi*dlat/dt
            cx(k) = cfac*dtnmi*dlon/dt
            cmag(k) = sqrt(cx(k)**2 + cy(k)**2)
         elseif (icode .eq. 011) then
c           Use forward difference
            dlat =     (ttlat(k+1)-ttlat(k))
            dlon =     (ttlon(k+1)-ttlon(k))
            dt   =     (ttime(k+1)-ttime(k))
            alat = 0.5*(ttlat(k+1)+ttlat(k))
            cfac = cos(dtr*alat)
c 
            cy(k) =      dtnmi*dlat/dt
            cx(k) = cfac*dtnmi*dlon/dt
            cmag(k) = sqrt(cx(k)**2 + cy(k)**2)
         elseif (icode .eq. 110) then
c           Use backward difference
            dlat =     (ttlat(k)-ttlat(k-1))
            dlon =     (ttlon(k)-ttlon(k-1))
            dt   =     (ttime(k)-ttime(k-1))
            alat = 0.5*(ttlat(k)+ttlat(k-1))
            cfac = cos(dtr*alat)
c 
            cy(k) =      dtnmi*dlat/dt
            cx(k) = cfac*dtnmi*dlon/dt
            cmag(k) = sqrt(cx(k)**2 + cy(k)**2)
         else
c           Two of three points are missing. Can not calculate speed components
            cx(k) = rmissval
            cy(k) = rmissval
            cmag(k) = rmissval
         endif
c        write(6,888) k*6,ttlat(k),ttlon(k),cx(k),cy(k)
c 888    format('t,lat,lon,cx,cy: ',i4,1x,4(f8.1,1x))
   99 continue
c 
      return
      END SUBROUTINE tspdcal
c 
c***********************************************************************
c***********************************************************************
c
c     basic utility procedures
c
c***********************************************************************
c-----7---------------------------------------------------------------72
c
c     mathematics/statistics utility procedures
c
c-----7---------------------------------------------------------------72
c 
c-----7---------------------------------------------------------------72
c     subroutine gaussj
c-----7---------------------------------------------------------------72
      SUBROUTINE gaussj(a,n,np,b,m,mp)
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: n, np, m, mp
      real, dimension(np,np), intent(inout) :: a
      real, dimension(np,mp), intent(inout) :: b
c 
      !list local variables
      integer, parameter :: nmax=50
      integer :: i, j, k, l, ll      !counters
      integer :: irow, icol
      real :: big, dum, pivinv
      integer, dimension(nmax) :: ipiv, indxr, indxc
c 
      do j=1,n
        ipiv(j)=0
      enddo
c 
      do 22 i=1,n      !begin large do loop
c 
         big = 0.
         do j=1,n
            if (ipiv(j) .ne. 1) then
               do k=1,n
                  if (ipiv(k) .eq. 0) then
                     if (abs(a(j,k)) .ge. big) then
                        big = abs(a(j,k))
                        irow = j
                        icol = k
                     endif
                  elseif (ipiv(k) .gt. 1) then
                     PAUSE 'Singular matrix'
                  endif
               enddo
            endif
         enddo
c 
         ipiv(icol) = ipiv(icol)+1
         if (irow .ne. icol) then
            do l=1,n
               dum = a(irow,l)
               a(irow,l) = a(icol,l)
               a(icol,l) = dum
            enddo
            do l=1,m
               dum = b(irow,l)
               b(irow,l) = b(icol,l)
               b(icol,l) = dum
            enddo
         endif
c 
         indxr(i) = irow
         indxc(i) = icol
         if (a(icol,icol) .eq. 0.) PAUSE 'Singular matrix.'
         pivinv = 1./a(icol,icol)
         a(icol,icol) = 1.
         do l=1,n
            a(icol,l) = a(icol,l)*pivinv
         enddo
         do l=1,m
            b(icol,l) = b(icol,l)*pivinv
         enddo
c 
         do ll=1,n
            if (ll .ne. icol) then
               dum = a(ll,icol)
               a(ll,icol) = 0.
               do l=1,n
                  a(ll,l) = a(ll,l)-a(icol,l)*dum
               enddo
               do l=1,m
                  b(ll,l) = b(ll,l)-b(icol,l)*dum
               enddo
            endif
         enddo
c 
22    continue      !end large do loop
c 
      do l=n,1,-1
         if (indxr(l) .ne. indxc(l)) then
            do k=1,n
               dum = a(k,indxr(l))
               a(k,indxr(l)) = a(k,indxc(l))
               a(k,indxc(l)) = dum
            enddo
         endif
      enddo
c 
      return
      END SUBROUTINE gaussj
c 
c-----7---------------------------------------------------------------72
c     subroutine moment
c-----7---------------------------------------------------------------72
      SUBROUTINE moment(data1,n,ave,adev,sdev,var,skew,curt)
c Given an array of DATA1 of length N, this routine returns its mean AVE,
c average deviation ADEV, standard deviation SDEV, variance VAR, 
c skewness SKEW, and kurtosis CURT
c 
      IMPLICIT NONE
c 
      !list calling variables
      INTEGER, INTENT(IN) :: n
      REAL, DIMENSION(n), INTENT(IN) :: data1
      REAL, INTENT(OUT) :: adev,ave,curt,sdev,skew,var
c
      !list local variables
      INTEGER j
      REAL p,s,ep
c 
      if(n.le.1)pause 'n must be at least 2 in moment'
c
c First pass to get the mean
      s=0.
      do 11 j=1,n
        s=s+data1(j)
11    continue
      ave=s/n
c
c Second pass to get the first (absolute), second, third, and fourth
c moments of the deviation from the mean
      adev=0.
      var=0.
      skew=0.
      curt=0.
      ep=0.
      do 12 j=1,n
        s=data1(j)-ave
        ep=ep+s
        adev=adev+abs(s)
        p=s*s
        var=var+p
        p=p*s
        skew=skew+p
        p=p*s
        curt=curt+p
12    continue
      adev=adev/n
      var=(var-ep**2/n)/(n-1)
      sdev=sqrt(var)
c 
      if(var.ne.0.)then
        skew=skew/(n*sdev**3)
        curt=curt/(n*var**2)-3.
      else	
	pause 'no skew or kurtosis when zero variance in moment'
      endif
c      
      return
      END SUBROUTINE moment
c 
c-----7---------------------------------------------------------------72
c     subroutine patch
c-----7---------------------------------------------------------------72
      SUBROUTINE patch(f,rmissval,mft)
c     This routine fills in missing values of f
c     using interpolation or extrapolation. 
c     The version is for a 1D real array
c 
      IMPLICIT NONE
c 
      ! list calling variables
      integer, intent(in) :: mft                   !length-1 of 1D array
      real, dimension(0:mft), intent(inout) :: f   !1D array
      real, intent(in) ::    rmissval              !real missing value
c 
      !list local variables
      integer :: k, kk              !looping counters
      integer :: ifwd, ibwd         !forward/backward indices
      real ::    ffwd, fbwd         !forward/backward values of f
      real ::    tnow, tfwd, tbwd   !real values of indices
      real ::    wtbwd, wtfwd       !weights for interpolation
c 
      do k=0,mft
         if (f(k) .ge. rmissval) then
c 
c           Search forward for good data
            ifwd = -99
            if (k .lt. mft) then
               do kk=k+1,mft
                  if (f(kk) .lt. rmissval) then
                     ifwd=kk
                     ffwd=f(kk)
                     go to 1020
                  endif
               enddo
            endif
 1020       continue
c
c           Search backward for good data
            ibwd = -99
            do kk=k-1,0,-1
               if (f(kk) .lt. rmissval) then
                  ibwd=kk
                  fbwd=f(kk)
                  go to 1030
               endif
            enddo
 1030       continue
c 
c           Alter missing value (extrapolate or interpolate)
            if     (ibwd .gt. -99 .and. ifwd .eq. -99) then
c              Extrapolate forward
               f(k) = fbwd
            elseif (ibwd .eq. -99 .and. ifwd .gt. -99) then
c              Extrapolate backward
               f(k) = ffwd
            elseif (ibwd .gt. -99 .and. ifwd .gt. -99) then
c              Interpolate
               tnow = float(k)
               tbwd = float(ibwd)
               tfwd = float(ifwd)
c 
               wtbwd = (tfwd-tnow)/(tfwd-tbwd)
               wtfwd = (tnow-tbwd)/(tfwd-tbwd)
c 
               f(k) = wtbwd*fbwd + wtfwd*ffwd
            endif
         endif
      enddo
c 
      return
      END SUBROUTINE patch
c 
c-----7---------------------------------------------------------------72
c     subroutine patchi
c-----7---------------------------------------------------------------72
      SUBROUTINE patchi(f,rmissval,mft)
c     This routine fills in missing values of f using interpolation
c     only.  Missing values at beginning or end of array are left alone.
c     The version is for a 1D real array
c 
      IMPLICIT NONE
c 
      ! list calling variables
      integer, intent(in) :: mft                   !length-1 of 1D array
      real, dimension(0:mft), intent(inout) :: f   !1D array
      real, intent(in) ::    rmissval              !real missing value
c 
      !list local variables
      integer :: k, kk              !looping counters
      integer :: ifwd, ibwd         !forward/backward indices
      real ::    ffwd, fbwd         !forward/backward values of f
      real ::    tnow, tfwd, tbwd   !real values of indices
      real ::    wtbwd, wtfwd       !weights for interpolation
c 
      do k=0,mft
         if (f(k) .ge. rmissval) then
c 
c           Search forward for good data
            ifwd = -99
            if (k .lt. mft) then
               do kk=k+1,mft
                  if (f(kk) .lt. rmissval) then
                     ifwd=kk
                     ffwd=f(kk)
                     go to 1020
                  endif
               enddo
            endif
 1020       continue
c
c           Search backward for good data
            ibwd = -99
            do kk=k-1,0,-1
               if (f(kk) .lt. rmissval) then
                  ibwd=kk
                  fbwd=f(kk)
                  go to 1030
               endif
            enddo
 1030       continue
c 
c           Alter missing value (interpolate only)
            if (ibwd .gt. -99 .and. ifwd .gt. -99) then
c              Interpolate
               tnow = float(k)
               tbwd = float(ibwd)
               tfwd = float(ifwd)
c 
               wtbwd = (tfwd-tnow)/(tfwd-tbwd)
               wtfwd = (tnow-tbwd)/(tfwd-tbwd)
c 
               f(k) = wtbwd*fbwd + wtfwd*ffwd
            endif
         endif
      enddo
c 
      return
      END SUBROUTINE patchi
c 
c-----7---------------------------------------------------------------72
c
c     coordinate conversion utility procedures
c
c-----7---------------------------------------------------------------72
c 
c-----7---------------------------------------------------------------72
c     subroutine ctorh
c-----7---------------------------------------------------------------72
      SUBROUTINE ctorh(x,y,r,theta)
c     This routine converts from Cartesion coordinates
c     to radial coordinates, where theta is in
c     degrees measured clockwise from
c     the +y-axis (standard meteorological heading).
c 
      IMPLICIT NONE
c 
      !list calling variables
      real, intent(in) :: x, y         !cartesian coordinates
      real, intent(out) ::  r, theta   !radial coordinates
c
      !list local variables
      real :: rtd   !radians to degrees conversion factor
c 
      r = sqrt(x*x + y*y)
c 
      if (r .le. 0.0) then
         theta = 0.0
         return
      endif
c 
      rtd = 57.296
      theta = rtd*acos(x/r)
      if (y .lt. 0.0) theta = 360.0 - theta
c
c     Convert theta to heading
      theta = 90.0 - theta
      if (theta .lt. 0.0) theta = theta + 360.0
c 
      return
      END SUBROUTINE ctorh
c 
c-----7---------------------------------------------------------------72
c     subroutine rhtoc
c-----7---------------------------------------------------------------72
      SUBROUTINE rhtoc(r,thetah,x,y)
c     This routine converts from radial coordinates
c     to Cartesian coordinates, where theta is in
c     degrees measured clockwise from
c     the +y-axis (standard meteorological heading).
c 
      IMPLICIT NONE
c 
      !list calling variables
      real, intent(in) ::  r, thetah   !radial coordinates
      real, intent(out) :: x, y        !cartesian coordinates
c
      !list local variables
      real :: theta   !converted theta
      real :: rtd     !radians to degrees conversion factor
c
c     Convert theta from heading to standard definition
      theta = 90.0 - thetah
      if (theta .lt. 0.0) theta = theta + 360.0
c 
      rtd = 57.296
      x = r*cos(theta/rtd)
      y = r*sin(theta/rtd)
c 
      return
      END SUBROUTINE rhtoc
c 
c-----7---------------------------------------------------------------72
c     subroutine lltoxy
c-----7---------------------------------------------------------------72
      SUBROUTINE lltoxy(olon,olat,colat,tlon,tlat,xtem,ytem)             
c     This routine calculates the x,y coordinates (xtem,ytem) of the     
c     point with longitude and latitude tlon,tlat relative to a          
c     coordinate system with origin at olon,olat.  In the current        
c     version, a simple tangent plane approximation is used for the      
c     transformation.                                                    
c 
      IMPLICIT NONE
c 
      !list calling variables
      real, intent(in) ::  olon, olat, colat, tlon, tlat
      real, intent(out) :: xtem, ytem
c 
      !list local variables
      real, parameter :: dtk = 111.1
c                                                                        
      xtem = dtk*(tlon-olon)*colat                                       
      ytem = dtk*(tlat-olat)                                             
c                                                                        
      return                                                             
      END SUBROUTINE lltoxy
c 
c-----7---------------------------------------------------------------72
c     subroutine xytoll
c-----7---------------------------------------------------------------72
      SUBROUTINE xytoll(olon,olat,colat,xtem,ytem,tlon,tlat)
c     This routine calculates the longitude and latitude tlon,tlat
c     of the point with x,y coordinates xtem,ytem
c     relative to a coordinate system with origin at
c     olon,olat.  In the current version, a simple tangent plane
c     approximation is used for the transformation.
c 
      IMPLICIT NONE
c 
      !list calling variables
      real, intent(in) ::  olon, olat, colat, xtem, ytem
      real, intent(out) :: tlon, tlat
c 
      !list local variables
      real, parameter :: dtk = 111.1
c 
      tlon = olon + xtem/(dtk*colat)
      tlat = olat + ytem/(dtk)
c 
      return
      END SUBROUTINE xytoll
c 
c-----7---------------------------------------------------------------72
c     subroutine llintp
c-----7---------------------------------------------------------------72
      SUBROUTINE llintp(f1,slon1,slat1,dlon1,dlat1,im1,jm1,i1,j1,
     +                  f2,slon2,slat2,dlon2,dlat2,im2,jm2,i2,j2,
     +                  izp,ierr)
c
c     This routine linearly interpolates f1 on an evenly spaced
c     lat,lon grid to obtain f2 on a different lat,lon grid. 
c     The subroutine arguments are defined as follows:
c
c     f1(im1,jm1):  Contains the function to be interpolated. The
c                   first index represents longitude (increasing
c                   eastward) and the second index represents 
c                   latitude (increasing northward).
c
c     f2(im2,jm2):  The interpolated function with indices defined 
c                   the same as for f1.
c
c     slon1         The first longitude of f1 (deg E positive)
c     slat1         The first latitude  of f1 (deg N positive)
c     dlon1         The longitude increment of f1 (deg)
c     dlat1         The latitude  increment of f1 (deg)
c     slon2         The first longitude of f2 (deg E positive)
c     slat2         The first latitude  of f2 (deg N positive)
c     dlon2         The longitude increment of f2 (deg)
c     dlat2         The latitude  increment of f2 (deg)
c
c     im1,jm1       The dimensions of f1
c     im2,jm2       The dimensions of f2
c
c     i1,j1         The number of longitude,latitude points of f1
c                   to use in the interpolation
c     i2,j2         The number of longitude,latitude points of f2
c                   to interpolate
c
c     izp           Zonal Periodic flag: 
c                       =1 when f1 is periodic in the zonal direction
c                          (normally used only when f1 spans 360 deg
c                          of longitue)
c                       =0 if not periodic
c
c     ierr          Error flag: =0 for normal return
c                               =1 if f2 domain exceeds f1 domain
c                                  (non fatal)
c                               =2 if indices i1,j1 or i2,j2 exceed
c                                  dimension of f1 or f2 (fatal) 
c                               =3 if dlon or dlat .le. 0.0 (fatal) 
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: im1, jm1, im2, jm2, i1, j1, i2, j2
      real, dimension(im1,jm1), intent(in) :: f1
      real, dimension(im2,jm2), intent(out) :: f2
      real, intent(in) :: dlon1, dlat1, dlon2, dlat2
      real, intent(in) :: slon1, slat1, slon2, slat2
      integer, intent(in) :: izp
      integer, intent(out) :: ierr
c 
      !list local variables
      integer :: i, j, i00, j00
      real :: pi, dtr, erad, adtr
      real :: rlonn1, rlonx1, rlatn1, rlatx1
      real :: rlon, rlat, rlon00, rlat00
      real :: f00, f01, f10, f11
      real :: dx0, dx1, dy, x, y, a, b, c, d
c 
c     Initialize error flag
      ierr=0
c 
c     Check indices and dlat,dlon
      if (i1 .gt. im1  .or.  j1 .gt. jm1  .or. 
     +    i2 .gt. im2  .or.  j2 .gt. jm2)  then
          ierr=2
          return
      endif
c 
      if (dlat1 .le. 0.0 .or. dlon1 .le. 0.0 .or.
     +    dlat2 .le. 0.0 .or. dlon2 .le. 0.0) then
         ierr=3
         return
      endif
c 
c     Specify needed constants
      pi   = 3.14159265
      dtr  = pi/180.0
      erad = 6371.0
      adtr = erad*dtr
c 
c     Calculate min and max long,lat of f1 domain
      rlonn1 = slon1
      rlonx1 = slon1 + dlon1*float(i1-1)
      rlatn1 = slat1
      rlatx1 = slat1 + dlat1*float(j1-1)
c 
c     Start loop for f2 points
      do 10 j=1,j2
      do 10 i=1,i2
         rlon = slon2 + dlon2*float(i-1)
         rlat = slat2 + dlat2*float(j-1)
c 
c        Check if current f2 point is outside of f1 domain.
c        If yes, move the f2 point to the nearest point in the
c        f1 domain and set error flag. 
c 
         if (izp .ne. 1) then
c           Adjust f2 longitude for case without zonal periodicity
            if (rlon .gt. rlonx1) then
               rlon = rlonx1
               ierr=1
            endif
c 
            if (rlon .lt. rlonn1) then
               rlon = rlonn1
               ierr=1
            endif
         else
c           Zonal periodic case
            if (rlon .ge. 360.0) rlon=rlon-360.0
         endif
c 
         if (rlat .gt. rlatx1) then
            rlat = rlatx1
            ierr=1
         endif
c 
         if (rlat .lt. rlatn1) then
            rlat = rlatn1
            ierr=1
         endif
c 
c        Find the indices of the f1 point closest to,
c        but with lon,lat less than the current f2 point.
         i00 = 1 + ifix( (rlon-rlonn1)/dlon1 )
         j00 = 1 + ifix( (rlat-rlatn1)/dlat1 )
         if (i00 .lt.    1)    i00=   1
         if (izp .ne. 1) then
            if (i00 .gt. i1-1) i00=i1-1
         endif
         if (j00 .lt.    1)    j00=   1
         if (j00 .gt. j1-1)    j00=j1-1
c 
c        Define the four f1 values to be used in the linear
c        interpolation.
         f00 = f1(i00  ,j00  )
         f01 = f1(i00  ,j00+1)
c 
         if (izp .eq. 1 .and. i00 .eq. i1) then
            f10 = f1(    1,j00  )
            f11 = f1(    1,j00+1)
         else
            f10 = f1(i00+1,j00  )
            f11 = f1(i00+1,j00+1)
         endif
c 
c        Calculate the lon,lat of the point i00,j00
         rlon00 = rlonn1 + dlon1*float(i00-1)
         rlat00 = rlatn1 + dlat1*float(j00-1)
c 
c        Calculate the x,y distances between the four f1 points
c        where x,y = 0,0 at i00,j00
         dx0 = dlon1*adtr*cos( dtr*(rlat00        ) )
         dx1 = dlon1*adtr*cos( dtr*(rlat00 + dlat1) )
         dy  = dlat1*adtr 
c 
c        Calculate the x,y coordinates of the current f2 point
         x = adtr*(rlon-rlon00)*cos(dtr*rlat)
         y = adtr*(rlat-rlat00)
c
c        Calculate the coefficients for the linear interpolation
         a = f00
         b = (f10-f00)/dx0
         c = (f01-f00)/dy
         d = (f11 - f00 - b*dx1 - c*dy)/(dx1*dy)
c 
c        Perform interpolation and then go to the next f2 point
         f2(i,j) = a + b*x + c*y + d*x*y
   10 continue
c 
      return
      END SUBROUTINE llintp
c 
c-----7---------------------------------------------------------------72
c
c     time-based utility procedures
c
c-----7---------------------------------------------------------------72
c-----7---------------------------------------------------------------72
c     subroutine jdate
c-----7---------------------------------------------------------------72
      SUBROUTINE jdate(iyr,imon,iday,jday)
c     This routine calculates the Julian date
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) ::  iyr, imon, iday   !Year, Month, Day
      integer, intent(out) :: jday              !Julian day
c
      !list local variables
      integer, dimension(12) :: idmon   !total # of days before month
c 
      idmon = (/0,31,59,90,120,151,181,212,243,273,304,334/)
c 
      jday = idmon(imon) + iday
      if (mod(iyr,4) .eq. 0 .and. imon .gt. 2) jday=jday+1
c 
      return
      END SUBROUTINE jdate
c-----7---------------------------------------------------------------72
c     subroutine chartointmon
c-----7---------------------------------------------------------------72
      SUBROUTINE chartointmon(charmon,intmon)
c     This subroutine takes a 3-character abbreviation for month and
c      turns it into the corresponding integer value for that month.
c
c     Error condition: returns intmon=0 if non-valid charmon provided
c 
      IMPLICIT NONE
c 
      !list calling variables
      character(3), intent(in) :: charmon     !character month
      integer, intent(out) ::     intmon      !integer month
c      
      select case (charmon)
      case ('JAN')
         intmon=1
      case ('FEB')
         intmon=2
      case ('MAR')
         intmon=3
      case ('APR')
         intmon=4
      case ('MAY')
         intmon=5
      case ('JUN')
         intmon=6
      case ('JUL')
         intmon=7
      case ('AUG')
         intmon=8
      case ('SEP')
         intmon=9
      case ('OCT')
         intmon=10
      case ('NOV')
         intmon=11
      case ('DEC')
         intmon=12
      case default
         intmon=0
      end select
c 
      return     
      END SUBROUTINE chartointmon
c
c-----7---------------------------------------------------------------72
c     subroutine tdiff
c-----7---------------------------------------------------------------72
      SUBROUTINE tdiff(iy2,im2,id2,it2,iy1,im1,id1,it1,idelt)
c     This routine calculates the number of hours (delt) between
c     two date/times.
c
c     Note: Times are in hours
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: iy2, im2, id2, it2   !time 2
      integer, intent(in) :: iy1, im1, id1, it1   !time 1
      integer, intent(out) :: idelt               !time2-time1 (in hrs)
c
      !list local variables
      integer :: i            !counter
      integer :: iry          !reference year
      integer :: ity1, ity2   !total hrs from reference year to time1,2
      integer, dimension(12) :: nday   !total # of days before month
c 
      nday = (/0,31,59,90,120,151,181,212,243,273,304,334/)
c
c     Calculate reference year
      iry = iy1-2
      if (iy2 .lt. iry) iry=iy2-2
c
c     Calculate the number of hours from 00 Jan. 1 of the reference year
      ity1 = 0
      do 10 i=iry,iy1-1
         if (mod(i,4) .eq. 0) then
            ity1 = ity1 + 24*366
         else
            ity1 = ity1 + 24*365
         endif
   10 continue
c 
      ity2 = 0
      do 15 i=iry,iy2-1
         if (mod(i,4) .eq. 0) then
            ity2 = ity2 + 24*366
         else
            ity2 = ity2 + 24*365
         endif
   15 continue
c 
      ity1 = ity1 + 24*nday(im1)
      if ((mod(iy1,4) .eq. 0) .and. im1 .gt. 2) ity1=ity1+24
c 
      ity2 = ity2 + 24*nday(im2)
      if ((mod(iy2,4) .eq. 0) .and. im2 .gt. 2) ity2=ity2+24
c 
      ity1 = ity1 + 24*id1 + it1
      ity2 = ity2 + 24*id2 + it2
c 
      idelt = ity2 - ity1
c 
      return
      END SUBROUTINE tdiff
c 
c-----7---------------------------------------------------------------72
c     subroutine yr2to4
c-----7---------------------------------------------------------------72
      SUBROUTINE yr2to4(iyr2,iyr4)
c     This routine calculates the 4-digit year from a provided 2-digit
c     year, based on the assumption that all years <=50 are in the 
c     2000s, and all years >50 are in the 1900s.
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: iyr2
      integer, intent(out) :: iyr4
c 
      if (iyr2 .gt. 50) then
         iyr4 = iyr2 + 1900
      else
         iyr4 = iyr2 + 2000
      endif
c 
      return
      END SUBROUTINE yr2to4
c  
c-----7---------------------------------------------------------------72
c
c     miscellaneous utility procedures
c
c-----7---------------------------------------------------------------72
c 
c-----7---------------------------------------------------------------72
c     subroutine upcase
c-----7---------------------------------------------------------------72
      SUBROUTINE upcase (string,nch)
c     This routine converts all lower case characters (ascii 97 - 122)
c     in the variable string to upper case characters (ascii 65 - 90).
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: nch
      character, dimension(*), intent(inout) :: string
c 
      !list local variables
      integer :: i, ich
c 
c     loop thru each character in the string
      do i=1,nch
         ich = ichar(string(i))
c 
c     if it is lower case, subtract 32 from it to make it upper case.
         if ((ich .gt. 96) .and. (ich .lt. 123)) 
     +      string(i:i) = char(ichar(string(i:i))-32)
      enddo
c 
      return
      END SUBROUTINE upcase
c 
      END MODULE ships_util
