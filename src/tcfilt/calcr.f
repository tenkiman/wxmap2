      subroutine calcr(ro,rtan,xc,yc,yold,u,v)

      include 'params.h'

      dimension xr(nmx),u(ni,nj),v(ni,nj)

      common /total/ ddel,dtha

      include 'const.h'

      fact=cos(yold)
      dx=ddel/pi180
      dy=dtha/pi180

      do i=1,nmx
        theta= 2.*pi*float(i-1)/float(nmx)
        x=ro*cos(theta)/fact +xc +1.
        y=ro*sin(theta)+yc +1.
        ix=int(x/dx)
        iy=int(y/dy)
        ix1=ix+1
        iy1=iy+1
        p=x/dx-float(ix)
        q=y/dy-float(iy)
c      xr(i)=(1.-p)*(1.-q)*xf(ix,iy) +(1.-p)*q*xf(ix,iy+1)
c    1      +  (1.-q)*p*xf(ix+1,iy) + p*q*xf(ix+1,iy+1)
       xr(i)=-sin(theta)*
     1    ((1.-p)*(1.-q)*u(ix,iy) +(1.-p)*q*u(ix,iy+1)
     1      +  (1.-q)*p*u(ix+1,iy) + p*q*u(ix+1,iy+1))
     1         +cos(theta)*
     1   ((1.-p)*(1.-q)*v(ix,iy) +(1.-p)*q*v(ix,iy+1)
     1       +  (1.-q)*p*v(ix+1,iy) + p*q*v(ix+1,iy+1))
      end do
      rtan = 0.0
c
c calculate azimuthally averaged tangential wind at radius ro
c
       do i=1,nmx
         rtan = rtan + xr(i)
       end do
       rtan = rtan/float(nmx)
       return
       end
