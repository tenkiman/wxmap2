      PROGRAM TCLIMO
C
C........................START PROLOGUE.................................
C
C  PROGRAM NAME:  TCLIMO
C
C  DESCRIPTION:  USING INPUT FROM THE CARQ MESSAGE (TAPE20) GENERATE
C                CLIM, XTRP AND TPAC FORECASTS (TAPE33) FOR FOLLOWING
C                   WESTERN NORTH PACIFIC  (NREGN = 1)
C                   EASTERN NORTH PACIFIC  (NREGN = 2),
C                   NORTH INDIAN OCEAN     (NREGN = 3),
C                   SOUTHWEST INDIAN OCEAN (NREGN = 4), OR
C                   SOUTHEAST INDIAN AND
C                   SOUTH PACIFIC OCEAN    (NREGN = 5)
C
C                   CODE/METHOD TAKEN FROM:
C                         Sampson, C. R., R. J. Miller, R. A. Kreitner and T. L Tsui
C                         1990: Tropical cyclone track objective aids for the 
C                         microcomputer: PCLM, XTRP, PCHP.  NOARL Technical Note, No. 61,
C                         Naval Research Laboratory, Monterey, CA, 15 pp.
C                    
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC - GSA), APRIL 91
C
C  CURRENT PROGRAMMER:  BUCK SAMPSON (NRL, MONTEREY), JULY 95
C   
C
C  COMPUTER/OPERATING SYSTEM:  UNIX
C
C  LIBRARIES OF RESIDENCE:                  
C
C  CLASSIFICATION:             UNCLASSIFIED
C
C  USAGE (JCL):                TCLIMO WP0195
C
C  INPUT FILES:
C     TAPE20  - CONTAINS TROPICAL CYCLONE PRESENT AND PAST LOCATIONS IN
C               BEST TRACK FORMAT
C     TAPE2   - CLIMATOLOGY FILES OF PAST BEST TRACK DATA
C
C  OUTPUT FILES:
C     TAPE33  - FORECASTS, EVERY 12 HRS PLAIN LANGUAGE AND EVERY
C               24 HRS FOR CCRS FORMAT
C
C  ERROR CONDITIONS:  ABORT PROGRAM IF WRONG BASIN OR MISSING CYCLONE
C        INFORMATION. NOTE, -12 HOUR POSITION IS NOT REQUIRED.
C
C........................MAINTENANCE SECTION............................
C
C  BRIEF DESCRIPTION OF PROGRAM MODULES:
C     CALTLN  - CALCULATE NEW LAT/LON FROM OLD LAT/LON GIVEN HEADING AND
C               DISTANCE
C     CLIMO   - PRODUCES CLIMATOLOGY FORECAST
C     EXTRAP  - CALULATE FORCAST BASED UPON EXTRAPLOATION
C     HEADEM  - OUTPUT HEADER INFO FOR PLAIN LANGUAGE FORECAST
C     HEDIST  - CALCULATE HEADING AND DISTANCE BETWEEN LAT/LON POINTS
C     IJAYDAY - CALCULATE MONTH AND DAY FROM YEAR AND JULIAN DAY
C     JAYDAY  - CALCULATE JULIAN DAY
C     RDCARQ  - READS CARQ INFO FROM TAPE20
C     RDCLIMO - READS CLIMATOLOGY OBSERVATIONS
C     TPACEM  - CALCULATE PERSISTENCE AND CLIMATOLOGY FORECAST WITH
C               WEIGHTS OF 0.5 - HPAC FORECAST
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     CFP    - ROUNDED OUTPUT ARRAY OF LATITUDE AND LONGITUDE TIMES 10
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
C     IHR    - NUMBER OF HOURS IN DAY FOR PRESENT POSITION
C     ISTOP  - INDICATOR FOR PROGRAM TERMINATION, -1 TERMINATE
C     IT     - NUMBER OF POSITIONS FOR OUTPUT
C     IYR    - LAST TWO DIGITS OF YEAR
C     LTLNWND - same as cfp only array of integers rather than reals
C     MON    - NUMBER OF MONTH FOR PRESENT POSITION
C     NSIND  - INDICATOR FOR BASIN, SEE ABOVE
C     P      - ARRAY OF PREDICTOR VALUES
C     PLAT12 - LATITUDE  OF 12-HOUR OLD POSITION
C     PLAT24 - LATITUDE  OF 24-HOUR OLD POSITION, ZERO MEANS MISSING
C     PLON12 - LONGITUDE OF 12-HOUR OLD POSITION
C     PLON24 - LONGITUDE OF 24-HOUR OLD POSITION, ZERO MEANS MISSING
C
C  METHOD:
C     CLIMO - CALCULATE CLIMATOLOGY FORECAST BASED UPON CLIMATOLOGY
C             CYCLONES WHICH ARE WITHIN A GIVEN RADIUS OF INITIAL
C             POSITION AND WITHIN A SPECIFIED TIME WINDOW OF INITIAL
C             TIME.
C     XTRAP - CALCULATE EXTRAPOLATED POSITIONS BASED UPON PAST 12-HR
C             DIRECTION AND SPEED.
C     HPAC  - COMBINE CLIMATOLOGY AND EXTRAPLOATION FORECASTS WITH
C             EQUAL WEIGHTING.
C
C  LANGAUGE:  FTN5 (FORTRAN77)
C
C  RECORD OF CHANGES:
C             
C  <<CHANGE NOTICE>>                         -- SAMPSON, B.
C                CONVERTED TO RUN IN ATCF 3.0
c
c     Modified to use new data format,  6/98   A. Schrader
c     Modified to use last bt posit century 11/98 Sampson 
C
C........................END PROLOGUE..................................
C
      include 'dataioparms.inc'

      character*100 filename,storms
      character*6 strmid
      character*2 century
      character*2 cent
      CHARACTER*4 AIDNM
      CHARACTER*1 PEW, FEW(6)
      character*1 cdummy
      integer     ltlnwnd(numtau,llw)
      integer     ii, iarg
C
      DIMENSION CP(6,3), XP(6,2), CFP(6,3)
C
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C
      CHARACTER CNAME*6, CDTG*8, CNS*1, CEW*1, EW12*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG
C   FLN   - FIX LONGITUDE, DEG
C   PLT12 - PAST 12 HR LATITUDE, DEG
C   PLN12 - PAST 12 HR LONGITUDE, DEG
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12
C
C
C                   EXPLANATION OF /CLIM/ VARIABLES
C
C   CLTXX - FORECAST LATITUDE  AT XX HOURS, BASED UPON CLIMATOLOGY
C   CLNXX - FORECAST LONGITUDE AT XX HOURS, BASED UPON CLIMATOLOGY
C   CWDXX - FORECAST MAXIMUM SUSTAINED WIND SPEED (KT) AT XX HOURS,
C           BASED UPON CLIMATOLOGY
C
      COMMON/CLIM/ CLT12,CLT24,CLT36,CLT48,CLT60,CLT72,
     .             CLN12,CLN24,CLN36,CLN48,CLN60,CLN72,
     .             CWD12,CWD24,CWD36,CWD48,CWD60,CWD72
C
C                   EXPLANATION OF /XTRP/ VARIABLES
C
C   CLTXX - FORECAST LATITUDE  AT XX HOURS, BASED UPON EXTRAPOLATION
C           OR HPAC
C   CLNXX - FORECAST LONGITUDE AT XX HOURS, BASED UPON EXTRAPOLATION
C           OR HPAC
C
      COMMON/XTRP/ XLT12,XLT24,XLT36,XLT48,XLT60,XLT72,
     .             XLN12,XLN24,XLN36,XLN48,XLN60,XLN72
C
C
      EQUIVALENCE (CP(1,1),CLT12), (XP(1,1),XLT12)
C
C                   SET TIME (DAYS) AND DISTANCE (NM) WINDOW VALUES
C
      DATA NDAYS/15/, RADIUS/210.0/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
Cx*****************  OPEN THE OUTPUT FILE, TAPE33  **********************
Cx
Cx    OPEN (UNIT=33,FILE='TAPE33')
cx    REWIND (33)
      call openfile (33,'tclimo.dbg','UNKNOWN',ierr)
c
c  get the storms directory name
c
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
c
c  open the ccrs output file
c
      filename=storms(1:ind)//'/wptot.dat'
      call openfile (60,filename,'unknown',ioerror)
      if (ioerror .lt. 0) go to 900
c
c  go to end of output file
c
   50 continue
      read(60,'(a1)',end=60)cdummy
      go to 50
   60 continue
C
C****************** READ ARQ MESSAGE  *********************
C
      CALL RDCARQ (cent, IERR1)
C
C******************  REWIND TAPE33 FOR OUTPUT FILE  ********************
C
cx    REWIND (33)
      IF (IERR1 .EQ. 0) THEN
C
C*****************  CALL TO COMPUTE CLIMATOLOGY FORECAST  **************
C
        KTRY = 0
  110   CONTINUE
        CALL CLIMO (NDAYS,RADIUS,NC24,NC48,NC72)
        IF (NC72.EQ.0 .AND. KTRY.EQ.0) THEN
C
C                   NO 72 HOUR FORECAST, SO INCREASE TIME WINDOW
C
          KTRY  = -1
          NDAYS = 2*NDAYS
          GOTO 110
C
        ELSE
C
C****************** OUTPUT PLAIN LANGUAGE CLIM FORECAST TO THE PRINTER
C
          AIDNM = 'CLIM'
          CALL HEADEM (NREGN,AIDNM)
C
          IF (PLT12.NE.0.0 .AND. PLN12.NE.0.0) THEN
C                   12-HOUR OLD POSITION IS AVAILABLE
            ITAU = -12
            IF (EW12 .EQ. 'E') THEN
              PLN = PLN12
            ELSE
              PLN = 360.0 -PLN12
            ENDIF
            CALL HEDIST (PLT12,PLN12,FLT,FLN,HEAD,DIST,RHEAD,RDIST)
            PRINT 9010, ITAU,ABS(PLT12),CNS,PLN,EW12,-99.0,RHEAD,
     .                 RDIST/12.0
c9010       FORMAT (11X,'TAU =',I3,'  LAT = ',F5.1,A1,
 9010       FORMAT (' TAU =',I3,'  LAT = ',F5.1,A1,
     .            '  LON = ',F6.1,A1,'  WIND = ',F4.0,'  HEAD = ',F5.1,
     .            '  SPEED =',F5.1)
          ENDIF
          ITAU = 0
          IF (CEW .EQ. 'E') THEN
            PLN = FLN
          ELSE
            PLN = 360.0 -FLN
          ENDIF
          CALL HEDIST (FLT,FLN,CLT12,CLN12,HEAD,DIST,RHEAD,RDIST)
          PRINT 9010, ITAU,ABS(FLT),CNS,PLN,CEW,FWD,RHEAD,RDIST/12.0
          DO 210 I=1, 6
            ITAU = ITAU +12
            FPLT = ABS (CP(I,1))
            FPLN = CP(I,2)
            IF (FPLN .GT. 180.0) THEN
              PEW = 'W'
              FPLN = 360.0 -FPLN
            ELSE
              PEW = 'E'
            ENDIF
            IF (I .NE. 6) THEN
              CALL HEDIST (CP(I,1),CP(I,2),CP(I+1,1),CP(I+1,2),HEAD,
     .                        DIST,RHEAD,RDIST)
              PRINT 9010, ITAU,FPLT,CNS,FPLN,CEW,ANINT(CP(I,3)),RHEAD,
     .                      RDIST/12.0
            ELSE
              PRINT 9015, ITAU,FPLT,CNS,FPLN,CEW,ANINT(CP(I,3))
            ENDIF
c9015       FORMAT (11X,'TAU =',I3,'  LAT = ',F5.1,A1,
 9015       FORMAT (' TAU =',I3,'  LAT = ',F5.1,A1,
     .            '  LON = ',F6.1,A1,'  WIND = ',F4.0)
C
C                ROUNDED VERSION OF THE FORECAST FOR CCRS
C
cx          CFP(I,1) = 0.1*ANINT (FPLT*10.0)
cx          CFP(I,2) = 0.1*ANINT (FPLN*10.0)
cx          CFP(I,3) = 0.1*ANINT (CP(I,3)*10.0)
cx          FEW(I)   = PEW
c
c  convert to ccrs right now (skip 60 hr forecast)
c
            cfp(i,1) = anint (fplt*10.0)
	    if(cns.eq.'S')cfp(i,1)=-cfp(i,1)
            cfp(i,2) = anint (fpln*10.0)
	    if(pew.eq.'E'.and.cfp(i,2).ne.0.0) cfp(i,2)=3600-cfp(i,2)
            cfp(i,3) = 0.1*anint (cp(i,3)*10.0)
cx zero out intensity less than zero ... bs 10/4/96
	    if(cfp(i,3).lt.0)cfp(i,3)=0

  210     CONTINUE
	    
C
Cx****************  WRITE THE CCRS CLIMO FORECAST TO FILE   **********
C
cx        WRITE (*,9030)
cx   1    24,CFP(2,1),CNS,CFP(2,2),FEW(2),CFP(2,3),2*NDAYS,NC24,
cx   2    48,CFP(4,1),CNS,CFP(4,2),FEW(4),CFP(4,3),2*NDAYS,NC48,
cx   3    72,CFP(6,1),CNS,CFP(6,2),FEW(6),CFP(6,3),2*NDAYS,NC72
c9030     FORMAT (3('  ** CLIM **  ',I2,14X,F4.1,A1,1X,F5.1,A1,5X,F5.1,
cx   .            5X,I3,5X,I3,/))
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c
c     get the storm id
c
          call getarg(iarg,strmid)
          iarg = iarg + 1
          call upcase (strmid,6)

          call getarg(iarg,century)
          iarg = iarg + 1

c  set the 5th element to 72 hour fcst for ease of writing
	  cfp(5,1)= cfp(6,1)
	  cfp(5,2)= cfp(6,2)
	  cfp(5,3)= cfp(6,3)

          do ii=1,numtau
             ltlnwnd(ii,1) = 0
             ltlnwnd(ii,2) = 0
             ltlnwnd(ii,3) = 0
          enddo
          do ii=1, 5
             do jj=1, 3
                ltlnwnd(ii,jj) = int( cfp(ii,jj) )
             enddo
          enddo
          call writeAid( 60, strmid, cent, cdtg, 'CLIM', ltlnwnd )
        ENDIF
C
        IF (PLT12.NE.0.0 .AND. PLN12.NE.0.0) THEN
C                   12-HOUR OLD POSITION IS AVAILABLE
C
C****************** CALL TO COMPUTE EXTRAPOLATION FORECAST  ************
C
          CALL EXTRAP (PLT12,PLN12,FLT,FLN)
C
C****************** OUTPUT PLAIN LANGUAGE XTRP FORECAST TO THE PRINTER
C
          AIDNM = 'XTRP'
          CALL HEADEM (NREGN,AIDNM)
          ITAU = 0
          DO 220 I=1, 6
            ITAU = ITAU +12
            FPLT = ABS (XP(I,1))
            FPLN = XP(I,2)
            IF (FPLN .LE. 180.0) THEN
              PEW = 'E'
            ELSE
              PEW = 'W'
              FPLN = 360.0 -FPLN
            ENDIF
            PRINT 9017, ITAU,FPLT,CNS,FPLN,CEW
c9017       FORMAT (11X,'TAU =',I3,'  LAT = ',F5.1,A1,
 9017       FORMAT (' TAU =',I3,'  LAT = ',F5.1,A1,
     .            '  LON = ',F6.1,A1)
C
C                ROUNDED VERSION OF THE FORECAST FOR CCRS
C
cx          CFP(I,1) = 0.1*ANINT (FPLT*10.0)
cx          CFP(I,2) = 0.1*ANINT (FPLN*10.0)
cx          CFP(I,3) = -99.0
cx          FEW(I)   = PEW
c
c  convert to ccrs right now (skip 60 hr forecast)
c
            cfp(i,1) = anint (fplt*10.0)
	    if(cns.eq.'S')cfp(i,1)=-cfp(i,1)
            cfp(i,2) = anint (fpln*10.0)
	    if(pew.eq.'E'.and.cfp(i,2).ne.0.0) cfp(i,2)=3600-cfp(i,2)
            cfp(i,3) = 0

  220     CONTINUE
C
C*****************  WRITE THE CCRS XTRP FORECAST TO TAPE 33  ***********
C
cx        WRITE (33,9040)
cx   1    24,CFP(2,1),CNS,CFP(2,2),FEW(2),
cx   2    48,CFP(4,1),CNS,CFP(4,2),FEW(4),
cx   3    72,CFP(6,1),CNS,CFP(6,2),FEW(6)
c9040     FORMAT (3('  ** XTRP **  ',I2,15X,F4.1,A1,2X,F5.1,A1,/))
C
	  
c  set the 5th element to 72 hour fcst for ease of writing
	  cfp(5,1)= cfp(6,1)
	  cfp(5,2)= cfp(6,2)
	  cfp(5,3)= cfp(6,3)

cx	  write (60,9041)
cx     1	       cdtg,(int(cfp(i,1)),int(cfp(i,2)),i=1,5),
cx     2         (int(cfp(i,3)),i=1,5),strmid
cx 9041     format('03XTRP',a8,10i4,5i3,1x,a6)

          IF (NC24 .GT. 0) THEN
C                  CLIMATOLOGY FORECAST WAS PRODUCED FOR AT LEAST TAU 24
C
C*****************  CALCULATE TPAC WITH FACTOR OF 0.5 (HPAC)  **********
C                   PLACE IN XTRAP ARRAYS
C
            CALL TPACEM
C
C*****************  OUTPUT PLAIN LANGUAGE TPAC FORECAST TO THE PRINTER
C
            AIDNM = 'TPAC'
            CALL HEADEM (NREGN,AIDNM)
            ITAU = 0
            DO 230 I=1, 6
              ITAU = ITAU +12
              FPLT = ABS (XP(I,1))
              FPLN = XP(I,2)
              IF (FPLN .LE. 180.0) THEN
                PEW = 'E'
              ELSE
                PEW = 'W'
                FPLN = 360.0 -FPLN
              ENDIF
              PRINT 9017, ITAU,FPLT,CNS,FPLN,CEW
C
C                   ROUNDED VERSION OF THE FORECAST FOR CCRS
C
              CFP(I,1) = 0.1*ANINT (FPLT*10.0)
              CFP(I,2) = 0.1*ANINT (FPLN*10.0)
              FEW(I)   = PEW
c
c  convert to ccrs right now (skip 60 hr forecast)
c
            cfp(i,1) = anint (fplt*10.0)
	    if(cns.eq.'S')cfp(i,1)=-cfp(i,1)
            cfp(i,2) = anint (fpln*10.0)
	    if(pew.eq.'E'.and.cfp(i,2).ne.0.0) cfp(i,2)=3600-cfp(i,2)
            cfp(i,3) = 0

  230       CONTINUE
C
C*****************  WRITE THE CCRS TPAC FORECAST TO TAPE 33  ***********
C
cx          WRITE (33,9050)
cx   1      24,CFP(2,1),CNS,CFP(2,2),FEW(2),
cx   2      48,CFP(4,1),CNS,CFP(4,2),FEW(4),
cx   3      72,CFP(6,1),CNS,CFP(6,2),FEW(6)
c9050       FORMAT (3('  ** HPAC **  ',I2,15X,F4.1,A1,2X,F5.1,A1,/))
	    

c  set the 5th element to 72 hour fcst for ease of writing
	    cfp(5,1)= cfp(6,1)
	    cfp(5,2)= cfp(6,2)
	    cfp(5,3)= cfp(6,3)

          do ii=1, 5
             do jj=1, 3
                ltlnwnd(ii,jj) = int( cfp(ii,jj) )
             enddo
          enddo
          call writeAid( 60, strmid, cent, cdtg, 'HPAC', ltlnwnd )
          ENDIF
C
        ELSE
C
C*****************  MISSING 12-HOUR OLD POSITION  **********************
C
C******             WRITE THE CCRS XTRP FORECAST TO TAPE 33
C
cx        WRITE (33,9060)
cx   1    24,0.0,CNS,0.0,FEW(2),
cx   2    48,0.0,CNS,0.0,FEW(4),
cx   3    72,0.0,CNS,0.0,FEW(6)
c9060     FORMAT (3('  ** XTRP **  ',I2,15X,F4.1,A1,2X,F5.1,A1,/))
C
C******             WRITE THE CCRS TPAC FORECAST TO TAPE 33
C
cx        WRITE (33,9070)
cx   1    24,0.0,CNS,0.0,FEW(2),
cx   2    48,0.0,CNS,0.0,FEW(4),
cx   3    72,0.0,CNS,0.0,FEW(6)
c9070     FORMAT (3('  ** TPAC **  ',I2,15X,F4.1,A1,2X,F5.1,A1,/))
C
        ENDIF
      ELSE
        CLOSE (33)
        STOP 'TCLIM: ARQ INPUT PROBLEM'
      ENDIF
C
      CLOSE (33)
      STOP 'TCLIM: GOOD STOP'
C
  900 continue
      print *, 'error opening:',filename
      stop 'TCLIM: OPEN FILE ERROR'

      END

      SUBROUTINE RDCARQ (cent, IERR1)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  RDCARQ
C
C  DESCRIPTION:  READ CARQ MESSAGE FOR TROPICAL CYCLONE SUPPORT
c                Current version reads best track for cyclone info.
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON   (CSC)  APRIL 1991
C
C  CURRENT PROGRAMMER, DATE:  B. SAMPSON, JULY 1995
C
C  USAGE (CALLING SEQUENCE):  CALL RDCARQ (IERR1)
C
C  INPUT PARAMETERS:  NONE
C
C  OUTPUT PARAMETERS:
C     cent  - century of last best track position                  
C     IERR1 - ERROR FLAG, 0 NO ERROR, NON-ZERO ARQ MESSAGE PROBLEM
C
C  INPUT FILES:  TAPE33
C
C  COMMON BLOCKS:  SEE BELOW
C
C  ERROR CONDITIONS:  BAD CARQ MESSAGE
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C        <CHANGE NOTICE>  B. SAMPSON  JULY, 1995
C         CARQ DATA NOW READ FROM BEST TRACK   
c        sampson nrl Nov 98  cent = century of last bt position
C
C........................END PROPLOGUE..................................
C
      CHARACTER*1 CBASN1
      CHARACTER*2 CBASN2,CSTRMK,CYEAR
      CHARACTER*3 CYCNAM
      CHARACTER*80 CARD
      character*100 storms,filename
      character*8 cdtg12
      character*6 strmid
      character*2 century
      character*2 cent
      character*8 btdtg
      character   btns*1, btew*1
      integer     ios, iarg
      integer     ibtwind
      real        btlat, btlon

C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C
      CHARACTER CNAME*6, CDTG*8, CNS*1, CEW*1, EW12*1
      character *8 tdtg
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG
C   FLN   - FIX LONGITUDE, DEG
C   PLT12 - PAST 12 HR LATITUDE, DEG
C   PLN12 - PAST 12 HR LONGITUDE, DEG
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C*****              INITIALIZE FINDING FLAGS
C
      ICNAM = 0
      ICDTG = 0
      ICFIX = 0
      ICP00 = 0
      ICP12 = 0
      NREGN = 0
      IERR1 = 0
      FLT   =   0.0
      FLN   =   0.0
      FWD   = -99.0
      PLT12 =   0.0
      PLN12 =   0.0

c*************  This code added to read best track ...bs 7/5/95 *******
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
      print *,'          tclim forecast for ',strmid
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      write(33,'(a,a)') 'filename:',filename
      open (92,file=filename,status='old',err=701)
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
         call readBT( 92,cent,tdtg,btlat,btns,btlon,btew,ibtwind,ios )
         if (tdtg.ne.'        ') cdtg=tdtg
      enddo

      write(33,'(a,a)') 'cdtg:',cdtg
c
c  now find the current, -12, and -24 hr positions
c
      call icrdtg (cdtg,cdtg12,-12)
cx    call icrdtg (cdtg,cdtg24,-24)
      rewind 92
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 92,cent,btdtg,btlat,cns,btlon,btew,ibtwind,ios )
         if( ios .eq. 0 ) then
            if( btdtg .eq. cdtg12 ) then
               plt12 = btlat
               plon12 = btlon
               ew12 = btew
            else if( btdtg .eq. cdtg ) then
               flt = btlat
               flon = btlon
               cew = btew
               fwd = float(ibtwind)
            endif
         endif
      enddo

      write(33,*)'plt12,cns,plon12,ew12:'
      write(33,*) plt12,cns,plon12,ew12
      write(33,*) 'flt,cns,flon,cew,fwd:'
      write(33,*)  flt,cns,flon,cew,fwd
      close (92)
       
	
c*****************   end of read best track data ********************



C
C*****              INPUT THE CARQ DATA
C
cx    DO 110 IC=1, 10000
cx      READ (33,500,END=199) CARD
cx500   FORMAT (A80)
cx      IF (CARD(1:4) .EQ. 'ID T') THEN
C
C*************    EXTRACT CYCLONE NUMBER AND BASIN  ********************
C
          ICNAM  = -1
cx        CYCNAM = CARD(7:9)
          IF (CYCNAM(1:1) .EQ. ' ') CYCNAM(1:1) = '0'
          CSTRMK = CYCNAM(1:2)
          CBASN1 = CYCNAM(3:3)
          IF (CBASN1.EQ.'S' .OR. CBASN1.EQ.'P') THEN
C                   SOUTHERN HEMISPHERE CYCLONE
            NSIND = -1
          ELSE
C                   NORTHERN HEMISPHERE CYCLONE
            NSIND = 1
          ENDIF
C
cx      ELSEIF (CARD(1:3).EQ.'DTG') THEN
C
C*************    EXTRACT DTG    *********************
C
cx        CDTG  = CARD(7:14)
          CYEAR = CDTG(1:2)
          READ (CDTG,501) IYR,MON,IDAY,IHR
  501     FORMAT (4I2)
C                   CHECK VALIDITY OF REPORTED DTG
          IF (JAYDAY (IYR,MON,IDAY).NE.0 .AND. MOD (IHR,6).EQ.0)
     .       ICDTG = -1
  
cx      ELSEIF (CARD(1:7) .EQ. 'INITIAL') THEN
C
C*************    EXTRACT PRESENT POSITION     *********************
C
          ICFIX = -1
cx        READ (CARD,502) FLT,CNS,FLON,CEW
cx502     FORMAT (16X,F4.1,A1,1X,F5.1,A1)
          IF (FLT.GT.1.0 .AND. FLT.LE.60.0 .AND.
     .        FLON .LE. 180.0) ICP00 = -1
          IF (CNS .EQ. 'N') THEN
C                  CHECK HEMISPHERE CALCULATION FLAG FOR NORTHERN OCEANS
            IF (NSIND .NE. 1) NSIND = -99
          ELSEIF (CNS .EQ. 'S') THEN
C                  CHECK HEMISPHERE CALCULATION FLAG FOR SOUTHERN OCEANS
            IF (NSIND .NE. -1) NSIND = -99
C
C****************** MAKE SOUTHERN HEMISPHERE LATITUDE NEGATIVE *********
C
            FLT = -FLT
          ELSE
C                   SET FLAG FOR BAD LATITUDE INDICATOR
            NSIND = 0
          ENDIF
C                   SET FLAG FOR BAD LONGITUDE INDICATOR, AS REQUIRED
          IF (CEW.NE.'E' .AND. CEW.NE.'W') NSIND = 0
C
          FLN = FLON
          IF (NSIND .EQ. 1) THEN
            IF (CEW.EQ.'E' .AND. FLN.LT.100.0) THEN
C                           AREA IS NORTH INDIAN OCEAN
              NREGN = 3
            ELSEIF (CEW.EQ.'E' .AND. FLN.LE.180.0) THEN
C                           AREA IS NORTHWEST PACIFIC
              NREGN = 1
            ELSEIF (CEW.EQ.'W' .AND. FLN.GE.80.0 .AND.
     .             (CBASN1.EQ.'E' .OR. CBASN1.EQ.'C')) THEN
C                           AREA IS EASTERN NORTH PACIFIC
              NREGN = 2
C
C*******************  MAKE LONGITUDE 0 - 360 EAST  ********************
C
              FLN   = 360.0 -FLN
            ELSEIF (CEW .EQ. 'W') THEN
C                             MUST BE AN ATLANTIC CYCLONE
              IERR1 = -99
            ENDIF
          ELSEIF (NSIND .EQ. -1) THEN
            IF (CEW.EQ.'E' .AND. FLN.LT.100.0) THEN
C                           AREA IS SOUTHWEST INDIAN OCEAN
              NREGN = 4
            ELSE
C                           AREA IS SOUTH PACIFIC
              NREGN = 5
              IF (CEW .EQ. 'W') FLN = 360.0 -FLN
            ENDIF
          ENDIF
          IF (IERR1.EQ.-99 .OR. CBASN1.EQ.'L') THEN
            PRINT 610, CYCNAM ,CDTG
  610       FORMAT (' NO TCLIMO - ATLANTIC BASIN ',A3,' AT ',A8)
            IERR1 = -99
          ELSEIF (NSIND .EQ. -99) THEN
            PRINT 615, CYCNAM, CDTG
  615       FORMAT (' NO TCLIMO - WRONG BASIN INDICATED FOR ',A3,
     .              ' AT ',A8)
C           IERR1 = -88
          ELSEIF (NREGN .EQ. 0) THEN
            PRINT 616, CYCNAM, CDTG
  616       FORMAT (' NO TCLIMO - NO AGREEMENT LAT/LON AND BASIN FOR '
     .              ,A3,' AT ',A8)
C           IERR1 = -88
          ENDIF
C
C****************** TERMINATE FURTHER READING OF ARQ MESSAGE ***********
C******************        IF FATAL ERRORS SO FAR            ***********
C
          IF (IERR1 .NE. 0) GOTO 300
C
cx      ELSEIF (CARD(4:8) .EQ. 'HOUR') THEN
C
C*************      EXTRACT PREVIOUS 12-HOUR POSITION     **************
C
cx        READ (CARD,503) ITIME
cx503     FORMAT (I2)
cx        IF (ITIME .EQ. 12) THEN
C
C                         12-HR OLD POSIT
C
cx          READ (CARD,504) PLT12,PLON12,EW12
cx504       FORMAT (16X,F4.1,2X,F5.1,A1)
            IF (PLT12.GT.1.0 .AND. PLT12.LE.60.0 .AND.
     .          PLON12 .LE. 180.0) ICP12 = -1
            PLT12 = SIGN (PLT12,FLT)
            IF (EW12 .EQ. 'E') THEN
              PLN12 = PLON12
            ELSEIF (EW12 .EQ. 'W') THEN
              PLN12 = 360.0 -PLON12
            ENDIF
cx        ENDIF
C
cx      ELSEIF (CARD(1:3) .EQ. 'MAX') THEN
C
C*************  EXTRACT PRESENT MAXIMUM WIND SPEED  ********************
C
cx        READ (CARD,505) FWD
cx505     FORMAT (9X,F3.0)
cx      ENDIF
cx110 CONTINUE
C
C******             NO MORE CARQ DATA
C
  199 CONTINUE
C
C******             CHECK ON EXTRACTION
C
      IF (ICNAM.EQ.0 .OR. ICDTG.EQ.0) THEN
        WRITE (*,620)
  620   FORMAT (1X,'NO TCLIMO - MISSING CYCLONE NAME AND/OR DTG')
        IERR1 = -77
      ENDIF
      IF (IERR1 .EQ. 0) THEN
C
C*****              CHANGE BASIN INDICATOR FROM ONE LETTER TO TWO
C
        IF (CBASN1 .EQ. 'W') THEN
C                   NORTHWEST PACIFIC
          CBASN2 = 'WP'
        ELSEIF (CBASN1.EQ.'A' .OR. CBASN1.EQ.'B') THEN
C                   ARABIAN OR BAY OF BENGAL
          CBASN2 = 'IO'
        ELSEIF (CBASN1.EQ.'C' .OR. CBASN1.EQ.'E') THEN
C                   EASTERN NORTH PACIFIC, INCLUDING CENTRAL
          CBASN2 = 'EP'
        ELSEIF (CBASN1.EQ.'S' .OR. CBASN1.EQ.'P') THEN
C                   SOUTH INDIAN OR PACIFIC OCEANS
          CBASN2 = 'SH'
        ELSE
C                   UNKNOWN BASIN IDICATOR
          CBASN2 = 'XX'
        ENDIF
C
C*****              COMPLETE NAME
C
        WRITE (CNAME,630) CBASN2,CSTRMK,CYEAR
  630   FORMAT (A2,A2,A2)
        WRITE (*,640) CNAME,CDTG,
     .                ABS(PLT12),CNS,PLON12,EW12,
     .                ABS(FLT),CNS,FLON,CEW,FWD
  640   FORMAT (//,' TCLIMO PROCESSING ',A6,' AT ',A8,/,
     .          6X,'12-HR OLD : ',F4.1,A1,1X,F5.1,A1,/,
     .          6X,' START AT : ',F4.1,A1,1X,F5.1,A1,' WIND ',F4.0,//)
C
C******       CHECK WHICH POSITIONS ARE AVAILABLE
C
        IF (ICFIX.EQ.0 .OR. ICP00.EQ.0) THEN
cx        WRITE (*,650)  CNAME,CDTG
          write (*,650)  cname,cdtg
  650     FORMAT (' TCLIMO, MISSING OR BAD 00-HR POSITION FOR ',A6,
     .            ' AT ',A8)
          IERR1 = -1
        ELSEIF (ICP12 .EQ. 0) THEN
cx        WRITE (*,660)  CNAME,CDTG
          write (33,660)  cname,cdtg
  660     FORMAT (' TCLIMO, MISSING OR BAD 12-HR OLD POSITION FOR ',
     .            A6,' AT ',A8)
        ELSE
C                   CHECK SPEED AND DIRECTION
          PLT1 = SIGN (PLT12,FLT)
          PLT2 = FLT
          CALL HEDIST (PLT1,PLN12,PLT2,FLN,DIR,DST,RDIR,RDST)
          SPD12 = DST/12.0
cx        WRITE (*,670) SPD12,DIR
          write (33,670) spd12,dir
  670     FORMAT (' TCLIMO, LAST 12-HR SPEED ',F6.2,' DIR ',F5.1)
          IF (SPD12 .GT. 60.0) THEN
C                   SET 12-HR PAST POSITION TO MISSING
            PLT12 = 0.0
            PLN12 = 0.0
          ENDIF
        ENDIF
      ENDIF
  300 CONTINUE
      RETURN
  701 continue
      write (*,*) 'tclimo, open error on input file:',filename
      ierr1 = -1
      go to 300
C
      END
      SUBROUTINE CLIMO (NDAYS,RADIUS,NC24,NC48,NC72)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  CLIMO
C
C  DESCRIPTION:  MAKE TROPICAL CYCLONE CLIMATOLOGY FORECAST
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON   (CSC)  APRIL 1991
C
C  CURRENT PROGRAMMER, DATE:
C
C  USAGE (CALLING SEQUENCE):  CALL CLIMO (NDAYS,RADIUS,NC24,NC48,NC72)
C
C  INPUT PARAMETERS:
C     NDAYS  - NUMBER OF DAYS, PLUS MINUS TO SEARCH
C     RADIUS - SEARCH RADIUS, N.M.
C
C  OUTPUT PARAMETERS:
C     NC24   - NUMBER OF ANALOGS/FORECASTS FOR TAU 24
C     NC48   - NUMBER OF ANALOGS/FORECASTS FOR TAU 48
C     NC72   - NUMBER OF ANALOGS/FORECASTS FOR TAU 72
C
C  INPUT FILES:  CLIMATOLOGY FILES ON UNIT NUNIT FROM SHARDSK, ID=OP
C                NAMES ARE CALCULATED ON THE FLY
C
C  COMMON BLOCKS:  SEE BELOW
C
C  ERROR CONDITIONS:  NOT ENOUGH CLIMATOLOGY TO MAKE FORECAST
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C         CACULATE JULIAN DATE
C         CALCULATE STARTING MONTH INDEX
C         CALCULATE ENDING MONTH INDEX
C     110 CONTINUE
C         READ ENTIRE CYCLONE TRACK (99 MAX)
C            CHECK SCREENS, TIME THEN DISTANCE
C               FIRST PASS OF TIME AND DISTANCE:
C                  CHECK THAT A TAU 24 EXISTS (1-6, OTHERS-12 HR)
C                     PERFORM CPA CHECK
C                        CHECK THAT A TAU 24 EXISTS:
C                           CALCULATE TAU 0 OFFSETS
C                           CALCULATE RUNNING AVERAGE OF FORECAST
C                                     POSITIONS AND WINDS
C                           GOTO 110
C
C  RECORD OF CHANGES:
C
C   <<CHANGE NOTICE>>  CLIMO*01  (13 DEC 1992)  --  HAMILTON,H.
C            CORRECT ERROR IN CALCULATING STARTING JULIAN DATE
C            FOR FIRST PART OF NEW YEAR
C
C........................END PROPLOGUE..................................
C
      CHARACTER CMONTH(12)*3, CREGS(5)*4, REGFILE*7, CSTR*30
      character*80   dir, filename
C
      LOGICAL KONTIG
C
      DIMENSION NDST(99), NPTR(99), CCC(18)
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C
      CHARACTER CNAME*6, CDTG*8, CNS*1, CEW*1, EW12*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG
C   FLN   - FIX LONGITUDE, DEG
C   PLT12 - PAST 12 HR LATITUDE, DEG
C   PLN12 - PAST 12 HR LONGITUDE, DEG
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12
C
C
C                   EXPLANATION OF /STORMC/ VARIABLES
C
C   STNAME - NAME OF CLIMATOLOGY TROPICAL CYCLONE
C   STYPE  - TYPE OF TRACK INDICATOR
C
      CHARACTER STYPE*1, STNAME*8
C
      COMMON /STORMC/ STNAME,STYPE
C
C                   EXPLANATION OF /STORM/ VARIABLES
C
C         IYR    - YEAR OF FIRST POSITION OF CYCLONE
C         JDAY   - JULIAN DAY OF POSITION
C         IHR    - HOUR OF POSITION
C         XLON   - LONGITUDE OF POSITION, (0 - 360) EAST
C         YLAT   - LATITUDE  OF POSITION, (DEG - ALL POSITIVE)
C         WIND   - MAXIMUM SUSTAINED WIND SPEED, (KT)
C         NR     - NUMBER OF RECORDS READ
C
      COMMON /STORM/ IYR(99),JDAY(99),IHR(99),XLON(99),YLAT(99),
     .               WIND(99),NR
C
C
C                   EXPLANATION OF /CLIM/ VARIABLES
C
C   CLTXX - FORECAST LATITUDE  AT XX HOURS, BASED UPON CLIMATOLOGY
C   CLNXX - FORECAST LONGITUDE AT XX HOURS, BASED UPON CLIMATOLOGY
C   CWDXX - FORECAST MAXIMUM SUSTAINED WIND SPEED (KT) AT XX HOURS,
C           BASED UPON CLIMATOLOGY
C
      COMMON/CLIM/ CLT12,CLT24,CLT36,CLT48,CLT60,CLT72,
     .             CLN12,CLN24,CLN36,CLN48,CLN60,CLN72,
     .             CWD12,CWD24,CWD36,CWD48,CWD60,CWD72
C
      EQUIVALENCE (CCC(1),CLT12)
C
C                   SET LOCAL FILE NAME TO TAPE2
C                   NEPAJAN - DUMMY FILENAME, CALCULATED ON FLY
C                   SET ID TO OP AND INDICATE DISK PACK SHARDSK
      DATA CSTR/'TAPE2,NEPAJAN,ID=OP,SN=SHARDSK'/
C                   FIRST FOUR CHARACTERS OF FILENAMES
      DATA CREGS/'NWPA', 'NEPA', 'NOIN', 'SWIN', 'SWPA'/
C                   LAST THREE CHARACTERS OF FILENAMES
      DATA CMONTH/'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
     .            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'/
C
C                   SET UNIT NUMBER FOR CLIMATOLOGY DATA
      DATA NUNIT/2/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C*****************  CACULATE JULIAN DATE OF FIX POSITION  **************
C
      READ (CDTG,501) IFYR,IFMON,IFDAY
  501 FORMAT (3I2)
      JFDATE = JAYDAY (IFYR,IFMON,IFDAY)
C
C*****************  CALCULATE STARTING MONTH INDEX  ********************
C
      JSDATE = JFDATE -NDAYS
      JSYR   = IFYR
      IF (JSDATE .LT. 1) THEN
        JSYR = JSYR -1
        IF (JSYR .LT. 0) JSYR = 99
        IF (MOD (JSYR,4) .EQ. 0) THEN
          JDAYS = 366
        ELSE
          JDAYS = 365
        ENDIF
        JSDATE = JDAYS +JSDATE
      ENDIF
C                   OBTAIN STARTING KMONS AND KDAYS
      CALL IJAYDAY (JSYR,JSDATE,KMONS,KDAYS)
C
C*****************  CALCULATE ENDING MONTH INDEX  **********************
C
      JEDATE = JFDATE +NDAYS
      JEYR   = IFYR
      IF (MOD (JEYR,4) .EQ. 0) THEN
        JDAYS = 366
      ELSE
        JDAYS = 365
      ENDIF
      IF (JEDATE .GT. JDAYS) THEN
        JEYR   = JEYR +1
        JEDATE = JEDATE -JDAYS
      ENDIF
C                   OBTAIN ENDING KMONE AND KDAYE
      CALL IJAYDAY (JEYR,JEDATE,KMONE,KDAYE)
C
      MO  = KMONS
      MOX = KMONE +1
      IF (MOX .EQ. 13) MOX = 1
cx    PRINT 9010, CMONTH(MO),CMONTH(MOX)
      write(33,9010) cmonth(mo),cmonth(mox)
 9010 FORMAT (' TCLIMO, CLIMO USING OBSERVATIONS STARTING IN ',A3,
     . ' AND STOPPING BEFORE THE FOLLOWING ',A3)
      IF (KMONE .GT. MO) THEN
C                   MONTHS OF TIME WINDOW DONT CROSS FROM DEC TO JAN
        KONTIG = .TRUE.
      ELSE
C                   MONTHS OF TIME WINDOW CROSS FROM DEC TO JAN
        KONTIG = .FALSE.
      ENDIF
      IF (NREGN .EQ. 1) THEN
C                   CLIMATOLOGY OBSERVATIONS ARE 6 HOURS APART
        MNNR = 5
        MN12 = 2
        MN24 = 4
        MN36 = 6
        MN48 = 8
        MN60 = 10
        MN72 = 12
      ELSE
C                   CLIMATOLOGY OBSERVATIONS ARE 12 HOURS APART
        MNNR = 3
        MN12 = 1
        MN24 = 2
        MN36 = 3
        MN48 = 4
        MN60 = 5
        MN72 = 6
      ENDIF
      KP12 = 0
      KW12 = 0
      KP24 = 0
      KW24 = 0
      KP36 = 0
      KW36 = 0
      KP48 = 0
      KW48 = 0
      KP60 = 0
      KW60 = 0
      KP72 = 0
      KW72 = 0
      NC24 = 0
      NC48 = 0
      NC72 = 0
      NCTW = 0
      NCTD = 0
      NCR  = 0
C
C                   ZERO OUT ALL FORECASTS OF POSITION AND WIND
C
      DO 110 N=1, 18
        CCC(N) = 0.0
  110 CONTINUE
cx    PRINT 9015, FLT, FLN, FWD
      write(33,9015) flt, fln, fwd
 9015 FORMAT(' TCLIMO, CLIMO STARTING AT ',F5.1,', ',F5.1,' WIND ',F4.0)
C
C********  READ CYCLONE CLIMATOLOGY FILE, ONE COMPLETE CYCLONE AT A TIME
C
C                   CALCULATE CLIMATOLOGY FILENAME
      REGFILE(1:4) = CREGS(NREGN)
  120 CONTINUE
      REGFILE(5:7) = CMONTH(MO)
c
c  filenames are now all lower case
c
      call locase (regfile,7)

cx    PRINT 9020, REGFILE
      write(33,9020) regfile
 9020 FORMAT (' TCLIMO, CLIMO CHECKING CYCLONE HISTORY FILE: ',A7)
      CSTR(7:13) = REGFILE
C                   WARNING: USE DELETE ON CDC MAINFRAME ONLY
cx    CLOSE (NUNIT,STATUS='DELETE')
cx    CALL ATTACH (CSTR,IERC,ICYL)
      ierc=0
      close (nunit)
      IF (IERC .EQ. 0) THEN
C
C                   THIS MONTH'S FILE IS AVAILABLE
C                   OTHERWISE, GO ON TO THE NEXT FILE/MONTH
C
cx      PRINT 9030, REGFILE, ICYL
c9030   FORMAT (' TCLIMO, CLIMO OPENING HISTORY FILE ',A7,' CYCLE ',I3)
        write(33,9030) regfile
 9030   FORMAT (' TCLIMO, CLIMO OPENING HISTORY FILE ',A7)
cx      OPEN (NUNIT,FILE='TAPE2',ACCESS='SEQUENTIAL',FORM='FORMATTED',
cx   .        STATUS='OLD',IOSTAT=ISTATUS)
c
c  get the standalone directory
c
	call getenv("STANDALONE",dir)
	ind=index(dir," ")-1
c
c  put full path name into character array
c
	write(filename,'(a,a,a)')dir(1:ind),'/tyan_dat/',regfile
	write(33,'(a,a)')'filename:',filename
c
c  open climatology data file
c
	open (nunit,file=filename,
     .        access='SEQUENTIAL', form='FORMATTED',
     .        status='OLD',iostat=istatus)

	IF (ISTATUS .EQ. 0) THEN
cx        PRINT 9040, REGFILE
          write(33,9040) regfile
 9040     FORMAT (' TCLIMO, CLIMO PROCESSING HISTORY FILE ',A7)
          REWIND (NUNIT)
C                   SET END-OF-FILE FLAG TO NO EOF.
          IEOF = 0
  130     CONTINUE
C
C                    READ A COMPLETE SET OF NR CLIMATOLOGY OBSERVATIONS
C
          CALL RDCLIMO (NUNIT,NREGN,IEOF)
          NCR = NCR +1
CCC       PRINT*,'CLIMO, PROCESSING ',NR,' OBSERVATIONS OF ',STNAME
C
C                   IF OBSERVATION SET IF LESS THAN MNNR, DO NOT USE
C
          IF (NR .GE. MNNR) THEN
C
C****************  PROCESS CYCLONE OBSERVATIONS  ***********************
C
            NS = 0
            DO 140 N=1, NR -MN24
              IF (KONTIG) THEN
                IF (JDAY(N).GE.JSDATE .AND. JDAY(N).LE.JEDATE) THEN
C                             SET KONT TO CONTINUE PROCESSING
                  KONT = -1
                ELSE
C                             CLIMATOLOGY DATE OUTSIDE TIME WINDOW
                  KONT = 0
                ENDIF
              ELSE
                IF ((JDAY(N).GE.JSDATE .AND. JDAY(N).LE.366) .OR.
     .               JDAY(N).LE.JEDATE) THEN
C                             SET KONT TO CONTINUE PROCESSING
                  KONT = -1
                ELSE
C                             CLIMATOLOGY DATE OUTSIDE TIME WINDOW
                  KONT = 0
                ENDIF
              ENDIF
              IF (KONT .NE. 0) THEN
C
C*************************  PASSED TIME WINDOW SCREEN  *****************
C
                NCTW = NCTW +1
                CALL HEDIST(FLT,FLN,YLAT(N),XLON(N),HED,DST,RHED,RDST)
                IF (DST .LE. RADIUS) THEN
C
C*************************  PASSED DISTANCE SCREEN  ********************
C
C                          THERE IS AT LEAST A TAU 24 POSITION FROM THIS
C                          POSITION, SO SAVE POINTER AND DISTANCE
                  NCTD = NCTD +1
                  NS = NS +1
                  NPTR(NS) = N
                  NDST(NS) = DST
                ENDIF
              ENDIF
  140       CONTINUE
            IF (NS .NE. 0) THEN
C                     FIND CLOSEST POINT OF APPROACH (CPA) OF CYCLONE
              MNDST = RADIUS +1.1
              DO 150 N=1, NS
                IF (NDST(N) .LT. MNDST) THEN
                  MNDST = NDST(N)
                  NMIN  = NPTR(N)
                ENDIF
  150           CONTINUE
C                    CALCULATE TAU 0 OFFSETS
              OFFLT = FLT -YLAT(NMIN)
              OFFLN = FLN -XLON(NMIN)
              IF (WIND(NMIN) .GT. 0.0) THEN
                OFFWD = FWD -WIND(NMIN)
                KALWD = -1
              ELSE
                KALWD = 0
              ENDIF
              KP12 = KP12 +1
C                        CALCULATE RUNNING LAT AND LON 12 HR FORECAST
              CLT12 = (CLT12*(KP12 -1) +YLAT(NMIN+MN12) +OFFLT)/KP12
              CLN12 = (CLN12*(KP12 -1) +XLON(NMIN+MN12) +OFFLN)/KP12
              IF (KALWD.NE.0 .AND. WIND(NMIN+MN12).GT.0.0) THEN
C                         CALCULATE RUNNING WIND 12 HR FORECAST
                KW12  = KW12 +1
                CWD12 = (CWD12*(KW12 -1) +WIND(NMIN+MN12) +OFFWD)/KW12
              ENDIF
              KP24 = KP24 +1
C                        CALCULATE RUNNING LAT AND LON 24 HR FORECAST
              CLT24 = (CLT24*(KP24 -1) +YLAT(NMIN+MN24) +OFFLT)/KP24
              CLN24 = (CLN24*(KP24 -1) +XLON(NMIN+MN24) +OFFLN)/KP24
              IF (KALWD.NE.0 .AND. WIND(NMIN+MN24).GT.0.0) THEN
C                         CALCULATE RUNNING WIND 24 HR FORECAST
                KW24  = KW24 +1
                CWD24 = (CWD24*(KW24 -1) +WIND(NMIN+MN24) +OFFWD)/KW24
              ENDIF
              IF (NMIN+MN36 .LE. NR) THEN
C                       CALCULATE 36 HOUR FORECASTS
                KP36 = KP36 +1
C                        CALCULATE RUNNING LAT AND LON 36 HR FORECAST
                CLT36 = (CLT36*(KP36 -1) +YLAT(NMIN+MN36) +OFFLT)/KP36
                CLN36 = (CLN36*(KP36 -1) +XLON(NMIN+MN36) +OFFLN)/KP36
                IF (KALWD.NE.0 .AND. WIND(NMIN+MN36).GT.0.0) THEN
C                         CALCULATE RUNNING WIND 36 HR FORECAST
                  KW36  = KW36 +1
                  CWD36 = (CWD36*(KW36 -1) +WIND(NMIN+MN36) +OFFWD)/
     .                     KW36
                ENDIF
                IF (NMIN+MN48 .LE. NR) THEN
C                          CALCULATE 48 HOUR FORECASTS
                  KP48 = KP48 +1
C                           CALCULATE RUNNING LAT AND LON 48 HR FORECAST
                  CLT48 = (CLT48*(KP48 -1) +YLAT(NMIN+MN48) +OFFLT)/
     .                     KP48
                  CLN48 = (CLN48*(KP48 -1) +XLON(NMIN+MN48) +OFFLN)/
     .                     KP48
                  IF (KALWD.NE.0 .AND. WIND(NMIN+MN48).GT.0.0) THEN
C                            CALCULATE RUNNING WIND 48 HR FORECAST
                    KW48  = KW48 +1
                    CWD48 = (CWD48*(KW48 -1) +WIND(NMIN+MN48) +OFFWD)/
     .                      KW48
                  ENDIF
                  IF (NMIN+MN60 .LE. NR) THEN
C                           CALCULATE 60 HOUR FORECASTS
                    KP60 = KP60 +1
C                           CALCULATE RUNNING LAT AND LON 60 HR FORECAST
                    CLT60 = (CLT60*(KP60 -1) +YLAT(NMIN+MN60) +OFFLT)/
     .                       KP60
                    CLN60 = (CLN60*(KP60 -1) +XLON(NMIN+MN60) +OFFLN)/
     .                       KP60
                    IF (KALWD.NE.0 .AND. WIND(NMIN+MN60).GT.0.0) THEN
C                              CALCULATE RUNNING WIND 60 HR FORECAST
                      KW60  = KW60 +1
                      CWD60 = (CWD60*(KW60 -1) +WIND(NMIN+MN60)
     .                        +OFFWD)/KW60
                    ENDIF
                    IF (NMIN+MN72 .LE. NR) THEN
C                           CALCULATE 72 HOUR FORECASTS
                      KP72 = KP72 +1
C                           CALCULATE RUNNING LAT AND LON 72 HR FORECAST
                      CLT72 = (CLT72*(KP72 -1) +YLAT(NMIN+MN72)
     .                        +OFFLT)/KP72
                      CLN72 = (CLN72*(KP72 -1) +XLON(NMIN+MN72)
     .                        +OFFLN)/KP72
                      IF (KALWD.NE.0 .AND. WIND(NMIN+MN72).GT.0.0)THEN
C                              CALCULATE RUNNING WIND 72 HR FORECAST
                        KW72  = KW72 +1
                        CWD72 = (CWD72*(KW72 -1) +WIND(NMIN+MN72)
     .                          +OFFWD)/KW72
                      ENDIF
                    ENDIF
                  ENDIF
                ENDIF
              ENDIF
            ENDIF
C                   READ NEXT SET OF CLIMATOLOGY OBSERVATIONS, IF NO EOF
            IF (IEOF .EQ. 0) GOTO 130
C
          ELSEIF (IEOF .EQ. 0) THEN
cx          PRINT*,'TCLIMO, CLIMO NOT ENOUGH OBS FOR ',STNAME
            write(33,*)'TCLIMO, CLIMO NOT ENOUGH OBS FOR ',stname
C                   READ NEXT SET OF CLIMATOLOGY OBSERVATIONS
            GOTO 130
C
          ELSE
cx          PRINT*,'TCLIMO, CLIMO NOT ENOUGH OBS FOR ',STNAME
cx          PRINT*,'TCLIMO, CLIMO EOF REACHED FOR MONTH ',CMONTH(MO)
            write(33,*)'TCLIMO, CLIMO NOT ENOUGH OBS FOR ',STNAME
            write(33,*)'TCLIMO, CLIMO EOF REACHED FOR MONTH ',CMONTH(MO)
          ENDIF
        ELSE
cx        PRINT*,'TCLIMO, ***** CLIMO OPEN ERROR IS ',ISTATUS,' *****'
          write(33,*)'TCLIMO, **** CLIMO OPEN ERROR IS ',ISTATUS,' ****'
        ENDIF
      ELSE
cx      PRINT*,'TCLIMO, ***** CLIMO ATTACH ERROR IS ',IERC,' *****'
        write(33,*)'TCLIMO, ***** CLIMO ATTACH ERROR IS ',IERC,' *****'
      ENDIF
C                 IF FILE NOT OK OR IF END REACHED, TRY THE NEXT MONTH
      MO = MO +1
      IF (MO .EQ. 13) MO = 1
      IF (MO .NE. MOX) GOTO 120
C
C                   WARNING: USE DELETE ON CDC MAINFRAME ONLY
cx    CLOSE (NUNIT,STATUS='DELETE')
      close (nunit)
C
C            THAT'S ALL THE DATA WITHIN +/- NDAYS DAYS OF CARQ CYCLONE
C
      IF (KP24 .LE. 0) THEN
C                   NO 24, 48 OR 72 HOUR FORECAST WAS MADE
        WRITE (33,9140)
 9140   FORMAT (//,20X,' U N C L A S S I F I E D',//)
        WRITE (33,9150)
 9150   FORMAT (' INSUFFICIENT CYCLONES FOR CLIM **********')
        WRITE (33,9140)
      ENDIF
cx    PRINT*,'TCLIMO, CLIMO READ ',NCR,' CYCLONES, FOUND ',NCTW,
cx   .       ' IN TIME WINDOW, AND ',NCTD,' WITHIN ',RADIUS,
cx   .       'NM DISTANCE'
      PRINT*,' TOTAL OF ',NCR,' CYCLONES READ '
      PRINT*,' POSITS PASSED TIME RESTRICTION (',NDAYS,'DAYS):',NCTW
      PRINT*,' POSITS PASSED DISTANCE RESTRICTION (',RADIUS,'NM):',NCTD
      NC24 = KP24
      NC48 = KP48
      NC72 = KP72
cx    PRINT*,'TCLIMO, CLIMO MADE ',NC24,' 24HR ',NC48,' 48HR ',NC72,
cx   .       ' 72HR FORECASTS WITH ',NDAYS,' DAYS WINDOW'
      PRINT*,' POSITS USED IN 24HR FORECAST:',NC24
      PRINT*,' POSITS USED IN 48HR FORECAST:',NC48
      PRINT*,' POSITS USED IN 72HR FORECAST:',NC72
      print*, ' '
      RETURN
C
      END
      SUBROUTINE RDCLIMO (NUNIT,NREGN,IEOF)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME: RDCLIMO
C
C  DESCRIPTION:  READS ONE COMPLETE ANALOG TROPICAL CYCLONE, EACH RECORD
C            IS ONE OBSERVATION OUT OF THE COMPLETE SET OF OBSERVATIONS,
C            AND LOAD COMMON'S STORMC AND STORM
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON (CSC) APRIL 1991
C
C  CURRENT PROGRAMMER, DATE:
C
C  USAGE (CALLING SEQUENCE):  CALL RDCLIM (NUNIT,NREGN,IEOF)
C
C  INPUT PARAMETERS:
C    NUNIT - READ UNIT NUMBER
C    NREGN - INDEX TO BASIN OR REGION OF CYCLONE
C
C  OUTPUT PARAMETERS:  IEOF - END-OF-FILE INDICATOR
C                             0 - NO END OF FILE
C                             1 - END OF FILE REACHED
C
C  INPUT FILES BY REGIONS:  (XXX - THREE CHARACTER MONTH)
C         1 - NWPAXXX, NORTHWEST PACIFIC
C         2 - NEPAXXX, NORTHEAST PACIFIC
C         3 - NOINXXX, NORTH INDIAN
C         4 - SWINXXX, SOUTHWEST INDIAN
C         5 - SWPAXXX, SOUTHWEST PACIFIC (INCLUDES SE INDIAN OCEAN)
C
C  COMMON BLOCKS:  (SEE BELOW)
C
C  ERROR CONDITIONS: NONE
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:
C        VARIABLES IN EACH RECORD OF EACH MONTHLY FILE (IN SEQUENCE)
C
C  FOR: NWPA REGION
C
C      MON     - MONTH OF INITIAL TROPICAL CYCLONE OBSERVATION
C      JYR     - YEAR OF INITIAL TROPICAL CYCLONE OBS, LAST TWO DIGITS
C      IDSTORM - STORM NUMBER, MUST NOT CHANGE FOR A GIVEN CYCLONE
C      IOBSVID - OBSERVATION NUMBER, MUST BE IN ASCENDING ORDER
C      IOBSYR  - YEAR OF OBSERVATION
C      IOBSMON - MONTH OF OBSERVATION
C      IOBSDAY - DAY OF OBSERVATION
C      IOBSHR  - HOUR OF OBSERVATION
C      IOBSLAT - LATITUDE X10, (+N,-S)
C      IOBSLON - LONGITUDE X10, (+E, -W)
C  *   IHD12   - LAST 12-HOUR HEADING, (DEG)
C  *   ISPD12  - LAST 12-HOUR SPEED, (TENTHS OF KT)
C  *   IHD18   - LAST 18-HOUR HEADING, (DEG)
C  *   ISPD18  - LAST 18-HOUR SPEED, (TENTHS OF KT)
C  *   IHD24   - LAST 24-HOUR HEADING, (DEG)
C  *   ISPD24  - LAST 24-HOUR SPEED, (TENTHS OF KT)
C  *   IHD48   - LAST 48-HOUR HEADING, (DEG)
C  *   ISPD48  - LAST 48-HOUR SPEED, (TENTHS OF KT)
C  *   IRADIUS - RADIUS (SIZE), (DEG)
C  *   IDELRAD - LAST 12-HOUR CHANGE IN RADIUS, (DEG)
C  *   ISLPRES - MINIMUM SEA LEVEL PRESSURE, SLP, (MB)
C  *   IDELSLP - LAST 12-HOUR CHANGE IN SLP, (MB)
C      IWNDSPD - MAXIMUM SUSTAINED WIND SPEED, (KT)
C  *   MINHGT  - MINIMUM 700 MB HEIGHT, (TENS OF M)
C  *   IRDGLAT - 700 MB RIDGE LATITUDE, (TENTHS OF DEG)
C  *   IRDGHGT - 700 MB RIDGE HEIGHT, (TENS OF M)
C  *   ITROLON - 700 MB TROUGH LONGITUDE, (TENTHS OF DEG)
C  *   ITROHGT - 700 MB TROUGH HEIGHT, (TENS OF M)
C      IOBNAME - CYCLONE NAME
C  *   IOBTYPE - CYCLONE TYPE - (S - STRAIGHT, R - RECURVER, O - OTHER)
C
C  FOR: NEPA REGION
C
C      MON     - MONTH OF INITIAL TROPICAL CYCLONE OBSERVATION
C      JYR     - YEAR OF INITIAL TROPICAL CYCLONE OBS, LAST TWO DIGITS
C      IDSTORM - STORM NUMBER, MUST NOT CHANGE FOR A GIVEN CYCLONE
C      IOBSVID - OBSERVATION NUMBER, MUST BE IN ASCENDING ORDER
C      IOBSYR  - YEAR OF OBSERVATION
C      IOBSMON - MONTH OF OBSERVATION
C      IOBSDAY - DAY OF OBSERVATION
C      IOBSHR  - HOUR OF OBSERVATION
C      IOBSLAT - LATITUDE X10, (+N,-S)
C      IOBSLON - LONGITUDE X10, (+E, -W)
C      IWNDSPD - MAXIMUM SUSTAINED WIND SPEED, (KT)
C      IOBNAME - CYCLONE NAME
C  *   IOBTYPE - CYCLONE TYPE - (S - STRAIGHT, R - RECURVER, O - OTHER)
C
C  FOR:  NOIN, SWIN AND SWPA REGIONS
C
C      MON     - MONTH OF INITIAL TROPICAL CYCLONE OBSERVATION
C      JYR     - YEAR OF INITIAL TROPICAL CYCLONE OBS, LAST TWO DIGITS
C      IDSTORM - STORM NUMBER, MUST NOT CHANGE FOR A GIVEN CYCLONE
C      IOBSVID - OBSERVATION NUMBER, MUST BE IN ASCENDING ORDER
C      IOBSYR  - YEAR OF OBSERVATION
C      IOBSMON - MONTH OF OBSERVATION
C      IOBSDAY - DAY OF OBSERVATION
C      IOBSHR  - HOUR OF OBSERVATION
C      IOBSLAT - LATITUDE X10, (+N,-S)
C      IOBSLON - LONGITUDE X10, (+E, -W)
C  *   IHD12   - LAST 12-HOUR HEADING, (DEG)
C  *   ISPD12  - LAST 12-HOUR SPEED, (TENTHS OF KT)
C      IWNDSPD - MAXIMUM SUSTAINED WIND SPEED, (KT)
C      IOBNAME - CYCLONE NAME
C  *   IOBTYPE - CYCLONE TYPE - (S - STRAIGHT, R - RECURVER, O - OTHER)
C
C  *   THESE VALUES ARE NOT USED BY TCLIMO, BUT ARE IN THE CLIMATOLOGY
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     NONE, EXCEPT FOR COMMONS, WHICH ARE EXPLAINED BELOW
C
C  METHOD:
C     READ ONE COMPLETE ANALOG TROPICAL CYCLONE, EACH RECORD IS ONE
C     OBSERVATION OUT OF THE COMPLETE SET OF OBSERVATIONS,
C     AND LOAD COMMON'S STORMC AND STORM PRIOR TO RETURN.
C     NOTE, THERE ARE REGIONAL DIFFERENCES BETWEEN THE VARIABLES IN
C     COMMON.
C
C  RECORD OF CHANGES:
C
C     sampson nrl, june 96      eliminated bz in read formats
C
C........................END PROPLOGUE..................................
C
      CHARACTER*1 IOBTYPE*1, STRING*6, IOBNAME*8
C
C                   EXPLANATION OF /STORMC/ VARIABLES
C
C   STNAME - NAME OF CLIMATOLOGY TROPICAL CYCLONE
C   STYPE  - TYPE OF TRACK INDICATOR
C
      CHARACTER STYPE*1, STNAME*8
C
      COMMON /STORMC/ STNAME,STYPE
C
C                   EXPLANATION OF /STORM/ VARIABLES
C
C         IYR    - YEAR OF FIRST POSITION OF CYCLONE
C         JDAY   - JULIAN DAY OF POSITION
C         IHR    - HOUR OF POSITION
C         XLON   - LONGITUDE OF POSITION, (0 - 360) EAST
C         YLAT   - LATITUDE  OF POSITION, (DEG - ALL POSITIVE)
C         WIND   - MAXIMUM SUSTAINED WIND SPEED, (KT)
C         NR     - NUMBER OF RECORDS READ
C
      COMMON /STORM/ IYR(99),JDAY(99),IHR(99),XLON(99),YLAT(99),
     .               WIND(99),NR
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IEOF   = 0
      IOBSVN = 0
C                   COUNT OF OBSERVATIONS READ
      NR = 0
  110 CONTINUE
C                 IOBSVNL IS PREVIOUS OBSERVATION NUMBER
      IOBSVNL = IOBSVN
  120 CONTINUE
C
C                   READ AN OBSERVATION
C
      IF (NREGN .EQ. 1) THEN
C
C                   READ ANALOG DATA FOR NWPAC
C
CCC     READ (2,9001,END=160) MON,JYR,IDSTORM,IOBSID,IOBSYR,IOBSMON,
CCC  .  IOBSDAY,IOBSHR,IOBSLAT,IOBSLON, IHD12,ISPD12,IHD18,ISPD18,IHD24
CCC  .  ISPD24,IHD48,ISPD48, IRADIUS,IDELRAD,ISLPRES,IDELSLP, IWNDSPD,
CCC  .  MINHGT,IRDGLAT,IRDGHGT,ITROLON,ITROHGT,IOBNAME,IOBTYPE
CCC           * * * NOTE, BZ MEANS CONVERT BLANKS TO ZERO
C9001   FORMAT (BZ,8I2,I4,I5,8I3,2(I4,I3),I3,3X,2I3,3I4,8X,A8,1X,A1)
        READ (NUNIT,9001,END=160) MON,JYR,IDSTORM,IOBSID,IOBSYR,
     .        IOBSMON,IOBSDAY,IOBSHR,IOBSLAT,IOBSLON,IWNDSPD,IOBNAME,
     .        IOBTYPE
C             * * * NOTE, BZ MEANS CONVERT BLANKS TO ZERO
c9001   FORMAT (BZ,8I2,I4,I5,38X,I3,29X,A8,1X,A1)
 9001   format (8i2,i4,i5,38x,i3,29x,a8,1x,a1)
C
      ELSEIF (NREGN .EQ. 2) THEN
C
C                   READ ANALOG DATA FOR NEPAC
C
        READ (NUNIT,9002,END=160) MON,JYR,IDSTORM,IOBSID,IOBSYR,
     .        IOBSMON,IOBSDAY,IOBSHR,IOBSLAT,IOBSLON,IWNDSPD,IOBNAME,
     .        IOBTYPE
c9002   FORMAT (BZ,8I2,I4,I5,I4,1X,A8,1X,A1)
 9002   format (8i2,i4,i5,i4,1x,a8,1x,a1)
C
      ELSE
C
C                   READ ANALOG DATA FOR IND, SWI AND SWP REGIONS
C
CCC     READ (2,9003,END=160) MON,JYR,IDSTORM,IOBSID,IOBSYR,IOBSMON,
CCC  .  IOBSDAY,IOBSHR,IOBSLAT,IOBSLON,IHD12,ISPD12,IWNDSPD,IOBNAME,
CCC  .  IOBTYPE
C9003   FORMAT (BZ,8I2,I4,I5,2I3,I3,1X,A8,1X,A1)
        READ (NUNIT,9003,END=160) MON,JYR,IDSTORM,IOBSID,IOBSYR,
     .        IOBSMON,IOBSDAY,IOBSHR,IOBSLAT,IOBSLON,IWNDSPD,IOBNAME,
     .        IOBTYPE
c9003   FORMAT (BZ,8I2,I4,I5,6X,I4,1X,A8,1X,A1)
 9003   format (8i2,i4,i5,6x,i4,1x,a8,1x,a1)
      ENDIF
C
C                   YR, STORM ID, AND OBS NO. ARE COMBINED TO PRODUCE
C                   TOTAL OBSERVATION NAME - IOBSVN
      WRITE (STRING,9010) JYR,IDSTORM,IOBSID
 9010 FORMAT (3I2)
      READ (STRING,9020) IOBSVN
 9020 FORMAT (BZ,I6)
C
      IF (NR.NE.0 .AND. IOBSVN.NE.IOBSVNL+1) THEN
C                   OBSERVATION NUMBERS ARE IN INCREASING SEQUENCE.
C                   IF NOT IN SEQUENCE, PREVIOUS READ WAS LAST DATA FOR
C                   THIS CYCLONE, SO BACK STEP TO END OF DATA FOR THIS
C                   CYCLONE AND RETURN TO CALLING ROUTINE.
        BACKSPACE (NUNIT)
        GOTO 170
C
      ENDIF
C
      IF (NR .GE. 99) THEN
C              MAX OF 99 OBSERVATIONS ALLOWED PER CYCLONE.
C              THE REST WILL BE IN THE NEXT SET OF OBSERVATIONS.
cx      PRINT 9070, NR,STNAME,MM,JY
        write(33,9070) nr,stname,mm,jy
 9070   FORMAT (' RDCLIMO, MAXIMUM OF ',I2,' OBSERVATIONS REACHED FOR',
     .          ' CYCLONE ',A8,' DURING MONTH ',I2,' YEAR ',I2)
        BACKSPACE (NUNIT)
        GOTO 170
C
      ENDIF
C                   CALCUALTE OBS JULIAN DAY
      IDAY = JAYDAY (IOBSYR,IOBSMON,IOBSDAY)
      IF (IDAY .EQ. 0) THEN
C                   IF OBSV. DATE IN ERROR, IGNORE REC.
cx      PRINT*,'TCLIMO, RDCLIMO INVALID OBSERVATION DATE: YR ',
        write(33,*)'TCLIMO, RDCLIMO INVALID OBSERVATION DATE: YR ',
     .          IOBSYR,' MON ',IOBSMON,' DAY ',IOBSDAY
        GOTO 120
C
      ENDIF
C                   COUNT THE ALLOWABLE OBSERVATIONS
      NR = NR +1
C                   GET THE PARAMETERS OF ACCEPTED OBSERVATION
      IF (NR .EQ. 1) THEN
        STNAME = IOBNAME
        STYPE  = IOBTYPE
        MM     = MON
        JY     = JYR
      ENDIF
      IYR(NR)  = IOBSYR
      JDAY(NR) = IDAY
      IHR(NR)  = IOBSHR
      YLAT(NR) = 0.1*(FLOAT (IOBSLAT))
      XLON(NR) = 0.1*(FLOAT (IOBSLON))
C
C                   PUT LONGITUDE IN (0 - 360) EAST RANGE
C
      IF (IOBSLON .LT. 0) XLON(NR) = 360.0 +XLON(NR)
      WIND(NR) = FLOAT (IWNDSPD)
C                   JUMP TO READ ANOTHER OBSERVATION
      GOTO 110
C
  160 CONTINUE
C                   IF EOF WAS READ FOR THE MONTH'S FILE, SET IEOF = 1.
      IEOF = 1
cx    PRINT*,'TCLIMO, RDCLIMO - END OF FILE/MONTH REACHED'
      write(33,*)'TCLIMO, RDCLIMO - END OF FILE/MONTH REACHED'
  170 CONTINUE
      RETURN
C
      END
      SUBROUTINE HEADEM (NREGN,AIDNM)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  HEADEM
C
C  DESCRIPTION:  WRITE OUTPUT HEADING
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON (CSC) APRIL 1991
C
C  CURRENT PROGRAMMER:
C
C  USAGE (CALLING SEQUENCE):
C                 CALL HEADEM (NREGN,AIDNM)
C
C  INPUT PARAMETERS:
C     NREGN - REGION NUMBER
C     AIDNM - AID NAME
C
C  OUTPUT PARAMETERS:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      CHARACTER*4 AIDNM
C
      CHARACTER*8 CDTG
      CHARACTER*6 CNAME
      CHARACTER*1 CNS,CEW,EW12
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NREGN .EQ. 1) THEN
        PRINT 681, AIDNM,CNAME,CDTG
cx681   FORMAT(' ',10X,'NORTHWEST PACIFIC ',A4,' FORECAST FOR  ',
  681   FORMAT('   NORTHWEST PACIFIC ',A4,' FORECAST FOR  ',
     .         A6,' AT ',A8)
      ELSEIF (NREGN .EQ. 2) THEN
        PRINT 682, AIDNM,CNAME,CDTG
cx682   FORMAT(' ',10X,'NORTHEAST PACIFIC ',A4,' FORECAST FOR  ',
  682   FORMAT('   NORTHEAST PACIFIC ',A4,' FORECAST FOR  ',
     .         A6,' AT ',A8)
      ELSEIF (NREGN .EQ. 3) THEN
        PRINT 683, AIDNM,CNAME,CDTG
cx683   FORMAT(' ',10X,'NORTH INDIAN ',A4,' FORECAST FOR  ',A6,
  683   FORMAT('   NORTH INDIAN ',A4,' FORECAST FOR  ',A6,
     .         ' AT ',A8)
      ELSEIF (NREGN .EQ. 4) THEN
        PRINT 684, AIDNM,CNAME,CDTG
cx684   FORMAT(' ',10X,'SOUTHWEST INDIAN ',A4,' FORECAST FOR  ',
  684   FORMAT('   SOUTHWEST INDIAN ',A4,' FORECAST FOR  ',
     .         A6,' AT ',A8)
      ELSEIF (NREGN .EQ. 5) THEN
        PRINT 685, AIDNM,CNAME,CDTG
cx685   FORMAT(' ',10X,'SOUTH PACIFIC ',A4,' FORECAST FOR  ',A6,
  685   FORMAT('   SOUTH PACIFIC ',A4,' FORECAST FOR  ',A6,
     .         ' AT ',A8)
      ENDIF
      RETURN
C
      END
      SUBROUTINE HEDIST (SL,SG,EL,EG,HEAD,DIST,RHED,RDST)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  HEDIST
C
C  DESCRIPTION:  CALCULATE HEADING AND DISTANCE FROM SL,SG TO EL,EG IN
C                THE TROPICS AND MID-LATIUDE, RHUMB-LINE
C
C  CURRENT PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC)  MAR 1991
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):
C                 CALL HEDIST (SL,SG,EL,EG,HEAD,DIST,RHED,RDST)
C
C  INPUT PARAMETERS:
C     EG   - ENDING LONGITUDE, (0 - 360 EAST OR -W) (DEG)
C     EL   - ENDING LATITUDE, (+NH, -SH) (DEG)
C     SG   - STARTING LONGITUDE, (0 - 360 EAST OR -W) (DEG)
C     SL   - STARTING LATITUDE, (+NH, -SH) (DEG)
C
C  OUTPUT PARAMETERS:
C     HEAD - HEADING,  POSITIVE W/O ROUNDING (DEGREES)
C     DIST - DISTANCE, POSITIVE W/O ROUNDING (N.M.)
C     RHED - HEADING,  (TENTH OF DEG)
C     RDST - DISTANCE, (TENTH OF N.M.)
C
C  ERROR CONDITIONS:  NONE, VALID LAT/LON NOT CHECKED
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     RAD  - DEGREES PER RADIAN
C     RADI - RADIANS PER DEGREE
C     RDI2 - 0.5*RADI
C     A45R - RADIANS FOR 45 DEG ANGLE
C
C  METHOD:  BASED UPON RHUMB LINE CALCULATIONS FROM TEXAS INSTRUMENTS
C           NAVIGATION PACKAGE FOR HAND HELD CALCULATOR
C
C  RECORD OF CHANGES:  sampson, nrl   reset TINY for maxion and sun
C
C
C........................END PROPLOGUE..................................
C
      SAVE RAD,RADI,RDI2,A45R
C
CCC   DATA TINY/0.1E-8/
C                   CHANGE SIZE OF TINY FOR MICRO
CCC   DATA TINY/0.1E-6/
C                   CHANGE SIZE OF TINY FOR Maxion and Sun
      DATA TINY/0.1E-1/
C                   MAXIMUM POLEWARD LATITUDE, HARDWARE DEPENDENT
CCC   DATA PLMX/89.99/
      DATA INIL/-1/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (INIL .NE. 0) THEN
         INIL = 0
         RAD  = 180.0/ACOS (-1.0)
         RADI = 1/RAD
         RDI2 = 0.5*RADI
         A45R = 45.0*RADI
      ENDIF
      HEAD = 0.0
      DIST = 0.0
C                    SAME POINT RETURNS 0 DIST AND 0 HEAD
      IF (SL.NE.EL .OR. SG.NE.EG) THEN
         XL = SL
         XG = SG
C                   IF LONGITUDE IS WEST, CONVERT TO 0-360 EAST
         IF (XG .LT. 0.0) XG = XG +360.0
         YL = EL
         YG = EG
C                   IF LONGITUDE IS WEST, CONVERT TO 0-360 EAST
         IF (YG .LT. 0.0) YG = YG +360.0
C                    CHECK FOR SHORTEST ANGULAR DISTANCE
         IF (XG.GT.270.0 .AND. YG.LT.90.0) YG = YG +360.0
         IF (YG.GT.270.0 .AND. XG.LT.90.0) XG = XG +360.0
C
         IF (ABS (XL -YL) .LE. TINY) THEN
C                    RESOLVE 90 OR 270 HEADING
            HEAD = 90.0
            IF (YG .LT. XG) HEAD = 270.0
            DIST = 60.0*(YG -XG)*COS (XL*RADI)
         ELSE
            DIST = 60.0*(XL -YL)
            IF (ABS (XG -YG) .LE. TINY) THEN
C                  RESOLVE 0 OR 180 HEADING, NOTE HEAD IS PRESET TO ZERO
               IF (YL .LT. XL) HEAD = 180.0
            ELSE
C                   CHECK FOR POSITIONS POLEWARD OF 89+ DEGREES LATITUDE
CCC            IF (ABS (XL).GT.PLMX .OR. ABS (YL).GT.PLMX) THEN
C              (HARDWARE DEPENDENT - NOT REQUIRED FOR TROPICAL CYCLONES)
CCC               XLT = XL
CCC               IF (ABS (XLT) .GT. PLMX) XLT = SIGN (PLMX,XL)
CCC               YLT = YL
CCC               IF (ABS (YLT) .GT. PLMX) YLT = SIGN (PLMX,YL)
CCC               XR   = TAN (XLT*RDI2 +SIGN (A45R,XL))
CCC               YR   = TAN (YLT*RDI2 +SIGN (A45R,YL))
CCC            ELSE
                  XR   = TAN (XL*RDI2 +SIGN (A45R,XL))
                  YR   = TAN (YL*RDI2 +SIGN (A45R,YL))
CCC            ENDIF
               ELN1 = SIGN (ALOG (ABS (XR)),XR)
               ELN2 = SIGN (ALOG (ABS (YR)),YR)
cx    make sure no divide by zero
	       if (eln1.eq.eln2)eln1=eln1+.0001
               HEAD = RAD*(ATAN ((XG -YG)/(RAD*(ELN1 -ELN2))))
               IF (YL   .LT. XL)  HEAD = HEAD +180.0
               IF (HEAD .LE. 0.0) HEAD = HEAD +360.0
C                   CORRECT INITIAL DISTANCE, BASED ONLY ON LATITIUDE
               DIST = DIST/COS (HEAD*RADI)
            ENDIF
         ENDIF
      ENDIF
      DIST  = ABS (DIST)
      IDIST = NINT (DIST*10.0)
      RDST  = 0.1*(FLOAT (IDIST))
      IF (DIST.NE.0.0 .AND. HEAD.EQ.0.0) HEAD = 360.0
      IHEAD = NINT (HEAD*10.0)
      RHED  = 0.1*(FLOAT (IHEAD))
      RETURN
C
      END
      FUNCTION JAYDAY (IY,IM,ID)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  JAYDAY
C
C  DESCRIPTION:  CALCULATE JULIAN DAY GIVEN YEAR, MONTH AND DAY
C
C  ORIGINAL PROGRAMMER, DATE:  R. F. ALDEN   (ODSI)  1978
C                              S. MCBROOM    (SSAI)  1986
C
C  CURRENT PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC)  NOV 1990
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):
C              JULIAN = JAYDAY (IY,IM,ID)
C
C  INPUT PARAMETERS:
C     IY - YEAR, LAST TWO DIGITS
C     MO - MONTH, 1 - 12
C     ID - DAY, 1 - 28, 29, 30 OR 31
C
C  OUTPUT PARAMETERS:
C     JAYDAY - GREATER THAN ZERO, JULIAN DAY FOR INPUT
C              ZERO, ERROR IN YEAR, MONTH OR DAY OF INPUT
C
C  ERROR CONDITIONS:  (SEE ABOVE)
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     MTH - JULIAN DAYS FOR NON LEAP YEAR
C
C  METHOD:  SELF EXPLANATORY
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      DIMENSION MTH(13)
C
      DATA MTH/0,31,59,90,120,151,181,212,243,273,304,334,365/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (IY.GE.0 .AND. IM.GT.0 .AND. IM.LT.13) THEN
C                   YEAR AND MONTH INDEXS O.K.
cx       IF (IY.EQ.0 .OR. MOD (IY,4).NE.0) THEN
C                   NOTE, BY DEFINITION 1900 IS NOT A LEAP YEAR, BUT
C                         2000 IS, THEREFORE THE 1900 CYCLONE POSITIONS
C                         MUST BE REMOVED FROM THE DATA BASE BEFORE 2000
C                         AND THE ABOVE LINE OF CODE CHANGED
cx    Done. Should work until 3000 -after that, who cares.
cx    Whole problem is trivial in the grand scheme of things
cx    with this model. Not worth fretting about.   sampson, nrl 10/27/98
	 IF (MOD (IY,4).NE.0) THEN
            IADD = 0
         ELSE
C                   IADD = 1 FOR LEAP YEARS (YRS EVENLY DIVISABLE BY 4)
            IADD = 1
         ENDIF
C
         MAXDAYS = MTH(IM+1) -MTH(IM)
         IF (IM.EQ.2) MAXDAYS = MAXDAYS +IADD
         IF (ID.GT.0 .AND. ID.LE.MAXDAYS) THEN
C                   DAY INDEX O.K.
C                   MAKE IADD 0 FOR JAN AND FEB
            IF (IM .LT. 3) IADD = 0
            JAYDAY = MTH(IM) +ID +IADD
         ELSE
C                   MAKE JAYDAY ZERO TO SIGNAL ERROR
            JAYDAY = 0
         ENDIF
      ELSE
C                   MAKE JAYDAY ZERO TO SIGNAL ERROR
         JAYDAY = 0
      ENDIF
      RETURN
C
      END
      SUBROUTINE IJAYDAY (IY,JDAY,MO,KD)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  IJAYDAY
C
C  DESCRIPTION:  CALCULATE MONTH AND DAY GIVEN YEAR AND JULIAN DAY
C
C  ORIGINAL PROGRAMMER, DATE:  R. F. ALDEN   (ODSI)  1978
C                              S. MCBROOM    (SSAI)  1986
C
C  CURRENT PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC)  NOV 1990
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):  CALL IJAYDAY (IY,JDAY,MO,KD)
C
C  INPUT PARAMETERS:
C     IY   - YEAR, LAST TWO DIGITS
C     JDAY - JULIAN DAY
C
C  OUTPUT PARAMETERS:
C     MO - MONTH, 1 - 12, 0 IF ERROR ON INPUT
C     KD - DAY, 1 - 28, 29, 30 OR 31, 0 IF ERROR ON INPUT
C
C  ERROR CONDITIONS:  (SEE ABOVE)
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     MTH  - JULIAN DAYS FOR NON-LEAP YEAR AND LEAP YEAR
C     MTHD - DAYS IN MONTH FOR NON-LEAP YEAR AND LEAP YEAR
C
C  METHOD:  SELF EXPLANATORY
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      DIMENSION MTH(24), MTHD(24)
C
      DATA MTH/0,31,59,90,120,151,181,212,243,273,304,334,
     .         0,31,60,91,121,152,182,213,244,274,305,335/
C
      DATA MTHD/31,28,31,30,31,30,31,31,30,31,30,31,
     .          31,29,31,30,31,30,31,31,30,31,30,31/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (JDAY.GT.0 .AND. IY.GE.0) THEN
C                   POSSIBLE VALID JULIAN DATE
cx       IF (IY.EQ.0 .OR. MOD(IY,4).NE.0) THEN
C                   NOTE, BY DEFINITION 1900 IS NOT A LEAP YEAR, BUT
C                         2000 IS, THEREFORE THE 1900 CYCLONE POSITIONS
C                         MUST BE REMOVED FROM THE DATA BASE BEFORE 2000
C                         AND THE ABOVE LINE OF CODE CHANGED
cx    Done. Should work until 3000 -after that, who cares.
cx    Whole problem is trivial in the grand scheme of things
cx    with this model. Not worth fretting about.   sampson, nrl 10/27/98
	 IF (MOD (IY,4).NE.0) THEN
            IADD = 0
         ELSE
C                   LEAP YEAR, USE LEAP YEAR TABLES (K+12)
            IADD = 12
         ENDIF
         DO 110 MO=1, 12
           IF (JDAY -MTH(MO+IADD) .LE. MTHD(MO+IADD)) THEN
C                   HAVE MONTH, NOW CALCULATE DAY
              KD = JDAY -MTH(MO+IADD)
              GOTO 120
C
           ENDIF
  110    CONTINUE
      ENDIF
C                   MAKE MONTH AND DAY ZERO TO SIGNAL ERROR
      MO = 0
      KD = 0
  120 CONTINUE
      RETURN
C
      END
      SUBROUTINE EXTRAP (PLT1,PLN1,PLT2,PLN2)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  EXTRAP
C
C  DESCRIPTION:  CALCULATE FUTURE POSITIONS EVERY 12 HOURS
C                USING EXTRAPLOATION BASED UPON LAST 12-HOUR
C                DIRECTION AND DISTANCE.
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC)  MAR 1991
C
C  USAGE (CALLING SEQUENCE):
C                 CALL EXTRAP (PLT1,PLN1,PLT2,PLN2)
C
C  INPUT PARAMETERS:
C     PLT1 - PRIOR LATITUDE, DEG
C     PLN1 - PRIOR LONGITUDE, (0 - 360 EAST) DEG
C     PLT2 - LAST LATITUDE, DEG
C     PLN2 - LAST LONGITUDE, (0 - 360 EAST) DEG
C
C  OUTPUT PARAMETERS:  NONE
C
C  OUTPUT COMMON:
C     ALL VALUES IN COMMON /XTRP/
C
C  ERROR CONDITIONS:  NONE, VALID LAT/LON NOT CHECKED
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:  SIMPLE EXTRAPOLATION
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C                   EXPLANATION OF /XTRP/ VARIABLES
C
C   CLTXX - FORECAST LATITUDE  AT XX HOURS, BASED UPON EXTRAPOLATION
C           OR HPAC
C   CLNXX - FORECAST LONGITUDE AT XX HOURS, BASED UPON EXTRAPOLATION
C           OR HPAC
C
      COMMON/XTRP/ XLT12,XLT24,XLT36,XLT48,XLT60,XLT72,
     .             XLN12,XLN24,XLN36,XLN48,XLN60,XLN72
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      CALL HEDIST (PLT1,PLN1,PLT2,PLN2,DIR,DST,RDIR,RDST)
      CALL CALTLN (DIR,DST,PLT2,PLN2,XLT,XLN,XLT12,XLN12)
      SLT = XLT
      SLN = XLN
      CALL CALTLN (DIR,DST,SLT,SLN,XLT,XLN,XLT24,XLN24)
      SLT = XLT
      SLN = XLN
      CALL CALTLN (DIR,DST,SLT,SLN,XLT,XLN,XLT36,XLN36)
      SLT = XLT
      SLN = XLN
      CALL CALTLN (DIR,DST,SLT,SLN,XLT,XLN,XLT48,XLN48)
      SLT = XLT
      SLN = XLN
      CALL CALTLN (DIR,DST,SLT,SLN,XLT,XLN,XLT60,XLN60)
      SLT = XLT
      SLN = XLN
      CALL CALTLN (DIR,DST,SLT,SLN,XLT,XLN,XLT72,XLN72)
      RETURN
C
      END
      SUBROUTINE CALTLN (HEAD,DIST,SLAT,SLON,ELAT,ELON,RLAT,RLON)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  CALTLN
C
C  DESCRIPTION:  CALCULATE ELAT,ELON GIVEN RHUMB-LINE HEADING (HEAD)
C                AND DISTANCE (DIST) FROM SLAT,SLON.
C
C  CURRENT PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC)  MAR 1991
C
C  USAGE (CALLING SEQUENCE):
C                 CALTLN (HEAD,DIST,SLAT,SLON,ELAT,ELON,RLAT,RLON)
C
C  INPUT PARAMETERS:
C     DIST - DISTANCE TO TRAVEL, N.M.
C     HEAD - HEADING TO TRAVEL, DEG.
C     SLAT - STARTING LATITUDE, (+NH, -SH) (DEG)
C     SLON - STARTING LONGITUDE, (0 - 360 EAST OR -W) (DEG)
C
C  OUTPUT PARAMETERS:
C     ELAT - ENDING LATITUDE, DEGREE W/O ROUNDING
C     ELON - ENDING LONGITUDE, DEGREE W/O ROUNDING
C     RLAT - ENDING LATITUDE, TENTH OF DEGREE
C     RLON - ENDING LONGITUDE, TENTH OF DEGREE
C
C  ERROR CONDITIONS:  NONE, VALID LAT/LON NOT CHECKED
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C     DEGRAD - RADIANS PER DEGREE
C     HDGRAD - 0.5*DEGRAD
C     RADDEG - DEGREES PER RADIAN
C     RAD045 - RADIANS FOR 45 DEG ANGLE
C
C  METHOD:  BASED UPON RHUMB LINE CALCULATIONS FROM TEXAS INSTRUMENTS
C           NAVIGATION PACKAGE FOR HAND HELD CALCULATOR
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      SAVE RADDEG, DEGRAD, HDGRAD, RAD045, INIL
      DATA INIL/-1/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (INIL .NE. 0) THEN
         INIL   = 0
         DEGRAD = ACOS (-1.0)/180.0
         HDGRAD = 0.5*DEGRAD
         RAD045 = 45.0*DEGRAD
         RADDEG = 1.0/DEGRAD
      ENDIF
C
      ICRS = NINT (HEAD)
      IF (ICRS.EQ.90 .OR. ICRS.EQ.270) THEN
         DLON = DIST/(60.0*COS (SLAT*DEGRAD))
C                   LONGITUDE IS IN DEGREES EAST, TO 360.0
         IF (ICRS .EQ. 270) THEN
            ELON = SLON -DLON
         ELSE
            ELON = SLON +DLON
         ENDIF
         ELAT = SLAT
      ELSE
         CRPD = HEAD*DEGRAD
         ELAT = SLAT +(DIST*COS(CRPD)/60.0)
         IF (MOD (ICRS,180) .NE. 0) THEN
C                   FOLLOWING TEST NOT REQUIRED FOR TROPICAL CYCLONES
CCC         IF (ABS (ELAT) .GT. 89.0) ELAT = SIGN (89.0,ELAT)
            ELON = SLON +RADDEG*(ALOG (TAN (RAD045 +HDGRAD*ELAT))
     .             -ALOG (TAN (RAD045 +HDGRAD*SLAT)))*TAN (CRPD)
         ELSE
            ELON = SLON
         ENDIF
      ENDIF
      ICRS = NINT (10.0*ELAT)
      RLAT = 0.1*FLOAT (ICRS)
      ICRS = NINT (10.0*ELON)
      RLON = 0.1*FLOAT (ICRS)
      RETURN
C
      END
      SUBROUTINE TPACEM
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  TPACEM
C
C  DESCRIPTION:  CALCULATE PERSISTENCE AND CLIMATOLOGY FORECAST WITH
C                WEIGHTS OF 0.5 - HPAC FORECAST
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON  (CSC)  APR 1991
C
C  CURRENT PROGRAMMER:
C
C  USAGE (CALLING SEQUENCE):  CALL TPACEM
C
C  INPUT PARAMETERS (FORMAL):  NONE
C
C  OUTPUT PARAMETERS (FORMAL):  NONE
C
C  INPUT COMMON:
C     ALL VALUES IN COMMONS /CLIM/ AND /XTRP/
C
C  OUTPUT COMMON:
C     ALL VALUES IN COMMON /XTRP/
C
C  ERROR CONDITIONS:  NONE
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:  SIMPLE WEIGHTING
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      DIMENSION CP(6,3), XP(6,2)
C
C                   EXPLANATION OF /CLIM/ VARIABLES
C
C   CLTXX - FORECAST LATITUDE  AT XX HOURS, BASED UPON CLIMATOLOGY
C   CLNXX - FORECAST LONGITUDE AT XX HOURS, BASED UPON CLIMATOLOGY
C   CWDXX - FORECAST MAXIMUM SUSTAINED WIND SPEED (KT) AT XX HOURS,
C           BASED UPON CLIMATOLOGY
C
      COMMON/CLIM/ CLT12,CLT24,CLT36,CLT48,CLT60,CLT72,
     .             CLN12,CLN24,CLN36,CLN48,CLN60,CLN72,
     .             CWD12,CWD24,CWD36,CWD48,CWD60,CWD72
C
C                   EXPLANATION OF /XTRP/ VARIABLES
C
C   CLTXX - FORECAST LATITUDE  AT XX HOURS, BASED UPON EXTRAPOLATION
C           OR HPAC
C   CLNXX - FORECAST LONGITUDE AT XX HOURS, BASED UPON EXTRAPOLATION
C           OR HPAC
C
      COMMON/XTRP/ XLT12,XLT24,XLT36,XLT48,XLT60,XLT72,
     .             XLN12,XLN24,XLN36,XLN48,XLN60,XLN72
C
      EQUIVALENCE (CP(1,1),CLT12), (XP(1,1),XLT12)
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      DO 110 N=1, 6
        IF (CP(N,1).NE.0.0 .AND. CP(N,2).NE.0.0) THEN
          XP(N,1) = 0.5*(CP(N,1) +XP(N,1))
          XP(N,2) = 0.5*(CP(N,2) +XP(N,2))
        ELSE
          XP(N,1) = 0.0
          XP(N,2) = 0.0
        ENDIF
  110 CONTINUE
      RETURN
C
      END
