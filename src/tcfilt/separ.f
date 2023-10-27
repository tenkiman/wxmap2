      subroutine separ(xd,xh,xzero,maxr0,meanr0)
c
c  seperates a field into hurricane component and remainder
c
      include 'params.h'

      parameter(nmx1=nmx+1,nmx2=nmx*2,nmx6=nmx*6)

      dimension xr(nmx),xd(ni,nj)
      dimension xh(ni,nj),xzero(ni,nj)

      common /winds/ dmmm(ni,nj,2),tang(ni,nj),
     $     del(ni,nj),tha(ni,nj),tanp(ni,nj),ds(ni,nj)

      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      common /ifact/nnn,r0vect(nmx),rb,ienv

      common /xxx/ xf(ni,nj),xc,yc,dx,dy

      common /total/ ddel,dtha

      dimension b(nmx),w(nmx),ab(nmx,nmx1),ipvt(nmx)
     $     ,wrk(nmx6),iwrk(nmx2)
      
      common /matrix/ a(nmx,nmx),capd2
      common /vect/xvect(nmx),yvect(nmx)

      data xr/24*0./

      logical verb,maxr0,meanr0

      include 'const.h'

      verb=.true.
      verb=.false.

C         
C         if maxr0 then use max r0 vice local r0
C         set on input
C


c  xc,yc are hurricane coordinates
c  r0  is radius at which hurricane component of field goes to zero
c  xr array contains the field values of 12 equally spaced points
c     on circle of radius r0 centered at xc,yc
c
c  set r0 to be max value of r0vect
c
c
      r0=0.0
      r0mean=0.0

      do i=1,nmx
        r0=amax1(r0,r0vect(i))
        r0mean=r0mean+r0vect(i)
      end do
      r0mean=r0mean/nmx

      print*,'ssssssssssssss ',r0,r0mean

      fact =  cos(yold*pi180)
      if(verb) print*,'r0=',r0,capd2,a(1,1),a(2,1),fact


cc
cc   xc is the i position of the center of the old vortex
cc   yc is the j position of the center of the old vortex
cc   ddel is the long. in radians of the outer nest
cc   dtha is the lat.  in radians of the outer nest
cc
c no fact here
c      dx=fact*ddel/pi180
c

      dx=ddel/pi180
      dy=dtha/pi180

      if(verb) then
        print *,'in separ xold,yold ',xold,yold
        print *,'in separ xcorn,ycorn ',xcorn,ycorn
      endif
      
      xc = (xold-xcorn)*dx
      yc = (yold-ycorn)*dy
      is=int((xc-r0/fact)/dx) +1.
      ie=int((xc+r0/fact)/dx + 1.)
      js=int((yc-r0)/dy) +1.
      je=int((yc+r0)/dy + 1.)

      if(verb) then
        print *,'in separ dx,dy = ',dx,dy
        print *,'         xc,yc = ',xc,yc
        print *,'         is,ie = ',is,ie
        print *,'         js,je = ',js,je
      endif

      do  j = 1 , nj
        do i = 1 , ni
          xf(i,j)  = xd(i,j)
        end do
      end do
      
c
c  subroutine bound computes field values of array xr using
c         bilinear interpolation
c
c
      call bound(xr,r0vect)

c
c  xrop(nmx) are the interpolated values of the disturbance
c   field at the r0vect pts
c
c r0max is the maximum value in r0vect(nmx). within the loop a local
c r0 is computed for use in the separation. at the start of the loop
c r0 is again set to r0max to define the domain.
c
c
c

       do iw = 1,nmx
         w(iw) = 0.
       end do

       r0max=r0

       do 10 ix=is,ie
         do 11 jy=js,je

           r0=r0max
           if(meanr0) then
             r0=r0mean
           endif

           x=del(ix,jy)/pi180 -xcorn
           y=tha(ix,jy)/pi180 -ycorn
           delx=(x-xc)*fact
           dely=(y-yc)
           dr=sqrt((delx)**2 +(dely)**2)

           if(dr.gt.r0) then
ccc             print*, 'rrrrrrrrrrrrrr ',ix,jy,dr,r0,delx,dely
             goto 11
           endif

           if(delx.ne.0.0) theta=atan((dely)/(delx))
           if(delx.eq.0.0 .and. dely.lt.0.0) theta=270.*pi180
           if(delx.eq.0.0 .and. dely.gt.0.0) theta=90. *pi180
           if(delx.lt.0.) theta=theta+pi
           if(theta.lt.0.0) theta=2.*pi+theta

           n1=int(theta*nmx/(2.*pi))

           if(verb) then
             if(n1.gt.nmx) print *,'n1.gt.nmx ',n1,theta*57.296
             if(n1.lt.0) print *,'n1 .lt. 0 ',n1,theta*57.296
           endif

           n2=n1+2
           if(n2.gt.nmx)n2=n2-nmx
           delth=theta- 2.*pi*float(n1)/float(nmx)
c         
           if(.not.maxr0) then
             r0=delth*float(nmx)/(2.*pi)*(r0vect(n2)-r0vect(n1+1))
     $            +r0vect(n1+1)
           endif
           if(dr.gt.r0) goto 11
           xr0=delth*float(nmx)/(2.*pi)*(xr(n2)-xr(n1+1)) +xr(n1+1)
c
c now add new code to compute distance from each gridpt. to r0vect pts
c

           do ip=1,nmx
             dpij= (fact*(x-xvect(ip)))**2 +(y-yvect(ip))**2
             b(ip)=exp(-dpij/capd2)
           end do
           
           do ip=1,nmx
             do jp=1,nmx
               ab(ip,jp)=a(ip,jp)
             end do
             ab(ip,nmx1)=b(ip)
           end do

c         
c  solve system using constrained least squares method
c         

           call wnnls(ab,nmx,0,nmx,nmx,0,1.,w,rnm,md,iwrk,wrk)

           temp=0.0
           rtest=0.0
           do ip=1,nmx
             temp=temp +w(ip)*xr(ip)
             if(xr(ip).ne.0.0) rtest=1.0
           end do

           xh(ix,jy)=xf(ix,jy)-temp
           xd(ix,jy)=temp
           xzero(ix,jy)=temp
              
 11      continue
 10    continue

       return
       end
