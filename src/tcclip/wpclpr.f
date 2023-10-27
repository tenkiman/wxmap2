C***********************************************************************
      SUBROUTINE WPCLPR(IDATIM,ALAT00,ALON00,ALAT12,ALON12,ALAT24,
     $     ALON24,WIND,CNMIS,CLALO,P1TOP8)

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
      COMMON/BLOCK1/RCM(90,6),RCZ(95,6),CNSTM(6),CNSTZ(6)
      INTEGER*2 NPM(90,6),NPZ(95,6)
      COMMON/BLOCK2/NPM,NPZ
      REAL*4 P(166),CNMIS(12),CLALO(12),P1TOP8(8)
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
      CALL NMI2LL(ALAT00,ALON00,CNMIS,CLALO)
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
      SUBROUTINE NMI2LL(ALAT0,ALON0,CNMIS,CLALO)
C INCOMING ARGUMENTS:
C     ALAT0, ALON0...INITIAL STORM POSTION
C     CNMIS...........FORECAST MERIDIONAL & ZONAL DISPLACEMENTS IN NMI.
C RETURNED ARGUMENT:
C     CLALO..........FORECASTS IN TERMS OF LAT/LON (SEE NOTE, BELOW)
C
      REAL*4 CNMIS(12),CLALO(12)
      CALL STHGPR(ALAT0,F1(ALON0),360.,1.,0.,0.)
      DO 10 I=1,6
      CALL XY2LLH(CNMIS(2*I),CNMIS(2*I-1),CLALO(2*I-1),CLALO(2*I))
C NOTE: ABOVE SUBROUTINE RETURNS LONGITUDES WEST OF 180 AS NEGATIVE AND
C EAST OF 180 AS POSITIVE.  CONVERT ALL LONGITUDES TO WHERE EAST IS POSITIVE
C ZERO TO 180 AND WEST IS POSITIVE 180 TO 360 DEGS. 
      IF(CLALO(2*I).GE.0.AND.CLALO(2*I).LT.180.)CLALO(2*I)=360.-
     $CLALO(2*I)
      IF(CLALO(2*I).LT.0.)CLALO(2*I)=-CLALO(2*I)
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
