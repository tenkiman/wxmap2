      program ua2g
C         
C         convert upper air observations WITHOUT sfc obs to GrADS format
C         
C         recipe to run this sample program and display in GrADS:
C
C*******
C*******  set the icray flag in the parameter statement (icray=1 for cray)
C*******  if NOT a cray then comment out the call assign line
C*******
C         
C         unix:
C
C         f77 ua2g.f -o ua2g
C         ua2g
C         stnmap -i ua.seq.ctl
C         grads -lc "open ua.seq.ctl"
C         
C         Files:
C         
C         ua.txt    ASCII source data
C         
C         unix:
C
C         ua.seq.obs    GrADS binary format (sequential) 
C         ua.seq.smp    station map file (16 bytes on 32-bit machines
C         ua.seq.ctl    GrADS data descriptor file
C
C---      np - max # of levels and icray option
C
      parameter(np=500)

      character id*8
      character card*80
      character chmns*1,chmew*1
C         
C         arrays to store the multi-level variables
C
      dimension p(np),z(np),t(np),td(np),u(np),v(np)

      undef=1e20
      d2r=3.141592654/180.0
C         
C         define the relative time to 0 (valid at the time of the time index)
C
      rt=0.0
C         
C         open the files
C
      open(10,file='ua.txt',status='old',err=800,form='formatted')
C         
C         for cray, this assign produces pure station data WITHOUT blocks
C         as in unix unformatted writes
C
      open(12,file='ua.seq.obs',form='unformatted',status='unknown')

C         
C         read the first card to get things going
C         
      read(10,'(a)') card

      ns=0
      
      junk=0
      do while(junk.eq.0)
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
C         
C         the pressure level
C
          p(l)=float(iplev)
C         
C         set date to undefined if not available
C
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
C         
C         convert winds to u,v
C
            dir=90.0-idir*1.0
            spd=ispd*0.514
            u(l)=-spd*cos(dir*d2r)
            v(l)=-spd*sin(dir*d2r)
          endif
          
          l=l+1
C         
C         go to next vertical level
C
          go to 900

        endif

 910    continue
C         
C         got the data; printer output
C
        nl=l-1
        print*
        write(*,'(a,i3)') 'Sounding # ',ns
        write(*,'(a,i3)') 'Number fo levels = ',nl
        write(*,'(a,a)') 'Station id = ',id
        write(*,'(a,f5.1,a1,1x,f4.1,a1)') 'Lon/Lat = ',
     $       rlon,chmew,rlat,chmns
        print*
        do l=1,nl
          write(*,'(6(f7.2,1x))') p(l),z(l),t(l),td(l),u(l),v(l)
        enddo
C         
C         VERY IMPORTANT - set the last char in the id to the endo
C         of string character in C
C
        id(8:8)='\0'
C         
C         upper air data only; set the iflag to 0
C         
        iflag=0
C         
C         GrADS wants lon to start and 0 and increase eastward,
C         hence deg W are negative 
C
        if(chmns.eq.'S') rlat=-rlat
        if(chmew.eq.'W') rlon=360.0-rlon
C         
C         write out the header
C         
        write(12) id,rlat,rlon,rt,nl,iflag
C         
C         write the data
C
        write(12) (p(l),z(l),t(l),td(l),u(l),v(l),l=1,nl)
C         
C         go for more data
C
        go to 900

      enddo
C         
C         error conditions
C

      go to 999
 800  continue
      print*,'unable to open tmp.asc'
      stop
      

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

      stop 'all done'
      end


