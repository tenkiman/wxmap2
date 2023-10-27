      PROGRAM JTWC92
C
C........................START PROLOGUE.................................
C
C  PROGRAM NAME:  JTWC92
C
C  DESCRIPTION:
C
C      A STATISTICAL-DYNAMICAL MODEL FOR THE PREDICTION OF WESTERN NORTH
C      PACIFIC TROPICAL CYCLONE MOTION THROUGH 72H.  FORECASTS ARE BASED
C      ON: CLIMATOLOGY AND PERSISTENCE, AND DEEP-LAYER-MEAN GEOPOTENTIAL
C      HEIGHT FIELDS.
C
C  ORIGINAL PROGRAMMERS, DATE:  CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C                               JAMES M. SHELTON, MAY 1992 (SAIC)
C                                HARRY D. HAMILTON  (GSA - CSC)  JULY 1992
C
C  CURRENT PROGRAMMER:  buck sampson, aug 1995                   
C
C  COMPUTER/OPERATING SYSTEM: CDC 8XX COMPUTERS WITH NOS/BE
C
C  LIBRARIES OF RESIDENCE:  
C
C  CLASSIFICATION:          UNCLASSIFIED
C
C  USAGE (JCL):             (FOLLOWING JTWCPR)
C                           JTWC92.
C
C  INPUT FILES:
C    TAPE91 - CYCLONE DATA from best track file (b??????.dat)
C    TAPE92 - UNFORMATTED DEEP-LAYER-MEAN FIELDS, SEQUENTIAL
C             FROM JTWCPR.
C
C  OUTPUT FILES:
Cxx  TAPE19  - FORECASTS AND DIAGNOSTICS FOR CVCQFC.
Cxx  PRINTEM - FULL SUMMARY OF CALCULATIONS.
cx   wptot.dat  - forecasts in ccrs format.
cx   to screen - full summary of calculations.
C
C  ERROR CONDITIONS:
C    IF CYCLONE IS NOT WITHIN NW PACIFIC, DO NOT EXECUTE.
C    IF FIELDS LESS THAN TAU 24 FROM INITIAL CYCLONE POSITION, DO NOT
C    EXECUTE.
C
C  ADDITIONAL COMMENTS:
C   THE DEEP-LAYER-MEAN FIELDS HAVE BEEN SPECTRALLY REDUCED TO WAVE
C   NUMBERS THROUGH 30 WITH DOUBLE FAST FOURIER TRASFORMS OF THE GLOBAL
C   DEEP-LAYER-MEAN FIELDS FROM NOGAPS.  THESE VALUES HAVE BEEN
C   INTERPOLATED TO A NORTHERN HEMISPHERE POLAR STEREOGRAPHIC PROJECTION
C   GRID, 65-BY-65 (A SUPER SET OF THE OLD STANDARD 63-BY-63 POLAR).
C
C........................MAINTENANCE SECTION............................
C
C  BRIEF DESCRIPTION OF PROGRAM MODULES:
C
C      WPCLPR - PREPARES PRELIMINARY FORECAST BASED ON CLIMATOLOGY AND
C               PERSISTENCE.
C
C      ANLS   - PREPARES PRELIMINARY FORECAST BASED ON "ANALYSIS" FIELDS
C
C      PPRG   - PREPARES PRELIMINARY FORECAST BASED ON "ANALYSIS" FIELDS
C               AND FORECAST FIELDS.
C
C      BLKDT2 - NAVIGATIONAL ROUTINES USED FOR TRANSLATING AND ROTATING
C               GRIDS, FOR POSITIONING STORM IN GRID, ETC.
C
C      RSOLV  - COMBINES THE VARIOUS FORECASTS
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  COMMON BLOCKS:
C
C  METHOD:
C    1.  MAKE WESTERN NORTH PACIFIC CLIPER (CLIMATOLOGY/PERSISTENCE)
C        FORECASTS.
C    2.  MAKE FORECASTS BASED UPON INITIAL FIELDS (VALID TIME SAME AS
C        INITIAL TROPICAL CYCLONE POSITION)
C    3.  INDIVIDUAL FORECASTS FOR EACH 12-HOUR TAU BASED UPON ALL FIELDS
C        THROUGH THE VALID TIME OF THE FORECAST.  THAT IS, TAU 24 IS NOT
C        BASED UPON FORECAST POSITION OF TAU 12.
C    4.  COMBINE ALL THREE FORECASTS TO PRODUCE FINAL FORECASTS.
C
C  LANGAUGE:  CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C     8/16/95   converted to run in ATCF 3.0  sampson
c
c     Modified to use new data format,  6/98   A. Schrader
c     Modified to use last bt posit century "cent" 11/98 Sampson 
C
C........................END PROLOGUE..................................
C
      include 'dataioparms.inc'

      character*100 storms,filename
      character*8  cdatim
      character*6  strmid
      character*2 century
      character*2 cent
      CHARACTER*1 CNS, CEW
      integer     ltlnwnd(numtau,llw)
      integer     ii, jj, iarg
C
      DIMENSION CNMIS(12), IR(4)
C
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
      COMMON /BLK07/PLAT(6), PLON(6), ACLAT(6), ACLON(6), CLAT(6),
     *              CLON(6), ACPLAT(6), ACPLON(6), ALAT(6), ALON(6)
      COMMON /BLK08/NITER
      COMMON /BLK09/TEMP1(12), TEMP2(12), TEMP3(6), TEMP4(6), TEMP5(6),
     *              TEMP6(6)
      COMMON /PUTOUT/NUNIT
      CHARACTER*10 SNAME
C
      COMMON /STMNAM/SNAME
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
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
c     get the storm id
c
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call upcase(strmid,6)
c
c  get the first two digits of the storm year
c
      call getarg(iarg,century)
      iarg = iarg + 1

cx    CALL GETCCL (IR)
cx    IF (IR(2) .EQ. 0) THEN
cx      IERR = -1
cx      GOTO 300
C
cx    ENDIF
C                 OPEN OUTPUT FILE FOR S/R NVNTRY AND SUMMARY
cx    NUNIT =7
cx    OPEN (NUNIT,FILE='PRINTEM')
      nunit =7
      call openfile (nunit,'jtwc92.dbg','unknown',ioerror)

C
C                  SET ITERATION COUNT IN NITER
C
      NITER = 3
c
      write (*,*) ' ************************************************* '
      write (*,*) '           jtwc92 forecast for ',strmid
C
C                  GET INITIAL STORM DATA
C
      CALL STMDTA (NUNIT,NZ,cent,IERR)
      write (*,*) '            INITIAL TIME:',idatim

cx                open input file containing gridded data
      write(cdatim,'(i8.8)')idatim 
      write(filename,'(a,a,a)')storms(1:ind),"/jt92.",cdatim
      open (unit=92, file=filename,form="unformatted",
     &      status='old',err=980)
      IF (NFLDS .LT. 3) THEN
        WRITE (NUNIT,*) ' JTWC92, LESS THAN TAU 24 FIELDS AVAILABLE $ $'
        IERR = -1
      ENDIF
      IF (IERR .NE. 0) GOTO 300
C
C     GET CLIPER FORECAST IN ZONAL AND MERIDIONAL COMPONENTS (CNMIS)
C
      CALL WPCLIP (IDATIM, SLAT00, SLON00, SLAT12, SLON12, SLAT24,
     * SLON24, WIND, CNMIS)
C
C     ROTATE CLIPER FORECAST DISPLACEMENTS RELATIVE TO GRID ORIENTATION
C
      CALL RT (CNMIS, CDISP)
C
C     SPECIFY CLIPER ROTATED DISPLACEMENT (CDISP) FORECASTS IN TERMS OF
C     LAT/LON
C
      CALL RSOLV (CDISP, CLAT, CLON)
C
C     GET FORECASTS USING CURRENT ANALYSIS ONLY
C
      CALL ANLS (NZ)
C
C     SPECIFY ROTATED ANALYSIS DISPLACEMENT FORECASTS IN TERMS OF
C     LAT/LON.
C
      CALL RSOLV (ADISP, ALAT, ALON)
C
C     NOTE: ABOVE RETURNED LONGITUDES (ALON) ARE NEGATIVE FOR EAST
C
C     COMBINE CLIPER AND ANALYSIS MODE FORECASTS
C
      CALL CBNAC (NZ)
C
C     RESOLVE ABOVE FORECAST DISPLACEMENTS INTO FORECAST LAT/LONS
C
      CALL RSOLV (ACDISP, ACLAT, ACLON)
C
C     NOTE: ABOVE RETURNED LONGITUDES (ACLON) ARE NEGATIVE FOR EAST
C
C     NUMBER OF FORECAST CYCLES (LIMIT IS 3) THROUGH PERFECT-PROG SYSTEM
C     IS GIVEN BY INTEGER VARIABLE NITER (BLK 8) AS SPECIFIED ABOVE
C
      DO 130 NCYCLE = 1, NITER
         WRITE (NUNIT, 9000) NCYCLE
 9000   FORMAT (//10X,'PERFECT-PROG MODE, CYCLE IS NUMBER',I2/)
         IF ( NCYCLE .GT. 1 ) THEN
            CALL PPROG(NZ, ACPLAT, ACPLON, NCYCLE)
         ELSE
            CALL PPROG(NZ, ACLAT, ACLON, NCYCLE)
         ENDIF
C
C        SPECIFY PERFECT-PROG ROTATED DISPLACEMENT FORECASTS IN TERMS OF
C        LAT/LON
C
         CALL RSOLV(PDISP, PLAT, PLON)
C
C        COMBINE CLIPER, ANAL AND PERF-PROG FORECASTS...
C
         CALL CBNACP(NZ)
C
C        RESOLVE COMBINED FORECAST DISPLACEMENTS INTO FORECAST LAT/LONS
C
         CALL RSOLV(ACPDSP, ACPLAT, ACPLON)
         IF ( NCYCLE .EQ. 1 ) THEN
            DO 110 I = 1, 12
               TEMP1(I) = PDISP(I)
               TEMP2(I) = ACPDSP(I)
  110       CONTINUE
            DO 120 I = 1, 6
               TEMP3(I) = PLAT(I)
               TEMP4(I) = PLON(I)
               TEMP5(I) = ACPLAT(I)
               TEMP6(I) = ACPLON(I)
  120       CONTINUE
         ENDIF
  130 CONTINUE
C
C     OUTPUT FORECASTS FROM ALL SYSTEMS (132 COLUMN OUTPUT)
C
      CALL SUMMRY (NZ)
cx    CLOSE (NUNIT)
C
C                   OPEN FILE FOR OPERATIONAL OUTPUT FOR CVCQFC
C
cx    OPEN (19,FILE='TAPE19')
C
C                   OUTPUT FORECAST AND PLAIN LANGAGE FOR CVCQFC
C
      NGPLR=5
      REWIND (92)

cx
cx  write the forecast to adeck file
cx
      write(filename,'(a,a)')storms(1:ind),"/wptot.dat"
      call openfile (60,filename,'old',ioerror)
      if (ioerror.ne.0) go to 980
  190 continue
      read(60,'(a1)',end=200)cdummy
      go to 190
  200 continue
      do ii=1,numtau
         ltlnwnd(ii,1) = 0
         ltlnwnd(ii,2) = 0
         ltlnwnd(ii,3) = 0
      enddo
      do ii=1, nflds-2
         jj = ii
         if( jj .eq. 5 ) jj = 6
         if( acplat(jj).gt.0.0 .and. acplat(jj).lt.90.0 .and.
     1        acplon(jj).gt.-180.0 .and. acplon(jj).lt.180.0 ) then
            ltlnwnd(ii,1) = nint(acplat(jj)*10.0)
            ltlnwnd(ii,2) = nint(acplon(jj)*10.0)
            if( acplon(jj).gt.-180.0 .and. acplon(jj).lt.0.0  ) then
               ltlnwnd(ii,2) = nint(3600.0+acplon(jj)*10.0)
            endif
         else
            ltlnwnd(ii,1) = 0
            ltlnwnd(ii,2) = 0
         endif           
         ltlnwnd(ii,3) = 0
      enddo
      write(cdatim,'(i8.8)')idatim 
      call writeAid( 60, strmid, cent, cdatim, 'JT92', ltlnwnd )
      close(60)


      DO 210 N=1, NFLDS
        ITAU = (N -1)*12
        IF (N .EQ. 1) THEN
C                   PROCESS INITIAL POSITION
C                   BY DEFINITION, MUST START IN NW PACIFIC
          FLAT = SLAT00
          FLON = -SLON00
          CALL FINDLO (FLAT,FLON,NGPLR,ALATNG,ALONNG,NLOWS)
          IF (NLOWS .GT. 0) THEN
            IF (ALATNG .GT. 0) THEN
              CNS = 'N'
            ELSE
              CNS = 'S'
              ALATNG = -ALATNG
            ENDIF
            IF (ALONNG .LT. 180.0) THEN
              CEW = 'W'
            ELSE
              CEW = 'E'
              ALONNG = 360.0 -ALONNG
            ENDIF
          ELSE
C                   SET MISSING VALUES
            CNS = '*'
            CEW = '*'
            ALATNG = 999999.9
            ALONNG = 999999.9
          ENDIF
C                   WRITE DIAGNOSTIC
cx        WRITE (19,9010) ITAU,ALATNG,CNS,ALONNG,CEW,NLOWS
          write (*,9010) itau,alatng,cns,alonng,cew,nlows
        ELSE
C                   PROCESS FORECAST POSITIONS
          FLAT = ACPLAT(N-1)
          FLON = ACPLON(N-1)
          CALL FINDLO (FLAT,FLON,NGPLR,ALATNG,ALONNG,NLOWS)
          IF (N .NE. 6) THEN
C                   OMIT TAU 60 OUTPUT
            IF (NLOWS .GT. 0) THEN
              IF (ALATNG .GT. 0) THEN
                CNS = 'N'
              ELSE
                CNS = 'S'
                ALATNG = -ALATNG
              ENDIF
              IF (ALONNG .LT. 180.0) THEN
                CEW = 'W'
              ELSE
                CEW = 'E'
                ALONNG = 360.0 -ALONNG
              ENDIF
            ELSE
C                   SET MISSING VALUES
              CNS = '*'
              CEW = '*'
              ALATNG = 999999.9
              ALONNG = 999999.9
            ENDIF
C                   WRITE DIAGNOSTIC
cx          WRITE (19,9010) ITAU,ALATNG,CNS,ALONNG,CEW,NLOWS
            write (*,9010) itau,alatng,cns,alonng,cew,nlows
            IF (FLAT .GT. 0.0) THEN
              CNS = 'N'
            ELSE
              CNS = 'S'
              FLAT = -FLAT
            ENDIF
            IF (FLON .GT. 0) THEN
              CEW = 'W'
            ELSE
              CEW = 'E'
              FLON = -FLON
            ENDIF
C                   WRITE FORECAST
cx          WRITE (19,9020) ITAU,FLAT,CNS,FLON,CEW
            write (*,9020) itau,flat,cns,flon,cew
          ENDIF
        ENDIF
  210 CONTINUE
 9010 FORMAT (' JT92  DIAG ',I2.2,F7.1,A1,F7.1,A1,' FOUND ',I2,
     .        ' LOW(S)')
 9020 FORMAT (' JT92  TAU=',I2,1X,F4.1,A1,1X,F5.1,A1)
  
C
  300 CONTINUE
      IF (IERR .EQ. 0) THEN
        IR(3) = 0
      ELSE
        IR(3) = 7
      ENDIF
cx    CALL SETCCL (IR)
cx    STOP
      print *, "JT92: NORMAL RUN"
      close (nunit)
      stop 
  980 continue
      write (nunit,*)'cannot open ',filename
      write (*,*)'cannot open ',filename
      close (nunit)
      stop 
C
      END
      SUBROUTINE STMDTA (NUNIT,NZ,cent,IERR)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  STMDTA
C
C  DESCRIPTION:      READ CYCLONE DATA, CHECK AREA, SET FORECAST ZONE
C                    AND LOCAL GRID ROTATION
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON  (GSA -CSC)  JULY 1992
C
C  LIBRARY OF RESIDENCE:  MT1731
C
C  CLASSIFICATION:        UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):  CALL STMDTA (IERR)
C
C  INPUT PARAMETERS:
C    NUNIT - UNIT NUMBER FOR DIAGNOSTIC OUTPUT
C
C  OUTPUT PARAMETERS:  NONE
C    IERR  - EROR FLAG, 0 - NO ERROR, -1 - WRONG AREA FOR JTWC92
C
C  INPUT FILES:
C    TAPE91 - CYCLONE DATA AND NUMBER OF DEEP LAYER MEAN FIELDS
C             AVAILABLE ON TAPE92
C
C               INPUT TAPE91 DOCUMENTATION FOR JTWC92
C
C            11111111112222222222333333333344444444445
C   12345678901234567890123456789012345678901234567890
C   91082012 14W  60 7 286N1317E 282N1333E 279N1347E
C
C    COL        ITEM
C    1- 8  DTG (YYMMDDHH) OF INITIAL LAT/LON
C   10-12 CYCLONE IDENTIFICATION, NUMBER AND ORIGINAL BASIN
C   14-16 MAXIMUM WIND SPEED (KTS)
C   18    NUMBER OF FIELDS PROCESSED BY JTWCPR FOR JTWC92
C   20-22 LATITUDE, INITIAL (286 = 28.6)
C   23    HEMISPHERE INDICATOR
C   24-27 LONGITUDE, INITIAL (1317 = 131.7)
C   28    HEMISPHERE INDICATOR
C   30-32 LATITUDE, 12HR OLD
C   33    HEMISPHERE INDICATOR
C   34-37 LONGITUDE, 12HR OLD
C   38    HEMISPHERE INDICATOR
C   40-42 LATITUDE, 24HR OLD
C   43    HEMISPHERE INDICATOR
C   44-47 LONGITUDE, 24HR OLD
C   48    HEMISPHERE INDICATOR
C
C  OUTPUT FILES:
C    PRINTEM - DIAGNOSTICS, IF ERROR
C
C  COMMON BLOCKS:  ALL LOADED IN THIS ROUTINE
C
C     /STMNAM/ - CYCLONE IDENTIFICATION, NUMBER AND ORIGINAL BASIN
C     /BLK04/  - PROCESS CONTROL DATA
C     /BLK05/  - CYCLONE DATA, LOCAL GRID DATA
C
C  ERROR CONDITIONS:  CYCLONE NOT IN NW PACIFIC
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:  NONE
C
C  LANGAUGE:  CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      CHARACTER CNS(3)*1, CEW(3)*1, ALPHA*8
C
      CHARACTER*10 SNAME
      character*6 strmid
      character*8 cdtg
      integer iage
C
      COMMON /STMNAM/SNAME
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
c
c     get the storm id
c
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
C
cx  call routine to read best track file
      call getbtrk( cent, cdtg, slat00, slon00, slat12, slon12, 
     1             slat24, slon24, cns, cew, wind )
      read( cdtg, '(i8.8)' ) idatim
      sname(1:2) = strmid(3:4)
      sname(3:3) = strmid(1:1)
      call upcase( sname, 3 )
      nflds = 7
      write (6,*)'TRACK POSITS:'
      write (6,'(I8,1X,A3,1X,I3,1X,I1,1X,3(F4.1,A1,1X,F5.1,A1,1X))') 
     1        idatim, sname(1:3), nint(wind), nflds, slat00, cns(1), 
     1        slon00, cew(1), slat12, cns(2), slon12, cew(2), slat24, 
     1        cns(3), slon24, cew(3)
C
C                   CHECK THAT CYCLONE IS IN NW PACIFIC
C
      IERR = 0
      IF (CNS(1) .NE. 'N')   IERR = -1
      IF (CEW(1) .NE. 'E')   IERR = -1
      IF (SLON00 .LT. 100.0) IERR = -1
      IF (IERR .EQ. 0) THEN
C
C                   CYCLONE IS IN NW PACIFIC
C
        WRITE (ALPHA,'(I8)') IDATIM
        READ (ALPHA,'(4I2)') KYR, MO, KDA, IUTC
        LFP    = (NFLDS -1)*12
        LASTHR = LFP/6
C
C                   DETERMINE LAST 12-HR HEADING
C
        IF (CEW(2) .EQ. 'E') THEN
C                   LL2DB REQUIRES EAST LONGITUDE TO BE NEGATIVE
          CALL LL2DB (SLAT12,-SLON12, SLAT00,-SLON00, GCDIST, AHP12H)
        ELSE
          CALL LL2DB (SLAT12,SLON12, SLAT00,-SLON00, GCDIST, AHP12H)
C                   MAKE SLON12 DEGREES EAST
          SLON12 = 360.0 -SLON12
        ENDIF
C
C                   DETERMINE LAST 12-HR SPEED (KTS)
C
        ASP12H = GCDIST/12.0
C
C                   DETERMINE ZONE FOR FORECASTING, 1, 2 OR 3
C
        NZ = LZONE (AHP12H,SLAT00)
C
C                   DETERMINE ROTATION ANGLE OF LOCAL GRID
C
        IF (NZ .NE. 3) THEN
C                   ZONES 1 AND 2 ROTATION IS PAST HEADING
          GRDROT = AHP12H
        ELSE
C                   EQUATORIAL ZONE ROTATION IS NORTH
          GRDROT = 360.0
        ENDIF
C
C                   ENSURE SLON24 IS IN DEGREES EAST
C
        IF (CEW(3) .EQ. 'W') SLON24 = 360.0 -SLON24
      ELSE
        WRITE (NUNIT,*)
     .        'JTWC92, STMDTA - CYCLONE NOT IN NW PACIFIC $ $ $ $'
      ENDIF
      RETURN
C
      END

C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            getbtrk
C
C  DESCRIPTION:
C
C      Get data from best track file
C
C  ORIGINAL PROGRAMMER, DATE:   Ann Schrader (SAIC) June, 1998
C
C  USAGE (CALLING SEQUENCE):    call getbtrk(cdtg,flt,flon,plt12,plon12,
C                                            plt24,plon24,cns,cew,wind)
C
C  INPUT FILES:
C
C      b????????.dat      best track file for storm 
C
C  COMMON BLOCKS:
C
C
C.........................MAINTENANCE SECTION...........................
C
C
C  PRINCIPAL VARIABLES AND ARRAYS (RETURNED ARGUMENT):
C
C
C  METHOD:
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      subroutine getbtrk( cent, cdtg, flt, flon, plt12, plon12, plt24, 
     1                    plon24, cns, cew, wind )

      character*100 storms,filename
      character*8 cdtg,dtg12,dtg24
      character*8 tdtg
      character*8 btdtg
      character*6 strmid
      character*2 century
      character*2 cent
      character btns*1, btew*1
      character cns(3)*1, cew(3)*1
      integer ibtwind, ios, iarg
      integer ifound00, ifound12, ifound24
      real btlat, btlon
      real flt, flon, plt24, plon24, plt12, plon12
      real wind

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
c     get the storm id
c
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c  get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      call openfile (91,filename,'old',ioerror)
      if (ioerror.lt.0) go to 950
c
c  convert the 1st two characters of stormid to uppercase
c
      call upcase(strmid,6)
c
c  find the last dtg in the best track file
c
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 91,cent,tdtg,btlat,btns,btlon,btew,ibtwind,ios )
         if (tdtg.ne.'        ') cdtg=tdtg
      enddo
c
c  now find the current, -12, and -24 hr positions
c
      call icrdtg (cdtg,dtg12,-12)
      call icrdtg (cdtg,dtg24,-24)
      rewind 91
      ifound00 = 0
      ifound12 = 0
      ifound24 = 0
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 91,cent,btdtg,btlat,btns,btlon,btew,ibtwind,ios )
         if( btdtg .eq. dtg24 ) then
            plt24 = btlat
            cns(3) = btns
            plon24 = btlon
            cew(3) = btew
            ifound24 = 1
         else if( btdtg .eq. dtg12 ) then
            plt12 = btlat
            cns(2) = btns
            plon12 = btlon
            cew(2) = btew
            ifound12 = 1
         else if( btdtg .eq. cdtg ) then
            flt = btlat
            cns(1) = btns
            flon = btlon
            cew(1) = btew
            wind = float(ibtwind)
            ifound00 = 1
         endif
      enddo
         
      if ( ifound00.eq.0 .or. ifound12.eq.0 .or. ifound24.eq.0 ) then
         write(7,*) "JTWC92: NEEDS AT LEAST 5 POSITIONS (24HRS) TO RUN"
         stop 
      endif
      close (91)
      return
  950 continue
      write (*,*)'cannot open ', filename
      stop
      end

      SUBROUTINE RT (DISP, CDISP)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            RT
C
C  DESCRIPTION:
C
C      CONVERT STORM DISPLACEMENTS REPRESENTED IN A MERIDIONAL/ZONAL
C      ORTHOGONAL SYSTEM TO AN ALONG TRACK/ACROSS TRACK ORTHOGONAL SYS-
C      TEM.  ROTATION IS RELATIVE TO AVERAGE STORM HEADING OVER PERIOD
C      FROM CURRENT TIME TO TIME 12H EARLIER.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL RT(DISP,CDISP)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK05/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES AND ARRAYS (INCOMING ARGUMENT):
C
C      DISP      =   (REAL) (DISP(I),I=1,12) ARRAY CONTAINING FORECAST
C                    STORM DISPLACEMENTS (NMI) AT 12-HRLY INTERVALS, 12
C                    THROUGH 72H RELATIVE TO A MERIDIONAL/ZONAL ORTH0G-
C                    ONAL SYSTEM.  ARRAY ADDRESSES 1, 3, 5, 7, 9, 11 ARE
C                    FOR A MERIDIONAL COMPONENT OF MOTION WHILE 2, 4, 6,
C                    8, 10 AND 12 ARE FOR A ZONAL COMPONENT OF MOTION
C                    FOR PERIODS 12, 24, 36, 48, 60, 72H, RESPECTIVELY.
C
C  PRINCIPAL VARIABLES AND ARRAYS (RETURNED ARGUMENT):
C
C      CDISP     =   (REAL) (CDISP(I),I=1,12) SIMILAR TO INCOMING
C                    ARRAY DISP EXCEPT THAT STORM POSITIONS ARE RELA-
C                    TIVE TO AN ALONG/ACROSS TRACK ORTHOGONAL SYSTEM
C                    WITH ALONG TRACK MOTION GIVEN BY VARIABLE 'ROTGRD'
C
C  OTHER IMPORTANT VARIABLES:
C
C      ROTGRD    =   (REAL) DIRECTION TOWARDS WHICH ALONG TRACK MOTION
C                    IS TO BE ORIENTED.  FOR NORTH AND SOUTH ZONES THIS
C                    IS DEFINED AS THE STORM MOTION FROM POSITION AT
C                    -12H TO THE INITIAL POSITION (PERSISTENCE TRACK).
C                    FOR THE EQUATORIAL ZONE, THIS IS SET TO 360 DEGREES
C                    WHICH IS EQUIVALENT TO A MERIDIONAL/ZONAL SYSTEM.
C
C
C
C  METHOD:
C
C      1.  ROTATION IS BASED ON NAVIGATIONAL SYSTEM DESCRIBED IN BLOCK
C          DATA SUBPROGRAM BLKDT2.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      DIMENSION DISP(12), CDISP(12)
C
      DO 10 I = 1, 6
         CALL STHGPR(SLAT00, -SLON00, 360., 1., 0., 0.)
         CALL XY2LLH(DISP(2*I), DISP(2*I - 1), QLAT, QLON)
         CALL STHGPR(SLAT00, -SLON00, GRDROT, 1.0, 0., 0.)
         CALL LL2XYH(QLAT, QLON, CDISP(2*I), CDISP(2*I - 1))
   10 CONTINUE
      RETURN
      END
      BLOCK DATA INLIZE
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            INLIZE
C
C  DESCRIPTION:                INITIALIZE ARRAYS AND VARIABLES.
C
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK06, BLK07, BLK09/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES AND ARRAYS (INCOMING ARGUMENT):
C
C      NONE. ALL ARRAYS, VARIABLES ARE ONLY INITIALIZED.
C
C  METHOD:
C
C      1.  ALL VARIABLES AND ARRAYS ARE INITIALIZED TO -99.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      DIMENSION C06(60), C07(60), C09(48)
C
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
      COMMON /BLK07/PLAT(6), PLON(6), ACLAT(6), ACLON(6), CLAT(6),
     *              CLON(6), ACPLAT(6), ACPLON(6), ALAT(6), ALON(6)
      COMMON /BLK09/TEMP1(12), TEMP2(12), TEMP3(6), TEMP4(6), TEMP5(6),
     *              TEMP6(6)
C
      EQUIVALENCE (C06(1),ADISP(1))
      EQUIVALENCE (C07(1),PLAT(1))
      EQUIVALENCE (C09(1),TEMP1(1))
C
      DATA C06/60 * -99.9/
      DATA C07/60 * -99.9/
      DATA C09/48 * -99.9/
C
      END
      SUBROUTINE WPCLIP (IDATIM, ALAT00, ALON00, ALAT12, ALON12, ALAT24,
     *                  ALON24, WIND, CNMIS)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            WPCLIP
C
C  DESCRIPTION:
C
C      PROGRAM MODULE GIVING 72H FORECAST OF TROPICAL CYCLONE MOTION
C      BASED ON PREDICTORS DERIVED FROM CLIMATOLOGY AND PERSISTENCE.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL WPCLIP(IDATIM,ALAT00,ALON00,ALAT12,
C                               ALON12,ALAT24,ALON24,WIND,CNMIS,CLALO,
C                               P1TOP8)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK01/,/BLK02/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      IDATIM     =  (INTEGER)  DATE TIME IN FORM YYMODAHR WHERE YY IS
C                    LAST TWO DIGITS OF YEAR, MO IS MONTH NUMBER, DA IS
C                    DAY OF MONTH AND HR IS UTC TIME. EXAMPLE...91082012
C                    FOR 1200 UTC ON AUGUST 20, 1991.
C
C      ALAT00     =  (REAL)  INITIAL LATITUDE (NORTH) OF STORM.
C
C      ALON12     =  (REAL)  INITIAL STORM LONGITUDE (EAST). NOTE THAT
C                    LONGITUDE OF 170W WOULD BE ENTERED AS 190.
C
C      ALAT12     =  (REAL)  LATITUDE (NORTH) 12H EARLIER THAN ALAT00.
C
C      ALON12     =  (REAL)  LONGITUDE (EAST) 12H EARLIER THAN ALON00.
C
C      ALAT24     =  (REAL)  LATITUDE (NORTH) 24H EARLIER THAN ALAT00.
C
C      ALON24     =  (REAL)  LONGITUDE (EAST) 24H EARLIER THAN ALON00.
C
C      WIND       =  (REAL)  INITIAL MAXIMUM WIND IN KNOTS.
C
C  PRINCIPAL VARIABLES (OUTGOING ARGUMENTS):
C
C      CNMIS     =   (REAL)  (CNMIS(I),I=1,12) ARRAY OF FORECAST DIS-
C                    PLACEMENTS (NMI) WHERE POSITIONS 1, 3, 5, 7, 9, 11
C                    ARE FORECAST MERIDIONAL DISPLACEMENTS 12H THROUGH
C                    72H (TOWARDS NORTH POSITIVE AND TOWARDS SOUTH NEGA-
C                    TIVE). POSITIONS 2, 4, 6, 8, 10 AND 12 ARE FORECAST
C                    ZONAL DISPLACEMENTS 12H THROUGH 72H (TOWARDS EAST
C                    POSITIVE AND TOWARDS WEST NEGATIVE).
C
C  OTHER IMPORTANT VARIABLES:
C
C     P           =  (REAL)  (P(L),L=1,166)  ADDRESSES 3 THRU 166 GIVE
C                    VALUES OF THE 164 POSSIBLE PREDICTORS GENERATED BY
C                    THE 3RD-ORDER BINOMIAL EXPANSION OF THE 8 BASIC
C                    PREDICTORS USED IN THE MODULE.  POSITIONS 1 AND 2
C                    IN THE ARRAY ARE NOT CURRENTLY USED.
C
C     RCM         =  (REAL)  ((RCM(I,J),J=I,6),I=1,90) ARRAY GIVING
C                    THE 90 (I-INDEX) MERIDIONAL REGRESSION COEFFICIENTS
C                    FOR THE SIX 12H TIME INTERVALS, 12 THROUGH 72H
C                    (J-INDEX).  THESE COEFFICIENTS ARE ENTERED INTO
C                    PROGRAM IN BLOCK DATA SUBPROGRAM /BLKDT1/.
C
C     RCZ         =  (REAL)  ((RCZ(I,J),J=I,6),I=1,95) ARRAY GIVING
C                    THE 95 (I-INDEX) ZONAL REGRESSION COEFFICIENTS FOR
C                    THE SIX 12H TIME INTERVALS, 12 THROUGH 72H
C                    (J-INDEX).  THESE COEFFICIENTS ARE ENTERED INTO
C                    PROGRAM IN BLOCK DATA SUBPROGRAM /BLKDT1/.
C
C     NPM         =  (INTEGER)  ((NPM(I,J),J=1,6),I=1,90) ARRAY GIVING
C                    THE 90 MERIDIONAL PREDICTOR NUMBERS.  THESE NUMBERS
C                    ARE ADDRESSES FOR ARRAY P(166).  THIS ARRAY IS
C                    DEFINED IN BLOCK DATA SUBPROGRAM /BLKDT1/.
C
C     NPZ         =  (INTEGER)  ((NPZ(I,J),J=1,6),I=1,95) ARRAY GIVING
C                    THE 95 ZONAL PREDICTOR NUMBERS.  THESE NUMBERS ARE
C                    ADDRESSES IN ARRAY P(166).  THIS ARRAY IS DEFINED
C                    IN BLOCK DATA SUBPROGRAM /BLKDT1/.
C
C     CNSTM       =  (REAL)  (CNSTM(J),J=1,6) ARRAY GIVING THE MERID-
C                    IONAL INTERCEPT VALUES FOR THE SIX 12H TIME
C                    PERIODS, 12H THROUGH 72H.
C
C     CNSTZ       =  (REAL)  (CNSTM(J),J=1,6) ARRAY GIVING THE ZONAL
C                    INTERCEPT VALUES FOR THE SIX 12H TIME PERIODS, 12H
C                    THROUGH 72H.
C
C  METHOD:
C
C      1.  WPCLIP USES PRE-COMPUTED REGRESSION EQUATIONS (SEE TECHNICAL
C          REPORT).
C
C      2.  CLIMATOLOGY PORTION OF MODEL IS REPRESENTED BY INITIAL LATI-
C          TUDE, INITIAL LONGITUDE, A JULIAN DAY NUMBER FUNCTION AND THE
C          MAXIMUM WIND AS WELL AS CERTAIN PRODUCTS AND CROSS-PRODUCTS
C          OF THESE VARIABLES.
C
C      3.  PERSISTENCE PORTION OF MODEL IS REPRESENTED BY STORM MOTION
C          OVER THE PAST 12 AND 24H AS COMPUTED FROM THE INITIAL, 12H
C          OLD AND 24H OLD STORM POSITIONS.
C
C      4.  PROGRAM WAS DEVELOPED USING STORM TRACKS OVER YEARS 1945-1988
C
C      5.  ALL MONTHS WERE INCLUDED IN DEVELOPMENTAL DATA SET.
C      6.  STORMS INITIALLY LOCATED EAST OF 180 DEGS WERE EXCLUDED.
C
C      7.  STORMS INITIALLY LOCATED NORTH OF 50N WERE EXCLUDED.
C      8.  STORMS WHICH INITIALLY CLASSIFIED AS DEPRESSIONS OR
C          CLASSIFIED AS DEPRESSIONS AT VERIFICATION TIME WERE EXCLUDED.
C
C      9.  RESULTANT SAMPLE SIZE FROM ABOVE CRITERIA.....
C          18891 AT 12H, 16851 AT 24H, 14979 AT 36H,
C          13224 AT 48H, 11598 AT 60H, 10094 AT 72H.
C
C     10.  INDIVIDUAL CASES IN DEVELOPMENTAL DATA SET WERE AT 6 HRLY
C          INTERVALS
C
C     11.  PROGRAM PREPARED BY CHARLES J. NEUMANN, SAIC, OCT NOV DEC,
C          1989.
C     12.  THIS VERSION OF WPCLIP REPLACES EARLIER VERSION REPORTED ON
C          BY XU AND NEUMANN (1985) IN NOAA TECHNICAL MEMORANDUM NWS NHC
C          28. EARLIER XU & NEUMANN VERSION HAD CERTAIN SEASONAL AND
C          GEOGRAPHICAL RESTRICTIONS.  CURRENT VERSION HAS NO
C          RESTRICTIONS OTHER THAN AS NOTED ABOVE.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  WPCLIP*01  (28 APR 1993)  --  HAMILTON,H.
C           1. LIMIT THE RANGE OF P1 FROM 7.5 TO 45, BUT USE ACTUAL
C              LATITUDE IN CALL TO STHGPR - SAME CHANGES AS PUT IN
C              UPGRADED VERSION OF WPCLPR.
C           2. REMOVE UNNECESSARY ARRAYS AND CALL TO SUBROUTINE NMI2LL
C
C.........................END PROLOGUE.................................
C
      COMMON/BLOCK1/NPM,NPZ,RCM(90,6),RCZ(95,6),CNSTM(6),CNSTZ(6)
C
      INTEGER NPM(90, 6), NPZ(95, 6)
      REAL P(166), CNMIS(12)
C
C     ALL REGRESSION COEFFICIENTS AND PREDICTOR NUMBERS ARE CONTAINED IN
C     IN BLOCK DATA BLKDT1.  THERE ARE 90 PREDICTORS AND PREDICTOR
C     NUMBERS FOR MERIDIONAL MOTION AND 95 PREDICTORS AND PREDICTOR
C     NUMBERS FOR ZONAL MOTION. ((RCM(I,J),J=1,6,I=1,90) AND
C     ((NPM(I,J),J=1,6),I=1,90) ARE COEFFICIENTS AND PREDICTOR NUMBERS
C     FOR MERIDIONAL MOTION WHILE ((RCZ(I,J),J=1,6,I=1,95) AND
C     ((NPZ(I,J),J=1,6),I=1,95) ARE COEFFICIENTSC AND PREDICTOR NUMBERS
C     FOR ZONAL MOTION. SUBSCRIPT J REFERS TO TIME WHERE J=1=12H.......
C     ..J=6=72H.  6 MERIDIONAL INTERCEPT VALUES ARE GIVEN BY
C     (CNSTM(J),J=1,6) WHILE THE 6 ZONAL INTERCEPT VALUES ARE GIVEN BY
C     (CNSTZ(J),J=1,6).
C
C     P1 THRU P8 ARE 8 PRIMARY PREDICTORS WHERE...
C     P1 IS INITIAL LATITUDE  (DEGS NORTH)
C     P2 IS INITIAL LONGITUDE (DEGS EAST)
C     P3 IS FUNCTION OF JULIAN DAY NUMBER WITH FEB 11 0000UTC
C     SET TO DAY NUMBER 0 AND AUG 12 SET TO MID-YEAR
C     P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)
C     P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
C     P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
C     P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
C     P8 IS MAXIMUM WIND (KNOTS)
C
C      FUNCTIONS AND SUBPROGRAMS NEEDED BY WPCLIP ARE AS FOLLOWS:
C     DATA NEEDED BY PROGRAM ARE CONTAINED IN BLOCK DATA BLKDT1 AND
C     BLKDT2
C     WPCLIP CALLS SUBROUTINES STHGPR, LL2XYH, PSETUP AND NMI2LL
C     AND UTILIZES FUNCTIONS F1, F2
C     NMI2LL CALLS SUBROUTINE XY2LLH AND UTILIZES FUNCTION F1
C
C     SET UP 8 BASIC PREDICTORS......
C                   KEEP P1 WITHIN 7.5 TO 45.0 DEGREES NORTH
C
      IF (ALAT00 .GT. 45.0) THEN
        P1 = 45.0
      ELSEIF (ALAT00 .LT. 7.5) THEN
        P1 = 7.5
      ELSE
        P1 = ALAT00
      ENDIF
      P2 = ALON00
C     JULIAN DAY NUMBER. GET CONVERSION FACTOR (.008613) SUCH THAT SIN
C     OF DAY NUMBER 0 (FEB 11) HAS VALUE NEAR ZERO AND MID-YEAR (AUG 12)
C     HAS VALUE NEAR 1.00.  NOTE THAT DAY NUMBER IS OFFSET BY 41 DAYS
C     SUCH THAT FEB 11 IS DAY NUMBER 0 AND AUG 12 IS MID-YEAR.
      CONVRT = 2.*ACOS(0.)/364.75
      P3 = F2(IDATIM) - 41.
      IF ( P3 .LT. 0. ) P3 = P3 + 365.
      P3 = SIN(P3*CONVRT)
      P8 = WIND
C     USE AL TAYLOR ROUTINES (SEE NOTE BELOW) FOR CONVERTING
C     LATITUDE/LONGITUDE TO DISPLACEMENTS.
C     THESE SAME ROUTINES ARE LATER USED FOR CONVERTING DISPLACEMENTS
C     BACK TO LATITUDES AND LONGITUDES........
C     NOTE....AL TAYLOR ROUTINES REFER TO SUBROUTINES STHGPR,LL2XYH,
C     XY2LLH, LL2DB (PREDICTORS NUMBER P4 THRU P7)
      CALL STHGPR (ALAT00, F1(P2), 360.0, 1.0, 0.0, 0.0)
      CALL LL2XYH(ALAT12, F1(ALON12), P5, P4)
      CALL LL2XYH(ALAT24, F1(ALON24), P7, P6)
C     CHANGE SIGN
      P4 =  - P4
      P5 =  - P5
      P6 =  - P6
      P7 =  - P7
C
C     PREPARE FORECAST, FIRST, OBTAIN ALL POSSIBLE 3RD ORDER PRODUCTS
C     AND CROSS-PRODUCTS OF THE 8 BASIC PREDICTORS AND RETURN THESE IN
C     ARRAY (P(L),L=1,166).  THERE ARE 164 POSSIBLE COMBINATIONS AND
C     THESE ARE GIVEN BY SUBSCRIBTS 3 THROUGH 166. P(1) AND P(2) ARE
C     NOT USED AND HAVE BEEN RETURNED AS DUMMY VARIABLES. NOT ALL OF THE
C     164 POSSIBLE PREDICTORS ARE USED IN PROGRAM.
      CALL PSETUP(P1, P2, P3, P4, P5, P6, P7, P8, P)
C     OBTAIN FORECAST MERIDIONAL DISPLACEMENTS 12 THRU 72H
      DO 20 J = 1, 6
C        INITIALIZE COMPUTATION WITH INTERCEPT VALUE
         CNMIS(2*J - 1) = CNSTM(J)
         DO 10 I = 1, 90
            K = NPM(I, J)
            CNMIS(2*J - 1) = CNMIS(2*J - 1) + RCM(I, J)*P(K)
   10    CONTINUE
   20 CONTINUE
C
C     OBTAIN FORECAST ZONAL DISPLACEMENTS 12 THRU 72H
C
      DO 40 J = 1, 6
C        INITIALIZE COMPUTATION WITH INTERCEPT VALUE
         CNMIS(2*J) = CNSTZ(J)
         DO 30 I = 1, 95
            K = NPZ(I, J)
            CNMIS(2*J) = CNMIS(2*J) + RCZ(I, J)*P(K)
   30    CONTINUE
   40 CONTINUE
      RETURN
      END
      FUNCTION F1 (ALON)
C.........................START PROLOGUE................................
C
C  FUNCTION NAME:            REAL FUNCTION F1
C
C  DESCRIPTION:
C
C      ASCERTAINS THAT EAST LONGITUDES 0 TO 180 ARE SIGNED NEGATIVE AND
C      WEST LONGITUDES 0 TO 180 ARE SIGNED POSITIVE.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    R=F1(ALON)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C      ALON   =      CYCLONE LONGITUDE IN DEGREES EAST
C
C  RETURNED VARIABLE (FUNCTION):
C
C      F1     =      LONGITUDE IN RANGE 0 TO +180 OR 0 TO -180 DEGREES.
C
C  METHOD:
C
C      1.  INPUT TO NAVIGATIONAL ROUTINES USED HEREIN REQUIRE EAST LONG-
C          ITUDES TO BE SIGNED NEGATIVELY, 0 TO 180 AND WEST LONGITUDES,
C          SIGNED POSITIVELY FROM 0 TO 180.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C      NONE
C.........................END PROLOGUE..................................
C
      IF (ALON .LE. 180.0) THEN
        F1 = -ALON
      ELSE
        F1 = 360.0 -ALON
      ENDIF
      RETURN
C
      END
      FUNCTION F2 (IDATIM)
C.........................START PROLOGUE................................
C
C  FUNCTION NAME:            REAL FUNCTION F2
C
C  DESCRIPTION:
C
C      COMPUTES JULIAN DAY NUMBER.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    R=F2(IDATIM)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C      IDATIM   =    (INTEGER) DATE TIME IN FORM YYMMDDHH WHERE YY IS
C                    CURRENT YEAR - 1900, MM IS MONTHS 1 THROUGH 12, DD
C                    IS DAY OF MONTH AND HH IS UTC 00, 06, 12 OR 18.
C
C  RETURNED ARGUMENT (FUNCTION):
C
C      F2       =    (REAL) JULIAN DAY NUMBER RANGING FROM 0.0 FOR 0000
C                    UTC 1 JAN TO 364.75 FOR 1800 UTC 31 DEC.
C
C  METHOD:
C
C
C      1.  FUNCTION DOES NOT CONSIDER LEAP YEARS.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      CHARACTER*8 ALFA
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
      WRITE (ALFA, '(I8)') IDATIM
      READ (ALFA, '(2X,3I2)') MO, KDA, KHR
      MON = MO
      IF ( MON .EQ. 13 ) MON = 1
      DANBR = 3055*(MON + 2)/100 - ((MON + 10)/13)*2 - 91 + KDA
      F2 = DANBR - 1. + FLOAT(KHR/6)*0.25
      RETURN
      END
      BLOCK DATA BLKDT2
C.........................START PROLOGUE................................
C
C  BLOCK DATA SUBPROGRAM NAME: BLKDT2
C
C  DESCRIPTION:
C
C      PROVIDES COMPILATION TIME INITIALIZATION TO PROGRAM MODULE WHICH
C      COMPUTES ALONG AND ACROSS TRACK GRID POINT LOCATIONS RELATIVE TO
C      CURRENT POSITION AND HEADING OF A TROPICAL CYCLONE OR VICE VERSA.
C
C  ORIGINAL PROGRAMMER, DATE:   ALBION D. TAYLOR, NOAA, MARCH, 1982
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  COMMON BLOCKS: /HGRPRM/
C
C
C.........................MAINTENANCE SECTION...........................
C
C      VARIABLES INITIALIZED:
C
C      1) A(3,3) (WORKING ARRAY) TO  0.,-1.,0.  ,1.,0.,0.,  0.,0.,1.
C      2) RADPDG (RADIANS PER DEGREE) TO 1.7453293E-2
C      3) RRTHNM (RADIUS OF EARTH IN NAUTICAL MILES) TO 3440.17
C      4) DGRIDH (DEFAULT VALUE OF GRID POINT SPACING IN NMI) TO 120.
C      5) HGRIDX (X-DIRECTION POSITION OF STORM IN GRID) TO 0.0
C      6) HGRIDY (Y-DIRECTION POSITION OF STORM IN GRID) TO 0.0
C
C  METHOD:
C
C      1.  PROVIDES COMPILATION TIME INITIALIZATION OF ABOVE VALUES.
C
C      2.  INCLUDES COMMENTS WHICH PROVIDE COMPLETE DOCUMENTATION.
C
C      3.  OTHER MODULE MEMBERS ARE SUBROUTINES STHGPR, LL2XYH, XY2LLH.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      COMMON /HGRPRM/A(3,3), RADPDG, RRTHNM, DGRIDH, HGRIDX, HGRIDY
C
      DATA A/0., -1., 0., 1., 0., 0., 0., 0., 1./
      DATA RADPDG/1.7453293E-2/, RRTHNM/3440.17/
      DATA DGRIDH/120./
      DATA HGRIDX/0.0/, HGRIDY/0.0/
      END
      SUBROUTINE PSETUP (P1, P2, P3, P4, P5, P6, P7, P8, P)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            PSETUP
C
C  DESCRIPTION:
C
C      PART OF WPCLIP MODULE. DEFINES (COMPUTES) ALL POSSIBLE PREDICTORS
C      USED IN THE PROGRAM.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL PSETUP(P1,P2,P3,P4,P5,P6,P7,P8,P)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      NONE
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      P1     =      (REAL) INITIAL STORM LATITUDE (DEGREES NORTH)
C
C      P2     =      (REAL) INITIAL STORM LONGITUDE (DEGREES EAST)
C
C      P3     =      (REAL) JULIAN DAY NUMBER SINE FUNCTION (0 S P3 S)
C                    DEFINED (COMPUTED) IN SUBROUTINE WPCLIP
C
C      P4     =      (REAL) LATITUDINAL (MERIDIONAL) DISPLACEMENT OF
C                    STORM IN NMI FROM POSITION 12H EARLIERTHAN CURRENT
C                    POSITION.  DISPLACEMENTS (NORTH/SOUTH) ARE (+/-).
C
C      P5     =      (REAL) LONGITUDINAL (ZONAL) DISPLACEMENT OF STORM
C                    IN NMI FROM POSITION 12H EARLIER THAN CURRENT POSI-
C                    TION.  DISPLACEMENTS (EAST/WEST) ARE (+/-).
C
C      P6     =      (REAL) LATITUDINAL (MERIDIONAL) DISPLACEMENT OF
C                    STORM IN NMI FROM POSITION 24H EARLIER THAN CURRENT
C                    POSITION.  DISPLACEMENTS (NORTH/SOUTH) ARE (+/-).
C
C      P7     =      (REAL) LONGITUDINAL (ZONAL) DISPLACEMENT OF STORM
C                    IN NMI FROM POSITION 24H EARLIER THAN CURRENT POSI-
C                    TION.  DISPLACEMENTS (EAST/WEST) ARE (+/-).
C
C      P8     =      (REAL) CURRENT MAXIMUM WIND (KNOTS) IN STORM.
C
C  PRINCIPAL VARIABLES (RETURNED):
C      P      =      (REAL) (P(L),L=3,166) WHERE POSITIONS 3 THROUGH
C                    166 GIVE THE 164 VALUES OF ALL PREDICTORS USED IN
C                    PROGRAM.  ARRAY POSITIONS 1 AND 2 ARE NOT USED.
C  METHOD:
C
C      1.  THE PREDICTORS, (P(L),L=3,164), REPRESENT ALL POSSIBLE
C          PRODUCTS AND CROSS PRODUCTS, UP TO ORDER 3, OF THE EIGHT
C          PRIMARY PREDICTORS P1 THROUGH P8.
C
C      2.  NOT ALL OF THE 164 POSSIBLE PREDICTORS ARE NECESSARILY USED
C          IN THE PROGRAM.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      DIMENSION P(166)
C
      DUMMY = 9999.
      P(1) = DUMMY
      P(2) = DUMMY
C     P(003)THRU P(166) ARE ALL POSSIBLE PREDICTORS AS OBTAINED FROM
C     CUBIC POLYNOMIAL EXPANSION OF ORIGINAL 8 BASIC PREDICTORS P1 THRU
C     P8.
C     LIST THE PREDICTORS................
      P(3) = P8
      P(4) = P8*P8
      P(5) = P8*P8*P8
      P(6) = P7
      P(7) = P7*P8
      P(8) = P7*P8*P8
      P(9) = P7*P7
      P(10) = P7*P7*P8
      P(11) = P7*P7*P7
      P(12) = P6
      P(13) = P6*P8
      P(14) = P6*P8*P8
      P(15) = P6*P7
      P(16) = P6*P7*P8
      P(17) = P6*P7*P7
      P(18) = P6*P6
      P(19) = P6*P6*P8
      P(20) = P6*P6*P7
      P(21) = P6*P6*P6
      P(22) = P5
      P(23) = P5*P8
      P(24) = P5*P8*P8
      P(25) = P5*P7
      P(26) = P5*P7*P8
      P(27) = P5*P7*P7
      P(28) = P5*P6
      P(29) = P5*P6*P8
      P(30) = P5*P6*P7
      P(31) = P5*P6*P6
      P(32) = P5*P5
      P(33) = P5*P5*P8
      P(34) = P5*P5*P7
      P(35) = P5*P5*P6
      P(36) = P5*P5*P5
      P(37) = P4
      P(38) = P4*P8
      P(39) = P4*P8*P8
      P(40) = P4*P7
      P(41) = P4*P7*P8
      P(42) = P4*P7*P7
      P(43) = P4*P6
      P(44) = P4*P6*P8
      P(45) = P4*P6*P7
      P(46) = P4*P6*P6
      P(47) = P4*P5
      P(48) = P4*P5*P8
      P(49) = P4*P5*P7
      P(50) = P4*P5*P6
      P(51) = P4*P5*P5
      P(52) = P4*P4
      P(53) = P4*P4*P8
      P(54) = P4*P4*P7
      P(55) = P4*P4*P6
      P(56) = P4*P4*P5
      P(57) = P4*P4*P4
      P(58) = P3
      P(59) = P3*P8
      P(60) = P3*P8*P8
      P(61) = P3*P7
      P(62) = P3*P7*P8
      P(63) = P3*P7*P7
      P(64) = P3*P6
      P(65) = P3*P6*P8
      P(66) = P3*P6*P7
      P(67) = P3*P6*P6
      P(68) = P3*P5
      P(69) = P3*P5*P8
      P(70) = P3*P5*P7
      P(71) = P3*P5*P6
      P(72) = P3*P5*P5
      P(73) = P3*P4
      P(74) = P3*P4*P8
      P(75) = P3*P4*P7
      P(76) = P3*P4*P6
      P(77) = P3*P4*P5
      P(78) = P3*P4*P4
      P(79) = P3*P3
      P(80) = P3*P3*P8
      P(81) = P3*P3*P7
      P(82) = P3*P3*P6
      P(83) = P3*P3*P5
      P(84) = P3*P3*P4
      P(85) = P3*P3*P3
      P(86) = P2
      P(87) = P2*P8
      P(88) = P2*P8*P8
      P(89) = P2*P7
      P(90) = P2*P7*P8
      P(91) = P2*P7*P7
      P(92) = P2*P6
      P(93) = P2*P6*P8
      P(94) = P2*P6*P7
      P(95) = P2*P6*P6
      P(96) = P2*P5
      P(97) = P2*P5*P8
      P(98) = P2*P5*P7
      P(99) = P2*P5*P6
      P(100) = P2*P5*P5
      P(101) = P2*P4
      P(102) = P2*P4*P8
      P(103) = P2*P4*P7
      P(104) = P2*P4*P6
      P(105) = P2*P4*P5
      P(106) = P2*P4*P4
      P(107) = P2*P3
      P(108) = P2*P3*P8
      P(109) = P2*P3*P7
      P(110) = P2*P3*P6
      P(111) = P2*P3*P5
      P(112) = P2*P3*P4
      P(113) = P2*P3*P3
      P(114) = P2*P2
      P(115) = P2*P2*P8
      P(116) = P2*P2*P7
      P(117) = P2*P2*P6
      P(118) = P2*P2*P5
      P(119) = P2*P2*P4
      P(120) = P2*P2*P3
      P(121) = P2*P2*P2
      P(122) = P1
      P(123) = P1*P8
      P(124) = P1*P8*P8
      P(125) = P1*P7
      P(126) = P1*P7*P8
      P(127) = P1*P7*P7
      P(128) = P1*P6
      P(129) = P1*P6*P8
      P(130) = P1*P6*P7
      P(131) = P1*P6*P6
      P(132) = P1*P5
      P(133) = P1*P5*P8
      P(134) = P1*P5*P7
      P(135) = P1*P5*P6
      P(136) = P1*P5*P5
      P(137) = P1*P4
      P(138) = P1*P4*P8
      P(139) = P1*P4*P7
      P(140) = P1*P4*P6
      P(141) = P1*P4*P5
      P(142) = P1*P4*P4
      P(143) = P1*P3
      P(144) = P1*P3*P8
      P(145) = P1*P3*P7
      P(146) = P1*P3*P6
      P(147) = P1*P3*P5
      P(148) = P1*P3*P4
      P(149) = P1*P3*P3
      P(150) = P1*P2
      P(151) = P1*P2*P8
      P(152) = P1*P2*P7
      P(153) = P1*P2*P6
      P(154) = P1*P2*P5
      P(155) = P1*P2*P4
      P(156) = P1*P2*P3
      P(157) = P1*P2*P2
      P(158) = P1*P1
      P(159) = P1*P1*P8
      P(160) = P1*P1*P7
      P(161) = P1*P1*P6
      P(162) = P1*P1*P5
      P(163) = P1*P1*P4
      P(164) = P1*P1*P3
      P(165) = P1*P1*P2
      P(166) = P1*P1*P1
      RETURN
      END
      FUNCTION NEWCYC (NOWCYC, N)
C.........................START PROLOGUE................................
C
C  FUNCTION NAME:            INTEGER FUNCTION NEWCYC
C
C  DESCRIPTION:
C
C      COMPUTES NEW DATETIME BEFORE OR AFTER AN OLD DATETIME
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON
C
C  USAGE (CALLING SEQUENCE):    I=IDATIM(NOWCYC,N)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      NOWCYC   =    (INTEGER) DATE TIME IN FORM YYMMDDHH WHERE YY IS
C                    CURRENT YEAR - 1900, MM IS MONTHS 1 THROUGH 12, DD
C                    IS DAY OF MONTH AND HH IS UTC 00, 06, 12 OR 18.
C
C      N        =    (INTEGER) NUMBER OF HOURS TO BE ADDED OR SUBTRACTED
C                    FROM NOWCYC.  MAXIMUM IS 744 HOURS.
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENT):
C
C      NEWCYC   =    (INTEGER) NOWCYC PLUS OR MINUS N HOURS
C  METHOD:
C
C      1.  HAS PROVISION FOR LEAP YEARS
C
C      2.  MAXIMUM NUMBER OF HOURS AHEAD OR BEHIND IS 744
C
C      3. ADDITIONAL HOURS AHEAD OR BACK CAN BE OBTAINED WITH MULTIPLE
C         CALLS.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      CHARACTER*8 ALFA
      INTEGER NHEM(15), NOLEAP(15)
C
      DATA NOLEAP/0, 744, 1488, 2160, 2904, 3624, 4368, 5088, 5832,
     * 6576, 7296, 8040, 8760, 9504, 10248/
C     ABOVE DATA STATEMENT GIVES NUMBER OF HOURS FOR NON-LEAP YEAR
C     MONTHS MONTHS 0000UTC ON 1 DEC THRU 0000UTC ON 1 FEB OF SECOND
C     YEAR.
C
C     OBTAIN YEAR (KYR),MONTH (M0),DAY (KDA) AND HOUR (JTM) IN INTEGER
C     FORMAT
      WRITE (ALFA, '(I8)') NOWCYC
      READ (ALFA, '(4I2)') KYR, MO, KDA, JTM
      DO 10 I = 1, 15
         NHEM(I) = NOLEAP(I)
   10 CONTINUE
C     IS THIS A LEAP YEAR? (YEAR 2000 IS A LEAP YEAR)
      IF ( MOD(KYR, 4) .EQ. 0 ) THEN
         DO 20 I = 4, 15
            NHEM(I) = NHEM(I) + 24
   20    CONTINUE
      ENDIF
C     HOW MANY HRS FROM BEGINNING OF TIME WINDOW AT 0000UTC, 1 DEC
C     (NHROLD)?
      NHROLD = NHEM(MO + 1) + (KDA - 1)*24 + JTM
C     HOW MANY HRS NEEDED FROM BEGINNING OF WINDOW (NHRNEW)?
      NHRNEW = NHROLD + N
C
      DO 30 MO = 2, 15
C        MO = 2 = PREVIOUS YEAR; M0 = 15 = NEXT YEAR; DO WE NEED TO ADD
C        OR SUBTRACT A YEAR??
         KYRNEW = KYR - (2/MO) + MO/15
C        CHANGE OF CENTURY?
         IF ( KYRNEW .EQ. 100 ) KYRNEW = 0
         IF ( KYRNEW .EQ. -1 ) KYRNEW = 99
C
         IF ( NHRNEW .LT. NHEM(MO) ) GOTO 40
   30 CONTINUE
   40 NDIF = NHRNEW - NHEM(MO - 1)
      LDA = (NDIF + 24)/24
      LTM = NDIF + 24 - (LDA*24)
      INDEX = MOD(MO - 3, 12) + (2/MO)*12 + 1
      NEWCYC = KYRNEW*1000000 + INDEX*10000 + LDA*100 + LTM
      RETURN
      END
      BLOCK DATA BLKDT1
C.........................START PROLOGUE................................
C
C  BLOCK DATA SUBPROGRAM NAME: BLOCK DATA BLKDT1
C
C  DESCRIPTION:
C
C      CONSTANTS NEEDED FOR WESTERN PACIFIC CLIPER MODULE (WPCLIP).
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    COMPILATION TIME DATA ENTRY
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK01/,/BLK02/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (ENTERED INTO /BLK01/):
C
C     RCM         =  (REAL)  ((RCM(I,J),J=I,6),I=1,90) ARRAY GIVING THE
C                    90 (I) MERIDIONAL REGRESSION COEFFICIENTS FOR
C                    THE SIX 12H TIME INTERVALS, 12 THROUGH 72H (J).
C
C     RCZ         =  (REAL)  ((RCZ(I,J),J=I,6),I=1,95) ARRAY GIVING THE
C                    90 (I) ZONAL REGRESSION COEFFICIENTS FOR THE SIX
C                    12H TIME INTERVALS, 12 THROUGH 72H (J).
C
C     CNSTM       =  (REAL)  (CNSTM(J),J=1,6) ARRAY GIVING THE MERIDION-
C                    AL INTERCEPT VALUES FOR THE SIX 12H TIME PERIODS,
C                    12H THROUGH 72H.
C
C     CNSTZ       =  (REAL)  (CNSTM(J),J=1,6) ARRAY GIVING THE ZONAL
C                    INTERCEPT VALUES FOR THE SIX 12H TIME PERIODS, 12H
C                    THROUGH 72H.
C
C  PRINCIPAL VARIABLES (ENTERED INTO /BLK02/):
C
C     NPM         =  (INTEGER)  ((NPM(I,J),J=1,6),I=1,90) ARRAY GIVING
C                    THE 90 MERIDIONAL PREDICTOR NUMBERS.  THESE NUMBERS
C                    REPRESENT ADDRESSES IN ARRAY P(166).
C
C     NPZ         =  (INTEGER)  ((NPZ(I,J),J=1,6),I=1,95) ARRAY GIVING
C                    THE 95 ZONAL PREDICTOR NUMBERS.  THESE NUMBERS
C                    REPRESENT ADDRESSES IN ARRAY P(166).
C
C  METHOD:
C
C      1.  CONSTANTS WERE DETERMINED USING A DEVELOPMENTAL DATA SET
C          1945-1988.  SEE TECHNICAL MANUAL ON WPCLIP PROGRAM.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON/BLOCK1/NPM,NPZ,RCM(90,6),RCZ(95,6),CNSTM(6),CNSTZ(6)
C
      REAL R12M(90), R24M(90), R36M(90), R48M(90), R60M(90), R72M(90)
      REAL R12Z(95), R24Z(95), R36Z(95), R48Z(95), R60Z(95), R72Z(95)
      INTEGER N12M(90), N24M(90), N36M(90), N48M(90), N60M(90),
     *        N72M(90)
      INTEGER N12Z(95), N24Z(95), N36Z(95), N48Z(95), N60Z(95),
     *        N72Z(95)
      INTEGER NPM(90, 6), NPZ(95, 6)
C
C
C
      EQUIVALENCE
     $(N12M(1),NPM(1,1)),(N24M(1),NPM(1,2)),(N36M(1),NPM(1,3))
      EQUIVALENCE
     $(N48M(1),NPM(1,4)),(N60M(1),NPM(1,5)),(N72M(1),NPM(1,6))
      EQUIVALENCE
     $(N12Z(1),NPZ(1,1)),(N24Z(1),NPZ(1,2)),(N36Z(1),NPZ(1,3))
      EQUIVALENCE
     $(N48Z(1),NPZ(1,4)),(N60Z(1),NPZ(1,5)),(N72Z(1),NPZ(1,6))
C
      EQUIVALENCE
     $(R12M(1),RCM(1,1)),(R24M(1),RCM(1,2)),(R36M(1),RCM(1,3))
      EQUIVALENCE
     $(R48M(1),RCM(1,4)),(R60M(1),RCM(1,5)),(R72M(1),RCM(1,6))
      EQUIVALENCE
     $(R12Z(1),RCZ(1,1)),(R24Z(1),RCZ(1,2)),(R36Z(1),RCZ(1,3))
      EQUIVALENCE
     $(R48Z(1),RCZ(1,4)),(R60Z(1),RCZ(1,5)),(R72Z(1),RCZ(1,6))
C
C  12HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R12M/
     A .3243071E-1, .8344170E-1, .3097537E-5, .1585081E-4,-.5781467E+0,
     B .5559386E-1,-.1366367E-2,-.3860944E-3,-.1971581E-1,-.1506403E+0,
     C-.4094524E-4,-.5283375E-5,-.3027484E+0, .8434259E-5,-.3899679E-4,
     D .9574963E-7, .4653325E+0, .1591545E-4, .7693003E-2,-.1005234E-5,
     E .3358553E-7, .1633963E-3, .1816813E-1,-.6719710E-4,-.1759287E-4,
     F-.7372505E-6,-.1096292E-3, .6955126E-2, .5218342E-4, .5895122E+0,
     G .2061950E-4,-.2190146E-3, .5322326E-4,-.2373855E-4, .4469749E-4,
     H-.2265381E-4, .1979948E-5,-.5109265E-2,-.2950181E-3, .6109930E+1,
     I .7605872E+1,-.4546854E-4, .1600313E-5,-.2928901E-2, .4102941E+1,
     J .1390362E-3,-.3042169E-6, .2936898E-2, .2463492E-4,-.5564410E-5,
     K-.1063433E-1, .2013024E-4, .1141800E-3,-.3022033E-2, .8813960E-4,
     L-.5440627E+1, .3820794E+3,-.8052462E+2,-.1642693E-1, .1319590E-2,
     M .3117979E-3,-.5988197E+3,-.1305264E-2, .5542873E+1, .4542397E-2,
     N .2795997E-1,-.1545122E+0,-.9023645E-2,-.5600628E-4,-.1015321E+1,
     O .8042760E-3,-.9450367E-4,-.4567757E+1, .3214121E-1,-.1547069E-1,
     P .2040100E+1,-.2301845E-2, .4422556E-4,-.5294287E-2,-.3743809E-3,
     Q-.2507454E-5,-.3437747E-2, .1066433E-3,-.1318755E-3, .4227765E-6,
     R .1076038E-3, .1793193E-3, .2274033E-5,-.2935162E-2, .5331651E-7/
C
C  12HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N12M/
     A         037,         022,         021,         053,         006,
     B         137,         163,         077,         120,         082,
     C         057,         044,         150,         100,         136,
     D         011,         158,         142,         043,         049,
     E         031,         015,         101,         104,         116,
     F         020,         119,         089,         132,         068,
     G         130,         066,         055,         046,         117,
     H         139,         045,         092,         071,         107,
     I         122,         153,         131,         111,         086,
     J         070,         010,         065,         048,         016,
     K         125,         095,         076,         166,         160,
     L         149,         079,         085,         114,         157,
     M         161,         058,         165,         143,         145,
     N         148,         084,         128,         133,         113,
     O         069,         129,         073,         112,         110,
     P         064,         018,         106,         052,         109,
     Q         041,         074,         138,         032,         051,
     R         108,         062,         029,         081,         054/
C
C  24HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R24M/
     A .3153820E+0, .2997032E+0, .1041448E-4, .5041134E-4,-.1156390E+1,
     B .5317333E-1,-.2084367E-2, .3042450E-4,-.8799762E-4, .1022893E+2,
     C .6685339E+0,-.1132432E-3,-.9044307E-4, .7902439E-3, .1087582E-5,
     D .1859850E-6,-.1018892E-2,-.3072454E-5,-.2157618E-4, .7834254E-3,
     E .3795866E+1,-.7374839E-4, .2412219E-1,-.4092464E-1,-.1858413E-3,
     F-.2764014E-4,-.3711128E+0, .1323014E-1, .2087213E-3, .7945657E-4,
     G-.2079803E-5,-.7822717E-5, .5451679E-4,-.5515313E-5, .1539684E-3,
     H-.7315785E-4, .1385716E+1,-.2411789E+0,-.7403991E-2, .2715513E-1,
     I-.8068998E-2, .7467210E-1,-.2263752E+1, .4163469E-4, .9148016E-5,
     J .7552782E-1,-.4364474E-3, .4935954E-3,-.7837036E-2,-.1643844E-3,
     K-.5313780E-2, .2868564E-4,-.1810828E+3, .1136112E+4,-.1415626E+4,
     L-.2540406E-1,-.3354503E+1,-.9715013E-2, .9202192E-4,-.7580452E+1,
     M-.7241050E-2, .1560430E+1, .2163080E-2,-.2943305E-1,-.2664132E+2,
     N .3334467E+2,-.4484441E-1, .1021904E+2,-.1022645E-2, .1614939E-2,
     O-.1983720E+2,-.7248729E-4, .2943276E-2,-.9322744E-3, .2136197E-1,
     P .5946692E-4,-.2623588E-5, .6422937E-3, .7898051E-4,-.4097134E-3,
     Q .4658792E-6,-.6674667E-5,-.9276444E-5,-.3350714E-3, .8076304E-4,
     R-.9702706E-2, .7907680E-2,-.1429927E-1,-.1911111E-4,-.2009685E-3/
C  24HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N24M/
     A         037,         022,         021,         053,         006,
     B         137,         163,         100,         136,         107,
     C         082,         057,         153,         077,         049,
     D         011,         066,         020,         044,         015,
     E         064,         139,         101,         110,         119,
     F         116,         150,         089,         161,         160,
     G         010,         016,         048,         051,         055,
     H         046,         068,         081,         111,         145,
     I         132,         148,         084,         130,         045,
     J         112,         071,         108,         018,         104,
     K         165,         131,         085,         079,         058,
     L         120,         113,         166,         117,         073,
     M         092,         158,         157,         125,         149,
     N         143,         114,         086,         032,         128,
     O         122,         133,         069,         062,         043,
     P         095,         054,         138,         070,         076,
     Q         031,         029,         041,         129,         106,
     R         052,         065,         074,         142,         109/
C
C  36HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R36M/
     A .5950992E+0, .5950849E+0, .1579387E-4, .1456014E-2, .3207405E-1,
     B-.7676163E-3,-.5470162E-2, .3885264E-4, .2219862E+2,-.5390780E-1,
     C-.1517608E-3,-.2491167E-2,-.1428840E-3, .4585012E-6,-.3401252E-4,
     D-.1972049E-4,-.5636768E-5,-.1414913E-4,-.1650207E-4, .2669300E-1,
     E-.3509095E-2,-.7492083E+1,-.1600104E-3, .1732787E-3,-.4668803E-1,
     F-.3349135E+4,-.2492286E+1, .5827907E-4,-.2699760E-5,-.4194588E+1,
     G .1183714E+0,-.6774910E+1, .2363143E+4,-.2766386E+3,-.4127603E-5,
     H-.6793531E-1, .6692806E-4, .2140080E-3,-.1051408E-3, .1574291E-1,
     I .1702305E-1, .3132313E+1,-.4267311E-3,-.1081547E-3, .9454913E-1,
     J .2723925E-4, .4721174E-4, .5315742E-5, .2633784E-2, .2876436E+1,
     K-.6931119E+2,-.1433271E-1,-.6981828E+2, .9248463E+2,-.1159544E-1,
     L-.1766660E-3, .8383029E-4, .1154778E+1,-.2878250E-3,-.4039820E-1,
     M .6119043E-1,-.5965958E+0,-.9011731E-4,-.2723274E-2, .1115074E-2,
     N .7571446E-4,-.1824643E-1, .1490073E-2,-.1465571E-4, .7776189E-2,
     O .1428073E+1,-.2494387E-2, .1327341E+2,-.5822539E-2, .3420847E-2,
     P-.4875488E-2,-.1737409E-3, .1659009E-1,-.2884431E-1, .3345077E-1,
     Q-.2379260E-3,-.2867373E+0, .1725656E-4, .3078079E-4,-.2416038E-3,
     R-.1258763E-3,-.1207252E-2, .1942326E-5, .8619620E-5,-.3816745E-4/
C
C  36HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N36M/
     A         037,         022,         021,         138,         089,
     B         129,         018,         048,         107,         110,
     C         139,         032,         136,         011,         044,
     D         016,         020,         051,         131,         137,
     E         163,         113,         057,         142,         120,
     F         058,         006,         100,         010,         084,
     G         148,         073,         079,         085,         031,
     H         114,         053,         055,         046,         043,
     I         101,         064,         071,         104,         112,
     J         045,         095,         049,         157,         158,
     K         149,         166,         122,         143,         165,
     L         133,         130,         068,         070,         125,
     M         145,         081,         116,         066,         015,
     N         117,         132,         108,         054,         069,
     O         082,         062,         086,         111,         077,
     P         052,         119,         065,         074,         128,
     Q         160,         150,         029,         153,         109,
     R         076,         092,         041,         106,         161/
C
C  48HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R48M/
     A .3937869E+1, .2704789E-2, .2041786E-4,-.5296992E-5, .3595185E-5,
     B-.1586901E+0,-.8895839E-2, .1017758E+1,-.1341447E-1, .4795113E+2,
     C .1117224E-3, .2237810E-5,-.4391966E-4,-.5562625E+3, .1197306E-1,
     D-.1089932E+0,-.6775073E+4, .4272758E+4,-.3806239E-1,-.3994735E-2,
     E-.4841974E-1,-.2401614E-3, .3658880E+1, .3839169E-4, .7278352E-4,
     F-.1407710E-4, .3700307E-6,-.1041093E-3,-.6224410E+0,-.2864941E-1,
     G .1032796E+0,-.1316307E-3, .2266372E-3,-.4527995E-6, .1751338E-2,
     H .6244212E-4, .8839133E-1,-.1296256E-2,-.4048634E-1,-.1973882E-3,
     I .2567629E-3, .4855618E-5,-.3332841E-3, .2033777E+0,-.6754591E-1,
     J-.1992392E-3,-.1316714E+2,-.7344471E-1, .3646203E-2,-.1834054E-5,
     K .1025236E-3,-.3341298E-4, .2875189E-1,-.5913152E-3,-.2675888E-5,
     L-.1456183E-3, .4367509E-1,-.3902138E+1, .6231806E-1,-.3691021E-2,
     M-.3008487E-3,-.3720047E-4, .9663910E+1,-.3045679E-2,-.1404164E+3,
     N .4988254E+1,-.2738102E-1,-.1190210E+3, .1629256E+3,-.1440433E-2,
     O .3320168E-2,-.2063279E-1, .3450813E-2, .2031545E-2, .1344573E+0,
     P-.5192478E-1, .1217591E+0,-.8695283E+1,-.4237666E+1, .6357585E-4,
     Q-.2035649E-1, .1203182E-1,-.2478962E-3,-.3098815E-2,-.9350809E-5,
     R .2607693E-4,-.2601418E-2, .1757823E-3, .1826342E-5,-.1595340E+0/
C
C  48HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N48M/
     A         037,         138,         021,         048,         041,
     B         022,         109,         082,         018,         107,
     C         095,         044,         131,         085,         111,
     D         120,         058,         079,         137,         163,
     E         125,         160,         064,         153,         100,
     F         051,         011,         136,         081,         101,
     G         128,         046,         142,         054,         077,
     H         117,         145,         070,         132,         057,
     I         055,         053,         104,         068,         110,
     J         116,         113,         114,         108,         010,
     K         130,         016,         065,         076,         031,
     L         139,         043,         006,         089,         032,
     M         161,         119,         086,         066,         122,
     N         158,         166,         149,         143,         129,
     O         157,         165,         092,         015,         148,
     P         074,         112,         073,         084,         029,
     Q         052,         069,         133,         062,         020,
     R         045,         071,         106,         049,         150/
C
C  60HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R60M/
     A .3203984E-2, .3214552E+1, .2423918E-4,-.7785958E+0,-.1492266E-1,
     B .1039869E+1,-.3005961E-1, .2310288E-3,-.2280654E+0, .5501085E+1,
     C .2990582E+0,-.9901556E-2,-.2098349E-1,-.1705836E-3,-.6350436E-3,
     D .7693167E-1, .5199465E-3, .6955174E-2, .8453595E-3, .1846887E-1,
     E-.5268668E-3,-.8680647E-1,-.5915611E+0,-.7375913E+0, .7631609E-4,
     F-.2451390E-2, .9023706E+2,-.1148612E+5,-.9789110E+3, .6385988E+4,
     G-.2257996E-2,-.2955700E-3, .3620264E-3, .1243156E+0, .2286977E-2,
     H-.2588321E-3,-.2050898E-4, .1036300E+0,-.3067020E-3,-.1872121E+2,
     I-.7393541E-1,-.1216293E+2, .2388042E-1,-.2839831E-4, .4525014E-4,
     J-.2995554E-4, .4003014E-6, .1001026E+0,-.5637052E-2,-.4621421E-4,
     K-.4773916E-4,-.9231204E-3,-.1052938E+0,-.4006194E-6,-.4930203E+1,
     L-.8322347E-1,-.1939114E-2,-.7524058E-4, .4381766E-2,-.6379662E-1,
     M .3660681E-1,-.1722834E-4, .5012191E-4, .9200552E-4, .1084389E-3,
     N-.4450581E-2, .3444209E-5, .9086277E-1,-.5094324E+1,-.2391547E-2,
     O-.1673092E+3, .2319061E+3,-.1755640E+3, .7775852E+1,-.5396487E-1,
     P-.1063858E-1,-.1351081E-3, .6457442E-2,-.2869241E-1, .1514071E+0,
     Q .2197347E-3,-.2746503E-2,-.3307905E-2,-.7339347E+0, .3619938E-4,
     R .1011086E-3,-.2434152E-4, .4017977E+1, .6680801E-6,-.1003097E-1/
C
C  60HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N60M/
     A         138,         037,         021,         022,         109,
     B         082,         018,         095,         120,         064,
     C         137,         163,         132,         046,         153,
     D         148,         160,         108,         106,         069,
     E         133,         125,         081,         068,         100,
     F         070,         107,         058,         085,         079,
     G         062,         057,         055,         043,         161,
     H         119,         051,         128,         116,         113,
     I         114,         073,         111,         054,         041,
     J         053,         011,         145,         077,         048,
     K         139,         104,         052,         010,         084,
     L         110,         129,         016,         015,         074,
     M         065,         020,         045,         130,         029,
     N         071,         049,         089,         006,         032,
     O         149,         143,         122,         158,         166,
     P         092,         136,         157,         165,         112,
     Q         117,         066,         076,         150,         044,
     R         142,         131,         086,         031,         101/
C
C  72HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R72M/
     A .3488563E-2, .3701970E+1,-.9708924E+0, .4008871E-2,-.1293923E-1,
     B-.7090221E-1,-.3742748E-3, .1105047E-1,-.4330272E-3,-.8182453E-1,
     C .1095407E-1, .5478795E+0,-.1447806E+0,-.9794039E-1, .2239485E+0,
     D-.1661157E-2, .4048455E-1,-.1006988E-2, .1850597E+0,-.2174177E+1,
     E-.8687648E-3,-.6220469E-2, .1288180E+3, .1852817E-2, .6048402E-1,
     F-.1280221E+4, .8505950E+4,-.1602371E+5,-.3252233E+0,-.1609533E-1,
     G .1029853E+2,-.3748759E-4, .9792199E-4, .4511779E-3,-.2162620E-3,
     H .2205770E-3,-.1151997E-1, .3387292E-4, .2349918E-1,-.2588824E+2,
     I-.8928016E-1, .6423026E-2,-.3158766E-6,-.5107375E-2, .5468760E-3,
     J .8253090E-2,-.2154140E+3, .2989108E+3,-.2354096E+3,-.3862253E-1,
     K-.2662852E-4, .1051974E+2,-.8225405E-1,-.3635149E-1,-.7247429E+1,
     L .3891779E-3,-.8137807E-5, .5224281E-4,-.2422649E-2,-.5477626E+0,
     M-.8151363E-4,-.7235619E-4,-.1810511E-3, .1377748E+1,-.3594793E-4,
     N-.2512651E-2, .4714961E-1,-.9353195E-1,-.2171966E+2, .7037701E-4,
     O .6227463E-6,-.9167926E+0,-.1582993E-3, .1218130E+0,-.1326393E-1,
     P .3112528E-4, .2236540E-3,-.4258522E-2, .7624116E-5, .3593528E-5,
     Q .7404723E-3,-.2894253E-1,-.4697331E-3, .1298922E+0,-.1438011E+1,
     R .8325552E-3,-.3026344E-5, .7633657E+0, .1031796E-2, .1344312E-4/
C
C  72HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N72M/
     A         138,         037,         022,         161,         109,
     B         074,         057,         108,         119,         125,
     C         101,         137,         148,         052,         128,
     D         153,         069,         133,         112,         082,
     E         104,         062,         107,         160,         145,
     F         085,         079,         058,         120,         132,
     G         064,         020,         045,         055,         046,
     H         095,         163,         021,         111,         113,
     I         114,         015,         041,         066,         142,
     J         157,         149,         143,         122,         092,
     K         130,         158,         166,         165,         006,
     L         117,         049,         100,         070,         081,
     M         053,         054,         136,         086,         016,
     N         129,         065,         110,         073,         044,
     O         011,         150,         131,         043,         077,
     P         029,         139,         076,         031,         010,
     Q         106,         018,         116,         089,         068,
     R         032,         051,         084,         071,         048/
C
C    12 THROUGH 72HR MERIDIONAL INTERCEPT VALUES
      DATA CNSTM/
     $-.17755E+3,-.30486E+3,-.73569E+1,0.99119E+3,0.22569E+4,0.33789E+4/
C
C  12HR ZONAL REGRESSION COEFFICIENTS
      DATA R12Z/
     A .9006323E+0, .2636530E+0, .2715837E-1,-.5035076E-5,-.4328413E-2,
     B-.1534302E+2,-.1670920E+2, .1099782E+2,-.5405415E-6,-.1375598E-4,
     C .2705107E-5,-.2260919E-5,-.3761767E-1,-.7464690E-3,-.1119880E+1,
     D-.3803272E-1, .1807599E-3, .2247620E+0,-.4954901E-3, .1190615E+0,
     E .4359363E-3,-.1709496E-5, .9452690E-6,-.4804899E-5, .1946948E-3,
     F-.1015711E-4, .9425162E-1, .4855394E-2, .5402028E-2, .4124690E-6,
     G-.8267158E-4, .3497515E-2,-.1692273E-2,-.3936120E-5, .2677127E-5,
     H .3451866E-1, .2196571E-4, .3035431E+0, .1088666E+3,-.4243606E-2,
     I .1757287E+0,-.2453161E-4, .2089448E-4, .1354813E-2, .6455932E-6,
     J-.2679381E-2,-.5688711E+0,-.1587587E+1, .3006070E-2,-.1166579E-4,
     K .1542880E-2,-.1347129E-2,-.2322664E-4, .3315306E-3, .8377724E-4,
     L .2618641E+0, .5893461E+0,-.5805363E+0,-.7381478E-4, .1035842E-1,
     M-.1843956E-4, .2631674E-4,-.1101112E-1,-.2608365E-6,-.8394727E-5,
     N-.4267192E-3, .2838702E-2,-.4894629E-5, .7210605E-3, .5548951E-3,
     O-.5022169E-1,-.5837255E+0, .3080611E-2, .3913114E-3,-.8009970E-3,
     P .2737874E-1,-.1580960E-5, .3713773E-5, .1506041E-2,-.1662541E-3,
     Q .2841699E-2, .4002706E-5, .1652561E+2,-.1215014E+0, .2955007E-3,
     R-.1946682E-2, .2823429E-4,-.2398549E-2,-.1147224E-4,-.3934242E-4,
     S-.5558193E-3, .1033347E-3, .2654649E-1,-.3655712E-4,-.0649221E-9/
C
C  12HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N12Z/
     A         022,         012,         006,         036,         110,
     B         122,         149,         143,         020,         048,
     C         034,         041,         128,         161,         084,
     D         148,         133,         083,         157,         150,
     E         025,         035,         021,         098,         070,
     F         103,         137,         047,         156,         031,
     G         126,         145,         028,         054,         045,
     H         146,         130,         158,         085,         166,
     I         164,         139,         131,         018,         042,
     J         125,         068,         107,         120,         046,
     K         032,         072,         106,         153,         142,
     L         073,         113,         037,         163,         112,
     M         057,         055,         074,         039,         117,
     N         155,         096,         116,         078,         069,
     O         080,         003,         108,         138,         159,
     P         123,         134,         016,         013,         129,
     Q         065,         088,         086,         114,         121,
     R         132,         104,         043,         095,         140,
     S         076,         109,         064,         165,         011/
C
C  24HR ZONAL REGRESSION COEFFICIENTS
      DATA R24Z/
     A .2211812E+1, .2502268E-2, .1611160E+0,-.2591848E+2, .1432364E-1,
     B-.9113922E-5, .6079792E-2,-.1401346E+1, .1332991E-4, .7052931E-2,
     C-.2593970E-3, .2451430E-5, .4769637E-2,-.4306809E-4, .3054334E-5,
     D .1000287E-1,-.5108636E+2,-.4080394E-3, .6407317E-3, .2993321E-5,
     E-.4237494E-4, .1457416E-4, .6738167E+0,-.2469574E-3,-.9215541E-5,
     F-.3256473E+1, .3334723E+0,-.1323649E-2, .1331422E+0, .2425374E-3,
     G-.1390987E-4,-.6551803E-3, .2598725E+1, .1060368E+1, .8170489E-4,
     H-.2564629E-5,-.1473495E-4,-.1176913E-1,-.3080450E-3, .3336047E-2,
     I .3844014E-3, .3177928E+0, .2574205E+3,-.5082541E-4,-.1202910E-3,
     J-.1963487E+1, .3509171E-2, .9577802E-5, .1449019E-4,-.5303399E+1,
     K .3860714E+2,-.1294830E-4, .2337055E+2,-.1995571E-2,-.1613782E-1,
     L-.1645496E+0, .4070771E-2, .4351837E-2,-.1486245E-2,-.2518986E-5,
     M .4734735E-6,-.1403628E-5,-.2059850E-4, .3792110E-3,-.1089386E-3,
     N .3298255E-1,-.8059559E-3,-.2020980E+0,-.2919412E-1, .9324504E-3,
     O .1088125E-4, .5408395E-1,-.4968320E-2,-.1688111E-2,-.2543072E-3,
     P .1081524E-3, .6010513E-6,-.6003507E-6,-.2923749E-4, .4013145E-4,
     Q .1901449E+0, .9298589E-3,-.2121820E+1, .1362282E+1,-.1177176E+0,
     R-.1236508E-2, .1540775E-1,-.2104262E-1, .1784882E-1,-.4841833E-2,
     S .6806184E-2, .5477094E+0,-.1416732E+0, .7317505E-1, .3173007E-6/
C
C  24HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N24Z/
     A         022,         013,         006,         122,         156,
     B         036,         065,         003,         045,         120,
     C         129,         021,         018,         095,         034,
     D         108,         149,         157,         032,         134,
     E         041,         048,         083,         072,         117,
     F         084,         137,         161,         146,         133,
     G         054,         165,         113,         158,         131,
     H         031,         098,         166,         109,         025,
     I         121,         164,         085,         139,         126,
     J         068,         069,         088,         130,         107,
     K         143,         116,         086,         159,         110,
     L         114,         096,         047,         028,         103,
     M         011,         020,         046,         142,         106,
     N         112,         163,         128,         074,         138,
     O         016,         123,         043,         070,         140,
     P         104,         042,         035,         057,         055,
     Q         073,         153,         037,         012,         148,
     R         155,         145,         125,         132,         076,
     S         078,         064,         080,         150,         039/
C
C  36HR ZONAL REGRESSION COEFFICIENTS
      DATA R36Z/
     A .3727141E+1,-.7587179E-3, .2658744E+0,-.1064598E-3, .1630746E-1,
     B .3809214E-2, .1670243E+1, .1278819E+0,-.2416541E+1, .1913527E-1,
     C .2704694E-5,-.1120205E-4,-.1614327E-2, .2591370E-3,-.1047507E+3,
     D .1332363E-2, .9398222E-6, .3414695E-5, .3046316E-2,-.2506951E-4,
     E-.4670072E+1, .2852724E+0,-.2901490E-2,-.5540189E-2, .3602891E-4,
     F .1995485E+1, .4871011E+3, .2478877E+0,-.1650441E-1, .5286175E-5,
     G-.2476632E-2, .5060762E-2,-.9612819E-4,-.1830817E+0,-.9639716E+1,
     H .5297878E-3, .3464923E-2,-.8071997E-4, .5602714E-4,-.2543369E-4,
     I .3584953E-3, .1382637E-2,-.5244200E+0,-.2599436E-4, .1835390E-4,
     J .6094095E-2, .6309593E-6,-.7754817E-5, .2240740E-4, .3052519E+2,
     K .3810123E-2,-.2447143E-2,-.3723550E+1, .1524773E+1, .4064334E-4,
     L .7461656E+2, .5375246E+1, .3403604E+0, .1128191E-3,-.4142378E-4,
     M-.1096141E-2,-.2166006E-4,-.3244383E-3,-.1244384E-2, .2974604E-1,
     N-.3203653E-1,-.3656643E-3, .3284611E-3,-.7873988E-4,-.1792683E-2,
     O .1730848E-1,-.5773084E-1, .2119286E-2, .2361585E-1,-.1913189E-5,
     P .1293529E-4,-.1816199E+0,-.8990942E+0, .8328797E-1, .4267458E-3,
     Q-.1628386E-3,-.1352078E-1, .2006030E-1, .2214782E+1, .5751397E-3,
     R-.1934013E+0,-.2339948E+1,-.2175043E-2,-.2371471E+1, .3393036E+1,
     S .6895464E-2,-.7135277E-3, .2778157E-6, .6514657E-3,-.3385307E-5/
C
C  36HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N36Z/
     A         022,         129,         006,         139,         065,
     B         013,         122,         156,         003,         108,
     C         021,         036,         043,         104,         149,
     D         157,         011,         035,         047,         117,
     E         084,         137,         161,         110,         130,
     F         158,         085,         146,         166,         103,
     G         070,         025,         057,         128,         107,
     H         109,         069,         041,         048,         098,
     I         121,         142,         150,         116,         088,
     J         018,         034,         031,         045,         086,
     K         096,         159,         068,         083,         134,
     L         143,         113,         164,         055,         046,
     M         163,         054,         106,         140,         132,
     N         125,         155,         131,         095,         072,
     O         145,         074,         138,         112,         020,
     P         016,         114,         080,         123,         133,
     Q         126,         076,         078,         012,         153,
     R         148,         037,         165,         064,         073,
     S         120,         028,         042,         032,         039/
C
C  48HR ZONAL REGRESSION COEFFICIENTS
      DATA R48Z/
     A .4461890E+1,-.1317868E-2,-.7756542E-1,-.2763940E+1, .1010894E+0,
     B .3552770E-3,-.1131051E-2,-.2969235E-5, .1778276E+1, .2697765E-1,
     C .1864808E-5, .3829534E-1, .2664764E+2,-.1670381E+3, .1257320E+3,
     D-.3611783E-4, .2327583E-1,-.4939107E-2, .1812029E+0, .3345573E+1,
     E .8995103E+1,-.1514329E+2,-.6056705E-4,-.7867934E-5, .8154577E-3,
     F .9369705E-4,-.5978556E+1,-.1621266E+0,-.3687867E-3,-.5121806E-2,
     G .1744368E-5,-.1546340E+1,-.6412392E-5, .1418515E-3,-.6517249E-4,
     H-.3501834E-1, .3596652E-1,-.3548717E+1,-.2720283E-3,-.1781469E-2,
     I .4078705E-3, .2880435E+0, .6823913E+3, .4768583E-1, .3167891E-2,
     J-.2810874E-3, .3799080E-5,-.4648817E-2, .6123276E-2,-.2612873E-4,
     K-.4936589E+1, .1889149E+1, .1788154E-4,-.1734991E-2,-.8497788E+1,
     L .5695087E-1, .2262154E-3, .2080020E-4, .7392030E-4,-.1816474E-1,
     M .4006617E-5, .6725874E+0,-.1372697E-3, .1686805E-3, .3139948E-2,
     N-.2296015E+0, .1188443E+2,-.1883356E-4,-.5851002E-5, .3567081E-1,
     O-.9073536E-3,-.1360315E-2,-.8653859E-1, .3236842E-2, .1021488E-4,
     P .6974207E-3, .3197120E-4,-.5162931E-5,-.9823154E-3,-.3572130E-1,
     Q-.1283591E+1, .3775808E+0, .3752357E+2, .3439863E-2,-.2016348E+0,
     R .6570792E-2, .1875953E-2, .2744629E-2, .6777080E-3,-.2940123E-4,
     S .7908021E-5,-.1325029E+0, .3122459E-6,-.2446544E-3,-.5342702E-4/
C
C  48HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N48Z/
     A         022,         129,         125,         080,         123,
     B         121,         109,         020,         012,         065,
     C         021,         110,         122,         149,         143,
     D         116,         043,         161,         128,         158,
     E         113,         107,         041,         036,         133,
     F         130,         084,         148,         106,         165,
     G         011,         037,         048,         104,         046,
     H         076,         108,         003,         126,         159,
     I         131,         146,         085,         078,         155,
     J         139,         042,         070,         025,         098,
     K         068,         083,         103,         153,         064,
     L         145,         120,         088,         134,         166,
     M         054,         006,         057,         055,         013,
     N         137,         073,         117,         031,         132,
     O         140,         072,         074,         138,         016,
     P         028,         039,         034,         163,         112,
     Q         150,         156,         086,         157,         114,
     R         096,         069,         047,         142,         095,
     S         045,         164,         035,         018,         032/
C
C  60HR ZONAL REGRESSION COEFFICIENTS
      DATA R60Z/
     A .2069224E+1,-.1103176E-2,-.2064642E+0,-.4983683E+1, .1536261E+0,
     B .3199196E+2,-.5460705E-2, .1255320E-5, .1520694E+0,-.6864076E+0,
     C-.2703545E-3,-.1377396E+2, .1772634E+1, .1634603E-2,-.2168856E+3,
     D .2124165E+3,-.5698305E+1, .1273810E+2,-.7063864E-2, .9227938E-2,
     E-.2284709E-2, .1370015E+2,-.2228472E+2, .6789817E+1,-.8620483E-2,
     F .1313456E-2, .5443990E-5,-.2303747E-2,-.3724907E-4, .7411583E-4,
     G .1284778E+0,-.1373733E-1, .2003673E-1, .1401725E+0, .2426811E+1,
     H-.8314399E-2, .3955336E-2, .1900598E-4, .5113706E-1,-.3800525E+1,
     I .6040041E+3,-.9981981E+1, .1325930E-3, .3052361E-5, .2668688E-3,
     J .2324372E-5, .7160340E-2, .1391306E-2,-.3548335E-4,-.1137031E-2,
     K-.6057272E-2,-.1427741E-1,-.9021798E-4,-.6861619E-3, .4349863E-4,
     L .2274543E-3,-.4777696E+1,-.5904185E-4,-.8227909E-1, .3152315E-1,
     M .2462513E-2, .5017710E+0,-.1096284E-1,-.1977392E-1, .7290724E-2,
     N-.2129486E-4, .3000092E+1,-.1765608E-4,-.2304361E+1, .6947934E+0,
     O .3114901E-1,-.3943682E+1, .4459878E-3,-.1227436E-3,-.6873362E-5,
     P .2243630E-4,-.1889643E+1, .5570258E-2,-.1523624E+0, .1353138E+0,
     Q .1710850E-2, .6295090E-3,-.8884525E-6, .3560092E-2,-.8806022E-4,
     R-.2366248E-3, .4754374E-2, .1822556E-4,-.1445557E-2, .2511212E-1,
     S .1707720E-5, .2121491E-3,-.2604274E-4,-.1148665E-5,-.7936591E-6/
C
C  60HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N60Z/
     A         022,         129,         125,         080,         123,
     B         086,         109,         020,         137,         148,
     C         057,         122,         083,         155,         149,
     D         143,         068,         073,         112,         163,
     E         159,         113,         107,         158,         013,
     F         142,         042,         070,         036,         134,
     G         132,         166,         096,         145,         006,
     H         072,         025,         034,         108,         003,
     I         085,         064,         039,         021,         055,
     J         054,         078,         018,         095,         140,
     K         120,         165,         046,         139,         103,
     L         130,         084,         116,         074,         065,
     M         138,         146,         161,         076,         069,
     N         016,         012,         098,         164,         156,
     O         043,         037,         131,         106,         031,
     P         041,         150,         157,         114,         128,
     Q         028,         133,         011,         032,         048,
     R         126,         047,         117,         153,         110,
     S         035,         121,         104,         088,         045/
C
C  72HR ZONAL REGRESSION COEFFICIENTS
      DATA R72Z/
     A .2395405E-1,-.7806209E-3,-.1842410E+0,-.8005585E+1, .1556506E+0,
     B-.6327140E+1, .2253897E+2, .6253895E-1,-.1755240E-1, .1005779E+0,
     C .3755404E-3, .2901980E-2, .3114197E+3,-.7669319E+2,-.2248932E+3,
     D .2924744E+3,-.2680036E+2, .1069149E+2, .1748429E+2,-.2428297E-1,
     E .2038599E+1, .1848174E-1, .3960758E-1,-.1984342E-4,-.2583482E-2,
     F .1510835E-1, .1105277E+1,-.1305345E+1, .4382738E-1,-.1063787E+1,
     G .8457217E-5,-.3720603E+1,-.3133037E+1, .7266772E-1,-.2743943E-3,
     H-.4373971E-2,-.2921431E-2,-.1547001E-4, .4130158E-2, .3275995E+1,
     I .3118712E-3,-.8542968E-1, .7297505E-2,-.1557678E-1,-.4920905E-4,
     J .3283889E+1, .1532788E+0,-.6655574E+1,-.1290537E-1, .6191022E+0,
     K-.3637749E+1,-.3909813E-3,-.1151147E-3, .1544773E-1,-.7489980E-3,
     L-.2239653E-3, .1315061E-2,-.2339805E-1,-.2173305E-1,-.1989875E-3,
     M .8305500E-1,-.1606589E-1,-.7300878E-1,-.6183341E-4,-.8706669E-3,
     N .9752020E-4, .3106925E-3, .2559696E-4, .6615661E-2, .1022580E-2,
     O-.2911379E-2, .8294057E-2, .3898194E-4,-.2959543E-4,-.5492775E-4,
     P-.3474458E+1,-.2484927E-4, .3654421E-4, .9827073E+0,-.2147585E+1,
     Q-.1078548E+0, .7978876E-3, .8899623E-4,-.3249739E-1, .5067226E-4,
     R-.2651358E-2,-.7893836E-6, .2138504E-5, .1093593E-4,-.8047551E-3,
     S-.1532810E-5, .4060731E-2, .1511806E-3,-.1593887E-3, .2311149E-6/
C
C  72HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N72Z/
     A         096,         129,         125,         080,         123,
     B         037,         086,         022,         120,         112,
     C         055,         142,         085,         122,         149,
     D         143,         107,         158,         113,         165,
     E         083,         166,         132,         020,         155,
     F         163,         137,         073,         065,         148,
     G         042,         068,         003,         108,         106,
     H         072,         032,         054,         028,         012,
     I         039,         074,         047,         161,         036,
     J         006,         145,         164,         109,         146,
     K         064,         057,         046,         069,         126,
     L         048,         133,         013,         018,         104,
     M         043,         076,         128,         088,         139,
     N         041,         130,         034,         157,         131,
     O         140,         025,         045,         016,         116,
     P         084,         098,         103,         156,         150,
     Q         114,         138,         117,         110,         095,
     R         070,         011,         035,         134,         159,
     S         031,         078,         121,         153,         021/
C
C    12 THROUGH 72HR ZONAL INTERCEPT VALUES
      DATA CNSTZ/
     $-.67623E+3,-.91219E+3,-.13468E+4,-.16390E+4,-.96035E+3,-.13693E+2/
      END
      SUBROUTINE STHGPR (XLATH, XLONH, BEAR, GRIDSZ, XI, YJ)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            STHGPR
C
C  DESCRIPTION:
C
C      PART OF PROGRAM MODULE WHICH COMPUTES ALONG AND ACROSS TRACK GRID
C      POINT LOCATIONS RELATIVE TO THE CURRENT POSITION AND HEADING OF A
C      TROPICAL CYCLONE OR VICE VERSA.  THIS PROGRAM INITIALIZE SUBPRO-
C      GRAMS XY2LLH AND LL2XYH AND MUST BE CALLED EVERY TIME LOCATION OR
C      HEADING OF STORM CHANGES.  STHGPR INITIALIZATION IS PROVIDED BY
C      BLOCK DATA SUBROUTINE BLKDT2.
C
C  ORIGINAL PROGRAMMER, DATE:   ALBION D. TAYLOR, NOAA, MARCH, 1982
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL STHGPR(XLATH,XLONH,BEAR,GRIDSZ,XI,
C                               YJ)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS: /HGRPRM/
C
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      XLATH  =      (REAL) STORM LATITUDE WHERE DEGREES NORTH ARE
C                    ENTERED AS POSITIVE VALUES AND DEGREES SOUTH ARE
C                    ENTERED  AS NEGATIVE VALUES.
C
C      XLONH  =      (REAL) STORM LONGITUDE WHERE DEGREES WEST ARE
C                    ENTERED AS POSITIVE VALUES 0 TO 180 AND DEGREES
C                    EAST ARE ENTERED AS NEGATIVE VALUES, 0 TO 180.
C
C      BEAR   =      (REAL) CURRENT HEADING OF THE STORM.
C
C      GRIDSZ =      (REAL) ORTHOGONAL DISTANCE BETWEEN GRID POINTS.
C
C      XI     =      (REAL) POSITION OF STORM IN GRID-POINT INTERVALS
C                    IN THE ACROSS TRACK SENSE (I-VALUES)
C
C      YJ     =      (REAL) POSITION OF STORM IN GRID-POINT INTERVALS
C                    IN THE ALONG-TRACK SENSE (J-VALUES)
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENTS):
C
C     NONE
C
C  METHOD
C
C      1.  STORM POSITION IS TAKEN AS I=0,J=0 (XI=0.,YJ=0.) IN GRID
C
C      2.  THIS MODULE INCLUDES SUBPROGRAM BLKDT2 WHEREIN A COMPLETE
C          DESCRIPTION OF THE NAVIGATIONAL METHODOLOGY IS GIVEN.  MODULE
C          ALSO INCLUDES SUBPROGRAMS XY2LLH AND LL2XYH.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON /HGRPRM/A(3,3), RADPDG, RRTHNM, DGRIDH, HGRIDX, HGRIDY
C
      CLAT = COS(RADPDG*XLATH)
      SLAT = SIN(RADPDG*XLATH)
      SLON = SIN(RADPDG*XLONH)
      CLON = COS(RADPDG*XLONH)
      SBEAR = SIN(RADPDG*BEAR)
      CBEAR = COS(RADPDG*BEAR)
      A(1, 1) = CLAT*SLON
      A(1, 2) = CLAT*CLON
      A(1, 3) = SLAT
      A(2, 1) =  - CLON*CBEAR + SLAT*SLON*SBEAR
      A(2, 2) = SLON*CBEAR + SLAT*CLON*SBEAR
      A(2, 3) =  - CLAT*SBEAR
      A(3, 1) =  - CLON*SBEAR - SLAT*SLON*CBEAR
      A(3, 2) = SLON*SBEAR - SLAT*CLON*CBEAR
      A(3, 3) = CLAT*CBEAR
      DGRIDH = GRIDSZ
      HGRIDX = XI
      HGRIDY = YJ
      RETURN
      END
      SUBROUTINE LL2XYH (XLAT, XLONG, XI, YJ)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            LL2XYH
C
C  DESCRIPTION:
C
C      GIVEN STORM POSITION, RETURNS FLOATING POINT GRID OFFSET VALUES
C      XI0 AND YJ0.
C
C
C  ORIGINAL PROGRAMMER, DATE:   ALBION D. TAYLOR, NOAA, MARCH, 1982
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL LL2XYH(XLAT,XLONG,XI0,YJ0)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS: /HGRPRM/
C
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      XLAT  =       (REAL) STORM LATITUDE WHERE NORTH/SOUTH ARE
C                    ENTERED AS (+/-) O TO 90.
C
C      XLONG  =      (REAL) STORM LONGITUDE WHERE DEGREES (WEST/EAST)
C                    ARE ENTERED AS (+/-) 0 TO 180.
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENTS)
C
C      XI     =      (REAL)  FLOATING POINT STORM POSITION GRID-POINT
C                    INTERVALS IN THE ACROSS TRACK SENSE (I-VALUES).
C
C      YJ     =      (REAL)  FLOATING POINT STORM POSITION GRID-POINT
C                    INTERVALS IN THE ALONG-TRACK SENSE (J-VALUES).
C
C  METHOD:
C
C      1.  BEFORE CALLING THIS ROUTINE, MODULE MUST BE INITIALIZED BY
C          CALLING SUBROUTINE STHGPR.
C
C      2.  IN JTWC92 USAGE, VALUES OF XI0 AND YJ0, IN SUBROUTINE STHGPR,
C          ARE BOTH SET TO 0.0.
C
C      3.  MODULE INCLUDES BLKDT2, STHGPR, LL2XYH AND XY2LLH
C
C      4.  LL2XYH IS THE INVERSE OF XY2LLH.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON /HGRPRM/A(3,3), RADPDG, RRTHNM, DGRIDH, HGRIDX, HGRIDY
      DIMENSION ZETA(3), ETA(3)
      CLAT = COS(RADPDG*XLAT)
      SLAT = SIN(RADPDG*XLAT)
      SLON = SIN(RADPDG*XLONG)
      CLON = COS(RADPDG*XLONG)
      ZETA(1) = CLAT*SLON
      ZETA(2) = CLAT*CLON
      ZETA(3) = SLAT
      DO 20 I = 1, 3
         ETA(I) = 0.
         DO 10 J = 1, 3
            ETA(I) = ETA(I) + A(I, J)*ZETA(J)
   10    CONTINUE
   20 CONTINUE
      R = SQRT(ETA(1)*ETA(1) + ETA(3)*ETA(3))
      XI = HGRIDX + RRTHNM*ATAN2(ETA(2), R)/DGRIDH
      IF ( R .LE. 0. ) THEN
         YJ = 0.
      ELSE
         YJ = HGRIDY + RRTHNM*ATAN2(ETA(3), ETA(1))/DGRIDH
      ENDIF
      RETURN
      END
      SUBROUTINE XY2LLH (XI, YJ, XLAT, XLONG)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            XY2LLH
C
C  DESCRIPTION:
C
C      GIVEN STORM POSITION IN LAT/LON, RETURNS FLOATING POINT GRID
C      OFFSETS XI0 AND YJ0.
C
C  ORIGINAL PROGRAMMER, DATE:   ALBION D. TAYLOR, NOAA, MARCH, 1982
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL XY2LLH(XI0,YJ0,XLAT,XLONG)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS: /HGRPRM/
C
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      XI     =      (REAL) STORM POSITION IN FLOATING-POINT GRID
C                    INTERVALS IN ACROSS TRACK SENSE (I).
C
C      YJ     =      (REAL) STORM POSITION IN FLOATING-POINT GRID
C                    INTERVALS IN ALONG-TRACK SENSE (J).
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENTS):
C
C      XLAT  =       (REAL) STORM LATITUDE WHERE NORTH/SOUTH IS (+/-).
C
C      XLONG  =      (REAL) STORM LONGITUDE WHERE WEST/EAST IS (+/-).
C
C  METHOD:
C
C      1.  BEFORE CALLING THIS ROUTINE, MODULE MUST BE INITIALIZED BY
C          CALLING SUBROUTINE STHGPR.
C
C      2.  IN JTWC92 USAGE, VALUES OF XI0 AND YJ0, IN SUBROUTINE STHGPR,
C          ARE BOTH SET TO 0.0.
C
C      3.  MODULE INCLUDES BLKDT2, STHGPR, LL2XYH AND XY2LLH
C
C      4.  XY2LLH IS THE INVERSE OF LL2XYH.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON /HGRPRM/A(3,3), RADPDG, RRTHNM, DGRIDH, HGRIDX, HGRIDY
      DIMENSION ZETA(3), ETA(3)
      CXI = COS(DGRIDH*(XI - HGRIDX)/RRTHNM)
      SXI = SIN(DGRIDH*(XI - HGRIDX)/RRTHNM)
      SYJ = SIN(DGRIDH*(YJ - HGRIDY)/RRTHNM)
      CYJ = COS(DGRIDH*(YJ - HGRIDY)/RRTHNM)
      ETA(1) = CXI*CYJ
      ETA(2) = SXI
      ETA(3) = CXI*SYJ
      DO 20 I = 1, 3
         ZETA(I) = 0.
         DO 10 J = 1, 3
            ZETA(I) = ZETA(I) + A(J, I)*ETA(J)
   10    CONTINUE
   20 CONTINUE
      R = SQRT(ZETA(1)*ZETA(1) + ZETA(2)*ZETA(2))
      XLAT = ATAN2(ZETA(3), R)/RADPDG
      IF ( R .LE. 0. ) THEN
         XLONG = 0.
      ELSE
         XLONG = ATAN2(ZETA(1), ZETA(2))/RADPDG
      ENDIF
      RETURN
      END
      SUBROUTINE LL2DB (XLATO, XLONO, XLATT, XLONT, DIST, BEAR)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            LL2DB
C
C  DESCRIPTION:
C
C      GIVEN A LATITUDE/LONGITUDE OF A POINT ON THE EARTH AND THE
C      LATITUDE/LONGITUDE OF ANOTHER (TARGET) POINT, RETURNS THE
C      DISTANCE AND BEARING TO THAT OTHER POINT.
C
C  ORIGINAL PROGRAMMER, DATE:   ALBION D. TAYLOR, NOAA, MARCH, 1982
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL LL2DB(XLATO,XLONO,XLATT,XLONT,DIST,
C                              BEAR)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      NONE
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      XLATO  =      (REAL) LATITUDE OF STORM. (NORTH/SOUTH) IS (+/-).
C
C      XLONO =       (REAL) LONGITUDE OF STORM. (WEST/EAST) IS (+/-).
C
C      XLATT =       (REAL) STORM LATITUDE WITH ALGEBRAIC SIGN
C                    CONVENTION SAME AS WITH XLATO.
C
C      XLONT =       (REAL) STORM LONGITUDE WITH ALGEBRAIC SIGN
C                             CONVENTION SAME AS WITH XLONO.
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENTS):
C
C      DIST  =       (REAL) DISTANCE TO TARGET POINT IN NMI.
C
C      BEAR  =       (REAL) BEARING (DEGREES CLOCKWISE FROM NORTH) TO
C                    TARGET POINT.
C
C  METHOD:
C
C      1.  SEE PROGRAM FOR ADDITIONAL COMMENTS ABOUT METHODOLOGY.
C
C      2.  RADIUS OF EARTH (2440.17 NMI) AND NUMBER OF RADIANS PER
C          DEGREE OF ARC (0.017453293) ARE SPECIFIED IN DATA STATEMENT.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      COMMON /HGRPRM/A(3,3), RADPDG, RRTHNM, DGRIDH, HGRIDX, HGRIDY
C
CCC   DATA RRTHNM/3440.17/, RADPDG/1.7453293E-2/
C     RRTHNM=RADIUS OF EARTH IN NAUT. MILES, RADPDG==OF RADIANS
C     PER DEGREE
      CLATO = COS(RADPDG*XLATO)
      SLATO = SIN(RADPDG*XLATO)
      CLATT = COS(RADPDG*XLATT)
      SLATT = SIN(RADPDG*XLATT)
      CDLON = COS(RADPDG*(XLONT - XLONO))
      SDLON = SIN(RADPDG*(XLONT - XLONO))
      Z = SLATT*SLATO + CLATT*CLATO*CDLON
      Y =  - CLATT*SDLON
      X = CLATO*SLATT - SLATO*CLATT*CDLON
      R = SQRT(X*X + Y*Y)
      DIST = RRTHNM*ATAN2(R, Z)
      IF ( R .LE. 0. ) THEN
         BEAR = 0.
      ELSE
         BEAR = ATAN2( - Y,  - X)/RADPDG + 180.
      ENDIF
      RETURN
      END
      FUNCTION LZONE (AHP12H, SLAT00)
C.........................START PROLOGUE................................
C
C  FUNCTION NAME:            INTEGER FUNCTION LZONE
C
C  DESCRIPTION:
C
C      DETERMINES STRATIFICATION ZONE
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    I=LZONE(AHP12H,SLAT00)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C.........................MAINTENANCE SECTION..........................
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C      AHP12H   =    (REAL) HEADING OF STORM BASED ON INITIAL POSITION
C                    AND POSITION 12H EARLIER.
C
C      SLAT00   =    (REAL) INITIAL STORM LATITUDE IN DEGREES NORTH
C
C  PRINCIPAL VARIABLE (RETURNED FUNCTION):
C
C      LZONE    =    (INTEGER) STRATIFICATION ZONE 1, 2 OR 3
C
C  METHOD:
C
C        LZONE = 1 (SOUTH ZONE) IF:
C          STORMS INITIALLY GE 12N AND LT 22N AND HEADING GE 210 AND
C          LE 330 DEGS.
C
C        LZONE = 2 (NORTH ZONE) IF:
C          STORMS INITIALLY GE 22N;
C          STORMS LT 22N AND GE 15N AND HEADING GT 330 AND LT 210 DEGS.
C
C        LZONE = 3  (EQUATORIAL ZONE) IF:
C          STORMS INITIALLY LT 12N;
C          STORMS GE 12N AND LT 15N AND HEADING GT 330 AND LT 210 DEGS.
C
C  LANGUAGE:                       FORTRAN 77
C
C
C
C  RECORD OF CHANGES:
C
C.........................END PROLOGUE..................................
C
      LOGICAL TOWEST, LAINCL
C
      IF ( AHP12H .GT. -.000001 .AND. AHP12H .LT. 0.000001 ) AHP12H =
     * 360.
      TOWEST = AHP12H .LE. 330. .AND. AHP12H .GE. 210.
      LAINCL = SLAT00 .LT. 15 .AND. SLAT00 .GE. 12.0
C
C     IS STORM IN ZONE 3?????
      IF ( SLAT00 .LT. 12.0 .OR. (LAINCL .AND. .NOT. TOWEST) ) THEN
         LZONE = 3
C
C     IS STORM IN ZONE 1 OR ZONE 2?????
      ELSE IF ( SLAT00 .LT. 22.0 .AND. TOWEST ) THEN
         LZONE = 1
      ELSE
         LZONE = 2
      ENDIF
      END
      SUBROUTINE GET (CLAT, CLON, FLD, DI, XXFI, XXFJ)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            GET
C
C  DESCRIPTION:
C
C      GIVEN A LATITUDE/LONGITUDE OF A POINT ON A POLAR STEREOGRAPHIC
C      PROJECTION, WITH FIELD VALUES DEFINED ON A 65 X 65 GRID, RETURNS
C      FIELD VALUE AT THE GIVEN POINT ALONG WITH FLOATING POINT GRID
C      LOCATION XXFI AND XXFJ OF THE POINT.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL GET(CLAT,CLON,FLD,DI,XXFI,XXFJ)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      NONE
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      CLAT   =      (REAL) LATITUDE OF POINT (+/- FOR NORTH/SOUTH)
C
C      CLON   =      (REAL) LONGITUDE OF STORM.  (+/- FOR WEST/EAST)
C
C      FLD    =      (REAL) ARRAY ((FLD(I,J),J=1,65),I=1,65) OR
C                    (FLD(K),K=1,4225) GIVING VALUES OF A FIELD AT EACH
C                    OF 4225 GRID POINTS.
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENTS):
C
C      DI    =       VALUE OF FIELD AT INCOMING LATITUDE/LONGITUDE
C
C      XXFI  =       (REAL) FLOATING-POINT VALUE OF GRID POINT NUMBER
C                    IN THE I-DIRECTION.
C
C      XXFJ  =       (REAL) FLOATING-POINT VALUE OF GRID POINT NUMBER
C                    IN THE J-DIRECTION.
C  METHOD:
C
C      1.  BI-QUADRATIC INTERPOLATION APPLICABLE TO A (65 X 65) POLAR
C          STEREOGRAPHIC PROJECTION WITH POLE POSITION AT I=33, J=33.
C          POSITION (I=1,J=1) IS AT LOWER LEFT HAND CORNER OF GRID WITH
C          A LATITUDE NEAR 20.9S AND A LONGITUDE OF 125W.
C
C      2. GRID SPACING IS 381 KM AT 60N.
C
C      3. EXPANDED VERSION OF STANDARD FNOC 63 X 63 GRID.
C
C      4. VALUES OF XXFI AND/OR XXFJ .LT. 1.0 ARE SET EQUAL TO 1.0
C         VALUES OF XXFI AND/OR XXFJ .GT. 65.0 ARE SET EQUAL TO 65.0
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      DIMENSION FLD(65, 65), ERAS(4)
C
      COMMON /HGRPRM/A(3,3), RADPDG, RRTHNM, DGRIDH, HGRIDX, HGRIDY
C
      EQUIVALENCE (RADPDG,T)
C
C     PROGRAM RETURNS INTERPOLATED VALUE FROM 65 X 65 POLAR
C     STEREOGRAPHIC GRID AT POINT CLAT, CLON.
C
      XXLAT = T*CLAT
      XXCLAT = COS(XXLAT)
      XXSLAT = SIN(XXLAT)
      XXLON =  - T*(CLON + 10.0)
      XXCLON = COS(XXLON)
      XXSLON = SIN(XXLON)
      XXFI = 31.18*XXCLON*XXCLAT/(XXSLAT + 1.) + 33.
      XXFJ = 31.18*XXSLON*XXCLAT/(XXSLAT + 1.) + 33.
      IF ( XXFI .LT. 1.0 ) XXFI = 1.0
      IF ( XXFJ .LT. 1.0 ) XXFJ = 1.0
      IF ( XXFI .GT. 65.0 ) XXFI = 65.0
      IF ( XXFJ .GT. 65.0 ) XXFJ = 65.0
      KQUAD = 6
      IF ( XXFI .LE. 3.0 .OR. XXFI .GE. 63.0 ) KQUAD = 5
      IF ( XXFJ .LE. 3.0 .OR. XXFJ .GE. 63.0 ) KQUAD = 5
      I = XXFI
      J = XXFJ
      XDELI = XXFI - FLOAT(I)
      XDELJ = XXFJ - FLOAT(J)
      IF ( KQUAD .EQ. 6 ) THEN
         XI2TM = 0.25*XDELI*(XDELI - 1.0)
         XJ2TM = 0.25*XDELJ*(XDELJ - 1.0)
         JJ = J - 1
         DO 10 K = 1, 4
            ERAS(K) = FLD(I, JJ) + XDELI*(FLD(I + 1, JJ) - FLD(I, JJ))
     *       + XI2TM*(FLD(I + 2, JJ) + FLD(I - 1, JJ) - FLD(I, JJ) -
     *       FLD(I + 1, JJ))
            JJ = JJ + 1
   10    CONTINUE
         DI = ERAS(2) + XDELJ*(ERAS(3) - ERAS(2)) + XJ2TM*(ERAS(1) -
     *    ERAS(2) - ERAS(3) + ERAS(4))
      ELSE
         IP1 = I+1
         JP1 = J+1
         IF ( IP1 .GT. 65 ) IP1 = 65
         IF (JP1 .GT. 65 ) JP1 = 65
         ERAS(1) = FLD(I, J)
         ERAS(4) = FLD(I, JP1)
         ERAS(2) = ERAS(1) + XDELI*(FLD(IP1, J) - ERAS(1))
         ERAS(3) = ERAS(4) + XDELI*(FLD(IP1, JP1) - ERAS(4))
         DI = ERAS(2) + XDELJ*(ERAS(3) - ERAS(2))
      ENDIF
      RETURN
      END
      SUBROUTINE ANLS (LZ)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            ANLS
C
C  DESCRIPTION:
C
C      PROGRAM MODULE FOR COMPUTING TROPICAL CYCLONE DISPLACEMENTS BASED
C      ON THE INITIAL DEEP-LAYER-MEAN GEOPOTENTIAL HEIGHT ANALYSIS.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL ANLS(LZ)
C
C  INPUT FILES:
C
C      FIRST RECORD (INITIAL ANALYSIS) FROM FILE 3 CONTAINING DEEP-
C      LAYER-MEAN GEOPOTENTIAL HEIGHT DEPARTURES FROM NORMAL IN 65 X 65
C      GRID FORMAT. VALUES ARE READ INTO ARRAY Z(4225)
C
C  COMMON BLOCKS:
C
C      /BLK03/,/BLK04/,/BLK05/,/BLK10/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS)
C
C      LZ     =      (INTEGER) INDEX FOR STRATIFICATION ZONE WHERE:
C                    1 = SOUTH ZONE
C                    2 = NORTH ZONE
C                    3 = EQUATORIAL ZONE
C
C  PRINCIPAL VARIABLES (OUTGOING IN COMMON BLOCK /BLKO6/)
C
C       ADISP     =  (REAL) (ADISP(J),J=1,12) ARRAY GIVING FORECAST
C                    DISPLACEMENTS IN NAUTICAL MILES WHERE J = 1, 3, 5,
C                    7, 9, 11 REFER TO ALONG TRACK (OR MERIDIONAL) AND
C                    J = 2, 4, 6, 8, 10 AND 12 REFER TO ACROSS TRACK (OR
C                    ZONAL) MOTION FOR 12 THROUGH 72H.
C
C  OTHER IMPORTANT VARIABLES:
C
C       C        =   (REAL) (((C(I,J,K),K=1,6),J=1,12,),I=1,21) ARRAY
C                    CONTAINING ALL REGRESSION COEFFICIENTS AND OTHER
C                    CONSTANTS UTILIZED IN PREDICTING MOTION FROM ANALY-
C                    SIS FIELDS ALONE AND FROM PERFECT-PROG FIELDS
C                    ALONE.  DATA ARE ENTERED IN BLOCK DATA SUBPROGRAM
C                    BLKDT5.  SUBSCRIPT ADDRESS INDEXING IS AS FOLLOWS:
C
C       I        =   INDEX FOR SPECIFYING TYPE OF CONSTANT FOR GIVEN
C                    PREDICTOR NUMBER-SEE SUBPROGRAM BLKDT5 FOR DETAILS.
C
C       J        =   INDEX WHICH SPECIFIES ALONG OR ACROSS TRACK (OR
C                    MERIDIONAL/ZONAL) COMPONENT OF MOTION AND FORECAST
C                    INTERVAL, 12 THROUGH 72H.  SEE BLOCK DATA SUBPRO-
C                    GRAM BLKDT5 FOR DETAILS.
C
C       K        =   INDEX WHICH FURTHER SPECIFIES STRATIFICATION
C                    ZONE NUMBER 1, 2 OR 3 AND WHETHER ANALYSIS OR PER-
C                    FECT PROG MODE.  SEE BLOCK DATA SUBPROGRAM BLKDT5
C                    FOR DETAILS.
C
C       NP       =   (INTEGER) NUMBER OF GEOPOTENTIAL HEIGHT PREDIC-
C                    TORS (EXCLUDING INTERCEPT VALUE) FOR THIS K-INDEX.
C                    MAXIMUM NUMBER OF PREDICTORS FOR ANY GIVEN TIME
C                    INTERVAL IS 4.  UNUSED CONSTANTS WERE ENTERED IN
C                    ARRAY C(I,J,K) AS MISSING, USING LARGE NUMBER
C                    9999999E+25.
C
C       XI       =   (REAL) NUMBER OF 150 NMI GRID POINT INTERVALS IN
C                    THE I-DIRECTION (ACROSS TRACK MOTION FOR ZONES 1
C                    AND 2; ZONAL MOTION FOR ZONE 3).
C
C       YJ       =   (REAL) NUMBER OF 150 NMI GRID POINT INTERVALS IN
C                    THE J-DIRECTION (ALONG TRACK MOTION FOR ZONES 1
C                    AND 2; MERIDIONAL MOTION FOR ZONE 3)
C
C       QLAT     =   (REAL) LATITUDE (0 TO 90; +/- FOR NORTH/SOUTH) OF
C                    TRANSLATED AND ROTATED GRID POINT
C
C       QLON     =   (REAL) LONGITUDE (0 TO 180; +/- FOR WEST/EAST) OF
C                    TRANSLATED AND ROTATED GRID POINT.
C
C  VARIABLES SAVED IN COMMON BLOCK /BLK10/ FOR LATER USE:
C
C     HTSAVE(4,12) = (REAL) HEIGHT VALUES.
C
C     GP(4,12,2)   = (REAL) GRID POINT LATITUDES AND LONGITUDES.
C
C     LSAVE(12)    = (INTEGER) NUMBER OF PREDICTORS FOR GIVEN FORECAST.
C
C  METHOD:
C
C      1.  READ IN HEIGHT VALUES ON LARGE POLAR STEREOGRAPHIC 65X65 GRID
C
C      2.  DETERMINE LAT/LON (QLAT,QLON) OF TRANSLATED AND ROTATED POINT
C          ON ABOVE GRID USING NAVIGATIONAL MODULE BLKDT2.
C
C      3.  FIND (USING SUBROUTINE GET) HEIGHT VALUE AT POINT QLAT,QLON
C          ON LARGE 65 X 65 GRID.
C
C      4.  DETERMINE CORRECT INDEXING IN ARRAY C(I,J,K) WHICH CONTAINS
C          REGRESSION COEFFICIENTS AND OTHER DATA.
C
C      5.  COMBINE HEIGHT VALUES (DEPARTURES FROM NORMAL) AND REGRESSION
C          COEFFICIENTS INTO FORECAST DISPLACEMENTS (ADISP).
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      COMMON/BLK03/
     A          AA12S(21),AX12S(21),AA24S(21),AX24S(21),
     B          AA36S(21),AX36S(21),AA48S(21),AX48S(21),
     C          AA60S(21),AX60S(21),AA72S(21),AX72S(21),
     D          PA12S(21),PX12S(21),PA24S(21),PX24S(21),
     E          PA36S(21),PX36S(21),PA48S(21),PX48S(21),
     F          PA60S(21),PX60S(21),PA72S(21),PX72S(21),
C
     G          AA12N(21),AX12N(21),AA24N(21),AX24N(21),
     H          AA36N(21),AX36N(21),AA48N(21),AX48N(21),
     I          AA60N(21),AX60N(21),AA72N(21),AX72N(21),
     J          PA12N(21),PX12N(21),PA24N(21),PX24N(21),
     K          PA36N(21),PX36N(21),PA48N(21),PX48N(21),
     L          PA60N(21),PX60N(21),PA72N(21),PX72N(21),
C
     M          AM12E(21),AZ12E(21),AM24E(21),AZ24E(21),
     N          AM36E(21),AZ36E(21),AM48E(21),AZ48E(21),
     O          AM60E(21),AZ60E(21),AM72E(21),AZ72E(21),
     P          PM12E(21),PZ12E(21),PM24E(21),PZ24E(21),
     Q          PM36E(21),PZ36E(21),PM48E(21),PZ48E(21),
     R          PM60E(21),PZ60E(21),PM72E(21),PZ72E(21)
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
      COMMON /BLK10/HTSAVE(4,12), GP(4,12,2), LSAVE(12)
C
      INTEGER LSAVE
      DIMENSION C(21,12,6)
      EQUIVALENCE (C(1,1,1),AA12S(1))
C
      DATA BIG/1.0E20/, GSIZE/150./
C     INITIALIZE AL TAYLOR ROUTINE
      CALL STHGPR(SLAT00, -SLON00, GRDROT, GSIZE, 0., 0.)
C     GET DEEP LAYER HEIGHT FIELD IN 65X65 FORMAT
      REWIND (92)
      READ (92) HTS
cx
cx  check height values against PEPS heights
cx
cx    call openfile (69,'jtwc92.hts','unknown',ioerror)
cx    do 999 j=4161,1,-65
cx        write (69,'(1x,65i6)')(nint(hts(ii)),ii=j,j+64)
cx999 continue
cx    close (69)

      K = 2*LZ - 1
C
C     DESCRIPTION OF K...
C     K=1      SOUTH ZONE ANALYSIS MODE  K=2 SOUTH ZONE PERFECT-PROG MOD
C     K=3      NORTH ZONE ANALYSIS MODE  K=4 NORTH ZONE PERFECT-PROG MOD
C     K=5 EQUATORIAL ZONE ANALYSIS MODE  K=6 EQTRL ZONE PERFECT-PROG MOD
C
      DO 20 J = 1, 12
         NP = 4
C        NP GIVES NUMBER OF HEIGHT PREDICTORS EXCLUDING INTERCEPT
         IF ( C(21, J, K) .GT. BIG ) NP = 3
         IF ( C(16, J, K) .GT. BIG ) NP = 2
         LSAVE(J) = NP
C        INITIALIZE DISPLACEMENT WITH INTERCEPT VALUE
         ADISP(J) = C(5*NP + 1, J, K)
C        NOW, LOOP THRU EACH OF THE NP PREDICTORS, FIND LOCATION AND
C        VALUE OF EACH PREDICTOR ON 65X65 GRID ACCORDING TO XI, YJ
C        (RELATIVE TO STORM POSITION) AND ROTATED ACCORDING TO GRDROT
         DO 10 L = 1, NP
            RC = C(5*L - 4, J, K)
            XI = C(5*L - 2, J, K)/GSIZE
            YJ = C(5*L - 3, J, K)/GSIZE
            CALL XY2LLH(XI, YJ, QLAT, QLON)
            CALL GET(QLAT, QLON, HTS, RHT, XXFI, XXFJ)
            HTSAVE(L, J) = RHT
            GP(L, J, 1) = QLAT
            GP(L, J, 2) = QLON
            ADISP(J) = ADISP(J) + RC*RHT
   10    CONTINUE
   20 CONTINUE
      CALL NVNTRY(LSAVE, HTSAVE, 1, LZ, K, GP, ADISP)
      RETURN
      END
      SUBROUTINE GETHT (XI, YJ, J, ZLAT, ZLON, LL, RHT)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            GETHT
C
C  DESCRIPTION:
C
C      GET TIME-AVERAGED DEEP-LAYER-MEAN HEIGHT VALUE (DEPARTURE FROM
C      NORMAL) AT A JTWC92 GRID POINT
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL GETHT(XI,YJ,J,ZLAT,ZLON,LL,RHT)
C
C  INPUT FILES:
C
C      FILE 92 CONTAINING UP TO 7 RECORDS OF DEEP-LAYER-MEAN GEOPO-
C             TENTIAL HEIGHT DEPARTURES FROM NORMAL IN 65 X 65 GRID
C             FORMAT FOR, RESPECTIVELY,  T+00, 12, 24, 36, 48, 60, 72H.
C
C  COMMON BLOCKS:
C
C      /BLK04/,/BLK05/,/BLK10/,/STMNAM/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      XI     =      (REAL) ACROSS TRACK LOCATION OF GEOPOTENTIAL HEIGHT
C                    PREDICTOR RELATIVE TO JTWC92 GRID SYSTEM WITH STORM
C                    AT GRID POINT XI=0, YJ=0 AT TIME J.  POSITIVE
C                    VALUES ARE TO RIGHT OF PERSISTENCE TRACK WHILE NEG-
C                    ATIVE VALUES ARE TO LEFT OF PERSISTENCE TRACK.
C
C      YJ     =      (REAL) SIMILAR TO XI EXCEPT FOR ALONG TRACK PREDIC-
C                    ORS WITH POSITIVE VALUES IN DIRECTION OF STORM
C                    HEADING AND NEGATIVE VALUES IN OPPOSITE DIRECTION.
C
C      J      =      (INTEGER) INDEX FOR FORECAST INTERVAL WHERE J=1 AND
C                    J=2 ARE FOR 12H MOTION, J=3,J=4 ARE FOR 24H MOTION,
C                    ......J=11,J=12 ARE FOR 72H MOTION.
C
C      ZLAT   =      (REAL) (ZLAT(I),I=1,6) ESTIMATES OF STORM FORECAST
C                    LATITUDE AT EACH OF THE SIX 12H INTERVAL TIME
C                    PERIODS, 12 THROUGH 72H.
C
C      ZLON   =      (REAL) SIMILAR TO ZLAT EXCEPT FOR LONGITUDE.
C
C      LL     =      (INTEGER) PREDICTOR NUMBER (MAXIMUM IS 4)
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENT):
C
C
C      RHT    =      (REAL) NEEDED PREDICTOR VALUE (DEEP=LAYER-MEAN
C                    DEPARTURE FROM NORMAL GEOPOTENTIAL HEIGHT)
C                    AVERAGED OVER TIME PERIOD N.
C
C  OTHER IMPORTANT VARIABLES:
C
C      N      =      (INTEGER) COMPUTED INDEX FOR FORECAST PERIOD HAVING
C                    VALUES 2 THROUGH 7 WHERE 2 IS FOR 12H MOTION AND 7
C                    IS FOR 72H MOTION.
C
C      SHT    =      (REAL) DEEP-LAYER-MEAN GEOPOTENTIAL HEIGHT DEPAR-
C                    TURE FROM NORMAL RELATIVE TO STORM GRID FOR A
C                    SINGLE TIME PERIOD.
C
C      GP     =      (REAL) ARRAY FOR SAVING LOCATION OF GRID POINT
C                    (NEEDED FOR OPTIONAL PLOTTING OF GRID POINT)
C
C  METHOD:
C
C      1.  IN JTWC92 MODEL, HEIGHT PREDICTOR VALUES ARE AVERAGED OVER
C          FORECAST INTERVAL WHERE 12H FORECAST IS AVERAGE OF 00H AND
C          12H, 24H FORECAST IS AVERAGE OF 00H, 12H AND 24H, ETC.  THIS
C          ROUTINE OBTAINS GRID POINT VALUE AT EACH TIME INTERVAL (SHT)
C          AND AVERAGES OVER ENTIRE TIME PERIOD (RHT).
C
C      2.  USES SUBROUTINE GET TO OBTAIN HEIGHT VALUE AT STORM GRID
C          POINT ON LARGE 65X65 POLAR STEREOGRAPHIC GRID.
C
C      3.  USES NAVIGATIONAL MODULE BLKDT2 TO OBTAIN GRID POINT LOCATION
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      INTEGER LSAVE
C
      DIMENSION ZLAT(6), ZLON(6)
C
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      COMMON /BLK10/HTSAVE(4,12), GP(4,12,2), LSAVE(12)
      CHARACTER*10 SNAME
C
      COMMON /STMNAM/SNAME
C     INITIALIZE RHT AND SPECIFY THE GRIDSIZE
      RHT = 0.
      GSIZE = 150.
C     7 FIELDS OF HT DATA, 0 THRU 72H, AT 12 H INTERVALS, ALREADY RESIDE
C     ON UNIT 92
      REWIND (92)
C     FIND NUMBER OF FIELDS TO BE AVERAGED TOGETHER (PREDICTORS)
      N = (J + 1)/2 + 1
C     FIND HEIGHT ON CURRENT GRID. THIS IS ALWAYS NEEDED
      I = 1
      CALL STHGPR(SLAT00, -SLON00, GRDROT, GSIZE, 0., 0.)
      CALL XY2LLH(XI, YJ, QLAT, QLON)
      READ (92) HTS
      CALL GET(QLAT, QLON, HTS, SHT, XXFI, XXFJ)
      RHT = RHT + SHT
C     NOW, GET N-1 ADDITIONAL HEIGHTS FROM FORECAST FIELDS 2 THRU 7
      DO 10 I = 2, N
         CALL STHGPR(ZLAT(I - 1), ZLON(I - 1), GRDROT, GSIZE, 0., 0.)
         CALL XY2LLH(XI, YJ, QLAT, QLON)
         READ (92) HTS
         CALL GET(QLAT, QLON, HTS, SHT, XXFI, XXFJ)
         GP(LL, J, 1) = QLAT
         GP(LL, J, 2) = QLON
         RHT = RHT + SHT
   10 CONTINUE
      RHT = RHT/FLOAT(N)
      RETURN
      END
      BLOCK DATA BLKDT3
C.........................START PROLOGUE................................
C
C  BLOCK DATA SUBPROGRAM NAME: BLOCK DATA BLKDT3
C
C  DESCRIPTION:
C
C      CONSTANTS NEEDED FOR COMBINING SEPARATE ANALYSIS AND CLIPER FORE-
C      CASTS INTO A SINGLE FORECAST.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    COMPILATION TIME DATA ENTRY
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK01/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (ENTERED INTO /BLK01/):
C
C     CSZ         =  (REAL)  ((CSZ(I,J),J=I,12),I=1,3) ARRAY GIVING THE
C                    COEFFICIENTS FOR COMBINING SOUTH ZONE ANALYSIS AND
C                    CLIPER FORECASTS.  SEE COMMENTS IN BLKDT3 FOR
C                    ADDITIONAL DETAILS.
C
C     CNZ         =  (REAL)  ((CNZ(I,J),J=I,12),I=1,3) ARRAY GIVING THE
C                    COEFFICIENTS FOR COMBINING NORTH ZONE ANALYSIS AND
C                    CLIPER FORECASTS.  SEE COMMENTS IN BLKDT3 FOR
C                    ADDITIONAL DETAILS.
C
C     CEZ         =  (REAL)  ((CEZ(I,J),J=I,12),I=1,3) ARRAY GIVING THE
C                    COEFFICIENTS FOR COMBINING EQUATORIAL ZONE ANALYSIS
C                    AND CLIPER FORECASTS.  SEE COMMENTS IN BLKDT3 FOR
C                    ADDITIONAL DETAILS.
C  METHOD:
C
C      1.  CONSTANTS WERE DETERMINED USING A DEVELOPMENTAL DATA SET
C          1974-1988--SEE TECHNICAL MANUAL ON JTWC92 MODEL.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C.........................END PROLOGUE.................................
      COMMON /BLK01/CSZ(3,12), CNZ(3,12), CEZ(3,12)
C
C     LIST SOUTH-ZONE COEFFICIENTS
C
C                ANALYSIS     CLIPER    INTERCEPT
      DATA CSZ/ 0.3560133,  0.8393797, -22.18916,
     A          0.7856915,  0.6377671,  -2.46021,
     B          0.3943791,  0.8141772, -46.00102,
     C          0.7603369,  0.6529584,  -9.05554,
     D          0.4678432,  0.7515591, -69.86653,
     E          0.7802526,  0.6555407, -22.55145,
     F          0.4896714,  0.7038437, -79.75958,
     G          0.7644986,  0.7188117, -45.45003,
     H          0.3388501,  0.8270582, -87.67030,
     I          0.7161613,  0.6956298, -61.54748,
     J          0.2266602,  0.8809745, -75.11439,
     K          0.7777599,  0.6657874, -93.01203/
C
C  LIST NORTH-ZONE COEFFICIENTS
C
C                ANALYSIS     CLIPER    INTERCEPT
      DATA CNZ/ 0.4275668,  0.7008533, -14.68638,
     A          0.7351827,  0.6377471,  -3.20971,
     B          0.4687149,  0.6846445, -32.49862,
     C          0.6410977,  0.6525653,  -6.36033,
     D          0.5270643,  0.6034886, -38.05290,
     E          0.5539764,  0.7054612,  -7.35792,
     F          0.4949767,  0.6439755, -50.33935,
     G          0.5142303,  0.7067674,  -8.25432,
     H          0.4603612,  0.6657113, -57.11054,
     I          0.4659835,  0.7126104, -14.64377,
     J          0.3909320,  0.6701524, -40.39208,
     K          0.4144063,  0.6243135, -10.91086/
C
C  LIST EQUATORIAL-ZONE COEFFICIENTS
C
C                ANALYSIS     CLIPER    INTERCEPT
      DATA CEZ/ 0.4096627,  0.9655295, -16.42813,
     A          0.2708202,  0.8442582,   9.75742,
     B          0.5711438,  0.7989697, -34.95947,
     C          0.3278370,  0.7989216,  23.19300,
     D          0.6631167,  0.6924309, -52.67696,
     E          0.4103713,  0.7227247,  39.43386,
     F          0.6703778,  0.6388986, -64.42731,
     G          0.4247743,  0.7006151,  49.91011,
     H          0.7538467,  0.5818445, -88.55721,
     I          0.4013907,  0.7164836,  57.16465,
     J          0.7872400,  0.5189977, -97.97286,
     K          0.4494286,  0.7119452,  88.95536/
      END
      BLOCK DATA BLKDT4
C.........................START PROLOGUE................................
C
C  BLOCK DADA SUBPROGRAM NAME: BLOCK DATA BLKDT4
C
C  DESCRIPTION:
C
C      CONSTANTS NEEDED FOR COMBINING SEPARATE ANALYSIS, PERFECT-PROG
C      AND CLIPER FORECASTS INTO A COMBINED FORECAST.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON
C
C  USAGE (CALLING SEQUENCE):    COMPILATION TIME DATA ENTRY
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK02/
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES (ENTERED INTO /BLK02/):
C
C     XSZ         =  (REAL)  ((XSZ(I,J),J=I,12),I=1,4) ARRAY GIVING THE
C                    COEFFICIENTS FOR COMBINING ANALYSIS, PERFECT-PROG
C                    AND CLIPER FORECASTS IN SOUTH ZONE.  SEE COMMENTS
C                    IN BLKDT4 FOR ADDITIONAL DETAILS.
C
C     XNZ         =  (REAL)  ((XNZ(I,J),J=I,12),I=1,4) ARRAY GIVING THE
C                    COEFFICIENTS FOR COMBINING ANALYSIS, PERFECT-PROG
C                    AND CLIPER FORECASTS IN NORTH ZONE.  SEE COMMENTS
C                    IN BLKDT4 FOR ADDITIONAL DETAILS.
C
C     XEZ         =  (REAL)  ((XEZ(I,J),J=I,12),I=1,4) ARRAY GIVING THE
C                    COEFFICIENTS FOR COMBINING ANALYSIS, PERFECT-PROG
C                    AND CLIPER FORECASTS IN EQUATORIAL ZONE.  SEE
C                    COMMENTS IN BLKDT4 FOR ADDITIONAL DETAILS.
C
C  METHOD:
C
C      1.  CONSTANTS WERE DETERMINED USING A DEVELOPMENTAL DATA SET
C          1974-1988 SEE TECHNICAL MANUAL ON JTWC92 MODEL.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON/BLK02/XSZ(4,12), XNZ(4,12), XEZ(4,12)
      DIMENSION C(4,12,3)
      EQUIVALENCE (XSZ(1,1),C(1,1,1))
C
C
C  LIST SOUTH ZONE COEFFICIENTS
C
C                ANALYSIS   PFCT-PROG    CLIPER   INTERCEPT
      DATA XSZ/ 0.1254122, 0.2704492, 0.8310344, -25.51049,
     A         -0.3411632, 1.0777102, 0.5932866,  -1.90254,
     B         -0.4098193, 0.8359465, 0.7668581, -42.62730,
     C         -0.7359390, 1.2423904, 0.4887244,   0.09138,
     D         -0.1057081, 0.7080585, 0.6582809, -81.07791,
     E         -0.6536346, 1.1587826, 0.3722247,   3.85741,
     F         -0.1250034, 0.7776725, 0.5979454, -99.42776,
     G         -0.5790690, 1.0859380, 0.2783734,  14.55081,
     H         -0.2644188, 0.8379073, 0.5855494, -80.04594,
     I         -0.6422848, 1.0601823, 0.2278254,  38.48532,
     J         -0.3477332, 0.8610104, 0.5953250, -68.29493,
     K         -0.5060994, 1.0278732, 0.1170940,  55.72622/
C
C  LIST NORTH ZONE COEFFICIENTS
C
C                ANALYSIS   PFCT-PROG    CLIPER   INTERCEPT
      DATA XNZ/-0.4273737, 0.8865087, 0.6603159, -13.64164,
     A         -0.2430585, 1.0033218, 0.4784171,  -2.02875,
     B         -0.2950917, 0.9294578, 0.4417607, -15.81762,
     C         -0.1072703, 0.8834799, 0.4272839,  -4.48914,
     D         -0.2416227, 0.9882522, 0.2734231,  -5.50972,
     E         -0.2032586, 0.9437850, 0.3683179,  -2.28136,
     F         -0.1862885, 0.9743145, 0.2065112,   1.64533,
     G         -0.1316404, 0.9449439, 0.2459050,  -1.34863,
     H         -0.1443541, 0.9793275, 0.1433110,   7.21964,
     I         -0.0945960, 0.9517731, 0.1719652,  -2.20527,
     J         -0.1524750, 0.9733027, 0.1381641,  15.01788,
     K         -0.2005756, 0.9839120, 0.1869238,   0.58746/
C
C  LIST EQUATORIAL ZONE COEFFICIENTS
C
C                ANALYSIS   PFCT-PROG    CLIPER   INTERCEPT
      DATA XEZ/ 0.2878967, 0.1685914, 0.9467677, -17.57962,
     A          0.0558927, 0.2755805, 0.8046221,  11.84718,
     B          0.2964450, 0.4117714, 0.7443755, -42.17306,
     C          0.0073607, 0.4458140, 0.7014064,  28.81969,
     D          0.3252928, 0.5464986, 0.5986865, -68.64258,
     E          0.0041285, 0.5751939, 0.5835468,  47.94237,
     F          0.3477108, 0.6680120, 0.5080394,-106.20208,
     G         -0.1555238, 0.7578501, 0.5246634,  50.04234,
     H          0.4113051, 0.6769755, 0.4280824,-132.88655,
     I         -0.1110786, 0.7722651, 0.4990175,  77.02752,
     J          0.4743668, 0.7238585, 0.3342479,-167.15023,
     K         -0.0717304, 0.7949221, 0.4797796, 113.14570/
C
      END
      BLOCK DATA BLKDT5
C.........................START PROLOGUE................................
C
C  BLOCK DATA SUBPROGRAM NAME: BLOCK DATA BLKDT5
C
C  DESCRIPTION:
C
C      ENTER REGRESSION COEFFICIENTS, PREDICTOR ADDRESSES, PREDICTOR
C      MEANS AND PREDICTOR STANDARD DEVIATIONS INTO LABELED COMMON
C      BLOCK /BLK03/C(21,12,6)
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    COMPILATION TIME DATA ENTRY
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:C
C      /BLK03/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLE (ENTERED INTO /BLK03/):
C
C       C        =   (REAL) (((C(I,J,K),K=1,6),J=1,12,),I=1,21) ARRAY
C                    CONTAINING ALL REGRESSION COEFFICIENTS AND OTHER
C                    CONSTANTS UTILIZED IN PREDICTING MOTION FROM ANALY-
C                    SIS FIELDS ALONE AND FROM PERFECT-PROG FIELDS
C                    ALONE. SUBSCRIPT ADDRESS INDEXING IS AS FOLLOWS:
C
C                    I = INDEX FOR SPECIFYING TYPE OF CONSTANT FOR GIVEN
C                    PREDICTOR NUMBER-SEE SUBPROGRAM BLKDT5 FOR DETAILS.
C
C                    J = INDEX WHICH SPECIFIES ALONG OR ACROSS TRACK (OR
C                    MERIDIONAL/ZONAL) COMPONENT OF MOTION AND FORECAST
C                    INTERVAL, 12 THROUGH 72H.  SEE BLOCK DATA SUBPRO-
C                    GRAM BLKDT5 FOR DETAILS.
C
C                    K = INDEX WHICH FURTHER SPECIFIES STRATIFICATION
C                    ZONE NUMBER 1, 2 OR 3 AND WHETHER ANALYSIS OR PER-
C                    FECT PROG MODE.  SEE BLOCK DATA SUBPROGRAM BLKDT5
C                    FOR DETAILS.
C
C  METHOD:
C
C      1.  CONSTANTS WERE DETERMINED USING A DEVELOPMENTAL DATA SET
C          1974-1988 SEE TECHNICAL MANUAL ON JTWC92 MODEL.
C
C      2.  THERE ARE A MAXIMUM OF FOUR PREDICTORS AND A MINIMUM OF TWO
C          FOR EACH FORECAST ENTITY.  IF THERE ARE LESS THAN FOUR PRE-
C          DICTORS, MISSING ARRAY ELEMENTS ARE ASSIGNED LARGE NUMBER
C          >1.0E+25.  IF THERE ARE NO MISSING ENTRIES, IT CAN BE ASSUMED
C          THAT THERE ARE 4 PREDICTORS (THE MAXIMUM NUMBER).  IF
C          C(21,J,K) CONTAINS LARGE NUMBER, THERE ARE 3 PREDICTORS; IF
C          C(16,J,K) CONTAINS LARGE NUMBER, THERE ARE 2 PREDICTORS (MIN-
C          IMUM NUMBER).
C
C      3.  ABOVE TEST FOR NUMBER OF PREDICTORS IS USED IN SUBROUTINES
C          ANLS AND PPRG.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON/BLK03/
     A          AA12S(21),AX12S(21),AA24S(21),AX24S(21),
     B          AA36S(21),AX36S(21),AA48S(21),AX48S(21),
     C          AA60S(21),AX60S(21),AA72S(21),AX72S(21),
     D          PA12S(21),PX12S(21),PA24S(21),PX24S(21),
     E          PA36S(21),PX36S(21),PA48S(21),PX48S(21),
     F          PA60S(21),PX60S(21),PA72S(21),PX72S(21),
C
     G          AA12N(21),AX12N(21),AA24N(21),AX24N(21),
     H          AA36N(21),AX36N(21),AA48N(21),AX48N(21),
     I          AA60N(21),AX60N(21),AA72N(21),AX72N(21),
     J          PA12N(21),PX12N(21),PA24N(21),PX24N(21),
     K          PA36N(21),PX36N(21),PA48N(21),PX48N(21),
     L          PA60N(21),PX60N(21),PA72N(21),PX72N(21),
C
     M          AM12E(21),AZ12E(21),AM24E(21),AZ24E(21),
     N          AM36E(21),AZ36E(21),AM48E(21),AZ48E(21),
     O          AM60E(21),AZ60E(21),AM72E(21),AZ72E(21),
     P          PM12E(21),PZ12E(21),PM24E(21),PZ24E(21),
     Q          PM36E(21),PZ36E(21),PM48E(21),PZ48E(21),
     R          PM60E(21),PZ60E(21),PM72E(21),PZ72E(21)
      DIMENSION C(21,12,6)
      EQUIVALENCE (C(1,1,1),AA12S(1))
C LIST 12 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE......
      DATA AA12S/ .1290186E+1,  150.,  600.,   7.74, 22.99,
     A           -.1614307E+1, -150., -450., -18.47, 16.42,
     B            .8918272E+0, -300.,  150.,  -7.01, 18.77,
     C           -.7495558E-1,  150., 1650.,-179.83,140.33, .5886214E+2/
C LIST 12 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE.....
      DATA AX12S/-.6900823E+0,  600.,    0.,  -3.55, 17.90,
     A            .5170291E+0, -600.,    0.,  -4.03, 16.41, .5655301E+1,
     B            10*9999999E+25/
C LIST 24 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE......
      DATA AA24S/ .3492238E+1,  150.,  450.,   7.81, 18.86,
     A           -.2393392E+1,  300., -450., -17.22, 16.90, .1344235E+3,
     B            10*9999999E+25/
C LIST 24 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE.....
      DATA AX24S/-.1671966E+1,  600.,    0.,  -3.39, 18.06,
     A            .1300572E+1, -600.,    0.,  -4.12, 16.39, .2156880E+2,
     B            10*9999999E+25/
C LIST 36 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE......
      DATA AA36S/ .4226137E+1,  300.,  450.,   6.50, 20.46,
     A           -.5837515E+1, -150., -450., -18.04, 16.25,
     B            .3023605E+1, -300.,    0., -14.97, 19.33, .2029262E+3,
     C             5*9999999E+25/
C LIST 36 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE.....
      DATA AX36S/-.2890875E+1,  600.,    0.,  -3.13, 18.28,
     A            .2442633E+1, -600., -150.,  -7.29, 15.86, .5377945E+2,
     B            10*9999999E+25/
C LIST 48 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE......
      DATA AA48S/ .3902971E+1,    0.,  600.,  10.52, 21.56,
     A            .1297669E+1,  900.,  450., -22.06, 49.78,
     B           -.8840854E+1, -300., -450., -15.02, 15.46,
     C            .6097634E+1, -450., -150., -10.33, 16.42, .2850713E+3/
C LIST 48 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE.....
      DATA AX48S/-.4042238E+1,  600.,    0.,  -2.86, 18.21,
     A            .3429598E+1, -600., -150.,  -6.98, 15.82, .9236961E+2,
     B            10*9999999E+25/
C LIST 60 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE......
      DATA AA60S/ .3847068E+1,    0.,  600.,  10.56, 21.51,
     A            .1269450E+1,  900.,  600., -36.64, 61.91, .4382542E+3,
     B            10*9999999E+25/
C LIST 60 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE.....
      DATA AX60S/-.4410327E+1,  600.,    0.,  -2.36, 18.00,
     A            .3590925E+1, -600.,  150.,  -0.64, 17.38, .1117862E+3,
     B            10*9999999E+25/
C LIST 72 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE......
      DATA AA72S/ .3220887E+1,    0.,  750.,   6.63, 28.20,
     A            .1730622E+1,  900.,  450., -19.00, 47.78, .5004260E+3,
     B            10*9999999E+25/
C LIST 72 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, SOUTH-ZONE.....
      DATA AX72S/-.4752186E+1,  600.,    0.,  -1.89, 17.95,
     A            .3706368E+1, -600.,    0.,  -4.02, 16.47, .1700915E+3,
     B            10*9999999E+25/
C
C
C LIST 12 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE......
      DATA PA12S/ .1876157E+1,    0.,  450.,   8.21, 18.55,
     A           -.1381047E+1,  150., -450., -19.35, 16.36, .6377657E+2,
     B            10*9999999E+25/
C LIST 12 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE.....
      DATA PX12S/-.9917780E+0,  450.,    0.,  -6.06, 16.73,
     A            .8538845E+0, -600.,    0.,  -3.50, 15.71, .2997463E+1,
     B            10*9999999E+25/
C LIST 24 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE......
      DATA PA24S/ .4087493E+1,    0.,  450.,   7.29, 18.68,
     A           -.3112370E+1,  150., -450., -19.30, 16.11,
     B           -.8541209E-1, -450., 1650.,-137.89,145.66, .1012872E+3,
     C             5*9999999E+25/
C LIST 24 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE.....
      DATA PX24S/-.2946771E+1,  450.,    0.,  -6.97, 17.06,
     A            .2483065E+1, -450.,  150.,  -1.04, 16.75, .3932201E+1,
     B            10*9999999E+25/
C LIST 36 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE......
      DATA PA36S/ .6485939E+1,    0.,  450.,   6.05, 18.88,
     A           -.4909337E+1,  150., -450., -19.29, 15.82,
     B           -.1456681E+0, -600., 1650.,-129.87,148.76, .1375660E+3,
     C             5*9999999E+25/
C LIST 36 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE.....
      DATA PX36S/-.5227543E+1,  450.,    0.,  -7.90, 17.76,
     A            .4970374E+1, -600.,    0.,  -2.67, 15.36, .1698421E+2,
     B            10*9999999E+25/
C LIST 48 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE......
      DATA PA48S/ .8959438E+1,    0.,  450.,   4.46, 19.44,
     A           -.6815402E+1,  150., -450., -19.13, 15.52,
     B           -.2015008E+0, -450., 1650.,-144.00,146.83, .1679601E+3,
     C             5*9999999E+25/
C LIST 48 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE.....
      DATA PX48S/-.7631576E+1,  450.,    0.,  -9.09, 18.79,
     A            .7356467E+1, -600.,    0.,  -1.97, 15.36, .2510689E+2,
     B            10*9999999E+25/
C LIST 60 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE......
      DATA PA60S/ .1143566E+2,    0.,  450.,   2.44, 20.26,
     A           -.8849182E+1,  150., -450., -19.13, 15.33,
     B           -.2586736E+0,    0., 1650.,-188.76,142.55, .1862722E+3,
     C             5*9999999E+25/
C LIST 60 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE.....
      DATA PX60S/-.9662222E+1,  450.,    0., -10.36, 19.79,
     A            .9529518E+1, -600.,    0.,  -1.43, 15.30, .3338466E+2,
     B            10*9999999E+25/
C LIST 72 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE......
      DATA PA72S/ .1377050E+2,    0.,  450.,   0.47, 21.17,
     A           -.1087332E+2,  150., -450., -19.15, 15.09,
     B           -.3647718E+0,  300., 1650.,-220.75,139.19, .1937350E+3,
     C             5*9999999E+25/
C LIST 72 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, SOUTH-ZONE.....
      DATA PX72S/-.1276722E+2,  450.,    0., -11.54, 20.55,
     A            .1209164E+2, -450.,    0.,  -5.64, 15.58, .8505331E+2,
     B            10*9999999E+25/
C
C
C
C LIST 12 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE......
      DATA AA12N/-.2215036E+1,  300., -450., -52.15, 62.48,
     A            .9588088E+0,    0.,  600.,   9.91, 25.65,
     B            .7487179E+0,  450., -600., -68.81, 85.40,
     C            .8207121E+0,  150.,  300.,  -7.41, 29.17, .5926875E+2/
C LIST 12 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE.....
      DATA AX12N/-.7066579E+0,  600.,    0., -35.02, 41.07,
     A            .8885921E+0, -450.,    0., -17.49, 25.73, .2613338E-1,
     B            10*9999999E+25/
C LIST 24 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE......
      DATA AA24N/-.2200787E+1,  300., -450., -43.19, 52.61,
     A            .2748432E+1,  150.,  600.,   7.41, 25.09, .1102810E+3,
     B            10*9999999E+25/
C LIST 24 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE.....
      DATA AX24N/-.1257987E+1,  750.,    0., -44.49, 50.44,
     A            .2011584E+1, -450.,  300.,  -3.37, 21.36,-.2024361E+2,
     B            10*9999999E+25/
C LIST 36 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE......
      DATA AA36N/-.3176988E+1,  300., -450., -36.23, 44.44,
     A            .3741836E+1,  150.,  600.,   5.93, 24.31, .1627570E+3,
     B            10*9999999E+25/
C LIST 36 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE.....
      DATA AX36N/-.2192626E+1,  750.,  150., -35.53, 44.51,
     A            .3151331E+1, -300.,  450.,   2.37, 22.44,-.2673947E+2,
     B            10*9999999E+25/
C LIST 48 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE......
      DATA AA48N/-.5107602E+1,  300., -300., -28.93, 30.96,
     A            .4676688E+1,  150.,  600.,   4.55, 22.92, .1865626E+3,
     B            10*9999999E+25/
C LIST 48 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE.....
      DATA AX48N/-.2924908E+1,  750.,  150., -32.28, 42.48,
     A            .4581874E+1, -300.,  450.,   1.66, 21.74,-.1590983E+2,
     B            10*9999999E+25/
C LIST 60 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE......
      DATA AA60N/-.4696362E+1,  300., -450., -28.83, 32.77,
     A            .3621606E+1,  150.,  750.,   0.64, 27.15, .2617068E+3,
     B            10*9999999E+25/
C LIST 60 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE.....
      DATA AX60N/-.3429637E+1,  750.,  150., -28.57, 40.77,
     A            .6179613E+1, -450.,  450.,  -0.26, 21.00,-.1163041E+1,
     B            10*9999999E+25/
C LIST 72 HOUR ALONG-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE......
      DATA AA72N/-.3948996E+1,  450., -450., -27.75, 35.95,
     A            .2726535E+1,  300.,  750.,  -4.94, 29.58, .3394082E+3,
     B            10*9999999E+25/
C LIST 72 HOUR ACROSS-TRACK CONSTANTS FOR ANALYSIS MODE, NORTH-ZONE.....
      DATA AX72N/-.1495222E+1,  750., 1050., -55.75, 77.39,
     A           -.1692597E+1, 1050.,    0., -56.41, 70.84,
     B            .4575808E+1, -450.,  450.,  -1.09, 20.70,-.8060368E+2,
     C             5*9999999E+25/
C
C
C
C LIST 12 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE......
      DATA PA12N/-.2398489E+1,  300., -450., -57.31, 69.70,
     A            .9676300E+0,    0.,  600.,   9.46, 25.90,
     B            .9847403E+0,  450., -600., -74.53, 92.38,
     C            .8091759E+0,  150.,  300.,  -9.64, 30.64, .6127223E+2/
C LIST 12 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE.....
      DATA PX12N/-.1176776E+0,  750.,    0., -57.16, 61.68,
     A            .1125247E+1, -450.,    0., -17.47, 27.89,
     B           -.8420944E+0,  450.,  150., -22.81, 33.78, .2953987E+1,
     C             5*9999999E+25/
C LIST 24 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE......
      DATA PA24N/-.4760008E+1,  300., -450., -52.05, 65.37,
     A            .1946335E+1, -150.,  600.,   8.16, 24.67,
     B            .1915872E+1,  450., -600., -67.23, 86.49,
     C            .1778245E+1,  150.,  300., -12.47, 29.48, .1129949E+3/
C LIST 24 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE.....
      DATA PX24N/ .1332989E+0,  750.,  150., -52.66, 58.89,
     A            .3114512E+1, -450.,    0., -16.61, 26.72,
     B           -.2783916E+1,  450.,  150., -25.83, 34.99, .1578286E+2,
     C             5*9999999E+25/
C LIST 36 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE......
      DATA PA36N/-.6959373E+1,  300., -450., -46.94, 60.52,
     A            .5122660E+0, -150.,  600.,   5.85, 24.04,
     B            .2927350E+1,  450., -600., -59.61, 79.33,
     C            .4652802E+1,    0.,  450.,  -1.16, 24.58, .1502673E+3/
C LIST 36 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE.....
      DATA PX36N/ .1114827E+1,  600.,  150., -38.81, 46.57,
     A            .5433504E+1, -450.,    0., -15.72, 25.63,
     B           -.5684011E+1,  450.,  150., -28.42, 36.18, .2576050E+2,
     C             5*9999999E+25/
C LIST 48 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE......
      DATA PA48N/-.9642743E+1,  300., -450., -42.97, 55.14,
     A            .6696700E+0, -150.,  600.,   3.09, 23.83,
     B            .4190507E+1,  450., -600., -53.93, 71.89,
     C            .6323578E+1,    0.,  450.,  -3.93, 23.87, .1899913E+3/
C LIST 48 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE.....
      DATA PX48N/-.9148557E+0,  600.,  300., -37.67, 47.89,
     A            .8541476E+1, -450.,    0., -15.50, 24.66,
     B           -.5992708E+1,  300.,  150., -28.00, 31.89, .1621382E+2,
     C             5*9999999E+25/
C LIST 60 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE......
      DATA PA60N/-.9992147E+1,  150., -450., -37.72, 45.50,
     A            .6720293E+1, -150.,  450.,  -3.00, 22.29,
     B            .2121017E+1,  300., -900., -51.62, 73.80,
     C            .3282715E+1,  150.,  300., -19.25, 26.11, .2153569E+3/
C LIST 60 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE.....
      DATA PX60N/-.6705294E+0,  600.,  300., -36.92, 48.17,
     A            .1134804E+2, -450.,    0., -16.01, 23.10,
     B           -.8531271E+1,  300.,  150., -28.21, 30.61, .1144848E+2,
     C             5*9999999E+25/
C LIST 72 HOUR ALONG-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE......
      DATA PA72N/-.1310978E+2,  150., -450., -35.88, 42.62,
     A            .8190208E+1, -150.,  450.,  -5.13, 21.60,
     B            .2949601E+1,  300., -900., -47.81, 68.73,
     C            .4451074E+1,  150.,  300., -20.69, 26.28, .2403118E+3/
C LIST 72 HOUR ACROSS-TRACK CONSTANTS FOR PERF-PRG MODE, NORTH-ZONE.....
      DATA PX72N/ .8826834E-1,  600.,  300., -35.72, 47.05,
     A            .1057921E+2, -450.,  150., -11.19, 21.71,
     B           -.1167266E+2,  300.,  150., -28.51, 30.47,
     C            .4392403E+1, -300., -300., -28.47, 29.98, .6992560E+1/
C
C
C
C LIST 12 HOUR MERIDIONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE.......
      DATA AM12E/ .1525892E+1,    0.,  900.,  -2.53, 16.51,
     A           -.1573197E+1,  150., -450.,  -6.73, 16.59,
     B            .2449847E+0,  900.,  600.,  -9.98, 39.84, .3730908E+2,
     C             5*9999999E+25/
C LIST 12 HOUR ZONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE............
      DATA AZ12E/-.2499288E+1,  600.,    0.,   3.18, 23.20,
     A            .1362548E+1, -450., -300., -15.58, 14.30,-.6727318E+2,
     B            10*9999999E+25/
C LIST 24 HOUR MERIDIONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE.......
      DATA AM24E/ .3185940E+1,    0.,  900.,  -2.56, 16.18,
     A           -.3240126E+1,  150., -450.,  -6.81, 16.47,
     B            .6142418E+0,  900.,  600.,  -8.87, 38.31, .8061795E+2,
     C             5*9999999E+25/
C LIST 24 HOUR ZONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE............
      DATA AZ24E/-.4892923E+1,  600., -150.,   3.04, 22.93,
     A            .2866855E+1, -450., -300., -15.66, 14.13,-.1355645E+3,
     B            10*9999999E+25/
C LIST 36 HOUR MERIDIONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE.......
      DATA AM36E/ .4979753E+1,    0.,  900.,  -2.57, 15.74,
     A           -.5024430E+1,  150., -450.,  -6.71, 16.25,
     B            .9389045E+0,  900.,  450.,  -8.85, 38.07, .1290170E+3,
     C             5*9999999E+25/
C LIST 36 HOUR ZONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE............
      DATA AZ36E/-.7461955E+1,  600., -150.,   3.77, 22.34,
     A            .5189296E+1, -450., -300., -15.59, 14.07,-.1815936E+3,
     B            10*9999999E+25/
C LIST 48 HOUR MERIDIONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE.......
      DATA AM48E/ .2155643E+1,  900.,  600.,  -5.83, 35.73,
     A           -.5493794E+1,  450., -150.,   2.47, 18.51,
     B            .4926764E+1,    0.,  900.,  -2.16, 15.48, .2346296E+3,
     C             5*9999999E+25/
C LIST 48 HOUR ZONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE............
      DATA AZ48E/-.8866938E+1,  600., -150.,   4.65, 21.74,
     A            .6426198E+1, -450.,  750.,  -9.11, 14.41,-.2829546E+3,
     B            10*9999999E+25/
C LIST 60 HOUR MERIDIONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE.......
      DATA AM60E/ .1276772E+1, 1050.,    0., -32.84, 57.88,
     A           -.8052128E+1,  300., -300.,  -1.95, 16.90,
     B            .8296687E+1,    0.,  750.,  -1.88, 14.81, .2932725E+3,
     C             5*9999999E+25/
C LIST 60 HOUR ZONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE............
      DATA AZ60E/-.1006115E+2,  600., -300.,   5.65, 20.78,
     A            .7532554E+1, -450.,  750.,  -8.96, 14.07,-.3520769E+3,
     B            10*9999999E+25/
C LIST 72 HOUR MERIDIONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE.......
      DATA AM72E/ .1744204E+1, 1050.,    0., -31.16, 57.18,
     A           -.9858113E+1,  300., -150.,  -3.59, 17.07,
     B            .9695960E+1,    0.,  750.,  -1.83, 14.80, .3471145E+3,
     C             5*9999999E+25/
C LIST 72 HOUR ZONAL CONSTANTS FOR ANALYSIS MODE, EQTRL-ZONE............
      DATA AZ72E/-.1418931E+2,  450., -300.,   4.14, 17.56,
     A            .1267587E+2, -450.,  750.,  -8.83, 14.19,-.3939202E+3,
     B            10*9999999E+25/
C
C
C
C LIST 12 HOUR MERIDIONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE.......
      DATA PM12E/ .2112045E+1, -150.,  750.,  -4.43, 14.87,
     A           -.1965414E+1,    0., -450., -10.84, 15.06, .2966240E+2,
     B            10*9999999E+25/
C LIST 12 HOUR ZONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE............
      DATA PZ12E/-.3449185E+1,  450.,  300.,   4.52, 18.89,
     A            .2503676E+1, -450.,  450., -10.31, 13.90,-.5506097E+2,
     B            10*9999999E+25/
C LIST 24 HOUR MERIDIONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE.......
      DATA PM24E/ .4560854E+1, -150.,  750.,  -3.76, 14.53,
     A           -.4174262E+1,    0., -450., -10.94, 14.77, .6058156E+2,
     B            10*9999999E+25/
C LIST 24 HOUR ZONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE............
      DATA PZ24E/-.6925426E+1,  450.,  300.,   4.55, 18.65,
     A            .5089883E+1, -450.,  450.,  -9.89, 13.63,-.1134996E+3,
     B            10*9999999E+25/
C LIST 36 HOUR MERIDIONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE.......
      DATA PM36E/ .7893633E+1, -150.,  600.,  -3.89, 13.87,
     A           -.7428304E+1,    0., -450., -10.81, 14.52, .9206073E+2,
     B            10*9999999E+25/
C LIST 36 HOUR ZONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE............
      DATA PZ36E/-.1001108E+2,  450.,  300.,   4.62, 18.76,
     A            .7773966E+1, -450.,  450.,  -9.34, 13.36,-.1717538E+3,
     B            10*9999999E+25/
C LIST 48 HOUR MERIDIONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE.......
      DATA PM48E/ .1026727E+2, -150.,  600.,  -3.22, 13.68,
     A           -.9696667E+1,    0., -450., -10.76, 14.41, .1266049E+3,
     B            10*9999999E+25/
C LIST 48 HOUR ZONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE............
      DATA PZ48E/-.1312555E+2,  450.,  300.,   4.52, 18.69,
     A            .1007124E+2, -450.,  450.,  -8.79, 13.20,-.2350315E+3,
     B            10*9999999E+25/
C LIST 60 HOUR MERIDIONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE.......
      DATA PM60E/-.1273022E+2,    0., -450., -10.53, 14.33,
     A            .1317816E+2, -150.,  600.,  -2.60, 13.42, .1516426E+3,
     B            10*9999999E+25/
C LIST 60 HOUR ZONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE............
      DATA PZ60E/-.1638075E+2,  450.,  300.,   4.86, 18.14,
     A            .1246113E+2, -450.,  450.,  -8.37, 12.93,-.2926372E+3,
     B            10*9999999E+25/
C LIST 72 HOUR MERIDIONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE.......
      DATA PM72E/-.1554726E+2,    0., -450., -10.70, 14.38,
     A            .1550928E+2, -150.,  600.,  -2.16, 13.36, .1775699E+3,
     B            10*9999999E+25/
C LIST 72 HOUR ZONAL CONSTANTS FOR PERF-PRG MODE, EQTRL-ZONE............
      DATA PZ72E/-.1927090E+2,  450.,  300.,   4.93, 17.94,
     A            .1448736E+2, -450.,  450.,  -8.13, 12.88,-.3519534E+3,
     B            10*9999999E+25/
C
      END
      SUBROUTINE CBNAC (NZ)
C
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            CBNAC
C
C  DESCRIPTION:
C
C      COMBINES TWO FORECASTS OF TROPICAL CYCLONE DISPLACEMENT BASED ON
C      (1): INITIAL DEEP-LAYER-MEAN HEIGHT FIELD; (2) CLIMATOLOGY AND
C      PERSISTENCE INTO A SINGLE FORECAST.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL CBNAC(NZ)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK01/,/BLK06/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C      NZ     =      (INTEGER) ZONE NUMBER WHERE 1 IS SOUTH ZONE, 2 IS
C                    NORTH ZONE AND 3 IS EQUATORIAL ZONE.
C
C  PRINCIPAL VARIABLES (RETURNED IN COMMON BLOCK /BLKO6/
C
C      ACDISP   =    (REAL) (ACDISP,(I),I=1,12)  ARRAY CONTAINING NEEDED
C                    FORECAST DISPLACEMENT (NMI) OF STORM CENTER FROM
C                    ITS INITIAL POSITION WHERE INDICES 1, 3, 5, 7, 9,
C                    11 REFER TO 12 THROUGH 72H HOUR ALONG TRACK (OR
C                    MERIDIONAL, FOR EQUATORIAL ZONE) MOTION.  INDICES
C                    2, 4, 6, 8, 10 AND 12 REFER TO ACROSS TRACK (OR
C                    ZONAL FOR EQUATORIAL ZONE) MOTION.
C
C  OTHER IMPORTANT VARIABLES (INCOMING IN COMMON BLOCKS):
C
C      ADISP     =   (REAL) (ADISP(I),I=1,12)  ARRAY CONTAINING PREVI-
C                    OUSLY COMPUTED FORECAST DISPLACEMENTS BASED ON INI-
C                    TIAL ANALYSIS.  INDEXING SCHEME SAME AS FOR ARRAY
C                    ACDISP.
C
C      CDISP     =   (REAL) (CDISP(I),I=1,12)  ARRAY CONTAINING PREVI-
C                    OUSLY COMPUTED FORECAST DISPLACEMENTS BASED ON CLI-
C                    MATOLOGY AND PERSISTENCE.  INDEXING SCHEME SAME AS
C                    FOR ARRAY ACDISP.
C
C      C   =         (REAL) THREE DIMENSIONAL ARRAY
C                    (((C(I,J,K),K=1,3),J=1,12),I=1,4) CONTAINING
C                    REQUIRED REGRESSION COEFFICIENTS.  SEE BLOCK DATA
C                    SUBPROGRAM BLKDT3 FOR A DESCRIPTION OF SUBS-
C                    CRIPTING SCHEME.
C  METHOD:
C
C      1.  REGRESSION EQUATIONS ARE USED FOR COMBINING FORECASTS.
C
C      2.  REGRESSION EQUATIONS CONSTANTS RESIDE IN BLOCK DATA BLKDT3.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      DIMENSION C(3,12,3)
C
      COMMON /BLK01/CSZ(3,12), CNZ(3,12), CEZ(3,12)
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
C
      EQUIVALENCE (CSZ(1,1),C(1,1,1))
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C     COMBINE CLIPER AND ANALYSIS FORECASTS
C
      DO 10 J = 1, 12
         ACDISP(J) = C(1, J, NZ)*ADISP(J) + C(2, J, NZ)*CDISP(J) + C(3,
     *    J, NZ)
   10 CONTINUE
      RETURN
      END
      SUBROUTINE CBNACP (NZ)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            CBNACP
C
C  DESCRIPTION:
C
C      COMBINES THREE FORECASTS OF TROPICAL CYCLONE DISPLACEMENT BASED
C      ON (1): INITIAL DEEP-LAYER-MEAN HEIGHT FIELD; (2) FORECAST DEEP-
C      LAYER MEAN HEIGHT FIELDS AND (3) CLIMATOLOGY AND PERSISTENCE,
C      INTO A SINGLE FORECAST.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL CBNACP(NZ)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK02/,/BLK06/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C      NZ     =      (INTEGER) ZONE NUMBER WHERE 1 IS SOUTH ZONE, 2 IS
C                    NORTH ZONE AND 3 IS EQUATORIAL ZONE.
C
C  PRINCIPAL VARIABLES (RETURNED IN COMMON BLOCK /BLKO6/
C
C      ACPDSP   =    (REAL) (ACPDSP,(I),I=1,12)  ARRAY CONTAINING
C                    FORECAST DISPLACEMENT (NAUTICAL MILES) OF STORM
C                    CENTER FROM ITS INITIAL POSITION WHERE INDICES 1,
C                    3, 5, 7, 9, 11 REFER TO 12 THROUGH 72H ALONG TRACK
C                    (OR MERIDIONAL, FOR EQUATORIAL ZONE) MOTION.
C                    INDICES 2, 4, 6, 8, 10 AND 12 REFER TO ACROSS
C                    TRACK (OR ZONAL FOR EQUATORIAL ZONE) MOTION.
C
C  OTHER IMPORTANT VARIABLES (INCOMING IN COMMON BLOCKS):
C
C      ADISP     =   (REAL) (ADISP(I),I=1,12)  ARRAY CONTAINING PREVI-
C                    OUSLY COMPUTED FORECAST DISPLACEMENTS BASED ON INI-
C                    TIAL ANALYSIS.  INDEXING SCHEME SAME AS FOR ARRAY
C                    ACPDSP.
C
C      PDISP     =   (REAL) (PDISP(I),I=1,12)  ARRAY CONTAINING PREVI-
C                    OUSLY COMPUTED FORECAST DISPLACEMENTS BASED ON
C                    FORECAST FIELDS.  INDEXING SCHEME SAME AS FOR ARRAY
C                    ACPDSP.
C
C      CDISP     =   (REAL) (CDISP(I),I=1,12)  ARRAY CONTAINING PREVI-
C                    OUSLY COMPUTED FORECAST DISPLACEMENTS BASED ON CLI-
C                    MATOLOGY AND PERSISTENCE.  INDEXING SCHEME SAME AS
C                    FOR ARRAY ACDISP.
C
C      C   =         (REAL) THREE DIMENSIONAL ARRAY
C                    (((C(I,J,K),K=1,3),J=1,12),I=1,3) CONTAINING
C                    REQUIRED REGRESSION COEFFICIENTS.  SEE BLOCK DATA
C                    SUBPROGRAM BLKDT4 FOR A DESCRIPTION OF INDEXING.
C
C  METHOD:
C
C      1.  REGRESSION EQUATIONS ARE USED FOR COMBINING FORECASTS.
C
C      2.  REGRESSION EQUATIONS CONSTANTS RESIDE IN BLOCK DATA BLKDT3.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.....................END PROLOGUE......................................
C
      DIMENSION C(4,12,3)
C
      COMMON/BLK02/XSZ(4,12), XNZ(4,12), XEZ(4,12)
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
C
      EQUIVALENCE (XSZ(1,1),C(1,1,1))
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C     COMBINE ANALYSIS, PFCT-PROG AND CLIPER FORECASTS..
C
      DO 10 J = 1, LASTHR
         ACPDSP(J) = C(1, J, NZ)*ADISP(J) + C(2, J, NZ)*PDISP(J) + C(3,
     *    J, NZ)*CDISP(J) + C(4, J, NZ)
   10 CONTINUE
      RETURN
      END
      SUBROUTINE RSOLV (DISP, ALATS, ALONS)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            RSOLV
C
C  DESCRIPTION:
C
C      CONVERTS FORECASTS OF TROPICAL CYCLONE MOTION WHICH ARE SPECIFIED
C      AS ORTHOGONAL DISPLACEMENTS (EITHER IN THE ALONG/ACROSS TRACK
C      SENSE OR A MERIDIONAL/ZONAL SENSE) INTO FORECAST LAT/LONS.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON
C
C  USAGE (CALLING SEQUENCE):    CALL RSOLV(DISP,ALATS,ALONS)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK05/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C      DISP     =    (REAL)  ARRAY (DISP(I),I=1,12) CONTAINING STORM
C                    FORECAST DISPLACEMENTS (NAUTICAL MILES) FROM ITS
C                    INITIAL POSITION.  INDICES 1, 3, 5, 7, 9, 11 REFER
C                    TO ALONG TRACK (FOR NORTH AND SOUTH ZONES) OR MERI-
C                    DIONAL MOTION (FOR EQUATORIAL ZONE).  INDICES 2, 4,
C                    6, 8, 10, AND 12 REFER TO ACROSS TRACK (FOR NORTH &
C                    SOUTH ZONES) OR ZONAL MOTION (FOR EQUATORIAL ZONE).
C
C
C  PRINCIPAL VARIABLES (RETURNED ARGUMENTS):
C
C      ALATS     =   (REAL) (ALATS(I),I=1,6)  ARRAY CONTAINING FORECASTS
C                    OF STORM LATITUDE IN 12 H INTERVALS WHERE I=1 IS
C                    FOR 12 HOUR FORECAST PERIOD, I=2 IS FOR 24 HOUR
C                    PERIOD.........I=6 IS FOR 72 HOUR PERIOD.
C
C      ALONS     =   (REAL) (ALONS(I),I=1,6)  ARRAY CONTAINING FORECASTS
C                    OF STORM LONGITUDES (EAST) IN 12 H INTERVALS WHERE
C                    I=1 IS FOR 12 HOUR FORECAST PERIOD, I=2 IS FOR 24
C                    HOUR PERIOD, .........I=6 IS FOR 72 HOUR PERIOD.
C
C  OTHER VARIABLES:
C
C      LASTHR    =   (INTEGER) GIVES SIZE OF DISP ARRAY (MAXIMUM = 12)
C
C      LL        =   (INTEGER) GIVES SIZE OF ALATS AND ALONS ARRAYS
C                    (MAXIMUM = 6)
C  METHOD:
C
C      1.  USES NAVIGATIONAL MODULE BLKDT2 TO CONVERT FROM DISPLACEMENT
C          TO LATITUDE AND LONGITUDE.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      DIMENSION DISP(12), ALATS(6), ALONS(6)
C
      CALL STHGPR(SLAT00, -SLON00, GRDROT, 1., 0., 0.)
      DO 10 I = 1, 6
         IF(IFIX(DISP(2*I)).EQ.-99.AND.IFIX(DISP(2*I-1)).EQ.-99)GOTO 10
         CALL XY2LLH(DISP(2*I), DISP(2*I - 1), ALATS(I), ALONS(I))
   10 CONTINUE
      RETURN
      END
      SUBROUTINE PPROG (LZ, ACLAT, ACLON, NCYCLE)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            PPROG
C
C  DESCRIPTION:
C      PROGRAM MODULE FOR COMPUTING TROPICAL CYCLONE DISPLACEMENTS BASE
C      ON THE INITIAL DEEP-LAYER-MEAN GEOPOTENTIAL HEIGHT ANALYSIS AND
C     FORECASTS THEREOF.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL PPROG(LZ,ACLAT,ACLON,NCYCLE)
C
C  INPUT FILES:
C
C      CURRENT AND FORECAST FIELDS OF DEEP-LAYER-MEAN GEOPOTENTIAL HT
C      DEPARTURES FROM NORMAL IN 65 X 65 GRID FORMAT. FORECASTS ARE AT
C      12H INTERVALS, 12 THROUGH 72H.  EACH TIME PERIOD, 00H THROUGH 72H
C      (SEVEN FILES) IS A SEPARATE RECORD IN FILE 3.
C
C  COMMON BLOCKS:
C      /BLK03/,/BLK04/,/BLK05/,/BLK06/,/BLK10/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      LZ     =      (INTEGER) INDEX FOR STRATIFICATION ZONE WHERE:
C                    1 = SOUTH ZONE
C                    2 = NORTH ZONE
C                    3 = EQUATORIAL ZONE
C
C      ACLAT  =      (REAL) ARRAY (ACLAT(I),I=1,6) CONTAINING PREVIOUSLY
C                    COMPUTED "FIRST-GUESS" FORECAST OF TROPICAL CYCLONE
C                    LATITUDES AT 12H INTERVALS, 12 THROUGH 72H.
C
C      ACLON  =      (REAL) ARRAY (ACL0N(I),I=1,6) CONTAINING PREVIOUSLY
C                    COMPUTED "FIRST-GUESS" FORECAST OF TROPICAL CYCLONE
C                    LONGITUDES (EAST) AT 12H INTERVALS, 12 THROUGH 72H.
C
C      NCYCLE =      (INTEGER) INDEX FOR ITERATION CYCLE.
C
C  PRINCIPAL VARIABLES (RETURNED IN COMMON BLOCK /BLK06/):
C
C       PDISP  =    (REAL) ARRAY (PDISP(I),I=1,12) GIVING FORECAST
C                    DISPLACEMENTS IN NAUTICAL MILES RETURNED IN COMMON
C                    BLOCK /BLK06/.  INDEXING REFERS TO ORTHOGONAL COM-
C                    PONENT AND TIME PERIOD WHERE ODD NUMBERS ARE FOR
C                    ALONG TRACK OR MERIDIONAL MOTION AND EVEN NUMBERS
C                    ARE FOR ACROSS TRACK OR ZONAL MOTION 12 THROUGH 72H
C
C  OTHER IMPORTANT VARIABLES:
C
C       C        =   (REAL) (((C(I,J,K),K=1,6),J=1,12,),I=1,21) ARRAY
C                    WHICH CONTAINS ALL REGRESSION COEFFICIENTS AND
C                    OTHER CONSTANTS UTILIZED IN PREDICTING MOTION FROM
C                    ANALYSIS FIELDS ALONE AND FROM PERFECT-PROG FIELDS
C                    ALONE.  SUBSCRIPT ADDRESS INDEXING IS AS FOLLOWS:
C
C                    I = INDEX FOR SPECIFYING TYPE OF CONSTANT FOR GIVEN
C                    PREDICTOR NUMBER-SEE SUBPROGRAM BLKDT5 FOR DETAILS.
C
C                    J = INDEX WHICH SPECIFIES ALONG OR ACROSS TRACK (OR
C                    MERIDIONAL/ZONAL) COMPONENT OF MOTION AND FORECAST
C                    INTERVAL, 12 THROUGH 72H.  SEE BLOCK DATA SUBPRO-
C                    GRAM BLKDT5 FOR DETAILS.
C
C                    K = INDEX WHICH FURTHER SPECIFIES STRATIFICATION
C                    ZONE NUMBER 1, 2 OR 3 AND WHETHER ANALYSIS OR PER-
C                    FECT PROG MODE.  SEE BLOCK DATA SUBPROGRAM BLKDT5
C                    FOR DETAILS.
C
C       NP    =      (INTEGER) NUMBER OF GEOPOTENTIAL HEIGHT PREDICTORS
C                    (EXCLUDING INTERCEPT VALUE) FOR THIS K-INDEX. MAXI-
C                    MUM NUMBER OF PREDICTORS FOR ANY GIVEN TIME INTER-
C                    VAL IS 4.  UNUSED CONSTANTS WERE ENTERED IN ARRAY
C                    C(I,J,K) AS MISSING; USING LARGE NUMBER 9999999E+25
C
C       XI    =      (REAL) NUMBER OF 150 NMI GRID POINT INTERVALS IN
C                    THE I-DIRECTION (ACROSS TRACK MOTION FOR ZONES 1
C                    AND 2; ZONAL MOTION FOR ZONE 3).
C
C       YJ    =      (REAL) NUMBER OF 150 NMI GRID POINT INTERVALS IN
C                    THE J-DIRECTION (ALONG TRACK MOTION FOR ZONES 1
C                    AND 2; MERIDIONAL MOTION FOR ZONE 3).
C
C  VARIABLES SAVED IN COMMON BLOCK BLK10 FOR LATER USE:
C
C     HTSAVE(4,12) = (REAL) HEIGHT VALUES.
C
C     GP(4,12,2)   = (REAL) GRID POINT LATITUDES (K=1) AND
C                    LONGITUDES (K=2).
C
C     LSAVE(12) =    (INTEGER) NUMBER OF PREDICTORS FOR GIVEN FORECAST.
C
C  METHOD:
C
C      1.  THIS ROUTINE IS CALLED MORE THAN ONCE AS SPECIFIED BY VARIA-
C          BLE ITER (SEE SUBROUTINE OPTION). ITER IS CURRENTLY SET TO 3.
C          CALLING SEQUENCE NUMBER (1 TO ITER) IS GIVEN BY INCOMING
C          ARGUMENT NCYCLE.
C
C      2.  IN FIRST CALL, FIRST-GUESS OF STORM POSITIONS IS GIVEN BY
C          ARRAYS, ACLAT AND ACLON WHICH RESIDE IN COMMON BLOCK /BLK06/.
C          SUBSEQUENT CALLS USE PREVIOUS LAT/LON OUTPUT (ACPLAT,ACPLON)
C          FROM THIS ROUTINE (PPROG) AS FIRST GUESS.
C
C      3.  CALL TO SUBROUTINE NVNTRY IS MADE.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON/BLK03/
     A          AA12S(21),AX12S(21),AA24S(21),AX24S(21),
     B          AA36S(21),AX36S(21),AA48S(21),AX48S(21),
     C          AA60S(21),AX60S(21),AA72S(21),AX72S(21),
     D          PA12S(21),PX12S(21),PA24S(21),PX24S(21),
     E          PA36S(21),PX36S(21),PA48S(21),PX48S(21),
     F          PA60S(21),PX60S(21),PA72S(21),PX72S(21),
C
     G          AA12N(21),AX12N(21),AA24N(21),AX24N(21),
     H          AA36N(21),AX36N(21),AA48N(21),AX48N(21),
     I          AA60N(21),AX60N(21),AA72N(21),AX72N(21),
     J          PA12N(21),PX12N(21),PA24N(21),PX24N(21),
     K          PA36N(21),PX36N(21),PA48N(21),PX48N(21),
     L          PA60N(21),PX60N(21),PA72N(21),PX72N(21),
C
     M          AM12E(21),AZ12E(21),AM24E(21),AZ24E(21),
     N          AM36E(21),AZ36E(21),AM48E(21),AZ48E(21),
     O          AM60E(21),AZ60E(21),AM72E(21),AZ72E(21),
     P          PM12E(21),PZ12E(21),PM24E(21),PZ24E(21),
     Q          PM36E(21),PZ36E(21),PM48E(21),PZ48E(21),
     R          PM60E(21),PZ60E(21),PM72E(21),PZ72E(21)
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
      COMMON /BLK10/HTSAVE(4,12), GP(4,12,2), LSAVE(12)
C
      DIMENSION ACLAT(6), ACLON(6)
      INTEGER LSAVE
      DIMENSION C(21,12,6)
      EQUIVALENCE (C(1,1,1),AA12S(1))
      DATA BIG/1.0E20/, GSIZE/150./
C
      K = 2*LZ
C
C     DESCRIPTION OF K...
C     K=1      SOUTH ZONE ANALYSIS MODE  K=2 SOUTH ZONE PERFECT-PROG MOD
C     K=3      NORTH ZONE ANALYSIS MODE  K=4 NORTH ZONE PERFECT-PROG MOD
C     K=5 EQUATORIAL ZONE ANALYSIS MODE  K=6 EQTRL ZONE PERFECT-PROG MOD
C
      DO 20 J = 1, LASTHR
         NP = 4
C        NP GIVES NUMBER OF HEIGHT PREDICTORS EXCLUDING INTERCEPT
         IF ( C(21, J, K) .GT. BIG ) NP = 3
         IF ( C(16, J, K) .GT. BIG ) NP = 2
         LSAVE(J) = NP
C        INITIALIZE DISPLACEMENT WITH INTERCEPT VALUE
         PDISP(J) = C(5*NP + 1, J, K)
C        NOW, LOOP THRU EACH OF NP PREDICTORS FOR THIS TIME PERIOD (J),
C        DETERMINE APPROPRIATE HEIGHT VALUE AND COMPUTE FCST
C        DISPLACEMENTS
         DO 10 L = 1, NP
            RC = C(5*L - 4, J, K)
            XI = C(5*L - 2, J, K)/GSIZE
            YJ = C(5*L - 3, J, K)/GSIZE
            CALL GETHT(XI, YJ, J, ACLAT, ACLON, L, RHT)
            HTSAVE(L, J) = RHT
            PDISP(J) = PDISP(J) + RC*RHT
   10    CONTINUE
   20 CONTINUE
      CALL NVNTRY(LSAVE, HTSAVE, NCYCLE + 1, LZ, K, GP, PDISP)
      RETURN
      END
      SUBROUTINE SUMMRY (NZ)
C.........................START PROLOGUE................................
C  SUBPROGRAM NAME:            SUMMRY
C
C  DESCRIPTION:
C
C      WRITES OUT ALL FORECASTS TO DESIGNATED OUTPUT UNIT
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL SUMMRY(NZ)
C
C  INPUT FILES:
C
C      NONE
C  COMMON BLOCKS:
C
C      /BLK05/,/BLK06/,/BLK07/,/BLK08/,/BLK09/,/OUTPUT/,/STMNAM/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C      NZ     =      (INTEGER) INDEX FOR STRATIFICATION ZONE WHERE:
C                    1 = SOUTH ZONE
C                    2 = NORTH ZONE
C                    3 = EQUATORIAL ZONE
C
C  OTHER IMPORTANT VARIABLES:
C
C      SAVE   =      (REAL) ARRAY ((SAVE(I,J),J=1,7),I=1,12) FORECASTS
C                    ARRANGED IN MANNER CONVENIENT FOR PRINTER OUTPUT.
C                    INDEX J REFERS TO TYPE OF OUTPUT AND INDEX I
C                    REFERS TO ORTHOGONAL COMPONENT AND FORECAST
C                    INTERVAL WHERE I = 1, 3, 5, 7, 9, 11 IS FOR ALONG
C                    TRACK OR MERIDIONAL MOTION AND I = 2, 4, 6, 8, 10,
C                    12  IS FOR ACROSS TRACK ORZONAL MOTION FOR TIME
C                    PERIODS 12 THROUGH 72H, RESPECTIVELY.
C
C  METHOD:
C
C      1.  ALL FORECASTS, INCLUDING INTERMEDIATE RESULTS ARE WRITTEN TO
C          UNIT NUMBER NUNIT.
C
C      2.  THIS OUTPUT REQUIRES FULL 132 COLUMNS.
C
C      3.  FIRST PASS THROUGH SAVE ARRAY IS FOR STORM DISPLACEMENTS (IN
C          NAUTICAL MILES) FROM INITIAL STORM POSITION.  SECOND PASS
C          THROUGH SAVE ARRAY IS FOR DISPLACEMENTS CONVERTED TO
C          LATITUDES AND EAST LONGITUDES.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      COMMON /BLK06/ADISP(12), PDISP(12), CDISP(12), ACDISP(12),
     *              ACPDSP(12), DISP(12)
      COMMON /BLK07/PLAT(6), PLON(6), ACLAT(6), ACLON(6), CLAT(6),
     *              CLON(6), ACPLAT(6), ACPLON(6), ALAT(6), ALON(6)
      COMMON /BLK08/NITER
      COMMON /BLK09/TEMP1(12), TEMP2(12), TEMP3(6), TEMP4(6), TEMP5(6),
     *              TEMP6(6)
      COMMON /PUTOUT/NUNIT
      CHARACTER*10 SNAME
C
      COMMON /STMNAM/SNAME
C
      CHARACTER*21 HDNG(7)
      CHARACTER*16 NORS(3)
      CHARACTER*1 EORW(12, 7)
      DIMENSION SAVE(12, 7)
      DATA NORS/'SOUTH-ZONE.     ', 'NORTH-ZONE.     ',
     * 'EQUATORIAL-ZONE.'/
      DATA HDNG/'CLIPER ONLY          ', 'ANALYSIS ONLY        ',
     * 'ANALYSIS+CLIPER      ', 'PERFECT-PROG (PRELIM)',
     * 'PERFECT-PROG (FINAL) ', 'COMBINED (PREMIM)    ',
     * 'COMBINED (FINAL)     '/
C
      NOUT = NUNIT
      WRITE (NOUT, 1000) SNAME, SLAT00, SLON00, IDATIM
      WRITE (NOUT, 1010)
      WRITE (NOUT, 1020) SLAT12, SLON12, SLAT24, SLON24, NORS(NZ)
C     INITIALIZE ARRAY DESIGNATING N OR S LATITUDE  E OR W LONGITUDE
      DO 20 I = 1, 11, 2
         DO 10 J = 1, 7
            EORW(I, J) = 'N'
            EORW(I + 1, J) = 'E'
   10    CONTINUE
   20 CONTINUE
C
      DO 70 M = 1, 2
C        M=1 IS FOR DISPLACEMENTS; M=2 IS FOR LAT/LONS
         IF ( M .EQ. 2 ) THEN
            WRITE (NOUT, 1040)
            DO 30 J = 1, 11, 2
               K = (J + 1)/2
C              LATS
               SAVE(J, 1) = CLAT(K)
               SAVE(J, 2) = ALAT(K)
               SAVE(J, 3) = ACLAT(K)
               SAVE(J, 4) = TEMP3(K)
               SAVE(J, 5) = PLAT(K)
               SAVE(J, 6) = TEMP5(K)
               SAVE(J, 7) = ACPLAT(K)
C              LONS
               SAVE(J + 1, 1) = CLON(K)
               SAVE(J + 1, 2) = ALON(K)
               SAVE(J + 1, 3) = ACLON(K)
               SAVE(J + 1, 4) = TEMP4(K)
               SAVE(J + 1, 5) = PLON(K)
               SAVE(J + 1, 6) = TEMP6(K)
               SAVE(J + 1, 7) = ACPLON(K)
   30       CONTINUE
C
            DO 50 J = 2, 12, 2
               DO 40 K = 1, 7
                  IF ( SAVE(J, K) .GT. 0. ) EORW(J, K) = 'W'
                  IF ( IFIX(SAVE(J - 1, K )) .NE. -99 ) SAVE(J, K)
     *            = ABS(SAVE(J, K))
   40          CONTINUE
   50       CONTINUE
         ELSE
            WRITE (NOUT, 1030)
            DO 60 J = 1, 12
               SAVE(J, 1) = CDISP(J)
               SAVE(J, 2) = ADISP(J)
               SAVE(J, 3) = ACDISP(J)
               SAVE(J, 4) = TEMP1(J)
               SAVE(J, 5) = PDISP(J)
               SAVE(J, 6) = TEMP2(J)
               SAVE(J, 7) = ACPDSP(J)
   60       CONTINUE
         ENDIF
C
         IF ( M .EQ. 1 ) WRITE (NOUT, 1050) (HDNG(K), (SAVE(L, K), L =
     *    1, 12), K = 1, 7)
C
         IF ( M .EQ. 2 ) WRITE (NOUT, 1060) (HDNG(K), (SAVE(L, K), EORW
     *    (L, K), L = 1, 12), K = 1, 7)
C         IF ( M .EQ. 2 ) WRITE (30, 1060) (HDNG(K), (SAVE(L, K), EORW
C     *    (L, K), L = 1, 12), K = 1, 7)
C
   70 CONTINUE
      RETURN
 1000 FORMAT ('0', 16X, 'SUMMARY OF FORECASTS FOR STORM ', A,
     * '  INITIAL STORM POSITION IS', F5.1, 'N', F6.1, 'E',
     * '   DATE-TIME IS ', I8)
 1010 FORMAT (/16X,
     * 'FOR NORTH AND SOUTH ZONES, ALL DISPLACEMENTS ARE RELATIVE TO AVE
     *RAGE STORM HEADING BETWEEN INITIAL AND 12H OLD'
     * /16X,
     * 'POSITIONS.  FOR EQUATORIAL ZONE, ALL DISPLACEMENTS ARE RELATIVE
     *TO A FIXED (SIMULATED) STORM HEADING 0F 360 DEGS.'
     * )
 1020 FORMAT (25X, '12HR OLD POSITION IS', F5.1, 'N', F6.1, 'E',
     * '    24HR OLD POSITION IS', F5.1, 'N', F6.1, 'E', 4X,
     * 'STORM IS IN ', A/)
 1030 FORMAT (/7X,
     * 'FCST DISPLACEMENTS (NMI) 12ATRK  12XTRK  24ATRK  24XTRK  36ATRK
     * 36XTRK  48ATRK  48XTRK  60ATRK  60XTRK  72ATRK  72XTRK'
     * )
 1040 FORMAT (/7X,
     * 'FCST POSITIONS           12LATD  12LONG  24LATD  24LONG  36LATD
     * 36LONG  48LATD  48LONG  60LATD  60LONG  72LATD  72LONG'
     * )
 1050 FORMAT (10X, A, F7.1, 11F8.1)
 1060 FORMAT ((10X, A, F6.1, A, 11(F7.1, A)))
      END
      SUBROUTINE NVNTRY (L, H, INDEX, LZ, KK, GP, D)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            NVNTRY
C  DESCRIPTION:
C
C      PROVIDES DIAGNOSTIC INFORMATION ON GEOPOTENTIAL HEIGHT PREDICTORS
C      USED IN A GIVEN FORECAST CYCLE.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON, (SAIC)
C
C  USAGE (CALLING SEQUENCE):    CALL NVNTRY(L,H,INDEX,KK,GP,D)
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      /BLK03/,/BLK04/,BLK05/,/STMNAM/,/OUTPUT/
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENTS):
C
C      L      =      (INTEGER) ARRAY (L(J),J=1,12) GIVES NUMBER OF GEO-
C                    POTENTIAL HEIGHT PREDICTORS FOR GIVEN ORTHOGONAL
C                    COMPONENT OF MOTION AND FORECAST INTERVAL.  INDICES
C                    1, 3, 5, 7, 9, 11 ARE FOR ALONG TRACK (OR MERIDION-
C                    AL) MOTION) AND INDICES 2, 4, 6, 8, 10, 12 ARE FOR
C                    ACROSS TRACK (OR ZONAL) MOTION FOR TIME PERIODS 12
C                    THROUGH 72H, RESPECTIVELY.
C
C      H      =      (REAL) ARRAY ((H(I,J),J=1,12),I=1,4) PREDICTOR
C                    VALUES, GIVEN AS GEOPOTENTIAL HEIGHT DEPARTURES
C                    FROM NORMAL. INDEX I REFERS TO PREDICTOR NUMBER
C                    WITH TOTAL NUMBER OF PREDICTORS GIVEN BY L ARRAY,
C                    ABOVE.  INDEX J HAS SAME MEANING AS IN ARRAY L.
C
C      INDEX  =      (INTEGER) INDICATOR FOR TYPE OF PREDICTION: INDEX =
C                    1 IS FOR ANALYSIS MODE, INDEX 2, 3, 4 ARE FOR PER-
C                    FECT-PROG MODE WHERE INDEX-1 CORRESPONDS TO ITERA-
C                    TION (FORECAST CYCLE) NUMBER.
C
C      LZ     =      (INTEGER) ZONE NUMBER--CAN BE 1, 2 OR 3, DEPENDING
C                    ON ZONE--SEE SUBROUTINE FOR ZONE DESCRIPTION.
C
C      KK     =      (INTEGER) INDEX FOR ZONE SPECIFICATION AND PREDIC-
C                    TION MODE (ANALYSIS OR PERFECT-PROG).  KK VARIES
C                    1 THROUGH 6.  SEE SUBPROGRAM BLKDT5 FOR DETAILS.
C                    LZ AND KK ARE RELATED SUCH THAT LZ = (KK+1)/2.
C
C
C      GP     =      (REAL) ARRAY GP(((I,J,K),K=1,2),J=1,12),I=1,4)
C                    GIVES LATITUDES (K=1) AND LONGITUDES (K=2) OF UP TO
C                    I = 4 PREDICTOR GRID POINTS FOR ALONG TRACK (OR
C                    MERIDIONAL) MOTION 12 THROUGH 72H (J = 1, 3, 5, 7,
C                    9, 11) AND FOR ACROSS TRACK (OR ZONAL) MOTION 12
C                    THROUGH 72H ( J = 2, 4, 6, 8, 10, OR 12).
C
C       D     =      (REAL) ARRAY (D(J),J=1,12) FORECAST STORM DISPLACE-
C                    MENTS IN NMI FROM INITIAL POSITION.  INDEXING PARA-
C                    METER J HAS SAME MEANING AS IN ARRAY L, ABOVE.
C  OTHER IMPORTANT VARIABLES:
C
C       C     =      (REAL) ARRAY (((C(I,J,K),K=1,6),J=1,12),I=1,21)
C                    RESIDENCE OF MANY REQUIRED CONSTANTS NEEDED BY PRO-
C                    GRAM.  SEE BLKDT5 FOR DESCRIPTION OF SUBSCRIPTING.
C
C  METHOD:
C
C      1.  DISPLAYS AVERAGE VALUES OF PREDICTORS BASED ON DEVELOPMENTAL
C          DATA AND COMPARES THIS TO PRESENT VALUE OF PREDICTOR.
C
C      2.  COMPUTES AND DISPLAYS NUMBER OF STANDARD DEVIATIONS PRESENT
C          PREDICTOR VALUE DEVIATES FROM AVERAGE (DEVELOPMENT) VALUE.
C
C  LANGUAGE:                       FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      COMMON/BLK03/
     A          AA12S(21),AX12S(21),AA24S(21),AX24S(21),
     B          AA36S(21),AX36S(21),AA48S(21),AX48S(21),
     C          AA60S(21),AX60S(21),AA72S(21),AX72S(21),
     D          PA12S(21),PX12S(21),PA24S(21),PX24S(21),
     E          PA36S(21),PX36S(21),PA48S(21),PX48S(21),
     F          PA60S(21),PX60S(21),PA72S(21),PX72S(21),
C
     G          AA12N(21),AX12N(21),AA24N(21),AX24N(21),
     H          AA36N(21),AX36N(21),AA48N(21),AX48N(21),
     I          AA60N(21),AX60N(21),AA72N(21),AX72N(21),
     J          PA12N(21),PX12N(21),PA24N(21),PX24N(21),
     K          PA36N(21),PX36N(21),PA48N(21),PX48N(21),
     L          PA60N(21),PX60N(21),PA72N(21),PX72N(21),
C
     M          AM12E(21),AZ12E(21),AM24E(21),AZ24E(21),
     N          AM36E(21),AZ36E(21),AM48E(21),AZ48E(21),
     O          AM60E(21),AZ60E(21),AM72E(21),AZ72E(21),
     P          PM12E(21),PZ12E(21),PM24E(21),PZ24E(21),
     Q          PM36E(21),PZ36E(21),PM48E(21),PZ48E(21),
     R          PM60E(21),PZ60E(21),PM72E(21),PZ72E(21)
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
      COMMON /BLK05/SLAT00, SLON00, SLAT12, SLON12, SLAT24, SLON24,
     *              AHP12H, ASP12H, IDATIM, WIND, KYR, MO, KDA, IUTC,
     *              GRDROT
      COMMON /PUTOUT/NUNIT
      CHARACTER*10 SNAME
C
      COMMON /STMNAM/SNAME
C
      CHARACTER*35 HDNG(4)
      CHARACTER*16 NORS(3)
      CHARACTER*13 AORXT(2)
      CHARACTER*1 EORW
      INTEGER L(12)
      DIMENSION H(4, 12), GP(4, 12, 2), D(12)
      DIMENSION C(21,12,6)
      EQUIVALENCE (C(1,1,1),AA12S(1))
C
      DATA NORS/'SOUTH-ZONE.     ', 'NORTH-ZONE.     ',
     * 'EQUATORIAL-ZONE.'/
C
      DATA AORXT/'ALONG-TRACK, ', 'ACROSS-TRACK,'/
      DATA HDNG(1)/'ANALYSIS MODE                      '/
      DATA HDNG(2)/'PERFECT-PROG MODE, FIRST ITERATION '/
      DATA HDNG(3)/'PERFECT-PROG MODE, SECOND ITERATION'/
      DATA HDNG(4)/'PERFECT-PROG MODE, THIRD ITERATION '/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      NOUT = NUNIT
      WRITE (NOUT, 1000) NORS(LZ), HDNG(INDEX)
      WRITE (NOUT, 1010) SNAME, IDATIM, SLAT00, SLON00, GRDROT
      WRITE (NOUT, 1020)
      DO 20 I = 1, LASTHR
         M = (I + 1)/2*12
         K = MOD(I - 1, 2) + 1
         WRITE (NOUT, 1030) M, AORXT(K)
         NP = L(I)
         DO 10 J = 1, NP
            IF ( J .EQ. 1 ) WRITE (NOUT, 1040)
            FCST = H(J, I)*C(5*J - 4, I, KK)
            DIF = H(J, I) - C(5*J - 1, I, KK)
            GRDLON = GP(J, I, 2)
            EORW = 'W'
            IF ( GRDLON .LT. 0. ) EORW = 'E'
            GRDLON = ABS(GRDLON)
            SDN = DIF/C(5*J, I, KK)
            WRITE (NOUT, 1050) C(5*J - 2, I, KK), C(5*J - 3, I, KK), GP
     *       (J, I, 1), GRDLON, EORW, H(J, I), C(5*J - 1, I, KK), DIF,
     *       C(5*J, I, KK), SDN, C(5*J - 4, I, KK), FCST
   10    CONTINUE
         WRITE (NOUT, 1060) C(5*NP + 1, I, KK), D(I)
   20 CONTINUE
      RETURN
 1000 FORMAT ('1', 9X, 'PREDICTOR INVENTORY FOR ', A, A)
 1010 FORMAT (10X, 'STORMNAME = ', A, I8, '   INITIAL POSITION IS ',
     * F4.1, 'N', F6.1, 'E', '  GRID ROTATION IS ', F5.1)
 1020 FORMAT (10X,
     * 'NOTE.....PREDICTOR LOCATIONS (I = ACROSS TRACK, J = ALONG TRACK)
     * ARE RELATIVE TO ROTATED GRID (GRDROT) '
     * /10X,
     * 'AND STORM POSITION (FORECAST POSITIONS FOR PERFECT-PROG MODE, IN
     *ITIAL POSITION FOR ANALYSIS MODE).'
     * /)
 1030 FORMAT (8X, I2, 'HR ', A)
 1040 FORMAT (10X,
     * 'I(NM)  J(NM)  LAT    LON     GPH   MEAN HT  GPH-MEAN HT  STND DV
     *N  NBR SD    REG COEF    REG COEF*GPH'
     * )
 1050 FORMAT (8X, 2F7.0, F5.1, 'N', F6.1, A, 2F8.1, 2F11.1, F8.1,
     * E16.7, F9.1, 'NM')
 1060 FORMAT (45X, 'INTERCEPT AND TOTAL DISPLACEMENT ARE ', E15.7,
     * F9.1, 'NM')
      END
      SUBROUTINE FINDLO (TYLAT,TYLON,NGPLR,ALATNG,ALONNG,NLOWS)
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:            FINDLO
C
C  DESCRIPTION:                PRINCIPLE DRIVER FOR FINDING LOCATION
C                              OF NEAREST CLOSED VORTEX WITHIN NOGAPS
C                              FIELDS TO THE JTWC92 FORECAST POSITION.
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON
C
C  USAGE (CALLING SEQUENCE):    CALL FINDLO(TYLAT,TYLON,NGPLR,ALATNG,
C                                           ALONNG,CNTRP,NLOWS)
C
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      NONE
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C         TYLAT  -  "CORRECT" LATITUDE OF TYPHOON
C         TYLON  -  "CORRECT" LONGITUDE OF TYPHOON
C                   (NEGATIVE FOR EAST LONGITUDES)
C         NGPLR  -  NUMBER OF GRID POINTS LEFT, RIGHT, UP, DOWN
C                   FROM CONTROL GRID POINT TO BE INCLUDED IN SEARCH.
C                   VALUE OF 2 GIVES A 25 POINT NEST,VALUE OF 3 GIVES
C                   A 49 POINT NEST, ETC.
C
C  PRINCIPAL VARIABLES (OUTGOING ARGUMENT):
C
C         ALATNG -  LATITUDE OF NOGAPS TYPHOON CENTER
C         ALONNG -  LONGITUDE OF NOGAPS TYPHOON CENTER
C                   (RETURNED AS WEST LONG)
C         CNTRP  -  CENTRAL HEIGHT IN WHATEVER UNITS FIELD IS IN
C         NLOWS  -  NUMBER OF LOWS FOUND IN GRID NEST
C                   NOTE: NLOWS IS FOR PC VERSION OF JTWC92
C
C  OTHER IMPORTANT VARIABLES:
C
C         HTS    -  ARRAY(65X65) OF DLM FIELDS
C
C  METHOD: FINDS I,J ON GRID BASED ON TYPHOON LAT/LON THEN SEARCHS
C          NOGAPS FIELDS WITHIN NGPLR VARIABLE (SET AT 5 MAY 1992)
C          GRID POINTS FROM CENTER FOR CLOSED VORTEX.
C
C
C
C  LANGUAGE:                        FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      COMMON /BLK04/HTS(4225), NFLDS, LFP, LASTHR
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      READ (92) HTS
C FIND FLOATING POINT LOCATION OF JTWC92 LOW ON 65 X 65 GRID
      CALL GET(TYLAT,TYLON,HTS,DI,XXFI,XXFJ)
      CALL LO(HTS,65,65,1.0,1.0,XXFI,XXFJ,NGPLR,ALATNG,ALONNG,NLOWS)
      RETURN
C
      END
      SUBROUTINE LO (Z,IX,JY,DX,DY,XXFI,XXFJ,NGPLR,ALAT,ALON,N)
C
C.........................START PROLOGUE................................
C  SUBPROGRAM NAME:            LO
C  DESCRIPTION:                FIND LOW PRESSURE CENTERS IN ARRAY Z
C                              HAVING X AND Y DIMENSIONS OF IX AND JY
C                              DY AND DX ARE DISTANCE BETWEEN GRID
C                              POINTS IN RESPECTIVE DIRECTIONS, X AND Y.
C                              XXFI AND XXFJ ARE LOCATION OF OPERATIONAL
C                              TYPHOON CENTER IN GRID UNITS (1 TO 65).
C
C
C  ORIGINAL PROGRAMMER, DATE:   CHARLES J. NEUMANN, JANUARY, 1991 (SAIC)
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON
C
C  USAGE (CALLING SEQUENCE):    CALL LO(Z,IX,JY,DX,DY,XXFI,XXFJ,NGPLR,
C                                       ALAT,ALON,N)
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C         DX     -  DISTANCE BETWEEN GRID POINTS IN X DIRECTION
C         DY     -  DISTANCE BETWEEN GRID POINTS IN Y DIRECTION
C         XXFI   -  FIRST DIMENSION LOCATION OF TROPICAL CYCLONE
C         XXFJ   -  SECOND DIMENSION LOCATION OF TROPICAL CYCLONE
C         IX     -  FIRST DIMENSION OF ARRAY Z
C         JY     -  SECOND DIMENSION OF ARRAY Z
C         NGPLR  -  NUMBER OF GRID POINTS LEFT, RIGHT, UP, DOWN
C                   FROM CONTROL GRID POINT TO BE INCLUDED IN SEARCH.
C                   VALUE OF 2 GIVES A 25 POINT NEST,VALUE OF 3 GIVES
C                   A 49 POINT NEST, ETC.
C         Z      -  ARRAY OF DEEP-MEAN-LAYER HEIGHTS
C
C  PRINCIPAL VARIABLES (OUTGOING ARGUMENT):
C
C         ALAT   -  LATITUDE OF THE NOGAPS LOW
C         ALON   -  LONGITUDE OF THE NOGAPS LOW
CCC       CNTRP  -  HEIGHT VALUE OF NOGAPS LOW CENTER
C         N      -  NUMBER OF NOGAPS LOW CENTERS FOUND
C
C  METHOD: FINDS I,J ON GRID BASED ON TYPHOON LAT/LON THEN SEARCHS
C          NOGAPS FIELDS WITHIN NGPLR VARIABLE (5 PTS MAY 1992)
C          GRID POINTS FROM CENTER FOR CLOSED VORTEX. CURRENT SETUP
C          IS FOR 65 X 65 POLAR STEREOGRAPIC WITH GRID SPACING
C          OF 381 KM AT 60N AND WITH BOTTOM OF GRID PERPENDICULAR TO
C          80W.  LOWER LEFT HAND GRID POINT IS (1,1), UPPER RIGHT IS
C          (65,65) N POLE IS (33,33)
C
C
C  LANGUAGE:                        FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
      DIMENSION Z(IX,JY),TEMPLA(20),TEMPLO(20),TEMPP(20)
C DISTANCE BETWEEN GRID POINTS IN KM
      XMESHL=381
C ORIENTATION OF GRID
      ORIENT=80
C INITIALIZE OUTGOING ARGUMENTS IN CASE NO LOW IS FOUND
      ALAT=-99.9
      ALON=-99.9
CCC   CNTRP=-99.9
      N=0
      SMALL=999999
C
C GET CLOSEST GRID POINT TO INCOMING XXFI AND XXFJ
      IXXF=XXFI+.5
      JXXF=XXFJ+.5
C SET UP LOOP VALUES WITH GRID NEST CENTERED ON ABOVE VALUE
      INITL=JXXF-NGPLR
      IF(INITL.LT.2)INITL=2
      LASTL=JXXF+NGPLR
      IF(LASTL.GT.64)LASTL=64
      INITK=IXXF-NGPLR
      IF(INITK.LT.2)INITK=2
      LASTK=IXXF+NGPLR
      IF(LASTK.GT.64)LASTK=64
C SEARCH FOR LOW
      DO 100 L=INITL,LASTL
        DO 90 K=INITK,LASTK
          IF(Z(K,L).GE.Z(K+1,L)) GOTO 90
          IF(Z(K,L).GE.Z(K,L+1)) GOTO 90
          IF(Z(K,L).GT.Z(K,L-1)) GOTO 90
          IF(Z(K,L).GT.Z(K-1,L)) GOTO 90
          IF(Z(K,L).GE.Z(K-1,L+1)) GOTO 90
          IF(Z(K,L).GE.Z(K+1,L+1)) GOTO 90
          IF(Z(K,L).GT.Z(K-1,L-1)) GOTO 90
          IF(Z(K,L).GT.Z(K+1,L-1)) GOTO 90
C
C CENTER LOCATED NEAR GRID POINT X=K, Y=L. NOW FIND EXACT CENTER USING
C QUADRATIC INPERPOLATION
          ZMIN=99999.
C ITERATIONS SET AT INCREMENTS OF 0.05 GRID-POINT UNITS FROM -1 TO +1
C GRID POINTS
C
          DO 80 I=1,41
            Q=FLOAT(I-21)/20.
            QM=1.-Q
            QP=1.+Q
            DO 70 J=1,41
              P=FLOAT(J-21)/20.
              PM=1.-P
              PP=1.+P
              ROW1=-P*PM/2.*Z(K-1,L-1)+PM*PP*Z(K-1,L+0)+P*PP/2.*
     $             Z(K-1,L+1)
              ROW2=-P*PM/2.*Z(K+0,L-1)+PM*PP*Z(K+0,L+0)+P*PP/2.*
     $             Z(K+0,L+1)
              ROW3=-P*PM/2.*Z(K+1,L-1)+PM*PP*Z(K+1,L+0)+P*PP/2.*
     $             Z(K+1,L+1)
              ANS=-Q*QM/2.*ROW1+QM*QP*ROW2+Q*QP/2.*ROW3
              IF(ANS.LT.ZMIN)GOTO 50
              GOTO 70
   50         ZMIN=ANS
              QSAVE=Q
              PSAVE=P
   70       CONTINUE
   80     CONTINUE
          N=N+1
C
          FI=FLOAT(K-1)*DX+QSAVE*DX+1.0
          FJ=FLOAT(L-1)*DY+PSAVE*DY+1.0
          TEMPP(N)=ZMIN
          IF(ZMIN.LT.SMALL)THEN
            SMALL=ZMIN
            NSAVE=N
          ENDIF
C GET LAT/LON OF LOW CENTER(S)
          CALL W3FB05(FI-33.,FJ-33.,XMESHL,ORIENT,TEMPLA(N),TEMPLO(N))
   90   CONTINUE
  100 CONTINUE
C IF THERE IS MORE THAN ONE LOW, NEED T0 SELECT ONE WITH LOWEST CENTP
      IF(N.EQ.0)RETURN
      ALAT=TEMPLA(NSAVE)
      ALON=TEMPLO(NSAVE)
CCC   CNTRP=TEMPP(NSAVE)
      RETURN
      END
      SUBROUTINE W3FB05 (XI,XJ,XMESHL,ORIENT,ALAT,ALONG)
C
C.........................START PROLOGUE................................
C
C  SUBPROGRAM NAME:             W3FB05
C
C  DESCRIPTION:                 CONVERTS THE COORDINATES OF A LOCATION
C                               FROM THE GRID(I,J) COORDINATE SYSTEM
C                               OVERLAID ON THE POLAR STEREOGRAPHIC MAP
C                               PROJECTION TRUE AT 60 N OR S TO THE
C                               NATURAL CORRDINATE SYSTEM OF LAT/LON ON
C                               THE EARTH.
C
C  ORIGINAL PROGRAMMER, DATE:   ALBION D. TAYLOR, NOAA, MARCH, 1982
C
C  CURRENT PROGRAMMER:          JAMES M. SHELTON
C
C  USAGE (CALLING SEQUENCE):    CALL W3FB05(FI-33.,FJ-33.,XMESHL,ORIENT,
C                               TEMPLA(N),TEMPLO(N))
C
C
C  INPUT FILES:
C
C      NONE
C
C  COMMON BLOCKS:
C
C      NONE
C
C.........................MAINTENANCE SECTION...........................
C
C  PRINCIPAL VARIABLES (INCOMING ARGUMENT):
C
C       XI     -  I OF THE POINT RELATIVE TO THE N OR S POLE
C                 (USE XI-33.).
C       XJ     -  J OF THE POINT RELATIVE TO THE N OR S POLE
C       XMESHL -  MESH LENGTH OF GRID IN KM AT 60 N(<0 IF S HEM)
C       ORIENT -  ORIENTATION WEST LONGITUDE OF THE GRID
C
C
C  PRINCIPAL VARIABLES (OUTGOING ARGUMENT):
C
C       XLAT   -  LATITUDE IN DEGREES (< 0 IF SHEM)
C       XLONG  -  LONGITUDE IN DEGREES WEST
C
C
C  OTHER IMPORTANT VARIABLES:
C
C  METHOD:    UTILIZES SHERICAL TRIANGLES AND NAVIGATIONAL PRINCIPLES
C
C
C  LANGUAGE:                        FORTRAN 77
C
C  RECORD OF CHANGES:
C
C
C.........................END PROLOGUE..................................
C
      DEGPRD=57.29578
      EARTHR=6371.2
      GI2=((1.86603*EARTHR)/(XMESHL))**2
      R2=XI*XI+XJ*XJ
      IF(R2.NE.0.)GOTO 100
      ALONG=0.
      ALAT=90.
      IF(XMESHL.LT.0.)ALAT=-ALAT
      GOTO 400
C
  100 CONTINUE
      ALAT=ASIN((GI2-R2)/(GI2+R2))*DEGPRD
      ANGLE=DEGPRD*ATAN2(XJ,XI)
      IF(ANGLE.LT.0.0)ANGLE=ANGLE+360.
      IF(XMESHL.LT.0.)GOTO 200
      ALONG=270.+ORIENT-ANGLE
      GOTO 300
C
  200 CONTINUE
      ALONG=ANGLE+ORIENT-270.
      ALAT=-(ALAT)
  300 CONTINUE
      IF(ALONG.LT.0.)ALONG=ALONG+360.
      IF(ALONG.GE.360.)ALONG=ALONG-360.
C
  400 CONTINUE
      RETURN
      END
