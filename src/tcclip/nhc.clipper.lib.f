c*********************************************************************
        FUNCTION LASTCH (STRING)
C
C**     RETURNS THE POSITION OF THE LAST NON-BLANK CHARACTER OF A
C**             STRING
C
        CHARACTER*(*) STRING
C
        LAST = LEN(STRING)
C
        DO 10 I = LAST,1,-1
        IF (STRING(I:LAST).NE.' ') GO TO 20
   10   CONTINUE
C
        LASTCH = 0
        RETURN
C
   20   LASTCH = I
        RETURN
C
        END
c********************************************************************
      SUBROUTINE XTRAP ( iymdh, latcur, loncur, latm12, lonm12, STRMID )
C
C**   EXTRAPOLATION FORECAST USING THE PAST 12 HOUR MOTION
C
      common /extrap/ ifpxtrp( 11, 3 )
c
      DIMENSION FPXTRP( 10, 2 )
C
      REAL latcur, loncur, latm12, lonm12
C
      CHARACTER*1 EW
      CHARACTER*3 FTIME(10)
      CHARACTER*8 STRMID
C
      DATA FTIME / ' 12', ' 24', ' 36', ' 48', ' 60', 
     &             ' 72', ' 84', ' 96', '108', '120' /
C
C**   WRITE THE INPUT PARAMETER TO THE PRINTER
C
      WRITE ( *, '('' EXTRAPOLATION FORECAST'',/)' )
      WRITE ( *, '('' INPUT PARAMETERS FOR TROPICAL CYCLONE '', A,
     &             '' ON YMDH = '', I10.10, / )' ) STRMID, iymdh
      WRITE ( *, '('' LATCUR   = '', F5.1, '' N  LONCUR   = '', F6.1,
     &             '' W  LATM12 = '', F5.1, '' N  LONM12 = '', F6.1,
     &             '' W'',/)') latcur, loncur, latm12, lonm12
C
      call rhdst ( latm12, lonm12, latcur, loncur, dir, dst )
c
      call rltlg ( latcur, loncur, fpxtrp(1,1), fpxtrp(1,2),
     &             dir, dst*1.0 )
      call rltlg ( latcur, loncur, fpxtrp(2,1), fpxtrp(2,2), 
     &             dir, dst*2.0 )
      call rltlg ( latcur, loncur, fpxtrp(3,1), fpxtrp(3,2), 
     &             dir, dst*3.0 )
      call rltlg ( latcur, loncur, fpxtrp(4,1), fpxtrp(4,2), 
     &             dir, dst*4.0 )
      call rltlg ( latcur, loncur, fpxtrp(5,1), fpxtrp(5,2), 
     &             dir, dst*5.0 )
      call rltlg ( latcur, loncur, fpxtrp(6,1), fpxtrp(6,2), 
     &             dir, dst*6.0 )
      call rltlg ( latcur, loncur, fpxtrp(7,1), fpxtrp(7,2), 
     &             dir, dst*7.0 )
      call rltlg ( latcur, loncur, fpxtrp(8,1), fpxtrp(8,2), 
     &             dir, dst*8.0 )
      call rltlg ( latcur, loncur, fpxtrp(9,1), fpxtrp(9,2), 
     &             dir, dst*9.0 )
      call rltlg ( latcur, loncur, fpxtrp(10,1), fpxtrp(10,2), 
     &             dir, dst*10.0 )
c
      WRITE ( *, '( '' FORECAST POSITIONS'', / )' )
C
      WRITE ( *, '( ''  00 HR = '', F5.1, '' N '' ,F6.1, '' W'' )' )
     &       latcur, loncur
C
      do i = 1, 10
c
c**   Form the integer values for the adeck
c
         ifpxtrp( i + 1, 1 ) = int( fpxtrp( i, 1 )*10.0 + 0.5 )
         ifpxtrp( i + 1, 2 ) = int( fpxtrp( i, 2 )*10.0 + 0.5 )
C
c**   Write out the forecast for the correct hemisphere
c
         EW = 'W'
         FPRITE = ABS( FPXTRP(i,2) )
C
         IF ( FPXTRP(i,2) .LT. 0.0 ) THEN
            EW = 'E'
            FPXTRP(i,2) = 360.0 + FPXTRP(i,2)
         ELSEIF ( FPXTRP(i,2) .GT. 180.0 ) THEN
            EW = 'E'
            FPRITE = 360.0 - FPRITE
         ENDIF
C
         WRITE ( *, '( 1X, A, '' HR = '', F5.1, '' N '', F6.1, 1X, A )')
     &                FTIME(i), FPXTRP(i,1), FPRITE, EW
c
      enddo   
c
      RETURN
      END
C***********************************************************************
      SUBROUTINE RHDST ( FLAT, FLNG, TLAT, TLNG, DIR, DST )
C
C**   THIS IS A "GHDST" SUBROUTINE; FROM POINT (FLAT,FLNG) TO POINT
C**     (TLAT,TLNG) FINDS THE DIRECTION (DIR) AND DISTANCE (DST) IN NM
C**     DIRECTION IS CALCULATED ACCORDING TO RHUMB-LINE DIRECTION.
C
      DIR = 0.0
      DST = 0.0
C
      RNUM  = (FLNG - TLNG)*3.1415926535898/180.0
      TD1   = TAN((45.0 + (0.5*TLAT))*3.1415926535898/180.0)
      TD2   = TAN((45.0 + (0.5*FLAT))*3.1415926535898/180.0)
      RLTD1 = ALOG(TD1)
      RLTD2 = ALOG(TD2)
      DENOM = RLTD1 - RLTD2
      RMAG  = (RNUM*RNUM) + (DENOM*DENOM)
C
      IF (RMAG.NE.0.0) DIR = ATAN2(RNUM,DENOM)*180.0/3.1415926535898
      IF (DIR .LE.0.0) DIR = 360.0 + DIR
C
      DST  = 60.0*ABS(FLAT - TLAT)/ABS(COS(DIR*3.1415926535898/180.0))
      ICRS = DIR + 0.5
      IF (ICRS.EQ.90.OR.ICRS.EQ.270) DST = 60.0*ABS(FLNG - TLNG)*
     & COS(FLAT*3.1415926535898/180.0)
C
      DIR  = FLOAT(ICRS)
      ICRS = DST*10.0 + 0.5
      DST  = FLOAT(ICRS)/10.0
C
      RETURN
      END
C*******************************************************************
      SUBROUTINE RLTLG ( FLAT, FLNG, TLAT, TLNG, DIR, DST )
C
C**   THIS IS A "GLTLG" SUBROUTINE; FROM POINT (FLAT,FLNG) AND DIR,DST
C**       FINDS THE END POINT (TLAT,TLNG)
C**       DIRECTION IS THE RHUMB-LINE DIRECTION.
C
      TLAT = 0.0
      TLNG = 0.0
C
      ICRS = DIR
      IF (ICRS.EQ.90.OR.ICRS.EQ.270) GO TO 10
C
      CRPD = DIR*3.1415926535898/180.0
      TLAT = FLAT + (DST*COS(CRPD)/60.0)
      IF (TLAT.GT.89.0) TLAT = 89.0
      IF (TLAT.LT.-89.0) TLAT = -89.0
C
      TD1   = TAN((45.0 + (0.5*TLAT))*3.1415926535898/180.0)
      TD2   = TAN((45.0 + (0.5*FLAT))*3.1415926535898/180.0)
      RLTD1 = ALOG(TD1)
      RLTD2 = ALOG(TD2)
      DENOM = RLTD1 - RLTD2
      TLNG  = FLNG - ((TAN(CRPD)*DENOM)*180.0/3.1415926535898)
      GO TO 20
C
   10 DLON = DST/(60.0*COS(FLAT*3.1415926535898/180.0))
      IF (ICRS.EQ.90)  TLNG = FLNG - DLON
      IF (ICRS.EQ.270) TLNG = FLNG + DLON
      TLAT = FLAT
C
   20 ICRS = TLAT*10.0 + 0.5
      TLAT = FLOAT(ICRS)/10.0
      ICRS = TLNG*10.0 + 0.5
      TLNG = FLOAT(ICRS)/10.0
C
      RETURN
      END
c***************************************************************************
      SUBROUTINE ATCLIP ( iYMDH, Y, X, DNOW, SNOW,
     &     DM12, SM12, WKTS, STRMID)

C**   ATLANTIC CLIPER PROGRAM
C
C**   REFER TO NOAA TECHNICAL MEMORANDUM NWS SR-62 (C.J. NEUMANN,
C**   JAN 1972) FOR A DESCRIPTION OF CLIPER SYSTEM.
C
C
      common /cliper/ ifpclip(11,3),flat(7),flon(7)

      dimension fpclip(5,2)
c
      DIMENSION DISP(10),FULL(10),GULF(10),CNS(14,5),CEW(8,5),ND(12),
     1     P(14),XG(5),YG(5),XA(5),YA(5),FP(2,5)

      CHARACTER*1 EW
      CHARACTER*2 FTIME(5),myftime
      CHARACTER*8 STRMID
C
C**   LIST CONSTANTS FOR MERIDIONAL DISPLACEMENTS.
C
      DATA FTIME /'12','24','36','48','72'/
      DATA CNS/7.60553,13.59909,-2.575127,-.0001868914,.00460007,
     1.0022623,-.001491833,-.0002678624,-.00006994195,.00004407501,
     2-.0002049626,.00007781249,.1430621,-.00008156078,30.30846,
     322.91538,-2.484599,.004968631,.009297729,.02511378,-.007839641,
     4-.005977559,-.0003504201,.0001557468,-.0009956548,.0004778924,
     5.3879478,-.000671019,67.69324,31.94291,-3.697592,.009672852,
     6.009539232,.06322068,-.01332191,-.01610885,-.0007292257,
     7.0002341562,-.002814067,.001145255,.8940798,-.002181595,120.27143,
     838.94701,-4.380877,.01323013,.02292699,.09532129,-.01664333,
     9-.03200883,-.001216522,.000315372,-.005450743,.001867606,1.666658,
     1-.004353084,263.15653,48.41731,-4.456658,.01126704,.04297187,
     2.16962,-.01748416,-.06485724,-.002215515,.0003599106,-.012677,
     3.003690242,4.121246,-.01102184/
C
C**   LIST CONSTANTS FOR ZONAL DISPLACEMENTS.
C
      DATA CEW/-3.52591,13.69309,-2.637347,.8151257,.6867776,
     1-.002168753,-.000596625,.1247267,-13.12388,23.30256,-3.215529,
     23.584506,3.949364,-.007860247,-.006764091,.5135556,-28.48156,
     332.37355,-5.342858,8.073875,9.321241,-.01318171,-.02040824,
     41.044624,-44.13759,38.93667,-6.819777,14.10797,16.35476,
     5-.01967039,-.03853289,1.698018,-60.23074,46.26022,-8.8089,
     629.11625,32.91178,-.02181549,-.08553838,3.291178/
C
      DATA ND /0,31,59,90,120,151,181,212,243,273,304,334/
C
C**   WRITE THE INPUT PARAMETER TO THE PRINTER
C
      WRITE (*,'('' ATLANTIC CLIPER ''/)')
      WRITE (*,'('' INPUT PARAMETERS FOR TROPICAL CYCLONE '',A,
     & '' ON YMDH = '',I10.10,/)') STRMID,iYMDH
      WRITE (*,'('' LATCUR =  '',F4.1,''N  LONCUR = '',F5.1,
     &           ''W  DIRCUR = '',F4.0,'' DEG  SPDCUR = '',F3.0,
     &           '' KT'',/,'' WNDCUR = '',F4.0,'' KT'',18X,
     &           ''DIRM12 = '',F4.0,'' DEG  SPDM12 = '',F3.0,
     &           '' KT'',/)') Y, X, DNOW, SNOW, WKTS, DM12, SM12
C
C**   CHECK FOR STORM LOCATION AND DETERMINE WEIGHTING FACTORS
C
      WA = (X - Y - 61.0)/5.0
      WB = (Y - 13.0)/4.0
      IF (WA.GT.1.0) WA = 1.0
      IF (WA.LT.0.0) WA = 0.0
      IF (WB.GT.1.0) WB = 1.0
      IF (WB.LT.0.0) WB = 0.0
      WGULF = WA*WB
      WFULL = 1.0 - WGULF
C
C**   COMPUTE DAY NUMBER AND SUBTRACT OFF MEANS
C
      IY  = iYMDH/1000000
      MO  = iYMDH/10000 - IY*100
      KDA = iYMDH/100 - MO*100 - IY*10000
C
      DAN   = ND(MO) + KDA
      print*,'LLLLLLLLLLL dayn ',dan

      DANBR = ND(MO) + KDA - 248
      IF (DANBR.LT.-95.0) DANBR = -95.0
      IF (DANBR.GT. 82.0) DANBR =  82.0
C
      WMPH = (WKTS*1.15) - 71.0
      ALAT = Y - 24.0
      ALON = X - 68.0
C
C**   CONVERT PRESENT AND PAST MOTION TO U AND V COMPONENTS.
C
      T = 0.0174533
      UNOW = SIN(DNOW*T)*SNOW
      VNOW = COS(DNOW*T)*SNOW
      UM12 = SIN(DM12*T)*SM12
      VM12 = COS(DM12*T)*SM12
C
C**   CALL THE GULF OF MEXICO CORRECTIONS
C
      CALL CGULF (Y,X,UNOW,VNOW,UM12,VM12,DAN,WKTS,WGULF,GULF)
C
C**   SET UP MERIDIONAL PREDICTORS AND COMPUTE MERIDIONAL DISPLACEMENTS.
C
      P(1) = 1.0
      P(2) = VNOW
      P(3) = VM12
      P(4) = VNOW*VM12*VM12
      P(5) = WMPH*VM12
      P(6) = VNOW*WMPH
      P(7) = VNOW*VNOW*VM12
      P(8) = ALAT*ALAT*VNOW
      P(9) = DANBR*DANBR*VM12
      P(10) = VNOW*DANBR*DANBR
      P(11) = ALAT*ALAT*DANBR
      P(12) = WMPH*DANBR*VM12
      P(13) = UNOW
      P(14) = DANBR*DANBR
C
      DO 20 I = 1,5
      ZZ = 0.0
C
      DO 10 J = 1,14
      ZZ = ZZ + CNS(J,I)*P(J)
   10 CONTINUE
C
      FULL(2*I - 1) = ZZ
   20 CONTINUE
C
C**   SET UP ZONAL PREDICTORS AND COMPUTE ZONAL DISPLACEMENTS.
C
      P(2) = UNOW
      P(3) = UM12
      P(4) = ALAT
      P(5) = VNOW
      P(6) = VNOW*VNOW*UM12
      P(7) = ALAT*VNOW*UM12
      P(8) = ALON
C
      DO 40 I = 1,5
      ZZ = 0.0
C
      DO 30 J = 1,8
      ZZ = ZZ + CEW(J,I)*P(J)
   30 CONTINUE
C
C**   CHANGE SIGN TO DESIGNATE WESTWARD MOTION AS POSITIVE MOTION.
C
      FULL(2*I) = -ZZ
   40 CONTINUE
C
      DO 50 I = 1,10
      DISP(I) = GULF(I)*WGULF + FULL(I)*WFULL
   50 CONTINUE
C
      DO 60 I = 1,5
      YG(I) = GULF(2*I - 1)/60.0 + Y
      XG(I) = GULF(2*I)/COS((YG(I) + Y)*T/2.0)/60.0 + X
      IF (WGULF.EQ.0.0) YG(I) = -99.9
      IF (WGULF.EQ.0.0) XG(I) = -99.9
      YA(I) = FULL(2*I - 1)/60.0 + Y
      XA(I) = FULL(2*I)/COS((YA(I) + Y)*T/2.0)/60.0 + X
c
      FPCLIP(i,1) = DISP(2*I - 1)/60.0 + Y
      FPCLIP(i,2) = DISP(2*I)/COS((FPCLIP(i,1) + Y)*T/2.0)/60.0 + X
c
   60 CONTINUE
C
C**   WRITE ATLANTIC CLIPER POSITION FORECAST TO THE PRINTER
C
      WRITE (*,'('' FORECAST POSITIONS'',/)')
C         
      flat(1)=y
      flon(1)=x

      WRITE (*,'('' 00 HR = '',F5.1,'' N '',F6.1,'' W'')') Y,X
C
c**   Form the integer values for the adeck
c
      DO K = 1, 5
         ifpclip( k + 1, 1 ) = int ( fpclip( k, 1 )*10.0 + 0.5 )
         ifpclip( k + 1, 2 ) = int ( fpclip( k, 2 )*10.0 + 0.5 )
      enddo
c
c**   k = 5 is actually the 72-hour forecast, so correct
c
      ifpclip( 7, 1 ) = ifpclip( 6, 1 )
      ifpclip( 7, 2 ) = ifpclip( 6, 2 )
      ifpclip( 6, 1 ) = 0
      ifpclip( 6, 2 ) = 0
c
c**   Write out the forecast for the correct hemisphere
c
      do k = 1, 5
c
         EW = 'W'
         FPRITE = ABS(FPCLIP(k,2))
C
         IF (FPCLIP(k,2).LT.0.0) THEN
            EW = 'E'
            FPCLIP(k,2) = 360.0 + FPCLIP(k,2)
          ENDIF

C         
         if(k.eq.5) then

           flat60=(fpclip(4,1)+fpclip(5,1))*0.5
           flon60=(fpclip(4,2)+fpclip(5,2))*0.5

           flat(6)=flat60
           flon(6)=flon60
           flat(7)=fpclip(5,1)
           flon(7)=abs(fpclip(5,2))
           myftime='60'
           WRITE(*,'( 1X, A, '' HR = '', F5.1, '' N '', F6.1, 1X, A )') 
     &          '60',FPCLIP(k,1),FPRITE,EW
         else
          flat(k+1)=FPCLIP(k,1)
          flon(k+1)=FPRITE
         endif

         WRITE ( *, '( 1X, A, '' HR = '', F5.1, '' N '', F6.1, 1X, A )') 
     &        FTIME(K),FPCLIP(k,1),FPRITE,EW

C
       enddo
       print*
C
       return
       END
C***************************************************************
      SUBROUTINE CGULF (Y,X,U,V,U12,V12,DN,W,WGULF,GULF)
C
C**   THIS SUBROUTINE WAS ADDED JUNE 1980 AND INCLUDES A CLIPER EQUATION
C**   SET DEVELOPED FOR THE WESTERN GULF OF MEXICO AND NORTHWEST
C     CARIBBEAN SEA.  IT IS CALLED BY SUBROUTINE CLIPER.
C
      DIMENSION GULF(10),X12(37),X24(37),X36(37),X48(37),X72(37),
     1             P(37),Y12(37),Y24(37),Y36(37),Y48(37),Y72(37)
C
      DATA Y12/       0.0888784,   2.0189338,  -3.0232588,   5.0112631,
     1  -0.4663586,  -2.2601204,   1.6083838,  -0.0002354,   0.0025722,
     2   0.0380934,  -0.0006782,  -0.0451460,   0.0196852,   0.0053249,
     3  -0.0941109,   0.1065220,   0.0371968,  -0.0074174,   0.0114476,
     4   0.0397118,  -0.1690010,  -0.1136812,  -0.0028529,   0.0703457,
     5  -0.0153966,  -0.0423261,   0.1190649,   0.0001786,   0.0059967,
     6  -0.0224450,  -0.0375346,   0.1719109,   0.2308200,  -0.1857073,
     7  -0.0995993,   0.0085389, 138.45727/
C
      DATA Y24/      -0.1899584,   8.6911949,  -7.7038102,  17.8842992,
     1   1.8958812, -26.6646610,   0.8565066,  -0.0005621,  -0.0008909,
     2   0.0850158,   0.0034124,  -0.1292738,   0.0426631,   0.0168735,
     3  -0.1717200,   0.0842524,   0.0193852,  -0.0207373,   0.1633104,
     4   0.0636077,  -0.5315965,  -0.4433265,  -0.0009782,   0.2091911,
     5   0.1755244,   0.0419906,   0.3086234,  -0.0357209,   0.0119171,
     6  -0.1367056,  -0.0408844,   0.5093530,   0.8909345,  -0.5621746,
     7  -0.3903772,   0.0554313, 408.02599/
C
      DATA Y36/      -1.2791723,  18.5437755, -21.4965205,  15.7440568,
     1  13.7586086, -56.0136527,  -1.0273326,  -0.0010307,  -0.0173412,
     2  -0.0069898,   0.0192933,  -0.1414892,   0.0882439,   0.0368659,
     3  -0.2220821,   0.1678605,   0.1462510,  -0.0429246,  -0.0773177,
     4   0.1059194,  -1.3342283,  -0.8653569,   0.0101134,   0.3178639,
     5   0.4078366,  -0.0984645,   0.7358741,   0.0350543,   0.0221573,
     6   0.2828421,  -0.1563257,   1.0009459,   1.6636230,  -1.0310655,
     7  -0.6516668,   0.1635486,1203.12003/
C
      DATA Y48/      -2.2503651,  29.2124117, -40.3642497,  17.0779631,
     1  17.2671773,-104.0852329,  12.0955831,  -0.0017919,  -0.0235381,
     2  -0.0449264,   0.0317965,  -0.2155600,   0.1666921,   0.0817288,
     3   0.2846074,  -0.0195034,   0.2448353,  -0.0474278,  -0.1532889,
     4   0.1664857,  -1.9062156,  -1.2207714,   0.0097954,  -0.1064522,
     5   1.0404667,  -0.2380823,   0.9551006,  -0.0139472,   0.0130756,
     6   0.4827187,  -0.3369744,   0.9455972,   2.3926721,  -0.9962841,
     7  -0.9012016,   0.2849380,2280.38586/
C
      DATA Y72/      -1.4432551,  69.0610138, -95.5025662, -27.2247875,
     1  29.0697411,-193.8726068,  19.9328988,  -0.0065750,  -0.0171360,
     2  -0.0367320,   0.0388394,  -0.6790639,   0.4813834,   0.2157335,
     3   0.8932160,   0.0837914,   0.4136060,  -0.0491940,  -0.3513719,
     4   0.2171922,  -2.6074776,  -1.9936009,  -0.0604859,  -1.0243483,
     5   2.4907242,  -0.6472058,   1.1425050,  -0.0513188,  -0.0240031,
     6   0.6859001,  -0.3869234,   0.6265983,   3.8490617,  -0.7979159,
     7  -1.4598369,   0.3810998,4739.46017/
C
      DATA X12/      -0.6704965,   1.4162022,  -4.6100138,   1.9871832,
     1  17.5537836,  -2.1569492,  -5.3402337,   0.0012716,   0.0030864,
     2   0.0278260,   0.0000683,  -0.0343753,   0.0304263,   0.0099592,
     3   0.0788021,  -0.0810208,   0.1417678,   0.0012298,  -0.0018823,
     4  -0.0419311,   0.0747932,  -0.0306750,  -0.0050167,  -0.0070392,
     5   0.0516586,  -0.1393882,   0.0512521,   0.0067553,  -0.0037287,
     6  -0.0017485,   0.0441335,  -0.2081854,   0.1950879,   0.0235002,
     7  -0.1346830,  -0.0285769, 259.47152/
C
      DATA X24/      -3.2076529,  18.7032497, -51.1117663,   5.6067213,
     1  41.0624529,  -5.9989359, -10.5029546,   0.0062741,   0.0186705,
     2   0.1565185,  -0.0014309,  -0.3151049,   0.3294738,   0.0497310,
     3   0.4094322,  -0.3283910,   0.2947786,   0.0020355,   0.0202198,
     4  -0.1759863,   0.1977871,  -0.0611235,  -0.0238707,  -0.0192411,
     5   0.1737112,  -0.2251423,   0.3112377,  -0.0422888,  -0.0167690,
     6   0.0152779,   0.1156717,  -0.8251600,   0.5527846,   0.0455937,
     7  -0.3788840,  -0.1737905,2398.43577/
C
      DATA X36/      -6.6781488,  45.4614176,-144.0815478,  -5.8840358,
     1  69.7781262,  -2.2740308,  -4.6481818,   0.0134484,   0.0379086,
     2   0.3815790,  -0.0039753,  -0.7343225,   0.9044577,   0.1020808,
     3   1.2687996,  -0.5415504,   0.4282047,   0.0083583,   0.2549853,
     4  -0.4604174,   0.0714267,  -0.0236414,  -0.0567410,  -0.3394735,
     5   0.3102145,  -0.4093667,   0.5577365,  -0.0197161,  -0.0410260,
     6   0.0190018,   0.1124278,  -1.3487227,   0.5703272,  -0.0312319,
     7  -0.3382746,  -0.4661488,6604.67254/
C
      DATA X48/     -11.2833695,  67.7041708,-213.4578700,   7.2101560,
     1 103.3901233, -19.5321088, -14.6757722,   0.0229843,   0.0483794,
     2   0.4193408,  -0.0036961,  -0.9820638,   1.3240829,   0.1520701,
     3   2.3483309,  -1.0601856,   0.4061403,   0.0143723,   0.9105408,
     4  -0.9182075,   0.0862826,  -0.1668057,  -0.0868560,  -0.8808472,
     5   0.7276123,  -0.3159147,   0.5817031,  -0.0911473,  -0.0663834,
     6  -0.4230014,   0.3969854,  -2.0183565,   0.7029859,   0.2263893,
     7  -0.3186548,  -0.7828428,9918.98936/
C
      DATA X72/     -20.0923662, 140.1359479,-364.9217391, 111.3688979,
     1 174.4471782,-107.3250567, -43.3118878,   0.0429588,   0.0710944,
     2   0.5375573,  -0.0133502,  -1.8051834,   2.2847824,   0.2595816,
     3   4.8826019,  -3.0362177,   0.2986331,   0.0258721,   2.1804674,
     4  -1.8921960,   0.2580539,  -0.5958524,  -0.1663261,  -2.3306786,
     5   2.2924075,  -0.7559446,   0.7681488,   0.0810918,  -0.1449324,
     6  -1.4833308,   1.2019937,  -3.7551080,   1.0364360,   0.7572207,
     7  -0.3288727,  -1.4009940,16794.94253/
C
C**   INITIALIZE PREDICTAND ARRAY WITH ZEROS
C
      DO 10 I = 1,10
      GULF(I) = 0.0
   10 CONTINUE
C
      IF (WGULF.EQ.0.0) RETURN
C
C**   COMPUTE PREDICTORS
C
      P(1) = DN
      P(2) = Y
      P(3) = X
      P(4) = V
      P(5) = U
      P(6) = V12
      P(7) = U12
C
      L = 7
      DO 20 I = 1,7
      K = I
      DO 20 J = 1,K
      L = L + 1
      P(L) = P(I)*P(J)
   20 CONTINUE
C
      P(36) = W
      P(37) = 1.0
C
C**   COMPUTE DISPLACEMENTS
C
      DO 30 I = 1,37
      GULF(1) = GULF(1) + Y12(I)*P(I)
      GULF(2) = GULF(2) - X12(I)*P(I)
      GULF(3) = GULF(3) + Y24(I)*P(I)
      GULF(4) = GULF(4) - X24(I)*P(I)
      GULF(5) = GULF(5) + Y36(I)*P(I)
      GULF(6) = GULF(6) - X36(I)*P(I)
      GULF(7) = GULF(7) + Y48(I)*P(I)
      GULF(8) = GULF(8) - X48(I)*P(I)
      GULF(9) = GULF(9) + Y72(I)*P(I)
      GULF(10) = GULF(10) - X72(I)*P(I)
   30 CONTINUE
C
      RETURN
      END
c***********************************************************************
      SUBROUTINE ATSHIF ( ymdh, ALAT,  ALON, ALAT12, ALON12,
     &                           VEL, VEL12, STRMID )
C                                                                       
C**   MEMBER NAME IS ATSHIF
C                                                                       
C**   THIS VERSION OF ATLC SHIFOR HAS HOMOGENEOUS 2ND ORDER TERMS TO
C**   1.0% ROV CUTOFF, BASED ON 1967-1987 DATA INCLUDING DEPRESSIONS.
C**   DEVELOPED 5/88 BY ACP.
c**
C**   ALSO RUNS 3RD ORDER VERSION FOR COMPARISON ON PAPER PRTOUT ONLY.
c
      common /shifor/ ishifor( 11, 3 )
c
      dimension ishfor(6)
      DIMENSION C12(10),C24(10),C36(10),C48(10),C60(10),C72(10)         
      DIMENSION iwnd(7),WCH(6),INDAY(13)
c
      INTEGER*4 ymdh
      integer DAYNUM
      DOUBLE PRECISION C12,C24,C36,C48,C60,C72,P1,P2,P3,P4,P5,P6,P7
C
      CHARACTER*8 STRMID
c
      DATA INDAY/0,31,59,90,120,151,181,212,243,273,304,334,365/
      DATA C12/.1530475D+00,-.2553107D-03,.1459448D-03,.2279049D-02,    
     1         .1338358D-02,-.2182348D-03,-.4846294D-02,-.6557441D-03,  
     2         -.2692854D-02,.3909403D+00/                              
      DATA C24/.2596963D+00,-.3838384D-03,.1360290D-03,.4236407D-02,    
     1         .3268938D-02,-.1004894D-02,-.9218484D-02,-.1057957D-02,  
     2         -.8076836D-02,.1060404D+01/                              
      DATA C36/.3055408D+00,-.7437406D-04,-.8858569D-04,.5281386D-02,   
     1         .4389817D-02,-.2559764D-02,-.1191667D-01,-.1057314D-02,  
     2         -.1118904D-01,.2696558D+01/                              
      DATA C48/.3684350D+00,.5582401D-03,-.5871285D-03,.5942861D-02,    
     1         .4762164D-02,-.4090372D-02,-.1513060D-01,-.5448064D-03,  
     2         -.1383077D-01,.5411902D+01/                              
      DATA C60/.5268111D+00,.1340049D-02,-.1033111D-02,.5623851D-02,    
     1         .3776452D-02,-.4339567D-02,-.2023253D-01,-.4885447D-03,  
     2         -.1373462D-01,.8303001D+01/                              
      DATA C72/.7662474D+00,.2396768D-02,-.1519305D-02,.5221579D-02,    
     1         .1874980D-02,-.5469727D-02,-.2590622D-01,-.2277254D-03,  
     2	       -.1281859D-01,.1207121D+02/
c
c**   Write the input parameter to the printer
c
      write (*,'('' ATLANTIC SHIFOR'',/)')
      write ( *, '('' INPUT PARAMETERS FOR TROPICAL CYCLONE '', A,
     & '' ON YMDH = '', I10.10, / )' ) STRMID, ymdh
      write (*,'('' LATCUR = '',f5.1,'' N  LONCUR = '',f6.1,
     & '' W  WNDCUR = '',f4.0,'' KT'',/,'' LATM12 = '',f5.1,
     & '' N  LONM12 = '',f6.1,'' W  WNDM12 = '',f4.0,'' KT'',/)')
     & alat, alon, vel, alat12, alon12, vel12
c
      IWND(1) = VEL + 0.5
      DO 10 I = 2,7
         IWND(I) = -99
   10 continue
c
      IF (VEL.LT.15.0.OR.VEL12.LT.15.0) then
	  WRITE (6,1)
    1	  FORMAT (/,' ATSHIF NOT RUN DUE TO AT LEAST ONE INPUT WIND LES
     &S THAN 15 KT')
	  RETURN
      endif
c
      IYeaR  = ymdh/1000000
      IMOnth = (ymdh - IYear*1000000)/10000
      IDAy   = (ymdh - IYeaR*1000000 - IMOnth*10000)/100
c
      DAYNUM = INDAY(IMOnth) + IDAy
cc    IF (DAYNUM.LT.135.0) DAYNUM = 135.0
cc    IF (DAYNUM.GT.349.0) DAYNUM = 349.0
      RAD = 180.0/3.14159
      DX = ALON - ALON12
c
Cc    DY = ALAT - ALAT12
c
      D2 = (ALAT + ALAT12)/2.0
      U = -DX*60.0*COS(D2/RAD)/12.0
c
Cc    V = DY*60.0/12.0
c
      P1 = FLOAT(DAYNUM)
      P2 = ALAT
      P3 = ALON
      P4 = U
c
Cc    P5 = V
c
      P6 = VEL
      P7 = VEL - VEL12
c
      WCH(1) = C12(1)*P4+C12(2)*P1*P2+C12(3)*P1*P6+C12(4)*P1*P7+
     1 C12(5)*P2*P3+C12(6)*P2*P6+C12(7)*P4*P6+C12(8)*P6*P6+C12(9)*P6*P7+
     2 C12(10)                                                          
      WCH(2) = C24(1)*P4+C24(2)*P1*P2+C24(3)*P1*P6+C24(4)*P1*P7+
     1 C24(5)*P2*P3+C24(6)*P2*P6+C24(7)*P4*P6+C24(8)*P6*P6+C24(9)*P6*P7+
     2 C24(10)                                                          
      WCH(3) = C36(1)*P4+C36(2)*P1*P2+C36(3)*P1*P6+C36(4)*P1*P7+
     1 C36(5)*P2*P3+C36(6)*P2*P6+C36(7)*P4*P6+C36(8)*P6*P6+C36(9)*P6*P7+
     2 C36(10)                                                          
      WCH(4) = C48(1)*P4+C48(2)*P1*P2+C48(3)*P1*P6+C48(4)*P1*P7+
     1 C48(5)*P2*P3+C48(6)*P2*P6+C48(7)*P4*P6+C48(8)*P6*P6+C48(9)*P6*P7+
     2 C48(10)                                                          
      WCH(5) = C60(1)*P4+C60(2)*P1*P2+C60(3)*P1*P6+C60(4)*P1*P7+
     1 C60(5)*P2*P3+C60(6)*P2*P6+C60(7)*P4*P6+C60(8)*P6*P6+C60(9)*P6*P7+
     2 C60(10)                                                          
      WCH(6) = C72(1)*P4+C72(2)*P1*P2+C72(3)*P1*P6+C72(4)*P1*P7+
     1 C72(5)*P2*P3+C72(6)*P2*P6+C72(7)*P4*P6+C72(8)*P6*P6+C72(9)*P6*P7+
     2 C72(10)
c
      DO 20 I = 2, 7
         IWND(I) = VEL + WCH(I - 1) + 0.5
         IF (IWND(I).LT.0) IWND(I) = 0
   20 CONTINUE
c
      do i = 1, 6
         ishfor(i) = iwnd(i + 1)
      enddo
c
      do i = 1, 6
         ishifor( i + 1, 3 ) = ishfor(i)
      enddo   
c
      write ( *, '('' FORECAST INTENSITY (KT)'')' )
      WRITE ( *, 2 ) IWND(1), ( ishfor(i), i = 1, 6 )
    2 FORMAT (/,' 00 HR = ',I5,/,' 12 HR = ',I5,/,' 24 HR = ',
     & I5,/,' 36 HR = ',I5,/,' 48 HR = ',I5,/,' 60 HR = ',i5,/,
     & ' 72 HR = ',I5,/)
c
C**   NOW RUN 3RD ORDER VERSION FOR PAPER PRTOUT ONLY
c**   (Disabled by Jim Gross -- 2/7/90)
c
cc    CALL ASHIF3 (P1,P2,P3,P4,P6,P7)
c
      RETURN                                                            
      END
c*******************************************************************
      SUBROUTINE ASHIF3 (P1,P2,P3,P4,P6,P7)
c
C**   THIS VERSION OF ATLC SHIFOR HAS HOMOGENEOUS 3RD ORDER TERMS TO
C**   1.0% ROV CUTOFF, BASED ON 1967-1987 DATA INCLUDING DEPRESSIONS.
C**   DEVELOPED 5/88 BY ACP.
c
      DIMENSION C12(12),C24(12),C36(12),C48(12),C60(12),C72(12)         
      DIMENSION WCH(6),IWND(7)
c
      DOUBLE PRECISION C12,C24,C36,C48,C60,C72,P1,P2,P3,P4,P5,P6,P7
c
      DATA C12/.5252134D-01,.2259276D-02,.7801564D-03,.5335434D-03,     
     1         .1125294D-02,-.2513409D-05,-.5125665D-05,-.3354750D-04,  
     2         -.3416235D-05,-.2580465D-04,-.3247886D-03,-.1807719D+01/ 
      DATA C24/.4766981D-01,.4959559D-02,.2333130D-02,-.4905442D-02,    
     1         .2133818D-02,-.2521209D-04,.3855149D-05,-.6049613D-04,   
     2         -.1531506D-04,-.6860745D-04,-.3978876D-03,-.3157438D+01/ 
      DATA C36/.2730670D-01,.6647561D-02,.4850945D-02,-.1043806D-01,    
     1         .2587929D-02,-.4107225D-04,.9707236D-05,-.8189586D-04,   
     2         -.3070338D-04,-.1137476D-03,-.3204486D-03,-.3391049D+01/ 
      DATA C48/-.9544812D-01,.6922097D-02,.1037129D-01,-.7863326D-02,   
     1         .2197105D-02,-.4753532D-04,-.3884948D-05,-.9123283D-04,  
     2         -.4651861D-04,-.1686422D-03,-.3773180D-03,-.2190176D+01/ 
      DATA C60/-.8526621D-01,.5366142D-02,.1216446D-01,.2299124D-02,    
     1         .4058021D-02,-.3922367D-04,.1923083D-04,-.1109815D-03,   
     2         -.9224470D-04,-.2213808D-03,-.5093353D-03,-.2607086D+01/ 
      DATA C72/.8225810D-01,.4146847D-02,.9464166D-02,.1185835D-01,     
     1         .7024180D-02,-.3752321D-04,.7544587D-04,-.1410996D-03,   
     2	       -.1466218D-03,-.2613349D-03,-.5039879D-03,-.4044404D+01/
c
      IWND(1) = P6 + 0.5
      WCH(1) = C12(1)*P2+C12(2)*P1*P7+C12(3)*P2*P3+C12(4)*P2*P7+
     1 C12(5)*P3*P6+C12(6)*P1*P6*P7+C12(7)*P2*P3*P3+C12(8)*P2*P6*P6+    
     2 C12(9)*P3*P3*P6+C12(10)*P3*P4*P6+C12(11)*P7*P7*P7+C12(12)        
      WCH(2) = C24(1)*P2+C24(2)*P1*P7+C24(3)*P2*P3+C24(4)*P2*P7+
     1 C24(5)*P3*P6+C24(6)*P1*P6*P7+C24(7)*P2*P3*P3+C24(8)*P2*P6*P6+    
     2 C24(9)*P3*P3*P6+C24(10)*P3*P4*P6+C24(11)*P7*P7*P7+C24(12)        
      WCH(3) = C36(1)*P2+C36(2)*P1*P7+C36(3)*P2*P3+C36(4)*P2*P7+
     1 C36(5)*P3*P6+C36(6)*P1*P6*P7+C36(7)*P2*P3*P3+C36(8)*P2*P6*P6+    
     2 C36(9)*P3*P3*P6+C36(10)*P3*P4*P6+C36(11)*P7*P7*P7+C36(12)        
      WCH(4) = C48(1)*P2+C48(2)*P1*P7+C48(3)*P2*P3+C48(4)*P2*P7+
     1 C48(5)*P3*P6+C48(6)*P1*P6*P7+C48(7)*P2*P3*P3+C48(8)*P2*P6*P6+    
     2 C48(9)*P3*P3*P6+C48(10)*P3*P4*P6+C48(11)*P7*P7*P7+C48(12)        
      WCH(5) = C60(1)*P2+C60(2)*P1*P7+C60(3)*P2*P3+C60(4)*P2*P7+
     1 C60(5)*P3*P6+C60(6)*P1*P6*P7+C60(7)*P2*P3*P3+C60(8)*P2*P6*P6+    
     2 C60(9)*P3*P3*P6+C60(10)*P3*P4*P6+C60(11)*P7*P7*P7+C60(12)        
      WCH(6) = C72(1)*P2+C72(2)*P1*P7+C72(3)*P2*P3+C72(4)*P2*P7+
     1 C72(5)*P3*P6+C72(6)*P1*P6*P7+C72(7)*P2*P3*P3+C72(8)*P2*P6*P6+    
     2 C72(9)*P3*P3*P6+C72(10)*P3*P4*P6+C72(11)*P7*P7*P7+C72(12)
c
      DO 10 I = 2,7
         IWND(I) = P6 + WCH(I - 1) + 0.5
         IF (IWND(I).LT.0) IWND(I) = 0
   10 CONTINUE
c
      WRITE (6,101) IWND
  101 FORMAT(///,5X,'ASHIF3 00HR 12HR 24HR 36HR 48HR 60HR 72HR MAX WINDS
     1',//,5X,6X,7I5,' KT',///)
c
      RETURN                                                            
      END
c***************************************************************************
      subroutine atshif5d ( ymdh,  alat, alon, alat12, alon12, 
     &                       vel, vel12, strmid )
c     
c     atshif5d
c
c     This subroutine calculates tropical cyclone intensities through 120
c     hours based upon climatology and persistence using the years 
c     1967-1999.  The model was created using the total change in intensity 
c     for each period (12-hr,....120-hr) from intial conditions as the 
c     predictand and 35 predictors including and derived from 
c     julian day, latitude, longitude, zonal speed, meridional speed, 
c     current intensity the past 12-hour intensity trend.
c     
c     In the formulation of the model linear terms are first put into the
c     model using a forward stepping approach for the 12-hour forecast.   
c     The linear predictors chosen in this forward stepping process 
c     are then forced into the model and exposed to the 2nd order terms, 
c     which at this point are allowed to come into the model in a 
c     stepwise fashion.  A backward step is then performed to remove 
c     predictors that are no longer significant.  Then a final stepwise
c     stepping proceedure is performed possibly adding a removing predictors
c
c
c     Following the 12-hour forecast the predictors chosen for the previous
c     forecast period are then given preference in the selection process. 
c     Again, the predictors chosen in this forward stepping process 
c     are then forced into the model and exposed to the 2nd order terms, 
c     which at this point are allowed to come into the model in a 
c     stepwise fashion.  A backward pass through the data is then performed 
c     to remove predictors that are no longer significant. Followed by  
c     a final step that is stepwise.
c
c     J. Knaff (04/05/2001)
c
      common /shifor5/ ishifor5( 11, 3 )
      common /al5coef/ scoef(10,36), avg(10,36), sdev(10,36)
c
c     dimension coeficients.
c
      parameter(nc=36)
      real p(36), forecast(10)
      double precision  dv (10)

c
c     dimension input.
c
      integer ymdh,daynum
      integer iwnd(10)
      character*6 strmid
      character*8 aymdh
      real alat, alon, alat12, alon12, vel, vel12
c
c     intialize to zero
c
      do i=1,10
         dv(i)=0.0
         iwnd(i)=0
      end do
c    
c     write input parameters out to printer
c
      write (*,'('' ATLANTIC SHIFOR5'',/)')
      write (*,1001)strmid,ymdh
 1001 format('INPUT PARAMETERS FOR TROPICAL CYCLONE ',A,
     & ' ON YMDH = ',I10.10,/) 
      write (*,1002)alat,alon,vel,alat12,alon12,vel12
 1002 format(' LA0   = ',F5.1,' N  LO0   = ',F6.1,
     .     ' W  WND0   = ',F4.0,' KT',/,' LAM12 = ',F5.1,
     .     ' N  LOM12 = ',F6.1,' W  WNDM12 = ',F4.0,' KT',/)

c 
c     check for system intensity requirements.
c
      if (vel.lt.15.0.OR.vel12.lt.15.0) then
          write (6,1)
 1        format (/,' ATSHIF NOT RUN DUE TO AT LEAST ONE INPUT WIND LESS
     .THAN 15 KT')
          return
      endif
c
c     create predictor pool (first order terms, squares, and 
c     co-variances terms)
c
c     p1 = julian day - 253
c     p2 = lat
c     p3 = lon
c     p4 = u ! zonal speed of the storm over the last 12 hours
c     p5 = v ! meridional speed of the storm over the last 12 hours
c     p6 = vmax
c     p7 = delta vmax
c
c     calculate julian day
c
      iyear  = ymdh/1000000
      imonth = (ymdh - iyear*1000000)/10000
      iday   = (ymdh - iyear*1000000 - imonth*10000)/100
      call jday(imonth,iday,iyear,julday)
c
c     assign predictor values from the input data
c
      p(1) = dble(julday-253)
      p(2) = dble(alat)
      p(3) =dble(alon)
      avglat=(alat+alat12)/2.0
      p(4) =dble((alon-alon12)* (-60.0)/ 12.0 * 
     .     COS(rad*avglat))
      p(5)=dble((alat-alat12)*60./12.)
      p(6)=dble(vel)
      p(7)=dble(vel-vel12)
      p(8)=p(1)**2                !p1*p1  
      p(9)=p(1)*p(2)              !p1*p2
      p(10)=p(1)*p(3)             !p1*p3  
      p(11)=p(1)*p(4)             !etc....
      p(12)=p(1)*p(5)
      p(13)=p(1)*p(6)
      p(14)=p(1)*p(7)
      p(15)=p(2)**2
      p(16)=p(2)*p(3)
      p(17)=p(2)*p(4)
      p(18)=P(2)*p(5)
      p(19)=p(2)*p(6)
      p(20)=p(2)*p(7)
      p(21)=p(3)**2
      p(22)=p(3)*p(4)
      p(23)=p(3)*p(5)
      p(24)=p(3)*p(6)
      p(25)=p(3)*p(7)
      p(26)=p(4)**2
      p(27)=p(4)*p(5)
      p(28)=p(4)*p(6)
      p(29)=p(4)*p(7)
      p(30)=p(5)**2
      p(31)=p(5)*p(6)
      p(32)=p(5)*p(7)
      p(33)=p(6)**2
      p(34)=p(6)*p(7)
      p(35)=p(7)**2
      p(36)=vel
c
c     calculate the predicted incremental change in velocity
c          
      do i=1,10
         dv(i)=0.0 ! intitialize array to zero.
         do j=1,35
            dv(i)=dv(i)+dble(scoef(i,j)*((p(j)-avg(i,j))/sdev(i,j)))
         end do
         dv(i)=dv(i)*dble(sdev(i,36)) + dble(avg(i,36))
      end do
c
c     
c     construct forecast intensities
c
      forecast(1)=p(36)+dv(1)
      
      do i=1,10
         forecast(i)= p(36)+sngl(dv(i))
      end do
      do i=1,10
         if (forecast(i).lt.0.0)forecast(i)=0.0
         iwnd(i)=nint(forecast(i))
      end do
c
c     fill ishifor array for the atcf
c
      ishifor5(1,3)=nint(vel)
      do i = 1, 10
         ishifor5( i + 1, 3 ) = iwnd(i)
      enddo   
c
c     write forecasts to standard output.
c
      ivel = nint(vel)
      write ( *, '('' FORECAST INTENSITY (KT)'')' )
      WRITE ( *, 2 ) ivel, ( iwnd(i), i = 1, 10 )
    2 FORMAT (/,' 00 HR = ',I5,/,' 12 HR = ',I5,/,' 24 HR = ',
     & I5,/,' 36 HR = ',I5,/,' 48 HR = ',I5,/,' 60 HR = ',i5,/,
     & ' 72 HR = ',I5,/,' 84 HR = ',I5,/,' 96 HR = ',I5,/,
     & '108 HR = ',I5,/,'120 HR = ',I5,/)
c
      return
      end
c*******************************************************************
      subroutine jday(imon,iday,iyear,julday)
c     This routine calculates the Julian day (julday) from
c     the month (imon), day (iday), and year (iyear). The
c     appropriate correction is made for leap year.
c
      dimension ndmon(12)
c
c     Specify the number of days in each month
      ndmon(1)  = 31
      ndmon(2)  = 28
      ndmon(3)  = 31
      ndmon(4)  = 30
      ndmon(5)  = 31
      ndmon(6)  = 30
      ndmon(7)  = 31
      ndmon(8)  = 31
      ndmon(9)  = 30
      ndmon(10) = 31
      ndmon(11) = 30
      ndmon(12) = 31
c
c     Correct for leap year
      if (mod(iyear,4) .eq. 0) ndmon(2)=29
c
c     Check for illegal input
      if (imon .lt. 1 .or. imon .gt. 12) then
         julday=-1
         return
      endif
c
      if (iday .lt. 1 .or. iday .gt. ndmon(imon)) then
         julday=-1
         return
      endif
c
c     Calculate the Julian day
      julday = iday
      if (imon .gt. 1) then
         do 10 i=2,imon
            julday = julday + ndmon(i-1)
   10    continue
      endif
c
      return
      end
c**********************************************************************
      SUBROUTINE EPCL84 ( ymdh, la0, lo0, lam12, lom12, lam24, lom24,
     &                         dir0, spd0, wnd0, STRMID )
c
C**   Charlie's eastern Pacific CLIPER
c
      common /cliper/ ifpclip(11,3),flat(7),flon(7)
      COMMON /CL84/ CDI(12)
      COMMON /PP/ P(164)
c
      real fpclip(6,2)
      DIMENSION PAV(8),INX(88),INDAY(13),cfo(2,6)
c
      integer*4 ymdh
      real la0,lo0,lam12,lom12,lam24,lom24
      DOUBLE PRECISION DISP(2,6),C(88),COF(2,164,6),AICP(2,7)
C
      CHARACTER*8  STRMID
      character*75 include_path, epcof_file
c
      DATA PAV	 /16.8,120.3,230.6,3.4,-7.5,3.3,-7.8,61.5/
      DATA INDAY /0,31,59,90,120,151,181,212,243,273,304,334,365/
c
c**   Write the input parameter to the printer
c
      write (*,'('' EASTERN PACIFIC CLIPER'',/)')
      write (*,'('' INPUT PARAMETERS FOR TROPICAL CYCLONE '',A,
     & '' ON YMDH = '',i10,/)') STRMID, ymdh
      write (*,'('' LATCUR = '',f4.1,'' N LONCUR = '',f6.1,
     1 '' W'',/,
     & '' DIRCUR = '',f4.0,'' DEG  SPDCUR = '',f4.0,'' KT  WNDCUR = '',
     2 f4.0,'' KT'',/,
     & '' LATM12 = '',f4.1,'' N  LONM12 = '',f6.1,'' W'',/,
     3 '' LATM24 = '',f4.1,'' N  LONM24 = '',f6.1,'' W'',/)')
     4 la0,lo0,dir0,spd0,wnd0,lam12,lom12,lam24,lom24
c
      iyear   = ymdh/1000000
      imonth  = ymdh/10000 - iyear*100
      iday    = ymdh/100   - imonth*100  - iyear*10000
      ihour   = ymdh	   - iday*100	 - imonth*10000 - iyear*1000000
c
      DAYN = FLOAT(INDAY(imonth) + iday) + FLOAT(ihour)/24.0
      print*,'EEEEEEEEEEE dayn ',dayn
      IF (DAYN.LT.135.0) DAYN = 135.0
      IF (DAYN.GT.349.0) DAYN = 349.0
      DIR = dir0/57.29578
      V0 = spd0*COS(DIR)
      U0 = spd0*SIN(DIR)
c
      CALL STHGPR (lam12,lom12,360.0,1.0,0.0,0.0)
      CALL LL2XYH (la0,lo0,XF,YF)
      CALL LL2XYH (lam24,lom24,XP,YP)
c
      V1 = (YF - YP)/24.0
      U1 = (XF - XP)/24.0
c
      P(1) = la0 - PAV(1)
      P(2) = lo0 - PAV(2)
      P(3) = DAYN - PAV(3)
      P(4) = V0 - PAV(4)
      P(5) = U0 - PAV(5)
      P(6) = V1 - PAV(6)
      P(7) = U1 - PAV(7)
      P(8) = wnd0 - PAV(8)
c
      CALL MULT1
      CALL MULT2
      CALL MULT3
      CALL MULT4
c
      CALL STHGPR (la0,lo0,360.0,1.0,0.0,0.0)
c
      DO 10 NDIR = 1,2
      DO 10 J = 1,164
      DO 10 NTIM = 1,6
         COF(NDIR,J,NTIM) = 0.0
   10 continue
c
c**   Open regression coefficient file
c
c**   Get the command line parameter and the storms directory path
c
      call getenv ("ATCFINCLUDE", include_path )
c
c**   Construct the cdeck file name and open the file
c
      epcof_file = "nhc_epcliper.cof"    ! uncomment to run locally
c
      open ( 22, file=epcof_file, status='old', iostat=ios, err=1010 )
c
      NTIM = 1
   20 READ (22,1,END=40,iostat=ios,err=1020) NDIR,NC,
     & (INX(I),C(I),I = 1,NC),AICP(NDIR,NTIM)
    1 FORMAT (2I5,/,11(4(I3,E15.7),/),E15.7)
c
cc    write (*,1) NDIR,NC,(INX(I),C(I),I = 1,NC),AICP(NDIR,NTIM)
cc    pause ' Hit <CR> to continue.'
c
      DO 30 I = 1,NC
         J = INX(I) - 2
         COF(NDIR,J,NTIM) = C(I)
   30 continue
c
      IF (NDIR.EQ.1) GO TO 20
      NTIM = NTIM + 1
      GO TO 20
c
   40 close (22)
c
      DO 50 NDIR = 1,2
      DO 50 NTIM = 1,6
         DISP(NDIR,NTIM) = AICP(NDIR,NTIM)
   50 continue
c
      DO 60 NDIR = 1,2
      DO 60 NTIM = 1,6
      DO 60 J = 1,164
         IF (COF(NDIR,J,NTIM).EQ.0.) GO TO 60
         DISP(NDIR,NTIM) = DISP(NDIR,NTIM) + COF(NDIR,J,NTIM)*P(J)
         NF = 2*(NTIM - 1) + NDIR
         CDI(NF) = SNGL(DISP(NDIR,NTIM))
   60 CONTINUE
c
      DO 70 NTIM = 1,6
         NF = 2*NTIM
         AX = CDI(NF)
         AY = CDI(NF - 1)
c
         CALL XY2LLH (AX,AY,CFO(1,Ntim),CFO(2,Ntim))
c
   70 continue
c         
      flat(1)=la0
      flon(1)=lo0
      do i = 1,6
         fpclip(i,1) = cfo(1,i)
         fpclip(i,2) = cfo(2,i)
         flat(i+1)=cfo(1,i)
         flon(i+1)=cfo(2,i)
      enddo
c
      do i = 1, 6
c
         ifpclip( i + 1, 1 ) = int( fpclip( i, 1 )*10.0 + 0.5 )
         if ( fpclip( i, 2 ) .lt. 0.0 )
     &        fpclip( i, 2) = 360.0 + fpclip( i, 2 )
         ifpclip( i + 1, 2 ) = int( fpclip( i, 2 )*10.0 + 0.5 )
c
      enddo   
c
      write (*,'('' FORECAST POSITIONS'',/)')
      WRITE ( 6, 3 ) la0,lo0,(fpclip(i,1),fpclip(i,2), i = 1, 6)
    3 FORMAT (' 00 HR = ',F5.1,' N ',F6.1,' W',
     1	    /,' 12 HR = ',F5.1,' N ',F6.1,' W',
     2	    /,' 24 HR = ',F5.1,' N ',F6.1,' W',
     3	    /,' 36 HR = ',F5.1,' N ',F6.1,' W',
     4	    /,' 48 HR = ',F5.1,' N ',F6.1,' W',
     5	    /,' 60 HR = ',F5.1,' N ',F6.1,' W',
     6     /,' 72 HR = ',F5.1,' N ',F6.1,' W',/)

c
      RETURN
c
c**   Error messages
c
 1010 print *,' Error openning coeficient data file = ',ios
      stop
c
 1020 print *,' Error reading coefficient data file = ',ios
      stop
c
      END
c***********************************************************************
      SUBROUTINE MULT1
c
      COMMON /PP/ P(164)
c
      P( 9)=P(1)*P(1)
      P(10)=P(2)*P(2)
      P(11)=P(3)*P(3)
      P(12)=P(4)*P(4)
      P(13)=P(5)*P(5)
      P(14)=P(6)*P(6)
      P(15)=P(7)*P(7)
      P(16)=P(8)*P(8)
      P(17)=P(1)*P(2)
      P(18)=P(1)*P(3)
      P(19)=P(1)*P(4)
      P(20)=P(1)*P(5)
      P(21)=P(1)*P(6)
      P(22)=P(1)*P(7)
      P(23)=P(1)*P(8)
      P(24)=P(2)*P(3)
      P(25)=P(2)*P(4)
      P(26)=P(2)*P(5)
      P(27)=P(2)*P(6)
      P(28)=P(2)*P(7)
      P(29)=P(2)*P(8)
      P(30)=P(3)*P(4)
      P(31)=P(3)*P(5)
      P(32)=P(3)*P(6)
      P(33)=P(3)*P(7)
      P(34)=P(3)*P(8)
      P(35)=P(4)*P(5)
      P(36)=P(4)*P(6)
      P(37)=P(4)*P(7)
      P(38)=P(4)*P(8)
      P(39)=P(5)*P(6)
      P(40)=P(5)*P(7)
      P(41)=P(5)*P(8)
      P(42)=P(6)*P(7)
      P(43)=P(6)*P(8)
      P(44)=P(7)*P(8)
      P(45)=P(1)*P(1)*P(1)
      P(46)=P(2)*P(2)*P(2)
      P(47)=P(3)*P(3)*P(3)
c
      RETURN
      END
c*****************************************************************
      SUBROUTINE MULT2
c
      COMMON /PP/ P(164)
c
      P(48)=P(4)*P(4)*P(4)
      P(49)=P(5)*P(5)*P(5)
      P(50)=P(6)*P(6)*P(6)
      P(51)=P(7)*P(7)*P(7)
      P(52)=P(8)*P(8)*P(8)
      P(53)=P(1)*P(1)*P(2)
      P(54)=P(1)*P(1)*P(3)
      P(55)=P(1)*P(1)*P(4)
      P(56)=P(1)*P(1)*P(5)
      P(57)=P(1)*P(1)*P(6)
      P(58)=P(1)*P(1)*P(7)
      P(59)=P(1)*P(1)*P(8)
      P(60)=P(2)*P(2)*P(1)
      P(61)=P(2)*P(2)*P(3)
      P(62)=P(2)*P(2)*P(4)
      P(63)=P(2)*P(2)*P(5)
      P(64)=P(2)*P(2)*P(6)
      P(65)=P(2)*P(2)*P(7)
      P(66)=P(2)*P(2)*P(8)
      P(67)=P(3)*P(3)*P(1)
      P(68)=P(3)*P(3)*P(2)
      P(69)=P(3)*P(3)*P(4)
      P(70)=P(3)*P(3)*P(5)
      P(71)=P(3)*P(3)*P(6)
      P(72)=P(3)*P(3)*P(7)
      P(73)=P(3)*P(3)*P(8)
      P(74)=P(4)*P(4)*P(1)
      P(75)=P(4)*P(4)*P(2)
      P(76)=P(4)*P(4)*P(3)
      P(77)=P(4)*P(4)*P(5)
      P(78)=P(4)*P(4)*P(6)
      P(79)=P(4)*P(4)*P(7)
      P(80)=P(4)*P(4)*P(8)
      P(81)=P(5)*P(5)*P(1)
      P(82)=P(5)*P(5)*P(2)
      P(83)=P(5)*P(5)*P(3)
      P(84)=P(5)*P(5)*P(4)
      P(85)=P(5)*P(5)*P(6)
      P(86)=P(5)*P(5)*P(7)
c
      RETURN
      END
c************************************************************
      SUBROUTINE MULT3
c
      COMMON /PP/ P(164)
c
      P(87)=P(5)*P(5)*P(8)
      P(88)=P(6)*P(6)*P(1)
      P(89)=P(6)*P(6)*P(2)
      P(90)=P(6)*P(6)*P(3)
      P(91)=P(6)*P(6)*P(4)
      P(92)=P(6)*P(6)*P(5)
      P(93)=P(6)*P(6)*P(7)
      P(94)=P(6)*P(6)*P(8)
      P(95)=P(7)*P(7)*P(1)
      P(96)=P(7)*P(7)*P(2)
      P(97)=P(7)*P(7)*P(3)
      P(98)=P(7)*P(7)*P(4)
      P(99)=P(7)*P(7)*P(5)
      P(100)=P(7)*P(7)*P(6)
      P(101)=P(7)*P(7)*P(8)
      P(102)=P(8)*P(8)*P(1)
      P(103)=P(8)*P(8)*P(2)
      P(104)=P(8)*P(8)*P(3)
      P(105)=P(8)*P(8)*P(4)
      P(106)=P(8)*P(8)*P(5)
      P(107)=P(8)*P(8)*P(6)
      P(108)=P(8)*P(8)*P(7)
      P(109)=P(1)*P(2)*P(3)
      P(110)=P(1)*P(2)*P(4)
      P(111)=P(1)*P(2)*P(5)
      P(112)=P(1)*P(2)*P(6)
      P(113)=P(1)*P(2)*P(7)
      P(114)=P(1)*P(2)*P(8)
      P(115)=P(1)*P(3)*P(4)
      P(116)=P(1)*P(3)*P(5)
      P(117)=P(1)*P(3)*P(6)
      P(118)=P(1)*P(3)*P(7)
      P(119)=P(1)*P(3)*P(8)
      P(120)=P(1)*P(4)*P(5)
      P(121)=P(1)*P(4)*P(6)
      P(122)=P(1)*P(4)*P(7)
      P(123)=P(1)*P(4)*P(8)
      P(124)=P(1)*P(5)*P(6)
      P(125)=P(1)*P(5)*P(7)
c
      RETURN
      END
c**************************************************************
      SUBROUTINE MULT4
c
      COMMON /PP/ P(164)
c
      P(126)=P(1)*P(5)*P(8)
      P(127)=P(1)*P(6)*P(7)
      P(128)=P(1)*P(6)*P(8)
      P(129)=P(1)*P(7)*P(8)
      P(130)=P(2)*P(3)*P(4)
      P(131)=P(2)*P(3)*P(5)
      P(132)=P(2)*P(3)*P(6)
      P(133)=P(2)*P(3)*P(7)
      P(134)=P(2)*P(3)*P(8)
      P(135)=P(2)*P(4)*P(5)
      P(136)=P(2)*P(4)*P(6)
      P(137)=P(2)*P(4)*P(7)
      P(138)=P(2)*P(4)*P(8)
      P(139)=P(2)*P(5)*P(6)
      P(140)=P(2)*P(5)*P(7)
      P(141)=P(2)*P(5)*P(8)
      P(142)=P(2)*P(6)*P(7)
      P(143)=P(2)*P(6)*P(8)
      P(144)=P(2)*P(7)*P(8)
      P(145)=P(3)*P(4)*P(5)
      P(146)=P(3)*P(4)*P(6)
      P(147)=P(3)*P(4)*P(7)
      P(148)=P(3)*P(4)*P(8)
      P(149)=P(3)*P(5)*P(6)
      P(150)=P(3)*P(5)*P(7)
      P(151)=P(3)*P(5)*P(8)
      P(152)=P(3)*P(6)*P(7)
      P(153)=P(3)*P(6)*P(8)
      P(154)=P(3)*P(7)*P(8)
      P(155)=P(4)*P(5)*P(6)
      P(156)=P(4)*P(5)*P(7)
      P(157)=P(4)*P(5)*P(8)
      P(158)=P(4)*P(6)*P(7)
      P(159)=P(4)*P(6)*P(8)
      P(160)=P(4)*P(7)*P(8)
      P(161)=P(5)*P(6)*P(7)
      P(162)=P(5)*P(6)*P(8)
      P(163)=P(5)*P(7)*P(8)
      P(164)=P(6)*P(7)*P(8)
c
      RETURN
      END
c**********************************************************
      SUBROUTINE STHGPR (XLATH,XLONH,BEAR,GRIDSZ,XI0,YJ0)
c
C**   ALBION D. TAYLOR, MARCH 19, 1982
c
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
c
      CLAT=COS(RADPDG*XLATH)
      SLAT=SIN(RADPDG*XLATH)
      SLON=SIN(RADPDG*XLONH)
      CLON=COS(RADPDG*XLONH)
      SBEAR=SIN(RADPDG*BEAR)
      CBEAR=COS(RADPDG*BEAR)
c
      A(1,1)=   CLAT*SLON
      A(1,2)=   CLAT*CLON
      A(1,3)=   SLAT
      A(2,1)= - CLON*CBEAR + SLAT*SLON*SBEAR
      A(2,2)=   SLON*CBEAR + SLAT*CLON*SBEAR
      A(2,3)=              - CLAT*     SBEAR
      A(3,1)= - CLON*SBEAR - SLAT*SLON*CBEAR
      A(3,2)=   SLON*SBEAR - SLAT*CLON*CBEAR
      A(3,3)=		     CLAT*     CBEAR
c
      DGRIDH=GRIDSZ
      HGRIDX=XI0
      HGRIDY=YJ0
c
      RETURN
      END
c****************************************************************
      SUBROUTINE LL2XYH (XLAT,XLONG,XI,YJ)
c
C**   ALBION D. TAYLOR, MARCH 19, 1982
c
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
c
      DIMENSION ZETA(3),ETA(3)
c
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
c
   40 YJ=0.
      RETURN
c
      END
c*************************************************************
      SUBROUTINE XY2LLH (XI,YJ,XLAT,XLONG)
c
C**   ALBION D. TAYLOR, MARCH 19, 1982
c
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
c
      DIMENSION ZETA(3),ETA(3)
c
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
c
   40 XLONG=0.
      RETURN
c
      END
c*************************************************************************
      SUBROUTINE EPSHIF (IDTG,ALAT,ALON,ALAT12,ALON12,VEL,VEL12,STRMID)
c
C**   EPSHIF IS EASTERN PACIFIC SHIFOR INCLUDING DEPRS.
C**   IT HAS HOMOGENEOUS 2ND ORDER TERMS TO 1.0% ROV CUTOFF,
C**   BASED ON 1970-1987 DATA.	MADE 01/88 BY ACP.
c
      common /shifor/ ishifor( 11, 3)
c
      dimension ishfor (6)
      dimension WCHANG(6),WPROG(6),inday(13)
      DIMENSION C12(10),C24(10),C36(10),C48(10),C60(10),C72(10)         
c
      INTEGER*4 DAYNUM                                                  
      DOUBLE PRECISION C12,C24,C36,C48,C60,C72,P1,P2,P3,P4,P5,P6,P7
C
      CHARACTER*8 STRMID
c
      DATA INDAY/0,31,59,90,120,151,181,212,243,273,304,334,365/        
      DATA C12/-.6912588D+00,.2422006D+00, .2777518D+00,.3668967D-03,
     1	       .4983247D-03, .4698757D-02,-.2571267D-01,.2089339D-02,
     2         -.1305162D-02,.4762985D+02/                              
      DATA C24/-.1410459D+01,.4175249D+00, .7958590D+00,.7331509D-03,
     1		.2859806D-03,.9471405D-02,-.5050283D-01,.4312723D-02,
     2         -.5324955D-02,.9921691D+02/                              
      DATA C36/-.2164005D+01,.4616575D+00, .1291853D+01,.1099004D-02,
     1         -.6238143D-03,.1152570D-01,-.6813301D-01,.6890304D-02,   
     2         -.9012636D-02,.1555363D+03/                              
      DATA C48/-.2730543D+01,.3424764D+00, .1814229D+01,.1352651D-02,
     1         -.1594377D-02,.1016889D-01,-.7330770D-01,.9088275D-02,   
     2         -.1330736D-01,.2007760D+03/                              
      DATA C60/-.3137255D+01,.7369660D-01, .1921868D+01,.1493343D-02,
     1         -.1915669D-02,.4721941D-02,-.6673589D-01,.1098720D-01,   
     2         -.1459001D-01,.2381408D+03/                              
      DATA C72/-.3338384D+01,-.2580929D+00, .1924276D+01,.1481198D-02,
     1         -.2034402D-02,-.2579704D-02,-.5222275D-01,.1232012D-01,  
     2	       -.1543874D-01, .2610715D+03/
c
c**   Write the input parameter to the printer
c
      write (*,'('' EASTERN PACIFIC SHIFOR'',/)')
      write (*,'('' INPUT PARAMETERS FOR TROPICAL CYCLONE '',A,
     1 '' ON YMDH = '',i10.10,/)') STRMID, idtg
      write (*,'('' LATCUR = '',f5.1,'' N  LONCUR = '',f6.1,
     1 '' W  WNDCUR = '',f4.0,'' KT'',/,'' LATM12 = '',f5.1,
     2 '' N  LONM12 = '',f6.1,'' W  WNDM12 = '',f4.0,'' KT'',/)')
     3 alat, alon, vel, alat12, alon12, vel12
c
      DO 10 I = 1,6
         WCHANG(I) = -99.0
         WPROG(I) = -99.0
   10 continue
c
      JW    = VEL   + 0.5
      JWOLD = VEL12 + 0.5
      IF (JWOLD.LE.0) JWOLD = -99
      IF (VEL12.LE.0.) then
	  WRITE (6,1)
    1	  FORMAT (' EP SHIFOR NOT RUN...12HR OLD MAX WIND MISSING')
	  RETURN
      endif
c
C**   SPACE PREVIOUSLY OCCUPIED FOR NOT RUNNING DEPRESSION STAGE
C
      IYR = IDTG/1000000
      IMO = (IDTG - IYR*1000000)/10000
      IDA = (IDTG - IYR*1000000 - IMO*10000)/100
      DAYNUM = INDAY(IMO) + IDA
      IF (DAYNUM.LT.135.0) DAYNUM = 135.0
      IF (DAYNUM.GT.349.0) DAYNUM = 349.0
c
      RAD = 180.0/3.14159
      DX  = ALON - ALON12
      DY  = ALAT - ALAT12
      D2  = (ALAT + ALAT12)/2.0
      U   = - DX*60.0*COS(D2/RAD)/12.0
      V   = DY*60.0/12.0
c
      P1 = FLOAT(DAYNUM)
      P2 = ALAT
      P3 = ALON
      P4 = U
      P5 = V
      P6 = VEL
      P7 = VEL - VEL12
c
      WCHANG(1)=C12(1)*P3+C12(2)*P6+C12(3)*P7+C12(4)*P1*P6+C12(5)*P1*P7+
     1 C12(6)*P2*P3+C12(7)*P2*P6+C12(8)*P3*P3+C12(9)*P6*P7+C12(10)      
      WCHANG(2)=C24(1)*P3+C24(2)*P6+C24(3)*P7+C24(4)*P1*P6+C24(5)*P1*P7+
     1 C24(6)*P2*P3+C24(7)*P2*P6+C24(8)*P3*P3+C24(9)*P6*P7+C24(10)      
      WCHANG(3)=C36(1)*P3+C36(2)*P6+C36(3)*P7+C36(4)*P1*P6+C36(5)*P1*P7+
     1 C36(6)*P2*P3+C36(7)*P2*P6+C36(8)*P3*P3+C36(9)*P6*P7+C36(10)      
      WCHANG(4)=C48(1)*P3+C48(2)*P6+C48(3)*P7+C48(4)*P1*P6+C48(5)*P1*P7+
     1 C48(6)*P2*P3+C48(7)*P2*P6+C48(8)*P3*P3+C48(9)*P6*P7+C48(10)      
      WCHANG(5)=C60(1)*P3+C60(2)*P6+C60(3)*P7+C60(4)*P1*P6+C60(5)*P1*P7+
     1 C60(6)*P2*P3+C60(7)*P2*P6+C60(8)*P3*P3+C60(9)*P6*P7+C60(10)      
      WCHANG(6)=C72(1)*P3+C72(2)*P6+C72(3)*P7+C72(4)*P1*P6+C72(5)*P1*P7+
     1 C72(6)*P2*P3+C72(7)*P2*P6+C72(8)*P3*P3+C72(9)*P6*P7+C72(10)
c
      DO I = 1, 6
         WPROG(I) = VEL + WCHANG(I)
         IF (WPROG(I).LT.0.) WCHANG(I) = -VEL
         IF (WPROG(I).LT.0.) WPROG(I)  = 0.0
      enddo
c
      do i = 1, 6
         ishfor(i) = wprog(i) + 0.5
      enddo
      ivel = vel + 0.5
c
      do i = 1, 6
c
         ishifor( i + 1, 3 ) = ishfor(i)
c
      enddo   
c
      write ( *, '('' FORECAST INTENSITY (KT)'')' )
      WRITE ( *, 3 ) iVEL, ( ishfor(i), i = 1, 6 )
    3 FORMAT (/,' 00 HR = ',i3,/,' 12 HR = ',i3,/,' 24 HR = ',
     & i3,/,' 36 HR = ',i3,/,' 48 HR = ',i3,/,' 60 HR = ',i3,/,
     & ' 72 HR = ',i3,/)
c
      RETURN                                                            
      END
c***************************************************************************
      subroutine epshif5d(ymdh,elat,elon,elat12,elon12,vel,vel12,
     .     strmid)
c     
c     epshif5d
c
c     This subroutine calculates tropical cyclone in the eastern Pacific
c     intensities through 120 hours based upon climatology and persistence 
c     using tropical cyclone data during the years 1975-1999 for development.
c     Tropical cyclones used in this developmental dataset had initial 
c     positions south of 35N and east of 160W and were 50km from any 
c     coastline.  The linear regression model (one for each forecast time)
c     was created using the total change in intensity for each period 
c     (12-hr,....120-hr) from intial conditions as the predictand and 
c     35 predictors including and derived from julian day, latitude, 
c     longitude, zonal speed, meridional speed, current intensity the 
c     past 12-hour intensity trend.
c     
c     In the formulation of the model linear terms are first put into the
c     model using a forward stepping approach for the 12-hour forecast.   
c     The linear predictors chosen in this forward stepping process 
c     are then forced into the model and exposed to the 2nd order terms, 
c     which at this point are allowed to come into the model in a 
c     stepwise fashion.  A backward step is then performed to remove 
c     predictors that are no longer significant.  Then a final stepwise
c     stepping proceedure is performed possibly adding a removing predictors
c
c
c     Following the 12-hour forecast the predictors chosen for the previous
c     forecast period are then given preference in the selection process. 
c     Again, the predictors chosen in this forward stepping process 
c     are then forced into the model and exposed to the 2nd order terms, 
c     which at this point are allowed to come into the model in a 
c     stepwise fashion.  A backward pass through the data is then performed 
c     to remove predictors that are no longer significant. Followed by  
c     a final step that is stepwise. Probabilities were set at .000000001%.
c
c     J. Knaff (04/12/2001)
c
      common /shifor5/ ishifor5( 11, 3 )
      common /ep5coef/ scoef(10,36), avg(10,36), sdev(10,36)
c
c     dimension coeficients.
c
      parameter(nc=36)
      real p(36), forecast(10)
      double precision  dv (10)

c
c     dimension input.
c
      integer ymdh,daynum
      integer iwnd(10)
      character*6 strmid
      character*8 aymdh
      real elat, elon, elat12, elon12, vel, vel12
c
c     intialize to zero
c
      do i=1,10
         dv(i)=0.0
         iwnd(i)=0
      end do
c    
c     write input parameters out to printer
c
      write (*,'('' EASTERN PACIFIC SHIFOR5'',/)')
      write (*,1001)strmid,ymdh
 1001 format('INPUT PARAMETERS FOR TROPICAL CYCLONE ',A,
     & ' ON YMDH = ',I10.10,/) 
      write (*,1002)elat,elon,vel,elat12,elon12,vel12
 1002 format(' LA0   = ',F5.1,' N  LO0   = ',F6.1,
     .     ' W  WND0   = ',F4.0,' KT',/,' LAM12 = ',F5.1,
     .     ' N  LOM12 = ',F6.1,' W  WNDM12 = ',F4.0,' KT',/)

c 
c     check for system intensity requirements.
c
      if (vel.lt.15.0.OR.vel12.lt.15.0) then
          write (6,1)
 1        format (/,' EPSHIF NOT RUN DUE TO AT LEAST ONE INPUT WIND LESS
     .THAN 15 KT')
          return
      endif
c
c     create predictor pool (first order terms, squares, and 
c     co-variances terms)
c
c     p1 = absolute value of (julian day - 238)
c     p2 = lat
c     p3 = lon
c     p4 = u ! zonal speed of the storm over the last 12 hours
c     p5 = v ! meridional speed of the storm over the last 12 hours
c     p6 = vmax
c     p7 = delta vmax
c
c     calculate julian day
c
      iyear  = ymdh/1000000
      imonth = (ymdh - iyear*1000000)/10000
      iday   = (ymdh - iyear*1000000 - imonth*10000)/100
      call jday(imonth,iday,iyear,julday)
c
c     assign predictor values from the input data
c
      p(1) = dble(abs(julday-238))
      p(2) = dble(elat)
      p(3) =dble(elon)
      avglat=(elat+elat12)/2.0
      p(4) =dble((elon-elon12)* (-60.0)/ 12.0 * 
     .     COS(rad*avglat))
      p(5)=dble((elat-elat12)*60./12.)
      p(6)=dble(vel)
      p(7)=dble(vel-vel12)
      p(8)=p(1)**2                !p1*p1  
      p(9)=p(1)*p(2)              !p1*p2
      p(10)=p(1)*p(3)             !p1*p3  
      p(11)=p(1)*p(4)             !etc....
      p(12)=p(1)*p(5)
      p(13)=p(1)*p(6)
      p(14)=p(1)*p(7)
      p(15)=p(2)**2
      p(16)=p(2)*p(3)
      p(17)=p(2)*p(4)
      p(18)=P(2)*p(5)
      p(19)=p(2)*p(6)
      p(20)=p(2)*p(7)
      p(21)=p(3)**2
      p(22)=p(3)*p(4)
      p(23)=p(3)*p(5)
      p(24)=p(3)*p(6)
      p(25)=p(3)*p(7)
      p(26)=p(4)**2
      p(27)=p(4)*p(5)
      p(28)=p(4)*p(6)
      p(29)=p(4)*p(7)
      p(30)=p(5)**2
      p(31)=p(5)*p(6)
      p(32)=p(5)*p(7)
      p(33)=p(6)**2
      p(34)=p(6)*p(7)
      p(35)=p(7)**2
      p(36)=vel
c
c     calculate the predicted incremental change in velocity
c     
c     
      do i=1,10
         dv(i)=0.0 ! intitialize array to zero.
         do j=1,35
            dv(i)=dv(i)+dble(scoef(i,j)*((p(j)-avg(i,j))/sdev(i,j)))
         end do
         dv(i)=dv(i)*dble(sdev(i,36)) + dble(avg(i,36))
      end do
c
c     
c     construct forecast intensities
c
      forecast(1)=p(36)+dv(1)
      
      do i=1,10
         forecast(i)= p(36)+sngl(dv(i))
      end do
      do i=1,10
         if (forecast(i).lt.0.0)forecast(i)=0.0
         iwnd(i)=nint(forecast(i))
      end do
c
c     fill ishifor array for the atcf
c
      ishifor5(1,3)=nint(vel)
      do i = 1, 10
         ishifor5( i + 1, 3 ) = iwnd(i)
      enddo   

      ivel = nint(vel)
      write ( *, '('' FORECAST INTENSITY (KT)'')' )
      WRITE ( *, 2 ) ivel, ( iwnd(i), i = 1, 10 )
    2 FORMAT (/,' 00 HR = ',I5,/,' 12 HR = ',I5,/,' 24 HR = ',
     & I5,/,' 36 HR = ',I5,/,' 48 HR = ',I5,/,' 60 HR = ',i5,/,
     & ' 72 HR = ',I5,/,' 84 HR = ',I5,/,' 96 HR = ',I5,/,
     & '108 HR = ',I5,/,'120 HR = ',I5,/)
c
      return
      end
c************************************************************************
      block data
c
c     This subprogram contains the standardized coefficients, means and
c     standard deviations of the predictors used in the eastern Pacific
c     version of the Statistical Hurricane Intensity Forecast.  These
c     data are used in subroutine epshif5d and are passed via a common
c     block.
c
c     scoef    are the standardized coefficients
c     avg      are the averages
c     sdev     are the standard deviations
c
c
      common /ep5coef/ epscoef(10,36), epavg(10,36), epsdev(10,36)
      common /al5coef/ alscoef(10,36), alavg(10,36), alsdev(10,36)
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
c
      data (epscoef( 1,j),j=1,36) / 0.0000000E+00,-0.1823524E+00,
     .-0.6025346E-01, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.7614017E+00, 0.0000000E+00,-0.9648295E-01, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2989867E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2441196E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 1,j),j=1,36) / 0.3409045E+02, 0.1647778E+02,
     . 0.1194100E+03,-0.7575877E+01, 0.2703427E+01, 0.6359764E+02,
     . 0.8415730E+00, 0.1709157E+04, 0.5391900E+03, 0.3987097E+04,
     .-0.2346845E+03, 0.8988298E+02, 0.1862021E+04, 0.3237899E+02,
     . 0.2843427E+03, 0.1978615E+04,-0.1227261E+03, 0.4757833E+02,
     . 0.9302553E+03,-0.9259438E+00, 0.1446544E+05,-0.9215050E+03,
     . 0.3176249E+03, 0.6665289E+04, 0.5694735E+02, 0.8057443E+02,
     .-0.1971690E+02,-0.4274374E+03,-0.7634565E+01, 0.1694525E+02,
     . 0.1703698E+03, 0.4083034E+01, 0.3833088E+04, 0.7290146E+02,
     . 0.1182917E+03,-0.6213483E-01/
      data (epsdev( 1,j),j=1,36) / 0.2338930E+02, 0.3581487E+01,
     . 0.1437713E+02, 0.4814886E+01, 0.3104484E+01, 0.2800452E+03,
     . 0.1084420E+02, 0.2377903E+04, 0.3472305E+03, 0.2704805E+04,
     . 0.2426896E+03, 0.1372968E+03, 0.1545159E+04, 0.4306967E+03,
     . 0.1266151E+03, 0.5390896E+03, 0.8227717E+02, 0.6035736E+02,
     . 0.5446276E+03, 0.1866596E+03, 0.3603070E+04, 0.6238622E+03,
     . 0.3774387E+03, 0.3333336E+04, 0.1306984E+04, 0.7470361E+02,
     . 0.2940368E+02, 0.4714602E+03, 0.9879948E+02, 0.2882326E+02,
     . 0.3413755E+03, 0.4834698E+02, 0.3712495E+04, 0.2072621E+04,
     . 0.2253573E+03, 0.1101109E+02/
      data (epscoef( 2,j),j=1,36) / 0.0000000E+00,-0.2201037E+00,
     .-0.1125746E+01, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.7669960E+00, 0.0000000E+00,-0.1205761E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.3805355E+00, 0.9819010E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.3280108E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 2,j),j=1,36) / 0.3388374E+02, 0.1621464E+02,
     . 0.1190225E+03,-0.7737213E+01, 0.2666646E+01, 0.6608255E+02,
     . 0.1375492E+01, 0.1694369E+04, 0.5275113E+03, 0.3950797E+04,
     .-0.2393237E+03, 0.8834578E+02, 0.1907476E+04, 0.5036208E+02,
     . 0.2745901E+03, 0.1940280E+04,-0.1240043E+03, 0.4571776E+02,
     . 0.9503964E+03, 0.8596223E+01, 0.1436974E+05,-0.9367046E+03,
     . 0.3124024E+03, 0.6867745E+04, 0.1217556E+03, 0.8150956E+02,
     .-0.2046919E+02,-0.4495492E+03,-0.1176072E+02, 0.1598613E+02,
     . 0.1734764E+03, 0.5824803E+01, 0.4036648E+04, 0.9347293E+02,
     . 0.1184358E+03,-0.3540846E+00/
      data (epsdev( 2,j),j=1,36) / 0.2337367E+02, 0.3417155E+01,
     . 0.1426190E+02, 0.4652715E+01, 0.2979298E+01, 0.2928763E+03,
     . 0.1079621E+02, 0.2404624E+04, 0.3395607E+03, 0.2700929E+04,
     . 0.2367192E+03, 0.1330576E+03, 0.1568953E+04, 0.4286487E+03,
     . 0.1185794E+03, 0.5170034E+03, 0.7846817E+02, 0.5543961E+02,
     . 0.5550459E+03, 0.1833025E+03, 0.3568410E+04, 0.6010082E+03,
     . 0.3588002E+03, 0.3373653E+04, 0.1297714E+04, 0.7369955E+02,
     . 0.2833205E+02, 0.4820746E+03, 0.9938897E+02, 0.2604367E+02,
     . 0.3510014E+03, 0.4619587E+02, 0.3774183E+04, 0.2161811E+04,
     . 0.2182329E+03, 0.1938118E+02/
      data (epscoef( 3,j),j=1,36) / 0.0000000E+00,-0.2303735E+00,
     .-0.1473419E+01, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.7107538E+00, 0.0000000E+00,-0.1389359E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.4188341E+00, 0.1300377E+01, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.6600728E-01,
     . 0.0000000E+00, 0.0000000E+00,-0.3934926E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 3,j),j=1,36) / 0.3368899E+02, 0.1595987E+02,
     . 0.1186078E+03,-0.7856443E+01, 0.2622831E+01, 0.6849837E+02,
     . 0.2040401E+01, 0.1680311E+04, 0.5164424E+03, 0.3916439E+04,
     .-0.2425100E+03, 0.8671753E+02, 0.1946771E+04, 0.7170458E+02,
     . 0.2654435E+03, 0.1902633E+04,-0.1242365E+03, 0.4395626E+02,
     . 0.9662881E+03, 0.2062413E+02, 0.1426791E+05,-0.9467457E+03,
     . 0.3062754E+03, 0.7042070E+04, 0.2034481E+03, 0.8239523E+02,
     .-0.2073621E+02,-0.4684744E+03,-0.1724166E+02, 0.1511958E+02,
     . 0.1754523E+03, 0.7855410E+01, 0.4233243E+04, 0.1224204E+03,
     . 0.1156651E+03,-0.9270607E+00/
      data (epsdev( 3,j),j=1,36) / 0.2335459E+02, 0.3275283E+01,
     . 0.1414661E+02, 0.4546905E+01, 0.2870793E+01, 0.3072913E+03,
     . 0.1056016E+02, 0.2435531E+04, 0.3325807E+03, 0.2700756E+04,
     . 0.2341398E+03, 0.1308612E+03, 0.1594228E+04, 0.4169710E+03,
     . 0.1119010E+03, 0.4971324E+03, 0.7578139E+02, 0.5153394E+02,
     . 0.5683723E+03, 0.1760623E+03, 0.3533794E+04, 0.5863201E+03,
     . 0.3425258E+03, 0.3432086E+04, 0.1268322E+04, 0.7296887E+02,
     . 0.2785581E+02, 0.4960866E+03, 0.9846447E+02, 0.2392651E+02,
     . 0.3619989E+03, 0.4294414E+02, 0.3852650E+04, 0.2257165E+04,
     . 0.2120755E+03, 0.2645941E+02/
      data (epscoef( 4,j),j=1,36) / 0.0000000E+00,-0.6944878E+00,
     .-0.1674557E+01, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.6274028E+00, 0.0000000E+00,-0.1514233E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.5581393E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.4049150E+00, 0.1250209E+01, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.7471567E-01,
     . 0.0000000E+00, 0.0000000E+00,-0.4392256E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 4,j),j=1,36) / 0.3350910E+02, 0.1571008E+02,
     . 0.1181326E+03,-0.7945663E+01, 0.2557487E+01, 0.7075982E+02,
     . 0.2670429E+01, 0.1667663E+04, 0.5056566E+03, 0.3882390E+04,
     .-0.2444269E+03, 0.8436892E+02, 0.1976468E+04, 0.9222919E+02,
     . 0.2567841E+03, 0.1864842E+04,-0.1238269E+03, 0.4194849E+02,
     . 0.9755518E+03, 0.3153982E+02, 0.1415158E+05,-0.9529552E+03,
     . 0.2972958E+03, 0.7171507E+04, 0.2793818E+03, 0.8310629E+02,
     .-0.2060539E+02,-0.4832446E+03,-0.2235800E+02, 0.1434458E+02,
     . 0.1753482E+03, 0.9751166E+01, 0.4404444E+04, 0.1549809E+03,
     . 0.1150295E+03,-0.1737848E+01/
      data (epsdev( 4,j),j=1,36) / 0.2334276E+02, 0.3158935E+01,
     . 0.1401045E+02, 0.4469423E+01, 0.2793746E+01, 0.3236109E+03,
     . 0.1038819E+02, 0.2472404E+04, 0.3255645E+03, 0.2702188E+04,
     . 0.2325489E+03, 0.1293590E+03, 0.1617585E+04, 0.4053358E+03,
     . 0.1064771E+03, 0.4795868E+03, 0.7352919E+02, 0.4875947E+02,
     . 0.5826815E+03, 0.1700602E+03, 0.3490472E+04, 0.5741495E+03,
     . 0.3301058E+03, 0.3499914E+04, 0.1247264E+04, 0.7179615E+02,
     . 0.2745527E+02, 0.5120160E+03, 0.9851597E+02, 0.2227744E+02,
     . 0.3742758E+03, 0.4073142E+02, 0.3942398E+04, 0.2366353E+04,
     . 0.2132211E+03, 0.3194976E+02/
      data (epscoef( 5,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.6812104E+00, 0.0000000E+00,-0.1495004E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2898585E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.5135095E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2273493E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.8122859E-01,
     . 0.0000000E+00, 0.0000000E+00,-0.3064732E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 5,j),j=1,36) / 0.3327280E+02, 0.1547144E+02,
     . 0.1176365E+03,-0.8025509E+01, 0.2476860E+01, 0.7294497E+02,
     . 0.3328004E+01, 0.1649972E+04, 0.4945912E+03, 0.3841616E+04,
     .-0.2455439E+03, 0.8077078E+02, 0.1994411E+04, 0.1132713E+03,
     . 0.2486167E+03, 0.1828098E+04,-0.1232210E+03, 0.3979703E+02,
     . 0.9797526E+03, 0.4265947E+02, 0.1403067E+05,-0.9581615E+03,
     . 0.2865943E+03, 0.7265209E+04, 0.3586360E+03, 0.8392738E+02,
     .-0.2025503E+02,-0.4949773E+03,-0.2786637E+02, 0.1355154E+02,
     . 0.1738348E+03, 0.1159021E+02, 0.4546875E+04, 0.1918206E+03,
     . 0.1140813E+03,-0.2786772E+01/
      data (epsdev( 5,j),j=1,36) / 0.2330202E+02, 0.3041842E+01,
     . 0.1386926E+02, 0.4418356E+01, 0.2723592E+01, 0.3420756E+03,
     . 0.1015003E+02, 0.2512109E+04, 0.3184644E+03, 0.2702379E+04,
     . 0.2311652E+03, 0.1254157E+03, 0.1632792E+04, 0.3962381E+03,
     . 0.1006864E+03, 0.4603183E+03, 0.7158336E+02, 0.4644048E+02,
     . 0.5971776E+03, 0.1630912E+03, 0.3445141E+04, 0.5664914E+03,
     . 0.3198441E+03, 0.3571135E+04, 0.1213577E+04, 0.7166328E+02,
     . 0.2698355E+02, 0.5301886E+03, 0.9685469E+02, 0.2155422E+02,
     . 0.3892121E+03, 0.3890517E+02, 0.4031562E+04, 0.2486870E+04,
     . 0.2124573E+03, 0.3609719E+02/
      data (epscoef( 6,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.6261557E+00, 0.0000000E+00,-0.1497080E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2719499E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.5162974E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2741849E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.7807224E-01,
     . 0.0000000E+00, 0.0000000E+00,-0.2952774E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 6,j),j=1,36) / 0.3309105E+02, 0.1524456E+02,
     . 0.1170965E+03,-0.8085144E+01, 0.2390498E+01, 0.7491747E+02,
     . 0.3891728E+01, 0.1636725E+04, 0.4848110E+03, 0.3805275E+04,
     .-0.2458836E+03, 0.7685264E+02, 0.2000089E+04, 0.1311931E+03,
     . 0.2410369E+03, 0.1792407E+04,-0.1222881E+03, 0.3766839E+02,
     . 0.9766734E+03, 0.5174439E+02, 0.1390026E+05,-0.9611770E+03,
     . 0.2751466E+03, 0.7302574E+04, 0.4254768E+03, 0.8465199E+02,
     .-0.1974076E+02,-0.5023709E+03,-0.3289441E+02, 0.1277484E+02,
     . 0.1704612E+03, 0.1295930E+02, 0.4633386E+04, 0.2234049E+03,
     . 0.1132493E+03,-0.3925989E+01/
      data (epsdev( 6,j),j=1,36) / 0.2327682E+02, 0.2939717E+01,
     . 0.1373689E+02, 0.4391593E+01, 0.2657386E+01, 0.3626381E+03,
     . 0.9905671E+01, 0.2560954E+04, 0.3121063E+03, 0.2704248E+04,
     . 0.2283015E+03, 0.1202093E+03, 0.1636206E+04, 0.3908052E+03,
     . 0.9559690E+02, 0.4429090E+03, 0.7007668E+02, 0.4442154E+02,
     . 0.6100070E+03, 0.1564196E+03, 0.3400547E+04, 0.5635516E+03,
     . 0.3103789E+03, 0.3626780E+04, 0.1178258E+04, 0.7209558E+02,
     . 0.2665871E+02, 0.5498324E+03, 0.9543129E+02, 0.2097211E+02,
     . 0.4054575E+03, 0.3702311E+02, 0.4106859E+04, 0.2619981E+04,
     . 0.2103640E+03, 0.3879220E+02/
      data (epscoef( 7,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.5853452E+00, 0.0000000E+00,-0.1406750E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2364586E+00, 0.0000000E+00,-0.8097417E-01,
     . 0.0000000E+00,-0.4477453E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.3301889E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.8612577E-01,-0.2660320E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 7,j),j=1,36) / 0.3287039E+02, 0.1503177E+02,
     . 0.1165874E+03,-0.8148692E+01, 0.2312446E+01, 0.7469045E+02,
     . 0.4279135E+01, 0.1621358E+04, 0.4750126E+03, 0.3765667E+04,
     .-0.2458547E+03, 0.7305763E+02, 0.1991023E+04, 0.1410150E+03,
     . 0.2340843E+03, 0.1759192E+04,-0.1215257E+03, 0.3584299E+02,
     . 0.9667653E+03, 0.5768961E+02, 0.1377877E+05,-0.9648518E+03,
     . 0.2649892E+03, 0.7298661E+04, 0.4706489E+03, 0.8548945E+02,
     .-0.1926236E+02,-0.5090874E+03,-0.3672544E+02, 0.1212880E+02,
     . 0.1640531E+03, 0.1378406E+02, 0.4672013E+04, 0.2449278E+03,
     . 0.1147646E+03,-0.4972365E+01/
      data (epsdev( 7,j),j=1,36) / 0.2325965E+02, 0.2851655E+01,
     . 0.1364507E+02, 0.4369481E+01, 0.2604390E+01, 0.3572350E+03,
     . 0.9822130E+01, 0.2620210E+04, 0.3063521E+03, 0.2710421E+04,
     . 0.2250002E+03, 0.1148629E+03, 0.1627826E+04, 0.3834453E+03,
     . 0.9109157E+02, 0.4275875E+03, 0.6883896E+02, 0.4284667E+02,
     . 0.6080621E+03, 0.1531289E+03, 0.3367195E+04, 0.5614836E+03,
     . 0.3026992E+03, 0.3670575E+04, 0.1166571E+04, 0.7268656E+02,
     . 0.2630556E+02, 0.5491028E+03, 0.9548569E+02, 0.2073056E+02,
     . 0.3987535E+03, 0.3619340E+02, 0.4166875E+04, 0.2772995E+04,
     . 0.2160317E+03, 0.4040804E+02/
      data (epscoef( 8,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.1366803E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2516920E+00, 0.0000000E+00,-0.9944827E-01,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2916846E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.3086647E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 8,j),j=1,36) / 0.3267741E+02, 0.1483578E+02,
     . 0.1161084E+03,-0.8193725E+01, 0.2257631E+01, 0.7162686E+02,
     . 0.4580464E+01, 0.1611289E+04, 0.4663680E+03, 0.3730107E+04,
     .-0.2449940E+03, 0.7036105E+02, 0.1976781E+04, 0.1472987E+03,
     . 0.2277729E+03, 0.1728568E+04,-0.1205942E+03, 0.3454231E+02,
     . 0.9528255E+03, 0.6192274E+02, 0.1366508E+05,-0.9661400E+03,
     . 0.2576956E+03, 0.7274969E+04, 0.5052988E+03, 0.8597862E+02,
     .-0.1888309E+02,-0.5160939E+03,-0.3935513E+02, 0.1167900E+02,
     . 0.1558802E+03, 0.1408596E+02, 0.4682938E+04, 0.2563573E+03,
     . 0.1164193E+03,-0.5997314E+01/
      data (epsdev( 8,j),j=1,36) / 0.2331542E+02, 0.2770294E+01,
     . 0.1356292E+02, 0.4341210E+01, 0.2565874E+01, 0.3118126E+03,
     . 0.9770463E+01, 0.2700221E+04, 0.3019180E+03, 0.2728907E+04,
     . 0.2217190E+03, 0.1108056E+03, 0.1614140E+04, 0.3789682E+03,
     . 0.8680218E+02, 0.4127718E+03, 0.6735981E+02, 0.4158892E+02,
     . 0.5858888E+03, 0.1504650E+03, 0.3336576E+04, 0.5575274E+03,
     . 0.2972206E+03, 0.3702202E+04, 0.1157438E+04, 0.7301750E+02,
     . 0.2609112E+02, 0.5195650E+03, 0.9562437E+02, 0.2091177E+02,
     . 0.3571355E+03, 0.3537364E+02, 0.4208102E+04, 0.2944192E+04,
     . 0.2209439E+03, 0.4131228E+02/
      data (epscoef( 9,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.1245924E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.2065900E+00, 0.0000000E+00,-0.1119146E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.3103650E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.3156649E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg( 9,j),j=1,36) / 0.3256700E+02, 0.1464551E+02,
     . 0.1155945E+03,-0.8221828E+01, 0.2212730E+01, 0.6724372E+02,
     . 0.4851480E+01, 0.1610180E+04, 0.4590651E+03, 0.3702369E+04,
     .-0.2446719E+03, 0.6839015E+02, 0.1959760E+04, 0.1568171E+03,
     . 0.2217126E+03, 0.1698372E+04,-0.1193639E+03, 0.3350007E+02,
     . 0.9351116E+03, 0.6553180E+02, 0.1354381E+05,-0.9647840E+03,
     . 0.2514245E+03, 0.7223625E+04, 0.5354881E+03, 0.8602952E+02,
     .-0.1838713E+02,-0.5213773E+03,-0.4177164E+02, 0.1129564E+02,
     . 0.1469301E+03, 0.1391820E+02, 0.4667659E+04, 0.2648191E+03,
     . 0.1178677E+03,-0.7068398E+01/
      data (epsdev( 9,j),j=1,36) / 0.2344619E+02, 0.2687708E+01,
     . 0.1348207E+02, 0.4293741E+01, 0.2530070E+01, 0.2366000E+03,
     . 0.9713761E+01, 0.2796710E+04, 0.2982126E+03, 0.2756915E+04,
     . 0.2191171E+03, 0.1077691E+03, 0.1599424E+04, 0.3733430E+03,
     . 0.8225807E+02, 0.3977646E+03, 0.6485299E+02, 0.4052077E+02,
     . 0.5554506E+03, 0.1482124E+03, 0.3306920E+04, 0.5491180E+03,
     . 0.2916813E+03, 0.3740634E+04, 0.1145511E+04, 0.7211736E+02,
     . 0.2558451E+02, 0.4751219E+03, 0.9594357E+02, 0.2122226E+02,
     . 0.2924824E+03, 0.3480763E+02, 0.4253586E+04, 0.3133444E+04,
     . 0.2277168E+03, 0.4168740E+02/
      data (epscoef(10,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.6412943E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.1008322E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.1808974E+00, 0.0000000E+00,-0.9930872E-01,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (epavg(10,j),j=1,36) / 0.3244245E+02, 0.1446961E+02,
     . 0.1151464E+03,-0.8219359E+01, 0.2156941E+01, 0.6130843E+02,
     . 0.5112215E+01, 0.1608799E+04, 0.4521713E+03, 0.3675283E+04,
     .-0.2431198E+03, 0.6584370E+02, 0.1934150E+04, 0.1645114E+03,
     . 0.2161679E+03, 0.1671032E+04,-0.1178861E+03, 0.3231959E+02,
     . 0.9146586E+03, 0.6895284E+02, 0.1344060E+05,-0.9605197E+03,
     . 0.2440476E+03, 0.7157191E+04, 0.5657189E+03, 0.8555419E+02,
     .-0.1777317E+02,-0.5241910E+03,-0.4391199E+02, 0.1068508E+02,
     . 0.1363673E+03, 0.1368596E+02, 0.4633374E+04, 0.3485460E+03,
     . 0.1163851E+03,-0.8081436E+01/
      data (epsdev(10,j),j=1,36) / 0.2358951E+02, 0.2607800E+01,
     . 0.1348963E+02, 0.4242887E+01, 0.2456545E+01, 0.2957923E+02,
     . 0.9501540E+01, 0.2905742E+04, 0.2946989E+03, 0.2792864E+04,
     . 0.2139260E+03, 0.1052045E+03, 0.1575003E+04, 0.3630870E+03,
     . 0.7811045E+02, 0.3847938E+03, 0.6279043E+02, 0.3821323E+02,
     . 0.5127150E+03, 0.1431177E+03, 0.3302588E+04, 0.5408215E+03,
     . 0.2809234E+03, 0.3784311E+04, 0.1114523E+04, 0.7099328E+02,
     . 0.2340798E+02, 0.4078613E+03, 0.9483244E+02, 0.1876076E+02,
     . 0.1704033E+03, 0.3395292E+02, 0.4303698E+04, 0.8312715E+03,
     . 0.2208521E+03, 0.4166153E+02/
cc       end


c*****************************************************************************
cc      block data
c
c     block data for the standardized coeficients to the 5-day
c     Atlantic SHIFOR
c
c     These are used by alshif5d and passed via a common block
c     initialized in this subprogram.  The common block is not passed
c     to the main program.
c
c     scoef    are the standardized coeficients
c     avg      are the averages
c     sdev     are the standard deviations.
c
c
cc      common /al5coef/ alscoef(10,36), alavg(10,36), alsdev(10,36)
c
      data (alscoef( 1,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.9632107E-01, 0.2161774E+00, 0.0000000E+00,-0.2598887E+00,
     . 0.6619257E+00,-0.6903946E-01, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.3840485E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.2655196E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 1,j),j=1,36) / 0.6924230E+00, 0.2501092E+02,
     . 0.6001072E+02,-0.2517827E+01, 0.4779600E+01, 0.5636170E+02,
     . 0.2587011E+01, 0.1030277E+04, 0.1775327E+02, 0.4254318E+02,
     . 0.3506200E+02,-0.1217535E+02, 0.1154956E+03,-0.1672390E+02,
     . 0.6990111E+03, 0.1512090E+04,-0.2923416E+01, 0.1318952E+03,
     . 0.1450323E+04, 0.5226493E+02, 0.3901107E+04,-0.1370406E+03,
     . 0.2816506E+03, 0.3394556E+04, 0.1688047E+03, 0.9963890E+02,
     .-0.9566036E-01,-0.1150216E+03,-0.1612303E+02, 0.4871619E+02,
     . 0.2915584E+03, 0.1450799E+02, 0.3791872E+04, 0.1823332E+03,
     . 0.8294604E+02, 0.2005495E+01/
      data (alsdev( 1,j),j=1,36) / 0.3209314E+02, 0.8571875E+01,
     . 0.1731675E+02, 0.9659969E+01, 0.5086838E+01, 0.2480592E+02,
     . 0.8733048E+01, 0.1864341E+04, 0.8357047E+03, 0.2234280E+04,
     . 0.2879513E+03, 0.2154462E+03, 0.1749152E+04, 0.3003741E+03,
     . 0.4446778E+03, 0.6461969E+03, 0.2631858E+03, 0.1692676E+03,
     . 0.8461565E+03, 0.2281288E+03, 0.2127881E+04, 0.5451351E+03,
     . 0.3145661E+03, 0.1852198E+04, 0.5793061E+03, 0.1301999E+03,
     . 0.7732862E+02, 0.5875003E+03, 0.9362686E+02, 0.7837893E+02,
     . 0.3577816E+03, 0.6779141E+02, 0.3409085E+04, 0.6547117E+03,
     . 0.1612456E+03, 0.9235003E+01/
      data (alscoef( 2,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.1233280E+00, 0.2059798E+00, 0.0000000E+00,-0.2399135E+00,
     . 0.7064717E+00,-0.1008747E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.1276496E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.3583669E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.3909434E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 2,j),j=1,36) / 0.9079197E+00, 0.2451084E+02,
     . 0.5893240E+02,-0.3085352E+01, 0.4501705E+01, 0.5650076E+02,
     . 0.2622774E+01, 0.9678882E+03, 0.2445280E+02, 0.7167412E+02,
     . 0.3633494E+02,-0.1068501E+02, 0.1269655E+03,-0.1328003E+02,
     . 0.6709643E+03, 0.1464025E+04,-0.2066254E+02, 0.1185758E+03,
     . 0.1428452E+04, 0.5308390E+02, 0.3755662E+04,-0.1573582E+03,
     . 0.2618678E+03, 0.3339356E+04, 0.1592436E+03, 0.9354892E+02,
     .-0.6658569E+01,-0.1436312E+03,-0.1608299E+02, 0.4283905E+02,
     . 0.2740909E+03, 0.1404197E+02, 0.3795095E+04, 0.1763668E+03,
     . 0.7905362E+02, 0.3726980E+01/
      data (alsdev( 2,j),j=1,36) / 0.3110060E+02, 0.8378330E+01,
     . 0.1681333E+02, 0.9167630E+01, 0.4751629E+01, 0.2455349E+02,
     . 0.8496373E+01, 0.1768235E+04, 0.7934583E+03, 0.2132501E+04,
     . 0.2678891E+03, 0.1941161E+03, 0.1705528E+04, 0.2929895E+03,
     . 0.4255700E+03, 0.6396952E+03, 0.2369832E+03, 0.1480606E+03,
     . 0.8353543E+03, 0.2164446E+03, 0.2038278E+04, 0.5116897E+03,
     . 0.2930400E+03, 0.1768569E+04, 0.5501223E+03, 0.1166377E+03,
     . 0.6353190E+02, 0.5536301E+03, 0.8621957E+02, 0.6173920E+02,
     . 0.3307446E+03, 0.5880326E+02, 0.3329759E+04, 0.6239390E+03,
     . 0.1531375E+03, 0.1532608E+02/
      data (alscoef( 3,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.1334133E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.6672866E+00,-0.1210680E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.2524992E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.5450201E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.1718453E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.4152353E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 3,j),j=1,36) / 0.9616966E+00, 0.2404943E+02,
     . 0.5779779E+02,-0.3558863E+01, 0.4308050E+01, 0.5671110E+02,
     . 0.2737719E+01, 0.9210535E+03, 0.2779111E+02, 0.8878762E+02,
     . 0.3805056E+02,-0.1038823E+02, 0.1297228E+03,-0.1325298E+02,
     . 0.6464169E+03, 0.1417209E+04,-0.3392802E+02, 0.1093273E+03,
     . 0.1409962E+04, 0.5483954E+02, 0.3607683E+04,-0.1723524E+03,
     . 0.2469319E+03, 0.3293460E+04, 0.1577506E+03, 0.9111264E+02,
     .-0.1095332E+02,-0.1681860E+03,-0.1828591E+02, 0.3958164E+02,
     . 0.2626406E+03, 0.1389569E+02, 0.3815360E+04, 0.1803387E+03,
     . 0.7714023E+02, 0.4966674E+01/
      data (alsdev( 3,j),j=1,36) / 0.3033690E+02, 0.8249646E+01,
     . 0.1634490E+02, 0.8857997E+01, 0.4585509E+01, 0.2448144E+02,
     . 0.8346269E+01, 0.1721265E+04, 0.7590904E+03, 0.2051263E+04,
     . 0.2579913E+03, 0.1808050E+03, 0.1664844E+04, 0.2869225E+03,
     . 0.4123503E+03, 0.6362572E+03, 0.2202684E+03, 0.1374561E+03,
     . 0.8296448E+03, 0.2083708E+03, 0.1948476E+04, 0.4887198E+03,
     . 0.2799759E+03, 0.1721974E+04, 0.5274450E+03, 0.1109338E+03,
     . 0.5723892E+02, 0.5324178E+03, 0.8228619E+02, 0.5533614E+02,
     . 0.3181781E+03, 0.5351896E+02, 0.3303091E+04, 0.6109392E+03,
     . 0.1502984E+03, 0.2018737E+02/
      data (alscoef( 4,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.1179411E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.5688543E+00,-0.1263167E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.3047682E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.6389252E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.1818729E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.3632210E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 4,j),j=1,36) / 0.8890815E+00, 0.2363174E+02,
     . 0.5672563E+02,-0.3959007E+01, 0.4171206E+01, 0.5699431E+02,
     . 0.2956177E+01, 0.8737126E+03, 0.2832931E+02, 0.9426695E+02,
     . 0.3968130E+02,-0.1056524E+02, 0.1285152E+03,-0.1212280E+02,
     . 0.6245836E+03, 0.1374201E+04,-0.4443031E+02, 0.1024761E+03,
     . 0.1394454E+04, 0.5930000E+02, 0.3471278E+04,-0.1841963E+03,
     . 0.2358062E+03, 0.3260008E+04, 0.1639787E+03, 0.9053625E+02,
     .-0.1423454E+02,-0.1899361E+03,-0.2018777E+02, 0.3704388E+02,
     . 0.2550115E+03, 0.1441322E+02, 0.3847742E+04, 0.1924855E+03,
     . 0.7592820E+02, 0.5805893E+01/
      data (alsdev( 4,j),j=1,36) / 0.2954891E+02, 0.8132701E+01,
     . 0.1592306E+02, 0.8653384E+01, 0.4432809E+01, 0.2448550E+02,
     . 0.8197918E+01, 0.1667888E+04, 0.7266108E+03, 0.1972593E+04,
     . 0.2514733E+03, 0.1682396E+03, 0.1624908E+04, 0.2809930E+03,
     . 0.4014341E+03, 0.6329095E+03, 0.2091046E+03, 0.1281973E+03,
     . 0.8236214E+03, 0.2017373E+03, 0.1863299E+04, 0.4736634E+03,
     . 0.2677355E+03, 0.1698982E+04, 0.5058230E+03, 0.1072277E+03,
     . 0.5339523E+02, 0.5209970E+03, 0.8075079E+02, 0.5054678E+02,
     . 0.3098015E+03, 0.5224454E+02, 0.3286008E+04, 0.5994625E+03,
     . 0.1427729E+03, 0.2406040E+02/
      data (alscoef( 5,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.1066351E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.4361093E+00,-0.1229526E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.3588182E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.7048543E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.7875312E-01,
     . 0.0000000E+00,-0.1810176E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.2748392E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 5,j),j=1,36) / 0.7411598E+00, 0.2323304E+02,
     . 0.5587768E+02,-0.4325152E+01, 0.4093352E+01, 0.5715955E+02,
     . 0.3132390E+01, 0.8297267E+03, 0.2728141E+02, 0.9450549E+02,
     . 0.4206970E+02,-0.1141570E+02, 0.1228300E+03,-0.1365545E+02,
     . 0.6040857E+03, 0.1336892E+04,-0.5336236E+02, 0.9788639E+02,
     . 0.1375858E+04, 0.6265878E+02, 0.3368683E+04,-0.1953185E+03,
     . 0.2288874E+03, 0.3232563E+04, 0.1698837E+03, 0.9092222E+02,
     .-0.1654315E+02,-0.2097693E+03,-0.2138794E+02, 0.3543734E+02,
     . 0.2507907E+03, 0.1472942E+02, 0.3870560E+04, 0.2028622E+03,
     . 0.7680764E+02, 0.6461952E+01/
      data (alsdev( 5,j),j=1,36) / 0.2879951E+02, 0.8020582E+01,
     . 0.1569833E+02, 0.8499159E+01, 0.4322857E+01, 0.2456659E+02,
     . 0.8186252E+01, 0.1617134E+04, 0.6940360E+03, 0.1907284E+04,
     . 0.2470698E+03, 0.1595705E+03, 0.1592168E+04, 0.2760713E+03,
     . 0.3922771E+03, 0.6302870E+03, 0.2006715E+03, 0.1216372E+03,
     . 0.8166120E+03, 0.1994494E+03, 0.1810311E+04, 0.4624083E+03,
     . 0.2593056E+03, 0.1694290E+04, 0.4982435E+03, 0.1037749E+03,
     . 0.5123920E+02, 0.5120408E+03, 0.8149457E+02, 0.4752918E+02,
     . 0.3031102E+03, 0.5243453E+02, 0.3284298E+04, 0.5991281E+03,
     . 0.1446465E+03, 0.2705362E+02/
      data (alscoef( 6,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.8026610E-01, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.3887290E+00,-0.1167581E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.3965225E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.7556319E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.9791975E-01,
     . 0.0000000E+00,-0.1792372E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,-0.2562578E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 6,j),j=1,36) / 0.5282349E+00, 0.2288561E+02,
     . 0.5509222E+02,-0.4616736E+01, 0.4066473E+01, 0.5720878E+02,
     . 0.3269119E+01, 0.7833530E+03, 0.2451029E+02, 0.8987844E+02,
     . 0.4654677E+02,-0.1255986E+02, 0.1154485E+03,-0.1190449E+02,
     . 0.5868539E+03, 0.1304664E+04,-0.5985332E+02, 0.9588982E+02,
     . 0.1357026E+04, 0.6501071E+02, 0.3277084E+04,-0.2018239E+03,
     . 0.2255694E+03, 0.3203238E+04, 0.1741666E+03, 0.9196463E+02,
     .-0.1768923E+02,-0.2261230E+03,-0.2270596E+02, 0.3445014E+02,
     . 0.2489540E+03, 0.1535398E+02, 0.3879045E+04, 0.2116815E+03,
     . 0.7734914E+02, 0.6904808E+01/
      data (alsdev( 6,j),j=1,36) / 0.2798798E+02, 0.7945013E+01,
     . 0.1555665E+02, 0.8406735E+01, 0.4233170E+01, 0.2462512E+02,
     . 0.8165998E+01, 0.1559906E+04, 0.6625800E+03, 0.1841586E+04,
     . 0.2441215E+03, 0.1501844E+03, 0.1544518E+04, 0.2655307E+03,
     . 0.3854558E+03, 0.6318023E+03, 0.1945790E+03, 0.1180420E+03,
     . 0.8090012E+03, 0.1964395E+03, 0.1767535E+04, 0.4526402E+03,
     . 0.2536928E+03, 0.1695497E+04, 0.4891541E+03, 0.1022458E+03,
     . 0.5073444E+02, 0.5048276E+03, 0.8129501E+02, 0.4514432E+02,
     . 0.2981933E+03, 0.5209768E+02, 0.3278063E+04, 0.5976022E+03,
     . 0.1443764E+03, 0.2930631E+02/
      data (alscoef( 7,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.1047530E+00,-0.8868639E-01, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.4587812E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.8218156E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.1123108E+00,
     . 0.0000000E+00,-0.1655864E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 7,j),j=1,36) / 0.4207630E+00, 0.2255040E+02,
     . 0.5443819E+02,-0.4917055E+01, 0.4062362E+01, 0.5703888E+02,
     . 0.3388848E+01, 0.7403136E+03, 0.2312487E+02, 0.9094167E+02,
     . 0.4966651E+02,-0.1176302E+02, 0.1092751E+03,-0.4587674E+01,
     . 0.5698082E+03, 0.1275754E+04,-0.6694496E+02, 0.9490926E+02,
     . 0.1333167E+04, 0.6673709E+02, 0.3206201E+04,-0.2110588E+03,
     . 0.2246610E+03, 0.3166486E+04, 0.1796703E+03, 0.9265514E+02,
     .-0.1852151E+02,-0.2425760E+03,-0.2346312E+02, 0.3375825E+02,
     . 0.2468534E+03, 0.1563206E+02, 0.3860909E+04, 0.2147707E+03,
     . 0.7540719E+02, 0.7243947E+01/
      data (alsdev( 7,j),j=1,36) / 0.2721044E+02, 0.7830068E+01,
     . 0.1558119E+02, 0.8276644E+01, 0.4154732E+01, 0.2465152E+02,
     . 0.7996647E+01, 0.1486568E+04, 0.6332492E+03, 0.1784579E+04,
     . 0.2395884E+03, 0.1394451E+03, 0.1492160E+04, 0.2504226E+03,
     . 0.3766640E+03, 0.6321689E+03, 0.1879339E+03, 0.1158340E+03,
     . 0.7986561E+03, 0.1904583E+03, 0.1749101E+04, 0.4422272E+03,
     . 0.2496878E+03, 0.1696971E+04, 0.4733990E+03, 0.1008219E+03,
     . 0.4979871E+02, 0.4965642E+03, 0.7946046E+02, 0.4403391E+02,
     . 0.2927683E+03, 0.5060949E+02, 0.3274097E+04, 0.5828798E+03,
     . 0.1414711E+03, 0.3087317E+02/
      data (alscoef( 8,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.9537594E-01, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.4518728E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.8478302E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.1335201E+00,
     . 0.0000000E+00,-0.1486502E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 8,j),j=1,36) / 0.4769039E+00, 0.2223271E+02,
     . 0.5392975E+02,-0.5245444E+01, 0.4073866E+01, 0.5679109E+02,
     . 0.3439451E+01, 0.6933816E+03, 0.2537599E+02, 0.9890241E+02,
     . 0.5022994E+02,-0.1020454E+02, 0.1035189E+03,-0.2918435E+01,
     . 0.5532652E+03, 0.1250069E+04,-0.7521220E+02, 0.9437025E+02,
     . 0.1308384E+04, 0.6672680E+02, 0.3154948E+04,-0.2238049E+03,
     . 0.2245567E+03, 0.3128242E+04, 0.1821682E+03, 0.9341725E+02,
     .-0.1931823E+02,-0.2613367E+03,-0.2460387E+02, 0.3332844E+02,
     . 0.2451973E+03, 0.1544944E+02, 0.3841154E+04, 0.2145339E+03,
     . 0.7453392E+02, 0.7796921E+01/
      data (alsdev( 8,j),j=1,36) / 0.2633330E+02, 0.7680913E+01,
     . 0.1570454E+02, 0.8119729E+01, 0.4091335E+01, 0.2482301E+02,
     . 0.7920240E+01, 0.1413855E+04, 0.6058992E+03, 0.1721314E+04,
     . 0.2337595E+03, 0.1330247E+03, 0.1450492E+04, 0.2424808E+03,
     . 0.3661280E+03, 0.6296606E+03, 0.1804536E+03, 0.1136799E+03,
     . 0.7890709E+03, 0.1860230E+03, 0.1750739E+04, 0.4317303E+03,
     . 0.2462065E+03, 0.1700974E+04, 0.4660102E+03, 0.1003206E+03,
     . 0.4966600E+02, 0.4872369E+03, 0.7847066E+02, 0.4366581E+02,
     . 0.2870837E+03, 0.5009062E+02, 0.3295655E+04, 0.5789249E+03,
     . 0.1388171E+03, 0.3218217E+02/
      data (alscoef( 9,j),j=1,36) / 0.0000000E+00, 0.3089123E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.1055703E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.5977988E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.1598280E+00,
     . 0.1132629E+00,-0.2142111E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00,-0.2412702E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg( 9,j),j=1,36) / 0.4476055E+00, 0.2192138E+02,
     . 0.5340811E+02,-0.5579272E+01, 0.4054054E+01, 0.5657278E+02,
     . 0.3548601E+01, 0.6483376E+03, 0.2617615E+02, 0.1013527E+03,
     . 0.5210487E+02,-0.9421763E+01, 0.9515031E+02,-0.3575154E+01,
     . 0.5370754E+03, 0.1224067E+04,-0.8324326E+02, 0.9253274E+02,
     . 0.1284906E+04, 0.6745268E+02, 0.3103078E+04,-0.2374746E+03,
     . 0.2228494E+03, 0.3088268E+04, 0.1870104E+03, 0.9521982E+02,
     .-0.2048142E+02,-0.2797499E+03,-0.2673219E+02, 0.3287624E+02,
     . 0.2417376E+03, 0.1522926E+02, 0.3831306E+04, 0.2196652E+03,
     . 0.7287435E+02, 0.8194879E+01/
      data (alsdev( 9,j),j=1,36) / 0.2546458E+02, 0.7520314E+01,
     . 0.1583576E+02, 0.8007618E+01, 0.4055698E+01, 0.2512221E+02,
     . 0.7765975E+01, 0.1336978E+04, 0.5802391E+03, 0.1659712E+04,
     . 0.2310691E+03, 0.1320454E+03, 0.1407886E+04, 0.2287508E+03,
     . 0.3549326E+03, 0.6250199E+03, 0.1747647E+03, 0.1116726E+03,
     . 0.7815645E+03, 0.1800884E+03, 0.1754649E+04, 0.4243386E+03,
     . 0.2447865E+03, 0.1705707E+04, 0.4525801E+03, 0.1010436E+03,
     . 0.5000002E+02, 0.4821107E+03, 0.7772745E+02, 0.4336179E+02,
     . 0.2819421E+03, 0.5012947E+02, 0.3344774E+04, 0.5673912E+03,
     . 0.1336848E+03, 0.3292386E+02/
      data (alscoef(10,j),j=1,36) / 0.0000000E+00, 0.0000000E+00,
     . 0.9469541E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.1078930E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     .-0.1727341E+00, 0.0000000E+00,-0.6476331E+00, 0.0000000E+00,
     . 0.0000000E+00,-0.6957146E+00, 0.0000000E+00, 0.1605409E+00,
     . 0.1261314E+00,-0.1576631E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.0000000E+00, 0.0000000E+00, 0.0000000E+00,
     . 0.0000000E+00, 0.1000000E+01/
      data (alavg(10,j),j=1,36) / 0.3980477E+00, 0.2159967E+02,
     . 0.5280331E+02,-0.5925649E+01, 0.4006236E+01, 0.5633189E+02,
     . 0.3727766E+01, 0.6011931E+03, 0.2631410E+02, 0.1027855E+03,
     . 0.5542253E+02,-0.9485357E+01, 0.8738937E+02,-0.7033623E+00,
     . 0.5208379E+03, 0.1195026E+04,-0.9081781E+02, 0.8989330E+02,
     . 0.1261422E+04, 0.7061524E+02, 0.3041471E+04,-0.2519473E+03,
     . 0.2191908E+03, 0.3042551E+04, 0.1953049E+03, 0.9791512E+02,
     .-0.2154251E+02,-0.2975466E+03,-0.2856389E+02, 0.3216120E+02,
     . 0.2370388E+03, 0.1545336E+02, 0.3819031E+04, 0.2332690E+03,
     . 0.7262690E+02, 0.8647505E+01/
      data (alsdev(10,j),j=1,36) / 0.2452266E+02, 0.7370310E+01,
     . 0.1591915E+02, 0.7926909E+01, 0.4014973E+01, 0.2541850E+02,
     . 0.7665672E+01, 0.1239007E+04, 0.5538984E+03, 0.1587020E+04,
     . 0.2307229E+03, 0.1327658E+03, 0.1352833E+04, 0.2263261E+03,
     . 0.3441646E+03, 0.6174752E+03, 0.1699011E+03, 0.1090849E+03,
     . 0.7755641E+03, 0.1731434E+03, 0.1751020E+04, 0.4186579E+03,
     . 0.2430095E+03, 0.1705991E+04, 0.4421535E+03, 0.1029045E+03,
     . 0.4997415E+02, 0.4806690E+03, 0.7786277E+02, 0.4229101E+02,
     . 0.2772892E+03, 0.4837127E+02, 0.3400294E+04, 0.5601602E+03,
     . 0.1343539E+03, 0.3347443E+02/
cc       end
C***********************************************************************
cc      BLOCK DATA

C**   THIS DATASET IS NOW NAMED' NWS.WD80.CJN.SOURCE1(PGM04)
 
C**	    ALBION D. TAYLOR, MARCH 19, 1982
C**   THE HURRICANE GRID IS BASED ON AN OBLIQUE EQUIDISTANT CYLINDRICAL
C**   MAP PROJECTION ORIENTED ALONG THE TRACK OF THE HURRICANE.
C
C**   THE X (OR I) COORDINATE XI OF A POINT REPRESENTS THE DISTANCE
C**   FROM THAT POINT TO THE GREAT CIRCLE THROUGH THE HURRICANE, IN
C**   THE DIRECTION OF MOTION OF THE HURRICANE MOTION.	POSITIVE VALUES
C**   REPRESENT DISTANCES TO THE RIGHT OF THE HURRICANE MOTION, NEGATIVE
C**   VALUES REPRESENT DISTANCES TO THE LEFT.
C**   THE Y (OR J) COORDINATE OF THE POINT REPRESENTS THE DISTANCE
C**   ALONG THE GREAT CIRCLE THROUGH THE HURRICANE TO THE PROJECTION
C**   OF THE POINT ONTO THAT CIRCLE.  POSITIVE VALUES REPRESENT
C**   DISTANCE IN THE DIRECTION OF HURRICANE MOTION, NEGATIVE VALUES
C**   REPRESENT DISTANCE IN THE OPPOSITE DIRECTION.
C
C**   SCALE DISTANCES ARE STRICTLY UNIFORM IN THE I-DIRECTION ALWAYS.
C**   THE SAME SCALE HOLDS IN THE J-DIRECTION ONLY ALONG THE HURRICANE TRAC
C**   ELSEWHERE, DISTANCES IN THE J-DIRECTION ARE EXAGERATED BY A FACTOR
C**   INVERSELY PROPORTIONAL TO THE COSINE OF THE ANGULAR DISTANCE FROM
C**   THE TRACK.  THE SCALE IS CORRECT TO 1 PERCENT WITHIN A DISTANCE OF
C**   480 NM OF THE STORM TRACK, 5 PERCENT WITHIN 1090 NM, AND
C**   10 PERCENT WITHIN 1550 NM.
C
C**   BIAS VALUES ARE ADDED TO THE XI AND YJ COORDINATES FOR CONVENIENCE
C**   IN INDEXING.
C
C**   A PARTICULAR GRID IS SPECIFIED BY THE USER BY MEANS OF A CALL
C**   TO SUBROUTINE STHGPR (SET HURRICANE GRID PARAMETERS)
C**   WITH ARGUMENTS (XLATH,XLONH,BEAR,GRIDSZ,XIO,YJO)
C**   WHERE
c
C**   XLATH,XLONH = LATITUDE, LONGITUDE OF THE HURRICANE
C**   BEAR	  = BEARING OF THE HURRICANE MOTION
C**   GRIDSZ	  = SIZE OF GRID ELEMENTS IN NAUTICAL MILES
C**   XIO, YJO	  = OFFSETS IN I AND J COORDINATES (OR I AND J
C                     COORDINATES OF HURRICANE)
C**   AND WHERE
c
C**   LATITUDES, LONGITUDES AND BEARINGS ARE GIVEN IN DEGREES,
C**   POSITIVE VALUES ARE NORTH AND WEST, NEGATIVE SOUTH AND EAST,
C**   BEARINGS ARE GIVEN CLOCKWISE FROM NORTH.
C
C**   THE CALL TO STHGPR SHOULD BE MADE ONCE ONLY, AND BEFORE REFERENCE
C**   TO ANY CALL TO LL2XYH OR XY2LLH.	IN DEFAULT, THE SYSTEM
C**   WILL ASSUME A STORM AT LAT,LONG=0.,0., BEARING DUE NORTH,
C**   WITH A GRIDSIZE OF 120 NAUTICAL MILES AND OFFSETS OF 0.,0. .
C
C**   TO CONVERT FROM GRID COORDINATES XI AND YJ, USE A CALL TO
C**   CALL XY2LLH(XI,YJ,XLAT,XLONG)
C**   THE SUBROUTINE WILL RETURN THE LATITUDE AND LONGITUDE CORRESPONDING
C**   TO THE GIVEN VALUES OF XI AND YJ.
C
C**   TO CONVERT FROM LATITUDE AND LONGITUDE TO GRID COORDINATES, USE
C**   CALL LL2XYH(XLAT,XLONG,XI,YJ)
C**   THE SUBROUTINE WILL RETURN THE I-COORDINATE XI AND Y-COORDINATE
C**   YJ CORRESPONDING TO THE GIVEN VALUES OF LATITUDE XLAT AND
C**   LONGITUDE XLONG.
c
cc      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
c
      DATA A /0.,-1.,0., 1.,0.,0.,  0.,0.,1./
      DATA RADPDG/1.745 3293 E-2/,RRTHNM /3 440.17/
      DATA DGRIDH/120./
      DATA HGRIDX,HGRIDY/0.,0./
c
      END
C******************************************************************
C
C  BRIEF DESCRIPTION OF PROGRAM MODULES:
C
C   backspaceFile - Repositions the specified file back "numRcrds" records.
C   doWriteAidRcd - Write the aid record to the output data file.
C   getAidDTG - Gets the first aid data for the specified DTG from
C              the input file.
C   getAidTAU - Gets the first A_RECORD record for the specified tau
C              from the supplied AID_DATA.  
C   getARecord - Reads one record of specified type from the input file.
C   getBigAidDTG - Gets all the aid data for the specified DTG from
C                  the input file
C   getSingleTAU - Gets the aid data for the specified tau from the
C              supplied AID_DATA.
C   getTech - Gets data for a specified aid technique from the supplied
C             BIG_AID_DATA structure and returns an AID_DATA structure
C   newWriteAidRcd - Write the aid record to the output data file.
C                    NHC version
C   processArcd - Assigns the data for a A_RECORD structure.
C   readARecord - Reads one AID_DATA data info from the input file.
C   readBest - Read one record from the best track file,
C              including the basin and cyclone number.
C   readBT   - Read one record from the best track file.
C   readNext - Reads the next ATCF_RECORD record from the input file.
C   writeAid - Write the aid record to the output data file.
C   writeAidRcd - Write the aid record to the output data file.
C                JTWC, NPMOC version
C   
C******************************************************************


C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  readBT
C
C  DESCRIPTION:  Read one record from the best track file.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call readBT (datFile,cent,dtg,flat,ns,flon,ew,iwind,ios)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of best track file
C
C  OUTPUT PARAMETERS:
C     cent - century of posit (2 characters, e.g. 19)
C     dtg - YYMMDDHH, date-time-group read from the best track file
C     flat - latitude read from the best track file
C     ns - one character north/south indicator for latitude
C     flon - longitude read from the best track file
C     ew - one character east/west indicator for longitude
C     iwind - max wind read from the best track file
C     ios - input/output status upon completion or the read operation
C           0 - successful read
C           negative - end-of-file
C           positive - error
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C   sampson, nrl    nov 9 98   added cent
C
C........................END PROLOGUE..................................
C
      subroutine readBT (datFile,cent,dtg,flat,ns,flon,ew,iwind,ios)   
c
c         formal parameters
      integer           datFile
      character*8       dtg
      character*2       cent
      real              flat, flon
      character*1       ns, ew
      integer           iwind
      integer           ios

      read( datFile, '(8x,a2,a8,17x,f3.1,a1,2x,f4.1,a1,2x,i3)', 
     1     iostat=ios ) cent, dtg, flat, ns, flon, ew, iwind
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  readBest
C
C  DESCRIPTION:  Read one record from the best track file.
C                Same as readBT except also reads the basin and 
C                cyclone number.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call readBest (datFile, basin, cycnum, cent, dtg, flat, ns, 
C                           flon, ew, iwind, ios )
C
C  INPUT PARAMETERS:  
C     datFile - unit number of best track file
C
C  OUTPUT PARAMETERS:
C     basin - basin read from the best track file
C     cycnum - cyclone num read from the best track file
C     cent - century (2 characters, e.g. 19)
C     dtg - YYMMDDHH, date-time-group read from the best track file
C     flat - latitude read from the best track file
C     ns - one character north/south indicator for latitude
C     flon - longitude read from the best track file
C     ew - one character east/west indicator for longitude
C     iwind - max wind read from the best track file
C     ios - input/output status upon completion or the read operation
C           0 - successful read
C           negative - end-of-file
C           positive - error
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C   sampson, nrl    nov 9 98   added cent
C
C........................END PROLOGUE..................................
C
      subroutine readBest (datFile, basin, cycnum, cent, dtg, flat, ns, 
     &     flon, ew, iwind, ios )
c
c         formal parameters
      integer           datFile
      character*2       basin
      character*2       cycnum
      character*8       dtg
      character*2       cent
      real              flat, flon
      character*1       ns, ew
      integer           iwind
      integer           ios

      read( datFile, '(a2,2x,a2,2x,a2,a8,17x,f3.1,a1,2x,f4.1,a1,2x,i3)', 
     1     iostat=ios )basin,cycnum,cent,dtg,flat,ns,flon,ew,iwind
C
      RETURN
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  doWriteAidRcd
C
C  DESCRIPTION:  Write the aid record to the output data file.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call doWriteAidRcd (datFile,stormID,cdtg,techname,itau,llwnd)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     stormID - storm id, eg. cp021997
C     cdtg - current dtg, eg. 1998060912
C     techname - objective aid name, eg. CLIM
C     itau - forecast period
C     llwnd - array of integers dimensioned (3) where 
C             and the three components are lat, lon and wind
C
C  OUTPUT PARAMETERS: NONE
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine doWriteAidRcd (datFile, stormID, cdtg, techname, 
     1     itau, llwnd )

      include 'dataioparms.inc'
c
c         formal parameters
      integer           datFile
      character*8       stormID
      character*10      cdtg
      character*4       techname
      integer           itau
      integer           llwnd(llw)
c
c         local variables
      character*2       basin
      character*2       stormnum
      character*1       ns, ew
      character*2       technum
      integer           ilat, ilon
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      basin = stormID(1:2)
      call upcase( basin, 2 )
      stormnum = stormID(3:4)

c     Assign the objective aid technique number
      if( techname .eq. 'CARQ' ) then
         technum = '01'
      else if( techname .eq. 'WRNG' ) then
         technum = '02'
      else
         technum = '03'
      endif

cx    Check for model runs where lat/lon out of range - convert to 0's
cx    sampson nrl oct 26, 1998
cx    sampson nrl aug 19, 2000  changed lon check for less than zero
cx    Handle cases of forecasts crossing 0 longitude,  ajs 1/17/01
      if( llwnd(2) .lt. 0 ) then
          llwnd(2) = llwnd(2) + 3600
      endif

      if( llwnd(1) .lt. -900  .or. 
     1    llwnd(1) .gt.  900  .or.
     2    llwnd(2) .lt.    0  .or. 
     3    llwnd(2) .gt.  3600 ) then
         llwnd(1) = 0
         llwnd(2) = 0
      endif
cx    Check for model runs where wind out of range - convert to 0's
cx    sampson nrl oct 26, 1998
      if( llwnd(3) .lt. 0 .or. llwnd(3) .gt. 300) 
     1     llwnd(3) = 0
      
      if( llwnd(1) .ne. 0 .or. llwnd(2) .ne. 0 
     1     .or. llwnd(3) .ne. 0) then
c     Convert from -900 thru 900 to 900S thru 900N
         ns = 'N'
         ilat = llwnd(1)
         if( ilat .lt. 0 ) then
            ilat = -ilat
            ns = 'S'
         endif
c     Convert from 0 thru 3600 (WH < 1800 < EH) to 1800W thru 1800E
         ew = 'W'
         ilon = llwnd(2)
         if( ilon .gt. 1800 ) then
            ilon = 3600 - ilon
            ew = 'E'
         endif
c     Write the aid record...
cx    only if the lat and lon are meaningful
         if ( ilon .le. 1800 .and. ilat .lt. 900 ) then
            write(datFile,9080) basin, stormnum, cdtg, 
     1           technum, techname, itau, ilat, ns, ilon, ew, 
     1           llwnd(3)
 9080       format( A2,', ',A2,', ',A10,', ',A2,', ',A4,', ',
     1           I3,', ',I3,A1,', ',I4,A1,', ',I3 )
         endif
      endif
      
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  writeAidRcd
C
C  DESCRIPTION:  Write the aid record to the output data file,
C                JTWC, NPMOC version
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call writeAidRcd (datFile,stormID,cdtg,techname,ltlnwnd)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     stormID - storm id, eg. cp021997
C     cdtg - current dtg, eg. 1998060912
C     techname - objective aid name, eg. CLIM
C     ltlnwnd - array of integers dimensioned (10,3) where 
C               the first dimension is the TAUs 12, 24, 36, 48, 72, ...
C               and the second dimension is lat, lon and wind
C
C  OUTPUT PARAMETERS: NONE
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C  sampson, nrl  Apr 99     R120 - has only 72, 96 and 120 hr fcsts
C  sampson, nrl  Jan 00     C120 - 120 hour forecast, 12 hr interval
C  sampson, nrl  Apr 00     XTRP - 120 hour forecast, 12 hr interval
C  sampson, nrl  May 01     ST5D - 120 hour forecast, 12 hr interval
C........................END PROLOGUE..................................
C
      subroutine writeAidRcd (datFile, stormID, cdtg, techname, 
     1     ltlnwnd )

      include 'dataioparms.inc'
c
c         formal parameters
      integer           datFile
      character*8       stormID
      character*10      cdtg
      character*4       techname
      integer           ltlnwnd(numtau,llw)
c
c         local variables
      integer           ii, jj, itau
      integer           llwnd(llw)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c

      loopend = 5
      if (techname.eq.'C120' .or. techname.eq.'XTRP' .or.
     &    techname.eq.'ST5D') loopend = numtau

c     Loop on the taus: 12, 24, 36, 48 and 72
      do ii = 1, loopend
         if( techname .eq. 'CARQ' .or. techname .eq. 'WRNG' ) then
            itau = -( (5-ii) * 6)
cx       long-range forecasts (e.g., C120) ... sampson NRL Jan 00
cx       does all taus in 12 hr increments
         else if ( techname.eq.'C120' .or. techname.eq.'XTRP'
     1	      .or. techname.eq.'ST5D') then
	    itau = ii * 12
cx       special case for extended forecasts (R120) ... sampson NRL Apr 99
         else if ( techname .eq. 'R120' ) then
	    itau = ii * 12 + 60
cx       old case for 72 hour forecasts ... 
         else
            itau = ii * 12
            if( itau .eq. 60 ) itau = 72
         endif
         do jj = 1, llw
            llwnd(jj) = ltlnwnd(ii,jj)
         enddo
         call doWriteAidRcd(datFile, stormID, cdtg, techname, itau, 
     &                      llwnd )
      enddo
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  newWriteAidRcd
C
C  DESCRIPTION:  Write the aid record to the output data file,
C                NHC version
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call newWriteAidRcd (datFile,stormID,cdtg,techname,ltlnwnd)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     stormID - storm id, eg. cp021997
C     cdtg - current dtg, eg. 1998060912
C     techname - objective aid name, eg. CLIM
C     ltlnwnd - array of integers dimensioned (newnumtau,llw) where 
C               the first dimension is the TAUs 0, 12, 24, 36, 48, 60, 72...
C               and the second dimension is lat, lon and wind
C
C  OUTPUT PARAMETERS: NONE
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine newWriteAidRcd (datFile, stormID, cdtg, techname, 
     1     ltlnwnd )

      include 'dataioparms.inc'
c
c         formal parameters
      integer           datFile
      character*8       stormID
      character*10      cdtg
      character*4       techname
      integer           ltlnwnd(newnumtau,llw)
c
c         local variables
      integer           ii, jj, itau
      integer           llwnd(llw)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c

      loopend = newnumtau
c     For CARQ and WRNG loop on the taus: -24, -18, -12, -6 and 0
      if (techname.eq.'CARQ' .or. techname.eq.'WRNG') loopend = 5

c     For all other aids loop on the taus: 
c        0, 12, 24, 36, 48, 60, 72, 84, 96, 108 and 120
      do ii = 1, loopend
         if( techname .eq. 'CARQ' .or. techname .eq. 'WRNG' ) then
            itau = -( (5-ii) * 6)
cx       do all taus in 12 hr increments
         else
	    itau = (ii-1) * 12
         endif
         do jj = 1, llw
            llwnd(jj) = ltlnwnd(ii,jj)
         enddo
         call doWriteAidRcd(datFile, stormID, cdtg, techname, itau, 
     &                      llwnd )
      enddo
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  writeAid
C
C  DESCRIPTION:  Write the aid record to the output data file.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call writeAid (datFile,stormID,century,cdtg,techname,ltlnwnd)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     stormID - storm id, eg. cp0297
C     century - 1st two digits of the storm year, eg. 19
C     cdtg - current dtg, eg. 98060912
C     techname - objective aid name, eg. CLIM
C     ltlnwnd - array of integers dimensioned (numtau,llw) where 
C               the first dimension is the TAUs 12, 24, 36, 48, 60, 72 ...
C               and the second dimension is lat, lon and wind
C
C  OUTPUT PARAMETERS: NONE
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C  sampson, nrl  Apr 99     R120 - has only 72, 96 and 120 hr fcsts
C  sampson, nrl  Jan 00     C120 - 120 hour forecast, 12 hr interval
C  sampson, nrl  Apr 00     XTRP - 120 hour forecast, 12 hr interval
C  sampson, nrl  May 01     ST5D - 120 hour forecast, 12 hr interval
C........................END PROLOGUE..................................
C
      subroutine writeAid (datFile, stormID, century, cdtg, techname,
     1     ltlnwnd )

      include 'dataioparms.inc'
c
c         formal parameters
      integer           datFile
      character*6       stormID
      character*2       century
      character*8       cdtg
      character*4       techname
      integer           ltlnwnd(numtau,llw)
c
c         local variables
      character*2       basin
      character*2       stormnum
      character*1       ns, ew
      character*2       technum
      integer           ii, itau
      integer           ilat, ilon
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      basin = stormID(1:2)
      call upcase( basin, 2 )
      stormnum = stormID(3:4)

c     Assign the objective aid technique number
      if( techname .eq. 'CARQ' ) then
         technum = '01'
      else if( techname .eq. 'WRNG' ) then
         technum = '02'
      else
         technum = '03'
      endif
cx  
      loopend = 5
      if (techname.eq.'C120' .or. techname.eq.'XTRP' .or.
     &    techname.eq.'ST5D' ) loopend = numtau

c     Loop on the taus: 12, 24, 36, 48 and 72
      do ii = 1, loopend
         if( techname .eq. 'CARQ' .or. techname .eq. 'WRNG' ) then
            itau = -( (5-ii) * 6)
cx       long-range forecasts (e.g., C120) ... sampson NRL Jan 00
cx       does all taus in 12 hr increments
         else if ( techname.eq.'C120' .or. techname.eq.'XTRP' .or.
     &             techname.eq.'ST5D' ) then
	    itau = ii * 12
cx       special case for extended forecasts (R120) ... sampson NRL Apr 99
         else if ( techname .eq. 'R120' ) then
	    itau = ii * 12 + 60
cx       old case for 72 hour forecasts ... 
         else
            itau = ii * 12
            if( itau .eq. 60 ) itau = 72
         endif
cx       Check for model runs where lat/lon out of range - convert to 0's
cx       sampson nrl oct 26, 1998
	 if( ltlnwnd(ii,1) .lt. -900  .or. 
     1	     ltlnwnd(ii,1) .gt.  900  .or.
     2       ltlnwnd(ii,2) .lt. -1800 .or. 
     3       ltlnwnd(ii,2) .gt.  3600 ) then
      	       ltlnwnd(ii,1) = 0
      	       ltlnwnd(ii,2) = 0
         endif
cx       Check for model runs where wind out of range - convert to 0's
cx       sampson nrl oct 26, 1998
	 if( ltlnwnd(ii,3) .lt. 0 .or. ltlnwnd(ii,3) .gt. 300) 
     1	       ltlnwnd(ii,3) = 0

         if( ltlnwnd(ii,1) .ne. 0 .or. ltlnwnd(ii,2) .ne. 0 
     1        .or. ltlnwnd(ii,3) .ne. 0) then
c           Convert from -900 thru 900 to 900S thru 900N
            ns = 'N'
            ilat = ltlnwnd(ii,1)
            if( ilat .lt. 0 ) then
               ilat = -ilat
               ns = 'S'
            endif
c           Convert from 0 thru 3600 (WH < 1800 < EH) to 1800W thru 1800E
            ew = 'W'
            ilon = ltlnwnd(ii,2)
            if( ilon .gt. 1800 ) then
               ilon = 3600 - ilon
               ew = 'E'
            endif
c           Write the aid record...
cx          only if the lat and lon are meaningful
	    if ( ilon .lt. 1800 .and. ilat .lt. 900 ) then
               write(datFile,9080) basin, stormnum, century, cdtg, 
     1              technum, techname, itau, ilat, ns, ilon, ew, 
     1              ltlnwnd(ii,3)
 9080         format( A2,', ',A2,', ',A2,A8,', ',A2,', ',A4,', ',
     1              I3,', ',I3,A1,', ',I4,A1,', ',I3 )
            endif
         endif
      enddo
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  readNext
C
C  DESCRIPTION:  Reads the next ATCF_RECORD record from the input file
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call readNext (datFile,record,ios)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C
C  OUTPUT PARAMETERS:
C     rcd - structure to read record into
C     ios - return 0 success, neg for end of file, pos for error
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine readNext (datFile, rcd, ios )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      integer            datFile
      type (ATCF_RECORD) rcd
      integer            ios
c
c         local variables
      character line*200
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c
c     Zero out the dtg, tech, lat, lon and vmax just in case
      rcd%DTG = '          '
      rcd%tech = '    '
      rcd%latns = '    '
      rcd%lonew = '     '
      rcd%vmax = '   '
c
c     Read one data record.
      read( datFile, '(a200)', iostat=ios ) line
      if( ios .eq. 0 ) then
c
c     Get the individual fields from the data record.
         read( line, '(a2,2x,a2,2x,a10,2x,a2,2x,a4,2x,a3)' )
     &        rcd%basin, rcd%cyNum, rcd%DTG, rcd%technum, rcd%tech, 
     &        rcd%tau
         read( line, '(35x,a4,2x,a5,2x,a3)' )
     &        rcd%latns, rcd%lonew, rcd%vmax
         read( line, '(53x,a4,2x,a2,2x,a3,2x,a3,4(2x,a4))' )
     &        rcd%mslp, rcd%ty, rcd%rad, rcd%windcode, rcd%radii(1), 
     &        rcd%radii(2), rcd%radii(3), rcd%radii(4)
         read( line, '(97x,a4,2x,a4,5(2x,a3),2x,a3,2x,a3,2x,a3)' )
     &        rcd%radp, rcd%rrp, rcd%mrd, rcd%gusts, rcd%eye, 
     &        rcd%unused, rcd%maxseas, rcd%initials, rcd%dir, rcd%speed
         read( line, '(149x,a10,2x,a1)' )  
     &        rcd%stormname, rcd%depth
         read( line, '(164x,a2,2x,a3,4(2x,a3))' )  
     &        rcd%seas, rcd%seascode, rcd%seasrad(1), rcd%seasrad(2),
     &        rcd%seasrad(3), rcd%seasrad(4)
      endif
C     
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  getARecord
C
C  DESCRIPTION:  Reads one record of specified type from the input file
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call getARecord (datFile,"CARQ",aidRcd,result)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     technique - "CARQ", "WRNG", "JTWC" ...
C
C  OUTPUT PARAMETERS:
C     aidRcd - structure to read data into
C     result - return 0 for fail, neg for end-of-file, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine getARecord (datFile, technique, aidRcd, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      integer         datFile
      character*4     technique
      type (AID_DATA) aidRcd
      integer         result
c
c         local variables
      logical*2   found
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1
      found = .false.
c
c     Loop on reading records until a record is found
c     of the type specified
      do while( result.eq.1 .and. .not.found )
c
c        Read the next record in the data file.
         call readARecord( datFile, aidRcd, result )
c
c        If tech name matches specified record type then process.
         if( technique .eq. aidRcd%aRecord(1)%tech ) found = .true.
c
      enddo
c
      if( result.ne.0 .and. .not.found ) result = 0
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  readARecord
C
C  DESCRIPTION:  Reads one AID_DATA data info from the input file.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call readARecord (datFile,aidRcd,result)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C
C  OUTPUT PARAMETERS:
C     aidRcd - structure to read data into
C     result - return 0 for fail, neg for end-of-file, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine readARecord (datFile, aidRcd, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      integer         datFile
      type (AID_DATA) aidRcd
      integer         result
c
c         local variables
      integer            ii
      integer            readStat
      type (ATCF_RECORD) recrd
      character          savDTG*10
      character          savtech*4
      logical*2          done
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 0
c
c     Read the next record in the data file
      call readNext( datFile, recrd, readStat )
c
c     Save the date-time-group and the technique
      if( readStat .eq. 0 ) then
         result = 1
         savDTG = recrd%DTG
         savtech = recrd%tech
      endif
c
c     Read all of the tau's for this DTG and tech
      ii=0
      aidRcd%numrcrds = 0
      done = .false.
      do while (result.eq.1 .and. readStat.eq.0
     &          .and. ii.lt.AidTauMax .and. .not.done)
         ii = ii + 1
c
c        Process the A_RECORD
         call processArcd( aidRcd%aRecord(ii), recrd, result )
c        Copy the ATCF_RECORD
         aidRcd%atcfRcd(ii) = recrd
         aidRcd%numrcrds = ii
c
c        Read the next record in the data file
         call readNext( datFile, recrd, readStat )
c
c        If read a new dtg or tech then flag done and backup one record
         if( savDTG.ne.recrd%DTG .or. savtech.ne.recrd%tech ) then
            done = .true.
            backspace( datFile )
         endif
      enddo

      if( readStat .gt. 0 ) result = 0
      if( readStat .lt. 0 ) result = readStat
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  getSingleTAU
C
C  DESCRIPTION:  Gets the aid data for the specified tau from the
C                supplied AID_DATA.  Returns the data for the tau 
C                in tauData.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call getSingleTAU (aidRcd, 72, tauData, result)
C
C  INPUT PARAMETERS:  
C     aidRcd - supplied AID_DATA structure
C     tau    - requested tau
C
C  OUTPUT PARAMETERS:
C     tauData - struct to read data into
C     result - return 0 for fail, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine getSingleTAU ( aidRcd, tau, tauData, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      type (AID_DATA) aidRcd, tauData
      integer         tau
      integer         result
c
c         local variables
      integer   ii, jj
      logical*2 found
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1
c
c     Find the requested tau in the AID_DATA structure.
      found = .false.
      ii = 1
      jj = 1
      tauData%numrcrds = 0
      do while( ii.le.aidRcd%numrcrds )
         if( aidRcd%aRecord(ii)%tau .eq. tau ) then
            found = .true.
            tauData%aRecord(jj) = aidRcd%aRecord(ii)
            tauData%atcfRcd(jj) = aidRcd%atcfRcd(ii)
            jj = jj + 1
            tauData%numrcrds = tauData%numrcrds + 1
         endif
         ii = ii + 1
      enddo

      if( .not.found ) result = 0
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  getAidTAU
C
C  DESCRIPTION:  Gets the first A_RECORD record for the specified tau from
C                the supplied AID_DATA.
C                Note: this only get the first RAD (35, 50, 65, 100 kt),
C                for the requested tau.  If all the records for the tau
C                are needed then use getSingleTAU().
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call getAidTAU (aidRcd, 72, aRecord, result)
C
C  INPUT PARAMETERS:  
C     aidRcd - supplied AID_DATA structure
C     tau    - requested tau
C
C  OUTPUT PARAMETERS:
C     aRecord - struct to read data into
C     result - return 0 for fail, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine getAidTAU ( aidRcd, tau, aRecord, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      type (AID_DATA) aidRcd
      integer         tau
      type (A_RECORD) aRecord
      integer         result
c
c         local variables
      integer   ii
      logical*2 found
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1
c
c     Find the requested tau in the AID_DATA structure.
      found = .false.
      ii = 1
      do while( ii.le.aidRcd%numrcrds .and. .not.found )
         if( aidRcd%aRecord(ii)%tau .eq. tau ) then
            found = .true.
            aRecord = aidRcd%aRecord(ii)
         endif
         ii = ii + 1
      enddo

      if( .not.found ) result = 0
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  getAidDTG
C
C  DESCRIPTION:  Gets the first aid data for the specified DTG 
C                from the input file
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call getAidDTG (datFile, dtg, aidRcd, result)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     dtg    - requested dtg (date-time-group)
C
C  OUTPUT PARAMETERS:
C     aidRcd - structure to read data into
C     result - return 0 for fail, neg for end-of-file, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine getAidDTG ( datFile, dtg, aidRcd, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      integer           datFile
      character*8       dtg
      type (AID_DATA)   aidRcd
      integer           result
c
c         local variables
      logical*2 found
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1
      found = .false.
c
c     Loop on reading records until a record is found
c     with the dtg specified
      do while( result.eq.1 .and. .not.found )
c
c        Read the next record in the data file.
         call readARecord( datFile, aidRcd, result )
c
c        If dtg matches specified dtg then process.
         if( dtg .eq. aidRcd%aRecord(1)%DTG(3:10) ) found = .true.
c
      enddo
c
      if( result.ne.0 .and. .not.found ) result = 0
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  getTech
C
C  DESCRIPTION:  Gets the data for a specified aid technique
C                from the supplied BIG_AID_DATA structure and
C                returns an AID_DATA structure
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  Sept 2000
C
C  USAGE:  call getTech (bigAidRcd, tech, aidRcd, result)
C
C  INPUT PARAMETERS:  
C     bigAidRcd - BIG_AID_DATA structure containing all records for a dtg
C     tech - requested obj aid technique
C
C  OUTPUT PARAMETERS:
C     aidRcd - structure to read data into
C     result - return 0 for fail, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine getTech ( bigAidRcd, tech, aidRcd, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      type (BIG_AID_DATA) bigAidRcd
      character*4     tech
      type (AID_DATA) aidRcd
      integer         result
c
c         local variables
      integer   ii, jj
      logical*2 found
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1
c
c     Find the requested tech in the BIG_AID_DATA structure.
      found = .false.
      ii = 1
      jj = 1
      aidRcd%numrcrds = 0
      do while( ii .le. bigAidRcd%numrcrds )
         if( bigAidRcd%aRecord(ii)%tech .eq. tech ) then
            found = .true.
            aidRcd%aRecord(jj) = bigAidRcd%aRecord(ii)
            aidRcd%atcfRcd(jj) = bigAidRcd%atcfRcd(ii)
            jj = jj + 1
            aidRcd%numrcrds = aidRcd%numrcrds + 1
         endif
         ii = ii + 1
      enddo

      if( .not.found ) result = 0
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  getBigAidDTG
C
C  DESCRIPTION:  Gets all the aid data for the specified DTG 
C                from the input file 
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  Sept 2000
C
C  USAGE:  call getBigAidDTG (datFile, dtg, bigAidRcd, result)
C
C  INPUT PARAMETERS:  
C     datFile - unit number of output data file
C     dtg    - requested dtg (date-time-group)
C
C  OUTPUT PARAMETERS:
C     bigAidRcd - structure to read data into
C     result - return 0 for fail, neg for end-of-file, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine getBigAidDTG ( datFile, dtg, bigAidRcd, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      integer           datFile
c      character*8       dtg
      character*10       dtg
      type (BIG_AID_DATA)   bigAidRcd
      type (AID_DATA)   aidRcd
      integer           readStat
      integer           result
      integer           ii, jj
c
c         local variables
      logical*2 found
      logical*2 dtgmatch
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1
      readStat = 1
      found = .false.
      dtgmatch = .false.
c
c     Loop on reading records until a record is found
c     with the dtg specified
      do while( result.eq.1 .and. .not.found )
c
c        Read the next record in the data file.
         call readARecord( datFile, aidRcd, readStat )
         result = readStat
c
c        If dtg matches specified dtg then process.
         if( dtg .eq. aidRcd%aRecord(1)%DTG ) found = .true.
c
      enddo

      if( found ) dtgmatch = .true.
c     If found assign the aidRcd read into bigAidRcd 
      if( dtgmatch ) then
         do ii=1, aidRcd%numrcrds
            bigAidRcd%aRecord(ii) = aidRcd%aRecord(ii)
            bigAidRcd%atcfRcd(ii) = aidRcd%atcfRcd(ii)
         enddo
         bigAidRcd%numrcrds = aidRcd%numrcrds
      endif

c     Loop on reading records as long as dtg matches specified dtg
      do while( readStat.eq.1 .and. dtgmatch )
c
c        Read the next record in the data file.
         call readARecord( datFile, aidRcd, readStat )
         result = readStat
c
c        If dtg matches specified dtg then process.
         if( dtg .ne. aidRcd%aRecord(1)%DTG ) dtgmatch = .false.
c        If matching dtg then assign aidRcd into bigAidRcd
         if( readStat.ne.0 .and. dtgmatch ) then
            jj = bigAidRcd%numrcrds + 1
            do ii=1, aidRcd%numrcrds
               bigAidRcd%aRecord(jj) = aidRcd%aRecord(ii)
               bigAidRcd%atcfRcd(jj) = aidRcd%atcfRcd(ii)
               jj = jj + 1
            enddo
            bigAidRcd%numrcrds = bigAidRcd%numrcrds + aidRcd%numrcrds
         endif
c
      enddo
      
c     Backup the file to just after the last matching dtg.
      if( found .and. .not. dtgmatch .and. aidRcd%numrcrds .gt. 0 )
     &   call backspaceFile( datFile, aidRcd%numrcrds )
c
      if( result.ne.0 .and. .not.found ) result = 0
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  backspaceFile
C
C  DESCRIPTION:  Repositions the specified file back "numRcrds" records.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  Sept 2000
C
C  USAGE:  call backspaceFile ( datFile, numRcrds )
C
C  INPUT PARAMETERS:  
C     datFile - unit number of the objective aids file
C     numRcrds - number of records to back up
C
C  OUTPUT PARAMETERS:
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine backspaceFile (datFile, numRcrds)
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      integer            datFile
      integer            numRcrds
      integer            ii
c
c         local variables
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do ii=1, numRcrds
         backspace datFile
      enddo
C
      END


C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  processArcd
C
C  DESCRIPTION:  Assigns the data for a A_RECORD structure.
C
C  PROGRAMMER, DATE:  Ann Schrader   (SAIC)  June 1998
C
C  USAGE:  call processArcd ( aidRcd%aRecord(ii), recrd, result )
C
C  INPUT PARAMETERS:  
C     atcfRcd - ATCF_RECORD struct containing data
C
C  OUTPUT PARAMETERS:
C     aidRcd - A_RECORD struct to receive data
C     result - return 0 for fail, 1 for success
C
C  ERROR CONDITIONS:
C
C........................MAINTENANCE SECTION............................
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C  METHOD:
C
C  RECORD OF CHANGES:
C
C........................END PROLOGUE..................................
C
      subroutine processArcd (aidRcd, atcfRcd, result )
c
      implicit none
c
      INCLUDE  'dataformats.inc'
c
c         formal parameters
      type (A_RECORD)    aidRcd
      type (ATCF_RECORD) atcfRcd
      integer            result
c
c         local variables
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      result = 1

      aidRcd%basin = atcfRcd%basin
      read( atcfRcd%cyNum, '(i2)' ) aidRcd%cyNum
      aidRcd%DTG = atcfRcd%DTG
      read( atcfRcd%technum, '(i2)' ) aidRcd%technum
      aidRcd%tech = atcfRcd%tech
      read( atcfRcd%tau, '(i3)' ) aidRcd%tau
      read( atcfRcd%latns, '(f3.1,a1)' ) aidRcd%lat, aidRcd%NS
      read( atcfRcd%lonew, '(f4.1,a1)' ) aidRcd%lon, aidRcd%EW
      read( atcfRcd%vmax, '(i3)' ) aidRcd%vmax
      read( atcfRcd%mslp, '(i4)' ) aidRcd%mslp
      aidRcd%ty = atcfRcd%ty
      read( atcfRcd%rad, '(i3)' ) aidRcd%rad
      aidRcd%windcode = atcfRcd%windcode
      read( atcfRcd%radii(1), '(i4)' ) aidRcd%radii(1)
      read( atcfRcd%radii(2), '(i4)' ) aidRcd%radii(2)
      read( atcfRcd%radii(3), '(i4)' ) aidRcd%radii(3)
      read( atcfRcd%radii(4), '(i4)' ) aidRcd%radii(4)
      read( atcfRcd%radp, '(i4)' ) aidRcd%radp
      read( atcfRcd%rrp, '(i4)' ) aidRcd%rrp
      read( atcfRcd%mrd, '(i3)' ) aidRcd%mrd
      read( atcfRcd%gusts, '(i3)' ) aidRcd%gusts
      read( atcfRcd%eye, '(i3)' ) aidRcd%eye
      read( atcfRcd%maxseas, '(i3)' ) aidRcd%maxseas
      aidRcd%initials = atcfRcd%initials
      read( atcfRcd%dir, '(i3)' ) aidRcd%dir
      read( atcfRcd%speed, '(i3)' ) aidRcd%speed
      aidRcd%stormname = atcfRcd%stormname
      aidRcd%depth = atcfRcd%depth
      read( atcfRcd%seas, '(i2)' ) aidRcd%seas
      aidRcd%seascode = atcfRcd%seascode
      read( atcfRcd%seasrad(1), '(i3)' ) aidRcd%seasrad(1)
      read( atcfRcd%seasrad(2), '(i3)' ) aidRcd%seasrad(2)
      read( atcfRcd%seasrad(3), '(i3)' ) aidRcd%seasrad(3)
      read( atcfRcd%seasrad(4), '(i3)' ) aidRcd%seasrad(4)
C
      END
      subroutine upcase (string,nchar)

c  this routine converts all lower case characters (ascii 97 - 122)
c  in the variable string to upper case characters (ascii 65 - 90).

      character string*(*)

c  loop thru each character in the string


c     call prctrc('upcase',.true.)

      do 100 i=1,nchar

c  if it is lower case, subtract 32 from it to make it upper case.

      ich = ichar(string(i:i))
      if ((ich .gt. 96) .and. (ich .lt. 123)) string(i:i) = 
     &         char(ichar(string(i:i))-32)
  100 continue

c     call prctrc('upcase',.false.)

      return
      end
