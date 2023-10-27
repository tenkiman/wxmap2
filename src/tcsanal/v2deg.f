      program main
      include 'params.h'

      parameter(nr=10)
      dimension r(nr)
      dimension vtc(nr)

      dr=60.0
      do i=1,nr
        r(i)=dr*(i-1)
      end do
      

      vmb=30.0
      vme=140.0
      dvm=5.0

      vmax=vmb

      do while(vmax.le.vme) 

        if(vmax.gt.50.0) then
          r50c=0.56*vmax+0.19
          r30c=0.70*vmax+55.3
        else
          r50c=0.0
          r30c=55.3
        endif
        
        
        r50c10=r50c
        r30c10=r30c

        r50c05=r50c*0.75
        r30c05=r30c*0.75

        r50c15=r50c*1.25
        r30c15=r30c*1.5

        call ngptcbog(r50c10,r30c10,vmax,r,vtc,nr,
     $       rmaxngp10,alphangp10)
        v1deg10=vtc(2)
        v2deg10=vtc(3)
        v4deg10=vtc(5)

        call ngptcbog(r50c05,r30c05,vmax,r,vtc,nr,
     $       rmaxngp05,alphangp05)
        v1deg05=vtc(2)
        v2deg05=vtc(3)
        v4deg05=vtc(5)

        call ngptcbog(r50c15,r30c15,vmax,r,vtc,nr,
     $       rmaxngp15,alphangp15)
        v1deg15=vtc(2)
        v2deg15=vtc(3)
        v4deg15=vtc(5)


        print*
        write(*,'(a,i3,a,a)') 'vmax: ',int(vmax),
     $       ' kt V1/2/4/deg in kt R in nm'
        write(*,'(a,a)') '       R30        R50       Rmax       Alpha',
     $       '    V1deg     V2deg     V4deg'
        write(*,'(a,7f10.3)') 
     $       '05: ',r30c05,r50c05,rmaxngp05,alphangp05,v1deg05,
     $       v2deg05,v4deg05
        write(*,'(a,7f10.3)') 
     $       '10: ',r30c10,r50c10,rmaxngp10,alphangp10,v1deg10,
     $       v2deg10,v4deg10
        write(*,'(a,7f10.3)') 
     $       '15: ',r30c15,r50c15,rmaxngp15,alphangp15,v1deg15,
     $       v2deg15,v4deg15

        vmax=vmax+dvm

      end do


       
        

      stop
      end



      subroutine ngptcbog(rad50,rad30,vmax,r,vtc,nr,
     $     rmaxngp,alphangp)

      include 'params.h'

      dimension r(nr),vtc(nr)
c
c          compute initial position of the storm
c
      radrat=1.0
      rm=165000.0
      alpha=0.9

c         cms50kt and cms30kt convert 50 and 30 kt to m/s.

      cms50kt = 50.0/1.94595
      cms30kt = 30.0/1.94595

      r50 = rad50*radrat
      r30 = rad30*radrat

c     convert n.mi.to meters

      r50 = 1852.0*r50
      r30 = 1852.0*r30

      vm=vmax/1.95

      if(r50.gt.0.0.and.r30.gt.0.0) then
        alpha = alog(30./50.)/alog(r50/r30)
        if(alpha.gt.0.9) alpha = 0.9
        rm = r50*(cms50kt/vm)**(1.0/alpha)
      else
        if(r50.gt.0.0) then
          rm = r50*(cms50kt/vm)**(1.0/alpha)
        else
          if(r30.gt.0.0) then
            rm = r30*(cms30kt/vm)**(1.0/alpha)
          endif
        endif
      endif

C
C rmax min = 20 km
C
      rmmin=15*1852
      if(rm.lt.rmmin) rm=rmmin

      if(verb) then
        write(*,'(a,f6.2,1x,f5.2,1x,f7.1,1x,f8.1,2x,f8.1)')
     $       'vmax,alpha,rm,r50,r30 (SI): ',vmax,alpha,rm,r50,r30
      endif

      do i=1,nr

        r1=1852.0*r(i)
        if (r1.le.rm) then
          tcrs=vm*(r1/rm)
        else
          tcrs=vm*(r1/rm)**(-alpha)
          if(r1.gt.333000.) then
            tcrs=tcrs*(1.2-r1/1111200.)
          endif
        endif

        vtc(i)=tcrs*1.945
CCC        write(*,'(a,6(f9.1,1x))') 'rrrr ',r(i),r1,vm,rm,tcrs,vtc(i)

      enddo

      rmaxngp=rm/1852.0
      alphangp=alpha


      return
      end



C --- below is full bogus code for winds/mass         
      
CC       pi=4.0*atan(1.0)
CC       omega4=4.0*pi/86400.0

CC c          compute coriolis force at observation point
         
CC       fcor=omega4*sin (blat(ll)*d2r)

CC c         take absolute value into account for the s.h.

CC       fcor=abs(fcor)

CC c          compute height and wind at observation point
        
CC       r1=(blat(ll)-slat(na))*onedeg
CC       avlat=0.5*(blat(ll)+slat(na))
CC       r2=(blon(ll)-slon(na))*cos (avlat*d2r)*onedeg
CC       r1=r1*r1+r2*r2
CC       r1=sqrt(r1)
CC       a4=((fcor*rm*vm)/(1.0-alpha))*(ru/rm)**(1.0-alpha)

CC c     check to see if inside radius of max winds

CC       if (r1.le.rm) then
CC         tcrs(ll,lb)=vm*(r1/rm)
CC         a1=(vm/2.0)*(fcor*rm+vm)*((r1/rm)**2.0)
CC         a2=(fcor*rm*vm/2.0)*(1.0+alpha)/(1.0-alpha)
CC         a3=vm*vm*(1.0+alpha)/(2.0*alpha)
CC         zo(ll,lb)=a1+a2-a3+c2-a4
CC       else
CC         tcrs(ll,lb)=vm*(r1/rm)**(-alpha)
CC         if(r1.gt.333000.) then
CC           tcrs(ll,lb)=tcrs(ll,lb)*(1.2-r1/1111200.)
CC         endif
CC         a1=((fcor*rm*vm)/(1.0-alpha))*(r1/rm)**(1.0-alpha)
CC         a2=(vm*vm/(-2.0*alpha))*(r1/rm)**(-2.0*alpha)
CC         zo(ll,lb)=a1+a2+c2-a4
CC       endif

CC       zo(ll,lb)=zo(ll,lb)/g

CC c          convert to direction and speed

CC       tcrd(ll,lb)=450.0-sang(ll)


CC      program test
CC      parameter (nr=101)
CC      dimension r(nr),vtc(nr)
CC      dr=10.0
CC      do i=1,nr
CC        r(i)=(i-1)*dr
CC      end do
CC      print*,'input rad50:'
CC      read*,rad50
CC      print*,'input rad30:'
CC      read*,rad30
CC      print*,'input vmax:'
CC      read*,vmax
CC      call ngptcbog(rad50,rad30,vmax,r,vtc,nr)
CC      do i=1,nr
CC        write(*,'(f6.1,1x,f6.1)') r(i),vtc(i)
CC      end do
CC      stop
CC     end




