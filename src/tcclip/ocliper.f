cx      PROGRAM OCLIPR
C
C........................START PROLOGUE.................................
C
C  PROGRAM NAME:  OCLIPR
C
C  DESCRIPTION:  USING INPUT FROM THE CARQ MESSAGE (TAPE20) GENERATE
C                CLIPER FORECAST (TAPE40) FOR ALL BUT WESTERN NORTH PAC
C                   NORTH INDIAN OCEAN     (NSIND =  1),
C                   CENTRAL NORTH PACIFIC  (NSIND =  3),
C                   EASTERN NORTH PACIFIC  (NSIND =  4),
C                   SOUTHWEST INDIAN OCEAN (NSIND = -1),
C                   SOUTHEAST INDIAN OCEAN (NSIND = -2), OR
C                   SOUTH PACIFIC OCEAN    (NSIND = -3)
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON  (MM -GSA), JUNE 90
C
C  CURRENT PROGRAMMER:         BUCK SAMPSON, NRL
C
C  CLASSIFICATION:             UNCLASSIFIED
C
C  USAGE:                      OCLIPR WP0190
C
C  INPUT FILES:
C     b????.dat  - TROPICAL CYCLONE PRESENT AND PAST LOCATIONS
C
C  OUTPUT FILES:
C     to screen  - CLIPER FORECAST, EVERY 12 HRS IN PLAIN TEXT FORMAT 
C     wptot.dat  - same as above in adeck format (missing 60 hr fcst)
C
C  ERROR CONDITIONS:  ABORT PROGRAM IF WRONG BASIN OR MISSING CYCLONE
C        INFORMATION. NOTE, -24 HOUR POSITION IS NOT REQUIRED.
C
C........................MAINTENANCE SECTION............................
C
C  BRIEF DESCRIPTION OF PROGRAM MODULES:
C     FIXPRD - ROUTINE TO CALCULATE 35 PREDICTORS
C     CLDXDY - ROUTINE TO APPLY REGRESSION COEFFICIENTS TO PREDICTORS
C              TO CALCULATE DX (LONGITUDE, N.M.) AND DY (LATITUDE, N.M.)
C              DISPLACEMENTS.
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     AIDNM  - OBJECTIVE FORECAST AIDE NAME
C     ALT    - AVERAGE LATITUDE BETWEEN TWO POSITIONS
C     CARD   - 80 CHARACTERS OF CARQ INPUT
C     CBASN1 - ONE LETTER DESIGNATION OF BASIN
C     CBASN2 - TWO LETTER BASIN INDICATOR
C     CEW    - LONGITUDE INDICATOR, E FOR EAST W FOR WEST
C     CMMDD  - CHARACTER OF MONTH (MM) AND DAY (DD)
C     CNAME  - CYCLONE NAME (APLHA-NUMERIC DESIGNATION)
C     CNS    - LATITUDE INDICATOR, N FOR NORTH, S FOR SOUTH
C     CNMDEG - INVERSE OF NAUTICAL MILES PER DEGREE OF LATITUDE OR
C              LONGITUDE (AT EQUATOR)
C     CSTRMK - STORM NUMBER, FOR GIVEN BASIN
C     CYCNAM - CYCLONE NAME (NUMBER AND ONE LETTER BASIN INDICATOR)
C     CYEAR  - YEAR (LAST TWO NUMBERS)
C     DEGRAD - CONVERSION FOR DEGREES TO RADIANS
C     DX     - CALCULATED LONGITUDE DISPLACEMENTS (N.M.)
C     DY     - CALCULATED LATITUDE  DISPLACEMENTS (N.M.)
C     EW12   - LONGITUDE INDICATOR FOR 12-HOUR OLD POSITION
C     EW24   - LONGITUDE INDICATOR FOR 24-HOUR OLD POSITION
C     FLAT   - LATITUDE  OF PRESENT POSITION
C     FLN12  - FORECAST 12-HOUR LONGITUDE
C     FLN24  - FORECAST 24-HOUR LONGITUDE
C     FLN36  - FORECAST 36-HOUR LONGITUDE
C     FLN48  - FORECAST 48-HOUR LONGITUDE
C     FLN60  - FORECAST 60-HOUR LONGITUDE
C     FLN72  - FORECAST 72-HOUR LONGITUDE
C     FLN    - PRESENT LONGITUDE IN DEGREES EAST (360 -FLON FOR WEST)
C     FLON   - LONGITUDE OF PRESENT POSITION
C     FLT12  - FORECAST 12-HOUR LATITUDE
C     FLT24  - FORECAST 24-HOUR LATITUDE
C     FLT36  - FORECAST 36-HOUR LATITUDE
C     FLT48  - FORECAST 48-HOUR LATITUDE
C     FLT60  - FORECAST 60-HOUR LATITUDE
C     FLT72  - FORECAST 72-HOUR LATITUDE
C     FP     - ARRAY OF FORECAST LATITUDE AND LONGITUDE POSITIONS
C     ICNAM  - INDICATOR FOR FINDING NAME, 0 NOT FOUND
C     ICDTG  - INDICATOR FOR FINDING DATE-TIME-GROUP, 0 NOT FOUND
C     ICFIX  - INDICATOR FOR FINDING PRESENT LOCATION, 0 NOT FOUND
C     ICP12  - INDICATOR FOR FINDING -12 HOUR POSITION, 0 NOT FOUND
C     ICP24  - INDICATOR FOR FINDING -24 HOUR POSITION, 0 NOT FOUND
C     IDAY   - NUMBER OF DAY OF MONTH FOR PRESENT POSITION
C     IFP    - ROUNDED INTEGER OF LATITUDE AND LONGITUDE TIMES 10
C     IHR    - NUMBER OF HOURS IN DAY FOR PRESENT POSITION
C     ISTOP  - INDICATOR FOR PROGRAM TERMINATION, -1 TERMINATE
C     IT     - NUMBER OF POSITIONS FOR OUTPUT
C     IYR    - LAST TWO DIGITS OF YEAR
C     MON    - NUMBER OF MONTH FOR PRESENT POSITION
C     NSIND  - INDICATOR FOR BASIN, SEE ABOVE
C     P      - ARRAY OF PREDICTOR VALUES
C     PLAT12 - LATITUDE  OF 12-HOUR OLD POSITION
C     PLAT24 - LATITUDE  OF 24-HOUR OLD POSITION, ZERO MEANS MISSING
C     PLON12 - LONGITUDE OF 12-HOUR OLD POSITION
C     PLON24 - LONGITUDE OF 24-HOUR OLD POSITION, ZERO MEANS MISSING
C     JWIND  - MAXIMUM SUSTAINED WIND, NOT FOECAST - SET TO ZEROES
C
C  REFERENCES:
C  1.  STATISTICAL PREDICTION OF TROPICAL STORM MOTION OVER THE BAY OF
C      BENGAL AND ARABIAN SEA, CHARLES J. NEUMANN AND G. S. MANDAL,
C      INDIAN J. MET. HYDROL. GEOPHYS., (1978),29,3,487-500.
C
C  2.  STATISTICAL PREDICTION OF TROPICAL CYCLONE MOTION OVER THE
C      SOUTHWEST INDIAN OCEAN, CHARLES J. NEUMANN AND ELIE A.
C      RANDRIANARISON, MONTHLY WEATHER REVIEW, (1976), VOL 104, 76-85.
C
C  METHOD:
C    1.  THE PUBLISHED REGRESSION COEFFICIENTS IN REFERENCE 1 APPEARED
C        TO HAVE ERRORS, SO THEY WERE REGENERATED BASED UPON THE BEST
C        TRACK DATA AVAILABLE ON FNOC COMPUTERS FROM 1945 TO 1988.
C    2.  THE FORMULATION OF THE PREDICTORS ARE THE SAME, EXCEPT THE
C        ORDER OF THE FIRST SEVEN PREDICTORS WERE MADE THE SAME AS
C        REFERENCE 2.
C    3.  REFERENCE 2 WAS IMPLEMENTED DIRECTLY FROM THE PUBLISHED REPORT.
C    4.  SAME EQUATIONS ARE USED FOR SOUTHEAST INDIAN OCEAN, SOUTH
C        PACIFIC, CENTRAL NORTH PACIFIC AND EASTERN NORTH PACIFIC.
C    4.  BASIC SEVEN PREDICTORS ARE EXPANDED TO 35 USING SECOND ORDER
C        POLYNOMIAL.
C    5.  REGRESSION COEFFICIENTS ARE MULTIPLIED BY THE PREDICTORS AND
C        "INTERCEPT" VALUES ARE ADDED TO CALCULATE THE DX AND DY
C        STATISTICAL FORECAST DISPLACEMENTS FOR EACH DESIRED FORECAST.
C    6.  NOTE, ONE OR MORE OF THE FIRST THREE PREDICTORS MAY BE BIASED
C        PRIOR TO BEING USED.
C
C  LANGAUGE:  FTN5 (FORTRAN77)
C
C  RECORD OF CHANGES:
C
C     <<CHANGE NOTICE>>  OCLIPR*01  (18 JULY 1990) -- HAMILTON, H.
C              ADD CHANGES TO INTEGRATE INTO CARQ WITH WPCLPR
C
C     <<CHANGE NOTICE>>  OCLIPR*02  (20 MAR 1991) -- HAMILTON, H.
C              CORRECT -24HR POSITION FLAG FOR SOUTH PACIFIC
C
C     <<CHANGE NOTICE>> (27 JUNE 1995) -- SAMPSON, B.
C              VERSION TO RUN ON ATCF 3.0
C
c     Modified to use new data format,  6/98   A. Schrader
c     Modified to use bt posit century  11/98  B. Sampson
C
C........................END PROLOGUE..................................
C
      include 'dataioparms.inc'

      character*100 storms,filename
      CHARACTER*80 CARD
      CHARACTER*8 CDTG,dtgm12,dtgm24
      CHARACTER*8 tdtg
      character*8 btdtg
      CHARACTER*6 CNAME,strmid
      CHARACTER*4 CMMDD,AIDNM
      CHARACTER*3 CYCNAM,JWIND
      CHARACTER*2 CBASN2,CSTRMK,CYEAR
      CHARACTER*1 CNS,CEW,FEW(6),CBASN1,EW12,EW24
      character*1 btns, btew
      character*1 cdummy
      character*2 century
      character*2 cent
      integer     ltlnwnd(numtau,llw)
      integer     ii, iarg
      integer     ibtwind, ios
      real        btlat, btlon
C
      DIMENSION P(35), DX(6), DY(6)
      DIMENSION FP(2,6),IFP(2,6)
C
      EQUIVALENCE (FP(1,1),FLT12), (FP(2,1),FLN12)
      EQUIVALENCE (FP(1,2),FLT24), (FP(2,2),FLN24)
      EQUIVALENCE (FP(1,3),FLT36), (FP(2,3),FLN36)
      EQUIVALENCE (FP(1,4),FLT48), (FP(2,4),FLN48)
      EQUIVALENCE (FP(1,5),FLT60), (FP(2,5),FLN60)
      EQUIVALENCE (FP(1,6),FLT72), (FP(2,6),FLN72)
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c  get the storms directory name
c
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c
c  get the storm id
c
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)

      call getarg(iarg,century)
      iarg = iarg + 1
c
c  write heading on output
c
      print *,'**************************************************'
      print *,'          ocliper forecast for ',strmid
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      open (20,file=filename,status='old',err=9001)
      write(filename,'(a,a)')storms(1:ind),"/wptot.dat"
      call openfile ( 60, filename, 'unknown', ioerror )
      if( ioerror .lt. 0 ) goto 9003
      rewind 20
cx    rewind 40
cx    rewind 60
c
c  go to the end of the output file
c
   20 continue
      read (60,'(a1)',end=25)cdummy
      go to 20
   25 continue
c
c  convert the 1st two characters of stormid to uppercase
c
      call upcase(strmid,6)
      cycnam(1:2)=strmid(3:4)
      cycnam(3:3)=strmid(1:1)
      if(cycnam(3:3).eq.'I')cycnam(3:3)='A'
c
c  find the last dtg in the best track file
c
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 20,cent,tdtg,btlat,btns,btlon,btew,ibtwind,ios )
         if (tdtg.ne.'        ') cdtg=tdtg
      enddo
c
c  now find the current, -12, and -24 hr positions
c
      call icrdtg (cdtg,dtgm12,-12)
      call icrdtg (cdtg,dtgm24,-24)
      rewind 20
      ios = 0
      do while ( ios .eq. 0 )
         call readBT(20, cent,btdtg,btlat,btns,btlon,btew,ibtwind,ios)
         if( ios .eq. 0 ) then
            if( btdtg .eq. dtgm24 ) then
               plat24 = btlat
               plon24 = btlon
               ew24 = btew
            else if( btdtg .eq. dtgm12 ) then
               plat12 = btlat
               plon12 = btlon
               ew12 = btew
            else if( btdtg .eq. cdtg ) then
               flat = btlat
               cns = btns
               flon = btlon
               cew = btew
            endif
         endif
      enddo

      close (20)

C
C***** OPEN THE INPUT (20) AND OUTPUT (40) FILES
C
cx    OPEN (UNIT=20,FILE='TAPE20')
cx    OPEN (UNIT=40,FILE='TAPE40')
cx    REWIND 20
C
C*****              INITIALIZE FINDING FLAGS
C
      ICNAM  = 0
      ICDTG  = 0
      ICFIX  = 0
      ICP12  = 0
      ICP24  = 0
      ISTOP  = 0
C
C*****              INPUT THE CARQ DATA
C
cx    DO 110 IC=1, 10000
cx      READ (20,500,END=199) CARD
cx500   FORMAT (A80)
cx      IF (CARD(1:4) .EQ. 'ID T') THEN
C
C*************    EXTRACT STORM NUMBER AND BASIN  *********************
C
          ICNAM  = -1
cx        CYCNAM = CARD(7:9)
          IF (CYCNAM(1:1) .EQ. ' ') CYCNAM(1:1) = '0'
          CSTRMK = CYCNAM(1:2)
          CBASN1 = CYCNAM(3:3)
C
cx      ELSEIF (CARD(1:3).EQ.'DTG') THEN
C
C*************    EXTRACT DTG    *********************
C
           ICDTG = -1
cx         CDTG  = CARD(7:14)
           READ (CDTG,501) IYR,MON,IDAY,IHR
  501      FORMAT (4I2)
           CMMDD = CDTG(3:6)
           CYEAR = CDTG(1:2)
           IF (CBASN1.EQ.'S' .OR. CBASN1.EQ.'P') THEN
C                   SOUTHERN HEMISPHERE CYCLONE
              NSIND = -1
              IF (MON .GE. 7) THEN
C                   1 JULY 90 IS START OF 91 SEASON FOR S.H. CYCLONES
                 NYR = IYR +1
                 IF (NYR .EQ. 100) NYR = 0
                 NYR1 = NYR/10
                 NYR2 = NYR -10*NYR1
                 IZRO = ICHAR ('0')
                 CYEAR(1:1) = CHAR (IZRO +NYR1)
                 CYEAR(2:2) = CHAR (IZRO +NYR2)
              ENDIF
           ELSE
C                   NORTHERN HEMISPHERE CYCLONE
              NSIND = 1
           ENDIF
C
cx      ELSEIF (CARD(1:7) .EQ. 'INITIAL') THEN
C
C*************    EXTRACT PRESENT POSITION     *********************
C
           ICFIX = -1
cx         READ (CARD,502) FLAT,CNS,FLON,CEW
cx502      FORMAT (16X,F4.1,A1,1X,F5.1,A1)
           FLT = FLAT
           FLN = FLON
           IF (CNS .EQ. 'N') THEN
C                   SET CALCULATION FLAG FOR NORTHERN OCEANS
              IF (NSIND .NE. 1) NSIND = -99
           ELSEIF (CNS .EQ. 'S') THEN
C                   SET CALCULATION FLAG FOR SOUTHERN OCEANS
              IF (NSIND .NE. -1) NSIND = -99
              FLAT  = -FLAT
           ELSE
C                   SET FLAG FOR BAD LATITUDE INDICATOR
              NSIND = 0
           ENDIF
C
           IF (NSIND .GT. 0) THEN
              IF (CEW.EQ.'E' .AND. FLON.GT.100.0 .AND. FLON.LT.180.0)
     .           THEN
C                           AREA IS NORTHWEST PACIFIC
                 NSIND = 2
                 ISTOP = -1
              ELSEIF (CEW.EQ.'W' .AND. FLON.GT.140.0 .OR. FLON.EQ.180.0)
     .           THEN
C                           AREA IS CENTRAL NORTH PACIFIC
                 NSIND = 3
                 FLN   = 360.0 -FLN
cx               disabled this basin  ... sampson 9/16/01
		 istop = -1
              ELSEIF(CEW.EQ.'W' .AND. FLON.LE.140.0 .AND. CBASN1.EQ.'E')
     .           THEN
C                           AREA IS EASTERN NORTH PACIFIC
                 NSIND = 4
                 FLN   = 360.0 -FLN
              ELSEIF (CEW .NE. 'E') THEN
C                             MUST BE AN ATLANTIC CYCLONE
                 ISTOP = -1
              ENDIF
           ELSEIF (NSIND.LT.0 .AND. NSIND.GT.-99) THEN
              IF (CEW.EQ.'E' .AND. FLON.GE.100.0 .AND. FLON.LT.135.0)
     .           THEN
C                           AREA IS SOUTHEAST INDIAN OCEAN
                 NSIND = -2
              ELSEIF (CEW.EQ.'E' .AND. FLON.GE.135.0 .OR. CEW.EQ.'W')
     .           THEN
C                           AREA IS SOUTH PACIFIC
                 NSIND = -3
                 IF (CEW .EQ. 'W') FLN = 360.0 -FLN
              ENDIF
           ENDIF
           IF (ISTOP .EQ. -1) THEN
              IF (NSIND .EQ. 2) THEN
                 PRINT 600, CYCNAM, CDTG
  600            FORMAT (' NO OCLIPR - WP BASIN FOR ',A3,' AT ',A8)
C
C                ********************************************
C
                 STOP 'OCLIP: CANT DO WP BASIN'
C
C                ********************************************
C
              ELSEIF (CBASN1 .EQ. 'L') THEN
                 PRINT 610, CYCNAM ,CDTG
cx               REWIND 40
cx               WRITE (40,610) CYCNAM, CDTG
  610            FORMAT (' NO OCLIPR - ATLANTIC BASIN FOR ',A3,' AT ',
     .                   A8)
C
C                ***********************************************
C
                 STOP 'OCLIP: CANT DO ATLANTIC BASIN'
C
C                ***********************************************
C
              ELSE
                 NSIND = -99
              ENDIF
           ENDIF
           IF (NSIND .EQ. -99) THEN
              PRINT 615, CYCNAM, CDTG
cx            REWIND 40
cx            WRITE (40,615) CYCNAM, CDTG
  615         FORMAT (1X,'NO OCLIPR - WRONG BASIN INDICATED FOR ',A3,
     .           ' AT ',A8)
C
C                ********************************************
C
              STOP 'OCLIP: BASIN NO MATCH LAT'
C
C                ********************************************
C
           ENDIF
C
cx      ELSEIF (CARD(4:8) .EQ. 'HOUR') THEN
C
C*************      EXTRACT PREVIOUS POSITIONS     *********************
C
cx         READ (CARD,503) ITIME
cx503      FORMAT (I2)
cx         IF (ITIME .EQ. 12) THEN
C
C                         12-H OLD POSIT
C
cx            READ (CARD,504) PLAT12,PLON12,EW12
  504         FORMAT (16X,F4.1,2X,F5.1,A1)
              PLT12 = PLAT12
              PLN12 = PLON12
              IF (EW12 .EQ. 'W') PLN12 = 360.0 -PLN12
              IF (IABS (NSIND) .EQ. 1) THEN
C                            INDIAN OCEAN, NORTH AND SOUTHWEST
                 IF (PLT12.GT.1.0 .AND. PLT12.LE.40.0 .AND.
     .                 PLN12.GE.35.0 .AND. PLN12.LT.120.0)
     .              ICP12 = -1
              ELSEIF (NSIND .EQ. 3) THEN
C                            CENTRAL NORTH PACIFIC
                 IF (PLT12.GT.1.0 .AND. PLT12.LE.40.0 .AND.
     .                 PLN12.GE.180.0 .AND. PLN12.LE.225.0)
     .              ICP12 = -1
              ELSEIF (NSIND .EQ. 4) THEN
C                            EASTERN NORTH PACIFIC
                 IF (PLT12.GT.1.0 .AND. PLT12.LE.35.0 .AND.
     .                 PLN12.GE.215.0 .AND. PLN12.LE.275.0)
     .              ICP12 = -1
              ELSEIF (NSIND .EQ. -2) THEN
C                            SOUTHEAST INDIAN OCEAN
                 IF (PLT12.GT.1.0 .AND. PLT12.LE.40.0 .AND.
     .                 PLN12.GE.95.0 .AND. PLN12.LT.140.0)
     .              ICP12 = -1
              ELSEIF (NSIND .EQ. -3) THEN
                 IF (PLT12.GT.1.0 .AND. PLT12.LE.45.0 .AND.
     .                 PLN12.GE.130.0 .AND. PLN12.LE.230.0)
     .              ICP12 = -1
              ENDIF
C
cx         ELSEIF (ITIME .EQ. 24) THEN
C
C                         24-H OLD POSIT
C
cx            READ (CARD,504) PLAT24,PLON24,EW24
              PLT24 = PLAT24
              PLN24 = PLON24
              IF (EW24 .EQ. 'W') PLN24 = 360.0 -PLN24
              IF (IABS (NSIND) .EQ. 1) THEN
C                            INDIAN OCEAN, NORTH AND SOUTHWEST
                 IF (PLT24.GT.1.0 .AND. PLT24.LE.40.0 .AND.
     .                 PLN24.GE.35.0 .AND. PLN24.LT.110.0)
     .              ICP24 = -1
              ELSEIF (NSIND .EQ. 3) THEN
C                            CENTRAL NORTH PACIFIC
                 IF (PLT24.GT.1.0 .AND. PLT24.LE.40.0 .AND.
     .                 PLN24.GE.180.0 .AND. PLN24.LE.225.0)
     .              ICP24 = -1
              ELSEIF (NSIND .EQ. 4) THEN
C                            EASTERN NORTH PACIFIC
                 IF (PLT24.GT.1.0 .AND. PLT24.LE.35.0 .AND.
     .                 PLN24.GE.215.0 .AND. PLN24.LE.275.0)
     .              ICP24 = -1
              ELSEIF (NSIND .EQ. -2) THEN
C                            SOUTHEAST INDIAN OCEAN
                 IF (PLT24.GT.1.0 .AND. PLT24.LE.40.0 .AND.
     .                 PLN24.GE.95.0 .AND. PLN24.LT.140.0)
     .              ICP24 = -1
              ELSEIF (NSIND .EQ. -3) THEN
C                            SOUTH PACIFIC
                 IF (PLT24.GT.1.0 .AND. PLT24.LE.45.0 .AND.
     .                 PLN24.GE.130.0 .AND. PLN24.LE.230.0)
     .              ICP24 = -1
              ENDIF
cx         ENDIF
cx      ENDIF
cx110 CONTINUE
C
C******       NO MORE CARQ DATA, DERIVE CLIPER FORECAST
C
  199 CONTINUE
C
C******             CHECK ON EXTRACTION
C
      IF (ICNAM.EQ.0 .OR. ICDTG.EQ.0) THEN
         WRITE (*,620)
cx       WRITE (40,620)
  620    FORMAT (1X,'MISSING STORM NAME AND/OR DTG.  NO OCLIPR')
         ISTOP = -1
      ENDIF
      IF (ISTOP .EQ. 0) THEN
C
C...                CHANGE BASIN INDICATOR FROM ONE LETTER TO TWO
C
         IF (CBASN1.EQ.'A' .OR. CBASN1.EQ.'B') THEN
C                   ARABIAN OR BAY OF BENGAL
            CBASN2 = 'IO'
         ELSEIF (CBASN1 .EQ. 'C') THEN
C                   CENTRAL NORTH PACIFIC
            CBASN2 = 'CP'
         ELSEIF (CBASN1 .EQ. 'E') THEN
C                   EASTERN NORTH PACIFIC
            CBASN2 = 'EP'
         ELSEIF (CBASN1.EQ.'S' .OR. CBASN1.EQ.'P') THEN
C                   SOUTH INDIAN OR PACIFIC OCEANS
            CBASN2 = 'SH'
         ELSEIF (CBASN1 .EQ. 'W') THEN
C                   STORM ORIGINATED IN WESTERN NORTH PACIFIC
            IF (CEW.EQ.'W' .OR. FLON.EQ.180.0) THEN
               IF (FLON .GT. 140.0) THEN
                  CBASN2 = 'CP'
               ELSE
                  CBASN2 = 'EP'
               ENDIF
            ELSE
               CBASN2 = 'IO'
            ENDIF
         ELSE
C                   UNKNOWN BASIN IDICATOR
            CBASN2 = 'XX'
         ENDIF
C
C...                COMPLETE NAME
C
         WRITE (CNAME,630) CBASN2,CSTRMK,CYEAR
  630    FORMAT (A2,A2,A2)
C
C******       CHECK WHICH POSITIONS ARE AVAILABLE
C
         IF (ICFIX.EQ.0 .AND. ICP12.EQ.0) THEN
            WRITE (*,640)  CNAME,CDTG
cx          WRITE (40,640) CNAME,CDTG
  640       FORMAT (' MISSING OR BAD 00-HR AND 12-HR OLD POSITION FOR ',
     .               A6,' AT ',A8)
            ISTOP = -1
         ELSEIF (ICFIX .EQ. 0) THEN
            WRITE (*,650)  CNAME,CDTG
cx          WRITE (40,650) CNAME,CDTG
  650       FORMAT (' MISSING OR BAD 00-HR POSITION FOR ',A6,
     .              ' AT ',A8)
            ISTOP = -1
         ELSEIF (ICP12 .EQ. 0) THEN
            WRITE (*,660)  CNAME,CDTG
cx          WRITE (40,660) CNAME,CDTG
  660       FORMAT (' MISSING OR BAD 12-HR OLD POSITION FOR ',A6,
     .              ' AT ',A8)
            ISTOP = -1
         ELSEIF (NSIND .EQ. 0) THEN
            WRITE (*,670)  CNAME,CDTG
cx          WRITE (40,670) CNAME,CDTG
  670       FORMAT (' INCORRECT LATITUDE INDICATOR FOR ',A6,
     .              ' AT ',A8)
            ISTOP = -1
         ELSEIF (CEW.NE.'E' .AND. CEW.NE.'W') THEN
            WRITE (*,680)  CNAME,CDTG
cx          WRITE (40,680) CNAME,CDTG
  680       FORMAT (' INCORRECT LONGITUDE INDICATOR FOR ',A6,
     .              ' AT ',A8)
            ISTOP = -1
         ENDIF
      ENDIF
      IF (ISTOP .EQ. 0) THEN
         IF (ICP24 .EQ. 0) THEN
C                   SET 24-HR PAST POSITION TO MISSING
            PLT24 = 0.0
            PLN24 = 0.0
          ENDIF



C
C*****              CALL TO COMPUTE THE PREDICTOR ARRAYS
C
         CALL FIXPRD (NSIND,IYR,MON,IDAY,IHR,FLT,FLN,PLT12,PLN12,
     .                PLT24,PLN24,P)
C
C*****              CALL THE CLIPER ROUTINE
C
         CALL CLDXDY (NSIND,P,DX,DY)
C
C*****              CONVERT DX AND DY TO LATITUDE/LONGITUDE
C
         DEGRAD = ACOS (-1.0)/180.0
         CNMDEG = 1.0/60.0
         IF (NSIND .GT. 0) THEN
C                   CALCULATE FORECAST FOR NORTHERN HEMISPHERE, EXCEPT
C                   NORTHWEST PACIFIC OCEAN AND ATLANTIC OCEAN
            FLT12 = FLAT +DY(1)*CNMDEG
            FLT24 = FLAT +DY(2)*CNMDEG
            FLT36 = FLAT +DY(3)*CNMDEG
            FLT48 = FLAT +DY(4)*CNMDEG
            FLT60 = FLAT +DY(5)*CNMDEG
            FLT72 = FLAT +DY(6)*CNMDEG
            ALT   = 0.5*(FLAT +FLT12)
            FLN12 = FLN +DX(1)*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT12 +FLT24)
            FLN24 = FLN12 +(DX(2) -DX(1))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT24 +FLT36)
            FLN36 = FLN24 +(DX(3) -DX(2))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT36 +FLT48)
            FLN48 = FLN36 +(DX(4) -DX(3))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT48 +FLT60)
            FLN60 = FLN48 +(DX(5) -DX(4))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT60 +FLT72)
            FLN72 = FLN60 +(DX(6) -DX(5))*CNMDEG*COS (ALT*DEGRAD)
            IT    = 7
         ELSE
C                   CALCULATE FORECAST FOR SOUTHERN HEMISPHERE
C                     (NOTE, 60-HR FORECAST IS NOT INCLUDED FOR SW INDIA
            FLT12 = FLAT -DY(1)*CNMDEG
            FLT24 = FLAT -DY(2)*CNMDEG
            FLT36 = FLAT -DY(3)*CNMDEG
            FLT48 = FLAT -DY(4)*CNMDEG
            FLT60 = FLAT -DY(5)*CNMDEG
            IF (NSIND .NE. -1) THEN
               FLT72 = FLAT -DY(6)*CNMDEG
            ELSE
               FLT72 = FLT60
            ENDIF
            ALT   = 0.5*(FLAT +FLT12)
            FLN12 = FLN -DX(1)*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT12 +FLT24)
            FLN24 = FLN12 -(DX(2) -DX(1))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT24 +FLT36)
            FLN36 = FLN24 -(DX(3) -DX(2))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT36 +FLT48)
            FLN48 = FLN36 -(DX(4) -DX(3))*CNMDEG*COS (ALT*DEGRAD)
            ALT   = 0.5*(FLT48 +FLT60)
            FLN60 = FLN48 -(DX(5) -DX(4))*CNMDEG*COS (ALT*DEGRAD)
            IF (NSIND .NE. -1) THEN
               ALT   = 0.5*(FLT60 +FLT72)
               FLN72 = FLN60 -(DX(6) -DX(5))*CNMDEG*COS (ALT*DEGRAD)
               IT    = 7
            ELSE
               FLN72 = FLN60
               IT    = 5
            ENDIF
         ENDIF
C
C*****              OUTPUT PLAIN LANGUAGE FORECAST TO THE PRINTER
C
         IF (NSIND .EQ. 1) THEN
            PRINT 681, CNAME,CDTG
  681       FORMAT(' ',10X,'NORTH INDIAN CLIPER FORECAST FOR  ',A4,
     .             ' ON ',A8,//)
         ELSEIF (NSIND .EQ. 3) THEN
            PRINT 682, CNAME,CDTG
  682       FORMAT(' ',10X,'CENTRAL PACIFIC CLIPER FORECAST FOR  ',A4,
     .             ' ON ',A8,//)
         ELSEIF (NSIND .EQ. 4) THEN
            PRINT 683, CNAME,CDTG
  683       FORMAT(' ',10X,'EAST PACIFIC CLIPER FORECAST FOR  ',A4,
     .             ' ON ',A8,//)
         ELSEIF (NSIND .EQ. -1) THEN
            PRINT 684, CNAME,CDTG
  684       FORMAT(' ',10X,'SOUTHWEST INDIAN CLIPER FORECAST FOR  ',A4,
     .             ' ON ',A8,//)
         ELSEIF (NSIND .EQ. -2) THEN
            PRINT 685, CNAME,CDTG
  685       FORMAT(' ',10X,'SOUTHEAST INDIAN CLIPER FORECAST FOR  ',A4,
     .             ' ON ',A8,//)
         ELSEIF (NSIND .EQ. -3) THEN
            PRINT 686, CNAME,CDTG
  686       FORMAT(' ',10X,'SOUTH PACIFIC CLIPER FORECAST FOR  ',A4,
     .             ' ON ',A8,//)
         ENDIF
         ITAU = -24
         PRINT 691, ITAU,PLAT24,CNS,PLON24,EW24
  691    FORMAT (' ',10X,'TAU = ',I3,'    LAT = ',F5.1,A1,
     .           '  LONG = ',F6.1,A1,/)
         ITAU = -12
         PRINT 691, ITAU,PLAT12,CNS,PLON12,EW12
         ITAU = 0
         PRINT 691, ITAU,ABS(FLAT),CNS,FLON,CEW
         DO 210 I=1, 6
           ITAU = ITAU +12
           FPLT = ABS (FP(1,I))
           FPLN = FP(2,I)
           IF (NSIND .EQ. 3) THEN
C                     CENTRAL NORTH PACIFIC
               IF (FPLN .GT. 180.0) THEN
                  CEW = 'W'
                  FPLN = 360.0 -FPLN
               ELSE
                  CEW = 'E'
               ENDIF
           ELSEIF (NSIND .EQ. 4) THEN
C                     EASTERN NORTH PACIFIC
              FPLN = 360.0 -FPLN
           ELSEIF (NSIND .EQ. -3) THEN
C                     SOUTH PACIFIC
              IF (FPLN .GT. 180.0) THEN
                 FPLN = 360.0 -FPLN
                 CEW = 'W'
              ELSE
                 CEW = 'E'
              ENDIF
           ENDIF
           IF (I .NE. IT) PRINT 691, ITAU,FPLT,CNS,FPLN,CEW
C
C                INTEGER VERSION OF THE FORECAST FOR CCRS
C
           IFP(1,I) = ANINT (FPLT*10.0)
           IFP(2,I) = ANINT (FPLN*10.0)
           FEW(I)   = CEW
  210    CONTINUE
C
C******             NAME OF THE AID, USE SAME NAME FOR ALL CLIPER'S
C
         AIDNM = 'CLIP'
C
C******             WRITE THE CCRS FORECAST TO TAPE 40
C
cx       REWIND 40
cx       WRITE (40,692) AIDNM,CNAME,CDTG
cx692    FORMAT (A4,1X,A6,1X,A8)
cx       JWIND = '000'
cx       WRITE (40,693) CMMDD,
cx   1   IFP(1,2),CNS,IFP(2,2),FEW(2),JWIND,
cx   2   IFP(1,4),CNS,IFP(2,4),FEW(4),JWIND,
cx   3   IFP(1,6),CNS,IFP(2,6),FEW(6),JWIND
cx693    FORMAT (A4,1X,3(I3,A1,1X,I4,A1,1X,A3,1X))
c
c  print the forecast in adeck format
c
	 do 220 i=1,6
	   if(cns   .eq.'S')ifp(1,i)=-ifp(1,i)
	   if(few(i).eq.'E')ifp(2,i)=3600 -ifp(2,i)
cx
cx   idiot checks for model misfunction
cx 
	   if(ifp(1,i).gt.900 .or. ifp(1,i).lt.-900)ifp(1,i)=0
	   if(ifp(2,i).gt.3600 .or. ifp(2,i).lt.-3600)ifp(2,i)=0
  220    continue

         do ii=1,numtau
            ltlnwnd(ii,1) = 0
            ltlnwnd(ii,2) = 0
            ltlnwnd(ii,3) = 0
         enddo
         do ii=1, 4
            ltlnwnd(ii,1) = ifp(1,ii)
            ltlnwnd(ii,2) = ifp(2,ii)
            ltlnwnd(ii,3) = 0
         enddo
         ltlnwnd(5,1) = ifp(1,6)
         ltlnwnd(5,2) = ifp(2,6)
         ltlnwnd(5,3) = 0
         call writeAid( 60, strmid, cent, cdtg, 'CLIP', ltlnwnd )

	 close (60)
      ENDIF
      STOP
C
 9001 continue
      print*,' ocliper: error opening best track data file'
      stop 1
 9002 continue
      print*,' ocliper: error opening ocliper.txt'
      stop 1
 9003 continue
      print*,' ocliper: error opening wptot.dat'
      stop 1

      END
      SUBROUTINE FIXPRD (NSIND,IYR,MON,IDY,IHR,FLT,FLN,PLT12,PLN12,
     .                   PLT24,PLN24,P)
C
C...................... START PROLOGUE .................................
C
C  SUBPROGRAM NAME:  FIXPRD
C
C  DESCRIPTION:  LOAD BASE SEVEN PREDICTORS, THEN CALCULATE REMAINING
C                PREDICTORS FOR A SECOND ORDER POLYNOMIAL.
C
C  ORIGINAL PROGRAMMER:  HARRY D. HAMILTON, (MM - GSA)   MAY 1990
C
C  USAGE (CALLING SEQUENCE):
C     CALL FIXPRD (NSIND,IYR,MON,IDY,IHR,FLT,FLN,PLT12,PLN12,PLT24,
C                  PLN24,P)
C
C  INPUT VARIABLES:
C     FLT    - LATITUDE  OF PRESENT LOCATION
C     FLN    - LONGITUDE OF PRESENT LOCATION
C     IDY    - NUMBER OF DAY OF MONTH FOR PRESENT LOCATION
C     IHR    - NUMBER OF HOUR FOR PRESENT LOCATION
C     IYR    - LAST TWO DIGITS OF YEAR
C     MON    - NUMBER OF MONTH FOR PRESENT LOCATION
C     NSIND  - NORTH/SOUTH BASIN INDICATOR
C                  1 - NORTH INDIAN OCEAN
C                  3 - CENTRAL NORTH PACIFIC OCEAN
C                  4 - NORTHEAST PACIFIC OCEAN
C                 -1 - SOUTHWEST INDIAN OCEAN
C                 -2 - SOUTHEAST INDIAN OCEAN
C                 -3 - SOUTH PACIFIC OCEAN
C     PLT12  - LATITUDE  OF -12 HOUR POSITION, DEGREES -PLUS NORTH
C     PLN12  - LONGITUDE OF -12 HOUR POSITION, DEGREES EAST
C     PLT24  - LATITUDE  OF -24 HOUR POSITION, ZERO MEANS MISSING
C     PLN24  - LONGITUDE OF -24 HOUR POSITION, ZERO MEANS MISSING
C
C  OUTPUT VARIABLES:
C     P      - ARRAY OF PREDICTORS
C
C...................... MAINTENANCE SECTION ............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C     ALT    - AVERAGE LATITUDE BETWEEN TWO POSITIONS
C     DXDT12 - AVERAGE ZONAL SPEED (KTS) IN LAST 12 HOURS
C     DYDT12 - AVERAGE MERIDIONAL SPEED (KTS) IN LAST 12 HOURS
C     DXDT24 - AVERAGE ZONAL SPEED (KTS) IN LAST 24 HOURS
C     DYDT24 - AVERAGE MERIDIONAL SPEED (KTS) IN LAST 24 HOURS
C     NDAYS  - INITIALLY NUMBER OF DAYS IN NON-LEAP YEAR MONTHS
C
C  LANGUAGE:  FTN5
C
C  RECORD OF CHANGES:
C
C...................... END PROLOGUE ...................................
C
      DIMENSION P(35)
      DIMENSION NDAYS(11)
C
      DATA NDAYS/31,28,31,30,31,30,31,31,30,31,30/
      DATA NNN/0/, NCHK/10/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NNN .LE. NCHK) THEN
      PRINT 601, NSIND,IYR,MON,IDY,IHR,FLT,FLN,PLT12,PLN12,PLT24,PLN24
  601 FORMAT (' NSIND ',I2,' YR ',I2,' MON ',I2,' DAY ',I2,' HR ',I2,/,
     . ' FIX ',F5.1,2X,F6.1,/,
     . ' -12 ',F5.1,2X,F6.1,/,
     . ' -24 ',F5.1,2X,F6.1)
         NNN = NNN +1
      ENDIF
C
C                   CHECK FOR LEAP YEAR, IF SO CHANGE DAYS IN FEBRUARY
      LYR = 1900 +IYR
      IF (MOD (LYR,4) .NE. 0) THEN
         NDAYS(2) = 28
      ELSE
         NDAYS(2) = 29
      ENDIF
      P(1) = 0.0
      DO 110 N=1, MON-1
        P(1) = P(1) +NDAYS(N)
  110 CONTINUE
      P(1) = P(1) +IDY +FLOAT (IHR)/24.0
      P(2) = ABS (FLT)
      P(3) = FLN
      IF (NSIND .LT. 0) THEN
C         SOUTHERN HEMISPHERE, DETERMINE THE NUMBER OF DAYS SINCE 1 JULY
         IF (MOD (LYR,4) .NE. 0) THEN
C                   NON-LEAP YEAR DETERMINATION
            IF (P(1) .LT. 181.8) THEN
C                   DATE IS PRIOR TO 1 JULY
               P(1) = P(1) +184.0
            ELSE
C                   DATE IS 1 JULY OR LATER
               P(1) = P(1) -181.0
            ENDIF
         ELSE
C                   LEAP YEAR DETERMINATION
            IF (P(1) .LT. 182.8) THEN
C                   DATE IS PRIOR TO 1 JULY
               P(1) = P(1) +184.0
            ELSE
C                   DATE IS 1 JULY OR LATER
               P(1) = P(1) -182.0
            ENDIF
         ENDIF
C                   BIAS FIRST PREDICTOR
         P(1) = P(1) -220.0
         IF (NSIND .EQ. -1) THEN
C                   SOUTHWEST INDIAN OCEAN
            P(2) = P(2)  -16.0
            P(3) = P(3)  -62.0
         ELSEIF (NSIND .EQ. -2) THEN
C                   SOUTHEAST INDIAN OCEAN
            P(3) = (360.0 -FLN) -224.0
         ELSE
C                   SOUTH PACIFIC OCEAN
            P(3) = (360.0 -FLN) -180.0
         ENDIF
      ELSEIF (NSIND .EQ. 3) THEN
C                   CENTRAL NORTH PACIFIC OCEAN
         P(3) = FLN -179.0
      ELSEIF (NSIND .EQ. 4) THEN
C                   EASTERN NORTH PACIFIC OCEAN
         P(3) = FLN -219.0
      ENDIF
C
C          CALCULATE PAST 12 AND 24 HR MERIDIONAL AND ZONAL SPEEDS (KTS)
C          NOTE: POLEWARD AND EASTWARD ARE POSITIVE IN CALCULATIONS
C
      DEGRAD = ACOS (-1.0)/180.0
      ALT    = ABS (0.5*(FLT +PLT12))
      DX12   = (FLN -PLN12)*COS (ALT*DEGRAD)
C                   60.0 N.M. / 12 HOURS IS 5.0
      DXDT12 = 5.0*DX12
      DYDT12 = 5.0*(ABS (FLT) -ABS (PLT12))
      IF (PLT24.NE.0.0 .AND. PLN24.NE.0.0) THEN
C                   CALCULATE AVERAGE 24 HR SPEED COMPONENTS
         ALT    = ABS (0.5*(PLT12 +PLT24))
C                   60.0 N.M. / 24 HOURS IS 2.5
         DXDT24 = 2.5*(DX12 +(PLN12 -PLN24)*COS (ALT*DEGRAD))
         DYDT24 = 2.5*(ABS (FLT) -ABS (PLT24))
      ELSE
C                   ASSUME CONSTANT SPEED
         DXDT24 = DXDT12
         DYDT24 = DYDT24
      ENDIF
      IF (NSIND .GT. 0) THEN
C                   LOAD NEXT FOUR PREDICTORS FOR NORTHERN HEMISPHERE
C                   NOTE: NORTHWARD AND EASTWARD ARE POSITIVE
         P(4) = DYDT12
         P(5) = DXDT12
         P(6) = DYDT24
         P(7) = DXDT24
      ELSE
C                   LOAD NEXT FOUR PREDICTORS FOR SOUTHERN HEMISPHERE
C                   NOTE: SOUTHWARD AND WESTWARD ARE POSITIVE
         P(4) =  DYDT12
         P(5) = -DXDT12
         P(6) =  DYDT24
         P(7) = -DXDT24
      ENDIF
      IF (NNN .LE. NCHK) THEN
         PRINT*,'FIXPRD P(1) ',P(1),' (2) ',P(2),' (3) ',P(3)
         PRINT*,'       DY12 ',P(4),' DX12 ',P(5)
         PRINT*,'       DY24 ',P(6),' DX24 ',P(7)
      ENDIF
C
C                   CALCULATE THE REMAINING PREDICTOR VALUES
C
      K = 7
      DO 220 I=1, 7
        DO 210 L=1, I
          K    = K +1
          P(K) = P(I)*P(L)
  210   CONTINUE
  220 CONTINUE
      RETURN
C
      END
      SUBROUTINE CLDXDY (NSIND,P,DX,DY)
C
C...................... START PROLOGUE .................................
C
C  SUBPROGRAM NAME:  CLDXDY
C
C  DESCRIPTION:  CALCULATE ZONAL (DX) AND MERIDIONAL (DY) DISPLACEMENTS
C         GIVEN 35 PREDICTORS (P) AND STATITICAL REGRESSION COEFFICIENTS
C
C  ORIGINAL PROGRAMMER:  HARRY D. HAMILTON, (MM - GSA)   MAY 1990
C
C  USAGE (CALLING SEQUENCE):  CALL CLDXDY (NSIND,P,DX,DY)
C
C  INPUT VARIABLES:
C
C     NSIND  - NORTH/SOUTH OCEAN BASIN INDICATOR
C                  1 - NORTH INDIAN OCEAN
C                  3 - CENTRAL NORTH PACIFIC
C                  4 - EAST NORTH PACIFIC
C                 -1 - SOUTHWEST INDIAN OCEAN
C                 -2 - SOUTHEAST INDIAN OCEAN
C                 -3 - SOUTH PACIFIC OCEAN
C
C     P      - ARRAY OF PREDICTORS
C
C  OUTPUT VARIABLES:
C     DX     - ZONAL DISPLACEMENTS, N.M.
C     DY     - MERIDIONAL DISPLACEMENTS, N.M.
C
C...................... MAINTENANCE SECTION ............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     COFXCP - ZONAL REGRESSION COEFFICIENTS FOR CENTRAL NORTH PACIFIC
C     COFXEP - ZONAL REGRESSION COEFFICIENTS FOR EASTERN NORTH PACIFIC
C     COFXNI - ZONAL REGRESSION COEFFICIENTS FOR NORTH INDIAN OCEAN
C     COFXWI - ZONAL REGRESSION COEFFICIENTS FOR SOUTHWEST INDIAN OCEAN
C     COFXEI - ZONAL REGRESSION COEFFICIENTS FOR SOUTHEAST INDIAN OCEAN
C     COFXSP - ZONAL REGRESSION COEFFICIENTS FOR SOUTH PACIFIC OCEAN
C     COFYCP - MERIDIONAL REGRESSION COEFFICIENTS FOR CENTRAL NORTH PAC
C     COFYEP - MERIDIONAL REGRESSION COEFFICIENTS FOR EASTERN NORTH PAC
C     COFYNI - MERIDIONAL REGRESSION COEFFICIENTS FOR NORTH INDIAN OCEAN
C     COFYWI - MERIDIONAL REGRESSION COEFFICIENTS FOR SOUTHWEST INDIAN O
C     COFYEI - MERIDIONAL REGRESSION COEFFICIENTS FOR SOUTHEAST INDIAN O
C     COFYSP - MERIDIONAL REGRESSION COEFFICIENTS FOR SOUTH PACIFIC OCEA
C
C  REMARKS:
C     SINCE FORTRAN 77 STANDARDS REQUIRE A MAXIMUM OF 19 CONTINUATIONS,
C     THE REGRESSION DATA BLOCKS ARE SPLIT INTO TWO PARTS AND
C     EQUVALENCED TO ASSOCIATED PRINCIPAL VARIABLE NAME OF EACH BLOCK.
C     NOTE, CDC FTN5 FOLLOWS THIS STANDARD, BUT MICROSOFT DOES NOT.
C
C  LANGUAGE:  FTN5        STANDARD
C
C  RECORD OF CHANGES:
C
C    <<CHANGE NOTICE>>  CLDXDY*01  (01 AUG 1990) -- HAMILTON, H.
C                UPDATE REGRESSION COEFFICIENTS FOR SE INDIAN AND
C                SOUTH PACIFIC BASINS WITH BEST TRACK DATA THROUGH 1989
C
C...................... END PROLOGUE ...................................
C
      DIMENSION P(35),DY(6),DX(6)
C                   NORTH INDIAN OCEAN
      DIMENSION COFXNI(0:35,6), COFXN1(0:35,3), COFXN2(0:35,3)
      DIMENSION COFYNI(0:35,6), COFYN1(0:35,3), COFYN2(0:35,3)
C                   CENTRAL NORTH PACIFIC OCEAN
      DIMENSION COFXCP(0:35,6), COFXC1(0:35,3), COFXC2(0:35,3)
      DIMENSION COFYCP(0:35,6), COFYC1(0:35,3), COFYC2(0:35,3)
C                   NORTHEASTERN PACIFIC OCEAN
      DIMENSION COFXEP(0:35,6), COFXP1(0:35,3), COFXP2(0:35,3)
      DIMENSION COFYEP(0:35,6), COFYP1(0:35,3), COFYP2(0:35,3)
C                   SOUTHWEST INDIAN OCEAN
      DIMENSION COFXWI(0:35,5), COFXW1(0:35,3), COFXW2(0:35,2)
      DIMENSION COFYWI(0:35,5), COFYW1(0:35,3), COFYW2(0:35,2)
C                   SOUTHEAST INDIAN OCEAN
      DIMENSION COFXEI(0:35,6), COFXE1(0:35,3), COFXE2(0:35,3)
      DIMENSION COFYEI(0:35,6), COFYE1(0:35,3), COFYE2(0:35,3)
C                   SOUTH PACIFIC OCEAN
      DIMENSION COFXSP(0:35,6), COFXS1(0:35,3), COFXS2(0:35,3)
      DIMENSION COFYSP(0:35,6), COFYS1(0:35,3), COFYS2(0:35,3)
C
C                   NORTH INDIAN OCEAN
      EQUIVALENCE (COFXNI(0,1),COFXN1(0,1))
      EQUIVALENCE (COFXNI(0,4),COFXN2(0,1))
      EQUIVALENCE (COFYNI(0,1),COFYN1(0,1))
      EQUIVALENCE (COFYNI(0,4),COFYN2(0,1))
C                   CENTRAL NORTH PACIFIC
      EQUIVALENCE (COFXCP(0,1),COFXC1(0,1))
      EQUIVALENCE (COFXCP(0,4),COFXC2(0,1))
      EQUIVALENCE (COFYCP(0,1),COFYC1(0,1))
      EQUIVALENCE (COFYCP(0,4),COFYC2(0,1))
C                   EASTERN NORTH PACIFIC
      EQUIVALENCE (COFXEP(0,1),COFXP1(0,1))
      EQUIVALENCE (COFXEP(0,4),COFXP2(0,1))
      EQUIVALENCE (COFYEP(0,1),COFYP1(0,1))
      EQUIVALENCE (COFYEP(0,4),COFYP2(0,1))
C                   SOUTHWEST INDIAN OCEAN
      EQUIVALENCE (COFXWI(0,1),COFXW1(0,1))
      EQUIVALENCE (COFXWI(0,4),COFXW2(0,1))
      EQUIVALENCE (COFYWI(0,1),COFYW1(0,1))
      EQUIVALENCE (COFYWI(0,4),COFYW2(0,1))
C                   SOUTHEAST INDIAN OCEAN
      EQUIVALENCE (COFXEI(0,1),COFXE1(0,1))
      EQUIVALENCE (COFXEI(0,4),COFXE2(0,1))
      EQUIVALENCE (COFYEI(0,1),COFYE1(0,1))
      EQUIVALENCE (COFYEI(0,4),COFYE2(0,1))
C                   SOUTH PACIFIC OCEAN
      EQUIVALENCE (COFXSP(0,1),COFXS1(0,1))
      EQUIVALENCE (COFXSP(0,4),COFXS2(0,1))
      EQUIVALENCE (COFYSP(0,1),COFYS1(0,1))
      EQUIVALENCE (COFYSP(0,4),COFYS2(0,1))
C
C                   NORTH INDIAN OCEAN
      DATA COFXN1/       -187.055,-0.792781,6.159461,5.173059,-4.384362,
     1 4.692245,2.816026,3.320626,0.001898,0.005209,-0.036352,-0.001605,
     2 -0.059217,-0.026482,0.023209,-0.158597,0.006285,0.817984,.006820,
     3 0.199170,0.013111,0.805893,-0.119838,-0.023451,0.108761,0.041453,
     4 -1.095076,-.413465,0.323029,-.006081,-.221499,0.020062,-1.065527,
     5 0.317362,0.586736,-0.122211,
     6        -673.855,-2.028291,20.826173,17.306994,-8.362610,8.374212,
     7 1.726714,5.143383,0.005104,0.015036,-0.142006,-0.005810,-.203665,
     8 -0.086728,0.045897,-0.457765,0.036803,1.707531,0.017448,0.291314,
     9 0.037552,1.378041,-0.430983,-.041676,0.421463,0.098006,-2.423458,
     A -0.547482,0.772453,-.017638,-.411752,0.057361,-2.169534,1.339732,
     B 1.236815,-0.699305,
     C      -1500.70,-3.116510,39.161508,37.274625,-14.494063,11.999563,
     D -13.345788,0.709031,0.008499,0.027405,-.272154,-.013588,-.395372,
     E -0.188579,0.057097,-0.998592,0.200531,-.310654,0.051887,0.305103,
     F 0.018814,2.129966,-0.054807,-0.025930,1.150324,0.114944,1.512554,
     G -0.459515,-.938758,-.043939,-.453013,0.161076,-3.159568,1.577810,
     H 1.305672,-1.125264/
C
      DATA COFXN2/    -2674.12,-4.190128,67.135982,64.461558,-50.534022,
     1 22.619964,7.476372,-3.586954,0.012400,0.039145,-.517538,-.023990,
     2 -0.654263,-0.329445,0.098239,-.988382,0.474690,-.693223,0.109551,
     3 0.162152,-0.180456,1.496288,-0.072369,-.047409,1.271781,-.020564,
     4 3.046693,1.464708,-2.169023,-.096965,-.369744,0.344741,-3.339648,
     5 2.314967,-0.044056,-1.731743,
     6    -4317.73,-5.211147,103.538745,101.539093,-67.672504,25.317590,
     7 26.492298,2.057552,0.016801,0.035070,-0.845048,-.035608,-.921158,
     8 -.529451,0.084739,-1.000890,0.754557,-2.209312,0.156530,0.270366,
     9 -0.364882,0.979859,-0.135686,-.015645,1.165566,-.348469,6.263508,
     A 3.367099,-3.806902,-.137631,-.490102,0.445575,-3.080898,2.948261,
     B -2.074834,-2.260468,
     C    -6489.63,-5.838681,143.164975,151.210754,-68.978403,15.798493,
     D 31.624683,26.124268,0.019810,0.016988,-1.293185,-0.042490,
     E -1.151889,-.819301,0.162949,-1.533011,.629002,-4.960129,0.263052,
     F 0.377197,-0.553137,-1.008550,-.385313,-.051263,1.698093,-.425348,
     G 11.937986,5.755615,-6.424937,-.255393,-.752302,0.537170,-.456080,
     H 4.403536,-5.717464,-3.672673/
C
      DATA COFYN1/-101.472,0.090715,-.015324,2.904251,8.782723,9.166660,
     1 -2.307040,-6.019680,-.000286,0.004550,-.060361,-.000998,0.000341,
     2 -0.015739,-0.007289,-.073419,0.047106,-.310035,-.003945,0.052700,
     3 -0.100754,-0.277130,-.116348,0.013318,0.092681,-.027556,0.715199,
     4 0.590569,-0.546824,0.001174,-0.104040,0.082218,0.040528,0.214804,
     5 -0.220098,-0.080730,
     6          -332.830,0.253372,1.913448,8.868694,24.659431,21.312034,
     7 -11.329896,-12.003258,-0.000659,0.011725,-0.215390,-0.003213,
     8 0.001110,-0.048323,-0.021963,-.459984,0.068630,-.627300,-.025470,
     9 0.075164,-0.177353,-0.408175,-.050325,0.039976,0.386954,-.050361,
     A 1.258610,1.145360,-1.095431,0.019078,-0.216461,0.114852,0.159674,
     B 0.106862,-0.564382,0.011274,
     C         -617.232,0.866490,2.113132,15.652218,22.515126,19.715591,
     D -3.509371,-0.380828,-.001511,0.016782,-.403608,-.008228,0.029823,
     E -0.083987,-0.011782,-.735887,0.177485,-.954485,-.032651,0.086397,
     F -0.121832,-0.806140,0.213716,0.052786,0.506789,-.202836,1.602507,
     G 1.747110,-1.486153,0.024457,-0.358739,-.019821,0.630507,-.263132,
     H -1.206334,0.204521/
C
      DATA COFYN2/       -937.464,1.829204,0.091854,22.926830,51.149062,
     1 22.910087,-18.917639,7.344457,-.002864,.020294,-.573389,-.014456,
     2 0.074195,-.122008,-.028327,-1.276686,0.068155,-1.962962,-.040461,
     3 0.039802,-0.153966,-0.115203,0.397859,0.083405,0.791370,-.204083,
     4 2.529331,1.701616,-1.903818,0.031290,-0.431036,-.088755,-.311373,
     5 -0.610810,-1.132114,0.402651,
     6        -1281.60,2.696496,-5.087535,31.803192,80.702960,40.511208,
     7 -40.861799,2.679969,-.004125,0.019554,-.740695,-.019363,0.160229,
     8 -0.176442,-.033035,-1.427979,-.218201,-1.628518,-.039143,.063768,
     9 -0.323794,0.244134,0.691441,0.094611,0.747854,0.012891,0.669860,
     A 1.043422,-0.585533,0.025515,-0.609925,-.051926,-.878297,-.808384,
     B -0.482940,0.201981,
     C       -1947.16,3.758112,-12.034687,48.887498,82.208666,38.203879,
     D -40.311881,16.768066,-.006137,0.016117,-.939227,-.022172,.276587,
     E -0.287237,-.023529,-1.848692,-.159820,-2.461435,-.023334,.002296,
     F -0.345922,0.328497,0.954503,0.112539,1.026837,-0.173888,3.047941,
     G 0.233481,-1.823571,0.001454,-.779013,-.125505,0.026118,-1.447248,
     H -0.975012,0.357889/
C
C                   CENTRAL NORTH PACIFIC OCEAN
      DATA COFXC1/     603.283,-2.876348,-19.088602,-8.929860,-4.630769,
     1 26.648334,-0.024666,-17.417127,0.002786,0.043161,.205832,.029309,
     2 0.006656,0.039730,-0.023077,0.397928,0.188535,1.585797,-0.045941,
     3-0.103990,-0.010464,2.837054,-0.210391,0.054397,-.395733,-.295315,
     4-3.264180,-3.047547,1.840740,0.051441,0.090111,-.022545,-2.877951,
     5 0.834392,2.980134,-0.635852,
     6      1248.81,-5.375614,-42.354697,-22.618672,56.195859,29.841288,
     7-78.545594,-16.491845,0.003421,0.094988,0.496512,.076716,-.028446,
     8 0.104471,-0.197567,0.391525,-0.213649,2.294748,-0.070126,.070556,
     9 0.688719,3.935745,-0.597758,0.334041,-.428842,-.084509,-4.641770,
     A-3.355615,2.700299,0.101652,-0.096089,-.735868,-3.467494,2.718060,
     B 2.766478,-1.997753,
     C     1961.48,-8.690144,-65.973242,-34.395045,102.136298,14.520661,
     D-164.468492,-6.519844,0.006476,0.164100,0.664215,.108127,-.099917,
     E 0.201392,-0.385455,1.496550,-0.827649,3.133605,-.018192,0.629484,
     F 1.258606,6.910331,0.439720,0.662037,-0.951595,0.403963,-4.752706,
     G-6.647059,1.232682,0.112744,-.804005,-1.228253,-6.175215,1.353457,
     H 5.356999,-1.473953/
C
      DATA COFXC2/ 2575.48,-10.497334,-103.601888,-50.629499,-30.131350,
     1 111.890281,-60.803415,-130.159165,0.004538,0.292950,0.866300,
     2 0.147838,-0.240213,0.375406,0.018106,3.934939,-0.817590,5.249147,
     3-0.469598,1.817147,1.420475,10.434333,-.335491,0.376574,-3.004027,
     4 0.276628,-10.008741,-10.951975,3.590409,0.686831,-2.299870,
     5-1.216784,-10.433933,3.354919,10.177755,-2.632591,
     6   679.928,7.812790,-122.267225,-87.413071,-162.824240,211.684580,
     7 3.313547,-330.599958,-.035193,0.297663,1.156501,.236332,-.274840,
     8 0.687564,0.390109,5.501964,-0.131969,8.136072,-0.961930,2.740444,
     9 1.137965,15.218438,5.111563,0.335534,-5.110766,-0.141522,
     A-17.932842,-15.256993,8.425635,1.554470,-4.031678,-0.657377,
     B-15.010792,-7.554354,14.925647,2.062527,
     C  -2483.08,30.449575,-57.337693,-126.038494,-277.431995,25.028050,
     D 130.420116,-226.169693,-0.076840,0.053306,0.652851,0.353595,
     E-0.408595,1.027928,0.766447,5.181536,-0.258771,2.042596,0.046936,
     F 4.619627,-1.735356,17.107800,16.688705,.031010,-6.189455,.235439,
     G-11.702697,-25.242164,10.335707,0.866325,-7.759841,2.721704,
     H-22.124899,-31.693851,32.394092,14.102564/
C
      DATA COFYC1/      276.593,-0.864203,-8.211217,-5.330710,49.413163,
     1-13.634151,-44.836458,15.083091,-.000108,0.018134,.087885,.013098,
     2 0.058279,0.021053,-0.123090,-0.020296,-0.170061,0.346950,.039323,
     3-0.046474,0.123023,-1.023594,-1.008076,0.148088,-0.011490,.166734,
     4-0.526720,2.031968,0.101291,-0.049110,0.121480,-0.117492,1.365479,
     5 1.881686,-2.341076,-0.857866,
     6       650.550,-2.108063,-13.763850,-14.444025,48.483860,0.481402,
     7-36.545577,0.937388,0.000668,0.015458,0.238791,0.038454,0.159038,
     8 0.038747,-0.032184,0.028669,-0.291474,2.067753,-.090194,0.430613,
     9 0.506261,-1.623482,-1.036713,0.054220,-.052348,.182417,-3.989803,
     A 3.420457,1.631482,0.079908,-0.101399,-0.465680,2.285323,2.220598,
     B-4.294541,-0.978614,
     C      957.750,-1.526757,-34.702984,-28.796283,67.012152,21.677229,
     D-38.670922,-45.331042,-.002790,0.041630,0.560583,0.084721,.304998,
     E 0.019375,-0.059632,1.073808,-0.426278,4.902573,-.296804,1.969458,
     F 0.634964,-2.266064,0.401645,0.029315,-1.105290,.116408,-9.923833,
     G 3.744579,4.381570,0.407457,-1.435651,-0.647423,4.131083,-.145947,
     H-6.419881,0.037211/
C
      DATA COFYC2/    1804.49,-1.816507,-86.614925,-60.573528,92.068015,
     1 45.628595,-36.774669,-114.511222,-0.008533,0.110691,1.248857,
     2 0.180430,0.609382,0.072718,-0.349736,3.741129,0.058599,7.242322,
     3-0.361423,2.247408,0.370755,-4.812143,2.077820,0.264875,-4.261102,
     4-0.655600,-15.048710,5.750691,7.721191,.622365,-1.718573,-.346236,
     5 7.450843,-2.774276,-9.360442,0.400518,
     6   2531.17,4.339785,-153.356357,-115.539844,-60.926083,-11.431475,
     7 83.105853,-93.068755,-.029542,0.119243,2.167832,.317238,1.478855,
     8 0.141074,0.128788,3.347650,1.387130,9.818776,-0.458925,4.373031,
     9 0.678477,-7.107852,5.408543,-0.007724,-5.175692,-1.791623,
     A-22.523368,4.497898,12.658629,.883143,-4.349841,-.765974,7.791929,
     B-12.341626,-6.475657,5.906068,
     C 3621.45,-0.708627,-146.779545,-127.355755,-73.831083,-174.668090,
     D 38.213932,106.601937,-.015151,-.104958,2.591823,.342411,1.989491,
     E 0.065883,0.082368,4.027136,0.372771,4.757637,-0.224322,6.579593,
     F 1.018478,-1.625054,4.542081,.234054,-6.119137,.058293,-13.755410,
     G-5.827765,9.307271,0.541421,-7.769791,-0.637532,-1.252832,
     H-17.602364,8.690186,12.315534/
C
C                   EASTERN NORTH PACIFIC OCEAN
      DATA COFXP1/      176.444,-1.217153,-5.088348,-0.640642,-8.792946,
     1 15.679242,3.272106,-2.050981,0.002611,0.005183,0.071006,-.001858,
     2 0.056718,-0.002290,0.038316,-0.019338,0.054133,0.039173,-.006355,
     3 0.026323,-0.014298,0.225755,0.112699,-0.019901,0.093971,-.028433,
     4-0.152474,-0.016018,0.008150,0.007055,-0.153077,-.015437,-.223262,
     5 0.154424,-0.068585,-0.215072,
     6      431.522,-3.367599,-11.330967,-0.919330,-20.772977,27.867622,
     7 7.738984,-3.140968,0.007547,0.009434,0.197250,-0.006319,0.137406,
     8-0.005849,0.077776,0.374868,0.092543,0.215215,0.037135,0.028626,
     9-0.164263,0.565207,0.601384,-0.039147,-.157320,-.040384,-1.206353,
     A-0.254229,0.803749,-0.036320,-0.253445,0.108949,-0.317887,.056247,
     B-0.233812,-0.567102,
     C      737.840,-6.267697,-17.559503,-0.741235,-27.295732,42.128813,
     D 7.350758,-8.565816,0.014033,0.022790,0.291315,-0.012724,0.209985,
     E-0.003946,0.118001,0.375384,-0.011360,-0.580869,0.054932,0.265233,
     F-0.340449,1.081509,0.712198,-0.057237,-0.100210,0.044816,0.130039,
     G-1.434128,0.475848,-0.056079,-0.580632,0.279816,-1.080421,.441931,
     H 0.977198,-1.051838/
C
      DATA COFXP2/    1032.64,-8.865149,-25.553775,-0.845305,-31.339374,
     1 45.465187,5.621636,2.411229,0.020744,0.021028,0.500357,-0.024363,
     2 0.295225,0.012830,0.169271,0.566984,-0.325334,1.360165,0.044681,
     3 0.765812,-0.287159,-1.075956,0.034759,-0.097935,-.225482,.412329,
     4-3.094409,0.867031,1.848904,-0.054737,-1.368859,0.194802,1.313134,
     5 2.127012,-1.833829,-1.949350,
     6     1388.85,-11.319681,-34.315748,-4.058451,-17.746192,64.026044,
     7-25.694244,0.874573,0.027738,-0.002198,0.857263,-0.036940,.370123,
     8 0.069914,0.098205,0.706701,-0.294563,2.121104,0.032878,0.626632,
     9-0.484947,-2.209814,-0.238769,-.007598,-.081151,.644343,-3.498334,
     A 2.337233,1.852171,-0.058986,-1.610135,0.341860,2.777005,3.208369,
     B-3.991728,-2.651729,
     C    2114.83,-14.434530,-55.762955,-17.127219,-36.531650,38.224492,
     D-7.715176,55.724040,0.034651,-0.025454,1.460197,-0.034232,.638603,
     E 0.154791,0.092755,1.065132,0.015709,2.525440,0.057200,1.732184,
     F-0.133634,-3.596901,-0.848428,0.012124,-.755176,.469129,-3.530896,
     G 2.894337,1.869471,-0.120626,-3.075190,-.282015,3.271160,4.611340,
     H-3.507991,-3.177923/
C
      DATA COFYP1/       24.7245,0.139545,-1.363008,-0.645745,30.819742,
     1-2.033931,-24.906396,3.850013,-0.000666,0.007262,-.060869,.001596,
     2 0.032744,-0.005297,-0.012791,-0.767106,-.000108,.146694,-.003081,
     3 0.150439,-0.026428,-0.119442,-0.457308,0.019294,0.914346,.018350,
     4-0.271303,0.242048,0.016162,0.000239,-0.173279,-0.000616,0.395769,
     5 0.741055,-0.419196,-0.284753,
     6         93.0067,0.668867,-9.944640,-1.771479,47.422698,-1.562227,
     7-43.237482,6.801468,-0.002588,0.024490,-0.040588,0.004516,.093411,
     8-0.015185,-0.014377,-0.942678,0.069545,0.440809,-0.030785,.598653,
     9-0.096815,0.789586,-0.692390,0.042852,1.309045,-.013483,-1.447516,
     A-0.708906,0.791119,0.025252,-0.710357,0.042426,-0.045962,1.019569,
     B 0.206375,-0.296494,
     C        227.178,1.608664,-28.610481,-3.423128,32.567895,-4.113655,
     D-34.619063,16.695027,-0.005470,0.050758,0.097208,0.005034,.223035,
     E-0.027435,0.046543,-0.323129,0.138256,-2.376964,-0.060227,.893941,
     F 0.025787,0.830134,0.037116,0.010553,1.014018,-0.089630,3.427932,
     G-1.025618,-1.197321,0.054066,-1.283732,-0.136615,-0.084652,
     H-0.810148,0.736347,0.889586/
C
      DATA COFYP2/       336.254,3.071052,-53.225511,-4.472731,7.535354,
     1 5.247461,-13.656489,14.927371,-0.009230,0.074780,.359799,.006324,
     2 0.392898,-0.055916,0.083413,1.415697,0.142380,-2.114934,-.088504,
     3 1.210020,-0.128332,-0.197154,-.425113,-.014458,-.299847,-.169888,
     4 1.799323,0.213044,-0.000871,0.087453,-1.986646,-0.021999,.936942,
     5 0.301733,-0.372261,.371819,
     6        452.543,4.373952,-76.108910,-6.527581,-8.129832,18.230520,
     7-4.085129,7.285725,-0.012690,0.094349,0.601886,0.012070,0.576908,
     8-0.081275,0.065836,3.463122,-0.045409,-0.568536,-.079899,1.122703,
     9-0.414014,0.679954,-.741943,-.007489,-1.746520,-.098194,-1.014096,
     A-0.685764,1.381733,0.083327,-2.173513,0.238217,0.710337,1.423773,
     B-0.278055,-0.343816,
     C         503.199,5.783882,-97.290813,-8.330486,5.397878,30.059794,
     D-15.699890,-9.424669,-0.016332,0.109328,0.887509,0.018635,.787804,
     E-0.108127,0.089867,2.702111,-0.320023,-1.031185,-.093654,1.515987,
     F-0.635088,-0.351940,-0.816228,-0.048563,-.848200,.018860,-.575374,
     G-1.240937,1.333129,0.098757,-2.456967,0.518161,1.513177,1.584708,
     H 0.068229,-0.545383/
C
C                   SOUTHWEST INDIAN OCEAN
      DATA COFXW1/ 8.85,   -0.04317,-0.47100, 0.28890, 0.64421, 9.09629,
     1   -1.24071, 2.44450,-0.00007,-0.00054, 0.02787, 0.00154, 0.02965,
     2   -0.00588,-0.01031,-0.24413,-0.01922,-1.08952, 0.02458, 0.05026,
     3   -0.00002, 0.86531, 0.09836, 0.00792, 0.33308, 0.04539, 2.26445,
     4   -0.67652,-1.21334,-0.02329,-0.07359, 0.00469,-1.69576,-0.16913,
     5    1.22754,-0.00987,
     6            26.40,   -0.09499,-1.56304, 0.87038, 1.25312,16.36656,
     7   -4.35203, 5.17253,-0.00025, 0.00158, 0.08594, 0.00520, 0.08131,
     8   -0.01874, 0.00906,-0.12192,-0.01489,-1.84779, 0.02587,-0.09237,
     9   -0.07877, 0.80859, 0.32147,-0.01558, 0.35944, 0.06198, 3.48327,
     A   -0.23527,-1.64780,-0.02901, 0.09437, 0.10398,-2.55274,-0.50374,
     B    1.43450,-0.00941,
     C            49.86,   -0.15204,-3.43849, 1.46725, 1.68639,23.34833,
     D   -9.00506, 6.95212,-0.00056, 0.00502, 0.19020, 0.00989, 0.15466,
     E   -0.03998, 0.04759, 0.02857,-0.07878,-2.37247, 0.03030,-0.00529,
     F   -0.13053, 1.00374, 0.65892,-0.05952, 0.38569, 0.17570, 4.40197,
     G   -0.13457,-1.96715,-0.04129, 0.09585, 0.22037,-3.72017,-1.04475,
     H    2.05842, 0.03325/
C
      DATA COFXW2/75.72,   -0.19973,-6.41157, 2.00373,-1.74756,29.15463,
     J  -11.21200, 8.24483,-0.00104, 0.00971, 0.32731, 0.01556, 0.24343,
     K   -0.06460, 0.12336,-0.12177,-0.21885,-3.55715, 0.02626, 0.16101,
     L   -0.12944, 2.04001, 0.78656,-0.14062, 0.88493, 0.41868, 7.17998,
     M   -0.85176,-3.40784,-0.05179, 0.03488, 0.30267,-5.61806,-1.36126,
     N    3.43812, 0.07769,
     O            120.04,  -0.34954,-15.60674,3.32784,-8.90326,35.98238,
     P  -18.62158,11.22854,-0.00327, 0.01516, 0.59088, 0.02035, 0.42508,
     Q   -0.10614, 0.24784,-0.70086,-0.31780,-5.10852,-0.00748, 0.51011,
     R   -0.11038, 3.33342, 1.10956,-0.26575, 2.62155, 0.72766,10.98705,
     S   -1.04709,-5.37939,-0.05049,-0.27487, 0.44125,-8.58832,-2.06114,
     T    5.37853, 0.15729/
C
      DATA COFYW1/ 9.93,   -0.01216, 0.38476,-0.07987, 8.90468, 0.07934,
     1    2.38371, 0.01449, 0.00001, 0.00096,-0.01984,-0.00165,-0.01208,
     2    0.00032,-0.00401, 0.18068, 0.00657, 0.19088, 0.01231,-0.16032,
     3   -0.01308, 0.27659,-0.18774, 0.00697,-0.41024, 0.00286,-0.54472,
     4   -0.31252, 0.17143,-0.00790, 0.19253, 0.01552, 0.14900, 0.20217,
     5   -0.19874,-0.01636,
     6            27.20,   -0.02251, 0.78202,-0.19498,16.27608,-0.38505,
     7    4.53478, 0.79186, 0.00010, 0.00137,-0.04584,-0.00443,-0.03397,
     8    0.00123,-0.02315, 0.11231, 0.05891, 0.19771, 0.03059,-0.49534,
     9   -0.03230, 0.25076,-0.40840, 0.03081,-0.64744,-0.03252,-0.93780,
     A   -0.31535, 0.38932,-0.01899, 0.58493, 0.03416, 0.37090, 0.47352,
     B   -0.48479,-0.06912,
     C            51.27,   -0.05782, 1.35060,-0.33008,22.26088, 0.15738,
     D    6.90287, 0.98559, 0.00027,-0.00086,-0.07613,-0.00789,-0.06189,
     E    0.00141,-0.03411, 0.01728, 0.15978, 0.01345, 0.05310,-0.74585,
     F   -0.03548,-0.06300,-0.56337, 0.04854,-0.87813,-0.11517,-0.94091,
     G   -0.12597, 0.43890,-0.03162, 0.92455, 0.04140, 0.98246, 0.65371,
     H   -1.11649,-0.11570/
C
      DATA COFYW2/82.08,   -0.11532, 2.11405,-0.37212,30.13377, 1.44800,
     J    6.03031, 0.65684, 0.00037,-0.00607,-0.09134,-0.01095,-0.09293,
     K   -0.00028,-0.05081,-0.02140, 0.25120, 0.16397, 0.08131,-0.95144,
     L   -0.01559,-0.36491,-0.79596, 0.07823,-1.15842,-0.19785,-1.72125,
     M   -0.12677, 0.92125,-0.05319, 1.24125, 0.02259, 1.35108, 0.91083,
     N   -1.33300,-0.16736,
     O            165.71,  -0.27764, 5.59260,-0.07266,38.09911, 2.81297,
     P    8.35808, 1.06048, 0.00026,-0.02056,-0.10778,-0.01118,-0.17583,
     Q   -0.01598,-0.06719,-0.40205, 0.30732, 0.00177, 0.14874,-1.17684,
     R    0.03782,-0.52230,-1.11454, 0.12066,-1.51338,-0.25690,-1.87784,
     S   -0.32999, 1.16062,-0.10374, 1.68553,-0.04559, 1.71213, 1.32859,
     T   -1.61865,-0.27375/
C
C                   SOUTHEAST INDIAN OCEAN
      DATA COFXE1/       54.1696,0.307481,-3.788630,-1.855264,-7.445009,
     1 12.807069,18.155954,-.133817,-.003132,-.005613,0.084327,-.001673,
     2 0.067346,0.020593,0.013550,0.355563,-0.179778,-0.295783,0.210177,
     3 -0.258205,0.128591,1.947225,-.445815,-.016839,-1.067642,0.195684,
     4 0.891716,-2.566936,-.363599,-.218125,0.164910,-.149264,-2.100426,
     5 0.899614,2.704363,-0.551310,
     6         3.20495,-0.041905,10.071705,-2.570640,-0.580891,5.336623,
     7 14.122333,18.637610,-.009122,0.024544,-.574915,0.008904,0.192289,
     8 0.018192,-0.035097,0.052602,-.323721,-1.646908,0.240209,0.872923,
     9 0.286382,3.317597,-0.738536,-0.053303,-.483736,0.016692,1.523008,
     A -5.182074,.244765,-.236681,-1.159300,-.400157,-3.357327,1.334352,
     B 5.154274,-0.549034,
     C        143.221,1.326230,-3.797019,-2.298517,-28.631012,-2.737578,
     D 49.908101,48.403689,-.018596,-.030532,-.197153,-.033394,0.256229,
     E 0.006523,-0.346845,-.089357,0.823255,-3.755827,0.493978,2.258766,
     F 0.436047,5.994304,-3.579361,0.481483,-.803849,-1.308275,5.225804,
     G -9.922545,-0.914466,-0.601965,-3.751845,-0.506274,-5.037957,
     H 8.179629,8.861037,-4.120479/
C
      DATA COFXE2/        148.588,-0.563006,-2.176602,2.177883,1.116246,
     1 64.062542,-.055581,-18.979475,-.021911,.093512,-.298816,0.006114,
     2 0.057767,-0.055681,-0.197705,0.134889,-.518659,1.733380,0.569574,
     3 -0.681269,-.236496,8.425502,-5.062797,0.217042,-.422024,0.655442,
     4 -2.838779,-12.206012,2.013880,-0.730193,-0.559743,0.142101,
     5 -9.361098,11.337056,12.923715,-5.461919,
     6         7.85701,-0.450432,26.734779,4.721884,69.568751,39.470325,
     7 -51.769763,35.680215,-.037301,.189951,-1.563122,-.027252,.105099,
     8 -0.129576,-.352623,-7.119261,.856339,-11.362943,.728061,2.538472,
     9 -0.592198,14.457560,-7.561651,0.101779,7.256028,-1.499878,
     A 15.398166,-21.489977,-2.310001,-0.797851,-5.923155,0.917552,
     B -15.609668,16.357393,22.025374,-8.273308,
     C       351.797,-1.947244,-24.251411,14.129133,-8.093985,31.099031,
     D -44.234571,43.535912,-.038553,.384468,-.019910,-.018893,-.056062,
     E -.283923,-.226115,-1.531370,1.764841,-8.183654,0.659153,3.915056,
     F -0.725954,15.221676,-9.359150,-0.292250,6.144175,-1.998749,
     G 10.697148,-27.984724,-2.179864,-0.767029,-6.995707,0.941724,
     H -17.158497,20.864009,29.495337,-10.649934/
C
      DATA COFYE1/39.7513,0.092976,-3.049719,1.156329,8.637743,0.604570,
     1 -9.039984,1.025807,0.000215,0.001849,0.080792,-0.003472,-.001847,
     2 -0.032442,-0.005694,0.059397,-.025703,0.093695,0.035460,-.266027,
     3 0.211330,-0.110721,-0.301174,-.002497,0.419980,0.034233,-.153918,
     4 0.487864,-0.014521,-0.033419,0.132047,-.182529,0.103112,0.242458,
     5 -0.598999,0.068000,
     6            135.574,0.174146,-9.654474,0.019073,0.770671,7.392553,
     7 -3.190202,-6.586346,-.000629,-.021303,0.183747,0.001360,0.148426,
     8 -0.070714,0.082104,-0.022546,0.526766,1.103690,0.051462,-.395899,
     9 0.188197,-1.987253,-0.361641,-.029619,0.546222,-.217579,-.823469,
     A 1.709942,-0.417588,-0.051178,0.239398,-.104555,1.365064,-.122979,
     B -1.362524,0.569030,
     C       210.934,-0.795950,-14.592750,-2.749388,68.743688,10.814522,
     D -77.833910,-9.282737,0.003850,0.000284,0.157171,0.023554,.577427,
     E -0.134321,0.196216,-3.891553,0.253245,3.866531,0.072519,-.596091,
     F 0.294256,1.540376,0.705632,-0.080306,4.232557,0.432173,-4.381848,
     G -1.412135,0.547763,-.022441,.462217,-.345692,-2.663388,-2.186780,
     H 2.523137,1.457037/
C
      DATA COFYE2/     347.886,-0.711877,-25.822781,-0.995306,-9.849999,
     1 -17.664886,-12.493152,31.003873,-.007353,.060852,.545701,.010525,
     2 0.458765,-0.153665,0.035264,0.148266,1.079599,-0.422554,-.122230,
     3 1.237090,-0.027776,-0.845705,1.445817,-.146340,1.181456,-.278536,
     4 1.263510,0.100697,-0.626375,0.178856,-2.334009,0.078126,0.405432,
     5 -3.864354,0.409229,2.361441,
     6         324.922,1.044656,-28.663670,9.814322,-44.460319,5.694172,
     7 45.786090,1.877262,-0.004128,-.035391,1.002101,-.021196,-.142951,
     8 -0.274392,0.118625,3.546886,1.173263,2.799384,-0.122471,-.530721,
     9 -.127726,1.356365,-.484660,-.111246,-3.577146,-.198249,-3.923387,
     A -2.995836,1.136396,0.150926,-.191272,0.518622,-2.821280,1.076225,
     B 3.925428,-0.804845,
     C         96.1369,2.301570,25.023617,-6.317081,-12.654657,3.001899,
     D 53.610158,3.959842,-.013385,-.188957,-1.505780,-.023510,0.837419,
     E -0.128273,0.224162,0.077468,2.173795,1.864156,-.243738,-1.701845,
     F 0.790409,3.307749,-.806837,.112680,-2.506851,-1.219300,-1.227320,
     G -5.360858,-.588267,0.320686,1.694496,-.573932,-6.349020,1.534711,
     H 6.822473,-1.053484/
C
C                   SOUTH PACIFIC OCEAN
      DATA COFXS1/      277.808,1.637000,0.644847,-43.202879,-26.603102,
     1 -0.204127,17.312904,8.622575,-.003789,-.020245,-.089580,-.062098,
     2 0.200912,0.897378,-0.036377,0.548322,0.484668,-1.327258,0.000438,
     3 0.023037,0.247072,-0.103728,-0.005585,0.044251,-.227122,-.383136,
     4 3.266846,0.099966,-2.113100,0.011388,-0.040093,-.346099,-.087431,
     5 -0.041801,0.168291,0.021666,
     6          287.974,2.098620,3.143082,-41.929970,16.241356,0.594023,
     7 -45.596825,8.050411,-.008233,-.015519,-.170110,-.085603,-.097508,
     8 0.918414,-0.019150,-0.808948,-.697516,-.086527,-.004378,-.021163,
     9 0.466043,0.003465,-0.018171,-0.036721,1.752530,1.142126,1.013379,
     A 0.039878,-0.855239,0.019161,0.079374,-0.282568,0.233884,-.062243,
     B -0.379629,0.006669,
     C         210.803,1.572564,10.761042,-39.397827,6.353170,-1.182371,
     D -44.991860,7.950505,-.010655,0.005663,-.278774,-.068030,-.444628,
     E 0.938308,-0.021797,-0.699592,-.285625,0.207563,-.003471,0.063001,
     F 0.760424,-0.056836,-0.072956,-.016271,1.712284,0.935392,0.234238,
     G 0.236228,0.174088,0.013047,0.113723,-0.366618,-0.152848,-.013251,
     H 0.071449,0.023857/
C
      DATA COFXS2/     -16.6732,1.419053,29.074668,-30.489003,23.937049,
     1 -2.237867,-61.628765,7.479886,-.023164,.062678,-.484806,-.092617,
     2 -1.030244,0.891926,0.009134,-0.771131,-.604421,0.573958,-.002660,
     3 0.155368,0.875939,-0.386650,-0.125813,-.104096,1.322456,1.479344,
     4 -1.348800,0.573678,1.929669,0.011166,0.187578,-0.317167,0.285194,
     5 0.071017,-0.502059,0.014671,
     6         -147.255,0.123737,37.786976,-19.067365,3.897754,6.963529,
     7 -35.842723,8.077474,-.040369,.164162,-.579927,-.093355,-1.503113,
     8 0.728067,0.151129,-0.219493,0.026593,3.174633,-0.021734,-.176205,
     9 1.001160,0.848585,-0.119872,-.296145,0.587667,0.647904,-6.736088,
     A -0.480981,4.855162,-0.002947,0.165092,-.451229,-.997854,0.056177,
     B 0.576049,0.049793,
     C       -137.579,-1.151886,29.378451,-7.768730,12.934090,20.291428,
     D -38.145474,4.339478,-.052281,.276839,-.440051,-.106948,-1.555223,
     E 0.422746,0.068451,-0.987064,0.114977,4.415282,-0.017008,-.647208,
     F 0.687358,-1.053506,-.496636,-.274467,1.297452,0.256240,-8.180402,
     G 0.855098,4.976539,0.021020,0.222118,-0.049126,0.067857,0.904501,
     H -0.203919,-0.017811/
C
      DATA COFYS1/      20.7530,-0.151065,-0.106692,-0.425412,12.538425,
     1 0.079991,-2.416376,0.037196,0.000376,0.005741,0.001750,0.002051,
     2 0.016090,-0.001960,0.001353,-0.037038,-.021793,0.132247,-.000859,
     3 -0.010117,-0.019661,0.091685,-.004742,0.005321,-.000364,-.024290,
     4 -0.377538,-0.072199,0.267634,0.000782,0.009742,-.005355,-.126097,
     5 0.014367,0.106077,0.000615,
     6          59.7713,-0.462340,0.231868,-1.417984,19.206045,0.216475,
     7 -0.755133,0.340544,0.001827,0.021342,-0.016134,0.003050,0.055554,
     8 -0.011458,0.031247,-0.099030,0.130879,-.223180,0.000641,-.008414,
     9 -0.189176,-0.041262,-.041416,-.017284,-.054774,-.173561,-.005988,
     A 0.030994,0.300577,0.000703,-0.014311,0.158339,-0.118664,0.122039,
     B 0.115038,-0.031633,
     C          129.024,-0.350933,0.646077,-4.106727,29.142729,1.429881,
     D -5.301779,0.142199,0.004079,0.018873,-.083765,-0.001157,0.156219,
     E -0.011008,0.056393,-0.467005,0.207610,0.123945,0.000041,-.078966,
     F -0.262734,-0.061642,-.021121,-.031835,0.226075,-.225116,-.706277,
     G 0.059596,0.745225,0.005767,-0.002106,0.204791,-0.042847,0.097758,
     H 0.122994,-0.042942/
C
      DATA COFYS2/       243.860,0.224270,-3.305727,-6.931600,37.292824,
     1 2.385613,-8.167757,-0.762610,0.007115,0.000184,-.071020,-.014817,
     2 0.271967,-0.001074,0.008460,-0.300864,-.241638,0.815149,0.001350,
     3 -0.123945,-0.348365,-.181456,-.051091,0.025411,0.078437,0.087022,
     4 -1.761516,0.194867,1.058981,0.009874,0.048777,0.267587,0.270582,
     5 0.176749,-0.122139,-0.056659,
     6        399.428,0.913552,-9.781836,-10.167173,47.720878,-0.048324,
     7 -18.094320,-.424421,0.010986,-.019946,0.012551,-.034951,0.386553,
     8 0.009208,0.010928,-0.471031,-0.434301,-.368029,0.015205,0.005443,
     9 -0.365735,0.220663,0.019161,0.023805,0.248842,0.329284,0.454467,
     A -0.229316,0.059805,0.000048,0.041593,0.289830,-0.369357,0.039853,
     B 0.523523,-0.062826,
     C       539.646,1.596496,-16.127985,-11.036288,37.778242,-0.266623,
     D -7.198366,-3.461205,0.015097,-.038777,0.111319,-.054449,0.416051,
     E -0.005333,-0.018209,-.186756,-.165406,-.502083,0.003070,0.003973,
     F -0.351237,0.245886,0.063206,0.057408,-0.202155,0.128515,0.676214,
     G -0.314543,0.188935,0.006791,0.165683,0.314517,-0.135177,-.057859,
     H 0.407168,-0.062347/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NSIND .EQ. 1) THEN
C                   CALCULATE DISPLACEMENT FOR NORTH INDIAN OCEAN
         DO 120 J=1, 6
           DX(J) = COFXNI(0,J)
           DY(J) = COFYNI(0,J)
           DO 110 I=1, 35
             DX(J) = DX(J) +P(I)*COFXNI(I,J)
             DY(J) = DY(J) +P(I)*COFYNI(I,J)
  110      CONTINUE
  120    CONTINUE
      ELSEIF (NSIND .EQ. 3) THEN
C                   CALCULATE DISPLACEMENT FOR CENTRAL NORTH PACIFIC
         DO 140 J=1, 6
           DX(J) = COFXCP(0,J)
           DY(J) = COFYCP(0,J)
           DO 130 I=1, 35
             DX(J) = DX(J) +P(I)*COFXCP(I,J)
             DY(J) = DY(J) +P(I)*COFYCP(I,J)
  130      CONTINUE
  140    CONTINUE
      ELSEIF (NSIND .EQ. 4) THEN
C                   CALCULATE DISPLACEMENT FOR EASTERN NORTH PACIFIC
         DO 160 J=1, 6
           DX(J) = COFXEP(0,J)
           DY(J) = COFYEP(0,J)
           DO 150 I=1, 35
             DX(J) = DX(J) +P(I)*COFXEP(I,J)
             DY(J) = DY(J) +P(I)*COFYEP(I,J)
  150      CONTINUE
  160    CONTINUE
      ELSEIF (NSIND .EQ. -1) THEN
C                   CALCULATE DISPLACEMENT FOR SOUTHWEST INDIAN OCEAN
         DO 220 J=1, 5
           DX(J) = COFXWI(0,J)
           DY(J) = COFYWI(0,J)
           DO 210 I=1, 35
             DX(J) = DX(J) +P(I)*COFXWI(I,J)
             DY(J) = DY(J) +P(I)*COFYWI(I,J)
  210      CONTINUE
  220    CONTINUE
      ELSEIF (NSIND .EQ. -2) THEN
C                   CALCULATE DISPLACEMENT FOR SOUTHEAST INDIAN OCEAN
         DO 240 J=1, 6
           DX(J) = COFXEI(0,J)
           DY(J) = COFYEI(0,J)
           DO 230 I=1, 35
             DX(J) = DX(J) +P(I)*COFXEI(I,J)
             DY(J) = DY(J) +P(I)*COFYEI(I,J)
  230      CONTINUE
  240    CONTINUE
      ELSEIF (NSIND .EQ. -3) THEN
C                   CALCULATE DISPLACEMENT FOR SOUTH PACIFIC OCEAN
         DO 260 J=1, 6
           DX(J) = COFXSP(0,J)
           DY(J) = COFYSP(0,J)
           DO 250 I=1, 35
             DX(J) = DX(J) +P(I)*COFXSP(I,J)
             DY(J) = DY(J) +P(I)*COFYSP(I,J)
cx  debugging info ... bs 11/4/97
cx	     xvar=P(I)*COFXSP(I,J)
cx	     yvar=P(I)*COFYSP(I,J)
cx	     print *,'i,j,xvar,yvar'
cx	     print *, i,j,xvar,yvar
cx	     if (i.eq.5 .or. i.eq.7) then
cx		print *,'i,j,p(i),cofxsp(i,j),cofysp(i,j)'
cx  		print *,i,j,p(i),cofxsp(i,j),cofysp(i,j)
cx            endif
  250      CONTINUE
cx	     print *,'dxtot=',dx,'   dytot=',dy
  260    CONTINUE
      ENDIF
      RETURN
C
      END
