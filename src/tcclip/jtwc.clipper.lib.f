C***********************************************************************
      SUBROUTINE WPCLPR(IDATIM,ALAT00,ALON00,ALAT12,ALON12,ALAT24,
     $     ALON24,WIND)

C
C THIS IS CLIPER PROGRAM FOR WESTERN PACIFIC BASIN.  THE FOLLOWING SHOULD
C BE NOTED:
C (1) PROGRAM WAS DEVELOPED USING STORM TRACKS OVER YEARS 1945-1988.
C (2) ALL MONTHS WERE INCLUDED IN DEVELOPMENTAL DATA SET.
C (3) STORMS INITIALLY LOCATED EAST OF 180 DEGS WERE EXCLUDED.
C (4) STORMS INITIALLY LOCATED NORTH OF 50N WERE EXCLUDED.
C (4) STORMS WHICH INITIALLY CLASSIFIED AS DEPRESSIONS OR CLASSIFIED AS
C     DEPRESSIONS AT VERIFICATION TIME WERE EXCLUDED.
C (5) RESULTANT SAMPLE SIZE FROM ABOVE CRITERIA.....
C                  18891 AT 12H, 16851 AT 24H, 14979 AT 36H,
C                  13224 AT 48H, 11598 AT 60H, 10094 AT 72H.
C (6) INDIVIDUAL CASES IN DEVELOPMENTAL DATA SET WERE AT 6 HRLY INTERVALS
C (7) PROGRAM PREPARED BY CHARLES J. NEUMANN, SAIC, OCT NOV DEC, 1989.
C (8) THIS VERSION OF WPCLPR REPLACES EARLIER VERSION REPORTED ON BY
C     XU AND NEUMANN (1985) IN NOAA TECHNICAL MEMORANDUM NWS NHC 28.
C     EARLIER XU & NEUMANN VERSION HAD CERTAIN SEASONAL AND GEOGRAPHICAL
C     RESTRICTIONS.  CURRENT VERSION HAS NO RESTRICTIONS OTHER THAN AS
C     NOTED ABOVE.  MINIMUM VALUE OF P1 IS SET TO 7.5.
C
C INCOMING ARGUMENTS ARE AS FOLLOWS:
C   IDATIM (INTEGER*4) IS IN FORM YY/MO/DA/HR AS 89052306
C   ALAT00 AND ALON00 ARE INITIAL STORM POSITION (REAL*4)
C   ALAT12 AND ALON12 ARE POSITION 12H EARLIER   (REAL*4)
C   ALAT24 AND ALON24 ARE POSITION 24H EARLIER   (REAL*4)
C     NOTE: IT IS ASSUMED THAT LATITUDES ARE NORTH AND THAT LONGITUDES
C           ARE EAST.  INITIAL LONGITUDE OF 160W MUST BE ENTERED AS
C           200 DEGREES. HOWEVER, PROGRAM HAS NOT BEEN
C           DESIGNED FOR INITIAL POSITIONS IN WESTERN HEMISPHERE.
C   WIND IS MAXIMUM WIND NEAR STORM CENTER IN KNOTS (REAL*4)
C
C RETURN ARGUMENT IS STORM DISPLACEMENTS IN NAUTICAL MILES AS GIVEN BY
C (CNMIS(J),J=1,12),  LAT/LON POSITIONS AS GIVEN BY (CLALO(J),J=1,12)
C AND VALUES OF 8 BASIC PREDICTORS AS GIVEN BY (P1TOP8(K),K=1,8)
C
C ARRANGEMENT OF CNMIS AND CLALO ARRAY IS AS FOLLOWS:
C      CNMIS(01) IS MERIDIONAL 12H DISPLACEMENT (NMI)
C      CNMIS(02) IS ZONAL 12H DISPLACEMENT (NMI)
C      CNMIS(03) IS MERIDIONAL 24H DISPLACEMENT (NMI)
C      CNMIS(04) IS ZONAL 24H DISPLACEMENT (NMI)
C      CNMIS(05) IS MERIDIONAL 36H DISPLACEMENT (NMI)
C      CNMIS(06) IS ZONAL 36H DISPLACEMENT (NMI)
C      CNMIS(07) IS MERIDIONAL 48H DISPLACEMENT (NMI)
C      CNMIS(08) IS ZONAL 48H DISPLACEMENT (NMI)
C      CNMIS(09) IS MERIDIONAL 60H DISPLACEMENT (NMI)
C      CNMIS(10) IS ZONAL 60H DISPLACEMENT (NMI)
C      CNMIS(11) IS MERIDIONAL 72H DISPLACEMENT (NMI)
C      CNMIS(12) IS ZONAL 72H DISPLACEMENT (NMI)
C NOTE: NEGATIVE DISPLACEMENTS ARE TOWARDS WEST OR SOUTH.
C       CLALO ARRAY CORRESPONDS TO CNMIS ARRAY EXCEPT THAT DISPLACEMENTS
C       HAVE BEEN CONVERTED TO LATITUDES NORTH AND LONGITUDES EAST
C         
      common/wpclpfcst/ CFCST(12)
      COMMON/BLOCK1/RCM(90,6),RCZ(95,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(90,6),NPZ(95,6)
      COMMON/BLOCK2/NPM,NPZ
      REAL*4 P(166),CNMIS(12),P1TOP8(8)
C
C ALL REGRESSION COEFFICIENTS AND PREDICTOR NUMBERS ARE CONTAINED IN
C BLOCK DATA BLKDT1.  THERE ARE 90 PREDICTORS AND PREDICTOR
C NUMBERS FOR MERIDIONAL MOTION AND 95 PREDICTORS AND PREDICTOR NUMBERS
C FOR ZONAL MOTION. ((RCM(I,J),J=1,6),I=1,90) AND ((NPM(I,J),J=1,6),I=1,90)
C ARE COEFFICIENTS AND PREDICTOR NUMBERS FOR MERIDIONAL MOTION WHILE
C ((RCZ(I,J),J=1,6),I=1,95) AND ((NPZ(I,J),J=1,6),I=1,95) ARE COEFFICIENTS
C AND PREDICTOR NUMBERS FOR ZONAL MOTION. SUBSCRIPT J REFERS TO TIME WHERE
C J=1=12H.........J=6=72H.
C 6 MERIDIONAL INTERCEPT VALUES ARE GIVEN BY (CNSTM(J),J=1,6) WHILE THE
C 6 ZONAL INTERCEPT VALUES ARE GIVEN BY (CNSTZ(J),J=1,6).
C
C P1 THRU P8 ARE 8 PRIMARY PREDICTORS WHERE...
C      P1 IS INITIAL LATITUDE  (DEGS NORTH)
C         MINIMUM ALLOWABLE VALUE OF P1 IS 7.5       
C      P2 IS INITIAL LONGITUDE (DEGS EAST)
C      P3 IS FUNCTION OF JULIAN DAY NUMBER WITH FEB 11 0000UTC
C          SET TO DAY NUMBER 0 AND AUG 12 SET TO MID-YEAR
C      P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)
C      P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
C      P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
C      P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
C      P8 IS MAXIMUM WIND (KNOTS)
C
C FUNCTIONS AND SUBPROGRAMS NEEDED BY WPCLPR ARE AS FOLLOWS:
C    DATA NEEDED BY PROGRAM ARE CONTAINED IN BLOCK DATA BLKDT1 AND BLKDT2
C    WPCLPR CALLS SUBROUTINES STHGPR, LL2XYH, PSETUP AND NMI2LL
C           AND UTILIZES FUNCTIONS F1, F2
C    NMI2LL CALLS SUBROUTINE XY2LLH AND UTILIZES FUNCTION F1
C
C SET UP 8 BASIC PREDICTORS......

      print*,'idatim ',idatim
      print*,'wind   ',wind
      print*,'wpclpr ',alat00,alon00,alat12,alon12
      print*,'wpclpr ',alat24,alon24,wind


      P1=ALAT00
      P2=ALON00
C JULIAN DAY NUMBER. GET CONVERSION FACTOR (.008613) SUCH THAT SIN
C OF DAY NUMBER 0 (FEB 11) HAS VALUE NEAR ZERO AND MID-YEAR (AUG 12)
C HAS VALUE NEAR 1.00.  NOTE THAT DAY NUMBER IS OFFSET BY 41 DAYS SUCH
C THAT FEB 11 IS DAY NUMBER 0 AND AUG 12 IS MID-YEAR.
      CONVRT=2.*ACOS(0.)/364.75
      P3=F2(IDATIM)-41.
      IF(P3.LT.0.)P3=P3+365.
      P3=SIN(P3*CONVRT)
      P8=WIND
C USE AL TAYLOR ROUTINES (SEE NOTE BELOW) FOR CONVERTING LATITUDE/LONGITUDE
C TO DISPLACEMENTS.
C THESE SAME ROUTINES ARE LATER USED FOR CONVERTING DISPLACEMENTS BACK TO
C LATITUDES AND LONGITUDES........
C NOTE....AL TAYLOR ROUTINES REFER TO SUBROUTINES STHGPR,LL2XYH,XY2LLH
C (PREDICTORS NUMBER P4 THRU P7)
      CALL STHGPR(P1,F1(P2),360.,1.,0.,0.)
      CALL LL2XYH(ALAT12,F1(ALON12),P5,P4)
      CALL LL2XYH(ALAT24,F1(ALON24),P7,P6)
C ABOVE ALGEBRAIC SIGNS NEED TO BE REVERSED.....
      P4=-P4
      P5=-P5
      P6=-P6
      P7=-P7
C BASIC PREDICTOR SETUP IS COMPLETE. PUT 8 VALUES INTO ARRAY P1TOP8 FOR
C POSSIBLE USE IN CALLING PROGRAM.  ALSO, DETERMINE THAT P1 IS AT LEAST 7.5
      IF(ALAT00.GT.7.5)THEN
      P1FIX=ALAT00
      ELSE
      P1FIX=7.5
      ENDIF
      P1TOP8(1)=P1FIX
      P1TOP8(2)=P2
      P1TOP8(3)=P3
      P1TOP8(4)=P4
      P1TOP8(5)=P5
      P1TOP8(6)=P6
      P1TOP8(7)=P7
      P1TOP8(8)=P8
C
C PREPARE FORECAST, FIRST, OBTAIN ALL POSSIBLE 3RD ORDER PRODUCTS AND
C CROSS-PRODUCTS OF THE 8 BASIC PREDICTORS AND RETURN THESE IN ARRAY
C (P(L),L=1,166).  THERE ARE 164 POSSIBLE COMBINATIONS AND THESE ARE
C GIVEN BY SUBSCRIBTS 3 THROUGH 166. P(1) AND P(2) ARE NOT USED AND HAVE
C BEEN RETURNED AS DUMMY VARIABLES. NOT ALL OF THE 164 POSSIBLE PREDICTORS
C ARE USED IN PROGRAM.
      CALL PSETUP(P1FIX,P2,P3,P4,P5,P6,P7,P8,P)
C OBTAIN FORECAST MERIDIONAL DISPLACEMENTS 12 THRU 72H
      DO 60 J=1,6
C INITIALIZE COMPUTATION WITH INTERCEPT VALUE
      CNMIS(2*J-1)=CNSTM(J)
      DO 50 I=1,90
      K=NPM(I,J)
      CNMIS(2*J-1)=CNMIS(2*J-1)+RCM(I,J)*P(K)
   50 CONTINUE
   60 CONTINUE
C
C OBTAIN FORECAST ZONAL DISPLACEMENTS 12 THRU 72H
C
      DO 80 J=1,6
C INITIALIZE COMPUTATION WITH INTERCEPT VALUE
      CNMIS(2*J)=CNSTZ(J)
      DO 70 I=1,95
      K=NPZ(I,J)
      CNMIS(2*J)=CNMIS(2*J)+RCZ(I,J)*P(K)
   70 CONTINUE
   80 CONTINUE
C CONVERT DISPLACEMENTS TO LATITUDE AND LONGITUDE
      CALL NMI2LL(ALAT00,ALON00,CNMIS,CFCST)
      RETURN
      END
C***********************************************************************
      FUNCTION F1(ALON)
C CONVERT FROM E LONGITUDE TO THOSE ACCEPTABLE IN AL TAYLOR ROUTINES
      IF(ALON.GT.180.)F1=360.-ALON
      IF(ALON.LE.180.)F1=-ALON
      RETURN
      END
C***********************************************************************
      FUNCTION F2(IDATIM)
C OBTAIN JULIAN DAY NUMBER
C 0000UTC ON 1 JAN IS SET TO DAY NUMBER 0 AND 1800UTC ON 31 DEC IS SET TO
C DAY NUMBER 364.75.  LEAP YEARS ARE IGNORED.
      CHARACTER*8 ALFA
      WRITE(ALFA,'(I8)')IDATIM
      READ(ALFA,'(4I2)')KYR,MO,KDA,KHR
      MON=MO
      IF(MON.EQ.13)MON=1
      DANBR=3055*(MON+2)/100-(MON+10)/13*2-91+KDA
      F2=DANBR-1.+FLOAT(KHR/6)*0.25
      RETURN
      END
C***********************************************************************
      BLOCK DATA BLKDT2
C
C   ALBION D. TAYLOR, MARCH 19, 1982
C  THE HURRICANE GRID IS BASED ON AN OBLIQUE EQUIDISTANT CYLINDRICAL
C  MAP PROJECTION ORIENTED ALONG THE TRACK OF THE HURRICANE.
C
C    THE X (OR I) COORDINATE XI OF A POINT REPRESENTS THE DISTANCE
C  FROM THAT POINT TO THE GREAT CIRCLE THROUGH THE HURRICANE, IN
C  THE DIRECTION OF MOTION OF THE HURRICANE MOTION.  POSITIVE VALUES
C  REPRESENT DISTANCES TO THE RIGHT OF THE HURRICANE MOTION, NEGATIVE
C  VALUES REPRESENT DISTANCES TO THE LEFT.
C    THE Y (OR J) COORDINATE OF THE POINT REPRESENTS THE DISTANCE
C  ALONG THE GREAT CIRCLE THROUGH THE HURRICANE TO THE PROJECTION
C  OF THE POINT ONTO THAT CIRCLE.  POSITIVE VALUES REPRESENT
C  DISTANCE IN THE DIRECTION OF HURRICANE MOTION, NEGATIVE VALUES
C  REPRESENT DISTANCE IN THE OPPOSITE DIRECTION.
C
C     SCALE DISTANCES ARE STRICTLY UNIFORM IN THE I-DIRECTION ALWAYS.
C  THE SAME SCALE HOLDS IN THE J-DIRECTION ONLY ALONG THE HURRICANE TRACK
C  ELSEWHERE, DISTANCES IN THE J-DIRECTION ARE EXAGERATED BY A FACTOR
C  INVERSELY PROPORTIONAL TO THE COSINE OF THE ANGULAR DISTANCE FROM
C  THE TRACK.  THE SCALE IS CORRECT TO 1 PERCENT WITHIN A DISTANCE OF
C  480 NM OF THE STORM TRACK, 5 PERCENT WITHIN 1090 NM, AND
C  10 PERCENT WITHIN 1550 NM.
C
C  BIAS VALUES ARE ADDED TO THE XI AND YJ COORDINATES FOR CONVENIENCE
C  IN INDEXING.
C
C  A PARTICULAR GRID IS SPECIFIED BY THE USER BY MEANS OF A CALL
C  TO SUBROUTINE STHGPR (SET HURRICANE GRID PARAMETERS)
C  WITH ARGUMENTS (XLATH,XLONH,BEAR,GRIDSZ,XIO,YJO)
C   WHERE
C     XLATH,XLONH = LATITUDE, LONGITUDE OF THE HURRICANE
C     BEAR        = BEARING OF THE HURRICANE MOTION
C     GRIDSZ      = SIZE OF GRID ELEMENTS IN NAUTICAL MILES
C     XIO, YJO    = OFFSETS IN I AND J COORDINATES (OR I AND J
C                     COORDINATES OF HURRICANE)
C    AND WHERE
C     LATITUDES, LONGITUDES AND BEARINGS ARE GIVEN IN DEGREES,
C     POSITIVE VALUES ARE NORTH AND WEST, NEGATIVE SOUTH AND EAST,
C     BEARINGS ARE GIVEN CLOCKWISE FROM NORTH.
C
C  THE CALL TO STHGPR SHOULD BE MADE ONCE ONLY, AND BEFORE REFERENCE
C  TO ANY CALL TO LL2XYH OR XY2LLH.  IN DEFAULT, THE SYSTEM
C  WILL ASSUME A STORM AT LAT,LONG=0.,0., BEARING DUE NORTH,
C  WITH A GRIDSIZE OF 120 NAUTICAL MILES AND OFFSETS OF 0.,0. .
C
C  TO CONVERT FROM GRID COORDINATES XI AND YJ, USE A CALL TO
C    CALL XY2LLH(XI,YJ,XLAT,XLONG)

C  THE SUBROUTINE WILL RETURN THE LATITUDE AND LONGITUDE CORRESPONDING
C  TO THE GIVEN VALUES OF XI AND YJ.
C
C  TO CONVERT FROM LATITUDE AND LONGITUDE TO GRID COORDINATES, USE
C    CALL LL2XYH(XLAT,XLONG,XI,YJ)
C  THE SUBROUTINE WILL RETURN THE I-COORDINATE XI AND Y-COORDINATE
C  YJ CORRESPONDING TO THE GIVEN VALUES OF LATITUDE XLAT AND
C  LONGITUDE XLONG.
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DATA A /0.,-1.,0., 1.,0.,0.,  0.,0.,1./
      DATA RADPDG/1.745 3293 E-2/,RRTHNM /3 440.17/
      DATA DGRIDH/120./
      DATA HGRIDX,HGRIDY/0.,0./
      END
C***********************************************************************
      SUBROUTINE PSETUP(P1,P2,P3,P4,P5,P6,P7,P8,P)
      DIMENSION P(166)
C P1 THRU P8 ARE ARE 8 PRIMARY PREDICTORS WHERE...
C      P1 IS INITIAL LATITUDE  (DEGS)
C         MINIMUM ALLOWABLE VALUE OF P1 IS 7.5 
C      P2 IS INITIAL LONGITUDE (DEGS)
C      P3 IS JULIAN DAY NUMBER FUNCTION (O TO 1.00)
C      P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)            
C      P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
C      P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
C      P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
C      P8 IS MAXIMUM WIND (KNOTS)
C
C P(001 AND 002) ARE DUMMY VARIABLES AND ARE NOT FURTHER USED.
      DUMMY=9999.
      P(001)=DUMMY
      P(002)=DUMMY
C P(003)THRU P(166) ARE ALL POSSIBLE PREDICTORS AS OBTAINED FROM CUBIC
C POLYNOMIAL EXPANSION OF ORIGINAL 8 BASIC PREDICTORS P1 THRU P8.   
C
C LIST THE PREDICTORS................
C NOTE: DESIGNATOR IN COLUMN 73 INDICATES WHETHER PREDICTOR WAS USED  
C IN EQUATIONS FOR ZONAL MOTION (Z); IN EQUATIONS FOR MERIDIONAL MOTION (M)
C OR IN BOTH SETS (B).  A BLANK IN COLUMN 73 INDICATES THAT PREDICTOR WAS
C NOT USED BUT HAS BEEN RETAINED IN PSETUP FOR REFERENCE PURPOSES AND TO
C FACILITATE INDEXING.
      P(003)=P8                                                         
      P(004)=P8*P8                                                      
      P(005)=P8*P8*P8                                                   
      P(006)=P7                                                         
      P(007)=P7*P8                                                      
      P(008)=P7*P8*P8                                                   
      P(009)=P7*P7                                                      
      P(010)=P7*P7*P8                                                   
      P(011)=P7*P7*P7                                                   
      P(012)=P6                                                         
      P(013)=P6*P8                                                      
      P(014)=P6*P8*P8                                                   
      P(015)=P6*P7                                                      
      P(016)=P6*P7*P8                                                   
      P(017)=P6*P7*P7                                                   
      P(018)=P6*P6                                                      
      P(019)=P6*P6*P8                                                   
      P(020)=P6*P6*P7                                                   
      P(021)=P6*P6*P6                                                   
      P(022)=P5                                                         
      P(023)=P5*P8                                                      
      P(024)=P5*P8*P8                                                   
      P(025)=P5*P7                                                      
      P(026)=P5*P7*P8                                                   
      P(027)=P5*P7*P7                                                   
      P(028)=P5*P6                                                      
      P(029)=P5*P6*P8                                                   
      P(030)=P5*P6*P7                                                   
      P(031)=P5*P6*P6                                                   
      P(032)=P5*P5                                                      
      P(033)=P5*P5*P8                                                   
      P(034)=P5*P5*P7                                                   
      P(035)=P5*P5*P6                                                   
      P(036)=P5*P5*P5                                                   
      P(037)=P4                                                         
      P(038)=P4*P8                                                      
      P(039)=P4*P8*P8                                                   
      P(040)=P4*P7                                                      
      P(041)=P4*P7*P8                                                   
      P(042)=P4*P7*P7                                                   
      P(043)=P4*P6                                                      
      P(044)=P4*P6*P8                                                   
      P(045)=P4*P6*P7                                                   
      P(046)=P4*P6*P6                                                   
      P(047)=P4*P5                                                      
      P(048)=P4*P5*P8                                                   
      P(049)=P4*P5*P7                                                   
      P(050)=P4*P5*P6                                                   
      P(051)=P4*P5*P5                                                   
      P(052)=P4*P4                                                      
      P(053)=P4*P4*P8                                                   
      P(054)=P4*P4*P7                                                   
      P(055)=P4*P4*P6                                                   
      P(056)=P4*P4*P5                                                   
      P(057)=P4*P4*P4                                                   
      P(058)=P3                                                         
      P(059)=P3*P8                                                      
      P(060)=P3*P8*P8                                                   
      P(061)=P3*P7                                                      
      P(062)=P3*P7*P8                                                   
      P(063)=P3*P7*P7                                                   
      P(064)=P3*P6                                                      
      P(065)=P3*P6*P8                                                   
      P(066)=P3*P6*P7                                                   
      P(067)=P3*P6*P6                                                   
      P(068)=P3*P5                                                      
      P(069)=P3*P5*P8                                                   
      P(070)=P3*P5*P7                                                   
      P(071)=P3*P5*P6                                                   
      P(072)=P3*P5*P5                                                   
      P(073)=P3*P4                                                      
      P(074)=P3*P4*P8                                                   
      P(075)=P3*P4*P7                                                   
      P(076)=P3*P4*P6                                                   
      P(077)=P3*P4*P5                                                   
      P(078)=P3*P4*P4                                                   
      P(079)=P3*P3                                                      
      P(080)=P3*P3*P8                                                   
      P(081)=P3*P3*P7                                                   
      P(082)=P3*P3*P6                                                   
      P(083)=P3*P3*P5                                                   
      P(084)=P3*P3*P4                                                   
      P(085)=P3*P3*P3                                                   
      P(086)=P2                                                         
      P(087)=P2*P8                                                      
      P(088)=P2*P8*P8                                                   
      P(089)=P2*P7                                                      
      P(090)=P2*P7*P8                                                   
      P(091)=P2*P7*P7                                                   
      P(092)=P2*P6                                                      
      P(093)=P2*P6*P8                                                   
      P(094)=P2*P6*P7                                                   
      P(095)=P2*P6*P6                                                   
      P(096)=P2*P5                                                      
      P(097)=P2*P5*P8                                                   
      P(098)=P2*P5*P7                                                   
      P(099)=P2*P5*P6                                                   
      P(100)=P2*P5*P5                                                   
      P(101)=P2*P4                                                      
      P(102)=P2*P4*P8                                                   
      P(103)=P2*P4*P7                                                   
      P(104)=P2*P4*P6                                                   
      P(105)=P2*P4*P5                                                   
      P(106)=P2*P4*P4                                                   
      P(107)=P2*P3                                                      
      P(108)=P2*P3*P8                                                   
      P(109)=P2*P3*P7                                                   
      P(110)=P2*P3*P6                                                   
      P(111)=P2*P3*P5                                                   
      P(112)=P2*P3*P4                                                   
      P(113)=P2*P3*P3                                                   
      P(114)=P2*P2                                                      
      P(115)=P2*P2*P8                                                   
      P(116)=P2*P2*P7                                                   
      P(117)=P2*P2*P6                                                   
      P(118)=P2*P2*P5                                                   
      P(119)=P2*P2*P4                                                   
      P(120)=P2*P2*P3                                                   
      P(121)=P2*P2*P2                                                   
      P(122)=P1                                                         
      P(123)=P1*P8                                                      
      P(124)=P1*P8*P8                                                   
      P(125)=P1*P7                                                      
      P(126)=P1*P7*P8                                                   
      P(127)=P1*P7*P7                                                   
      P(128)=P1*P6                                                      
      P(129)=P1*P6*P8                                                   
      P(130)=P1*P6*P7                                                   
      P(131)=P1*P6*P6                                                   
      P(132)=P1*P5                                                      
      P(133)=P1*P5*P8                                                   
      P(134)=P1*P5*P7                                                   
      P(135)=P1*P5*P6                                                   
      P(136)=P1*P5*P5                                                   
      P(137)=P1*P4                                                      
      P(138)=P1*P4*P8                                                   
      P(139)=P1*P4*P7                                                   
      P(140)=P1*P4*P6                                                   
      P(141)=P1*P4*P5                                                   
      P(142)=P1*P4*P4                                                   
      P(143)=P1*P3                                                      
      P(144)=P1*P3*P8                                                   
      P(145)=P1*P3*P7                                                   
      P(146)=P1*P3*P6                                                   
      P(147)=P1*P3*P5                                                   
      P(148)=P1*P3*P4                                                   
      P(149)=P1*P3*P3                                                   
      P(150)=P1*P2                                                      
      P(151)=P1*P2*P8                                                   
      P(152)=P1*P2*P7                                                   
      P(153)=P1*P2*P6                                                   
      P(154)=P1*P2*P5                                                   
      P(155)=P1*P2*P4                                                   
      P(156)=P1*P2*P3                                                   
      P(157)=P1*P2*P2                                                   
      P(158)=P1*P1                                                      
      P(159)=P1*P1*P8                                                   
      P(160)=P1*P1*P7                                                   
      P(161)=P1*P1*P6                                                   
      P(162)=P1*P1*P5                                                   
      P(163)=P1*P1*P4                                                   
      P(164)=P1*P1*P3                                                   
      P(165)=P1*P1*P2                                                   
      P(166)=P1*P1*P1                                                   
      RETURN
      END
C***********************************************************************
      SUBROUTINE NMI2LL(ALAT0,ALON0,CNMIS,CFCST)
C INCOMING ARGUMENTS:
C     ALAT0, ALON0...INITIAL STORM POSTION
C     CNMIS...........FORECAST MERIDIONAL & ZONAL DISPLACEMENTS IN NMI.
C RETURNED ARGUMENT:
C     CFCST..........FORECASTS IN TERMS OF LAT/LON (SEE NOTE, BELOW)
C
      REAL*4 CNMIS(12),CFCST(12)
      CALL STHGPR(ALAT0,F1(ALON0),360.,1.,0.,0.)
      DO 10 I=1,6
      CALL XY2LLH(CNMIS(2*I),CNMIS(2*I-1),CFCST(2*I-1),CFCST(2*I))
C NOTE: ABOVE SUBROUTINE RETURNS LONGITUDES WEST OF 180 AS NEGATIVE AND
C EAST OF 180 AS POSITIVE.  CONVERT ALL LONGITUDES TO WHERE EAST IS POSITIVE
C ZERO TO 180 AND WEST IS POSITIVE 180 TO 360 DEGS. 
      IF(CFCST(2*I).GE.0.AND.CFCST(2*I).LT.180.)CFCST(2*I)=360.-
     $CFCST(2*I)
      IF(CFCST(2*I).LT.0.)CFCST(2*I)=-CFCST(2*I)
   10 CONTINUE
      RETURN
      END
C**********************************************************************
      FUNCTION NEWCYC(NOWCYC,N)
C GIVEN CYCLE TIME NOWCYC, GET NEW CYCLE TIME (NEWCYC) GIVEN BY
C NOWCYC + N HOURS.  LIMIT 0F N IS + OR - 744 HOURS.  ALLOWANCES
C ARE MADE FOR LEAP YEARS.
C (C.J.NEUMANN, SAIC, OCTOBER, 1989)
      CHARACTER*8 ALFA
      INTEGER NHEM(15),NOLEAP(15)
      DATA NOLEAP /000,744,1488,2160,2904,3624,4368,5088,5832,6576,7296,
     $8040,8760,9504,10248/
C ABOVE DATA STATEMENT GIVES NUMBER OF HOURS FOR NON-LEAP YEAR MONTHS
C MONTHS 0000UTC ON 1 DEC THRU 0000UTC ON 1 FEB OF SECOND YEAR.
C
C OBTAIN YEAR (KYR),MONTH (M0),DAY (KDA) AND HOUR (JTM) IN INTEGER FORMAT
      WRITE(ALFA,'(I8)')NOWCYC
      READ(ALFA,'(4I2)')KYR,MO,KDA,JTM
      DO 10 I=1,15
   10 NHEM(I)=NOLEAP(I)
C IS THIS A LEAP YEAR? (YEAR 2000 IS A LEAP YEAR)
      IF(MOD(KYR,4).EQ.0)THEN
      DO 20 I=4,15
   20 NHEM(I)=NHEM(I)+24
      ENDIF
C HOW MANY HRS FROM BEGINNING OF TIME WINDOW AT 0000UTC, 1 DEC (NHROLD)?
      NHROLD=NHEM(MO+1)+(KDA-1)*24+JTM
C HOW MANY HRS NEEDED FROM BEGINNING OF WINDOW (NHRNEW)?
      NHRNEW=NHROLD+N
C
      DO 30 MO=2,15
C MO = 2 = PREVIOUS YEAR; M0 = 15 = NEXT YEAR; DO WE NEED TO ADD OR
C SUBTRACT A YEAR??
      KYRNEW=KYR-(2/MO)+MO/15
C CHANGE OF CENTURY?
      IF(KYRNEW.EQ.100)KYRNEW=0
      IF(KYRNEW.EQ.-1)KYRNEW=99
C
      IF(NHRNEW.LT.NHEM(MO))GOTO 40
   30 CONTINUE
   40 NDIF=NHRNEW-NHEM(MO-1)
      LDA=(NDIF+24)/24
      LTM=NDIF+24-(LDA*24)
      INDEX=MOD(MO-3,12)+(2/MO)*12+1
      NEWCYC=KYRNEW*1000000+INDEX*10000+LDA*100+LTM
      RETURN
      END
C***********************************************************************
      BLOCK DATA BLKDT1
C
C ENTER ALL CONSTANTS NEEDED BY WPCLPR PROGRAM......
C
      INTEGER*2 N12M(90),N24M(90),N36M(90),N48M(90),N60M(90),N72M(90)
      INTEGER*2 N12Z(95),N24Z(95),N36Z(95),N48Z(95),N60Z(95),N72Z(95)
      REAL*4 R12M(90),R24M(90),R36M(90),R48M(90),R60M(90),R72M(90)
      REAL*4 R12Z(95),R24Z(95),R36Z(95),R48Z(95),R60Z(95),R72Z(95)
      COMMON/BLOCK1/RCM(90,6),RCZ(95,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(90,6),NPZ(95,6)
      COMMON/BLOCK2/NPM,NPZ
C NOTE: THESE CONSTANTS ARE FOR 10 PREDICTORS FROM EACH SET USING DAY
C NUMBER SIN FUNCTION SHIFTED BY 41 DAYS
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
C
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
C***********************************************************************
      SUBROUTINE STHGPR(XLATH,XLONH,BEAR,GRIDSZ,XI0,YJ0)
C   ALBION D. TAYLOR, MARCH 19, 1982
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      CLAT=COS(RADPDG*XLATH)
      SLAT=SIN(RADPDG*XLATH)
      SLON=SIN(RADPDG*XLONH)
      CLON=COS(RADPDG*XLONH)
      SBEAR=SIN(RADPDG*BEAR)
      CBEAR=COS(RADPDG*BEAR)
      A(1,1)=   CLAT*SLON
      A(1,2)=   CLAT*CLON
      A(1,3)=   SLAT
      A(2,1)= - CLON*CBEAR + SLAT*SLON*SBEAR
      A(2,2)=   SLON*CBEAR + SLAT*CLON*SBEAR
      A(2,3)=              - CLAT*     SBEAR
      A(3,1)= - CLON*SBEAR - SLAT*SLON*CBEAR
      A(3,2)=   SLON*SBEAR - SLAT*CLON*CBEAR
      A(3,3)=                CLAT*     CBEAR
      DGRIDH=GRIDSZ
      HGRIDX=XI0
      HGRIDY=YJ0
      RETURN
      END
C***********************************************************************
      SUBROUTINE LL2XYH(XLAT,XLONG,XI,YJ)
C   ALBION D. TAYLOR, MARCH 19, 1982
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DIMENSION ZETA(3),ETA(3)
      CLAT=COS(RADPDG*XLAT)
      SLAT=SIN(RADPDG*XLAT)
      SLON=SIN(RADPDG*XLONG)
      CLON=COS(RADPDG*XLONG)
      ZETA(1)=CLAT*SLON
      ZETA(2)=CLAT*CLON
      ZETA(3)=SLAT
      DO 20 I=1,3
      ETA(I)=0.
      DO 20 J=1,3
      ETA(I)=ETA(I) + A(I,J)*ZETA(J)
   20 CONTINUE
      R=SQRT(ETA(1)*ETA(1) + ETA(3)*ETA(3))
      XI=HGRIDX+RRTHNM*ATAN2(ETA(2),R)/DGRIDH
      IF(R.LE.0.) GO TO 40
      YJ=HGRIDY+RRTHNM*ATAN2(ETA(3),ETA(1))/DGRIDH
      RETURN
   40 YJ=0.
      RETURN
      END
C***********************************************************************
      SUBROUTINE XY2LLH(XI,YJ,XLAT,XLONG)
C   ALBION D. TAYLOR, MARCH 19, 1982
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DIMENSION ZETA(3),ETA(3)
      CXI=COS(DGRIDH*(XI-HGRIDX)/RRTHNM)
      SXI=SIN(DGRIDH*(XI-HGRIDX)/RRTHNM)
      SYJ=SIN(DGRIDH*(YJ-HGRIDY)/RRTHNM)
      CYJ=COS(DGRIDH*(YJ-HGRIDY)/RRTHNM)
      ETA(1)=CXI*CYJ
      ETA(2)=SXI
      ETA(3)=CXI*SYJ
      DO 20 I=1,3
      ZETA(I)=0.
      DO 20 J=1,3
      ZETA(I)=ZETA(I) + A(J,I)*ETA(J)
   20 CONTINUE
      R=SQRT(ZETA(1)*ZETA(1) + ZETA(2)*ZETA(2))
      XLAT=ATAN2(ZETA(3),R)/RADPDG
      IF(R.LE.0.) GO TO 40
      XLONG=ATAN2(ZETA(1),ZETA(2))/RADPDG
      RETURN
   40 XLONG=0.
      RETURN
      END
C***********************************************************************
      SUBROUTINE DB2LL(XLATO,XLONO,DIST,BEAR,XLATT,XLONT)
C
C  THIS DATASET IS NOW NAMED' NWS.WD80.CJN.SOURCE1(PGM10)
C
C      ALBION D. TAYLOR MARCH 18, 1981
      DATA RRTHNM/3 440.17/,RADPDG/1.745 3293 E-2/
C   RRTHNM=RADIUS OF EARTH IN NAUT. MILES, RADPDG==OF RADIANS
C   PER DEGREE
C*---------------------------------------------------------------------*
C* GIVEN AN ORIGIN AT LATITUDE, LONGITUDE=XLATO,XLONO, WILL LOCATE     *
C* A TARGET POINT AT A DISTANCE DIST IN NAUTICAL MILES, AT BEARING     *
C* BEAR (DEGREES CLOCKWISE FROM NORTH). RETURNS LATITUDE XLATT         *
C* AND LONGITUDE XLONT OF TARGET POINT.                                *
C*                                                                     *
C* ALL LATITUDES ARE IN DEGREES, NORTH POSITIVE AND SOUTH NEGATIVE.    *
C* ALL LONGITUDES ARE IN DEGREES, WEST POSITIVE AND EAST NEGATIVE.     *
C*                                                                     *
C* NOTE-- WHEN ORIGIN IS AT NORTH OR SOUTH POLE, BEARING IS NO LONGER  *
C* MEASURED FROM NORTH.  INSTEAD, BEARING IS MEASURED CLOCKWISE        *
C* FROM THE LONGITUDE OPPOSITE THAT SPECIFIED IN XLONO.                *
C* EXAMPLE-- IF XLATO=90., XLONO=80., THE OPPOSITE LONGITUDE IS -100.  *
C* (100 EAST), AND A TARGET AT BEARING 30. WILL LIE ON THE -70.        *
C* (70 EAST) MERIDIAN                                                  *
C*---------------------------------------------------------------------*
      CDIST=COS(DIST/RRTHNM)
      SDIST=SIN(DIST/RRTHNM)
      CLATO=COS(RADPDG*XLATO)
      SLATO=SIN(RADPDG*XLATO)
      CLONO=COS(RADPDG*XLONO)
      SLONO=SIN(RADPDG*XLONO)
      CBEAR=COS(RADPDG*BEAR)
      SBEAR=SIN(RADPDG*BEAR)
      Z=CDIST*SLATO + CLATO*SDIST*CBEAR
      Y=CLATO*CLONO*CDIST + SDIST*(SLONO*SBEAR - SLATO*CLONO*CBEAR)
      X=CLATO*SLONO*CDIST - SDIST*(CLONO*SBEAR + SLATO*SLONO*CBEAR)
      R=SQRT(X*X+Y*Y)
      XLATT=ATAN2(Z,R)/RADPDG
      IF (R.LE.0.) GO TO 20
      XLONT=ATAN2(X,Y)/RADPDG
      RETURN
   20 XLONT=0.
      RETURN
      END
C***********************************************************************
      SUBROUTINE LL2DB(XLATO,XLONO,XLATT,XLONT,DIST,BEAR)
C      ALBION D. TAYLOR MARCH 18, 1981
      DATA RRTHNM/3 440.17/,RADPDG/1.745 3293 E-2/
C   RRTHNM=RADIUS OF EARTH IN NAUT. MILES, RADPDG==OF RADIANS
C   PER DEGREE
C*---------------------------------------------------------------------*
C* GIVEN AN ORIGIN AT LATITUDE, LONGITUDE=XLATO,XLONO, WILL LOCATE     *
C* A TARGET POINT AT LATITUDE, LONGITUDE = XLATT, XLONT.  RETURNS      *
C* DISTANCE DIST IN NAUTICAL MILES, AND BEARING BEAR (DEGREES CLOCKWISE*
C* FROM NORTH).                                                        *
C*                                                                     *
C* ALL LATITUDES ARE IN DEGREES, NORTH POSITIVE AND SOUTH NEGATIVE.    *
C* ALL LONGITUDES ARE IN DEGREES, WEST POSITIVE AND EAST NEGATIVE.     *
C*                                                                     *
C* NOTE-- WHEN ORIGIN IS AT NORTH OR SOUTH POLE, BEARING IS NO LONGER  *
C* MEASURED FROM NORTH.  INSTEAD, BEARING IS MEASURED CLOCKWISE        *
C* FROM THE LONGITUDE OPPOSITE THAT SPECIFIED IN XLONO.                *
C* EXAMPLE-- IF XLATO=90., XLONO=80., THE OPPOSITE LONGITUDE IS -100.  *
C* (100 EAST), AND A TARGET AT BEARING 30. WILL LIE ON THE -70.        *
C* (70 EAST) MERIDIAN                                                  *
C*---------------------------------------------------------------------*
      CLATO=COS(RADPDG*XLATO)
      SLATO=SIN(RADPDG*XLATO)
      CLATT=COS(RADPDG*XLATT)
      SLATT=SIN(RADPDG*XLATT)
      CDLON=COS(RADPDG*(XLONT-XLONO))
      SDLON=SIN(RADPDG*(XLONT-XLONO))
      Z=SLATT*SLATO + CLATT*CLATO*CDLON
      Y= - CLATT*SDLON
      X=CLATO*SLATT - SLATO*CLATT*CDLON
      R=SQRT(X*X+Y*Y)
      DIST=RRTHNM*ATAN2(R,Z)
      IF (R.LE.0.) GO TO 20
      BEAR=ATAN2(-Y,-X)/RADPDG + 180.
      RETURN
   20 BEAR=0.
      RETURN
      END
C***********************************************************************
      SUBROUTINE SEICLP(IDATIM,ALAT00,ALON00,ALAT12,ALON12,ALAT24,
     $ALON24,WIND)
C
C THIS IS A CLIPER PROGRAM FOR THE AUSTRALIA/SE INDIAN OCEAN BASIN (AREA 
C     OF SOUTHERN HEMISPHERE BETWEEN 142E AND 100E.)
C     FOLLOWING SHOULD BE NOTED:
C (1) PROGRAM WAS DEVELOPED USING SOUTHERN HEMISPHERE STORM TRACKS OVER 
C     YEARS 1970/1971 TO 1999/2000.
C (2) ALL MONTHS EXCEPT 1 JULY THROUGH 15 SEPTEMBER WERE INCLUDED IN 
C     DEVELOPMENTAL DATA SET.  THESE DATES ARE CONVERTED TO 30 JUNE
C     OR 16 SEPTEMBER, WHICHEVER IS CLOSER IN TIME.
C     
C (3) PORTIONS OF STORMS HAVING VERIFYING POSITIONS EAST OF 142 DEGREES
C     OR WEST OF 100 DEGREES WERE EXCLUDED FROM DEVELOPMENTAL DATA SET.
C     NUMBER OF TC'S INCLUDED = 279
C (4) STORMS POSITIONS SOUTH OF 50S WERE EXCLUDED FROM DEVELOPMENTAL
C     DATA SET.
C (5) STORMS WHICH INITIALLY CLASSIFIED AS DEPRESSIONS OR CLASSIFIED AS
C     DEPRESSIONS AT VERIFICATION TIME WERE EXCLUDED.
C (6) SAMPLE SIZE,  2582 AT 12H,  2229 AT 24H,  1918 AT 36H,
C                   1644 AT 48H,  1381 AT 60H,  1157 AT 72H.
C (7) INDIVIDUAL CASES IN DEVELOPMENTAL DATA SET WERE AT 6 HRLY INTERVALS
C (8) PROGRAM PREPARED BY CHARLES J. NEUMANN, SAIC, OCTOBER, 2000.
C
C INCOMING ARGUMENTS ARE AS FOLLOWS:
C   IDATIM (INTEGER*4) IS IN FORM YY/MO/DA/HR AS 01040106 FOR
C   DATE APRIL 1, 2001, 0600UTC.
C   ALAT00 AND ALON00 ARE INITIAL STORM POSITION (REAL*4)
C   ALAT12 AND ALON12 ARE POSITION 12H EARLIER   (REAL*4)
C   ALAT24 AND ALON24 ARE POSITION 24H EARLIER   (REAL*4)
C     NOTE: IT IS ASSUMED THAT LATITUDES AND LONGITUDES WILL BE ENTERED
C           AS POSITIVE VALUES.
C
C   WIND IS MAXIMUM WIND (1-MINUTE AVERAGE) NEAR STORM CENTER IN KNOTS
C   (REAL*4).
C
C RETURNED ARGUMENTS ARE:
C   STORM DISPLACEMENTS AS GIVEN BY (DISP(J),J=1,12);
C   POSITIONS AS GIVEN BY (CDISP(J),J=1,12);
C   VALUES OF 8 BASIC PREDICTORS AS GIVEN BY (P1TOP8(K),K=1,8)
C
C ARRANGEMENT OF DISP AND CDISP ARRAY IS AS FOLLOWS:
C      DISP(01) IS MERIDIONAL 12H DISPLACEMENT (NMI)
C      DISP(02) IS ZONAL 12H DISPLACEMENT (NMI)
C      DISP(03) IS MERIDIONAL 24H DISPLACEMENT (NMI)
C      DISP(04) IS ZONAL 24H DISPLACEMENT (NMI)
C      DISP(05) IS MERIDIONAL 36H DISPLACEMENT (NMI)
C      DISP(06) IS ZONAL 36H DISPLACEMENT (NMI)
C      DISP(07) IS MERIDIONAL 48H DISPLACEMENT (NMI)
C      DISP(08) IS ZONAL 48H DISPLACEMENT (NMI)
C      DISP(09) IS MERIDIONAL 60H DISPLACEMENT (NMI)
C      DISP(10) IS ZONAL 60H DISPLACEMENT (NMI)
C      DISP(11) IS MERIDIONAL 72H DISPLACEMENT (NMI)
C      DISP(12) IS ZONAL 72H DISPLACEMENT (NMI)
C NOTE: SEE NOTE 1 AND NOTE 2 FOR SIGN CONVENTION OF ABOVE DISP ARRAY.
C       CDISP ARRAY CORRESPONDS TO DISP ARRAY EXCEPT THAT DISPLACEMENTS
C       HAVE BEEN CONVERTED TO LATITUDES SOUTH AND LONGITUDES EAST
C
      common/seiclpfcst/ cfcst(12)
      COMMON/BLOCKSE1/RCM(16,6),RCZ(14,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(16,6),NPZ(14,6)
      COMMON/BLOCKSE2/NPM,NPZ
      REAL*4 P(166),DISP(12),P1TOP8(8)
C INITIALLY, 5 PREDICTORS OUT OF 164 POSSIBLE PREDICTORS (LISTED IN
C SUBROUTINE SETUP) WERE SELECTED FOR EACH TIME PERIOD AND FOR BOTH ZONAL
C AND MERIDIONAL MOTION.  A FINAL SET OF PREDICTORS FOR EACH COMPONENT OF
C MOTION INCLUDED ALL PREDICTORS SELECTED AT LEAST ONCE, 12 THRU 72H.
C THIS TURNED OUT TO BE 16 PREDICTORS FOR MERIDIONAL MOTION AND 14 FOR
C ZONAL MOTION.
C
C ALL REGRESSION COEFFICIENTS AND PREDICTOR NUMBERS ARE 
C ENTERED IN BLOCK DATA BLKSE1.  THERE ARE 16 PREDICTORS AND PREDICTOR
C NUMBERS FOR MERIDIONAL MOTION AND 14 PREDICTORS AND PREDICTOR NUMBERS
C FOR ZONAL MOTION. ((RCM(I,J),J=1,6,I=1,16) & ((NPM(I,J),J=1,6),I=1,16)
C ARE COEFFICEINTS AND PREDICTOR NUMBERS FOR MERIDIONAL MOTION WHILE
C ((RCZ(I,J),J=1,6,I=1,14) AND ((NPZ(I,J),J=1,6),I=1,14) ARE COEFFICIENTS
C AND PREDICTOR NUMBERS FOR ZONAL MOTION. SUBSCRIPT J REFERS TO TIME WHERE
C J=1=12H.........J=6=72H.
C 6 MERIDIONAL INTERCEPT VALUES ARE GIVEN BY (CNSTM(J),J=1,6) WHILE THE
C 6 ZONAL INTERCEPT VALUES ARE GIVEN BY (CNSTZ(J),J=1,6).
C P1 THRU P8 ARE 8 PRIMARY PREDICTORS WHERE...
C      P1 IS INITIAL LATITUDE  (DEGS SOUTH)
C      P2 IS INITIAL LONGITUDE (DEGS EAST)
C      P3 IS JULIAN DAY NUMBER FUNCTION DEFINED AS NUMBER OF DAYS (ABSOLUTE)
C      EITHER SIDE OF FEBRUARY 25 (APPROXIMATE MID-SEASON FOR THIS AREA).
C      P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)
C      P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
C      P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
C      P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
C      P8 IS MAXIMUM WIND (KNOTS) ASSUMING A 1-MINUTE WIND MEASURING
C         SYSTEM.
C FUNCTIONS AND SUBPROGRAMS NEEDED BY SEICLP ARE AS FOLLOWS:
C    DATA NEEDED BY PROGRAM ARE CONTAINED IN BLOCK DATA BLKSE1 AND BLKSE2
C    SEICLP CALLS SUBROUTINES STHGPR, LL2XYH, SETUP AND YX2LL
C           AND UTILIZES FUNCTIONS F1, F2
C    YX2LL CALLS SUBROUTINE XY2LLH AND UTILIZES FUNCTION F1
C SET UP 8 BASIC PREDICTORS......
      P1=ALAT00
      P2=ALON00
C JULIAN DAY NUMBER
      DANBR=F2(IDATIM)
      IDN=DANBR+.5
C AVERAGE TC DAY NUMBER FOR THIS BASIN IS NEAR 56 (25 MARCH)
      MEANDN=56
C
C CHANGE DAY NUMBERS FOR OFF-SEASON STORMS
      IF(IDN.GT.181.AND.IDN.LE.220)IDN=181
      IF(IDN.GT.220.AND.IDN.LT.259)IDN=259
C
      IF(IDN.GE.1.AND.IDN.LE.181)IDADIF=IABS(MEANDN-IDN)
      IF(IDN.GE.259)IDADIF=366-IDN+MEANDN
      P3=IDADIF
      P8=WIND
C USE AL TAYLOR ROUTINE FOR CONVERTING LATITUDE/LONGITUDE TO DISPLACEMENTS.
C THIS SAME ROUTINE IS LATER USED FOR CONVERTING DISPLACEMENTS BACK TO
C LATITUDES AND LONGITUDES........
C (PREDICTORS NUMBER P4 THRU P7)
      CALL STHGPR(P1,F1(P2),360.,1.,0.,0.)
      CALL LL2XYH(ALAT12,F1(ALON12),P5,P4)
      CALL LL2XYH(ALAT24,F1(ALON24),P7,P6)
C CHANGE SIGN
      P4=-P4
      P5=-P5
      P6=-P6
      P7=-P7
C BASIC PREDICTOR SETUP IS COMPLETE. PUT 8 VALUES INTO ARRAY P1TOP8 FOR
C POSSIBLE USE IN CALLING PROGRAM
      P1TOP8(1)=P1
      P1TOP8(2)=P2
      P1TOP8(3)=P3
      P1TOP8(4)=P4
      P1TOP8(5)=P5
      P1TOP8(6)=P6
      P1TOP8(7)=P7
      P1TOP8(8)=P8
C
C PREPARE FORECAST, FIRST, OBTAIN ALL POSSIBLE 3RD ORDER PRODUCTS AND
C CROSS-PRODUCTS OF THE 8 BASIC PREDICTORS AND RETURN THESE IN ARRAY
C (P(L),L=1,166).  THERE ARE 164 POSSIBLE COMBINATIONS AND THESE ARE
C GIVEN BY SUBSCRIBTS 3 THROUGH 166. P(1) AND P(2) ARE NOT USED AND HAVE
C BEEN RETURNED AS DUMMY VARIABLES. NOT ALL OF THE 164 POSSIBLE PREDICTORS
C ARE USED IN PROGRAM.
      CALL SETUP(P1,P2,P3,P4,P5,P6,P7,P8,P)
C OBTAIN FORECAST MERIDIONAL DISPLACEMENTS 12 THRU 72H
      DO 60 J=1,6
C INITIALIZE COMPUTATION WITH INTERCEPT VALUE
      DISP(2*J-1)=CNSTM(J)
      DO 50 I=1,16
      K=NPM(I,J)
      DISP(2*J-1)=DISP(2*J-1)+RCM(I,J)*P(K)
   50 CONTINUE
   60 CONTINUE
C
C OBTAIN FORECAST ZONAL DISPLACEMENTS 12 THRU 72H
C
      DO 80 J=1,6
C INITIALIZE COMPUTATION WITH INTERCEPT VALUE
      DISP(2*J)=CNSTZ(J)
      DO 70 I=1,14
      K=NPZ(I,J)
      DISP(2*J)=DISP(2*J)+RCZ(I,J)*P(K)
   70 CONTINUE
   80 CONTINUE
C CONVERT DISPLACEMENTS TO LATITUDE AND LONGITUDE
      CALL YX2LL(ALAT00,ALON00,DISP,CFCST)
C NOTE 1
C IN ABOVE ARRAY ABOVE ZONAL DISPLACEMENTS ARE NEGATIVE TO THE WEST AND
C MERIDIONAL DISPLACEMENTS ARE NEGATINE TO THE NORTH.  REVERSE SIGN
C OF LATITUDINAL DISPLACEMENTS SUCH THAT TOWARDS SOUTH IS NEGATIVE.
      DO 90 J=1,11,2
   90 DISP(J)=-DISP(J)
C NOTE 2
C NOW, DISPLACEMENTS ARE CORRECT IN MATHEMATICAL SENSE.
      RETURN
      END
C***********************************************************************
cx    FUNCTION F1(ALON)
cxCONVERT FROM E LONGITUDE TO THOSE ACCEPTABLE IN AL TAYLOR ROUTINES
cx    IF(ALON.GT.180.)F1=360.-ALON
cx    IF(ALON.LE.180.)F1=-ALON
cx    RETURN
cx    END
cx**********************************************************************
cx    FUNCTION F2(IDATIM)
cxOBTAIN JULIAN DAY NUMBER
cx0000UTC ON 1 JAN IS SET TO DAY NUMBER 0. AND 1800UTC ON 31 DEC IS SET 
cxTO DAY NUMBER 364.75.  LEAP YEARS ARE IGNORED.
cx    CHARACTER*8 ALFA
cx    WRITE(ALFA,'(I8)')IDATIM
cx    READ(ALFA,'(4I2)')KYR,MO,KDA,KHR
cx    MON=MO
cx    IF(MON.EQ.13)MON=1
cx    DANBR=3055*(MON+2)/100-(MON+10)/13*2-91+KDA
cx    F2=DANBR-1.+FLOAT(KHR/6)*0.25
cx    RETURN
cx    END
C***********************************************************************
      BLOCK DATA BLKSE2
C
C   ALBION D. TAYLOR, MARCH 19, 1982
C  THE HURRICANE GRID IS BASED ON AN OBLIQUE EQUIDISTANT CYLINDRICAL
C  MAP PROJECTION ORIENTED ALONG THE TRACK OF THE HURRICANE.
C
C    THE X (OR I) COORDINATE XI OF A POINT REPRESENTS THE DISTANCE
C  FROM THAT POINT TO THE GREAT CIRCLE THROUGH THE HURRICANE, IN
C  THE DIRECTION OF MOTION OF THE HURRICANE MOTION.  POSITIVE VALUES
C  REPRESENT DISTANCES TO THE RIGHT OF THE HURRICANE MOTION, NEGATIVE
C  VALUES REPRESENT DISTANCES TO THE LEFT.
C    THE Y (OR J) COORDINATE OF THE POINT REPRESENTS THE DISTANCE
C  ALONG THE GREAT CIRCLE THROUGH THE HURRICANE TO THE PROJECTION
C  OF THE POINT ONTO THAT CIRCLE.  POSITIVE VALUES REPRESENT
C  DISTANCE IN THE DIRECTION OF HURRICANE MOTION, NEGATIVE VALUES
C  REPRESENT DISTANCE IN THE OPPOSITE DIRECTION.
C
C     SCALE DISTANCES ARE STRICTLY UNIFORM IN THE I-DIRECTION ALWAYS.
C  THE SAME SCALE HOLDS IN THE J-DIRECTION ONLY ALONG THE HURRICANE TRACK
C  ELSEWHERE, DISTANCES IN THE J-DIRECTION ARE EXAGERATED BY A FACTOR
C  INVERSELY PROPORTIONAL TO THE COSINE OF THE ANGULAR DISTANCE FROM
C  THE TRACK.  THE SCALE IS CORRECT TO 1 PERCENT WITHIN A DISTANCE OF
C  480 NM OF THE STORM TRACK, 5 PERCENT WITHIN 1090 NM, AND
C  10 PERCENT WITHIN 1550 NM.
C
C  BIAS VALUES ARE ADDED TO THE XI AND YJ COORDINATES FOR CONVENIENCE
C  IN INDEXING.
C
C  A PARTICULAR GRID IS SPECIFIED BY THE USER BY MEANS OF A CALL
C  TO SUBROUTINE STHGPR (SET HURRICANE GRID PARAMETERS)
C  WITH ARGUMENTS (XLATH,XLONH,BEAR,GRIDSZ,XIO,YJO)
C   WHERE
C     XLATH,XLONH = LATITUDE, LONGITUDE OF THE HURRICANE
C     BEAR        = BEARING OF THE HURRICANE MOTION
C     GRIDSZ      = SIZE OF GRID ELEMENTS IN NAUTICAL MILES
C     XIO, YJO    = OFFSETS IN I AND J COORDINATES (OR I AND J
C                     COORDINATES OF HURRICANE)
C    AND WHERE
C     LATITUDES, LONGITUDES AND BEARINGS ARE GIVEN IN DEGREES,
C     POSITIVE VALUES ARE NORTH AND WEST, NEGATIVE SOUTH AND EAST,
C     BEARINGS ARE GIVEN CLOCKWISE FROM NORTH.
C
C  THE CALL TO STHGPR SHOULD BE MADE ONCE ONLY, AND BEFORE REFERENCE
C  TO ANY CALL TO LL2XYH OR XY2LLH.  IN DEFAULT, THE SYSTEM
C  WILL ASSUME A STORM AT LAT,LONG=0.,0., BEARING DUE NORTH,
C  WITH A GRIDSIZE OF 120 NAUTICAL MILES AND OFFSETS OF 0.,0. .
C
C  TO CONVERT FROM GRID COORDINATES XI AND YJ, USE A CALL TO
C    CALL XY2LLH(XI,YJ,XLAT,XLONG)
C
C  THE SUBROUTINE WILL RETURN THE LATITUDE AND LONGITUDE CORRESPONDING
C  TO THE GIVEN VALUES OF XI AND YJ.
C
C  TO CONVERT FROM LATITUDE AND LONGITUDE TO GRID COORDINATES, USE
C    CALL LL2XYH(XLAT,XLONG,XI,YJ)
C  THE SUBROUTINE WILL RETURN THE I-COORDINATE XI AND Y-COORDINATE
C  YJ CORRESPONDING TO THE GIVEN VALUES OF LATITUDE XLAT AND
C  LONGITUDE XLONG.
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DATA A /0.,-1.,0., 1.,0.,0.,  0.,0.,1./
      DATA RADPDG/1.745 3293 E-2/,RRTHNM /3 440.17/
      DATA DGRIDH/120./
      DATA HGRIDX,HGRIDY/0.,0./
      END
cx**********************************************************************
cx    SUBROUTINE STHGPR(XLATH,XLONH,BEAR,GRIDSZ,XI0,YJ0)
cx  ALBION D. TAYLOR, MARCH 19, 1982
cx    COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
cx    CLAT=COS(RADPDG*XLATH)
cx    SLAT=SIN(RADPDG*XLATH)
cx    SLON=SIN(RADPDG*XLONH)
cx    CLON=COS(RADPDG*XLONH)
cx    SBEAR=SIN(RADPDG*BEAR)
cx    CBEAR=COS(RADPDG*BEAR)
cx    A(1,1)=   CLAT*SLON
cx    A(1,2)=   CLAT*CLON
cx    A(1,3)=   SLAT
cx    A(2,1)= - CLON*CBEAR + SLAT*SLON*SBEAR
cx    A(2,2)=   SLON*CBEAR + SLAT*CLON*SBEAR
cx    A(2,3)=              - CLAT*     SBEAR
cx    A(3,1)= - CLON*SBEAR - SLAT*SLON*CBEAR
cx    A(3,2)=   SLON*SBEAR - SLAT*CLON*CBEAR
cx    A(3,3)=                CLAT*     CBEAR
cx    DGRIDH=GRIDSZ
cx    HGRIDX=XI0
cx    HGRIDY=YJ0
cx    RETURN
cx    END
cx**********************************************************************
cx    SUBROUTINE LL2XYH(XLAT,XLONG,XI,YJ)
cx  ALBION D. TAYLOR, MARCH 19, 1982
cx    COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
cx    DIMENSION ZETA(3),ETA(3)
cx    CLAT=COS(RADPDG*XLAT)
cx    SLAT=SIN(RADPDG*XLAT)
cx    SLON=SIN(RADPDG*XLONG)
cx    CLON=COS(RADPDG*XLONG)
cx    ZETA(1)=CLAT*SLON
cx    ZETA(2)=CLAT*CLON
cx    ZETA(3)=SLAT
cx    DO 20 I=1,3
cx    ETA(I)=0.
cx    DO 20 J=1,3
cx    ETA(I)=ETA(I) + A(I,J)*ZETA(J)
cx 20 CONTINUE
cx    R=SQRT(ETA(1)*ETA(1) + ETA(3)*ETA(3))
cx    XI=HGRIDX+RRTHNM*ATAN2(ETA(2),R)/DGRIDH
cx    IF(R.LE.0.) GO TO 40
cx    YJ=HGRIDY+RRTHNM*ATAN2(ETA(3),ETA(1))/DGRIDH
cx    RETURN
cx 40 YJ=0.
cx    RETURN
cx    END
cx**********************************************************************
cx    SUBROUTINE XY2LLH(XI,YJ,XLAT,XLONG)
cx  ALBION D. TAYLOR, MARCH 19, 1982
cx    COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
cx    DIMENSION ZETA(3),ETA(3)
cx    CXI=COS(DGRIDH*(XI-HGRIDX)/RRTHNM)
cx    SXI=SIN(DGRIDH*(XI-HGRIDX)/RRTHNM)
cx    SYJ=SIN(DGRIDH*(YJ-HGRIDY)/RRTHNM)
cx    CYJ=COS(DGRIDH*(YJ-HGRIDY)/RRTHNM)
cx    ETA(1)=CXI*CYJ
cx    ETA(2)=SXI
cx    ETA(3)=CXI*SYJ
cx    DO 20 I=1,3
cx    ZETA(I)=0.
cx    DO 20 J=1,3
cx    ZETA(I)=ZETA(I) + A(J,I)*ETA(J)
cx 20 CONTINUE
cx    R=SQRT(ZETA(1)*ZETA(1) + ZETA(2)*ZETA(2))
cx    XLAT=ATAN2(ZETA(3),R)/RADPDG
cx    IF(R.LE.0.) GO TO 40
cx    XLONG=ATAN2(ZETA(1),ZETA(2))/RADPDG
cx    RETURN
cx 40 XLONG=0.
cx    RETURN
cx    END
cx**********************************************************************
cx    SUBROUTINE SETUP(P1,P2,P3,P4,P5,P6,P7,P8,P)
cx    DIMENSION P(166)
cxP1 THRU P8 ARE ARE 8 PRIMARY PREDICTORS WHERE...
cx     P1 IS INITIAL LATITUDE  (DEGS)
cx     P2 IS INITIAL LONGITUDE (DEGS)
cx     P3 IS JULIAN DAY NUMBER FUNCTION
cx     P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)
cx     P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
cx     P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
cx     P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
cx     P8 IS MAXIMUM WIND (KNOTS)
cx
cxP(001 AND 002) ARE DUMMY VARIABLES AND ARE NOT FURTHER USED.
cx    DUMMY=9999.
cx    P(001)=DUMMY
cx    P(002)=DUMMY
cxP(003)THRU P(166) ARE ALL POSSIBLE PREDICTORS AS OBTAINED FROM CUBIC
cxPOLYNOMIAL EXPANSION OF ORIGINAL 8 BASIC PREDICTORS P1 THRU P8.
cxLIST THE PREDICTORS................
cx    P(003)=P8
cx    P(004)=P8*P8
cx    P(005)=P8*P8*P8
cx    P(006)=P7
cx    P(007)=P7*P8
cx    P(008)=P7*P8*P8
cx    P(009)=P7*P7
cx    P(010)=P7*P7*P8
cx    P(011)=P7*P7*P7
cx    P(012)=P6
cx    P(013)=P6*P8
cx    P(014)=P6*P8*P8
cx    P(015)=P6*P7
cx    P(016)=P6*P7*P8
cx    P(017)=P6*P7*P7
cx    P(018)=P6*P6
cx    P(019)=P6*P6*P8
cx    P(020)=P6*P6*P7
cx    P(021)=P6*P6*P6
cx    P(022)=P5
cx    P(023)=P5*P8
cx    P(024)=P5*P8*P8
cx    P(025)=P5*P7
cx    P(026)=P5*P7*P8
cx    P(027)=P5*P7*P7
cx    P(028)=P5*P6
cx    P(029)=P5*P6*P8
cx    P(030)=P5*P6*P7
cx    P(031)=P5*P6*P6
cx    P(032)=P5*P5
cx    P(033)=P5*P5*P8
cx    P(034)=P5*P5*P7
cx    P(035)=P5*P5*P6
cx    P(036)=P5*P5*P5
cx    P(037)=P4
cx    P(038)=P4*P8
cx    P(039)=P4*P8*P8
cx    P(040)=P4*P7
cx    P(041)=P4*P7*P8
cx    P(042)=P4*P7*P7
cx    P(043)=P4*P6
cx    P(044)=P4*P6*P8
cx    P(045)=P4*P6*P7
cx    P(046)=P4*P6*P6
cx    P(047)=P4*P5
cx    P(048)=P4*P5*P8
cx    P(049)=P4*P5*P7
cx    P(050)=P4*P5*P6
cx    P(051)=P4*P5*P5
cx    P(052)=P4*P4
cx    P(053)=P4*P4*P8
cx    P(054)=P4*P4*P7
cx    P(055)=P4*P4*P6
cx    P(056)=P4*P4*P5
cx    P(057)=P4*P4*P4
cx    P(058)=P3
cx    P(059)=P3*P8
cx    P(060)=P3*P8*P8
cx    P(061)=P3*P7
cx    P(062)=P3*P7*P8
cx    P(063)=P3*P7*P7
cx    P(064)=P3*P6
cx    P(065)=P3*P6*P8
cx    P(066)=P3*P6*P7
cx    P(067)=P3*P6*P6
cx    P(068)=P3*P5
cx    P(069)=P3*P5*P8
cx    P(070)=P3*P5*P7
cx    P(071)=P3*P5*P6
cx    P(072)=P3*P5*P5
cx    P(073)=P3*P4
cx    P(074)=P3*P4*P8
cx    P(075)=P3*P4*P7
cx    P(076)=P3*P4*P6
cx    P(077)=P3*P4*P5
cx    P(078)=P3*P4*P4
cx    P(079)=P3*P3
cx    P(080)=P3*P3*P8
cx    P(081)=P3*P3*P7
cx    P(082)=P3*P3*P6
cx    P(083)=P3*P3*P5
cx    P(084)=P3*P3*P4
cx    P(085)=P3*P3*P3
cx    P(086)=P2
cx    P(087)=P2*P8
cx    P(088)=P2*P8*P8
cx    P(089)=P2*P7
cx    P(090)=P2*P7*P8
cx    P(091)=P2*P7*P7
cx    P(092)=P2*P6
cx    P(093)=P2*P6*P8
cx    P(094)=P2*P6*P7
cx    P(095)=P2*P6*P6
cx    P(096)=P2*P5
cx    P(097)=P2*P5*P8
cx    P(098)=P2*P5*P7
cx    P(099)=P2*P5*P6
cx    P(100)=P2*P5*P5
cx    P(101)=P2*P4
cx    P(102)=P2*P4*P8
cx    P(103)=P2*P4*P7
cx    P(104)=P2*P4*P6
cx    P(105)=P2*P4*P5
cx    P(106)=P2*P4*P4
cx    P(107)=P2*P3
cx    P(108)=P2*P3*P8
cx    P(109)=P2*P3*P7
cx    P(110)=P2*P3*P6
cx    P(111)=P2*P3*P5
cx    P(112)=P2*P3*P4
cx    P(113)=P2*P3*P3
cx    P(114)=P2*P2
cx    P(115)=P2*P2*P8
cx    P(116)=P2*P2*P7
cx    P(117)=P2*P2*P6
cx    P(118)=P2*P2*P5
cx    P(119)=P2*P2*P4
cx    P(120)=P2*P2*P3
cx    P(121)=P2*P2*P2
cx    P(122)=P1
cx    P(123)=P1*P8
cx    P(124)=P1*P8*P8
cx    P(125)=P1*P7
cx    P(126)=P1*P7*P8
cx    P(127)=P1*P7*P7
cx    P(128)=P1*P6
cx    P(129)=P1*P6*P8
cx    P(130)=P1*P6*P7
cx    P(131)=P1*P6*P6
cx    P(132)=P1*P5
cx    P(133)=P1*P5*P8
cx    P(134)=P1*P5*P7
cx    P(135)=P1*P5*P6
cx    P(136)=P1*P5*P5
cx    P(137)=P1*P4
cx    P(138)=P1*P4*P8
cx    P(139)=P1*P4*P7
cx    P(140)=P1*P4*P6
cx    P(141)=P1*P4*P5
cx    P(142)=P1*P4*P4
cx    P(143)=P1*P3
cx    P(144)=P1*P3*P8
cx    P(145)=P1*P3*P7
cx    P(146)=P1*P3*P6
cx    P(147)=P1*P3*P5
cx    P(148)=P1*P3*P4
cx    P(149)=P1*P3*P3
cx    P(150)=P1*P2
cx    P(151)=P1*P2*P8
cx    P(152)=P1*P2*P7
cx    P(153)=P1*P2*P6
cx    P(154)=P1*P2*P5
cx    P(155)=P1*P2*P4
cx    P(156)=P1*P2*P3
cx    P(157)=P1*P2*P2
cx    P(158)=P1*P1
cx    P(159)=P1*P1*P8
cx    P(160)=P1*P1*P7
cx    P(161)=P1*P1*P6
cx    P(162)=P1*P1*P5
cx    P(163)=P1*P1*P4
cx    P(164)=P1*P1*P3
cx    P(165)=P1*P1*P2
cx    P(166)=P1*P1*P1
cx    RETURN
cx    END
C***********************************************************************
cx    SUBROUTINE YX2LL(ALAT0,ALON0,DISP,CFCST)
cxINCOMING ARGUMENTS:
cx    ALAT0, ALON0...INITIAL STORM POSTION
cx    DISP...........FORECAST MERIDIONAL & ZONAL DISPLACEMENTS IN NMI.
cxRETURNED ARGUMENT:
cx    CDISP..........FORECASTS IN TERMS OF LAT/LON
cx
cx    REAL*4 DISP(12),CFCST(12)
cx    CALL STHGPR(ALAT0,F1(ALON0),360.,1.,0.,0.)
cx    DO 10 I=1,6
cx    CALL XY2LLH(DISP(2*I),DISP(2*I-1),CFCST(2*I-1),CFCST(2*I))
cxNOTE: ABOVE SUBROUTINE RETURNS LONGITUDES WEST OF 180 AS NEGATIVE AND
cxEAST OF 180 AS POSITIVE.  CONVERT ALL LONGITUDES TO EAST
cxREMOVIT
cx    IF(CFCST(2*I).GE.0.AND.CFCST(2*I).LT.180.)CFCST(2*I)=360.-
cx   $CFCST(2*I)
cx    IF(CFCST(2*I).LT.0.)CFCST(2*I)=-CFCST(2*I)
cx 10 CONTINUE
cx    RETURN
cx    END
cx*********************************************************************
cx    FUNCTION NEWCYC(NOWCYC,N)
cxGIVEN CYCLE TIME NOWCYC, GET NEW CYCLE TIME (NEWCYC) GIVEN BY
cxNOWCYC + N HOURS.  LIMIT 0F N IS + OR - 744 HOURS.  ALLOWANCES
cxARE MADE FOR LEAP YEARS.
cx(C.J.NEUMANN, SAIC, OCTOBER, 1989)
cx    CHARACTER*8 ALFA
cx    INTEGER NHEM(15),NOLEAP(15),ADDYR
cx    DATA NOLEAP /000,744,1488,2160,2904,3624,4368,5088,5832,6576,7296,
cx   $8040,8760,9504,10248/
cxABOVE DATA STATEMENT GIVES NUMBER OF HOURS FOR NON-LEAP YEAR MONTHS
cxMONTHS 0000UTC ON 1 DEC THRU 0000UTC ON 1 FEB OF SECOND YEAR.
cx
cxOBTAIN YEAR (KYR),MONTH (M0),DAY (KDA) AND HOUR (JTM) IN INTEGER FORMAT
cx    WRITE(ALFA,'(I8)')NOWCYC
cx    READ(ALFA,'(4I2)')KYR,MO,KDA,JTM
cx    DO 10 I=1,15
cx 10 NHEM(I)=NOLEAP(I)
cxIS THIS A LEAP YEAR? (YEAR 2000 IS A LEAP YEAR)
cx    IF(MOD(KYR,4).EQ.0)THEN
cx    DO 20 I=4,15
cx 20 NHEM(I)=NHEM(I)+24
cx    ENDIF
cxHOW MANY HRS FROM BEGINNING OF TIME WINDOW AT 0000UTC, 1 DEC (NHROLD)?
cx    NHROLD=NHEM(MO+1)+(KDA-1)*24+JTM
cxHOW MANY HRS NEEDED FROM BEGINNING OF WINDOW (NHRNEW)?
cx    NHRNEW=NHROLD+N
cx
cx    DO 30 MO=2,15
cxMO = 2 = PREVIOUS YEAR; M0 = 15 = NEXT YEAR; DO WE NEED TO ADD OR
cxSUBTRACT A YEAR??
cx    KYRNEW=KYR-(2/MO)+MO/15
cxCHANGE OF CENTURY?
cx    IF(KYRNEW.EQ.100)KYRNEW=0
cx    IF(KYRNEW.EQ.-1)KYRNEW=99
cx
cx    IF(NHRNEW.LT.NHEM(MO))GOTO 40
cx 30 CONTINUE
cx 40 NDIF=NHRNEW-NHEM(MO-1)
cx    LDA=(NDIF+24)/24
cx    LTM=NDIF+24-(LDA*24)
cx    INDEX=MOD(MO-3,12)+(2/MO)*12+1
cx    NEWCYC=KYRNEW*1000000+INDEX*10000+LDA*100+LTM
cx    RETURN
cx    END
cx*******************************************************************8
cx    SUBROUTINE LL2DB(XLATO,XLONO,XLATT,XLONT,DIST,BEAR)
cx     ALBION D. TAYLOR MARCH 18, 1981
cx    DATA RRTHNM/3 440.17/,RADPDG/1.745 3293 E-2/
cx  RRTHNM=RADIUS OF EARTH IN NAUT. MILES, RADPDG==OF RADIANS
cx  PER DEGREE
cx---------------------------------------------------------------------*
cx GIVEN AN ORIGIN AT LATITUDE, LONGITUDE=XLATO,XLONO, WILL LOCATE     *
cx A TARGET POINT AT LATITUDE, LONGITUDE = XLATT, XLONT.  RETURNS      *
cx DISTANCE DIST IN NAUTICAL MILES, AND BEARING BEAR (DEGREES CLOCKWISE*
cx FROM NORTH).                                                        *
cx                                                                     *
cx ALL LATITUDES ARE IN DEGREES, NORTH POSITIVE AND SOUTH NEGATIVE.    *
cx ALL LONGITUDES ARE IN DEGREES, WEST POSITIVE AND EAST NEGATIVE.     *
cx                                                                     *
cx NOTE-- WHEN ORIGIN IS AT NORTH OR SOUTH POLE, BEARING IS NO LONGER  *
cx MEASURED FROM NORTH.  INSTEAD, BEARING IS MEASURED CLOCKWISE        *
cx FROM THE LONGITUDE OPPOSITE THAT SPECIFIED IN XLONO.                *
cx EXAMPLE-- IF XLATO=90., XLONO=80., THE OPPOSITE LONGITUDE IS -100.  *
cx (100 EAST), AND A TARGET AT BEARING 30. WILL LIE ON THE -70.        *
cx (70 EAST) MERIDIAN                                                  *
cx---------------------------------------------------------------------*
cx    CLATO=COS(RADPDG*XLATO)
cx    SLATO=SIN(RADPDG*XLATO)
cx    CLATT=COS(RADPDG*XLATT)
cx    SLATT=SIN(RADPDG*XLATT)
cx    CDLON=COS(RADPDG*(XLONT-XLONO))
cx    SDLON=SIN(RADPDG*(XLONT-XLONO))
cx    Z=SLATT*SLATO + CLATT*CLATO*CDLON
cx    Y= - CLATT*SDLON
cx    X=CLATO*SLATT - SLATO*CLATT*CDLON
cx    R=SQRT(X*X+Y*Y)
cx    DIST=RRTHNM*ATAN2(R,Z)
cx    IF (R.LE.0.) GO TO 20
cx    BEAR=ATAN2(-Y,-X)/RADPDG + 180.
cx    RETURN
cx 20 BEAR=0.
cx    RETURN
cx    END
C***********************************************************************
      BLOCK DATA BLKSE1
C
C ENTER ALL CONSTANTS NEEDED BY SEICPR PROGRAM......
C
      INTEGER*2
     $       N12M(16),N24M(16),N36M(16),N48M(16),N60M(16),N72M(16)
      INTEGER*2
     $       N12Z(14),N24Z(14),N36Z(14),N48Z(14),N60Z(14),N72Z(14)
      REAL*4 R12M(16),R24M(16),R36M(16),R48M(16),R60M(16),R72M(16)
      REAL*4 R12Z(14),R24Z(14),R36Z(14),R48Z(14),R60Z(14),R72Z(14)
      COMMON/BLOCKSE1/RCM(16,6),RCZ(14,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(16,6),NPZ(14,6)
      COMMON/BLOCKSE2/NPM,NPZ
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
     A .6500266E+0, .4346360E-5,-.1586378E-5, .1144783E-4, .5048783E-5,
     B .2668805E-3,-.1150471E-4, .2681863E-5,-.4829064E-4,-.9490418E-5,
     C .1263979E-4,-.3055094E-5,-.1968997E-5, .1506849E-5, .2188557E-6,
     D-.2363125E-6/
C
C  12HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N12M/
     A         037,         053,         017,         071,         100,
     B         138,         110,         056,         157,         014,
     C         065,         062,         026,         121,         091,
     D         042/
C
C  24HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R24M/
     A .6670975E-3, .9767612E+0,-.4016455E-5, .2219380E-4, .3137972E-5,
     B-.3051675E-4, .2629791E-4,-.2129713E-4,-.8695877E-4, .7082292E-5,
     C-.7412803E-5, .2748492E-4,-.1680689E-5, .7428285E-5,-.3940199E-5,
     D-.1566399E-5/
C
C  24HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N24M/
     A         138,         037,         017,         056,         091,
     B         110,         053,         014,         157,         100,
     C         026,         065,         042,         071,         062,
     D         121/
C
C  36HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R36M/
     A .1250097E-2,-.3822699E-4,-.4209243E-5,-.1356181E-3, .5742563E-5,
     B .9596518E+0, .3140751E-4,-.4294882E-4, .5567016E-4,-.7244950E-5,
     C-.1478741E-4, .9795566E-5,-.6965742E-5,-.9348780E-5, .2514677E-4,
     D-.7001534E-5/
C
C  36HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N36M/
     A         138,         014,         017,         157,         091,
     B         037,         056,         110,         053,         042,
     C         026,         100,         062,         121,         065,
     D         071/
C
C  48HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R48M/
     A .1815626E-2,-.1489150E-4, .1158459E+1,-.7293896E-4,-.2011209E-4,
     B-.2939316E-4, .5922391E-5,-.2560332E-4,-.2025014E-3,-.4017675E-4,
     C .1188901E-4, .1556017E-4,-.9906227E-5, .2288921E-4,-.4250887E-5,
     D .2646512E-6/
C
C  48HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N48M/
     A         138,         042,         037,         110,         121,
     B         062,         091,         026,         157,         014,
     C         100,         056,         071,         065,         053,
     D         017/
C
C  60HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R60M/
     A .2067777E-2,-.1384777E-3,-.3541299E-3,-.6422765E-4,-.3528279E-4,
     B .1111489E+1,-.1282683E-4, .4729876E-5,-.2850844E-4, .1535681E-4,
     C-.4623132E-4, .2807974E-4,-.4005565E-4,-.6783397E-5, .5561948E-6,
     D .7085590E-5/
C
C  60HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N60M/
     A         138,         065,         157,         062,         026,
     B         037,         042,         091,         121,         100,
     C         110,         056,         071,         014,         017,
     D         053/
C
C  72HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R72M/
     A .2259347E-2,-.3210257E-3,-.8231678E-4,-.4438970E-3,-.4845527E-4,
     B .1471507E-4,-.9748230E-5, .1188192E-3,-.1123290E-3, .6557345E-4,
     C .7651687E-5,-.3061854E-4, .5066699E+0, .2636657E-4,-.1313600E-5,
     D-.1035049E-4/
C
C  72HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N72M/
     A         138,         065,         062,         157,         026,
     B         100,         042,         053,         071,         056,
     C         091,         121,         037,         014,         017,
     D         110/
C
C    12 THROUGH 72HR MERIDIONAL INTERCEPT VALUES
      DATA CNSTM/
     $ .19093E+2, .55071E+2, .11086E+3, .18268E+3, .27011E+3, .33529E+3/
C
C  12HR ZONAL REGRESSION COEFFICIENTS
      DATA R12Z/
     A .1296249E+1, .8375126E-5,-.1378439E+0,-.1327108E-4, .2397764E-4,
     B-.2489660E-5, .8464961E-2,-.2047595E+0,-.7229803E-4, .2126735E-4,
     C-.3955738E-5, .3863061E-2, .7852138E-5, .5536868E-4/
C
C  12HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N12Z/
     A         022,         044,         006,         042,         049,
     B         036,         166,         158,         152,         084,
     C         117,         125,         053,         089/
C
C  24HR ZONAL REGRESSION COEFFICIENTS
      DATA R24Z/
     A .2528738E+1, .2169040E-4,-.4290250E+0, .2484030E-1,-.6118201E-5,
     B-.5986292E+0,-.2447727E-4, .4172904E-4, .9053409E-4,-.1539276E-4,
     C-.3145838E-3, .2625315E-4, .2009991E-1, .1955873E-2/
C
C  24HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N24Z/
     A         022,         053,         006,         166,         036,
     B         158,         042,         049,         084,         117,
     C         152,         044,         125,         089/
C
C  36HR ZONAL REGRESSION COEFFICIENTS
      DATA R36Z/
     A .3506600E+1, .4677240E-1, .6067485E-2, .2020475E-3,-.1054669E-4,
     B-.2988771E-4, .4541072E-4,-.1097270E+1,-.1025092E-2,-.2096134E-4,
     C .3237902E-4, .7223325E-1,-.6436815E+0, .2281674E-4/
C
C  36HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N36Z/
     A         022,         166,         089,         084,         036,
     B         117,         044,         158,         152,         042,
     C         049,         125,         006,         053/
C
C  48HR ZONAL REGRESSION COEFFICIENTS
      DATA R48Z/
     A .4371525E+1, .6868443E-1,-.9669937E-2, .3271418E-3,-.4574040E-4,
     B-.1046727E-4,-.1574199E+1,-.1356174E-3, .7263980E-4, .1305655E+1,
     C-.2078065E-4, .3972008E-4,-.5117910E-1,-.3080416E-4/
C
C  48HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N48Z/
     A         022,         166,         089,         084,         117,
     B         036,         158,         152,         044,         006,
     C         042,         049,         125,         053/
C
C  60HR ZONAL REGRESSION COEFFICIENTS
      DATA R60Z/
     A .4757084E+1, .8786910E-1,-.1940565E+1, .6936690E-3, .4315261E-3,
     B-.5061832E-4,-.7381739E-5, .6156225E-4,-.1702064E-1, .5585419E-4,
     C-.2396341E-4,-.1508715E+0, .2208045E+1,-.4975949E-5/
C
C  60HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N60Z/
     A         022,         166,         158,         152,         084,
     B         117,         036,         053,         089,         049,
     C         042,         125,         006,         044/
C
C  72HR ZONAL REGRESSION COEFFICIENTS
      DATA R72Z/
     A .5412447E+1, .1236903E+0,-.2725503E+1,-.1207977E+0, .5459844E-3,
     B-.6757351E-4,-.7194847E-5, .1144012E-3, .4378634E-3, .6353992E-4,
     C-.2713346E-4,-.3563588E-4, .1248191E+1,-.1034481E-1/
C
C  72HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N72Z/
     A         022,         166,         158,         125,         084,
     B         117,         036,         053,         152,         049,
     C         042,         044,         006,         089/
C
C    12 THROUGH 72HR ZONAL INTERCEPT VALUES
      DATA CNSTZ/
     $ .11519E+2, .32226E+2, .51082E+2, .66364E+2, .58771E+2, .86333E+2/
      END
C***********************************************************************
C
      SUBROUTINE SWPCLP(IDATIM,ALAT00,ALON00,ALAT12,ALON12,ALAT24,
     $ALON24,WIND)
C
C Developed by:
C Charles J. Neumann, Science Applications International Corporation, 
C June, 2000.   (revised 10/25/00)
C
C Installed in ATCF3.5:
C Sampson, NRL (5/1/01)  
C
C Documentation:
C SAIC Final Report on the Southwest Pacific CLIPER Model (SWCLP)
C October, 2000
C
C
C THIS IS A CLIPER PROGRAM FOR THE EAST AUSTRALIA\SW PACIFIC OCEAN BASIN.  
C THE FOLLOWING SHOULD BE NOTED:
C (1) PROGRAM WAS DEVELOPED USING STORM TRACKS OVER YEARS 1970/1971 TO
C     1998/1999
C (2) DEVELOPMENTAL DATA SET INCLUDED ALL DATES EXCEPT JULY 1 THROUGH
C     SEPTEMBER 15.
C (3) ANY STORMS HAVING POSITIONS WEST OF 142E WERE EXCLUDED FROM
C     DEVELOPMENTAL DATA SET.  NUMBER OF TC'S INCLUDED = 296
C (4) STORMS POSITIONS SOUTH OF 50S WERE EXCLUDED FROM DEVELOPMENTAL
C     DATA SET.
C (5) STORMS WHICH INITIALLY CLASSIFIED AS DEPRESSIONS OR CLASSIFIED AS
C     DEPRESSIONS AT VERIFICATION TIME WERE EXCLUDED.
C (6) SAMPLE SIZE,  4619 AT 12H,  4075 AT 24H,  3588 AT 36H,
C                   3125 AT 48H,  2698 AT 60H,  2307 AT 72H.
C (7) INDIVIDUAL CASES IN DEVELOPMENTAL DATA SET WERE AT 6 HRLY INTERVALS
C
C INCOMING ARGUMENTS ARE AS FOLLOWS:
C   IDATIM (INTEGER*4) IS IN FORM YY/MO/DA/HR AS 01040106 FOR
C   DATE APRIL 1, 2001.
C   ALAT00 AND ALON00 ARE INITIAL STORM POSITION (REAL*4)
C   ALAT12 AND ALON12 ARE POSITION 12H EARLIER   (REAL*4)
C   ALAT24 AND ALON24 ARE POSITION 24H EARLIER   (REAL*4)
C     NOTE: IT IS ASSUMED THAT S LATITUDES AND E LONGITUDES WILL BE 
C     ENTERED AS POSITIVE VALUES.
C   WIND IS MAXIMUM WIND (1-MINUTE AVERAGE) NEAR STORM CENTER IN KNOTS
C   (REAL*4).
C
C RETURNED ARGUMENTS ARE:
C   STORM DISPLACEMENTS AS GIVEN BY (DISP(J),J=1,12);
C   POSITIONS AS GIVEN BY (CDISP(J),J=1,12);
C   VALUES OF 8 BASIC PREDICTORS AS GIVEN BY (P1TOP8(K),K=1,8)
C
C ARRANGEMENT OF DISP AND CDISP ARRAY IS AS FOLLOWS:
C      DISP(01) IS MERIDIONAL 12H DISPLACEMENT (NMI)
C      DISP(02) IS ZONAL 12H DISPLACEMENT (NMI)
C      DISP(03) IS MERIDIONAL 24H DISPLACEMENT (NMI)
C      DISP(04) IS ZONAL 24H DISPLACEMENT (NMI)
C      DISP(05) IS MERIDIONAL 36H DISPLACEMENT (NMI)
C      DISP(06) IS ZONAL 36H DISPLACEMENT (NMI)
C      DISP(07) IS MERIDIONAL 48H DISPLACEMENT (NMI)
C      DISP(08) IS ZONAL 48H DISPLACEMENT (NMI)
C      DISP(09) IS MERIDIONAL 60H DISPLACEMENT (NMI)
C      DISP(10) IS ZONAL 60H DISPLACEMENT (NMI)
C      DISP(11) IS MERIDIONAL 72H DISPLACEMENT (NMI)
C      DISP(12) IS ZONAL 72H DISPLACEMENT (NMI)
C NOTE: NEGATIVE DISPLACEMENTS ARE TOWARDS WEST OR SOUTH.
C       CDISP ARRAY CORRESPONDS TO DISP ARRAY EXCEPT THAT DISPLACEMENTS
C       HAVE BEEN CONVERTED TO LATITUDES SOUTH AND LONGITUDES EAST
C
      common/swpclpfcst/ cfcst(12)
      COMMON/BLOCKSW1/RCM(31,6),RCZ(31,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(31,6),NPZ(31,6)
      COMMON/BLOCKSW2/NPM,NPZ
      REAL*4 P(166),DISP(12),P1TOP8(8)
C INITIALLY, 008 PREDICTORS OUT OF 164 POSSIBLE PREDICTORS (LISTED IN
C SUBROUTINE SETUP) WERE SELECTED FOR EACH TIME PERIOD AND FOR BOTH ZONAL
C AND MERIDIONAL MOTION.  A FINAL SET OF PREDICTORS FOR EACH COMPONENT OF
C MOTION INCLUDED ALL PREDICTORS SELECTED AT LEAST ONCE, 12 THRU 72H.
C THIS TURNED OUT TO BE 31 PREDICTORS FOR MERIDIONAL MOTION AND 31 FOR
C ZONAL MOTION.
C
C ALL REGRESSION COEFFICIENTS ARE PREDICTOR NUMBERS ARE CONTAINED IN
C BLOCK DATA BLKSW1.  THERE ARE 31 PREDICTORS AND PREDICTOR
C NUMBERS FOR MERIDIONAL MOTION AND 31 PREDICTORS AND PREDICTOR NUMBERS
C FOR ZONAL MOTION. ((RCM(I,J),J=1,6,I=1,31) & ((NPM(I,J),J=1,6),I=1,31)
C ARE COEFFICEINTS AND PREDICTOR NUMBERS FOR MERIDIONAL MOTION WHILE
C ((RCZ(I,J),J=1,6,I=1,31) AND ((NPZ(I,J),J=1,6),I=1,31) ARE COEFFICIENTS
C AND PREDICTOR NUMBERS FOR ZONAL MOTION. SUBSCRIPT J REFERS TO TIME WHERE
C J=1=12H.........J=6=72H.
C 6 MERIDIONAL INTERCEPT VALUES ARE GIVEN BY (CNSTM(J),J=1,6) WHILE THE
C 6 ZONAL INTERCEPT VALUES ARE GIVEN BY (CNSTZ(J),J=1,6).
C P1 THRU P8 ARE 8 PRIMARY PREDICTORS WHERE...
C    P1 IS INITIAL LATITUDE  (DEGS SOUTH)
C    P2 IS INITIAL LONGITUDE (DEGS EAST)
C    P3 IS JULIAN DAY NUMBER FUNCTION DEFINED AS NUMBER OF DAYS (ABSOLUTE)
C          EITHER SIDE OF MARCH 1 (APPROXIMATE MID-SEASON FOR THIS AREA).
C    P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)
C    P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
C    P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
C    P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
C    P8 IS MAXIMUM WIND (KNOTS) ASSUMING A 1-MINUTE WIND MEASURING
C          SYSTEM.
C FUNCTIONS AND SUBPROGRAMS NEEDED BY SWPCLP ARE AS FOLLOWS:
C    DATA NEEDED BY PROGRAM ARE CONTAINED IN BLOCK DATA BLKSW1 AND BLKSW2
C    SWPCLP CALLS SUBROUTINES STHGPR, LL2XYH, SETUP, YX2LL AND UPRCAS
C           AND UTILIZES FUNCTIONS F1, F2
C    YX2LL CALLS SUBROUTINE XY2LLH AND UTILIZES FUNCTION F1
C SET UP 8 BASIC PREDICTORS......
      P1=ALAT00
      P2=ALON00
C JULIAN DAY NUMBER
      DANBR=F2(IDATIM)
      IDN=DANBR+.5
C AVERAGE TC DAY NUMBER FOR THIS BASIN IS NEAR 60 (1 MARCH)
      MEANDN=60
C PUT OFF-SEASON DAY NUMBERS IN ALLOWABLE RANGE
      IF(IDN.GT.181.AND.IDN.LE.220)IDN=181
      IF(IDN.GT.220.AND.IDN.LT.259)IDN=259
C
      IF(IDN.GE.1.AND.IDN.LE.181)IDADIF=IABS(MEANDN-IDN)
      IF(IDN.GE.259)IDADIF=366-IDN+MEANDN
      P3=IDADIF
      P8=WIND
C USE AL TAYLOR ROUTINE FOR CONVERTING LATITUDE/LONGITUDE TO DISPLACEMENTS.
C THIS SAME ROUTINE IS LATER USED FOR CONVERTING DISPLACEMENTS BACK TO
C LATITUDES AND LONGITUDES........
C (PREDICTORS NUMBER P4 THRU P7)
      CALL STHGPR(P1,F1(P2),360.,1.,0.,0.)
      CALL LL2XYH(ALAT12,F1(ALON12),P5,P4)
      CALL LL2XYH(ALAT24,F1(ALON24),P7,P6)
C CHANGE SIGN
      P4=-P4
      P5=-P5
      P6=-P6
      P7=-P7
C BASIC PREDICTOR SETUP IS COMPLETE. PUT 8 VALUES INTO ARRAY P1TOP8 FOR
C POSSIBLE USE IN CALLING PROGRAM
      P1TOP8(1)=P1
      P1TOP8(2)=P2
      P1TOP8(3)=P3
      P1TOP8(4)=P4
      P1TOP8(5)=P5
      P1TOP8(6)=P6
      P1TOP8(7)=P7
      P1TOP8(8)=P8
C
C PREPARE FORECAST, FIRST, OBTAIN ALL POSSIBLE 3RD ORDER PRODUCTS AND
C CROSS-PRODUCTS OF THE 8 BASIC PREDICTORS AND RETURN THESE IN ARRAY
C (P(L),L=1,166).  THERE ARE 164 POSSIBLE COMBINATIONS AND THESE ARE
C GIVEN BY SUBSCRIPTS 3 THROUGH 166. P(1) AND P(2) ARE NOT USED AND HAVE
C BEEN RETURNED AS DUMMY VARIABLES. NOT ALL OF THE 164 POSSIBLE PREDICTORS
C ARE USED IN PROGRAM.
      CALL SETUP(P1,P2,P3,P4,P5,P6,P7,P8,P)
C OBTAIN FORECAST MERIDIONAL DISPLACEMENTS 12 THRU 72H
      DO 60 J=1,6
C INITIALIZE COMPUTATION WITH INTERCEPT VALUE
      DISP(2*J-1)=CNSTM(J)
      DO 50 I=1,31
      K=NPM(I,J)
      DISP(2*J-1)=DISP(2*J-1)+RCM(I,J)*P(K)
   50 CONTINUE
   60 CONTINUE
C
C OBTAIN FORECAST ZONAL DISPLACEMENTS 12 THRU 72H
C
      DO 80 J=1,6
C INITIALIZE COMPUTATION WITH INTERCEPT VALUE
      DISP(2*J)=CNSTZ(J)
      DO 70 I=1,31
      K=NPZ(I,J)
      DISP(2*J)=DISP(2*J)+RCZ(I,J)*P(K)
   70 CONTINUE
   80 CONTINUE
C CONVERT DISPLACEMENTS TO LATITUDE AND LONGITUDE
      CALL YX2LL(ALAT00,ALON00,DISP,CFCST)
C REVERSE SIGN OF LATITUDINAL DISPLACEMENTS
      DO 90 J=1,11,2
   90 DISP(J)=-DISP(J)
      RETURN
      END
cx**********************************************************************
cx    FUNCTION F1(ALON)
cxCONVERT FROM E LONGITUDE TO THOSE ACCEPTABLE IN AL TAYLOR ROUTINES
cx    IF(ALON.GT.180.)F1=360.-ALON
cx    IF(ALON.LE.180.)F1=-ALON
cx    RETURN
cx    END
cx**********************************************************************
cx    FUNCTION F2(IDATIM)
cxOBTAIN JULIAN DAY NUMBER
cx0000UTC ON 1 JAN IS SET TO DAY NUMBER 0 AND 1800UTC ON 31 DEC IS SET TO
cxDAY NUMBER 364.75.  LEAP YEARS ARE IGNORED.
cx    CHARACTER*8 ALFA
cx    WRITE(ALFA,'(I8)')IDATIM
cx    READ(ALFA,'(4I2)')KYR,MO,KDA,KHR
cx    MON=MO
cx    IF(MON.EQ.13)MON=1
cx    DANBR=3055*(MON+2)/100-(MON+10)/13*2-91+KDA
cx    F2=DANBR-1.+FLOAT(KHR/6)*0.25
cx    RETURN
cx    END
C***********************************************************************
      BLOCK DATA BLKSW2
C
C   ALBION D. TAYLOR, MARCH 19, 1982
C  THE HURRICANE GRID IS BASED ON AN OBLIQUE EQUIDISTANT CYLINDRICAL
C  MAP PROJECTION ORIENTED ALONG THE TRACK OF THE HURRICANE.
C
C    THE X (OR I) COORDINATE XI OF A POINT REPRESENTS THE DISTANCE
C  FROM THAT POINT TO THE GREAT CIRCLE THROUGH THE HURRICANE, IN
C  THE DIRECTION OF MOTION OF THE HURRICANE MOTION.  POSITIVE VALUES
C  REPRESENT DISTANCES TO THE RIGHT OF THE HURRICANE MOTION, NEGATIVE
C  VALUES REPRESENT DISTANCES TO THE LEFT.
C    THE Y (OR J) COORDINATE OF THE POINT REPRESENTS THE DISTANCE
C  ALONG THE GREAT CIRCLE THROUGH THE HURRICANE TO THE PROJECTION
C  OF THE POINT ONTO THAT CIRCLE.  POSITIVE VALUES REPRESENT
C  DISTANCE IN THE DIRECTION OF HURRICANE MOTION, NEGATIVE VALUES
C  REPRESENT DISTANCE IN THE OPPOSITE DIRECTION.
C
C     SCALE DISTANCES ARE STRICTLY UNIFORM IN THE I-DIRECTION ALWAYS.
C  THE SAME SCALE HOLDS IN THE J-DIRECTION ONLY ALONG THE HURRICANE TRACK
C  ELSEWHERE, DISTANCES IN THE J-DIRECTION ARE EXAGGERATED BY A FACTOR
C  INVERSELY PROPORTIONAL TO THE COSINE OF THE ANGULAR DISTANCE FROM
C  THE TRACK.  THE SCALE IS CORRECT TO 1 PERCENT WITHIN A DISTANCE OF
C  480 NM OF THE STORM TRACK, 5 PERCENT WITHIN 1090 NM, AND
C  10 PERCENT WITHIN 1550 NM.
C
C  BIAS VALUES ARE ADDED TO THE XI AND YJ COORDINATES FOR CONVENIENCE
C  IN INDEXING.
C
C  A PARTICULAR GRID IS SPECIFIED BY THE USER BY MEANS OF A CALL
C  TO SUBROUTINE STHGPR (SET HURRICANE GRID PARAMETERS)
C  WITH ARGUMENTS (XLATH,XLONH,BEAR,GRIDSZ,XIO,YJO)
C   WHERE
C     XLATH,XLONH = LATITUDE, LONGITUDE OF THE HURRICANE
C     BEAR        = BEARING OF THE HURRICANE MOTION
C     GRIDSZ      = SIZE OF GRID ELEMENTS IN NAUTICAL MILES
C     XIO, YJO    = OFFSETS IN I AND J COORDINATES (OR I AND J
C                     COORDINATES OF HURRICANE)
C    AND WHERE
C     LATITUDES, LONGITUDES AND BEARINGS ARE GIVEN IN DEGREES,
C     POSITIVE VALUES ARE NORTH AND WEST, NEGATIVE SOUTH AND EAST,
C     BEARINGS ARE GIVEN CLOCKWISE FROM NORTH.
C
C  THE CALL TO STHGPR SHOULD BE MADE ONCE ONLY, AND BEFORE REFERENCE
C  TO ANY CALL TO LL2XYH OR XY2LLH.  IN DEFAULT, THE SYSTEM
C  WILL ASSUME A STORM AT LAT,LONG=0.,0., BEARING DUE NORTH,
C  WITH A GRIDSIZE OF 120 NAUTICAL MILES AND OFFSETS OF 0.,0. .
C
C  TO CONVERT FROM GRID COORDINATES XI AND YJ, USE A CALL TO
C    CALL XY2LLH(XI,YJ,XLAT,XLONG)

C  THE SUBROUTINE WILL RETURN THE LATITUDE AND LONGITUDE CORRESPONDING
C  TO THE GIVEN VALUES OF XI AND YJ.
C
C  TO CONVERT FROM LATITUDE AND LONGITUDE TO GRID COORDINATES, USE
C    CALL LL2XYH(XLAT,XLONG,XI,YJ)
C  THE SUBROUTINE WILL RETURN THE I-COORDINATE XI AND Y-COORDINATE
C  YJ CORRESPONDING TO THE GIVEN VALUES OF LATITUDE XLAT AND
C  LONGITUDE XLONG.
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DATA A /0.,-1.,0., 1.,0.,0.,  0.,0.,1./
      DATA RADPDG/1.745 3293 E-2/,RRTHNM /3 440.17/
      DATA DGRIDH/120./
      DATA HGRIDX,HGRIDY/0.,0./
      END
cx**********************************************************************
cx    SUBROUTINE STHGPR(XLATH,XLONH,BEAR,GRIDSZ,XI0,YJ0)
cx  ALBION D. TAYLOR, MARCH 19, 1982
cx    COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
cx    CLAT=COS(RADPDG*XLATH)
cx    SLAT=SIN(RADPDG*XLATH)
cx    SLON=SIN(RADPDG*XLONH)
cx    CLON=COS(RADPDG*XLONH)
cx    SBEAR=SIN(RADPDG*BEAR)
cx    CBEAR=COS(RADPDG*BEAR)
cx    A(1,1)=   CLAT*SLON
cx    A(1,2)=   CLAT*CLON
cx    A(1,3)=   SLAT
cx    A(2,1)= - CLON*CBEAR + SLAT*SLON*SBEAR
cx    A(2,2)=   SLON*CBEAR + SLAT*CLON*SBEAR
cx    A(2,3)=              - CLAT*     SBEAR
cx    A(3,1)= - CLON*SBEAR - SLAT*SLON*CBEAR
cx    A(3,2)=   SLON*SBEAR - SLAT*CLON*CBEAR
cx    A(3,3)=                CLAT*     CBEAR
cx    DGRIDH=GRIDSZ
cx    HGRIDX=XI0
cx    HGRIDY=YJ0
cx    RETURN
cx    END
cx**********************************************************************
cx    SUBROUTINE LL2XYH(XLAT,XLONG,XI,YJ)
cx  ALBION D. TAYLOR, MARCH 19, 1982
cx    COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
cx    DIMENSION ZETA(3),ETA(3)
cx    CLAT=COS(RADPDG*XLAT)
cx    SLAT=SIN(RADPDG*XLAT)
cx    SLON=SIN(RADPDG*XLONG)
cx    CLON=COS(RADPDG*XLONG)
cx    ZETA(1)=CLAT*SLON
cx    ZETA(2)=CLAT*CLON
cx    ZETA(3)=SLAT
cx    DO 20 I=1,3
cx    ETA(I)=0.
cx    DO 20 J=1,3
cx    ETA(I)=ETA(I) + A(I,J)*ZETA(J)
cx 20 CONTINUE
cx    R=SQRT(ETA(1)*ETA(1) + ETA(3)*ETA(3))
cx    XI=HGRIDX+RRTHNM*ATAN2(ETA(2),R)/DGRIDH
cx    IF(R.LE.0.) GO TO 40
cx    YJ=HGRIDY+RRTHNM*ATAN2(ETA(3),ETA(1))/DGRIDH
cx    RETURN
cx 40 YJ=0.
cx    RETURN
cx    END
cx *********************************************************************
cx    SUBROUTINE XY2LLH(XI,YJ,XLAT,XLONG)
cx  ALBION D. TAYLOR, MARCH 19, 1982
cx    COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
cx    DIMENSION ZETA(3),ETA(3)
cx    CXI=COS(DGRIDH*(XI-HGRIDX)/RRTHNM)
cx    SXI=SIN(DGRIDH*(XI-HGRIDX)/RRTHNM)
cx    SYJ=SIN(DGRIDH*(YJ-HGRIDY)/RRTHNM)
cx    CYJ=COS(DGRIDH*(YJ-HGRIDY)/RRTHNM)
cx    ETA(1)=CXI*CYJ
cx    ETA(2)=SXI
cx    ETA(3)=CXI*SYJ
cx    DO 20 I=1,3
cx    ZETA(I)=0.
cx    DO 20 J=1,3
cx    ZETA(I)=ZETA(I) + A(J,I)*ETA(J)
cx 20 CONTINUE
cx    R=SQRT(ZETA(1)*ZETA(1) + ZETA(2)*ZETA(2))
cx    XLAT=ATAN2(ZETA(3),R)/RADPDG
cx    IF(R.LE.0.) GO TO 40
cx    XLONG=ATAN2(ZETA(1),ZETA(2))/RADPDG
cx    RETURN
cx 40 XLONG=0.
cx    RETURN
cx    END
C***********************************************************************
      SUBROUTINE SETUP(P1,P2,P3,P4,P5,P6,P7,P8,P)
      DIMENSION P(166)
C P1 THRU P8 ARE ARE 8 PRIMARY PREDICTORS WHERE...
C      P1 IS INITIAL LATITUDE  (DEGS)
C      P2 IS INITIAL LONGITUDE (DEGS)
C      P3 IS JULIAN DAY NUMBER FUNCTION (O TO 1.00)
C      P4 IS MERIDIONAL DISPLACEMENT 00 TO -12H (NMI)
C      P5 IS ZONAL DISPLACEMENT 00 TO -12H (NMI)
C      P6 IS MERIDIONAL DISPLACEMENT 00 TO -24H (NMI)
C      P7 IS ZONAL DISPLACEMENT 00 TO -24H (NMI)
C      P8 IS MAXIMUM WIND (KNOTS)
C
C P(001 AND 002) ARE DUMMY VARIABLES AND ARE NOT FURTHER USED.
      DUMMY=9999.
      P(001)=DUMMY
      P(002)=DUMMY
C P(003)THRU P(166) ARE ALL POSSIBLE PREDICTORS AS OBTAINED FROM CUBIC
C POLYNOMIAL EXPANSION OF ORIGINAL 8 BASIC PREDICTORS P1 THRU P8.
C LIST THE PREDICTORS................
      P(003)=P8
      P(004)=P8*P8
      P(005)=P8*P8*P8
      P(006)=P7
      P(007)=P7*P8
      P(008)=P7*P8*P8
      P(009)=P7*P7
      P(010)=P7*P7*P8
      P(011)=P7*P7*P7
      P(012)=P6
      P(013)=P6*P8
      P(014)=P6*P8*P8
      P(015)=P6*P7
      P(016)=P6*P7*P8
      P(017)=P6*P7*P7
      P(018)=P6*P6
      P(019)=P6*P6*P8
      P(020)=P6*P6*P7
      P(021)=P6*P6*P6
      P(022)=P5
      P(023)=P5*P8
      P(024)=P5*P8*P8
      P(025)=P5*P7
      P(026)=P5*P7*P8
      P(027)=P5*P7*P7
      P(028)=P5*P6
      P(029)=P5*P6*P8
      P(030)=P5*P6*P7
      P(031)=P5*P6*P6
      P(032)=P5*P5
      P(033)=P5*P5*P8
      P(034)=P5*P5*P7
      P(035)=P5*P5*P6
      P(036)=P5*P5*P5
      P(037)=P4
      P(038)=P4*P8
      P(039)=P4*P8*P8
      P(040)=P4*P7
      P(041)=P4*P7*P8
      P(042)=P4*P7*P7
      P(043)=P4*P6
      P(044)=P4*P6*P8
      P(045)=P4*P6*P7
      P(046)=P4*P6*P6
      P(047)=P4*P5
      P(048)=P4*P5*P8
      P(049)=P4*P5*P7
      P(050)=P4*P5*P6
      P(051)=P4*P5*P5
      P(052)=P4*P4
      P(053)=P4*P4*P8
      P(054)=P4*P4*P7
      P(055)=P4*P4*P6
      P(056)=P4*P4*P5
      P(057)=P4*P4*P4
      P(058)=P3
      P(059)=P3*P8
      P(060)=P3*P8*P8
      P(061)=P3*P7
      P(062)=P3*P7*P8
      P(063)=P3*P7*P7
      P(064)=P3*P6
      P(065)=P3*P6*P8
      P(066)=P3*P6*P7
      P(067)=P3*P6*P6
      P(068)=P3*P5
      P(069)=P3*P5*P8
      P(070)=P3*P5*P7
      P(071)=P3*P5*P6
      P(072)=P3*P5*P5
      P(073)=P3*P4
      P(074)=P3*P4*P8
      P(075)=P3*P4*P7
      P(076)=P3*P4*P6
      P(077)=P3*P4*P5
      P(078)=P3*P4*P4
      P(079)=P3*P3
      P(080)=P3*P3*P8
      P(081)=P3*P3*P7
      P(082)=P3*P3*P6
      P(083)=P3*P3*P5
      P(084)=P3*P3*P4
      P(085)=P3*P3*P3
      P(086)=P2
      P(087)=P2*P8
      P(088)=P2*P8*P8
      P(089)=P2*P7
      P(090)=P2*P7*P8
      P(091)=P2*P7*P7
      P(092)=P2*P6
      P(093)=P2*P6*P8
      P(094)=P2*P6*P7
      P(095)=P2*P6*P6
      P(096)=P2*P5
      P(097)=P2*P5*P8
      P(098)=P2*P5*P7
      P(099)=P2*P5*P6
      P(100)=P2*P5*P5
      P(101)=P2*P4
      P(102)=P2*P4*P8
      P(103)=P2*P4*P7
      P(104)=P2*P4*P6
      P(105)=P2*P4*P5
      P(106)=P2*P4*P4
      P(107)=P2*P3
      P(108)=P2*P3*P8
      P(109)=P2*P3*P7
      P(110)=P2*P3*P6
      P(111)=P2*P3*P5
      P(112)=P2*P3*P4
      P(113)=P2*P3*P3
      P(114)=P2*P2
      P(115)=P2*P2*P8
      P(116)=P2*P2*P7
      P(117)=P2*P2*P6
      P(118)=P2*P2*P5
      P(119)=P2*P2*P4
      P(120)=P2*P2*P3
      P(121)=P2*P2*P2
      P(122)=P1
      P(123)=P1*P8
      P(124)=P1*P8*P8
      P(125)=P1*P7
      P(126)=P1*P7*P8
      P(127)=P1*P7*P7
      P(128)=P1*P6
      P(129)=P1*P6*P8
      P(130)=P1*P6*P7
      P(131)=P1*P6*P6
      P(132)=P1*P5
      P(133)=P1*P5*P8
      P(134)=P1*P5*P7
      P(135)=P1*P5*P6
      P(136)=P1*P5*P5
      P(137)=P1*P4
      P(138)=P1*P4*P8
      P(139)=P1*P4*P7
      P(140)=P1*P4*P6
      P(141)=P1*P4*P5
      P(142)=P1*P4*P4
      P(143)=P1*P3
      P(144)=P1*P3*P8
      P(145)=P1*P3*P7
      P(146)=P1*P3*P6
      P(147)=P1*P3*P5
      P(148)=P1*P3*P4
      P(149)=P1*P3*P3
      P(150)=P1*P2
      P(151)=P1*P2*P8
      P(152)=P1*P2*P7
      P(153)=P1*P2*P6
      P(154)=P1*P2*P5
      P(155)=P1*P2*P4
      P(156)=P1*P2*P3
      P(157)=P1*P2*P2
      P(158)=P1*P1
      P(159)=P1*P1*P8
      P(160)=P1*P1*P7
      P(161)=P1*P1*P6
      P(162)=P1*P1*P5
      P(163)=P1*P1*P4
      P(164)=P1*P1*P3
      P(165)=P1*P1*P2
      P(166)=P1*P1*P1
      RETURN
      END
C***********************************************************************
      SUBROUTINE YX2LL(ALAT0,ALON0,DISP,CFCST)
C INCOMING ARGUMENTS:
C     ALAT0, ALON0...INITIAL STORM POSTION
C     DISP...........FORECAST MERIDIONAL & ZONAL DISPLACEMENTS IN NMI.
C RETURNED ARGUMENT:
C     CDISP..........FORECASTS IN TERMS OF LAT/LON
C
      REAL*4 DISP(12),CFCST(12)
      CALL STHGPR(ALAT0,F1(ALON0),360.,1.,0.,0.)
      DO 10 I=1,6
      CALL XY2LLH(DISP(2*I),DISP(2*I-1),CFCST(2*I-1),CFCST(2*I))
C NOTE: ABOVE SUBROUTINE RETURNS LONGITUDES WEST OF 180 AS NEGATIVE AND
C EAST OF 180 AS POSITIVE.  CONVERT ALL LONGITUDES TO EAST
      IF(CFCST(2*I).GE.0.AND.CFCST(2*I).LT.180.)CFCST(2*I)=360.-
     $CFCST(2*I)
      IF(CFCST(2*I).LT.0.)CFCST(2*I)=-CFCST(2*I)
   10 CONTINUE
      RETURN
      END
cx*********************************************************************
cx    FUNCTION NEWCYC(NOWCYC,N)
cxGIVEN CYCLE TIME NOWCYC, GET NEW CYCLE TIME (NEWCYC) GIVEN BY
cxNOWCYC + N HOURS.  LIMIT 0F N IS + OR - 744 HOURS.  ALLOWANCES
cxARE MADE FOR LEAP YEARS.
cx(C.J.NEUMANN, SAIC, OCTOBER, 1989)
cx    CHARACTER*8 ALFA
cx    INTEGER NHEM(15),NOLEAP(15),ADDYR
cx    DATA NOLEAP /000,744,1488,2160,2904,3624,4368,5088,5832,6576,7296,
cx   $8040,8760,9504,10248/
cxABOVE DATA STATEMENT GIVES NUMBER OF HOURS FOR NON-LEAP YEAR MONTHS
cxMONTHS 0000UTC ON 1 DEC THRU 0000UTC ON 1 FEB OF SECOND YEAR.
cx
cxOBTAIN YEAR (KYR),MONTH (M0),DAY (KDA) AND HOUR (JTM) IN INTEGER FORMAT
cx    WRITE(ALFA,'(I8)')NOWCYC
cx    READ(ALFA,'(4I2)')KYR,MO,KDA,JTM
cx    DO 10 I=1,15
cx 10 NHEM(I)=NOLEAP(I)
cxIS THIS A LEAP YEAR? (YEAR 2000 IS A LEAP YEAR)
cx    IF(MOD(KYR,4).EQ.0)THEN
cx    DO 20 I=4,15
cx 20 NHEM(I)=NHEM(I)+24
cx    ENDIF
cxHOW MANY HRS FROM BEGINNING OF TIME WINDOW AT 0000UTC, 1 DEC (NHROLD)?
cx    NHROLD=NHEM(MO+1)+(KDA-1)*24+JTM
cxHOW MANY HRS NEEDED FROM BEGINNING OF WINDOW (NHRNEW)?
cx    NHRNEW=NHROLD+N
cx
cx    DO 30 MO=2,15
cxMO = 2 = PREVIOUS YEAR; M0 = 15 = NEXT YEAR; DO WE NEED TO ADD OR
cxSUBTRACT A YEAR??
cx    KYRNEW=KYR-(2/MO)+MO/15
cxCHANGE OF CENTURY?
cx    IF(KYRNEW.EQ.100)KYRNEW=0
cx    IF(KYRNEW.EQ.-1)KYRNEW=99
cx
cx    IF(NHRNEW.LT.NHEM(MO))GOTO 40
cx 30 CONTINUE
cx 40 NDIF=NHRNEW-NHEM(MO-1)
cx    LDA=(NDIF+24)/24
cx    LTM=NDIF+24-(LDA*24)
cx    INDEX=MOD(MO-3,12)+(2/MO)*12+1
cx    NEWCYC=KYRNEW*1000000+INDEX*10000+LDA*100+LTM
cx    RETURN
cx    END
cx*******************************************************************8
cx    SUBROUTINE LL2DB(XLATO,XLONO,XLATT,XLONT,DIST,BEAR)
cx     ALBION D. TAYLOR MARCH 18, 1981
cx    DATA RRTHNM/3 440.17/,RADPDG/1.745 3293 E-2/
cx  RRTHNM=RADIUS OF EARTH IN NAUT. MILES, RADPDG==OF RADIANS
cx  PER DEGREE
cx---------------------------------------------------------------------*
cx GIVEN AN ORIGIN AT LATITUDE, LONGITUDE=XLATO,XLONO, WILL LOCATE     *
cx A TARGET POINT AT LATITUDE, LONGITUDE = XLATT, XLONT.  RETURNS      *
cx DISTANCE DIST IN NAUTICAL MILES, AND BEARING BEAR (DEGREES CLOCKWISE*
cx FROM NORTH).                                                        *
cx                                                                     *
cx ALL LATITUDES ARE IN DEGREES, NORTH POSITIVE AND SOUTH NEGATIVE.    *
cx ALL LONGITUDES ARE IN DEGREES, WEST POSITIVE AND EAST NEGATIVE.     *
cx                                                                     *
cx NOTE-- WHEN ORIGIN IS AT NORTH OR SOUTH POLE, BEARING IS NO LONGER  *
cx MEASURED FROM NORTH.  INSTEAD, BEARING IS MEASURED CLOCKWISE        *
cx FROM THE LONGITUDE OPPOSITE THAT SPECIFIED IN XLONO.                *
cx EXAMPLE-- IF XLATO=90., XLONO=80., THE OPPOSITE LONGITUDE IS -100.  *
cx (100 EAST), AND A TARGET AT BEARING 30. WILL LIE ON THE -70.        *
cx (70 EAST) MERIDIAN                                                  *
cx---------------------------------------------------------------------*
cx    CLATO=COS(RADPDG*XLATO)
cx    SLATO=SIN(RADPDG*XLATO)
cx    CLATT=COS(RADPDG*XLATT)
cx    SLATT=SIN(RADPDG*XLATT)
cx    CDLON=COS(RADPDG*(XLONT-XLONO))
cx    SDLON=SIN(RADPDG*(XLONT-XLONO))
cx    Z=SLATT*SLATO + CLATT*CLATO*CDLON
cx    Y= - CLATT*SDLON
cx    X=CLATO*SLATT - SLATO*CLATT*CDLON
cx    R=SQRT(X*X+Y*Y)
cx    DIST=RRTHNM*ATAN2(R,Z)
cx    IF (R.LE.0.) GO TO 20
cx    BEAR=ATAN2(-Y,-X)/RADPDG + 180.
cx    RETURN
cx 20 BEAR=0.
cx    RETURN
cx    END
C***********************************************************************
      BLOCK DATA BLKSW1
C
C ENTER ALL CONSTANTS NEEDED BY SWPCPR PROGRAM......
C
      INTEGER*2
     $       N12M(31),N24M(31),N36M(31),N48M(31),N60M(31),N72M(31)
      INTEGER*2
     $       N12Z(31),N24Z(31),N36Z(31),N48Z(31),N60Z(31),N72Z(31)
      REAL*4 R12M(31),R24M(31),R36M(31),R48M(31),R60M(31),R72M(31)
      REAL*4 R12Z(31),R24Z(31),R36Z(31),R48Z(31),R60Z(31),R72Z(31)
      COMMON/BLOCKSW1/RCM(31,6),RCZ(31,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(31,6),NPZ(31,6)
      COMMON/BLOCKSW2/NPM,NPZ
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
     A-.4287692E+1, .2818728E+0, .1531582E+1,-.1054133E+0,-.2186656E-6,
     B-.4755538E-5, .8606674E-4, .3035332E-5, .1681255E+1,-.4292762E-2,
     C .5451203E-1,-.1388062E-3,-.1671499E-1, .9399905E-5,-.3655966E-4,
     D-.2632264E-4,-.7627359E-5, .4124779E-4, .3702111E-5,-.2835288E-5,
     E .1992647E-5, .4542270E-5,-.6337432E-6, .4555284E-5, .3172314E-5,
     F .3638802E-5,-.1500442E-5,-.5920183E-6, .7568453E-3, .1066462E-5,
     G .4031802E-6/
C
C  12HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N12M/
     A         037,         022,         012,         006,         091,
     B         035,         138,         049,         086,         114,
     C         101,         119,         092,         024,         126,
     D         149,         097,         117,         098,         100,
     E         130,         053,         031,         135,         008,
     F         146,         044,         115,         023,         108,
     G         050/
C
C  24HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R24M/
     A .7219834E-1,-.1812531E-2, .7759157E-4,-.9043463E-4, .1739864E-4,
     B .1723866E-3, .7950909E+1,-.2112079E-1,-.5877865E-5, .1316165E-4,
     C .3130879E-5,-.4076088E-5,-.1727260E+0, .5040320E+0, .5304649E-4,
     D-.1710418E-5,-.5500862E-4, .1253498E-6,-.1005590E-4, .1066905E-4,
     E .3660225E-5,-.1280670E-4, .2636333E+1,-.6546882E-5, .2211754E-4,
     F-.6047287E-4,-.1062746E-5, .7228092E-5,-.1749418E-3,-.5311209E+1,
     G-.3094506E-1/
C
C  24HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N24M/
     A         101,         023,         117,         126,         098,
     B         138,         086,         114,         035,         044,
     C         049,         091,         006,         022,         024,
     D         108,         135,         031,         100,         130,
     E         050,         053,         012,         008,         146,
     F         149,         115,         097,         119,         037,
     G         092/
C
C  36HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R36M/
     A .2131797E+0, .3706641E-4,-.1148131E-3,-.7029843E-1, .2650750E-4,
     B-.2310212E-4,-.1134127E-4, .1301733E+2,-.3398344E-1,-.1323961E-3,
     C .1777998E-3,-.4517950E-4, .7406342E+0, .1785662E-3, .2774475E-5,
     D-.2095038E-3, .1041766E-4, .5252792E-4,-.2006225E+0, .1877635E-3,
     E .6052240E+1,-.1077771E-1,-.1248108E-4, .4368852E-4, .2081658E-5,
     F .6929379E-4,-.5172233E-5,-.5611676E-3,-.1740277E+2,-.1233750E-4,
     G .3141744E-6/
C
C  36HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N36M/
     A         101,         097,         126,         092,         044,
     B         100,         035,         086,         114,         146,
     C         024,         008,         022,         138,         049,
     D         135,         050,         130,         006,         117,
     E         012,         023,         091,         098,         031,
     F         149,         108,         119,         037,         053,
     G         115/
C
C  48HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R48M/
     A-.1940412E-3, .3338362E-3, .1097468E-3,-.1320773E-3,-.7788396E-4,
     B-.4567575E-3,-.7994210E-4, .1468041E-4,-.4807591E-3, .4225687E-3,
     C-.2674650E-4, .9120648E-1,-.7511978E+1, .1880544E+2,-.4807551E-1,
     D .2930958E-3, .1312998E-4,-.3291533E-4, .1135152E-3, .1010927E-3,
     E .1262370E+1,-.1412983E-3,-.3165654E+0,-.2127615E-1, .4765577E-4,
     F .3932788E-1,-.2653732E-4, .9419601E-5,-.1224863E-4,-.2948578E+1,
     G .1947467E-5/
C
C  48HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N48M/
     A         119,         024,         053,         117,         008,
     B         135,         100,         031,         146,         149,
     C         035,         101,         037,         086,         114,
     D         138,         049,         091,         098,         130,
     E         022,         126,         006,         023,         097,
     F         092,         044,         050,         108,         012,
     G         115/
C
C  60HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R60M/
     A .1298005E-3, .4760712E-3,-.1217524E-3,-.8984325E-3,-.5744392E-3,
     B .1767888E-4,-.2822072E-4, .1014145E-3, .3170690E+2,-.8314960E-1,
     C-.4256153E-1,-.1177597E-3,-.3051235E-4, .8623369E-3, .1486915E-4,
     D .2637512E-4,-.4279953E-4, .1489218E-3, .1845038E-4,-.2632877E-3,
     E .1094307E+1, .8520777E-4,-.2106894E+0, .6038574E+1,-.1174886E-1,
     F-.2752771E-3,-.9248588E+1, .1021008E+0, .7847991E-4,-.6819550E-5,
     G-.2707957E-5/
C
C  60HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N60M/
     A         119,         024,         008,         146,         135,
     B         050,         108,         053,         086,         114,
     C         101,         100,         035,         149,         115,
     D         049,         091,         098,         031,         126,
     E         022,         130,         006,         037,         023,
     F         117,         012,         092,         138,         044,
     G         097/
C
C  72HR MERIDIONAL REGRESSION COEFFICIENTS
      DATA R72M/
     A .4869786E-3, .3139089E-4, .6226165E-3,-.1284850E-4, .1587036E-4,
     B-.1146980E-2,-.1792561E-3, .1090566E-2, .2936242E-4, .5015800E+2,
     C-.1335983E+0,-.1820270E+0,-.4730774E-3, .4767377E-4,-.3725974E-4,
     D-.1635298E-3, .2128050E-4,-.4045876E-4, .1044304E+1,-.1153728E-3,
     E-.2409394E+0,-.1702508E-3,-.1031337E-3,-.3930025E-4, .1297369E-3,
     F .6035300E-4,-.3732730E-3,-.1336571E+2, .1430393E+0, .1969062E+2,
     G .3655747E-2/
C
C  72HR MERIDIONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N72M/
     A         119,         115,         024,         130,         050,
     B         146,         008,         149,         044,         086,
     C         114,         101,         135,         049,         035,
     D         126,         031,         108,         022,         097,
     E         006,         138,         100,         091,         098,
     F         053,         117,         012,         092,         037,
     G         023/
C
C    12 THROUGH 72HR MERIDIONAL INTERCEPT VALUES
      DATA CNSTM/
     $-.14864E+3,-.69449E+3,-.11465E+4,-.16752E+4,-.28095E+4,-.44417E+4/
C
C  12HR ZONAL REGRESSION COEFFICIENTS
      DATA R12Z/
     A .8272212E+0,-.2821487E-1, .2188856E-4, .4904044E-4,-.1186432E-4,
     B .1891602E-4,-.1009734E-4, .4801687E-5, .3034516E-5,-.5680390E-1,
     C-.3707809E-6, .6521890E-5,-.9741484E-5, .1659947E-5,-.2275189E-5,
     D-.1905439E-4, .2371689E-2, .5194635E-4,-.2329734E-4,-.8382909E-3,
     E-.9148710E-2, .1659897E-4, .1048122E-3,-.1188157E-5, .6002806E-4,
     F-.8836303E-6,-.7455742E-5, .1938524E-6, .2163060E-6,-.6700967E-5,
     G-.7487800E-5/
C
C  12HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N12Z/
     A         022,         006,         076,         157,         054,
     B         056,         036,         034,         095,         012,
     C         021,         060,         067,         072,         121,
     D         142,         096,         069,         062,         089,
     E         150,         151,         165,         131,         009,
     F         010,         147,         019,         055,         144,
     G         163/
C
C  24HR ZONAL REGRESSION COEFFICIENTS
      DATA R24Z/
     A .2063707E+1,-.3357145E+0, .6836551E-5,-.3129525E-4, .1856783E-4,
     B-.1074454E-4,-.2365235E-4,-.1482711E+0,-.2725321E-4, .4400867E-4,
     C .1380769E-4,-.1281273E-3, .5862035E-4, .2064152E-3, .1986785E-2,
     D .4822288E-5, .9806713E-4,-.5071852E-4, .2002428E-5,-.8195533E-5,
     E-.2190036E-1, .1748470E-3,-.8485891E-4,-.9325183E-5, .1603337E-4,
     F-.2997504E-4,-.5949957E-4,-.7062224E-5,-.1847495E-3, .4589968E-7,
     G .3837156E-5/
C
C  24HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N24Z/
     A         022,         006,         095,         036,         072,
     B         055,         151,         012,         054,         056,
     C         034,         009,         144,         157,         096,
     D         019,         076,         067,         021,         121,
     E         150,         069,         062,         131,         060,
     F         147,         165,         142,         089,         010,
     G         163/
C
C  36HR ZONAL REGRESSION COEFFICIENTS
      DATA R36Z/
     A .2340691E-1,-.1054184E-1, .1140256E-4,-.5274031E-4, .1013532E-3,
     B .2381868E-3,-.3183674E-3,-.2538885E+0, .1124281E+1,-.3209144E-4,
     C .4905052E-4, .2290086E-4, .1203770E-4, .4073604E-5,-.9930932E-4,
     D .1722713E-3,-.2246730E-4,-.6333156E-3, .3771087E-4,-.5791333E-2,
     E-.1334337E-3, .2565115E-3,-.2889898E-4, .7081124E-4,-.8817424E-4,
     F .4131816E-4,-.8401021E-5, .2172888E-3, .1402107E-5,-.4444249E+0,
     G-.2584016E-5/
C
C  36HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N36Z/
     A         096,         089,         019,         036,         147,
     B         144,         165,         012,         006,         054,
     C         056,         034,         095,         021,         067,
     D         076,         055,         009,         072,         150,
     E         062,         069,         131,         142,         151,
     F         060,         121,         157,         010,         022,
     G         163/
C
C  48HR ZONAL REGRESSION COEFFICIENTS
      DATA R48Z/
     A .3610687E-1,-.1597900E-1, .4438812E-3,-.6364309E-4, .6768669E-5,
     B .3598207E-5,-.1276235E-2, .1692604E-3,-.1460915E-3, .1745373E-4,
     C .2265086E-3,-.2481118E+0,-.2989547E-4, .1720388E+1, .6090402E-4,
     D .2222404E-3, .2627062E-4,-.2712250E-4, .9088231E-4, .3761448E-4,
     E-.1995767E-3, .3809168E-3, .1210026E-3,-.1633291E+1,-.2673949E-3,
     F .6886311E-5,-.1157471E-3,-.7659700E-5,-.1022189E-2, .3323501E-5,
     G .2123853E-1/
C
C  48HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N48Z/
     A         096,         089,         144,         036,         131,
     B         021,         009,         147,         067,         095,
     C         076,         012,         055,         006,         072,
     D         157,         034,         054,         060,         056,
     E         062,         069,         142,         022,         163,
     F         019,         151,         121,         165,         010,
     G         150/
C
C  60HR ZONAL REGRESSION COEFFICIENTS
      DATA R60Z/
     A .3987733E-1,-.1704373E-1, .6661806E-3,-.1728967E-2,-.2469190E-4,
     B-.1376384E-3,-.2298098E-3, .9537430E-5, .9021796E-4, .6723615E-5,
     C-.9040680E-4, .4407617E-4, .1661725E-3, .2571493E-4, .1737037E+1,
     D .5629304E-3,-.2817416E-3, .1294186E+0, .1610824E-3,-.1702458E-3,
     E-.2705557E+0,-.4644499E-4, .2272446E-3,-.1372048E-2,-.2055748E+1,
     F-.2734174E-3, .5830324E-4,-.2907653E-4, .6683014E-4, .1259299E-5,
     G-.5199808E-6/
C
C  60HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N60Z/
     A         096,         089,         144,         009,         131,
     B         067,         163,         121,         072,         021,
     C         036,         034,         076,         095,         006,
     D         069,         062,         150,         060,         151,
     E         012,         055,         142,         165,         022,
     F         157,         056,         054,         147,         019,
     G         010/
C
C  72HR ZONAL REGRESSION COEFFICIENTS
      DATA R72Z/
     A-.2664871E+1, .2910618E-3, .1909511E+1,-.9914097E-5, .2680403E+0,
     B .7465051E-3,-.3595912E-3, .4981306E-3,-.6412225E-4,-.7438001E-5,
     C .3070849E-4, .9225095E-4,-.4781626E+0, .3906929E-4,-.1123542E-2,
     D-.1598617E-2,-.2515303E-3, .4130599E-1,-.1780620E-1,-.6823870E-4,
     E .3523589E-4, .5590919E-4,-.6953179E-3, .1265137E-4,-.5831036E-4,
     F-.2138516E-4,-.1483777E-3, .6939810E-3, .5264840E-3, .8924841E-6,
     G-.7022630E-5/
C
C  72HR ZONAL PREDICTOR NUMBERS ASSOCIATED WITH ABOVE COEFFICIENTS
      DATA N72Z/
     A         022,         060,         006,         010,         150,
     B         069,         062,         142,         055,         076,
     C         095,         072,         012,         121,         157,
     D         009,         151,         096,         089,         036,
     E         034,         056,         165,         021,         067,
     F         054,         131,         163,         144,         019,
     G         147/
C
C    12 THROUGH 72HR ZONAL INTERCEPT VALUES
      DATA CNSTZ/
     $ .10063E+2, .24147E+2, .14084E+2,-.12586E+2,-.11908E+3,-.24339E+3/
      END
C***********************************************************************
      SUBROUTINE UPRCAS(EORW00,EORW12,EORW24)
      CHARACTER*1 EORW00,EORW12,EORW24
C ASSURE THAT 'E' OR 'W' IS IN UPPER CASE
      IF(EORW00.EQ.'e')EORW00='E'
      IF(EORW12.EQ.'e')EORW12='E'
      IF(EORW24.EQ.'e')EORW24='E'
      IF(EORW00.EQ.'w')EORW00='W'
      IF(EORW12.EQ.'w')EORW12='W'
      IF(EORW24.EQ.'w')EORW24='W'
      RETURN
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


      subroutine oclip(nsind,ymdh,flt,fln,plt12,pln12,plt24,pln24)
      common/oldclpfcst/ cfcst(12)

C         
C         flt is always positive
C         fln is always deg E
C

      real p(35),dx(6),dy(6)

      integer ymdh

      iyr  = ymdh/1000000
      mon  = ymdh/10000 - iyr*100
      iday = ymdh/100   - mon*100  - iyr*10000
      ihr  = ymdh       - iday*100 - mon*10000 - iyr*1000000

      if(nsind.lt.0) then
        flat=-flt
      else
        flat=flt
      endif


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
C         CALCULATE FORECAST FOR SOUTHERN HEMISPHERE
C         (NOTE, 60-HR FORECAST IS NOT INCLUDED FOR SW INDIA
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

      cfcst(1)=flt12
      cfcst(2)=fln12
      cfcst(3)=flt24
      cfcst(4)=fln24
      cfcst(5)=flt36
      cfcst(6)=fln36
      cfcst(7)=flt48
      cfcst(8)=fln48
      cfcst(9)=flt60
      cfcst(10)=fln60
      cfcst(11)=flt72
      cfcst(12)=fln72


      return
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
