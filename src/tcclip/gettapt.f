      function gettapt (strmid, century)
c
c
c************************************************************
c
c
c   Description:  gettapt retrieves gridded data 
c                 (spherical, 2.5 degree layer winds)
c                 from the TEDS database and writes them
c                 to binary files for use by tapt
c
c   Programmer, date:   buck sampson, nrl  Aug 98
c
c   Classification: unclassified 
c
c   Useage:    gettapt wp0195 19
c		       where wp0195 is the storm id
c                      19 is the storm's century
c
c   Input:  
c              b????????.dat - best track data
c   Output:
c              screen        - plain text forecast
c              gettapt.dbg   - debugging data
c              tapt.yymmddhh - gridded data for tapt 
c
c********* Principal variables and arrays *******************
c
c     storms   - storms directory
c     filename - file name
c     strmid   - storm id (eg, wp0195)
c     century  - century of storm (eg, 19)
c     century  - century of last bt posit (eg, 19)
c     ldtg     - current, -12, -24 hr dtg
c     cdtg     - dtg 
c     cns      - North or South (N/S)
c     cew      - East or West (E/W)
c     ins      - current, -12 -24 hr N/S
c     iew      - current, -12 -24 hr E/W
c     mdate    - current dtg (4 integers)
c     f        - field data array
c     ilat     - latitude of track position
c     ilon     - longitude of track position
c     ntau     - forecast period
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
      character*80  card
      character*20  field
      character*8 ldtg(3)
      character*8 tdtg
      character*8 cdtg
      character*6 strmid
      character*2 century
      character*2 cent
      character*1 cns,cew
      character*1 ins(3),iew(3)

c
      real      lat, lon
      integer*4 mdate(4)
      integer*4 icentury
      integer*4 n1
      integer*4 n2
      integer*4 ierr
      real      f(925)
      dimension ilat(3), ilon(3)
      integer*4 ntau
c
c********************************************************************
c
      gettapt = 0
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
         write(6,*)'useage: gettapt wp0295 19'
         stop
      endif
      call locase (strmid,6)
c
c  open debugging file
c
      write(filename,'(a)')'gettapt.dbg'
      call openfile (7,filename,'unknown',ioerror)
      if (ioerror.lt.0) go to 950
c
c  write heading on output
c
      write(*,*)' '
      write(*,*)'********* gettapt for ',strmid,'**********************'
      write(*,*)' '
      write(7,*)' '
      write(7,*)'********* gettapt for ',strmid,'**********************'
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
      read(cent,'(i2)')icentury

   45 continue
      close (92)
      if (ilat(3).eq.0) then
	 write(7,*) "GETTAPT: NEED AT LEAST 3 POSITIONS (12HRS) TO RUN"
	 stop "GETTAPT: NEED AT LEAST 3 POSITIONS (12HRS) TO RUN"
      endif

    7 continue

   20 continue


      write(7,*) " "
      write(7,*) " ldtg = ",ldtg(1), ldtg(2), ldtg(3)
      write(7,*) " "


      iflg = 0
c
c  open database for read
c
      write(*,*) 'open TEDS'
      call ted_open(ierr)
      if (ierr.ne.0) then
           write(*,*) 'error opening TEDS database'
	   call ted_stop(ierr)
	   stop
      endif
c
c  open database for read
c
      write(filename,'(a,a,a)') storms(1:ind),"/tapt.",ldtg(1)
      write(7,*) 'tapt filename:',filename
      open(unit=9,  file=filename,form='unformatted',err=950)
      write (9) ldtg(1)

      do 850 k=1,4
c        loop 4 times - 0,24,48,72
      do 800 n=1,6
c
c        loop 6 fields - 200mb u,v  1000mb u  500mb z,u,v
c
c  200mb 
	    if     (n.eq.1) then   
  		n1=200
		n2=4
		iunit=9
                field='200 mb u comp'
	    elseif (n.eq.2) then
		n1=200
		n2=5
		iunit=9
                field='200 mb v comp'
c  1000mb 
	    elseif (n.eq.3) then 
		n1=1000
		n2=4
		iunit=9
                field='1000 mb u comp'
c  500mb
	    elseif (n.eq.4) then
		n1=500
		n2=1
		iunit=9
                field='500 mb z'
	    elseif (n.eq.5) then
		n1=500
		n2=4
		iunit=9
                field='500 mb u comp'
	    elseif (n.eq.6) then
		n1=500
		n2=5
		iunit=9
                field='500 mb v comp'
            endif

            read(ldtg(1),'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
            cdtg=ldtg(1) 
c   only have 00 and 12 Z fields to work with
	    if(mdate(4) .eq.  6 .or. mdate(4) .eq. 18) then
		    incr=-6
	            mdate(4)=mdate(4)+incr
		    call icrdtg(cdtg,cdtg,incr)
	    endif
            ntau=(k-1)*24
            write(7,*)'k:',k
c
c  itry is a counter for how many times to try to get 72 hr fields
c
            itry=0           

   70       continue
cx    	    write(6,*) ' '
cx          write(6,*)'cdtg:',cdtg,' ntau:',ntau,' field:',field
 	    write(7,*) ' '
            write(7,*)'icentury,cdtg:',icentury,cdtg,' ntau:',ntau
	    write(7,*)'lvl:',n1,' parm:',n2
            write(7,*) 'mdate:',mdate
  	    call get_grid_tapt(icentury,mdate,n1,n2,ntau,f(1),ierr)
	    if(ierr.ne.0) then
                if(ntau.gt.78) then
                   call system ("/bin/rm -f ?tapt.*")
                   write(6,*)'gettapt:no field available'
                   write(7,*)'gettapt:no field available'
                   call ted_stop (ierr)
                   close (7)
		   stop
                endif
                incr=-6
                ntau=ntau-incr
******************************************************
c special case for 72 hr fcst, use the 78 hr fcst from -18 hrs if you
c couldn't find the 78 hr fcst from -12 hrs.
                if (ntau.gt.78 .and. k.eq.7 .and. itry.lt.4) ntau=78
******************************************************
		call icrdtg(cdtg,cdtg,incr)
                read (cdtg,'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
                itry=itry+1
                go to 70
            endif
cx	    write(6,*) 'get_grid complete!'
            write(6,*)'acquired: cdtg=',cdtg,' tau=',ntau,
     &  	      ' field=',field
            write(7,*) '55n,90e  55n,180e'
            write(7,*) f(889),f(925)
            write(7,*) '5s,90e  5s,180e'
            write(7,*) f(1),f(37)

c      convert all elements from m/s to knots/10 (tapt wants this)
            do 80, ii=1,925
		 f(ii) = f(ii)*19.44
   80       continue
cx	    write (6,'(25(37f6.0,/))') (f(i),i=1,925)

c      write to output file
              if(iunit.eq.9) then
                 write (iunit) f
                 write(7,*) 'record written to tapt file'
              endif
  100       continue
c
  500    continue
  800    continue
  850 continue
      close (9)
      write(6,*) ' normal stop'
      write(7,*) ' normal stop'
      close (7)
      call ted_stop (sflag)

  899 stop 
c
  900 continue
      write (*,1015)
      write (*,1020) n, ldtg(1), ntau
c  quit TEDS
      call ted_stop (sflag)

      STOP "GETTAPT: FIELD NOT FOUND"
  950 continue
      write (*,*)'cannot open:',filename
      stop
c
c
 1015 format (" NO TAPT FORECAST - FNOC FIELD NOT FOUND")
 1020 format (" *** FIELD NOT FOUND ***,",5x,a3,2x,a8,2x," TAU = ",i3)
 1030 format (10x,i3,a1,i4,a1,8x,a2,a1,7x,i3,10x,
     1         2(1x,i3,a1,i4,a1),a8)
 1040 format (" TAU",10x,"DTG",11x,"LAT",7x,"LONG",10x,"CATEGORY")
 1050 format (" ")
 1070 format (2x,i2.2,8x,a8,8x,f4.1,a1,5x,f5.1,a1,8x,a10,a5)
 1080 format (1X,"TAPT FORECASTS STARTING AT TAU = ",i2,
     1      " USED ",A8," FORECAST FIELDS.")
 1090 format (6x,a2)
 2000 format (a6,a2)
 2020 format(7x,17(2x,f5.1))
 2030 format(2x,f5.1,17(1x,f6.0))
c
      end
