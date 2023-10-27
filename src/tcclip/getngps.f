      function getngps (strmid, century)
c
c
c************************************************************
c
c
c   Description:  getngps retrieves gridded data 
c                 (spherical, 1.0 degree winds)
c                 from the TEDS database and writes them
c                 to binary files for use by ngps vortex tracker
c
c   Programmer, date:   buck sampson, nrl  Jul 97
c
c   Classification: unclassified 
c
c   Useage:    getngps wp0195 19
c		       where wp0195 is the storm id
c                            19 is the storms's century
c
c   Input:  
c              b????????.dat - best track data
c   Output:
c              screen        - plain text forecast
c              getngps.dbg   - debugging data
c              ngpl.yymmddhh - gridded data for 1000 mb tracker 
c              ngpu.yymmddhh - gridded data for quality control 
c
c********* Principal variables and arrays *******************
c
c     storms   - storms directory
c     filename - file name
c     strmid   - storm id (eg, wp0195)
c     century  - century of storm (eg, 19)
c     cent     - century of latest bt posit (eg, 19)
c     ldtg     - current, -12, -24 hr dtg
c     cdtg     - dtg 
c     cns      - North or South (N/S)
c     cew      - East or West (E/W)
c     ins      - current, -12 -24 hr N/S
c     iew      - current, -12 -24 hr E/W
c     iqual    - quality control flag (1=get qual fields, 0=don't)
c     mdate    - current dtg (4 integers)
c     fxxxx    - field data arrays
c     ilat     - latitude of track position
c     ilon     - longitude of track position
c     ntau     - forecast period
c     iunit    - unit for output file
c     lvl1     - level1 index         
c     lvl2     - level2 index         
c     parm     - parameter index     
c     
c********* Change Record ************************************
c
c  upgraded to new database   ....  sampson Sep 98
c
c
c************************************************************
c
c
c
      character*200 storms,filename
      character*20  field
      character*8 ldtg(3)
      character*8 cdtg
      character*8 tdtg
      character*6 strmid
      character*2 century
      character*2 cent
      character*1 cns,cew
      character*1 ins(3),iew(3)

c
      real      lat, lon
      integer   iqual
      integer*4 mdate(4)
      integer*4 lvl1
      integer*4 parm
      integer*4 ierr
      real      fu1000(65160)
      real      fv1000(65160)
      real      fpsfc(65160)
      real      fu850(65160)
      real      fv850(65160)
      real      fu700(65160)
      real      fv700(65160)
      real      fu500(65160)
      real      fv500(65160)
      dimension ilat(3), ilon(3)
      integer*4 ntau
      integer*4 iunit
      integer*4 icentury
c
c********************************************************************
c
      getngps = 0
      lvl2 = 0
cx  quality control fields flag (1=get them, 0=don't)
      iqual=1
      iunit=9
      junit=10
c
c  get the storms directory name
c
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
c
c     get the storm id
c
cx    call getarg(1,strmid)
      if(strmid(1:6).eq.'      ') then
         write(6,*)'useage: getngps wp0295 19'
         stop
      endif
      call locase (strmid,6)
c
c  open debugging file
c
      write(filename,'(a)')'getngps.dbg'
      call openfile (7,filename,'unknown',ioerror)
      if (ioerror.lt.0) go to 950
c
c  write heading on output
c
      write(*,*)' '
      write(*,*)'********* getngps for ',strmid,'**********************'
      write(*,*)' '
      write(7,*)' '
      write(7,*)'********* getngps for ',strmid,'**********************'
      write(7,*)' '
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b",
     1      strmid(1:4), century, strmid(5:6), ".dat"
      write(7,*) 'storm filename:',filename
      call openfile (92,filename,'old',ioerror)
      if (ioerror.lt.0) go to 950
c
c  find the last dtg in the best track file
c
      ios = 0
      do while ( ios .eq. 0 )
	 call readBT( 92,cent,tdtg,lat,cns,lon,cew,iwnd,ios )
         if (tdtg.ne.'        ') cdtg=tdtg
      enddo
      write (ldtg(1),'(a8)') cdtg
      call icrdtg (ldtg(1),ldtg(2),-6)
      call icrdtg (ldtg(1),ldtg(3),-12)
c
c  now find the current, -6, and -12 hr positions
c
      rewind 92
      ios = 0
      do while ( ios .eq. 0 )
	call readBT( 92,cent,cdtg,lat,cns,lon,cew,iwnd,ios )
        if( ios .eq. 0 ) then
	   if (cdtg.eq.ldtg(1)) then
	     ilat(1)=lat*10.0
	     ins(1) =cns
	     ilon(1)=lon*10.0
	     iew(1) =cew
           elseif (cdtg.eq.ldtg(2)) then
	     ilat(2)=lat*10.0
	     ins(2) =cns
	     ilon(2)=lon*10.0
	     iew(2) =cew
           elseif (cdtg.eq.ldtg(3)) then
	     ilat(3)=lat*10.0
	     ins(3) =cns
	     ilon(3)=lon*10.0
	     iew(3) =cew
           endif
        endif
      enddo
      read(century,'(i2)')icentury

   45 continue
      close (92)
      if (ilat(3).eq.0) then
	 write(7,*) "GETNGPS: NEED AT LEAST 3 POSITIONS (12HRS) TO RUN"
	 stop "GETNGPS: NEED AT LEAST 3 POSITIONS (12HRS) TO RUN"
      endif

    7 continue

   20 continue

      write(7,*) " "
      write(7,*) " ldtg = ",ldtg(1), ldtg(2), ldtg(3)
      write(7,*) " "
c
c  open database for read
c
      write(*,*) 'open TEDS'
      call ted_open(ierr)
      if (ierr.ne.0) then 
	  call ted_stop(ierr)
          stop
      endif
cx
cx  Per FNMOC request, make dtg stamp for 06z -> 00z, 18z->12z
cx  This is ok, because we don't have intermediate times anyway
      cdtg=ldtg(1)
      if (cdtg(7:8).eq.'06' .or. cdtg(7:8).eq.'00') then
                cdtg(7:8)='00'
      elseif (cdtg(7:8).eq.'12' .or. cdtg(7:8).eq.'18') then
                cdtg(7:8)='12'
      endif
c
c  open output files
c
      write(filename,'(a,a,a)') storms(1:ind),"/ngpl.",ldtg(1)
      write(7,*) 'ngpl filename:',filename
      open(unit=iunit, file=filename,form='unformatted',err=950)
      write (iunit) cdtg
      write(filename,'(a,a,a)') storms(1:ind),"/ngpu.",ldtg(1)
      write(8,*) 'ngpu filename:',filename
      open(unit=junit, file=filename,form='unformatted',err=950)
      write (junit) cdtg

      do 850 k=1,11
c        loop 11 times - 0,12,24,36,48,60,72,84,96,108,120
      do 800 n=1,9
c
c        loop 9 fields - 
c                         1000 u,v (m/s) - goes into ngpl
c                         sfc pres (mb)  - goes into ngpu
c                         850 u,v  (m/s) - goes into ngpu
c                         700 u,v (m/s)  - goes into ngpu
c                         500 u,v (m/s)  - goes into ngpu
c
c
c
c  1000 mb 
	    if     (n.eq.1) then   
  		lvl1=1000
  		lvl2=0
		parm=4
                field='1000 mb u'
	    elseif (n.eq.2) then   
  		lvl1=1000
  		lvl2=0
		parm=5
                field='1000 mb v'
c
c  quality control field check, skip fields if set to zero
            elseif (n.gt.2 .and. iqual.eq.0) then
                goto 500
c
c  surface 
	    elseif (n.eq.3) then
		lvl1=0
		lvl2=0
		parm=6
                field='surface pres'
c
c  850 mb 
	    elseif (n.eq.4) then
		lvl1=850
		lvl2=0
		parm=4
                field='850 mb u comp'
	    elseif (n.eq.5) then 
		lvl1=850
		lvl2=0
		parm=5
                field='850 mb v comp'
c
c  700 mb 
	    elseif (n.eq.6) then
		lvl1=700
		lvl2=0
		parm=4
                field='700 mb u comp'
	    elseif (n.eq.7) then 
		lvl1=700
		lvl2=0
		parm=5
                field='700 mb v comp'
c
c  500 mb 
	    elseif (n.eq.8) then
		lvl1=500
		lvl2=0
		parm=4
                field='500 mb u comp'
	    elseif (n.eq.9) then
		lvl1=500
		lvl2=0
		parm=5
                field='500 mb v comp'
            endif

            read(ldtg(1),'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
            cdtg=ldtg(1)  
            ntau=(k-1)*12
            write(7,*)'k:',k
cx
cx   for these fields, data is only available every 12 hours
cx
            if (mdate(4).eq.06) then
                         mdate(4)=00
                         cdtg(7:8) ='00'
            elseif (mdate(4).eq.18) then
                         mdate(4)=12
                         cdtg(7:8) ='12'
            endif
c
c  itry is a counter for how many times to try to get 72 hr fields
c
            itry=0           

   70       continue
cx          write(6,*) ' '
cx          write(6,*)'cdtg:',cdtg,' ntau:',ntau,' field:',field
 	    write(7,*) ' '
            write(7,*)'icentury,cdtg:',icentury,cdtg,' ntau:',ntau
            write(7,*)' lvl1:',lvl1,' lvl2:',lvl2,' parm:',parm
            write(7,*) 'mdate:',mdate
  	    if (n.eq.1) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fu1000(1),ierr)
  	    elseif (n.eq.2) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fv1000(1),ierr)
  	    elseif (n.eq.3) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fpsfc(1),ierr)
  	    elseif (n.eq.4) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fu850(1),ierr)
  	    elseif (n.eq.5) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fv850(1),ierr)
  	    elseif (n.eq.6) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fu700(1),ierr)
  	    elseif (n.eq.7) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fv700(1),ierr)
  	    elseif (n.eq.8) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fu500(1),ierr)
  	    elseif (n.eq.9) then
               call get_grid_1deg
     &	       (icentury,mdate,lvl1,lvl2,parm,ntau,fv500(1),ierr)
            endif

c  check to see if acquired fields are acceptable.  We are looking 

	    if(ierr.ne.0) then

c  1000 mb winds tau greater than 144 failed,
c  initial time 1000mb fields (tau=6 for 06z and 18z, tau=12 for 00z and 12z)
c  must exist.
c  
                if(n.eq.2 .and. itry.gt.1) then
                   close (iunit)
                   close (junit)
                   call system ("/bin/rm -f ngpl.*")
                   call system ("/bin/rm -f ngpu.*")
                   write(6,*)'getngps:no field available'
                   write(7,*)'getngps:no field available'
                   close (7)
                   call ted_stop (ierr)
		   stop
c  1000 mb winds complete, but for shortened forecast length.
                elseif(n.eq.1 .and. itry.gt.1) then
                   close (iunit)
                   close (junit)
                   write(6,*)'getngps:shortened forecast'
                   write(7,*)'getngps:shortened forecast'
                   close (7)
                   call ted_stop (ierr)
		   stop

cx other parameters are less important, set flag, and keep going

                elseif(ntau.gt.144 .and. n.gt.2) then
                   close (junit)
                   write(6,*)'getngps:quality control field shortened'
                   write(7,*)'getngps:quality control field shortened'
                   iqual=0
                   go to 800
                endif


                incr=-12
                ntau=ntau-incr
		call icrdtg(cdtg,cdtg,incr)
                read (cdtg,'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
                itry=itry+1
                go to 70
            endif
cx	    write(6,*) 'get_grid_1deg complete!'
	    write(6,*)'acquired: cdtg=',cdtg,' tau=',ntau,
     &                ' field=',field

  100       continue
c
  500    continue
  800    continue

c        write to output to files
         write (iunit) fu1000
         write (iunit) fv1000
         write(7,*) 'fields written to ngpl file'
         if(iqual.eq.1) then
           write (junit) fpsfc
           write (junit) fu850
           write (junit) fv850
           write (junit) fu700
           write (junit) fv700
           write (junit) fu500
           write (junit) fv500
           write(7,*) 'fields written to ngpu file'
         endif
								     

  850 continue
      close (iunit)
      write(6,*) ' normal stop'
      write(7,*) ' normal stop'
      close (7)
      call ted_stop (sflag)

  899 stop "GETNGPS: NORMAL RUN"
c
  900 continue
      write (*,1015)
      write (*,1020) n, ldtg, ntau
c  quit TEDS
      call ted_stop (sflag)

      STOP "GETNGPS: FIELD NOT FOUND"
  950 continue
      write (*,*)'cannot open ', filename
      stop
c
c
 1015 format (" NO NGPS FORECAST - FNOC FIELD NOT FOUND")
 1020 format (" *** FIELD NOT FOUND ***,",5x,a3,2x,a8,2x," TAU = ",i3)
 1030 format (10x,i3,a1,i4,a1,8x,a2,a1,7x,i3,10x,
     1         2(1x,i3,a1,i4,a1),a8)
 1040 format (" TAU",10x,"DTG",11x,"LAT",7x,"LONG",10x,"CATEGORY")
 1050 format (" ")
 1070 format (2x,i2.2,8x,a8,8x,f4.1,a1,5x,f5.1,a1,8x,a10,a5)
 1080 format (1X,"NGPS FORECASTS STARTING AT TAU = ",i2,
     1      " USED ",A8," FORECAST FIELDS.")
 1090 format (6x,a2)
 2000 format (a6,a2)
 2020 format(7x,17(2x,f5.1))
 2030 format(2x,f5.1,17(1x,f6.0))
c
      end

