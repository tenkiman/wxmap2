      subroutine center(up,vp,delg,thag)

      include 'params.h'

      parameter (kmax=18, lgi=20 )
      
      parameter(igl=500)

      common /gdinf/  ngd,ngr,ntr,dt,js,jn,ie,iw,iimax,imax,jjmax,
     $     jmax,nstflg,icx,icy,ihx,ihy,dftx,dfty

      common /var/  dist,nn1,nn2,nn3,nn4,ifl

      common /winds/ dmmm(ni,nj,2),tang(ni,nj),
     $     del(ni,nj),tha(ni,nj),tanp(ni,nj),ds(ni,nj)

      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      dimension  up(ni,nj),vp(ni,nj)
      dimension  cmsum(2,6),dll(igl),thh(igl),wind(igl)
      dimension  xm(igl),rm(igl)
      dimension  tabpr(igl),tfour(igl),tfive(igl),tsix(igl)
      dimension  tpres(igl),dss(igl),tanw(ni,nj)


      logical verb

      include 'const.h'

      verb=.false.

      rad = arad*1e3

      afct = 150.

ccccc      afct = 1.0e10

      dfct = 2.0*afct
      xcc = xv
      ycc = yv
      dx = xcc - xcorn
      dy = ycc - ycorn
      ix = ifix(dx) + 1
      iy = ifix(dy) + 1

      if(verb) then
        print*
        print*,'(i,j) of center:  ',ix,iy
        print*
      endif


      ddd = del(ix,iy)/pi180

      ddd1 = ddd
      ttt = tha(ix,iy)/pi180
      if(verb) print*,'(lon,lat) of center: ',ddd1,ttt

      do j=1,6
        do i=1,2
          cmsum(i,j) = 0.0
        end do
      end do

      alpha = .125

      irang = 10

      ib = ix - irang
      ie = ix + irang
      jb = iy - irang
      je = iy + irang
      itot = (ie-ib+1)*(je-jb+1)

      if(verb) print *,'ib,ie,jb,je,itot ',ib,ie,jb,je,itot

      ii = 0
      do j = jb , je
        do i = ib , ie
          ii = ii + 1
          dss(ii) = ds(i,j)
          dll(ii) = del(i,j)
          thh(ii) = tha(i,j)
          wind(ii) = sqrt(up(i,j)*up(i,j)+vp(i,j)*vp(i,j) )
        end do
      end do
      
      do i = 1 , itot
        angl= .5*(tha(ix,iy) + thh(i) )
        cosf = cos(angl)
        dx =      cosf*rad*abs(dll(i) -  del(ix,iy) )
        dy =           rad*abs(thh(i) -  tha(ix,iy) )
        rm(i) = sqrt(dx*dx+dy*dy)
      end do

      do i = 1 , itot
        if(rm(i).lt.afct)then
          xm(i) = 1.0
        else
          xm(i) = exp(-( (rm(i) - afct)/dfct)**2)
        endif
      end do

      do i = 1 , itot
        cmsum(1,1) =  cmsum(1,1)+wind(i)*dll(i)*dss(i)*xm(i)
        cmsum(1,2) =  cmsum(1,2)+wind(i)*dss(i)*xm(i)
        cmsum(2,1) =  cmsum(2,1)+wind(i)*thh(i)*dss(i)*xm(i)
        cmsum(2,2) =  cmsum(2,2)+wind(i)*dss(i)*xm(i)
      end do
       
      delg=  cmsum(1,1)/cmsum(1,2)
      thag=  cmsum(2,1)/cmsum(2,2)

c         
c  print the global position from set2 computation
c         

      if(verb) then
        write(6,445) delg/pi180,thag/pi180
 445    format(2x,'global position from windspeed',2f9.3)

        print*,'distance for max wind check (degrees):  ',dist
        print*
      endif

      return
      end
