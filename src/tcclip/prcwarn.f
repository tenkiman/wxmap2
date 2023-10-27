      program prcwarn
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  prcwarn
!
!  DESCRIPTION:  Process tropical cyclone warning messages that arrive
!                via AUTODIN or AWN
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  N/A
!
!  PARAMETERS:  none
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:
!    Command line argument:  $CRDATE - export of watch dtg
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!         List of major key words in a tropical warning message
!                               1         2         3
!                      12345678901234567890123456789012
!      data ckey(1)  /'O'/
!      data ckey(2)  /'FM'/
!      data ckey(3)  /'TO'/
!      data ckey(4)  /'BT'/
!      data ckey(5)  /'UNCLAS'/
!      data ckey(6)  /'SUBJ:'/
!      data ckey(7)  /'WARNING POSITION:'/
!      data ckey(8)  /'PRESENT WIND DISTRIBUTION:'/
!      data ckey(9)  /'REPEAT POSIT:'/
!      data ckey(10) /'FORECASTS:'/
!      data ckey(11) /'12 HRS, VALID AT:'/
!      data ckey(12) /'VECTOR TO 24 HR POSIT:'/
!      data ckey(13) /'24 HRS, VALID AT:'/
!      data ckey(14) /'VECTOR TO 36 HR POSIT:'/
!      data ckey(15) /'36 HRS, VALID AT:'/
!      data ckey(16) /'VECTOR TO 48 HR POSIT:'/
!      data ckey(17) /'EXTENDED OUTLOOK:'/
!      data ckey(18) /'48 HRS, VALID AT:'/
!      data ckey(19) /'VECTOR TO 72 HR POSIT:'/
!      data ckey(20) /'72 HRS, VALID AT:'/
!      data ckey(21) /'REMARKS:'/
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         bldumy      build dummy template of warning summary
!         chkltln     check lat/lon of position
!         cleanem     clean-up and look for key words
cx        dbstop      ISIS database close call
!         fndyrmo     obtain year and month of message
!         gonogo      determin if this is a tropical cyclone warning
!         lodem1a     load first part of line 1
!         lodem1b     load second part of line 1
!         lodem2      load second part of forecast line
!         lodemf      load first part of forecast line
!         origid      obtain originator code
!         prepmsg     prepare message for decoding
cx        pxfgetarg   obtain command line argument (CraySoft 90)
cx        getarg      obtain command line argument 
!         wrtmsg      write warning summary into ISIS
!         xychk       check for "X" or "Y" in summary
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         casum      char*240   array of amplifying remarks from WITHIN
!                               forecast section of warning - NOT from
!                               ending remarks of message
!         cmsg       char*80    processed warning message
!         cnnn       char*240   last line of summary
!         csdtg      char*10    computer watch dtg (00 or 12 Z for hour)
!         cwsum      char*240   processed warning message
!         cx         char*1     working character
!         fname      char*20    working file name
cx        includes   char*100   directory of file "atcfsite.nam"
!         iclen      integer    character length of argumnet
!         ier1a      integer    error flag from lodem1a
!         ier1b      integer    error flag from lodem1b
!         ier2       integer    error flag from lodem2
!         ierc       integer    error flag for command argument
!         ierck      integer    error flag from xychk
!         ierf       integer    error flag of forecast section
!         ierk       integer    error flag from chkltln
!         ierr       integer    error flag from prepmsg
!         iersf      integer    sum of errors from forecast sections
!         ierwr      integer    error flag from wrtmsg
cx        ind        integer    number of characters in a string
!         ioe        integer    I/O status flag
!         ire        integer    running errors, 1 per line
!         iyr        integer    year (YYYY) of tropical season
!         jump       integer    error flag for gonogo and fndyrmo
!         keys       integer    array of indicies of lines in message
!                               that contain key word(s)
!         ks         integer    starting character location
!         line       char*80    input line from file
!         lncnt      integer    line count of warning summary
!         msgk       integer    processed warning message count
!         na         integer    number of amplification lines (casum)
!         nd         integer    number of data lines in cwsum
!         nhyr       char*4     Northern hemisphere tropical season
!         nk         integer    number of keys found
!         nkmax      integer    maximum number of keys allowed
!         nll        integer    ending line number for search
!         nserr      integer    software error flag
!         nsl        integer    starting line number for search
!         nsmax      integer    working maximum length of upper part of
!                               summary (cwsum)
!         nwnd       integer    type of wind flag, 1 - analysis
!         nwsm       integer    number of warning summaries written
!         orgsta     char*4     sending organization station code
!         rxpln      char*240   RX+ line of message (real for AUTODIN,
!                               fake for AWN)
cx        siteid     char*4     site id for originator of message
cx        storms     char*100   directory of storm files         
!         shyr       char*4     Southern hemisphere tropical season
!         wmsg       char*80    warning message
!         wrnyr      char*4     warning tropical season year
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
cx  sampson, nrl oct 96  ... convert to ATCF 3.0
cx  A. Schrader, SAIC  6/98  ...  Modified to use new data format
cx  sampson Aug 98  changed to capture last wind radius in 4 quad 
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer nwlmax, nkeymx, nslmax
      parameter (nwlmax = 200,  nkeymx = 21,  nslmax = 10)
!
      integer lncnt, nkmax, nk, ierr, n, na, nd, nsl, nll, nsmax, nserr
      integer ier1a, ier1b, ier2, ierk, ierf, iersf, ire, k, ks, jump
      integer nwnd, iclen, ierc, msgk, nwsm, ierck, ierwr, ioe, iyr
      integer keys(nkeymx)
      character*1 cx
      character*4 orgsta, nhyr, shyr, wrnyr
      character*10 csdtg
      character*20 fname
      character*80 wmsg(nwlmax), cmsg(nwlmax-1)
      character*240 cwsum(nslmax), casum(nslmax), cnnn, rxpln
cx
      character*100 filename
      character*100 storms
      character*100 includes
      character*80  line
      character*6   strmid
      character*4   siteid
      character*2   century
      integer       ind
      integer       ioerror, iarg
cx
!
      equivalence (wmsg(2),cmsg(1))
! . . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . .
!
!                   open diagnostic file
!
      open (33,file='prcwarn.dig')
      write (33,*) ' DIAGNOSTICS of processing follow'
!
!                   obtain the watch dtg (YYYYMMDDHH) {HH= 00 or 12}
!                   as command line argument
!
cx    call pxfgetarg (1,csdtg,iclen,ierc)
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg (iarg,csdtg(3:10))
      iarg = iarg + 1
      iclen=10

cx  the following will only work until 2089!
      if (csdtg(3:3).eq.'9') then
	 csdtg(1:2)='19'
      else
	 csdtg(1:2)='20'
      endif

cx    if (ierc.eq.0 .and. iclen.eq.10) then
      if (csdtg(1:1).ne.' ' .and. csdtg(10:10).ne.' ') then
        write (*,*) 'PROCESSING tropical warnings on watch : ',csdtg
!
!                   set tropical cyclone season year
!                       nhyr - NH,  shyr - SH
!
        nhyr = csdtg(1:4)
        if (csdtg(5:6) .lt. '07') then
          shyr = nhyr
        else
          read (nhyr,'(i4)') iyr
          iyr = iyr +1
          write (shyr,'(i4)') iyr
        endif
      elseif (iclen .ne. 10) then
        write (*,*) 'MISSING full dtg, found : ',csdtg
        call exit (1)
!
      else
        write (*,*) 'MISSING command line CRDATE'
        call exit (1)
!
      endif
!
!               open input data file for either AUTODIN or AWN messages
!
cx
cx  get the storms directory name
cx
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cx
cx  get the storm id
cx
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c   get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
cajs  write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".wrn"
      write(filename,'(6a)') storms(1:ind), "/", 
     1     strmid(1:4), century, strmid(5:6), ".wrn"
cx    open (10,file='warnmsg',iostat=ioe,status='old',form='formatted')
      open (10,file=filename,iostat=ioe,status='old',form='formatted')
      if (ioe .ne. 0) then
        write (*,*) 'FAILED - MISSING input file'
        call exit (1)
!
      endif
!
!                   read in tropical cyclone warning message (AUTODIN
!                   or AWN) and prepare message for processing
!
      nserr = 0
      nkmax = nkeymx
      nsmax = nslmax
      msgk  = 0
      nwsm  = 0
!
!     skip first line in warning message,  ajs
!     need to have the "SUBJ:" line as the first line
!     instead of ,e.g., WTPN31 PGTW 250300.
!
!     read (10,'(a80)',iostat=ioe) line
!            top of processing loop, read messages till EOF
  100 continue
cx    if (msgk .gt. 0) pause 'msg end'
      if (msgk .gt. 0) print *, 'msg end'
!
      wrnyr = ' '
      fname = ' '
      ire   = 0
cx
cx  get the originating site name from atcfsite.nam
cx
      call getenv("ATCFINC",includes)
      ind=index(includes," ")-1
      write(filename,'(a,a)')includes(1:ind),"/atcfsite.nam"
      open (11,file=filename,err=720,status='old')
      rewind 11
cx    read (11,*) 
cx    read (11,'(a4)') siteid
   10 continue
      read (11,'(a80)') line
      if (line(1:13).ne.'START_OF_DATA')go to 10
      read (11,*)
      read (11,*)
      read (11,'(a4)')  siteid
      close(11)

      write(rxpln,'(a4,1x,a10,a2,1x,a4)')'ATCF',csdtg,'00',siteid
      call prepmsg (cmsg,nwlmax,lncnt,keys,nkmax,nk,rxpln,ierr)
      if (ierr .gt. 0) then
        write (*,*) 'prcwarn - internal SOFTWARE problem'
        write (33,*) ' prcwarn - internal SOFTWARE problem'
        if (nserr .eq. 0) then
          open (99,file='soft_error')
          write (99,'(" FAILED - prcwarn had software error")')
          rewind (99)
          close  (99)
          nserr = -1
        endif
        ierr = 0
      endif
      if (nk .gt. 6) then
        wmsg(1) = rxpln(1:80)
        msgk    = msgk +1
        write (fname,'("msg.inl.",i2.2)') msgk
        open (66,file=fname)
        do n=1, lncnt +1
          write (66,'(i4,2x,a70)') n, wmsg(n)
        enddo
        close (66)
        fname = ' '
        if (nk .gt. 0) then
!
!                   one or more key word(s) were found
!
          write (fname,'("keys.inl.",i2.2)') msgk
          open (53,file=fname)
          do k=1, nk
            if (keys(k).gt.0 .and. keys(k).lt.200) then
              write (53,'(i3,3x,i3,2x,a60)') k, keys(k),
     &                   cmsg(keys(k))(1:60)
            else
              write (53,'(i3,3x,i3,3x,"missing")') k, keys(k)
            endif
          enddo
          close (53)
          fname = ' '
!
!                   See if message is a tropical warning
!
          call gonogo (cmsg,lncnt,keys,nk,jump)
          if (jump .le. 0) then
            write (*,*) 'This is NOT a tropical cyclone message.'
            write (33,*) 'This is NOT a tropical cyclone message.'
            if (ierr .eq. 0) goto 100
!
          endif
!
!                     process tropical cyclone warning message
!
          write (*,*) 'Processing warning, found ',jump,' key strings'
          write (33,*) 'Processing warning, found ',jump,' key strings'
          cnnn = rxpln
          if (keys(1).gt.0 .and. keys(1).lt.nwlmax) then
!
!                   obtain warning message year and month
!                   check with dtg (year and month) of receipt
!                   note, at this time cnnn is ODR RX+ or AWN line
!
            call fndyrmo (cmsg(keys(1)),csdtg,cnnn,jump)
            if (jump .lt. 0) then
!
!                   if jump less than zero, BAD dtg of release
!
              write (*,*) 'BAD release message dtg in header'
              write (33,*) 'BAD release message dtg in header'
              if (ierr .eq. 0) goto 100
!
            endif
          else
!                   load cnnn with missing message dtg flags
!
            cnnn = 'NNNN XXXX XXXXXXXXXXXX ' // rxpln(18:31)
          endif
!
!                   perform clean-up work and look for key words
!
          call cleanem (cmsg,lncnt,keys,nk)
          write (33,*)
          write (33,*) ' KEYS found during processing message'
          do k=1, 21
            if (keys(k).gt.0 .and. keys(k).lt.nwlmax) then
              write (33,'(i4,2x,a60)') keys(k), cmsg(keys(k))(1:60)
!             write (*,'(i3,2x,i2,2x,a60)') k, keys(k),
!    &                  cmsg(keys(k))(1:60)
            endif
          enddo
          write (33,*)
          fname = ' '
!
!                   Build warning summary template
!
          call bldumy (cmsg,lncnt,keys,nk,cwsum,nsmax,nd)
          write (*,*) ' Built ',nd,' warning summary template lines'
          do n=1, nd
            write (*,*) cwsum(n)(1:60)
            write (33,*) cwsum(n)(1:60)
            casum(n) = ' '
          enddo
          write (33,*)
          write (33,*) 'bldumy built ',nd,' warn-sum lines'
          write (33,*)
!
!                   obtain originator's id
!
          call origid (cmsg(2),orgsta)
          write (6,*) 'processing msg fm ',orgsta
          write (33,*) ' processing msg fm ',orgsta
          cnnn(6:9) = orgsta
!
!               start replacing template values with extracted values
!
          write(*,*) 'STARTING ire= ',ire
          if (keys(6) .gt. 0) then
!
!                   set starting (nsl) and ending (nll) message lines
!                   to screen
!
            nsl = keys(6) +1
            if (keys(7) .gt. 0) then
              nll = keys(7) -1
            else
              nll = nsl +5
            endif
!
!                   parse first part of warning summary header
!
            call lodem1a (cmsg,lncnt,nsl,nll,orgsta,cwsum(1),ier1a)
            if (ier1a .gt. 0) ire = ire +1
            if (ier1a.ne.0) write(33,*) 'ier1a= ',ier1a,' ERROR= ',ire
          endif
          if (keys(7) .gt. 0) then
!
!                   set starting (nsl) and ending (nll) message lines
!                   to screen
!
            nsl = keys(7) +1
            if (keys(8) .gt. 0) then
              nll = keys(8) -1
            else
              nll = nsl +5
            endif
!
!                   parse second part of warning summary header &
!                   first part of initial position data
!
            call lodem1b (cmsg,lncnt,nsl,nll,csdtg,cnnn,cwsum(1),       &
     &                    cwsum(2),ier1b)
!
!                ierb1 is less than zero if:
!                     summary has been found in history
!                     dtg is outside of window for processing
!
            if (ier1b .lt. 0) then
!             nogo = -1
              goto 100
!
            elseif (ier1b .gt. 0) then
              ire = ire +1
            endif
            if (ier1b.ne.0) write(33,*) 'ier1b= ',ier1b,' ERROR= ',ire
          endif
          if (keys(8) .gt. 0) then
            nsl = keys(8) +1
            if (keys(9) .gt. 0) then
              nll = keys(9) -1
            else
              nll = nsl +5
            endif
            nwnd = 1
!
!                   parse second part of initial position data
!
            call lodem2 (cmsg,lncnt,nsl,nll,nwnd,cwsum(2),casum(1),
     &                   ier2)
            write (33,*) 'RESULTS:'
            write (33,'(a240)') cwsum(2)
            if (casum(1)(11:11) .ne. ' ') then
              casum(1)(5:9) = '000HR'
              write (33,'(a240)') casum(1)
            endif
          else
            ier2 = -1
          endif
          if (ier2 .ne. 0) ire = ire +1
          if (ier2 .ne. 0) write(33,*) 'ier2= ',ier2,' ERROR= ',ire
          if (keys(9) .gt. 0) then
            nsl = keys(9)
            if (keys(10) .gt. 0) then
              nll = keys(10) -1
            else
              nll = nsl
            endif
!
!                   Check that repeat of initial position agrees with
!                   initial position
!
            call chkltln (cmsg,lncnt,nsl,nll,cwsum(2),ierk)
          else
            ierk = -1
          endif
          if (ierk .eq. 0) then
!
!                   set warning year for ISIS
!
            if (cwsum(2)(9:9) .eq. 'N') then
              wrnyr = nhyr
            else
              wrnyr = shyr
            endif
          else
            ire = ire +1
          endif                                                                 
          if (ierk.ne.0) write(33,*) 'ierk= ',ierk,' ERROR= ',ire                              
!                                                                               
!                   3 => keys(11)  tau 12 data                                  
!                   4 => keys(13)  tau 24 data                                  
!                   5 => keys(15)  tau 36 data                                  
!                   6 => keys(18)  tau 48 data
!                   7 => keys(20)  tau 72 data
!
          iersf = 0
          do n=3, nd
            if (n .eq. 3) then
              ks = 11
            elseif (n .eq. 4) then
              ks = 13
            elseif (n .eq. 5) then
              ks = 15
            elseif (n .eq. 6) then
              ks = 18
            elseif (n .eq. 7) then
              ks = 20
            else
              ks = -1
            endif
!
!                   set count of forecast data errors to zero
!
            ierf = 0
            if (ks .gt. 10) then
              if (keys(ks) .gt. 0) then
!
!                   set starting and ending lines to scan
!
                nsl = keys(ks)
                if (keys(ks+1) .gt. 0) then
                  nll = keys(ks+1) -1
                elseif (keys(ks+2) .gt. 0) then
                  nll = keys(ks+2) -1
                elseif (keys(21) .gt. 0) then
cx  changed to capture last wind radius in 4 quad  ... sampson Aug 98
cx		  nll = nsl +5
                  nll = nsl +6
                  if (nll .ge. keys(21)) nll = keys(21) -1                      
                else                                                            
cx  changed to capture last wind radius in 4 quad  ... sampson Aug 98
cx		  nll = nsl +5
                  nll = nsl +6
                  if (nll .ge. lncnt) nll = nll -3                              
                endif                                                           
!                                                                               
!                   parse all forecast data                                     
!                                                                               
                print *, 'before lodemf, nsl and nll =',nsl,nll                 
                print *, 'before lodemf, ks and keys(ks)=',ks,keys(ks)          
                print *, 'before lodemf, keys(ks+1)=',keys(ks+1) 
                print *, 'before lodemf, keys(ks+2)=',keys(ks+2)          
                call lodemf (cmsg,lncnt,nsl,nll,orgsta,cwsum(n),        &       
     &                       casum(n-1),ierf)                                   
                if (wrnyr .eq. ' ') then                                        
!                                                                               
!                     set warning year for ISIS                                 
!                                                                               
                  if (cwsum(n)(9:9) .ne. 'Y') then                              
                    if (cwsum(n)(9:9) .eq. 'N') then                            
                      wrnyr = nhyr                                              
                    elseif (cwsum(n)(9:9) .eq. 'S') then                        
                      wrnyr = shyr                                              
                    endif                                                       
                  endif                                                         
                endif                                                           
                if (casum(n-1)(11:11) .ne. ' ')                         &       
     &              casum(n-1)(5:9) = cwsum(n)(2:4) // 'HR'                     
                iersf = iersf +ierf                                             
              else                                                              
                write(*,*) 'Missing key for ks= ',ks                            
              endif                                                             
            endif                                                               
          enddo                                                                 
          write (*,*)                                                           
          write (*,*) 'found ',iersf,' errors in forecasts'                     
          write (33,*)                                                          
          write (33,*) 'found ',iersf,' errors in forecasts'                    
          if (iersf .ne. 0) ire = ire +1                                        
cx        if (casum(1)(5:5) .eq. ' ') then                                      
cx          na = 0
cx        else                                                                  
cx          na = 1                                                              
cx        endif                                                                 
cx  for ATCF, always produce AMP line
	  na = 1
	  casum(1)(1:3) = 'AMP'

          do n=na +1, nd -1                                                     
            if (casum(n)(5:5) .ne. ' ') then                                    
              na = na +1                                                        
              if (na .ne. n) casum(na) = casum(n)                               
              if (na .eq. 1) casum(1)(1:3) = 'AMP'                              
            endif                                                               
          enddo                                                                 
!                                                                               
!                   check that warning year has been set for ISIS               
!                                                                               
          if (wrnyr .eq. ' ') then                                              
!                     check for hemisphere, based upon basin                    
            cx = cwsum(1)(14:14)
            if (cx .ne. 'Y') then                                               
              if (cx.ne.'S' .and. cx.ne.'P') then                               
                wrnyr = nhyr                                                    
              else                                                              
                wrnyr = shyr                                                    
              endif                                                             
            else                                                                
              wrnyr = '0000'                                                    
            endif                                                               
          endif                                                                 
!                                                                               
!                  write tropical cyclone warning message to ISIS               
!                                                                               
          call wrtmsg (wmsg,lncnt+1,cwsum(1),cnnn,csdtg,wrnyr,keys,             
     &                 nk,ierwr)
          if (ierwr .ne. 0) then                                                
            write (*,*) 'WARNING: error in ISIS write of message'               
            write (33,*) 'WARNING: error in ISIS write of message'              
          endif                                                                 
!                                                                               
!                   open output warning summaries file                          
!                   (the next program will write them to ISIS)                  
!                                                                               
cx        if (nwsm .eq. 0) open (44,file='warnsum')                             
	  ind=index(storms," ")-1
cajs      write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".sum"
          write(filename,'(6a)') storms(1:ind), "/", 
     1         strmid(1:4), century, strmid(5:6), ".sum"
cx        if  (nwsm .eq. 0) open (44,file=filename)
          if (nwsm .eq. 0) then
                 call openfile (44,filename,'unknown',ioerror)  
          endif                           
!                                                                               
!                   perform final check for errors in summary                   
!                                                                               
          call xychk (cwsum,nd,casum,na,ierck)
          if (ierck.ne.0 .and. ire.eq.0) ire = 1
          if (ierck.ne.0) write(33,*) 'ierck= ',ierck,' ERROR= ',ire
          write (*,*)                                                           
          write (*,*) 'prcwarn ',ire,' total errors in message'                 
          write (*,*)                                                           
          write (33,*)                                                          
          write (33,*) ' prcwarn ',ire,' total errors in message'               
          write (33,*)                                                          
!                                                                               
!                   write warning summary, initial and forecast data            
!                                                                               
          do n=1, nd                                                            
            write (*,*) cwsum(n)(1:60)                                          
            write (33,*) cwsum(n)(1:80)                                         
            write (44,9240) cwsum(n)                                            
          enddo                                                                 
 9240     format (a240)                                                         
!                                                                               
!                   write warning summary, amplification data                   
!                                                                               
          do n=1, na                                                            
            write (*,*) casum(n)(1:60)
            write (33,*) casum(n)(1:80)
            write (44,9240) casum(n)
          enddo
!
!                   put source of message on ending line
!
          if (wmsg(1)(1:3) .eq. 'AWN') then
            cnnn(39:41) = 'AWN'
          else
            cnnn(39:41) = 'AUT'
          endif
          cnnn(43:44) = 'NE'
          if (ire .gt. 99) ire = 99
          write (cnnn(45:46),'(i2.2)') ire
!
!                   write warning summary, ending signal/data
!
          write (*,*) cnnn(1:60)
          write (33,*) cnnn(1:80)
          write (44,9240) cnnn
          write (33,*)
          nwsm = nwsm +1
        else
          write (*,*) 'This is not a warning'
          write (33,*) ' prcwarn - this is not a warning'
        endif
      endif
      if (ierr .eq. 0) then
!                   look for another message
        goto 100
!
      elseif (ierr .ne. -99) then
        write (*,*) 'Error processing message - abort'
        write (33,*) ' prcwarn, Error processing message - abort'
      else
!                   EOF reached with good processing
        ierr = 0
      endif
      if (nwsm .gt. 0) then
        rewind (44)
        close  (44)
        write (*,*) 'MUST process ',nwsm,' summaries'
        write (33,*) ' MUST process ',nwsm,' prcwarn summaries'
      endif
      rewind (33)
      close  (33)
cx    call dbstop
      if (ierr .eq. 0) then
        write (*,*) 'COMPLETED OK - prcwarn'
      else
        write (*,*) 'COMPLETED with I/O error - prcwarn'
        open (99,file='io_error')
        write (99,'(" FAILED - prcwarn had I/O error")')
        rewind (99)
        close  (99)
      endif
      stop
cx    call exit (0)
cx  
  720 continue
      write (*,*) 'Input site ID information file not available.'
      stop 2

!
      end
      subroutine awnchk (card,keep)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  awnchk
!
!  DESCRIPTION:  Check that card is header line for AWN message
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  none
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  see method 1) for restrictions
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call awnchk (card,keep)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*80          in     line of message
!    keep            integer          out    flag 0 - not AWN
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!     Example of AWN header line of tropical warning:
!                      1            < for reference
!             123456789012345678    < for reference
!             WTPS31 PGTW 201500    < header line
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!      Name              Description
!    ---------       --------------------------------------------------
!     uponly         Ensure all characters are upper case
!     lftjust        Ensure all data is left justified
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     -------    -----------------------------------------
!         na         integer    count of alpha characters
!         nn         integer    count of digit characters
!
!  METHOD:  1) data on card has been left justified and put in upper
!              case prior to calling this S/R
!           2) check for matching pattern of characters and integer
!              for AWN header line
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f90/f77 with some f90 extentions
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer keep
      character card*80
!
      integer n, na, nn
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      call uponly (card)
      call lftjust (card,keep)
      if (keep .ne. 0) then
        keep = 0
        na   = 0
        nn   = 0
        do n=1, 6
          if (card(n:n).ge.'A' .and. card(n:n).le.'Z') then
            na = na +1
          elseif (card(n:n).ge.'0' .and. card(n:n).le.'9') then
            nn = nn +1
          endif
        enddo
        if (na.eq.4 .and. nn.eq.2) then
          do n=8, 11
            if (card(n:n).ge.'A' .and. card(n:n).le.'Z') na = na +1
          enddo
          if (na .eq. 8) then
            do n=13, 18
              if (card(n:n).ge.'0' .and. card(n:n).le.'9') nn = nn +1
            enddo
            if (nn .eq. 8) keep = -1
          endif
        endif
      endif
      return
!
      end
      subroutine bldumy (cmsg,lncnt,key,nk,cwsum,nsmax,nd)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  bldumy
!
!  DESCRIPTION:  Build X/Y template of tropical cyclone warning summary,
!                (header and position lines, only)
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  none
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call bldumy (cmsg,lncnt,key,nk,cwsum,nsmax,nd)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        input    TC warning message
!    cwsum           char*240       output   X/Y tmplate of summary
!    key             integer        input    array of key-lines
!    lncnt           integer        input    line count of cmsg
!    nd              integer        output   number of data lines in sum
!    nk              integer        input    number of keys
!    nsmax           integer        input    maximum summary line count
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!***************     Explanation of first line in summary     **********
!
!        Symbolic example of first line of summary, with column numbers
!
!                 111111111122222222223333333333444444
!        123456789012345678901234567890123456789012345..............
!        YYYYMMDDHH IDB NAME       WNRA NC DEG KT METH ---- ACC
!                       1234567890
!
!                  Explanation of symbols, left to right
!
!      YYYYMMDDHH - DATE-TIME-GROUP of initial position
!             IDB - CYCLONE IDENTIFICATION, number and origin basin
!            NAME - NAME or "NONAME" of tropical cyclone
!            WNRA - WARNING NUMBER - three digits and a character,
!                   this charcater may be a blank character
!              NC - NUMBER OF TROPICAL CYCLONES in present basin
!             DEG - TRACK OF CYCLONE last 6/12 hours, degrees
!              KT - SPEED OF CYCLONE last 6/12 hours, kts
!            METH - METHODS OF LOCATION, four characters for each method
!                     SATL - satellite
!                     RADR - radrar
!                     SYNP - synoptic data
!                     AIRC - aircarft
!                     XTRP - extrapolation
!                     OTHR - other
!            ---- - more than one method may be specified
!             ACC - ACCURACY of initial position, nm
!
!***********       Explanation of position line of summary        *****
!
!     Symbolic example of position line of summary, with column numbers
!
!                 1111111111222222222233333333334444
!        1234567890123456789012345678901234567890123...............
!        THHH LAT  LON   MXW RSPD NMI DD ---
!
!                  Explanation of symbols, left to right
!
!          T - TAU of position flag
!        HHH - valid hours of position
!        LAT - LATITUDE  and N or S for hemisphere, degrees and tenths
!        LON - LONGITUDE and E OR W for hemisphere, degrees and tenths
!        MXW - MAXIMUM SUSTAINED WIND SPEED, kts
!       RSPD - R is a flag for radius and SPD is wind speed, in kts
!        NMI - RADIUS IN NM of SPD winds
!         DD - DESCRIPTION of radius, two characters - OPTIONAL
!                DD allowed abreviations:
!                   NN, NE, EE, SE, SS, SW, WW, NW - DIRECTION
!                   QD - QUADRANT
!                   SC - SEMICIRCLE
!                   EW - ELSEWHERE
!                   OW - OVER WATER
!                   OL - OVER LAND
!        --- - Note: may be several NMI DD sets after each RSPD, and
!                    there may be several RSPD NMI DD SETS for each tau
!
!*********   Explanation of amplification lines in summary     *********
!
!   Symbolic example of first line of amplification, with column numbers
!
!                  1111111111222222222233333333334444
!         1234567890123456789012345678901234567890123...............
!         AMP ZZZHR < COMMENTS FOR TAU ZZZ >
!
!         AMP - START OF AMPLIFICATION SECTION, on first line only
!       ZZZHR - ZZZ is the TAU of amplification in the message
!
!   Symbolic example of subsequent first lines of amplification, with
!            column numbers
!
!                  1111111111222222222233333333334444
!         1234567890123456789012345678901234567890123...............
!             ZZZHR < COMMENTS FOR TAU ZZZ >
!
!       ZZZHR - ZZZ is the TAU of amplification in the message
!
!
!   Note: ampifications in the summary come from within the warning
!         not from the remarks section of the message.
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         chead      char*80    dummy X/Y heading
!         ctxx       char*80    dummy X/Y position line
!
!  METHOD: N/A
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f90 or f77 with f90 extensions
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lncnt, nk, nsmax, nd
      integer key(nk)
      character*80 cmsg(lncnt)
      character*240 cwsum(nsmax)
!
!         local variables
      integer n
      character*80 chead, ctxx
!
!                          1         2         3         4
!                 1234567890123456789012345678901234567890123456789
!                 YYYYMMDDHH IDB NAME       NRWA NC DEG KT METH ACC
      data chead/'XXXXXXXXXX XXY Y          XXXY XX XXX XX YYYY XXX'/
!                                1234567890
!
!                         1         2         3         4
!                1234567890123456789012345678901234567890123............
!                TAU  LAT  LON   MXW RSPD NMI DD --- '
      data ctxx/'TXXX XXXY XXXXY XXX '/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cwsum(1) = ' '
      cwsum(1)(1:80) = chead
      cwsum(2) = ' '
      cwsum(2)(1:80) = 'T000' // ctxx(5:80)
      nd = 2
      do n=7, nk
        if (key(n) .gt. 0) then
          if (cmsg(key(n))(4:16) .eq. 'HRS, VALID AT') then
!                   good for forecasts out to 99 hours
            nd = nd +1
            if (nd .le. nsmax) then
              cwsum(nd) = ' '
              cwsum(nd)(1:80) = ctxx
              cwsum(nd)(2:4)  = '0' // cmsg(key(n))(1:2)
            endif
          elseif (cmsg(key(n))(5:17) .eq. 'HRS, VALID AT') then
!                   good for forecasts greater than 99 hours
            nd = nd +1
            if (nd .le. nsmax) then
              cwsum(nd) = ' '
              cwsum(nd)(1:80) = ctxx
              cwsum(nd)(2:4)  = cmsg(key(n))(1:3)
            endif
          endif
        endif
      enddo
      if (nd .gt. nsmax) then
        write (*,*) ' prcwarn, cwsum array too small'
        write (33,*) 'Array for cwsum too small...'
        nd = nsmax
      endif
      return
!
      end
      subroutine chkcrp (word,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  chkcrp
!
!  DESCRIPTION:  Check for end of radius description(s)
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call chkcrp (word,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ---------------------------
!    ierr            integer        output   error flag, 0 - match found
!    word            char*20        input    word to be checked
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     -------    -----------------------------------------
!         keys       char*10    array of valid names
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  fortran 77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer ierr
      character*20 word
!
!         local variables
      integer n
      character*10 keys(5)
!
      data keys(1)/'REPEAT    '/
      data keys(2)/'FORECASTS '/
      data keys(3)/'VECTOR    '/
      data keys(4)/'EXTENDED  '/
      data keys(5)/'REMARK    '/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr = -1
      do n=1, 5
        if (word(1:5) .eq. keys(n)(1:5)) ierr = 0
      enddo
      return
!
      end
      subroutine chkhist (cdtg,cid,cnrb,cname,cnnn,kont)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  chkhist
!
!  DESCRIPTION:  Check history for warning summary
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  ISIS Message Data Database User's Guide (FNMOC)
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  FNMOC system with ISIS
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call chkhist (cdtg,cid,cnrb,cname,cnnn,kont)
!
!  PARAMETERS:
!    Name          Type        Usage           Description
!    ------      ---------    -------   ---------------------------
!    cdtg        char*10       input    cyclone position dtg
!    cid         char*3        in/out   cyclone ID  /Atlantic only
!    cname       char*10       input    cyclone name
!    cnnn        char*240      input    NNNN line of summary
!    cnrb        char*4        input    cyclone warning number
!    kont        integer       output   flag for continuation,
!                                       0 - found match, DO NOT continue
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:
!       Name             Table        Usage            Description
!    ----------     --------------  ---------   ------------------------
!      ISIS            TC            output     TC warning summaries
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!     Template of cnnn character string:
!                  1         2         3         4
!         123456789012345678901234567890123456789012345678901234567890
!         NNNN ORIG YYYYMMDDHHmm YYYYMMDDHHmmss CIR
!
!     Template of chist(1):
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         yyyymmddhh idb name       nrw nc deg kt meth ---- acc
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         scrnxy      screen for "X" or "Y"
!
!  LOCAL VARIABLES:
!        Name        Type                 Description
!       ------       --------   ----------------------------------------
!       arvl_dtg     char*14    message arrival dtg (YYYYMMDDHHmmss)
!       chist        char*240   summary array from history
!       clasif       char*8     classification in ISIS
!       com_cir      char*24    communications circuit (AUTODIN/AWN)
!       enc_typ      char*24    type of encoding for ISIS
!       ierrd        integer    local ISIS read error flag, 0 - no error
!       ierr_rd      integer    ISIS completion flag
!       ierxy        integer    X/Y error flag, 0 - no error
!       in_msg_id1   char*32    cyclone number & basin of origin
!       in_msg_id2   char*32    dtg of first position (YYYYMMDDHH)
!       in_msg_id3   char*32    warning number & amendment letter
!       in_msg_id4   char*32    cyclone name
!       in_msg_id5   char*32    ISIS identification #5, not used
!       in_msg_typ   char*24    ISIS message sub_type
!       msg_dtg      char*16    dtg of message (YYYYMMDDHHmm)
!       msg_typ      char*24    ISIS message type
!       nm           integer    number of input parameters
!       nr           integer    number of summaries read
!       nslmax       integer    maximum number of lines in a summary
!       num_byte     integer    number of bytes - characters
!       org_tx       char*32    originating transmission source
!       out_msg_id1  char*32    ISIS identification #1
!       out_msg_id2  char*32    ISIS identification #2
!       out_msg_id3  char*32    ISIS identification #3
!       out_msg_id4  char*32    ISIS identification #4
!       out_msg_id5  char*32    ISIS identification #5
!       out_msg_typ  char*24    ISIS message sub_type
!       status       char*8     requested status of processing
!       status_out   char*8     status of processing
!       w_dtg        char*10    requested watch dtg of message
!       w_dtg_out    char*10    watch dtg of message
!
!  METHOD:  N/A
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f90 or f77 with f90 extensions
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer nslmax
      parameter (nslmax = 20)
!
      integer kont
      character cdtg*10, cid*3, cnrb*4, cname*10, cnnn*240
!
      integer ierxy, ierrd, n, nm, nr, ls
!
!                   ISIS MSG_RD parameters
!         INPUT:
!     integer num_byte  < NOT DOCUMENTED as required input >
      character*8  clasif
      character*8  status
      character*10 w_dtg
      character*24 msg_typ, in_msg_typ
      character*32 in_msg_id1, in_msg_id2, in_msg_id3, in_msg_id4
      character*32 in_msg_id5
!
!         OUTPUT:
      integer num_byte, ierr_rd
      character*8 status_out
      character*10 w_dtg_out
      character*14 arvl_dtg
      character*16 msg_dtg
      character*24 out_msg_typ, com_cir, enc_typ
      character*32 out_msg_id1, out_msg_id2*32, out_msg_id3, out_msg_id4
      character*32 out_msg_id5, org_tx
      character*240 chist(nslmax)
!
      data msg_typ/'TC'/
!                   do NOT search WRNG_SMRY_ERROR
      data in_msg_typ/'WRNG_SMRY_INDIV'/
!                   the 5th id is not used in MSG_RD for this message
!                   sub_type, so set to underbar to represent "blank"
      data in_msg_id5/'_'/
      data clasif/'UNCLASS'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (*,*) 'HIST checking: ',cid,'  ',cname,' warning ',cnrb
      write (*,*) ' for ',cdtg,' nnnn: ',cnnn(1:41)
!                   set kont for continuation - no match found
      kont = -1
!
!                   set input parameters for WRNG_SMRY_INDIV
!
      nm = 0
      call scrnxy (cid,3,ierxy)
      if (ierxy .eq. 0) then
!                   tropical cyclone ID - number and original basin
        in_msg_id1 = cid
      else
        in_msg_id1 = '*'
        nm = 1
      endif
      call scrnxy (cdtg,10,ierxy)
      if (ierxy .eq. 0) then
!                   dtg of initial position in warning - YYYYMMDDHH
        in_msg_id2 = cdtg
!                   try to fix problem caused by NEOC, see below
        if (cid .eq. 'XXL') in_msg_id2 = '*'
      else
        in_msg_id2 = '*'
        nm = nm +1
      endif
      call scrnxy (cnrb,4,ierxy)
      if (ierxy .eq. 0) then
!                   tropical warning number, include amendment
!                   modification letter (021 , 021A, 021B, etc)
        in_msg_id3 = cnrb
!                   set trailing blank to underbar
        if (in_msg_id3(4:4) .eq. ' ') in_msg_id3(4:4) = '_'
      else
        in_msg_id3 = '*'
        nm = nm +1
      endif
      if (cname(1:2) .ne. 'Y ') then
!                   tropical cyclone name
        in_msg_id4 = cname
      else
        in_msg_id4 = '*'
        nm = nm +1
      endif
      w_dtg = cdtg
      if (w_dtg(9:10) .eq. '06') then
        w_dtg(9:10) = '00'
      elseif (w_dtg(9:10) .eq. '18') then
        w_dtg(9:10) = '12'
      endif
      status = '*'
      nr = 0
!
  100 continue
      num_byte = nslmax*240
      write(*,*) 'CALLING msg_rd'
      write(*,*) 'msg_typ=',msg_typ,' in_msg_typ=',in_msg_typ
      write(*,*) 'id1=',in_msg_id1,' id2=',in_msg_id2
      write(*,*) 'id3=',in_msg_id3,' id4=',in_msg_id4
      write(*,*) 'clasif=',clasif,' bytes= ',num_byte
cx  disabled !
cx    pause
cx    call msg_rd (msg_typ,in_msg_typ,in_msg_id1,in_msg_id2,in_msg_id3, &
cx   &             in_msg_id4,in_msg_id5,clasif,w_dtg,status,
cx   &             out_msg_typ,                                         &
cx   &             out_msg_id1,out_msg_id2,out_msg_id3,out_msg_id4,     &
cx   &             out_msg_id5,num_byte,chist,w_dtg_out,msg_dtg,        &
cx   &             arvl_dtg,org_tx,com_cir,status_out,enc_typ,ierr_rd)
      write(*,*) 'BACK from msg_rd'
      nr = nr +1
      if (ierr_rd .lt. 0) then
!                   ISIS read error
        ierrd = -1
      elseif (ierr_rd .eq. 100) then
!                   ISIS no find signal
        if (nr .eq. 1) then
          write (*,*) 'NO WARNING SUMMARY FOUND'
          ierrd = 90
        else
          write (*,*) 'NO MORE SUMMARIES FOUND'
          ierrd = 99
        endif
      else
!                   good ISIS read
        ierrd = 0
      endif
      if (ierrd .eq. 0) then
!
!                   check summary for match
!
        if (nm .eq. 0) then
!                   signal that a match has been found
          kont = 0
        else
          if (cnnn(11:22) .ne. 'XXXXXXXXXXXX') then
!                   the msg dtg should be good
            ls = num_byte/240 -3
            do n=ls, num_byte/240
              if (chist(n)(1:4) .eq. 'NNNN') then
!                   see if originator and msg dtg matches
                if (chist(n)(1:22) .eq. cnnn(1:22)) kont = 0
              endif
            enddo
          endif
          if (kont.ne.0 .and. cid(1:3).eq.'XXL') then
!                   try to fix problem of NEOC not including number
!                   with named tropical cyclones
            if (chist(1)(14:14).eq.'L' .and.                            &
     &          chist(1)(16:21).ne.'NONAME') then
!                  1         2         3         4
!         123456789012345678901234567890123456789012345678901234567890
!         yyyymmddhh idb name       wrna nc deg kt meth ---- acc
!                        1234567890
              if (cname .eq. chist(1)(16:25)) then
!
!                   found Atlantic cyclone with same name
!
                cid = chist(1)(12:14)
                in_msg_id1 = cid
                call scrnxy (cdtg,10,ierxy)
                if (ierxy .eq. 0) in_msg_id2 = cdtg
              endif
            endif
          endif
        endif
      elseif (ierrd .ge. 90 ) then
!                   no more summaries to read
        goto 200
!
      else
!                   ISIS read error
        write (*,*) '**** ISIS error is ',ierr_rd
        goto 200
!
      endif
!                   jump to read next summary, if no match
!
      if (kont .ne. 0) goto 100
!
  200 continue
      return
!
      end
      subroutine chkltln (cwmsg,lng,nsl,nll,cwsum,ir3)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  chkltln
!
!  DESCRIPTION:  Check initial position latitude and longitude with
!                REPEAT position
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call chkltln (cwmsg,lng,nsl,nll,cwsum,ir3)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwmsg           char*80        input    cyclone warning message
!    cwsum           char*240       input    position line of warning summary
!    ir3             integer        output   error flag, 0 - no error
!    lng             integer        input    length of message
!    nll             integer        input    ending search line in message
!    nsl             integer        input    starting search line in message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                      ACTION
!     ----------------------------     ----------------------------
!     repeat and initial positions     set error flag and exit
!     are not the same
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         extncn      extract number, character and number with no separations
!         numbck      check that check sum is correct
!         omitpd      omit period embedded in character numbers
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cew        char*1     east-west hemisphere indicator
!         chkn       char*1     check-sum number
!         cns        char*1     north-south hemisphere indicator
!         i3         integer    number 3
!         i4         integer    number 4
!         i5         integer    number 5
!         ierr2      integer    error flag for latitude checking
!         ierr3      integer    error flag for longitude checking
!         ire        integer    sum of errors found
!         kl         integer    last character positioned used
!         ks         integer    starting character position for search
!         nl         integer    number of line in message for processing
!         word       char*10    working character string for lat/lon
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  none
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lng, nsl, nll, ir3
      character cwmsg(lng)*80, cwsum*240
!
!         local variables
      integer i3, i4, i5, ierr2, ierr3, ire, kl, ks, nl, n
      character*1 cns, cew, chkn
      character*10 word
!
      data i3/3/, i4/4/, i5/5/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (33,*) 'into chkltln to process: '
      do n=nsl, nll
        write (33,'(i3,1x,a70)') n,cwmsg(n)(1:70)
      enddo
      write (33,*)
!
!                   extract repeat initial latitude
!
      nl   = nsl
      ks   = 10
      ire  = 0
      word = ' '
!
!                               lat  n/s cknum
      call extncn (cwmsg(nl),ks,word,cns,chkn,kl,ierr2)
      if (ierr2 .eq. 0) then
!
!                   check validity of check-sum number
!
        call numbck (word,i4,chkn,ierr2)
        if (ierr2 .eq. 0) then
!
!                     omit decimal point in latitude position
!
          call omitpd (word,i3)
          if (cwsum(6:8) .ne. 'XXX') then
            if (cwsum(6:8) .eq. word(1:3)) then
              if (cwsum(9:9) .eq. cns) then
                write (*,*) 'prcwrn, chkltln - good latitude recheck'
              else
                write (*,*) 'prcwrn, chkltln - bad n/s recheck'
                ire = 1
                cwsum(9:9) = 'Y'
              endif
            else
              write (*,*) 'msg ',cwsum(6:8),'  rep ',word(1:3)
              write (*,*) 'prcwrn, chkltln - bad latitude recheck'
              ire = 1
              cwsum(6:8) = 'XXZ'
            endif
          else
            write (*,*) 'prcwrn, chkltln - cant recheck latitude'
          endif
        else
          write (*,*) 'prcwrn, chkltln failed repeat lat check sum'
          ire = 1
          cwsum(6:8) = 'XXZ'
        endif
      else
        write (*,*) 'prcwrn, chkltln - cant find repeat latitude'
      endif
!
!                   extract repeat initial longitude
!
      if (ierr2 .eq. 0) then
        ks = kl
      else
        ks = 21
      endif
      word = ' '
      call extncn (cwmsg(nl),ks,word,cew,chkn,kl,ierr3)
      if (ierr3 .eq. 0) then
        call numbck (word,i5,chkn,ierr3)
        if (ierr3 .eq. 0) then
          call omitpd (word,i4)
          if (cwsum(11:14) .ne. 'XXXX') then
            if (cwsum(11:14) .eq. word(1:4)) then
              if (cwsum(15:15) .eq. cew) then
                write (*,*) 'prcwrn, chkltln - good longitude recheck'
              else
                write (*,*) 'prcwrn, chkltln - bad e/w recheck'
                ire = ire +1
                cwsum(15:15) = 'Y'
              endif
            else
              write (*,*) 'prcwrn, chkltln - bad longitude recheck'
              ire = ire +1
              cwsum(11:14) = 'XXXZ'
            endif
          else
            write (*,*) 'prcwrn, chkltln - cant recheck longitude'
          endif
        else
          write (*,*) 'prcwrn, chkltln failed repeat lon check sum'
          ire = ire +1
          cwsum(11:14) = 'XXXZ'
        endif
      else
        write (*,*) 'prcwrn, chkltln - cant find repeat longitude'
      endif
      if (ire .eq. 0) then
        ir3 = 0
      else
        ir3 = 1
        write (*,*) 'chkltln had ',ire,' errors in processing'
      endif
      return
!
      end
      subroutine cleanem (cmsg,lncnt,keys,kcnt)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  cleanem
!
!  DESCRIPTION:  Clean-up the line indecies to key words in message
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call cleanem (cmsg,lncnt,keys,kcnt)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        in/out   cyclone message
!    kcnt            integer        in/out   count of good keys
!    keys            integer        in/out   line numbers of good keys
!    lncnt           integer        input    line count of message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS: none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         fixem1      fix bad/missing key indicies, try 1
!         fixem2      fix bad/missing key indicies, try 2
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         ckey       char*32    array of valid check keys
!         cline      char*32    working string
!         kindx      integer    array in indicies of ckey of found keys
!         klast      integer    character count of ckey characters
!         ktmp       integer    array of temporary initial keys found
!         nb         integer    number of bad keys
!         nf         integer    number of keys found
!         nm         integer    number of missing keys
!         ns         integer    index for next search
!         skey       char*32    special key for outlook
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer nkmax
      parameter (nkmax = 21)
!
!         formal parameters
      integer lncnt, kcnt
      integer keys(nkmax)
      character*80 cmsg(lncnt)
!
!         local variables
      integer j, n, ns, nf, nb, nm
      integer ktmp(nkmax), klast(nkmax), kindx(nkmax)
      character*32 ckey(nkmax), skey, cline
!
!                             1         2         3
!                    12345678901234567890123456789012
      data ckey(1) /'O'/
      data ckey(2) /'FM'/
      data ckey(3) /'TO'/
      data ckey(4) /'BT'/
      data ckey(5) /'UNCLAS'/
      data ckey(6) /'SUBJ:'/
      data ckey(7) /'WARNING POSITION:'/
      data ckey(8) /'PRESENT WIND DISTRIBUTION:'/
      data ckey(9) /'REPEAT POSIT:'/
      data ckey(10) /'FORECASTS:'/
      data ckey(11) /'12 HRS, VALID AT:'/
      data ckey(12) /'VECTOR TO 24 HR POSIT:'/
      data ckey(13) /'24 HRS, VALID AT:'/
      data ckey(14) /'VECTOR TO 36 HR POSIT:'/
      data ckey(15)/'36 HRS, VALID AT:'/
      data ckey(16)/'VECTOR TO 48 HR POSIT:'/
      data ckey(17)/'EXTENDED OUTLOOK:'/
      data ckey(18)/'48 HRS, VALID AT:'/
      data ckey(19)/'VECTOR TO 72 HR POSIT:'/
      data ckey(20)/'72 HRS, VALID AT:'/
      data ckey(21)/'REMARKS:'/
!
!                1 2 3 4 5
      data klast/1,2,2,2,6,
!                6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21
     &           5,17,26,13,10,17,22,17,22,17,22,17,17,22,17, 8/
      data skey/'EXTENDED OUTLOK:  '/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do n=1, nkmax
        kindx(n) = 0
        ktmp(n)  = 0
      enddo
      do j=1, kcnt
        ktmp(j) = keys(j)
      enddo
      do n=1, nkmax
        keys(n) = 0
      enddo
      nf = 0
      do j=1, kcnt
        cline(1:32) = cmsg(ktmp(j))(1:32)
        if (nf .eq. 0) then
          do n=1, nkmax
            if (cline(1:klast(n)) .eq. ckey(n)(1:klast(n))) then
!                     found good keyword, so mark it in kindx
              kindx(n) = n
              keys(n)  = ktmp(j)
              ns = n +1
              nf = 1
              goto 100
!
            endif
          enddo
        else
          do n=ns, nkmax
            if (cline(1:klast(n)) .eq. ckey(n)(1:klast(n))) then
!                     found good keyword, so mark it in kindx
              kindx(n) = n
              keys(n)  = ktmp(j)
              ns = n +1
              nf = nf +1
              goto 100
!
            elseif (n .eq. 17) then
              if (cline(1:klast(n)) .eq. skey(1:klast(n))) then
!                       correct problem caused by removing repetitive
!                       characters in key words
                cmsg(ktmp(j))(1:32) = ckey(17)
!                       found good keyword, so mark it in kindx
                kindx(n) = n
                keys(n)  = ktmp(j)
                ns = n +1
                nf = nf +1
                goto 100
!
              endif
            endif
          enddo
          write(*,*) 'FAILED TEST -> ',cline(1:32)
          write (33,*) 'FAILED TEST -> ',cline(1:32)
          if (cline(1:1).ge.'0' .and. cline(1:1).le.'9') then
            if (ns .le. 11) then
              ns = 11
            elseif (ns .le. 13) then
              ns = 13
            elseif (ns .le. 15) then
              ns = 15
            elseif (ns .le. 18) then
              ns = 18
            elseif (ns .le. 20) then
              ns = 20
            endif
          endif
          kindx(ns) = -ns
          keys(ns)  = ktmp(j)
          ns = ns +1
          goto 100
!
        endif
  100   continue
      enddo
!
!                   check results
!
      write (*,*)
      nm = 0
      nb = 0
      if (nf .eq. kcnt) write (*,*) 'All initial key lines are good.'
      do n=6, nkmax
        if (kindx(n) .eq. 0) then
!                   key word is missing
          nm = nm +1
        elseif (kindx(n) .lt. 0) then
!                   key word is bad
          nb = nb +1
        endif
      enddo
      if (nb .gt. 0) then
        write (*,*) 'BAD key lines for following good keys'
        do n=6, nkmax
          if (kindx(n) .lt. 0) write (*,*) ckey(n)
        enddo
        write (*,*)
        call fixem1 (cmsg,lncnt,ckey,klast,kindx,keys,nkmax)
        nb = 0
        do n=6, nkmax
          if (kindx(n) .lt. 0) then
            write (*,*) 'BAD for good: ',ckey(n)
            nb = nb +1
          endif
        enddo
        write (*,*)
        if (nb .gt. 0) then
          write (*,*) 'Still have ',nb,' BAD key lines'
        else
          write (*,*) 'ALL found keys lines are GOOD'
        endif
      endif
      if (nm .gt. 0) then
        write (*,*) 'MISSING key lines are: '
        do n=6, nkmax
          if (kindx(n) .eq. 0) write (*,*) ckey(n)
        enddo
      endif
      if (nb.gt.0 .or. nm.gt.0)
     &    call fixem2 (cmsg,lncnt,ckey,klast,kindx,keys,nkmax)
      nb = 0
      nm = 0
      do n=6, nkmax
        if (kindx(n) .lt. 0) then
          write (*,*) 'BAD: ',ckey(n)
          nb = nb +1
        elseif (kindx(n) .eq. 0) then
          write (*,*) 'MISSING: ',ckey(n)
          nm = nm +1
        endif
      enddo
      kcnt = nkmax
      return
!
      end
      subroutine degrbl (word,nc,wrds,numc,nw,nk,ifnd)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  degrbl
!
!  DESCRIPTION:  de-garble word, by finding best match from set of good words
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call degrbl (word,nc,wrds,numc,nw,nk,ifnd)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    ifnd            integer        output   index to degarbled word
!    nc              integer        input    number of characters in word
!    nk              integer        output   number of characters in "good"
!                                            degarbled word
!    numc            integer        input    array of character count in wrds
!    nw              integer        input    number of words in wrds
!    word            char*20        input    word to degarble
!    wrds            char*10        input    array of "good" words
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                    ACTION
!     -----------------            ----------------------------
!   too many prospective words     signal error and return
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cw         char*1     working character
!         cwl        char*1     last character processed
!         cwrd       char*20    working word
!         jsum       integer    sum of matching characters
!         ksum       integer    sum of matching characters
!         m1         integer    last index 1
!         m2         integer    last index 2
!         match      integer    count of character matches
!         mncnt      integer    minimum count of required matches
!         ms         integer    starting character index
!         msum       integer    combined scores
!         n          integer    do index
!         n1         integer    index 1
!         n2         integer    index 2
!         nl         integer    last prospective index
!         np         integer    temporary pointer
!         np1        integer    pointer to number one
!         np2        integer    pointer to number two
!         nprcnt     integer    minimum allowed percent of matching
!         npt        integer    temporary pointer
!         nptr       integer    character pointer
!         nr         integer    offset range of characters
!         ns         integer    minimum character count
!         nseqi      integer    initial sequence
!         nseqp      integer    prospective sequence
!         nsum       integer    sum of initial and prospective matches
!         nt         integer    maximum character count
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  F77 with F90 extensions or F90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer nn
      parameter (nn = 20)
!
!         formal arguments
      integer ifnd, nc, nk, nw, numc(nw)
      character word*20, wrds(nw)*10
!
!         local variables
      integer j, jsum, k, ksum, m, m1, m2, mncnt, ms, msum, n, n1, n2
      integer nl, np, np1, np2, nprcnt, npt, nr, ns, nt
      integer match(nn), nptr(nn), nseqi(5,20), nseqp(5,20), nsum(5,2)
      character*1 cw, cwl
      character cwrd*20
!
      data nr/1/, nprcnt/75/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      if (nw .gt. nn) then
        write (*,*) 'prcwrn, degrbl arrays too small $$$$$'
        nk   = -1
        ifnd = -1
        goto 300
!
      endif
!                   eliminate sequential character replication
!
      k         = 1
      cwl       = word(1:1)
      cwrd(1:1) = cwl
      do n=2, nc
        cw = word(n:n)
        if (cw .ne. cwl) then
          k         = k +1
          cwrd(k:k) = cw
          cwl       = cw
        endif
      enddo
      nk = k
!                   establish allowed character count range
      ns = nk -nr
      nt = nk +nr
!
      do n=1, nw
        match(n) = 0
        nptr(n)  = n
        if (numc(n).ge.ns .and. numc(n).le.nt) then
!
!                   selected key word is within character counts
!                   so obtain count of matching characters
!
          do k=1, nk
            cw = cwrd(k:k)
            do m=1, numc(n)
              if (cw .eq. wrds(n)(m:m)) then
!                   sum matching characters
                match(n) = match(n) +1
                goto 130
!
              endif
            enddo
  130       continue
          enddo
        endif
      enddo
!
!                   sort character match, most first, with pointers
!
      do n=1, nw-1
        jsum = match(nptr(n))
        do m=n+1, nw
          if (match(nptr(m)) .gt. jsum) then
            jsum     = match(nptr(m))
            np       = nptr(n)
            nptr(n)  = nptr(m)
            nptr(m)  = np
          endif
        enddo
      enddo
!
      np2   = 0
      np1   = 0
      npt   = nptr(1)
      mncnt = nint (0.01*float (nprcnt)*float (numc(npt)))
      if (match(npt) .ge. mncnt) then
!
!                   there is at least one possible solution, so
!                   check sequence of characters, top five maximum
!
        do n=1, 5
          npt = nptr(n)
          if (match(npt) .ge. mncnt) then
!
!                   has minimum number or more of matching characters
!
            nl = n
            do k=1, nk
              nseqi(n,k) = -1
              nseqp(n,k) = -1
              cw = cwrd(k:k)
              ms = 1
  210         continue
              do m=ms, numc(npt)
                if (cw .eq. wrds(npt)(m:m)) then
                  do j=1, k
                    if (nseqp(n,j) .eq. m) then
                      ms = ms +1
                      goto 210
!
                    endif
                  enddo
!                      load sequence arrays with character placement
                  nseqi(n,k) = k
                  nseqp(n,k) = m
                  goto 250
!
                endif
              enddo
  250         continue
            enddo
          endif
        enddo
        do n=1, nl
          nsum(n,1) = 0
          nsum(n,2) = 0
          m1 = 0
          m2 = 0
!
!                   sum scores for proper sequence of characters
!
          do k=1, nk
            n1 = nseqi(n,k)
            if (n1 .eq. m1+1) nsum(n,1) = nsum(n,1) +1
            if (n1 .gt. 0) m1 = n1
            n2 = nseqp(n,k)
            if (n2 .eq. m2+1) nsum(n,2) = nsum(n,2) +1
            if (n2 .gt. 0) m2 = n2
          enddo
        enddo
        jsum = 0
        ksum = 0
!
!                   pick first and second place winners
!
        do n=1, nl
!                   use combined scores
          msum = nsum(n,1) +nsum(n,2)
          if (msum .gt. jsum) then
            np2  = np1
            np1  = nptr(n)
            ksum = jsum
            jsum = msum
          elseif (msum .eq. jsum) then
            np2  = nptr(n)
            ksum = jsum
          endif
        enddo
!
!                   if there is not a tie, set second place to zero
!
        if (ksum .ne. jsum) np2 = 0
      endif
      if (np1.gt.0 .and. np2.eq.0) then
!
!                   there is a clear winner
!
        nk   = numc(np1)
        ifnd = np1
      else
!
!                   there is no clear winner, so indicate none
!
        nk   = 0
        ifnd = 0
      endif
  300 continue
      return
!
      end
      subroutine dumyauto (cmsg,nlmax,nl,keys,nkmax,nk,cnnn,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  dumyauto
!
!  DESCRIPTION:  place dummy AUTODIN heading on AWN message
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call dumyauto (cmsg,nlmax,nl,keys,nkmax,nk,cnnn,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        in/out   AWN tropical cyclone warning
!                                            message
!    cnnn            char*240       in/out   last line of warning summary
!    ierr            integer        output   error flag, 0 - no error
!    keys            integer        output   index to key words
!    nk              integer        output   number of key words
!    nkmax           integer        input    dimension of keys
!    nl              integer        output   line index of message
!    nlmax           integer        input    maximum line count of message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!                               examples:
!      of "saved" AUTODIN lines               of dummy AWN
!
!  O 201351Z APR 95                       O 201500Z APR 95
!  FM NAVPACMETOCCEN WEST GU//JTWC//      FM JTWC
!  TO AIG NINE TWO TWO NINE               TO AWN AWN AWN
!  BT                                     BT
!  UNCLAS //N03145//                      UNCLAS
!  SUBJ: TROPICAL CYCLONE WARNING         SUBJ: TROPICAL CYCLONE WARNING
!  WTPS31 PGTW 201500
!    (Note: above line is start of
!     AWN message - it is left out
!     of dummy clone)
!
!
!         example of cnnn on input
!           1         2
!  1234567890123456789012
!  AWN WTPS31 PGTW 201500
!
!         example of cmsg(1) on output
!           1         2
!  1234567890123456789012
!  O 201500Z APR 95
!
!         example of cnnn on output
!
!           1         2         3         4
!  1234567890123456789012345678901234567890
!  AWN YYYYMMDDHHmm YYYYMMDDHHmmss
!
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name               Description
!         -------         ----------------------
!         date_and_time   obtain system date and time
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cmon       char*3     array of months
!         fmcod      char*4     array of station codes
!         fmsta      char*7     array of station names
!         from       char*7     name of sending station
!         idayw      integer    day of the warning
!         ihrmax     integer    maximum hour for match
!         ihrmin     integer    minimum hour for match
!         ihrw       integer    hour of the warning
!         imon       integer    index for month
!         imxday     integer    array of maximum days for each month
!         ival       integer    array of integer values of date-time
!         iyr        integer    year
!         kgo        integer    flag for offset of warning and computer
!                               times
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!                       sampson, nrl              Oct 92
!                        disabled date_and_time
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal arguments
      integer nlmax, nl, nkmax, nk, ierr
      integer keys(nkmax)
      character cmsg(nlmax)*80, cnnn*240
!
!         local variables
      integer idayw, ihrmax, ihrmin, ihrw, imon, imxday(12), ival(8)
      integer iyr, kgo, n
      character fmsta(3)*7, fmcod(3)*4, from*7, cmon(12)*3
!
      data fmcod /'PGTW', 'PHNC', 'KNGU'/
      data fmsta /'JTWC', 'PEARL', 'NORFOLK'/
      data cmon /'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
     &           'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'/
      data imxday/31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr = 0
!                                        1
!                12         345678      90
      cmsg(1) = 'O ' // cnnn(17:22) // 'Z '
      from = ' '
      do n=1, 3
        if (cnnn(12:15) .eq. fmcod(n)) from = fmsta(n)
      enddo
      if (from .eq. ' ') from = 'UNKN'
      cmsg(2) = 'FM ' // from
      cnnn    = 'AWN'
!                   load cnnn with recipt time (YYYYMMDDHHmmss.sss)
cx    call date_and_time (cnnn(18:18),cnnn(26:26),cnnn(70:70),ival)
      write(*,*) cmsg(1)(3:4),'  ',cnnn(24:25)
      if (cmsg(1)(3:4) .eq. cnnn(24:25)) then
!                   the days match
        write(*,*) 'days match'
        ihrmin = ival(5) -6
        ihrmax = ival(5) +3
        read (cmsg(1)(5:6),'(i2)') ihrw
        if (ihrw.ge.ihrmin .and. ihrw.le.ihrmax) then
          cmsg(1)(11:13) = cmon(ival(2))
          cmsg(1)(15:16) = cnnn(20:21)
        else
          ierr = -1
          write (*,*) 'prcwarn, AWN days match - outside hr window'
        endif
      elseif (cmsg(1)(5:6) .eq. '21') then
!                   1800 +3 = 2100 message release time
!                   the message time is 2100, so see if the message
!                   arrived shortly after 0000 of the next day
        write (*,*) 'prcwarn, AWN days DO NOT match'
        kgo = 0
        read (cmsg(1)(3:4),'(i2.2)') idayw
        if (ival(3) .eq. idayw +1) then
!                   the warning is one day less
          kgo = +1
        elseif (ival(3) .eq. 1) then
!                   it's the first of the month
!                   see if verifying day is last day of the month
          imon = ival(2) -1
          if (imon .lt. 1) imon = 12
          if (idayw .eq. imxday(imon)) then
            kgo = -1
          elseif (ival(2) .eq. 3) then
!                   it's 1 MAR, check for leap year
            if (idayw .eq. 29) kgo = -1
          endif
        endif
        if (kgo .ne. 0) then
          if (ival(5) .lt. 12) then
            if (kgo .gt. 0) then
!                   the month and year are the same as computer's
              cmsg(1)(11:13) = cmon(ival(2))
              cmsg(1)(14:15) = cnnn(20:21)
            else
!                   the month is one less than the computer's
              cmsg(1)(11:13) = cmon(imon)
              if (imon .ne. 12) then
!                   the year is the same as the computer's
                cmsg(1)(14:15) = cnnn(20:21)
              else
!                   the year is one less than the computer's
                iyr = ival(1) -1
                write (cmsg(1)(14:15),'(i2)') iyr
              endif
            endif
          endif
        else
          ierr = -1
        endif
      else
        ierr = -1
      endif
      write(*,*) 'error is ',ierr
      if (ierr .eq. 0) then
        cmsg(3) = 'TO AWN AWN AWN'
        cmsg(4) = 'BT'
        cmsg(5) = 'UNCLAS'
        cmsg(6) = 'SUBJ: TROPICAL CYCLONE WARNING'
        do n=1, 6
          keys(n) = n
        enddo
        nl = 6
        nk = 6
!                 finish loading cnnn so lftjust will hold receipt
!                 time in same place as RX+ AUTODIN line
        cnnn(5:16)   = cnnn(18:29)
        cnnn(32:240) = ' '
      endif
      do n=1, 10
        write (*,*) cmsg(n)
      enddo

      return
!
      end
      subroutine extncn (card,ks,cn1,ch,cn2,kl,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  extncn
!
!  DESCRIPTION:  extract sequential digits,character,digit group
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call extncn (card,ks,cn1,ch,cn2,kl,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*80        input    character string
!    ch              char*1         output   extracted character
!    cn1             char*10        output   extracted first  number
!    cn2             char*1         output   extracted second number
!    ierr            integer        output   error flag, 0 - no error
!    kl              integer        output   last character index
!    ks              integer        input    starting character index
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cx         char*1     working character
!         kn1        integer    first  integer found flag
!         kn2        integer    second integer found flag
!         nb1        integer    leading blanks indicator
!         ncc        integer    character found indicator
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer ks, kl, ierr
      character card*80, cn1*10, ch*1, cn2*1
!
!         local variables
      integer nb1, kn1, ncc, kn2, k
      character cx*1
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nb1 = 0
      cn1 = ' '
      kn1 = 0
      ch  = ' '
      ncc = 0
      cn2 = ' '
      kn2 = 0
      ierr  = -1
      do k=ks, 80
        cx = card(k:k)
        if (kn1.eq.0 .and. cx.eq.' ') then
          nb1 = nb1 +1
        elseif (ncc.eq.0 .and. ((cx.ge.'0' .and. cx.le.'9') .or.
     &          cx.eq.'.')) then
          if (k .eq. ks) nb1 = 1
          kn1 = kn1 +1
          if (kn1 .le. 10) then
            cn1(kn1:kn1) = cx
          else
            goto 100
!
          endif
        elseif (kn1.gt.0 .and. ncc.eq.0 .and. cx.ge.'A' .and. cx.le.'Z')
     &    then
          ncc = 1
          ch  = cx
        elseif (ncc.eq.1 .and. cx.ge.'0' .and. cx.le.'9') then
          kn2 = kn2 +1
          if (kn2 .eq. 1) then
            cn2 = cx
          else
            goto 100
!
          endif
        elseif (cx.eq.' ' .and. nb1.gt.0 .and. kn2.eq.1) then
          kl   = k
          ierr = 0
          goto 100
!
        elseif (kn1 .ne. 0) then
          goto 100
!
        endif
      enddo
  100 continue
      return
!
      end
      subroutine fixem1 (cmsg,lncnt,ckey,klast,kindx,keys,nkmax)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  fixem1
!
!  DESCRIPTION:  try one of fixing warning message
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call fixem1 (cmsg,lncnt,ckey,klast,kindx,keys,nkmax)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    ckey            char*32        input    expected true key words
!    cmsg            char*80        in/out   warning msg (excess lines removed)
!    keys            integer        input    line number of key lines in cmsg,
!                                            adjusted
!    kindx           integer        in/out   index values to keys
!                                             >0 good key found, valid index
!                                              0 no key found
!                                             <0 missing or bad key found
!    klast           integer        input    index to last character position
!                                            in ckeys
!    lncnt           integer        input    line count of cmsg
!    nkmax           integer        input    dimension of ckeys, klast, kindx
!                                            & keys
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!     contents of ckey on input:
!
!                            1         2         3
!                   12345678901234567890123456789012
!         ckey(1) /'O'/
!         ckey(2) /'FM'/
!         ckey(3) /'TO'/
!         ckey(4) /'BT'/
!         ckey(5) /'UNCLAS'/
!         ckey(6) /'SUBJ:'/
!         ckey(7) /'WARNING POSITION:'/
!         ckey(8) /'PRESENT WIND DISTRIBUTION:'/
!         ckey(9) /'REPEAT POSIT:'/
!         ckey(10) /'FORECASTS:'/
!         ckey(11) /'12 HRS, VALID AT:'/
!         ckey(12) /'VECTOR TO 24 HR POSIT:'/
!         ckey(13) /'24 HRS, VALID AT:'/
!         ckey(14) /'VECTOR TO 36 HR POSIT:'/
!         ckey(15)/'36 HRS, VALID AT:'/
!         ckey(16)/'VECTOR TO 48 HR POSIT:'/
!         ckey(17)/'EXTENDED OUTLOOK:'/
!         ckey(18)/'48 HRS, VALID AT:'/
!         ckey(19)/'VECTOR TO 72 HR POSIT:'/
!         ckey(20)/'72 HRS, VALID AT:'/
!         ckey(21)/'REMARKS:'/
!
!     Note:  when operational tropical forecasts are for more than 72 hours,
!            ckey must be changed accordingly
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         joinemk     join character strings
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cline      char*80    working character line
!         kb         integer    index to bad key
!         kd         integer    index to good key
!         nm         integer    index, minus
!         np         integer    index, plus
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
!     implicit none
!
!         formal parameters
      integer lncnt, nkmax
      integer klast(nkmax), kindx(nkmax), keys(nkmax)
      character cmsg(lncnt)*80, ckey(nkmax)*32
!
!         local variables
      integer kb, kd, n, nm, np
      character cline*80
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (33,*) 'INTO fixem1 with following keys:'
      do n=1, nkmax
        kd = iabs (kindx(n))
        if (kd .gt. 0) write (33,*) 'n= ',n,' ',cmsg(keys(kd))(1:40)
      enddo
      do n=1, nkmax
        if (kindx(n) .lt. 0) then
          kb    = -kindx(n)
          cline = cmsg(keys(kb))
          write(*,*) 'BAD in 1: ',cline
          if (n .lt. 6) then
            call joinemk (ckey(n),klast(n),cmsg(keys(kb)))
            kindx(n) = n
          elseif (n .eq. 6) then
            if (cline(4:klast(6)) .eq. ckey(6)(4:klast(6))) then
              call joinemk (ckey(6),klast(6),cmsg(keys(kb)))
              kindx(6) = 6
            endif
          elseif (n.eq.12 .or. n.eq.14 .or. n.eq.16 .or. n.eq.19) then
            if (n .ne. 16) then
              np = n +1
            else
              np = n +2
            endif
            if (kindx(np) .gt. 0) then
              call joinemk (ckey(n),klast(n),cmsg(keys(kb)))
              kindx(n) = kb
            elseif (cmsg(keys(kb))(11:12) .eq.                          &
     &              cmsg(-keys(kb)+1)(1:4)) then
!                       hours agree, but are not the standard
              kindx(n) = kb
            endif
          elseif (n.eq.13 .or. n.eq.15 .or. n.eq.18 .or. n.eq.20) then
            if (n .ne. 18) then
              nm = n -1
            else
              nm = n -2
            endif
            if (kindx(nm) .gt. 0) then
              call joinemk (ckey(n),klast(n),cmsg(keys(kb)))
              kindx(n) = kb
            endif
          endif
        endif
      enddo
      write (33,*) 'EXIT fixem1 with following keys:'
      do n=1, nkmax
        kd = iabs (kindx(n))
        if (kd .gt. 0) write (33,*) 'n= ',n,' ',cmsg(keys(kd))(1:40)
      enddo
      return
!
      end
      subroutine fixem2 (cmsg,lncnt,ckey,klast,kindx,keys,nkmax)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  fixem2
!
!  DESCRIPTION:  try two of fixing warning message
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call fixem2 (cmsg,lncnt,ckey,klast,kindx,keys,nkmax)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    ckey            char*32        input    expected true key words
!    cmsg            char*80        in/out   warning msg (excess lines removed)
!    keys            integer        input    line number of key lines in cmsg,
!                                            adjusted
!    kindx           integer        in/out   index values to keys
!                                             >0 good key found, valid index
!                                              0 no key found
!                                             <0 missing or bad key found
!    klast           integer        input    index to last character position
!                                            in ckeys
!    lncnt           integer        input    line count of cmsg
!    nkmax           integer        input    dimension of ckeys, klast, kindx
!                                            & keys
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!     contents of ckey on input:
!                                1         2         3
!                       12345678901234567890123456789012
!            ckey(6) = 'SUBJ:'
!         *  ckey(7) = 'WARNING POSITION:'
!         *  ckey(8) = 'PRESENT WIND DISTRIBUTION:'
!            ckey(9) = 'REPEAT POSIT:'
!         *  ckey(10)= 'FORECASTS:'
!         *  ckey(11)= '12 HRS, VALID AT:'
!            ckey(12)= 'VECTOR TO 24 HR POSIT:'
!         *  ckey(13)= '24 HRS, VALID AT:'
!            ckey(14)= 'VECTOR TO 36 HR POSIT:'
!         *  ckey(15)= '36 HRS, VALID AT:'
!            ckey(16)= 'VECTOR TO 48 HR POSIT:'
!         *  ckey(17)= 'EXTENDED OUTLOOK:'
!         *  ckey(18)= '48 HRS, VALID AT:'
!            ckey(19)= 'VECTOR TO 72 HR POSIT:'
!         *  ckey(20)= '72 HRS, VALID AT:'
!         *  ckey(21)= 'REMARKS:'
!
!         * keys w/o data on same line
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         remdup2     remove sequencial duplicates thru col 32
!         remdupb     left justify and remove extra blanks
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         ckline     char*32    working character string
!         cline      char*80    working character string
!         jj         integer    working index
!         kb         integer    bad index
!         kl         integer    last index
!         ln         integer    line index to good key line
!         lp         integer    prior good index
!         lx         integer    last good index
!         nfix       integer    fix-it flag, fixed when < 0
!         nn         integer    index to missing key line
!         nonel      integer    key lines w/o data on same line, when <0
!         np         integer    prior good index
!         nx         integer    next good index
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lncnt, nkmax
      integer klast(nkmax), kindx(nkmax), keys(nkmax)
      character cmsg(lncnt)*80, ckey(nkmax)*32
!
!         local variables
      integer j, jj, kb, kl, n, nfix, nn, np ,nx, l, ln, lp, lx
      integer nonel(21)
      character ckline*32, cline*80
!
!                 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18
      data nonel/ 0, 0, 0, 0, 0, 0,-1,-1, 0,-1,-1, 0,-1, 0,-1, 0,-1,-1, &
!                19 20 21
     &            0,-1,-1/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do n=6, nkmax
        if (kindx(n) .lt. 0) then
!                   found a bad key word, fix same
          kb = -kindx(n)
!                   found bad key line
          if (nonel(n) .lt. 0) then
!                   found key line that has no data with it
            cmsg(keys(kb)) = ckey(n)
            kindx(n) = kb
          else
            do j=1, 32
              if (cmsg(keys(kb))(j:j) .eq. ':') then
                cline = ckey(n)
                jj = j
                do l=klast(n)+1, 80
                  jj = jj +1
                  if (jj .le. 80) cline(l:l) = cmsg(keys(kb))(jj:jj)
                enddo
                kindx(n) = kb
                goto 100
!
              endif
            enddo
          endif
        endif
      enddo
!
  100 continue
      do n=6, nkmax
        if (kindx(n) .eq. 0) then
!                   found a missing key line
          nn = n
  200     continue
!                   set prior good index value, np
          np = nn -1
          if (np .ne. 0) then
            lp = kindx(np)
            if (lp .le. 0) then
              nn = np
              goto 200
!
            else
              lp = keys(lp) +1
            endif
          else
            lp = 1
          endif
          nn = n
  210     continue
!                   set next good index value, nx
          nx = nn +1
          if (nx .le. nkmax) then
            lx = kindx(nx)
            if (lx .le. 0) then
              nn = nx
              goto 210
!
            else
              lx = keys(lx) -1
            endif
          else
            lx = keys(lncnt) -1
          endif
          kl = klast(n) -1
          ckline = ' '
          ckline(1:kl) = ckey(n)(1:kl)
          nfix = 0
          do l=lp, lx
!                   remove duplicate blanks
            call remdupb (cmsg(l))
            if (ckline(1:kl) .eq. cmsg(l)(1:kl)) then
              cline = ' '
              cline = ckey(n)(1:klast(n)) // ' '// cmsg(l)(kl+1:80)
              cmsg(l) = ' '
              cmsg(l) = cline
              nfix = -1
              ln   =  l
              nn   =  n
            else
              cline = cmsg(l)
!                     remove duplicates thru column 32
              call remdup2 (cline)
              if (ckline(1:kl) .eq. cline(1:kl)) then
                cmsg(l) = cline
                cline = ' '
                cline = ckey(n)(1:klast(n)) // ' '// cmsg(l)(kl+1:80)
                cmsg(l) = ' '
                cmsg(l) = cline
                ln   =  l
                nn   =  n
                nfix = -1
              endif
            endif
            if (nfix .ne. 0) goto 300
!
          enddo
  300     continue
          if (nfix .ne. 0) then
            kindx(nn) = nn
            keys(nn)  = ln
          endif
        endif
      enddo
      return
!
      end
      subroutine fndkey (card,ks,kf)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  fndkey
!
!  DESCRIPTION:  Check card for a valid key
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call fndkey (card,ks,kf)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*80        input    character string from msg
!    kf              integer        output   key found indicator
!    ks              integer        in/out   index to key found when kf >0
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         remdup1     remove duplictes thru col 32
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         keys       char*6     vlaid key words
!         nk         integer    character count in keys
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal arguments
      integer ks, kf
      character card*80
!
!         local variables
      integer n, nk(6)
      character*6 keys(6)
!
      data keys/'O ',                                                   &
     &          'FM ',                                                  &
     &          'TO ',                                                  &
     &          'BT ',                                                  &
     &          'UNCLAS',                                               &
     &          'SUBJ:'/
      data nk/2, 3, 3, 3, 6, 5/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   check for match
!
      do n=1, 6
        if (card(1:nk(n)) .eq. keys(n)(1:nk(n))) goto 100
!
      enddo
!
!                   no match found, so check for ":" which SUBJ should have
!                   and check again for this important key word
!
      do n=1, 10
        if (card(n:n) .eq. ':') then
          call remdup1 (card)
          if (card(1:nk(6)) .eq. keys(6)(1:nk(6))) goto 100
!
        endif
      enddo
      n = 0
  100 continue
      kf = n
!                   do not change value of ks unless kf > 0
      if (n .ne. 0) ks = n
      return
!
      end
      subroutine fndyrmo (line,csdtg,ctxrx,nogo)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  fndyrmo
!
!  DESCRIPTION:  Find year and month of message, cross-check with time of
!                receipt
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:
!    1.  Assumes warnings are generated after the time change of csdtg.
!         i.e. 00Z warnings are normally issued at 03Z
!    2.  Will not work correctly after year 2099.
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call fndyrmo (line,csdtg,ctxrx,nogo)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    csdtg           char*10        input    computer synoptic/watch time
!                                            YYYYMMDDHH -> HH = 00 or 12
!    ctxrx           char*240       in/out   in: FNMOC ODR RX+ comm line
!                                            out: NNNN warning summary line,
!                                                 partly filled out
!    line            char*80        input    string of characters in following
!                                            format: O 251604Z JUL 95
!    nogo            integer        output   flag - 0 keep processing
!                                                  -1 skip further processing
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!        INPUT - ctxrx
!                in standard FNMOC ODR RX+ comm line format
!
!       OUTPUT - ctxrx
!                in tropical warning summary format for NNNN, as follows:
!                           1         2         3         4
!                  1234567890123456789012345678901234567890
!                  NNNN XXXX YYYYMMDDHHmm YYYYMMDDHHmmss
!                                Tx           Rx
!
!         Note: the 4 X's will be filled in by another S/R
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         c1         char*1     working first character
!         c2         char*1     working second character
!         c3         char*1     working third character
!         cyrmo      char*6     year and month (YYYYMM)
!         fcltr      char*1     array of first letters of months
!         ii         integer    index to mos, when >0
!         iyr        integer    century of the year, 19 or 20
!         kl         integer    limit of character search
!         mos        char*3     array of months, abreviations
!         nn         integer    count of digits
!         rxtime     char*14    ODR receipt time
!         wrd        char*3     working string
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal arguments
      integer nogo
      character line*80, csdtg*10, ctxrx*240
!
!         local variables
      integer i, ii, iyr, j, jj, k, kk, kl, nn
      character*1 c1, c2, c3, fcltr(8)
      character*3 mos(12), wrd
      character cyrmo*6, rxtime*14
!
      data mos /'JAN','FEB','MAR','APR','MAY','JUN',
     &          'JUL','AUG','SEP','OCT','NOV','DEC'/
!                   first letter of months
      data fcltr/'A','D','F','J','M','N','O','S'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      rxtime = ctxrx(18:31)
!
!                   fill each digit location with an X
!                        1         2
!               1234567890123456789012
      ctxrx  = 'NNNN XXXX XXXXXXXXXXXX ' // rxtime
!                         YYYYMMDDHHmm
      cyrmo  = ' '
      nogo   = 0
      do k=2, 78
        c1 = line(k:k)
        if (c1.ge.'A' .and. c1.le.'Y') then
          do j=1, 8
!
!                   see if start of month has been found
!
            if (c1 .eq. fcltr(j)) then
              c2 = line(k+1:k+1)
              if (c2.ge.'A' .and. c2.le.'Y') then
                c3 = line(k+2:k+2)
                if (c3.ge.'A' .and. c3.le.'Y') then
                  ii  = 0
                  wrd = c1 // c2 // c3
!
!                       SEARCH FOR MATCH WITH MONTH
!
                  do i=1, 12
                    if (wrd .eq. mos(i)) ii = i
                  enddo
                  if (ii .gt. 0) then
!
!                         OBTAIN YEAR
!
                    kl = min0 (k+13, 80)
                    do i=k+3, kl
                      c1 = line(i:i)
                      if (c1.ge.'0' .and. c1.le.'9') then
                        c2 = line(i+1:i+1)
                        if (c2.ge.'0' .and. c2.le.'9') then
!
!                           LOAD cyrmo WITH YEAR_MONTH
!
                          wrd = ' '
                          wrd = c1 // c2
                          read (wrd,'(i2)') iyr
!                               load first two digits
                          if (iyr .ge. 95) then
!                                 use computer's time
                            cyrmo(1:2) = csdtg(1:2)
                          else
!                                 it has to be 20
                            cyrmo(1:2) = '20'
                          endif
!                               load last two digits of year
                          cyrmo(3:4) = c1 // c2
!                               load month, as two digits
                          write (cyrmo(5:6),'(i2.2)') ii
!
!                               check with time of receipt
!
                          write(*,*) cyrmo,'  ',rxtime(1:6)
                          if (cyrmo .ne. rxtime(1:6)) then
                            nogo = -1
                            goto 100
!
                          endif
!
!                   ******* obtain DDHHmm of message transmit time *****
!
                          do kk=k-1, 2, -1
                            if (line(kk:kk) .eq. 'Z') then
                              write(*,*)'found Z @ ',kk,' kk6 = ',kk -6
                              nn = 0
                              if ((kk -6) .gt. 1) then
                                do jj=kk-6, kk-1
                                  if (line(jj:jj).ge.'0' .and.          &
     &                                line(jj:jj).le.'9') nn = nn +1
                                enddo
                              endif
                              if (nn .eq. 6) then
!
!                   ******* load YYYYMMDDHHmm of message transmit time *****
!
                                ctxrx(11:22) = cyrmo // line(kk-6:kk-1)
                                goto 100
!
                              endif
                            endif
                          enddo
                        endif
                      endif
                    enddo
                    goto 100
!
                  endif
                endif
              endif
            endif
          enddo
        endif
      enddo
  100 continue
      return
!
      end
      subroutine fnumfd (line,ks,cnum,nd,kf)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  fnumfd
!
!  DESCRIPTION:  find first number in line starting at column ks
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call fnumfd (line,ks,cnum,nd,kf)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cnum            char*16        output   character string of collected
!                                            digits, if kf >0
!    kf              integer        output   flag >0 found a number and last
!                                                    column of digit
!                                                  0 no digit found
!    ks              integer        input    starting column number for search
!    line            char*80        input    character string for extraction
!    nd              integer        output   number of digits collected
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:  none
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nd, kf, ks
      character line*80, cnum*16
!
!         local variabels
      integer k, kk
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cnum = ' '
      do k=ks, 80
        if (line(k:k).ge.'0' .and. line(k:k).le.'9') then
          kf = k
          nd = 1
          cnum(1:1) = line(k:k)
          do kk=k+1, 80
            if (line(kk:kk).lt.'0' .or. line(kk:kk).gt.'9') goto 100
!
            kf = kk
            nd = nd +1
            cnum(nd:nd) = line(kk:kk)
            if (nd .eq. 16) goto 100
!
          enddo
        endif
      enddo
      nd = 0
      kf = 0
  100 continue
      return
!
      end
      subroutine gonogo (cmsg,lncnt,keys,kcnt,jump)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  gonogo
!
!  DESCRIPTION:  Determine if message is a tropical cyclone warning
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call gonogo (cmsg,lncnt,keys,kcnt,jump)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        input    message to be checked
!    jump            integer        output   flag >0  keep processing
!                                                 -1  not a TC warning
!    kcnt            integer        input    number of keys in keys
!    keys            integer        input    array of key words
!    lncnt           integer        input    number of lines in message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         ckeys      char*25    array of key-words
!         jj         integer    last line of message found with valid key
!         jt         integer    maximum line for checking
!         nkey       integer    number of characters in ckeys key-words
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lncnt, kcnt, jump
      integer keys(kcnt)
      character*80 cmsg(lncnt)
!
!         local variables
      integer j, jj, jt, k, m, nkey(6)
      character*25 ckeys(6)
!
!                              1         2
!                     1234567890123456789012345
      data ckeys(1) /'TROPICAL CYCLONE WARNING'/
      data ckeys(2) /'WARNING POSITION'/
      data ckeys(3) /'PRESENT WIND DISTRIBUTION'/
      data ckeys(4) /'REPEAT POSIT'/
      data ckeys(5) /'FORECASTS'/
      data ckeys(6) /'HRS, VALID AT'/
!                1   2   3   4  5   6
      data nkey/24, 16, 25, 12, 9, 23/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   check first required key words, subject of message
!
      jump = 0
      do k=6, 10
        if (cmsg(k)(k:k+23) .eq. ckeys(1)(1:nkey(1))) then
         jump = 1
         goto 110
!
        endif
      enddo
  110 continue
!
!                   check required key words 2 thru 5
!
      jj = 0
      do j=7, 10
        do m=2, 5
          if (cmsg(keys(j))(1:nkey(m)) .eq. ckeys(m)(1:nkey(m))) then
            jump = jump +1
            jj   = j
            goto 120
!
          endif
        enddo
  120   continue
      enddo
      if (jump .lt. 4) then
!
!                   try for more "HRS, VALID AT"
!
        jt = min0 (11,lncnt)
        do j=jj+1, jt
          if (cmsg(keys(j))(4:16) .eq. ckeys(6)(1:nkey(6))) then
            jump = jump +1
          elseif (cmsg(j)(3:15) .eq. ckeys(6)(1:nkey(6))) then
            jump = jump +1
          elseif (cmsg(j)(5:17) .eq. ckeys(6)(1:nkey(6))) then
            jump = jump +1
          endif
        enddo
      endif
!
!                   if at least four "required" key strings are not
!                   found, it is not a proper tropcial cyclone warning
!                   message; so set jump to "true".
!
      if (jump .lt. 4) jump = -1
      return
      end
      subroutine joinemk (cline1,kposit,cline2)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  joinemk
!
!  DESCRIPTION: join good key-words with data following bad key-words
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call joinemk (cline1,kposit,cline2)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline1          char*32        input    correct key words
!    cline2          char*80        in/out   line of message to be corrected
!                                            with data after ":" saved
!    kposit          integer        input    location of ":" in cline1
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED: none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         js         integer    column position of last data to be moved
!         kl         integer    column position for data moved data
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer kposit
      character cline1*32, cline2*80
!
!         local variables
      integer js, k, kk, kl, ks
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do ks=1, 80
!
!                   find end of key words on cline2
!
        if (cline2(ks:ks) .eq. ':') then
          if (ks .ge. kposit) then
!
!                   position of ":" on cline1 is <= position on cline2
!                   so load cline1 onto first part of cline2
!
            do k=1, kposit
              cline2(k:k) = cline1(k:k)
            enddo
            kk = ks
!
!                   now move data to lower column numbers
!
            do k=kposit +1, 80
              kk = kk +1
              if (kk .le. 80) cline2(k:k) = cline2(kk:kk)
            enddo
!                   all finished, so jump to exit
            goto 100
!
          else
!
!                   valid data must be shifted to higher column values
!
            do k=80, ks+1, -1
              if (cline2(k:k) .ne. ' ') then
!
!                   found end-point of data to be saved
!                   calculate new end-point of data
!
                kl = kposit +k -ks
                if (kl .le. 80) then
                  js = k
                else
!
!                   this should not happen, but if it does,
!                   save what data we can
!
                  js = k +80 -kl
                  kl = 80
                endif
!
!                   move data to new correct location
!
                do kk=js, ks+1, -1
                  cline2(kl:kl) = cline2(kk:kk)
                  kl = kl -1
                enddo
              endif
!
!                   load corrected key-words in first part of cline2
!
              do kk=1, kposit
                cline2(kk:kk) = cline1(kk:kk)
              enddo
!                   all finished, so jump to exit
              goto 100
!
            enddo
          endif
        endif
      enddo
  100 continue
      return
!
      end
      subroutine lftjust (card,keep)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lftjust
!
!  DESCRIPTION:  Left justify values, if values are to be retained
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call lftjust (card,keep)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*80        in/out   line from warning message
!    keep            integer        output   flag for keeping or not keeping
!                                            returned values in card
!                                              -1 - keep
!                                               0 - do not keep
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cl         char*1     last character read
!         cline      char*80    working string
!         cx         char*1     working character
!         nk         integer    number of characters loaded into cline
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer keep
      character*80 card
!
!         local variables
      integer nk, k, kk
      character cx*1, cl*1, cline*80
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cline = ' '
      keep  = 0
      do k=1, 80
        cl = card(k:k)
        if (cl.ne.' ' .and. cl.ne.'-') then
!
!                   left justify values and remove consecutive blanks
!
          cline(1:1) = cl
          nk = 1
          do kk=k+1, 80
            cx = card(kk:kk)
            if (cx.ne.' ' .or. (cl.eq.' ' .and. cx.ne.' ') .or.         &
     &         (cl.ne.' ' .and. cx.eq.' ')) then
              nk = nk +1
              cline(nk:nk) = card(kk:kk)
            endif
            cl = cx
          enddo
!
          if (cline(1:4) .ne. 'PAGE') then
!
!                     check that valid data is available
!
            do kk=1, 80
              cx = card(kk:kk)
              if (cx.ge.'A' .and. cx.le.'Z') then
                keep = -1
              elseif (cx.ge.'0' .and. cx.le.'9') then
                keep = -1
              endif
              if (keep .ne. 0) goto 100
!
            enddo
          else
            cline = ' '
          endif
          goto 100
!
        endif
      enddo
  100 continue
      card = cline
      return
!
      end
      subroutine lodamp (cline,csamp,ks)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lodamp
!
!  DESCRIPTION:  Load summary amplification line
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call lodamp (cline,csamp,ks)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline           char*80        input    line from message
!    csamp           char*240       output   AMP line of summary
!    ks              integer        in/out   starting and ending location of
!                                            information
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cx         char*1     working character
!         nb         integer    count of blanks
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer ks
      character cline*80, csamp*240
!
!         local variables
      integer k, nb
      character cx*1
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nb = 1
      do k=1, 80
        cx = cline(k:k)
        if (cx .ne. ' ') then
          ks = ks +1
          if (ks .le. 240) then
            csamp(ks:ks) = cx
            nb = 0
          endif
        elseif (nb .eq. 0) then
          ks = ks +1
          if (ks .le. 240) then
            csamp(ks:ks) = cx
            nb = 1
          endif
        endif
      enddo
      return
!
      end
      subroutine lodem1a (cmsg,lncnt,nsl,nll,orgsta,wsum,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lodem1a
!
!  DESCRIPTION:  Load part of first line of warning summary
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call lodem1a (cmsg,lncnt,nsl,nll,orgsta,wsum,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        input    warning message
!    ierr            integer        output   error flag, 0 no error
!    lncnt           integer        input    line count of message
!    nll             integer        input    last line for search
!    nsl             integer        input    starting line for search
!    orgsta          char*4         input    originator's station ID
!    wsum            char*240       in?/out  warning summary line to be filled
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!    improper words or         signal error with error flag, and leave
!    missing words             "X" for digit or "Y" for character in
!                              dummy filled template
!
!  ADDITIONAL COMMENTS:
!
!     Example of warning message lines to be processed by this S/R:
!
!         SUBJ:  TROPICAL CYCLONE WARNING
!         WHPN31 PHNC 080400
!         1. HURRICANE ORLENE (17E) WARNING NR 22
!         02 ACTIVE TROPICAL CYCLONES IN EASTPAC
!         MAX SUSTAINED WINDS BASED ON ONE-MINUTE AVERAGE
!
!     Template of WSUM output:
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         YYYYMMDDHH IDB NAME       NRWA NC DEG KT METH ---- ACC
!                        1234567890
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         fnumfd      find first number in line after starting column
!         wrdfnd      try to find requested word or words
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cnum       char*8     character representation of found number
!         cv         char*1     working character
!         iexer      integer    flag for finding "EXERCISE", 0 - no find
!         ire        integer    sum errors found
!         kf         integer    starting column of found word
!         kl         integer    index to word found
!         knf        integer    column number of number of active cyclones
!         ks         integer    starting column for search
!         kswnr      integer    column number of previous found number
!         nc         integer    count of found characters
!         nd         integer    number of digits in found number
!         nk         integer    number of characters in words (wrds)
!         nl         integer    line number being processed
!         nn         integer    index to words in wrds
!         ns         integer    starting column for search
!         nw         integer    number of words in wrds
!         wrds       integer    array of words for searching
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!  Allow 2 character storm names  sampson 1/26/00
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lncnt, nsl, nll, ierr
      character orgsta*4, cmsg(lncnt)*80, wsum*240
!
!         local variables
      integer ire, n, nc, nd, nk(5), nl, nn, ns, nw, j, k, kf, kl, ks
      integer knf, kswnr, iexer
      character*1 cv
      character*16 cnum, wrds(5)
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (33,*) 'INTO lodem1a to process: '
      wrds(1) = 'EXERCISE'
      nk(1)   =  8
      nw      =  1
      ks      =  1
      iexer   =  0
      do n=nsl, nll
!
!                   see if word "EXERCISE" is present in these lines
!
        write (33,'(I3,1X,A70)') n, cmsg(n)(1:70)
        call wrdfnd (cmsg(n),ks,wrds,nk,nw,kf,kl)
!
!                   message is for an exercise if kl > 0
!
        if (kl .gt. 0) iexer = -1
      enddo
      write (33,*)
      ire = 0
      wrds(1) = 'WARNING NR'
      nk(1)   = 10
      wrds(2) = 'WARNING'
      nk(2)   = 7
      wrds(3) = ' NR '
      nk(3)   = 4
      nw      = 3
      ks      = 5
      nl      = 0
      do n=nsl, nll
!
!                   look for precurser to warning number
!
        call wrdfnd (cmsg(n),ks,wrds,nk,nw,kf,kl)
        if (kl .gt. 0) then
!
!                   word kl was found, starting in column kf
!
          ks = kf +nk(kl)
          call fnumfd (cmsg(n),ks,cnum,nd,kf)
          if (kf .gt. 0) then
!
!                  number was found starting in column kf with nd digits
!
            if (nd .eq. 2) then
              cnum(3:3) = cnum(2:2)
              cnum(2:2) = cnum(1:1)
              cnum(1:1) = '0'
              cv        = cmsg(n)(kf+2:kf+2)
            elseif (nd .eq. 1) then
              cnum(3:3) = cnum(1:1)
              cnum(1:2) = '00'
              cv        = cmsg(n)(kf+1:kf+1)
            elseif (nd .eq. 3) then
cx  sampson nrl june 1,1998  - set letter to whatever is right after warning number
cx            cv = cmsg(n)(kf+3:kf+3)
              cv = cmsg(n)(kf+1:kf+1)
            endif
!
!                   have warning number, now get mod (letter or blank)
!
            if (cv.ge.'A'.and.cv.le.'Z' .or. cv.eq.' ') then
              cnum(4:4) = cv
            else
              cnum(4:4) = 'Y'
            endif
!
!                   ***** LOAD WARNING NUMBER *****
!
            wsum(27:30) = cnum(1:4)
            kswnr       = kf
            nl          = n
          endif
        endif
      enddo
      if (nl .gt. 0) then
!
!                   obtain cyclone number
!
        ks = 4
        call fnumfd (cmsg(nl),ks,cnum,nd,kf)
        if (kf .gt. 0) then
!
!                  number was found starting in column kf with nd digits
!
          if (nd .eq. 2) then
            if (kf .ne. kswnr) then
!
!                  have cyclone number, now get basin indicator
!
              cnum(3:3) = cmsg(nl)(kf+1:kf+1)
              if (orgsta .eq. 'NEOC') cnum(3:3) = 'L'
              if (cnum(3:3).eq.'A' .or. cnum(3:3).eq.'B' .or.           &
     &            cnum(3:3).eq.'W' .or. cnum(3:3).eq.'C' .or.           &
     &            cnum(3:3).eq.'E' .or. cnum(3:3).eq.'L' .or.           &
     &            cnum(3:3).eq.'S' .or. cnum(3:3).eq.'P') then
!
!                   ***** LOAD CYCLONE NUMBER AND BASIN *****
!
                wsum(12:14) = cnum(1:3)
              else
!
!                   ***** LOAD CYCLONE NUMBER W/O BASIN *****
!
                wsum(12:13) = CNUM(1:2)
                ire = ire +1
                write(*,*) 'cyclone b= ',cnum(3:3)
                write(*,*) cmsg(nl)(kf:kf+5)
cx              pause
              endif
            elseif (orgsta .eq. 'NEOC') then
!
!                   NEOC may not number named cyclones
!
              wsum(13:13) = 'L'
              ire = ire +1
            else
              ire = ire +1
            endif
          else
            write(*,*) 'cyclone nd = ',nd
            write(*,*) cmsg(nl)
cx          pause
          endif
        endif
!
!                   obtain cyclone name
!
        nw = 0
        kl = 3
        do j=1, 5
          wrds(j) = ' '
          nc      = 0
          ks      = kl +1
          do k=ks, 80
            cv = cmsg(nl)(k:k)
            if (cv .ne. ' ') then
cx   allow odd characters in the name ... sampson nrl 07/27/01
              if ( (cv.ge.'A' .and. cv.le.'Z') .or. cv.eq.'-') then
                nc = nc +1
                if (nc .le. 10) wrds(j)(nc:nc) = cv
              endif
            else
              if (cv.eq.' ' .and. nc.ne.0) goto 110
!
            endif
          enddo
          k = 81
  110     continue
          kl    = k
          if (nc .gt. 0) then
            nk(j) = min0 (nc,10)
            nw    = nw +1
            if (wrds(j)(1:7) .eq. 'WARNING') GOTO 120
!
          endif
        enddo
        ire = ire +1
        goto 200
!
  120   continue
cx    fix to allow 2 character cyclone names ... sampson nrl 1/26/00
cx      if (nk(nw-1) .le. 2) then
        if (nk(nw-1) .le. 1) then
          nn = nw -2
        else
          nn = nw -1
        endif
        if (wrds(nn)(1:7).eq.'CYCLONE' .or.                             &
     &      wrds(nn).eq.'DEPRESSION') then
!
!                   ***** LOAD NONAME FOR NAME OF CYCLONE *****
!
          wsum(16:25) = 'NONAME    '
        else
!
!                   ***** LOAD EXTRACTED NAME FOR CYCLONE *****
!
          wsum(16:25) = wrds(nn)
        endif
        goto 130
!
      else
        ire   = ire +1
        kswnr = 0
      endif
  130 continue
      cnum = '01'
      if (kswnr .ne. 0) then
        wrds(1) = 'ACTIVE'
        nk(1)   = 6
        nw      = 1
        ks      = 1
        ns      = nl +1
        call wrdfnd (cmsg(ns),ks,wrds,nk,nw,kf,kl)
        if (kl .gt. 0) then
!
!                   word kl was found, starting in column kf
!
          call fnumfd (cmsg(ns),ks,cnum,nd,knf)
          if (knf.eq.0 .or. knf.gt.kf) cnum = ' '
        endif
      endif
      if (cnum .ne. ' ') then
!
!                   ***** LOAD NUMBER OF ACTIVE CYCLONES IN BASIN *****
!
        wsum(32:33) = cnum(1:2)
      else
        ire = ire +1
      endif
  200 continue
      if (ire .eq. 0) then
        ierr = 0
      else
        ierr = 1
        write (6,*) 'lodem1a had ',ire,' ERRORS in processing'
      endif
!
!                exercise warning should have warning number in the 90's
!
      if (iexer.ne.0 .and. wsum(12:12).ne.'9') wsum(12:12) = '9'
      write (6,'(1X,A79)') wsum(1:79)
      write (33,*) 'RESULTS:'
      write (33,'(1x,a240)') wsum
      return
!
      end
      subroutine lodem1b (cmsg,lncnt,nsl,nll,csdtg,ctxrx,wsum1,wsum2,   &
     &                    ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lodem1b
!
!  DESCRIPTION:  Finish loading first line of summary and start loading
!                first part of first TAU line - initial location
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call lodem1b (cmsg,lncnt,nsl,nll,csdtg,ctxrx,wsum1,wsum2,ierr)
!
!  PARAMETERS:
!       Name        Type          Usage            Description
!    --------     ----------     -------    ----------------------------
!    cmsg         char*80        input      warning message
!    csdtg        char*10        input      computer synoptic (watch) time
!    ctxrx        char*240       input      Tx and Rx line (RX+ line)
!    ierr         integer        output     error flag:
!                                            <0 - no more processing
!                                             0 - no error
!                                            >0 - correctable error(s)
!    lncnt        integer        input      line count of message
!    nll          integer        input      ending line for search
!    nsl          integer        input      starting line for search
!    wsum1        char*240       in/out     first line of summary
!    wsum2        char*240       in/out     second line of summary
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     bad or missing data      flag as error and keep checking
!
!  ADDITIONAL COMMENTS:
!
!     Example of lines to process:
!
!         WARNING POSITION:
!         080000Z8 --- 17.9N7  131.2W7
!         MOVEMENT PAST SIX HOURS - 300 DEGREES AT 11 KTS
!         POSITION ACCURATE TO WITHIN 030 NM
!         POSITION BASED ON CENTER LOCATED BY SATELLITE
!
!     Template of wsum1:
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         yyyymmddhh idb name       nrwa nc deg kt meth ---- acc
!
!     Template of wsum2:
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         tau  latn longt mxw rspd nmi dd ---
!
!     Example of ctxrx character string:
!                  1         2         3         4
!         123456789012345678901234567890123456789012345678901234567890
!         NNNN JTWC YYYYMMDDHHmm YYYYMMDDHHmmss CIR
!
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         chkhist     check ISIS for previous processing of ths warning
!   date_and_time     obtain real computer date and time
!         dtgmod      modifiy exiting dtg to produce offset dtg
!         extncn      extract number-character-number sequence (lat/lon)
!         fnumfd      find first number after starting column location
!         neocln      correct longitude from NEOC, as required
!         numbck      verify number by checking with checksum
!         omitpd      omit period from character string
!         wrdfnd      look for given word or words in character string
!         wrdsfd      identify all words found from specified words
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         accy       char*3     accuracy of initial position, nm
!         cbn        char*1     one character cyclone basin indicator
!         cew        char*1     East - West hemisphere indicator
!         chkn       char*1     checksum number
!         cns        char*1     North - South hemisphere indicator
!         cz         char*1     character 'Z' from dtg, not used directly
!         date       char*8     system date
!         fdtg       char*10    future limit of dtg window
!         i3         integer    numeral 3
!         i4         integer    numeral 4
!         i5         integer    numeral 5
!         i6         integer    numeral 6
!         ierr1      integer    position dtg error flag, 0 no error
!         ierr2      integer    latitude error flag, 0 no error
!         ierr3      integer    longitude error flag, 0 no error
!         ilat       integer    latitude times 10
!         ilon       integer    logitude times 10
!         ire        integer    sum of internal errors
!         ivals      integer    integer values of date and time
!         kf         integer    column number of found object
!         kl         integer    index of word found
!         kndx       integer    array of indicies of found word(s)
!         kont       integer    continuation of processing flag
!                                0 - stop, -1 - continue
!         ks         integer    starting column number for search
!         kss        integer    starting column number for search
!         line       char*80    working string
!         meth       char*4     method of fix
!         moderr     integer    dtg modification error flag
!         nd         integer    number of digits
!         nk         integer    number of characters
!         nl         integer    number of message line being processed
!         nmeth      integer    number of methods found
!         nogo       integer    flag for continuation of processing
!                                 0 - continue, -1 - stop
!         nw         integer    number of words for search
!         pdtg       char*10    past limit of dtg window
!         rsta       char*4     received from station
!         time       char*10    system time
!         word       char*10    working string
!         wrds       char*10    array of requested words
!         zone       char*5     offset to GMT, hours - not used
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!                     disabled section of code dealing with system time
!                     sampson,NRL          OCT 95
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nsl, nll, ierr
      integer lncnt
      character cmsg(lncnt)*80, csdtg*10
      character ctxrx*240, wsum1*240, wsum2*240
!
!         local variables
      integer moderr, i3, i4, i5, i6, n, nogo, ire, nl, ks, kl
      integer kont, ierr1, ierr2, ierr3, ilat, ilon, nw, kf, nd, nmeth
      integer kss
      integer ivals(8)
      integer nk(5), kndx(5)
      character*1 cz, chkn, cns, cew, cbn
      character rsta*4
      character date*8, time*10, zone*5
      character*10 pdtg, fdtg
      character line*80, word*16, wrds(5)*10, accy*3, meth(5)*4
!
      data meth/'SATL', 'AIRC', 'SYNP', 'RADR', 'XTRP'/
      data i3/3/, i4/4/, i5/5/, i6/6/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (33,*) 'INTO lodem1b to process: '
      do n=nsl, nll 
        write (33,'(i3,1x,a70)') n, cmsg(n)(1:70)
      enddo
      write (33,*)
!
      ierr  = 0
      nogo  = 0
      ire   = 0
cx  must initialize this to one too!  bs 2/12/96
      ks    = 1
!
!                   extract initial warning dtg (ddhhmm)
!
      nl   = nsl
      word = ' '
      call extncn (cmsg(nl),ks,word,cz,chkn,kl,ierr1)
      if (ierr1 .eq. 0) then
        call numbck (word,i6,chkn,ierr1)
        if (ierr1 .ne. 0)
     &      write (33,*) 'prcwrn, lodem1b, dtg failed checksum'
      endif
      if (ierr1 .eq. 0) then
!
!          ************** load day and hour of initial position ********
!
        wsum1(7:10) = word(1:4)
!
!          ************** load year and month of initial position ******
!
        if (ctxrx(11:16) .ne. 'XXXXXX') then
!                   use year and month of message dtg
          wsum1(1:6) = ctxrx(11:16)
        else
!                   use year and month of message receipt dtg
          wsum1(1:6) = ctxrx(24:29)
        endif
        write(*,*) 'wsum(1)= ',wsum1(1:40)
!
!                   obtain 24 hour time of system
!
cx      call date_and_time (date,time,zone,ivals)
!
!                   set time window, pdtg = past_dtg of window
!                                    fdtg = future_dtg of window
!
cx      if (ivals(5) .ge. 18) then
cx        pdtg = csdtg
cx      elseif (ivals(5) .ge. 12) then
cx        call dtgmod (csdtg,-6,pdtg,moderr)
cx      elseif (ivals(5) .ge. 6) then
cx        pdtg = csdtg
cx      else
cx        call dtgmod (csdtg,-6,pdtg,moderr)
cx      endif
cx      call dtgmod (csdtg,+12,fdtg,moderr)
cx      if (moderr .ne. 0) then
cx         write(33,*) 'dtgmod error= ',moderr,' csdtg= ',csdtg
cx      endif
!
!                   check that warning is within time window
!
cx      if (wsum1(1:10) .lt. pdtg) then
cx        write (*,*) ' ***** warning too old to process'
cx        write (33,*) ' prcwarn, lodem1b, dtg too old to process'
cx        nogo = -1
cx        goto 999
!
cx      elseif (wsum1(1:10) .gt. fdtg) then
cx        write (*,*) ' ***** warning too far into future'
cx        write (33,*) ' prcwrn, lodem1b, dtg too far into future'
cx        nogo = -1
cx        goto 999
!
cx      endif
      else
        ire = ire +1
        write (*,*) 'prcwrn, lodem1b missing/bad initial dtg'
        write (33,*) 'prcwrn, lodem1b missing/bad initial dtg'
      endif
!
!                   check tropical cyclone warning summary history
!
      line = wsum1(1:80)
!                   dtg        cy id       warn nr     name
cx    call chkhist (line(1:10),line(12:14),line(27:29),line(16:25),
!                  msg dtg
cx   &              ctxrx,kont)
cx    if (kont .eq. 0) then
!               cyclone warning found in history file
cx      write (*,*) ' ***** cyclone found in history *****'
cx      write (33,*) ' prcwrn, lodem1b, cyclone found in history *****'
cx      nogo = -1
cx      goto 999
!
cx    endif
!
!                   check validity of NEOC cyclone number
!
      if (wsum1(12:14) .eq. 'XXL') then
!                   see if call to history fixed this error
        if (line(12:13) .ne. 'XX') wsum1(12:13) = line(12:13)
      endif
!
!         ****************** load tau 000 ******************************
!
      wsum2(2:4) = '000'
!
!                   extract initial latitude
!
      ks   = 10
      word = ' '
      call extncn (cmsg(nl),ks,word,cns,chkn,kl,ierr2)
      if (ierr2 .eq. 0) then
        call numbck (word,i4,chkn,ierr2)
        if (ierr2 .ne. 0) then
          write (*,*) 'prcwrn, lodem1b failed initial lat check sum'
          write (33,*) 'lodem1b, failed initial lat check sum'
        endif
      endif
      if (cns.eq.'N' .or. cns.eq.'S') then
        if (line(14:14) .ne. 'Y') then
          cbn = line(14:14)
          if (cns .eq. 'N') then
            if (cbn.ne.'A' .and. cbn.ne.'B' .and. cbn.ne.'W' .and.
     &          cbn.ne.'C' .and. cbn.ne.'E' .and. cbn.ne.'L') then
              write (33,*) 'prcwrn, lodem1b basin latitude conflict'
              ire   = ire +1
              ierr2 = -1
            endif
          else
            if (cbn.ne.'S' .and. cbn.ne.'P') then
              write (33,*) 'prcwrn, lodem1b basin latitude conflict'
              ire   = ire +1
              ierr2 = -1
            endif
          endif
        endif
      endif
      if (ierr2 .eq. 0) then
        call omitpd (word,i3)
        read (word,'(i3)') ilat
cx      if (ilat.ge.50 .and. ilat.le.600) then
        if (ilat.ge.10 .and. ilat.le.650) then
!
!             ************* load initial latitude *********************
!
          wsum2(6:8) = word(1:3)
          wsum2(9:9) = cns
        else
          write (33,*) 'prcwrn, lodem1b latitude out of range'
          ire = ire +1
        endif
      endif
!
!                   extract initial longitude
!
      rsta = ctxrx(6:9)
      ks   = kl
      word = ' '
      call extncn (cmsg(nl),ks,word,cew,chkn,kl,ierr3)
      if (ierr3 .eq. 0) then
!                   allow neoc to omit leading zero in longitude
        if (rsta .eq. 'NEOC') call neocln (word)
        call numbck (word,i5,chkn,ierr3)
        if (ierr3 .ne. 0)
     &     write (33,*) 'prcwrn, lodem1b failed initial lon check sum'
      endif
      if (cew.eq.'E' .or. cew.eq.'W') then
        if (line(14:14) .ne. 'Y') then
          cbn = line(14:14)
          if (cew .eq. 'E') then
cx  added E and C ... bs 9/4/97
            if (cbn.ne.'A' .and. cbn.ne.'B' .and. cbn.ne.'W' .and.
     &          cbn.ne.'S' .and. cbn.ne.'P' .and. cbn.ne.'C' .and.
     &          cbn.ne.'E') then
              write (33,*) 'prcwrn, lodem1b basin longitude conflict'
              ire   = ire +1
              ierr3 = -1
            endif
          else
            if (cbn.ne.'C' .and. cbn.ne.'E' .and. cbn.ne.'P' .and.
     &          cbn.ne.'L') then
              write (33,*) 'prcwrn, lodem1b basin longitude conflict'
              ire   = ire +1
              ierr3 = -1
            endif
          endif
        endif
      endif
      if (ierr3 .eq. 0) then
        call omitpd (word,i4)
        read (word,'(i4)') ilon
        if (ilon.ge.100 .and. ilon.le.1800) then
!
!             ************* load initial longitude *********************
!
          wsum2(11:14) = word(1:4)
          wsum2(15:15) = cew
        else
          write (33,*) 'prcwrn, lodem1b longitude out of range'
          ire = ire +1
        endif
      else
        ire = ire +1
      endif
!
!                   obtain past movement
!
      nl = nl +1
      wrds(1) = 'MOVEMENT  '
      nk(1)   = 9
      wrds(2) = 'POSITION  '
      nk(2)   = 9
      nw      = 2
      ks      = 1
      call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)
      if (kl .eq. 1) then
!
!                   extract past movement
!
        ks = 22
        call fnumfd (cmsg(nl),ks,word,nd,kf)
        if (nd .eq. 3) then
!
!           ******************* load past direction of motion ********
!
          wsum1(35:37) = word(1:3)
!
!                   extract past movement
!
          ks = kf +nd
          call fnumfd (cmsg(nl),ks,word,nd,kf)
          if (nd .eq. 2) then
!
!           ******************* load past speed of motion ********
!
            wsum1(39:40) = word(1:2)
          else
            write (33,*) 'prcwrn, lodem1b missing speed of motion'
          endif
        else
          wrds(1) = 'STATION   '
          nk(1)   = 7
          nw      = 1
          ks      = 22
          call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)
          if (kl .eq. 1) then
!
!           ******************* load past quasistationary motion ******
!
            wsum1(35:40) = '000 00'
          else
            write (33,*) 'prcwrn, lodem1b missing direction of motion'
            ire = ire +1
          endif
        endif
      elseif (kl .eq. 2) then
        nl = nl -1
      else
        write (33,*) 'prcwrn, lodem1b missing past motion'                      
        ire = ire +1
      endif                                                                     
!
!                   extract accuracy                                            
!                                                                               
      accy = ' '
      nl   = nl +1
      wrds(1) = 'POSITION  '                                                    
      nk(1)   = 9
      nw      = 1                                                               
      ks      = 1                                                               
      call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)                                
      if (kl .eq. 1) then
        ks = 22                                                                 
        call fnumfd (cmsg(nl),ks,word,nd,kf)
        if (nd .eq. 3) then
!
!           ******************* save accuracy of position *************         
!                                                                               
          accy = word(1:3)                                                      
!                                                                               
        else                                                                    
          write (33,*) 'prcwrn, lodem1b missing accuracy'
          ire = ire +1                                                          
        endif
      else                                                                      
        write (33,*) 'prcwrn, lodem1b missing accuracy'                         
        ire = ire +1                                                            
      endif                                                                     
!                                                                               
!                   obtain method(s) of fixing position
!                                                                               
      nmeth = 0
      nl    = nl +1                                                             
      if (nl .le. nll) then                                                     
        wrds(1) = 'POSITION  '
        nk(1)   = 9                                                             
        nw      = 1                                                             
        ks      = 1
        call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)                              
        if (kl .eq. 1) then
          wrds(1) = 'LOCATED BY'                                                
          nk(1)   = 10
          wrds(2) = ' BY       '                                                
          nk(2)   = 4                                                           
          nw      = 2                                                           
          ks      = 20
          call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)                            
          if (kl .ne. 0) then
            ks      = kf +nk(kl)                                                
            wrds(1) = 'SATELLITE '                                              
            nk(1)   = 9                                                         
            wrds(2) = 'AIRCRAFT  '
            nk(2)   = 8                                                         
            wrds(3) = 'SYNOPTIC  '
            nk(3)   = 8
            wrds(4) = 'RADAR     '
            nk(4)   = 5                                                         
            wrds(5) = 'EXTRAPOLAT'                                              
            nk(5)   = 10                                                        
            nw      = 5                                                         
            call wrdsfd (cmsg(nl),ks,wrds,nk,nw,kndx)
            kss = 37
            do n=1, nw
              if (kndx(n) .ne. 0) then
                kss = kss +5
!
!           ******************* load method of position *************
!
                wsum1(kss:kss+3) = meth(n)
                nmeth = nmeth +1
              endif
            enddo
            nl = nl +1
            if (nl .le. nll) then
              ks = 1
              call wrdsfd (cmsg(nl),ks,wrds,nk,nw,kndx)
              do n=1, nw
                if (kndx(n) .ne. 0) then
                  kss = kss +5
!
!           ******************* load method of position *************
!
                  wsum1(kss:kss+3) = meth(n)
                  nmeth = nmeth +1
                endif
              enddo
            endif
          endif
        endif
      endif
      if (accy .ne. ' ') then

        if (nmeth .gt. 0) then
          kss = kss +5
        else
          kss = 47
        endif
!
!           ******************* load accuracy of position *************
!
        wsum1(kss:kss+2) = accy
      endif
      if (ire .ne. 0) then
        ierr = iabs(ire)
        write (33,*) 'lodem1b had ',ire,' errors in processing'
      endif
      write (33,*) 'RESULTS:'
      write (33,'(1x,a240)') wsum1
      write (33,'(1x,a240)') wsum2
      write (33,*)
  999 continue
      if (nogo .lt. 0) ierr = -1
      return
!
      end
      subroutine lodem2 (cmsg,lng,nsl,nll,nwx,cwsum,casum,ir2)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lodem2
!
!  DESCRIPTION:  load from maximum wind to end of forecast information
!                for analysis and forecast positions in warning
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call lodem2 (cmsg,lng,nsl,nll,nwx,cwsum,casum,ir2)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    casum           char*240       output   warning summary part 2 - AMP
!                                            section
!    cmsg            char*80        input    warning message
!    cwsum           char*240       in?/out  warning summary, part 1
!    ir2             integer        in?/out  error flag, 0 - no error
!    lng             integer        input    length of message, in lines
!    nll             integer        input    ending line for search
!    nsl             integer        input    starting line for search
!    nwx             integer        input    flag for type of data
!                                              1 - initial (analysis)
!                                              2 - forecast
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!    bad or missing data       flag error and keep checking
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         fnumfd      find first number after give column location
!         lodamp      load amplification line of summary
!         radcrp      obtain radius description
!         wrdfnd      find word from group of words
!         wrdsfd      identifiy which words were found
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cnum       char*10    working string for number
!         ire        integer    sum of internal errors
!         kasl       integer    starting and ending column of amplification
!                               information
!         kf         integer    first character position of requested data
!         kl         integer    last character position used
!         kndx       integer    array for indicies of words found
!         ks         integer    starting column for search
!         kss        integer    starting column of data
!         match      integer    count of match
!         nd         integer    count of digits found
!         nk         integer    array of character counts in wrds
!         nl         integer    line number being processed
!         nrad       integer    number of radii
!         nrmk       integer    number of internal remarks found in
!                               message - amplifications to forecast
!         nw         integer    number of words for search
!         wrds       char*10    array for requested words for search
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lng, nsl, nll, nwx, ir2
      character cmsg(lng)*80, cwsum*240, casum*240
!
!         local variables
      integer kasl, ks, kf, kl, kss, n, nl, nd, nw, nrmk, nrad, match
      integer ire
      integer nk(2), kndx(2)
      character wrds(2)*10, cnum*16
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (33,*) 'INTO lodem2 to process: '
      do n=nsl, nll
        write (33,'(i3,1x,a70)') n,cmsg(n)(1:70)
      enddo
      write (33,*)
!
!                   obtain maximum sustained wind speed
!
      ir2 = 0
      ire = 0
      nl      = nsl
      wrds(1) = 'MAX SUSTAI'
      nk(1)   = 10
      wrds(2) = 'SUSTAINED '
      nk(2)   = 9
      nw      = 2
      ks      = 1
      call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)
      if (kl .gt. 0) then
        ks = 20
        call fnumfd (cmsg(nl),ks,cnum,nd,kf)
        if (nd .eq. 2) then
          wrds(1) = 'WINDS     '
          nk(1)   = 6
          wrds(2) = ' KT       '
          nk(2)   = 4
          nw      = 2
          call wrdsfd (cmsg(nl),ks,wrds,nk,nw,kndx)
          match = 0
          do n=1, nw
            if (kndx(n) .ne. 0) match = match +1
          enddo
          if (match .eq. 2) then
            cnum(3:3) = cnum(2:2)
            cnum(2:2) = cnum(3:3)
            cnum(1:1) = '0'
            nd = 3
          endif
        endif
        if (nd .eq. 3) then
!
!           ***************** load max wind speed **************
!
          cwsum(17:19) = cnum(1:3)
        else
          ire = ire +1
        endif
      else
        ire = ire +1
      endif
      if (ire .ne. 0) then
        if (nwx .eq. 1) then
          write (*,*) 'prcwrn, lodem2 cant find INITIAL max wind'
        else
          write (*,*) 'prcwrn, lodem2 cant find FORECAST max wind'
        endif
      endif
!
      nrmk  = 0
      nrad  = 0
      kss   = 21
!
  200 continue
      nl = nl +1
      if (nl .le. nll) then
        wrds(1) = 'RADIUS OF '
        nk(1)   = 10
        nw      = 1
        ks      = 1
        call wrdfnd (cmsg(nl),ks,wrds,nk,nw,kf,kl)
        if (kl.eq.1 .and. kf.eq.1) then
!
!                   process wind radii info
!
          nrad = nrad +1
          call fnumfd (cmsg(nl),ks,cnum,nd,kf)
          if (nd .eq. 2) then
            wrds(1) = ' KT WINDS '
            nk(1)   = 6
            nw      = 1
            ks      = kf +1
            call wrdsfd (cmsg(nl),ks,wrds,nk,nw,kndx)
            if (kndx(1) .ne. 0) then
              cnum(3:3) = cnum(2:2)
              cnum(2:2) = cnum(1:1)
              cnum(1:1) = '0'
              nd = 3
            endif
          endif
          if (nd .eq. 3) then
!
!           ************** load radius wind speed **********************
!
            cwsum(kss:kss+3) = 'R' // cnum(1:3)
            kss = kss +5
!
!                   obtain first radius of winds
!                                                                               
            ks = kf +nd
            call fnumfd (cmsg(nl),ks,cnum,nd,kf)
            if (nd .eq. 2) then                                                 
              cnum(3:3) = cnum(2:2)                                             
              cnum(2:2) = cnum(1:1)                                             
              cnum(1:1) = '0'                                                   
              nd = 3                                                            
            endif                                                               
            if (nd .eq. 3) then
              cwsum(kss:kss+2) = cnum(1:3)
              kss = kss +4                                                      
              ks  = kf +nd
!                                                                               
!                   obtain radius description                                   
!                                                                               
              call radcrp (cmsg,nll,nl,ks,cwsum,kss)
!
            else
              ire = ire +1
              if (nwx .eq. 1) then                                              
                write (*,*) 'prcwrn, lodem2 cant get INITIAL radius'
              else                                                              
                write (*,*) 'prcwrn, lodem2 cant get FORECAST radius'           
              endif                                                             
              cwsum(kss:kss+2) = 'XXX'
              kss = kss +4
              goto 200                                                          
!                                                                               
            endif                                                               
!                                                                               
!                   look for more radii                                         
!
  300       continue
            if (nl+1 .le. nll) then
              if (cmsg(nl+1)(1:1) .ge.'0' .and.                                 
     &            cmsg(nl+1)(1:1).le.'9') then                                  
                nl = nl +1
!                                                                               
!                   obtain second and subsequent radius of winds
!                                                                               
                ks = 1
                call fnumfd (cmsg(nl),ks,cnum,nd,kf)
                if (nd .eq. 2) then                                             
                  cnum(3:3) = cnum(2:2)                                         
                  cnum(2:2) = cnum(1:1)                                         
                  cnum(1:1) = '0'                                               
                  nd = 3                                                        
                endif                                                           
                if (nd .eq. 3) then
                  cwsum(kss:kss+2) = cnum(1:3)
                  kss = kss +4                                                  
                  ks  = kf +nd
!                                                                               
!                   obtain radius description                                   
!                                                                               
                  call radcrp (cmsg,nll,nl,ks,cwsum,kss)                        
!
                endif
                goto 300
!
              endif
            endif
          else
            cwsum(kss:kss+7) = 'RXXX XXX'
            kss = kss +9
          endif
          goto 200
!
        elseif (nrad.eq.0 .and. nrmk.le.1) then
!
!                   process internal remark
!
          if (nrmk .eq. 0) then
            kasl = 10
            call lodamp (cmsg(nl),casum,kasl)
            nrmk = 1
          else
            call lodamp (cmsg(nl),casum,kasl)
            nrmk = nrmk +1
          endif
          goto 200
!
        endif
      endif
      if (nrad.eq.0 .and. cwsum(17:19).gt.'035') then
        if (nwx .eq. 1) then
          write (*,*) 'prcwrn, lodem2 no INITIAL wind radius'                   
          ire = ire +1                                                          
        else                                                                    
          write (*,*) 'prcwrn, lodem2 no FORECAST wind radius'                  
        endif                                                                   
      endif
      if (ire .ne. 0) then                                                      
        ir2 = ir2 +1                                                            
        write (*,*) 'lodem2 had ',ir2,' errors in processing'                   
      endif                                                                     
      return                                                                    
!                                                                               
      end
      subroutine lodemf (cwmsg,lng,nsl,nll,rsta,cwsum,casum,ir3)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lodemf
!
!  DESCRIPTION:
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call lodemf (cwmsg,lng,nsl,nll,rsta,cwsum,casum,ir3)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    casum           char*240       in/out   amplification section of summary
!    cwmsg           char*80        input    cyclone warning message
!    cwsum           char*240       in/out   warning section of summary
!    ir3             integer        in/out   sum of errors
!    lng             integer        input    number of lines in message
!    nll             integer        input    last line for search
!    nsl             integer        input    first line for search
!    rsta            char*4         input    four character code for receipt
!                                            from station code
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!     example of lines to process ****************
!                  1         2         3         4         5
!         12345678901234567890123456789012345678901234567890
!         12 hrs, valid at:
!         081200z1 --- 18.9n8  133.2w9
!         max sustained winds - 085 kt, gusts 105 kt
!         "comment about cyclone - going extratropical, etc" (optional)
!         radius of 050 kt winds - 050 nm east semicircle
!         040 nm elsewhere
!         radius of 035 kt winds - 125 nm northeast quadrant
!         100 nm elsewhere over water
!
!         ************** template of cwsum output **********************
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         tau  latn longt mxw rspd nmi dd ---
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         extncn      extract digits, character and digit
!         fnumfd      extract first set of digits from starting position
!         lodem2      load max wind and radii information
!         neocln      correct longitude for NEOC warnings
!         numbck      check check-sum number
!         omitpd      omit decimal point
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cew        char*1     East-West hemisphere indicator
!         chkn       char*1     checksum character
!         cns        char*1     North-Soutn hemisphere indicator
!         cnum       char*10    working character string for number
!         cz         char*1     working character for "Z"
!         i3         integer    digit 3
!         i4         integer    digit 4
!         i5         integer    digit 5
!         i6         integer    digit 6
!         ierr1      integer    dtg error flag
!         ierr2      integer    latitude error flag
!         ierr3      integer    longitude error flag
!         ilat       integer    latitude times 10
!         ilon       integer    longitude times 10
!         ire        integer    sum of errors for one set of warning lines
!         kf         integer    last column of first found set of characters
!         kl         integer    last column
!         ks         integer    starting column for search
!         nd         integer    number of digits
!         nhr        integer    forecast hour
!         nl         integer    number of line of message being processed
!         word       char*10    working character string
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer lng, nsl, nll, ir3
      character cwmsg(lng)*80, rsta*4, cwsum*240, casum*240
!
!         local variables
      integer i3, i4, i5, i6, ierr1, ierr2, ierr3, ilat, ilon, ire, kf
      integer kl, ks, nd, nhr, nl, n
      character*1 cz, chkn, cns, cew
      character cnum*16, word*10
!
      data i3/3/, i4/4/, i5/5/, i6/6/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      write (33,*) 'into lodemf to process: '
      do n=nsl, nll
        write (33,'(i3,1x,a70)') n,cwmsg(n)(1:70)
      enddo
      write (33,*)
!
      nl    = nsl
      ire   = 0
!
!                   extract tau in hrs
!
      ks    = 1
      call fnumfd (cwmsg(nl),ks,cnum,nd,kf)
      if (kf.gt.0 .and. nd.eq.2) then
!
!                   standard opertional forecast
!
        cwsum(2:4) = '0' // cnum(1:2)
        read (cnum(1:2),'(i2)') nhr
!     elseif (kf.gt.0 .and. nd.eq.3) then
!
!                   extended outlook (NOT USED YET)
!
!       cwsum(2:4) =  cnum(1:3)
!       read (cnum(1:3),'(i3)') nhr
      else
        nhr = 5
        ire = 1
        write (*,*) 'prcwrn, lodemf cant find tau'
      endif
!
!                   obtain dtg of forecast, for checking
!
      nl   = nl +1
      ks   = 1
      word = ' '
      call extncn (cwmsg(nl),ks,word,cz,chkn,kl,ierr1)
      if (ierr1 .eq. 0) then
        call numbck (word,i6,chkn,ierr1)
        if (ierr1 .ne. 0)
     &      write (*,*) 'prcwrn, lodemf failed dtg checksum'
      else
        write (*,*) 'prcwrn, lodemf missing/bad forecast dtg'
      endif
!
!                   extract forecast latitude
!
      ks   = 10
      word = ' '
      call extncn (cwmsg(nl),ks,word,cns,chkn,kl,ierr2)
      if (ierr2 .eq. 0) then
        call numbck (word,i4,chkn,ierr2)
        if (ierr2 .ne. 0)
     &     write (*,*) 'prcwrn, lodemf failed forecast lat check sum'
      endif
      if (ierr2 .eq. 0) then
        call omitpd (word,i3)
        read (word,'(i3)') ilat
cx      if (ilat.ge.50 .and. ilat.le.650) then
        if (ilat.ge.10 .and. ilat.le.650) then
!
!             ************* load forecast latitude *********************
!
          cwsum(6:8) = word(1:3)
          if (cns.eq.'N' .or. cns.eq.'S') then
            cwsum(9:9) = cns
          else
            write (*,*) 'prcwrn, lodemf hemi not N or S'
          endif
        else
          write (*,*) 'prcwrn, lodemf latitude out of range'
          ire = ire +1
        endif
      endif
!
!                   extract forecast longitude
!
      ks   = kl
      word = ' '
      call extncn (cwmsg(nl),ks,word,cew,chkn,kl,ierr3)
      if (ierr3 .eq. 0) then
!                   allow neoc to omit leading zero in longitude
        if (rsta .eq. 'NEOC') call neocln (word)
        call numbck (word,i5,chkn,ierr3)
        if (ierr3 .ne. 0)
     &     write (*,*) 'prcwrn, lodemf failed forcast lon check sum'
      endif
      if (ierr3 .eq. 0) then
        call omitpd (word,i4)
        read (word,'(i4)') ilon
        if (ilon.ge.100 .and. ilat.le.1800) then
!
!             ************* load initial longitude *********************
!
          cwsum(11:14) = word(1:4)
          if (cew.eq.'W' .or. cew.eq.'E') then
            cwsum(15:15) = cew
          else
            write (*,*) 'prcwrn, lodemf long hemi not W or E'
            ire = ire +1
          endif
        else
          write (*,*) 'prcwrn, lodemf longitude out of range'
          ire = ire +1
        endif
      endif
      nl = nl +1
      if (nl .le. nll) then
!
!                   obtain forecast maximum sustained wind speed
!                   and wind radii and descritptions
!
        call lodem2 (cwmsg,lng,nl,nll,nhr,cwsum,casum,ire)
      endif
      if (ire .ne. 0) then
        ir3 = ir3 +1
        write (*,*) 'lodemf had ',ire,' errors in processing'
      endif
      write (6,'(1x,a79)') cwsum(1:79)
      write (33,*) 'RESULTS:'
      write (33,'(a240)') cwsum
      if (casum(11:11) .ne. ' ') then
        write (6,'(1x,a79)') casum(1:79)
        write (33,'(a240)') casum
      endif
      write (33,*)
      return
!
      end
      subroutine matwd1 (word,nw,ckey,nc,nk,key)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  matwd1
!
!  DESCRIPTION:  match word with word(s) in ckey, count characters for
!                full match
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call matwd1 (word,nw,ckey,nc,nk,key)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    ckey            char*10        input    array of words to search
!    key             integer        output   index to found match or 0
!    nc              integer        input    number of characters in words
!    nk              integer        input    number of words to search
!    nw              integer        input    number of characters in word
!    word            char*20        input    word to be matched
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:  none
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer key
      integer j, k, nc, nk, nw
      character word*20, ckey(nk)*10
!
!         local variables
!
      dimension nc(nk)
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      key = 0
      do k=1, nk
!
!                   check that number of characters match
!
        if (nw .eq. nc(k)) then
          do j=1, 10
            if (word(j:j) .ne. ckey(k)(j:j)) goto 120
!
            if (j .eq. nc(k)) then
              key = k
              goto 130
!
            endif
          enddo
        endif
  120   continue
      enddo
  130 continue
      return
!
      end
      subroutine matwd2 (word,ckey,nc,nk,key)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  matwd2
!
!  DESCRIPTION:  matching of word with set of possible words
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call matwd2 (word,ckey,nc,nk,key)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    ckey            char*10        input    array of words for matching
!    key             integer        output   index to matched word, or zero
!    nc              integer        input    number of characters in words
!    nk              integer        input    number of characters in word
!    word            char*20        input    master word
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!     warning:  words to match must not be similar, see matwd1 for more
!               string matching
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:  none
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer key, nk
      integer nc(nk)
      character word*20, ckey(nk)*10
!
!         local variables
      integer j, k
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      key = 0
      do k=1, nk
        do j=1, 10
          if (word(j:j) .ne. ckey(k)(j:j)) goto 120
!
          if (j .eq. nc(k)) then
            key = k
            goto 130
!
          endif
        enddo
  120   continue
      enddo
  130 continue
      return
!
      end
      subroutine neocln (clon)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  neocln
!
!  DESCRIPTION:  Correct longitude for NEOC, as required
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call neocln (clon)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    clon            char*10        in/out   longitude in character format
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     Bad data for longitude   Do not change data, no signal required
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cx         char*1     working character
!         ierr       integer    error flag
!         nn         integer    column of start of longitude
!         num1       integer    number of digits in longitude
!         num2       integer    checksum digit
!         numc       integer    number of characters
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      character*10 clon
!
!         local variables
      integer n, nn, num1, numc, num2, ierr
      character*1 cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nn   = 0
      num1 = 0
      numc = 0
      num2 = 0
      ierr = 0
      do n=1, 10
        cx = clon(n:n)
        if (cx.ne.' ' .and. cx.ne.'.') then
          if (numc .eq. 0) then
            if (cx.ge.'0' .and. cx.le.'9') then
              num1 = num1 +1
              if (num1 .eq. 1) nn = n
            elseif (cx .eq. 'W') then
              numc = numc +1
            else
              ierr = ierr +1
            endif
          elseif (num1 .gt. 0) then
            if (cx.ge.'0' .and. cx.le.'9') then
              num2 = num2 +1
            else
              ierr = ierr +1
            endif
          else
            ierr = ierr +1
          endif
        endif
      enddo
      if (ierr .eq. 0) then
        if (num1.eq.3 .and. numc.eq.1 .and. num2.eq.1) then
!
!                 longitude appears good except for missing leading zero
!
          do n=9, nn, -1
            clon(n+1:n+1) = clon(n:n)
          enddo
!                   add leading zero, when it is left out by NEOC
          clon(nn:nn) = '0'
        endif
      endif
      return
!
      end
      subroutine numbck (cnum,nc,chkn,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  numbck
!
!  DESCRIPTION:  Verify number by checking with checksum
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call numbck (cnum,nc,chkn,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    chkn            char*1         input    character of checksum
!    cnum            char*10        input    character of leading digits
!    ierr            integer        output   error flag, 0 - no error
!    nc              integer        input    number of leading digits
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     formal checksum not      set error flag, and exit
!     equal sum of digits
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         ncksm      integer    integer of formal chksum
!         nn         integer    leading digit
!         nsum       integer    sum of leading digits to build checksum
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nc, ierr
      character cnum*16, chkn*1
!
!         local variables
      integer n, nn, nsum, ncksm
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr = 0
      nsum = 0
      do n=1, nc
!
!                   sum leading digits in cnum
!
        if (cnum(n:n).ne.' ' .and. cnum(n:n).ne.'.') then
          if (cnum(n:n).ge.'0' .and. cnum(n:n).le.'9') then
            read (cnum(n:n),9001) nn
            nsum = nsum +nn
          else
            ierr = -1
          endif
        endif
      enddo
 9001 format (i1)
      if (ierr .eq. 0) then
!
!                   calculate checksum
!
  110   continue
        if (nsum -10 .ge. 0) then
          nsum = nsum -10
          goto 110
!
        endif
        if (chkn(1:1).ge.'0' .and. chkn(1:1).le.'9') then
!
!                   convert formal checksum to integer and compare
!                   with derived checksum
!
          read (chkn(1:1),9001) ncksm
          if (ncksm .ne. nsum) ierr = -1
        else
          ierr = -1
        endif
      endif
      return
!
      end
      subroutine omitpd (cnum,nc)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  omitpd
!
!  DESCRIPTION:  omit period in character string
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call omitpd (cnum,nc)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cnum            char*10        in/out   string w/o "."
!    nc              integer        input    number of characters in cnum
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cx         char*1     working character
!         k          integer    number of character digits
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nc
      character*10 cnum
!
!         local variables
      integer n, k, l
      character*1 cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      k = 0
      do n=1, 10
        if (k .lt. nc) then
          cx = cnum(n:n)
          if (cx.ge.'0' .and. cx.le.'9') then
!
!                   load cnum with numerals only, left justified
!
            k = k +1
            cnum(k:k) = cx
          endif
        endif
      enddo
      if (k .lt. nc) then
!
!                   numerals are not right justified, relative to nc
!                   right justify numerals
!
        n = nc
        do l=k, 1, -1
          cnum(n:n) = cnum(l:l)
          n = n -1
        enddo
!
!                   load leading spaces with zero
!
        do l=n, 1, -1
          cnum(l:l) = '0'
        enddo
      endif
      return
!
      end
      subroutine origid (cline,orgsta)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  origid
!
!  DESCRIPTION:  obtain originator's code designation
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call origid (cline,orgsta)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline           char*80        input    character string
!    orgsta          char*4         output   originator's code
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         strngf      check for a character string match
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         kc         integer    matching flag, 0 - no match
!         nc         integer    number of characters in string to match
!         word       char*80    string to be matched
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      character cline*80, orgsta*4
!
!         local variables
      integer nc, kc
      character*80 word
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                  process FROM line, look for releasing center
!
      word = 'JTWC'
      nc   = 4
      call strngf (cline,word,nc,kc)
      if (kc .eq. 0) then
!                 JTWC  not found, so look for PEARL
        word = 'PEARL'
        nc   = 5
        call strngf (cline,word,nc,kc)
        if (kc .eq. 0) then
!                 PEARL not found, so look for NORFOLK
          word = 'NORFOLK'
          NC   = 7
          call strngf (cline,word,nc,kc)
          if (kc .ne. 0) orgsta = 'NEOC'
        else
          orgsta = 'NWOC'
        endif
      else
        orgsta = 'JTWC'
      endif
      if (kc .eq. 0) then
        orgsta = 'UNKN'
        write (*,*) '***** UNKNOWN RELEASING CENTER ',cline
        write (33,*) '***** UNKNOWN RELEASING CENTER ', cline
      endif
      return
!
      end
      subroutine radcrp (cwmsg,nt,ns,ks,cwsum,kss)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  radcrp
!
!  DESCRIPTION:  Obtain radius description(s)
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call radcrp (cwmsg,nt,ns,ks,cwsum,kss)
!
!  PARAMETERS:
!       Name         Type       Usage        Description
!    ----------   ----------   -------  ----------------------------
!    cwmsg        char*80      input    cyclone warning message
!    cwsum        char*240     output   line of warning summary
!    ks           integer      in/      starting message column for processing
!                                /out   ending message column of processing
!    kss          integer      in       starting summary column for loading
!                                /out   ending summary column of loading
!    ns           integer      in/      starting line number of message
!                                /out   last line processed
!    nt           integer      input    dimension of cwmsg
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         chkcrp      check for end of radius description(s)
!         degrbl      degarble
!         matwd1      match word, type1
!         matwd2      match word, type2
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         abr1       char*2     first  abreviations of radius
!         abr2       char*2     second abreviations of radius
!         abr3       char*2     third  abreviations of radius
!         camp1      char*10    first  key amplification
!         camp2      char*10    second key amplification
!         cdir       char*10    direction key words
!         cdsp       char*10    description key words
!         cv         char*1     working character
!         ierr       integer    chkcrp error flag, 0 - no error
!         ifnd       integer    success of degarble flag, >0 success
!         kdim       integer    dimension of keys and numc
!         key        integer    index to various abreviations
!         keys       char*10    radius description key words
!         ktry       integer    try/no try flag
!         kw         integer    index for wrds and ncpw
!         namp2      integer    number of characters in camp2
!         nb         integer    blank character count
!         nc         integer    non-blank character count
!         ncpw       integer    number of characters in wrds
!         ndir       integer    number of characters in cdir
!         ndsp       integer    number of characters in cdsp
!         nk         integer    index to word found
!         nks        integer    next starting column location
!         nl         integer    line of message being processed
!         nns        integer    next starting line
!         numc       integer    number of characters in keys
!         nw         integer    count of descriptive words processed
!         nwrds      integer    count of descriptive words processed
!         wrds       char*20    dynamic array for words to process
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nt, ns, ks, kss
      character cwmsg(nt)*80, cwsum*240
!
!         local variables
      integer k, kdim, key, ktry, kw, nb, nc, nk, nks, nl, nns
      integer nw, nwrds, ierr, ifnd
      integer ndir(11), ndsp(4), namp2(2), ncpw(6), numc(14)
      character*1 cv
      character*2 abr1(9), abr2(4), abr3(2)
      character*10 cdir(11), cdsp(4), camp1, camp2(2)
!                dimension of keys must not be greater than nn in degrbl
      character wrds(6)*20, keys(14)*10
!
!                   note: all is short for all quadrants (NEOC)
      data cdir/'NORTHEAST', 'SOUTHEAST', 'SOUTHWEST', 'NORTHWEST',
     &          'NORTH',     'EAST',      'SOUTH',     'WEST',
     &          'ELSEWHERE',  'OVER', 'ALL'/
      data ndir/9, 9, 9, 9, 5, 4, 5, 4, 9, 4, 3/
!
      data abr1/'NE', 'SE', 'SW', 'NW', 'NN', 'EE', 'SS', 'WW', 'EW'/
!
      data cdsp/'SEMI', 'QUAD', 'SEMICIRCLE', 'QUADRANT'/
      data ndsp/4, 4, 10, 8/
!
      data abr2/'SC', 'QD', 'SC', 'QD'/
!
      data camp1/'OVER'/
      data camp2/'WATER', 'LAND'/
      data namp2/5, 4/
!
      data abr3/'OW', 'OL'/
!
      data keys/'EAST', 'WEST', 'OVER', 'LAND',                         &
     &          'NORTH', 'SOUTH', 'WATER',                              &
     &          'QUADRANT',                                             &
     &          'NORTHEAST', 'NORTHWEST', 'SOUTHEAST', 'SOUTHWEST',     &
     &          'ELSEWHERE', 'SEMICIRCLE'/
      data numc/4,4,4,4,5,5,5,8,9,9,9,9,9,10/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nl = ns
      nw =  0
      nc =  0
      nb =  0
      wrds(1) = ' '
      ncpw(1) = 0
!
!                   parse line of message for description of one radius
!
      do k=ks, 80
        cv = cwmsg(nl)(k:k)
        if (cv .eq. ' ') then
          nc = 0
          nb = nb +1
        elseif (cv.ge.'A' .and. cv.le.'Z') then
          if (nc.eq.0 .and. nb.le.1) then
            nw = nw +1
            if (nw .eq. 7) goto 130
!
            wrds(nw) = ' '
          endif

          nc = nc +1
          if (nc .le. 20) then
!
!                   build descriptive words for processing
!
            wrds(nw)(nc:nc) = cv
            ncpw(nw) = nc
            nb = 0
          endif
        elseif (cv.ge.'0' .and. cv.le.'9') then
!                   found next radius, so processing is over
          goto 130
!
        endif
      enddo
!                   signal that end of line has been reached
      nks = 81
      if (nl+1 .le. nt) then
!
!                   see if radius description continues on next line
!
        if (cwmsg(nl+1)(1:1).ne.'R' .and. (cwmsg(nl+1)(1:1).ge.'A'
     &     .and. cwmsg(nl+1)(1:1).le.'Z')) then
          nl = nl +1
          nc = 0
          nb = 0
!
!                   process next line of message for the rest of description
!
          do k=1, 80
            cv = cwmsg(nl)(k:k)
            if (cv .eq. ' ') then
              nc = 0
              nb = nb +1
            elseif (cv.ge.'A' .and. cv.le.'Z') then
              if (nc.eq.0 .and. nb.le.1) then
                nw = nw +1
                if (nw .eq. 7) goto 130
!
                wrds(nw) = ' '
              endif
              nc = nc +1
              if (nc .le. 20) then
                wrds(nw)(nc:nc) = cv
                ncpw(nw) = nc
                nb = 0
              endif
            elseif (cv.ge.'0' .and. cv.le.'9') then
!                   found next radius, so processing is over
              goto 130
!
            endif
          enddo
!                   signal that end of line has been reached
          nks = 81
        endif
      endif
  130 continue
!
!                   process description(s) and load summary
!
      if (nw .gt. 6) write (*,*) 'prcwrn, radcrp too many words $$$$$'
      nw  = min0 (6,nw)
      nns = nl
      if (nks.eq. 81) nks = 1
!
!                   set dimension of keys and numc for s/r degrbl
!
      kdim = 14
!
!                   note, first word should be nm with ncpw(1) of 2
!
      if (nw.gt.1 .or. ncpw(1).gt.2) then
        nwrds = nw
!
!                   set index to wrds for signifcant key word
!
        if (ncpw(1) .le. 2) then
!                   first word of nm is not a significant key word
          kw = 2
        else
!                   set kw to 1 for nonstandard message
          kw = 1
        endif
!                   set dimension of cdir and ndir
        nw   = 11
        ktry = 0
  140   continue
!
!                   search for match in cdir array for first key word
!
        call matwd1 (wrds(kw),ncpw(kw),cdir,ndir,nw,key)
        if (key .gt. 0) then
          if (key .le. 9) then
            cwsum(kss:kss+1) = abr1(key)
            kss = kss +3
            if (key .lt. 9) then
!
!                   direction was first match, now look for sc or qd
!                   in next wrds
!
              kw = kw +1
              if (kw .le. nwrds) then
!                         set dimension of cdsp and ndsp
                nw   = 4
                ktry = 0
  150           continue
!
!                   search for match in cdsp array for second key word
!
                call matwd2 (wrds(kw),cdsp,ndsp,nw,key)
                if (key .gt. 0) then
                  cwsum(kss:kss+1) = abr2(key)
                elseif (ktry .eq. 0) then
!
!                          check on garble problem
!
                  ktry = -1
                  call degrbl (wrds(kw),ncpw(kw),keys,numc,kdim,nk,ifnd)
                  if (ifnd .gt. 0) then
!                         correct spelling of key word and try again
                    wrds(kw) = keys(ifnd)
                    ncpw(kw) = nk
                    goto 150
!
                  else
                    write (*,*) 'prcwrn, radcrp no degrbl match for ',
     &                            wrds(kw),' $$$$$'
                    call chkcrp (wrds(kw),ierr)
                    if (ierr .ne. 0) then
                      cwsum(kss:kss+1) = 'YY'
                    else
!                         key word found without ending in :
                      goto 200
!
                    endif
                  endif
                else
                  cwsum(kss:kss+1) = 'YY'
                endif
              else
                cwsum(kss:kss+1) = 'YY'
              endif
              kss = kss +3
            endif
            kw  = kw +1
!
!                   see if description continues
!
            if (kw .le. nwrds) then
!
!                   next word can only be over in standard message
!
              if (wrds(kw)(1:10) .eq. camp1) then
                kw = kw +1
!
!                  over has been found, in standard message, next word
!                  must be water, but NEOC includes land - so must check
!
                if (kw .le. nwrds) then
                  nw   = 2
                  ktry = 0
  160             continue
                  call matwd2 (wrds(kw),camp2,namp2,nw,key)
                  if (key .gt. 0) then
                    cwsum(kss:kss+1) = abr3(key)
                  elseif (ktry .eq. 0) then
!
!                          check on garble problem
!
                    ktry = -1
                    call degrbl (wrds(kw),ncpw(kw),keys,numc,kdim,nk,
     &                           ifnd)
                    if (ifnd .gt. 0) then
                      wrds(kw) = keys(ifnd)
                      ncpw(kw) = nk
                      goto 160
!
                    else
                      write (*,*) 'prcwrn, radcrp no degrbl match',
     &                            ' for ',wrds(kw),' $$$$$'
                      call chkcrp (wrds(kw),ierr)
                      if (ierr .ne. 0) then
                        cwsum(kss:kss+1) = 'YY'
                      else
!                         key word found without ending in :
                        goto 200
!
                      endif
                    endif
                  else
                    cwsum(kss:kss+1) = 'YY'
                  endif
                else
                  cwsum(kss:kss+1) = 'YY'
                endif
                kss = kss +3
              endif
            endif
          elseif (key .eq. 10) then
!
!               key word of over has been found, check for water or land
!               (thanks to NEOC's nonstandard warnings)
!
            kw = kw +1
            if (kw .le. nwrds) then
              nw   = 2
              ktry = 0
  170         continue
              call matwd1 (wrds(kw),ncpw(kw),camp2,namp2,nw,key)
              if (key .gt. 0) then
                cwsum(kss:kss+1) = abr3(key)
              elseif (ktry .eq. 0) then
!
!                                check on garble problem
!
                ktry = -1
                call degrbl (wrds(kw),ncpw(kw),keys,numc,kdim,nk,ifnd)
                if (ifnd .gt. 0) then
                  wrds(kw) = keys(ifnd)
                  ncpw(kw) = nk
                  goto 170
!
                else
                  write (*,*) 'prcwrn, radcrp no degrbl match for ',
     &                         wrds(kw),' $$$$$'
                  call chkcrp (wrds(kw),ierr)
                  if (ierr .ne. 0) then
                    cwsum(kss:kss+1) = 'YY'
                  else
!                         key word found without ending in :
                    goto 200
!
                  endif
                endif
              else
                cwsum(kss:kss+1) = 'YY'
              endif
            else
              cwsum(kss:kss+1) = 'YY'
            endif
            kss = kss +3
          endif
        elseif (ktry .eq. 0) then
!
!                   check on garble problem
!
          ktry = -1
          call degrbl (wrds(kw),ncpw(kw),keys,numc,kdim,nk,ifnd)
          if (ifnd .gt. 0) then
            wrds(kw) = keys(ifnd)
            ncpw(kw) = nk
            goto 140
!
          else
            write (*,*) 'prcwrn, radcrp no degrbl match for ',
     &                   wrds(kw),' $$$$$'
            call chkcrp (wrds(kw),ierr)
            if (ierr .ne. 0) then
              cwsum(kss:kss+1) = 'YY'
              kss = kss +3
            else
!                         key word found without ending in :
              goto 200
!
            endif
          endif
        else
          cwsum(kss:kss+1) = 'YY'
          kss = kss +3
        endif
      endif
  200 continue
      ns = nns
      ks = nks
      return
!
      end
      subroutine remdup1 (cline)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  remdup1
!
!  DESCRIPTION:  Remove sequential duplicate characters through ":"
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call remdup1 (cline)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline           char*80        in/out   line of warning message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cl         char*1     last character loaded
!         cx         char*1     working character
!         kk         integer    working index for modified line data
!         ks         integer    working index for initial line data
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameter
      character*80 cline
!
!         local variables
      integer k, ks, kk
      character*1 cl, cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cl = cline(1:1)
      kk = 1
      do k=2, 80
        cx = cline(k:k)
        if (cx .ne. ':') then
!
!                   check for sequential duplicate character
!
          if (cx .ne. cl) then
            cl = cx
            kk = kk +1
            if (kk .ne. k) cline(kk:kk) = cx
          endif
        else
!
!                   load ":" and stop processing
!
          kk = kk +1
          if (kk .ne. k) cline(kk:kk) = cx
          ks = k +1
          goto 200
!
        endif
      enddo
      ks = 81
  200 continue
      if (ks .le. 80) then
!
!                   ensure only one ":" is loaded
!
        cx = cline(ks:ks)
        if (cx .eq. ':') then
          ks = ks +1
          goto 200
!
        elseif (kk .ne. ks) then
!
!                   one or more duplicates have been found,
!                   left-shift the remaining data
!
          do k=ks, 80
            kk = kk +1
            cline(kk:kk) = cline(k:k)
          enddo
!
!                   blank fill to end of line
!
          do k=kk+1, 80
            cline(k:k) = ' '
          enddo
        endif
      endif
      return
!
      end
      subroutine remdup2 (cline)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  remdup2
!
!  DESCRIPTION:  Remove sequential duplicate characters through col 32
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call remdup2 (cline)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline           char*80        in/out   line of warning message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cl         char*1     last character loaded
!         cx         char*1     working character
!         kk         integer    character index to modified line
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameter
      character*80 cline
!
!         local variables
      integer k, kk
      character*1 cl, cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cl = cline(1:1)
      kk = 1
      do k=2, 32
        cx = cline(k:k)
!
!                   remove sequential duplicates
!
        if (cx .ne. cl) then
          cl = cx
          kk = kk +1
          if (kk .ne. k) cline(kk:kk) = cx
        endif
      enddo
      if (kk .ne. 32) then
!
!                   one or more duplicates were found,
!                   left-shift remaining data
!
        do k=33, 80
          kk = kk +1
          cline(kk:kk) = cline(k:k)
        enddo
!
!                   blank fill till end of line
!
        do k=kk+1, 80
          cline(k:k) = ' '
        enddo
      endif
      return
!
      end
      subroutine remdupb (cline)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  remdupb
!
!  DESCRIPTION:  Left justify and remove sequencial blanks
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call remdupb (cline)
!
!  PARAMETERS:
!       Name            Type        Usage            Description
!    ----------      ----------     ------   ----------------------------
!    cline           char*80        in/out   line of warning message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cl         char*1     last processed character
!         cx         char*1     working character
!         kk         integer    index to modified line
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameter
      character cline*80
!
!         local variables
      integer k, j, kk
      character*1 cl, cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do j=1, 80
        cl = cline(j:j)
        if (cl .ne. ' ') then
!
!                   load first non-blank character
!
          kk = 1
          if (j .ne. 1) cline(1:1) = cl
          do k=j+1, 80
            cx = cline(k:k)
!
!                     load remainder, omit duplicate blanks
!
            if (cx .ne. ' ') then
              kk = kk +1
              cline(kk:kk) = cx
            else
              if (cl .ne. ' ') then
                kk = kk +1
                cline(kk:kk) = cx
              endif
            endif
            cl = cx
          enddo
          do k=kk+1, 80
            cline(k:k) = ' '
          enddo
          goto 100
!
        endif
      enddo
  100 continue
!
      end
      subroutine scanem (card,keep,key)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  scanem
!
!  DESCRIPTION:  Left justify values, scan card for valid data:
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call scanem (card,keep,key)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*80        in/out   line of message
!    keep            integer        output   valid flag, -1 - valid data
!    key             integer        output   key flag,   -1 - valid key word
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         remdup1     remove sequential duplicates through ":"
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cl         char*1     last character processed
!         cline      char*80    working line of modified data
!         cx         char*1     working character
!         na         integer    sum of alpha characters
!         nk         integer    index for cline, sum of good characters
!         nn         integer    sum of digit characters
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer keep, key
      character*80 card
!
!         local variables
      integer n, na, nk, nn, k, kk
      character cx*1, cl*1, cline*80
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cline = ' '
      keep  = 0
      key   = 0
      do k=1, 80
        cl = card(k:k)
        if (cl.ne.' ' .and. cl.ne.'-') then
!
!                   left justify values and remove consecutive blanks
!
          cline(1:1) = cl
          nk = 1
          do kk=k+1, 80
            cx = card(kk:kk)
            if (cx.ne.' ' .or. (cl.eq.' ' .and. cx.ne.' ') .or.
     &         (cl.ne.' ' .and. cx.eq.' ')) then
              nk = nk +1
              cline(nk:nk) = card(kk:kk)
            endif
            cl = cx
          enddo
!
!                   check for PAGE, do not keep if so
!
          if (cline(1:4) .ne. 'PAGE') then
!
!                     check that valid data is available
!
            na = 0
            nn = 0
            do n=1, nk
              cx = cline(n:n)
              if (cx.ge.'A' .and. cx.le.'Z') then
                na = na +1
              elseif (cx.ge.'0' .and. cx.le.'9') then
                nn = nn +1
              elseif (cx .eq. ':') then
!                   should be a key word, so check
                if (na .gt. 0) then
                  key  = -1
                  keep = -1
!
!                   remove adjacent duplicate letters from key word(s)
!
                  call remdup1 (cline)
!
!                   correct the one key word that has duplicate letter
!
                  if (cline(1:16) .eq. 'EXTENDED OUTLOK:')
     &                cline = 'EXTENDED OUTLOOK:'
                  goto 100
!
                else
!                   only words should be followed by a :, so remove :
                  cline(n:n) = ' '
                endif
              endif
            enddo
            if (na.gt.0 .or. nn.gt.0) keep = -1
          endif
          goto 100
!
        endif
      enddo
  100 continue
      card = cline
      return
!
      end
      subroutine scrnxy (string,nk,ifxy)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  scrnxy
!
!  DESCRIPTION:  Search for "X" or "Y" in character string
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call scrnxy (string,nk,ifxy)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    ifxy            integer        output   "X_Y" flag, 0 - no find
!    nk              integer        input    number of characters in string
!    string          char(*)        input    string of characters to check
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:  none
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nk, ifxy
      character string(*)
!
!         local variable
      integer k
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ifxy = 0
      do k=1, nk
        if (string(k).eq.'X' .or. string(k).eq.'Y') ifxy = -1
      enddo
      return
!
      end
      subroutine strngf (card,strg,nc,kc)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  strngf
!
!  DESCRIPTION:  Determine if there is a string of characters in card that
!                matches the string of characters in strg
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call strngf (card,strg,nc,kc)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*80        input    long character string
!    kc              integer        output   success flag, -1 found match
!    nc              integer        input    number of characters in strg
!    strg            char*80        input    key word to be found in card
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         lc         integer    last character position for match
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer  nc, kc
      character*80 card, strg
!
!         local variables
      integer n, lc
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      kc = 0
      do n=1, 80 -nc
        lc = n +nc -1
        if (card(n:lc) .eq. strg(1:nc)) then
          kc = -1
          goto 110
!
        endif
      enddo
  110 continue
      return
!
      end
      subroutine uponly (card)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  uponly
!
!  DESCRIPTION:  Convert string of characters to upper case
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call uponly (card)
!
!  PARAMETERS:
!    Name        Type        Usage            Description
!    -----      -------     -------  ----------------------------
!    card       char*80     in/out   string of characters for conversion
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         iaoff      integer    off-set from "a" to "A"
!         inil       integer    flag for one-time initialization
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      character card*80
!
!         local variables
      integer inil, iaoff, k
!
      save inil, iaoff
!
      data inil/0/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      if (inil .eq. 0) then
        inil  = -1
        iaoff = ichar('a') -ichar('A')
      endif
      do k=1, 80
        if (card(k:k).ge.'a' .and. card(k:k).le.'z')                     &
     &      card(k:k) = char (ichar (card(k:k)) -iaoff)
      enddo
      return
!
      end
      subroutine wrdfnd (line,ks,wrds,nk,nw,kf,kl)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  wrdfnd
!
!  DESCRIPTION:  Search string line for a match from set of words in wrds
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call wrdfnd (line,ks,wrds,nk,nw,kf,kl)
!
!  PARAMETERS:
!    Name       Type         Usage            Description
!    -----     --------     -------  ----------------------------
!    kf        integer      output   starting character in line of match,
!                                    when kl > 0
!    kl        integer      output   index to word matched, 0 - no match
!    ks        integer      input    starting character index of line
!    line      char*80      input    character string to be searched
!    nk        integer      input    number of characters in each word
!    nw        integer      input    number of words in arrays wrds
!    wrds      char*10      input    array of words for a one time match
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         j          integer    working character index for wrds
!         kss        integer    working starting character index of line
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer ks, nw, kf, kl
      integer nk(nw)
      character line*80, wrds(nw)*10
!
!         local variables
      integer j, k, kk, kss, n
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do n=1, nw
        kss = ks
  100   continue
        do k=kss, 80
          if (line(k:k) .eq. wrds(n)(1:1)) then
            kf = k
            j  = 1
            do kk=k+1, 80
              j = j +1
              if (line(kk:kk) .ne. wrds(n)(j:j)) then
                kss = kk +1
                goto 100
!
              elseif (j .eq. nk(n)) then
                kl = n
                goto 200
!
              endif
            enddo
          endif
        enddo
      enddo
      kl = 0
  200 continue
      return
!
      end
      subroutine wrdsfd (line,ks,wrds,nk,nw,kl)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  wrdsfd
!
!  DESCRIPTION:  Search string line for one or more matches with words in wrds
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call wrdsfd (line,ks,wrds,nk,nw,kl)
!
!  PARAMETERS:
!    Name       Type        Usage            Description
!    -----     -------     -------   ----------------------------
!    kl        integer     output    array of flags for match, 0 - no match
!    ks        integer     input     starting character position for search
!    line      char*80     input     character string to be searched
!    nk        integer     input     number of characters in each word
!    nw        integer     input     number of words in wrds
!    wrds      char*10     input     array of wrds to be matched
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:  none
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         j          integer    working character index to words in wrds
!         kss        integer    working starting character for search
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer ks, nw, kl(nw), nk(nw)
      character line*80, wrds(nw)*10
!
!         local variables
      integer n, kss, j, k, kk
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do n=1, nw
!
!                   mark no match for this word
!
        kl(n) = 0
        kss   = ks
  100   continue
        do k=kss, 80
          if (line(k:k) .eq. wrds(n)(1:1)) then
            j = 1
            do kk=k+1, 80
              j = j +1
              if (line(kk:kk) .ne. wrds(n)(j:j)) then
                kss = kk +1
                goto 100
!
              elseif (j .eq. nk(n)) then
!
!                   found a match, mark it and continue search
!
                kl(n) = n
                goto 110
!
              endif
            enddo
          endif
        enddo
  110   continue
      enddo
      return
!
      end
      subroutine wrtmsg (cwmsg,nmsgl,cwsum,cnnn,w_dtg,wrnyr,keys,       &
     &                   nk,ierwr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  wrtmsg
!
!  DESCRIPTION:  Write tropical cyclone warning message into ISIS
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call wrtmsg (cwmsg,nmsgl,cwsum,cnnn,w_dtg,wrnyr,keys,nk,ierwr)
!
!  PARAMETERS:
!     Name       Type      Usage          Description
!    ------    --------   -------  ----------------------------
!    cnnn      char*240   input    NNNN line of summary
!    cwmsg     char*80    input    tropical cyclone warning message
!    cwsum     char*240   input    tropical cyclone warning summary
!    ierwr     integer    output   write error flag, 0 - no error
!    keys      integer    input    array of message lines containing key words
!    nk        integer    input    number of key lines found in message
!    nmsgl     integer    input    message length in lines
!    wrnyr     char*4     input    year of warning
!    w_dtg     char*10    input    watch dtg  (00 or 12 for hr)
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     ISIS write error         print ISIS call parameters, and return
!     array too small          signal error and return
!
!  ADDITIONAL COMMENTS:
!
!     cwmsg(1) is RX+ OR AWN receipt line
!     cwmsg(2) is presidence and msg dtg line of message
!     cwmsg(3) is FM line of message
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         msg_wr      ISIS driver for writing message
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----      -----------------------------------------
!         arvl_dtg   char*14   arrival dtg of message
!         clasif     char*8    classification of message
!         com_cir    char*24   message communications circuit
!         enc_typ    char*24   encoding type
!         ll         integer   working line number of message
!         ls         integer   starting working line number of message
!         msg_dtg    char*12   message dtg
!         msg_id1    char*32   tropical cyclone identification
!         msg_id2    char*32   dtg of initial position in warning
!         msg_id3    char*32   number of tropical cyclone warning
!         msg_id4    char*32   year of warning:
!                                N.H. - 1 Jan through 31 Dec
!                                S.H. - 1 July through 30 June, Jan's year
!         msg_id5    char*32   not used, fill with "blank"
!         msg_subtyp char*24   ISIS sub-type of message
!         msg_typ    char*24   ISIS type of message
!         mxlines    integer   maximum number of lines in message for ISIS
!         num_byte   integer   number of bytes in message
!         org_tx     char*32   originator of message text
!         status     char*8    status of message when placed into ISIS
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer mxlines
      parameter (mxlines = 200)
!
!         formal parameters
      integer nmsgl, nk, ierwr
      integer keys(nk)
      character w_dtg*10, wrnyr*4
      character*80 cwmsg(mxlines)
      character*240 cwsum, cnnn
!
!         local variables
      integer k, l, ll, ls, n
!
!                   ISIS MSG_WR parameters
!         INPUT:
      integer num_byte
      character*8  clasif, status
!     character*10 w_dtg
      character*14 arvl_dtg
      character*12 msg_dtg
      character*24 msg_typ, msg_subtyp
      character*24 com_cir, enc_typ
      character*32 msg_id1, msg_id2, msg_id3, msg_id4, msg_id5
      character*32 org_tx
!
      data msg_typ/'TC'/
      data msg_subtyp/'WRNG_MSG'/
      data clasif/'UNCLASS'/
!                not used, so set to "blank"
      data msg_id5/'_'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      if (nmsgl .le. mxlines) then
!
!                   set input parameters for WRNG_MSG
!
!                   tropical cyclone ID - number and original basin
        msg_id1 = cwsum(12:14)
!                   dtg of initial position in warning - YYYYMMDDHH
        msg_id2 = cwsum(1:10)
!                   tropical warning number, include amendment
!                   modification letter (21 , 21A, 21B, etc)
        msg_id3 = cwsum(27:29)
!                   set trailing blank to underbar
        if (msg_id3(3:3) .eq. ' ') msg_id3(3:3) = '_'
!                   set NH/SH seasonal warning year YYYY
        msg_id4 = wrnyr
!
        ll = keys(6)
        do n=7, nk
          if (keys(n).ne.0 .and. keys(n).le.mxlines) then
            ls = ll +2
            ll = keys(n)
            do l=ls, ll
              if (cwmsg(l)(79:79).eq.' ' .and.                          &
     &            cwmsg(l)(80:80).eq.' ') then
                do k=78, 1, -1
                  cwmsg(l)(k+2:k+2) = cwmsg(l)(k:k)
                enddo
                cwmsg(l)(1:1) = ' '
                cwmsg(l)(2:2) = ' '
              endif
            enddo
          endif
        enddo
        write(33,*) 'FINAL version of message'
        do l=1, nmsgl
          write (33,'(a80)') cwmsg(l)
        enddo
!
!                   blank fill empty lines
!
        if (nmsgl .lt. mxlines) then
          do n=nmsgl+1, mxlines
            cwmsg(n) = ' '
          enddo
        endif
!
        num_byte = mxlines*80
        msg_dtg  = cnnn(11:22)
        arvl_dtg = cwmsg(1)(18:31)
        org_tx   = cwmsg(3)(4:35)
        if (cwmsg(1)(1:3) .eq. 'RX+') then
          com_cir  = 'AUTODIN'
        else
          com_cir  = 'AWN'
        endif
        status   = 'processed'
        enc_typ  = 'none'
        ierwr = 0
!
!        call msg_wr (msg_typ,msg_subtyp,msg_id1,msg_id2,msg_id3,msg_id4, &
!     &             msg_id5,clasif,num_byte,cwmsg,w_dtg,msg_dtg,arvl_dtg, &
!     &             org_tx,com_cir,status,enc_typ,ierwr)
!
        if (ierwr .ne. 0) then
          write(*,*) 'msg_typ = ',msg_typ
          write(*,*) 'msg_subtyp = ',msg_subtyp
          write(*,*) 'msg_id1 = ',msg_id1
          write(*,*) 'msg)id2 = ',msg_id2
          write(*,*) 'msg_id3 = ',msg_id3
          write(*,*) 'msg_id4 = ',msg_id4
          write(*,*) 'msg_id5 = ',msg_id5
          write(*,*) 'clasif  = ',clasif
          write(*,*) 'num_byte= ',num_byte
          write(*,*) 'cwmsg   = ',cwmsg(6)(1:40)
          write(*,*) 'w_dtg   = ',w_dtg
          write(*,*) 'msg_dtg = ',msg_dtg
          write(*,*) 'arvl_dtg= ',arvl_dtg
          write(*,*) 'org_tx  = ',org_tx
          write(*,*) 'com_cir = ',com_cir
          write(*,*) 'status  = ',status
          write(*,*) 'enc_typ = ',enc_typ
        else
          write(*,*) 'prcwarn, AUTO/AWN MESSAGE written to ISIS '
!          do n=1, nmsgl
!            write(*,*) n,' ',cwmsg(n)(1:60)
!          enddo
        endif                                                                   
      else                                                                      
        write (*,*) 'ERROR, message too long'                                   
        ierwr = 900
      endif
      return
!
      end
      subroutine xychk (cwsum,nl,casum,na,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  xychk
!
!  DESCRIPTION:  perform final quality check of summary
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call xychk (cwsum,nl,casum,na,ierr)
!
!  PARAMETERS:
!     Name      Type        Usage            Description
!    ------    --------    -------   ----------------------------
!    casum     char*240     input    amplification section of summary
!    cwsum     char*240     in/out   first part of warning summary
!    ierr      integer      output   error flag, 0 - no error
!    na        integer      input    number of lines in amplification
!    nl        integer      input    number of lines in first part
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!         ************** TEMPLATE OF WSUM HEADER **********************
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         YYYYMMDDHH IDB NAME       NRWA NC DEG KT METH ---- ACC
!                        1234567890
!
!         ************** TEMPLATE OF WSUM FORCAST **********************
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         tau  latn longt mxw Rspd nmi dd ---
!
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         ctau       char*3     forecast hour (tau)
!         cx         char*1     working character
!         iamp       integer    amplification found flag, 0 - no find
!         irwnd      integer    wind speed for given radius
!         mxwnd      integer    maximum wind speed of cyclone for tau
!         nr         integer    sum of radii for given tau
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer nl, na, ierr
      character*240 cwsum(nl), casum(na)
!
!         local variables
      integer n, k, mxwnd, nr, iamp, irwnd, nn
      character cx*1, ctau*3
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   scan for "X" or "Y", which signals an error
!
      ierr = 0
      do n=1, nl
        do k=1, 240
          if (cwsum(n)(k:k).eq.'X' .or. cwsum(n)(k:k).eq.'Y') then
            if (n .ne. 1) then                                                  
              ierr = -1                                                         
            elseif (k.lt.16 .or. (k.gt.25 .and. k.lt.41)) then
!                   omit columns with cyclone name
              ierr = -1
            elseif (cwsum(n)(k:k) .eq. 'Y') then
!                   double 'Y' is always an error
              if (cwsum(n)(k-1:k-1).eq.'Y' .or. cwsum(n)(k+1:k+1).eq.
     &            'Y') ierr = -1
            elseif (k.gt.46 .and. cwsum(n)(k:k).eq.'X') then
              ierr = -1
            endif
            if (ierr .ne. 0) goto 100
!
          endif                                                                 
        enddo                                                                   
      enddo                                                                     
  100 continue                                                                  
!
!                   check initial and forecast data for:                        
!                         name of cyclone error                                 
!                         wind speed errors
!                         wind radius errors
!                                                                               
      do n=2, nl                                                                
        ctau = cwsum(n)(2:4)                                                    
!                     set max wind value to missing
        mxwnd = -99                                                             
        nr    = 0                                                               
        do k=5, 240
          if (cwsum(n)(k:k) .eq. 'R') then                                      
            nr = nr +1                                                          
            if (k .eq. 21) then
!                                                                               
!                   found first radius indicator
!                                                                               
              if (cwsum(n)(17:19) .ne. 'XXX') then                              
!
!                       obtain max wind speed for this position                 
!                                                                               
                read (cwsum(n)(17:19),'(i3.3)') mxwnd                           
                if (n.eq.2 .and. mxwnd.ge.35) then                              
!
!                         perform name check                                    
!                                                                               
                  if (cwsum(1)(16:16) .ne. 'X') then
                    if (cwsum(1)(16:21) .eq. 'NONAME') then                     
!                                                                               
!                             see if NONAME is appropriate                      
!                                                                               
                      if (cwsum(2)(9:9) .eq. 'N') then
!                                                                               
!                             see if cyclone has a name
!
                        if (cwsum(2)(15:15) .eq. 'W') then                      
!                               this is an error, x-out NONAME                  
                          cwsum(1)(16:21) = 'XXXXXX'                            
                        elseif (cwsum(2)(11:11) .ne. '0') then                  
!                                 this is an error, x-out NONAME
                          cwsum(1)(16:21) = 'XXXXXX'
                        endif
                        if (cwsum(1)(16:16) .eq. 'X') ierr = -1
                      endif
                    endif
                  endif
                endif
              endif
            else
              if (cwsum(n)(k+1:k+3) .ne. 'XXX') then
                read (cwsum(n)(k+1:k+3),'(i3.3)') irwnd
                if (mxwnd.gt.0 .and. irwnd.gt.mxwnd) then
!
!                         radius wind greater than max wind
!
                  cwsum(n)(k+1:k+3) = 'XXX'
                  ierr = -1
                endif
              endif
            endif
          endif
        enddo
        if (nr .eq. 0) then
!
!                   no radius of winds information for this tau
!
          if (mxwnd .gt. 35) then
!
!                     see if radius is required
!
            iamp = 0
            do nn=1, na
              if (casum(nn)(5:7) .eq. ctau) iamp = -1
            enddo
            if (iamp .eq. 0) then                                               
!                       no amplifying remarks is an error                       
              ierr = -1
              cwsum(n)(21:24) = 'RXXX'                                          
            endif                                                               
          endif                                                                 
        endif                                                                   
      enddo                                                                     
!                                                                               
      return
!                                                                               
      end
      subroutine prepmsg (cmsg,nlmax,nl,keys,nkmax,nk,rtxrx,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  prepmsg
!
!  DESCRIPTION:  Read one message, AUTODIN or AWN, and prepare for decoding
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call prepmsg (cmsg,nlmax,nl,keys,nkmax,nk,rtxrx,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        output   body of warning message
!    ierr            integer        output   eror flag:
!                                             0 - no error
!                                            >0 - fatal error, software
!                                                 restriction
!                                            <0 - fatal error, I/O error
!    keys            integer        output   keys found in message
!    nk              integer        output   number of keys found
!    nkmax           integer        input    dimension of keys
!    nl              integer        output   number lines retained in message
!    nlmax           integer        input    dimension of cmsg
!    rtxrx           char*240       output   RX+ line for AUTODIN
!                                            Rx times for AWN
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     I/O error                set error flag to negative value & return
!     Software limitation      set error flag to positive value & return
!
!  ADDITIONAL COMMENTS:
!
!         format of rtxrx on output:
!
!           for AUTODIN message:
!              1         2         3
!     12345678901234567890123456789012
!     RX+XXXX+JJJ+HHmm+YYYYMMDDHHmmss+
!
!           for AWN message:
!              1         2         3
!     12345678901234567890123456789012
!     AWN YYYYMMDDHHmm YYYYMMDDHHmmss
!
!     where:
!          + - separator
!       XXXX - 4-digit sequence number
!        JJJ - Julian day
!       YYYY - year
!         MM - month
!         DD - day          these time values are for receipt
!         HH - hour
!         mm - minute
!         ss - second
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         awnchk      see if message came via AWN
!         dumyauto    make top of AWN message look like AUTODIN
!         fndkey      check message line for valid key
!         lftjust     left justify line and check for valid data on line
!         scanem      scan message for valid data then for key word(s)
!         uponly      put characters in upper case
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         awn_sav    char*80    temporary storage for next AWN MANOP
!         card       char*80    working string for line of message
!         cardm0     char*80    present valid line of message
!         cardm1     char*80    minus 1 line of message
!         cardm2     char*80    minus 2 line of message
!         ioe        integer    I/O error flag, 0 no error
!         keep       integer    valid data indicator, -1 valid
!         key        integer    key word indicator, -1 found key word(s)
!         kk         integer    key word indicator, -1 found key
!         ks         integer    index to keys for found key word(s)
!         msg_typ    char*8     type, AUTODIN or AWN, message being processed
!         npass      integer    count of passes in top of program, another
!                               indicator for AUTODIN or AWN
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extensions or f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal arguments:
      integer nlmax, nl, nkmax, nk, ierr
      integer keys(nkmax)
      character cmsg(nlmax)*80, rtxrx*240
!
!         local variables:
      integer npass, keep, ks, kk, key, ioe
      character*80 card, cardm0, cardm1, cardm2, awn_sav
      character*8 msg_typ
!
      save msg_typ, awn_sav
!
      data msg_typ /' '/
      data awn_sav /' '/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ks     = 0
      nk     = 0
      nl     = 0
      ierr   = 0
      cardm2 = ' '
      cardm1 = ' '
      cardm0 = ' '
!
!                   (following section of code is for ATCF only)
!
      if (rtxrx(1:4) .eq. 'ATCF') then
!
!                   put in dummy AUTODIN type lines, for ATCF
!
        call atcf2auto (cmsg,nlmax,nl,keys,nkmax,nk,rtxrx,ierr)
        msg_typ = 'ATCF'
        if (ierr .eq. 0) goto 200
!
        write (*,*) 'ATCF - BAD rtxrx line follows: '
        write (*,*) ' ',rtxrx(1:40)
        ierr = -99
        goto 300
!
      endif
!
!                   (following sections of code are for FNMOC only)
!
      rtxrx  = ' '
      if (msg_typ .ne. 'AWN') then
!                   plan to process AUTODIN message
        npass = 0
      else
!                   process AWN message
        npass = 1
        if (awn_sav .ne. ' ') then
!
!                   first line of next AWN message is in awn_sav, so
!                   load card and skip next read of card
!
          card    = awn_sav
          awn_sav = ' '
          goto 101
!
        endif
      endif
!
!                   look for first valid line of message
!
  100 continue
      read (10,'(a80)',iostat=ioe,end=150) card
      if (ioe .eq. 0) then
        call uponly (card)
        call lftjust (card,keep)
        write(*,*) ' ',keep,' ', card(1:40)
        if (keep .eq. 0) goto 100
!
      else
        write (*,*) 'Initial section read error is ',ioe
        write (33,*) 'PRCWARN, initial section READ error= ',ioe
        ierr = -2
        goto 300

      endif
!
!                   continuation point for AWN messages
!
  101 continue
      if (npass .eq. 0) then
!
!                   look for AUTODIN messages
!
        if (card(1:3) .eq. 'RX+') then
!                     found RX+ line, from ODR for AUTODIN message
!                     in real-time or from ISIS
          msg_typ = 'AUTODIN'
          rtxrx   = card
          goto 200

        elseif (card(1:3) .eq. 'AWN') then
!                     found AWN line, processing message from ISIS
!                     rather than in real-time from AWN
          rtxrx = card
          goto 200
!
        elseif (card(1:2) .eq. 'WT') then
!
!                   see if message is AWN
!
          write(*,*) 'FOUND WT'
          write(*,*) card
          call awnchk (card,keep)
          if (keep .ne. 0) then
!                   found AWN MANOP line
            rtxrx   = 'AWN ' // card
            write(*,*) rtxrx
            npass   = 1
            msg_typ = 'AWN'
!
!                   put in dummy AUTODIN type lines, if valid AWN
!
            call dumyauto (cmsg,nlmax,nl,keys,nkmax,nk,rtxrx,ierr)
            if (ierr .eq. 0) then
!                   good AWN message, keep processing
              write(*,*) 'PROCESSING AWN message...'
              ks      = 6
              goto 200
!
            else
!                   wrong/old AWN message, look for next AWN message
              write (*,*) 'WRONG AWN message found'
              write (33,*) 'WRONG AWN message found'
              ierr = 0
            endif
          else
            write(*,*) 'awnchk, keep= ',keep
          endif
        endif
      elseif (card(1:2) .eq. 'WT') then
!
!                   see if message is AWN
!
        write (*,*) 'CHECKING for AWN message ...'
        call awnchk (card,keep)
        if (keep .ne. 0) then
!                   found AWN MANOP line
          rtxrx = 'AWN ' // card
!
!                   put in dummy AUTODIN type lines, if valid AWN
!
          call dumyauto (cmsg,nlmax,nl,keys,nkmax,nk,rtxrx,ierr)
          if (ierr .eq. 0) then
!                   good AWN message, keep processing
            write(*,*) 'PROCESSING AWN message...'
            msg_typ = 'AWN'
            ks      = 6
            goto 200
!
          else
!                   wrong/old AWN message, look for next AWN message
            write (*,*) 'WRONG AWN message found'
            write (33,*) 'WRONG AWN message found'
            ierr = 0
          endif
        endif
      endif
      goto 100
!
!                   EOF section processing
!
  150 continue
      if ((msg_typ.eq.'AWN' .or. msg_typ.eq.'ATCF') .and. nk.gt.6) then
        nl = nl +1
!                   indicate end of message
        cmsg(nl) = 'NNNN'
      endif
      write (*,*) 'PRCWARN, EOF reached on message file'
      write (33,*) 'PRCWARN, EOF reached on message file'
!                   signal EOF to driver program
      ierr = -99
      goto 300
!
!                   top of line-by-line input of message
!                          (FNMOC and TESS)
!
  200 continue
      read (10,'(a80)',iostat=ioe,end=150) card
      if (ioe .eq. 0) then
!                   ensure all text is upper case
        call uponly (card)
        if (ks .lt. 3) then
          call lftjust (card,keep)
          if (keep .ne. 0) then
!
!                   line of message has valid data for checking
!
            call fndkey (card,ks,kk)
            cardm2 = cardm1
            cardm1 = cardm0
            cardm0 = card
            if (kk .ne. 0) then
!
!                     key word ks was found
!
              nk = nk +1
              keys(ks) = ks
              nl = ks
              cmsg(nl) = cardm0
              if (nl .eq. 3) then
!                       check if earlier key words were missed
                if (keys(1) .eq. 0) then
                  keys(1) = 208
                  cmsg(1) = cardm2
                  nk = nk +1
                endif
                if (keys(2) .eq. 0) then
                  keys(2) = 208
                  cmsg(2) = cardm1
                  nk = nk +1
                endif
              endif
            elseif (nk .ne. 0) then
              if (ks .eq. 1) then
                ks = 2
              else
                ks = 3
              endif
              nk = nk +1
              keys(ks) = 209
              nl = ks
              cmsg(nl)  = cardm0
            endif
          endif
        elseif (ks .lt. 6) then
          call lftjust (card,keep)
          if (keep .ne. 0) then
!                     valid data line has been found in msg
            call fndkey (card,ks,kk)
            cardm2 = cardm1
            cardm1 = cardm0
            cardm0 = card
            if (kk .ne. 0) then
!
!                     key word ks was found
!
              nk = nk +1
              keys(ks) = ks
              nl = ks
              cmsg(nl) = cardm0
              if (nl .eq. 6) then
                write(*,*) 'cmsg(6)= ',cmsg(nl)
!                       check if earlier key words were missed
                if (keys(4) .eq. 0) then
                  keys(4) = 208
                  cmsg(4) = cardm2
                  nk = nk +1
                endif
                if (keys(5) .eq. 0) then
                  keys(5) = 208
                  cmsg(5) = cardm1
                  nk = nk +1
                endif
              endif
            elseif (nk .ge. 4) then
              if (ks .eq. 4) then
                ks = 5
                nk = nk +1
                keys(ks) = 209
                nl = ks
                cmsg(nl)  = cardm0
              endif
            endif
          endif
        else
!
!                   process body of message, after SUBJ:
!
          call scanem (card,keep,key)
          if (keep .ne. 0) then
            nl =  nl +1
            if (nl .le. nlmax) then
              if (key .ne. 0) then
                nk = nk +1
                if (nk .le. nkmax) then
                  keys(nk) = nl
                else
                  write (*,*)  'Too many keys in message'
                  write (33,*) ' Too many keys in message'
                  ierr = 500 +nk -nkmax
                endif
              endif
              cmsg(nl) = card
              if (card(1:4) .eq. 'NNNN') then
                goto 300
!
              elseif (nk.gt.10 .and. card(1:2).eq.'WT') then
!
!                   see if found first line of next AWN message
!                   AWN messages will NOT have NNNN between messages
!
                call awnchk (card,keep)
                if (keep .ne. 0) then
!
!                   found AWN MANOP line of next AWN message, save same
!
                  awn_sav  = card
!                     signal end of AWN message to processing software
                  cmsg(nl) = 'NNNN'
                  goto 300
!
                endif
              endif
            else
              write (*,*) 'Message array too small'
              write (33,*) ' prcwarn, Message array too small'
              ierr = nlmax -nl
            endif
          endif
        endif
        goto 200
!
      else
        write (*,*) 'I/O error = ',ioe
        write (33,*) ' I/O error = ',ioe
        ierr = -2
      endif
  300 continue
      if (msg_typ .eq. 'AWN' .and. nl.gt.6) ierr = 0
      return
!
      end
      subroutine atcf2auto (cmsg,nlmax,nl,keys,nkmax,nk,rxpl,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  atcf2auto
!
!  DESCRIPTION:  place dummy AUTODIN heading on ATCF pre-message
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  none
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call dumyauto (cmsg,nlmax,nl,keys,nkmax,nk,rxpl,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cmsg            char*80        in/out   ATCF tropical cyclone warning
!                                            pre-message
!    rxpl            char*240       input    RX+ line
!    ierr            integer        output   error flag, 0 - no error
!    keys            integer        output   index to key words
!    nk              integer        output   number of key words
!    nkmax           integer        input    dimension of keys
!    nl              integer        output   line index of message
!    nlmax           integer        input    maximum line count of message
!
!  COMMON BLOCKS:  none
!
!  FILES:  none
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!                               examples:
!      of "saved" AUTODIN lines               of dummy ATCF
!
!  O 201351Z APR 95                       O 201500Z APR 95
!  FM NAVPACMETOCCEN WEST GU//JTWC//      FM JTWC
!  TO AIG NINE TWO TWO NINE               TO ATCF ATCF ATCF
!  BT                                     BT
!  UNCLAS //N03145//                      UNCLAS
!
!         example of rxpl on input
!           1         2
!  1234567890123456789012
!  ATCF YYYYMMDDHHmm PGTW  < indicates sending station
!
!         example of cmsg(1) on output
!           1         2
!  1234567890123456789012
!  O 201500Z APR 95
!
!         example of rxpl on output
!
!           1         2         3         4
!  1234567890123456789012345678901234567890
!  RX+ YYYYMMDDHHmm YYYYMMDDHHmmss
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name               Description
!         -------         ----------------------
!         date_and_time   obtain system date and time
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cmon       char*3     array of months
!         fmcod      char*4     array of station codes
!         fmsta      char*7     array of station names
!         from       char*7     name of sending station
!         imon       integer    index for month
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f90
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal arguments
      integer nlmax, nl, nkmax, nk, ierr
      integer keys(nkmax)
      character cmsg(nlmax)*80, rxpl*240
!
!         local variables
      integer nd, kf, imon, n
!
      character cdtg*16
      character fmsta(3)*7, fmcod(3)*4, from*7, cmon(12)*3
!
      data fmcod /'PGTW', 'PHNC', 'KNGU'/
      data fmsta /'JTWC', 'PEARL', 'NORFOLK'/
      data cmon /'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
     &           'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      call fnumfd (rxpl,5,cdtg,nd,kf)
      if (nd .eq. 12) then
        read (cdtg,'(4x,i2)') imon
        if (imon.ge.1 .and. imon.le.12) then
          cmsg(1) = 'O '//cdtg(7:12)//' '//cmon(imon)//' '//cdtg(3:4)
          from = 'UNKN'
          do n=1, 3
            if (rxpl(19:22) .eq. fmcod(n)) from = fmsta(n)
          enddo
          cmsg(2) = 'FM ' // from
          cmsg(3) = 'TO ATCF ATCF ATCF'
          cmsg(4) = 'BT'
          cmsg(5) = 'UNCLAS'
          do n=1, 5
            keys(n) = n
          enddo
          nl = 5
          nk = 5
!                 load rxpl so lftjust will hold receipt
!                 time in same place as RX+ AUTODIN line
          rxpl = 'RX+ ' // cdtg(1:12) // ' ' // cdtg(1:12) // '59'
          ierr = 0
        else
          ierr = -1
        endif
      else
        ierr = -1
      endif
      return
!
      end
