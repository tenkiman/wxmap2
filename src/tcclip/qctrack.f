      program qctrack
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)prctctd.f90	1.2 7/11/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  qctrack
!
!  DESCRIPTION:  PROCESS TROPICAL CYCLONE TRACKING DATA FROM NOGAPS & NORAPS
!
!  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:  NONE
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  HP/Unix
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:
!
!  PARAMETERS: NONE
!
!  COMMON BLOCKS:  NONE
!
!  FILES:
!    NAME     UNIT  FILE TYPE  ATTRIBUTE  USAGE       DESCRIPTION
!   -------   ----  ---------  ---------  -----   ---------------------
!   TCTRCKS    10   PERMANENT  SEQUENTIAL   IN    T. C. TRACKING DATA
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     I/O AND PROCESSING       SET ERROR FLAG TO NON-ZERO AND
!     ERRORS                   TURN ON SWITCH 6
!
!  ADDITIONAL COMMENTS:
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          NAME           DESCRIPTION
!         -------     ----------------------
!         REDTCTD     READ TROPICAL CYCLONE TRACKING DATA
!          PRCTCD     PROCESS TRACKING DATA
!          OUTCTD     OUTPUT TRACKING DATA
!
!  LOCAL VARIABLES:
!    NAME      TYPE                DESCRIPTION
!   ------     ----     ------------------------------------------------
!    BOGUS     CHAR     TROPICAL CYCLONE BOGUS POSITION DATA
!     CDTG     CHAR     DATE-TIME-GROUP OF STARTING POSITION
!    CYCID     CHAR     TROPICAL CYCLONE NUMBER AN ORIGIN BASIN CODE
!     FLAT     REAL     FORECAST LATITUDE  OF TROPICAL CYCLONE
!     FLON     REAL     FORECAST LONGITUDE OF TROPICAL CYCLONE
!     IER1      INT     ERROR FLAG FROM REDTCTD
!     IER2      INT     ERROR FLAG FROM PRCTCD
!     IER3      INT     ERROR FLAG FROM OUTCTD
!     IOE       INT     I/O ERROR FLAG
!     KONF      INT     CONFIDENCE INDICATOR FOR EACH POSITION
!     KONT      INT     COUNT OF TRACKING POSITIONS FOR EACH CYCLONE
!                          (1 - FOR CCRS
!                          (2 - FOR PLAIN LANGUAGE
!     MAXF      INT     MAXIMUM NUMBER OF FORECAST POSITIONS
!    MAXTC      INT     MAXIMUM NUMBER OF TROPICAL CYCLONES
!    MXFCT      INT     MAXIMUM NUMBER OF FORECAST POSITIONS
!     NTCT      INT     NUMBER OF TROPICAL CYCLONE TRACKS
!    TCDAT     CHAR     TROPICAL CYCLONE TRACKING DATA
!
!  METHOD:  PROCESS TROPICAL CYCLONE TRACKING DATA AND WRITE
!           QC'D VALUES ON DESIGANTED FILES (BASED UPON CENTER) ON
!           OPARSDK FOR LATER DOWNLOAD TO ATCF'S AND FOR DIRECT DDN
!           TRANSMISSION TO ATCF OF CENTER RESPONSIBLE FOR TROPICAL
!           CYCLONE WARNING.
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:
!
!  MAKEFILE:  N/A
!
!  RECORD OF CHANGES:
!
!  <<change notice>>  V1.1  (19 JUN 1996)  Hamilton, H.
!    initial installation on OASIS
!
!  <<change notice>>  V1.2  (17 JUL 1996)  Hamilton, H.
!    correct length of string NORAPS_ASIA from 10 to 11
!
!   Modified to run on ATCF           96     Sampson    
!
!   Modified to use new data format,  6/98   A. Schrader
!
!...................END PROLOGUE.......................................
!
      implicit none
!
      integer maxtc, mxfct
      parameter (maxtc = 9,  mxfct = 25)
!
      integer ntct, maxf, ialen, nogo, ioe, ioer, ier1, ier2, ier3
      integer numm, nuin, nout, lbp, iarg
      integer kont(2,maxtc), konf(mxfct,maxtc)
!
      character cdummy*1
      character*6 strmid
      character cdtg*10, cmodel*16
      character tcdat(mxfct,maxtc)*40, cycid(maxtc)*3, bogus(maxtc)*25
      character*100 storms
      character*132 filename
!
      real flat(mxfct,maxtc), flon(mxfct,maxtc)
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
c*************  This code added to get storm id ...bs 9/30/97 ****
c
c  get the storms directory name
c
      call getenv("ATCFSTRMS",storms)
      lbp=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c
c     get the storm id
c
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)

c
c  write heading on output
c
      print *,'********************************************************'
      print *,' '
      print *,'          ngpr model ',strmid
      print *,' '

      nogo = 0
c
c                   open diagnostic output file
c
      open (33,file='track.diag',iostat=ioe)
      if (ioe .ne. 0) then
        write(*,*) ' cant open track.diag file, error is ',ioe
        nogo = -55
c
      endif
c
c                   open input tracking data file
c
      nuin = 10
      filename = storms(1:lbp) // "/" // strmid //".tctracks"
	    open (nuin,file=filename,iostat=ioe,status='old')
      if (ioe .ne. 0) then
        write (*,*) 'qctrack, OPEN ERROR - MISSING FILE: '
	write (*,*)filename 
        nogo = -55
      endif
c
c                   open output file
c
      nout = 20
      filename = ' '
      filename = storms(1:lbp) // "/wptot.dat"
      open (nout,file=filename,status='old',iostat=ioer)
      if (ioer .lt. 0) then
        write (*,*) 'qctrack, OPEN ERROR is ',ioer,' ',filename
        nogo = -55
      endif
      rewind (nuin)
      rewind (nout)
c
c                   go to the end of the output file
c
   20 continue
      read (nout,'(a1)',end=25) cdummy
      go to 20
c
   25 continue
!
!                   check for I/O error
!
      if (nogo .ne. 0) then
        nogo = -nogo
cx  I don't really want a "fail" here ... bs 11/9/97
cx        call exit (nogo)
	write (*,*) 'early exit due to read failure:',nogo
        stop
!
      endif
!
      cmodel(1:6) = 'NOGAPS'
      numm = 03
!
      ier1 = 0
      ier2 = 0
      ier3 = 0
!
!                   CHECK FOR GO
!
      maxf = mxfct
      ntct = maxtc
      call redtctd (tcdat,maxf,ntct,kont,cycid,cdtg,bogus,ier1)
      if (ntct .gt. 0) then
!
!                   PROCESS TRACKING DATA
!
        call prctcd (bogus,tcdat,maxf,ntct,kont,cycid,flat,flon,
     &               konf,ier2)
        if (ier2 .eq. 0) then
!
!                   OUTPUT TRACKING DATA
!
          call outctd (nout,numm,ialen,flat,flon,kont,
     &                 konf,maxf,ntct,cycid,cdtg,ier3)
        else
          write (*,*) 'qctrack, NO 24-HR FORECASTS TO OUTPUT.'
        endif
      endif
      if (ier1 .ne. 0) then
        if (ier1 .eq. 5) then
          write (*,*) 'qctrack, ERROR IN READING TRACKING DATA'
        elseif (ier1 .eq. -1) then
          write (*,*) 'qctrack, ERROR EARLY EOF ON TRACKING DATA'
        else
          write (*,*) 'qctrack, ERROR IN PROCESSING TRACKING DATA'
        endif
      endif
!
!                   SIGNAL ERROR TO JCL
!
      if (ier1.ne.0 .or. ier2.ne.0 .or. ier3.ne.0) then
cx      write (*,*) 'qctrack - ERRORS, ier1 ',ier1,'  ier2 ',ier2,
cx   &              '  ier3 ',ier3
      else
        write (*,*) 'qctrack - NO ERRORs'
      endif
!     call exit (0)
      stop
!
      end
      subroutine chkbdat (bogus,nf,flat,flon,fspd,konf,kont)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)chkbdat.f90	1.1 6/14/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  CHKBDAT
!
!  DESCRIPTION:  CHECK TRACKING DATA THAT MIGHT BE BAD
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:  NONE
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:  APLIB(1731)
!
!  USAGE:  CALL CHKBDAT (BOGUS,NF,FLAT,FLON,FSPD,KONF,KONT)
!
!  PARAMETERS:
!     NAME        TYPE      USAGE             DESCRIPTION
!   --------      ----      ------   ------------------------------
!     BOGUS       REAL        IN     REAL BOGUS VALUES ARRAY
!                                      1) LAT, DEG +NH -SH
!                                      2) LON, DEG (0 - 360) EAST
!                                      3) HEAD, DEG
!                                      4) SPEED OF MOVEMENT, KT
!        NF       REAL        IN     MAXIMUM NUMBER OF FORECASTS
!      FLAT       REAL        IN     ARRAY OF FORECAST LATITUDES
!      FLON       REAL        IN     ARRAY OF FORECAST LONGITUDES
!      FSPD       REAL        IN     ARRAY OF FORECAST SPEED OF MOVEMENT
!      KONF        INT      IN/OUT   ARRAY OF CONFIDENCE FACTORS
!      KONT        INT      IN/OUT   COUNT OF FORECASTS
!                                      (1 - FOR CCRS
!                                      (2 - FOR PLAIN LANGUAGE
!
!  COMMON BLOCKS:  NONE
!
!  FILES:  NONE
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:  NONE
!
!  ADDITIONAL COMMENTS:
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  NONE
!
!  LOCAL VARIABLES:
!      NAME      TYPE               DESCRIPTION
!     ------     ----    -----------------------------------------------
!     DEGRAD     REAL    DEG TO RADIAN CONVERSION FACTOR
!        ELT     REAL    ESTIMATED LATITIDE
!        ELN     REAL    ESTIMATED LONGITUDE
!         F1     REAL    WEIGHTING FACTOR
!          J      INT    INDEX TO "BAD" LOCATION
!         KB      INT    COUNT OF "BAD" POSITIONS
!       NSUS      INT    ARRAY OF SUSPECT BAD VALUES BY INDEX
!        RAD     REAL    RADIAL DISTANCE, EITHER NM OR DEG LAT
!       RAD1     REAL    RADIAL DISTANCE, PART 1, DEG LAT
!       RAD2     REAL    RADIAL DISTANCE, PART 2, DEG LAT
!
!  METHOD:  1. ASSUME ALL CONFIDENCE OF 3 OR LESS ARE "GOOD" VALUES
!           2. USUALLY ESTIMATE POSITION FROM TWO PREVIOUS POSITIONS
!              AND SEE THAT LOCATED POSITION IS WITHIN SOME REASONABLE
!              DISTANCE.
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortarn 90
!
!  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
!
!  MAKEFILE:  N/A
!
!  RECORD OF CHANGES:
!
!
!...................END PROLOGUE.......................................
!
      implicit none
!
!         FORMAL PARAMETERS
      integer nf, konf(nf), kont(2)
      real bogus(4), flat(nf), flon(nf), fspd(nf)
!
!         LOCAL VARIABLES
      integer n, nsus(21), j, kb, mm, mp
      real degrad, rad1, rad2, rad, elt, eln, f1
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      degrad = acos (-1.0)/180.0
      kb = 0
      do n=1, kont(1)
        if (konf(n) .gt. 3) then
!
!                   ASSUME POSITION MAY BE BAD
!
          kb = kb +1
          if (kb .le. 21) then
!                   LOAD NSUS WITH INDEX TO "BAD" POSITIONS
            nsus(kb) = n
          endif
        endif
      enddo
!
!                   EVALUATE KB "BAD" POSITIONS
!
      do n=1, kb
        j = nsus(n)
        if (j .eq. 1) then
!
!                   CHECK FIRST POSITION, TAU = 0, WITH BOGUS
!
          if (abs (bogus(1)) .lt. 90.0) then
!
!                   BOGUS VALUES ARE GOOD, SO USE THEM
!
            rad1 = abs (flat(1) -bogus(1))
            rad2 = cos (0.5*(flat(1) +bogus(1))*degrad)
            rad2 = rad2*abs (flon(1) -bogus(2))
            rad  = sqrt (rad1*rad1 +rad2*rad2)
            if (rad .gt. 2.0) then
!
!                   INITIAL POSITION TOO FAR FROM BOGUS POSITION
!
              write (*,*) 'CYCLONE TOO FAR FROM BOGUS POSITION'
              konf(1) = 7
              goto 150
!
            endif
          else
!
!                   INITIAL POSITION CAN'T BE CHECKED
!                   SO ASSUME IT IS BAD
!
              write (*,*) 'CANT CHECK INITIAL POSITION'
              konf(1) = 7
              goto 150
!
          endif
        elseif (j .lt. kont(1)) then
!
!                   CHECK MID VALUES
!
          mm = j -1
          do mp=j+1, kont(1)
!                     LOOK FOR "GOOD" FUTURE POSITION
            if (konf(mp) .le. 3) goto 130
!
          enddo
          mp = j -2
          if (mp .ge. 1) then
!
!                     USE TWO PRECEEDING POSITIONS
!
            elt  = flat(mm) +(flat(mm) -flat(mp))
            eln  = flon(mm) +(flon(mm) -flon(mp))
            rad1 = abs (flat(j) -elt)
            rad2 = cos (0.5*(flat(j) +elt)*degrad)
            rad2 = rad2*abs (flon(j) -eln)
            rad  = sqrt (rad1*rad1 +rad2*rad2)
            if (rad .gt. 1.0) then
!
!                   POSITION TOO FAR FROM ESTIMATED POSITION
!
              write (*,*) 'TOO FAR FROM EP, TYPE 1'
              konf(j) = 7
              goto 150
!
            endif
          else
!
!                     USE ONLY PRECEEDING POSITION
!
            rad1 = abs (flat(j) -flat(mm))
            rad2 = cos (0.5*(flat(j) +flat(mm))*degrad)
            rad2 = rad2*abs (flon(j) -flon(mm))
!                   CONVERT FROM DEG-LAT TO NM
            rad  = 60.0*(sqrt (rad1*rad1 +rad2*rad2))
            if (rad .gt. 6*fspd(mm)) then
!
!                   POSITION TOO FAR FROM ESTIMATED POSITION
!
              write (*,*) 'TOO FAR FROM EP, TYPE 2'
              konf(j) = 7
              goto 150
!
            endif
            goto 140
!
          endif
  130     continue
!
!                   USE PRECEEDING AND FOLLOWING LOCATIONS
!
          f1   = 1.0/(mp -mm)
          elt  = flat(mm) +f1*(flat(mp) -flat(mm))
          eln  = flon(mm) +f1*(flon(mp) -flon(mm))
          rad1 = abs (flat(j) -elt)
          rad2 = cos (0.5*(flat(j) +elt)*degrad)
          rad2 = rad2*abs (flon(j) -eln)
          rad  = sqrt (rad1*rad1 +rad2*rad2)
          if (rad .gt. 1.0) then
!
!                   POSITION TOO FAR FROM ESTIMATED POSITION
!
            write (*,*) 'TOO FAR FROM EP, TYPE 3'
            konf(j) = 7
            goto 150
!
          endif
        else
!
!                   CHECK END POSITION
!
          mp = j -2
          if (mp .ge. 1) then
!
!                   USE LAST TWO PRIOR POSITIONS, WHICH IT HAS TO BE
!
            mm = j -1
            elt  = flat(mm) +(flat(mm) -flat(mp))
            eln  = flon(mm) +(flon(mm) -flon(mp))
            rad1 = abs (flat(j) -elt)
            rad2 = cos (0.5*(flat(j) +elt)*degrad)
            rad2 = rad2*abs (flon(j) -eln)
            rad  = sqrt (rad1*rad1 +rad2*rad2)
            if (rad .gt. 1.0) then
!
!                   POSITION TOO FAR FROM ESTIMATED POSITION
!
              write (*,*) 'TOO FAR FROM EP, TYPE 4'
              konf(j) = 7
            endif
          else
!
!                   USE LAST TWO POSITIONS, THIS CODE IS HERE FOR
!                   COMPLETNESS, FOR IT WILL NEVER BE USED
!
            rad1 = abs (flat(j) -flat(j-1))
            rad2 = cos (0.5*(flat(j) +flat(j-1))*degrad)
            rad2 = rad2*abs (flon(j) -flon(j-1))
!                   CONVERT FROM DEG-LAT TO NM
            rad  = 60.0*(sqrt (rad1*rad1 +rad2*rad2))
            if (rad .gt. 6*fspd(j-1)) then
!
!                   POSITION TOO FAR FROM ESTIMATED POSITION
!
              write (*,*) 'TOO FAR FROM EP, TYPE 5'
              konf(j) = 7
            endif
          endif
        endif
  140   continue
      enddo
      j = kont(1) +1
  150 continue
      kont(1) = j -1
!
      end
      subroutine chkcdat (bogus,nf,flat,flon,fhed,fspd,konf,kwid,kont)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)chkcdat.f90	1.1 6/14/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  CHKCDAT
!
!  DESCRIPTION:  CHECK TRACKING DATA
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:  NONE
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL CHKCDAT (BOGUS,NF,FLAT,FLON,FHED,FSPD,KONF,KWID,KONT)
!
!  PARAMETERS:
!     NAME        TYPE      USAGE             DESCRIPTION
!   --------      ----      ------   ------------------------------
!     BOGUS       REAL        IN     REAL BOGUS VALUES ARRAY
!                                      1) LAT, DEG +NH -SH
!                                      2) LON, DEG (0 - 360) EAST
!                                      3) HEAD, DEG
!                                      4) SPEED OF MOVEMENT, KT
!        NF       REAL        IN     MAXIMUM NUMBER OF FORECASTS
!      FLAT       REAL        IN     ARRAY OF FORECAST LATITUDES
!      FLON       REAL        IN     ARRAY OF FORECAST LONGITUDES
!      FHED       REAL        IN     ARRAY OF FORECAST HEADINGS
!      FSPD       REAL        IN     ARRAY OF FORECAST SPEED OF MOVEMENT
!      KONF        INT      IN/OUT   ARRAY OF CONFIDENCE FACTORS
!      KWID        INT        IN     ARRAY OF WIND SUPPORT AND
!                                    INTERSECTION SUPPORT FACTORS
!      KONT        INT      IN/OUT   COUNT OF FORECASTS
!                                       (1 - FOR CCRS
!                                       (2 - FOR PLAIN LANGUAGE
!
!  COMMON BLOCKS:  NONE
!
!  FILES:  NONE
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:  NONE
!
!  ADDITIONAL COMMENTS:
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  NONE
!
!  LOCAL VARIABLES:
!      NAME      TYPE               DESCRIPTION
!     ------     ----    -----------------------------------------------
!     DEGRAD     REAL    DEG TO RADIAN CONVERSION FACTOR
!        ELT     REAL    ESTIMATED LATITIDE
!        ELN     REAL    ESTIMATED LONGITUDE
!         F1     REAL    WEIGHTING FACTOR
!      HDLMT     REAL    HEADING LIMIT, DEG
!     HEDLMT     REAL    HEADING LIMIT FOR TESTING, DEG
!          J      INT    INDEX TO "BAD" LOCATION
!         KB      INT    COUNT OF "BAD" POSITIONS
!       NSUS      INT    ARRAY OF SUSPECT BAD VALUES BY INDEX
!        RAD     REAL    RADIAL DISTANCE, EITHER NM OR DEG LAT
!       RAD1     REAL    RADIAL DISTANCE, PART 1, DEG LAT
!       RAD2     REAL    RADIAL DISTANCE, PART 2, DEG LAT
!      SPLMT     REAL    SPEED OF ADVANCE LIMIT FOR TESTING, KT
!
!  METHOD:
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
!
!  MAKEFILE:  N/A
!
!  RECORD OF CHANGES:
!
!
!...................END PROLOGUE.......................................
!
       implicit none
!
       real hdlmt, splmt
       parameter (hdlmt = 45.0,  splmt = 5.0)
!
!         FORMAL PARAMETERS
      integer nf, konf(nf), kwid(2,nf), kont(2)
      real bogus(4), flat(nf), flon(nf), fhed(nf), fspd(nf)
!
!         LOCAL VARIABLES
      integer j, n, ns, nx
      real degrad, rad1, rad2, rad
      real sumsp, sumsx, avgsp
      real sumhd, sumhx, avghd, avghx, hedlmt
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   CHECK FIRST POSITION WITH BOGUS
!
      degrad = acos (-1.0)/180.0
      if (abs (bogus(1)) .lt. 90.0) then
        rad1 = abs (flat(1) -bogus(1))
        rad2 = cos (0.5*(flat(1) +bogus(1))*degrad)
        rad2 = rad2*abs (flon(1) -bogus(2))
        rad  = sqrt (rad1*rad1 +rad2*rad2)
        if (rad .gt. 2.0) then
!
!               INITIAL POSITION TOO FAR FROM BOGUS POSITION
!
          write (*,*) 'ERROR, TOO FAR FROM INITIAL POSITION'
          konf(1) = 7
          n       = 1
          goto 140
!
        endif
      else
        if (kwid(1,1).lt.4 .and. kwid(2,1).lt.8) then
!
!                   ASSUME POSITION BAD
!
          write (*,*) 'ERROR, ASSUME POSITION IS BAD'
          konf(1) = 7
          n       = 1
          goto 140
!
        endif
      endif
!
!                   CHECK REMAINDER OF POSITIONS
!
      ns    = 1
      sumsp = fspd(1)
      sumhd = fhed(1)
      do n=2, kont(1)
        if (fspd(n) .gt. splmt) then
!
!                   SPEED OF MOVEMENT HIGH ENOUGH FOR CHECKING
!
          if (fspd(n) .gt. 2.0*fspd(n-1)) then
!
!                   POSITION IS SUSPECT, CHECK WITH RUNNING AVERAGES
!
            if (ns .eq. 5) then
!
!                     CHECK SPEED DIFFERENCE WITH AVERAGE
!
              if (fspd(n) .gt. 2.0*(sumsp/5.0)) then
!
!                       CHECK HEADING OFFSET
!
                if (abs (fhed(n) -avghd) .gt. 180.0) then
                  if (fhed(n).ge.270.0 .and. avghd.le.090.0) then
                    avghx = avghd +360.0
                  elseif (avghd.ge.270.0 .and. fhed(n).le.090.0) then
                    avghx = avghd -360.0
                  endif
                else
                  avghx = avghd
                endif
                if (fspd(n-1) .gt. splmt) then
                  hedlmt = hdlmt
                else
                  hedlmt = 2.0*hdlmt
                endif
                if (abs (fhed(n) -avghx) .gt. hedlmt) then
!
!                     ASSUME NOT TRACKING INITIAL CYCLONE
!                     END TRACKING DATA
!
                  write (*,*) 'ERROR, NOT TRACKING SAME CYCLONE, TYPE 1'
                  konf(n) = 7
                  goto 140
!
                endif
              endif
            else
              if (kont(1) -n .gt. ns) then
!
!                   CALCULATE RUNNING AVERAGE WITH FUTURE VALUES
!
                nx    = 0
                sumsx = 0.0
                sumhx = 0.0
                do j=n+1, kont(1)
                  nx = nx +1
                  sumsx = sumsx +fspd(j)
                  if (sumhx.ge.270.0 .and. fhed(j).le.090.0) then
                    sumhx = sumhx*(nx -1) +fhed(j) +360.0
                  elseif (sumhx.le.090.0 .and. fhed(j).ge.270.0) then
                    sumhx = sumhx*(nx -1) +fhed(j) -360.0
                  else
                    sumhx = sumhx*(nx -1) +fhed(j)
                  endif
                  sumhx = sumhx/nx
                  if (nx .eq. 5) goto 120
!
                enddo
  120           continue
                avgsp = sumsx/nx
                avghd = sumhx
              else
!
!                     USE WHAT WE HAVE, EVEN THOUGH IT IS LESS THAN 5
!
                avgsp = sumsp/ns
                avghd = sumhd
              endif
              if (fspd(n) .gt. 2.0*avgsp) then
!                       CHECK HEADING OFFSET
                if (abs (fhed(n) -avghd) .gt. 180.0) then
                  if (fhed(n).ge.270.0 .and. avghd.le.090.0) then
                    avghx = avghd +360.0
                  elseif (avghd.ge.270.0 .and. fhed(n).le.090.0) then
                    avghx = avghd -360.0
                  endif
                else
                  avghx = avghd
                endif
                if (fspd(n-1) .gt. splmt) then
                  hedlmt = hdlmt
                else
                  hedlmt = 2.0*hdlmt
                endif
                if (abs (fhed(n) -avghx) .gt. hedlmt) then
!
!                     ASSUME NOT TRACKING INITIAL CYCLONE
!                     END TRACKING DATA
!
                  write (*,*) 'ERROR, NOT TRACKING SAME CYCLONE, TYPE 2'
                  konf(n) = 7
                  goto 140
!
                endif
              endif
            endif
          endif
        endif
!
!                   CALCULATE AVERAGE RUNNING SUM OF SPEED OF MOVEMENT
!                   AND RUNNING AVERAGE HEADING
!
        if (ns .eq. 5) then
!
!                   MAINTAIN RUNNING SUM AND RUNNING AVERAGE,
!                   ADD NEWEST AND SUBTRACT OLDEST
!
          sumsp = sumsp +fspd(n) -fspd(n-5)
          if (sumhd.ge.270.0 .and. fhed(n).le.090.0) then
            sumhd = sumhd*5.0 +fhed(n) +360.0
          elseif (sumhd.le.090.0 .and. fhed(n).ge.270.0) then
            sumhd = sumhd*5.0 +fhed(n) -360.0
          else
            sumhd = sumhd*5.0 +fhed(n)
          endif
          sumhx = sumhd/6.0
          if (sumhx.ge.270.0 .and. fhed(n-5).le.090.0) then
            sumhd = sumhd -(fhed(n-5) +360.0)
          elseif (sumhx.le.090.0 .and. fhed(n).ge.270.0) then
            sumhd = sumhd -(fhed(n-5) -360.0)
          else
            sumhd = sumhd +fhed(n-5)
          endif
          sumhd = amod (sumhd/5.0,360.0)
        else
!
!                   ADD TO RUNNING SUM OF SPEED AND
!                   CALCULATE NEW RUNNING AVERAGE HEADING
!
          ns    = ns +1
          sumsp = sumsp +fspd(n)
          if (sumhd.ge.270.0 .and. fhed(n).le.090.0) then
            sumhd = sumhd*(ns -1) +fhed(n) +360.0
          elseif (sumhd.le.090.0 .and. fhed(n).ge.270.0) then
            sumhd = sumhd*(ns -1) +fhed(n) -360.0
          else
            sumhd = sumhd*(ns -1) +fhed(n)
          endif
          sumhd = amod (sumhd/ns, 360.0)
        endif
      enddo
      n = kont(1) +1
  140 continue
      kont(1) = n -1
!
      end
      subroutine chknum (card,ks,kt,nnum)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)chknum.f90	1.1 6/14/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  CHKNUM
!
!  DESCRIPTION:  CHECK THAT CHARACTERS BETWEEN KS-1 AND KT+1 ARE ALL
!                NUMBERS OR NUMBER(S) AND BLANK(S)
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  NONE
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:  NONE
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL CHKNUM (CARD,KS,KT,NNUM)
!
!  PARAMETERS:
!     NAME         TYPE        USAGE             DESCRIPTION
!   --------      -------      ------   ------------------------------
!     CARD         CHAR         IN      CHARACTER STRING
!     KS            INT         IN      STARTING CHARACTER FOR CHECKING
!     KT            INT         IN      ENDING CHARACTER FOR CHECKING
!     NNUM          INT         OUT     NUMBER OF DIGITS OR NUMBER OF
!                                       DIGITS AND BLANKS
!
!  COMMON BLOCKS:  NONE
!
!  FILES:  NONE
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:  NONE
!
!  ADDITIONAL COMMENTS:
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  NONE
!
!  LOCAL VARIABLES:
!          NAME      TYPE                 DESCRIPTION
!         ------     ----       ----------------------------------
!          CX        CHAR       WORKING CHARACTER
!          NBLK       INT       COUNT OF BLANKS
!          JS         INT       STARTING CHARACTER POSITION
!          JT         INT       ENDING CHARACTER POSITION
!
!  METHOD:  N/A
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:
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
!         FORMAL PARAMETERS
      integer ks, kt, nnum
      character*80 card
!
!         LOCAL VARIABLES
      integer nblk, js, jt, j
      character*1 cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nnum = 0
      nblk = 0
!                   VALIDATE STARTING AND ENDING POSITIONS
      js = max0 (ks,1)
      jt = min0 (kt,24)
      do j=js, jt
        cx = card(j:j)
        if (cx.ge.'0' .and. cx.le.'9') then
          nnum = nnum +1
        elseif (cx .eq. ' ') then
          nblk = nblk +1
        endif
      enddo
      if (nblk.gt.0 .and. nnum.ge.1) nnum = nnum +nblk
!
      end
      subroutine chrchk (ks,kl,tcdat,nd,np,nn,no)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)chrchk.f90	1.1 6/14/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  CHRCHK
!
!  DESCRIPTION:  DECODE CHARACTERS BETWEEN KS-1 AND KT+1 FOR DIGITS,
!                PERIODS AND OTHER
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  NONE
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:  NONE
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL CHRCHK (KS,KL,TCDAT,ND,NP,NG,NO)
!
!  PARAMETERS:
!     NAME         TYPE        USAGE             DESCRIPTION
!   --------      -------      ------   ------------------------------
!     KS            INT         IN      STARTING CHARACTER FOR CHECKING
!     KL            INT         IN      ENDING CHARACTER FOR CHECKING
!     TCDAT        CHAR         IN      CHARACTER STRING
!     ND            INT         OUT     NUMBER OF DIGITS OR NUMBER OF
!                                       DIGITS AND BLANKS
!     NN            INT         OUT     NUMBER OF NEGATIVE SIGNS
!     NP            INT         OUT     NUMBER OF PERIODS
!     NO            INT         OUT     NUMBER OF OTHER CHARACTERS
!
!  COMMON BLOCKS:  NONE
!
!  FILES:  NONE
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:  NONE
!
!  ADDITIONAL COMMENTS:
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  NONE
!
!  LOCAL VARIABLES:
!          NAME      TYPE                 DESCRIPTION
!         ------     ----       ----------------------------------
!          CX        CHAR       WORKING CHARACTER
!          JS         INT       STARTING CHARACTER POSITION
!          JT         INT       ENDING CHARACTER POSITION
!
!  METHOD:  N/A
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:
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
!        FORMAL PARAMETERS
      integer ks, kl, nd, nn, np, no
      character*40 tcdat
!
!         LOCAL VARIABLES
      integer j, js, jt
      character*1 cx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nd = 0
      np = 0
      no = 0
      nn = 0
!                   VALIDATE STARTING AND ENDING POSITIONS
      js = max0 (ks,1)
      jt = min0 (kl,40)
      do j=js, jt
        cx = tcdat(j:j)
        if (cx.ge.'0' .and. cx.le.'9') then
          nd = nd +1
        elseif (cx .eq. '.') then
          np = np +1
        elseif (cx .eq. '-') then
          nn = nn +1
        elseif (cx .ne. ' ') then
          no = no +1
        endif
      enddo
!
      end
      subroutine obsuafix (mxhr,mxcy,suadat,nhr,ncy,sfcp,rltln,cnsew)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION: @(#)obsuafix.f90	1.1 5/7/97 
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  obsuafix
!
!  DESCRIPTION:  extract surface pressure and U/A tracking data
!
!  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:  NONE
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:  NONE
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL CHKNUM (CARD,KS,KT,NNUM)
!
!  PARAMETERS:
!     NAME         TYPE        USAGE             DESCRIPTION
!   --------      -------      ------   ------------------------------
!     mxhr          int         in      second dimension of suadat
!     mxcy          int         in      third  dimension of suadat
!     suadat       real         in      contents of additional tracking
!                                       data from ngtrack:
!                                       (sfc,  850,  700,  500)
!                                         p   lt/ln lt/ln lt/ln  (7)
!     nhr           int         in      hour index to suadat
!     ncy           int         in      cyclone index to suadat
!     sfcp         real         out     surface pressure (hPa)
!     rltln        real         out     array of U/A lt/ln
!     cnsew        char         out     array of hemisphere indicators
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
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  none
!
!  LOCAL VARIABLES:
!          NAME      TYPE                 DESCRIPTION
!         ------     ----       ----------------------------------
!            m        int       first index to suadat array
!
!  METHOD:  n/a
!
!  INCLUDE FILES:  none
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:
!
!  MAKEFILE:
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  V1.1   (14 MAY 1997)  --  Hamilton, H.
!    Ininitial installation for processing additional support data
!    from ngtrack
!
!...................END PROLOGUE.......................................
!
      implicit none
!
!         formal parameters
      integer                                  ::  mxhr, mxcy, nhr, ncy
      character (len = 1), dimension (2,3)     ::  cnsew
      real (kind = 4)                          ::  sfcp
      real (kind = 4), dimension (2,3)         ::  rltln
      real (kind = 4), dimension (7,mxhr,mxcy) ::  suadat
!
!         local variables
      integer  ::  m, n
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      sfcp  = suadat(1,nhr,ncy)   !  surface pressure
      cnsew = ' '
      do n=1, 3    !  process 850, 700 and 500 lt/ln positions
        m = 2*n
        rltln(1,n) = suadat(m,nhr,ncy)
        if (abs (rltln(1,n)) .gt. 0.0 .and.
     &      abs (rltln(1,n)) .lt. 80.0) then
          if (rltln(1,n) .gt. 0.0) then
            cnsew(1,n) = 'N'
          else
            cnsew(1,n) = 'S'
            rltln(1,n) = abs (rltln(1,n))
          endif
        endif
        m = m +1
        rltln(2,n) = suadat(m,nhr,ncy)
        if (rltln(2,n) .gt. 0.0 .and. rltln(2,n) .lt. 360.0) then
          if (rltln(2,n) .le. 180.0) then
            cnsew(2,n) = 'E'
          else
            cnsew(2,n) = 'W'
            rltln(2,n) = 360.0 -rltln(2,n)
          endif
        endif
        if (rltln(1,n) .eq. 0.0) rltln(2,n) = 0.0
        if (rltln(2,n) .eq. 0.0) rltln(1,n) = 0.0
        if (rltln(1,n) .eq. 0.0) then
          cnsew(1,n) = ' '
          cnsew(2,n) = ' '
        endif
      enddo
!
      end
      subroutine outctd (nout,numm,lenp,flat,flon,kont,konf,nf,nc,
     &                   cycid,cdtg,ierr)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  OUTCTD
!
!  DESCRIPTION:  OUTPUT NOGAPS TROPICAL CYCLONE TRACKING DATA FOR ATCF
!
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL OUTCTD (NUMM,PATH,FLAT,FLON,KONT,KONF,NF,NC,CYCID,CDTG,IERR)
!
!  PARAMETERS:
!     NAME       TYPE     USAGE             DESCRIPTION
!   --------    ------    ------    -----------------------------------
!       NOUT      INT       IN      OUTPUT UNIT NUMBER
!       NUMM      INT       IN      ATCF MODEL NUMBER
!                                         36 - NRPP - NORAPS - Pacifc O
!                                         37 - NRPI - NORAPS - Indian O
!                                         03 - NGPR - NOGAPS - (0 - 72)
!                                         50 - NGPX - NOGAPS - (0 - 120)
!       PATH     CHAR       IN      PATH TO OUTPUT DIRECTORY
!       LENP      INT       IN      LENGTH OF PATH
!       FLAT     REAL       IN      ARRAY OF FORECAST LATITUDE
!       FLON     REAL       IN      ARRAY OF FORECAST LONGITUDE, 0-360E
!       KONT      INT       IN      ARRAY OF NUMBER OF FORECASTS
!                                     (1 - FOR A-DECK
!                                     (2 - FOR PLAIN LANGUAGE
!       KONF      INT       IN      ARRAY OF CONFIDENCE NUMBERS
!         NF      INT       IN      MAX NUMBER OF FORECASTS
!         NC      INT       IN      NUMBER OF CYCLONE TRACKS
!      CYCID     CHAR       IN      CYCLONES NUMBER AND ORIGIN BASIN
!       CDTG     CHAR       IN      FORECAST STARTING DATE-TIME-GROUP
!       IERR      INT       OUT     ERROR FLAG, 0 NO ERROR
!
!  COMMON BLOCKS:  NONE
!
!  FILES:
!    NAME    UNIT  FILE TYPE  ATTRIBUTE   USAGE       DESCRIPTION
!   -------  ----  ---------  ----------  -----   ---------------------
!   dynamic  dynamic perm     SEQUENTIAL   OUT    DDN/DPS DATA FILE
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     I/O ERROR                DIAGNOSTIC AND EXIT
!
!  ADDITIONAL COMMENTS:
!
!                       FOR: First tracking - NGPS
!                              1
!     INDEX  1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
!
!       TAU  0 6 1 1 2 3 3 4 4 5 6 6 7 7 8
!                2 8 4 0 6 2 8 4 0 6 2 8 4
!
!                                    ! ! !
!   A-DECK_00    *   *   *   *       *
!  NGPS PTS      1   2   3   4       5
!                                      !
!   A-DECK_06      *   *   *   *       *
!  NGPS PTS        1   2   3   4       5
!                                        !
!   A-DECK_12        *   *   *   *       *
!  NGPS PTS          1   2   3   4       5
!
! 12 Hourly data ... bs 9/30/97
!       TAU  0  12  24  36  48  60 72     
!  A-DECK_00     *   *   *   *      *
!  NGPS PTS  1   2   3   4   5      7
!                                      !
!                              1                   2         2
!     INDEX  1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
!
!       TAU  0 6 1 1 2 3 3 4 4 5 6 6 7 7 8 9 9 1 1 1 1 1 1 1 1
!                2 8 4 0 6 2 8 4 0 6 2 8 4 0 6 0 0 1 2 2 3 3 4
!                                              2 8 4 0 6 2 8 4
!                                    !               ! ! !
!   A-DECK_00                        *   *   *   *   *
!  NGPX PTS                          1   2   3   4   5
!                                      !               !
!   A-DECK_06                          *   *   *   *   *
!  NGPX PTS                            1   2   3   4   5
!                                        !               !
!   A-DECK_12                            *   *   *   *   *
!  NGPX PTS                              1   2   3   4   5
!
!       FORMAT_00  OF NGPS/NRPP/NRPI A-DECK  (NR's go to 48 only)
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         43NGPSYYMMDDHH-LATLONG-LATLONG-LATLONG-LATLONG-LATLONG  0  0
!   TAU:                   12      24      36      48      72
!                  7         8
!         12345678901234567890
!           0  0  0 BBNNYC
!
!       FORMAT_00 OF NGPX A-DECK - EXTENSION OF NGPS
!                  1         2         3         4         5         6
!         123456789012345678901234567890123456789012345678901234567890
!         50NGPXYYMMDDHH-LATLONG-LATLONG-LATLONG-LATLONG-LATLONG  0  0
!   TAU:                   72      84      96      108     120
!                  7         8
!         12345678901234567890
!           0  0  0 BBNNYC
!
!   WHERE:  YY - LAST TWO DIGITS OF YEAR
!           MM - NUMBER OF MONTH
!           DD - DAY OF MONTH
!           HH - HOUR OF TAU ZERO POSITION
!            - - SIGN OF LATITUDE, BLANK FOR NH AND "-" FOR SH
!          LAT - TEN TIMES LATITUDE, (DEG)
!         LONG - TEN TIMES WEST LONGITUDE, (0 -360 WEST) (DEG)
!           BB - TWO CHARACTER ORIGINAL BASIN CODE OF TROPICAL CYCLONE
!           NN - TROPICAL CYCLONE NUMBER
!           YC - NH = YY, SH = YY for MON <= 6, else SH = YY +1
!
!   CONFIDENCE RATING IN PLAIN LANGUAGE:
!               0 - NOT RATED (MISSING LOCATION)
!               1 - ONLY ONE CYCLONE IN AREA
!     ******  ALL THE FOLLOWING HAVE 2 OR MORE CYCLONES IN SEARCH AREA
!               2 - CYCLONE SELECTED IS CLOSEST TO BOTH EP & LKL
!                     AND HAS THE HIGHER WIND SPEED
!               3 - CYCLONE SELECTED IS CLOSEST TO EITHER EP OR LKL
!                     WITH GOOD WIND SUPPORT AND SPEED
!     ******  ALL THE FOLLOWING ARE OMITTED FROM A-DECK, BUT ARE RETAINED
!                     IN THE PLAIN LANGUAGE OUTPUT.  NOTE, A 1, 2 OR 3
!                     RATING FOLLOWING A 7 IS ALSO OMITTED FROM A-DECK.
!               4 - CYCLONE SELECTED IS CLOSEST TO EITHER EP OR LKL
!                     WITH BEST WIND AND INTERSECTION SUPPORT
!               5 - CYCLONE SELECTED IS CLOSEST TO EITHER EP OR LKL
!                     WITH HIGHEST WIND SPEED
!               6 - CYCLONE SELECTED HAS HIGHEST WIND SPEED
!               7 - QUALITY CONTROL CHECKING HAS FOUND ABNORMAL SPEED
!                   OF MOVEMENT AND HEADING.  CONTINUED TRACKING OF
!                   INITIAL CYCLONE DOUBTFUL, FURTHER QC CHECKING
!                   IS SUSPENDED.  THIS POSITION AND REMAINDER OF
!                   TRACK NOT IN A-DECK FORMAT.  ALL TRACKING POSITIONS
!                   ARE IN PLAIN LANGUAGE FOR TDO EVALUATION.
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:  
!      NAME                   FUNCTION
!    ----------        ------------------------------------------------
!    obsuafix          extract surface pressure and U/A tracking data
!                      from array suadat
!
!  LOCAL VARIABLES:
!          NAME      TYPE                 DESCRIPTION
!         ------     ----       ----------------------------------
!         CB         CHAR       TWO CHARACTER TC BASIN FLAG
!         CEW        CHAR       EAST/WEST CHARACTER FLAG
!         CNS        CHAR       NORTH/SOUTH CHARACTER FLAG
!         CS         CHAR       SINGLE CHARACTER FORMATION FLAG - NOTE,
!                               THIS FLAG WILL BE IN "ERROR" IF TC
!                               LEAVES INITIAL CB LOCATION
!         NDPSTX      INT       COUNT OF DDN/DPS CYCLONES
!         NI87        INT       INDEX TO CENTER OF RESPONSIBILITY
!         SUADAT     REAL       SURFACE & U/A DATA FOR SAES
!
!  METHOD:  WRITE ATCF A-DECK FORMAT FIRST
!           WRITE PLAIN LANGUAGE
!           TRANSMIT MESSAGE VIA DDN
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
!
!  MAKEFILE:  N/A
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  V1.1  (19 JUN 1996) -- HAMILTON, H.
!    initial installation on OASIS
!
!  <<CHANGE NOTICE>>  V1.2  (31 JUL 1996) -- HAMILTON, H.
!    modify routine so up to 6 A-decks may be produced from one forecast
!    of NOGAPS; Up to 3 NGPS and up to 3 NGPX with 6-hour difference in
!    starting times.
!
!  <<CHANGE NOTICE>>  V1.3  (01 AUG 1996) -- Hamilton, H.
!    add index to cyclone ID in call to BOH
!
!  <<CHANGE NOTICE>>  V1.4  (07 AUG 1996) -- Hamilton, H.
!    remove bypass to BOH
!
!  <<CHANGE NOTICE>>  V1.5  (14 AUG 1996) -- Hamilton, H.
!    change icao for JTWC from ATGQ to ATQG - requested by Buck S.
!
!  <<CHANGE NOTICE>>  V1.6  (21 AUG 1996) -- Hamilton, H.
!    remove model number in plain language
!
!  <<CHANGE NOTICE>>  V1.7  (28 AUG 1996) -- Hamilton, H.
!    transmit to NHC with ICAO of ATMQ
!
!  <<CHANGE NOTICE>>  V1.8  (05 SEP 1996) -- Hamilton, H.
!    change two-letter basin code from NA to AL for Atlantic
!
!  <<CHANGE NOTICE>>  V1.9  (18 SEP 1996) -- Hamilton, H.
!    remove minor intermittent bugs in A-deck and correct year for
!    Southern Hemisphere cyclones after June of each year
!
!  <<CHANGE NOTICE>>  V1.10  (18 SEP 1996) -- Hamilton, H.
!    split lat/lon in plain language output
!
!  <<CHANGE NOTICE>>  V1.11  (14 MAY 1997) -- Hamilton, H.
!    add surface and u/a data to plain language output for SAES
!
!  <<CHNAGE NOTICE>>  V1.12  (28 MAY 1997) -- Hamilton, H.
!    add taus 108 & 120 to output
!
!...................END PROLOGUE.......................................
!
      implicit none
!
      include 'dataioparms.inc'
      integer, parameter  ::  maxhr = 25,  maxtc = 9
!
!         FORMAL PARAMETERS
      integer nout, numm, lenp, nf, nc, kont(2,nc), konf(nf,nc), ierr
      character cycid(9)*3, cdtg*10
      real flat(nf,nc), flon(nf,nc)
!
!         LOCAL VARIABLES
      integer konfm, ioe, izero, inine, m, n, j, k, ni87, in2
      integer itau, ndpstx, mu, kp, jt, iyr, imo, llmax, lmax, l
      integer iopn, nrd, nadd, ll
      integer nps(5,3), npx(5,3), npr(5)
      integer lat(5), lon(5)
      integer lbp
      integer ltlnwnd(numtau,llw)
      integer ii
      integer iwnd
      integer ios, iarg
!
      character*1 cns, cew, cs, cns1, cns2, cns3, cew1, cew2, cew3
      character*1 cnsew(2,3)
      character*2 cb
      character*3 cidsua(maxtc)
      character*4 cayr
      character*6 cnikio(4), cstatx
      character*6 strmid
      character*2 century
      character*2 cent
      character*8 tempdtg
      character*10 fdtg(3)
      character*100 storms
      character*200 filename
!
      real suadat(7,maxhr,maxtc)
      real plat, plon, sfcp, rlt85, rln85, rlt70, rln70, rlt50, rln50
      real rltln(2,3)
!
      equivalence (rlt85,rltln(1,1)), (rln85,rltln(2,1))
      equivalence (rlt70,rltln(1,2)), (rln70,rltln(2,2))
      equivalence (rlt50,rltln(1,3)), (rln50,rltln(2,3))
      equivalence (cns1,cnsew(1,1)), (cew1,cnsew(2,1))
      equivalence (cns2,cnsew(1,2)), (cew2,cnsew(2,2))
      equivalence (cns3,cnsew(1,3)), (cew3,cnsew(2,3))
!
      data cnikio/'36NRPP', '37NRPI', '03NGPR', '03NGPY'/
!                  index to taus
      data nps/ 3,  5,  7,  9, 13,
     &          4,  6,  8, 10, 14,
     &          5,  7,  9, 11, 15/
      data npx/13, 15, 17, 19, 21,
     &         14, 16, 18, 20, 22,
     &         15, 17, 19, 21, 23/
      data npr/ 2,  3,  4,  5,  7/
!
      data llmax/23/  ! max number in npx
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
c
c  get the storms directory name
c
      call getenv("ATCFSTRMS",storms)
      lbp=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c
c     get the storm id
c
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c     get the century for the storm file
c
      call getarg(iarg,century)
      iarg = iarg + 1
c
c     get the last best track posit century too (could be different from above)
c
      ios = 0
      do while ( ios .eq. 0 )
	 call readBT( 92,cent,tempdtg,lat,cns,lon,cew,iwnd,ios )
      enddo

c
      write (*,*) ' outctd, process',nc,' cyclones for ATCF aid ',numm
      if (numm .eq. 03) then
        cstatx = cnikio(3)
      elseif (numm .eq. 36) then
        cstatx = cnikio(1)
      elseif (numm .eq. 37) then
        cstatx = cnikio(2)
      elseif (numm .eq. 43) then
        cstatx = cnikio(3)
      elseif (numm .eq. 50) then
        cstatx = cnikio(3)
      elseif (numm .eq. 48) then
        cstatx = cnikio(3)
      else
        ierr = 99
        write (*,*) 'prctctd, outctd UNKNOWN model number is ',numm
        goto 200
!
      endif
      ndpstx = 0
      read (cdtg,'(i4,i2)') iyr, imo
      if (imo .gt. 6) iyr = iyr +1
      write (cayr,'(i4)') iyr
!
!                   set starting times for A-DECKs
!
      fdtg(1) = cdtg
      call icrdtg (cdtg(3:10),tempdtg,6)
      fdtg(2) = '  '//tempdtg
      call icrdtg (cdtg(3:10),tempdtg,12)
      fdtg(3) = '  '//tempdtg
!
      izero = ichar ('0')
      inine = ichar ('9')
      mu    = 80
!
      filename = storms(1:lbp) // "/" // strmid // ".suainfo" 
      open (65,file=filename,iostat=iopn,access='sequential',
     &  form='unformatted',status='old')
      if (iopn .eq. 0) then
!
!                   OBTAIN supporting surface and U/A data
!
        read (65) cidsua
        read (65) suadat
        nrd = 65
      else
        write (*,*) 'MISSING ALL sua data' 
	cidsua = ' '
        suadat = 0.0
        nrd    = -1
      endif
      close (65)
      do n=1, nc
        if (kont(1,n).eq.0 .and. kont(2,n).eq.0) cycle
!
!                   KEY A-DECK TWO LETTER BASIN CODES OFF STANDARD
!                   ONE LETTER BASIN CODE
!
        ni87 = 1              ! set to JTWC, change as required below
        cs   = cycid(n)(3:3)
        if (cs .eq. 'A' .or. cs.eq.'B') then
!                   ARABIN SEA AND BAY OF BENGAL, NORTH INDIAN OCEAN
           cb = 'IO'
        elseif (cs .eq. 'W') then
!                   WESTERN PACIFIC OCEAN
           cb = 'WP'
        elseif (cs .eq. 'C') then
!                   CENTRAL PACIFIC OCEAN
           cb = 'CP'
           if (flon(1,n) .ge. 180.0) ni87 = 2
        elseif (cs .eq. 'E') then
!                   EASTERN PACIFIC OCEAN
           cb = 'EP'
           if (flon(1,n) .ge. 180.0) ni87 = 2
        elseif (cs .eq. 'S' .or. cs .eq. 'P') then
!                   SOUTH INDIAN AND SOUTH PACIFIC OCEANS
           cb   = 'SH'
           plon = flon(1,n)
           if (plon .gt. 180.0 .and. plon .le. 360.0) ni87 = 2
        elseif (cs .eq. 'L') then
!                   NORTH ATLANTIC OCEAN
           cb   = 'AL'
           ni87 = 3
        else
!                   UNKNOWN OCEAN BASIN
           cb = 'XX'
        endif
!
!               CHECK FOR NON-NUMBER IN LEADING POSITION OF STORM NUMBER
!
        in2 = ichar (cycid(n)(1:1))
        if (in2.lt.izero .or. in2.gt.inine) cycid(n)(1:1) = '0'
!
!                   set maximum A-DECK forecasts
!
cx  Don't do NORAPS tracking yet ... bs 9/29/97

cx      if (numm .lt. 40) then
cx        jt = 1               !  NORAPS tracking
cx      else
cx        jt = 3               !  NOGAPS tracking
          jt = 1               !  NOGAPS tracking now only for current dtg  ... sampson mar 99
cx      endif
!
        lmax = 0
        kp   = min (kont(2,n),llmax)
        do l=1, kp

cx  we are hardwiring confidence now .... bs 9/30/97
cx  should be disabled for 1 degree data ... bs 9/30/97
cx	  konf(l,n)=1
          if (konf(l,n) .gt. 0 .and. konf(l,n) .le. 3 ) then
!
!                    confidence good enough for A-DECK output
!
            lmax = l
          else
            exit
          endif
        enddo
        write(*,*) 'For ',cycid(n),'  A-taus=',lmax,
     &             '  P-taus=',kont(2,n)
        ioe = 999              !  set open flag
        do j=1, jt
!
!                   PROCESS NGPS and NORAPS for A-DECK format
!
          do k=1, 5
            lat(k) = 0
            lon(k) = 0
cx  We are now only doing every 12 hours (we don't have every 6 hours) .. bs
cx          m      = nps(k,j)        ! set index
            m      = npr(k)        ! set index
            if (m .le. lmax) then
!
!                 prior and present confidence good enough for A-DECK
!
              if (cb .ne. 'SH') then
                if (flat(m,n) .gt. 0.0 .and. flat(m,n) .lt. 80.0)
     &             lat(k) = anint (10.0*flat(m,n))
              else
                if (flat(m,n) .lt. 0.0 .and. flat(m,n) .gt. -80.0)
     &             lat(k) = anint (10.0*flat(m,n))
              endif
              if (flon(m,n) .gt. 0.0 .and. flon(m,n) .lt. 360.0)
     &          lon(k) = anint (amod ((10.0*(360.0 -flon(m,n))),
     &                   3600.0))
              if (lat(k) .eq. 0) lon(k) = 0
              if (lon(k) .eq. 0) lat(k) = 0
            endif
          enddo
          if (ioe .eq. 999) then
            mu  = nout
	    ioe = 0
          endif
!
          if (lat(1) .eq. 0 .or. lat(2) .eq. 0) cycle
!
          if (ioe .eq. 0) then
!
!                     write NORAPS and NOGAPS forecasts
!
             do ii=1,numtau
                ltlnwnd(ii,1) = 0
                ltlnwnd(ii,2) = 0
                ltlnwnd(ii,3) = 0
             enddo
             if (cb .ne. 'SH') then
cajs          write (mu,602,iostat=ioe,err=706) cstatx, fdtg(j)(3:10),
cajs &          lat(1),lon(1), lat(2),lon(2), lat(3),lon(3),
cajs &          lat(4),lon(4), lat(5),lon(5),
cajs &          cb,cycid(n)(1:2),fdtg(j)(3:4)
ca602         format (a6,a8,10i4,'  0  0  0  0  0 ',3a2)
               do ii=1, 5
                  ltlnwnd(ii,1) = lat(ii)
                  ltlnwnd(ii,2) = lon(ii)
                  ltlnwnd(ii,3) = 0
               enddo
               call writeAid( mu, strmid, century, fdtg(j)(3:10), 
     &                       cstatx(3:6), ltlnwnd )
            else
cajs          write (mu,602,iostat=ioe,err=706) cstatx, fdtg(j)(3:10),
cajs &          lat(1),lon(1), lat(2),lon(2), lat(3),lon(3),
cajs &          lat(4),lon(4), lat(5),lon(5),
cajs &          cb,cycid(n)(1:2),cayr(3:4)
               do ii=1, 5
                  ltlnwnd(ii,1) = lat(ii)
                  ltlnwnd(ii,2) = lon(ii)
                  ltlnwnd(ii,3) = 0
               enddo
               call writeAid( mu, strmid, century, fdtg(j)(3:10), 
     &                       cstatx(3:6), ltlnwnd )
            endif
          else
	    write (*,*) '--- No Adeck Produced, Confidence Problem ---'
	    write (*,*) ' Enter forecast manually if locations valid '
          endif
        enddo
        if (jt .eq. 3 .and. ioe .eq. 0) then
          do j=1, jt
!
!                 PROCESS NGPX FOR A-DECK FORMAT
!
            do k=1, 5
              lat(k) = 0
              lon(k) = 0
              m      = npx(k,j)
              if (m .le. lmax) then
!
!                   prior and present confidence good enough for A-DECK
!
                if (cb .ne. 'SH') then
                  if (flat(m,n) .gt. 0.0 .and. flat(m,n) .lt. 80.0)
     &              lat(k) = anint (10.0*flat(m,n))
                else
                  if (flat(m,n) .lt. 0.0 .and. flat(m,n) .gt. -80.0)
     &              lat(k) = anint (10.0*flat(m,n))
                endif
                if (flon(m,n) .gt. 0.0 .and. flon(m,n) .lt. 360.0)
     &           lon(k) = anint (amod ((10.0*(360.0 -flon(m,n))),
     &                    3600.0))
                if (lat(k) .eq. 0) lon(k) = 0
                if (lon(k) .eq. 0) lat(k) = 0
              endif
            enddo
            if (lat(1) .ne. 0 .and. lat(2) .ne. 0) then
!
!                 WRITE NGPX FORECASTS IN A-DECK FORMAT FOR DDN
!
              if (cb .ne. 'SH') then
cajs            write (mu,602,iostat=ioe,err=706) cnikio(4),
cajs &           fdtg(j)(3:10), lat(1),lon(1), lat(2),lon(2),
cajs &           lat(3),lon(3), lat(4),lon(4), lat(5),lon(5),
cajs &           cb,cycid(n)(1:2),fdtg(j)(3:4)
                 do ii=1, 5
                    ltlnwnd(ii,1) = lat(ii)
                    ltlnwnd(ii,2) = lon(ii)
                    ltlnwnd(ii,3) = 0
                 enddo
                 call writeAid( mu, strmid, century, fdtg(j)(3:10), 
     &                         cnikio(3)(3:6), ltlnwnd )
              else
cajs            write (mu,602,iostat=ioe,err=706) cnikio(4),
cajs &           fdtg(j)(3:10), lat(1),lon(1), lat(2),lon(2),
cajs &           lat(3),lon(3), lat(4),lon(4), lat(5),lon(5),
cajs &           cb,cycid(n)(1:2),cayr(3:4)
                 do ii=1, 5
                    ltlnwnd(ii,1) = lat(ii)
                    ltlnwnd(ii,2) = lon(ii)
                    ltlnwnd(ii,3) = 0
                 enddo
                 call writeAid( mu, strmid, century, fdtg(j)(3:10), 
     &                         cnikio(3)(3:6), ltlnwnd )
              endif
            endif
          enddo
        endif
        if (ioe .eq. 0) then
          write (*,9099)
 9099     format('*END')
!
!                   WRITE FORECASTS IN PLAIN LANGUAGE FORMAT
!
cx  changed write to standard output ... bs 9/29/97
          write (*,603,iostat=ioe,err=706) cstatx(3:6)
  603     format (/,15x,a4,' OUTPUT')
!                   WRITE DTG, CYCLONE NUMBER AND BASIN CODE
!                   and column HEADERS
          write (*,604,iostat=ioe,err=706) cdtg(3:10),cycid(n)(1:2),cs
  604     format (9x,a8,6x,'STM ',a2,a1,/,
     &    2x,'TAU',3x,'LAT',3x,'LON',4x,'CONF',3x,'SFCP',6x,'LTLN 850',
     &    7x,'LTLN 700',7x,'LTLN 500')
!
!                   WRITE LOCATION STARTING AT TAU 0, FOR EVERY 6 HOURS
!                         (suainfo missing for tau 102 & 114)
!
          if (nrd .eq. 65) then
            if (cidsua(n) .eq. cycid(n)) then
              nadd = -1
            else
              write (*,*) 'CYCLONE error, looking for ',cidsua(n),
     &        ' found ', cycid(n)
              nadd = 0
            endif
          else
            nadd = 0
          endif
          kp = min0 (nf,kont(2,n) +1)
          do k=1, kp
cx  now we are only doing 12 hourly data .. bs 9/30/97
cx          itau = 6*(k -1)
            itau = 12*(k -1)
            cns  = ' '
            cew  = ' '
            plat = flat(k,n)
!                   SET BAD LATITUDE TO ZERO
            if (cb .ne. 'SH') then
              if (plat .lt. 0.0) plat = 0.0
              if (plat .ne. 0.0) cns = 'N'
            else
              if (plat .gt. 0.0) plat = 0.0
              if (plat .ne. 0.0) cns = 'S'
              if (cns .eq. 'S') plat = abs (plat)
            endif
            plon = flon(k,n)
!                   SET BAD LONGITUDE TO ZERO
            if (plon .lt. 0.0 .or. plon .gt. 360.0) plon = 0.0
            if (plon .le. 180.0 .and. ni87 .eq. 1) then
              if (plon .ne. 0.0) cew = 'E'
            else
              if (plon .ne. 0.0) then
                plon = 360.0 -plon
                cew = 'W'
              endif
            endif
!
!                   LOAD CONFIDENCE FACTOR
!
            konfm = konf(k,n)
            if (plat .eq. 0.0 .or. plon .eq. 0.0) konfm = 0
            if (konfm .eq. 0) then
              plat = 0.0
              plon = 0.0
              cns  = ' '
              cew  = ' '
            endif
            if (nadd .eq. -1) then
!
!                   obtain supporting surface and U/A data
!
              call obsuafix (maxhr,maxtc,suadat,k,n,sfcp,rltln,cnsew)
              if ( k .ne. 18 .and. k .ne. 20) then
                write (*,605,iostat=ioe,err=706) itau,plat,cns,plon,cew
     &               ,konfm,sfcp,rlt85,cns1,rln85,cew1,rlt70,cns2,rln70
     &               ,cew2,rlt50,cns3,rln50,cew3
              else
!
!                     U/A data missing for TAUs 102 & 114
!
                write (*,605,iostat=ioe,err=706) itau,plat,cns,plon,cew
     &               ,konfm,sfcp
              endif
            else
              write (*,605,iostat=ioe,err=706) itau,plat,cns,plon,cew,
     &              konfm
            endif
          enddo
  605     format (1x,i3,3x,f4.1,a1,1x,f5.1,a1,4x,i1,3x,f6.1,
     &           3(3x,f4.1,a1,1x,f5.1,a1))
          write  (*,9099)
        endif
	ndpstx=ndpstx+1
      enddo
!
  200 continue
      write (*,*) 'qctrack wrote ',ndpstx,' messages'
      return
!
!                   ERROR SECTION
!
  706 continue
      print *, ' $ $ $ WRITE ERROR ON OUTPUT FILE is ',ioe
      ierr = -1
      goto 200
!
      end
      subroutine prctcd (bogus,tcdat,nf,nc,kont,cycid,flat,flon,konf,
     &                   ierr)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)prctcd.f90	1.1 6/14/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  PRCTCD
!
!  DESCRIPTION:  PROCESS TROPICAL CYCLONE TRACKING DATA
!
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL PRCTCD (BOGUS,TCDAT,NF,NC,KONT,CYCID,FLAT,FLON,KONF,
!                       IERR)
!
!  PARAMETERS:
!     NAME       TYPE     USAGE           DESCRIPTION
!   --------     ----     -----    -------------------------------------
!    BOGUS       CHAR       IN     BOGUS POSITION DATA
!    TCDAT       CHAR       IN     TROPICAL CYCLONE TRACKING DATA
!       NF        INT       IN     MAXIMUM NUMBER OF FORECAST POSITIONS
!       NC        INT       IN     NUMBER OF TROPICAL CYCLONE TRACKS
!     KONT        INT       IN     ARRAY OF MAX FORECAST POSITIONS
!    CYCID       CHAR       IN     T. C. NUMBER AND ORIGIN BASIN
!     FLAT       REAL      OUT     FORECAST LATITIUDE, +NH, -SH
!     FLON       REAL      OUT     FORECAST LONGITUDE, 0 - 360 EAST
!     KONF        INT      OUT     CONFIDENCE INDICATOR
!     IERR        INT      OUT     ERROR FLAG
!
!  COMMON BLOCKS:  NONE
!
!  FILES:  NONE
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        -----------------------------------------
!     BAD DATA                 TERMINATE PROCESSING THAT CYCLONE
!
!  ADDITIONAL COMMENTS:
!     FORMAT OF BOGUS AND TCDAT:
!
!       BOGUS DATA:
!                  1         2
!         1234567890123456789012345
!          NNB LAT   LON   HEAD SPD
!          36W 259N 1584E  2856 112
!
!       TCDAT DATA:
!                  1         2         3         4
!         1234567890123456789012345678901234567890
!          TAU CID -LAT   LON    HEAD   SPD  K J I
!          *** 36W  25.9  158.4  285.6  11.2 0 0 0  - BOGUS LINE
!          000 36W  25.5  158.5  285.6  11.2 1 4 8  - TAU ZERO
!
!   TAU    - FORECAST PERIOD IN HOURS
!   CID    - CYCLONE NUMBER AND SINGLE LETTER BASIN INDICATOR
!   LAT    - +NH, -SH, DEG
!   LON    - 0 TO 360 DEGREES EAST
!   HEAD   - HEADING OF CYCLONE, DEG
!   SPD    - SPEED OF MOVEMENT, KT
!   K      - CONFIDENCE RATING:
!               0 - NOT RATED
!               1 - ONLY ONE CYCLONE IN AREA
!     ******  ALL THE FOLLOWING HAVE 2 OR MORE CYCLONES IN SEARCH AREA
!               2 - CYCLONE SELECTED IS CLOSEST TO BOTH EP & LKL
!                     AND HAS THE HIGHER WIND SPEED
!               3 - CYCLONE SELECTED IS CLOSEST TO EITHER EP OR
!                     LKL WITH GOOD WIND SUPPORT AND SPEED
!               4 - CYCLONE SELECTED IS CLOSEST TO EITHER EP OR
!                     LKL WITH BEST WIND AND INTERSECTION SUPPORT
!               5 - CYCLONE SELECTED IS CLOSEST TO EITHER EP OR
!                     LKL WITH HIGHEST WIND SPEED
!               6 - CYCLONE SELECTED HAS HIGHEST WIND SPEED
!   J      - WIND SUPPORT NUMBERS IN QUADRANTS, WILL BE 3 OR 4
!   I      - INTERSECTION SUPPORT NUMBER (NUMBER OF INTERSECTIONS USED
!            TO ESTABLISH POSITION), WILL BE FROM 2 TO 8
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          NAME           DESCRIPTION
!         -------     ----------------------
!          CHRCHK     CHECK FOR ALL DIGITS BETWEEN KS AND KT
!         CHKBDAT     CHECK DATA THAT MAY BE BAD
!         CHKCDAT     CHECK DATA THAT IS PROBABLY CORRECT
!
!  LOCAL VARIABLES:
!      NAME      TYPE                 DESCRIPTION
!     ------     ----       ----------------------------------
!       BHED     REAL       BOGUS HEADING, DEG
!       BLAT     REAL       BOGUS LATITUDE, DEG
!       BLON     REAL       BOGUS LONGITUDE, DEG
!       BSPD     REAL       BOGUS SPEED OF MOVEMENT, KT
!       FHED     REAL       FORECAST HEADING, DEG
!       FSPD     REAL       FORECAST SPEED OF MOVEMENT, KT
!     IKNVRT      INT       CONVERSION FLAG, -1 CONVERT TO REAL/INTEGER
!         KI      INT       INTERSCETION SUPPORT FACTOR
!         KJ      INT       WIND SUPPORT FACTOR
!         KK      INT       CONFIDENCE FACTOR
!         KL      INT       ENDING CHARACTER POSITION
!         KO      INT       COUNT OF OK POSITIONS
!         KS      INT       STARTING CHARACTER POSITION
!         LK      INT       LACK OF GOOD CONFIDENCE INDICATOR
!       LOAD      INT       LOAD FLAG, -1 LOAD
!      MXFCP      INT       MAX NUMBER OF FORECAST CYCLONE POSITIONS
!       MXNF      INT       MAX NUMBER OF FORECASTS
!       MXTC      INT       MAX NUMBER OF TROPICAL CYCLONES
!         ND      INT       NUMBER OF DIGITS
!     NEARLY      INT       NUMBER OF EARLY CUT-OFFS
!         NO      INT       NUMBER OF OTHER CHARACTERS
!         NP      INT       NUMBER OF PERIODS
!       PHED     REAL       PROSPECTIVE HEADING, DEG
!       PLAT     REAL       PROSPECTIVE LATITUDE, DEG
!       PLON     REAL       PROSPECTIVE LONGITUDE, DEG
!       PSPD     REAL       PROSPECTIVE SPEED OF MOVEMENT, KT
!     RBOGUS     REAL       REAL BOGUS VALUES OF LAT, LON, HEAD, SPEED
!
!  METHOD: N/A
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
!
!  MAKEFILE:  N/A
!
!  RECORD OF CHANGES:
!
!    <<change notice>>  (19 JUN 1996)  Hamilton, H.
!      initial installation on OASIS
!
!...................END PROLOGUE.......................................
!
      implicit none
!
!         FORMAL PARAMETERS
      integer nf,nc, kont(2,nc), konf(nf,nc), ierr
      character bogus(nc)*25, tcdat(nf,nc)*40, cycid(nc)*3
      real flat(nf,nc), flon(nf,nc)
!
!         LOCAL VARIABLES
      integer mxtc, mxnf
      parameter (mxtc = 9,  mxnf = 25)
!
      integer nearly, mxfcp, ko, lk, ks, kl, nd, np ,no, iknvrt, load
      integer kk, kj, ki, n, k, nn
      integer kwdit(2,mxnf)
      real blat, blon, bhed, bspd, plat, plon, phed, pspd
      real fhed(mxnf), fspd(mxnf), rbogus(4,mxtc)
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      nearly = 0
      mxfcp  = 0
      do n=1, nc
        ko = 0
        lk = 0
        write (*,*) 'PROCESSING ',kont(1,n),' POSITIONS OF CYCLONE ',
     &               cycid(n)
!
!  * * * * * *      PROCESS BOGUS DATA      * * * * * *
!
!                     SET TO MISSING VALUES
!
        blat =  99.9
        blon = 999.9
        bhed = -99.9
        bspd = -99.9
!                         PERFORM LATITUDE CHECK
        ks = 6
        kl = 8
        call chrchk (ks,kl,bogus(n),nd,np,nn,no)
        if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
          read (bogus(n)(6:8),9003) blat
 9003     format (f3.1)
          if (bogus(n)(9:9) .eq. 'S') then
            blat = -blat
          elseif (bogus(n)(9:9) .ne. 'N') then
            blat = 99.9
          endif
!                         PERFORM LONGITUDE CHECK
          ks = 11
          kl = 14
          call chrchk (ks,kl,bogus(n),nd,np,nn,no)
          if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
            read (bogus(n)(11:14),9004) blon
 9004       format (f4.1)
            if (bogus(n)(15:15) .eq. 'W') then
              blon = 360.0 -blon
            elseif (bogus(n)(15:15) .ne. 'E') then
              blon = 999.9
              blat =  99.9
            endif
          else
            write (*,*) 'FAILED INITIAL CHECK, LON= ',bogus(n)(11:14)
          endif
        else
          write(*,*) 'FAILED INITIAL CHECK, LAT= ',bogus(n)(6:8)
        endif
        if (abs (blat) .lt. 90.0) then
!                     PERFORM HEADING CHECK
          ks = 18
          kl = 21
          call chrchk (ks,kl,bogus(n),nd,np,nn,no)
          if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
            read (bogus(n)(18:21),9004) bhed
!                       PERFORM SPEED CHECK
            ks = 23
            kl = 25
            call chrchk (ks,kl,bogus(n),nd,np,nn,no)
            if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
              read (bogus(n)(23:25),9003) bspd
            else
              write(*,*) 'FAILED INITIAL CHECK, SPEED= ',bogus(n)(23:25)
            endif
          else
            write(*,*) 'FAILED INITIAL CHECK, HEAD= ',bogus(n)(18:21)
          endif
        endif
!
!                   LOAD REAL BOGUS VALUES
!
        rbogus(1,n) = blat
        rbogus(2,n) = blon
        rbogus(3,n) = bhed
        rbogus(4,n) = bspd
!
!  * * * * * *      CHECK FORECAST VALUES    * * * * * *
!
        ko = 0
        lk = 0
        do k=1, kont(1,n)
          iknvrt = 0
!                   PERFORM LATITUDE CHECK
          ks = 10
          kl = 14
          call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
          if (nd.ge.1 .and. np.eq.1 .and. no.eq.0) then
!                     PERFORM LONGITUDE CHECK
            ks = 17
            kl = 21
            call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
            if (nd.ge.1 .and. np.eq.1 .and. no.eq.0) then
!                     PERFORM HEADING CHECK
              ks = 24
              kl = 28
              call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
              if (nd.ge.1 .and. np.eq.1 .and. no.eq.0) then
!                       PERFORM SPEED CHECK
                ks = 31
                kl = 34
                call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
                if (nd.ge.1 .and. np.eq.1 .and. no.eq.0) then
!                         PERFORM CONFIDENCE CHECK
                  ks = 36
                  kl = 36
                  call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
                  if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
!                           PERFORM WIND SUPPORT CHECK
                    ks = 38
                    kl = 38
                    call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
                    if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
!                           PERFORM INTERSECTION SUPPORT CHECK
                      ks = 40
                      kl = 40
                      call chrchk (ks,kl,tcdat(k,n),nd,np,nn,no)
                      if (nd.ge.1 .and. np.eq.0 .and. no.eq.0) then
                        iknvrt = -1
                      endif
                    endif
                  endif
                endif
              endif
            endif
          endif
          if (iknvrt .eq. -1) then
!
!                   CONVERT FROM CHARACTER TO REAL/INTEGER
!
            read (tcdat(k,n),9010) plat, plon, phed, pspd, kk, kj, ki
 9010       format (9x,f5.1,2x,f5.1,2x,f5.1,2x,f4.1,3(1x,i1))
            load = 0
            if (abs (plat) .lt. 90.0) then
!
!                   LATITUDE IS GOOD, SO CHECK CONFIDENCE
!
              if (kk .gt. 2) lk = -1   ! "BAD" CHECKING WILL BE REQUIRED
!
!                     LOAD OUTPUT VALUES
!
              ko = ko +1
              flat(ko,n)  = plat
              flon(ko,n)  = plon
              konf(ko,n)  = kk
              fhed(ko)     = phed
              fspd(ko)     = pspd
              kwdit(1,ko) = kj
              kwdit(2,ko) = ki
            else
              write(*,*) 'NO LOAD OF ',tcdat(k,n)
            endif
          else
!
!                   BAD DATA, STOP PROCESSING THIS CYCLONE
!
            if (tcdat(k,n)(11:14) .ne. '99.9') then
              write (*,*) 'BAD DATA AT K= ',k
              write (*,*) 'DATA= ',tcdat(k,n)
            endif
            nearly = nearly +1
            exit
!
          endif
        enddo
!
!                   SET INITIAL COUNT FOR CCRS OUTPUT
!
        kont(1,n) = ko
!
!                   SET COUNT FOR PLAIN LANGUAGE OUTPUT
!
        kont(2,n) = ko
        write (*,*) ' FOR CYCLONE ',cycid(n),' HAVE ',kont(1,n),
     &              ' CONVERSIONS'
        if (kont(1,n).gt.0 .and. lk.eq.-1) then
!
!                   THERE IS ONE OR MORE QUESTIONABLE POSITIONS TO BE
!                   CHECKED
!
          call chkbdat (rbogus(1,n),nf,flat(1,n),flon(1,n),fspd, 
     &                  konf(1,n),kont(1,n))
          write(*,*) 'BACK FM CHKBDAT - RETAINED ',kont(1,n)
        endif
        if (kont(1,n) .gt. 0) then
!
!                   THERE IS ONE OR MORE POSITIONS TO BE CHECKED
!
          call chkcdat (rbogus(1,n),nf,flat(1,n),flon(1,n),fhed,fspd,
     &                  konf(1,n),kwdit,kont(1,n))
          write(*,*) 'BACK FM CHKCDAT - RETAINED ',kont(1,n)
        endif
        mxfcp = max0 (mxfcp,kont(1,n),kont(2,n))
        write (*,*) 'CYCLONE ',cycid(n),' HAS ',kont(1,n),' GOOD POINTS'
      enddo
      if (mxfcp .ge. 1) then
!
!                   THERE IS AT LEAST ONE INITIAL POSITION FOUND
!
        ierr = 0
      else
        write (*,*) 'THERE ARE NO INITIAL POSITION(S)'
        ierr = -1
      endif
!
      end
      subroutine redtctd (tcdat,maxf,ntct,kont,cycid,cdtg,bogus,ierr)
!
!..........................START PROLOGUE..............................
!
!  SCCS IDENTIFICATION:  @(#)redtctd.f90	1.1 6/14/96
!
!  CONFIGURATION IDENTIFICATION:
!
!  MODULE NAME:  REDTCTD
!
!  DESCRIPTION:  READ NOGAPS TROPICAL CYCLONE TRACKING DATA
!
!
!  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
!                              U.S. GOVERNMENT DOMAIN
!                              ALL RIGHTS RESERVED
!
!  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
!                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
!                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
!
!  REFERENCES:
!
!  CLASSIFICATION:  UNCLASSIFIED
!
!  RESTRICTIONS:
!
!  COMPUTER/OPERATING SYSTEM
!               DEPENDENCIES:  Sun/Solaris
!
!  LIBRARIES OF RESIDENCE:
!
!  USAGE:  CALL REDTCTD (TCDAT,MAXF,NTCT,KONT,CYCID,CDTG,BOGUS,IERR)
!
!  PARAMETERS:
!     NAME        TYPE     USAGE             DESCRIPTION
!   --------      ----     -----     ----------------------------------
!    TCDAT        CHAR      OUT      T. C. TRACKING DATA ARRAY
!     MAXF         INT      IN       FIRST DIMENSION OF TCDAT
!     NTCT         INT     IN/OUT    SECOND DIMENSION OF TCDAT / NUMNBER
!                                    OF TROPICAL CYCLONES TRACKED
!     KONT         INT      OUT      ARRAY OF MAXIMUM FORECASTS
!    CYCID        CHAR      OUT      T. C. NUMBER AND ORGIN BASIN FLAG
!     CDTG        CHAR      OUT      DATE-TIME-GROUP OF FORECAST START
!    BOGUS        CHAR      OUT      NOGAPS T. C. BOGUS DATA
!     IERR         INT      OUT      ERROR FLAG, 0 - NO ERROR
!
!  COMMON BLOCKS:  NONE
!
!  FILES:
!    NAME     UNIT  FILE TYPE  ATTRIBUTE  USAGE         DESCRIPTION
!   -------  -----  ---------  ---------  ------   ---------------------
!   TCTRCKS   10    PERMANENT  SEQUENTIAL   IN     T. C. TRACKING DATA
!
!  DATA BASES:  NONE
!
!  NON-FILE INPUT/OUTPUT:  NONE
!
!  ERROR CONDITIONS:
!         CONDITION                 ACTION
!     -----------------        ----------------------------
!     I/O READ ERROR           DIAGNOSTIC, SET ERROR FLAG
!     EARLY EOF                DIAGNOSTIC, SET ERROR FLAG
!     BAD DATA                 DIAGNOSTIC, SET ERROR FLAG
!
!  ADDITIONAL COMMENTS:
!       FORMAT OF TROPICAL CYCLONE TRACKING DATA FILE
!         FIRST LINE
!                  1         2
!         12345678901234567890
!          NNN YYYYMMDDHH
!
!         BOGUS DATA
!                  1         2
!         1234567890123456789012345
!          NNB LAT   LON   HEAD SPD
!          37W 101N 1501E  2827 091
!
!         FORECAST DATA
!                  1         2         3         4
!         1234567890123456789012345678901234567890
!          TAU NNB -LATI  LONGI  HEAD   SPD  K J I
!          *** 37W  10.1  150.1  282.7   9.1 0 0 0 - BOGUS LINE
!          000 37W  10.1  150.5  282.7   9.1 2 4 8 - TAU ZERO
!
!...................MAINTENANCE SECTION................................
!
!  MODULES CALLED:
!          NAME           DESCRIPTION
!         -------     ----------------------
!         CHKNUM      CHECK FOR DIGITS
!
!  LOCAL VARIABLES:
!        NAME      TYPE                 DESCRIPTION
!       ------     ----       ------------------------------------------
!         CARD     CHAR       WORKING CHARACTER STRING
!          IOE      INT       SIMULATED I/O ERROR FLAG
!           KS      INT       STARTING CHARACTER LOCATION
!           KT      INT       ENDING CHARACTER LOCATION
!         NCYT      INT       NUMBER OF TROPICAL CYCLONES TRACKED
!         NCTR      INT       NUMBER OF CYCLONES TRACKED READ
!         NDIG      INT       NUMBER OF DIGITS
!
!  METHOD:  N/A
!
!  INCLUDE FILES:  NONE
!
!  COMPILER DEPENDENCIES:  Fortran 90
!
!  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
!
!  MAKEFILE:  N/A
!
!  RECORD OF CHANGES:
!
!    <<change notice>>  V1.1  (19 JUN 1996)  Hamilton, H.
!      initial installation on OASIS
!
!...................END PROLOGUE.......................................
!
       implicit none
!
!         FORMAL PARAMETERS
      integer maxf, ntct, ierr, kont(2,ntct)
      character tcdat(maxf,ntct)*40, cycid(9)*3, cdtg*10, bogus(ntct)*25
!
!         LOCAL VARIABLES
      integer ioe, j, k, ks, kt, n, ndig, ncyt, nctr
      character*40 card
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
      ncyt = 0
      nctr = 0
      ioe  = 0
      card = ' '
!
!                   READ FIRST LINE, OBTAIN NUMBER OF TRACKS AND DTG
!
      read (10,9040,err=705,end=710) card
 9040 format (a40)
      ks = 2
      kt = 4
      call chknum (card,ks,kt,ndig)
      if (ndig .eq. 3) then
        read (card(ks:kt),'(I3)') ncyt
        write (*,*) 'PROCESSING ',ncyt,' CYCLONE TRACKS'
        if (ncyt .gt. 0) then
          ncyt = min0 (ncyt,ntct)
          ks = 6
          kt = 15
	  call chknum (card,ks,kt,ndig)
          if (ndig .eq. 10) then
!
!                 OBTAIN STARTING DTG OF TRACKING DATA
!
            cdtg = card(ks:kt)
          else
!                 SIGNAL READ ERROR
            ioe = 5
          endif
        endif
      else
!                 SIGNAL READ ERROR
        ioe = 5
      endif
      if (ioe .eq. 0) then
!
!                 READ BOGUS DATA, SAVE FOR POSSIBLE QC
!
        do n=1, ncyt
          card = ' '
          read (10,9040,err=705,end=710) card
          bogus(n) = card(1:25)
        enddo
!
!                 READ TRACKING DATA
!
        card = ' '
        do n=1, ncyt
  115     continue
          if (card(2:4) .ne. '***') then
!
!                 LOOKING FOR HEADER
!
            card = ' '
            read (10,9040,err=705,end=710) card
            goto 115
!
          endif
          cycid(n) = card(6:8)
          j = 0
          do k=1, maxf
            card = ' '
            read (10,9040,err=705,end=710) card
            if (card(2:2).lt.'0' .or. card(2:2).gt.'9') then
!
!                 FOUND ENDING DIAGNOSTICS OR NEXT HEADER
!
              kont(1,n) = k -1
              write (*,*) 'FOUND ',kont(1,n),' POSITIONS FOR ',cycid(n)
              nctr = nctr +1
              goto 130
!
            endif
            if (card(6:8) .eq. cycid(n)) then
              j = j +1
              tcdat(j,n) = card
            else
              write (*,*) 'ERROR, FOUND ',card(6:8),' LOOKING FOR ', 
     &                     cycid(n),' N= ',n
            endif
          enddo
          kont(1,n) = maxf
          write (*,*) 'FOUND ',kont(1,n),' POSITIONS FOR ',cycid(n)
          nctr = nctr +1
  130     continue
        enddo
      endif
  200 continue
      if (nctr .lt. ncyt) write (*,*) 'PROCESSED ',nctr,' OF ',ncyt,
     &    ' TRACKS'
      ntct = nctr
      ierr = ioe
      return
!
  705 continue
      write (*,*) ' READ ERROR ON INPUT TRACKING DATA FILE'
      ioe = 5
      goto 200
!
  710 continue
      write (*,*) ' EARLY EOF ON INPUT TRACKING DATA FILE'
      ioe = -1
      goto 200
!
      end
