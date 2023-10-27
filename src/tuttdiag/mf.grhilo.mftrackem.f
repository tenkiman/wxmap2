      subroutine grhilo_proc_mftrackem(
     $     fld,undef,xi,yi,ni,nj,
     $     ib,ie,jb,je,dtau,
     $     elat,elon,vcrit,sdistmin,
     $     slat,slon,svort)
c         
c         routine to find all critical points in a 2-d scalar grid (fld) 
c         
c         np is the max # of critical points
c         the i,j ; lat/lon ; and critical value are returned
c
c         
      logical dovortcon

      parameter(dovortcon=.false.)
ccc      parameter(dovortcon=.true.)

      dimension fld(ni,nj),xi(ni),yi(nj)

      include 'grhilo.f'

ccc      verb=.true.

      rnm2deg=1.0/60.0
      slat=99.9
      slon=999.9

C         
C         storm must be within 'sdistmin' deg
C         of the first guess location to be valid
C

Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn         
C         
C         NHEM
C
Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn         


      if(nh.ge.1.and.elat.gt.0.0) then

        if(nh.gt.1) then
ccc       call indexx(nh,ych,ndxh)
          call indexx(nh,ach,ndxh)
        else
          ndxh(1)=1
        endif
        
        sdist=9999.9
        nstm=0

        do i=1,nh

          ii=nh-i+1
          val=ach(ndxh(ii))

          if(verb) then
            write(*,'(a,2(i3,1x),2(f7.3,1x),2x,2(f6.2,1x))')
     $           'grhilo.mftrackem',i,ii,ych(ndxh(ii)),xch(ndxh(ii)),val,vcrit
          endif
          
          if(val.gt.vcrit) then

            tlon=xch(ndxh(ii))
            tlat=ych(ndxh(ii))

            dx=elon-tlon
            dy=elat-tlat

            dx=abs(dx)
            dy=abs(dy)

            sdistn=sqrt(dx*dx + dy*dy)
            call rumdirdist(tlat,tlon,elat,elon,rhead,rdist)
            sdistn=rdist*rnm2deg

            if(verb) then
              print*,'4444444elon/tlon: ',elon,tlon,'elat/tlat:',elat,tlat,'dist: ',sdistn,sdistmin
            endif

            if(sdistn.lt.sdistmin) then

              call rumdirdist(tlat,tlon,elat,elon,rhead,rdist)
              call rumdirdist(slat0,slon0,tlat,tlon,thead,tdist)

              nstm=nstm+1

              flat(nstm)=tlat
              flon(nstm)=tlon
              fval(nstm)=val
              fdist(nstm)=rdist

              if(dtau.ne.0) then
                fspd(nstm)=tdist/dtau
              else
                fspd=0.0
              endif

            endif


            if(sdistn.lt.sdist.and.sdistn.lt.sdistmin) then

              slat=tlat
              slon=tlon

              call rumdirdist (slat,slon,elat,elon,rhead,rdist)
              sdist=rdist*rnm2deg
              svort=val

              if(verb) then
                write(*,'(a,f8.2,a,2(f8.2,1x),a,2(f8.2,1x))')
     $               'val > vcrit NHEM sdist:',sdist,' svort: ',svort,vcrit,' slat/slon: ',slat,slon
              endif

            end if

          endif

        end do
c         
c         see how many potential storms that satisfy the conditions
c
        if(nstm.ge.1) then

          slatcon=0.0
          sloncon=0.0
          sdistcon=0.0
          ncon=0

          fvortmax=-9999.9


          do n=1,nstm

            if(fval(n).gt.fvortmax) fvortmax=fval(n)
            
            if(verb) then
              write(*,'(a,i2,a,2(f8.2,1x),a,2(f8.2,1x),a,2(f8.2,1x))')
     $             'DDDDD val > vcrit n: ',n,' rdist/spd:',fdist(n),fspd(n),
     $             ' svort: ',fval(n),vcrit,' tlat/lon: ',
     $             flat(n),abs(360.0-flon(n))

            endif

          enddo

          do n=1,nstm

            fdistconmax=99999.0
            fdistconmax=250.0
            fvortconmin=10.0


            if(fdist(n).le.fdistconmax.and.fvortmax.le.fvortconmin) then
              ncon=ncon+1
              slatcon=slatcon+flat(n)
              sloncon=sloncon+flon(n)
              sdistcon=sdistcon+fdist(n)
            endif

            
          end do
          
          if(ncon.gt.1.and.dovortcon) then
            slatcon=slatcon/ncon
            sloncon=sloncon/ncon
            sdistcon=sdistcon/ncon
            print*,'CCC doing con: ',ncon,slatcon,sloncon,sdistcon
            slat=slatcon
            slon=sloncon
            sdist=sdistcon
          endif

        endif


        
      endif


Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss         
C         
C         SHEM
C
Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss         

      if(nl.ge.1.and.elat.lt.0.0) then

        sdist=9999.9
        nstm=0

        if(nl.gt.1) then
          call indexx(nl,ycl,ndxl)
        else
          ndxl(1)=1
        endif

        do i=1,nl
          ii=i
          val=acl(ndxl(ii))
          val=abs(val)

          if(val.gt.vcrit) then

            tlat=ycl(ndxl(ii))
            tlon=xcl(ndxl(ii))

            sdistn=sqrt(dx*dx + dy*dy)
            call rumdirdist(tlat,tlon,elat,elon,rhead,rdist)
            sdistn=rdist*rnm2deg
            
            nstm=nstm+1

            if(sdistn.lt.sdist.and.sdistn.lt.sdistmin) then

              slat=tlat
              slon=tlon
              call rumdirdist (slat,slon,elat,elon,rhead,rdist)
              sdist=rdist*rnm2deg
              svort=val

              if(verb) then
                write(*,'(a,5(f8.2,1x))')
     $               'val > vcrit SHEM :',sdist,svort,vcrit,tlat,tlon
              endif


            end if
          endif

        end do
      endif


      return
      end

