      program uas2g
C         
C         convert upper air observations WITH sfc obs to GrADS format
C         
C         recipe to run this sample program and display in GrADS:
C         
C         unix:
C
C         f77 uas2g.f -o uas2g
C         uas2g
C         stnmap -i uas.seq.ctl
C         grads -lc "open uas.seq.ctl"
C         
C         Files:
C         
C         uas.txt    ASCII source data: s.txt
C         
C         unix:
C
C         uas.seq.be.obs    GrADS binary format (sequential, big endian machine) 
C         uas.seq.be.smp    station map file (version 1 - 16 bytes on 32-bit machines version 2 -- 32 bytes all machines)
C         uas.seq.be.ctl    GrADS data descriptor file
C
C---      np - max # of levels
C
      parameter(np=500,icray=0)
      character id*8
      character card*80
      character chmns*1,chmew*1
C         
C         arrays to store the multi-level variables
C
      dimension p(np),z(np),t(np),td(np),u(np),v(np)
C         
C         value of the undefined value and unit conversion parameters
C
      undef=1e20
      d2r=3.141592654/180.0
C         
C         define the relative time to 0 (valid at the time of the time index)
C

      rt=0.0
C         
C         open the files
C
      open(10,file='uas.txt',status='old',err=800,form='formatted')


      open(12,file='uas.seq.obs',form='unformatted',status='unknown')

      ns=0

      junk=1
      do while(junk.eq.1)
C         
C         it's ugly; it's fortran, the return point for reading another card
C
 900    continue
C         
C         when no more cards exit normally to 999
C
        read(10,'(a)',end=999,err=810) card
C         
C         bypass blank cards
C
        if(card(1:4).eq.'    ') then
          go to 900
        endif
C         
C         card with the station id
C
        if(card(1:7).eq.'METXUAR') then
          id=card(18:22)
          l=0
          ns=ns+1
          go to 900
        endif
C         
C         the station location
C
        if(card(2:4).eq.'LOC') then
          read(card,'(10x,f4.1,a1,f5.1,a1)') rlat,chmns,rlon,chmew
          go to 900
        endif
C         
C         get the surface data 
C
        if(card(1:3).eq.'SFC') then
          print*,'12345678901234567890123456789012345678901234567890'
          print*,card
          read(card(37:39),'(i3)') ipsl
          read(card(41:43),'(i3)') its
          read(card(45:47),'(i3)') itds
          read(card(49:50),'(i2)') idir
          read(card(51:52),'(i2)') ispd

          print*,ipsl,its,itds,idir,ispd
C         
C         unit conversion (I forget the break point...)
C         
          if(ipsl.ge.500) then
            psl=900+ipsl*0.1
          else
            psl=1000+ipsl*0.1
          endif

          ts=(its-32.0)/1.8
          tds=(itds-32.0)/1.8
          us=-ispd*sin(idir*10*d2r)/1.94
          vs=-ispd*cos(idir*10*d2r)/1.94
C         
C         go to next card after creating sfc data
C
          go to 900
        endif
C         
C         this card indicates that the subsequent card
C         starts the upper air data; set l=1
C
        if(card(1:6).eq.' PRESS') then
          l=1
          go to 900
        endif
C         
C         all done go to next record
C
        if(card(1:5).eq.'ENDAT') go to 910
        
        if(l.ne.0) then

          read(card,'(2x,i4,3x,i5,1x,f5.1,2x,f4.4,1x,i3,1x,i3)')
     $         iplev,iz,t(l),dd,idir,ispd

          p(l)=float(iplev)

          if(iz.eq.99999) then
            z(l)=undef
          else
            z(l)=float(iz)
          endif

          if(dd.eq.99.9) then
            td(l)=undef
          else
            td(l)=t(l)-dd
          endif
          
          if(idir.eq.999) then
            dir=undef
            spd=undef
            u(l)=undef
            v(l)=undef
          else
            dir=90.0-idir*1.0
            spd=ispd*0.514
            u(l)=-spd*cos(dir*d2r)
            v(l)=-spd*sin(dir*d2r)
          endif
          
cc          print*,card
cc          write(*,'(9(f7.2,1x))') p(l),z(l),t(l),td(l),dir,spd,u(l),v(l)
          
          l=l+1

          go to 900

        endif

 910    continue
C         
C*******     got the data; print and write for GrADS
C
        nl=l-1
        print*
        write(*,'(a,i3)') 'Sounding # ',ns
        write(*,'(a,i3)') 'Number fo levels = ',nl
        write(*,'(a,a)') 'Station id = ',id
        write(*,'(a,f5.1,a1,1x,f4.1,a1)')
     $       'Lon/Lat = ',rlon,chmew,rlat,chmns
        print*

        do l=1,nl
          write(*,'(6(f7.2,1x))') p(l),z(l),t(l),td(l),u(l),v(l)
        enddo

        id(8:8)='\0'
C         
C         both sfc and upper air data; set iflag to 1
C         
        iflag=1
C         
C         GrADS wants lon to start and 0 and increase eastward,
C         hence deg W are negative 
C
        if(chmns.eq.'S') rlat=-rlat
        if(chmew.eq.'W') rlon=360.0-rlon
C         
C         nl is the number of levels; add 1 to include sfc data
C         
        nls=nl+1
C         
C         write out the header
C
        write(12) id,rlat,rlon,rt,nls,iflag
C         
C         write out both the sfc and upper air data using ONE write
C
        write(12) 
     $       psl,ts,tds,us,vs,
     $       (p(l),z(l),t(l),td(l),u(l),v(l),l=1,nl)
C         
C         go back for another set of obs
C
        go to 900

      enddo

      
      go to 999
 800  continue
      print*,'unable to open tmp.asc'
      go to 999

 810  continue
      print*,'error reading file'
      stop

 999  continue

C         
C         write out end of time record
C         
      rlon=0.0
      rlat=0.0
      rt=0.0
      nlev=0
      write(12) id,rlat,rlon,rt,nlev,iflag

      close(12)
      close(10)

      stop
      end


