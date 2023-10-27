       subroutine calct(deltar,xc,yc,yo,xf,rmxlim)
c
c  calculates the radial profile for eight azimuthal angles
c         
      
      include 'params.h'
      
      dimension xf(ni,nj)

      dimension idst(nmx),hmax(nmx),rmax(nmx)

      common /scale/rmxavg,rfind
      common /pass/xr(ini,nmx),dist(nmx)
      common /total/ ddel,dtha
      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,id1,id2

      logical verb

      include 'const.h'

      verb=.false.

      fact=cos(yo)
c
c      set the factor to determine lower limit of dist search
c
      bfact = .5
      rdistl =  bfact*rmxavg

      if(verb) then
        print*,'calct',deltar,xc,yc,yo,yold
        print*
        print*,'b factor to determine rdistl: ',bfact
      endif

c         
c         assume the maximum wind is within rfavg of center (but <10.8 also)
c         

      irend =int(rmxlim/deltar)

      iravg =int(rdistl/deltar)
      

      if(verb) then
        print*,'lower limit and radius of dist search: ',rdistl,iravg
        print*,'upper limit and radius of dist search: ',rmxlim,irend
      endif

      dx=ddel*(1.0/pi180)
      dy=dtha/pi180

c         
c         angle loop
c         
      do 10 i=1,nmx

        theta= 2.*pi*float(i-1)/float(nmx)

        do 11 ir=1,ini

          ro=float(ir)*deltar
          x=(ro*cos(theta))/(fact)+xc+1.0
          y=(ro*sin(theta))+yc+1.0
          ix=int(x/dx)
          iy=int(y/dy)
          ix1=ix+1
          iy1=iy+1
          p=x/dx-float(ix)
          q=y/dy-float(iy)
          xr(ir,i)=(1.-p)*(1.-q)*xf(ix,iy) +(1.-p)*q*xf(ix,iy+1)
     1         +  (1.-q)*p*xf(ix+1,iy) + p*q*xf(ix+1,iy+1)
 11     continue
c         
c         find relative max after which ro check begins
c         
        do id = 1,nmx
          idst(id) = 0
          hmax(id)=-10.e10
        end do

        do 12 ir=iravg,irend
          hmax(i)=amax1(hmax(i),xr(ir,i))
          if(hmax(i).eq.xr(ir,i))dist(i)=float(ir)*deltar
          if(hmax(i).eq.xr(ir,i))idst(i)=ir
 12     continue

c         
c         if the max. value is also the endpt it maynot be a relative max
c         check backwards from irend for the last relative max
c         
c         
        irvgu = iravg+1
        if(irvgu.le.2)then
          irvgu = 3
        endif
c         
        if(irend.eq.idst(i).or.iravg.eq.idst(i)) then
          do 13 ir=irend,irvgu,-1
            if(xr(ir-1,i).lt.0.) goto14
            
            if(xr(ir-1,i).gt.xr(ir,i).and.xr(ir-1,i).ge.xr(ir-2,i)) then
              dist(i)=float(ir-1)*deltar

              if(verb) then
                print*,'readjusting dist'
     $               ,dist(i),hmax(i),xr(ir-1,i),rmxlim
              endif

              go to 14
            endif
 13       continue
 14       continue
          
        endif

        if(idst(i).lt.iravg)then
          if(verb)  print*,'lower limit check, dist changed to rmxlim, i is: ',i
          dist(i) = rmxlim
        endif

 10   continue
      
      do idd = 1,nmx
        dist(idd) = dist(idd) * 1.1
      end do
      
      if(verb) then
        print*,'relative max found '
        print 4400,dist
 4400   format(25f4.1)
        write(6,400)
     1       (float(ir)*deltar,(xr(ir,i)/100.,i=1,1),ir=1,ini)
 400    format(25f5.1)
      endif

      return
      end
