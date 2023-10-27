      subroutine amatrix

      include 'params.h'

      common /matrix/ a(nmx,nmx),capd2
      common /vect/xvect(nmx),yvect(nmx)
      common /ifact/nnn,r0vect(nmx),rb,ienv
      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      include 'const.h'

      yo=yold*pi180
      fact=cos(yo)
c         capd2=(2.25)*(2.25)
c         capd2=(12.0)*(12.0) -- original from nps, now set in tcfilt.f
c
c  capd2 defines the radius of influence for each point
c  during the oi
c
      do ip=1,nmx
        do jp=ip,nmx
          dpij=(fact*(xvect(ip)-xvect(jp)))**2 +(yvect(ip)-yvect(jp))**2
          a(ip,jp)= exp(-dpij/capd2)
          a(jp,ip)= a(ip,jp)
        end do
      end do

      return
      end
