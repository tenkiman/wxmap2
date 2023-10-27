      SUBROUTINE SORTRL (NCOUNT,NYR,NDAY,MYR,MDAY,MHR,CLT,CLN,WND,
     .                   ALT,ALN,CNAM,ERR)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  SORTRL
C
C  DESCRIPTION:  SORT BASED UPON ERROR DISTANCE, LEAST FIRST, KEEP
C                ASSOCIATED ARRAY VALUES IN SAME SEQUENCE AS EEROR
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL SORTRL (NCOUNT,NYR,NDAY,MYR,MDAY,MHR,CLT,CLN,WND,
C                       ALT,ALN,CNAM,ERR)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     NCOUNT       INIT          IN     NUMBER OF VALUES FOR SORTING
C        NYR       INIT        IN/OUT   ASSOCIATED ARRAY
C       NDAY       INIT        IN/OUT   ASSOCIATED ARRAY
C        MYR       INIT        IN/OUT   ASSOCIATED ARRAY
C       MDAY       INIT        IN/OUT   ASSOCIATED ARRAY
C        MHR       INIT        IN/OUT   ASSOCIATED ARRAY
C        CLT       REAL        IN/OUT   ASSOCIATED ARRAY
C        CLN       REAL        IN/OUT   ASSOCIATED ARRAY
C        WND       REAL        IN/OUT   ASSOCIATED ARRAY
C        ALT       REAL        IN/OUT   ASSOCIATED ARRAY
C        ALN       REAL        IN/OUT   ASSOCIATED ARRAY
C       CNAM       CHAR        IN/OUT   ASSOCIATED ARRAY
C        ERR       REAL        IN/OUT   ERROR, NM
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C            CTV     CHAR       TEMPORARY VARIABLE FOR SORT
C             ER     REAL       TEMPORARY VARIABLE FOR SORT
C            ITV     INIT       TEMPORARY VARIABLE FOR SORT
C            RTV     REAL       TEMPORARY VARIABLE FOR SORT
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
c
c     Modified to use new data format,  6/98   A. Schrader
C
C
C...................END PROLOGUE.......................................
C
C                   FORMAL PARAMETERS
C
      CHARACTER*8 CNAM(6)
C
      INTEGER  NYR(6),NDAY(6),MYR(6),MDAY(6),MHR(6)
C
      REAL  CLT(6),CLN(6),WND(6),ALT(6),ALN(6),ERR(6)
C
C                   LOCAL VARIABLES
C
      CHARACTER*8 CTV
C
      INTEGER  N, J, ITV
C
      REAL  ER, RTV
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      DO 120 N=1, NCOUNT-1
        ER = ERR(N)
        DO 110 J=N+1, NCOUNT
          IF (ER .GT. ERR(J)) THEN
            ITV     = NYR(N)
            NYR(N)  = NYR(J)
            NYR(J)  = ITV
            ITV     = NDAY(N)
            NDAY(N) = NDAY(J)
            NDAY(J) = ITV
            ITV     = MYR(N)
            MYR(N)  = MYR(J)
            MYR(J)  = ITV
            ITV     = MDAY(N)
            MDAY(N) = MDAY(J)
            MDAY(J) = ITV
            ITV     = MHR(N)
            MHR(N)  = MHR(J)
            MHR(J)  = ITV
            RTV     = CLT(N)
            CLT(N)  = CLT(J)
            CLT(J)  = RTV
            RTV     = CLN(N)
            CLN(N)  = CLN(J)
            CLN(J)  = RTV
            RTV     = WND(N)
            WND(N)  = WND(J)
            WND(J)  = RTV
            RTV     = ALT(N)
            ALT(N)  = ALT(J)
            ALT(J)  = RTV
            RTV     = ALN(N)
            ALN(N)  = ALN(J)
            ALN(J)  = RTV
            CTV     = CNAM(N)
            CNAM(N) = CNAM(J)
            CNAM(J) = CTV
            ERR(N)  = ERR(J)
            ERR(J)  = ER
            ER      = ERR(N)
          ENDIF
  110   CONTINUE
  120 CONTINUE
      RETURN
C
      END
      SUBROUTINE MAKFCT (NFCS,KSTRC,CFSTRT,CFRECR,KDST,KDRC,CDSTRT,
     .                   CDRECR)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  MAKFCT
C
C  DESCRIPTION:  CALCULATE 12-HOUR FORECASTS FOR STRAIGHT AND
C                RECURVER TYPE TROPICAL CYCLONES
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL MAKFCT (NFCS,KSTRC,CFSTRT,CFRECR)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       NFCS       INIT        IN/OUT   NUMBER OF FORECAST
C      KSTRC       INIT        IN/OUT   FLAG FOR TYPE OF CYCLONES TO
C                                       PROCESS  4 - ALL
C                                                3 - RECURVER & STRAIGHT
C                                                2 - RECURVER ONLY
C                                                1 - STRAIGHT ONLY
C     CFSTRT       CHAR        IN/OUT   ARRAY FOR STRAIGHT FORECAST
C     CFRECR       CHAR        IN/OUT   ARRAY FOR RECURVER FORECAST
C       KDST       INIT          IN     FLAG FOR WINDOW SIZE, STRAIGHT
C       KDRC       INIT          IN     FLAG FOR WINDOW SIZE, RECURVER
C     CDSTRT       CHAR        IN/OUT   ARRAY FOR STRAIGHT DIAGNOSTICS
C     CDRECR       CHAR        IN/OUT   ARRAY FOR RECURVER DIAGNOSTICS
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C       BCLMA    ALT12A    REAL      IN     STRAIGHT LATITUDE FORECAST,
C                                           DEG (-SH)
C       BCLMA    ALN12A    REAL      IN     STRAIGHT LONGITUDE FORECAST,
C                                           DEG (360 E)
C       BCLMA      E12A    REAL      IN     "FIX" ERROR, STRAIGHT, NM
C       BCLMA     MR12A    INIT      IN     COUNT OF STRAIGHT 12-HR
C                                           VALUES
C       BCLMA    WND12A    REAL      IN     FORECAST 12-HR WIND CHANGE,
C                                           KT
C       BCLMA    ALT24A    REAL      IN     STRAIGHT LATITUDE FORECAST,
C                                           DEG (-SH)
C       BCLMA    ALN24A    REAL      IN     STRAIGHT LONGITUDE FORECAST,
C                                           DEG (360 E)
C       BCLMA      E24A    REAL      IN     "FIX" ERROR, STRAIGHT, NM
C       BCLMA     MR24A    INIT      IN     COUNT OF STRAIGHT 24-HR
C                                           VALUES
C       BCLMA    WND24A    REAL      IN     FORECAST 12-HR WIND CHANGE,
C                                           KT
C       BCLMB    ALT12B    REAL      IN     RECURVER LATITUDE FORECAST,
C                                           DEG (-SH)
C       BCLMB    ALN12B    REAL      IN     RECURVER LONGITUDE FORECAST,
C                                           DEG (360 E)
C       BCLMB      E12B    REAL      IN     "FIX" ERROR, RECURVER, NM
C       BCLMB     MR12B    INIT      IN     COUNT OF RECURVER 12-HR
C                                           VALUES
C       BCLMB    WND12B    REAL      IN     FORECAST 12-HR WIND CHANGE,
C                                           KT
C       BCLMB    ALT24B    REAL      IN     RECURVER LATITUDE FORECAST,
C                                           DEG (-SH)
C       BCLMB    ALN24B    REAL      IN     RECURVER LONGITUDE FORECAST,
C                                           DEG (360 E)
C       BCLMB      E24B    REAL      IN     "FIX" ERROR, RECURVER, NM
C       BCLMB     MR24B    INIT      IN     COUNT OF RECURVER 24-HR
C                                           VALUES
C       BCLMB    WND24B    REAL      IN     FORECAST 12-HR WIND CHANGE,
C                                           KT
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C         FORMAT OF CFSTRT AND CFRECR
C             1         2         3         4         5         6
C    1234567890123456789012345678901234567890123456789012345678901234567
C     TYAN TYPE XXXYXXXXY ZZZ XXXYXXXXY ZZZ XXXYXXXXY ZZZ XXXYXXXXY ZZZ
C             7         8
C           8901234567890
C           XXXYXXXXY ZZZ
C
C     IDENTIFIER - TYAN
C           TYPE - STRT FOR STRAIGHT AND RECR FOR RECURVER
C      XXXYXXXXY - LATITUDE-LONGITUDE TIMES TEN, Y IS N OR S AND E OR W
C            ZZZ - WIND SPEED, KT
C
Cx    MISSING TAU IS:  999Y9999Y 999
cx    missing tau is:    0y   0y   0
C     FORECAST TAUS ARE:  12, 24, 36, 48, 72
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C          CONSEN     OBTAIN CONSENSUS OF POSITION
C          FORCHR     CONVER FORECAST TO CHARACTER STRING
C          LODAFS     LOAD ANALOG FORECAST STRING
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C           CLAT     REAL       ARRAY FOR ALL FORECAST LATITUDES,  DEG
C           CLON     REAL       ARRAY FOR ALL FORECAST LONGITUDES, DEG
C           CWND     REAL       ARRAY FOR ALL FORECAST 12-HR WIND
C                               CHANGES, KT
C           CERR     REAL       ARRAY FOR ALL "FIX" POSITION ERRORS, NM
C         DWNDST     REAL       AVERAGE OF CONSENSUS WIND DIFFERENCES,
C                               FOR STRAIGHT, KT
C         DWNDRT     REAL       AVERAGE OF CONSENSUS WIND DIFFERENCES,
C                               FOR RECURVER, KT
C         FLATST     REAL       CONSENSUS STRAIGHT LATITUDE, DEG (- SH)
C         FLONST     REAL       CONSENSUS STRAIGHT LONGITUDE, DEG (360 E
C         FLATRT     REAL       CONSENSUS RECURVER LATITUDE, DEG (- SH)
C         FLONRT     REAL       CONSENSUS RECURVER LONGITUDE, DEG (360 E
C          KSTRT     INIT       FLAG, STRAIGHT, 0 -BAD
C          KRECR     INIT       FLAG, RECURVER, 0 -BAD
C         STRING     CHAR       FORECAST IN CHARACTER MODE
C         WINDRT     REAL       FORECAST MAX WIND SPEED, RECURVER, KT
C         WINDST     REAL       FORECAST MAX WIND SPEED, STRAIGHT, KT
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
C                   FORMAL PARAMETERS
C
      CHARACTER*80 CFSTRT, CFRECR, CDSTRT, CDRECR
C
      INTEGER  NFCS, KSTRC, KDST, KDRC
C
C                   LOCAL VARIABLES
C
      CHARACTER*13 STRING
C
      INTEGER  KSTRT, KRECR, N, NC, NPST, NSST, NPRC, NSRC
C
      REAL CLAT(10), CLON(10), CWND(10), CERR(10)
      REAL FLATST, FLONST, DWNDST, WINDST
      REAL FLATRC, FLONRC, DWNDRC, WINDRC
C
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW24  - PAST 24 HR EAST/WEST HEMISPHERE INDOCATOR, E OR W
C
      CHARACTER CNAME*7, CDTG*8, CNS*1, CEW*1, EW12*1, EW24*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12,EW24
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG (+ NH, - SH)
C   FLN   - FIX LONGITUDE, DEG (EAST)
C   PLT12 - PAST 12 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN12 - PAST 12 HR LONGITUDE, DEG (EAST)
C   PLT24 - PAST 24 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN24 - PAST 24 HR LONGITUDE, DEG (EAST)
C   HD12S - HEADING  FROM -12 TO FIX LOCATION (STRAIGHT), DEG
C   DT12S - DISTANCE FROM -12 TO FIX LOCATION (STRAIGHT), NM
C   HD24S - HEADING  FROM -24 TO FIX LOCATION (STRAIGHT), DEG
C   DT24S - DISTANCE FROM -24 TO FIX LOCATION (STRAIGHT), NM
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12,PLT24,PLN24
     .             ,HD12S,DT12S,HD24S,DT24S
C
C
C                   EXPLANATION OF /POSITR/ VARIABLES FOR RECURVERS
C
C   NREGNR - NUMBER OF BASIN FROM FIX POSITION
C   FLTR   - INITIAL LATITUDE, DEG
C   FLNR   - INITIAL LONGITUDE, DEG
C   PLT12R - PAST 12 HR LATITUDE,  DEG
C   PLN12R - PAST 12 HR LONGITUDE, DEG
C   PLT24R - PAST 24 HR LATITUDE,  DEG
C   PLN24R - PAST 24 HR LONGITUDE, DEG
C   HD12R  - HEADING  FROM -12 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -12 TO FIX LOCATION (RECURVER), NM
C   HD24R  - HEADING  FROM -24 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -24 TO FIX LOCATION (RECURVER), NM
C
      COMMON/POSITR/ NREGNR,FLTR,FLNR,FWDR,PLT12R,PLN12R,PLT24R,PLN24R,
     .               HD12R,DT12R,HD24R,DT24R
C
C  <<CHANGE NOTICE>>  $TYANB101  (21 JUL 1993)  --  HAMILTON,H.
C           ADD HEADING AND DISTANCE TO DCREASE RUNNING TIME.
C           ADD /POSITR/ TO ALLOW FORECASTING BY TYAN93.
C
C                   EXPLANATION OF /CBCLM/ VARIABLES
C
C   CYCYYX  - NAME/IDENTIFICATION OF CLIMO CYCLONE
C       YY  - HOUR, 12 OR 24
C        X  - A - S-TYPE (STRAIGHT)
C             B - R-TYPE (RECURVER)
C             C - O-TYPE (OTHER)
C             D - ALL-TYPES (S, R AND O)
C
      CHARACTER*8 CYC12A,CYC24A,CYC12B,CYC24B,CYC12C,CYC24C,
     .            CYC12D,CYC24D
C
      COMMON/CBCLM/ CYC12A(6),CYC24A(6),CYC12B(6),CYC24B(6),
     .              CYC12C(6),CYC24C(6),CYC12D(6),CYC24D(6)
C
C                   EXPLANATION OF /BCLMX/ VARIABLES
C
C   NYRYYX - YEAR OF INITIAL POSITION
C   NDYYYX - JULIAN DAY OF INITIAL POSITION
C   MYRYYX - YEAR OF POSITION
C   DYJYYX - JULIAN DAY OF POSITION
C   MHRYYX - HOUR OF POSITION
C   CLTYYX - LATITUDE OF POSITION (+ NH, - SH)
C   CLNYYX - LONGITUDE OF POSITION (0 - 360 EAST)
C   WNDYYX - ANALOG FORECAST 12-HR WIND SPEED CHANGE, KT
C   EYYX   - WEIGHTED ERROR DIFFERENCE BETWEEN TRANSPOSED CLIMATOLOGY
C            AND YY HOUR POSITION LATER
C   ALTYXX - ANALOG TAU 12 FORECAST OF LATITUDE, DEG
C   ALNYYX - ANALOG TAU 12 FORECAST OF LONGITUDE, DEG
C   MRYYX  - NUMBER OF VALUES
C      YY  - HOUR, 12 OR 24
C       X  - A - S-TYPE (STRAIGHT)
C            B - R-TYPE (RECURVER)
C            C - O-TYPE (OTHER)
C            D - ALL-TYPES (S, R AND O)
C
      COMMON/BCLMA/ NYR12A(6),NDY12A(6),MYR12A(6),MDY12A(6),MHR12A(6),
     .              CLT12A(6),CLN12A(6),WND12A(6),E12A(6),
     .              ALT12A(6),ALN12A(6),MR12A,
     .              NYR24A(6),NDY24A(6),MYR24A(6),MDY24A(6),MHR24A(6),
     .              CLT24A(6),CLN24A(6),WND24A(6),E24A(6),
     .              ALT24A(6),ALN24A(6),MR24A
      COMMON/BCLMB/ NYR12B(6),NDY12B(6),MYR12B(6),MDY12B(6),MHR12B(6),
     .              CLT12B(6),CLN12B(6),WND12B(6),E12B(6),
     .              ALT12B(6),ALN12B(6),MR12B,
     .              NYR24B(6),NDY24B(6),MYR24B(6),MDY24B(6),MHR24B(6),
     .              CLT24B(6),CLN24B(6),WND24B(6),E24B(6),
     .              ALT24B(6),ALN24B(6),MR24B
      COMMON/BCLMC/ NYR12C(6),NDY12C(6),MYR12C(6),MDY12C(6),MHR12C(6),
     .              CLT12C(6),CLN12C(6),E12C(6),MR12C,
     .              NYR24C(6),NDY24C(6),MYR24C(6),MDY24C(6),MHR24C(6),
     .              CLT24C(6),CLN24C(6),E24C(6),MR24C
      COMMON/BCLMD/ NYR12D(6),NDY12D(6),MYR12D(6),MDY12D(6),MHR12D(6),
     .              CLT12D(6),CLN12D(6),E12D(6),MR12D,
     .              NYR24D(6),NDY24D(6),MYR24D(6),MDY24D(6),MHR24D(6),
     .              CLT24D(6),CLN24D(6),E24D(6),MR24D
C
C
C  <<CHANGE NOTICE>>  $TYANB201  (21 JUL 1993)  --  HAMILTON,H.
C           ADD WNDYYX, ALTYYX, ALNYYX, WHERE YY IS 12
C           OR 24 AND X IS A OR B, TO ALLOW FORECASTING BY TYAN93
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (KSTRC .NE. 2) THEN
C
C                   ESTIMATE TAU 12 POSITION FOR TYPE STRAIGHT
C
        KSTRT  = -1
        WINDST = -99.0
        IF ((MR12A +MR24A) .GT. 1) THEN
          DO 110 N=1, MR12A
            CLAT(N) = ALT12A(N)
            CLON(N) = ALN12A(N)
            CWND(N) = WND12A(N)
            CERR(N) = E12A(N)
  110     CONTINUE
          NC = MR12A
          DO 120 N=1, MR24A
            NC = NC +1
            CLAT(NC) = ALT24A(N)
            CLON(NC) = ALN24A(N)
            CWND(NC) = WND24A(N)
            CERR(NC) = E24A(N)
  120     CONTINUE
C
C                   OBTAIN CONSENSUS VALUES
C
          CALL CONSEN (CLAT,CLON,CWND,CERR,NC,FLATST,FLONST,DWNDST,
     .                 NPST,NSST)
          IF (FWD.GT.0.0 .AND. ABS (DWNDST).LT.50.0)
     .       WINDST = FWD +DWNDST
        ELSEIF (MR12A .EQ. 1) THEN
          FLATST = ALT12A(1)
          FLONST = ALN12A(1)
          NPST   = 1
          IF (FWD.GT.0.0 .AND. ABS (WND12A(1)).LT.50.0) THEN
            WINDST = FWD +WND12A(1)
            NSST   = 1
          ELSE
            NSST = 0
          ENDIF
        ELSEIF (MR24A .EQ. 1) THEN
          FLATST = ALT24A(1)
          FLONST = ALN24A(1)
          NPST   = 1
          IF (FWD.GT.0.0 .AND. ABS (WND24A(1)).LT.50.0) THEN
            WINDST = FWD +WND24A(1)
            NSST   = 1
          ELSE
            NSST = 0
          ENDIF
        ELSE
          KSTRT = 0
        ENDIF
      ELSE
        KSTRT = 0
      ENDIF
      IF (KSTRT .NE. 0) THEN
C
C                   GOOD 12 HOUR STRAIGHT FORECAST, LOAD STRING
C                           (OMIT TAU 60 HR FORECAST)
C
        IF (NFCS .NE. 5) CALL FORCHR (FLATST,FLONST,WINDST,STRING)
        IF (NFCS .NE. 6) THEN
C
C                   BACK LOAD FOR NEXT STRAIGHT FORECAST
C
          PLT24 = PLT12
          PLN24 = PLN12
          PLT12 = FLT
          PLN12 = FLN
          FLT   = FLATST
          FLN   = FLONST
          FWD   = WINDST
        ENDIF
      ELSE
C
C                   MISSING 12 HOUR STRAIGHT FORECAST
C
cx      STRING = '999' // CNS // '9999' // CEW // ' 999'
        string = '  0' // cns // '   0' // cew // '   0'
        NPST   = 0
        NSST   = 0
      ENDIF
C
C * * * * * * * *   LOAD STRAIGHT FORECAST INTO CFSTRT   * * * * * * * *
C                        (OMIT TAU 60 HR FORECAST)
C
      IF (NFCS .NE. 5) CALL LODAFS (NFCS,STRING,CFSTRT)
C
C
C * * * * * * * *  LOAD STRAIGHT DIAGOSTICS INTO CDSTRT  * * * * * * * *
C
      CALL LODDSR (KDST,NPST,NSST,NFCS,CDSTRT)
C
      IF (KSTRC .NE. 1) THEN
C
C                   ESTIMATE TAU 12 POSITION FOR TYPE RECURVER
C
        KRECR  = -1
        WINDRC = -99.0
        IF ((MR12B +MR24B) .GT. 1) THEN
          DO 210 N=1, MR12B
            CLAT(N) = ALT12B(N)
            CLON(N) = ALN12B(N)
            CWND(N) = WND12B(N)
            CERR(N) = E12B(N)
  210     CONTINUE
          NC = MR12B
          DO 220 N=1, MR24B
            NC = NC +1
            CLAT(NC) = ALT24B(N)
            CLON(NC) = ALN24B(N)
            CWND(NC) = WND24B(N)
            CERR(NC) = E24B(N)
  220     CONTINUE
C
C                   OBTAIN CONSENSUS VALUES
C
          CALL CONSEN (CLAT,CLON,CWND,CERR,NC,FLATRC,FLONRC,DWNDRC,
     .                 NPRC,NSRC)
          IF (FWDR.GT.0.0 .AND. ABS (DWNDRC).LT.50.0)
     .       WINDRC = FWDR +DWNDRC
        ELSEIF (MR12B .EQ. 1) THEN
          FLATRC = ALT12B(1)
          FLONRC = ALN12B(1)
          NPRC   = 1
          IF (FWDR.GT.0.0 .AND. ABS (WND12B(1)).LT.50.0) THEN
            WINDRC = FWDR +WND12B(1)
            NSRC   = 1
          ELSE
            NSRC = 0
          ENDIF
        ELSEIF (MR24B .EQ. 1) THEN
          FLATRC = ALT24B(1)
          FLONRC = ALN24B(1)
          NPRC   = 1
          IF (FWDR.GT.0.0 .AND. ABS (WND24B(1)).LT.50.0) THEN
            WINDRC = FWDR +WND24B(1)
            NSRC   = 1
          ELSE
            NSRC = 0
          ENDIF
        ELSE
          KRECR = 0
        ENDIF
      ELSE
        KRECR = 0
      ENDIF
      IF (KRECR .NE. 0) THEN
C
C                   GOOD 12 HOUR RECURVER FORECAST, LOAD STRING
C                           (OMIT TAU 60 HR FORECAST)
C
        IF (NFCS .NE. 5) CALL FORCHR (FLATRC,FLONRC,WINDRC,STRING)
        IF (NFCS .NE. 6) THEN
C
C                   BACK LOAD FOR NEXT RECURVER FORECAST
C
          PLT24R = PLT12R
          PLN24R = PLN12R
          PLT12R = FLTR
          PLN12R = FLNR
          FLTR   = FLATRC
          FLNR   = FLONRC
          FWDR   = WINDRC
        ENDIF
      ELSE
C
C                   MISSING 12 HOUR RECURVER FORECAST
C
cx      STRING = '999' // CNS // '9999' // CEW // ' 999'
        string = '  0' // cns // '   0' // cew // '   0'
        NPRC   = 0
        NSRC   = 0
      ENDIF
C
C * * * * * * * *   LOAD RECURVER FORECAST INTO CFRECR   * * * * * * * *
C                        (OMIT TAU 60 HR FORECAST)
C
      IF (NFCS .NE. 5) CALL LODAFS (NFCS,STRING,CFRECR)
C
C * * * * * * * *  LOAD RECURVER DIAGNOSTICS INTO CDRECR  * * * * * * *
C
      CALL LODDSR (KDRC,NPRC,NSRC,NFCS,CDRECR)
C
      IF (NFCS .NE. 6) THEN
C
C * * * * * * * *   SET KSTRC FOR NEXT FORECAST   * * * * * * * * * * *
C
        IF (KSTRT.NE.0 .AND. KRECR.NE.0) THEN
C                   SET FOR BOTH STRAIGHT AND RECURVER
          KSTRC = 3
        ELSEIF (KRECR .NE. 0) THEN
C                   SET FOR RECURVER ONLY
          KSTRC = 2
        ELSEIF (KSTRT .NE. 0) THEN
C                   SET FOR STRAIGHT ONLY
          KSTRC = 1
        ELSE
C
C                   SET STRING WITH MISSING VALUES FOR CFSTRT AND CFRECR
C
cx        STRING = '999' // CNS // '9999' // CEW // ' 999'
          string = '  0' // cns // '   0' // cew // '   0'
C
C                   SET DIAGNOSTIC VALUES TO ZERO FOR CDSTRT AND CDRECR
C
          KDST = 0
          NPST = 0
          NSST = 0
          KDRC = 0
          NPRC = 0
          NSRC = 0
          DO 310 N=NFCS+1, 6
            IF (N .NE. 5) THEN
C                   OMIT TAU 60
              CALL LODAFS (N,STRING,CFSTRT)
              CALL LODAFS (N,STRING,CFRECR)
            ENDIF
            CALL LODDSR (KDST,NPST,NSST,N,CDSTRT)
            CALL LODDSR (KDRC,NPRC,NSRC,N,CDRECR)
  310     CONTINUE
C
C * * * * * * * *   TERMINATE FORECASTS   * * * * * * * * * * * * * * *
C
          NFCS = 6
        ENDIF
      ENDIF
      RETURN
C
      END
      SUBROUTINE CONSEN (FLT,FLN,WND,ERR,NC,CLT,CLN,CWND,NCP,NCW)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  CONSEN
C
C  DESCRIPTION:  CALCULATE CONSENSUS FORECASTS
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL CONSEN (FLT,FLN,WND,ERR,NC,CLT,CLN,CWND)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C        FLT       REAL          IN     ARRAY OF FORECAST LATITUDE,  DEG
C        FLN       REAL          IN     ARRAY OF FORECAST LONGITUDE, DEG
C        WND       REAL          IN     ARRAY OF FORECAST MAXIMUM WIND
C                                       DIFFERENCE OVER NEXT 12 HRS, KT
C        ERR       REAL          IN     ERROR ARRAY OF "FIX" LOCATIONS,
C                                       NM
C         NC       INIT          IN     NUMBER OF FORECASTS
C        CLT       REAL          OUT    CONSENSUS LATITUDE,  DEG
C        CLN       REAL          OUT    CONSENSUS LONGITUDE, DEG
C       CWND       REAL          OUT    AVERAGE OF CONSENSUS MAX WIND
C                                       CHANGE FROM "FIX" TIME TO
C                                       TAU 12 HR, KT
C        NCP       INIT          OUT    NUMBER OF CYCLONES USED FOR
C                                       CALCULATING POSITION
C        NCW       INIT          OUT    NUMBER OF CYCLONES USED FOR
C                                       CALCULATING MAX WIND SPEED
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C          TRKDST     CALCULATE HEADING AND DISTANCE, HEADING IS NOT
C                     USED, NM
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C            ALT     REAL       WORKING STORAGE FOR LATITUDE, DEG (-SH)
C            ALN     REAL       WORKING STORAGE FOR LONGITUDE DEG (360 E
C          AVGLT     REAL       AVERAGE LATITUDE,  DEG (- SH)
C          AVGLN     REAL       AVERAGE LONGITUDE, DEG (360 E)
C           DIFF     REAL       TEMPORARY STORAGE OF WEIGHTED "FIX"
C                               ERROR, NM, OR DIFFERENCE BETWEEN
C                               FORECAST LAT/LON AND AVERAGE LAT/LON, NM
C            DIS     REAL       WORKING STORAGE FOR DISTANCE, NM
C             DT     REAL       RHUMB-LINE DISTANCE, NM
C             HD     REAL       RHUMB-LINE HEADING, DEG (NOT USED)
C           NPTR     INIT       ARRAY OF POINTERS
C          ITEMP     INIT       TEMPORARY VARIABLE FOR SORTING
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
C                   FORMAL PARAMETERS
C
      INTEGER NC, NCP, NCW
C
      REAL FLT(NC), FLN(NC), WND(NC), ERR(NC), CLT, CLN, CWND
C
C                   LOCAL VARIABLES
C
      INTEGER  NPTR(10), ITEMP, N, J
C
      REAL  ALT(10), ALN(10), DIS(10), AVGLT, AVGLN, DIFF, HD, DT
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      NCP = MIN0 (NC,10)
      IF (NCP .GT. 3) THEN
C
C                   INITIALIZE POINTERS
C
        DO 110 N=1, NCP
          NPTR(N) = N
  110   CONTINUE
C
C                   LIMIT INITIAL GROUP SIZE TO TOP SEVEN
C
        IF (NCP .GT. 7) THEN
C
C                   SORT BASED UPON 12/24 HR WEIGHTED ERROR, LEAST FIRST
C
          DO 130 N=1, NCP -1
            DIFF = ERR(NPTR(N))
            DO 120 J=N+1, NCP
              IF (ERR(NPTR(J)) .LT. DIFF) THEN
                ITEMP   = NPTR(N)
                NPTR(N) = NPTR(J)
                DIFF    = ERR(NPTR(N))
                NPTR(J) = ITEMP
              ENDIF
  120       CONTINUE
  130     CONTINUE
C                   LIMIT MAXIMUM NUMBER OF CYCLONES TO 7
          NCP = 7
        ENDIF
C
C * * * * * * * *   OBTAIN CONSENSUS FOR FORECAST POSITION  * * * * * *
C
  200   CONTINUE
C
C                   CALCULATE GROUP AVERAGE LAT/LON
C
        AVGLT = 0.0
        AVGLN = 0.0
        DO 210 N=1, NCP
          AVGLT = AVGLT +FLT(NPTR(N))
          AVGLN = AVGLN +FLN(NPTR(N))
  210   CONTINUE
        AVGLT = AVGLT/NCP
        AVGLN = AVGLN/NCP
C
C                   OBTAIN RUNNING AVERAGES WITH ONE POSITION OMITTED
C
        DO 230 N=1, NCP
          ALT(NPTR(N)) = 0.0
          ALN(NPTR(N)) = 0.0
          DO 220 J=1, NCP
            IF (J .NE. N) THEN
              ALT(NPTR(N)) = ALT(NPTR(N)) +FLT(NPTR(J))
              ALN(NPTR(N)) = ALN(NPTR(N)) +FLN(NPTR(J))
            ENDIF
  220     CONTINUE
          ALT(NPTR(N)) = ALT(NPTR(N))/(NCP -1)
          ALN(NPTR(N)) = ALN(NPTR(N))/(NCP -1)
  230   CONTINUE
C
C                   CALCULATE DIFFERENCE BETWEEN GROUP AVERAGE AND
C                   RUNNING AVERAGES
C
        DO 240 N=1, NCP
          CALL TRKDST (AVGLT,AVGLN,ALT(NPTR(N)),ALN(NPTR(N)),HD,DT)
          DIS(NPTR(N)) = ABS (DT)
  240   CONTINUE
C
C                   SORT ON DIFFERENCE, LEAST FIRST
C
        DO 260 N=1, NCP -1
          DIFF = DIS(NPTR(N))
          DO 250 J=N+1, NCP
            IF (DIS(NPTR(J)) .LT. DIFF) THEN
              ITEMP   = NPTR(N)
              NPTR(N) = NPTR(J)
              DIFF    = DIS(NPTR(N))
              NPTR(J) = ITEMP
            ENDIF
  250     CONTINUE
  260   CONTINUE
C
C                   REMOVE LAT/LON CAUSING GREATEST DIFFERENCE
C
        NCP = NCP -1
C
C * * * * * * * *   BASE CONSENSUS ON MAXIMUM OF FIVE ESTIMATES  * * * *
C
        IF (NCP .GT. 5) GOTO 200
C
C * * * * * * * *   LOAD CLT/CLN WITH CONSENSUS LAT/LON  * * * * * * *
C
        CLT = ALT(NPTR(NCP+1))
        CLN = ALN(NPTR(NCP+1))
C
C                   CALCULATE AVERAGE WIND FROM CONSENSUS
C
        CWND = 0.0
        NCW  = 0
        DO 270 N=1, NCP
          IF (ABS (WND(NPTR(N))) .LT. 50.0) THEN
            CWND = CWND +WND(NPTR(N))
            NCW  = NCW +1
          ENDIF
  270   CONTINUE
        IF (NCW .GT. 1) THEN
          CWND = CWND/NCW
        ELSEIF (NCW .EQ. 0) THEN
          CWND = -99.0
        ENDIF
C
      ELSEIF (NCP .GT. 0) THEN
C
C * * * * * * * *   CALCUALTE AVERAGE OF THREE OR LESS  * * * * * * * *
C
        CLT  = 0.0
        CLN  = 0.0
        CWND = 0.0
        NCW  = 0
        DO 310 N=1, NCP
          CLT  = CLT +FLT(N)
          CLN  = CLN +FLN(N)
          IF (ABS (WND(N)) .LT. 50.0) THEN
            CWND = CWND +WND(N)
            NCW = NCW +1
          ENDIF
  310   CONTINUE
        CLT  = CLT/NCP
        CLN  = CLN/NCP
        IF (NCW .GT. 1) THEN
          CWND = CWND/NCW
        ELSEIF (NCW .EQ. 0) THEN
          CWND = -99.0
        ENDIF
C
      ELSE
C
C                   INDICATE ERROR IN INDEX NC
C
        CLT  =  -99.0
        CLN  = -999.0
        CWND =  -99.0
        NCP  =    0
        NCW  =    0
      ENDIF
      RETURN
C
      END
      SUBROUTINE FORCHR (FLT,FLN,WND,STR)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  FORCHR
C
C  DESCRIPTION:  LOAD STR WITH CHARACTER VALUES OF FLT, FLN AND WND
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL FORCHR (FLT,FLN,WND,STR)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C        FLT       REAL          IN     FORECAST LATITUDE,  DEG
C        FLN       REAL          IN     FORECAST LONGITUDE, DEG
C        WND       REAL          IN     FORECAST MAX WIND SPEED, KT
C        STR       CHAR          OUT    CHARACTER STRING OF FORECAST
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:   NONE
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C           IFLT     INIT       NEAREST ABSOLUTE LATITUDE TIMES 10
C           IFLN     INIT       NEAREST ABSOLUTE LONGITUDE TIMES 10
C           IWND     INIT       NEAREST WHOLE WIND SPEED
C           IDKT     INIT       REMAINDERING OF IWND WITH 5
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
C                   FORMAL PARAMETERS
C
      CHARACTER*13 STR
C
      REAL  FLT, FLN, WND
C
C                   LOCAL VARIABLES
C
      INTEGER  IFLT, IFLN, IWND, IDKT
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      STR  = ' '
      IFLT = NINT (10.0*ABS (FLT))
      WRITE (STR(1:3),'(I3.3)') IFLT
      IF (FLT .GE. 0.0) THEN
        STR(4:4) = 'N'
      ELSE
        STR(4:4) = 'S'
      ENDIF
      IFLN = NINT (10.0*FLN)
      IF (IFLN .LE. 1800) THEN
        STR(9:9) = 'E'
      ELSE
        IFLN = 3600 -IFLN
        STR(9:9) = 'W'
      ENDIF
      WRITE (STR(5:8),'(I4.4)') IFLN
      IF (WND .GT. 0.0) THEN
C                   MAKE WIND NEAREST MULTIPLE OF 5
        IWND = NINT (WND)
        IDKT = MOD (IWND,5)
        IWND = 5*(IWND/5)
        IF (IDKT .GT. 2) IWND = IWND +5
      ELSE
C                   WIND IS MISSING, SO SET TO MISSING VALUE
        IWND = 999
      ENDIF
      WRITE (STR(11:13),'(I3.3)') IWND
      RETURN
C
      END
      SUBROUTINE LODAFS (N,CSHORT,CLONG)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  LODAFS
C
C  DESCRIPTION:  LOAD SHORT STRING OF FORECAST INTO LONG STRING OF ALL
C                FORECASTS
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:      NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:    NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:     OPSPL1/MT1731
C
C  USAGE:  CALL LODAFS (N,CSHORT,CLONG)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C          N       INIT          IN     NUMBER OF FORECAST
C     CSHORT       CHAR          IN     SHORT STRING OF FORECAST
C      CLONG       CHAR        IN/OUT   LONG STRING OF FORECASTS
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:   NONE
C
C  LOCAL VARIABLES:  NONE
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C                      Sampson 7/7/95  Assign blanks in string
C
C...................END PROLOGUE.......................................
C
cx    CHARACTER CSHORT*13, CLONG*80
      character*13 cshort
      character*80 clong
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (N .EQ. 1) THEN
        CLONG(12:24) = CSHORT
	clong(25:25) = ' '
      ELSEIF (N .EQ. 2) THEN
        CLONG(26:38) = CSHORT
	clong(39:39) = ' '
      ELSEIF (N .EQ. 3) THEN
        CLONG(40:52) = CSHORT
	clong(53:53) = ' '
      ELSEIF (N .EQ. 4) THEN
        CLONG(54:66) = CSHORT
	clong(67:67) = ' '
      ELSEIF (N .EQ. 6) THEN
        CLONG(68:80) = CSHORT
      ENDIF
      RETURN
C
      END
      SUBROUTINE LODDSR (KW,KP,KS,NF,STRING)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  LODDSR
C
C  DESCRIPTION:  LOAD STRING WITH WINDOW, POSITION AND MAX WIND SPEED
C                DESCRIPTORS
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL LODDSR (KW,KP,KS,NF,STRING)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C        KW        INIT          IN     COUNT OF PASS THRU CLIMATOLOGY
C        KP        INIT          IN     COUNT OF CYCLONES FOR POSITION
C        KS        INIT          IN     COUNT OF CYCLONES FOR MAX WIND
C                                       SPEED
C        NF        INIT          IN     COUNT OF FORECAST
C    STRING        CHAR         IN/OUT  DIAGNOSTIC TABLE VALUES
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          CKW       CHAR       COUNT OF PASSES THRU CLIMATOLOGY 1 OR 2
C                               EXPRESSED IN CHARACTER MODE, N OR W
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C                      Sampson 7/7/95  Assign blanks in string
C
C...................END PROLOGUE.......................................
C
C                   FORMAL PARAMETERS
C
      CHARACTER*80 STRING
C
      INTEGER KW, KP, KS, NF
C
C                   LOCAL VARIABLES
C
      CHARACTER*1 CKW
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (KW .EQ. 1) THEN
        CKW = 'N'
      ELSEIF (KW .EQ. 2) THEN
        CKW = 'W'
      ELSE
        CKW = ' '
      ENDIF
      IF (NF .EQ. 1) THEN
        WRITE (STRING(12:16),9010) CKW,KP,KS
	string (17:17) = ' '
      ELSEIF (NF .EQ. 2) THEN
        WRITE (STRING(18:22),9010) CKW,KP,KS
	string (17:17) = ' '
      ELSEIF (NF .EQ. 3) THEN
        WRITE (STRING(24:28),9010) CKW,KP,KS
	string (29:29) = ' '
      ELSEIF (NF .EQ. 4) THEN
        WRITE (STRING(30:34),9010) CKW,KP,KS
	string (35:35) = ' '
      ELSEIF (NF .EQ. 5) THEN
        WRITE (STRING(36:40),9010) CKW,KP,KS
	string (41:41) = ' '
      ELSEIF (NF .EQ. 6) THEN
        WRITE (STRING(42:46),9010) CKW,KP,KS
      ENDIF
 9010 FORMAT (A1,1X,I1,1X,I1)
      RETURN
C
      END
      SUBROUTINE DSLTLN (SLAT,SLON,HEAD,DIST,ELAT,ELON)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  DSLTLN
C
C  DESCRIPTION:  CALCULATE ELAT,ELON GIVEN RHUMB-LINE HEADING (HEAD)
C                AND DISTANCE (DIST) FROM SLAT,SLON
C
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL DSLTLN (SLAT,SLON,HEAD,DIST,ELAT,ELON)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       SLAT       REAL          IN     STARTING LATITUDE,  DEG (-SH)
C       SLON       REAL          IN     STARTING LONGITUDE, DEG (360 E)
C       HEAD       REAL          IN     HEADING FROM SLAT,SLON, DEG TRUE
C       DIST       REAL          IN     RHUMB DISTANCE, NM
C       ELAT       REAL          OUT    ENDING LATITUDE,  DEG (-SH)
C       ELON       REAL          OUT    ENDING LONGITUDE, DEG (360 E)
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         DEGRAD     REAL       CONVERSION FACTOR, DEG TO RADIANS
C           DLON     REAL       DELTA LONGITUDE BETWEEN SLON AND ELON,
C                               DEG
C         HDGRAD     REAL       0.5 TIMES DEGRAD
C           HDRD     REAL       HEADING EXPRESSED IN RADIANS
C           ICRS     INIT       NEARST WHOLE HEADING, DEG
C           INIL     INIT       FLAG, 0 - CALCULATE FACTORS
C         RADDEG     REAL       CONVERSION FACTOR, RADIANS TO DEG
C         RAD045     REAL       45 DEGREES EXPRESSED IN RADIANS
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
C                   FORMAL PARAMETERS
C
      REAL  SLAT,SLON,HEAD,DIST,ELAT,ELON
C
C                   LOCAL VARIABLES
C
      INTEGER  INIL, ICRS
C
      REAL  RADDEG,DEGRAD,HDGRAD,RAD045,DLON,HDRD
C
C                   SAVE FLAG AND FACTORS BETWEEN SUBROUTINE CALLS
C
      SAVE INIL, RADDEG, DEGRAD, HDGRAD, RAD045
C
      DATA INIL/0/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (INIL .EQ. 0) THEN
        INIL = -1
        DEGRAD = ACOS (-1.0)/180.0
        HDGRAD = 0.5*DEGRAD
        RAD045 = 45.0*DEGRAD
        RADDEG = 1.0/DEGRAD
      ENDIF
C
      ICRS = NINT (HEAD)
      IF (ICRS.EQ.90 .OR. ICRS.EQ.270) THEN
        DLON = DIST/(60.0*COS (SLAT*DEGRAD))
C                   LONGITUDE IS IN DEGREES EAST, 0.0 TO 360.0
        IF (ICRS .EQ. 270) THEN
          ELON = SLON -DLON
        ELSE
          ELON = SLON +DLON
        ENDIF
        ELAT = SLAT
      ELSE
        HDRD = HEAD*DEGRAD
        ELAT = SLAT +(DIST*COS(HDRD)/60.0)
        IF (MOD (ICRS,180) .NE. 0) THEN
C                   FOLLOWING TEST NOT REQUIRED FOR TROPICAL CYCLONES
CCC       IF (ABS (ELAT) .GT. 89.0) ELAT = SIGN (89.0,ELAT)
          ELON = SLON +RADDEG*(ALOG (TAN (RAD045 +HDGRAD*ELAT))
     .            -ALOG (TAN (RAD045 +HDGRAD*SLAT)))*TAN (HDRD)
        ELSE
          ELON = SLON
        ENDIF
      ENDIF
      RETURN
C
      END
      PROGRAM TYAN93
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  TYAN93
C
C  DESCRIPTION:  PROVIDE JTWC/NWOC ETC. LIST OF CLIMATOLOGY TROPICAL
C                CYCLONES THAT BEST MATCH THE PAST 12-HR AND 24-HR
C                WORKING BEST TRACK PROVIDED IN ARQ MESSAGE
C                PROVIDE FORECASTS OF POSITION AND MAX WIND SPEED EVERY
C                12 HOURS THROUGH 72 HOURS.
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  USES FNOC STANDARD ARQ AND CLIMATOLGY DATABASE FORMATS
C                 CHARACTERISTICS OF NOS/BE OPERATING SYSTEM ARE USED.
C                 USES FNOC FNWCLIB FOR UTILITY SUBROUTINES.
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  UNIX
C
C  LIBRARIES OF RESIDENCE:  
C
C  USAGE:       TYAN93 WP0195
C
C  PARAMETERS:  NONE
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES OF LISTED COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C      CNSEW     CNAME     CHAR      IN      TROPICAL CYCLONE NAME/ID
C                CDTG      CHAR      IN      CYCLONE DTG (YYMMDDHH) OF
C                                            PRESENT POSITION
C                CNS       CHAR      IN      N OR S FOR LATITUDE
C                EW12      CHAR      IN      E OR W FOR LONGITUDE, -12HR
C                EW24      CHAR      IN      E OR W FOR LONGITUDE, -24HR
C      CBCLM     CYC12A    CHAR      IN      12HR ARRAY OF CLIMATOLOGY
C                                            STRAIGHT CYCLONE NAMES
C                CYC24A    CHAR      IN      24HR ARRAY OF CLIMATOLOGY
C                                            STRAIGHT CYCLONE NAMES
C                CYC12B    CHAR      IN      12HR ARRAY OF CLIMATOLOGY
C                                            RECURVER CYCLONE NAMES
C                CYC24B    CHAR      IN      24HR ARRAY OF CLIMATOLOGY
C                                            RECURVER CYCLONE NAMES
C                CYC12C    CHAR      IN      12HR ARRAY OF CLIMATOLOGY
C                                            OTHER CYCLONE NAMES
C                CYC24C    CHAR      IN      24HR ARRAY OF CLIMATOLOGY
C                                            OTHER CYCLONE NAMES
C                CYC12D    CHAR      IN      12HR ARRAY OF CLIMATOLOGY
C                                            TOTAL CYCLONE NAMES
C                CYC24D    CHAR      IN      24HR ARRAY OF CLIMATOLOGY
C                                            TOTAL CYCLONE NAMES
C      BCLMA     NYR12A    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (S)
C                NDY12A    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (S)
C                MYR12A    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (S)
C                MDY12A    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (S)
C                MHR12A    INIT      IN      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (S)
C                NYR24A    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (S)
C                NDY24A    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (S)
C                MYR24A    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (S)
C                MDY24A    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (S)
C                MHR24A    INIT      IN      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (S)
C      BCLMB     NYR12B    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (R)
C                NDY12B    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (R)
C                MYR12B    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (R)
C                MDY12B    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (R)
C                MHR12B    INIT      IN      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (R)
C                NYR24B    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (R)
C                NDY24B    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (R)
C                MYR24B    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (R)
C                MDY24B    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (R)
C                MHR24B    INIT      IN      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (R)
C      BCLMC     NYR12C    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (O)
C                NDY12C    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (O)
C                MYR12C    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (O)
C                MDY12C    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (O)
C                MHR12C    INIT      IN      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (O)
C                NYR24C    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (O)
C                NDY24C    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (O)
C                MYR24C    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (O)
C                MDY24C    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (O)
C                MHR24C    INIT      IN      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (O)
C      BCLMD     NYR12D    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (T)
C                NDY12D    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (T)
C                MYR12D    INIT      IN      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (T)
C                MDY12D    INIT      IN      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (T)
C                MHR12D    INIT      IN      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (T)
C                NYR24D    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (T)
C                NDY24D    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (T)
C                MYR24D    INIT      IN      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (T)
C                MDY24D    INIT      IN      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (T)
C                MHR24D    INIT      IN      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (T)
C      POSIT     NREGN     INIT      IN      REGION-BASIN INDICATOR
C                FLT       REAL      IN      PRESENT CYCLONE LATITUDE
C                FLN       REAL      IN      PRESENT CYCLONE LONGITUDE
C                FWD       REAL      IN      PRESENT MAXIMUM WIND SPEED
C                PLT12     REAL      IN      PAST 12-HR LATITUDE
C                PLN12     REAL      IN      PAST 12-HR LONGITUDE
C                PLT24     REAL      IN      PAST 24-HR LATITUDE
C                PLN24     REAL      IN      PAST 24-HR LONGITUDE
C
C  FILES:
C    NAME     UNIT   ATTRIBUTE  USAGE         DESCRIPTION
C   -------  -----   ---------  ------   ---------------------
C  b??????.dat  92   SEQUENTIAL   IN     CARQ REQUEST
C  ???????       2   SEQUENTIAL   IN     CLIMATOLOGY DATA BASE
C   SCREEN      *    SEQUENTIAL   OUT    MATCHING CYCLONES
C  tyan93.dbg   13   SEQUENTIAL   OUT    DEBUGGING DATA
C
C  DATA BASES:  NO TABLE-DRIVEN DATA BASE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C     BAD ARQ MESSAGE          TERMINATE PROCESSING
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         BSTCLM      PROVIDE MATCHING OF CLIMATOLGY TRACKS AND
C                     WORKING-BEST TRACK
C         HEDING      WRITE HEADING LINE FOR CVQCFC
C         JLTOMD      CONVERT YEAR AND JULIAN DAY TO MONTH AND DAY
C         MAKFCT      MAKE 12-HOUR FORECASTS OF POSITION AND WIND SPEED
C         REDARQ      READ ARQ MESSAGE
C         TRKDST      GIVEN TWO POSITIONS, CALCUALTE TRACK AND DISTANCE
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         AIDNAM     CHAR       TROPICAL CYCLONE OBJECTIVE AID NAME
C         CDSTRT     CHAR       DIAGNOSTIC STRING FOR STRAIGHT
C         CDRECR     CHAR       DIAGNOSTIC STRING FOR RECURVER
C         CDTG12     CHAR       TEMPORARY STORAGE FOR NEXT "FIX" DTG
C         CFSTRT     CHAR       FORECAST STRING FOR STRAIGHT
C         CFRECR     CHAR       FORECAST STRING FOR RECURVER
C         COUNT      CHAR       COUNT OF MATCHED CLIMATOLOGY CYCLONES
C         DIST       REAL       DISTANCE IN NM BETWEEN TWO POSITIONS
C         DSTLAT     REAL       LATITUDE  WINDOW, DEGREES
C         DSTLON     REAL       LONGITUDE WINDOW, DEGREES
C         DSTLT      REAL       LATITUDE  WINDOW, DEG
C         DSTLN      REAL       LONGITUDE WINDOW, DEG
C         HEAD       REAL       HEADING FROM POSITION ONE TO TWO, DEG
C         IERR1      INIT       ARQ MESSAGE ERROR FLAG, 0 - NO ERROR
C         ITAU       INIT       DIFFERENCE IN HOURS BETWEEN POSITIONS
C         JDAY       INIT       JULIAN DAY OF BEST CLIMATOLOGY POSITION
C         JMON       INIT       MONTH OF BEST CLIMATOLOGY POSITION
C         KDAY       INIT       JULIAN DAY OF FIRST CLIMATOLOGY POSITION
C         KDRC       INIT       NUMBER OF PASSES USED FOR RECURVER
C         KDST       INIT       NUMBER OF PASSES USED FOR STRAIGHT
C         KMON       INIT       MONTH OF FIRST CLIMATOLOGY POSITION
C         KSTRC      INIT       FLAG FOR TYPE(S) OF CYCLONES TO PROCESS
C                                  4 - PROCESS S, R AND O TYPES
C                                  3 - PROCESS S AND R TYPES, ONLY
C                                  2 - PROCESS R TYPE ONLY
C                                  1 - PROCESS S TYPE ONLY
C         KTRY       INIT       COUNT OF PASSES THROUGH CLIMATOLOGY
C         LR12A      INIT       MR12A VALUE FROM LAST PASS
C         LR12B      INIT       MR12B VALUE FROM LAST PASS
C         LR24A      INIT       MR24A VALUE FROM LAST PASS
C         LR24B      INIT       MR24B VALUE FROM LAST PASS
C         NFCS       INIT       NUMBER OF 12-HOUR FORECAST
C         NSTRT      INIT       NUMBER OF STRAIGHT CYCLONE MATCHES
C         NRECR      INIT       NUMBER OF RECURVER CYCLONE MATCHES
C         PLN        REAL       PAST LONGITUDE
C
C  METHOD:  1. READ ARQ MESSAGE TO OBTAIN WORKING BEST TRACK, ETC.
C           2. READ WINDOWED CLIMATOLOGY FILES AND SCREEN WITH:
C              A. DAYS
C              B. DISTANCE
C              C. WIND SPEED
C              D. TRACK DEVIATION
C           3. KEEP AND SORT TOP FIVE CLIMATOLOGY TROPICAL CYCLONES
C              FOR BEST MATCHING OVER 12-HR AND 24-HR PERIODS FOR:
C              A. STRAIGHT
C              B. RECURVER
C              C. OTHER
C              D. TOTAL (S, R AND O)
C           4. IF NO MATCH, ON FIRST PASS, DOUBLE DISTANCE WINDOW AND
C              TRY AGAIN.
C           5. FORECAST 12-HOUR POSITION AND MAX WIND SPEED FOR STRAIGHT
C              AND RECURVER TYPE TROPICAL CYCLONE TRACKS.
C           6. REPEAT 12-HOUR FORECAST OUT TO 72 HOURS.
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>> TYAN93*01  (21 JUL 1993)  --  HAMILTON,H.
C           ADD CAPABILITY OF FORECASTING TO TYAN93, FOR TAUS
C           12, 24, 36, 48 AND 72 HOURS
C
C  <<CHANGE NOTICE>> TYAN93*02  (05 JUL 1993)  --  SAMPSON,B.
C           CONVERT TO RUN IN ATCF 3.0
C           OUTPUT TO SCREEN REDIRECTED TO DEBUGGING FILE
C           OUTPUT (PLAIN TEXT) TO TAPE55 REDIRECTED TO SCREEN 
C
C
C...................END PROLOGUE.......................................
C
  
      CHARACTER*4 AIDNM
      CHARACTER*5 COUNT(5)
      CHARACTER*8 CDTG12, INCRD5, cdtgsav
      CHARACTER*80 CFSTRT, CFRECR, CDSTRT, CDRECR
C
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW24  - PAST 24 HR EAST/WEST HEMISPHERE INDOCATOR, E OR W
C
      CHARACTER CNAME*7, CDTG*8, CNS*1, CEW*1, EW12*1, EW24*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12,EW24
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG (+ NH, - SH)
C   FLN   - FIX LONGITUDE, DEG (EAST)
C   PLT12 - PAST 12 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN12 - PAST 12 HR LONGITUDE, DEG (EAST)
C   PLT24 - PAST 24 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN24 - PAST 24 HR LONGITUDE, DEG (EAST)
C   HD12S - HEADING  FROM -12 TO FIX LOCATION (STRAIGHT), DEG
C   DT12S - DISTANCE FROM -12 TO FIX LOCATION (STRAIGHT), NM
C   HD24S - HEADING  FROM -24 TO FIX LOCATION (STRAIGHT), DEG
C   DT24S - DISTANCE FROM -24 TO FIX LOCATION (STRAIGHT), NM
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12,PLT24,PLN24
     .             ,HD12S,DT12S,HD24S,DT24S
C
C
C                   EXPLANATION OF /POSITR/ VARIABLES FOR RECURVERS
C
C   NREGNR - NUMBER OF BASIN FROM FIX POSITION
C   FLTR   - INITIAL LATITUDE, DEG
C   FLNR   - INITIAL LONGITUDE, DEG
C   PLT12R - PAST 12 HR LATITUDE,  DEG
C   PLN12R - PAST 12 HR LONGITUDE, DEG
C   PLT24R - PAST 24 HR LATITUDE,  DEG
C   PLN24R - PAST 24 HR LONGITUDE, DEG
C   HD12R  - HEADING  FROM -12 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -12 TO FIX LOCATION (RECURVER), NM
C   HD24R  - HEADING  FROM -24 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -24 TO FIX LOCATION (RECURVER), NM
C
      COMMON/POSITR/ NREGNR,FLTR,FLNR,FWDR,PLT12R,PLN12R,PLT24R,PLN24R,
     .               HD12R,DT12R,HD24R,DT24R
C
C  <<CHANGE NOTICE>>  $TYANB101  (21 JUL 1993)  --  HAMILTON,H.
C           ADD HEADING AND DISTANCE TO DCREASE RUNNING TIME.
C           ADD /POSITR/ TO ALLOW FORECASTING BY TYAN93.
C
C                   EXPLANATION OF /CBCLM/ VARIABLES
C
C   CYCYYX  - NAME/IDENTIFICATION OF CLIMO CYCLONE
C       YY  - HOUR, 12 OR 24
C        X  - A - S-TYPE (STRAIGHT)
C             B - R-TYPE (RECURVER)
C             C - O-TYPE (OTHER)
C             D - ALL-TYPES (S, R AND O)
C
      CHARACTER*8 CYC12A,CYC24A,CYC12B,CYC24B,CYC12C,CYC24C,
     .            CYC12D,CYC24D
C
      COMMON/CBCLM/ CYC12A(6),CYC24A(6),CYC12B(6),CYC24B(6),
     .              CYC12C(6),CYC24C(6),CYC12D(6),CYC24D(6)
C
C                   EXPLANATION OF /BCLMX/ VARIABLES
C
C   NYRYYX - YEAR OF INITIAL POSITION
C   NDYYYX - JULIAN DAY OF INITIAL POSITION
C   MYRYYX - YEAR OF POSITION
C   DYJYYX - JULIAN DAY OF POSITION
C   MHRYYX - HOUR OF POSITION
C   CLTYYX - LATITUDE OF POSITION (+ NH, - SH)
C   CLNYYX - LONGITUDE OF POSITION (0 - 360 EAST)
C   WNDYYX - ANALOG FORECAST 12-HR WIND SPEED CHANGE, KT
C   EYYX   - WEIGHTED ERROR DIFFERENCE BETWEEN TRANSPOSED CLIMATOLOGY
C            AND YY HOUR POSITION LATER
C   ALTYXX - ANALOG TAU 12 FORECAST OF LATITUDE, DEG
C   ALNYYX - ANALOG TAU 12 FORECAST OF LONGITUDE, DEG
C   MRYYX  - NUMBER OF VALUES
C      YY  - HOUR, 12 OR 24
C       X  - A - S-TYPE (STRAIGHT)
C            B - R-TYPE (RECURVER)
C            C - O-TYPE (OTHER)
C            D - ALL-TYPES (S, R AND O)
C
      COMMON/BCLMA/ NYR12A(6),NDY12A(6),MYR12A(6),MDY12A(6),MHR12A(6),
     .              CLT12A(6),CLN12A(6),WND12A(6),E12A(6),
     .              ALT12A(6),ALN12A(6),MR12A,
     .              NYR24A(6),NDY24A(6),MYR24A(6),MDY24A(6),MHR24A(6),
     .              CLT24A(6),CLN24A(6),WND24A(6),E24A(6),
     .              ALT24A(6),ALN24A(6),MR24A
      COMMON/BCLMB/ NYR12B(6),NDY12B(6),MYR12B(6),MDY12B(6),MHR12B(6),
     .              CLT12B(6),CLN12B(6),WND12B(6),E12B(6),
     .              ALT12B(6),ALN12B(6),MR12B,
     .              NYR24B(6),NDY24B(6),MYR24B(6),MDY24B(6),MHR24B(6),
     .              CLT24B(6),CLN24B(6),WND24B(6),E24B(6),
     .              ALT24B(6),ALN24B(6),MR24B
      COMMON/BCLMC/ NYR12C(6),NDY12C(6),MYR12C(6),MDY12C(6),MHR12C(6),
     .              CLT12C(6),CLN12C(6),E12C(6),MR12C,
     .              NYR24C(6),NDY24C(6),MYR24C(6),MDY24C(6),MHR24C(6),
     .              CLT24C(6),CLN24C(6),E24C(6),MR24C
      COMMON/BCLMD/ NYR12D(6),NDY12D(6),MYR12D(6),MDY12D(6),MHR12D(6),
     .              CLT12D(6),CLN12D(6),E12D(6),MR12D,
     .              NYR24D(6),NDY24D(6),MYR24D(6),MDY24D(6),MHR24D(6),
     .              CLT24D(6),CLN24D(6),E24D(6),MR24D
C
C
C  <<CHANGE NOTICE>>  $TYANB201  (21 JUL 1993)  --  HAMILTON,H.
C           ADD WNDYYX, ALTYYX, ALNYYX, WHERE YY IS 12
C           OR 24 AND X IS A OR B, TO ALLOW FORECASTING BY TYAN93
C
C
C                   SET TIME (DAYS) AND DISTANCE (DEG) WINDOW VALUES
C
      DATA NDAYS/35/, DSTLAT/2.5/, DSTLON/5.0/
      DATA COUNT/' ONE ',' TWO ','THREE','FOUR ','FIVE '/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c  open debuggin file
c 
      call openfile (13,'tyan93.dbg','UNKNOWN',ioerror)
C
C****************** READ ARQ MESSAGE FROM FILE ARQ  *******************
C
      CALL REDARQ (cent, IERR1)
c
c  save the starting dtg
c     
      cdtgsav=cdtg

      IF (IERR1 .EQ. 0) THEN
C                   SET FORECAST AND DIAGNOSTIC FLAGS FOR CVCQFC
cx      CFSTRT(1:11) = ' TYAN STRT '
cx      CFRECR(1:11) = ' TYAN RECR '
cx      CDSTRT(1:11) = ' TYAN DGST '
cx      CDRECR(1:11) = ' TYAN DGRC '
c
c  initialize the WHOLE output string
c
        CFSTRT(1:40) = ' TYAN STRT                              '
        CFSTRT(40:80)= '                                        '
        CFRECR(1:40) = ' TYAN RECR                              '
        CFRECR(40:80)= '                                        '
        CDSTRT(1:40) = ' TYAN DGST                              '
        CDSTRT(40:80)= '                                        '
        CDRECR(1:40) = ' TYAN DGRC                              '
        CDRECR(40:80)= '                                        '
C
C*****************  WRITE HEADER ON OUTPUT FOR CVCQFC *****************
C
        AIDNM = 'TYAN'
        CALL HEDING (AIDNM)
C                   SET FORECAST COUNT TO ZERO
        NFCS = 0
C                   SET KSTRC TO INCLUDE OTHER AND TOTAL
        KSTRC  = 4
        CDTG12 = CDTG
C
C*************  CALL TO COMPUTE BEST MATCH WITH CLIMATOLOGY  ***********
C
  100   CONTINUE
        KTRY  = 1
        KDST  = 0
        KDRC  = 0
        DSTLT = DSTLAT
        DSTLN = DSTLON
        CDTG  = CDTG12
  110   CONTINUE
        CALL BSTCLM (NDAYS,DSTLT,DSTLN,KSTRC,KTRY,NSTRT,NRECR)
        IF (KTRY .EQ. 1) THEN
          LSTRC = KSTRC
          IF (KSTRC .EQ. 4) THEN
            IF (NSTRT.LT.3 .OR. NRECR.LT.3) KTRY = -1
          ELSE
            IF (NSTRT.LT.3 .AND. NRECR.LT.7) THEN
              KTRY = -1
            ELSEIF (NSTRT.LT.7 .AND. NRECR.LT.3) THEN
              KTRY = -1
            ELSEIF (KSTRC.NE.2 .AND. NSTRT.LT.3) THEN
              LR12B = MR12B
              LR24B = MR24B
              KSTRC = 1
              KDRC  = 1
              KTRY  = -1
            ELSEIF (KSTRC.NE.1 .AND. NRECR.LT.3) THEN
              LR12A = MR12A
              LR24A = MR24A
              KSTRC = 2
              KDST  = 1
              KTRY  = -1
            ENDIF
          ENDIF
          IF (KTRY .LT. 0) THEN
C
C                   TOO FEW CYCLONES FOUND IN TIME, DISTANCE AND
C                   WIND-SPEED WINDOWS, SO MODIFY DISTANCE AND
C                   WIND-SPEED WINDOWS ON NEXT TRY.
C
            KTRY  = 2
            DSTLT = 2.0*DSTLAT
            DSTLN = 2.0*DSTLON
            GOTO 110
C
          ENDIF
        ELSE
          IF (KSTRC .NE. LSTRC) THEN
            IF (KSTRC .EQ. 1) THEN
              MR12B = LR12B
              MR24B = LR24B
            ELSEIF (KSTRC .EQ. 2) THEN
              MR12A = LR12A
              MR24A = LR24A
            ENDIF
            KSTRC = LSTRC
          ENDIF
        ENDIF
        IF (KDST .EQ. 0) KDST = KTRY
        IF (KDRC .EQ. 0) KDRC = KTRY
        IF (KSTRC.EQ.4 .AND. (NSTRT.GT.0 .OR. NRECR.GT.0)) THEN
C
C****************** OUTPUT PLAIN LANGUAGE TYAN MATCHING ***********
C
          IF (PLT24.NE.0.0 .AND. PLN24.NE.0.0) THEN
C                   24-HOUR OLD POSITION IS AVAILABLE
            ITAU = -24
            IF (EW24 .EQ. 'E') THEN
              PLN = PLN24
            ELSE
              PLN = 360.0 -PLN24
            ENDIF
            CALL TRKDST (PLT24,PLN24,PLT12,PLN12,HEAD,DIST)
            WRITE (13,9010) ITAU,ABS(PLT24),CNS,PLN,EW24,HEAD,
     .                 DIST/12.0
          ENDIF
 9010     FORMAT (11X,'TAU =',I3,'  LAT = ',F5.1,A1,'  LON = ',F6.1,A1,
     .            '  HEAD = ',F6.2,'  SPEED =',F6.2)
          IF (PLT12.NE.0.0 .AND. PLN12.NE.0.0) THEN
C                   12-HOUR OLD POSITION IS AVAILABLE
            ITAU = -12
            IF (EW12 .EQ. 'E') THEN
              PLN = PLN12
            ELSE
              PLN = 360.0 -PLN12
            ENDIF
            CALL TRKDST (PLT12,PLN12,FLT,FLN,HEAD,DIST)
            WRITE (13,9010) ITAU,ABS(PLT12),CNS,PLN,EW12,HEAD,
     .                 DIST/12.0
          ENDIF
C
C****************   OUTPUT MATCHING CYCLONE DATA  **********************
C
          IF (MR12A .GT. 0) THEN
            WRITE (*,9051) COUNT(MR12A), CNAME
 9051       FORMAT (' TOP ANALOGS - ',A5,' STRAIGHT 12 HR MATCHES FOR ',
     .              A8)
            DO 210 N=1, MR12A
              CALL JLTOMD (NYR12A(N),NDY12A(N),KMON,KDAY)
              CALL JLTOMD (MYR12A(N),MDY12A(N),JMON,JDAY)
              WRITE (*,9061) CYC12A(N),KMON,NYR12A(N),KDAY,N,JMON,JDAY,
     .                        MYR12A(N),MHR12A(N)
  210       CONTINUE
 9061       FORMAT (1X,A7,' S STORM NO.',3I2.2,' RANK NO.',I2,
     .        ', BEST POSIT IS OB. ',I2.2,'/',I2.2,'/',I2.2,1X,I2.2,'Z')
          ENDIF
          IF (MR24A .GT. 0) THEN
            WRITE (*,9052) COUNT(MR24A), CNAME
 9052       FORMAT (' TOP ANALOGS - ',A5,' STRAIGHT 24 HR MATCHES FOR ',
     .              A8)
            DO 220 N=1, MR24A
              CALL JLTOMD (NYR24A(N),NDY24A(N),KMON,KDAY)
              CALL JLTOMD (MYR24A(N),MDY24A(N),JMON,JDAY)
              WRITE (*,9061) CYC24A(N),KMON,NYR24A(N),KDAY,N,JMON,JDAY,
     .                        MYR24A(N),MHR24A(N)
  220       CONTINUE
          ENDIF
          IF (MR12B .GT. 0) THEN
            WRITE (*,9053) COUNT(MR12B), CNAME
 9053       FORMAT (' TOP ANALOGS - ',A5,' RECURVER 12 HR MATCHES FOR ',
     .              A8)
            DO 230 N=1, MR12B
              CALL JLTOMD (NYR12B(N),NDY12B(N),KMON,KDAY)
              CALL JLTOMD (MYR12B(N),MDY12B(N),JMON,JDAY)
              WRITE (*,9062) CYC12B(N),KMON,NYR12B(N),KDAY,N,JMON,JDAY,
     .                        MYR12B(N),MHR12B(N)
  230       CONTINUE
 9062       FORMAT (1X,A7,' R STORM NO.',3I2.2,' RANK NO.',I2,
     .        ', BEST POSIT IS OB. ',I2.2,'/',I2.2,'/',I2.2,1X,I2.2,'Z')
          ENDIF
          IF (MR24B .GT. 0) THEN
            WRITE (*,9054) COUNT(MR24B), CNAME
 9054       FORMAT (' TOP ANALOGS - ',A5,' RECURVER 24 HR MATCHES FOR ',
     .              A8)
            DO 240 N=1, MR24B
              CALL JLTOMD (NYR24B(N),NDY24B(N),KMON,KDAY)
              CALL JLTOMD (MYR24B(N),MDY24B(N),JMON,JDAY)
              WRITE (*,9062) CYC24B(N),KMON,NYR24B(N),KDAY,N,JMON,JDAY,
     .                        MYR24B(N),MHR24B(N)
  240       CONTINUE
          ENDIF
          IF (MR12C .GT. 0) THEN
            WRITE (*,9055) COUNT(MR12C), CNAME
 9055       FORMAT (' TOP ANALOGS - ',A5,' OTHER 12 HR MATCHES FOR ',
     .              A8)
            DO 250 N=1, MR12C
              CALL JLTOMD (NYR12C(N),NDY12C(N),KMON,KDAY)
              CALL JLTOMD (MYR12C(N),MDY12C(N),JMON,JDAY)
              WRITE (*,9063) CYC12C(N),KMON,NYR12C(N),KDAY,N,JMON,JDAY,
     .                        MYR12C(N),MHR12C(N)
  250       CONTINUE
 9063       FORMAT (1X,A7,' O STORM NO.',3I2.2,' RANK NO.',I2,
     .        ', BEST POSIT IS OB. ',I2.2,'/',I2.2,'/',I2.2,1X,I2.2,'Z')
          ENDIF
          IF (MR24C .GT. 0) THEN
            WRITE (*,9056) COUNT(MR24C), CNAME
 9056       FORMAT (' TOP ANALOGS - ',A5,' OTHER 24 HR MATCHES FOR ',
     .              A8)
            DO 260 N=1, MR24C
              CALL JLTOMD (NYR24C(N),NDY24C(N),KMON,KDAY)
              CALL JLTOMD (MYR24C(N),MDY24C(N),JMON,JDAY)
              WRITE (*,9063) CYC24C(N),KMON,NYR24C(N),KDAY,N,JMON,JDAY,
     .                        MYR24C(N),MHR24C(N)
  260       CONTINUE
          ENDIF
          IF (MR12D .GT. 0) THEN
            WRITE (*,9057) COUNT(MR12D), CNAME
 9057       FORMAT (' TOP ANALOGS - ',A5,' TOTAL 12 HR MATCHES FOR ',
     .              A8)
            DO 270 N=1, MR12D
              CALL JLTOMD (NYR12D(N),NDY12D(N),KMON,KDAY)
              CALL JLTOMD (MYR12D(N),MDY12D(N),JMON,JDAY)
              WRITE (*,9064) CYC12D(N),KMON,NYR12D(N),KDAY,N,JMON,JDAY,
     .                        MYR12D(N),MHR12D(N)
  270       CONTINUE
 9064       FORMAT (1X,A7,' T STORM NO.',3I2.2,' RANK NO.',I2,
     .        ', BEST POSIT IS OB. ',I2.2,'/',I2.2,'/',I2.2,1X,I2.2,'Z')
          ENDIF
          IF (MR24D .GT. 0) THEN
            WRITE (*,9058) COUNT(MR24D), CNAME
 9058       FORMAT (' TOP ANALOGS - ',A5,' TOTAL 24 HR MATCHES FOR ',
     .              A8)
            DO 280 N=1, MR24D
              CALL JLTOMD (NYR24D(N),NDY24D(N),KMON,KDAY)
              CALL JLTOMD (MYR24D(N),MDY24D(N),JMON,JDAY)
              WRITE (*,9064) CYC24D(N),KMON,NYR24D(N),KDAY,N,JMON,JDAY,
     .                        MYR24D(N),MHR24D(N)
  280       CONTINUE
          ENDIF
C
C****************** PERFORM 12-HOUR FORECAST ***************************
C
          NFCS = 1
          CALL MAKFCT (NFCS,KSTRC,CFSTRT,CFRECR,KDST,KDRC,CDSTRT,CDRECR)
          WRITE (13,9140) CFSTRT
          WRITE (13,9140) CDSTRT
          WRITE (13,9140) CFRECR
          WRITE (13,9140) CDRECR
C                   INCREASE "FIX" DTG BY 12 HOURS
cx        CDTG12 = INCRD5 (CDTG,12)
	  CALL ICRDTG (CDTG,CDTG12,12)
          GOTO 100
C
        ELSEIF (NSTRT.GT.0 .OR. NRECR.GT.0) THEN
C
C****************** MAKE FORECASTS, 24, 36, 48, 60 AND 72 **********
C
          NFCS = NFCS +1
          CALL MAKFCT (NFCS,KSTRC,CFSTRT,CFRECR,KDST,KDRC,CDSTRT,CDRECR)
          WRITE (13,9140) CFSTRT
          WRITE (13,9140) CDSTRT
          WRITE (13,9140) CFRECR
          WRITE (13,9140) CDRECR
C                   INCREASE "FIX" DTG BY 12 HOURS
cx        CDTG12 = INCRD5 (CDTG,12)
	  CALL ICRDTG (CDTG,CDTG12,12)
          IF (NFCS .LT. 6) GOTO 100
C
C***************** WRITE FORECASTS *************************************
C
          WRITE (*,9140) CFSTRT
          WRITE (*,9140) CFRECR
cx        WRITE (*,9140) CDSTRT
cx        WRITE (*,9140) CDRECR
	  WRITE (*,*)' '
	  WRITE (*,*)'     BASIS OF TYAN FORECAST    '
	  WRITE (*,*)' FORECAST HOURS   12 24 36 48 60 72'

	  WRITE (*,*)' STRAIGHT WINDOW  ',
     .	     CDSTRT(12:12),'  ',CDSTRT(18:18),'  ',CDSTRT(24:24),'  ',
     .	     CDSTRT(30:30),'  ',CDSTRT(36:36),'  ',CDSTRT(42:42)
	  WRITE (*,*)' STRAIGHT POSIT   ',
     .	     CDSTRT(14:14),'  ',CDSTRT(20:20),'  ',CDSTRT(26:26),'  ',
     .	     CDSTRT(32:32),'  ',CDSTRT(38:38),'  ',CDSTRT(44:44)
	  WRITE (*,*)' STRAIGHT WND SPD ',
     .	     CDSTRT(16:16),'  ',CDSTRT(22:22),'  ',CDSTRT(28:28),'  ',
     .	     CDSTRT(34:34),'  ',CDSTRT(40:40),'  ',CDSTRT(46:46)

	  WRITE (*,*)' RECURVER WINDOW  ',
     .	     CDRECR(12:12),'  ',CDRECR(18:18),'  ',CDRECR(24:24),'  ',
     .	     CDRECR(30:30),'  ',CDRECR(36:36),'  ',CDRECR(42:42)
	  WRITE (*,*)' RECURVER POSIT   ',
     .	     CDRECR(14:14),'  ',CDRECR(20:20),'  ',CDRECR(26:26),'  ',
     .	     CDRECR(32:32),'  ',CDRECR(38:38),'  ',CDRECR(44:44)
	  WRITE (*,*)' RECURVER WND SPD ',
     .	     CDRECR(16:16),'  ',CDRECR(22:22),'  ',CDRECR(28:28),'  ',
     .	     CDRECR(34:34),'  ',CDRECR(40:40),'  ',CDRECR(46:46)

 9140     FORMAT (A80)
c
c  write the forecast in ccrs format
c
          call wtccrs(cent,cdtgsav,cfstrt,cfrecr)

          WRITE (*,'(" END ANALOGS")')
        ELSEIF (NFCS .EQ. 0) THEN
          WRITE (*,9150)
 9150     FORMAT (' INSUFFICIENT CYCLONES FOR TYAN93 **********')
        ENDIF
cx      CLOSE (55)
	write(13,*)'Good Run'
        CLOSE (13)
        STOP 'TYAN93: GOOD STOP'
      ELSE
cx      CLOSE (55)
	write(13,*)'Best Track Input Problem'
        CLOSE (13)
        STOP 'TYAN93: ARQ INPUT PROBLEM'
      ENDIF
C
      END
c 

      subroutine wtccrs(cent,cdtgsav,cfstrt,cfrecr)
c
C..........................START PROLOGUE..............................
c
C  MODULE NAME:  wtccrs
C
C  DESCRIPTION:  Reconstruct and write data in CCRS format to wptot.dat
c
C...................END PROLOGUE.......................................
C
      include 'dataioparms.inc'

      integer       ii, iarg
      integer       ltlnwnd(numtau,llw)
      character*100 storms,filename
      character*8   cdtgsav
      character*80  cfstrt, cfrecr
      character*6   strmid
      character*1   ns(5),ew(5),cdummy
      character*2   century
      character*2   cent
      dimension     ilat(5),ilon(5),iwnd(5)
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
      call upcase(strmid,6)
c
c  get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
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
c
c  initialize the ltlnwnd array
c
      do ii=1,numtau
         ltlnwnd(ii,1) = 0
         ltlnwnd(ii,2) = 0
         ltlnwnd(ii,3) = 0
      enddo
c
c  convert the lats and lons to ccrs, write to file
c
      read (cfstrt,9000,err=910)
     1            (ilat(i),ns(i),ilon(i),ew(i),iwnd(i),i=1,5)
 9000 format(10x,5(i4,a1,i4,a1,i4))
      do 100 i=1,5
         if(ns(i) .eq. 'S')ilat(i)=-ilat(i)
	 if(ew(i) .eq. 'E' .and. ilon(i).ne.0)ilon(i)=3600-ilon(i)
  100 continue
      do ii=1, 5
         ltlnwnd(ii,1) = ilat(ii)
         ltlnwnd(ii,2) = ilon(ii)
         ltlnwnd(ii,3) = iwnd(ii)
      enddo
      call writeAid( 60, strmid, cent, cdtgsav, 'STRT', ltlnwnd )
      
      read (cfrecr,9000,err=930)
     1	   (ilat(i),ns(i),ilon(i),ew(i),iwnd(i),i=1,5)
      do 300 i=1,5
         if(ns(i) .eq. 'S')ilat(i)=-ilat(i)
	 if(ew(i) .eq. 'E' .and. ilon(i).ne.0)ilon(i)=3600-ilon(i)
  300 continue
      do ii=1, 5
         ltlnwnd(ii,1) = ilat(ii)
         ltlnwnd(ii,2) = ilon(ii)
         ltlnwnd(ii,3) = iwnd(ii)
      enddo
      call writeAid( 60, strmid, cent, cdtgsav, 'RECR', ltlnwnd )
        
      close (60)
      return
  900 print *, 'error opening:',filename
      return
  910 print *, 'error reading STRT forecast output'
      return
  920 print *, 'error writing STRT forecast output'
      return
  930 print *, 'error reading RECR forecast output'
      return
  940 print *, 'error writing RECR forecast output'
      return
      end
	  
      SUBROUTINE REDARQ (cent,IERR1)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  REDARQ
C
C  DESCRIPTION:  READ ARQ MESSAGE FOR TROPICAL CYCLONE INFORMATIOON
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL REDARQ (cent, IERR1)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C      cent       character*2   out     century of last bt dtg  
C      IERR1      INTEGER       OUT     ERROR FLAG, 0 - NO ERROR
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES OF LISTED COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C      CNSEW     CNAME     CHAR     OUT      TROPICAL CYCLONE NAME/ID
C                CDTG      CHAR     OUT      CYCLONE DTG (YYMMDDHH) OF
C                                            PRESENT POSITION
C                CNS       CHAR     OUT      N OR S FOR LATITUDE
C                EW12      CHAR     OUT      E OR W FOR LONGITUDE, -12HR
C                EW24      CHAR     OUT      E OR W FOR LONGITUDE, -24HR
C      POSIT     NREGN     INIT     OUT      REGION-BASIN INDICATOR
C                FLT       REAL     OUT      PRESENT CYCLONE LATITUDE
C                FLN       REAL     OUT      PRESENT CYCLONE LONGITUDE
C                FWD       REAL     OUT      PRESENT MAXIMUM WIND SPEED
C                PLT12     REAL     OUT      PAST 12-HR LATITUDE
C                PLN12     REAL     OUT      PAST 12-HR LONGITUDE
C                PLT24     REAL     OUT      PAST 24-HR LATITUDE
C                PLN24     REAL     OUT      PAST 24-HR LONGITUDE
C
C  FILES:
C    NAME     UNIT  FILE TYPE  ATTRIBUTE  USAGE         DESCRIPTION
C   -------  -----  ---------  ---------  ------   ---------------------
C       ARQ     92  LOCAL      SEQUENTIAL   IN     CARQ REQUEST
C
C  DATA BASES:  NO TABLE-DRIVEN DATA BASE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C     BAD ARQ MESSAGE          TERMINATE PROCESSING
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         JDAYEM      CONVERT YEAR, MONTH AND DAY INTO JULIAN DAY
C         TRKDST      GIVEN TWO POSITIONS, CALCUALTE TRACK AND DISTANCE
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         CARD       CHAR       WORKING CHARACTER STRING
C         CBASN1     CHAR       ONE-CHARACTER BASIN CODE OF CYCLONE
C         CBASN2     CHAR       TWO-CHARACTER BASIN CODE OF CYCLONE
C         CSTRMK     CHAR       CYCLONE NUMBER IN GIVEN BASIN
C         CYCNAM     CHAR       CYCLONE IDENTIFICATION (02W)
C         CYEAR      CHAR       YEAR OF PRESENT CYCLONE LOCATION
C         DIR        REAL       DIRECTION FROM POSITION ONE TO TWO, DEG
C         DST        REAL       DISTANCE FROM POSITION ONE TO TWO, NM
C         FLON       REAL       PRESENT LONGITUDE OF CYCLONE
C         ICDTG      INIT       CHECK FLAG FOR DTG
C         ICFIX      INIT       CHECK FLAG FOR PRESENT POSITION
C         ICNAM      INIT       CHECK FLAG FOR CYCLONE NAME/ID
C         ICPOO      INIT       VALIDITY FLAG FOR FOR PRESENT POSITION
C         ICP12      INIT       VALIDITY FLAG FOR 12-HR PAST POSITION
C         ICP24      INIT       VALIDITY FLAG FOR 24-HR PAST POSITION
C         ITIME      INIT       HOUR OF PAST POSITION
C         NSIND      INIT       NORTH/SOUTH INDICATOR
C         PLON12     REAL       PAST 12-HR LONGITDUE
C         PLON24     REAL       PAST 24-HR LONGITUDE
C         SPD12      REAL       SPEED OF CYCLONE, LAST 12 HOURS
C         SPD24      REAL       SPEED OF CYCLONE, FROM -24 TO -12 HR
C
C  METHOD:
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  REDARQ*01  (21 JUL 1993)  --  HAMILTON,H.
C           LOAD HDXXY AND DTXXY, XX = 12 OR 24, Y = S OR R.
C           LOAD NEW /POSITR/ VALUES FOR RECURVE FORECASTING.
C
C  <<CHANGE NOTICE>>  REDARQ*01  (21 JUL 1993)  --  SAMPSON,B.
C           CHANGED TO READ BEST TRACK FILE INSTEAD OF CARQ
C
C...................END PROLOGUE.......................................
C
      CHARACTER*1 CBASN1
      CHARACTER*2 CBASN2,CSTRMK,CYEAR
      CHARACTER*3 CYCNAM
      CHARACTER*80 CARD
      character*100 storms,filename
      character*6 strmid
      character*8 cdtg,cdtg12,cdtg24
      character*8 tdtg
      character*8 btdtg
      character*2 century
      character btns*1, btew*1
      integer ibtwind, ios, iarg
      real btlat, btlon
C 
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW24  - PAST 24 HR EAST/WEST HEMISPHERE INDOCATOR, E OR W
C
      CHARACTER CNAME*7, CNS*1, CEW*1, EW12*1, EW24*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12,EW24
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG (+ NH, - SH)
C   FLN   - FIX LONGITUDE, DEG (EAST)
C   PLT12 - PAST 12 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN12 - PAST 12 HR LONGITUDE, DEG (EAST)
C   PLT24 - PAST 24 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN24 - PAST 24 HR LONGITUDE, DEG (EAST)
C   HD12S - HEADING  FROM -12 TO FIX LOCATION (STRAIGHT), DEG
C   DT12S - DISTANCE FROM -12 TO FIX LOCATION (STRAIGHT), NM
C   HD24S - HEADING  FROM -24 TO FIX LOCATION (STRAIGHT), DEG
C   DT24S - DISTANCE FROM -24 TO FIX LOCATION (STRAIGHT), NM
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12,PLT24,PLN24
     .             ,HD12S,DT12S,HD24S,DT24S
C
C
C                   EXPLANATION OF /POSITR/ VARIABLES FOR RECURVERS
C
C   NREGNR - NUMBER OF BASIN FROM FIX POSITION
C   FLTR   - INITIAL LATITUDE, DEG
C   FLNR   - INITIAL LONGITUDE, DEG
C   PLT12R - PAST 12 HR LATITUDE,  DEG
C   PLN12R - PAST 12 HR LONGITUDE, DEG
C   PLT24R - PAST 24 HR LATITUDE,  DEG
C   PLN24R - PAST 24 HR LONGITUDE, DEG
C   HD12R  - HEADING  FROM -12 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -12 TO FIX LOCATION (RECURVER), NM
C   HD24R  - HEADING  FROM -24 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -24 TO FIX LOCATION (RECURVER), NM
C
      COMMON/POSITR/ NREGNR,FLTR,FLNR,FWDR,PLT12R,PLN12R,PLT24R,PLN24R,
     .               HD12R,DT12R,HD24R,DT24R
C
C  <<CHANGE NOTICE>>  $TYANB101  (21 JUL 1993)  --  HAMILTON,H.
C           ADD HEADING AND DISTANCE TO DCREASE RUNNING TIME.
C           ADD /POSITR/ TO ALLOW FORECASTING BY TYAN93.
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .


C
C********* OPEN INPUT FILE WITH Q92 MESSAGE
C
cx    OPEN (92,FILE='ARQ',ERR=701)
C
C**********         INITIALIZE FINDING FLAGS
C
      ICNAM = 0
      ICDTG = 0
      ICFIX = 0
      ICP00 = 0
      ICP12 = 0
      ICP24 = 0
      NREGN = 0
      IERR1 = 0
      FLT   =   0.0
      FLN   =   0.0
      FWD   = -99.0
      PLT12 =   0.0
      PLN12 =   0.0
      PLT24 =   0.0
      PLN24 =   0.0


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
c
c  get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
c
c  write heading on output
c
      print *,'**************************************************'
cx    print *,'          tyan93 forecast for ',strmid
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
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

cx    print *, 'cdtg:',cdtg
c
c  now find the current, -12, and -24 hr positions
c
      call icrdtg (cdtg,cdtg12,-12)
      call icrdtg (cdtg,cdtg24,-24)
      rewind 92
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 92,cent,btdtg,btlat,cns,btlon,btew,ibtwind,ios )
         if( ios .eq. 0 ) then
            if( btdtg .eq. cdtg24 ) then
               plt24 = btlat
               plon24 = btlon
               ew24 = btew
            else if( btdtg .eq. cdtg12 ) then
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

cx    print *, 'plt24,cns,plon24,ew24:'
cx    print *,  plt24,cns,plon24,ew24
cx    print *, 'plt12,cns,plon12,ew12:'
cx    print *,  plt12,cns,plon12,ew12  
cx    print *, 'flt,cns,flon,cew,fwd:'
cx    print *,  flt,cns,flon,cew,fwd  
      close (92)


c*****************   end of read best track data ********************

C
C*****              INPUT THE CARQ DATA
C
cx    DO 110 IC=1, 10000
cx      READ (92,500,END=199) CARD
cx500   FORMAT (1X,A79)
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
          IF (JDAYEM (IYR,MON,IDAY).NE.0 .AND. MOD (IHR,6).EQ.0)
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
            WRITE (13,610) CYCNAM ,CDTG
  610       FORMAT (' NO TYAN93 - ATLANTIC BASIN ',A3,' AT ',A8)
            IERR1 = -99
          ELSEIF (NSIND .EQ. -99) THEN
            WRITE (13,615) CYCNAM, CDTG
  615       FORMAT (' NO TYAN93 - WRONG BASIN INDICATED FOR ',A3,
     .              ' AT ',A8)
C           IERR1 = -88
          ELSEIF (NREGN .EQ. 0) THEN
            WRITE (13,616) CYCNAM, CDTG
  616       FORMAT (' NO TYAN93 - NO AGREEMENT LAT/LON AND BASIN FOR '
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
C*************      EXTRACT PREVIOUS POSITIONS     *********************
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
cx        ELSEIF (ITIME .EQ. 24) THEN
C
C                         24-HR OLD POSIT
C
cx          READ (CARD,504) PLT24,PLON24,EW24
            IF (PLT24.GT.1.0 .AND. PLT24.LE.60.0 .AND.
     .          PLON24 .LE. 180.0) ICP24 = -1
            PLT24 = SIGN (PLT24,FLT)
            IF (EW24 .EQ. 'E') THEN
              PLN24 = PLON24
            ELSEIF (EW24 .EQ. 'W') THEN
              PLN24 = 360.0 -PLON24
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
        WRITE (13,620)
  620   FORMAT (1X,'NO TYAN93 - MISSING CYCLONE NAME AND/OR DTG')
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
        WRITE (13,640) CNAME,CDTG,
     .                ABS(PLT24),CNS,PLON24,EW24,
     .                ABS(PLT12),CNS,PLON12,EW12,
     .                ABS(FLT),CNS,FLON,CEW,FWD
  640   FORMAT (//,' TYAN93 PROCESSING ',A6,' AT ',A8,/,
     .          6X,'24-HR OLD : ',F4.1,A1,1X,F5.1,A1,/,
     .          6X,'12-HR OLD : ',F4.1,A1,1X,F5.1,A1,/,
     .          6X,' START AT : ',F4.1,A1,1X,F5.1,A1,' WIND ',F4.0,//)
C
C******       CHECK WHICH POSITIONS ARE AVAILABLE
C
        IF (ICFIX.EQ.0 .OR. ICP00.EQ.0) THEN
          WRITE (13,650)  CNAME,CDTG
  650     FORMAT (' TYAN93, MISSING OR BAD 00-HR POSITION FOR ',A6,
     .            ' AT ',A8)
          IERR1 = -1
        ELSEIF (ICP12 .EQ. 0) THEN
          WRITE (13,660)  CNAME,CDTG
  660     FORMAT (' TYAN93, MISSING OR BAD 12-HR OLD POSITION FOR ',
     .            A6,' AT ',A8)
          IERR1 = -1
        ELSE
C
C                   CHECK SPEED AND DIRECTION
C
          PLT1 = SIGN (PLT12,FLT)
          PLT2 = FLT
          CALL TRKDST (PLT1,PLN12,PLT2,FLN,DIR,DST)
          SPD12 = DST/12.0
          WRITE (13,670) SPD12,DIR
  670     FORMAT (' TYAN93, LAST 12-HR SPEED ',F6.2,' DIR ',F5.1)
          IF (SPD12.GT.60.0 .AND. ABS (FLT).LT.40.0) THEN
            WRITE (13,*) ' TYAN93, BAD 12-HR PAST POSITION '
            IERR1 = -1
          ELSE
            HD12S = DIR
            DT12S = DST
          ENDIF
          IF (ICP24 .NE. 0) THEN
            PLT1 = SIGN (PLT24,FLT)
            PLT2 = FLT
            CALL TRKDST (PLT1,PLN24,PLT2,FLN,DIR,DST)
            SPD24 = DST/24.0
            WRITE (13,680) SPD24,DIR
  680       FORMAT (' TYAN93, LAST 24-HR SPEED ',F6.2,' DIR ',F5.1)
            IF (SPD24.GT.60.0 .AND. ABS (FLT).LT.40.0) THEN
              WRITE (13,*) ' TYAN93, BAD 24-HR PAST POSITION '
              IERR1 = -1
          ELSE
            HD24S = DIR
            DT24S = DST
            ENDIF
          ELSE
C                   24-HR POSITION IS NOT REQUIRED, SO DO NOT SET IERR1
            WRITE (13,690)  CNAME,CDTG
  690       FORMAT (' TYAN93, MISSING OR BAD 24-HR OLD POSITION FOR ',
     .              A6,' AT ',A8)
              HD24S = 0.0
              DT24S = 0.0
          ENDIF
        ENDIF
      ENDIF
      IF (IERR1 .EQ. 0) THEN
C
C                   LOAD VALUES FOR RECURVER TYPE CYCLONES
C
        NREGNR = NREGN
        FLTR   = FLT
        FLNR   = FLN
        FWDR   = FWD
        PLT12R = PLT12
        PLN12R = PLN12
        PLT24R = PLT24
        PLN24R = PLN24
        HD12R  = HD12S
        DT12R  = DT12S
        HD24R  = HD24S
        DT24R  = DT24S
      ENDIF
  300 CONTINUE
      RETURN
C
  701 CONTINUE
cx    WRITE (*,*) 'TYAN93, OPEN ERROR ON INPUT FILE ARQ'
      write (13,*) 'tyan93, open error on input file:',filename
      IERR1 = -1
      GOTO 300
C
      END
      SUBROUTINE BSTCLM (NDAYS,DSTLAT,DSTLON,KSTRC,KTRY,NSTRT,NRECR)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  BSTCLM
C
C  DESCRIPTION:  PICK BEST MATCHES BETWEEN CLIMATOLOGY AND WORKING BEST
C                TRACK, FOR PAST 12 AND 24 HOURS
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL BSTCLM (NDAYS,DSTLAT,DSTLON,NM12,NM24)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     NDAYS        INIT          IN     NUMBER OF DAYS IN TIME WINDOW
C     DSTLAT       REAL          IN     DEGREES IN LATITUDE  WINDOW
C     DSTLON       REAL          IN     DEGREES IN LONGITUDE WINDOW
C     KSTRC        INIT          IN     TYPES FLAG FOR PROCESSING
C                                           4 - PROCESS ALL TYPES
C                                           3 - PROCESS S AND R, ONLY
C                                           2 - PROCESS R ONLY
C                                           1 - PROCESS S ONLY
C     KTRY         INIT          IN     COUNT OF TRIES, 1 OR 2
C     NSTRT        INIT          OUT    NUMBER OF STRAIGHT 12 AND 24 HR
C                                       MATCHES
C     NRECR        INIT          OUT    NUMBER OF RECURVER 12 AND 24 HR
C                                       MATCHES
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES OF LISTED COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C      CNSEW     CDTG      CHAR     IN       CYCLONE DTG (YYMMDDHH) OF
C                                            PRESENT POSITION
C      CBCLM     CYC12A    CHAR     OUT      12HR ARRAY OF CLIMATOLOGY
C                                            STRAIGHT CYCLONE NAMES
C                CYC24A    CHAR     OUT      24HR ARRAY OF CLIMATOLOGY
C                                            STRAIGHT CYCLONE NAMES
C                CYC12B    CHAR     OUT      12HR ARRAY OF CLIMATOLOGY
C                                            RECURVER CYCLONE NAMES
C                CYC24B    CHAR     OUT      24HR ARRAY OF CLIMATOLOGY
C                                            RECURVER CYCLONE NAMES
C                CYC12C    CHAR     OUT      12HR ARRAY OF CLIMATOLOGY
C                                            OTHER CYCLONE NAMES
C                CYC24C    CHAR     OUT      24HR ARRAY OF CLIMATOLOGY
C                                            OTHER CYCLONE NAMES
C                CYC12D    CHAR     OUT      12HR ARRAY OF CLIMATOLOGY
C                                            TOTAL CYCLONE NAMES
C                CYC24D    CHAR     OUT      24HR ARRAY OF CLIMATOLOGY
C                                            TOTAL CYCLONE NAMES
C      BCLMA     NYR12A    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (S)
C                NDY12A    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (S)
C                MYR12A    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (S)
C                MDY12A    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (S)
C                MHR12A    INIT     OUT      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (S)
C                CLT12A    REAL     OUT      12HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (S)
C                CLN12A    REAL     OUT      12HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (S)
C                E12A      REAL     OUT      12HR WEIGHTED ERROR (S)
C                MR12A     INIT     OUT      COUNT OF 12HR MATCHES (S)
C                NYR24A    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (S)
C                NDY24A    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (S)
C                MYR24A    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (S)
C                MDY24A    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (S)
C                MHR24A    INIT     OUT      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (S)
C                CLT24A    REAL     OUT      24HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (S)
C                CLN24A    REAL     OUT      24HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (S)
C                E24A      REAL     OUT      24HR WEIGHTED ERROR (S)
C                MR24A     INIT     OUT      COUNT OF 24HR MATCHES (S)
C      BCLMB     NYR12B    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (R)
C                NDY12B    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (R)
C                MYR12B    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (R)
C                MDY12B    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (R)
C                MHR12B    INIT     OUT      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (R)
C                CLT12B    REAL     OUT      12HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (R)
C                CLN12B    REAL     OUT      12HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (R)
C                E12B      REAL     OUT      12HR WEIGHTED ERROR (R)
C                MR12B     INIT     OUT      COUNT OF 12HR MATCHES (R)
C                NYR24B    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (R)
C                NDY24B    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (R)
C                MYR24B    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (R)
C                MDY24B    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (R)
C                MHR24B    INIT     OUT      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (R)
C                CLT24B    REAL     OUT      24HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (R)
C                CLN24B    REAL     OUT      24HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (R)
C                E24B      REAL     OUT      24HR WEIGHTED ERROR (R)
C                MR24B     INIT     OUT      COUNT OF 24HR MATCHES (R)
C      BCLMC     NYR12C    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (O)
C                NDY12C    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (O)
C                MYR12C    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (O)
C                MDY12C    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (O)
C                MHR12C    INIT     OUT      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (O)
C                CLT12C    REAL     OUT      12HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (O)
C                CLN12C    REAL     OUT      12HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (O)
C                E12C      REAL     OUT      12HR WEIGHTED ERROR (O)
C                MR12C     INIT     OUT      COUNT OF 12HR MATCHES (O)
C                NYR24C    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (O)
C                NDY24C    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (O)
C                MYR24C    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (O)
C                MDY24C    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (O)
C                MHR24C    INIT     OUT      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (O)
C                CLT24C    REAL     OUT      24HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (O)
C                CLN24C    REAL     OUT      24HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (O)
C                E24C      REAL     OUT      24HR WEIGHTED ERROR (O)
C                MR24C     INIT     OUT      COUNT OF 24HR MATCHES (O)
C      BCLMD     NYR12D    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (T)
C                NDY12D    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (T)
C                MYR12D    INIT     OUT      12HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (T)
C                MDY12D    INIT     OUT      12HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (T)
C                MHR12D    INIT     OUT      12HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (T)
C                CLT12D    REAL     OUT      12HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (T)
C                CLN12D    REAL     OUT      12HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (T)
C                E12D      REAL     OUT      12HR WEIGHTED ERROR (T)
C                MR12D     INIT     OUT      COUNT OF 12HR MATCHES (T)
C                NYR24D    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            INITIAL POSITION (T)
C                NDY24D    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF INITIAL POSITION (T)
C                MYR24D    INIT     OUT      24HR CLIMATOLOGY YEAR OF
C                                            BEST OBSERVATION (T)
C                MDY24D    INIT     OUT      24HR CLIMATOLOGY JULIAN DAY
C                                            OF BEST OBSERVATION (T)
C                MHR24D    INIT     OUT      24HR CLIMATOLOGY HOUR OF
C                                            BEST OBSERVATION (T)
C                CLT24D    REAL     OUT      24HR CLIMATOLOGY LAT OF
C                                            BEST OBSERVATION (T)
C                CLN24D    REAL     OUT      24HR CLIMATOLOGY LON OF
C                                            BEST OBSERVATION (T)
C                E24D      REAL     OUT      24HR WEIGHTED ERROR (T)
C                MR24D     INIT     OUT      COUNT OF 24HR MATCHES (T)
C      POSIT     NREGN     INIT     IN       REGION-BASIN INDICATOR
C                FLT       REAL     IN       PRESENT CYCLONE LATITUDE
C                FLN       REAL     IN       PRESENT CYCLONE LONGITUDE
C                FWD       REAL     IN       PRESENT MAXIMUM WIND SPEED
C                PLT12     REAL     IN       PAST 12-HR LATITUDE
C                PLN12     REAL     IN       PAST 12-HR LONGITUDE
C                PLT24     REAL     IN       PAST 24-HR LATITUDE
C                PLN24     REAL     IN       PAST 24-HR LONGITUDE
C      POSITR    FLTR      REAL    IN     PRESENT R-CYCLONE LATITUDE
C                FLNR      REAL    IN     PRESENT R-CYCLONE LONGITUDE
C                FWDR      REAL    IN     PRESENT R-CYCLONE MAX WIND
C                PLT12R    REAL    IN     PAST 12-HR LATITUDE,  FOR R
C                PLN12R    REAL    IN     PAST 12-HR LONGITUDE, FOR R
C                PLT24R    REAL    IN     PAST 24-HR LATITUDE,  FOR R
C                PLN24R    REAL    IN     PAST 24-HR LONGITUDE, FOR R
C      STORMC    STNAME    CHAR     IN       CLIMATOLOGY CYCLONE NAME
C                STYPE     CHAR     IN       TRACK CLASSIFICATION
C                                            STRAIGHT, RECURVER OR OTHER
C      STORM     IYR       INIT     IN       YEAR OF POSITION
C                JDAY      INIT     IN       JULIAN DAY OF POSITION
C                IHR       INIT     IN       HOUR OF POSITION
C                XLON      REAL     IN       LONGITUDE OF POSITION, (E)
C                YLAT      REAL     IN       LATITUDE  OF POSITION (+/-)
C                WIND      REAL     IN       MAXIMUM WIND SPEED, (KT)
C                NR        INIT     IN       COUNT OF POSITIONS
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         CLXEAE      CALCULATE CROSS-TRACK AND ALONG-TRACK ERRORS
C         JDAYEM      CALCULATE JULIAN DAY
C         JLTOMD      CONVERT YEAR AND JULIAN DAY TO MONTH AND DAY
C         REDCLM      READ CLIMATOLOGY DATA RECORDS
C         SORTEM      SORT ARRAY VALUES BASED UPON WEIGHTED ERROR
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         AE         REAL       ALONG-TRACK ERROR, NM
C         CMONTH     CHAR       ARRAY OF MONTH NAMES
C         CREGS      CHAR       ARRAY OF REGION ABREVIATIONS
C         CSTR       CHAR       NOS/BE CHARACTER STRING FOR ATTACHING
C         FLN12      REAL       PAST 12-HR LONGITUDE
C         FLN24      REAL       PAST 24-HR LONGITUDE
C         FLT12      REAL       PAST 12-HR LATITUDE
C         FLT24      REAL       PAST 24-HR LATITUDE
C         ICYL       INIT       CYCLE NUMBER OF ATTACHED FILE
C         IEOF       INIT       CLIMATOLOGY EOF FLAG
C         IERC       INIT       ERROR FLAG FROM ATTACH, 0 NO ERROR
C         IFDAY      INIT       DAY OF PRESENT CYCLONE POSITION
C         IFMON      INIT       MONTH OF PRESENT CYCLONE POSITION
C         IFYR       INIT       YEAR OF PRESENT CYCLONE POSITION
C         ISTATUS    INIT       STATUS OF OPEN OPERATION
C         JDAYS      INIT       NUMBER OF JULIAN DAYS IN A YEAR
C         JEDATE     INIT       ENDING JULIAN DAY FOR CLIMATOLOGY
C         JEYR       INIT       ENDING YEAR FOR CLIMATOLOGY
C         JFDATE     INIT       JULIAN DAY OF PRESENT CYCLONE POSITION
C         JS         INIT       STARTING INDEX INTO CLIMATOLOGY
C         JSDATE     INIT       STARTING JULIAN DAY FOR CLIMATOLOGY
C         JSYR       INIT       STARTING YEAR FOR CLIMATOLOGY
C         KL12       INIT       12HR ERROR CALCULATION FLAG
C         KL24       INIT       24HR ERROR CALCUALTION FLAG
C         KMONE      INIT       ENDING MONTH FOR CLIMATOLOGY
C         KMONS      INIT       STARTING MONTH FOR CLIMATOLOGY
C         KONT       INIT       FLAG FOR CONTIUATION OF PROCESSING
C         KONTIG     LOGICAL    FLAG TO INDICATE IF KMONS TO KMONE
C                               CROSSES FROM DECEMBER TO JANUARY
C         KONTK      INIT       SAME AS KONT, EXCEPT FOR RECURVER
C         KPTR       INIT       SAME AS NPTR, EXCEPT FOR RECURVER
C         LM12       INIT       INDEX TO CLIMATOLOGY FOR BEST 12-HR
C         LM24       INIT       INDEX TO CLIMATOLOGY FOE BEST 24-HR
C         MNNR       INIT       MINIMUM NUMBER OF REQUIRED OBSERVATIONS
C         MO         INIT       INDEX TO MONTHLY CLIMATOLOGY FILES
C         MOX        INIT       INDEX TO LAST CLIMATOLOGY MONTH PLUS ONE
C         NC         INIT       INDEX TO SCREENED CLIMATOLOGY VALUES
C         NCR        INIT       NUMBER OF CLIMATOLOGY RECORDS READ
C         NCTD       INIT       NUMBER OF CYCLONE POSITIONS THAT PASSED
C                               DISTANCE SCREEN
C         NCTW       INIT       NUMBER OF CYCLONE POSITIONS THAT PASSED
C                               TIME SCREEN
C         NCWS       INIT       NUMBER OF CYCLONE POSITIONS THAT PASSED
C                               WIND-SPEED SCREEN
C         NC12       INIT       NUMBER OF OBSERVATIONS FROM -12 TO 00 HR
C         NC24       INIT       NUMBER OF OBSERVATIONS FROM -24 TO 00 HR
C         NPHR       INIT       MAXIMUM HRS FOR MATCHING WITH WORKING
C                               BEST TRACK (12 OR 24)
C         NHPRR      INIT       SAME AS NPHR, EXCEPT FOR RECURVER
C         NK         INIT       SAME AS NS, EXCEPT FOR RECURVER
C         NPTR       INIT       ARRAY OF POINTERS TO SCREENED
C                               CLIMATOLOGY
C         NS         NS         NUMBER OF SCREENED OBSERVATIONS
C         NUINT      INIT       UNIT NUMBER FOR READING CLIMATOLOGY
C         OFFLN      REAL       LONGITUDE OFFSET BETWEEN WORKING BEST
C                               TRACK POSITION AND STARTING CLIMATOLOGY
C                               MATCHING POSITION, DEG
C         OFFLT      REAL       LATITUDE OFFSET BETWEEN WORKING BEST
C                               TRACK POSITION AND STARTING CLIMATOLOGY
C                               MATCHING POSITION, DEG
C         REGFLE     CHAR       REGIONAL, MONTHLY CLIMATOLOGY FILE NAME
C         RE12       REAL       RUNNING LEAST 12-HR WEIGHTED ERROR, NM
C         RE24       REAL       RUNNING LEAST 24-HR WEIGHTED ERROR, NM
C         SPDMX      REAL       ARRAY OF WIND-SPEED-SCREEN VALUES
C         WE         REAL       WEIGHTED ERROR, NM
C         XE         REAL       CROSS-TRACK ERROR, NM
C         XEWT       REAL       WEIGHT APPLIED TO XE
C
C  METHOD:  1. READ WINDOWED CLIMATOLOGY FILES AND SCREEN WITH:
C              A. DAYS
C              B. DISTANCE
C              C. WIND SPEED
C              D. TRACK DEVIATION
C              NOTE:  AFTER FIRST CALL, STRAIGHT AND RECURVER USE THEIR
C                     OWN "INITIAL" CONDITIONS DURING SCREENINGS.
C           2. KEEP AND SORT TOP FIVE CLIMATOLOGY TROPICAL CYCLONES
C              FOR BEST MATCHING OVER 12-HR AND 24-HR PERIODS FOR:
C              KSTRC - 4  DO ALL FOUR TYPES, S, R, O AND T
C                      3  DO TYPES S AND R
C                      2  DO TYPE R
C                      1  DO TYPE S
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  BSTCLM*01  (21 JUL 1993)  --  HAMILTON,H.
C           ADD CHANGES TO ALLOW TYAN93 TO FORECAST
C
C
C...................END PROLOGUE.......................................
C
      CHARACTER CMONTH(12)*3, CREGS(5)*4, REGFLE*7, CSTR*30
C
      LOGICAL KONTIG
C
      INTEGER NPTR(99), KPTR(99)
C
      REAL SPDMX(2)
      character*100 filename,dir
C
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW24  - PAST 24 HR EAST/WEST HEMISPHERE INDOCATOR, E OR W
C
      CHARACTER CNAME*7, CDTG*8, CNS*1, CEW*1, EW12*1, EW24*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12,EW24
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG (+ NH, - SH)
C   FLN   - FIX LONGITUDE, DEG (EAST)
C   PLT12 - PAST 12 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN12 - PAST 12 HR LONGITUDE, DEG (EAST)
C   PLT24 - PAST 24 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN24 - PAST 24 HR LONGITUDE, DEG (EAST)
C   HD12S - HEADING  FROM -12 TO FIX LOCATION (STRAIGHT), DEG
C   DT12S - DISTANCE FROM -12 TO FIX LOCATION (STRAIGHT), NM
C   HD24S - HEADING  FROM -24 TO FIX LOCATION (STRAIGHT), DEG
C   DT24S - DISTANCE FROM -24 TO FIX LOCATION (STRAIGHT), NM
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12,PLT24,PLN24
     .             ,HD12S,DT12S,HD24S,DT24S
C
C
C                   EXPLANATION OF /POSITR/ VARIABLES FOR RECURVERS
C
C   NREGNR - NUMBER OF BASIN FROM FIX POSITION
C   FLTR   - INITIAL LATITUDE, DEG
C   FLNR   - INITIAL LONGITUDE, DEG
C   PLT12R - PAST 12 HR LATITUDE,  DEG
C   PLN12R - PAST 12 HR LONGITUDE, DEG
C   PLT24R - PAST 24 HR LATITUDE,  DEG
C   PLN24R - PAST 24 HR LONGITUDE, DEG
C   HD12R  - HEADING  FROM -12 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -12 TO FIX LOCATION (RECURVER), NM
C   HD24R  - HEADING  FROM -24 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -24 TO FIX LOCATION (RECURVER), NM
C
      COMMON/POSITR/ NREGNR,FLTR,FLNR,FWDR,PLT12R,PLN12R,PLT24R,PLN24R,
     .               HD12R,DT12R,HD24R,DT24R
C
C  <<CHANGE NOTICE>>  $TYANB101  (21 JUL 1993)  --  HAMILTON,H.
C           ADD HEADING AND DISTANCE TO DCREASE RUNNING TIME.
C           ADD /POSITR/ TO ALLOW FORECASTING BY TYAN93.
C
C                   EXPLANATION OF /CBCLM/ VARIABLES
C
C   CYCYYX  - NAME/IDENTIFICATION OF CLIMO CYCLONE
C       YY  - HOUR, 12 OR 24
C        X  - A - S-TYPE (STRAIGHT)
C             B - R-TYPE (RECURVER)
C             C - O-TYPE (OTHER)
C             D - ALL-TYPES (S, R AND O)
C
      CHARACTER*8 CYC12A,CYC24A,CYC12B,CYC24B,CYC12C,CYC24C,
     .            CYC12D,CYC24D
C
      COMMON/CBCLM/ CYC12A(6),CYC24A(6),CYC12B(6),CYC24B(6),
     .              CYC12C(6),CYC24C(6),CYC12D(6),CYC24D(6)
C
C                   EXPLANATION OF /BCLMX/ VARIABLES
C
C   NYRYYX - YEAR OF INITIAL POSITION
C   NDYYYX - JULIAN DAY OF INITIAL POSITION
C   MYRYYX - YEAR OF POSITION
C   DYJYYX - JULIAN DAY OF POSITION
C   MHRYYX - HOUR OF POSITION
C   CLTYYX - LATITUDE OF POSITION (+ NH, - SH)
C   CLNYYX - LONGITUDE OF POSITION (0 - 360 EAST)
C   WNDYYX - ANALOG FORECAST 12-HR WIND SPEED CHANGE, KT
C   EYYX   - WEIGHTED ERROR DIFFERENCE BETWEEN TRANSPOSED CLIMATOLOGY
C            AND YY HOUR POSITION LATER
C   ALTYXX - ANALOG TAU 12 FORECAST OF LATITUDE, DEG
C   ALNYYX - ANALOG TAU 12 FORECAST OF LONGITUDE, DEG
C   MRYYX  - NUMBER OF VALUES
C      YY  - HOUR, 12 OR 24
C       X  - A - S-TYPE (STRAIGHT)
C            B - R-TYPE (RECURVER)
C            C - O-TYPE (OTHER)
C            D - ALL-TYPES (S, R AND O)
C
      COMMON/BCLMA/ NYR12A(6),NDY12A(6),MYR12A(6),MDY12A(6),MHR12A(6),
     .              CLT12A(6),CLN12A(6),WND12A(6),E12A(6),
     .              ALT12A(6),ALN12A(6),MR12A,
     .              NYR24A(6),NDY24A(6),MYR24A(6),MDY24A(6),MHR24A(6),
     .              CLT24A(6),CLN24A(6),WND24A(6),E24A(6),
     .              ALT24A(6),ALN24A(6),MR24A
      COMMON/BCLMB/ NYR12B(6),NDY12B(6),MYR12B(6),MDY12B(6),MHR12B(6),
     .              CLT12B(6),CLN12B(6),WND12B(6),E12B(6),
     .              ALT12B(6),ALN12B(6),MR12B,
     .              NYR24B(6),NDY24B(6),MYR24B(6),MDY24B(6),MHR24B(6),
     .              CLT24B(6),CLN24B(6),WND24B(6),E24B(6),
     .              ALT24B(6),ALN24B(6),MR24B
      COMMON/BCLMC/ NYR12C(6),NDY12C(6),MYR12C(6),MDY12C(6),MHR12C(6),
     .              CLT12C(6),CLN12C(6),E12C(6),MR12C,
     .              NYR24C(6),NDY24C(6),MYR24C(6),MDY24C(6),MHR24C(6),
     .              CLT24C(6),CLN24C(6),E24C(6),MR24C
      COMMON/BCLMD/ NYR12D(6),NDY12D(6),MYR12D(6),MDY12D(6),MHR12D(6),
     .              CLT12D(6),CLN12D(6),E12D(6),MR12D,
     .              NYR24D(6),NDY24D(6),MYR24D(6),MDY24D(6),MHR24D(6),
     .              CLT24D(6),CLN24D(6),E24D(6),MR24D
C
C
C  <<CHANGE NOTICE>>  $TYANB201  (21 JUL 1993)  --  HAMILTON,H.
C           ADD WNDYYX, ALTYYX, ALNYYX, WHERE YY IS 12
C           OR 24 AND X IS A OR B, TO ALLOW FORECASTING BY TYAN93
C
C
C  <<CHANGE NOTICE>>  $TYANB103  (21 JUL 1993)  --  SAMPSON,B.
C           FILE CHANGES FOR ATCF 3.0.
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
C         YLAT   - LATITUDE  OF POSITION, (DEG - + NH, - SH) ???
C         WIND   - MAXIMUM SUSTAINED WIND SPEED, (KT)
C         NR     - NUMBER OF RECORDS READ
C
      COMMON /STORM/ IYR(99),JDAY(99),IHR(99),XLON(99),YLAT(99),
     .               WIND(99),NR
C
C
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
C                   SET MAX WIND SPEED SCREENING SPEEDS
      DATA SPDMX/34.0, 69.0/
C                   SET CROSS-TRACK WEIGHTING FACTOR
      DATA XEWT/2.0/
C                   SET UNIT NUMBER FOR CLIMATOLOGY DATA
      DATA NUNIT/2/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C                   ZERO COUNT OF RETAINED MATCHED CYCLONES
      MR12A = 0
      MR24A = 0
      MR12B = 0
      MR24B = 0
      MR12C = 0
      MR24C = 0
      MR12D = 0
      MR24D = 0
      IF (ABS (PLT24).GT.0.0 .AND. ABS (PLN24).GT.0.0) THEN
        NPHR = 24
      ELSEIF (ABS (PLT12).GT.0.0 .AND. ABS (PLN12).GT.0.0) THEN
        NPHR = 12
      ELSE
        NPHR = 0
      ENDIF
C                   SET NPHRR FLAG FOR RECURVERS
      IF (ABS (PLT24R).GT.0.0 .AND. ABS (PLN24R).GT.0.0) THEN
        NPHRR = 24
      ELSEIF (ABS (PLT12R).GT.0.0 .AND. ABS (PLN12R).GT.0.0) THEN
        NPHRR = 12
      ELSE
        NPHRR = 0
      ENDIF
C
C*****************  CACULATE JULIAN DATE OF FIX POSITION  **************
C
      READ (CDTG,501) IFYR,IFMON,IFDAY
  501 FORMAT (3I2)
      JFDATE = JDAYEM (IFYR,IFMON,IFDAY)
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
      CALL JLTOMD (JSYR,JSDATE,KMONS,KDAYS)
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
      CALL JLTOMD (JEYR,JEDATE,KMONE,KDAYE)
C
      MO  = KMONS
      MOX = KMONE +1
      IF (MOX .EQ. 13) MOX = 1
cx    PRINT 9010, CMONTH(MO),CMONTH(MOX)
      write(13,9010) cmonth(mo),cmonth(mox)
 9010 FORMAT (' TYAN93, BSTCLM USING OBSERVATIONS STARTING IN ',A3,
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
        NC24 = 4
        NC12 = 2
        IF (NPHR .EQ. 24) THEN
          MNNR = 7
          JS   = 5
        ELSE
          MNNR = 5
          JS   = 3
        ENDIF
      ELSE
C                   CLIMATOLOGY OBSERVATIONS ARE 12 HOURS APART
        NC24 = 2
        NC12 = 1
        IF (NPHR .EQ. 24) THEN
          MNNR = 4
          JS   = 3
        ELSE
          MNNR = 3
          JS   = 2
        ENDIF
      ENDIF
C                   ZERO CLIMATOLOGY COUNTS
      NCR  = 0
      NCTW = 0
      NCTD = 0
      NCWS = 0
C
      WRITE (13,9015) FLT,FLN,FWD, FLTR,FLNR,FWDR, CDTG, KTRY
 9015 FORMAT (' TYAN93, BSTCLM STARTING STRAIGHT AT ',F5.1,',',F5.1,
     .   ' WIND ',F5.0,/,25X,'RECURVER AT ',F5.1,',',F5.1,' WIND ',F5.0,
     .   ' FOR ',A8,' TRY IS ',I1)
C
C********  READ CYCLONE CLIMATOLOGY FILE, ONE COMPLETE CYCLONE AT A TIME
C
C                   CALCULATE CLIMATOLOGY FILENAME
      REGFLE(1:4) = CREGS(NREGN)
  120 CONTINUE
      REGFLE(5:7) = CMONTH(MO)
c
c  filenames are now all lower case
c
      call locase (regfle,7)

cx    PRINT 9020, REGFLE
      write(13,9020) regfle
 9020 FORMAT (' TYAN93, CLIMO CHECKING CYCLONE HISTORY FILE: ',A7)
      CSTR(7:13) = REGFLE
C                   WARNING: USE DELETE ON CDC MAINFRAME ONLY
cx    CLOSE (NUNIT,STATUS='DELETE')
      close (nunit)
cx    CALL ATTACH (CSTR,IERC,ICYL)
      ierc=0
      IF (IERC .EQ. 0) THEN
C
C                   THIS MONTH'S FILE IS AVAILABLE
C                   OTHERWISE, GO ON TO THE NEXT FILE/MONTH
C
cx      PRINT 9030, REGFLE, ICYL
cx 9030   FORMAT (' TYAN93, BSTCLM OPENING HISTORY FILE ',A7,' CYCLE ',I3)
        write(13,9030) regfle
 9030   format (' TYAN93, BSTCLM OPENING HISTORY FILE ',a7)
cx      OPEN (NUNIT,FILE='TAPE2',ACCESS='SEQUENTIAL',FORM='FORMATTED',
cx   .        STATUS='OLD',IOSTAT=IOFLAG)
c
c  get the standalone directory
c
	call getenv("STANDALONE",dir)
	ind=index(dir," ")-1
c
c  put full path name into character array
c
	write(filename,'(a,a,a)')dir(1:ind),'/tyan_dat/',regfle
c
c  open climatology data file
c
        open (nunit,file=filename,
     .	      access='SEQUENTIAL', form='FORMATTED',
     .        status='OLD',iostat=ioflag)
        IF (IOFLAG .EQ. 0) THEN
cx        PRINT 9040, REGFLE
          write(13,9040) regfle
 9040     FORMAT (' TYAN93, BSTCLM PROCESSING HISTORY FILE ',A7)
          REWIND (NUNIT)
C                   SET END-OF-FILE FLAG TO NO EOF.
          IEOF = 0
  130     CONTINUE
C
C                    READ A COMPLETE SET OF NR CLIMATOLOGY OBSERVATIONS
C
          CALL REDCLM (NUNIT,NREGN,IEOF)
          NCR = NCR +1
          JGO = 0
          IF (KSTRC .LT. 4) THEN
C
C                   ONLY STRAIGHT OR RECURVER TYPES ARE BEING PROCESSED
C
            IF (STYPE.NE.'S' .AND. STYPE.NE.'R') THEN
C                       WRONG TYPE CYCLONE FOR PROCESSING
              JGO = -1
            ELSEIF (KSTRC.EQ.2 .AND. STYPE.NE.'R') THEN
C                       WRONG TYPE CYCLONE FOR PROCESSING
              JGO = -1
            ELSEIF (KSTRC.EQ.1 .AND. STYPE.NE.'S') THEN
C                       WRONG TYPE CYCLONE FOR PROCESSING
              JGO = -1
            ENDIF
            IF (JGO .NE. 0) THEN
C                   DO NOT PROCESS CYCLONE
              IF (IEOF .EQ. 0) THEN
C                   READ NEXT CYCLONE
                GOTO 130
C
              ELSE
C                   FINISHED PROCESSING ALL CYCLONES ON THIS FILE
                GOTO 200
C
              ENDIF
            ENDIF
          ENDIF
C
C                   IF OBSERVATION SET IS LESS THAN MNNR, DO NOT USE
C
          IF (NR .GE. MNNR) THEN
C
C****************  PROCESS CYCLONE OBSERVATIONS  ***********************
C
            NK = 0
            NS = 0
            DO 150 N=JS, NR -NC12
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
               NCTW  = NCTW +1
               KONTK = KONT
               IF (KSTRC .NE. 2) THEN
C
C                   CHECK ON STRAIGHT AND OTHER TYPE CLIMO CYCLONES
C
                IF (ABS (FLT -YLAT(N)) .LE. DSTLAT .AND.
     .              ABS (FLN -XLON(N)) .LE. DSTLON) THEN
C
C***************** PASSED S DISTANCE SCREEN  ***************************
C
                  NCTD = NCTD +1
                 IF (FWD.GT.0.0 .AND. WIND(N).GT.0.0) THEN
                  IF (FWD .LT. 30.0) THEN
                    IF (WIND(N) .GT. 30.0) KONT = 0
                  ELSEIF (FWD .LT. 35.0) THEN
                    IF (WIND(N).LT.25.0 .OR. WIND(N).GT.35.0) KONT = 0
                  ELSEIF (WIND(N) .LT. 35.0) THEN
                    KONT = 0
                  ELSEIF (WIND(N) .LT. (FWD -SPDMX(KTRY)) .OR.
     .                    WIND(N) .GT. (FWD +SPDMX(KTRY))) THEN
                    KONT = 0
                  ENDIF
                 ENDIF
                  IF (KONT .NE. 0) THEN
C
C***************** PASSED S WIND SPEED SCREEN **************************
C
C                          THERE IS AT LEAST A TAU 12 POSITION FROM THIS
C                          POSITION, SO SAVE POINTER
C
                    NS = NS +1
                    NPTR(NS) = N
                    NCWS = NCWS +1
                  ENDIF
                ENDIF
               ENDIF
               IF (KSTRC .NE. 1) THEN
C
C                   CHECK ON RECURVER TYPE CLIMO CYCLONES
C
                 IF (ABS (FLTR -YLAT(N)) .LE. DSTLAT .AND.
     .               ABS (FLNR -XLON(N)) .LE. DSTLON) THEN
C
C*************************  PASSED R-DISTANCE SCREEN  ******************
C
                   IF (FWDR.GT.0.0 .AND. WIND(N).GT.0.0) THEN
                     IF (FWDR .LT. 30.0) THEN
                       IF (WIND(N) .GT. 30.0) KONTK = 0
                     ELSEIF (FWDR .EQ. 30.0) THEN
                       IF (WIND(N).LT.25.0 .OR. WIND(N).GT.35.0)
     .                   KONTK = 0
                     ELSEIF (WIND(N) .LT. 35.0) THEN
                       KONTK = 0
                     ELSEIF (WIND(N) .LT. (FWDR -SPDMX(KTRY)) .OR.
     .                       WIND(N) .GT. (FWDR +SPDMX(KTRY))) THEN
                       KONTK = 0
                     ENDIF
                   ENDIF
                   IF (KONTK .NE. 0) THEN
C
C*************************  PASSED R WIND SPEED SCREEN  ****************
C
C                          THERE IS AT LEAST A TAU 12 POSITION FROM THIS
C                          POSITION, SO SAVE POINTER
C
                     NK       = NK +1
                     KPTR(NK) = N
                   ENDIF
                 ENDIF
               ENDIF
              ENDIF
  150       CONTINUE
            IF (NS .GT. 0) THEN
C
C                   CALCULATE ASSOCIATED ALONG AND CROSS TRACK ERRORS
C                   FOR STRAIGHT (AND RECURVER WHEN KSTRC IS 4)
C
              LM12 = 0
              LM24 = 0
              RE24 = 9999.99
              RE12 = 9999.99
              DO 160 N=1, NS
C                   NX IS THE INDEX INTO CLIMATOLOGY FOR "FIX" LOCATION
                NX = NPTR(N)
                IF (NPHR .EQ. 24) THEN
C                         CALCULATE 24 HR POSITION OFFSETS
                  NC    = NX -NC24
                  OFFLT = PLT24 -YLAT(NC)
                  FLT24 = YLAT(NX) +OFFLT
                  OFFLN = PLN24 -XLON(NC)
                  FLN24 = XLON(NX) +OFFLN
                  CALL CLXEAE (HD24S,DT24S,PLT24,PLN24,FLT24,FLN24,XE,
     .                         AE,KL24)
                  IF (KL24 .LT. 0) THEN
C                          XE AND AE HAVE VALID VALUES
                    WE = XEWT*ABS (XE) +ABS (AE)
                    IF (WE .LE. RE24) THEN
C                          SAVE LEAST ERROR AND INDEX VALUE
                      RE24 = WE
                      LM24 = NX
                    ENDIF
                  ENDIF
                ENDIF
C                        CALCULATE 12 HR POSITION OFFSETS
                NC    = NX -NC12
                OFFLT = PLT12 -YLAT(NC)
                FLT12 = YLAT(NX) +OFFLT
                OFFLN = PLN12 -XLON(NC)
                FLN12 = XLON(NX) +OFFLN
                CALL CLXEAE (HD12S,DT12S,PLT12,PLN12,FLT12,FLN12,XE,
     .                       AE,KL12)
                IF (KL12 .LT. 0) THEN
C                        XE AND AE HAVE VALID VALUES
                  WE = XEWT*ABS (XE) +ABS (AE)
                  IF (WE .LE. RE12) THEN
C                        SAVE LEAST ERROR AND INDEX VALUE
                    RE12 = WE
                    LM12 = NX
                  ENDIF
                ENDIF
  160         CONTINUE
C
C                   STORE IDENTIFICATION AND RESULTS
C                   OF S, R OR O VALUES
C
              IF (STYPE .EQ. 'S') THEN
                IF (LM12 .GT. 0) THEN
                  IF (MR12A .LT. 5) THEN
                    MR12A         = MR12A +1
                    NYR12A(MR12A) = IYR(1)
                    NDY12A(MR12A) = JDAY(1)
                    MYR12A(MR12A) = IYR(LM12)
                    MDY12A(MR12A) = JDAY(LM12)
                    MHR12A(MR12A) = IHR(LM12)
                    CLT12A(MR12A) = YLAT(LM12)
                    CLN12A(MR12A) = XLON(LM12)
                    IF (WIND(LM12).GT.0.0 .AND. WIND(LM12+NC12).GT.0.0)
     .                THEN
                      WND12A(MR12A) = WIND(LM12+NC12) -WIND(LM12)
                    ELSE
                      WND12A(MR12A) = -99.0
                    ENDIF
                    E12A(MR12A)   = RE12
                    OFFLT         = FLT -YLAT(LM12)
                    ALT12A(MR12A) = YLAT(LM12+NC12) +OFFLT
                    OFFLN         = FLN -XLON(LM12)
                    ALN12A(MR12A) = XLON(LM12+NC12) +OFFLN
                    CYC12A(MR12A) = STNAME
                    IF (MR12A .EQ. 5) CALL SORTEM (1,1,5)
                  ELSE
                    IF (RE12 .LT. E12A(5)) THEN
                      NYR12A(6) = IYR(1)
                      NDY12A(6) = JDAY(1)
                      MYR12A(6) = IYR(LM12)
                      MDY12A(6) = JDAY(LM12)
                      MHR12A(6) = IHR(LM12)
                      CLT12A(6) = YLAT(LM12)
                      CLN12A(6) = XLON(LM12)
                      IF (WIND(LM12).GT.0.0 .AND.
     .                    WIND(LM12+NC12).GT.0.0) THEN
                        WND12A(6) = WIND(LM12+NC12) -WIND(LM12)
                      ELSE
                        WND12A(6) = -99.0
                      ENDIF
                      E12A(6)   = RE12
                      OFFLT     = FLT -YLAT(LM12)
                      ALT12A(6) = YLAT(LM12+NC12) +OFFLT
                      OFFLN     = FLN -XLON(LM12)
                      ALN12A(6) = XLON(LM12+NC12) +OFFLN
                      CYC12A(6) = STNAME
                      CALL SORTEM (1,1,6)
                    ENDIF
                  ENDIF
                ENDIF
                IF (LM24 .GT. 0) THEN
                  IF (MR24A .LT. 5) THEN
                    MR24A         = MR24A +1
                    NYR24A(MR24A) = IYR(1)
                    NDY24A(MR24A) = JDAY(1)
                    MYR24A(MR24A) = IYR(LM24)
                    MDY24A(MR24A) = JDAY(LM24)
                    MHR24A(MR24A) = IHR(LM24)
                    CLT24A(MR24A) = YLAT(LM24)
                    CLN24A(MR24A) = XLON(LM24)
                    IF (WIND(LM24).GT.0.0 .AND. WIND(LM24+NC12).GT.0.0)
     .                THEN
                      WND24A(MR24A) = WIND(LM24+NC12) -WIND(LM24)
                    ELSE
                      WND24A(MR24A) = -99.0
                    ENDIF
                    E24A(MR24A)   = RE24
                    OFFLT         = FLT -YLAT(LM24)
                    ALT24A(MR24A) = YLAT(LM24+NC12) +OFFLT
                    OFFLN         = FLN -XLON(LM24)
                    ALN24A(MR24A) = XLON(LM24+NC12) +OFFLN
                    CYC24A(MR24A) = STNAME
                    IF (MR24A .EQ. 5) CALL SORTEM (1,2,5)
                  ELSE
                    IF (RE24 .LT. E24A(5)) THEN
                      NYR24A(6) = IYR(1)
                      NDY24A(6) = JDAY(1)
                      MYR24A(6) = IYR(LM24)
                      MDY24A(6) = JDAY(LM24)
                      MHR24A(6) = IHR(LM24)
                      CLT24A(6) = YLAT(LM24)
                      CLN24A(6) = XLON(LM24)
                      IF (WIND(LM24).GT.0.0 .AND.
     .                    WIND(LM24+NC12).GT.0.0) THEN
                        WND24A(6) = WIND(LM24+NC12) -WIND(LM24)
                      ELSE
                        WND24A(6) = -99.0
                      ENDIF
                      E24A(6)   = RE24
                      OFFLT     = FLT -YLAT(LM24)
                      ALT24A(6) = YLAT(LM24+NC12) +OFFLT
                      OFFLN     = FLN -XLON(LM24)
                      ALN24A(6) = XLON(LM24+NC12) +OFFLN
                      CYC24A(6) = STNAME
                      CALL SORTEM (1,2,6)
                    ENDIF
                  ENDIF
                ENDIF
              ENDIF
            ENDIF
            IF (STYPE.EQ.'R' .AND. NK.GT.0 .AND. KSTRC.NE.1) THEN
              IF (KSTRC .NE. 4) THEN
C
C                   CALCULATE ASSOCIATED ALONG AND CROSS TRACK ERRORS
C                   FOR RECURVER TYPE
C
                LM12 = 0
                LM24 = 0
                RE24 = 9999.99
                RE12 = 9999.99
                DO 170 N=1, NK
                  NX = KPTR(N)
                  IF (NPHRR .EQ. 24) THEN
C                         CALCULATE 24 HR POSITION OFFSETS
                    NC    = NX -NC24
                    OFFLT = PLT24R -YLAT(NC)
                    FLT24 = YLAT(NX) +OFFLT
                    OFFLN = PLN24R -XLON(NC)
                    FLN24 = XLON(NX) +OFFLN
                    CALL CLXEAE (HD24R,DT24R,PLT24R,PLN24R,FLT24,FLN24,
     .                           XE,AE,KL24)
                    IF (KL24 .LT. 0) THEN
C                          XE AND AE HAVE VALID VALUES
                      WE = XEWT*ABS (XE) +ABS (AE)
                      IF (WE .LE. RE24) THEN
C                          SAVE LEAST ERROR AND INDEX VALUE
                        RE24 = WE
                        LM24 = NX
                      ENDIF
                    ENDIF
                  ENDIF
C                        CALCULATE 12 HR POSITION OFFSETS
                  NC    = NX -NC12
                  OFFLT = PLT12R -YLAT(NC)
                  FLT12 = YLAT(NX) +OFFLT
                  OFFLN = PLN12R -XLON(NC)
                  FLN12 = XLON(NX) +OFFLN
                  CALL CLXEAE (HD12R,DT12R,PLT12R,PLN12R,FLT12,FLN12,XE,
     .                         AE,KL12)
                  IF (KL12 .LT. 0) THEN
C                        XE AND AE HAVE VALID VALUES
                    WE = XEWT*ABS (XE) +ABS (AE)
                    IF (WE .LE. RE12) THEN
C                        SAVE LEAST ERROR AND INDEX VALUE
                      RE12 = WE
                      LM12 = NX
                    ENDIF
                  ENDIF
  170           CONTINUE
              ENDIF
                IF (LM12 .GT. 0) THEN
                  IF (MR12B .LT. 5) THEN
                    MR12B         = MR12B +1
                    NYR12B(MR12B) = IYR(1)
                    NDY12B(MR12B) = JDAY(1)
                    MYR12B(MR12B) = IYR(LM12)
                    MDY12B(MR12B) = JDAY(LM12)
                    MHR12B(MR12B) = IHR(LM12)
                    CLT12B(MR12B) = YLAT(LM12)
                    CLN12B(MR12B) = XLON(LM12)
                    IF (WIND(LM12).GT.0.0 .AND. WIND(LM12+NC12).GT.0.0)
     .                THEN
                      WND12B(MR12B) = WIND(LM12+NC12) -WIND(LM12)
                    ELSE
                      WND12B(MR12B) = -99.0
                    ENDIF
                    E12B(MR12B)   = RE12
                    OFFLT         = FLTR -YLAT(LM12)
                    ALT12B(MR12B) = YLAT(LM12+NC12) +OFFLT
                    OFFLN         = FLNR -XLON(LM12)
                    ALN12B(MR12B) = XLON(LM12+NC12) +OFFLN
                    CYC12B(MR12B) = STNAME
                    IF (MR12B .EQ. 5) CALL SORTEM (2,1,5)
                  ELSE
                    IF (RE12 .LT. E12B(5)) THEN
                      NYR12B(6) = IYR(1)
                      NDY12B(6) = JDAY(1)
                      MYR12B(6) = IYR(LM12)
                      MDY12B(6) = JDAY(LM12)
                      MHR12B(6) = IHR(LM12)
                      CLT12B(6) = YLAT(LM12)
                      CLN12B(6) = XLON(LM12)
                      IF (WIND(LM12).GT.0.0 .AND.
     .                    WIND(LM12+NC12).GT.0.0) THEN
                        WND12B(6) = WIND(LM12+NC12) -WIND(LM12)
                      ELSE
                        WND12B(6) = -99.0
                      ENDIF
                      E12B(6)   = RE12
                      OFFLT     = FLTR -YLAT(LM12)
                      ALT12B(6) = YLAT(LM12+NC12) +OFFLT
                      OFFLN     = FLNR -XLON(LM12)
                      ALN12B(6) = XLON(LM12+NC12) +OFFLN
                      CYC12B(6) = STNAME
                      CALL SORTEM (2,1,6)
                    ENDIF
                  ENDIF
                ENDIF
                IF (LM24 .GT. 0) THEN
                  IF (MR24B .LT. 5) THEN
                    MR24B         = MR24B +1
                    NYR24B(MR24B) = IYR(1)
                    NDY24B(MR24B) = JDAY(1)
                    MYR24B(MR24B) = IYR(LM24)
                    MDY24B(MR24B) = JDAY(LM24)
                    MHR24B(MR24B) = IHR(LM24)
                    CLT24B(MR24B) = YLAT(LM24)
                    CLN24B(MR24B) = XLON(LM24)
                    IF (WIND(LM24).GT.0.0 .AND. WIND(LM24+NC12).GT.0.0)
     .                THEN
                      WND24B(MR24B) = WIND(LM24+NC12) -WIND(LM24)
                    ELSE
                      WND24B(MR24B) = -99.0
                    ENDIF
                    E24B(MR24B)   = RE24
                    OFFLT         = FLTR -YLAT(LM24)
                    ALT24B(MR24B) = YLAT(LM24+NC12) +OFFLT
                    OFFLN         = FLNR -XLON(LM24)
                    ALN24B(MR24B) = XLON(LM24+NC12) +OFFLN
                    CYC24B(MR24B) = STNAME
                    IF (MR24B .EQ. 5) CALL SORTEM (2,2,5)
                  ELSE
                    IF (RE24 .LT. E24B(5)) THEN
                      NYR24B(6) = IYR(1)
                      NDY24B(6) = JDAY(1)
                      MYR24B(6) = IYR(LM24)
                      MDY24B(6) = JDAY(LM24)
                      MHR24B(6) = IHR(LM24)
                      CLT24B(6) = YLAT(LM24)
                      CLN24B(6) = XLON(LM24)
                      IF (WIND(LM24).GT.0.0 .AND.
     .                    WIND(LM24+NC12) .GT.0.0) THEN
                        WND24B(6) = WIND(LM24+NC12) -WIND(LM24)
                      ELSE
                        WND24B(6) = -99.0
                      ENDIF
                      E24B(6)   = RE24
                      OFFLT     = FLTR -YLAT(LM24)
                      ALT24B(6) = YLAT(LM24+NC12) +OFFLT
                      OFFLN     = FLNR -XLON(LM24)
                      ALN24B(6) = XLON(LM24+NC12) +OFFLN
                      CYC24B(6) = STNAME
                      CALL SORTEM (2,2,6)
                    ENDIF
                  ENDIF
                ENDIF
            ENDIF
            IF (NS .GT. 0) THEN
              IF (STYPE.EQ.'O' .AND. KSTRC.EQ.4) THEN
                IF (LM12 .GT. 0) THEN
                  IF (MR12C .LT. 5) THEN
                    MR12C         = MR12C +1
                    NYR12C(MR12C) = IYR(1)
                    NDY12C(MR12C) = JDAY(1)
                    MYR12C(MR12C) = IYR(LM12)
                    MDY12C(MR12C) = JDAY(LM12)
                    MHR12C(MR12C) = IHR(LM12)
                    CLT12C(MR12C) = YLAT(LM12)
                    CLN12C(MR12C) = XLON(LM12)
                    E12C(MR12C)   = RE12
                    CYC12C(MR12C) = STNAME
                    IF (MR12C .EQ. 5) CALL SORTEM (3,1,5)
                  ELSE
                    IF (RE12 .LT. E12C(5)) THEN
                      NYR12C(6) = IYR(1)
                      NDY12C(6) = JDAY(1)
                      MYR12C(6) = IYR(LM12)
                      MDY12C(6) = JDAY(LM12)
                      MHR12C(6) = IHR(LM12)
                      CLT12C(6) = YLAT(LM12)
                      CLN12C(6) = XLON(LM12)
                      E12C(6)   = RE12
                      CYC12C(6) = STNAME
                      CALL SORTEM (3,1,6)
                    ENDIF
                  ENDIF
                ENDIF
                IF (LM24 .GT. 0) THEN
                  IF (MR24C .LT. 5) THEN
                    MR24C         = MR24C +1
                    NYR24C(MR24C) = IYR(1)
                    NDY24C(MR24C) = JDAY(1)
                    MYR24C(MR24C) = IYR(LM24)
                    MDY24C(MR24C) = JDAY(LM24)
                    MHR24C(MR24C) = IHR(LM24)
                    CLT24C(MR24C) = YLAT(LM24)
                    CLN24C(MR24C) = XLON(LM24)
                    E24C(MR24C)   = RE24
                    CYC24C(MR24C) = STNAME
                    IF (MR24C .EQ. 5) CALL SORTEM (3,2,5)
                  ELSE
                    IF (RE24 .LT. E24C(5)) THEN
                      NYR24C(6) = IYR(1)
                      NDY24C(6) = JDAY(1)
                      MYR24C(6) = IYR(LM24)
                      MDY24C(6) = JDAY(LM24)
                      MHR24C(6) = IHR(LM24)
                      CLT24C(6) = YLAT(LM24)
                      CLN24C(6) = XLON(LM24)
                      E24C(6)   = RE24
                      CYC24C(6) = STNAME
                      CALL SORTEM (3,2,6)
                    ENDIF
                  ENDIF
                ENDIF
              ENDIF
C
C                   LOAD TOTAL (S, R OR O) VALUES
C
              IF (LM12.GT.0 .AND. KSTRC.EQ.4) THEN
                IF (MR12D .LT. 5) THEN
                  MR12D         = MR12D +1
                  NYR12D(MR12D) = IYR(1)
                  NDY12D(MR12D) = JDAY(1)
                  MYR12D(MR12D) = IYR(LM12)
                  MDY12D(MR12D) = JDAY(LM12)
                  MHR12D(MR12D) = IHR(LM12)
                  CLT12D(MR12D) = YLAT(LM12)
                  CLN12D(MR12D) = XLON(LM12)
                  E12D(MR12D)   = RE12
                  CYC12D(MR12D) = STNAME
                  IF (MR12D .EQ. 5) CALL SORTEM (4,1,5)
                ELSE
                  IF (RE12 .LT. E12D(5)) THEN
                    NYR12D(6) = IYR(1)
                    NDY12D(6) = JDAY(1)
                    MYR12D(6) = IYR(LM12)
                    MDY12D(6) = JDAY(LM12)
                    MHR12D(6) = IHR(LM12)
                    CLT12D(6) = YLAT(LM12)
                    CLN12D(6) = XLON(LM12)
                    E12D(6)   = RE12
                    CYC12D(6) = STNAME
                    CALL SORTEM (4,1,6)
                  ENDIF
                ENDIF
              ENDIF
              IF (LM24.GT.0 .AND. KSTRC.EQ.4) THEN
                IF (MR24D .LT. 5) THEN
                  MR24D         = MR24D +1
                  NYR24D(MR24D) = IYR(1)
                  NDY24D(MR24D) = JDAY(1)
                  MYR24D(MR24D) = IYR(LM24)
                  MDY24D(MR24D) = JDAY(LM24)
                  MHR24D(MR24D) = IHR(LM24)
                  CLT24D(MR24D) = YLAT(LM24)
                  CLN24D(MR24D) = XLON(LM24)
                  E24D(MR24D)   = RE24
                  CYC24D(MR24D) = STNAME
                  IF (MR24D .EQ. 5) CALL SORTEM (4,2,5)
                ELSE
                  IF (RE24 .LT. E24D(5)) THEN
                    NYR24D(6) = IYR(1)
                    NDY24D(6) = JDAY(1)
                    MYR24D(6) = IYR(LM24)
                    MDY24D(6) = JDAY(LM24)
                    MHR24D(6) = IHR(LM24)
                    CLT24D(6) = YLAT(LM24)
                    CLN24D(6) = XLON(LM24)
                    E24D(6)   = RE24
                    CYC24D(6) = STNAME
                    CALL SORTEM (4,2,6)
                  ENDIF
                ENDIF
              ENDIF
            ENDIF
C                   READ NEXT SET OF CLIMATOLOGY OBSERVATIONS, IF NO EOF
            IF (IEOF .EQ. 0) GOTO 130
C
          ELSEIF (IEOF .EQ. 0) THEN
            WRITE (13,*)'TYAN93, CLIMO NOT ENOUGH OBS FOR ',STNAME
C                   READ NEXT SET OF CLIMATOLOGY OBSERVATIONS
            GOTO 130
C
          ELSE
            WRITE (13,*)'TYAN93,CLIMO NOT ENOUGH OBS FOR ',STNAME
            WRITE (13,*)'TYAN93,CLIMO EOF REACHED FOR MONTH ',CMONTH(MO)
          ENDIF
        ELSE
          WRITE (*,*)'TYAN93, ***** CLIMO OPEN ERROR IS ',IOFLAG,' ****'
        ENDIF
      ELSE
        WRITE (*,*)'TYAN93, ***** CLIMO ATTACH ERROR IS ',IERC,' *****'
      ENDIF
  200 CONTINUE
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
      IF (MR12A.GT.1 .AND. MR12A.LT.5) CALL SORTEM (1,1,MR12A)
      IF (MR24A.GT.1 .AND. MR24A.LT.5) CALL SORTEM (1,2,MR24A)
      IF (MR12B.GT.1 .AND. MR12B.LT.5) CALL SORTEM (2,1,MR12B)
      IF (MR24B.GT.1 .AND. MR24B.LT.5) CALL SORTEM (2,2,MR24B)
      IF (MR12C.GT.1 .AND. MR12C.LT.5) CALL SORTEM (3,1,MR12C)
      IF (MR24C.GT.1 .AND. MR24C.LT.5) CALL SORTEM (3,2,MR24C)
      IF (MR12D.GT.1 .AND. MR12D.LT.5) CALL SORTEM (4,1,MR12D)
      IF (MR24D.GT.1 .AND. MR24D.LT.5) CALL SORTEM (4,2,MR24D)
C
      WRITE (13,*) 'TYAN93, CLIMO READ ',NCR,' CYCLONES, FOUND ',NCTW,
     .            ' IN TIME WINDOW ',NCTD,' WITHIN DISTANCE, AND ',NCWS,
     .            ' IN WIND-SPEED RANGE'
      NSTRT = MR12A +MR24A
      NRECR = MR12B +MR24B
      IF (KSTRC .GE. 3) THEN
        NM12 = (MR12A +MR12B)/2
        NM24 = (MR24A +MR24B)/2
      ELSEIF (KSTRC .EQ. 2) THEN
        NM12 = MR12B
        NM24 = MR24B
      ELSE
        NM12 = MR12A
        NM24 = MR24A
      ENDIF
      WRITE (13,*) 'TYAN93, CLIMO MADE ',NM12,' 12HR ',NM24,' 24HR ',
     .       'MATCHES WITH ',DSTLAT,' DEG LAT AND ',DSTLON,' DEG LON'
      IF (NM12.LE.0 .AND. NM24.LE.0) THEN
C                   NO 12 OR 24 HOUR MATCHES WERE MADE
       WRITE (13,*) ' ***** INSUFFICIENT CYCLONES FOR TYAN93, FOR TRY ',
     .              KTRY
      ENDIF
      RETURN
C
      END
      SUBROUTINE REDCLM (NUNIT,NREGN,IEOF)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  REDCLM
C
C  DESCRIPTION:  READ ONE COMPLETE TROPICAL CYCLONE CLIMATOLOGY TRACK,
C                LOAD /STORMC/ AND /STORM/ VARIABLES
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL REDCLM (NUNIT,NREGN,IOEF)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     NUNIT        INIT          IN     UNIT NUMBER FOR READING CLIMO
C     NREGN        INIT          IN     REGION NUMBER
C     IOEF         INIT          OUT    EOF FLAG, 0 - NO EOF, 1 - EOF
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES OF LISTED COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C      STORMC    STNAME    CHAR     IN       CLIMATOLOGY CYCLONE NAME
C                STYPE     CHAR     IN       TRACK CLASSIFICATION
C                                            STRAIGHT, RECURVER OR OTHER
C      STORM     IYR       INIT     IN       YEAR OF POSITION
C                JDAY      INIT     IN       JULIAN DAY OF POSITION
C                IHR       INIT     IN       HOUR OF POSITION
C                XLON      REAL     IN       LONGITUDE OF POSITION, (E)
C                YLAT      REAL     IN       LATITUDE  OF POSITION (+/-)
C                WIND      REAL     IN       MAXIMUM WIND SPEED, (KT)
C                NR        INIT     IN       COUNT OF POSITIONS
C
C  FILES:
C    NAME     UNIT  FILE TYPE  ATTRIBUTE  USAGE         DESCRIPTION
C   -------  -----  ---------  ---------  ------   ---------------------
C  <DYNAMIC> NUNIT  PERMANENT  SEQUNTIAL    IN     CLIMATOLOGY DATA
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C  DYNAMIC CLIMATOLOGY FILE NAMES:  (XXX - THREE CHARACTER MONTH)
C         1 - NWPAXXX, NORTHWEST PACIFIC
C         2 - NEPAXXX, NORTHEAST PACIFIC
C         3 - NOINXXX, NORTH INDIAN
C         4 - SWINXXX, SOUTHWEST INDIAN
C         5 - SWPAXXX, SOUTHWEST PACIFIC (INCLUDES SE INDIAN OCEAN)
C
C  FORMAT OF CLIMATOLOGY DATA FILES:
C
C        VARIABLES IN EACH RECORD OF EACH MONTHLY FILE (IN SEQUENCE)
C
C  FOR: NWPA REGION (1)
C
C      MON     - MONTH OF INITIAL TROPICAL CYCLONE OBSERVATION
C      JYR     - YEAR OF INITIAL TROPICAL CYCLONE OBS, LAST TWO DIGITS
C      IDSTRM - STORM NUMBER, MUST NOT CHANGE FOR A GIVEN CYCLONE
C      IOBSVID - OBSERVATION NUMBER, MUST BE IN ASCENDING ORDER
C      IOBYR  - YEAR OF OBSERVATION
C      IOBMON - MONTH OF OBSERVATION
C      IOBDAY - DAY OF OBSERVATION
C      IOBHR  - HOUR OF OBSERVATION
C      IOBLAT - LATITUDE X10, (+N,-S)
C      IOBLON - LONGITUDE X10, (+E, -W)
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
C      IWNDSP - MAXIMUM SUSTAINED WIND SPEED, (KT)
C  *   MINHGT  - MINIMUM 700 MB HEIGHT, (TENS OF M)
C  *   IRDGLAT - 700 MB RIDGE LATITUDE, (TENTHS OF DEG)
C  *   IRDGHGT - 700 MB RIDGE HEIGHT, (TENS OF M)
C  *   ITROLON - 700 MB TROUGH LONGITUDE, (TENTHS OF DEG)
C  *   ITROHGT - 700 MB TROUGH HEIGHT, (TENS OF M)
C      IOBNAM - CYCLONE NAME
C  *   IOBTYP - CYCLONE TYPE - (S - STRAIGHT, R - RECURVER, O - OTHER)
C
C  FOR: NEPA REGION (2)
C
C      MON     - MONTH OF INITIAL TROPICAL CYCLONE OBSERVATION
C      JYR     - YEAR OF INITIAL TROPICAL CYCLONE OBS, LAST TWO DIGITS
C      IDSTRM - STORM NUMBER, MUST NOT CHANGE FOR A GIVEN CYCLONE
C      IOBSVID - OBSERVATION NUMBER, MUST BE IN ASCENDING ORDER
C      IOBYR  - YEAR OF OBSERVATION
C      IOBMON - MONTH OF OBSERVATION
C      IOBDAY - DAY OF OBSERVATION
C      IOBHR  - HOUR OF OBSERVATION
C      IOBLAT - LATITUDE X10, (+N,-S)
C      IOBLON - LONGITUDE X10, (+E, -W)
C      IWNDSP - MAXIMUM SUSTAINED WIND SPEED, (KT)
C      IOBNAM - CYCLONE NAME
C  *   IOBTYP - CYCLONE TYPE - (S - STRAIGHT, R - RECURVER, O - OTHER)
C
C  FOR:  NOIN, SWIN AND SWPA REGIONS (3, 4 AND 5)
C
C      MON     - MONTH OF INITIAL TROPICAL CYCLONE OBSERVATION
C      JYR     - YEAR OF INITIAL TROPICAL CYCLONE OBS, LAST TWO DIGITS
C      IDSTRM - STORM NUMBER, MUST NOT CHANGE FOR A GIVEN CYCLONE
C      IOBSVID - OBSERVATION NUMBER, MUST BE IN ASCENDING ORDER
C      IOBYR  - YEAR OF OBSERVATION
C      IOBMON - MONTH OF OBSERVATION
C      IOBDAY - DAY OF OBSERVATION
C      IOBHR  - HOUR OF OBSERVATION
C      IOBLAT - LATITUDE X10, (+N,-S)
C      IOBLON - LONGITUDE X10, (+E, -W)
C  *   IHD12   - LAST 12-HOUR HEADING, (DEG)
C  *   ISPD12  - LAST 12-HOUR SPEED, (TENTHS OF KT)
C      IWNDSP - MAXIMUM SUSTAINED WIND SPEED, (KT)
C      IOBNAM - CYCLONE NAME
C  *   IOBTYP - CYCLONE TYPE - (S - STRAIGHT, R - RECURVER, O - OTHER)
C
C  *   THESE VALUES ARE NOT USED BY TYAN93, BUT ARE IN THE CLIMATOLOGY
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         JDAYEM      CALCULATE JULIAN DAY
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         IDAY       INIT       JULIAN DAY OF OBSERVATION
C         IDSTRM     INIT       CYCLONE NUMBER
C         IOBNAM     CHAR       CYCLONE NAME/ID
C         IOBDAY     INIT       DAY OF OBSERVATION
C         IOBHR      INIT       HOUR OF OBSERVATION
C         IOBID      INIT       OBSERVATION NUMBER
C         IOBLAT     INIT       LATITUDE  OF OBSERVATION
C         IOBLON     INIT       LONGITUDE OF OBSERVATION
C         IOBMON     INIT       MONTH OF OBSERVATION
C         IOBVN      INIT       OBSERVATION TAG (JYR//IDSTRM//IOBID)
C         IOBVNL     INIT       LAST IOBVN
C         IOBYR      INIT       YEAR OF OBSERVATION
C         IOBTYP     CHAR       TRACK CLASSIFICATION (S, R, OR O)
C         IWNDSP     INIT       WIND SPEED OF OBSERVATION
C         JY         INIT       YEAR OF FIRST OBSERVATION
C         JYR        INIT       YEAR OF OBSERVATION
C         MM         INIT       MONTH OF FIRST OBSERVATION
C         MON        INIT       MONTH OF OBSERVATION
C         STRING     CHAR       SHORT WORKING CHARACTER STRING
C
C  METHOD:  1. READ CLIMATOLOGY FILES ACCORDING TO REGION:
C              A. 1 - NWPAC
C              B. 2 - NEPAC
C              C. 3, 4, AND 5 - IND, SWI AND SWP REGIONS
C           2. SET IOEF, 0 - NO EOF, 1 - EOF FOUND
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C       sampson nrl, june 96    changed read formats (no more bz)
C
C...................END PROLOGUE.......................................
C
      CHARACTER*1 IOBTYP*1, STRING*6, IOBNAM*8
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
C         YLAT   - LATITUDE  OF POSITION, (DEG - + NH, - SH) ???
C         WIND   - MAXIMUM SUSTAINED WIND SPEED, (KT)
C         NR     - NUMBER OF RECORDS READ
C
      COMMON /STORM/ IYR(99),JDAY(99),IHR(99),XLON(99),YLAT(99),
     .               WIND(99),NR
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IEOF   = 0
      IOBVN = 0
C                   COUNT OF OBSERVATIONS READ
      NR = 0
  110 CONTINUE
C                 IOBVNL IS PREVIOUS OBSERVATION NUMBER
      IOBVNL = IOBVN
  120 CONTINUE
C
C                   READ AN OBSERVATION
C
      IF (NREGN .EQ. 1) THEN
C
C                   READ ANALOG DATA FOR NWPAC
C
        READ (NUNIT,9001,END=160) MON,JYR,IDSTRM,IOBID,IOBYR,
     .        IOBMON,IOBDAY,IOBHR,IOBLAT,IOBLON,IWNDSP,IOBNAM,
     .        IOBTYP
C             * * * NOTE, BZ MEANS CONVERT BLANKS TO ZERO
c9001   FORMAT (BZ,8I2,I4,I5,38X,I3,29X,A8,1X,A1)
 9001   format (8i2,i4,i5,38x,i3,29x,a8,1x,a1)
C
      ELSEIF (NREGN .EQ. 2) THEN
C
C                   READ ANALOG DATA FOR NEPAC
C
        READ (NUNIT,9002,END=160) MON,JYR,IDSTRM,IOBID,IOBYR,
     .        IOBMON,IOBDAY,IOBHR,IOBLAT,IOBLON,IWNDSP,IOBNAM,
     .        IOBTYP
c9002   FORMAT (BZ,8I2,I4,I5,I4,1X,A8,1X,A1)
 9002   format (8i2,i4,i5,i4,1x,a8,1x,a1)
C
      ELSE
C
C                   READ ANALOG DATA FOR IND, SWI AND SWP REGIONS
C
        READ (NUNIT,9003,END=160) MON,JYR,IDSTRM,IOBID,IOBYR,
     .        IOBMON,IOBDAY,IOBHR,IOBLAT,IOBLON,IWNDSP,IOBNAM,
     .        IOBTYP
c9003   FORMAT (BZ,8I2,I4,I5,6X,I4,1X,A8,1X,A1)
 9003   format (8i2,i4,i5,6x,i4,1x,a8,1x,a1)
      ENDIF
C
C                   YR, STORM ID, AND OBS NO. ARE COMBINED TO PRODUCE
C                   TOTAL OBSERVATION NAME - IOBVN
      WRITE (STRING,9010) JYR,IDSTRM,IOBID
 9010 FORMAT (3I2)
      READ (STRING,9020) IOBVN
 9020 FORMAT (BZ,I6)
C
      IF (NR.NE.0 .AND. IOBVN.NE.IOBVNL+1) THEN
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
        WRITE(13, 9070) nr,stname,mm,jy
 9070   FORMAT (' REDCLM, MAXIMUM OF ',I2,' OBSERVATIONS REACHED FOR',
     .          ' CYCLONE ',A8,' DURING MONTH ',I2,' YEAR ',I2)
        BACKSPACE (NUNIT)
        GOTO 170
C
      ENDIF
C                   CALCUALTE OBS JULIAN DAY
      IDAY = JDAYEM (IOBYR,IOBMON,IOBDAY)
      IF (IDAY .EQ. 0) THEN
C                   IF OBSV. DATE IN ERROR, IGNORE REC.
        WRITE (13,*)'TYAN93, REDCLM INVALID OBSERVATION DATE: YR ',
     .          IOBYR,' MON ',IOBMON,' DAY ',IOBDAY
        GOTO 120
C
      ENDIF
C                   COUNT THE ALLOWABLE OBSERVATIONS
      NR = NR +1
C                   GET THE PARAMETERS OF ACCEPTED OBSERVATION
      IF (NR .EQ. 1) THEN
        STNAME = IOBNAM
        STYPE  = IOBTYP
        MM     = MON
        JY     = JYR
      ENDIF
      IYR(NR)  = IOBYR
      JDAY(NR) = IDAY
      IHR(NR)  = IOBHR
      YLAT(NR) = 0.1*(FLOAT (IOBLAT))
      XLON(NR) = 0.1*(FLOAT (IOBLON))
C
C                   PUT LONGITUDE IN (0 - 360) EAST RANGE
C
      IF (IOBLON .LT. 0) XLON(NR) = 360.0 +XLON(NR)
      WIND(NR) = FLOAT (IWNDSP)
C                   JUMP TO READ ANOTHER OBSERVATION
      GOTO 110
C
  160 CONTINUE
C                   IF EOF WAS READ FOR THE MONTH'S FILE, SET IEOF = 1.
      IEOF = 1
      WRITE (13,*)'TYAN93, REDCLM - END OF FILE/MONTH REACHED'
  170 CONTINUE
      RETURN
C
      END
      SUBROUTINE CLXEAE (BHED,BDST,BLT1,BLN1,FLT2,FLN2,XTE,ATE,KAL)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  CLXEAE
C
C  DESCRIPTION:  CALCULATE CROSS-TRACK AND ALONG-TRACK ERRORS
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL CLXEAE (BHED,BDST,BLT1,BLN1,FLT2,FLN2,XTE,ATE,KAL)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     BHED         REAL          IN     BASE HEADING OF CYCLONE, DEG
C     BDST         REAL          IN     BASE DISTANCE TRAVELED, NM
C     BLT1         REAL          IN     STARTING LATITUDE, DEG +NH, -SH
C     BLN1         REAL          IN     STARTING LONGITUDE, DEG EAST
C     FLT2         REAL          IN     FORECAST LATITUDE, DEG +NH, -SH
C     FLN2         REAL          IN     FORECAST LONGITUDE, DEG EAST
C     XTE          REAL          OUT    CROSS-TRACK ERROR, NM
C     ATE          REAL          OUT    ALONG-TRACK ERROR, NM
C     KAL          INIT          OUT    CALCULATION FLAG, 0 - NO CAL
C                                                        -1 - CAL MADE
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C          NOTE: THESE ARE NOT THE ATCF CROSS AND ALONG TRACK ERRORS
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         TRKDST      CALCULATE HEADING (DEG) AND DISTANCE (NM) BETWEEN
C                     TWO POSITIONS (LAT/LON)
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         ATOR       REAL       CONVERSION FACTOR, ANGLES TO RADIANS
C         FDST       REAL       DISTANCE FROM B1 TO F2, NM
C         FHED       REAL       HEADING FROM B1 TO F2, DEG
C         HEDOFF     REAL       DIFFERENCE BETWEEN BHED AND FHED, DEG
C
C  METHOD:  WHEN HEADING DIFFERENCE IS <= 45.0 DEGREES.
C           1. CROSS-TRACK ERROR DEFINITION:
C                RIGHT-ANGLE (TO RHUMB LINE FROM B1 TO B2) DISTANCE FROM
C                B2 TO RHUMB LINE (OR ITS EXTENSION) FROM B1 TO F2.
C                (DIRECTION ERROR IN NM)
C           2. ALONG-TRACK ERROR DEFINITION:
C                DIFFERENCE IN NM BETWEEN RHUMB LINE DISTANCES FROM B1 T
C                B2 AND FROM B1 TO F1.  (SPEED ERROR IN NM.)
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  CLXEAE*01  (21 JUL 1993)  --  HAMILTON,H
C           PASS BHED AND BDST RATHER THAN CALCULATE THEM
C
C...................END PROLOGUE.......................................
C
  
  
  
  
      SAVE INIL,ATOR
C
      DATA INIL/0/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (INIL .EQ. 0) THEN
        INIL = -1
        PI   = ACOS (-1.0)
        ATOR = PI/180.0
CCC     RTOA = 1.0/ATOR
      ENDIF
      CALL TRKDST (BLT1,BLN1,FLT2,FLN2,FHED,FDST)
      HEDOFF = FHED -BHED
      IF (ABS (HEDOFF) .GT. 180.0) THEN
        IF (HEDOFF .LT. 0) THEN
          HEDOFF = 360.0 +HEDOFF
        ELSE
          HEDOFF = HEDOFF -360.0
        ENDIF
      ENDIF
      IF (ABS (HEDOFF) .LE. 45.0) THEN
        XTE = BDST*TAN (HEDOFF*ATOR)
        ATE = FDST -BDST
        KAL = -1
      ELSE
C                   SIGNAL NO CALCULATION OF XTE AND ATE
        KAL = 0
      ENDIF
      RETURN
C
      END
      SUBROUTINE TRKDST (SL,SG,EL,EG,HEAD,DIST)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  TRKDST
C
C  DESCRIPTION:  CALCULATE TRACK AND DISTANCE FROM SL,SG TO EL,EG IN THE
C                TROPICS AND MID-LATITUDE USING RHUMB LINE
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL TRKDST (SL,SG,EL,EG,HEAD,DIST)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       SL         REAL          IN     STARTING LATITUDE, DEG +NH, -SH
C       SG         REAL          IN     STARTING LONGITUDE, DEG EAST
C       EL         REAL          IN     ENDING LATITUDE, DEG +NH, -SH
C       EG         REAL          IN     ENDING LONGITUDE, DEG EAST
C     HEAD         REAL          OUT    TRACK HEADING FROM S TO E, DEG
C     DIST         REAL          OUT    DISTANCE FROM S TO E, NM
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          A45R      REAL       RADIANS IN 45 DEGREES
C          RAD       REAL       DEGREES PER RADIAN
C          RADI      REAL       RADIANS PER DEGREE
C          RDI2      REAL       0.5*RADI
C
C  METHOD:  BASED UPON RHUMB LINE CALCULATIONS FROM TEXAS INSTRUMENTS
C           NAVIGATION PACKAGE FOR HAND HELD CALCUATOR
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:   Sampson, NRL   ... set TINY to large no. 9/21/95
C
C
C...................END PROLOGUE.......................................
C
      SAVE RAD,RADI,RDI2,A45R
C
CCC   DATA TINY/0.1E-8/
C                   CHANGE SIZE OF TINY FOR MICRO
CCC   DATA TINY/0.1E-6/
C                   CHANGE SIZE OF TINY FOR SUN and Maxion ..bs 9/21/95
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
cx  check to make sure no divide by 0
	       if (eln1.eq.eln2)eln1=eln1+.0001
               HEAD = RAD*(ATAN ((XG -YG)/(RAD*(ELN1 -ELN2))))
               IF (YL   .LT. XL)  HEAD = HEAD +180.0
               IF (HEAD .LT. 0.0) HEAD = HEAD +360.0
C                   CORRECT INITIAL DISTANCE, BASED ONLY ON LATITIUDE
               DIST = DIST/COS (HEAD*RADI)
            ENDIF
         ENDIF
         DIST  = ABS (DIST)
      ENDIF
      RETURN
C
      END
      SUBROUTINE SORTEM (NCLASS,NTYPE,NCOUNT)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  SORTEM
C
C  DESCRIPTION:  DRIVER FOR SORTING BASED UPON ERROR DISTANCE,
C                LEAST FIRST
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL SORTEM (NCLASS,NTYPE,NCOUNT)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     NCLASS       INIT          IN     TRACK CLASSIFICATION
C                                          1  STRAIGHT
C                                          2  RECURVER
C                                          3  OTHER
C                                          4  TOTAL (S, R AND O)
C      NTYPE       INIT          IN     TYPE OF MATCHING
C                                          1  12-HR PERIOD
C                                          2  24-HR PERIOD
C      NCOUNT      INIT          IN     NUMBER OF VALUES TO SORT
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         SORTER      PERFORM SORT
C         SORTRL      PERFORM LONG SORT FOR STRAIGHT AND RECURVER
C
C  LOCAL VARIABLES:  NONE
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  SORTEM*01  (21 JUL 1993)  --  HAMILTON,H.
C           CALL NEW S/R SORTRL FOR 'S' AND 'R' CLASS CYCLONES
C
C...................END PROLOGUE.......................................
C
C
C                   EXPLANATION OF /CBCLM/ VARIABLES
C
C   CYCYYX  - NAME/IDENTIFICATION OF CLIMO CYCLONE
C       YY  - HOUR, 12 OR 24
C        X  - A - S-TYPE (STRAIGHT)
C             B - R-TYPE (RECURVER)
C             C - O-TYPE (OTHER)
C             D - ALL-TYPES (S, R AND O)
C
      CHARACTER*8 CYC12A,CYC24A,CYC12B,CYC24B,CYC12C,CYC24C,
     .            CYC12D,CYC24D
C
      COMMON/CBCLM/ CYC12A(6),CYC24A(6),CYC12B(6),CYC24B(6),
     .              CYC12C(6),CYC24C(6),CYC12D(6),CYC24D(6)
C
C                   EXPLANATION OF /BCLMX/ VARIABLES
C
C   NYRYYX - YEAR OF INITIAL POSITION
C   NDYYYX - JULIAN DAY OF INITIAL POSITION
C   MYRYYX - YEAR OF POSITION
C   DYJYYX - JULIAN DAY OF POSITION
C   MHRYYX - HOUR OF POSITION
C   CLTYYX - LATITUDE OF POSITION (+ NH, - SH)
C   CLNYYX - LONGITUDE OF POSITION (0 - 360 EAST)
C   WNDYYX - ANALOG FORECAST 12-HR WIND SPEED CHANGE, KT
C   EYYX   - WEIGHTED ERROR DIFFERENCE BETWEEN TRANSPOSED CLIMATOLOGY
C            AND YY HOUR POSITION LATER
C   ALTYXX - ANALOG TAU 12 FORECAST OF LATITUDE, DEG
C   ALNYYX - ANALOG TAU 12 FORECAST OF LONGITUDE, DEG
C   MRYYX  - NUMBER OF VALUES
C      YY  - HOUR, 12 OR 24
C       X  - A - S-TYPE (STRAIGHT)
C            B - R-TYPE (RECURVER)
C            C - O-TYPE (OTHER)
C            D - ALL-TYPES (S, R AND O)
C
      COMMON/BCLMA/ NYR12A(6),NDY12A(6),MYR12A(6),MDY12A(6),MHR12A(6),
     .              CLT12A(6),CLN12A(6),WND12A(6),E12A(6),
     .              ALT12A(6),ALN12A(6),MR12A,
     .              NYR24A(6),NDY24A(6),MYR24A(6),MDY24A(6),MHR24A(6),
     .              CLT24A(6),CLN24A(6),WND24A(6),E24A(6),
     .              ALT24A(6),ALN24A(6),MR24A
      COMMON/BCLMB/ NYR12B(6),NDY12B(6),MYR12B(6),MDY12B(6),MHR12B(6),
     .              CLT12B(6),CLN12B(6),WND12B(6),E12B(6),
     .              ALT12B(6),ALN12B(6),MR12B,
     .              NYR24B(6),NDY24B(6),MYR24B(6),MDY24B(6),MHR24B(6),
     .              CLT24B(6),CLN24B(6),WND24B(6),E24B(6),
     .              ALT24B(6),ALN24B(6),MR24B
      COMMON/BCLMC/ NYR12C(6),NDY12C(6),MYR12C(6),MDY12C(6),MHR12C(6),
     .              CLT12C(6),CLN12C(6),E12C(6),MR12C,
     .              NYR24C(6),NDY24C(6),MYR24C(6),MDY24C(6),MHR24C(6),
     .              CLT24C(6),CLN24C(6),E24C(6),MR24C
      COMMON/BCLMD/ NYR12D(6),NDY12D(6),MYR12D(6),MDY12D(6),MHR12D(6),
     .              CLT12D(6),CLN12D(6),E12D(6),MR12D,
     .              NYR24D(6),NDY24D(6),MYR24D(6),MDY24D(6),MHR24D(6),
     .              CLT24D(6),CLN24D(6),E24D(6),MR24D
C
C
C  <<CHANGE NOTICE>>  $TYANB201  (21 JUL 1993)  --  HAMILTON,H.
C           ADD WNDYYX, ALTYYX, ALNYYX, WHERE YY IS 12
C           OR 24 AND X IS A OR B, TO ALLOW FORECASTING BY TYAN93
C
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NCLASS .EQ. 1) THEN
        IF (NTYPE .EQ. 1) THEN
          CALL SORTRL (NCOUNT,NYR12A,NDY12A,MYR12A,MDY12A,MHR12A,CLT12A,
     .                 CLN12A,WND12A,ALT12A,ALN12A,CYC12A,E12A)
        ELSE
          CALL SORTRL (NCOUNT,NYR24A,NDY24A,MYR24A,MDY24A,MHR24A,CLT24A,
     .                 CLN24A,WND24A,ALT24A,ALN24A,CYC24A,E24A)
        ENDIF
      ELSEIF (NCLASS .EQ. 2) THEN
        IF (NTYPE .EQ. 1) THEN
          CALL SORTRL (NCOUNT,NYR12B,NDY12B,MYR12B,MDY12B,MHR12B,CLT12B,
     .                 CLN12B,WND12B,ALT12B,ALN12B,CYC12B,E12B)
        ELSE
          CALL SORTRL (NCOUNT,NYR24B,NDY24B,MYR24B,MDY24B,MHR24B,CLT24B,
     .                 CLN24B,WND24B,ALT24B,ALN24B,CYC24B,E24B)
        ENDIF
      ELSEIF (NCLASS .EQ. 3) THEN
        IF (NTYPE .EQ. 1) THEN
          CALL SORTER (NCOUNT,NYR12C,NDY12C,MYR12C,MDY12C,MHR12C,
     .                 CLT12C,CLN12C,CYC12C,E12C)
        ELSE
          CALL SORTER (NCOUNT,NYR24C,NDY24C,MYR24C,MDY24C,MHR24C,
     .                 CLT24C,CLN24C,CYC24C,E24C)
        ENDIF
      ELSEIF (NCLASS .EQ. 4) THEN
        IF (NTYPE .EQ. 1) THEN
          CALL SORTER (NCOUNT,NYR12D,NDY12D,MYR12D,MDY12D,MHR12D,
     .                 CLT12D,CLN12D,CYC12D,E12D)
        ELSE
          CALL SORTER (NCOUNT,NYR24D,NDY24D,MYR24D,MDY24D,MHR24D,
     .                 CLT24D,CLN24D,CYC24D,E24D)
        ENDIF
      ENDIF
      RETURN
C
      END
      SUBROUTINE SORTER (NCOUNT,NYR,NDAY,MYR,MDAY,MHR,CLT,CLN,CNAM,ERR)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  SORTER
C
C  DESCRIPTION:  SORT BASED UPON ERROR DISTANCE, LEAST FIRST, KEEP
C                ASSOCIATED ARRAY VALUES IN SAME SEQUENCE AS EEROR
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL SORTER (NCOUNT,NYR,NDAY,MYR,MDAY,MHR,CLT,CLN,CNAM,ERR)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     NCOUNT       INIT          IN     NUMBER OF VALUES FOR SORTING
C        NYR       INIT        IN/OUT   ASSOCIATED ARRAY
C       NDAY       INIT        IN/OUT   ASSOCIATED ARRAY
C        MYR       INIT        IN/OUT   ASSOCIATED ARRAY
C       MDAY       INIT        IN/OUT   ASSOCIATED ARRAY
C        MHR       INIT        IN/OUT   ASSOCIATED ARRAY
C        CLT       REAL        IN/OUT   ASSOCIATED ARRAY
C        CLN       REAL        IN/OUT   ASSOCIATED ARRAY
C       CNAM       CHAR        IN/OUT   ASSOCIATED ARRAY
C        ERR       REAL        IN/OUT   ERROR, NM
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:  N/A
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
      CHARACTER*8 CNAM(6), CTV
C
      DIMENSION NYR(6),NDAY(6),MYR(6),MDAY(6),MHR(6),CLT(6),CLN(6),
     .          ERR(6)
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      DO 120 N=1, NCOUNT-1
        ER = ERR(N)
        DO 110 J=N+1, NCOUNT
          IF (ER .GT. ERR(J)) THEN
            ITV     = NYR(N)
            NYR(N)  = NYR(J)
            NYR(J)  = ITV
            ITV     = NDAY(N)
            NDAY(N) = NDAY(J)
            NDAY(J) = ITV
            ITV     = MYR(N)
            MYR(N)  = MYR(J)
            MYR(J)  = ITV
            ITV     = MDAY(N)
            MDAY(N) = MDAY(J)
            MDAY(J) = ITV
            ITV     = MHR(N)
            MHR(N)  = MHR(J)
            MHR(J)  = ITV
            RTV     = CLT(N)
            CLT(N)  = CLT(J)
            CLT(J)  = RTV
            RTV     = CLN(N)
            CLN(N)  = CLN(J)
            CLN(J)  = RTV
            CTV     = CNAM(N)
            CNAM(N) = CNAM(J)
            CNAM(J) = CTV
            ERR(N)  = ERR(J)
            ERR(J)  = ER
            ER      = ERR(N)
          ENDIF
  110   CONTINUE
  120 CONTINUE
      RETURN
C
      END
      SUBROUTINE HEDING (AIDNM)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  HEDING
C
C  DESCRIPTION:  WRITE HEADING OF TYAN93 OUTPUT FOR PROGRAM CVCQFC
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL HEDING (AIDNM)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C      AIDNM       CHAR          IN     OBJECTIVE AID NAME
C
C  COMMON BLOCKS:
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:  NONE
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
  
      CHARACTER*4 AIDNM
C
C
C                   EXPLANATION OF /CNSEW/ VARIABLES
C
C   CNAME - NAME OF TROPICAL CYCLONE
C   CDTG  - DTG OF INITIAL POSITION (YYMMDDHH)
C   CNS   - NORTH/SOUTH HEMISPHERE INDICATOR, N OR S
C   CEW   - INITIAL EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW12  - PAST 12 HR EAST/WEST HEMISPHERE INDICATOR, E OR W
C   EW24  - PAST 24 HR EAST/WEST HEMISPHERE INDOCATOR, E OR W
C
      CHARACTER CNAME*7, CDTG*8, CNS*1, CEW*1, EW12*1, EW24*1
C
      COMMON/CNSEW/ CNAME,CDTG,CNS,CEW,EW12,EW24
C
C                   EXPLANATION OF /POSIT/ VARIABLES
C
C   NREGN - NUMBER OF BASIN FROM FIX POSITION
C   FLT   - FIX LATITUDE, DEG (+ NH, - SH)
C   FLN   - FIX LONGITUDE, DEG (EAST)
C   PLT12 - PAST 12 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN12 - PAST 12 HR LONGITUDE, DEG (EAST)
C   PLT24 - PAST 24 HR LATITUDE,  DEG (+ NH, - SH)
C   PLN24 - PAST 24 HR LONGITUDE, DEG (EAST)
C   HD12S - HEADING  FROM -12 TO FIX LOCATION (STRAIGHT), DEG
C   DT12S - DISTANCE FROM -12 TO FIX LOCATION (STRAIGHT), NM
C   HD24S - HEADING  FROM -24 TO FIX LOCATION (STRAIGHT), DEG
C   DT24S - DISTANCE FROM -24 TO FIX LOCATION (STRAIGHT), NM
C
      COMMON/POSIT/ NREGN,FLT,FLN,FWD,PLT12,PLN12,PLT24,PLN24
     .             ,HD12S,DT12S,HD24S,DT24S
C
C
C                   EXPLANATION OF /POSITR/ VARIABLES FOR RECURVERS
C
C   NREGNR - NUMBER OF BASIN FROM FIX POSITION
C   FLTR   - INITIAL LATITUDE, DEG
C   FLNR   - INITIAL LONGITUDE, DEG
C   PLT12R - PAST 12 HR LATITUDE,  DEG
C   PLN12R - PAST 12 HR LONGITUDE, DEG
C   PLT24R - PAST 24 HR LATITUDE,  DEG
C   PLN24R - PAST 24 HR LONGITUDE, DEG
C   HD12R  - HEADING  FROM -12 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -12 TO FIX LOCATION (RECURVER), NM
C   HD24R  - HEADING  FROM -24 TO FIX LOCATION (RECURVER), DEG
C   DT12R  - DISTANCE FROM -24 TO FIX LOCATION (RECURVER), NM
C
      COMMON/POSITR/ NREGNR,FLTR,FLNR,FWDR,PLT12R,PLN12R,PLT24R,PLN24R,
     .               HD12R,DT12R,HD24R,DT24R
C
C  <<CHANGE NOTICE>>  $TYANB101  (21 JUL 1993)  --  HAMILTON,H.
C           ADD HEADING AND DISTANCE TO DCREASE RUNNING TIME.
C           ADD /POSITR/ TO ALLOW FORECASTING BY TYAN93.
C  <<CHANGE NOTICE>>  $TYANB102  (06 JUL 1995)  --  SAMPSON,B.
C           OUTPUT TO LU 55 NOW GOES TO SCREEN.
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NREGN .EQ. 1) THEN
        WRITE (*,681) AIDNM,CNAME,CDTG
  681   FORMAT(11X,'NORTHWEST PACIFIC ',A4,' MATCHING FOR  ',
     .         A7,' AT ',A8)
      ELSEIF (NREGN .EQ. 2) THEN
        WRITE (*,682) AIDNM,CNAME,CDTG
  682   FORMAT(11X,'NORTHEAST PACIFIC ',A4,' MATCHING FOR  ',
     .         A7,' AT ',A8)
      ELSEIF (NREGN .EQ. 3) THEN
        WRITE (*,683) AIDNM,CNAME,CDTG
  683   FORMAT(11X,'     NORTH INDIAN ',A4,' MATCHING FOR  ',
     .         A7,' AT ',A8)
      ELSEIF (NREGN .EQ. 4) THEN
        WRITE (*,684) AIDNM,CNAME,CDTG
  684   FORMAT(11X,' SOUTHWEST INDIAN ',A4,' MATCHING FOR  ',
     .         A7,' AT ',A8)
      ELSEIF (NREGN .EQ. 5) THEN
        WRITE (*,685) AIDNM,CNAME,CDTG
  685   FORMAT(11X,'    SOUTH PACIFIC ',A4,' MATCHING FOR  ',
     .         A7,' AT ',A8)
      ENDIF
      RETURN
C
      END
      SUBROUTINE JLTOMD (IY,JDAY,MO,KD)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  JLTOMD
C
C  DESCRIPTION:  CALCULATE MONTH AND DAY, GIVEN YEAR AND JULIAN DAY
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL JLTOMD (IY,JDAY,MO,KD)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       IY         INIT          IN     YEAR (LAST TWO DIGITS)
C     JDAY         INIT          IN     JULIAN DAY IN IY YEAR
C       MO         INIT          OUT    MONTH IN IY YEAR
C       KD         INIT          OUT    DAY IN MO
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  BAD YEAR AND JULIAN DAY, RETURN ZERO MO AND KD
C
C  ADDITIONAL COMMENTS:  ***** WARNING - WARNING *******
C    THE YEAR 1900 IS NOT A LEAP YEAR, BUT 20000 IS A LEAP YEAR.
C    THE FIRST YEAR OF THE DATA BASE IS 1900, USING TWO DIGITS FOR THE
C    YEAR MEANS STARTING IN 2000 THE FIRST YEAR OF THE DATA BASE MUST BE
C    REMOVED EACH YEAR.
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          IADD      INIT       FLAG TO USE NON-LEAP YEAR OR LEAP YEAR
C                               PORTION OF TABLES MTH  AND MTHD
C           MTH      INIT       TABLE OF RUNNING DAYS IN A YEAR AND IN A
C                               LEAP YEAR
C          MTHD      INIT       TABLE OF DAYS IN A MONTH IN A YEAR AND
C                               IN A LEAP YEAR
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
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
         IF (IY.EQ.0 .OR. MOD(IY,4).NE.0) THEN
C                   NOTE, BY DEFINITION 1900 IS NOT A LEAP YEAR, BUT
C                   2000 IS A LEAP YEAR, SO CHANGE ABOVE CODE IN 1999.
            IADD = 0
         ELSE
C                   LEAP YEAR, USE LEAP YEAR TABLES
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
      FUNCTION JDAYEM (IY,IM,ID)
C
C..........................START PROLOGUE..............................
C
C  MODULE NAME:  JDAYEM
C
C  DESCRIPTION:  CALCULATE JULIAN DAY, GIVEN YEAR, MONTH AND DAY
C
C  COPYRIGHT:                  (C) 1993 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  NONE
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  CDC 180/NOS/BE
C
C  LIBRARIES OF RESIDENCE:  OPSPL1/MT1731
C
C  USAGE:  CALL JDAYEM (IY,IM,ID)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       IY         INIT          IN     YEAR (LAST TWO DIGITS)
C       IM         INIT          IN     MONTH
C       ID         INIT          IN     DAY
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  NONE
C
C  ERROR CONDITIONS:  BAD YEAR, MONTH OR DAY, RETURN ZERO
C
C  ADDITIONAL COMMENTS:  *****  WARNING - WARNING  *****
C    THE YEAR 1900 IS NOT A LEAP YEAR, BUT 2000 IS A LEAP YEAR.
C    THE FIRST YEAR OF THE DATA BASE IS 1900, USING TWO DIGITS FOR THE
C    YEAR MEANS STARTING IN 2000 THE FIRST YEAR OF THE DATA BASE MUST BE
C    REMOVED EACH YEAR.
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          IADD      INIT       FLAG FOR NON-LEAP YEAR OR LEAP YEAR
C         MAXDYS     INIT       MAXIMUM NUMBER OF DAYS IN MONTH
C           MTH      INIT       TABLE OF RUNNING DAYS IN A YEAR
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  NONE
C
C  COMPILER DEPENDENCIES:  FORTRAN 77
C
C  COMPILE OPTIONS:        STANDARD FNOC OPERATIONAL OPTIONS
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
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
         MAXDAY = MTH(IM+1) -MTH(IM)
         IF (IM.EQ.2) MAXDAY = MAXDAY +IADD
         IF (ID.GT.0 .AND. ID.LE.MAXDAY) THEN
C                   DAY INDEX O.K.
C                   MAKE IADD 0 FOR JAN AND FEB
            IF (IM .LT. 3) IADD = 0
            JDAYEM = MTH(IM) +ID +IADD
         ELSE
C                   MAKE JDAYEM ZERO TO SIGNAL ERROR
            JDAYEM = 0
         ENDIF
      ELSE
C                   MAKE JDAYEM ZERO TO SIGNAL ERROR
         JDAYEM = 0
      ENDIF
      RETURN
C
      END
