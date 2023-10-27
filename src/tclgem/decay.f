      subroutine decay(ftime,rlat,rlon,vmax,vmaxa,dland,lulg)
C 
C     This routine adjusts a tropical cyclone intensity 
C     forecast to account for decay over land. this version is
C     valid for the atlantic basin and was written by M. DeMaria
C     and J. Kaplan of the Hurricane Research Division, May 1994.
C 
C     This version was modified 4/10/97 (MDM) to include the 
C     New England coefficients. The distance inland correction
C     is disabled in this version (idtlc=0). 
C 
C     New version created 9/30/2004 that allows for decay proportional
C     to the fraction of the storm circulation over land.
C     (Set rcrad > 0.0 to activate this option). The logic of the code
c     was changed so accomodate this option. The old distance inland
c     correction was completely eliminated with this modification. 
C 
C     ********** INPUT **********
C 
C       ftime: the time in hours (for example, 0.,12.,24. ... 72.)
C              The times need to sequential, but the time interval
C              does not need to be even. 
C       rlat:  The storm latitude (deg n) at the times in array ftime
C       rlon:  The storm longitude (deg w positive) at the times in
C              array ftime
C       vmax:  The storm maximum wind (kt) at the times in array ftime.
C              Set vmax=0 for missing forecast times. 
C       lulg:  Unit number for write statements
C 
C     ********** OUTPUT **********  
C 
C       vmaxa: The storm maximum wind (kt) adjusted for decay over land
C              at the times in array ftime.
C 
C       dland: The distance (km) from the storm center (rlat,rlon) to 
C              the nearest major land mass. dland is negative if the 
C              point is storm center is inland.
C 
C     ********** METHOD *********
C 
C     The simple exponential decay model developed by M. DeMaria 
C     and J. Kaplan at HRD is used to decay the storm intensity for
C     the portions of the track over land.
C 
C     In this version, the decay rate is proportional to the fraction
C     of the storm circualtion over land. 
C 
C     ********** PARAMETER SPECIFICATION **********
C 
C     Specify the maximum number of time values.
      parameter (imax=21)
C 
C     Specify the time interval (hr) for linearly interpolating 
C     the track positions.
      data dt /1.00/
C 
C     Set interp=1 to print out (to unit lulg) all intermediate 
C     intensity calculations or else set interp=0 for no print 
      data interp /1/ 
C 
C     Specify decay model parameters
C 
C     Coefficients for east/gulf coast
      data rf1,a1,vb1,rclat1 /0.9,0.095,26.7,36.0/
C     
C     Coefficients for New England
      data rf2,a2,vb2,rclat2 /0.9,0.183,29.6,40.0/
C 
C     Specify radius of storm circulation (km) for fractional
C     decay option. Set rcrad to zero to eliminate this option. 
C 
      data rcrad / 110.0/
c     data rcrad /   0.0/
c 
      common /mparm/ alpha,vb,redfac
C 
C     ********** DIMENSION ARRAYS **********
C 
      dimension ftime(imax),rlat(imax),rlon(imax)
      dimension vmax(imax),vmaxa(imax),dland(imax)
C 
c     Arrays for small time step
      parameter (imaxs=1000)
      dimension ftimes(imaxs),rlats(imaxs),rlons(imaxs)
      dimension vmaxs(imaxs),vmaxas(imaxs)
      dimension dlands(imaxs),flands(imaxs)
c 
C     ********** MODEL CODE *********
C 
C     Write model message to log file
      if (interp .gt. 0) then
         write(lulg,810) rcrad
  810    format(' Decay model with rcrad= ',f5.0,' km')
      endif
C 
c     Initialize vmaxa array to zero
      do i=1,imax
	 vmaxa(i) = 0.0
      enddo
c 
C     Find the number of valid forecast times
      itimet = 0
      do 10 i=1,imax
         if (vmax(i) .lt. 0.5) go to 1000
         itimet=i 
   10 continue
C 
 1000 continue
C     There must be at least two valid forecast times
      if (itimet .lt. 2) return
C 
C     Check to make sure times are sequential
      itime=0
      do 15 i=2,itimet
         if (ftime(i) .le. ftime(i-1)) go to 1100
         itime=i
   15 continue
C 
 1100 continue
      if (itime .lt. 2) return
c         
      if (interp .gt. 2) then
         do i=1,itime
            write(6,887) ftime(i),rlat(i),rlon(i),vmax(i)
         enddo
      endif
c 
c     Calcuate the time values at the small time interval points
      ntimes = 1 + (ftime(itime)-ftime(1))/dt
      do i=1,ntimes
	 ftimes(i) = ftime(1) + dt*float(i-1)
      enddo
c 
c     Interpolate the input lat,lon and max winds to the 
c     small time interval
c 
c       ++Find vmax on small time grid
      iflag=1
      lflag=0
      xi = 0.0
c 
      call xint(ftime,vmax,itime,iflag,lflag,xi,fi,ierr)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,vmax,itime,iflag,lflag,
     +                  ftimes(i),vmaxs(i),ierr)
      enddo
c 
c       ++Find lat on small time grid
      iflag=1
      call xint(ftime,rlat,itime,iflag,lflag,xi,fi,ierr)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,rlat,itime,iflag,lflag,
     +                  ftimes(i),rlats(i),ierr)
      enddo
c 
c       ++Find lon on small time grid
      iflag=1
      call xint(ftime,rlon,itime,iflag,lflag,xi,fi,ierr)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,rlon,itime,iflag,lflag,
     +                  ftimes(i),rlons(i),ierr)
      enddo
c 
c     Calcuate distance to land and fractional land at small time points
      do i=1,ntimes
         call aland(-rlons(i),rlats(i),dlands(i))
	 call fland(-rlons(i),rlats(i),rcrad,flands(i))
      enddo
c 
c     Integrate the decay model over the small time points
      do i=1,ntimes
	 if (rcrad .gt. 0.0) then
	    call fland(-rlons(i),rlats(i),rcrad,flands(i))
         else
	    flands(i) = 1.0
         endif
      enddo
c 
      vmaxas(1) = vmaxs(1)
c 
      do i=2,ntimes
c        At each step in this loop, the decay model is integrated
c        from t=ftimes(i-1) to t=ftimes(i)
c 
c        Calculate decay model parameters at current latitude
         rlatt = rlats(i-1)
         if     (rlatt .ge. rclat2) then
             redfac = rf2
             alpha  = a2
             vb     = vb2
         elseif (rlatt .le. rclat1) then 
             redfac = rf1
             alpha  = a1
             vb     = vb1
         else
             w1 = (rclat2-rlatt)/(rclat2-rclat1)
             w2 = (rlatt-rclat1)/(rclat2-rclat1)
C 
             redfac = w1*rf1 + w2*rf2
             alpha  = w1*a1  + w2*a2
             vb     = w1*vb1 + w2*vb2
         endif
C 
        vmaxt1 = vmaxas(i-1)
c 
	if (dlands(i) .ge. 0.0) then
c          ++ This is an over-water point
c 
c          Check to see if storm just moved over water.
c          If so, adjust for land/ocean surface roughness differences
           if (dlands(i-1) .lt. 0.) then
	      vmaxt1 = vmaxt1/redfac
           endif
c 
	   vmaxt2 = vmaxt1 + (vmaxs(i)-vmaxs(i-1))
         else
c          ++ This is an over-land point
c 
c          Check to see if storm just moved over land.
c          If so, adjust for ocean/land surface roughness differences
           if (dlands(i-1) .ge. 0.) then
	      vmaxt1 = redfac*vmaxt1
           endif
c 
           t      = ftimes(i)-ftimes(i-1)
           fbar   = 0.5*(flands(i)+flands(i-1))
	   vmaxt2 = vb + (vmaxt1-vb)* exp(-fbar*alpha*t)
	 endif
c 
	 vmaxas(i) = vmaxt2
      enddo
c 
      if (interp .gt. 2) then
         do i=1,ntimes
	    write(6,887) ftimes(i),vmaxs(i),vmaxas(i),rlats(i),rlons(i),
     +                   dlands(i),flands(i)
  887       format(8(f6.1,1x))
         enddo
      endif
c
c     Interpolate decay vmaxas back to original forecast times
      iflag=1
c 
      call xint(ftimes,vmaxas,ntimes,iflag,lflag,xi,fi,ierr)
c 
      iflag=0
      do i=1,itime
         call xint(ftimes,vmaxas,ntimes,iflag,lflag,
     +                  ftime(i),vmaxa(i),ierr)
      enddo
c 
c     Interpolate dlands back to original forecast times
      iflag=1
c 
      call xint(ftimes,dlands,ntimes,iflag,lflag,xi,fi,ierr)
c 
      iflag=0
      do i=1,itime
         call xint(ftimes,dlands,ntimes,iflag,lflag,
     +                  ftime(i),dland(i),ierr)
      enddo
c 
      return
      end
c 
      subroutine fland(slon,slat,rkm,fraction)
c     This routine calcuates the fraction of the circular area
c     centered at the point (slat,slon) that is over land. 
c 
c     Input: rkm - radius of circle in km
c            slat - center latitude of the circle  (deg N pos)
c            slon - center longitude of the circle (deg W neg)
c 
c     Output: fraction - the fraction of the circle over land
c 
c     Calculate the distance to nearest land at the circle center
      call aland(slon,slat,d00)
c 
c     Check for special cases
      if (rkm .le. 0.0) then
         fraction =  1.0
         return
      endif
c 
      if (d00 .gt. rkm) then
         fraction = 0.0
         return
      endif
c 
      if (d00 .lt. -rkm) then
         fraction = 1.0
         return
      endif
c 
c     Perform area integration 
      fraction = 0.0
      dx = 25.0
      if (dx .ge. rkm/4.0) dx = rkm/4.0
      dy = dx
c 
      pi = 3.14159
      dtr= pi/180.0
      xfac = 111.1*cos(slat*dtr)
      yfac = 111.1
c 
      n = ifix(rkm/dx)
c 
      ntotal = 0
      nland  = 0
      do j=-n,n
      do i=-n,n
         x = float(i)*dx
         y = float(j)*dy
         r = sqrt(x*x + y*y)
         if (r .gt. rkm) go to 1000
c 
         tlat = slat + x/xfac
         tlon = slon + y/yfac
c 
         call aland(tlon,tlat,tdtl)
         ntotal = ntotal+1
         if (tdtl .le. 0.0) nland = nland+1
 1000    continue
c 
      enddo
      enddo
c 
      fraction = float(nland)/float(ntotal)
c 
      return
      end
c       
      subroutine xint(x,f,n,iflag,lflag,xi,fi,ierr)
c     This routine applies a quadratic interpolation procedure
c     to f(x) between x(1) and x(n). f(x) is assumed to be
c     represented by quadratic polynomials between the points
c     x(i). The polynomials are chosen so that they equal f(i)
c     at the points x(i), the first derviatives on either
c     side of the interior x(i) match at x(i), and the second
c     derivative of the approximated function integrated
c     over the domain is minimized.
c 
c     This version is for interpolating longitude
c 
c     Input:  x(1),x(2) ... x(n)      The x values (must be sequential)
c             f(1),f(2) ... f(n)      The function values
c             n                       The number of x,f pairs
c             iflag                   Flag for initialization
c                                      =1 for coefficient calculation
c                                      =0 to use previous coefficients
c             lflag                   Flag for linear interpolation
c                                      =0 to perform linear interpolation 
c                                      =1 to perform quadratic interpolation
c             xi                      The x value at which to interpolate f
c 
c     Output: fi                      The interpolated function value
c             ierr                    Error flag
c                                      =0  Normal return
c                                      =1  Parameter nmax is too small
c                                      =2  The x values are not sequential
c                                      =3  Coefficient iteration did not
c                                          converge
c                                      =4  Mix-up finding coefficients
c                                      =5  if xi .gt. x(n) or .lt. x(1),
c                                          xi is set to nearest endpoint
c                                          before the interpolation
c 
c                                     Note: fi is set to -99.9 if
c                                           ierr=1,2,3 or 4
c 
      parameter (nmax=1000)
c 
      dimension x(n),f(n)
c 
c     Save variables
      dimension ax(nmax),bx(nmax),cx(nmax)
c 
c     Temporary local variables
      dimension df(nmax),dx(nmax),gm(nmax),ct(nmax)
c 
      common /xsave/ ax,bx,cx
c 
c     Specify unit number for debug write statements
c     and debug flag
      idbug  = 0
      lutest = 6
c 
c     Initialize error flag
      ierr   = 0
c 
c     Specify minimum reduction in cost function for convergence
      thresh = 1.0e-10
c 
c     Check to make sure nmax is large enough, and n is .gt. 1 
      if (n .gt. nmax .or. n .lt. 2) then
         ierr=1
         fi = -99.9
         return
      endif
c 
      if (iflag .eq. 1) then
c        Perform the initialization for later interpolation
c 
c        Check to make sure x is sequential
         do 10 i=1,n-1
            if (x(i) .ge. x(i+1)) then
               ierr=2
               fi = -99.9
               return
            endif
   10    continue
c 
c        Check for special case where n=2. Only linear interpolation
c        is possible.
         if (n .eq. 2) then
            cx(1) = 0.0
            bx(1) = (f(2)-f(1))/(x(2)-x(1))
            ax(1) = f(1) - bx(1)*x(1)
            go to 1500
         endif
c 
c        Calculate x and f differences
         do 15 i=1,n-1
            df(i) = f(i+1)-f(i)
            dx(i) = x(i+1)-x(i)
   15    continue
c 
c        Calculate domain size
         d = x(n) - x(1)
c 
c        Check for linearity of input points
         eps = 1.0e-10
         bb = (f(2)-f(1))/(x(2)-x(1))
         aa = f(1) - bb*x(1)
         dev = 0.0
         do 12 i=3,n
            dev = dev + abs(aa + bb*x(i) - f(i))
   12    continue
c 
         if (dev .lt. eps .or. lflag .eq. 0) then
            do 13 i=1,n-1
               cx(i) = 0.0
   13       continue
            go to 1000
         endif
c 
c        Iterate to find the c-coefficients
         cx(1) = 0.0
         nit  = 100
         slt  = 0.01
         cfsave = 1.0e+10
c 
         do 20 k=1,nit
c           Calculate c values
            do 25 i=2,n-1
               cx(i) = -cx(i-1)*dx(i-1)/dx(i) 
     +                -df(i-1)/(dx(i)*dx(i-1))
     +                +df(i  )/(dx(i)*dx(i  ))
   25       continue
c 
c           Calculate current value of cost function
            cf0 = 0.0
            do 26 i=1,n-1
               cf0 = cf0 + cx(i)*cx(i)*dx(i)
   26       continue
            cf0 = 0.5*cf0/d
c 
            if (idbug .ne. 0) then
               write(lutest,101) cf0
  101          format(/,' cf0=',e13.6)
            endif
c 
c           Check for convergence
            rel = abs(cf0 - cfsave)/abs(cfsave)
            if (rel .lt. thresh) go to 1000
            cfsave = cf0
c 
c           Calculate values of Lagrange multipliers
            gm(n-1) = cx(n-1)*dx(n-1)/d
c 
            if (n .gt. 3) then
               do 30 i=n-2,2,-1
                  gm(i) = cx(i)*dx(i)/d - gm(i+1)*dx(i)/dx(i+1)
   30          continue
            endif
c 
c           Calculate gradient of cost function with respect to c1
            dsdc1 =  dx(1)*(cx(1)/d - gm(2)/dx(2))
c 
c           Adjust cx(1) using trial step
            ct(1) = cx(1) - slt*dsdc1
c 
c           Calculate remaining c values at trial step
            do 33 i=2,n-1
               ct(i) = -ct(i-1)*dx(i-1)/dx(i) 
     +                 -df(i-1)/(dx(i)*dx(i-1))
     +                 +df(i  )/(dx(i)*dx(i  ))
   33       continue
c 
c           Calculate cost function at trial step
            cft = 0.0
            do 31 i=1,n-1
               cft = cft + ct(i)*ct(i)*dx(i)
   31       continue
            cft = 0.5*cft/d
c 
c            write(6,*) 'dsdc1,cft,cf0',dsdc1,cft,cf0
c           Calculate optimal step length and re-adjust cx(1)
            den = 2.0*((cft-cf0) + slt*dsdc1*dsdc1)
            if (den .ne. 0.0) then
               slo = dsdc1*dsdc1*slt*slt/den
            else
               slo =0.0
            endif
c 
c           Adjust slo if desired
            slo = 1.0*slo
c 
            cx(1) = cx(1) - slo*dsdc1
c 
            if (idbug .ne. 0) then
               write(lutest,100) k,cft,slt,slo
  100          format(' Iteration=',i4,'  cf1=',e11.4,' slt=',e11.4,
     +                                                ' slo=',e11.4)
c     
               do 99 j=1,n-1
                  write(lutest,102) j,cx(j)
  102             format('    i=',i2,' c=',f8.4)
   99          continue
            endif
c 
c           Calculate trial step for next time step
            slt = 0.5*slo
   20    continue
c 
c        Iteration did not converge
         ierr=3
         fi=-99.9
         return
c 
c        Iteration converged
 1000    continue
c 
         if (idbug .ne. 0) then
            write(lutest,104)
  104       format(/,' Iteration converged')
         endif
c 
c        Calculate b and a coefficients
         do 40 i=1,n-1
            bx(i) = df(i)/dx(i) - cx(i)*(x(i+1) + x(i))
            ax(i) = f(i) - bx(i)*x(i) - cx(i)*x(i)*x(i)
   40    continue        
      endif
c 
 1500 continue
c     Interpolate the function
c 
c     Check for xi out of bounds
      if (xi .lt. x(1)) then
         xi = x(1)
         ierr = 5
      endif
c 
      if (xi .gt. x(n)) then
         xi = x(n)
         ierr = 5
      endif
c 
c     Find the interval for the interpolation
      ii = 1
      do 50 i=2,n
         if (xi .le. x(i)) then
            ii = i-1
            go to 2000
         endif
   50 continue
c 
      fi = -99.9
      ierr=4
      return
c 
 2000 continue
      fi = ax(ii) + bx(ii)*xi + cx(ii)*xi*xi
c 
      return
      end
