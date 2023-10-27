      subroutine rodist

      include 'params.h'

      common /vect/xvect(nmx),yvect(nmx)
      common /ifact/nnn,r0vect(nmx),rb,ienv
      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      include 'const.h'

      yo=yold*pi180
      fact=cos(yo)

      xc=xold-xcorn
      yc=yold-ycorn

      do ip=1,nmx

        theta=float(ip-1)/float(nmx)*2.*pi
        r=r0vect(ip)
        xvect(ip)=r*cos(theta)/fact+xc
        yvect(ip)=r*sin(theta)+yc

      end do

      return
      end
