      function getotcm (strmid, century)
c
c
c************************************************************
c
c
c   Description:  getotcm retrieves gridded data 
c                 (spherical, 2.5 degree layer winds)
c                 from the TEDS database and writes them
c                 to binary files for use by otcm
c
c   Programmer, date:   buck sampson, nrl  Jun 96
c
c   Classification: unclassified 
c
c   Useage:    getotcm wp0195 19
c		       where wp0195 is the storm id
c		             19 is the storm's century     
c
c   Input:  
c              b????????.dat - best track data
c   Output:
c              screen        - plain text forecast
c              getotcm.dbg   - debugging data
c              otcm.yymmddhh - gridded data for otcm 
c
c********* Principal variables and arrays *******************
c
c     storms   - storms directory
c     filename - file name
c     strmid   - storm id (eg, wp0195)
c     century  - century of storm (eg, 19)
c     cent     - century of last bt posit (eg, 19)
c     ldtg     - current, -12, -24 hr dtg
c     cdtg     - dtg 
c     cns      - North or South (N/S)
c     cew      - East or West (E/W)
c     ins      - current, -12 -24 hr N/S
c     iew      - current, -12 -24 hr E/W
c     istartm  - starting time of run (6,12,18,0)
c     mdate    - current dtg (4 integers)
c     f        - field data array
c     ilat     - latitude of track position
c     ilon     - longitude of track position
c     ntau     - forecast period
c     iunit    - unit for output file
c     lvl1     - level index         
c     lvl2     - level index         
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
      character*100 storms,filename
      character*80  card
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
      integer*4 mdate(4)
      integer*4 lvl1, lvl2
      integer*4 parm
      integer*4 icentury
      integer*4 ierr
      integer*4 istartm
      real      f(10512)
      dimension ilat(3), ilon(3)
      integer*4 ntau
      integer*4 iunit
c
c********************************************************************
c
      getotcm = 0
      iunit=9
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
         write(6,*)'useage: getotcm wp0295 19' 
         stop
      endif
      call locase (strmid,6)
c
c  open debugging file
c
      write(filename,'(a)')'getotcm.dbg'
      call openfile (7,filename,'unknown',ioerror)
      if (ioerror.lt.0) go to 950
c
c  write heading on output
c
      write(*,*)' '
      write(*,*)'********* getotcm for ',strmid,'**********************'
      write(*,*)' '
      write(7,*)' '
      write(7,*)'********* getotcm for ',strmid,'**********************'
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
	 write(7,*) "GETOTCM: NEED AT LEAST 3 POSITIONS (12HRS) TO RUN"
	 stop "GETOTCM: NEED AT LEAST 3 POSITIONS (12HRS) TO RUN"
      endif

    7 continue

   20 continue


      write(7,*) " "
      write(7,*) " ldtg = ",ldtg(1), ldtg(2), ldtg(3)
      write(7,*) " "


c
c     loop 7 times (for the 0,12,24,36,48,60 and 72 hour forecasts)
c
      iflg = 0
c
c  open database for read
c
      write(*,*) 'open TEDS'
      call ted_open(ierr)
      if (ierr.ne.0) then
	 call ted_stop(ierr)
	 stop
      endif
c
c  open database for read
c
      write(filename,'(a,a,a)') storms(1:ind),"/otcm.",ldtg(1)
      write(7,*) 'otcm filename:',filename
      open(unit=iunit,
     1     file=filename,access='sequential',form='unformatted',err=950)
      write (iunit) ldtg(1)

      do 850 k=1,7
c        loop 7 times - 0,12,24,36,48,60,72
      do 800 n=1,13
c
c        loop 13 fields - 
c                         1000 u,v (m/s)  - only at initial tau
c                         1000 temp (k)
c                         1000 height (m)
c                         850 u,v  (m/s)
c                         850 temp (k)
c                         850 height (m)
c                         850 u,v  (m/s)
c                         850 temp (k)
c                         850 height (m)
c                         500 u,v (m/s)
c                         500 temp (k)
c                         250 u,v (m/s)
c                         250 temp (k) 
c
c
c  if not first tau, skip the 1000 mb winds
            if (k.gt.1 .and. n.lt.3) go to 100
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
	    elseif (n.eq.3) then
  		lvl1=1000
  		lvl2=0
		parm=2
                field='1000 mb temp'
	    elseif (n.eq.4) then
  		lvl1=1000
  		lvl2=0
		parm=1
                field='1000 mb geopotential height'
c
c  850 mb 
	    elseif (n.eq.5) then
  		lvl1=850
  		lvl2=0
		parm=4
                field='850 mb u comp'
	    elseif (n.eq.6) then 
  		lvl1=850
  		lvl2=0
		parm=5
                field='850 mb v comp'
	    elseif (n.eq.7) then
  		lvl1=850
  		lvl2=0
		parm=2
                field='850 mb temp'
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
	    elseif (n.eq.10) then
  		lvl1=500
  		lvl2=0
		parm=2
                field='500 mb temp'
c
c  250 mb 
	    elseif (n.eq.11) then
  		lvl1=250
  		lvl2=0
		parm=4
                field='250 mb u comp'
	    elseif (n.eq.12) then
  		lvl1=250
  		lvl2=0
		parm=5
                field='250 mb v comp'
	    elseif (n.eq.13) then
  		lvl1=250
  		lvl2=0
		parm=2
                field='250 mb temp'
            endif

            read(ldtg(1),'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
            cdtg=ldtg(1)  
            ntau=(k-1)*12
            write(7,*)'k:',k
cx
cx   for these fields, data is only available every 12 hours
cx   -- be sure to save the start time for tau check later
cx
	    istartm=mdate(4)
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
            write(7,*) 'istartm:',istartm
            write(7,*) 'k:',k
            call get_grid(icentury,mdate,lvl1,lvl2,parm,ntau,f(1),ierr)
c  check to see if acquired fields are acceptable.  We are looking for
c  fields such that initial fields 
c  (tau=6 for 06z and 18z, tau=12 for 00z and 12z)
	    if(ierr.ne.0) then
                if(ntau.gt.96 .or. 
     &             (k.lt.2 .and. istartm.eq. 6) .or.
     &             (k.lt.2 .and. istartm.eq.18) .or.
     &             (k.lt.2 .and. istartm.eq.00 .and. itry.gt.1) .or.
     &             (k.lt.2 .and. istartm.eq.12 .and. itry.gt.1))then
                   call system ("/bin/rm -f otcm.*")
                   write(6,*)'getotcm:no field available'
                   write(7,*)'getotcm:no field available'
                   close (7)
                   call ted_stop (ierr)
		   stop
                endif
                incr=-12
                ntau=ntau-incr
		call icrdtg(cdtg,cdtg,incr)
                read (cdtg,'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
                itry=itry+1
                go to 70
            endif
cx	    write(6,*) 'get_grid complete!'
	    write(6,*)'acquired: cdtg=',cdtg,' tau=',ntau,
     &                ' field=',field
	    write(7,*) 'get_grid complete!, f(1):',f(1)
            write(7,*) '30n,160e(6977)  30n,170e(6981) 30n,180w(6985)'
            write(7,*) f(6977),f(6981),f(6985)
            write(7,*) ' 30n,180e(6985) 40n,180e(7561) 50n,180e(8137)'
            write(7,*) f(6985),f(7561),f(8137)

c      write to output file
            write (iunit) f
            write(7,*) 'field written to otcm file'
  100       continue
c
  500    continue
  800    continue
  850 continue
      close (iunit)
      write(6,*) ' normal stop'
      write(7,*) ' normal stop'
      close (7)
      call ted_stop (sflag)

  899 stop "GETOTCM: NORMAL RUN"
c
  900 continue
      write (*,1015)
      write (*,1020) n, ldtg, ntau
c  quit TEDS
      call ted_stop (sflag)

      STOP "GETOTCM: FIELD NOT FOUND"
  950 continue
      write (*,*)'cannot open ', filename
      stop
c
c
 1015 format (" NO OTCM FORECAST - FNOC FIELD NOT FOUND")
 1020 format (" *** FIELD NOT FOUND ***,",5x,a3,2x,a8,2x," TAU = ",i3)
 1030 format (10x,i3,a1,i4,a1,8x,a2,a1,7x,i3,10x,
     1         2(1x,i3,a1,i4,a1),a8)
 1040 format (" TAU",10x,"DTG",11x,"LAT",7x,"LONG",10x,"CATEGORY")
 1050 format (" ")
 1070 format (2x,i2.2,8x,a8,8x,f4.1,a1,5x,f5.1,a1,8x,a10,a5)
 1080 format (1X,"OTCM FORECASTS STARTING AT TAU = ",i2,
     1      " USED ",A8," FORECAST FIELDS.")
 1090 format (6x,a2)
 2000 format (a6,a2)
 2020 format(7x,17(2x,f5.1))
 2030 format(2x,f5.1,17(1x,f6.0))
c
      end
