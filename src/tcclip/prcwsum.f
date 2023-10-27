      program prcwsum
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  prcwsum
!
!  DESCRIPTION:  driver program for checking tropical cyclone warning
!                summaries
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
!  FILES:
!       Name        Unit    Type    Attribute  Usage       Description
!    ----------     ----  --------  --------- -------  ------------------
!    warnsum         10                       input    initial summary
!    sum.isis        20                       output   diagnstics/new summary
!  cyclone_id.allow  30                       input    file of allowed
!                                                      cyclones to process
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:
!     Name       Type        Usage             Description
!   -------     -------      ------   ---------------------------------
!    csdtg      character    input    computer system dtg (00Z or 12Z) hour
!                                     from command line
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!
!  ADDITIONAL COMMENTS:
!
!         process warning summaries from:
!           (1) flat file - prcddn (DDN - ATCF) & prcwarn (AWN/AUTODIN)
!           (2) ISIS      - error summaries (from QC)
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         chkwsum     check tropical cyclone summary
!         dbread      read ISIS data base for messages
!         dbstop      terminate ISIS usage
!         dbwrit      write message to ISIS data base
!         filerd      read summary from flat file
!         pxfgetarg   obtain command line argument (CraySoft)
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cwsum      char*240   tropical cyclone warning summary array
!         cx         char*1     working single charater from string
!         fname      char*20    file name
!         iclen      integer    length of command line character string
!         ierc       integer    error flag from pxfgetarg
!         ierwt      integer    ISIS write error flag
!         ioe        integer    I/O error flag
!         istatus    integer    ISIS read error flag
!         keep       integer    flag for keeping summary data
!         lkont      integer    line count of summary
!         maxt       integer    maximum number of forecast (TAU) lines in a
!                               summary - must be changed if warning positions
!                               are changed.
!         ner1       integer    number of initial summaries with error(s)
!         ner2       integer    number of ISIS summaries with error(s)
!         nfltf      integer    number of summary from flat file
!         ngd1       integer    number of good initial summaries
!         ngd2       integer    number of good ISIS summaries
!         nisis      integer    number of summary from ISIS database
!         nlmax      integer    maximum allowed lines in summary - must be
!                               changed if warning message changes
!         nqcd       integer    source of summary 0 - AWN/DDN/AUTODIN
!                                                -1 - ISIS
!                               (all from ISIS have been reviewed by QC)
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  except for CraySoft pxfgetarg, none
!
!  COMPILE OPTIONS:  standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!                 sampson, NRL   Nov 95   - Converted to run in ATCF 3.0
!
!             A. Schrader, SAIC  6/98     -  Modified to use new data format
!
!..............................END PROLOGUE.............................
!
      implicit none
!
      integer nslmax, maxtau
      parameter (nslmax = 20,  maxtau = 6)
!
      character*1 cx
      character*10 csdtg
      character*20 fname
      character*240 cwsum(nslmax)
!
      integer iclen, ierc, ierwt, ioe, istatus, keep, lkont, maxt, ner1
      integer n, ner2, nfltf, ngd1, ngd2, nisis, nlmax, nqcd
cx
      character*100 filename
      character*100 storms
      character*6   strmid
      character*2   century
      integer       ind
      integer       ioerror, iarg
cx

! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!

      nlmax = nslmax
      maxt  = maxtau
      nfltf = 0
      ngd1  = 0
      ner1  = 0
      nqcd  = 0
!                   obtain command line parameter, csdtg
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

cx    if (ierc.eq.0 .and. iclen.eq.10) then
      if (csdtg(1:1).ne.' ' .and. csdtg(10:10).ne.' ') then
        write (*,*) 'PROCESSING tropical warnings on watch : ',csdtg
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
!                   open diagnostic file (also serves as summary ..bs 11/95)
!
cx    open (20,file='sum.isis',form='formatted',action='write')
cx    open (20,file='sum.isis',form='formatted')
cajs  write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".sum1"
      write(filename,'(6a)') storms(1:ind), "/", 
     1     strmid(1:4), century, strmid(5:6), ".sum1"
cx    open (20,file=filename,form='formatted')
      call openfile (20,filename,'unknown',ioerror)
!
!                   open allowed cyclone_id file
!
cx    open (30,file='cyclone_id.allow',status='old',form='formatted',   &
cx   &      action='read',iostat=ioe)
cx    open (30,file='cyclone_id.allow',status='old',form='formatted',   &
cx   &      iostat=ioe)
cx    if (ioe .ne. 0) then
cx      write (*,*)  'WARNING: cyclone_id.allow is missing'
cx      write (20,*) 'WARNING: cyclone_id.allow file not opened, ',     &
cx   &               'error is ',ioe
cx    endif
!
!                   open input file
!
cx    open (10,file='warnsum',status='old',form='formatted',            &
cx   &      action='read',iostat=ioe)
cajs  write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".sum"
      write(filename,'(6a)') storms(1:ind), "/", 
     1     strmid(1:4), century, strmid(5:6), ".sum"
      open (10,file=filename,iostat=ioe,status='old',form='formatted')

      if (ioe .eq. 0) then
!
!                   read flatfile input from DDN (ATCF) or prcwarn
!                   (AUTODIN or AWN)
!
        do while (ioe .eq. 0)
          call filerd (cwsum,nlmax,lkont,ioe)
          if (lkont.gt.0 .and. ioe.ge.0) then
            write(*,*) 'Processing ',lkont,' lines of summary'
            write(*,*) '(1)',cwsum(1)(1:50)
            nfltf = nfltf +1
!
!                   process warning summary for errors
!
            call chkwsum (cwsum,nslmax,lkont,maxt,csdtg,ngd1,ner1,keep)
            if (keep .ne. 0) then
              do n=1, lkont
                write (20,'(a240)') cwsum(n)
              enddo
cx            call dbwrit (cwsum,nlmax,lkont,keep,nqcd,csdtg,ierwt)
              if (ierwt .eq. 0) then
                write (*,*) 'Wrote flatfile ',nfltf,' to ISIS'
              else
                write (*,*) 'ISIS write problem with flatfile ',nfltf
              endif
            else
              write (*,*) 'OMIT writing flatfile ',nfltf
            endif
          elseif (lkont .gt. 0) then
            write (*,*) 'BAD read of flatfile ',nfltf+1
cx          pause
!
          endif
        enddo
        close (10)
      endif
      if (nfltf .eq. 0) write (*,*) 'FOUND NO flatfile input'
!
      nisis   = 0
      ngd2    = 0
      ner2    = 0
      nqcd    = -1
cx    istatus = 0
      istatus = 1
      do while (istatus .eq. 0)
!
!                   read ISIS WRNG_SMRY_ERROR that has been QC'd
!
cx      call dbread (cwsum,nlmax,nisis,lkont,istatus)
        if (istatus .eq. 0) then
!
!                   process warning summary for errors
!
          call chkwsum (cwsum,nslmax,lkont,maxt,csdtg,ngd2,ner2,keep)
          if (keep .ne. 0) then
cx          call dbwrit (cwsum,nlmax,lkont,keep,nqcd,csdtg,ierwt)
            if (ierwt .eq. 0) then
              write (*,*) 'Wrote ISIS file ',nisis,' to ISIS'
            else
              write (*,*) 'ISIS write problem with ISIS file ',nisis
            endif
          else
            write (*,*) 'OMIT ISIS write of: ',nisis
          endif
        endif
      enddo
      if (nisis .eq. 0) write (*,*) 'FOUND NO ISIS input'
!
      write (*,*) 'PROCESSED ',nfltf,' flat, good= ',ngd1,' err= ',ner1
      write (*,*) 'PROCESSED ',nisis,' ISIS, good= ',ngd2,' err= ',ner2
      close  (10)
      rewind (20)
      close  (20)
      print *, cwsum
cx    call dbstop
      end
      subroutine alphadsc (cwsum,ks,kt,ntyp)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  alphadsc
!
!  DESCRIPTION:  Determine type of radius description
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
!  USAGE:  call alphadsc (cwsum,ks,kt,ntyp)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsum           character      input    line of message
!    ks              integer        input    starting character position
!    kt              integer        input    ending character position
!    ntyp            integer        output   type of description
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
!     wrong character spread   set ntyp to -1
!     unknown abreviation      set ntyp to  0
!
!  ADDITIONAL COMMENTS:
!
!         DD - DESCRIPTION of radius, two characters - OPTIONAL
!                DD allowed abreviations:
!         type
!          1        NN, NE, EE, SE, SS, SW, WW, NW - DIRECTION
!          2        QD - QUADRANT
!          2        SC - SEMICIRCLE
!          3        EW - ELSEWHERE
!          4        OW - OVER WATER
!          4        OL - OVER LAND
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         dsc        char*2     allowed two character abreviations
!
!  METHOD:
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 extesions or f90
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
      integer ks, kt, ntyp
      character cwsum*240
!
!         local variables
      integer n
      character*2 dsc(13)
!
      data dsc/'NN','NE','EE','SE','SS','SW','WW','NW',                 & type1
     &         'QD','SC',                                               & type2
     &         'EW',                                                    & type3
     &         'OW','OL'/                                               & type4
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      if (kt .eq. ks +1) then
!
!                   all descriptions are only two characters
!                   (there are 13 valid descriptions, check for match)
!
        do n=1, 13
          if (cwsum(ks:kt) .eq. dsc(n)) then
!
!                   found match, now type it
!
            if (n .lt. 9) then
              ntyp = 1
            elseif (n .lt. 11) then
              ntyp = 2
            elseif (n .lt. 12) then
              ntyp = 3
            else
              ntyp = 4
            endif
            goto 200
!
          endif
        enddo
!
!                   no match found, so set type to zero
!
        ntyp = 0
      else
!
!                   wrong character count, so set type to -1
!
        ntyp = -1
      endif
  200 continue
      end
      subroutine ampchk (cwsum,indx,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  ampchk
!
!  DESCRIPTION:  check AMP summary lines
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
!  USAGE:  call ampchk (cwsum,indx,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsum           char*240       in/out   line of summary
!    ierr            integer        output   error flag, 0 no error
!    indx            integer        input    index to AMP line(s)
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
!     bad values in hour       set error flag to -1
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         numchk      see if all characters are digits
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cline      char*240   initial line of summary
!         iern       integer    error flag for digits
!         num        integer    number value of digits
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
      integer indx, ierr
      character cwsum*240
!
!         local variables
      integer k, num, iern
      character cline*240
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      cline = cwsum
      cwsum = ' '
      if (indx .eq. 0) then
!
!                   have not processed an AMP line before
!
        cwsum(1:3) = 'AMP'
        do k=1, 240
          if (cline(k:k) .eq. ' ') then
            if (k .eq. 4) then
!
!                found correct location of first blank of first AMP line
!
              if (cline(8:9) .eq. 'HR') then
                cwsum(5:240) = cline(5:240)
              elseif (cline(5:9) .ne. '     ') then
!
!                   see if 'HR' clobbered
!
                call numchk (cline,5,7,num,iern)
                if (num.gt.0 .and. iern.eq.0) then
!
!                     numbers are in right location to be HR value
!
                  cwsum(5:7) = cline(5:7)
                  cwsum(8:9) = 'HR'
                  cwsum(11:240) = cline(11:240)
                else
                  write(*,*) 'MAJOR PROBLEM 1'
                  cwsum(5:9)    = 'XXXHR'
                  cwsum(11:240) = cline(5:234)
                endif
              endif
            else
!
!                   allow for major problem
!
              write(*,*) 'MAJOR PROBLEM 2'
              cwsum(5:9) = 'XXXHR'
              cwsum(11:240) = cline(k+1:240-11)
            endif
            goto 200
!
          endif
        enddo
      else
!
!                   NOTE: leading blanks have been removed from
!                   subsequent amplification lines, correct on output
!
        if (cline(4:5) .eq. 'HR') then
            cwsum(5:240) = cline(1:236)
        else
!
!                   see if 'HR' clobbered
!
          call numchk (cline,1,3,num,iern)
          if (num.gt.0 .and. iern.eq.0) then
!
!                     numbers are in right location to be HR value
!
            cwsum(5:7) = cline(1:3)
            cwsum(8:9) = 'HR'
            cwsum(11:240) = cline(7:236)
          else
            write(*,*) 'MAJOR PROBLEM 3'
            cwsum(5:9)    = 'XXXHR'
            cwsum(11:240) = cline(7:236)
          endif
        endif
      endif
  200 continue
!
!                   check for errors in hour value
!
      if (cwsum(5:5).ne.'X' .and. cwsum(6:6).ne.'X' .and.               &
     &    cwsum(7:7).ne.'X') then
        ierr = 0
      else
!                   set error return flag
        ierr = -1
      endif
      return
!
      end
      subroutine chkwsum (cwsum,maxsum,lkont,mxtau,csdtg,ngood,nerror,  &
     &                    keep)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  chkwsum
!
!  DESCRIPTION:  driver routine to check tropical warning summary
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
!  USAGE:
!    call chkwsum (cwsum,maxsum,lkont,mxtau,csdtg,ngood,nerror,keep)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    csdtg           char*10        input    computer synoptic time
!    cwsum           char*240       in/out   warning summary
!    keep            integer        output   flag: 0 - no keep
!                                                 >0 - keep, good
!                                                 <0 - keep, error
!    lkont           integer        in/out   line count of summary
!    maxsum          integer        input    max line count of summary
!    mxtau           integer        input    max index for tau of forecast
!    nerror          integer        in/out   sum of error summaries
!    ngood           integer        in/out   sum of good summaries?
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
!  bad values, missing values  set keep to -1 and return
!  wrong dtg for processing    set keep to 0 and return
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         ampchk      check AMP lines of summary
!         chkxy       check for 'X' or 'Y' in specified range
!         ckbasin     check for valid basin code
!         dirspdck    check on direction and speed of movement
!         headck      check summary header line
!         nnnnck      check/build NNNN line
!         numchk      check for all digits in specified range
!         tauampxck   cross check TAU values with AMP values
!         tauchk      check tau line
!         xtrcdna     extract dna of character string
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cline      char*240   working line of summary
!         cmdtg      char*12    message dtg
!         cx         char*1     character of string in line
!         dna        char*8     array of dna values of string
!         ier1       integer    error flag, 0 no error
!         iera       integer    error flag, 0 no error
!         ierb       integer    error flag, 0 no error
!         ierk       integer    error flag, 0 no error
!         ierr       integer    error flag, 0 no error
!         iert       integer    error flag, 0 no error
!         ierx       integer    error flag, 0 no error
!         mxdna      integer    max length of dna array
!         na         integer    number of AMP lines
!         nl         integer    output line count
!         nq         integer    number of ? inserted in lines
!         nt         integer    number of last TAU line
!         num        integer    character digits as a number
!         numlin     integer    number of dna lines in string
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
!                   set maximum number of dna lines per string
      integer maxdna
      parameter (maxdna = 180)
!
!         formal arguments
      integer maxsum, lkont, mxtau, ngood, nerror, keep
      character csdtg*10
      character*240 cwsum(maxsum)
!
!         local variables
      integer ierr, ier1, n, nq, nt, numlin, mxdna, iert, ierg, ierds
      integer iera, ierb, ierk, ierl, ierx, na, num
      character*1 cx
      character*8 dna(maxdna)
      character*12 cmdtg
      character*240 cline
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      keep = 0
      ierr = 0
!
!                   process summary header line
!
      mxdna = maxdna
!                 extract dna of character string of header
      call xtrcdna (cwsum(1),dna,mxdna,numlin,ierx)
      if (ierx .eq. 0) then
!                   no error, so check header line
        call headck (cwsum(1),dna,numlin,csdtg,ier1)
        if (ier1 .lt. 0) then
!
!                   summary is not within time window
!
          write (*,*) 'warn= ',cwsum(1)(1:10),' w_dtg= ',csdtg
          write (*,*) 'Summary NOT within time window'
          goto 600
!
        elseif (ier1 .eq. 0) then
!                     check for 'X' or 'Y', omit name section
         write(*,*) 'PRIOR chkxy: ',cwsum(1)(1:40) 
         call chkxy (cwsum(1),1,14,ier1)
          if (ier1 .eq. 0) call chkxy (cwsum(1),27,40,ier1)
        endif
        write(*,*) 'AFTER chkxy: ',cwsum(1)(1:40)
        if (ier1 .gt. 0) then
!                     at least one 'X' or 'Y' was found in header
          ierr = 1
        endif
!
!                 check initial/forecast (TAU) lines in summary
!
        nq = 0
        nt = min0 (mxtau+2,lkont)
        write(*,*) 'nt= ',nt
        do n=2, nt
          write(*,*) 'n=',n,'  ',cwsum(n)(1:40)
  200     continue
          cx = cwsum(n)(1:1)
          if (cx .eq. 'T') then
!                 TAU line found, get dna of string
            call xtrcdna (cwsum(n),dna,mxdna,numlin,ierx)
            if (ierx .eq. 0) then
!                   no error, so check values
              call tauchk (cwsum(n),dna,numlin,nq,iert)
!                   if no errors, double check for missing data
              if (iert .eq. 0)  call chkxy (cwsum(n),1,240,iert)
!                   sum number of lines with at least one error
              if (iert .ne. 0) ierr = ierr +1
            else
!                   this should not occur w/o stack/hardware problems
              goto 700
!
            endif
          elseif (cx.eq.'A' .or. cx.eq.'S' .or. cx.eq.'N') then
            write (*,*) 'FINISHED TAU lines'
!                   check basin indicator from header with latitudes
            call ckbasin (cwsum,n-1,ierb)
            if (ierb .ne. 0) ierr = ierr +1
            goto 300
!
          else
!
!                   this should never happen, but ....
!
            if (cwsum(n)(1:1).lt.'0' .or. cwsum(n)(1:1).gt.'9') then
              call numchk (cwsum(n),2,3,num,ierk)
              if (num.ge.0 .and. ierk.eq.0) then
!                   second and third characters are digits
!                   assume 'T' got clobbered
                cwsum(n)(1:1) = 'T'
                goto 200
!
              endif
            else
!                   assume AMP line is missing, make same
              cwsum(n)(5:240) = cwsum(n)(1:235)
              cwsum(n)(1:4)   = 'AMP '
            endif
            write (*,*) 'FINISHED TAU lines, assumed'
!                   check basin indicator from header with latitudes
            call ckbasin (cwsum,n-1,ierb)
            if (ierb .ne. 0) ierr = ierr +1
            goto 300
!
          endif
        enddo
        n = nt
        write (*,*) 'FINISHED TAU lines, forced ending'
        call ckbasin (cwsum,n,ierb)
        if (ierb .ne. 0) ierr = ierr +1
!
!                   missing AMP, SER and NNNN lines <should not happen>
!
        n = n +1
        cwsum(n)   = 'AMP'
        cwsum(n+1) = 'NNNN'
        lkont = n +1
      else
!                   this should not occur w/o stack/hardware problems
        goto 700
!
      endif
  300 continue
!
!                   set count of TAU lines
!
      nt = n -1
!
!                   process AMP lines
!
      na = 0
      cx = cwsum(n)(1:1)
      if (cx .ne. 'N') then
!
!                   process amplification line(s)
!
  400   continue
        call ampchk (cwsum(n),na,iera)
        na = na +1
        if (iera .eq. 0) call chkxy (cwsum(n),1,7,iera)
        if (iera .ne. 0) ierr = ierr +1
        if (n .lt. lkont) then
          n = n +1
          if (cwsum(n)(1:1) .ne. 'N') goto 400
!
        endif
      else
!
!                   missing AMP line, make same
!
        write(*,*) 'ADDED AMP line!'
        cline = cwsum(n)
        cwsum(n) = 'AMP'
        n = n +1
        cwsum(n) = cline
        lkont = lkont +1
      endif
!
!                   if a ? has been inserted, cross check missing
!                   tau radius descriptions with amplifying remarks
!
      if (nq .ne. 0) call tauampxck (cwsum,n,ierr)
!
!                   check on direction(s) and speed(s)
!
      call dirspdck (cwsum,n,nt,ierg,ierds)
      if (ierds .gt. 0) then
        if (cwsum(n)(48:50) .eq. '   ') then
!
!                   indicate to QC that one or more positions in error
!
          cwsum(n)(48:54) = 'D/S BAD'
        elseif (cwsum(n)(48:54) .eq. 'D/S OK ') then
!
!                   QC indicates all positions are good
!
          ierds = 0
        endif
      elseif (ierds .eq. 0) then
!
!                   signal no direction/speed errors were found
!
        cwsum(n)(48:54) = '       '
      endif
      ierr = ierr +ierg +ierds
!
!                   build/check NNNN line, last line in summary
!
cx   just fill last line with 'NNNN'  .... bs 12/6/95
cx    call nnnnck (cwsum(1),ierr,cwsum(n))
      cwsum(n)='NNNN'
!
  500 continue
      if (ierr .eq. 0) then
!                   no errors were found in summary
        ngood = ngood +1
        keep  = 9999
      else
!                   one or more lines were found in error
        nerror = nerror +1
        keep   = -1
      endif
  600 continue
      return
!
!                   Major problem section
!
  700 continue
      write (*,*) 'MAJOR ERROR - stack/hardware problem'
      ierr = 99
      goto 500
!
      end
      subroutine chkxy (cline,ks,kt,nxy)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  chkxy
!
!  DESCRIPTION:  check for 'X' or 'Y' in sub-string
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
!  USAGE:  call chkxy (cline,ks,kt,nxy)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline           char*240       input    character string
!    ks              integer        input    starting character position
!    kt              integer        input    ending character position
!    nxy             integer        output
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
!     -----------------           ----------------------------
!  starting and/or ending         set nxy to -1 and return
!  character positons in error
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
!         formal arguments
      integer ks, kt, nxy
      character cline*240
!
!         local variable
      integer k
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nxy = 0
      if (ks.lt.1 .or. ks.gt.240) nxy = -1
      if (kt.lt.1 .or. kt.gt.240) nxy = -1
      if (ks .gt. kt) nxy = -1
      if (nxy .eq. 0) then
        do k=ks, kt
          if (cline(k:k).eq.'X' .or. cline(k:k).eq.'Y') nxy = nxy +1
        enddo
      endif
      end
      subroutine ckbasin (cwsum,lkont,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  ckbasin
!
!  DESCRIPTION:  check basin of origin agrees with position latitudes
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
!  USAGE:  call ckbasin (cwsum,lkont,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsum           char*240       in/out   tropical warning summary
!    ierr            integer        output   error flag, 0 - no error
!    lkont           integer        input    line count of summary
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
!     invalid basin indicator  set error flag, set basin to 'Y' and exit
!     latitude does not agree  set error flag, set basin to 'Y' and exit
!
!  ADDITIONAL COMMENTS:
!
!        Symbolic example of first line of summary, with column numbers
!
!                 111111111122222222223333333333444444
!        123456789012345678901234567890123456789012345.............
!        YYYYMMDDHH IDB NAME       NRW NC DEG KT METH ---- ACC
!
!                  Explanation of first 3 symbols, left to right
!
!      YYYYMMDDHH - DATE-TIME-GROUP of initial position
!             IDB - CYCLONE IDENTIFICATION, number and origin basin
!            NAME - NAME or "NONAME" of tropical cyclone
!
!***********       Explanation of position lines of summary        *****
!
!     Symbolic example of position line of summary, with column numbers
!
!                 1111111111222222222233333333334444
!        1234567890123456789012345678901234567890123...............
!        THHH LAT  LON   MXW RSPD NMI DD ---
!
!                  Explanation of first 3 symbols, left to right
!
!        T   - T is flag for TAU of position, hrs
!        HHH - hours of position 000 - 072 -> expansion
!        LAT - LATITUDE  and N or S for hemisphere, degrees and tenths
!        LON - LONGITUDE and E OR W for hemisphere, degrees and tenths
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cb         char*1     basin of origin indicator
!         cbasin     char*1     array of valid basin indicators
!         ch         char*1     array of hemisphere indicators
!         cx         char*1     working character
!         nh         integer    number of NH indicators
!         np         integer    number of valid positions
!         ns         integer    number of SH indicators
!
!  METHOD:  1)  See that basin indicator is valid.
!           2)  If valid, see that hemisphere indicators agree with
!               basin indicators, allow for non-valid hemiphere
!               indicators.
!           3)  If basin not in agreement with hemipshere indicators,
!               set basin to 'Y' for QC correction.
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
      integer mxck
      parameter (mxck = 5)
!
!         formal parameters
      integer lkont, ierr
      character cwsum(lkont)*240
!
!         local variables
      integer n, np, nh, ns
      character*1 cb, cx, ch(mxck), cbasin(8)
!
!                   valid basin of origin indicators, all but S and P
!                   are in NH.  {tropical cyclones can't cross equator}
      data cbasin/'A', 'B', 'W', 'C', 'E', 'L', 'S', 'P'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr = 1
!
!                   extract basin of origin
!
      cb = cwsum(1)(14:14)
      if (cb .ne. 'Y') then
!
!                   check that basin indicator is valid
!
        do n=1, 8
          if (cb .eq. cbasin(n)) ierr = 0
        enddo
      endif
      if (ierr .eq. 0) then
!
!                   check that valid basin indicator matches with
!                   hemisphere in latitudes (allow for some errors
!                   in latitude indicators)
!
        np = 0
        do n=2, lkont
          if (cwsum(n)(1:1) .eq. 'T') then
!
!                   process TAU lines of position
!
            cx = cwsum(n)(9:9)
            if (cx.eq.'N' .or. cx.eq.'S') then
!
!                     valid hemisphere found
!
              if (np .lt. mxck) then
!
!                       sum and store valid hemisphere indicators
!
                np     = np +1
                ch(np) = cx
              endif
            endif
          endif
        enddo
        if (np .gt. 0) then
          nh = 0
          ns = 0
          do n=1, np
            if (ch(n) .eq. 'N') then
              nh = nh +1
            else
              ns = ns +1
            endif
          enddo
          if (nh .gt. ns) then
!
!                   check that cyclone is in NH
!
            if (cb.eq.'S' .or. cb.eq.'P') ierr = 1
          else
!
!                   check that cyclone is in SH
!
            if (cb.ne.'S' .and. cb.ne.'P') ierr = 1
          endif
        endif
      endif
!
!                   if basin appears in error, signal error for QC
!                   by setting basin to 'Y'
!
      if (ierr .ne. 0) cwsum(1)(14:14) = 'Y'
      end
cx    subroutine dbread (cwsum,nlmax,ndbr,nlred,ierrd)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  dbread
!
!  DESCRIPTION:  read messages of type TC/WRNG_SMRY_ERROR with
!                status of ck_error from ISIS database
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
!  USAGE:  call dbread (cwsum,nlmax,ndbr,nlred,ierrd)
!
!  PARAMETERS:
!     Name      Type         Usage            Description
!    ------    ----------   -------  ----------------------------
!    cwsum     char*240     output   tropcial warning summary msg
!    ierrd     integer      output   read error flag, 0 - no error
!    ndbr      integer      in/out   number of messages read
!    nlmax     integer      input    maximum number of lines in msg
!    nlred     integer      output   number of lines in msg read
!
!  COMMON BLOCK:
!       Block     Name    Type     Usage              Notes
!      -------  --------  ----     ------   ----------------------------
!      /cisis/   qc_ids   char*32  output   message id1 thru id5 read
!
!  FILES:  none
!
!  DATA BASES:
!     Name       Table       Usage            Description
!    ------     -------     -------     --------------------------------
!     ISIS        TC         input      tropical warning summary with
!                                       error
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     ISIS read error          set error flag and exit
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     -------------------------------------
!         msg_rd      FNMOC ISIS utility to read messages
!
!  LOCAL VARIABLES:
!        Name        Type                 Description
!       ---------    ----       ----------------------------------------
!       arvl_dtg    char*14     arrival dtg of message
!       clasif      char*8      classification of message
!       com_cir     char*24     communications circuit that sent message
!       enc_typ     char*24     encoding type
!       ierr_rd     integer     ISIS completion code
!       in_msg_id1  char*32     cyclone number and basin of origin
!       in_msg_id2  char*32     dtg of first position in message
!       in_msg_id3  char*32     warning number and amendment of message
!       in_msg_id4  char*32     cyclone name
!       in_msg_id5  char*32     "not used"
!       in_msg_typ  char*24     message subtype
!       msg_dtg     char*16     message dtg
!       msg_typ     char*24     message type
!       num_byte    integer     number of bytes (available/read)
!       org_tx      char*32     originator of message
!       out_msg_typ char*24     message subtype - read
!       status_in   char*8      requested status
!       status_rd   char*8      status of message read
!       w_dtg_in    char*10     requested watch dtg
!       w_dtg_rd    char*10     read watch dtg
!
!  METHOD:  1) set message type to WRNG_SMRY_ERROR
!           2) set status to 'ck_error'
!           3) set in_w_dtg and all msg_id to '*' to read all these
!              type of messages that have an uncorrected error
!
!  INCLUDE FILES:
!       Name                           Description
!    ---------------    ------------------------------------------------
!    cisis.inc          contains common block cisis
!
!  COMPILER DEPENDENCIES:  none
!
!  COMPILE OPTIONS:  f77 with f90 extensions or f90
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!..............................END PROLOGUE.............................
!
cx    implicit none
!
!         formal parameters
cx    integer nlmax, ndbr, nlred, ierrd
cx    character*240 cwsum(nlmax)
!
!         local variables
cx    integer n, nl, nk
!
!                   ISIS MSG_RD parameters
!         INPUT:
cx    character*8  clasif, status_in
cx    character*10 w_dtg_in
cx    character*24 msg_typ, in_msg_typ
cx    character*32 in_msg_id1, in_msg_id2, in_msg_id3, in_msg_id4
cx    character*32 in_msg_id5
!                  Note: num_byte must be set as an input value
!
!         OUTPUT:
cx    integer num_byte, ierr_rd
!     character*8 status_rd
!     character*10 w_dtg_rd
cx    character*14 arvl_dtg
cx    character*16 msg_dtg
cx    character*24 out_msg_typ, com_cir, enc_typ
cx    character*32 org_tx
!
cx    INCLUDE 'cisis.inc'
!
cx    data msg_typ/'TC'/
cx    data in_msg_typ/'WRNG_SMRY_ERROR'/
cx    data clasif/'UNCLASS'/
!                   set all input to match any value
cx    data in_msg_id1/'*'/
cx    data in_msg_id2/'*'/
cx    data in_msg_id3/'*'/
cx    data in_msg_id4/'*'/
cx    data in_msg_id5/'*'/
cx    data status_in/'ck_error'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
cx    w_dtg_in = '*'
cx    num_byte = nlmax*240
!
!                   read error message from ISIS database
!
cx    call msg_rd (msg_typ,in_msg_typ,in_msg_id1,in_msg_id2,in_msg_id3, &
cx   &             in_msg_id4,in_msg_id5,clasif,w_dtg_in,status_in,     &
cx   &             out_msg_typ,                                         &
cx   &             qc_ids(1),qc_ids(2),qc_ids(3),qc_ids(4),qc_ids(5),   &
cx   &             num_byte,cwsum,w_dtg_rd,msg_dtg,arvl_dtg,org_tx,     &
cx   &             com_cir,status_rd,enc_typ,ierr_rd)
cx    ndbr = ndbr +1
cx    if (ierr_rd .lt. 0) then
!
!                   ISIS read error
!
cx      ierrd = -1
cx    elseif (ierr_rd .eq. 100) then
!
!                   ISIS no find signal
!
cx      if (ndbr .eq. 1) then
cx        write (*,*) 'NO ERROR WARNING SUMMARY FOUND'
cx        ierrd = 90
cx      else
cx        write (*,*) 'NO MORE ERROR SUMMARIES FOUND'
cx        ierrd = 99
cx      endif
cx    else
!                   good ISIS read
cx      ierrd = 0
cx    endif
cx    if (ierrd .eq. 0) then
cx      nlred = num_byte/240
cx      write (*,*) 'Good read of msg ',ndbr,' lines read ',nlred
cx      nl = 0
cx      do n=1, nlred
!                   remove blank lines
cx        if (cwsum(n) .ne. ' ') then
cx          nl = nl +1
cx          if (nl .ne. n) cwsum(nl) = cwsum (n)
cx          if (nl .gt. 0) then
!
!                   left justify, upper case and screen data
!
cx            call lftuppr (cwsum(nl),nk)
!                   nk is zero for no valid data
cx            if (nk .eq. 0) nl = nl -1
cx          endif
cx          if (cwsum(nl)(1:4) .eq. 'NNNN')  goto 150
!
cx        endif
cx      enddo
cx      write(*,*) 'WARNING NNNN NOT FOUND in dbread'
cx150   continue
cx      nlred = nl
cx    elseif (ierrd .ge. 90 ) then
!                    no more summaries to read
cx      write (*,*) 'No more summaries to read'
cx    else
!                   ISIS read error
cx      write (*,*) '**** ISIS error is ',ierr_rd
cx    endif
cx    return
!
cx    end
cx    subroutine dbwrit (cwsum,nlmax,lkont,keep,nqcd,csdtg,ierwt)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  dbwrit
!
!  DESCRIPTION:  write a warning message summary to ISIS and clean-up
!                as required.
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
!  USAGE:  call dbwrit (cwsum,nlmax,lkont,keep,nqcd,csdtg,ierwt)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ---------------------------
!    csdtg           char*10        input    computer synoptic time
!    cwsum           char*240       input    warning summary
!    ierwt           integer        unused   error flag, 0 - no error
!    keep            integer        input    good/bad summary
!                                             >0 all good data
!                                             <0 bad data in summary
!    lkont           integer        input    number of lines in summary
!    nlmax           integer        input    max number of lines in msg
!    nqcd            integer        input    flag for source of msg
!                                               0 - from AUTODIN/AWN/DDN
!                                              -1 - from ISIS error msg
!
!  COMMON BLOCK:
!       Block       Name     Type      Usage              Notes
!      --------   -------    -------   ------   -------------------------
!      /cisis/    status_rd  char*8    input    old status
!                 qc_ids     char*32   input    old qc_ids
!                 w_dtg_rd   char*10   input    old watch_dtg
!
!  FILES:
!       Name         Unit    Type    Attribute  Usage     Description
!    ----------      ----  --------  ---------  -------  ---------------
!   prcwsum.diag      20   local     sequential output   diagnostics
!   cyclone_id.allow  30   permanent sequential input    allowed cyclone
!   tapps.log         60   permanent sequential output   QC-log display
!
!  DATA BASES:
!       Name             Table        Usage            Description
!    ----------     --------------  ---------   -------------------------
!      ISIS              TC          in/out     TC warning summary
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     ISIS errors              set error flag and exit
!
!  ADDITIONAL COMMENTS:
!
!         ************** template of cwsum(1) ************************
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         yyyymmddhh idb name       wnra nc deg kt meth ---- acc
!                        1234567890
!
!         ************** template of cwsum(lkont) **********************
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         NNNN ORIG YYYYMMDDHHmm YYYYMMDDHHmmss CIR NExx
!                   123456789012 12345678901234
!                        tx            rx
!
!            MSG_SUBTYPE:   STATUS:        COMMENTS:
!          WRNG_SMRY_INDIV  ck_good  - initially good or corrected
!                           ck_windp - processed by windp/strikep
!          WRNG_SMRY_ERROR  ck_error - has at least one error
!                           ck_corr  - corrected msg placed in
!                                      WRNG_SMRY_INDIV as ck_good
!                                      old errors in body of this
!                                      message
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         chkxy       check for 'X' or 'Y' - bad data
!         msg_del     delete message with FNMOC ISIS routine
!         msg_rd      read message with FNMOC ISIS routine
!         msg_wr      write message with FNMOC ISIS routine
!
!  LOCAL VARIABLES:
!        Name        Type                 Description
!       ------       ----       -----------------------------------------
!       arvl_dtg     char*14    arrival dtg of message
!       clasif       char*8     classification
!       com_cir      char*24    communications circuit
!       cyc_id       char*3     cyclone number and basin of origin
!       enc_typ      char*24    type of encoding
!       ierdl        integer    delete error flag for
!       ierr_rd      integer    read error flag
!       ierwr        integer    write error flag
!       ioe          integer    I/O error flag
!       msg_dtg      char*12    message dtg
!       msg_id1      char*32    cyclone number and basin of origin
!       msg_id2      char*32    dtg of first position in message
!       msg_id3      char*32    warning number and amendment of message
!       msg_id4      char*32    cyclone name
!       msg_id5      char*32    "not used"
!       msg_subtyp   char*24    array of subtypes of messages
!       msg_typ      char*24    type of message
!       nm           integer    index to msg_subtyp array
!       num_byte     integer    number of bytes (available/read/written)
!       nxy          integer    count of 'X' and/or 'Y' in string
!       org_tx       char*32    origin of transmission
!       out_ids      char*32    output id's of summary
!       out_msg_typ  char*24    output msg sub-type
!       status       char*8     status code of message
!
!  METHOD:  1) Check that cyclone ID is an allowed ID for processing.
!           2) If keep > 0, write message summary in WRNG_SMRY_INDIV
!              else, write message summary in WRNG_SMRY_ERROR.
!           3) Write tapps.log information.
!           4) If good message came from ISIS with a previous error,
!              read old message with error, change status and write
!              message; then delete old message with error status.
!
!  INCLUDE FILES:
!       Name                         Description
!    -----------     -------------------------------------------------
!     cisis.inc      output message id's, w_dtg and status from initial
!                    message with at least one error
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
cx    implicit none
!
!         formal parameters
cx    integer nlmax, lkont, keep, nqcd, ierwt
cx    character cwsum(nlmax)*240, csdtg*10
!
!         local variables
!
cx    integer ierdl, ierr_rd, ierwr, ioe, nm, nxy
!
!                   ISIS MSG_WR parameters
!         INPUT:
cx    integer num_byte
cx    character*8  clasif, status
cx    character*10 w_dtg
cx    character*12 msg_dtg
cx    character*14 arvl_dtg
cx    character*24 msg_typ, msg_subtyp(2)
cx    character*24 com_cir, enc_typ
cx    character*32 msg_id1, msg_id2, msg_id3, msg_id4, msg_id5
cx    character*32 org_tx
!
!         OUTPUT:
!     integer ierwt
!
cx    character cyc_id*3
cx    character w_dtg_out*10
cx    character*24 out_msg_typ
cx    character*32 out_ids(5)
!
cx    INCLUDE 'cisis.inc'
!
cx    data msg_typ/'TC'/
cx    data msg_subtyp/'WRNG_SMRY_INDIV', 'WRNG_SMRY_ERROR'/
!                   the 5th id is not used in MSG_WR for this message
!                   sub_type, so set to underbar to represent "blank"
cx    data msg_id5/'_'/
cx    data clasif/'UNCLASS'/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
cx    write(*,*) 'INTO dbwrit, keep= ',keep
cx    nm = 0
cx    if (lkont .le. nlmax) then
cx      rewind (30)
cx      do
cx        read (30,'(a3)',iostat=ioe) cyc_id
cx        if (ioe .eq. 0) then
!
!                 check that cyclone is amoung the allowed
!
cx          if (cyc_id(1:3) .eq. cwsum(1)(12:14)) then
cx            cwsum(lkont)(56:73) = ' '
cx            exit
!
cx          endif
cx        else
!                 signal an error has been found
cx          keep = -1
!                 allert QC that cyclone ID is not authorized for
!                 full processing
cx          cwsum(lkont)(56:73) = 'cyc_id NOT ALLOWED'
cx          write (*,*) ' cyclone ID NOT ALLOWED is ',cyc_id(1:3)
cx          exit
!
cx        endif
cx      enddo
cx      if (keep .gt. 0) then
!
!                   summary checks good
!                     set input parameters for WRNG_SMRY_INDIV
!
!                   tropical cyclone ID - number and original basin
cx        msg_id1 = cwsum(1)(12:14)
!                   dtg of initial position in warning - YYYYMMDDHH
cx        msg_id2 = cwsum(1)(1:10)
!                   tropical warning number, include amendment
!                   modification letter (21 , 21A, 21B, etc)
cx        msg_id3 = cwsum(1)(27:30)
!                   set trailing blank to underbar
cx        if (msg_id3(4:4) .eq. ' ') msg_id3(4:4) = '_'
!                   tropical cyclone name
cx        msg_id4  = cwsum(1)(16:25)
cx        if (nqcd .eq. 0) then
cx          w_dtg = csdtg
cx        else
cx          w_dtg = w_dtg_rd
cx        endif
cx        status   = 'ck_good'
cx        nm       = 1
cx      elseif (keep .lt. 0) then
!
!                   summary checks bad
!                     set input parameters for WRNG_SMRY_ERROR
!
!                   tropical cyclone ID - number and original basin
cx        call chkxy (cwsum(1),12,13,nxy)
cx        if (nxy .eq. 0) then
cx          msg_id1 = cwsum(1)(12:14)
cx        else
cx          msg_id1 = '_'
cx        endif
!                   dtg of initial position in warning - YYYYMMDDHH
cx        call chkxy (cwsum(1),1,10,nxy)
cx        if (nxy .eq. 0) then
cx          msg_id2 = cwsum(1)(1:10)
cx        else
cx          msg_id2 = '_'
cx        endif
!                   tropical warning number, include amendment
!                   modification letter (21 , 21A, 21B, etc)
cx        call chkxy (cwsum(1),27,30,nxy)
cx        if (nxy .eq. 0) then
cx          msg_id3 = cwsum(1)(27:30)
!                     set trailing blank to underbar
cx          if (msg_id3(4:4) .eq. ' ') msg_id3(4:4) = '_'
cx        else
cx          msg_id3 = '_'
cx        endif
!                   tropical cyclone name
cx        if (cwsum(1)(16:16) .ne. 'Y') then
cx          msg_id4 = cwsum(1)(16:25)
cx        else
cx          msg_id4 = '_'
cx        endif
cx        if (nqcd .eq. 0) then
cx          w_dtg = csdtg
cx        else
cx          w_dtg = w_dtg_rd
cx        endif
cx        status = 'ck_error'
cx        nm = 2
cx      endif
cx      if (lkont .lt. nlmax)  cwsum(lkont+1) = ' '
!
cx      num_byte = nlmax*240
cx      msg_dtg  = cwsum(lkont)(11:22)
cx      arvl_dtg = cwsum(lkont)(24:37)
cx      org_tx   = cwsum(lkont)(6:9)
cx      com_cir  = cwsum(lkont)(39:41)
cx      enc_typ  = 'none'
cx      write(*,*) 'status= ',status
cx      write(*,*) 'nm= ',nm,'  keep= ',keep
cx      pause
!
cx      call msg_wr (msg_typ,msg_subtyp(nm),msg_id1,msg_id2,msg_id3,    &
cx   &              msg_id4,msg_id5,clasif,num_byte,cwsum,w_dtg,msg_dtg,&
cx   &              arvl_dtg,org_tx,com_cir,status,enc_typ,ierwr)
cx      if (ierwr .eq. 0) then
cx        write (*,*) 'Wrote ',msg_id1,' to ISIS for: '
cx        write (*,*) 'typ = ',msg_typ,' sub= ',msg_subtyp(nm)
cx        write (*,*) 'dtg= ',msg_id2
cx        ierwt = 0
cx      else
cx        write(*,*) 'msg_typ = ',msg_typ
cx        write(*,*) 'msg_subtyp = ',msg_subtyp
cx        write(*,*) 'msg_id1 = ',msg_id1
cx        write(*,*) 'msg_id2 = ',msg_id2
cx        write(*,*) 'msg_id3 = ',msg_id3
cx        write(*,*) 'msg_id4 = ',msg_id4
cx        write(*,*) 'msg_id5 = ',msg_id5
cx        write(*,*) 'clasif  = ',clasif
cx        write(*,*) 'num_byte= ',num_byte
cx        write(*,*) 'cswum   = ',cwsum(1)(1:40)
cx        write(*,*) 'w_dtg   = ',w_dtg
cx        write(*,*) 'msg_dtg = ',msg_dtg
cx        write(*,*) 'arvl_dtg= ',arvl_dtg
cx        write(*,*) 'org_tx  = ',org_tx
cx        write(*,*) 'com_cir = ',com_cir
cx        write(*,*) 'status  = ',status
cx        write(*,*) 'enc_typ = ',enc_typ
cx        open (60,file="tapps.log",form="formatted",action="write",    &
cx   &          status="old",position="append",iostat=ioe)
cx        if (ioe .eq. 0) then
cx          status = 'WRT_EROR'
cx          write (60,9060,iostat=ioe) msg_id1,msg_id2,msg_id3,msg_dtg, &
cx   &             arvl_dtg,status
c9060       format (a3,1x,a10,1x,a4,1x,a12,1x,a14,1x,a8)
cx          if (ioe .ne. 0) write (*,*) 'ERROR, write of tapps.log is ',&
cx   &          ioe
cx          close (60)
cx          pause
!
cx          ierwt = -1
cx          goto 900
!
cx        else
cx          write (*,*) 'ERROR, cant open tapps.log'
cx          ierwt = -1
cx          goto 900
!
cx        endif
cx      endif
!
!                   write to TAPPS.LOG file
!
cx      open (60,file="tapps.log",form="formatted",action="write",      &
cx   &          status="old",position="append")
cx      write (60,9060) msg_id1,msg_id2,msg_id3,msg_dtg,arvl_dtg,status
cx      close (60)
!
cx      if (nqcd.lt.0 .and. keep.gt.0) then
!
!                   Summary was corrected by QC, and summay is now good
!
!                     read old error summary
!
cx        call msg_rd (msg_typ,msg_subtyp(2),                           &
cx   &             qc_ids(1),qc_ids(2),qc_ids(3),qc_ids(4),qc_ids(5),   &
cx   &             clasif,w_dtg_rd,status_rd,                           &
cx   &             out_msg_typ,                                         &
cx   &           out_ids(1),out_ids(2),out_ids(3),out_ids(4),out_ids(5),&
cx   &           num_byte,cwsum,w_dtg_out,msg_dtg,arvl_dtg,org_tx,      &
cx   &           com_cir,status,enc_typ,ierr_rd)
cx        if (ierr_rd.ge.0 .and. ierr_rd.ne.100) then
!
!                   good read of old message, now re-write old error
!                   summary, but change status and use corrected msg_ids
!
cx          status = 'qc_corr'
cx          call msg_wr (msg_typ,msg_subtyp(nm),msg_id1,msg_id2,msg_id3,&
cx   &             msg_id4,msg_id5,clasif,num_byte,cwsum,w_dtg_rd,      &
cx   &             msg_dtg,arvl_dtg,org_tx,com_cir,status,enc_typ,ierwr)&
!
!                     delete old error summary, error status
!                     use old msg_ids
!
cx          if (ierwr .eq. 0) then
cx            call msg_del (msg_typ,msg_subtyp(2),                      &
cx   &              qc_ids(1),qc_ids(2),qc_ids(3),qc_ids(4),qc_ids(5),  &
cx   &              clasif,w_dtg_rd,status_rd,ierdl)
cx            if (ierdl .ne. 0) then
cx              write(*,*) 'ISIS delete error is ',ierdl
cx              ierwt = 70
cx            endif
cx          else
cx            ierwt = 60
cx          endif
cx        else
cx          write(*,*) 'ISIS ERROR in reading old error summary'
cx          ierwt = 50
cx        endif
cx      endif
cx    else
cx      write (*,*) 'ERROR, message too long'
cx      write (20,*) 'ERROR, dbwrit - message too long'
cx      ierwt = -77
cx    endif
cx900 continue
cx    return
!
cx    end
      subroutine dirspd (sl,sg,el,eg,time,head,spd)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  dirspd
!
!  DESCRIPTION:  Calculate heading and speed from "sl,sg" to "el,eg",
!                in "time" hours for the tropics and sub-tropics
!
!  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  None
!
!  CLASSIFICATION:  Unclassified
!
!  RESTRICTIONS:  None
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:   None
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call dirspd (sl,sg,el,eg,time,head,spd)
!
!  PARAMETERS:
!     NAME         TYPE        USAGE             DESCRIPTION
!   --------      -------      ------   ------------------------------
!        sl        real        input    starting latitude, -SH
!        sg        real        input    starting longitude, (0 - 360 E,
!                                       or -W)
!        el        real        input    ending latitude, -SH
!        eg        real        input    ending longitude, (0 - 360 E,
!                                       or -W)
!      time        real        input    time in hours for travel
!      head        real        output   heading (deg)
!       spd        real        output   speed (kt) or error flag when
!                                       value is negative
!
!  COMMON BLOCKS:  None
!
!  FILES:  None
!
!  DATA BASES:  None
!
!  NON-FILE INPUT/OUTPUT:  None
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!    negative time             return negative speed
!
!  ADDITIONAL COMMENTS:
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          NAME      TYPE                 DESCRIPTION
!         ------     ----       ----------------------------------
!         a45r       real       radians in 45 degrees
!         dist       real       distance between sl,sg and el,eg (nm)
!         eln1       real       calculation factor
!         eln2       real       calculation factor
!         ihead      int        integer of head times 10
!         inil       int        flag for initial calculations
!         ispd       int        integer of spd times 10
!         rad        real       degrees per radian
!         radi       real       radinas per degree
!         rdi2       real       0.5 times radi
!         tiny       real       tiny number, hardware dependent
!         xg         real       local copy of sg
!         xl         real       local copy of sl
!         xr         real       calculation factor
!         yr         real       calculation factor
!         yg         real       local copy of eg
!         yl         real       local copy of el
!
!  METHOD:  Based upon rhumb line calculations from Texas Instruments
!           navigation package for hand held calculator
!
!  INCLUDE FILES:  None
!
!  COMPILER DEPENDENCIES:  F77 with F90 extentions or F90
!
!  COMPILE OPTIONS:  Standard operational settings
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!
!...................END PROLOGUE.......................................
!
      implicit none
!
!         formal parameters
      real sl, sg, el, eg, time, head, spd
!
!         local variables
      integer ihead, inil, ispd
      real a45r, eln1, eln2, rad, radi, rdi2, tiny, xg, xl, yg, yl, dist
      real xr, yr
!
      save rad,radi,rdi2,a45r
!
!CC   DATA TINY/0.1E-8/
!                   SIZE OF TINY IS HARDWARE DEPENDENT
      data tiny/0.1e-6/
!                   MAXIMUM POLEWARD LATITUDE, HARDWARE DEPENDENT
!CC   DATA PLMX/89.99/
      data inil/-1/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      if (inil .ne. 0) then
        inil = 0
        rad  = 180.0/acos (-1.0)
        radi = 1/rad
        rdi2 = 0.5*radi
        a45r = 45.0*radi
      endif
!
!                   pre-set heading and distance, for same point input
!
      head = 0.0
      dist = 0.0
      if (abs (sl -el).gt.tiny .or. abs (sg -eg).gt.tiny) then
        xl = sl
        xg = sg
!
!                   if longitude is west, convert to 0-360 East
!
        if (xg .lt. 0.0) xg = xg +360.0
        yl = el
        yg = eg
!
!                   if longitude is west, convert to 0-360 East
!
        if (yg .lt. 0.0) yg = yg +360.0
!
!                    check for shortest angular distance
!
        if (xg.gt.270.0 .and. yg.lt.90.0) yg = yg +360.0
        if (yg.gt.270.0 .and. xg.lt.90.0) xg = xg +360.0
!
        if (abs (xl -yl) .le. tiny) then
!
!                    resolve 90 or 270 heading
!
          head = 90.0
          if (yg .lt. xg) head = 270.0
          dist = 60.0*(yg -xg)*cos (xl*radi)
        else
          dist = 60.0*(xl -yl)
          if (abs (xg -yg) .le. tiny) then
!
!                  resolve 0 or 180 heading, note head is preset to zero
!
            if (yl .lt. xl) head = 180.0
          else
!                   CHECK FOR POSITIONS POLEWARD OF 89+ DEGREES LATITUDE
!CC         IF (ABS (XL).GT.PLMX .OR. ABS (YL).GT.PLMX) THEN
!           (HARDWARE DEPENDENT - NOT REQUIRED FOR TROPICAL CYCLONES)
!CC           XLT = XL
!CC           IF (ABS (XLT) .GT. PLMX) XLT = SIGN (PLMX,XL)
!CC           YLT = YL
!CC           IF (ABS (YLT) .GT. PLMX) YLT = SIGN (PLMX,YL)
!CC           XR = TAN (XLT*RDI2 +SIGN (A45R,XL))
!CC           YR = TAN (YLT*RDI2 +SIGN (A45R,YL))
!CC         ELSE
              xr = tan (xl*rdi2 +sign (a45r,xl))
              yr = tan (yl*rdi2 +sign (a45r,yl))
!CC         ENDIF
            eln1 = sign (alog (abs (xr)),xr)
            eln2 = sign (alog (abs (yr)),yr)
            head = rad*(atan ((xg -yg)/(rad*(eln1 -eln2))))
            if (yl   .lt. xl)  head = head +180.0
            if (head .lt. 0.0) head = head +360.0
!
!                   correct initial distance, based only on latitude
!
            dist = dist/cos (head*radi)
          endif
        endif
        if (time .gt. 0.0) then
          spd  = dist/time
          ispd = anint (abs (spd)*10.0)
          spd  = 0.1*(float (ispd))
        else
!
!                   FLAG ERROR for bad value of time
!
          spd = -abs (dist)
        endif
        ihead = anint (head*10.0)
        head  = 0.1*(float (ihead))
      endif
      return
!
      end
      subroutine dirspdck (cwsum,nn,nt,ierr,ierds)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  dirspdck
!
!  DESCRIPTION:  driver routine to check on direction and speed of movement
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
!  USAGE:  call dirspdck (cwsum,nn,nt,ierds)
!
!  PARAMETERS:
!       Name         Type         Usage            Description
!    --------     ----------     -------    ----------------------------
!    cwsum        char*240       input      warning summary
!    ierds        integer        output     dir/spd error flag, 0 no error
!    ierr         integer        output     other error flag, 0 no error
!    nn           integer        input      number of lines in cwsum
!    nt           integer        input      line count of last tau line
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
!  bad directions/speeds       increment error flag for each error
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!        --------      ----------------------
!        chkxy         check for 'X' & 'Y' within given string range
!        exltln        extract latitud end longitude
!        dtrhrs        determine hours between positions
!        dirspd        compute direction (deg) and speed (kt) between
!                      positions
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!            alt     real       absolute value of latitiude
!        cnghead     real       change in heading between segments, degrees
!             cx     char       working hemisphere flag character
!            eln     real       ending longitude
!            elt     real       ending latitude
!          head1     real       heading of first  segment
!          head2     real       heading of second segment
!          hours     real       hours between starting and ending positions
!           ier1     int        error flag for first  segment
!           ier2     int        error flag for second segment
!           ierc     int        error flag from 1 to 2 segments
!         speed1     real       speed during first  segment, kt
!         speed2     real       speed during second segment, kt
!
!  METHOD:
!     1)  Check that position has valid characters
!     2)  Obtain latitude and longitude for starting and ending points of
!         segment.
!     3)  Obtain speed and direction of movement.
!     4)  If speed is over 80 kts, speed is bad
!         If speed is over 40 kts at less than 22.5 degrees, speed is bad
!     5)  If speed and heading are available for adjacent segments, and
!         speed is at lease 7.5 kts in both segments, then:
!            if heading changes more than 45 degrees, mark as error.
!            if speed in second segment is less than 1/2 or greater than
!            twice the speed of the first segment, mark as error.
!     6)  Do for all segments, pass segment 2 values to new segment 1
!         values during processing.
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
      integer nn, nt, ierr, ierds
      character*240 cwsum(nn)
!
!         local variables
      integer ks, kt, ier1, ier2, n, nxy1, nxy2, ilt, jln
      character cx*1
      real slt, sln, elt, eln, alt, head1, head2, speed1, speed2, hours
      real cnghead
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr   =   0
      ierds  =   0
      ks     =   2
      kt     =  15
      slt    =  99.9
      sln    = 999.9
      ier1   =  -1
      head1  =  -1.0
      speed1 =  -1.0
!
!                   process all TAU lines in summary
!
      do n=2, nt -1
!
!                   check for missing values of tau, lat & lon
!
        call chkxy (cwsum(n),ks,kt,nxy1)
        if (nxy1 .eq. 0) then
!
!                   if starting position is not set, set it
!
          if (slt.gt.90.0 .and. ier1.le.0) then
            call exltln (cwsum(n),ilt,jln,slt,sln)
            ier1 = 0
            if (ilt .gt.  700) then
              cwsum(n)(6:8) = 'XXX'
              ier1 = 1
            endif
            cx = cwsum(n)(9:9)
            if (cx.ne.'N' .and. cx.ne.'S') then
              cwsum(n)(9:9) = 'Y'
              ier1 = ier1 +1
            endif
            if (jln .gt. 1800) then
              cwsum(n)(11:14) = 'XXXX'
              ier1 = ier1 +1
            endif
            cx = cwsum(n)(15:15)
            if (cx.ne.'E' .and. cx.ne.'W') then
              cwsum(n)(15:15) = 'Y'
              ier1 = ier1 +1
            endif
          endif
        else
          slt    =  99.9
          sln    = 999.9
          head1  =  -1.0
          speed1 =  -1.0
          ier1   =  -1
        endif
!
!                   check for missing values of tau, lat & lon
!
        call chkxy (cwsum(n+1),ks,kt,nxy2)
        if (nxy2 .eq. 0) then
!
!                   extract ending position
!
          call exltln (cwsum(n+1),ilt,jln,elt,eln)
          ier2 = 0
          if (ilt .gt.  700) then
            cwsum(n+1)(6:8) = 'XXX'
            ier2 = 1
          endif
          cx = cwsum(n+1)(9:9)
          if (cx.ne.'N' .and. cx.ne.'S') then
            cwsum(n+1)(9:9) = 'Y'
            ier2 = ier2 +1
          endif
          if (jln .gt. 1800) then
            cwsum(n+1)(11:14) = 'XXXX'
            ier2 = ier2 +1
          endif
          cx = cwsum(n+1)(15:15)
          if (cx.ne.'E' .and. cx.ne.'W') then
            cwsum(n+1)(15:15) = 'Y'
            ier2 = ier2 +1
          endif
        else
          elt    =  99.9
          eln    = 999.9
          head2  =  -1.0
          speed2 =  -1.0
          ier2   =  -1
        endif
        if (ier1.eq.0 .and. ier2.eq.0) then
!
!                   get hours between starting and ending positions
!
          call dtrhrs (cwsum(n),cwsum(n+1),hours)
!
!                   get direction/speed from pt 1 to pt 2
!
          call dirspd (slt,sln,elt,eln,hours,head2,speed2)
          if (speed2 .ge. 0.0) then
!                     speed and heading were calculated
            alt = abs (elt)
            if (speed2 .gt. 80.0) then
              ierds = ierds +1
              ier2  = 1
            elseif (alt .lt. 22.5) then
              if (speed2 .gt. 40.0) then
                ierds = ierds +1
                ier2  = 1
              endif
            else
              ier2 = 0
            endif
            if (ier1.eq.0 .and. ier2.eq.0) then
!
!                   see if changes in heading and speed should be checked
!
              if (speed1.gt.7.5 .and. speed2.gt.7.5) then
!
!                     obtain change in heading
!
                cnghead = abs (head2 -head1)
                if (cnghead .gt. 179.0) then
                  if (head2.gt.180.0 .and. head1.lt.180.0) then
                    cnghead = abs (head2 -(head1 +360.0))
                  elseif (head1.gt.180.0 .and. head2.lt.180) then
                    cnghead = abs ((head2 +360.0) -head1)
                  endif
                endif
!
!                     check on changes in heading and speed
!
                if (cnghead.gt.45.0 .or. (speed2.lt.0.5*speed1 .or.     &
     &              speed2.gt.2.0*speed1)) ierds = ierds +1
              endif
            endif
          else
            head2  = -1.0
            speed2 = -1.0
          endif
!
!                   see if an error was found
!
          if (ier1.gt.0 .or. ier2.gt.0) ierr = ierr +1
!
        endif
        slt    = elt
        sln    = eln
        head1  = head2
        speed1 = speed2
        ier1   = ier2
      enddo
      end
      subroutine dtrhrs (clin1,clin2,hours)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  dtrhrs
!
!  DESCRIPTION:  determine hours between clin1 and clin2
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
!  USAGE:  call dtrhrs (clin1,clin2,hours)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ---------------------------
!    clin1           char*240       input    line of TAU summary
!    clin2           char*240       input    line of TAU summary
!    hours           real           output   hours between TAU's
!
!  COMMON BLOCK:  none
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
!        Name        Type                 Description
!       ------       ----       -----------------------------------------
!       hr1          real       hour from first  character string
!       hr2          real       hour from second character string
!
!  METHOD:  N/A
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
      character*240 clin1, clin2
      real hours
!
!         local variables
      real hr1, hr2
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      read (clin1(2:4),'(f3.0)') hr1
      read (clin2(2:4),'(f3.0)') hr2
      hours = hr2 -hr1
      end
      subroutine exltln (cline,ilt,jln,rlt,rln)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  exltln
!
!  DESCRIPTION:  extract latitude and longitude from TAU lines
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
!  USAGE:  call exltln (cline,ilt,jln,rlt,rln)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ---------------------------
!    cline           char*240       input    line of TAU summary
!    ilt             int            output   latitude  times 10 (deg)
!    jlt             int            output   longitude times 10 (deg)
!    rlt             real           output   latitude  (deg)  -South
!    rlt             real           output   longitude (deg - EAST)
!
!  COMMON BLOCK:  none
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
!  METHOD:  N/A
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
      integer ilt, jln
      character*240 cline
      real rlt, rln
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   obtain values as integer times 10
!
      read (cline(6:8),'(i3)') ilt
      read (cline(11:14),'(i4)') jln
!
!                   obtain, then modifiy real values as required
!
      read (cline(6:8),'(f3.1)') rlt
!                   return negative for Southern Hemisphere
      if (cline(9:9) .eq. 'S') rlt = -rlt
      read (cline(11:14),'(f4.1)') rln
!                   return longitude as degrees East
      if (cline(15:15) .eq. 'W') rln = 360.0 -rln
      end
      subroutine filerd (cwsum,nlmax,lkont,ioe)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  filerd
!
!  DESCRIPTION:  read tropical cyclone warning summary from flat-file
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
!  USAGE:  call filerd (cwsum,nlmax,lkont,ioe)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsum           char*240       output   warning summary
!    ioe             integer        output   I/O error flag
!    lkont           integer        output   number of lines read
!    nlmax           integer        input    max number of lines
!
!  COMMON BLOCKS:  none
!
!  FILES:
!       Name     Unit    Type    Attribute   Usage       Description
!    ---------   ----  --------  ---------  -------  ------------------
!     warnsum     10    local    sequential  input   warning summary
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     I/O error                set error flag and exit
!     missing ending line      set error flag and exit
!
!  ADDITIONAL COMMENTS:
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         lftuppr     left justify, upper case and screen data
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cline      char*240   working character string
!         cx         char*1     working character
!         j          integer    character index
!         m          integer    working line count
!         nk         integer    number of "good" characters
!
!  METHOD:  1)  read one line at a time
!           2)  screen characters, upper case and left jusftify
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
      integer nlmax, lkont, ioe
      character*240 cwsum(nlmax)
!
!         local variables
      integer j, k, m, n, nk
      character*1 cx
      character*240 cline
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      m = 0
      do n=1, nlmax
        cline = ' '
        read (10,'(a240)',iostat=ioe,end=200) cline
        j = 0
!
!                   screen input for valid characters
!
        do k=1, 240
          cx = cline(k:k)
cx   allow odd characters in the name... sampson nrl 07/27/01
          if (cx.eq.' ' .or. (cx.ge.'A' .and. cx.le.'Z') .or. (cx.ge.'0'&
     &      .and. cx.le.'9') .or. (cx.ge.'a' .and. cx.le.'z') .or. 
     &      (cx.eq.'-') ) then
            if (j .eq. 0) m = m +1
            j = j +1
            cwsum(m)(j:j) = cx
          endif
        enddo
        if (m .gt. 0) then
          call lftuppr (cwsum(m),nk)
          if (nk .eq. 0) m = m -1
          if (cwsum(m)(1:4) .eq. 'NNNN') goto 200
!
        endif
      enddo
  200 continue
      lkont = m
      if (m .gt. 0) then
        if (cwsum(m)(1:4) .eq. 'NNNN') then
          ioe = 0
        else
          write (*,*) 'WARNING, NNNN not found - filerd'
          ioe = 1
        endif
      else
        ioe = -99
      endif
      end
      subroutine fnddnabp (dna,maxdna,lk)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  fnddnabp
!
!  DESCRIPTION:  find next blank in dna, then increment index by one
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
!  USAGE:  call fnddnabp (dna,maxdna,lk)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    dna             char*8         input    array of dna lines
!    lk              integer        in/out   starting index for search,
!                                            location of next non-blank
!                                            -1 if no more data on line
!    maxdna          integer        input    max number of lines
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
      integer maxdna, lk
      character dna(maxdna)*8
!
!         local variable
      integer l
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do l=lk, maxdna
        if (dna(l)(4:4) .eq. 'b') then
          lk = l +1
          if (lk .gt. maxdna) lk = -1
          goto 200
!
        endif
      enddo
      lk = -1
  200 continue
      end
      subroutine headck (cwsum,dna,numdna,csdtg,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  headck
!
!  DESCRIPTION:  check heading line of summary for errors
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
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call headck (cwsum,dna,numdna,csdtg,ierr)
!
!  PARAMETERS:
!       Name           Type        Usage             Description
!    ----------     ----------    -------   ----------------------------
!    csdtg          char*10       input     computer synoptic watch time
!    cwsum          char*240      in/out    header line of summary
!    dna            char*8        input     array of dna lines of cwsum
!    ierr           integer       output    error flag, 0 - no error
!    numdna         integer       input     number of dna lines in dna
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
!     -----------------   ------------------------------------------
!    bad data in header   mark each bad digit with an 'X' and alpha
!                         with a 'Y', and increment error flag
!
!  ADDITIONAL COMMENTS:
!
!        Symbolic example of first line of summary, with column numbers
!
!                 1         2         3         4
!        123456789012345678901234567890123456789012345.............
!        YYYYMMDDHH IDB NAME       WNRA NC DEG KT METH ---- ACC
! group:     1       2   3          4    5  6   7  8
!
!                  Explanation of symbols, left to right
!
!      YYYYMMDDHH - DATE-TIME-GROUP of initial position
!             IDB - CYCLONE IDENTIFICATION, number and origin basin
!            NAME - NAME or "NONAME" of tropical cyclone
!            WNRA - WARNING NUMBER - three digits and a character,
!                   this charcater may be a blank character
!              NC - NUMBER OF TROPICAL CYCLONES in present basin
!             DEG - TRACK OF CYCLONE last six hours, degrees
!              KT - SPEED OF CYCLONE last six hours, kts
!            METH - METHODS OF LOCATION, four characters for each method
!                     SATL - satellite
!                     RADR - radar
!                     SYNP - synoptic data
!                     AIRC - aircarft
!                     XTRP - extrapolation
!                     OTHR - other
!            ---- - more than one method may be specified
!             ACC - ACCURACY of initial position, nm
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         fnddnabp    find dna line of next blank, then increment by one
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cline      char*240   working character string
!         cmdtg      char*10    message dtg of initial position
!         ier1       integer    first  error flag for dtgmod
!         ier2       integer    second error flag for dtgmod
!         ks         integer    starting character index
!         kt         integer    ending character index
!         lk         integer    line count for dna of string
!         ls         integer    character index reference
!         na         integer    accuracy indicator
!         nf         integer    method of fix indicator
!         num        integer    number converted from character string
!
!  METHOD:  1)  Use fnddnabp to parse the whole character string of the
!               header into "dna" lines.
!           2)  Go dna line by dna line to error check the header data
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
!  sampson  12/23/96   Enable storm numbers up to 79
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer numdna, ierr
      character cwsum*240, csdtg*10, dna(numdna)*8
!
!         local variables
      character*10 cmdtg, pdtg, fdtg
      character cline*240
      integer ks, kt, ls, lk, nerr, num, nf, na
      integer imhr, iphr, ier1, ier2
!
      data imhr/-6/, iphr/12/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr  =  0
      cline = cwsum
      cwsum = ' '
!
!                  load cwsum with valid values from cline or
!                  missing flags and increment the error flag
!
!                   check for valid dtg, group 1 data
!
cx    if (dna(1)(4:4).eq.'d' .and. dna(1)(5:7).eq.'010') then
!
!                   check that summary is within time window
!
cx      cmdtg = cline(1:10)
!
!                   obtain minimum allowed dtg, pdtg
!
cx      call dtgmod (csdtg,imhr,pdtg,ier1)
!
!                   obtain maximum allowed dtg, fdtg
!
cx      call dtgmod (csdtg,iphr,fdtg,ier2)
cx      if (ier1.eq.0 .and. ier2.eq.0) then
!
!                   check that cmdtg is within specified range of dtg
!
cx        if (cmdtg.lt.pdtg .or. cmdtg.gt.fdtg) then
cx          ierr = -1
cx          goto 900
!
cx        endif
cx      else
cx        write (*,*) 'ERROR, bad dtg is ',cmdtg
cx        cline(1:10) = 'XXXXXXXXXX'
cx        dna(1)(4:4) = 'a'
cx        ierr = 1
cx      endif
cx    else
cx      ierr = 1
cx    endif
      cwsum(1:10) = cline(1:10)
!
!                   find start of group 2 data
!
      lk = 1
      call fnddnabp (dna,numdna,lk)
 9001 format (a1)
 9002 format (i2)
 9003 format (i3)
!
!                   check on cyclone number & basin, group 2 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'002') then
        read (dna(lk)(1:3),9003) ks
        read (cline(ks:ks+1),9002) num
!
!                   check for valid number
!
        if (num.eq.0 .or. num.gt.79) then
!
!                   valid warning numbers are from 01 through 79,
!                   (used to be 01-50, bs)
!                   an 8n warning is a possible exercise
!
          if (cline(ks:ks) .ne. '8') then
            ierr = -1
            goto 900
!
          else
            cline(ks:ks) = 'X'
            ierr = ierr +1
          endif
        endif
        cwsum(12:13) = cline(ks:ks+1)
      else
        cwsum(12:13) = 'XX'
        ierr = ierr +1
      endif
!
!                   check for valid origin basin indicator
!
      if (dna(lk+1)(4:4) .eq. 'a') then
        read (dna(lk+1)(1:3),9003) ks
        cwsum(14:14) = cline(ks:ks)                                      &
      else
        cwsum(14:14) = 'Y'
        ierr = ierr +1
      endif
!
      call fnddnabp (dna,numdna,lk)
!
!                   check for "valid" name, group 3 data
!
      if (dna(lk)(4:4).ne.'a' .or. dna(lk)(5:7).le.'001') then
        cwsum(16:18) = 'YYY'
        ierr = ierr +1
      else
        read (dna(lk)(1:3),9003) ks
        read (dna(lk)(5:7),9003) num
        num = min0 (num,10)
        kt  = ks +num -1
        cwsum(16:25) = cline(ks:kt)
      endif
!
      call fnddnabp (dna,numdna,lk)
!
!                   check warning number, group 4 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'003') then
        read (dna(lk)(1:3),9003) ks
        cwsum(27:29) = cline(ks:ks+2)
      else
        cwsum(27:29) = 'XXX'
        ierr = ierr +1
      endif
!
!                   note: amendment may or may not exist, it will not
!                   exist on the first warning for this dtg
!
      if (dna(lk+1)(4:4) .eq. 'a') then
        read (dna(lk+1)(1:3),9003) ks
        cwsum(30:30) = cline(ks:ks)
      endif
!
      call fnddnabp (dna,numdna,lk)
!
!                   check number of warnings in basin, group 5
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'002') then
        read (dna(lk)(1:3),9003) ks
        cwsum(32:33) = cline(ks:ks+1)
        if (cwsum(32:33) .eq. '00') cwsum(32:33) = '01'
      else
        cline(32:33) = 'XX'
        ierr = ierr +1
      endif
!
      call fnddnabp (dna,numdna,lk)
!
!                   check heading of cyclone, group 6 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'003') then
        read (dna(lk)(1:3),9003) ks
        read (cline(ks:ks+2),9003) num
        if (num .le. 360) then
          cwsum(35:37) = cline(ks:ks+2)
        else
          cwsum(35:37) = 'XXX'
          ierr = ierr +1
        endif
      else
        cwsum(35:37) = 'XXX'
        ierr = ierr +1
      endif
!
      call fnddnabp (dna,numdna,lk)
!
!                   check speed of movement of cyclone, group 7 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'002') then
        read (dna(lk)(1:3),9003) ks
        read (cline(ks:ks+1),9002) num
        if (num .le. 70) then
          cwsum(39:40) = cline(ks:ks+1)
        else
          cwsum(39:40) = 'XX'
          ierr = ierr +1
        endif
      else
        cwsum(39:40) = 'XX'
        ierr = ierr +1
      endif
!
      nf = 0
      na = 0
      ls = 40
  200 continue
!
!                   top of internal loop for type group 8 & 9 data
!
      call fnddnabp (dna,numdna,lk)
      if (lk .gt. 0) then
!
!                   check method of "fix" of cyclone, group 8 data
!                   there may be more than one group 8 data
!
        if (dna(lk)(4:4).eq.'a' .and. dna(lk)(5:7).eq.'004') then
          read (dna(lk)(1:3),9003) ks
          cwsum(ls+2:ls+5) = cline(ks:ks+3)
          ls = ls +5
          nf = nf +1
          goto 200
!
        elseif (dna(lk)(4:4) .eq. 'a') then
          cwsum(ls+2:ls+5) = 'YYYY'
          ls = ls +5
          goto 200
!
        elseif (dna(lk)(4:4) .eq. 'd') then
!
!                     check for accuracy of method of "fix"
!
          if (dna(lk)(5:7) .eq. '003') then
            read (dna(lk)(1:3),9003) ks
            cwsum(ls+2:ls+4) = cline(ks:ks+2)
            na = 1
          else
            cwsum(ls+2:ls+4) = 'XXX'
            na   = 1
            ierr = ierr +1
          endif
        endif
      endif
      if (nf.eq.0 .and. na.eq.0) then
        cwsum(42:49) = 'YYYY XXX'
        ierr = ierr +2
      elseif (nf .eq. 0) then
        cline = ' '
        cline(47:49) = cwsum(42:44)
        cwsum(42:45) = 'YYYY'
        cwsum(47:49) = cline(47:49)
        ierr = ierr +1
      elseif (na .eq. 0) then
        cwsum(ls+2:ls+4) = 'XXX'
        ierr = ierr +1
      endif
  900 continue
      if (cwsum .eq. ' ') cwsum = cline 
      end
      subroutine lftuppr (card,nk)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  lftuppr
!
!  DESCRIPTION:  left justify, remove consecutive blanks and all
!                non-alpha/numeric characters, and put in upper case
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
!  USAGE:  call lftuppr (card,nk)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    card            char*240       in/out   working string
!    nk              integer        output   good character count
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
!  ADDITIONAL COMMENTS:  none
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       ----------------------------------------
!         cl         char*1     last character loaded
!         cline      char*240   working string
!         cx         char*1     character under evaluation
!         iaoff      integer    offset between lower case and upper case
!         inil       integer    flag for initialze iaoff
!         k          integer    character position
!         keep       integer    keep (-1) or no keep (0)
!         kk         integer    character position
!
!  METHOD:  Load cline with good data, character by character, then
!           back load into card.
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
      integer nk
      character*240 card
!
!         local variables
      integer inil, iaoff, k, keep, kk
      character cx*1, cl*1, cline*240
!
      save inil, iaoff
!
      data inil/0/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      if (inil .eq. 0) then
        inil = -1
!                   establish offset for upper case
        iaoff = ichar('a') -ichar('A')
      endif
!
      nk    =  0
      cline = ' '
      keep  =  0
      do k=1, 240
        cl = card(k:k)
        if (cl .ne. ' ') then
!
!                   left justify values and screen data
!
          if ((cl.ge.'A' .and. cl.le.'Z') .or. cl.eq.'-') then
            keep = -1
          elseif (cl.ge.'0' .and. cl.le.'9') then
            keep = -1
          elseif (cl.ge.'a' .and. cl.le.'z') then
!                   put cl in upper case
            cl   = char (ichar (card(k:k)) -iaoff)
            keep = -1
          endif
          if (keep .ne. 0) then
!
!                   load first character
!
            cline(1:1) = cl
            nk = 1
!
!                   remove consecutive blanks and screen data
!
            do kk=k+1, 240
              cx = card(kk:kk)
cx       allow "-" too sampson, nrl 7/27/01
              if ((cx.ge.'A' .and. cx.le.'Z') .or. cx.eq.'-') then
                keep = -1
              elseif (cx.ge.'0' .and. cx.le.'9') then
                keep = -1
              elseif (cx.ge.'a' .and. cx.le.'z') then
!                       put cx in upper case
                cx   = char (ichar (card(k:k)) -iaoff)
                keep = -1
              else
                keep = 0
              endif
              if (keep.ne.0 .or. (cl.ne.' ' .and. cx.eq.' ')) then
                nk = nk +1
                cline(nk:nk) = cx
                cl = cx
              endif
            enddo
            goto 200
!
          endif
        endif
      enddo
  200 continue
      card = cline
      return
!
      end
      subroutine nnnnck (cwsum,ierr,cwsnnn)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  nnnnck
!
!  DESCRIPTION:  check NNNN line and write ierr after NE flag
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
!  USAGE:  call nnnnck (cwsum,ierr,cwsnnn)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsnnn          char*240       in/out   NNNN  line of summary
!    cwsum           char*240       input    first line of summary
!    ierr            integer        input    line error count
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
!         Example of analysis time on cwsum(1):
!            1         2         3         4         5
!   12345678901234567890123456789012345678901234567890
!   YYYYMMDDHH
!
!            1         2         3         4         5
!   12345678901234567890123456789012345678901234567890
!   NNNN ORIG YYYYMMDDHHmm YYYYMMDDHHmmss CIR NEec
!             123456789012 12345678901234
!                 tx            rx
!   where:
!               NNNN - end of summary indicator
!               ORIG - origin code: JTWC, NWOC, NEOC, etc
!       YYYYMMDDHHmm - message dtg (transmit time)
!     YYYYMMDDHHnnss - arrival dtg
!                CIR - circuit code: AWN, AUT, DDN
!                 NE - number of errors flag
!                 ec - error count
!
!   NOTE: S/R dbwrit will put "cyc_id NOT ALLOWED" in columns (48:65)
!         when cyclone ID is not allowed
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name                  Description
!    -------------       -----------------------------------------
!    date_and_time       f90 system time routine
!           dtgmod       UUG utility - modify dtg by +/- hours
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!            cet     char       estimated dtg
!            cpt     char       analysis positione dtg
!            crx     char       recipt dtg
!            ctx     char       transmit dtg
!           date     char       YYYYMMDD
!        ivalues      int       date_and_time values - not used
!             n1      int       1
!             n2      int       2
!            n10      int       10
!            n12      int       12
!            nxy      int       sum of "X" and "Y" in character string
!           time     char       mmss.ss
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
!                       sampson, nrl              Oct 92
!                        disabled date_and_time, dtgmod
!..............................END PROLOGUE.............................
!
      implicit none
!
!         formal parameters
      integer ierr
      character*240 cwsum, cwsnnn
!
!         local variables
      integer n, n1, n2, n10, n12, nxy
      integer ivalues(8)
      character zone*5, date*8, time*10
      character cpt*10, cet*12, ctx*12, crx*14
!
      data n1/1/, n2/2/, n10/10/, n12/12/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   check on origin
!
      if (cwsnnn(6:9) .eq. ' ') cwsnnn(6:9) = 'UNKN'
!
!                   check on transmit and receipt times
!
      cpt = cwsum(1:10)
      call chkxy (cpt,n1,n10,nxy)
      if (nxy .ne. 0) cpt = ' '
      crx = cwsnnn(11:22)
      call chkxy (crx,n1,n12,nxy)
      if (nxy .ne. 0) then
cx      call date_and_time (date,time,zone,ivalues)
        crx = date // time(1:6)
!
!                   load estimated receipt time
!
        cwsnnn(11:22) = crx
      endif
      ctx = cwsnnn(24:35)
      call chkxy (ctx,n1,n12,nxy)
      if (nxy .ne. 0) then
!
!                   load estimated transmit time
!
        if (cpt .ne. ' ') then
!
!                   estimate transmit time as analysis position time +2 hr
!                   with minutes of 03
!
          cet = ' '
cx        call dtgmod (cpt,n2,cet)
          do n=1, 10
            if(ctx(n:n).lt.'0' .or. ctx(n:n).gt.'9') ctx(n:n) = cet(n:n)
          enddo
          if (ctx(11:11).lt.'0' .or. ctx(11:11).gt.'9') ctx(11:11) = '0'
          if (ctx(12:12).lt.'0' .or. ctx(12:12).gt.'9') ctx(12:12) = '3'
        else
          do n=1, 12
            if(ctx(n:n).lt.'0' .or. ctx(n:n).gt.'9') ctx(n:n) = crx(n:n)
          enddo
          if (ctx .ge. crx) then
!
!                   decrease estimate by 1 hour
!
            cpt = ' '
cx          call dtgmod (crx,-n1,cpt)
            ctx(1:10) = cpt
          endif
        endif
        cwsnnn(24:35) = ctx
      endif
!
!                   check on circuit of transmission
!
      if (cwsnnn(39:41) .eq. ' ') cwsnnn(39:41) = 'UNK'
!
!                   inform QC of error count
!
      if (cwsnnn(43:44) .eq. ' ') cwsnnn(43:44) = 'NE'
      ierr = min0 (99,ierr)
!
!                   load number of process errors found
!
      write (cwsnnn(45:46),'(I2.2)') ierr
      end
      subroutine numchk (cline,ks,kt,num,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  numchk
!
!  DESCRIPTION:  check for digits, ks thru kt in cline
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
!  RESTRICTIONS:  digits must represent a positive integer and
!                 digit count must be 1, 2, 3 or 10
!
!  COMPUTER/OPERATING SYSTEM DEPENDENCIES:
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  call numchk (cline,ks,kt,num,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ---------------------------
!    cline           char*240       input    character string
!    ierr            integer        output   error flag, 0 no error
!    ks              integer        input    starting character position
!    kt              integer        input    ending character position
!    num             integer        output   >= 0 - good number
!                                             < 0 - bad number
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
!     character index wrong    set error flag and return
!     outside resrictions      set error flag and return
!     not all digits           set error flag and return
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
      integer ks, kt, num, ierr
      character cline*240
!
!         local variable
      integer k
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr = 0
      if (ks.lt.1 .or. ks.gt.240) ierr = -1
      if (kt.lt.1 .or. kt.gt.240) ierr = -1
      if (ks .gt. kt) ierr = -1
      if (ierr .eq. 0) then
        do k=ks, kt
          if (cline(k:k).lt.'0' .or. cline(k:k).gt.'9') ierr = ierr +1
        enddo
        if (ierr .eq. 0) then
          if (kt -ks .eq. 0) then
            read (cline(ks:kt),'(i1)') num
          elseif (kt -ks .eq. 1) then
            read (cline(ks:kt),'(i2.2)') num
          elseif (kt -ks .eq. 2) then
            read (cline(ks:kt),'(i3.3)') num
          elseif (kt -ks .eq. 9) then
            read (cline(ks:kt),'(i10.10)') num
          else
            num = -99
          endif
        else
          num = -1
        endif
      else
        num = -999
      endif
      end
      subroutine tauampxck (cwsum,nl,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  tauampxck
!
!  DESCRIPTION:  cross check TAU line with match AMP line when "?"
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
!  USAGE:  call tauampxck (cwsum,nl,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsum           char*240       in/out   array of summay lines
!    ierr            integer        in/out   error flag, 0 - no error
!    nl              integer        input    number of lines in cwsum
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
!         CONDITION                     ACTION
!     -----------------            ----------------------------
!     missing radius description   add missing data indicators to
!     w/o matching AMP line        summary line and increment ierr
!
!  ADDITIONAL COMMENTS:
!     For unknown reasons, a tropical center can forecast the location
!     of a cyclone that becomes extratropical, but cannot forecast
!     the radius of the associated winds.  Likewise, JTWC does not
!     forecast wind speeds over land.
!
!     Therefore, it is possible that the last one or two forecast lines
!     may have high enough wind speeds that would otherwise require
!     radius descriptors.  If these radius descriptors are absent,
!     tauchk will signal this with one or two "?" on the offending TAU
!     line.  If there is an AMP for this time, the missing description
!     is not considered an error by this software.
!
!     If this approach does not work, we can scan the AMP line for
!     possible key words to determine if there is no error.
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         nas        integer    first line of AMP section
!         nat        integer    last line of AMP section
!
!  METHOD:  1)  Look for ? in TAU line, if found tauchk said there is a
!               missing radius description if there is not a matching
!               AMP line for this same position time.
!           2)  If ? found, look for matching AMP line:
!               a) if match found, remove ?
!               b) if no match found, signal missing data in summary
!                  line.  Do twice if two ?? are present.
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
      integer nl, ierr
      character*240 cwsum(nl)
!
!         local variables
      integer j, k, n, nas, nat

      j = 0
      k = 0
      n = 0
      nas = 0
      nat = 0
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      do n=3, nl
!                   find first AMP line in summary
        if (cwsum(n)(1:1) .eq. 'A') then
          nas = n
!                     find SER line in summary
          do j=n+1, nl
            if (cwsum(j)(1:1) .eq. 'S') then
!                       set nat to last AMP line in summary
              nat = j -1
              goto 200
!
            endif
          enddo
        endif
      enddo
!
!                   resolve if radius data is missing from TAU line
!
  200 continue
      do n=2, nas -1
        if (cwsum(n)(1:1) .eq. 'T') then
!
!                     look for TAU line with "?"
!
          do k=21, 239
            if (cwsum(n)(k:k) .eq. '?') then
!
!                       look for matching AMP line to TAU line
!
              do j=nas, nat
                if (cwsum(j)(5:7) .eq. cwsum(n)(2:4)) then
!
!                         have match, so remove "?" and/or "??"
!
                  cwsum(n)(k:k+1) = '  '
                  goto 210
!
                endif
              enddo
!
!                       no match found, so indicate missing data
!
              if (cwsum(n)(k+1:k+1) .eq. ' ') then
!                         only one ?, so add only one missing set
                cwsum(n)(k:k+7) = 'RXXX XXX'
              else
!                         two ?, so indicate that two are missing
                cwsum(n)(k:k+16) = 'RXXX XXX RXXX XXX'
              endif
!                     signal an error on this line
              ierr = ierr + 1
              goto 210
!
            elseif (cwsum(n)(k:k) .eq. ' ') then
!                   adjacent blanks indicate end of data on this line
              if (cwsum(n)(k+1:k+1) .eq. ' ') goto 210
!
            endif
          enddo
        endif
  210   continue
      enddo
      end
      subroutine tauchk (cwsum,dna,numdna,nq,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  tauchk
!
!  DESCRIPTION:  check the TAU lines, initial position and forecasts
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
!  USAGE:  call tauchk (cwsum,dna,numdna,nq,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cwsum           char*240       in/out   TAU line of summary
!    dna             char*8         input    array of dna lines
!    ierr            integer        output   error flag, 0 - no error
!    nq              integer        in/out   number of '?' placed in TAU
!                                            lines by this S/R
!    numdna          integer        input    number of dna lines
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
!    -----------------   ---------------------------------------------
!    bad data in line     mark each bad digit with an 'X' and alpha
!                         with a 'Y', and increment error flag
!    possible omission    add '?' on line and increment nq for further
!                         checking by another S/R
!
!  ADDITIONAL COMMENTS:
!
!     Symbolic example of position line in summary, with column numbers
!
!                 1         2         3         4
!        1234567890123456789012345678901234567890123...............
!        THHH LAT  LON   MXW RSPD NMI DD ---
! group   1    2    3     4   5    6   7 ....
!
!                  Explanation of symbols, left to right
!
!          T - T is flag for TAU of position, hrs
!        HHH - hours of position 000 - 072 -> expansion
!        LAT - LATITUDE  and N or S for hemisphere, degrees and tenths
!        LON - LONGITUDE and E OR W for hemisphere, degrees and tenths
!        MXW - MAXIMUM SUSTAINED WIND SPEED, kts
!       RSPD - R is a flag for radius and SPD is wind speed, in kts
!        NMI - RADIUS in nm of SPD winds
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
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          Name           Description
!         -------     ----------------------
!         fnddnabp    find next dna line that is not blank
!         numchk      check that character string is all digits
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cline      char*240   working string of summary line
!         iern       integer    error flag from numchk, 0 - no error
!         k          integer    location in character string
!         ks         integer    starting location in working string
!         lk         integer    line count in dna array
!         nr         integer    number of radius descriptions
!         ns         integer    starting location in output string
!         nt         integer    ending location in output string
!         num        integer    integer number from character digits
!
!  METHOD:  1)  Use fnddnabp to parse the whole character string of the
!               position line into "dna" lines.
!           2)  Go dna line by dna line to error check the position data
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
      integer ierr, numdna
      character*240 cwsum, dna(numdna)*8
!
!         local variables
      integer k, ks, n, nr, ns, nt, nq, lk, num, iern
      character*240 cline
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr       =  0
      nr         =  0
      ns         = 19
      cline      = cwsum
      cwsum      = ' '
      cwsum(1:1) = 'T'
!
!                  load cwsum with valid values from cline or
!                  missing flags and increment the error flag
!
      if (dna(2)(4:4).eq.'d' .and. dna(2)(5:7).eq.'003') then
        cwsum(2:4) = cline(2:4)
      else
        cwsum(2:4) = 'XXX'
        ierr = 1
      endif
!
!                   find start of group 2 data
!
      lk = 1
      call fnddnabp (dna,numdna,lk)
 9003 format (i3)
!
!                   check on latitude, group 2 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'003') then
        read (dna(lk)(1:3),9003) ks
        cwsum(6:8) = cline(ks:ks+2)
      else
        cwsum(6:8) = 'XXX'
        ierr = ierr +1
      endif
      if (dna(lk+1)(4:4) .eq. 'a') then
        read (dna(lk+1)(1:3),9003) ks
        cwsum(9:9) = cline(ks:ks)
      else
        cwsum(10:10) = 'Y'
      endif
      if (cwsum(10:10) .eq. 'Y') ierr = ierr +1
!
!                   find start of group 3 data
!
      call fnddnabp (dna,numdna,lk)
!
!                   check on longitude, group 3 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'004') then
        read (dna(lk)(1:3),9003) ks
        cwsum(11:14) = cline(ks:ks+3)
      else
        cwsum(11:14) = 'XXXX'
        ierr = ierr +1
      endif
      if (dna(lk+1)(4:4) .eq. 'a') then
        read (dna(lk+1)(1:3),9003) ks
        cwsum(15:15) = cline(ks:ks)
      else
        cwsum(15:15) = 'Y'
      endif
      if (cwsum(15:15) .eq. 'Y') ierr = ierr +1
!
!                   find start of group 4 data
!
      call fnddnabp (dna,numdna,lk)
!
!                   check on maximum wind speed, group 4 data
!
      if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'003') then
        read (dna(lk)(1:3),9003) ks
        cwsum(17:19) = cline(ks:ks+2)
        if (cwsum(17:19) .gt. '050') then
!                   set expected radius descriptions to 2
          nr = 2
        elseif (cwsum(17:19) .gt. '035') then
!                   set expected radius descriptions to 1
          nr = 1
        endif
      else
        cwsum(17:19) = 'XXX'
        ierr = ierr +1
      endif
      nt = 20
!
!                   finished with minimum amount of data
!                   find start of next group of data, if it exists
!
!
      call fnddnabp (dna,numdna,lk)
      if (lk .lt. 1) goto 400
!
!                   top of outer internal loop
!
  200 continue
      if (dna(lk)(4:4).eq.'a' .and. dna(lk)(5:7).eq.'001') then
        ns = nt +1
        read (dna(lk)(1:3),9003) ks
        cwsum(ns:ns) = cline(ks:ks)
!
!                   top of inner internal loop
!
  300   continue
        if (cwsum(ns:ns) .eq. 'R') then
!
!                   obtain wind speed for radius info to follow
!
          nr = nr -1
          ns = ns +1
          if (dna(lk+1)(4:4).eq.'d' .and. dna(lk+1)(5:7).eq.'003') then
            read (dna(lk+1)(1:3),9003) ks
            cwsum(ns:ns+2) = cline(ks:ks+2)
          else
            cwsum(ns:ns+2) = 'XXX'
            ierr = ierr +1
          endif
          nt = ns +3
!
!                   find next group of data, radius in nm
!
          call fnddnabp (dna,numdna,lk)
!
!                   obtain radius in nm
!
          ns = nt +1
!
!                   top of inner most internal loop
!
  350     continue
          if (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'003') then
            read (dna(lk)(1:3),9003) ks
            cwsum(ns:ns+2) = cline(ks:ks+2)
          else
            cwsum(ns:ns+2) = 'XXX'
            ierr = ierr +1
          endif
          nt = ns +3
!
!                   obtain descriptions
!
          do n=1, 5
!
!                     obtain index to next group of data
!
            call fnddnabp (dna,numdna,lk)
            if (lk .lt. 1) goto 400
!
            ns  = nt +1
            if (dna(lk)(4:4).eq.'a' .and. dna(lk)(5:7).eq.'002') then
              read (dna(lk)(1:3),9003) ks
              cwsum(ns:ns+1) = cline(ks:ks+1)
              nt = nt +3
            elseif (dna(lk)(4:4).eq.'d' .and. dna(lk)(5:7).eq.'003')    &
     &        then
              goto 350
!
            elseif (dna(lk)(4:4).eq.'a' .and. dna(lk)(5:7).eq.'001')    &
     &        then
              goto 200
!
            elseif (dna(lk)(5:7) .eq. '002') then
              cwsum(ns:ns+1) = 'YY'
            elseif (dna(lk)(5:7) .eq. '003') then
              cwsum(ns:ns+2) = 'XXX'
            endif
          enddo
        else
          if (dna(lk+1)(4:4).eq.'d' .and. dna(lk+1)(5:7).eq.'003') then
            cwsum(ns:ns) = 'R'
            goto 300
!
          endif
        endif
      else
        ns = nt +1
        cwsum(ns:ns) = 'Y'
        ns = ns +1
        cwsum(ns:ns+2) = 'XXX'
        ns = ns +4
        cwsum(ns:ns+2) = 'XXX'
      endif
  400 continue
!
!                   double check radius data
!
      ks = 21
!
!                   top of internal loop
!
  410 continue
      do k=ks, 233
        if (cwsum(k:k) .eq. 'R') then
          if (cwsum(k+5:k+7) .eq. '   ') then
            cwsum(k+5:k+7) =  'XXX'
            ierr = ierr +1
          elseif (cwsum(k+5:k+7) .ne. 'XXX') then
            call numchk (cwsum,k+5,k+7,num,iern)
cx  Change as per Harry Hamilton 7/16/97  ... bs
cx          if (num.lt.1 .or. iern.ne.0) then
            if (num.lt.0 .or. iern.ne.0) then
              cline = ' '
              cline(k+5:240) = cwsum(k+5:240)
              cwsum(k+5:240) = ' '
              cwsum(k+5:k+7) = 'XXX'
              cwsum(k+9:240) = cline(k+5:236)
              ierr = ierr +1
            endif
          endif
          ks = k +9
          goto 410
!
        elseif (cwsum(k-1:k-1).eq.' ' .and. cwsum(k:k).eq.' ') then
!
!                   double blank is end of data signal
!
          goto 420
!
        endif
      enddo
  420 continue
      if (nr .gt. 0) then
!
!                   not all expected radius data was found
!
        ns = max0 (nt +1,ns +2)
        cwsum(ns:ns) = '?'
        if (nr .gt. 1) cwsum(ns+1:ns+1) = '?'
        nq = nq +1
      endif
      end
      subroutine xtrcdna (cline,dna,maxdna,ndnal,ierr)
!
!.............................START PROLOGUE............................
!
!  SCCS IDENTIFICATION:  %W% %G%
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  xtrcdna
!
!  DESCRIPTION:  extract dna of character string
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
!  USAGE:  call xtrcdna (cline,dna,maxdna,nadb,ierr)
!
!  PARAMETERS:
!       Name            Type         Usage            Description
!    ----------      ----------     -------  ----------------------------
!    cline           char*240       input    character string
!    dna             char*8         output   array of dna lines
!    ierr            integer        output   error flag, 0 no error
!    maxdna          integer        input    max allowed dna lines
!    ndnal           integer        output   number of dna lines found
!
!  COMMON BLOCKS:  none
!
!  FILES:  noe
!
!  DATA BASES:  none
!
!  NON-FILE INPUT/OUTPUT:  none
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     type 4 data              set error flag and continue
!     too many dna lines       set error flag and exit
!
!  ADDITIONAL COMMENTS:
!
!  format of dna line:
!
!     12345678
!     sssteee
!  where:
!    sss - starting character position in string of new character type
!      t - type of characters:
!             a - alpha
!             b - blank
!             d - digits
!             o - other - this should not occur with prior screening
!    eee - count of same adjacent character type
!
!....................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          Name      Type                 Description
!         ------     ----       -----------------------------------------
!         cx         char*1     working character
!         k          integer    string index
!         kk         integer    character change type flag
!         ks         integer    starting character position in string
!         n          integer    line of dna being loaded
!         nk         integer    sum of same adjacent characters
!         nt         integer    character type
!
!  METHOD: classify each group of adjacent characters of the same type
!          as a dna line of the string.  Use four data types.
!              type       contents
!               1         all alpha - pre-screening puts in upper case
!               2         all digits
!               3         all blanks
!               4         all other types of characters - pre-screening
!                         has removed all these types
!
!          see additional comments for format of dna line
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  f77 with f90 options or f90
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
      integer maxdna, ndnal, ierr
      character*8 dna(maxdna)
      character*240 cline
!
      integer n, nk, nt, k, ks, kk
      character*1 cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ierr = 0
      n    = 0
      ks   = 1
!
!                   top of internal processing loop
!
  100 continue
      do k=ks, 240
        cx = cline(k:k)
        if (k .eq. ks) then
!
!                   start sum of character type of new set
!
          nk = 1
          kk = 0
          n  = n +1
          if (n .le. maxdna) then
            dna(n) = ' '
!
!                   determine character type of new set and load
!                   type indicater at position 4 in dna line
!
            if ( (cx.ge.'A' .and. cx.le.'Z') ) then
!                     alpha data type = 1
              nt = 1
              dna(n)(4:4) = 'a'
cx       allow "-" in acceptable characters ..... sampson nrl 7/27/01
            elseif (cx.eq.'-') then
              nt = 1
              dna(n)(4:4) = 'a'
	      write(*,*) 'dash in cx, assigned dna:', dna
            elseif (cx.ge.'0' .and. cx.le.'9') then
!                     digit data type = 2
              nt = 2
              dna(n)(4:4) = 'd'
            elseif  (cx .eq. ' ') then
!                     blank data type = 3
              nt = 3
              dna(n)(4:4) = 'b'
            else
!                     other data type = 4   {this should not occur}
              write (*,*) 'invlaid data type in string found by xtrcdna'
              nt = 4
              dna(n)(4:4) = 'o'
              ierr = ierr +1
            endif
!
!                   load starting index of this character type
!
            write (dna(n)(1:3),'(i3.3)') ks
          else
            write (*,*)'ERROR, xtrcdna - invalid summary line follows: '
            write (*,*) cline
            ierr = -1
            goto 200
!
          endif
        else
!
!                   see if data type should change
!
cx   allow - as acceptable  ...... sampson nrl 7/27/01
          if (nt.eq.1 .and. cx.ne.'-' .and.
     &	  (cx.lt.'A' .or. cx.gt.'Z') ) then
            kk = -1
          elseif (nt.eq.2 .and. (cx.lt.'0' .or. cx.gt.'9')) then
            kk = -1
          elseif (nt.eq.3 .and. cx.ne.' ') then
            kk = -1
          elseif (nt.eq.4 .and. ((cx.ge.'A'.and.cx.le.'Z') .or.         &
     &      (cx.ge.'0'.and.cx.le.'9') .or. cx.eq.' ')) then
            kk = -1
          else
!                     increase character count of same type
            nk = nk +1
          endif
          if (kk .ne. 0) then
!
!                   end of a type, load count and jump to top of loop
!
            write (dna(n)(5:7),'(i3.3)') nk
            ks = k
            goto 100
!
          endif
        endif
      enddo
!
!                   load count of last character type
!
      write (dna(n)(5:7),'(i3.3)') nk
  200 continue
!                   return number of dna lines found in string
      ndnal = n
      return
!
      end
