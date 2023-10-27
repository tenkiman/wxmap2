      subroutine bound2(u,v,tanuv,r0,xc,yc,yyo)
      
      include 'params.h'

      dimension u(ni,nj),v(ni,nj),tani(nmx)
      common  /total/ ddel,dtha

      include 'const.h'

      dx=ddel/pi180
      dy=dtha/pi180
      fact=cos(yyo)

      r0=r0*111.19

      do i=1,nmx

        theta= 2.*pi*float(i-1)/float(nmx)
        x=(r0*cos(theta))/(arad*fact*pi180)+xc
        y=(r0*sin(theta))/(arad*pi180)+yc
        ix=int(x/dx)
        iy=int(y/dy)
        ix1=ix+1
        iy1=iy+1
        p=x/dx-float(ix)
        q=y/dy-float(iy)
        tani(i)=-sin(theta)*
     1       ((1.-p)*(1.-q)*u(ix,iy) +(1.-p)*q*u(ix,iy+1)
     1       +  (1.-q)*p*u(ix+1,iy) + p*q*u(ix+1,iy+1))
     1       +cos(theta)*
     1       ((1.-p)*(1.-q)*v(ix,iy) +(1.-p)*q*v(ix,iy+1)
     1       +  (1.-q)*p*v(ix+1,iy) + p*q*v(ix+1,iy+1))

      end do

      tanuv=0.0
      do i=1,nmx
        tanuv=tanuv +tani(i)/float(nmx)
      end do
      return
      end
