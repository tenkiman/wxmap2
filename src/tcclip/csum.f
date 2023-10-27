      PROGRAM CSUM 
C
C********* CHANGE RECORD ************************************
C
C     CSUM*01 (06 AUG 85) CHANGES TO INPUT/OUTPUT FORMAT
C
C     CSUM*02 (17 SEP 85) CORRECT CODE ERROR, TURN ON DIAGNOSTICS
C
C     CSUM*03 (17 DEC 85) CORRECTS PROBLEM W/ DTG IN FORECAST
C
C     CSUM*04 (14 JAN 86) CORRECTS FOR POSITIONS OFF NH PS GRID
C
C     CSUM*05 ( 7 JUL 89) CHANGE PROGRAM TO READ SPHERICAL FIELDS,
C                         CHANGE INTERPOLATION FM BSSLG TO CYCINT AND
C                         ALLOW CYCLONE TO CROSS 180 LONGITUDE
C
C     <<CHANGE NOTICE>> CSUM*06 (27 FEB 92) -- CLIFFORD,M.
C               ALLOW FOR STORMS THAT CROSS FROM ONE BASIN TO
C               ANOTHER.
C
C     <<CHANGE NOTICE>> CSUM*07 (26 JUL 95) -- SAMPSON,B.
C               DISABLE IO BASIN, MAKE RUN IN ATCF 3.0
C               USING TEDS DATABASE
C               CHANGES ARE IN lower case AND NOTED WITH
C               'cx' IN THE FIRST TWO COLUMNS
cx
cx              only storms in NWP and ATL are processed   
cx              only those within climatological limits:
cx                  5-45N,100-180E in WP
cx                  5-50N, 20-100W in AL
cx
cx              Input:  
cx                    unit92    - b??????.dat, best track data
cx              Output:
cx                    screen    - plain text forecast
cx                    wptot.dat - forecast in "ccrs or adeck format"
cx                    csum.dbg  - debugging data
c
c     Modified to use new data format,  6/98   A. Schrader
c     Modified to use cent, century of last bt posit,  1198   B. Sampson 
C
C************************************************************
C
C     THIS PROGRAM COMPUTES THE 24, 48 AND 72 HOUR FORECAST
C     LAT AND LONG OF A TROPICAL CYCLONE USING MATSUMOTO'S
C     STATISTICAL METHOD TRACK PREDICTION.
C     SIX TABLES ARE COMPUTED FROM THE FNOC 500 MB,
C     SURFACE PRESSURE AND 200 MB FIELDS FOR EACH FORECAST.
C     THE TABLES ARE INTERPOLATED GRID POINT VALUES BASED ON
C     +/- 40 DEGREES LONGITUDE, +35 & -10 DEGREES LAT,
C     AROUND THE CURRENT LOCATION OF A TROPICAL CYCLONE.
C     THE 24, 48 AND 72 HOUR FORECASTS ARE ACTUALLY COMPUTED IN
C     THE APPROPRIATE SUBROUTINE FOR EACH TROPICAL CYCLONE BASIN.
C
C     THE SIX TABLES ARE:
C
C     FLDTBL(1,J,I) = CURRENT 500 MB HEIGHTS
C     FLDTBL(2,J,I) = PREVIOUS 24 HOUR 500 MB HEIGHTS
C     FLDTBL(3,J,I) = CURRENT SURFACE PRESSURE
C     FLDTBL(4,J,I) = PREVIOUS 24 HOUR SURFACE PRESSURE
C     FLDTBL(5,J,I) = CURRENT 200 MB HEIGHTS
C     FLDTBL(6,J,I) = PREVIOUS 24 HOUR 200 MB HEIGHTS
C
C
C     R E Q U I R E D   I N P U T S
C
C     INPUT IS THE FILE CONTAINING TLAT(1) - TLAT(3),
C     TLON(1) - TLON(3), IWIND, LDTG(1), INUM AND IBAS.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     IWIND = WIND INTENSITY AT WARNING TIME
C
C     LDTG(1) = THE DAY, TIME GROUP AT THE WARNING TIME
C     LDTG(2) = THE DAY, TIME GROUP 12 HOURS PREVIOUS
C     LDTG(3) = THE DAY, TIME GROUP 24 HOURS PREVIOUS
C
C     INUM = THE TROPICAL CYCLONE NUMBER.
C
C     IBAS = ONE LETTER TROPICAL CYCLONE BASIN IDENTIFIER.
C
C     O U T P U T
C
C     FLAT, FLON = FORECAST LATITUDE AND LONGITUDE TO BE OUTPUT
C

      include 'dataioparms.inc'

      character*100 storms,filename
      character*8 ldate,ldate1
      character*8 cdtg,dtg12,dtg24
      character*8 tdtg
      character*8 btdtg
      character*6 strmid
      character*2 century
      character*2 cent
      character*3 iele,iarea
      character*1 cns,cew
      character*1 ins,iew
      character*1 ibas,cdummy
      character btns*1, btew*1
      integer ltlnwnd(numtau,llw)
      integer ibtwind, ios, ii, iarg
      real btlat, btlon
      real tlat1, tlon1, tlat2, tlon2

      COMMON /FLDDAT/ FLDTBL(6,10,17)
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
cx    COMMON/   / IFILE(1033),NZ(20),IDATA(10512)
C
cx    INTEGER CHARCVF
C
      DIMENSION F(10512)
cx    DIMENSION IELE(6), IDTG(3), LDTG(3)
      DIMENSION IELE(6), LDTG(3)
      DIMENSION ITAU(3,2), KTAU(3,2)
      DIMENSION INS(3), IEW(3)
      DIMENSION IADD(3), UCONV(3)
      DIMENSION DGLON(3), ILAT(3), ILON(3)
      DIMENSION IAREA(3)
      DIMENSION ADD(3), IC(3), JC(3)
C
cx    EQUIVALENCE (IDATA(1),F(1))
C
cx    DATA IELE /3LF00, 3LF00, 3LA01, 3LA01, 3LI00, 3LI00/
      data iele /3HF00, 3HF00, 3HA01, 3HA01, 3HI00, 3HI00/
      DATA ITAU / 0, 24, 48, 0, 0, 24/
      DATA KTAU / 12, 36, 60, 0, 12, 36/
      DATA IADD / 557400, 0, 1178400/
      DATA UCONV / 100., 1., 100./
cx    DATA IAREA / 3LNWP, 3LNIO, 3LATL/
      data iarea / 3HNWP, 3HNIO, 3HATL/
      DATA ADD/-5000., -1000., -11784./
      DATA IC/0, 20, 20/
      DATA JC/24, 40, 0/
cx    DATA LAPS/1L$/
C
C********************************************************************
C
c*************  This code added to read best track ...bs 7/25/95 ****
c
c  get the storms directory name
c
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
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

      call getarg(iarg,century)
      iarg = iarg + 1
c
c  open debugging file
c
      call openfile (7,'csum.dbg','unknown',ioerror)
      if (ioerror.lt.0) go to 975
c
c  write heading on output
c
      print *,'********************************************************'
      print *,' '
      print *,'          csum forecast for ',strmid
      print *,' '
      write(7,*)'********* csum forecast for ',strmid,'**************'
      write(7,*)' '
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      call openfile (92,filename,'old',ioerror)
      if (ioerror.lt.0) go to 950
c
c  convert the 1st two characters of stormid to uppercase
c
      call upcase(strmid,6)
      ibas=strmid(1:1)
c  find the last dtg in the best track file
c
      write (7,*) 'find last dtg in the best track file'
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 92,cent,tdtg,btlat,btns,btlon,btew,ibtwind,ios )
         if (tdtg.ne.'        ') then
            read(tdtg,'(i8)')ldtg(1)
         endif
      enddo
      write (cdtg,'(i8.8)') ldtg(1)
      call icrdtg (cdtg,dtg12,-12)
      call icrdtg (cdtg,dtg24,-24)
      read (dtg12,'(i8)') ldtg(2)
      read (dtg24,'(i8)') ldtg(3)
cx    write(*,*) 'ldtg(1):',ldtg(1)
cx    write(*,*) 'ldtg(2):',ldtg(2)
cx    write(*,*) 'ldtg(3):',ldtg(3)
c
c  now find the current, -12, and -24 hr positions
c
      write (7,*) 'find current, -12 and -24 hr posits'
      rewind 92
cx    print *, 'inum:',inum
cx    print *, 'idtg:',idtg
cx    print *,'lat:',lat,cns
cx    print *,'lon:',lon,cew
cx    print *, iwnd
      ios = 0
      do while ( ios .eq. 0 )
         call readBT(92, cent, btdtg, btlat, cns, btlon, cew, iwnd, ios)
         if( ios .eq. 0 ) then
            read( btdtg, '(i8)' ) idtg

c           if current position 
            if (idtg.eq.ldtg(1)) then
               ilat(1) = anint( btlat*10.0 )
               ins(1) = cns
               ilon(1) = anint( btlon*10.0 )
               iew(1) = cew
               
c           else if -12 hr position
            elseif (idtg.eq.ldtg(2)) then
               ilat(2) = anint( btlat*10.0 )
               ins(2) = cns
               ilon(2) = anint( btlon*10.0 )
               iew(2) = cew
               
c           else if -24 hr position
            elseif (idtg.eq.ldtg(3)) then
               ilat(3) = anint( btlat*10.0 )
               ins(3) = cns
               ilon(3) = anint( btlon*10.0 )
               iew(3) = cew
            endif
         endif
      enddo
      close (92)
      if (ilat(3).eq.0) then
	 write(*,*) "CSUM: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
	 write(7,*) "CSUM: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
	 stop "CSUM: NEED AT LEAST 5 POSITIONS (24HRS) TO RUN"
      endif

cx    CALL ZEEMSG(1)
C
cx    READ 1030, ILAT(1),INS(1),ILON(1),IEW(1),INUM,IBAS,
cx   1   IWIND,(ILAT(I),INS(I),ILON(I),IEW(I),I=2,3),LDTG(1)
C
C     S. HEMISPHERE STORMS ARE NOT PROCESSED.
C
cx    IF (.NOT.(INS(1) .NE. 1HN)) GO TO 5
      if (ins(1) .eq. 'N') go to 5
cx       CALL ONSW(2)
         print *, "NO FCST FOR SOUTHERN HEMISPHERE"
         STOP "CSUM: ABORTED, NO FCST FOR SOUTHERN HEMISPHERE"
   5     CONTINUE
C
Cx    ONLY STORMS IN ATL, NWP, OR IO ARE PROCESSED; NO EPAC OR CPAC
Cx    STORMS.
cx    IF ((IBAS .EQ. 1HL) .OR. (IEW(1) .EQ. 1HE)) GO TO 7
cx    IF ((IBAS .EQ. 1HA) .OR. (IEW(1) .EQ. 1HE)) GO TO 7
cx
cx    only storms in NWP and ATL are processed   ...bs 7/27/95
cx   make sure that the tropical cyclone is within climatological limits
cx   5-45N,100-180E in WP, 5-50N,20-100W in AL
cx
      if (                      (ins(1)  .eq.'N')
     1                    .and. (iew(1)  .eq.'E')			 
     2                    .and. (ilat(1) .ge.  50)
     3                    .and. (ilat(1) .le. 450)
     4                    .and. (ilon(1) .ge.1000)
     5                    .and. (ilon(1) .le.1800)) go to 7
      if ((ibas .eq. 'A') .and. (ins(1)  .eq.'N')
     1                    .and. (iew(1)  .eq.'W')			 
     2                    .and. (ilat(1) .ge. 50)
     3                    .and. (ilat(1) .le. 500)
     4                    .and. (ilon(1) .ge. 200)
     5                    .and. (ilon(1) .le.1000)) go to 7
cx
cx       CALL ONSW(2)
         print *, "CSUM: TRACK OUTSIDE ALLOWED FORECAST AREAS"
         STOP "CSUM: ABORTED, TRACK OUTSIDE ALLOWED FORECAST AREAS"
    7 CONTINUE
C
      DO 10 I=1,3
         TLAT(I) = ILAT(I) * 0.1
         TLON(I) = ILON(I) * 0.1
   10 CONTINUE
C
      DO 20 I=1,3
         IF (INS(I) .EQ. 1HS) STOP "CSUM: ABORTED, NO FCST FOR SO HEMI"
         IF (IEW(I) .EQ. 1HW) TLON(I) = -TLON(I)
   20 CONTINUE
C
C     CONVERT ALL TIMES TO EITHER 00Z OR 12Z
C
cx    LDATE = LDTG(1)
      write(ldate,'(i8.8)') LDTG(1)
c     Year 2000 compliance, ajs
      if( ldate(1:1) .eq. ' ' ) ldate(1:1) = '0'
      if( ldate(2:2) .eq. ' ' ) ldate(2:2) = '0'
      if( ldate(3:3) .eq. ' ' ) ldate(3:3) = '0'
cx    DECODE (8,1090,LDTG(1)) IHR
cx    IF (IHR.LT.2L24 .AND. IHR.GT.2L12) IHR = 2L12
cx    IF (IHR .LT. 2L12) IHR = 2L00
cx    ENCODE (8,2000,LDTG(1)) LDATE,IHR
C
cx    LDTG(2) = INCRDTG(LDTG(1),-12)
cx    LDTG(3) = INCRDTG(LDTG(1),-24)
cx    PRINT *, "0"
cx    PRINT *, " LDTG = ",LDTG(1), LDTG(2), LDTG(3)
cx    PRINT *, "0"
      write(7,*) " "
      write(7,*) " LDTG = ",LDTG(1), LDTG(2), LDTG(3)
      write(7,*) " "
C
C     CONVERT DATE FROM DISPLAY CODE TO EXTERNAL BCD
C
cx    IDTG(1) = CHARCVF(LDTG(1),8)
cx    IDTG(2) = CHARCVF(LDTG(2),8)
cx    IDTG(3) = CHARCVF(LDTG(3),8)
C
C     PRINT *, " IWIND = ",IWIND
C
C
C     DETERMINE WHICH BASIN STORM IS IN
C
      IA=1
      IF (ILON(1) .LE. 1000) IA=2
      IF (IBAS .EQ. 1HL) IA=3
C
C     GET DIRECTION OF MOTION (DOM)
C
      SLON = AMOD ((360.0 -TLON(2)),360.0)
      ELON = AMOD ((360.0 -TLON(1)),360.0)
      CALL RHDST (TLAT(2),SLON,TLAT(1),ELON,DOM,DST)
cx    PRINT *, " DOM = ", DOM, " DST = ", DST
cx    PRINT *, "0"
      write(7,*) " dom = ", dom, " dst = ", dst
      write(7,*)  " "
      IDOM = DOM
C
cx    WRITE(19,1050)
cx    WRITE (19,1010) INUM,IBAS,IAREA(IA)
cx    WRITE (19,1050)
cx    WRITE (19,1040)
cx    WRITE (19,1050)
cx    WRITE (19,1070) 0,LDATE,ABS(TLAT(1)),INS(1),ABS(TLON(1)),IEW(1),
cx   1   10H          ,5H
      write (*,1070) 0,ldate,abs(tlat(1)),ins(1),abs(tlon(1)),iew(1),
     1   10H          ,5H
cx
cx    open the fields file, read the date-time-group, number of fields (4 or 6)
cx
      write(filename,'(a,a,a)')storms(1:ind),"/csum.",cdtg
      open (unit=9,file=filename,form="unformatted",
     &      status='old',err=990)
      read (9) ldate1
      if (ldate1.ne.ldate) then
           write(*,*) "dtg of fields does not match dtg of track"
           write(*,*) ldate1, " not equal to ",ldate
           stop 'CSUM: FIELD DTG DOES NOT EQUAL TRACK DTG'
      endif
C
C     LOOP 3 TIMES (FOR THE 24, 48 AND 72 HOUR FORECASTS)
C
      do ii=1,numtau
         ltlnwnd(ii,1) = 0
         ltlnwnd(ii,2) = 0
         ltlnwnd(ii,3) = 0
      enddo
      IFLG = 0
      DO 850 K=1,3
C
cx    WRITE (19,1050)
cx    PRINT *, " TLAT(1) = ",TLAT(1)," TLON(1) = ",TLON(1)
cx    PRINT *, " TLAT(2) = ",TLAT(2)," TLON(2) = ",TLON(2)
cx    PRINT *, " TLAT(3) = ",TLAT(3)," TLON(3) = ",TLON(3)
cx    PRINT *, "0"
C
C        FOR GLTLNIJ LONGITUDE IS POSITIVE FROM EAST TO WEST
C
         DO 40 I=1,3
         DGLON(I) = AMOD ((360.0 -TLON(I)),360.0)
   40    CONTINUE
C
C        200 MB STEERING FOR ATL AND NWP NORTH OF THE RIDGE
C
         NLIM = 4
         IF (IA .EQ. 3) NLIM=6
         IF (IA.EQ.1 .AND. IDOM.GT.30 .AND. IDOM.LE.120 .AND.
     1      IWIND.GE.90) NLIM=6
C
C        LOOP 4 - 6 TIMES (TO COMPUTE EACH OF THE REQUIRED TABLES)
C
cx 50    DO 500 N=1,6
   50    DO 500 N=1,6
C
C           TABLES 1,3 & 5 ARE CURRENT TIME
C           TABLES 2,4 & 6 ARE PREVIOUS 24 HOUR
C
            IF (MOD(N,2) .EQ. 0) NN = 2
            IF (MOD(N,2) .NE. 0) NN = 1
C
            IF (IFLG .EQ. 1) GO TO 55
            ITM = 1
            IF (K.EQ.1 .AND. MOD(N,2).EQ.0) ITM = 3
            NTAU = ITAU(K,NN)
            GO TO 60
C
   55       ITM = 2
            IF (K.EQ.1 .AND. MOD(N,2).EQ.0) ITM=3
            NTAU = KTAU(K,NN)
C
   60       CONTINUE
	    write(7,*) ' '
	    write(7,*) 'iele(n):',iele(n)
	    write(7,*) 'idtg(itm):',ldtg(itm)
	    write(7,*) 'ntau:',ntau
cx 60       CALL SYSLBLC (IELE(N), IDTG(ITM), NTAU, LAPS, IREC)
C           WRITE (19,1000) IELE(N), IDTG(ITM), NTAU, LAPS
C
cx          IFILE(1) = 7LGLOBLPE
cx          IF (CHECKNZ (IFILE, IREC ,10532)) 75, 100
C
cx 75       IF (IFLG .EQ. 1) GO TO 900
cx          IFLG = 1
cx          GO TO 55
C
  100       continue
cx100       CALL ZREADER (IFILE, IREC, NZ, 10532)
cx          ISCALE = (SHIFT(NZ(4),-20)) .AND. (.NOT.MASK(53))
cx          CALL FXFL (IDATA, F, ISCALE, 10512)
C
C           ADD CONSTANT AND CONVERT UNITS (CM TO METERS)
C
cx          ADDVL = IADD((N+1)/2)
cx          UNITC = 1.0/UCONV((N+1)/2)
cx          DO 150 IJ=1, 10512
cx             F(IJ) = UNITC*(F(IJ) +ADDVL)
cx150       CONTINUE
cx   temporary assignment just to get working
cx          DO 150 IJ=1, 10512
cx             F(IJ) = 0.0
cx150       CONTINUE
cx
cx  read spherical fields from unformatted file
cx
      read (9) f

C
      NX = (N+1) / 2
cx    CALL QPRNTG(F,IREC,IDTG(ITM),IC(IA),JC(IA),73,144,0,1.0,ADD(NX))
C
      T = TLON(1)
cx    PRINT *, "0"
cx    PRINT *, " N = ", N
cx    PRINT 2020,(T-40.),(T-35.),(T-30.),(T-25.),(T-20.),(T-15.),(T-10.)
cx   $ ,(T-5.),T,(T+5.),(T+10.),(T+15.),(T+20.),(T+25.),(T+30.),(T+35.),
cx   $ (T+40.)
      write(7,*) " "
      write(7,*) " N = ", N
      write(7,2020)
     $ (t-40.),(t-35.),(t-30.),(t-25.),(t-20.),(t-15.),(t-10.)
     $ ,(t-5.),t,(t+5.),(t+10.),(t+15.),(t+20.),(t+25.),(t+30.),(t+35.),
     $ (t+40.)
C
            ADJLAT = -10
            DO 300 J=1,10
               RLAT = TLAT(1) + ADJLAT
               ADJLON = 40
               DO 200 I=1,17
                  RLON = DGLON(1) + ADJLON
cx                CALL GLTLNIJ (RLAT, RLON, XI, YJ), RETURNS (170)
  		  xi = 1.0 + (360.0-rlon)*0.4
  		  yj = (rlat+92.5)*0.4
cx                GO TO 180
cx170             STOP "ERROR IN GLTLNIJ"
C
C                 INTERPOLATE GRID POINTS
C
  180             CONTINUE
cx                CALL CYCINT (XI,YJ,F,73,144,FVAL,IERR)
                  CALL CYCINT (XI,YJ,F,144,73,FVAL,IERR)
                  IF (IERR .NE. 0) STOP "CSUM: ABORTED, ERROR IN CYCINT"
C
                  FLDTBL(N,J,I) = FVAL

                  ADJLON = ADJLON - 5


  200          CONTINUE
cx    PRINT 2030, RLAT,(FLDTBL(N,J,I),I=1,17)
      write(7,2030)rlat,(fldtbl(n,j,i),i=1,17)
C
               ADJLAT = ADJLAT + 5
  300       CONTINUE
  500    CONTINUE
C
C        CALL SUBROUTINE TO OUTPUT +24 HOURS FORECAST POSITION
C
         KK = K
cx       CALL CSUFCST
         call csufcst( tlat1, tlon1, tlat2, tlon2 )
         if( kk .eq. 1 ) then
            ltlnwnd(1,1) = anint( tlat2*10.0 )
            ltlnwnd(1,2) = anint( tlon2*10.0 )
            ltlnwnd(2,1) = anint( tlat1*10.0 )
            ltlnwnd(2,2) = anint( tlon1*10.0 )
         else if( kk .eq. 2 ) then
            ltlnwnd(3,1) = anint( tlat2*10.0 )
            ltlnwnd(3,2) = anint( tlon2*10.0 )
            ltlnwnd(4,1) = anint( tlat1*10.0 )
            ltlnwnd(4,2) = anint( tlon1*10.0 )
         else if( kk .eq. 3 ) then
            ltlnwnd(5,1) = anint( tlat1*10.0 )
            ltlnwnd(5,2) = anint( tlon1*10.0 )
         endif

         IF (FLAT .NE. -999) GO TO 850
         print *, "BAD CYCLONE BASIN"
         STOP "CSUM: ABORTED, BAD CYCLONE BASIN"
C
  850 CONTINUE
      close (9)
c
c write the forecast to adeck file
c
      write(filename,'(a,a)')storms(1:ind),"/wptot.dat"
      call openfile (10,filename,'old',ioerror)
      if(ioerror.lt.0)go to 980
  860 continue
      read(10,'(a1)',end=870)cdummy
      go to 860
  870 continue
      call writeAid( 10, strmid, cent, tdtg, 'CSUM', ltlnwnd )
      close(10)

  899 STOP "CSUM: NORMAL RUN"
C
cx900 WRITE (19,1015)
cx    WRITE (19,1020) IELE(N), LDTG(ITM), NTAU
  900 CONTINUE
      write (*,1015)
      write (*,1020) iele(n), ldtg(itm), ntau
      STOP "CSUM: ABORTED, FIELD NOT FOUND"
  950 continue
      write (*,*)'cannot open ', filename
      stop "CSUM: ABORTED, CANNOT OPEN FILE"
  975 continue
      write (*,*)'cannot open csum.dbg'
      stop "CSUM: ABORTED, CANNOT OPEN csum.dbg"
  980 continue
      write (*,*)'cannot open ',filename
      stop "CSUM: ABORTED, CANNOT OPEN FILE"
  990 continue
      write (*,*)'cannot open ',filename
      stop "CSUM: ABORTED, CANNOT OPEN FILE"
C
C
c1000 FORMAT (/," FIELD ",5X,A3,2X,O20,2X,I3,2X,A1,/)
c1010 FORMAT (15X,"CSUM  FORECAST     TC ",A2,A1,", ",A3)
 1015 FORMAT (" NO CSUM FORECAST - FNOC FIELD NOT FOUND")
 1020 FORMAT (" *** FIELD NOT FOUND ***,",5X,A3,2X,A8,2X," TAU = ",I3)
 1030 FORMAT (10X,I3,A1,I4,A1,8X,A2,A1,7X,I3,10X,
     1         2(1X,I3,A1,I4,A1),A8)
 1040 FORMAT (" TAU",10X,"DTG",11X,"LAT",7X,"LONG",10X,"CATEGORY")
 1050 FORMAT (" ")
 1070 FORMAT (2X,I2.2,8X,A8,8X,F4.1,A1,5X,F5.1,A1,8X,A10,A5)
 1080 FORMAT (1X,"CSUM FORECASTS STARTING AT TAU = ",I2,
     1      " USED ",A8," FORECAST FIELDS.")
 1090 FORMAT (6X,A2)
 2000 FORMAT (A6,A2)
 2020 FORMAT(7X,17(2X,F5.1))
 2030 FORMAT(2X,F5.1,17(1X,F6.0))
C
      END
cx    SUBROUTINE CSUFCST
      subroutine csufcst(tlat1,tlon1,tlat2,tlon2)
C
C ********* CHANGE RECORD *********************************************
C
C     CSUFCST01 ( 7 JUL 89) ALLOW CYCLONE TO CROSS 180 LONGITUDE
C
C    CSUFCST02 (14 JUL 89) ELIMINATE ATLANTIC CAPABILITY AND CLEAN
C                          UP CODE FOR 12 HOUR POSITION
C
C     <<CHANGE NOTICE>> CSUFCST03 (27 FEB 92) -- CLIFFORD,M.
C               RESTORE ATLANTIC CAPABILITY.
C
C *********************************************************************
C
C     THIS SUBROUTINE CALLS THE ROUTINE TO FIGURE THE DIRECTION OF
C     MOTION, THEN IT STRATIFIES THE STORM INTO ON, NORTH OR SOUTH
C     OF THE RIDGE.  NEXT THE SUBROUTINE IS CALLED TO CALCULATE THE
C     +24 HOURS FORECAST POSTION.  SUBROUTINE HOUR IS CALLED TO
C     INTERPOLATE THE +12 HOURS POSITION.  THE +24 HOURS FORECAST
C     POSITION IS OUTPUT AND CONTROL IS RETURNED TO THE MAIN ROUTINE.
C
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, K
cx
      real tlat1, tlon1, tlat2, tlon2
      character*8 ldate
C
      DIMENSION YLAT(4), YLON(4)
cx    DIMENSION LOC1(3), LOC2(3)
      character*10 LOC1(3), LOC2(3)
      character lns*1, lew*1
C
      DATA LOC1 / 10HNORTH OF R, 10HON THE RID, 10HSOUTH OF R/
      DATA LOC2 / 5HIDGE , 5HGE   , 5HIDGE /
C
C***********************************************************************
C
C     CALL SUBROUTINE TO COMPUTE (DOM) DIRECTION OF MOTION
C
      SLON = AMOD ((360.0 -TLON(2)),360.0)
      ELON = AMOD ((360.0 -TLON(1)),360.0)
      CALL RHDST (TLAT(2),SLON,TLAT(1),ELON,DOM,DST)
      IDOM = DOM
C     PRINT *, " IDOM = ",IDOM
C
C     STRATIFY CYCLONES INTO ON, NORTH OR SOUTH OF THE RIDGE
C
      IL = 0
      IF (IDOM.GT.30 .AND. IDOM.LE.120) IL=1
      IF ((IDOM.GT.330 .AND. IDOM.LE.360) .OR.
     1     (IDOM.GE.0 .AND. IDOM.LE.30)) IL=2
      IF (TLAT(1).LE.15.0 .OR. (IDOM.GT.120.AND.IDOM.LE.330)) IL=3
cx    IF (IL .EQ. 0) WRITE (19,1090) IDOM
      if (il .eq. 0) write (*,1090) idom
C
C     AREA IS ATLANTIC OCEAN
C
      IF (IA .NE. 3) GO TO 100
         IF (IL .EQ. 1) CALL ATLNOTR
         IF (IL .EQ. 2) CALL ATLOTR
         IF (IL .EQ. 3) CALL ATLSOTR
         GO TO 500
C
C     AREA IS NORTH INDIAN OCEAN
C
  100 IF (IA .NE. 2) GO TO 200
         IF (IL .EQ. 1) CALL NIONOTR
         IF (IL .EQ. 2) CALL NIOOTR
         IF (IL .EQ. 3) CALL NIOSOTR
         GO TO 500
C
  200 IF (IA .EQ. 1) GO TO 300
cx       WRITE (19,1080) IA,TLON(1)
         write (*,1080) ia,tlon(1)
         FLAT = -999
         GO TO 999
C
C     AREA IS NORTHERN WEST PACIFIC
C
  300 IF (IL.EQ.1 .AND. IWIND.LT.90) CALL WPNOTR5
      IF (IL.EQ.1 .AND. IWIND.GE.90) CALL WPNOTR2
      IF (IL .EQ. 2) CALL WPOTR
      IF (IL .EQ. 3) CALL WPSOTR
C
cx500 LDATE = INCRDTG(LDATE,24)
  500 continue
      call icrdtg (ldate,ldate,24)
      LNS = 1HN
      LEW = 1HE
      IF (FLAT .LT. 0) LNS = 1HS
      FLONP = FLON
      IF (FLONP .GT.  180.0) FLONP = FLONP -360.0
      IF (FLONP .LT. -180.0) FLONP = 360.0 +FLONP
      IF (FLONP .LT.    0.0) LEW   = 1HW
      IF (ABS (FLONP) .EQ. 180.0) LEW = 1H
      IF (FLAT .EQ. -999) GO TO 999
C
C     OUTPUT +24 HOURS FORECAST POSITION
C
cx    WRITE (19,1070) (K*24),LDATE,ABS(FLAT),LNS,ABS(FLONP),LEW,
cx   1         LOC1(IL),LOC2(IL)
      write (*,1070) (k*24),ldate,abs(flat),lns,abs(flonp),lew,
     1         loc1(il),loc2(il)
C
      YLAT(1)=FLAT
      YLON(1)=FLON
      DO 650 I=1,3
         YLAT(I+1)=TLAT(I)
         YLON(I+1)=TLON(I)
  650 CONTINUE
      if (k.eq.1) then
C
C     INTERPOLATE LAT,LONG FOR TAU =12
C
        CALL HOUR (YLAT,ZLAT)
        CALL HOUR (YLON,ZLON)
        TLAT(3) = TLAT(1)
        TLON(3) = TLON(1)
        TLAT(2) = ZLAT
        TLON(2) = ZLON
        TLAT(1) = FLAT
        TLON(1) = FLON
cx      PRINT 1060, (K*24-12), TLAT(2), TLON(2)
cx      PRINT 1065, (K*24),    TLAT(1), TLON(1)
      elseif(k.eq.2) then
cx
cx  do 36 hour forecast
cx 
	tlat(3) = tlat(1)
	tlon(3) = tlon(1)
	tlat(2) = (flat + tlat(1))/2.
	tlon(2) = (flon + tlon(1))/2.
	tlat(1) = flat
	tlon(1) = flon
      else
	tlat(1) = flat
	tlon(1) = flon
      endif

      write(7,1060) (K*24-12), TLAT(2), TLON(2)
      write(7,1065) (K*24),    TLAT(1), TLON(1)
c
c  write to adeck character string
c
      tlat1=tlat(1)
      tlat2=tlat(2)
      if (lew.eq.'E') tlon1 = 360.0 - tlon(1)
      if (lew.eq.'E') tlon2 = 360.0 - tlon(2)
      if (lew.eq.'W') tlon1 = - tlon(1)
      if (lew.eq.'W') tlon2 = - tlon(2)

  999 RETURN
C
 1060 FORMAT (2X,I2.2,"-HOUR ESTIMATED POSITION IS : ",F6.2,F8.2)
 1065 FORMAT (2X,I2.2,"-HOUR  FORECAST POSITION IS : ",F6.2,F8.2)
 1070 FORMAT (2X,I2.2,8X,A8,8X,F4.1,A1,5X,F5.1,A1,8X,A10,A5)
 1080 FORMAT (" CSUM ERROR, UNIDENTIFIABLE TROPICAL CYCLONE",
     1   " BASIN, IA = ",I3,", LONGITUDE = ",F6.1)
 1090 FORMAT (" CSUM ERROR, DIR OF MOTION OUT OF RANGE, IDOM = ",I5)
      END
      SUBROUTINE WPNOTR2
C
C ********* CHANGE RECORD *********************************************
C
C     WPNOTR201 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR WESTERN PACIFIC TROPICAL CYCLONES,
C     NORTH OF THE RIDGE USING 200 MB STEERING.  THIS SUBROUTINE
C     SHOULD BE USED FOR TROPICAL CYCLONES WITH A WIND INTENSITY
C     OF 90 KNOTS OR GREATER.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     FLAT, FLON = RESULTANT FORECAST LATITUDE AND LONGITUDE
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .599, 2.781, -.407, .553, -4.198, -.289, -.479,
     1      4.766, -.532, 10.393, -4.958, .106, -1.639, -.031,
     1      1.911, -4.530, .155, 1.426, 1.568, -.137/
C
      DATA CU/ .191, .484, -3.952, .847, -5.038, .448, -.548,
     1      -.111, .224, 9.023, -2.589, -.088, -1.899, -.198,
     1      2.770, .230, -.068, .222, -4.979, 0/
C
C*********************************************************************
C
      CV0 = -3371.009
C
C           V  -12
      V(1) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C           P 15,25
      V(2) = F(3,6,14)
C
C           H 10,-5
      V(3) = F(1,5,8)
C
C           H 0,35
      V(4) = F(1,3,16)
C
C           P 10,-5
      V(5) = F(3,5,8)
C
C           ^H 20,-15
      V(6) = F(1,7,6) - F(2,7,6)
C
C           ^H 5,-10
      V(7) = F(1,4,7) - F(2,4,7)
C
C           ^P 0,10
      V(8) = F(3,3,11) - F(4,3,11)
C
C           H -10,0
      V(9) = F(1,1,9)
C
C           P -5,20
      V(10) = F(3,2,13)
C
C           P -5,40
      V(11) = F(3,2,17)
C
C           ^@ 200 N15 U
      V(12) = (F(5,5,9) - F(5,7,9)) /
     1         SIN((TLAT(1)+15)*3.1415926535898/180.) -
     1        (F(6,5,9) - F(6,7,9)) /
     1         SIN((TLAT(1)+15)*3.1415926535898/180.)
C
C           ^P 20,35
      V(13) = F(3,7,16) - F(4,7,16)
C
C           @ 200 NW10-5 U
      V(14) = (F(5,4,7) - F(5,6,7)) /
     1         SIN((TLAT(1)+10)*3.1415926535898/180.) -
     1        (F(5,3,8) - F(5,5,8)) /
     1         SIN((TLAT(1)+5)*3.1415926535898/180.)
C
C           ^P 25,0
      V(15) = F(3,8,9) - F(4,8,9)
C
C           ^P 0,30
      V(16) = F(3,3,15) - F(4,3,15)
C
C           ^H 15,40
      V(17) = F(1,6,17) - F(2,6,17)
C
C           ^P 30,-40
      V(18) = F(3,9,1) - F(4,9,1)
C
C           P 25,15
      V(19) = F(3,8,12)
C
C           ^H 30,-35
      V(20) = F(1,9,2) - F(2,9,2)
C
C------------------------------------------------------------------
C
      CU0 = 2567.649
C
C           @ 500 U
      U(1) = ((F(1,1,7) + F(1,1,8) + F(1,1,9) + F(1,1,10) + F(1,1,11))
     1      - (F(1,5,7) + F(1,5,8) + F(1,5,9) + F(1,5,10) + F(1,5,11)))
     1      / (5 * SIN(TLAT(1)*3.1415926535898/180.))
C
C           U -12
      U(2) = 1111.949 * COS(((TLAT(1)+TLAT(2))/2)*3.1415926535898/180.)
     1         * (TLON(1) - TLON(2))/12
C
C           ^P 10,5
      U(3) = F(3,5,10) - F(4,5,10)
C
C           H -5,15
      U(4) = F(1,2,12)
C
C           P 0,40
      U(5) = F(3,3,17)
C
C           ^H 10,-30
      U(6) = F(1,5,3) - F(2,5,3)
C
C           H -10,-30
      U(7) = F(1,1,3)
C
C           @ 200 NW20 V
      U(8) =  (F(5,7,6) - F(5,7,4)) /
     1         (SIN((TLAT(1)+20)*3.1415926535898/180.) *
     1           COS((TLAT(1)+20)*3.1415926535898/180.))
C
C           V  -12
      U(9) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C           ^P -10,25
      U(10) = F(3,1,14) - F(4,1,14)
C
C           ^P 25,-40
      U(11) = F(3,8,1) - F(4,8,1)
C
C           ^@ 200 NW15 U
      U(12) = (F(5,5,6) - F(5,7,6)) /
     1         SIN((TLAT(1)+15)*3.1415926535898/180.) -
     1        (F(6,5,6) - F(6,7,6)) /
     1         SIN((TLAT(1)+15)*3.1415926535898/180.)
C
C           P 25,40
      U(13) = F(3,8,17)
C
C           @ 500 V
      U(14) = ((F(1,1,11) + F(1,2,11) + F(1,3,11) +
     1          F(1,4,11) + F(1,5,11)) -
     1         (F(1,1,7) + F(1,2,7) + F(1,3,7) + F(1,4,7) + F(1,5,7)))
     1        / (5 * SIN(TLAT(1)*3.1415926535898/180.) *
     1           COS(TLAT(1)*3.1415926535898/180.) )
C
C           P 15,-40
      U(15) = F(3,6,1)
C
C           ^H 35,-5
      U(16) = F(1,10,8) - F(2,10,8)
C
C           @ 200 N20 U
      U(17) = (F(5,6,9) - F(5,8,9)) /
     1         SIN((TLAT(1)+20)*3.1415926535898/180.)
C
C           ^H 15,40
      U(18) = F(1,6,17) - F(2,6,17)
C
C           ^P 0,40
      U(19) = F(3,3,17) - F(4,3,17)
      U(20) = 0
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
 200  CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE WPNOTR5
C
C ********* CHANGE RECORD *********************************************
C
C     WPNOTR501 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR WESTERN PACIFIC TROPICAL CYCLONES,
C     NORTH OF THE RIDGE USING 500 MB STEERING.  THIS SUBROUTINE
C     SHOULD BE USED FOR TROPICAL CYCLONES WITH A WIND INTENSITY
C     OF LESS THAN 90 KNOTS.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     FLAT, FLON = RESULTANT FORECAST LATITUDE AND LONGITUDE
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ 4.427, .552, 1.776, -8.952, 8.643, .118, .400, -.527,
     1      -5.029, -1.584, .072, .364, -4.057, -.437, .174, .692,
     1      5.807, 4.216, -1.535, .081/
C
      DATA CU/ .430, -.345, .205, -4.643, .496, .698, -2.940, -5.845,
     1      -.145, 4.377, -.353, .368, -.300, -.757, 2.004, -1.495,
     1      -.929, .105, -2.804, -.072/
C
C*********************************************************************
C
      CV0 = 108.378
C
C           ^P -5,-35
      V(1) = F(3,2,2) - F(4,2,2)
C
C           V  -12
      V(2) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C           P 15,30
      V(3) = F(3,6,15)
C
C           P 5,0
      V(4) = F(3,4,9)
C
C           P 0,15
      V(5) = F(3,3,12)
C
C           ^@ 500 V
      V(6) =   ((F(1,1,11) + F(1,2,11) + F(1,3,11) +
     1          F(1,4,11) + F(1,5,11)) -
     1         (F(1,1,7) + F(1,2,7) + F(1,3,7) + F(1,4,7) + F(1,5,7)) )
     1        / (5 * SIN(TLAT(1)*3.1415926535898/180.) *
     1          COS(TLAT(1)*3.1415926535898/180.) )
     1        -
     1         ((F(2,1,11) + F(2,2,11) + F(2,3,11) +
     1          F(2,4,11) + F(2,5,11)) -
     1         (F(2,1,7) + F(2,2,7) + F(2,3,7) + F(2,4,7) + F(2,5,7)) )
     1        / (5 * SIN(TLAT(1)*3.1415926535898/180.) *
     1           COS(TLAT(1)*3.1415926535898/180.) )
C
C           H 0,30
      V(7) = F(1,3,15)
C
C           H 5,-5
      V(8) = F(1,4,8)
C
C           P -10,40
      V(9) = F(3,1,17)
C
C           ^P 25,-20
      V(10) = F(3,8,5) - F(4,8,5)
C
C           @ 500 N20 V      (H 20,5 - H 20,-5) / (SIN(LAT) * COS(LAT))
      V(11) = (F(1,7,10) - F(1,7,8)) /
     1         ( SIN((TLAT(1)+20)*3.1415926535898/180.) *
     1           COS((TLAT(1)+20)*3.1415926535898/180.) )
C
C           ^H 5,-25
      V(12) = F(1,4,4) - F(2,4,4)
C
C           ^P 5,-15
      V(13) = F(3,4,6) - F(4,4,6)
C
C           ^H 0,30
      V(14) = F(1,3,15) - F(2,3,15)
C
C           ^H 10,40
      V(15) = F(1,5,17) - F(2,5,17)
C
C           ^H -10,35
      V(16) = F(1,1,16) - F(2,1,16)
C
C           ^P -10,20
      V(17) = F(3,1,13) - F(4,1,13)
C
C           P -5,0
      V(18) = F(3,2,9)
C
C           ^P 15,35
      V(19) = F(3,6,16) - F(4,6,16)
C
C           ^@ 500 N10-5 U
      V(20) = (((F(1,4,9) - F(1,6,9)) /
     1         SIN((TLAT(1)+10)*3.1415926535898/180.)) -
     1        ((F(1,3,9) - F(1,5,9)) /
     1         SIN((TLAT(1)+5.0)*3.141592654/180.0))) -
     1       (((F(2,4,9) - F(2,6,9)) /
     1         SIN((TLAT(1)+10)*3.1415926535898/180.)) -
     1        ((F(2,3,9) - F(2,5,9)) /
     1         SIN((TLAT(1)+5.0)*3.141592654/180.0)))
C
C------------------------------------------------------------------
C
      CU0 = 11215.979
C
C           U -12
      U(1) = 1111.949 * COS(((TLAT(1)+TLAT(2))/2)*3.1415926535898/180.)
     1           * (TLON(1) - TLON(2))/12
C
C           H 15,0
      U(2) = F(1,6,9)
C
C           V -12
      U(3) = 1111.949 * (TLAT(1)-TLAT(2))/12
C
C           P 0,40
      U(4) = F(3,3,17)
C
C           ^H 10,-30
      U(5) = F(1,5,3) - F(2,5,3)
C
C           H -5,10
      U(6) = F(1,2,11)
C
C           ^P 25,-40
      U(7) = F(3,8,1) - F(4,8,1)
C
C           ^P 5,5
      U(8) = F(3,4,10) - F(4,4,10)
C
C           ^H 25,20
      U(9) = F(1,8,13) - F(2,8,13)
C
C           ^P 0,15
      U(10) = F(3,3,12) - F(4,3,12)
C
C           H -10,-30
      U(11) = F(1,1,3)
C
C           H 0,35
      U(12) = F(1,3,16)
C
C           H 10,15
      U(13) = F(1,5,12)
C
C           H -10,40
      U(14) = F(1,1,17)
C
C           ^P 35,-35
      U(15) = F(3,10,2) - F(4,10,2)
C
C           P 10,5
      U(16) = F(3,5,10)
C
C           P 25,40
      U(17) = F(3,8,17)
C
C           ^H 15,40
      U(18) = F(1,6,17) - F(2,6,17)
C
C           ^P 10,0
      U(19) = F(3,5,9) - F(4,5,9)
C
C           @ 500 NW10-5 U
      U(20) = (F(1,4,7)-F(1,6,7)) /
     1         SIN((TLAT(1)+10)*3.1415926535898/180.) -
     1         (F(1,3,8)-F(1,5,8)) /
     1          SIN((TLAT(1)+5)*3.1415926535898/180.)
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
 200  CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE WPOTR
C
C ********* CHANGE RECORD *********************************************
C
C     WPOTR*01 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR WESTERN PACIFIC TROPICAL CYCLONES
C     ON THE RIDGE, USING 500 MB STEERING.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C     FLAT, FLON = RESULTANT FORECAST LATITUDE AND LONGITUDE
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ -.055, .534, -1.025, 5.968, -7.715, -.191,
     1      3.423, .092, -1.182, -.124, -.290, 2.851,
     1      -.090, .374, -.069, .180, -5.257, 1.068,
     1      4.664, -.229/
C
      DATA CU/ -.597, .319, .198, -.130, -.669, .191, 6.560,
     1      .401, 5.444, 1.463, -2.644, -.082, 1.603,
     1      .693, -3.718, .200, -.168, .092, -.050, 0/
C
C********************************************************************
C
      CV0 = -4613.508
C
C           H 20,40
      V(1) = F(1,7,17)
C
C           V -12
      V(2) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C           H 5,-10
      V(3) = F(1,4,7)
C
C           P 0,40
      V(4) = F(3,3,17)
C
C           ^P -10,-10
      V(5) = F(3,1,7) - F(4,1,7)
C
C           ^H 20,-15
      V(6) = F(1,7,6) - F(2,7,6)
C
C           P -10,-40
      V(7) = F(3,1,1)
C
C           H 30,15
      V(8) = F(1,9,12)
C
C           P 30,10
      V(9) = F(3,9,11)
C
C           U -24
      V(10) = 1111.949 * COS((TLAT(1)+TLAT(3))/2*3.1415926535898/180.)
     1           * (TLON(1) - TLON(3))/24
C
C           ^H 15,-30
      V(11) = F(1,6,3) - F(2,6,3)
C
C           ^P 5,15
      V(12) = F(3,4,12) - F(4,4,12)
C
C           @ 500 N10-5 U
      V(13) = ((F(1,4,9) - F(1,6,9)) /
     1         SIN((TLAT(1)+10)*3.1415926535898/180.) ) -
     1        ((F(1,3,9) - F(1,5,9)) /
     1         SIN((TLAT(1)+5)*3.1415926535898/180.) )
C
C             H 0,10
      V(14) = F(1,3,11)
C
C           ^H 35,35
      V(15) = F(1,10,16) - F(2,10,16)
C
C           ^H 15,-40
      V(16) = F(1,6,1) - F(2,6,1)
C
C           ^P -10,5
      V(17) = F(3,1,10) - F(4,1,10)
C
C           ^P 30,-40
      V(18) = F(3,9,1) - F(4,9,1)
C
C           ^P 0,-15
      V(19) = F(3,3,6) - F(4,3,6)
C
C           ^H 10,-15
      V(20) = F(1,5,6) - F(2,5,6)
C
C--------------------------------------------------------------------
C
      CU0 = -3312.594
C
C           H 5,-5
      U(1) = F(1,4,8)
C
C           U -12
      U(2) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1         * (TLON(1) - TLON(2))/12
C
C           @ 500 NW5 U
      U(3) = (F(1,3,8) - F(1,5,8)) /
     1         SIN((TLAT(1)+5)*3.1415926535898/180.)
C
C           H 15,25
      U(4) = F(1,6,14)
C
C           ^H 5,-10
      U(5) = F(1,4,7) - F(2,4,7)
C
C           V -24
      U(6) = 1111.949 * (TLAT(1) - TLAT(3))/24
C
C           ^P -10,-30
      U(7) = F(3,1,3) - F(4,1,3)
C
C           H 0,40
      U(8) = F(1,3,17)
C
C           P -10,-5
      U(9) = F(3,1,8)
C
C           ^P 25,-5
      U(10) = F(3,8,8) - F(4,8,8)
C
C           ^P 10,15
      U(11) = F(3,5,12) - F(4,5,12)
C
C           ^H 20,-5
      U(12) = F(1,7,8) - F(2,7,8)
C
C           ^P 30,-40
      U(13) = F(3,9,1) - F(4,9,1)
C
C           P 35,35
      U(14) = F(3,10,16)
C
C           ^P -10,40
      U(15) = F(3,1,17) - F(4,1,17)
C
C           ^H 25,-35
      U(16) = F(1,8,2) - F(2,8,2)
C
C           H 5,20
      U(17) = F(1,4,13)
C
C           ^@ 500 N10-5 V
      SIN10 = SIN((TLAT(1)+10)*3.1415926535898/180.)
      SIN5 = SIN((TLAT(1)+5)*3.1415926535898/180.)
      COS10 = COS((TLAT(1)+10)*3.1415926535898/180.)
      COS5 = COS((TLAT(1)+5)*3.1415926535898/180.)
      U(18) = ((F(1,5,10)-F(1,5,8)) / (SIN10 * COS10)
     1      - (F(1,4,10)-F(1,4,8)) / (SIN5 * COS5))
     1      -
     1        ((F(2,5,10)-F(2,5,8)) / (SIN10 * COS10)
     1      - (F(2,4,10)-F(2,4,8)) / (SIN5 * COS5))
C
C           ^H 30,40
      U(19) = F(1,9,17) - F(2,9,17)
      U(20) = 0
C
C---------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE WPSOTR
C
C ********* CHANGE RECORD *********************************************
C
C     WPSOTR*01 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR WESTERN PACIFIC TROPICAL CYCLONES
C     SOUTH OF THE RIDGE, USING 500 MB STEERING.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .506, .257, 2.465, -7.410, .348, -.302, .057,
     1      -.420, -.102, -.179, 4.560, -1.651, -2.944,
     1      .247, .150, -.612, .323, .030, 0, 0/
C
      DATA CU / .604, -.417, -.508, -.117, -1.327, .059,
     1      5.807, .245, -.437, 6.250, -2.749, -2.675, .266,
     1      -.898, -.090, 1.477, 5.361, -.315, -2.094, 0/
C
C********************************************************************
C
      CV0 = -1280.997
C
C           V -12
      V(1) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C           H 15,5
      V(2) = F(1,6,10)
C
C           ^P 5,15
      V(3) = F(3,4,12) - F(4,4,12)
C
C           ^P -10,-10
      V(4) = F(3,1,7) - F(4,1,7)
C
C           H -5,15
      V(5) = F(1,2,12)
C
C           H 5,-5
      V(6) = F(1,4,8)
C
C           ^H 35,-35
      V(7) = F(1,10,2) - F(2,10,2)
C
C           P 35,15
      V(8) = F(3,10,12)
C
C           ^H 15,30
      V(9) = F(1,6,15) - F(2,6,15)
C
C           ^H 15,-25
      V(10) = F(1,6,4) - F(2,6,4)
C
C           P -5,10
      V(11) = F(3,2,11)
C
C           P 10,0
      V(12) = F(3,5,9)
C
C           P -10,40
      V(13) = F(3,1,17)
C
C           ^H -5,25
      V(14) = F(1,2,14) - F(2,2,14)
C
C           ^H 5,-20
      V(15) = F(1,4,5) - F(2,4,5)
C
C           ^H -10,-5
      V(16) = F(1,1,8) - F(2,1,8)
C
C           ^H -5,5
      V(17) = F(1,2,10) - F(2,2,10)
C
C           U -12
      V(18) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1          * (TLON(1) - TLON(2))/12
      V(19) = 0
      V(20) = 0
C
C--------------------------------------------------------------------
C
      CU0 = 3133.007
C
C           U -12
      U(1) = V(18)
C
C           H 10,-10
      U(2) = F(1,5,7)
C
C           ^H 5,5
      U(3) = F(1,4,10) - F(2,4,10)
C
C           V -12
      U(4) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C           ^P 15,10
      U(5) = F(3,6,11) - F(4,6,11)
C
C           H 35,-20
      U(6) = F(1,10,5)
C
C           ^P -10,10
      U(7) = F(3,1,11) - F(4,1,11)
C
C           H 5,-40
      U(8) = F(1,4,1)
C
C           P 35,30
      U(9) = F(3,10,15)
C
C           ^P -10,-35
      U(10) = F(3,1,2) - F(4,1,2)
C
C           ^P 5,15
      U(11) = F(3,4,12) - F(4,4,12)
C
C           P 5,25
      U(12) = F(3,4,14)
C
C           ^H 5,20
      U(13) = F(1,4,13) - F(2,4,13)
C
C           ^P 15,30
      U(14) = F(3,6,15) - F(4,6,15)
C
C           H 20,40
      U(15) = F(1,7,17)
C
C           P 15,40
      U(16) = F(3,6,17)
C
C           ^P -10,-10
      U(17) = F(3,1,7) - F(4,1,7)
C
C           P 30,-15
      U(18) = F(3,9,6)
C
C           ^P 5,5
      U(19) = F(3,4,10) - F(4,4,10)
      U(20) = 0
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END

C**********************************************************************
      SUBROUTINE HOUR (YG,Z)
C
C * * * * * CHANGE RECORD * * * * * * * * * * * * * * * * * * * * * * *
C
C     HOUR*01 (14 JULY 89)  REDUCE MEMORY BY CALCULATING ONLY 12-HOUR
C                           POSITION BASED ON FOUR POINTS
C
C * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
C
C   THIS ROUTINE CALCULATES THE TROPICAL CYCLONE LATITUDE
C   OR LONGITUDE POSITION FOR HOUR 12 BASED ON INPUT POSITIONS WHICH
C   CORRESPOND TO FIX TIMES OF -24, -12 AND 0, AND 24 HR FORECAST.
C
C   INPUT ARRAY YG IS EITHER LATITUDE OR LONGITUDE POSITIONS.
C   OUTPUT VALUE Z IS THE ESTIMATED 12 HOUR LATITUDE OR LONGITUDE.
C
C   HOUR CALLS SLOP TO CALCULATE THE SLOPE AT EACH OF THE FOUR POINTS.
C
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      DIMENSION YG(4)
      DIMENSION Y(4), S(4), T(4)
C                   THE X-VALUES IN TERMS OF TIME IN HOURS
      DATA T/0.0, 12.0, 24.0, 48.0/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C                   REVERSE ORDER OF LATITUDE OR LONGITUDE
      Y(1) = YG(4)
      Y(2) = YG(3)
      Y(3) = YG(2)
      Y(4) = YG(1)
C                   CALCULATE THE SLOPES, S, AT THE FOUR POSITIONS
      CALL SLOP (Y,T,S)
C                   ESTIMATE Z (Y) FOR T (X) OF 36 HOURS
      DY = Y(4) -Y(3)
      DT = 1.0/24.0
      P2 = DT*(3.0*DY*DT -2.0*S(3) -S(4))
      P3 = DT*DT*(S(3) +S(4) -2.0*DY*DT)
      Z  = Y(3) +12.0*(S(3) +12.0*(P2 +12.0*P3))
      RETURN
C
      END
      SUBROUTINE SLOP (Y,X,T)
C
C * * * * * CHANGE RECORD * * * * * * * * * * * * * * * * * * * * * * *
C
C     SLOP*01 (14 JULY 89)  LIMIT CALCULATIONS TO FOUR POINTS
C
C * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
C
C
C  THIS ROUTINE 'SLOP' CALCULATES THE SLOPES T OF Y OVER X AXIS
C   AT EACH OF THE M POINTS.  REFERENCE: AKIMA 1970, J. OF THE ASSOC.
C   FOR COMPUTING MACHINERY, 589-602.
C
      DIMENSION Y(4),X(4),T(4)
      DIMENSION WORK(7)
C
C
      DO 100 I=2, 4
      WORK(I+1)=(Y(I)-Y(I-1))/(X(I)-X(I-1))
100   CONTINUE
C
      WORK(1)=3.*WORK(3)-2.*WORK(4)
      WORK(2)=2.*WORK(3)-   WORK(4)
      WORK(6) = 2.0*WORK(5) -WORK(4)
      WORK(7) = 3.0*WORK(5) -2.0*WORK(4)
C
C
      DO 200 I=1, 4
      A=ABS(WORK(I+3)-WORK(I+2))
      B=ABS(WORK(I+1)-WORK(I)  )
      IF(A.NE.0. .OR. B.NE.0.) GO TO 220
      T(I)=0.5*(WORK(I+1)+WORK(I+2))
      GO TO 200
220   T(I)=(A*WORK(I+1) + B*WORK(I+2))/(A+B)
200   CONTINUE
C
C
      RETURN
      END
      SUBROUTINE ATLNOTR
C********CHANGE RECORD*******************************************
C
C     <<CHANGE NOTICE>> ATLNOTR01 (27 FEB 92) -- CLIFFORD,M.
C               CORRECT CODE ERROR.
C
C
C     THIS SUBROUTINE IS FOR ATLANTIC CYCLONES NORTH OF THE RIDGE,
C     200 MB STEERING IS USED.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .377, .304, -.170, -7.026, .460, -.112,
     1       1.661, 2.433, 2.693, -.237, .417, 2.044,
     1       -.464, 5.705, .097, -.348, 3.762, -5.302,
     1       .296, -.146/
C
      DATA CU/ .583, -4.999, .220, 3.103, .133, 2.821,
     1       .583, 1.731, -.485, -2.112, 8.311, -2.144,
     1       .169, -3.821, 2.712, .072, 1.475, -.117,
     1       -1.212, 1.629/
C
C***********************************************************************
C
      CV0 = -3159.411
C
C        @ 500 V
      V(1) = ((F(1,1,11) + F(1,2,11) + F(1,3,11) +
     1      F(1,4,11) + F(1,5,11)) -
     1     (F(1,1,7) + F(1,2,7) + F(1,3,7) + F(1,4,7) + F(1,5,7)))
     1    /  (5 * SIN(TLAT(1)*3.1415926535898/180.) *
     1       COS(TLAT(1)*3.1415926535898/180.) )
C
C        V -12
      V(2) = 1111.949 * (TLAT(1)-TLAT(2))/12
C
C        ^@ 200 N5 U
      V(3) = ((F(5,3,9) - F(5,5,9)) /
     1       SIN((TLAT(1)+5.)*3.1415926535898/180.)) -
     1      ((F(6,3,9) - F(6,5,9)) /
     1       SIN((TLAT(1)+5.)*3.1415926535898/180.))
C
C        P 5,0
      V(4) = F(3,4,9)
C
C        H -5,-35
      V(5) = F(1,2,2)
C
C        @ 200 NW10-5 U
      V(6) = ((F(5,4,7) - F(5,6,7)) /
     1       SIN((TLAT(1)+10.)*3.1415926535898/180.)) -
     1     ((F(5,3,8) - F(5,5,8)) /
     1        SIN((TLAT(1)+5.)*3.1415926535898/180.))
C
C        ^P 20,30
      V(7) = F(3,7,15) - F(4,7,15)
C
C        P 0,15
      V(8) = F(3,3,12)
C
C        P 10,-30
      V(9) = F(3,5,3)
C
C        ^H 0,-35
      V(10) = F(1,3,2) - F(2,3,2)
C
C        H 0,15
      V(11) = F(1,3,12)
C
C        ^P 10,15
      V(12) = F(3,5,12) - F(4,5,12)
C
C        ^H -5,-15
      V(13) = F(1,2,6) - F(2,2,6)
C
C        ^P -5,-10
      V(14) = F(3,2,7) - F(4,2,7)
C
C        ^H 30,10
      V(15) = F(1,9,11) - F(2,9,11)
C
C        ^H 5,-10
      V(16) = F(1,4,7) - F(2,4,7)
C
C        ^P -5,20
      V(17) = F(3,2,13) - F(4,2,13)
C
C        ^P -10,0
      V(18) = F(3,1,9) - F(4,1,9)
C
C        ^H -5,-5
      V(19) = F(1,2,8) - F(2,2,8)
C
C        ^H 0,40
      V(20) = F(1,3,17) - F(2,3,17)
C
C-----------------------------------------------------------------------
C
      CU0 = -6405.097
C
C        U -12
      U(1) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(2))/12
C
C        P 10,0
      U(2) = F(3,5,9)
C
C        @ 200 NW 5U
      U(3) = (F(5,3,8) - F(5,5,8)) /
     1       SIN((TLAT(1)+5.)*3.1415926535898/180.)
C
C        P 10,-30
      U(4) = F(3,5,3)
C
C        V -24
      U(5) = 1111.949 * (TLAT(1)-TLAT(3))/24
C
C        ^P 35,-30
      U(6) = F(3,10,3) - F(4,10,3)
C
C        H -10,15
      U(7) = F(1,1,12)
C
C        P 30,0
      U(8) = F(3,9,9)
C
C        ^H 5,-5
      U(9) = F(1,4,8) - F(2,4,8)
C
C        ^P 30,40
      U(10) = F(3,9,17) - F(4,9,17)
C
C        ^P -10,35
      U(11) = F(3,1,16) - F(4,1,16)
C
C        ^P 10,40
      U(12) = F(3,5,17) - F(4,5,17)
C
C        ^H 10,10
      U(13) = F(1,5,11) - F(2,5,11)
C
C        ^P 0,20
      U(14) = F(3,3,13) - F(4,3,13)
C
C        P 0,30
      U(15) = F(3,3,15)
C
C        H 30,40
      U(16) = F(1,9,17)
C
C        ^P 25,30
      U(17) = F(3,8,15) - F(4,8,15)
C
C        ^H 10,-20
      U(18) = F(1,5,5) - F(2,5,5)
C
C        ^P 25,-30
      U(19) = F(3,8,3) - F(4,8,3)
C
C        ^P 5,-40
      U(20) = F(3,4,1) - F(4,4,1)
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT=0.5*(FLAT + TLAT(1))*3.1415926535898/180.0
      FLON=TLON(1) + (UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE ATLOTR
C*******CHANGE RECORD********************************************
C
C     <<CHANGE NOTICE>> ATLOTR*01 (27 FEB 92) -- CLIFFORD,M.
C               CORRECT CODE ERROR.
C
C****************************************************************
C
C     THIS SUBROUTINE IS FOR ATLANTIC CYCLONES ON THE RIDGE.
C     THIS SUBROUTINE USES 200 MB STEERING.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .359, .454, .178, 4.351, -2.210, .955,
     1       2.535, -.087, -.240, -.437, 2.460, .126,
     1       -1.430, -.035, -.515, -.372, .063, .261,
     1       -.045, 0.0/
C
      DATA CU/ .308, .536, .508, -.055, -.938, 9.708,
     1       .958, .249, .087, 2.444, -.154, 2.661,
     1       3.834, -2.787, .149, -3.878, -1.689,
     1       .096, -2.834, 5.173/
C
C***********************************************************************
      PIE = 3.1415926535898
      TSIN = (5 * SIN(TLAT(1)*3.1415926535898/180.) *
     1       COS(TLAT(1)*3.1415926535898/180.))
C
      CV0 = -5549.292
C
C        @ 500 V
      V(1) = ((F(1,1,11) + F(1,2,11) + F(1,3,11) +
     1      F(1,4,11) + F(1,5,11)) -
     1     (F(1,1,7) + F(1,2,7) + F(1,3,7) + F(1,4,7) + F(1,5,7)))
     1     / TSIN
C
C        V -12
      V(2) = 1111.949 * (TLAT(1)-TLAT(2))/12
C
C        ^@ 200 V
cx   Correction according to csu paper 379 page 47, v component.
cx   ajs 5/00
cx    V(3) = ( ((F(5,1,11)+F(5,2,11)+F(5,3,11)+F(5,4,11)+F(5,5,11))
cx   1      -(F(5,1,7)+F(5,2,7)+F(5,3,7)+F(5,4,7)+F(5,5,7)))
cx   1      / TSIN)
cx   1      -
cx   1  ( ((F(6,1,11)+F(6,2,11)+F(6,3,11)+F(6,4,11)+F(6,5,11))
cx   1      -(F(6,11,7)+F(6,2,7)+F(6,3,7)+F(6,4,7)+F(6,5,7)))
cx   1      / TSIN)
      V(3) = ( ((F(5,1,11)+F(5,2,11)+F(5,3,11)+F(5,4,11)+F(5,5,11))
     1      -(F(5,1,7)+F(5,2,7)+F(5,3,7)+F(5,4,7)+F(5,5,7)))
     1      / TSIN)
     1      -
     1  ( ((F(6,1,11)+F(6,2,11)+F(6,3,11)+F(6,4,11)+F(6,5,11))
     1      -(F(6,1,7)+F(6,2,7)+F(6,3,7)+F(6,4,7)+F(6,5,7)))
     1      / TSIN)
C
C        ^P 0,40
      V(4) = F(3,3,17) - F(4,3,17)
C
C        ^P 5,-20
      V(5) = F(3,4,5) - F(4,4,5)
C
C        H -10,-25
      V(6) = F(1,1,4)
C
C        ^P 15,15
      V(7) = F(3,6,12) - F(4,6,12)
C
C        @ 200 NW 10-5 V
      V(8) = ((F(5,5,8) - F(5,5,6))
     1       / (SIN((TLAT(1)+10)*PIE/180.)*COS((TLAT(1)+10)*PIE/180.)))
     1   -
     1      ((F(5,4,9) - F(5,4,7))
     1      / (SIN((TLAT(1)+5)*PIE/180.)*COS((TLAT(1)+5)*PIE/180.)))
C
C        U -24
      V(9) = 1111.949 * COS((TLAT(1)+TLAT(3))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(3))/24
C
C        ^H -10,10
      V(10) = F(1,1,11) - F(2,1,11)
C
C        ^P 20,40
      V(11) = F(3,7,17) - F(4,7,17)
C
C        ^H 30,-40
      V(12) = F(1,9,1) - F(2,9,1)
C
C        ^P 35,-20
      V(13) = F(3,10,5) - F(4,10,5)
C
C        @ 200 NW20 V
      V(14) = (F(5,7,6) - F(5,7,4)) /
     1        (SIN((TLAT(1)+20)*3.1415926535898/180.) *
     1         COS((TLAT(1)+20)*3.1415926535898/180.))
C
C        ^H 0,-30
      V(15) = F(1,3,3) - F(2,3,3)
C
C        ^H -10,-10
      V(16) = F(1,1,7) - F(2,1,7)
C
C        ^@ 200 N10-5 V
      SC10 = SIN((TLAT(1)+10)*PIE/180.)*COS((TLAT(1)+10)*PIE/180.)
      SC5 = SIN((TLAT(1)+5)*PIE/180.)*COS((TLAT(1)+5)*PIE/180.)
      V(17) = (((F(5,5,10) - F(5,5,8)) / SC10) -
     1        ((F(5,4,10) - F(5,4,8)) / SC5)) -
     1        (((F(6,5,10) - F(6,5,8)) / SC10) -
     1         ((F(6,4,10) - F(6,4,8)) / SC5))
C
C        ^H 0,-40
      V(18) = F(1,3,1) - F(2,3,1)
C
C        @ 200 N10-5 U
      V(19) = ((F(5,4,9) - F(5,6,9))
     1        / SIN((TLAT(1)+10)*3.1415926535898/180.)) -
     1        ((F(5,3,9) - F(5,5,9))
     1       / SIN((TLAT(1)+5)*3.1415926535898/180.))
      V(20) = 0.0
C
C-----------------------------------------------------------------------
C
      CU0 = -17982.797
C
C        @ 500 U
      U(1) = ((F(1,1,7) + F(1,1,8) + F(1,1,9) +
     1       F(1,1,10) + F(1,1,11)) -
     1      (F(1,5,7)+F(1,5,8)+F(1,5,9)+F(1,5,10)+F(1,5,11))) /
     1      (5*SIN(TLAT(1)*3.1415926535898/180.))
C
C        H 0,5
      U(2) = F(1,3,10)
C
C        U -12
      U(3) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(2))/12
C
C        ^@ 200 NW20 V
      U(4) = ((F(5,7,6) - F(5,7,4))
     1      / (SIN((TLAT(1)+20.)*PIE/180.)*COS((TLAT(1)+20.)*PIE/180.)))
     1      - ((F(6,7,6) - F(6,7,4))
     1     / (SIN((TLAT(1)+20.)*PIE/180.)*COS((TLAT(1)+20.)*PIE/180.)))
C
C        ^H -10,-20
      U(5) = F(1,1,5) - F(2,1,5)
C
C        P -5,25
      U(6) = F(3,2,14)
C
C        ^P 30,30
      U(7) = F(3,9,15) - F(4,9,15)
C
C        H 15,-40
      U(8) = F(1,6,1)
C
C        @ 200 NW15 U
      U(9) = (F(5,5,6) - F(5,7,6))
     1       / SIN((TLAT(1)+15.)*3.1415926535898/180.)
C
C        P 35,-10
      U(10) = F(3,10,7)
C
C        ^H 15,-35
      U(11) = F(1,6,2) - F(2,6,2)
C
C        ^P 20,5
      U(12) = F(3,7,10) - F(4,7,10)
C
C        P 0,-35
      U(13) = F(3,3,2)
C
C        P 10,25
      U(14) = F(3,5,14)
C
C        ^H 20,20
      U(15) = F(1,7,13) - F(2,7,13)
C
C        ^P 5,20
      U(16) = F(3,4,13) - F(4,4,13)
C
C        ^P 15,-25
      U(17) = F(3,6,4) - F(4,6,4)
C
C        ^H 30,-40
      U(18) = F(1,9,1) - F(2,9,1)
C
C        ^P 10,0
      U(19) = F(3,5,9) - F(4,5,9)
C
C        ^P -5,-15
      U(20) = F(3,2,6) - F(4,2,6)
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT=0.5*(FLAT + TLAT(1))*3.1415926535898/180.0
      FLON=TLON(1) + (UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE ATLSOTR
C******CHANGE RECORD*********************************************
C
C     <<CHANGE NOTICE>> ATLSOTR01 (27 FEB 92) -- CLIFFORD,M.
C               CORRECT CODE ERROR.
C
C****************************************************************
C
C     THIS SUBROUTINE IS FOR ATLANTIC CYCLONES SOUTH OF THE RIDGE.
C     THIS SUBROUTINE USES 200 MB STEERING.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .469, .211, -.407, .245, -1.149, 10.404,
     1        -11.122, -6.875, 2.995, 1.700, -1.197, -3.636,
     1        5.374, -.742, .932, .163, -1.963, 3.443,
     1        1.040, -.082/
C
      DATA CU/ .321, -.465, -.376, 2.603, -2.147, .635,
     1        -.124, .178, -.264, .674, .717, 2.583,
     1        -.476, -5.704, .827, 0.0, 0.0, 0.0, 0.0, 0.0/
C
C***********************************************************************
C
      CV0 = -9080.922
C
C        V -12
      V(1) = 1111.949 * (TLAT(1)-TLAT(2))/12
C
C        H 15,5
      V(2) = F(1,6,10)
C
C        ^H 5,-15
      V(3) = F(1,4,6) - F(2,4,6)
C
C        H -5,30
      V(4) = F(1,2,15)
C
C        ^P 30,-15
      V(5) = F(3,9,6) - F(4,9,6)
C
C        ^P 5,15
      V(6) = F(3,4,12) - F(4,4,12)
C
C        ^P -10,10
      V(7) = F(3,1,11) - F(4,1,11)
C
C        ^P 5,-5
      V(8) = F(3,4,8) - F(4,4,8)
C
C        P 15,0
      V(9) = F(3,6,9)
C
C        ^P 20,40
      V(10) = F(3,7,17) - F(4,7,17)
C
C        P 25,-10
      V(11) = F(3,8,7)
C
C        ^P 0,-40
      V(12) = F(3,3,1) - F(4,3,1)
C
C        ^P 0,-25
      V(13) = F(3,3,4) - F(4,3,4)
C
C        H 0,-5
      V(14) = F(1,3,8)
C
C        H -10,10
      V(15) = F(1,1,11)
C
C        H 15,-35
      V(16) = F(1,6,2)
C
C        P 15,-25
      V(17) = F(3,6,4)
C
C        P 0,5
      V(18) = F(3,3,10)
C
C        P 25,-40
      V(19) = F(3,8,1)
C
C        ^H 20,-40
      V(20) = F(1,7,1) - F(2,7,1)
C
C---------------------------------------------------------------------
C
      CU0 = 12.750
C
C        U -12
      U(1) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(2))/12
C
C        H 15,-5
      U(2) = F(1,6,8)
C
C        ^H 10,5
      U(3) = F(1,5,10) - F(2,5,10)
C
C        P 15,-40
      U(4) = F(3,6,1)
C
C        ^P 25,30
      U(5) = F(3,8,15) - F(4,8,15)
C
C        P 35,30
      U(6) = F(3,10,15)
C
C        H 25,-20
      U(7) = F(1,8,5)
C
C        H 10,-35
      U(8) = F(1,5,2)
C
C        H 5,20
      U(9) = F(1,4,13)
C
C        ^H -5,10
      U(10) = F(1,2,11) - F(2,2,11)
C
C        P 35,-30
      U(11) = F(3,10,3)
C
C        P 15,20
      U(12) = F(3,6,13)
C
C        H 10,5
      U(13) = F(1,5,10)
C
C        ^P 5,10
      U(14) = F(3,4,11) - F(4,4,11)
C
C        ^P 35,40
      U(15) = F(3,10,17) - F(4,10,17)
C
      U(16) = 0.0
      U(17) = 0.0
      U(18) = 0.0
      U(19) = 0.0
      U(20) = 0.0
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT=0.5*(FLAT + TLAT(1))*3.1415926535898/180.0
      FLON=TLON(1) + (UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE NIONOTR
C
C ********* CHANGE RECORD *********************************************
C
C     NIONOTR01 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR CYCLONES IN THE NORTH INDIAN OCEAN WHICH
C     ARE NORTH OF THE RIDGE, 500 MB STEERING IS USED.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .3653, 1.3532, -16.2332, 28.7486, -23.9050,
     1        1.4433, 7.2717, -.7670, -.8584, -.8325,
     1       15.1203, .2050, -4.5111, 0.0, 0.0, 0.0, 0.0,
     1       0.0, 0.0, 0.0/
C
      DATA CU/ .3538, .2334, -.2209, 3.3336, -22.4239,
     1         -.4186, 10.1656, 7.9597, -7.9171, -6.1242,
     1         .5001, -.6807, 1.9375, 11.8670, -.2813,
     1        0.0, 0.0, 0.0, 0.0, 0.0/
C
C*********************************************************************
C
      CV0 = -5654.0409
C
C        V -24
      V(1) = 1111.949 * (TLAT(1)-TLAT(3))/24
C
C        H 5,20
      V(2) = F(1,4,13)
C
C        ^P 0,25
      V(3) = F(3,3,14) - F(4,3,14)
C
C        ^P 5,10
      V(4) = F(3,4,11) - F(4,4,11)
C
C        ^P -5,0
      V(5) = F(3,2,9) - F(4,2,9)
C
C        P 35,-20
      V(6) = F(3,10,5)
C
C        ^P 15,-25
      V(7) = F(3,6,4) - F(4,6,4)
C
C        ^H 20,30
      V(8) = F(1,7,15) - F(2,7,15)
C
C        ^H 5,35
      V(9) = F(1,4,16) - F(2,4,16)
C
C        H 5,0
      V(10) = F(1,4,9)
C
C        ^P -5,35
      V(11) = F(3,2,16) - F(4,2,16)
C
C        H 25,-20
      V(12) = F(1,8,5)
C
C        ^P 15,20
      V(13) = F(3,6,13) - F(4,6,13)
C
      DO 100 I=14,20
         V(I) = 0.0
  100 CONTINUE
C
C-----------------------------------------------------------------------
C
      CU0 = -624.6672
      PIE = 3.1415926535898
C
C        U -12
      U(1) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(2))/12
C
C        V -24
      U(2) = 1111.949 * (TLAT(1)-TLAT(3))/24
C
C        ^@ 500 NW10 V
      U(3) = ((F(1,5,8) - F(1,5,6)) /
     1       (SIN((TLAT(1)+10.)*PIE/180.)*COS((TLAT(1)+10.)*PIE/180.)))
     1       -  ((F(2,5,8) - F(2,5,6)) /
     1       (SIN((TLAT(1)+10.)*PIE/180.)*COS((TLAT(1)+10.)*PIE/180.)))
C
C        P 10,40
      U(4) = F(3,5,17)
C
C        ^P -10,30
      U(5) = F(3,1,15) - F(4,1,15)
C
C        ^H 20,35
      U(6) = F(1,7,16) - F(2,7,16)
C
C        ^P 0,-20
      U(7) = F(3,3,5) - F(4,3,5)
C
C        ^P 10,40
      U(8) = F(3,5,17) - F(4,5,17)
C
C        ^P -5,20
      U(9) = F(3,2,13) - F(4,2,13)
C
C        ^P 10,-5
      U(10) = F(3,5,8) - F(4,5,8)
C
C        H 5,-15
      U(11) = F(1,4,6)
C
C        H -10,40
      U(12) = F(1,1,17)
C
C        ^P 25,-5
      U(13) = F(3,8,8) - F(4,8,8)
C
C        ^P -10,0
      U(14) = F(3,1,9) - F(4,1,9)
C
C        H 10,25
      U(15) = F(1,5,14)
C
      DO 200 I=16,20
         U(I) = 0.0
  200 CONTINUE
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 300 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  300 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE NIOOTR
C
C ********* CHANGE RECORD *********************************************
C
C     NIOOTR*01 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR CYCLONES IN THE NORTH INDIAN OCEAN
C     WHICH ARE ON THE RIDGE, 500 MB STEERING IS USED.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .4757, 3.0908, -2.7541, .4747, .2503,
     1         7.3980, -7.0843, -.14414, .2748, -.2725,
     1         4.6092, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
     1         0.0, 0.0, 0.0/
C
      DATA CU/ .4841, 9.7347, -4.3658, 16.7942, -.2266,
     1         -.1340, -.2141, 3.2214, -4.7700, -12.3065,
     1         .1666, .3422, 2.8396, -6.2172, -1.3645,
     1         -.10431, 0.0, 0.0, 0.0, 0.0/
C
C***********************************************************************
      PIE = 3.1415926535898
      CV0 = 60.1728
C
C        V -12
      V(1) = 1111.949 * (TLAT(1) - TLAT(2))/12
C
C        ^P 30,40
      V(2) = F(3,9,17) - F(4,9,17)
C
C        ^P 25,25
      V(3) = F(3,8,14) - F(4,8,14)
C
C        ^H 0,15
      V(4) = F(1,3,12) - F(2,3,12)
C
C        ^@ 500 NW10-5 V
      V51 = ((F(1,5,8) - F(1,5,6)) /
     1       (SIN((TLAT(1)+10.)*PIE/180.)*COS((TLAT(1)+10.)*PIE/180.)))
     1      - ((F(1,4,9) - F(1,4,7)) /
     1       (SIN((TLAT(1)+5.)*PIE/180.)*COS((TLAT(1)+5.)*PIE/180.)))
      V52 = ((F(2,5,8) - F(2,5,6)) /
     1       (SIN((TLAT(1)+10.)*PIE/180.)*COS((TLAT(1)+10.)*PIE/180.)))
     1       - ((F(2,4,9) - F(2,4,7)) /
     1       (SIN((TLAT(1)+5.)*PIE/180.)*COS((TLAT(1)+5.)*PIE/180.)))
      V(5) = V51 - V52
C
C        ^P -5,30
      V(6) = F(3,2,15) - F(4,2,15)
C
C        ^P 10,0
      V(7) = F(3,5,9) - F(4,5,9)
C
C        @ 500 NW10-5 V
      V(8) = V51
C
C        ^H 25,-15
      V(9) = F(1,8,6) - F(2,8,6)
C
C        ^H 15,30
      V(10) = F(1,6,15) - F(2,6,15)
C
C        ^P 5,5
      V(11) = F(3,4,10) - F(4,4,10)
C
      DO 100 I=12,20
         V(I) = 0.0
  100 CONTINUE
C
C----------------------------------------------------------------------
C
      CU0 = -12198.8993
C
C        U -12
      U(1) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(2))/12
C
C        P -10,-35
      U(2) = F(3,1,2)
C
C        ^P 15,-25
      U(3) = F(3,6,4) - F(4,6,4)
C
C        ^P -5,-35
      U(4) = F(3,2,2) - F(4,2,2)
C
C        ^H 10,5
      U(5) = F(1,5,10) - F(2,5,10)
C
C        @ 500 N15 U
      U(6) = (F(1,5,9) - F(1,7,9)) /
     1       SIN((TLAT(1)+15.)*3.1415926535898/180)
C
C        ^H 35,-30
      U(7) = F(1,10,3) - F(2,10,3)
C
C        ^P 10,40
      U(8) = F(3,5,17) - F(4,5,17)
C
C        ^P 15,5
      U(9) = F(3,6,10) - F(4,6,10)
C
C        ^P -10,20
      U(10) = F(3,1,13) - F(4,1,13)
C
C        H 25,-30
      U(11) = F(1,8,3)
C
C        ^H 5,20
      U(12) = F(1,4,13) - F(2,4,13)
C
C        P 15,-15
      U(13) = F(3,6,6)
C
C        ^P 10,-15
      U(14) = F(3,5,6) - F(4,5,6)
C
C        P 30,-5
      U(15) = F(3,9,8)
C
C        ^@ 500 N5 V
      U16SC = SIN((TLAT(1)+5.)*PIE/180.)*COS((TLAT(1)+5.)*PIE/180.)
      U(16) = ((F(1,4,10) - F(1,4,8)) / U16SC) -
     1        ((F(2,4,10) - F(2,4,8)) / U16SC)
C
      DO 150 I=17,20
         U(I) = 0.0
  150 CONTINUE
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
      SUBROUTINE NIOSOTR
C
C ********* CHANGE RECORD *********************************************
C
C     NIOSOTR01 ( 7 JUL 89) CORRECT CODE ERROR
C
C *********************************************************************
C
C     THIS SUBROUTINE IS FOR CYCLONES IN THE NORTH INDIAN OCEAN, SOUTH
C     OF THE RIDGE, 500 MB STEERING IS USED.
C
C     TLAT(1), TLON(1) = LAT, LONG AT THE WARNING TIME
C     TLAT(2), TLON(2) = LAT, LONG 12 HOURS PREVIOUS TO THE WARNING TIME
C     TLAT(3), TLON(3) = LAT, LONG 24 HOURS PREVIOUS TO THE WARNING TIME
C
C     F(1,J,I) = 500 MB HEIGHTS AT THE WARNING TIME
C     F(2,J,I) = 500 MB HEIGHTS 24 HOURS PREVIOUS
C     F(3,J,I) = SURFACE PRESSURE AT THE WARNING TIME
C     F(4,J,I) = SURFACE PRESSURE 24 HOURS PREVIOUS
C     F(5,J,I) = 200 MB HEIGHTS AT THE WARNING TIME
C     F(6,J,I) = 200 MB HEIGHTS 24 HOURS PREVIOUS
C
cx    COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON
      character*8 ldate
      COMMON /USER/ TLAT(3), TLON(3), FLAT, FLON,
     1     IWIND, IDOM, LDATE, IA, KK
      COMMON /FLDDAT/ F(6,10,17)
C
      DIMENSION V(20), CV(20), U(20), CU(20)
C
      DATA CV/ .4760, .1193, 5.3690, .0677, -1.0161,
     1         .1604, -3.8486, 1.2326, -.1779, 4.9715,
     1         .0720, -.1533, -.1174, -.0525, .0430,
     1         0.0, 0.0, 0.0, 0.0, 0.0/
C
      DATA CU/ .4558, -.1678, -2.3967, .2793, -1.7260,
     1         -.1471, -2.5425, .1774, 7.8780, -.1105,
     1         -.1317, -1.8571, -.0426, .2052, -2.4812,
     1         2.8158, .0634, -.3391, 0.0, 0.0/
C
C***********************************************************************
C
      CV0 = -5666.9895
      PIE = 3.1415926535898
C
C        V -12
      V(1) = 1111.949 * (TLAT(1)-TLAT(2))/12
C
C        H 15,-35
      V(2) = F(1,6,2)
C
C        P -10,15
      V(3) = F(3,1,12)
C
C        @ 500 V
      V(4) = ((F(1,1,11)+F(1,2,11)+F(1,3,11)+F(1,4,11)+F(1,5,11))
     1      - (F(1,1,7)+F(1,2,7)+F(1,3,7)+F(1,4,7)+F(1,5,7)))
     1      / (5*SIN(TLAT(1)*PIE/180.)*COS(TLAT(1)*PIE/180.))
C
C        ^P 25,-25
      V(5) = F(3,8,4) - F(4,8,4)
C
C        H 15,40
      V(6) = F(1,6,17)
C
C        ^P 5,-5
      V(7) = F(3,4,8) - F(4,4,8)
C
C        ^P 15,20
      V(8) = F(3,6,13) - F(4,6,13)
C
C        ^H 5,-30
      V(9) = F(1,4,3) - F(2,4,3)
C
C        ^P -10,10
      V(10) = F(3,1,11) - F(4,1,11)
C
C        ^H 25,-5
      V(11) = F(1,8,8) - F(2,8,8)
C
C        H 10,30
      V(12) = F(1,5,15)
C
C        H 5,0
      V(13) = F(1,4,9)
C
C        ^H 30,40
      V(14) = F(1,9,17) - F(2,9,17)
C
C        H 30,25
      V(15) = F(1,9,14)
C
      DO 100 I=16,20
         V(I) = 0.0
  100 CONTINUE
C
C-----------------------------------------------------------------------
C
      CU0 = 3964.4589
C
C        U -12
      U(1) = 1111.949 * COS((TLAT(1)+TLAT(2))/2*3.1415926535898/180.)
     1       * (TLON(1) - TLON(2))/12
C
C        H 15,-5
      U(2) = F(1,6,8)
C
C        ^P 15,-10
      U(3) = F(3,6,7) - F(4,6,7)
C
C        H 0,-30
      U(4) = F(1,3,3)
C
C        ^P 35,-40
      U(5) = F(3,10,1) - F(4,10,1)
C
C        H 10,15
      U(6) = F(1,5,12)
C
C        ^P 10,10
      U(7) = F(3,5,11) - F(4,5,11)
C
C        H 15,-35
      U(8) = F(1,6,2)
C
C        ^P -10,0
      U(9) = F(3,1,9) - F(4,1,9)
C
C        ^H 25,-30
      U(10) = F(1,8,3) - F(2,8,3)
C
C        H 20,40
      U(11) = F(1,7,17)
C
C        P 5,20
      U(12) = F(3,4,13)
C
C        ^H 35,35
      U(13) = F(1,10,16) - F(2,10,16)
C
C        ^H 0,-5
      U(14) = F(1,3,8) - F(2,3,8)
C
C        ^P 10,40
      U(15) = F(3,5,17) - F(4,5,17)
C
C        ^P 0,40
      U(16) = F(3,3,17) - F(4,3,17)
C
C        @ 500 U
      U(17) = ((F(1,1,7)+F(1,1,8)+F(1,1,9)+F(1,1,10)+F(1,1,11))
     1       - (F(1,5,7)+F(1,5,8)+F(1,5,9)+F(1,5,10)+F(1,5,11)))
     1       / (5 * SIN(TLAT(1)*3.1415926535898/180.))
C
C        H -10,40
      U(18) = F(1,1,17)
      U(19) = 0.0
      U(20) = 0.0
C
C--------------------------------------------------------------------
C
      VV = CV0
      UU = CU0
      DO 200 I=1,20
         VV = VV + (V(I) * CV(I))
         UU = UU + (U(I) * CU(I))
  200 CONTINUE
C
      FLAT = (VV * 24) / 1111.949 + TLAT(1)
      HLAT = 0.5*(FLAT +TLAT(1))*3.141592654/180.0
      FLON = TLON(1) +(UU*24.0)/(1111.949*COS(HLAT))
C
      RETURN
      END
