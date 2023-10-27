      subroutine bound(xr,r0vect)

      include 'params.h'

      dimension xr(nmx),r0vect(nmx)

      common /xxx/  xf(ni,nj),xc,yc,dx,dy
      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      include 'const.h'

      fact=cos(yold*pi180)

      do i=1,nmx
        theta= 2.*pi*float(i-1)/float(nmx)
        x=r0vect(i)/fact*cos(theta)+xc +1.
        y=r0vect(i)*sin(theta)+yc +1.
        ix=int(x/dx)
        iy=int(y/dy)
        ix1=ix+1
        iy1=iy+1
        p=x/dx-float(ix)
        q=y/dy-float(iy)
        xr(i)=(1.-p)*(1.-q)*xf(ix,iy) +(1.-p)*q*xf(ix,iy+1)
     $       +  (1.-q)*p*xf(ix+1,iy) + p*q*xf(ix+1,iy+1)
      end do

      return
      end
