      subroutine maxth(dumu,dumv,dxc,dyc,rmxlim,tw)

      include 'params.h'

      parameter(lgth=30)

      dimension dumu(ni,nj),dumv(ni,nj),tw(ni,nj)
      dimension th(ni,nj),tanmx(ni,nj),tprof(7,7,lgth)
     1      ,itpos(7,7),tmax(7,7),tanavg(ini)

      common /total/ ddel,dtha

      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      common /winds/ dmmm(ni,nj,2),tang(ni,nj),
     $     del(ni,nj),tha(ni,nj)

      common /scale/rmxavg,rfind

      logical verb

      include 'const.h'

      verb=.false.

      fact=cos(yold)

      deltar=0.1
      dxc=xold/pi180-xcorn
      dyc=yold/pi180-ycorn
      ixc=int(dxc)+1
      iyc=int(dyc)+1
      ist=ixc-3
      jst=iyc-3
      iend=ixc+3
      jend=iyc+3

      npts=7

      if(verb)  print*,'ist,iend',ist,jst,iend,jend

c
c  compute radial profile of azimuthal avg. tang. wind at each pt
c

      do i=ist,iend
        do j=jst,jend
          xcen=(del(i,j)-del(1,1))/pi180 +1.0
          ycen=(tha(i,j)-tha(1,1))/pi180 +1.0
          yyo=tha(i,j)
          do ir=1,lgth
            rbd=float(ir)*0.2
            call bound2(dumu,dumv,tanpu,rbd,xcen,ycen,yyo)
            tprof(i-ist+1,j-jst+1,ir)=tanpu
          end do
        end do
      end do

      if(verb) then
        print *,' print 333 in maxth.. tprof(i,1,k),i=4,7'
        print 333,((tprof(i,1,k),i=4,7),(tprof(i,2,k),i=4,7),
     $       (tprof(i,3,k),i=4,7),(tprof(i,4,k),i=4,7),k=1,lgth)
 333    format(16f7.1)
      endif
      

c
c  find the first relative maximum along each azimuthal direction
c  find the position of the largest relative maximum
c         
C         funky way to store i j location; coded (see itpos)
C         

       hmax=0.0

       do i=1,npts
         do j=1,npts

           do ir=2,lgth
             if(tprof(i,j,ir).gt.tprof(i,j,ir-1).and.tprof(i,j,ir)
     1            .gt.tprof(i,j,ir+1)) then
               tmax(i,j)=tprof(i,j,ir)
               itpos(i,j)=1000*(ist+i)+j+jst
               hmax=amax1(tmax(i,j),hmax)
               if(hmax.eq.tmax(i,j)) ipos=itpos(i,j)
               if(hmax.eq.tmax(i,j)) rmxpos=float(ir)*0.2
               goto 53
             endif
           end do

           tmax(i,j)=tprof(i,j,1)
           itpos(i,j)=1001
           hmax=amax1(hmax,tmax(i,j))
           if(hmax.eq.tmax(i,j)) ipos=itpos(i,j)

 53        continue
         end do
       end do

       if(verb) then
         print*,'maxth, hmax', hmax,rmxpos,rmxpos/0.2
         print*,'tmax: ',((tmax(i,j),i=1,npts),j=1,npts)
         print*,'itpos: ',((itpos(i,j),i=1,npts),j=1,npts)
       endif

c
c  use position of the largest relative maximum as the adjusted
c  center location
c
       ycn=float(mod(ipos,1000))-1.
       xcn=float(ipos/1000)-1.
       ixc=int(xcn)+1
       iyc=int(ycn)+1
       xctest=(xcn+xcorn)*pi180
       yctest=(ycn+ycorn)*pi180
c
c  recompute the tangential wind component based on new center
c
       fact=cos(tha(1,iyc))

       if(verb) then
         print*,'in maxxth',ycn,xcn,fact,xctest/pi180,yctest/pi180
         print*,ixc,iyc,del(ixc+1,iyc+1)/pi180,tha(ixc+1,iyc+1)/pi180
       endif
       
       do  j=1,nj
         do i=1,ni
           dx=(del(i,j)-xctest)*fact
           dy=(tha(i,j)-yctest)
           if(dx.ne.0.)theta =atan2(dy,dx)
           if(dy.gt.0..and.dx.eq.0.)theta =90.*pi180
           if(dy.lt.0..and.dx.eq.0.)theta =270.*pi180
           tw(i,j)=-dumu(i,j)*sin(theta) +dumv(i,j)*cos(theta)
           
           if((i.eq.ixc.and.j.eq.iyc).and.verb) then
             print*,i,j,dumu(i,j),dumv(i,j)
     1            ,theta,tw(i,j),dx,dy,'check everything'
           end if

         end do
       end do
       
       if(verb) then
         print *,ixc,iyc,' tw(i,j) follows, i=ixc+/-5,j = iyc+/-5'
         write(6,7700)((tw(i,j)/100.,i=ixc-5,ixc+5),j=iyc+5,iyc-5,-1)
 7700    format(11f5.1)
       end if

       iflag=0
       hmax=0.
       rmxavg=0.
       do ir=3,ini
         rxx=float(ir)*deltar
         call calcr( rxx,rtan,xcn,ycn,yctest,dumu,dumv )
         tanavg(ir)=rtan
         if(tanavg(ir-2).lt.tanavg(ir-1).and.tanavg(ir).lt.tanavg(ir-1)
     1        .and.iflag.eq.0)then
           hmax=tanavg(ir-1)
           rmxavg=rxx-deltar
           iflag=1
         endif
       end do

       if(verb) then
         print*,'found rmxavg ',rmxavg,hmax
       endif

       dxc=xcn
       dyc=ycn
       yold=xcn+xcorn

       if(verb) then
         print 700,tanavg
 700     format(10f6.1)
       endif


       call findra( dxc,dyc,yctest,rmxavg,rfavg,tanavg)
       
       alim = .01
       rmxlim = alim*rmxavg + (1.0-alim)*rfavg

       if(verb) then
         print*,'a factor to determine rmxlim: ',alim
         print*,'found rfavg ',rfavg,rmxavg,rmxlim,dxc,dyc
       endif
       
       return
       end
