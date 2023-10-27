      subroutine grhilo_proc_vrt850(
     $     fld,rtau,curstm,
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

      real rtau

      real xhl(np),yhl(np),ahl(np),ghl(np),lhl(np),dhl(np)
      integer ndxl(np),ndxhl(np)

      real conlat(nc),conlon(nc),conval(nc),condist(nc)

      logical verb
      logical tough

      character ctype*1,select*1
      character curstm*28

cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

      tough=.true.
      tough=.false.

c--       use the max vort point
c
      select='m'
c--       use the closest vort point
c
ccc      select='c'

      verb=verbGrhiloVrt850

      if(flat.lt.0.0) then
        ctype='l'
      else
        ctype='h'
      endif

c--       find the max vort points
c
      call findExtrema(fld,
     $     ib,ie,jb,je,ctype,
     $     rfindVrt850,
     $     nhl)

c--       now get their props in between grid points -- value, lat,lon, gradient, laplacian and distance from flat,flon
c         

      do n=1,nhl

        call getExtremaProps(fld,
     $       ihl(n),jhl(n),flat,flon,
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

        
        if(val.gt.vcrit) then

          if(verb) then
            write(*,'(a,2(i3,1x),2(f7.3,1x),2x,2(f8.2,1x))')
     $           'grhilo.vrt850',i,ii,yhl(ndxhl(ii)),xhl(ndxhl(ii)),val,vcrit
          endif


          tlon=xhl(ndxhl(ii))
          tlat=yhl(ndxhl(ii))

          call rumdirdist(tlat,tlon,flat,flon,rhead,sdistn)

          if(verb) then
            print*,'4444444flon/tlon: ',flon,tlon,'flat/tlat:',flat,tlat,'dist: ',sdistn,sdistmin,'curstm: ',curstm
          endif

          if(sdistn.lt.sdistmin) then

            call rumdirdist(tlat,tlon,flat,flon,rhead,rdist)

            nstm=nstm+1
            if(nstm >= nc) then
              print*,'EEEEEEEEEEE too many possible vort pointsin grhilo_prc_vrt850;, sayoonara'
              stop 'nc too big'
            endif

            conlat(nstm)=tlat
            conlon(nstm)=tlon
            conval(nstm)=val
            condist(nstm)=rdist

            if(verb) print*,'VVVVVVVV ',nstm,conlat(nstm),conlon(nstm),conval(nstm),condist(nstm)

          endif

        endif

      end do


c--       find closest/largest vort max
c         
      
      svort=9999.
      slat=999.
      slon=9999.

      ndistmax=1

      if(nstm.ge.1) then

        condistmin=1e20
        convalmax=conval(1)

        if(verb) print*,'NNNNNNNNNNNN storms in the box: ',nstm,' ib,ie,jb,je: ',ib,ie,jb,je,' rtau: ',rtau,'curstm: ',curstm

        do n=1,nstm

          if(verb) print*,'n: ',n,'lat/lon/val/dist: ',conlat(n),conlon(n),conval(n),condist(n)

          if(condist(n).lt.condistmin) then
            ndist=n
            condistmin=condist(n)
          endif

          if(conval(n).gt.convalmax) then
            ndistmax=n
            convalmax=conval(n)
          endif
        enddo
        
        if(verb) then
          write(*,'(a,1x,a3,1x,a,i4,2x,4(f6.2,2x))') 'DDD ',curstm,'ndistmax, convalmax lat/lon/dist: ',
     $         ndistmax,convalmax,conlat(ndistmax),conlon(ndistmax),condist(ndistmax)

          write(*,'(a,1x,a3,1x,a,i4,2x,4(f6.2,2x))') 'DDD ',curstm,'ndist   , conval    lat/lon/dist: ',
     $         ndist,conval(ndist),conlat(ndist),conlon(ndist),condist(ndist)
        endif

        if(select .eq. 'c') then
          slat1=conlat(ndist)
          slon1=conlon(ndist)
          svort1=conval(ndist)

        elseif(select .eq. 'm') then
          slat1=conlat(ndistmax)
          slon1=conlon(ndistmax)
          svort1=conval(ndistmax)
        else
          print*,"EEEEEEEEEEEEEEEEEEEE error in mf.grfhilo.vrt850.f select must 'c' or 'm' is now: ",select
          stop 'mf.grfhilo.vrt850.f select'
        endif


        call rumdirdist(slat,slon,slat1,slon1,rhead,fdist)

        fspd=fdist/dtau

        if(verb) then
          write(*,'(a,i2,a,3(f8.2,1x),a,2(f8.2,1x),a,2(f8.2,1x),a,2(f8.2,1x),a,1(f8.2,1x))')
     $         'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFff(dist) ndist: ',ndist,
     $         ' sdist: ',condist(ndist),vcrit,conval(ndist),' conlat/conlon: ',
     $         conlat(ndist),conlon(ndist)
          
        endif

        slat=slat1
        slon=slon1
        svort=svort1

        
      endif

      return

      end subroutine grhilo_proc_vrt850
