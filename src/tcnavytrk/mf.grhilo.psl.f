      subroutine grhilo_proc_psl(
     $     fld,ktau,
     $     ib,ie,jb,je,
     $     flat,flon,vcrit,
     $     slat,slon,spsl,spsldef)
c         
c         routine to find all critical points in a 2-d scalar grid (fld) 
c         
c         np is the max # of critical points
c         the i,j ; lat/lon ; and critical value are returned
c
c         
      use trkParams
      use f77OutputMeta
      use mfutils
      
      real*4 fld(ni,nj)

      real acl(np),xcl(np),ycl(np),gcl(np),lcl(np),hll(np),dcl(np)
      real ach(np),xch(np),ych(np),gch(np),lch(np),hlh(np),dch(np)
      real xhl(np),yhl(np),ahl(np),ghl(np),lhl(np),dhl(np)

      integer ich(np),jch(np),icl(np),jcl(np)

      integer ndxl(np),ndxh(np)

      real rmax(np),rmin(np)
      character*1 chlh(np),chll(np)

      dimension tlats(nc),tlons(nc),tvals(nc),tdists(nc),tpcdef(nc)

      character hl*1

      logical verb
      logical tough

      character ctype*1
      character qtitle*24
      character oformat*24,cval*24

      verb=verbGrhiloPsl

      tough=.true.
      tough=.false.

      nhl=0
      nh=0
      nl=0

      ctype='l'

c--       find the lows
c
      call findExtrema(fld,
     $     ib,ie,jb,je,ctype,
     $     rfindPsl,
     $     nhl)

c--       now get their props in between grid points -- value, lat,lon, gradient, laplacian and distance from flat,flon
c         
      
      do n=1,nhl

        call getExtremaProps(fld,
     $       ihl(n),jhl(n),flat,flon,
     $       xcl(n),ycl(n),acl(n),gcl(n),lcl(n),dcl(np))

      enddo

      nl=nhl


c--       get first guess long from vrt850 fix
c
      slat0=slat
      slon0=slon

      slat=99.
      slon=999.
      spsl=9999.

      if(nl.ge.1) then

        if(nl.gt.1) then
          call indexx(nl,dcl,ndxl)
        else
          ndxl(1)=1
        endif
        
        sdist=9999.9
        nstm=0

        do n=1,nl
          ii=n
          val=acl(ndxl(ii))
        end do

        do n=1,nl
          ii=n
          val=acl(ndxl(ii))
          tlon=xcl(ndxl(ii))
          tlat=ycl(ndxl(ii))

          call rumdirdist(tlat,tlon,flat,flon,rhead,sdistn)

c--       great circle calc from steve lord in mfutils module; != rumdirdist, but diff is order 0.01%
c
ccc          sdistn1=distsp(tlat,tlon,flat,flon)
          
          if(sdistn.lt.sdistmin) then

            call rumdirdist(tlat,tlon,flat,flon,rhead,rdist)
            call rumdirdist(slat0,slon0,tlat,tlon,thead,tdist)

            nstm=nstm+1

            tlats(nstm)=tlat
            tlons(nstm)=tlon
            tvals(nstm)=val
            tdists(nstm)=rdist
            
c--       find max delta between center and p in sdistpsl
c         
            spsldef=1e20
            spsl=tvals(nstm)

            do j=jb,je
              do i=ib,ie
                call rumdirdist(tlat,tlon,ygrd(j),xgrd(i),rhead,sdist)
                if(sdist.le.sdistpsl) then
                  pcdef=spsl-fld(i,j)
                  if(pcdef.lt.spsldef) spsldef=pcdef
                endif
              enddo
            enddo

            tpcdef(nstm)=pcdef

            if(verb) write(*,'(a,i2,5(f6.1,2x))') 
     $           'PSL grhilo.psl   FFF000: ',nstm,tlats(nstm),tlons(nstm),tvals(nstm),tdists(nstm),tpcdef(nstm)

          endif

        end do


c--       find low with greatest psl deficit
c
        if(nstm.ge.1) then

          tpcdefmin=1e20

          if(verb) write(*,'(a,1x,i2,a,4(i3,1x),a,i3)') 
     $         'PSL grhilo.psl   FFF111: N storms in the box: ',nstm,' ib,ie,jb,je: ',ib,ie,jb,je,' tau: ',ktau

          do n1=1,nstm
            if(tpcdef(n1).lt.tpcdefmin) then
              ndist=n1
              tpcdefmin=tpcdef(n1)
              if(verb) write(*,'(a,i2,2x,2(f6.1,2x),i2)') 
     $             'PSL grhilo.psl   FFF222: ',n1,tpcdef(n1),tpcdefmin,ndist
            endif
          enddo
          
          slat=tlats(ndist)
          slon=tlons(ndist)
          spsl=tvals(ndist)
          sdist=tdists(ndist)
          spsldef=tpcdef(ndist)

          if(verb) write(*,'(a,5(f6.1,2x))') 
     $         'PSL grhilo.psl   FFF333: ',slat,slon,spsl,sdist,sdistpsl

          
          if(verb) then
            write(*,'(a,i2,a,4(f8.2,1x),a,i3,a,f7.2)')
     $           'PSL grhilo.psl   FFF444: ndist: ',ndist,' slat/slon/spsl/sdist:',slat,slon,spsl,sdist,
     $           ' tau: ',ktau,' spsldef: ',spsldef

          endif

          
        endif

      endif

      if(slat.gt.90.0) spsldef=999.9
      return
      end


