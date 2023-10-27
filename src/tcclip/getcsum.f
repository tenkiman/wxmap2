      function getcsum (strmid, century)
c
c
c************************************************************
c
c
c   Description:  getcsum retrieves gridded data
c                 (spherical, 2.5 degree)
c                 from the TEDS database and writes them
c                 to binary files for use by csum
c                 Gridded data are:
c                    current   500 mb heights
c                    24 hr old 500 mb heights
c                    current surface pressure
c                    24 hr old surface pressure
c                    *current 200 mb heights 
c                    *24 hr old 200 mb heights
c                 
c                      *atlantic or NWP north of ridge only
c
c   Programmer, date:   buck sampson, nrl  Oct 95
c
c   Classification: unclassified
c
c   Useage:    getcsum wp0195 19
c                      where wp0195 is the storm id
c                            19 is the storm's century     
c
c   Input:
c              b????????.dat - best track data
c   Output:
c              screen        - plain text forecast
c              getcsum.dbg   - debugging data
c              csum.yymmddhh - gridded data for csum
c
c********* Principal variables and arrays *******************
c
c     storms   - storms directory
c     filename - file name
c     strmid   - storm id (eg, wp0195)
c     century  - century (eg, 19)
c     cent     - century of last bt posit (eg, 19)
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
c
c********* Change Record ************************************
c
c  upgraded to new database   ....  sampson Sep 98
c
c************************************************************
c
c
      character*200 command
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
      character*1 ibas

c
      real      lat, lon
      integer*4 mdate(4)
      integer*4 level1
      integer*4 level2
      integer*4 ierr
      real      ftemp(10512)
      dimension ilat(3), ilon(3)
      dimension dglon(3)
      integer*4 ntau
      integer*4 itau(3,2)
      integer*4 ktau(3,2)
      integer*4 system
      integer*4 icentury
      integer*4 parm
      dimension tlat(3),tlon(3)
      data itau / 0, 24, 48, 0, 0, 24/
      data ktau / 12, 36, 60, 0, 12, 36/
c
c********************************************************************
c
      write(*,*) ' '
      write(*,*) ' '
      write(*,*) '********** Start getcsum **********'
      getcsum = 0
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
         write(6,*)'useage: getcsum wp0295 19'
         stop
      endif
      call locase (strmid,6)
c
c  open debugging file
c
      write(filename,'(a)')'getcsum.dbg'
      call openfile (7,filename,'unknown',ioerror)
      if (ioerror.lt.0) go to 950
c
c  write heading on output
c
      write(7,*)' '
      write(7,*)'********* getcsum for ',strmid,'**********************'
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
c  convert the 1st two characters of stormid to uppercase
c
      call upcase(strmid,6)
      ibas=strmid(1:1)
c
c  find the last dtg in the best track file
c
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 92,cent,tdtg,lat,cns,lon,cew,iwnd,ios )
         if (tdtg.ne.'        ') cdtg=tdtg
      enddo
      write (ldtg(1),'(a8)') cdtg
      call icrdtg (ldtg(1),ldtg(2),-12)
      call icrdtg (ldtg(1),ldtg(3),-24)
c
c  now find the current, -12, and -24 hr positions
c
      rewind 92
      ios = 0
      do while ( ios .eq. 0 )
        call readBT( 92,cent,cdtg,lat,cns,lon,cew,iwnd,ios )
        write(7,*) 'cdtg=:',cdtg
        write(7,*) 'lat=:',lat
        write(7,*) 'lon=:',lon
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
      write(7,*) 'ldtg=:',ldtg
      write(7,*) 'ilat=:',ilat
      write(7,*) 'ilon=:',ilon
      read(cent,'(i2)')icentury
      
   45 continue
      close (92)
      if (ilat(3).eq.0) then
	 write(7,*) "GETCSUM: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
	 stop "CSUM: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
      endif

cx
cx    only storms in NWP and ATL are processed   ...bs 7/27/95
cx   make sure that the tropical cyclone is within climatological limits
cx   5-45N,100-180E in WP, 5-50N,20-100W in AL
cx
      if ( (ins(1)  .eq.'N')
     1                    .and. (iew(1)  .eq.'E')
     2                    .and. (ilat(1) .ge.  50)
     3                    .and. (ilat(1) .le. 450)
     4                    .and. (ilon(1) .ge.1000)
     5                    .and. (ilon(1) .le.1800)) go to 7
      if ( (ins(1)  .eq.'N')
     1                    .and. (iew(1)  .eq.'W')
     2                    .and. (ilat(1) .ge. 50)
     3                    .and. (ilat(1) .le. 500)
     4                    .and. (ilon(1) .ge. 200)
     5                    .and. (ilon(1) .le.1000)) go to 7

      print *, "GETCSUM: TRACK POSIT OUTSIDE ALLOWED FORECAST AREAS"
      print *, "(5-45N,100-180E in WP, 5-50N,20-100W in AL)"
      print *, "LATEST POINT: ",ilat(1),ins(1),ilon(1),iew(1) 
      stop "GETCSUM: TRACK POSIT OUTSIDE ALLOWED FORECAST AREAS"
    7 continue

c
      do 10 I=1,3
         tlat(i) = float(ilat(i)) * 0.1
         tlon(i) = float(ilon(i)) * 0.1
   10 continue
c
      do 20 i=1,3
         if (ins(i) .eq. 1hS) stop "CSUM: NO FCST FOR SO HEMI"
         if (iew(i) .eq. 1hW) tlon(i) = -tlon(i)
   20 continue


      write(7,*) " "
      write(7,*) " LDTG = ",ldtg(1), ldtg(2), ldtg(3)
      write(7,*) " "


      ia=1
      if (ilon(1) .le. 1000) ia=2
      if (ibas .eq. 1hL) ia=3

c
c     get direction of motion (dom)
c
      slon = amod ((360.0 -tlon(2)),360.0)
      elon = amod ((360.0 -tlon(1)),360.0)
      call rhdst (tlat(2),slon,tlat(1),elon,dom,dst)
cx    print *, " DOM = ", dom, " DST = ", dst
cx    print *, "0"
      write(7,*) " DOM = ", dom, " DST = ", dst
      write(7,*)  " "
      idom = dom

c
c     loop 3 times (for the 24, 48 and 72 hour forecasts)
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

c  open output file write date-time-group
      write (filename,'(a,a,a)')storms(1:ind),"/csum.",ldtg(1)
      open (unit=9,file=filename,form="unformatted",err=950)
      write (9) ldtg(1)

      do 850 k=1,3
c
c        longitude is positive from east to west
c
         do 40 i=1,3
         dglon(i) = amod ((360.0 -tlon(i)),360.0)
   40    continue
c
c        200 mb steering for atl and nwp north of the ridge
c
         nlim = 4
         if (ia .eq. 3) nlim=6
         if (ia.eq.1 .and. idom.gt.30 .and. idom.le.120 .and.
     1      iwind.ge.90) nlim=6
c
c        loop 4 - 6 times (to compute each of the required tables)
c
cx 50    do 500 n=1,nlim
   50    do 500 n=1,6
c
c           tables 1,3 & 5 are current time
c           tables 2,4 & 6 are previous 24 hour
c
            if (mod(n,2) .eq. 0) nn = 2
            if (mod(n,2) .ne. 0) nn = 1
c
            if (iflg .eq. 1) go to 55
            itm = 1
            if (k.eq.1 .and. mod(n,2).eq.0) itm = 3
            ntau = itau(k,nn)
            go to 60
c
   55       itm = 2
            if (k.eq.1 .and. mod(n,2).eq.0) itm=3
            ntau = ktau(k,nn)
c
   60       continue
	    if     (n.eq.1 .or. n.eq.2) then
		level1=500
		level2=0
		parm=1
                field='500mb height'
	    elseif (n.eq.3 .or. n.eq.4) then
  		level1=0
  		level2=0
		parm=6
                field='surface pres'
	    elseif (n.eq.5 .or. n.eq.6) then
		level1=200
		level2=0
		parm=1
                field='200mb height'
            endif

            read(ldtg(itm),'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
            cdtg=ldtg(itm)  
            if(mdate(4) .eq.  6 .or. mdate(4) .eq. 18) then
                     incr=-6
                     mdate(4)=mdate(4)+incr
		     call icrdtg(cdtg,cdtg,incr)
            endif

   70       continue
cx          write(6,*)'cdtg:',cdtg,'ntau:',ntau,' field:', field
	    write(7,*) ' '
            write(7,*)'icentury,cdtg:',icentury,cdtg,'ntau:',ntau
            write(7,*)' level1:',level1,' level2:',level2,' parm:',parm
            write(7,*) 'mdate:',mdate
	    write(7,*) 'ntau:',ntau
  	    call get_grid (icentury,mdate,level1,level2,
     &			   parm,ntau,ftemp(1),ierr)
	    if(ierr.ne.0) then
                if(ntau.gt.72) then
                   write(6,*)'*************************************'
                   write(6,*)'****getcsum: fields not available****'
                   write(6,*)'****getcsum: try again later*********'
                   write(6,*)'*************************************'
                   write(7,*)'*************************************'
                   write(7,*)'****getcsum: fields not available****'
                   write(7,*)'****getcsum: try again later*********'
                   write(7,*)'*************************************'
                   close (7)
                   close (9)
cx      remove partly constructed file 
                   write (command,*)"rm ",storms(1:ind),"/csum.",ldtg(1)
                   call system(command)
                   call ted_stop (ierr)
		   stop
                endif
                incr=-12
                ntau=ntau-incr
		call icrdtg(cdtg,cdtg,incr)
		write(7,*) "cdtg:",cdtg
                read (cdtg,'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
                go to 70
            endif
cx	    write(6,*) 'get_grid complete!'
	    write(6,*)'acquired: cdtg=',cdtg,' tau=',ntau,
     &                ' field=',field
	    write(7,*) 'get_grid complete!'
            write(7,*) '30n,170e(6981)  30n,180e(6985) 30n,170w(6989)'
            write(7,*) ftemp(6981),ftemp(6985),ftemp(6989)
            write(7,*) ' 30n,180e(6985) 40n,180e(7561) 50n,180e(8137)'
            write(7,*) ftemp(6985),ftemp(7561),ftemp(8137)
c      write to output file 
            write (9) ftemp
  100       continue
c
  500    continue
  850 continue
c  close output file and quit TEDS
      close (9)
      write(6,*) ' normal stop'
      write(7,*) ' normal stop'
      close (7)
      call ted_stop (sflag)
      stop
  950 continue
      write (*,*)'cannot open ', filename
      stop
c
      end
