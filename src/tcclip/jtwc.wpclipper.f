      program jtwc_wpclipper

      character aymdh*10
      character sname*3,sbasin*3,strmid*8
      character card*120
      real latcur, loncur, latm12, lonm12, latm24, lonm24

      character cymdh*10,ciwndcur*3,cdircur*6,cspdcur*6,
     $     clatcur*6,cloncur*6,clatm12*6,clonm12*6,clatm24*6,clonm24*6

      real*4 cnmis(12),clalo(12),p1top8(8)

      call getarg(1,cymdh)
      call getarg(2,sname)
      call getarg(3,sbasin)
      call getarg(4,ciwndcur)
      call getarg(5,cdircur)
      call getarg(6,cspdcur) 
      call getarg(7,clatcur) 
      call getarg(8,cloncur) 
      call getarg(9,clatm12) 
      call getarg(10,clonm12) 
      call getarg(11,clatm24) 
      call getarg(12,clonm24) 

      read(cymdh,'(2x,i8') iymdh
      read(ciwndcur,'(i3)') iwndcur
      read(cdircur,'(f5.1)') dircur
      read(cspdcur,'(f5.2') spdcur
      read(clatcur,'(f5.1)') latcur
      read(cloncur,'(f5.1)') loncur
      read(clatm12,'(f5.1)') latm12
      read(clonm12,'(f5.1)') lonm12
      read(clatm24,'(f5.1)') latm24
      read(clonm24,'(f5.1)') lonm24


      narg=iargc()
      
      if(narg.lt.12) then

        print*,'Arguments to nhc.clipper.x:'
        print*,' '
        print*,' 1989090700 - dtg '
        print*,'        06L - storm id '
        print*,'        ATL - basin'
        print*,'        065 - max wind [kts]'
        print*,'      10.00 - current direction of motion [deg]'
        print*,'       4.57 - current speed of motion [kts]'
        print*,'       38.0 - current latitude [deg N]'
        print*,'      312.2 - current longitude [deg E]'
        print*,'       37.1 - tau-12 latitude [deg N]'
        print*,'      312.0 - tau-12 longitude [deg E]'
        print*,'       36.2 - tau-24 latitude [deg N]'
        print*,'      311.8 - tau-24 longitude [deg E]'
        print*,' '
        print*,'Example'
        print*,' '
        print*,'jtwc.wpclipper.x 1989090700 22W WPC 040 273.00 9.41',
     $       ' 20.0 135.6 19.9  137.6 19.8  139.6'
        print*,' '
        stop 

      endif

      rwndcur=iwndcur*1.0

      print*,iymdh,latcur,loncur,latm12,lonm12,latm24,lonm24,iwndcur
c
c  wpcliper can only run between 6n and 45n and between 100e and 180e.
c
      if(latcur .lt. 3. .or. latcur .gt. 45.) then
        stop 'wpclip can only be run between 3 - 45 N)'
      endif

      call wpclpr(iymdh,latcur,loncur,latm12,lonm12,latm24,lonm24,
     $     rwndcur,cnmis,clalo,p1top8)

      do i=1,6
        print*,clalo(i*2-1),clalo(i*2)
      end do

      stop
      end
