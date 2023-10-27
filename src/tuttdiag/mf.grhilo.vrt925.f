      subroutine grhilo_proc_vrt925(
     $     fld,
     $     ib,ie,jb,je,
     $     flat,flon,vcrit,
     $     slat,slon,svort)
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

      real xhl(np),yhl(np),ahl(np),ghl(np),lhl(np),dhl(np)
      integer ndxl(np),ndxhl(np)

      real conlat(nc),conlon(nc),conval(nc),condist(nc)

      logical verb
      logical tough

      character ctype*1

cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

      tough=.true.
      tough=.false.

      distnm=.true.

      verb=verbGrhiloVrt925

      slat=99.9
      slon=999.9

      if(blat.lt.0.0) then
        ctype='l'
      else
        ctype='h'
      endif

c--       find the max vort points
c
      call findExtrema(fld,
     $     ib,ie,jb,je,ctype,
     $     rfindVrt925,
     $     nhl)

c--       now get their props in between grid points -- value, lat,lon, gradient, laplacian and distance from flat,flon
c         
      do n=1,nhl

        call getExtremaProps(fld,
     $       ihl(n),jhl(n),
     $       xhl(n),yhl(n),ahl(n),ghl(n),lhl(n),dhl(n))

      enddo

      if(nhl.gt.1) then
        call indexx(nhl,ahl,ndxhl)
      else
        ndxhl(1)=1
      endif
      
      sdist=9999.9
      nstm=0

      do i=1,nhl

        ii=i

        val=ahl(ndxhl(ii))
        
c--       use abs for shem
c         
        val=abs(val)

        if(verb) then
          write(*,'(a,2(i3,1x),2(f7.3,1x),2x,2(f8.2,1x))')
     $         'grhilo.vrt925',i,ii,yhl(ndxhl(ii)),xhl(ndxhl(ii)),val,vcrit
        endif
        
        if(val.gt.vcrit) then

          tlon=xhl(ndxhl(ii))
          tlat=yhl(ndxhl(ii))

          call rumdirdist(tlat,tlon,flat,flon,rhead,sdistn)

          if(verb) then
            print*,'4444444flon/tlon: ',flon,tlon,'flat/tlat:',flat,tlat,'dist: ',sdistn,sdistmin
          endif

          if(sdistn.lt.sdistmin) then

            call rumdirdist(tlat,tlon,flat,flon,rhead,rdist)
            call rumdirdist(slat0,slon0,tlat,tlon,thead,tdist)

            nstm=nstm+1
            if(nstm >= nc) then
              print*,'EEEEEEEEEEE too many possible vort pointsin grhilo_prc_vrt925;, sayoonara'
              stop 'nc too big'
            endif

            conlat(nstm)=tlat
            conlon(nstm)=tlon
            conval(nstm)=val
            condist(nstm)=rdist

            if(verb) print*,'VVVVVVVVVVVVVVVVVVVVVVVVV ',nstm,conlat(nstm),conlon(nstm),conval(nstm),condist(nstm)

          endif

        endif

      end do


c--       find closest vort max
c         
      
      svort=9999.
      if(nstm.ge.1) then
        condistmin=1e20
        if(verb) print*,'NNNNNNNNNNNN storms in the box: ',nstm,' ib,ie,jb,je: ',ib,ie,jb,je

        do n=1,nstm
          if(condist(n).lt.condistmin) then
            ndist=n
            condistmin=condist(n)
          endif
        enddo
        
        slat=conlat(ndist)
        slon=conlon(ndist)
        svort=conval(ndist)

        if(verb) then
          write(*,'(a,i2,a,1(f8.2,1x),a,2(f8.2,1x),a,2(f8.2,1x),a,2(f8.2,1x))')
     $         'FFFFF(dist) ndist: ',ndist,' rdist/spd:',condist(ndist),
     $         ' sdist: ',condist(ndist),vcrit,' conlat/conlon: ',
     $         conlat(ndist),conlon(ndist),'eee: ',slat,slon
          
        endif
        
      endif

      return

      end subroutine grhilo_proc_vrt925
