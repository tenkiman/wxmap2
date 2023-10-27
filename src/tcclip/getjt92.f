      function getjt92 (strmid, century)
c
c
c
c************************************************************
c
c
c   Description:  getjt92 retrieves gridded data
c                 (NH, 2.5 degree layer deep layer mean heights)
c                 from the TEDS database and writes them
c                 to binary files for use by jtwc92
c
c   Programmer, date:   buck sampson, nrl  Oct 95
c
c   Classification: unclassified
c
c   Useage:    getjt92 wp0195 19
c                      where wp0195 is the storm id
c                            19 is the storm's century
c
c   Input:
c              b????????.dat - best track data
c   Output:
c              screen        - plain text forecast
c              jt92.dbg      - debugging data
c              jt92.yymmddhh - gridded data for jtwc92
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
c********* CHANGE RECORD ************************************
c
c  upgraded to new database   ....  sampson Sep 98
c
c
c************************************************************
c
c
      character*200 command
      character*200 storms,filename
      character*80  card
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
      integer*4 mdate(4)
      integer*4 lvl1
      integer*4 lvl2
      integer*4 parm
      integer*4 icentury
      integer*4 ierr
      integer*4 system
      real      f(65,65)
      real      f1(65,65)
      dimension ilat(3), ilon(3)
      integer*4 ntau
c
c********************************************************************
c
      getjt92 = 0
      write(*,*) ' '
      write(*,*) ' '
      write(*,*) '**** start getjt92 ****'
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
         write(6,*)'useage: getjt92 wp0295 19'
         stop
      endif
      call locase (strmid,6)
c
c  open debugging file
c
      write(filename,'(a)')'getjt92.dbg'
      call openfile (7,filename,'unknown',ioerror)
      if (ioerror.lt.0) go to 950
c
c  write heading on output
c
      write(7,*)' '
      write(7,*)'********* getjt92 for ',strmid,'**********************'
      write(7,*)' '
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b",
     1      strmid(1:4), century, strmid(5:6), ".dat"
      write(7,*) 'filename:',filename
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
c  now find the current, -12, and -24 hr positions
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


   45 continue
      close (92)
      if (ilat(3).eq.0) then
	 write(7,*) "GETJT92: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
	 stop "GETJT92: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
      endif

    7 continue

   20 continue


      write(7,*) " "
      write(7,*) " ldtg = ",ldtg(1), ldtg(2), ldtg(3)
      write(7,*) " "
c
c  reformat the century for retrieval
c
      read(cent,'(i2)')icentury


c
c  open database for read
c
      write(*,*) 'open TEDS'
      call ted_open(ierr)
      if (ierr.ne.0) then
	  call ted_stop(ierr)
	  stop
      endif

      do 850 k=1,7
c        loop 7 times (for the 0,12,24,36,48,60 and 72 hour forecasts)
c           -- this should be 100 and 1000, but FNMOC assigns wrong --
            lvl1=10
   	    lvl2=100
	    parm=1
            read(ldtg(1),'(4i2)')mdate(1),mdate(2),mdate(3),mdate(4)
            cdtg=ldtg(1)  
            ntau=(k-1)*12
            write(7,*)'k:',k
c
c  itry is a counter for how many times to try to get 72 hr fields
c
            itry=0

   70       continue
cx          write(6,*) ' '
cx          write(6,*)'cdtg:',cdtg,' ntau:',ntau,' dlm heights'
 	    write(7,*) ' '
            write(7,*)'icentury cdtg:',icentury,cdtg,' ntau:',ntau
            write(7,*)' lvl1:',lvl1,' lvl2:',lvl2,' parm:',parm
            write(7,*) 'mdate:',mdate
  	    call get_polar(icentury,mdate,lvl1,lvl2,parm,ntau,f,ierr)
	    if(ierr.ne.0) then
                if(ntau.gt.78) then
                   write(6,*)'***********************************'
                   write(6,*)'*****getjt92:field unavailable*****'
                   write(6,*)'*****getjt92:try again later*******'
                   write(6,*)'***********************************'
                   write(7,*)'***********************************'
                   write(7,*)'*****getjt92:field unavailable*****'
                   write(7,*)'*****getjt92:try again later*******'
                   write(7,*)'***********************************'
                   close (7)
cx      remove partly constructed file
                   write (command,*)"rm ",storms(1:ind),"/jt92.",ldtg(1)
                   call system(command)
                   call ted_stop (ierr)
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
     &                ' field=dlm heights'


  100       continue
C
  500    continue
  800    continue
c  write grids to file 
      if (k.eq.1)then 
       write(filename,'(a,a,a)')storms(1:ind),"/jt92.",ldtg(1)
       open (unit=9, file=filename,form="unformatted",err=950)
cx     write (9)  ldtg(1)
      endif
cx
cx  this is a kludge for screwed up projection onto NH Polar Stereo - some missing values!
      do 180 i=1,65
      do 180 j=2,64
        if(f(i,j) .lt. 0.0) f(i,j)= f(i,j-1)
  180 continue
cx
cx  Subtract the "average" value of dlm height from real values
cx  Charlie Neumann's published value is 6060.5
cx      
cx  At the same time, need to get mirror image of field
cx
      do 300 itemp=1,65
      do 200 jtemp=1,65
  	    f1(itemp,jtemp)=f(66-itemp,jtemp) - 6060.5
  200 continue
  300 continue
cx      
cx      
      do 310 j=2,64
      write(7,9021) (f1(i,j),i=2,64)
 9021 format(63f8.1,/)
  310 continue
     
      write (9) f1
  850 continue
      close (9)
      write(6,*) ' normal stop'
      write(7,*) ' normal stop'
      close (7)
      call ted_stop (sflag)
      stop
C
  950 continue
      write (*,*)'cannot open ', filename
      stop
C

      end
