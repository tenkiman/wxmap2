      PROGRAM OTHMSG
C
C                   GENERATE OTH-T RAINFORM GOLD MESSAGE
C
C   INPUT FILES:  1) LOGICAL UNIT 10: FILENAME COMES FROM COMMAND LINE,
C                    SHOULD BE ALL SUMMARIES FOR GIVEN DTG; MUST BE ALL
C                    SUMMARIES FOR A GIVEN BASIN FOR A GIVEN DTG (SEE
C                    DEFINITION OF BASIN BELOW FOR SIX BASINS)
C
C                 2) LOGICAL UNIT 11: FILENAME ( USUALLY THE NAME IS
C                    X:\LOCALE\ATCFSITE.NAM, WHERE X: IS THE ATCF
C                    RUNTIME HOME DISK PARTITION ) COMES FROM THE
C                    COMMAND LINE, SHOULD HOLD THE FOUR CHARACTER
C                    FORECASTING SITE ID (JTWC, NWOC, NEOC, ETC.)
C
cx                3) logical unit 12: $ATCFINC/jotshead.dat
cx                   header for the jots message
C
cx                4) logical unit 13: $ATCFSTRMS/"stormid".dgr
cx                   danger area points computed by atcf routine danger.c
C
C
C   OUTPUT FILES:  BASIN // MM // DD // HH // . // H // BIN NUMBER
C                  WP062212.H21 <- EXAMPLE
C
C  PROGRAMMER:  HARRY D. HAMILTON  (GSA - CSC)  JUNE 1992
C
C  MAINTAINER:  Kent Paul Dolan (GSA - CSC) Until 1993
C
C  Changes:     1992.04.05: Added code to read site ID information from a
C                           file whose name is on the command line, to
C                           correct a hard wired site identifier in the
C                           output message.
C
C          HDH: 1993.05.21: Add variable NCHNAM to common /TRDATA/
C sampson, nrl: 1995.11.05: Convert to run under ATCF 3.0
C sampson, nrl: 1995.12.20: Change OTHT format as required by JTWC
C sampson, nrl: 1997.03.25: Change OTHT format as required by JTWC
C sampson, nrl: 1997.06.26: Change OTHT format as required by NLMOC (text size and storm name)
C sampson, nrl: 1999.06.14: Change OTHT format to include danger area                         
C
C  COMMON BLOCKS:
C    /TRDATC/ - CHARACTER VARIABLES FOR TROPICAL CYCLONE DATA
C               WDTG - WARNING DTG OF FORM YYMMDDHH (CHAR*8)
C              CYCID - CYCLONE ID OF FORM NNX (CHAR*3)
C                      NN = STORM NUMBER, X = AREA DESIGNATOR
C             STNAME - STORM NAME (CHAR*10)
C             MOVDIR - DIRECTION OF MOVEMENT IN DEG (CHAR*3)
C                      000 = STATIONARY
C             MOVSPD - SPEED OF MOVEMENT IN KT (CHAR*2)
C              NS(4) - NORTH/SOUTH ARRAY (CHAR*1)
C              EW(4) - EAST/WEST ARRAY (CHAR*1)
C             STG(4) - CYCLONE STAGE (CHAR*1)
C              BASIN - BASIN DESIGNATOR (CHAR*2) 
C                      WP, EP, NA, IO, SP, SI
C               COLC - COLOR CODE (CHAR*1)
C             PRODNM - PRODUCT NAME (CHAR*33)
C            COMMENT - AMPLIFICATION (CHAR*80)
C    /TRDATA/ - NUMERICAL VARIABLES FOR TROPICAL CYCLONE DATA
C             NOWARN - NO. OF WARNINGS IN A BASIN (INTEGER)
C               NPTS - NO. OF POSITIONS TO PLOT PER CYCLONE (INTEGER)
C             LAT(4) - LATITUDE IN TENTHS OF DEGREES (INTEGER)
C             LON(4) - LONGITUDE IN TENTHS OF DEGREES (INTEGER)
C          MAXWND(4) - MAX WIND SPEED IN KT (INTEGER)
C          IRAD35(4) - MAX RADIUS OF 35 KT WINDS (INTEGER) 
C            KTAU(4) - TAU IN HOURS (INTEGER)
C              NC(4) - NO. OF CHARACTERS (INTEGER) IN LAT/LON
C               ICOL - COLOR CODE (INTEGER) - 7
C             I35FLG - PLOT 35 KT RADIUS INFO FLAG, 0 - NO PLOT
C             IAMPHR - AMPLIFICATION FLAG, < 0 - NO COMMENT
C                      OTHERWISE TAU OF AMPLIFICATION
C             IAMPCC - CHARACTER COUNT IN AMPLIFICATION
C             NCHNAM - NUMBER OF CHARACTERS IN CYCLONE NAME
C    /USR/ - USER INPUT VARIABLES
C                MTF - MODE OF TRANSMISSION (INTEGER)
C                      1=NEDN, 2=AUTODIN, 3=NODDS
C              IFORM - FORMAT FLAG FOR LAT, LONG (INTEGER) 
C                      0=INCLUDE SECONDS, 1=DO NOT INCLUDE SECONDS
C               ICHK - CHECKSUM FLAG FOR LAT, LONG (INTEGER)
C                      0=INCLUDE CHECKSUMS, 1=NO CHECKSUMS 
C      ******   IMSG - MSG TYPE FLAG (INTEGER)
C                      0 = GENERATE MOD. RAINFORM GOLD MESSAGE
C                      1 = GENERATE OTH-T GOLD MESSAGE
C              NUNIT - UNIT NUMBER FOR WRITING
C    /ERRS/ - ERROR FLAGS
C               IERR - ERROR CONDITION FLAG (INTEGER)
C                      0=NO ERROR, 1=ERROR ENCOUNTERED
C               IEOF - END OF FILE FLAG (INTEGER)
C                      0=NO EOF, 1=EOF ENCOUNTERED
C    /LOCALE/ SITEID - FOUR CHARACTER FORECASTING SITE NAME, LIKE 'JTWC',
C                      'NWOC', 'NEOC', ETC.
cx   /DANGER/   DDTG - 8 CHAR DTG (YYMMDDHH) OF DANGER AREA DATA
cx             NDANG - NUMBER OF POINTS IN DANGER AREA
cx             DAREA - CHAR STRING OF OTH-T FORMAT DANGER AREA POSITS
cx              INUM - NUMBER OF CHARS IN EACH DAREA ELEMENT
C***********************************************************************
C
cx    CHARACTER CARDS(20)*80
      character cards(20)*100
C
      CHARACTER WDTG*8,CYCID*3,STNAME*10,MOVDIR*3,MOVSPD*2,
     *          NS*1,EW*1,STG*1,BASIN*2,COLC*1,PRODNM*33,COMMENT*80
      CHARACTER*4 SITEID
C
      DIMENSION NBINS(20)
cx
      character*200 filename
      character*100 storms,includes
      character*80  line
      character*8   cdtg
      character*8   ddtg
      character*6   strmid
      character*2   century
      integer       ndang, inum(500)
      character*18  darea(500)
      integer       ind, iarg
cx

C
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
      COMMON /MSGS/ MWP21,MWP22,MWP23,MWP24, MEP25,MEP26,MEP27,MEP28,
     .              MNA29,MNA30,MNA31,MNA32, MIO33,MIO34,MIO35,MIO36,
     .              MSP37,MSP38, MSI39,MSI40
      COMMON /USR/ MTF,IFORM,ICHK,IMSG,NUNIT
      COMMON /ERRS/ IERR, IEOF
      COMMON /LOCALE/ SITEID
      COMMON /DANGER/ DDTG, NDANG, DAREA, INUM
C
      EQUIVALENCE (MWP21,NBINS(1))
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  .

c     Initialize local variables.  ajs
      ind = 0
      K = 0
      KNT = 0
      L = 0
      LC = 0
      LS = 0
      LT = 0
      MSG = 0
      N = 0

c     KPD  Print the copyright notice and delay a short time for the
c          user to notice that it exists, and to hit pause to read it if
c     desired.

cx    call copyrite

C
      DO 100 N=1, 20
        NBINS(N) = 0
  100 CONTINUE
      MSG = 0
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
cx
cx  get the date-time-group off the command line
cx
      call getarg (iarg,cdtg)
      iarg = iarg + 1
cx
cx  get the storms directory name
cx
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cx
cx    get the storm id
cx
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c     get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
cajs  write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".sum"
      write(filename,'(6a)') storms(1:ind), "/", 
     1     strmid(1:4), century, strmid(5:6), ".sum"
C
C                   OPEN INPUT FILES, FILENAMES COME FROM COMMAND LINE
C
cx    OPEN (10,FILE=' ',ERR=710,STATUS='OLD')
      open (10,file=filename,err=710,status='old')
      REWIND (10)

cx    OPEN (11,FILE=' ',ERR=720,STATUS='OLD')
      call getenv("ATCFINC",includes)
      ind=index(includes," ")-1
      write(filename,'(a,a)')includes(1:ind),"/atcfsite.nam"
      open (11,file=filename,err=720,status='old')
      REWIND 11
cx    READ (11,'(A4)') SITEID

  103 continue
      read (11,'(a80)',end=720) line
      if(line(1:13).ne.'START_OF_DATA')go to 103 
      read (11,*)
      read (11,'(a4)')  siteid
      CLOSE(11)

cx  Danger area file (if available)
cx
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
      write(filename,'(6a)') storms(1:ind), "/", 
     1     strmid(1:4), century, strmid(5:6), ".dgr"
      print *, "filename=", filename
      open (13,file=filename,err=104,status='old')
      REWIND (13)
cx  read in the danger area (if available)
      call readdgr
      close(13)
      go to 105
  104 continue
      print *, 'Open danger file unsuccessful'
C
  105 CONTINUE
C
C                   READ A WARNING SUMMARY FROM GENSUM/DSPLSUM
C
      DO 110 L=1, 20
        READ (10,'(A80)',END=120) CARDS(L)
        IF (CARDS(L)(1:4) .EQ. 'NNNN') GOTO 115
C
  110 CONTINUE
      L = 20
  115 CONTINUE
      L = L +1
  120 CONTINUE
      KNT = L -1
      IF (KNT .EQ. 0) GOTO 300
C
      MSG = MSG +1
      WRITE (*,*) 'READ ',KNT,' LINES OF WARNING SUMMARY ',MSG
cx  possible that this check doesn't work on Maxion ... bs 12/06/95
      DO 130 LS=1, KNT
cx  possible that this check doesn't work on Maxion ... bs 12/06/95
cx      IF (CARDS(LS)(1:1).GE.'0' .AND. CARDS(LS)(1:1).LE.'9') GOTO 140
       if   (cards(ls)(1:1).eq.'0' .or. cards(ls)(1:1).eq.'1') go to 140
       if   (cards(ls)(1:1).eq.'2' .or. cards(ls)(1:1).eq.'3') go to 140
       if   (cards(ls)(1:1).eq.'4' .or. cards(ls)(1:1).eq.'5') go to 140
       if   (cards(ls)(1:1).eq.'6' .or. cards(ls)(1:1).eq.'7') go to 140
       if   (cards(ls)(1:1).eq.'8' .or. cards(ls)(1:1).eq.'9') go to 140
C
  130 CONTINUE
      WRITE (*,*) 'INPUT FILE NOT WARNING SUMMARY FILE'
      STOP 1
C
  140 CONTINUE
C
C                   START LOADING COMMON VALUES
C
cx    WDTG   = CARDS(LS)(1:8)
      WDTG   = CARDS(LS)(3:10)
      print *, 'wdtg=',wdtg
cx    CYCID  = CARDS(LS)(10:12)
      CYCID  = CARDS(LS)(12:14)
cx    STNAME = CARDS(LS)(14:23)
      STNAME = CARDS(LS)(16:25)
      NCHNAM = 0
      DO 145 N=1, 10
        IF (STNAME(N:N) .NE. ' ') NCHNAM = NCHNAM +1
  145 CONTINUE
cx    READ (CARDS(LS)(29:30),'(I2)') NOWARN
      READ (CARDS(LS)(31:33),'(I3)') NOWARN
cx    MOVDIR = CARDS(LS)(32:34)
      MOVDIR = CARDS(LS)(35:37)
cx    MOVSPD = CARDS(LS)(36:37)
      MOVSPD = CARDS(LS)(39:40)
C
C                   FIND LINE NUMBER FOR LAST TAU POSITION
C
      DO 150 L=LS+1, KNT
cx      IF (CARDS(L)(1:3) .EQ. 'AMP') LT = L -1
cx      IF (CARDS(L)(1:3) .EQ. 'GLD') GOTO 160
        if (cards(l)(1:3) .eq. 'AMP') then
	    lt = l -1
	    go to 160
        endif
C
  150 CONTINUE
      WRITE (*,*) 'INPUT WARNING SUMMARY FILE NOT ALL THERE'
      STOP 1
C
  160 CONTINUE
cx  Im not sure about this line, but it works?  sampson 6/14/96
cx  Looks like we are determining whether or not comments are 
cx  are in the warning summary.
      l=l+1
cx ************************************
      IF (CARDS(L)(5:5) .NE. ' ') THEN
        DO 170 K=80, 1, -1
          IF (CARDS(L)(K:K) .NE. ' ') GOTO 180
C
  170   CONTINUE
        K = 80
  180   CONTINUE
        COMMENT = ' '
cx      COMMENT(1:K-3) = CARDS(L)(10:K)
        COMMENT(1:K-3) = CARDS(L)(10:K)
cx      READ (CARDS(L)(5:6),'(I2.2)') IAMPHR
        READ (CARDS(L)(5:7),'(I3.3)') IAMPHR
        IAMPCC = K -3
      ELSE
        IAMPHR = -1
        IAMPCC =  0
      ENDIF
      IF (CARDS(LT)(1:1) .NE. 'T') LT = LT -1
C
C                   LOAD LAT/LON AND RADIUS INFO
C
      LS   = LS +1
      NPTS = 0
  200 CONTINUE
      DO 210 L=LS, LT
        IF (CARDS(L)(1:1) .EQ. 'A') GOTO 220
C
        IF (CARDS(L)(1:1) .EQ. 'T') THEN
cx        READ (CARDS(L)(2:3),'(I2)') IHR
          READ (CARDS(L)(2:4),'(I3)') IHR
C
C                   PROCESS INITIAL AND EVERY 24 HOURS, BUT ALWAYS
C                   PROCESS LAST POSITION
C
          IF (MOD (IHR,24).EQ.0 .OR. L.EQ.LT) THEN
            NPTS = NPTS +1
cx          READ (CARDS(L)(5:7),'(I3)') LAT(NPTS)
            READ (CARDS(L)(6:8),'(I3)') LAT(NPTS)
cx          NS(NPTS) = CARDS(L)(8:8)
            NS(NPTS) = CARDS(L)(9:9)
cx          READ (CARDS(L)(10:13),'(I4)') LON(NPTS)
            READ (CARDS(L)(11:14),'(I4)') LON(NPTS)
cx          EW(NPTS) = CARDS(L)(14:14)
            EW(NPTS) = CARDS(L)(15:15)
            IF (NPTS .EQ. 1) CALL BASEM
cx          READ (CARDS(L)(16:18),'(I3)') MAXWND(NPTS)
            READ (CARDS(L)(17:19),'(I3)') MAXWND(NPTS)
            CALL STAGE
            KTAU(NPTS) = IHR
            LC = L
            PRINT*,'R35MX : ',CARDS(LC)(1:40)
            CALL R35MX (CARDS,KNT,LC,IRAD35(NPTS))
            PRINT*,'IRAD35 ',IRAD35(NPTS)
            IF (IRAD35(NPTS) .GT. 0) I35FLG = 35
            IF (L .NE. LC) THEN
              LS = LC +1
              GOTO 200
C
            ENDIF
          ENDIF
        ENDIF
  210 CONTINUE
  220 CONTINUE
      IF (STNAME.EQ.'NONAME' .OR. STNAME.EQ.' ') THEN
        STNAME = ' '
        STNAME(1:3) = CYCID
      ENDIF
      COLC   = 'G'
      PRODNM = ' '
      ICOL   = 7
      MTF    = 2
      IFORM  = 0
      ICHK   = 0
C
C                   SET FLAG TO GENERATE OTH-T GOLD FORMAT
C
      IMSG   = 1
      CALL TRWHDR
      IF (IERR .EQ. 0) THEN
        CALL TRWWRN
cx  added danger area to oth-t message  ... sampson nrl Jun 99
	CALL TRWDGR
      ELSE
        WRITE (*,*) 'OTHMSG, CANT WRITE GOLD MESSAGE, FATAL ERROR'
        STOP 3
C
      ENDIF
      WRITE (*,*) 'FINISHED PROCESSING SUMMARY ',MSG
      GOTO 105
C
  300 CONTINUE
      CLOSE (10)
      WRITE (*,*) 'FINISHED PROCESSING ',MSG,' SUMMARIES'
      DO 310 N=1, 20
        IF (NBINS(N).GT.0 .AND. NBINS(N).LT.4) THEN
C                   WRITE ENDAT AND CLOSE FILE
          NUNIT = N +20
          WRITE (NUNIT,'(A5)') 'ENDAT'
cx
cx  also need a BT and NNNN after ENDAT line ... bs 12/20/95
cx
	  write (nunit,'(a2)') 'BT'
	  write (nunit,'(a4)') 'NNNN'
          CLOSE (NUNIT)
        ENDIF
  310 CONTINUE
      STOP
C
  710 CONTINUE
      WRITE (*,*) 'Input message data file not available.'
      STOP 2

  720 CONTINUE
      WRITE (*,*) 'Input site ID information file not available.'
      STOP 2

C
      END

      SUBROUTINE BASEM
C
      CHARACTER WDTG*8,CYCID*3,STNAME*10,MOVDIR*3,MOVSPD*2,
     *          NS*1,EW*1,STG*1,BASIN*2,COLC*1,PRODNM*33,COMMENT*80
C
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NS(1) .EQ. 'N') THEN
        IF (EW(1) .EQ. 'W') THEN
          IF (CYCID(3:3) .EQ. 'L') THEN
            BASIN = 'NA'
          ELSE
            BASIN = 'EP'
          ENDIF
        ELSE
          IF (LON(1) .LT. 1000) THEN
            BASIN = 'NI'
          ELSE
            BASIN = 'WP'
          ENDIF
        ENDIF
      ELSE
        IF (EW(1) .EQ. 'W') THEN
          IF (LON(1) .GT. 600) THEN
            BASIN = 'SP'
          ELSE
            BASIN = 'SA'
          ENDIF
        ELSE
          IF (LON(1) .GT. 1350) THEN
            BASIN = 'SP'
          ELSE
            BASIN = 'SI'
          ENDIF
        ENDIF
      ENDIF
      RETURN
C
      END

      FUNCTION INCRD5 (DTG,ITDIF)
C
C                   INCRD5 = DTG +ITDIF
C
      CHARACTER*8 INCRD5, DTG
C
      DIMENSION MON(12)
C
      DATA MON/31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
c     Initialize local variables, ajs
      IYR = 0
      IMO = 0
      IDD = 0
      IHH = 0
      NYR = 0
      NMO = 0
      NDD = 0
      NHH = 0

      READ (DTG,'(4I2)') IYR,IMO,IDD,IHH
      NYR = IYR
      NMO = IMO
      NDD = IDD
      NHH = IHH
      IF (ITDIF .EQ. 0) THEN
        INCRD5 = DTG
      ELSE
        NHH = IHH +ITDIF
        IF (NHH .GT. 0) THEN
  110     CONTINUE
          IF (NHH .GE. 24) THEN
            NHH = NHH -24
            NDD = NDD +1
            IF (NDD .GT. MON(NMO)) THEN
              IF (NMO .EQ. 2) THEN
                IF (MOD (NYR,4) .EQ. 0) THEN
                  IF (NDD .EQ. 29) GOTO 110
C
                ENDIF
              ENDIF
              NDD = 1
              NMO = NMO +1
              IF (NMO .GT. 12) THEN
                NMO = 1
                NYR = NYR +1
                IF (NYR .GT. 99) NYR = 0
              ENDIF
            ENDIF
            GOTO 110
C
          ENDIF
        ELSE
  120     CONTINUE
          IF (IABS (NHH) .GE. 24) THEN
            NHH = NHH +24
            NDD = NDD -1
            IF (NDD .LT. 1) THEN
              NMO = NMO -1
              IF (NMO .LT. 1) THEN
                NYR = NYR -1
                IF (NYR .LT. 0) NYR = 99
              ENDIF
              NDD = MON(NMO)
              IF (NMO .EQ. 2) THEN
                IF (MOD (NYR,4) .EQ. 0) NDD = 29
              ENDIF
            ENDIF
            GOTO 120
C
          ENDIF
        ENDIF
        WRITE (INCRD5,'(4I2.2)') NYR,NMO,NDD,NHH
      ENDIF
      RETURN
C
      END

      FUNCTION NR2MTH (IMO)
C
C  FUNCTION TO RETURN 3 CHAR MONTH, GIVEN INTEGER 1 THRU 12
C  ANY OTHER VALUE RETURNS ASTERISKS.
C
C * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
C
      CHARACTER NR2MTH*3, MTH(12)*3
C
      DATA MTH /'JAN','FEB','MAR','APR','MAY','JUN',
     *          'JUL','AUG','SEP','OCT','NOV','DEC'/
C
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      IF (IMO .GE. 1 .AND. IMO .LE. 12) THEN
        NR2MTH = MTH(IMO)
      ELSE
        NR2MTH = '***'
      ENDIF
      RETURN
C
      END

      SUBROUTINE R35MX (CARDS,KNT,LC,IR35MX)
C
cx    CHARACTER CARDS(KNT)*80
      character cards(KNT)*100
C
      DIMENSION IR(4)
C
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
c     Initialize local variables, ajs
      N = 0
      K = 0
      JS = 0

      DO 110 N=1, 4
        IR(N) = 0
  110 CONTINUE
      NR =  0
      NT =  0
      NF =  0
      KS = 20
  120 CONTINUE
      DO 140 K=KS, 80
        IF (CARDS(LC)(K:K) .EQ. 'R') THEN
          IF (CARDS(LC)(K:K+3) .EQ. 'R035') THEN
            NF = -1
            JS = K +5
  125       CONTINUE
            DO 130 J=JS, 80
              IF (CARDS(LC)(J:J).GE.'0' .AND. CARDS(LC)(J:J).LE.'9')
     .          THEN
                NR = NR +1
                READ (CARDS(LC)(J:J+2),'(I3)') IR(NR)
                JS = J +4
                GOTO 125
C
              ENDIF
  130       CONTINUE
            NT = 1
            IF (CARDS(LC+1)(1:4) .EQ. '    ') THEN
C
C                   PROCESS CONTINUATION LINE
C
              LC = LC +1
              IF (NF .EQ. 0) THEN
                KS = 5
                GOTO 120
C
              ELSE
                JS = 5
                GOTO 125
C
              ENDIF
            ENDIF
          ENDIF
        ENDIF
  140 CONTINUE
      IF (NT .EQ. 0) THEN
C
C                   THERE CAN BE ONLY ONE CONTINUATION LINE
C
        NT = 1
        IF (CARDS(LC+1)(1:4) .EQ. '    ') THEN
C
C                   PROCESS CONTINUATION LINE
C
          LC = LC +1
          KS = 5
          GOTO 120
C
        ENDIF
      ENDIF
      IF (NR .GT. 1) THEN
        IR35MX = 0
        DO 210 N=1, NR
          IR35MX = MAX0 (IR35MX,IR(N))
  210   CONTINUE
      ELSE
        IR35MX = IR(1)
      ENDIF
      RETURN
C
      END

      SUBROUTINE STAGE
C
      CHARACTER WDTG*8,CYCID*3,STNAME*10,MOVDIR*3,MOVSPD*2,
     *          NS*1,EW*1,STG*1,BASIN*2,COLC*1,PRODNM*33,COMMENT*80
C
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IF (NS(1).EQ.'S' .OR. BASIN.EQ.'NI') THEN
        STG(NPTS) = 'C'
      ELSEIF (MAXWND(NPTS) .LT. 34) THEN
        STG(NPTS) = 'D'
      ELSEIF (MAXWND(NPTS) .LT. 64) THEN
        STG(NPTS) = 'S'
      ELSE
        IF (EW(1) .EQ. 'E') THEN
          STG(NPTS) = 'T'
        ELSE
          STG(NPTS) = 'H'
        ENDIF
      ENDIF
      RETURN
C
      END

      SUBROUTINE TRLABL
C
C..............START PROLOGUE....................................
C
C  MODULE NAME:                   TRLABL
C
C  DESCRIPTION:  SUBR TO WRITE LABELS IN THE WARNING MSG TEXT
C                USING THE GOLD FORMAT 
C
C  COPYRIGHT:                     (C) 1992 FLENUMOCEANCEN
C                                 U.S. GOVERNMENT DOMAIN
C                                 ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:     GS-09K-90BHD0001
C                                 ADP SUPPORT FOR HIGHLY TECHNICAL
C                                 SOFTWARE DEVELOPEMNT FOR SCIENTIFIC
C                                 APPLICATIONS
C
C  REFERENCES:                    TASK ORDER PFC172730, EPF026-P
C
C  CLASSIFICATION:                UNCLASSIFIED
C
C  RESTRICTIONS:                  NONE 
C
C  ORIGINAL PROGRAMMER, DATE:     DON CHIN, CSC-GSA (MAY 1992)
C
C  CURRENT PROGRAMMER:   HARRY D. HAMILTON  (GSA -CSC)  JUNE 1992
C
C  LIBRARIES OF RESIDENCE:        MT1731/OPSPL1
C
C  USAGE:  CALL TRLABL
C
C  PARAMETERS:  NONE
C
C  COMMON BLOCKS:  SEE MAIN PROGRAM
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C..............MAINTENANCE SECTION...............................
C
C  MODULES CALLED: 
C    INCRD5 - LIBRARY SUBR TO CALC NEW DTG GIVEN OLD DTG AND DIFF
C    NR2MTH - SUBR TO CONVERT MONTH (INTEGER) TO MONTH (CHAR*3)
C    TRLLCH - SUBR TO CONVERT LAT,LONG IN NUMERICAL FORMAT TO
C             CHARACTER FORMAT
C
C  LOCAL VARIABLES AND STRUCTURES:
C      CLL - TEMPORARY LAT/LONG (CHAR*18)
C     DTG1 - FIRST DATE-TIME (CHAR*8)
C     DTG2 - SECOND DATE-TIME (CHAR*8) 
C      IDA - DAY OF WEEK (INTEGER)
C      IHR - HOUR OF DAY (INTEGER)
C      IMO - MONTH OF YEAR (INTEGER)
C    ITDIF - TIME DIFFERENCE IN HRS (INTEGER)
C       IY - LAST 2 DIGITS OF YEAR (INTEGER)
C     LATT - TEMPORARY LAT VARIABLE (INTEGER)
C     LATX - TEMPORARY LAT VARIABLE (INTEGER)
C     LONG - TEMPORARY LONG VARIABLE (INTEGER)
C      MON - MONTH OF YEAR (CHAR*3)
C      NCC - NO. OF CHARACTERS COUNTER (INTEGER) 
C    RADII - RADII LABEL (CHAR*20)
C
C  METHOD:
C
C  COMPILER DEPENDENCES:  FORTRAN 77 (FTN5)
C
C  COMPILER OPTIONS:  NONE
C
C  RECORD OF CHANGES:
C
C..............END PROLOGUE......................................
C
      CHARACTER*15 CAMPZ
      CHARACTER CLL*18, MON*3, NR2MTH*3
      CHARACTER DTG1*8, DTG2*8, DTGA*8
      CHARACTER INCRD5*8, RADII*20
      CHARACTER WDTG*8,CYCID*3,STNAME*10,MOVDIR*3,MOVSPD*2,
     *          NS*1,EW*1,STG*1,BASIN*2,COLC*1,PRODNM*33,COMMENT*80
C
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
      COMMON /USR/ MTF,IFORM,ICHK,IMSG,NUNIT
      COMMON /ERRS/ IERR, IEOF
C
      DATA RADII /'35 KT RADII SHOWN'/ 
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
c     Initialize local variables, ajs
      LATT = 0
      LATX = 0
      LONG = 0
      IY = 0
      IMO = 0
      IDA = 0
      IHR = 0
      NCLNS = 0
      ITDIF = 0
      I = 0
      NCC = 0

C
C                   DISPLAY STORM NAME, DTG AND MOVEMENT
C
      LATT = LAT(1) - 20
      IF (EW(1) .EQ. 'W') THEN
        LONG = LON(1) - 25
      ELSE
        LONG = LON(1) + 25
      ENDIF
      CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
C
      IF (IMSG .NE. 1) THEN
C
        WRITE (NUNIT,600) CLL(1:NCC), CLL(1:NCC), ICOL
  600   FORMAT ('LINE/1/2/',A,'/',A,'/',I1)
C
      ENDIF
C
C                   BUILD PRODUCT NAME
C
      IF (STG(1) .EQ. 'T') THEN
        PRODNM = 'TYPHOON ' // STNAME
      ELSE IF (STG(1) .EQ. 'H') THEN
        PRODNM = 'HURRICANE ' // STNAME
      ELSE IF (STG(1) .EQ. 'C') THEN
        PRODNM = 'TROP CYCLONE ' // STNAME
      ELSE IF (STG(1) .EQ. 'S') THEN
        PRODNM = 'TROP STORM ' // STNAME
      ELSE
        PRODNM = 'TROP DEPRESSION ' // STNAME
      ENDIF
C
      IF (IMSG .NE. 1) THEN
        WRITE (NUNIT,610) PRODNM
  610   FORMAT ('LAMP/',A)
C
      ELSE
C
        WRITE (NUNIT,605) COLC,CLL(1:NCC),PRODNM
  605   FORMAT ('TEXT/20//',A1,'/',A,'/',A)
      ENDIF
C
      LATT = LATT - 10
      CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
C
C                   DECODE DTG
C
      READ (WDTG,700) IY, IMO, IDA, IHR
  700 FORMAT (4I2.2)
      MON = NR2MTH (IMO)
C
      IF (IMSG .NE. 1) THEN
C
        WRITE (NUNIT,600) CLL(1:NCC), CLL(1:NCC), ICOL
        WRITE (NUNIT,620) WDTG(5:6),MON,WDTG(7:8)
  620   FORMAT ('LAMP/',A2,1X,A3,1X,A2,'00Z')
C
      ELSE
        WRITE (NUNIT,625) COLC,CLL(1:NCC),WDTG(5:6),MON,WDTG(7:8)
  625   FORMAT ('TEXT/20//',A1,'/',A,'/',A2,1X,A3,1X,A2,'00Z')
      ENDIF
C
      LATT = LATT - 10
      CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
C
      IF (IMSG .NE. 1) THEN
C
        WRITE (NUNIT,600) CLL(1:NCC), CLL(1:NCC), ICOL
        IF (MAXWND(1) .GE. 100) THEN
          WRITE (NUNIT,630) MAXWND(1)
  630     FORMAT ('LAMP/MAX ',I3,' KT')
        ELSE
          WRITE (NUNIT,635) MAXWND(1)
  635     FORMAT ('LAMP/MAX ',I2,' KT')
        ENDIF
C
      ELSE
        IF (MAXWND(1) .GE. 100) THEN
          WRITE (NUNIT,632) COLC,CLL(1:NCC),MAXWND(1)
  632     FORMAT ('TEXT/20//',A1,'/',A,'/MAX ',I3,' KT')
        ELSE
          WRITE (NUNIT,633) COLC,CLL(1:NCC),MAXWND(1)
  633     FORMAT ('TEXT/20//',A1,'/',A,'/MAX ',I2,' KT')
        ENDIF
      ENDIF
      LATT = LATT - 10
      CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
C
      IF (MOVDIR .EQ. '000' .AND. MOVSPD .EQ. '00') MOVDIR = 'STA'
      IF (IMSG .NE. 1) THEN
C
        WRITE (NUNIT,600) CLL(1:NCC),CLL(1:NCC),ICOL
        IF (MOVDIR .EQ. 'STA') THEN
          WRITE (NUNIT,610) MOVDIR
        ELSE
          WRITE (NUNIT,610) MOVDIR // ' AT ' // MOVSPD // ' KT'
        ENDIF
C
      ELSE
        IF (MOVDIR .EQ. 'STA') THEN
          WRITE (NUNIT,641) COLC,CLL(1:NCC),MOVDIR
  641     FORMAT ('TEXT/20//',A1,'/',A,'/',A)
        ELSE
          WRITE (NUNIT,641) COLC,CLL(1:NCC),MOVDIR // ' AT ' //
     *                   MOVSPD // ' KT'
        ENDIF
      ENDIF
C
      IF (I35FLG .GT. 0) THEN
        LATT = LATT - 10
        CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
        IF (IMSG .NE. 1) THEN
          WRITE (NUNIT,600) CLL(1:NCC),CLL(1:NCC),ICOL
          WRITE (NUNIT,610) RADII
        ELSE
          WRITE (NUNIT,641) COLC, CLL(1:NCC), RADII
        ENDIF
      ENDIF
C
C                   CHANGE TC DTG TO SYNOPTIC DTG
C
      IHR = IHR/6 * 6
      WRITE (DTG1,700) IY, IMO, IDA, IHR
C
C                   CHECK ON WRITING AMPLIFICATION
C
      IF (IAMPHR .GE. 0) THEN
        DTGA = INCRD5 (DTG1,IAMPHR)
        CAMPZ = ' '
        CAMPZ = DTGA(5:8) // 'Z COMMENT:'
        IF (NS(1) .EQ. 'N') THEN
          LATT = LATT - 10
        ELSE
          IF (IAMPCC .GT. 30) THEN
            NCLNS = 3
          ELSE
            NCLNS = 2
          ENDIF
          LATT = LATT -10*NCLNS
        ENDIF
        IF (EW(1) .EQ. 'E') THEN
          LONG = LONG - 50
        ELSE
          LONG = LONG + 50
          IF (LONG .GT. 1800) LONG = 3600 -1800
        ENDIF
        CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
        IF (IMSG .NE. 1) THEN
          WRITE (NUNIT,600) CLL(1:NCC),CLL(1:NCC),ICOL
          WRITE (NUNIT,610) CAMPZ
        ELSE
          WRITE (NUNIT,641) COLC, CLL(1:NCC), CAMPZ
        ENDIF
        IF (NS(1) .EQ. 'N') THEN
          LATT = LATT - 10
        ELSE
          LATT = LATT + 10
        ENDIF
        CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
        IF (IMSG .NE. 1) THEN
          WRITE (NUNIT,600) CLL(1:NCC),CLL(1:NCC),ICOL
          WRITE (NUNIT,610) COMMENT(1:30)
        ELSE
          WRITE (NUNIT,641) COLC, CLL(1:NCC), COMMENT(1:30)
        ENDIF
        IF (IAMPCC .GT. 30) THEN
          IF (NS(1) .EQ. 'N') THEN
            LATT = LATT - 10
          ELSE
            LATT = LATT + 10
          ENDIF
          CALL TRLLCH (LATT,NS(1),LONG,EW(1),IFORM,ICHK,CLL,NCC)
          IF (IMSG .NE. 1) THEN
            WRITE (NUNIT,600) CLL(1:NCC),CLL(1:NCC),ICOL
            WRITE (NUNIT,610) COMMENT(31:60)
          ELSE
           WRITE (NUNIT,641) COLC, CLL(1:NCC), COMMENT(31:60)
          ENDIF
        ENDIF
      ENDIF
      ITDIF = 0
C
C                   CONVERT WARNING POSITIONS TO OFFSET LOCATION
C                   AND WRITE MAX WINDS (AT 24 HR INTERVALS)
C
      LATX = LAT(1)
      DO 200 I = 1, NPTS
C
C                   WRITE ALL EXCEPT TAU=12
C
        LATT = LAT(I)
        IF (LATT .LT. LATX) LATT = LATX
C
        IF (EW(I) .EQ. 'E') THEN
          LONG = LON(I) + 40 
        ELSE
          LONG = LON(I) - 40 
        ENDIF
C
C                   WRITE VERIFYING TIMES AND MAX WIND SPEEDS
C
      IF (I .GT. 1) THEN
        CALL TRLLCH (LATT,NS(I),LONG,EW(I),IFORM,ICHK,
     *             CLL,NCC)
C
        IF (IMSG .NE. 1) THEN
C
          WRITE (NUNIT,600) CLL(1:NCC),CLL(1:NCC),ICOL
        ENDIF
        ITDIF = KTAU(I)
        DTG2 = INCRD5 (DTG1,ITDIF)
C
        IF (IMSG .NE. 1) THEN
C
          IF (MAXWND(I) .GE. 100) THEN
            WRITE (NUNIT,640) DTG2(5:8), MAXWND(I)
  640       FORMAT ('LAMP/',A4,'Z MAX ',I3)
          ELSE
            WRITE (NUNIT,645) DTG2(5:8), MAXWND(I)
  645       FORMAT ('LAMP/',A4,'Z MAX ',I2)
          ENDIF
C
        ELSE
C
          IF (MAXWND(I) .GE. 100) THEN
            WRITE (NUNIT,647) COLC,CLL(1:NCC),DTG2(5:8), MAXWND(I)
  647       FORMAT ('TEXT/20//',A1,'/',A,'/',A4,'Z MAX ',I3)
          ELSE
            WRITE (NUNIT,648) COLC,CLL(1:NCC),DTG2(5:8), MAXWND(I)
  648       FORMAT ('TEXT/20//',A1,'/',A,'/',A4,'Z MAX ',I2)
          ENDIF
C
        ENDIF
C
      ENDIF
C
        LATX = LATT + 10
C
  200 CONTINUE
      RETURN
C
      END

      SUBROUTINE TRLLCH (LAT, NS, LON, EW, IFLG, ICHK, CLALO, NC)
C
C..............START PROLOGUE....................................
C
C  MODULE NAME:                   TRLLCH
C
C  DESCRIPTION:  SUBR TO CONVERT LATITUDE, LONGITUDE IN NUMERICAL
C                FORMAT WITH HEMISPHERE TO CHARACTER FORMAT,
C                WITH OR WITHOUT SECONDS, WITH OR WITHOUT CHECKSUMS
C
C  COPYRIGHT:                     (C) 1992 FLENUMOCEANCEN
C                                 U.S. GOVERNMENT DOMAIN
C                                 ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:     GS-09K-90BHD0001
C                                 ADP SUPPORT FOR HIGHLY TECHNICAL
C                                 SOFTWARE DEVELOPEMNT FOR SCIENTIFIC
C                                 APPLICATIONS
C
C  REFERENCES:                    TASK ORDER PFC172730, EPF026-P
C
C  CLASSIFICATION:                UNCLASSIFIED
C
C  RESTRICTIONS:                  NONE 
C
C  ORIGINAL PROGRAMMER, DATE:     DON CHIN, CSC-GSA (MAY 1992)
C
C  CURRENT PROGRAMMER:   HARRY D. HAMILTON  (GSA -CSC)  JUNE 1992
C
C  LIBRARIES OF RESIDENCE:        MT1731/OPSPL1
C
C  USAGE:  CALL TRLLCH (LAT, NS, LON, EW, IFLG, ICHK, CLALO, NC)
C
C  PARAMETERS:
C     NAME               TYPE        USAGE           DESCRIPTION
C  -------------      ----------    -------   -------------------------
C   LAT               INTEGER         IN       LATITUDE IN DEG X 10
C   NS                CHAR*1          IN       NORTH/SOUTH 
C   LON               INTEGER         IN       LONGITUDE IN DEG X 10 
C   EW                CHAR*1          IN       EAST/WEST
C   IFLG              INTEGER         IN       SECONDS FLAG
C   ICHK              INTEGER         IN       CHECKSUM FLAG
C   CLALO             CHAR*18         OUT      LAT/LONG
C   NC                INTEGER         OUT      NO. OF CHARS IN CLALO 
C
C  COMMON BLOCKS:  SEE MAIN PROGRAM
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C..............MAINTENANCE SECTION...............................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES AND STRUCTURES:
C     CLAT - TEMPORARY LATITUDE (CHAR*8
C     CLON - TEMPORARY LONGITUDE (CHAR*9)
C      LAX - TEMPORARY LATITUDE CHECKSUM ACCUMULATOR (INTEGER)
C      LCP - CHARACTER COUNTER/POINTER (INTEGER) 
C      LND - LONGITUDE DEGREES (INTEGER)
C      LNM - LONGITUDE MINUTES (INTEGER)
C      LOX - TEMPORARY LONGITUDE CHECKSUM ACCUMULATOR (INTEGER)
C      LTD - LATITUDE DEGREES (INTEGER)
C      LTM - LATITUDE MINUTES (INTEGER)
C
C  METHOD:
C
C  COMPILER DEPENDENCES:  FORTRAN 77 (FTN5)
C
C  COMPILER OPTIONS:  NONE
C
C  RECORD OF CHANGES:
C
C      sampson 12/3/96    allow for labels in other hemisphere (N/S)
C
C..............END PROLOGUE......................................
C
      CHARACTER CLALO*18, NS*1, EW*1
      CHARACTER CLAT*8, CLON*9
      character*1 nstemp
C
C * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
c     Initialize local variables, ajs
      LAX = 0
      LCP = 0
      LND = 0
      LNM = 0
      LOX = 0
      LTD = 0
      LTM = 0
cx
cx  check for negative lats, if found, set positive 
cx
      lattemp=lat
      nstemp=ns
      if (lat.lt.0) then
	  lattemp=-lat
	  if (ns.eq.'N')nstemp='S'
	  if (ns.eq.'S')nstemp='N'
      endif
C
C                   CALC LAT, LON IN DEG AND MINUTES
C
cx    LTD = LAT/10 
cx    LTM = MOD (LAT,10) * 6 
      ltd = lattemp/10 
      ltm = mod (lattemp,10) * 6 
      LND = LON/10 
      LNM = MOD (LON,10) * 6 
C
C                   CONVERT TO CHARACTER FORMAT
C
      WRITE (CLAT(1:4),610) LTD, LTM
  610 FORMAT (2I2.2)
      WRITE (CLON(1:5),620) LND, LNM
  620 FORMAT (I3.3,I2.2)
      LCP = 5
C
C                   ADD ZERO SECONDS IF REQUESTED
C
      IF (IFLG .EQ. 0) THEN
        CLAT(5:6) = '00'
        CLON(6:7) = '00'
        LCP = LCP + 2
      ENDIF
C
C                   ADD HEMISPHERE
C
cx    CLAT(LCP:LCP) = NS
      clat(lcp:lcp) = nstemp
      CLON(LCP+1:LCP+1) = EW 
C
C                   ADD CHECKSUMS, IF REQUESTED
C
      IF (ICHK .EQ. 0) THEN
        LCP = LCP + 1
        LAX = (LTD/10) + MOD (LTD,10) + (LTM/10) + MOD (LTM,10)
        LAX = MOD (LAX,10)
        LOX = (LND/100) + (LND/10) + MOD (LND,10) + (LNM/10) +
     *           MOD (LNM,10)
        LOX = MOD (LOX,10)
        WRITE (CLAT(LCP:LCP),630) LAX
  630   FORMAT (I1)
        WRITE (CLON(LCP+1:LCP+1),630) LOX
      ENDIF
C
C                   DETERMINE LAT, LON CHARACTER STRING
C
      NC = LCP + LCP + 2
      CLALO(1:NC) = CLAT(1:LCP) // '/' // CLON(1:LCP+1)
      RETURN
C
      END

      SUBROUTINE TRWHDR
C
C..............START PROLOGUE....................................
C
C  MODULE NAME:                   TRWHDR
C
C  DESCRIPTION:  WRITE THE TC WARNING GOLD MSG HEADER LINES.
C
C  COPYRIGHT:                     (C) 1992 FLENUMOCEANCEN
C                                 U.S. GOVERNMENT DOMAIN
C                                 ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:     GS-09K-90BHD0001
C                                 ADP SUPPORT FOR HIGHLY TECHNICAL
C                                 SOFTWARE DEVELOPEMNT FOR SCIENTIFIC
C                                 APPLICATIONS
C
C  REFERENCES:                    TASK ORDER PFC172730, EPF026-P
C
C  CLASSIFICATION:                UNCLASSIFIED
C
C  RESTRICTIONS:                  NONE 
C
C  ORIGINAL PROGRAMMER, DATE:     DON CHIN, CSC-GSA (MAY 1992)
C
C  CURRENT PROGRAMMER:   HARRY D. HAMILTON  (GSA -CSC)  JUNE 1992
C
C
C  MAINTAINER:  Kent Paul Dolan (GSA - CSC)
C
C  Changes:     1992.04.05: Added code to read site ID information from a
C                           file whose name is on the command line, to
C                           correct a hard wired site identifier in the
C                           output message.
C               1995.11.02: Converted to run in ATCF 3.0 - output filename
C                           is always (stormid.jts)  sampson, NRL, Nov 95
C
C  LIBRARIES OF RESIDENCE:        MT1731/OPSPL1
C
C  USAGE:                         CALL TRWHDR
C
C  PARAMETERS:  NONE
C
C  COMMON BLOCKS:  SEE MAIN PROGRAM
C
C  FILES:
C    NAME      UNIT   FILE TYPE   ATTRIBUTE  USAGE   DESCRIPTION
C  ----------  ----   ----------  ---------- -----  ---------------- 
C   ------      10    LOCAL       SEQUENTIAL  OUT   TC WARNING MSG FILE
C                                                   IN GOLD FORMAT
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C..............MAINTENANCE SECTION...............................
C
C  MODULES CALLED:  NR2MTH - FUNCTION TO CONVERT MONTH (INTEGER)
C                            TO MONTH (CHAR*3)
C
C  LOCAL VARIABLES AND STRUCTURES:
C     IEND - POINTER TO END OF CHARACTER STRING (INTEGER)
C      IMO - MONTH OF YEAR (INTEGER)
C     JBIN - BIN NO. USED FOR JVIDS (INTEGER)
C     JCHK - CHECKSUM (INTEGER)
C      MON - MONTH OF YEAR (CHAR*3)
C   OVLYNM - OVERLAY NAME (CHAR*10)
C
C  METHOD:
C
C  COMPILER DEPENDENCES:  FORTRAN 77 (FTN5)
C
C  COMPILER OPTIONS:  NONE
C
C  RECORD OF CHANGES:
C
C      HDH:     1993.05.24  correct code for jots display of PRODNM
C
C..............END PROLOGUE......................................
C
      CHARACTER*12 FNAME
C
      CHARACTER OVLYNM*10
      CHARACTER MON*3, NR2MTH*3, CN*1
C
      DIMENSION NWPB(4), NEPB(4), NNAB(4), NIOB(4), NSPB(2), NSIB(2)
      CHARACTER WDTG*8,CYCID*3,STNAME*10,MOVDIR*3,MOVSPD*2,
     *          NS*1,EW*1,STG*1,BASIN*2,COLC*1,PRODNM*33,COMMENT*80
      CHARACTER*4 SITEID
cx
      character*100 filename
      character*100 storms
      character*100 includes
      character*80  line1,line2,line3,line4
      character*6   strmid
      character*2   century
      integer       ind
      integer       ioerror, iarg
cx
C
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
      COMMON /MSGS/ MWP21,MWP22,MWP23,MWP24, MEP25,MEP26,MEP27,MEP28,
     .              MNA29,MNA30,MNA31,MNA32, MIO33,MIO34,MIO35,MIO36,
     .              MSP37,MSP38, MSI39,MSI40
      COMMON /USR/ MTF,IFORM,ICHK,IMSG,NUNIT
      COMMON /ERRS/ IERR, IEOF
      COMMON /LOCALE/ SITEID
C
      SAVE NWP, NEP, NNA, NIO, NSP, NSI
      SAVE KMWP, KMEP, KMNA, KMIO, KMSP, KMSI
C
      DATA NWPB/21,22,23,24/, NWP/0/, KMWP/0/
      DATA NEPB/25,26,27,28/, NEP/0/, KMEP/0/
      DATA NNAB/29,30,31,32/, NNA/0/, KMNA/0/
      DATA NIOB/33,34,35,36/, NIO/0/, KMIO/0/
      DATA NSPB/37,38/, NSP/0/, KMSP/0/
      DATA NSIB/39,40/, NSI/0/, KMSI/0/
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
c     Initialize local variables, ajs
      IEND = 0
      IMO = 0
      JBIN = 0
      JCHK = 0
      ind = 0
      ioerror = 0
      NN = 0
      J1 = 0
      J2 = 0
      J3 = 0
      J4 = 0
      I = 0

cx
cx  get the storms directory name
cx
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 2
cajs  Use the following starting arg # when compiling with f90
      iarg = 3
cx
cx    get the storm id
cx
      call getarg(iarg,strmid)
      iarg = iarg + 1
c
c     get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
      print *,"after getargs in TRWHDR"
      print *,"storms:",storms         
      print *,"strmid:",strmid         
C
C                   BUILD PRODUCT NAME, ARRAY STG MUST BE LOADED
C                   ACCORDING TO MAX WIND OF POSITION AND BASIN.
C
      IERR = 0
C                   NOTE: ONLY 14 CHARACTERS ARE DISPLAYED ON JOTS FOR
C                         PRODNM LABEL   (5/24/93)
C
cx  as prescribed by Alex Decaria, JTWC
cx    IF (STG(1) .EQ. 'T') THEN
cx      prodnm = 'TYPHOON ' // stname
cx    ELSE IF (STG(1) .EQ. 'H') THEN
cx      prodnm = 'HURRICANE ' // stname
cx    ELSE IF (STG(1) .EQ. 'C') THEN
cx      prodnm = 'TROP CYCLONE ' // stname
cx    ELSE IF (STG(1) .EQ. 'S') THEN
cx      prodnm = 'TROP STORM ' // stname
cx    ELSE
cx      PRODNM = 'TROP DEPRESSION ' // STNAME
cx    ENDIF
cxx as prescribed by Ed Fukada, NPMOC 3/26/97
cxx added E, C, L as prescribed by Ed Fukada, NPMOC 6/26/97
cxx tropical depression is treated differently, add storm number to these
      in=index(stname,' ') - 1
      if (cycid(3:3).eq.'W' .or. cycid(3:3).eq.'E' .or. 
     +    cycid(3:3).eq.'C' .or. cycid(3:3).eq.'L') then
        if (stg(1) .eq. 'T') then
          prodnm = 'TYPHOON '//stname(1:in)//'('//cycid//')'
        else if (stg(1) .eq. 'S') then
          prodnm = 'TROP STORM '//stname(1:in)//'('//cycid//')'
        else if (stg(1) .eq. 'H') then
          prodnm = 'HURRICANE '//stname(1:in)//'('//cycid//')'
        else
          prodnm = 'TROP DEPRESSION '//cycid//'('//stname(1:in)//')'
        endif
      else
        if (stg(1) .eq. 'T') then
          prodnm = 'TYPHOON '//cycid//'('//stname(1:in)//')'
        else if (stg(1) .eq. 'H') then
          prodnm = 'HURRICANE '//cycid//'('//stname(1:in)//')'
        else if (stg(1) .eq. 'C') then
          prodnm = 'TROP CYCLONE '//cycid//'('//stname(1:in)//')'
        else if (stg(1) .eq. 'S') then
          prodnm = 'TROP STORM '//cycid//'('//stname(1:in)//')'
        else
          prodnm = 'TROP DEPRESSION '//cycid//'('//stname(1:in)//')'
        endif
      endif
C
C                   GET MONTH IN CHARACTER FORMAT
C
cx    READ (WDTG,500) IMO
cx500 FORMAT (4X,I2,4X)
cx  also get the year while your at it.
      READ (WDTG,500) IYR,IMO
  500 FORMAT (I2,I2,4X)
      MON = NR2MTH (IMO)
C
C                   PRESET PARTS OF OUTPUT FILE NAME
C
      FNAME(1:8) = WDTG
      IF (IMSG .EQ. 0) THEN
C                   RAINFORM GOLD EXTENTION
        FNAME(9:10) = '.R'
      ELSE
C                   OTH-T GOLD EXTENTION
        FNAME(9:10) = '.H'
      ENDIF
C
C                   DETERMINE BASIN
C
      IF (BASIN .EQ. 'WP') THEN
C                   ALLOWED BINS ARE: 21, 22, 23 AND 24
        FNAME(1:2) = 'WP'
        KMWP = KMWP +1
        IF (KMWP .LE. 3) THEN
          MWP21 = KMWP
          NWP   = 1
          JBIN  = NWPB(NWP)
          NUNIT = JBIN
          IF (KMWP .EQ. 1) THEN
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMWP .LE. 6) THEN
          MWP22 = KMWP -3
          NWP   = 2
          JBIN  = NWPB(NWP)
          NUNIT = JBIN
          IF (KMWP .EQ. 4) THEN
            MWP21 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMWP .LE. 9) THEN
          MWP23 = KMWP -6
          NWP   = 3
          JBIN  = NWPB(NWP)
          NUNIT = JBIN
          IF (KMWP .EQ. 7) THEN
            MWP22 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMWP .LE. 12) THEN
          MWP24 = KMWP -9
          NWP   = 4
          JBIN  = NWPB(NWP)
          NUNIT = JBIN
          IF (KMWP .EQ. 10) THEN
            MWP23 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSE
          GOTO 710
C
        ENDIF
        NN   = NWP
      ELSE IF (BASIN .EQ. 'EP') THEN
C                   ALLOWED BINS ARE: 25, 26, 27 AND 28
        FNAME(1:2) = 'EP'
        KMEP       = KMEP +1
        IF (KMEP .LE. 3)THEN
          MEP25 = KMEP
          NEP   = 1
          JBIN  = NEPB(NEP)
          NUNIT = JBIN
          IF (KMEP .EQ. 1) THEN
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMEP .LE. 6) THEN
          MEP26 = KMEP -3
          NEP   = 2
          JBIN  = NEPB(NEP)
          NUNIT = JBIN
          IF (KMEP .EQ. 4) THEN
            MEP25 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMEP .LE. 9) THEN
          MEP27 = KMEP -6
          NEP   = 3
          JBIN  = NEPB(NEP)
          NUNIT = JBIN
          IF (KMEP .EQ. 7) THEN
            MEP26 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMEP .LE. 12) THEN
          MEP28 = KMEP -9
          NEP   = 4
          JBIN  = NEPB(NEP)
          NUNIT = JBIN
          IF (KMEP .EQ. 10) THEN
            MEP27 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSE
          GOTO 710
C
        ENDIF
        NN   = NEP
      ELSE IF (BASIN .EQ. 'NA') THEN
C                   ALLOWED BINS ARE: 29, 30, 31 AND 32
        FNAME(1:2) = 'NA'
        KMNA = KMNA +1
        IF (KMNA .LE. 3)THEN
          MNA29 = KMNA
          NNA   = 1
          JBIN  = NNAB(NNA)
          NUNIT = JBIN
          IF (KMNA .EQ. 1) THEN
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMNA .LE. 6) THEN
          MNA30 = KMNA -3
          NNA   = 2
          JBIN  = NNAB(NNA)
          NUNIT = JBIN
          IF (KMNA .EQ. 4) THEN
            MNA29 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMNA .LE. 9) THEN
          MNA31 = KMNA -6
          NNA   = 3
          JBIN  = NNAB(NNA)
          NUNIT = JBIN
          IF (KMNA .EQ. 7) THEN
            MNA30 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMNA .LE. 12) THEN
          MNA32 = KMNA -9
          NNA   = 4
          JBIN  = NNAB(NNA)
          NUNIT = JBIN
          IF (KMNA .EQ. 10) THEN
            MNA31 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSE
          GOTO 710
C
        ENDIF
        NN   = NNA
      ELSE IF (BASIN .EQ. 'IO') THEN
C                   ALLOWED BINS ARE: 33, 34, 35 AND 36
        FNAME (1:2) = 'IO'
        KMIO = KMIO +1
        IF (KMIO .LE. 3)THEN
          MIO33 = KMIO
          NIO   = 1
          JBIN  = NIOB(NIO)
          NUNIT = JBIN
          IF (KMIO .EQ. 1) THEN
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMIO .LE. 6) THEN
          MIO34 = KMIO -3
          NIO   = 2
          JBIN  = NIOB(NIO)
          NUNIT = JBIN
          IF (KMIO .EQ. 4) THEN
            MIO33 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMIO .LE. 9) THEN
          MIO35 = KMIO -6
          NIO   = 3
          JBIN  = NIOB(NIO)
          NUNIT = JBIN
          IF (KMIO .EQ. 7) THEN
            MIO34 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMIO .LE. 12) THEN
          MIO36 = KMIO -9
          NIO   = 4
          JBIN  = NIOB(NIO)
          NUNIT = JBIN
          IF (KMIO .EQ. 10) THEN
            MIO35 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSE
          GOTO 710
C
        ENDIF
        NN   = NIO
      ELSE IF (BASIN .EQ. 'SP') THEN
C                   ALLOWED BINS ARE: 37 AND 38
        FNAME(1:2) = 'SP'
        KMSP = KMSP +1
        IF (KMSP .LE. 3) THEN
          MSP37 = KMSP
          NSP   = 1
          JBIN  = NSPB(NSP)
          NUNIT = JBIN
          IF (KMSP .EQ. 1) THEN
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMSP .LE. 6) THEN
          MSP38 = KMSP -3
          NSP   = 2
          JBIN  = NSPB(NSP)
          NUNIT = JBIN
          IF (KMSP .EQ. 4) THEN
            MSP37 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSE
          GOTO 710
C
        ENDIF
        NN   = NSP
      ELSE
C                   ALLOWED BINS ARE: 39 AND 40
        FNAME(1:2) = 'SI'
        KMSI = KMSI +1
        IF (KMSI .LE. 3)THEN
          MSI39 = KMSI
          NSI   = 1
          JBIN  = NSIB(NSI)
          NUNIT = JBIN
          IF (KMSI .EQ. 1) THEN
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSEIF (KMSI .LE. 6) THEN
          MSI40 = KMSI -3
          NSI   = 2
          JBIN  = NSIB(NSI)
          NUNIT = JBIN
          IF (KMSI .EQ. 4) THEN
            MSI39 = 4
            WRITE (NUNIT-1,'(A5)') 'ENDAT'
            CLOSE (NUNIT-1)
            WRITE (FNAME(11:12),'(I2)') JBIN
cx          OPEN (NUNIT,FILE=FNAME,FORM='FORMATTED')
cx          OPEN (NUNIT,FILE=storms(1:ind)//"/"//FNAME,FORM='FORMATTED')
          ENDIF
        ELSE
          GOTO 710
C
        ENDIF
        NN = NSI
      ENDIF
cx
cx  get the include directory name
cx
      call getenv("ATCFINC",includes)
      ind=index(includes," ")-1
      write(filename,'(a,a)')includes(1:ind),"/jotshead.dat"
cx
cx    get the lines from $ATCFINC/jotshead.dat
cx
      call openfile (12,filename,'old',ioerror)
      if (ioerror.lt.0) then
         write (*,*) ' othmsg: Error opening ',filename
      endif
      read (12,'(a)') line1(1:9)
      read (12,'(a)') line2(1:16)
      read (12,'(a)') line3(1:12)
      read (12,'(a)') line4(1:16)
      print *, "header lines"
      print *, line1(1:9)
      print *, line2(1:16)
      print *, line3(1:12)
      print *, line4(1:16)
      print *, "************"
      close (12)
cx
cx    construct filename, open file
cx
      call getenv("ATCFSTRMS",includes)
      ind=index(includes," ")-1
cajs  write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".jts"
      write(filename,'(6a)') storms(1:ind), "/", 
     1     strmid(1:4), century, strmid(5:6), ".jts"
      print *,"filename:",filename
      print *,"nunit:",nunit
      call openfile (nunit,filename,'unknown',ioerror)
cx    WRITE (*,*) 'Writing on file ',FNAME
      write (*,*) 'Writing on file ',filename
C
C                   WRITE MSG HEADER LINES, DEPENDING ON IMSG
C
      IF (IMSG .NE. 1) THEN
C
C                   WRITE MSGID LINE, USES STATIC MSG NO. OF 087
C
CKPD        WRITE (NUNIT,610) MON
CKPD  610   FORMAT ('MSGID/JTWC/GOLD/087/',A3)

        WRITE (NUNIT,610) SITEID, MON
  610   FORMAT ('MSGID/',A4,'/GOLD/087/',A3)
C
C                   WRITE CTC LINE
C
        WRITE (NUNIT,620)
  620   FORMAT ('CTC/T0000////////MSG')
C
C                   WRITE OVLY LINE
C
        WRITE (CN,'(I1)') NN
        OVLYNM = 'TROPCL ' // BASIN // CN
        WRITE (NUNIT,630) OVLYNM,WDTG(5:8),MON,JBIN
  630   FORMAT ('OVLY/',A10,'/',A4,'00/',A3,'/',I3.3)
C
      ELSE
C
CKPD        WRITE (NUNIT,640) MON
CKPD  640   FORMAT ('MSGID/JTWC/OVLY2/0087/',A3)

cx
cx    write the jots header file lines (4 of them)
cx
        write (nunit,'(a9)')  line1(1:9)
	write (line2(11:13),'(a3)') mon
	write (line2(15:16),'(i2.2)') iyr
        write (nunit,'(a16)') line2(1:16)
        write (nunit,'(a12)') line3(1:12)
        write (nunit,'(a16)') line4(1:16)
cx
cx  write BT and UNCLAS lines above MSGID line
cx
	write (nunit,'(a2)')'BT'
	write (nunit,'(a6)')'UNCLAS'

cx  change to MSGID line per NLMOC request 5/2/00 sampson
cx      WRITE (NUNIT,640) SITEID, MON
cx640   FORMAT ('MSGID/',A4,'/OVLY2/0087/',A3)
	if (siteid.eq.'NLMC') then
	   write (nunit, 641) mon
        elseif (siteid.eq.'NWOC') then
	   write (nunit, 642)
	else
           WRITE (NUNIT,640) SITEID, MON
        endif
  640   FORMAT ('MSGID/',A4,'/OVLY2/0087/',A3)
  641   FORMAT ('MSGID/NLMOC/OVLY2/0087/',A3)
  642   FORMAT ('MSGID/NLMOC/OVLY2/0087/',A3)
C
C                   CALC CHECKSUM, LENGTH OF PRODNM AND WRITE OVLY LINE
C
        READ (WDTG(5:8),'(4I1)') J1,J2,J3,J4
        JCHK = MOD ((J1 + J2 + J3 + J4), 10)
        DO 200 I = 33, 1, -1 
          IF (PRODNM(I:I) .NE. ' ') THEN
            IEND = I
            GOTO 210
C
          END IF
  200   CONTINUE
        I = 33
  210   CONTINUE
cx
cx OVLY line as described by Alex Decaria, JTWC 12/95
cx
cx      WRITE (NUNIT,650) WDTG(5:8),JCHK,MON,PRODNM(1:IEND)
cx650   FORMAT ('OVLY/OCEANMET/',A4,'00Z',I1,'/',A3,'/1OF1/',A)
        print *,"basin:",basin
	if(basin.eq.'WP') then
         write (nunit,650) 'OVLY/WPAC STORM ',
     1	 cycid,wdtg(5:8),jchk,mon,prodnm(1:iend)
	elseif(basin.eq.'IO' .or. basin.eq.'SI' .or. basin.eq.'NI') then
         write (nunit,650) 'OVLY/IO STORM ',
     1	 cycid,wdtg(5:8),jchk,mon,prodnm(1:iend)
	elseif(basin.eq.'SP') then
         write (nunit,650) 'OVLY/SPAC STORM ',
     1	 cycid,wdtg(5:8),jchk,mon,prodnm(1:iend)
	elseif(basin.eq.'NA') then
         write (nunit,650) 'OVLY/ATL STORM ',
     1	 cycid,wdtg(5:8),jchk,mon,prodnm(1:iend)
	elseif(basin.eq.'EP') then
         write (nunit,650) 'OVLY/EPAC STORM ',
     1	 cycid,wdtg(5:8),jchk,mon,prodnm(1:iend)
	elseif(basin.eq.'CP') then
         write (nunit,650) 'OVLY/CPAC STORM ',
     1	 cycid,wdtg(5:8),jchk,mon,prodnm(1:iend)
	endif
  650   format (a,a3,'/',a4,'00Z',i1,'/',a3,'/1OF1/',a,'/METOC')
C
      ENDIF
      RETURN
C
  710 CONTINUE
      WRITE (*,*) 'RFGMSG, TRWHDR - TOO MANY MESSAGES'
      IERR = -1
      RETURN
C
      END

      SUBROUTINE TRWWRN
C
C..............START PROLOGUE....................................
C
C  MODULE NAME:                   TRWWRN
C
C  DESCRIPTION:  SUBR TO WRITE WARNING MSG LINES IN GOLD FORMAT,
C                INCLUDES TRACK, TC SYMBOLS AT EACH POSITION (AT
C                24 HR INTERVALS), MAX RADIUS OF 35 KT WINDS, AND
C                SIGNIFICANT LABELS.
C
C  COPYRIGHT:                     (C) 1992 FLENUMOCEANCEN
C                                 U.S. GOVERNMENT DOMAIN
C                                 ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:     GS-09K-90BHD0001
C                                 ADP SUPPORT FOR HIGHLY TECHNICAL
C                                 SOFTWARE DEVELOPEMNT FOR SCIENTIFIC
C                                 APPLICATIONS
C
C  REFERENCES:                    TASK ORDER PFC172730, EPF026-P
C
C  CLASSIFICATION:                UNCLASSIFIED
C
C  RESTRICTIONS:                  NONE 
C
C  ORIGINAL PROGRAMMER, DATE:     DON CHIN, CSC-GSA (MAY 1992)
C
C  CURRENT PROGRAMMER:   HARRY D. HAMILTON  (GSA -CSC)  JUNE 1992
C
C  LIBRARIES OF RESIDENCE:        MT1731/OPSPL1
C
C  USAGE:  CALL TRWWRN
C
C  PARAMETERS:  NONE
C
C  COMMON BLOCKS:  SEE MAIN PROGRAM
C
C  FILES:
C    NAME      UNIT   FILE TYPE   ATTRIBUTE  USAGE   DESCRIPTION
C  ----------  ----   ---------   ---------  -----  -----------------
C   TROUT       10    LOCAL       SEQUENTIAL  OUT    TC WARNING MSG
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C..............MAINTENANCE SECTION...............................
C
C  MODULES CALLED: 
C    TRLABL - SUBR TO WRITE LABELS INTO MSG
C    TRLLCH - SUBR TO CONVERT LAT, LONG TO CHARACTER FORMAT
C
C  LOCAL VARIABLES AND STRUCTURES:
C    CLALO - LATITUDE, LONGITUDE (CHAR*18)
C
C  METHOD:
C
C  COMPILER DEPENDENCES:  FORTRAN 77 (FTN5)
C
C  COMPILER OPTIONS:  NONE
C
C  RECORD OF CHANGES:
C    <<CHANGE NOTICE>>  21 MAY 93 -- HAMILTON,H.
C             CHANGE "LAMP" TO "RMKS" FOR MODIFIED RAINFORM GOLD
C             CHANGE ORDER OF OUTPUT FOR CORRECT SYMBOL LOCATION
C             AS DONE BY DON CHIN IN FNOC SOFTWARE
C
C     sampson nrl, 5/16/96   new format for OTH "LINE" line
C
C..............END PROLOGUE......................................
C
      CHARACTER CLALO(4)*18, CHRLIN*69
      CHARACTER WDTG*8,CYCID*3,STNAME*10,MOVDIR*3,MOVSPD*2,
     *          NS*1,EW*1,STG*1,BASIN*2,COLC*1,PRODNM*33,COMMENT*80
C
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /TRDATA/ NOWARN,NPTS,LAT(4),LON(4),MAXWND(4),IRAD35(4),
     *                KTAU(4),NC(4),ICOL,I35FLG,IAMPHR,IAMPCC,NCHNAM
      COMMON /USR/ MTF,IFORM,ICHK,IMSG,NUNIT
      COMMON /ERRS/ IERR, IEOF
C
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
c     Initialize local variables, ajs
      I = 0
      NK = 0
C
C                   CONVERT LAT, LON TO CHARACTER STRING IN RFG FORMAT
C
      DO 100 I=1, NPTS
        CALL TRLLCH (LAT(I),NS(I),LON(I),EW(I),IFORM,ICHK,CLALO(I),
     *               NC(I))
C
C                   WRITE INITIAL TC SYMBOL AT INITIAL POSITION AND
C                   OTHER SYBOLS AT OTHER LOCATIONS
C
        IF (IMSG .NE. 1) THEN
C                     MODIFIED RAINFORM GOLD
          WRITE (NUNIT,600) CLALO(I)(1:NC(I)), CLALO(I)(1:NC(I)), ICOL
  600     FORMAT ('LINE/1/2/',A,'/',A,'/',I1)
          WRITE (NUNIT,610) STG(I)
  610     FORMAT ('RMKS/',A1)
C
        ELSE
C                     OTH GOLD FORMAT
          WRITE (NUNIT,615) COLC,CLALO(I)(1:NC(I)),STG(I)
  615     FORMAT ('TEXT/20//',A1,'/',A,'/',A1)
C
        ENDIF
  100 CONTINUE
C
C                   WRITE SUBSEQUENT TRACK LINES AND TC SYMBOLS
C
      IF (NPTS .GE. 2) THEN
C
        DO 200 I=1, NPTS
C
          IF (IMSG .NE. 1) THEN
C
C                       PUT IN MODIFIED RAINFORM GOLD FORMAT
C
            IF (I .EQ. 1) THEN
              WRITE (CHRLIN,617) NPTS,CLALO(1)(1:NC(1))
  617         FORMAT ('LINE/1/',I1,'/',A)
              NK = 10 +NC(1)
            ELSE
              CHRLIN(NK:NK+18) = '/' // CLALO(I)(1:NC(I))
              NK = NK +19
            ENDIF
C
C                  WRITE LINE, AS REQUIRED
C
            IF (I .EQ. NPTS) THEN
              WRITE (CHRLIN(NK:NK+1),666) ICOL
  666         FORMAT ('/',I1)
              WRITE (NUNIT,618) CHRLIN
  618         FORMAT (A)
            ELSEIF (I .EQ. 3) THEN
              WRITE (NUNIT,618) CHRLIN
              CHRLIN = ' '
              NK = 1
            ENDIF
          ELSE
C
C                   PUT IN OTH GOLD FORMAT
C
            IF (I .EQ. 1) THEN
              WRITE (CHRLIN,619) NPTS,COLC,CLALO(1)(1:NC(1))
  619         FORMAT ('LINE/',I1,'//',A1,'/',A)
              NK = 11 +NC(1)
            ELSE
              CHRLIN(NK:NK+18) = '/' // CLALO(I)(1:NC(1))
              NK = NK +19
            ENDIF
C
C                  WRITE LINE, AS REQUIRED
C
            IF (I .EQ. NPTS) THEN
cx  Don't write the color after the last longitude ... new format bs 5/16/96
cx            WRITE (CHRLIN(NK:NK+1),666) ICOL
              WRITE (NUNIT,618) CHRLIN
            ELSEIF (I .EQ. 3) THEN
              WRITE (NUNIT,618) CHRLIN
              CHRLIN = ' '
              NK = 1
            ENDIF
          ENDIF
C
  200   CONTINUE
C
      ENDIF
C

C                   WRITE RADIUS OF 35 KTS
C
      DO 250 I=1, NPTS
C
        IF (IRAD35(I) .GT. 0) THEN
C
          IF (IMSG .NE. 1) THEN
C
            WRITE (NUNIT,620) CLALO(I)(1:NC(I)), IRAD35(I), ICOL
  620       FORMAT ('CIR/1/',A,'/',I3.3,'/',I1)
C
          ELSE
C
            WRITE (NUNIT,625) COLC,CLALO(I)(1:NC(I)),IRAD35(I),IRAD35(I)
  625       FORMAT ('ARC/0/',A1,'///',A,'/',I3.3,'NM/',I3.3,'NM')
          ENDIF
C
        ENDIF
C
  250 CONTINUE
C
C                   GENERATE LABELS AT WARNING POSITIONS
C
      CALL TRLABL
      RETURN
C
      END
      SUBROUTINE READDGR
C
C..............START PROLOGUE....................................
C
C  MODULE NAME:                   READDGR
C
C  DESCRIPTION:  SUBR TO READ DANGER AREA POINTS FROM FILE.     
C
C  CLASSIFICATION:                UNCLASSIFIED
C
C  RESTRICTIONS:                  NONE 
C
C  ORIGINAL PROGRAMMER, DATE:     B. SAMPSON, NRL (JUN 1999)
C
C  USAGE:  CALL READDGR
C
C  PARAMETERS:  NONE
C
C  COMMON BLOCKS:  SEE MAIN PROGRAM
C
C  FILES:
C    NAME      UNIT   FILE TYPE   ATTRIBUTE  USAGE   DESCRIPTION
C  ----------  ----   ---------   ---------  -----  -----------------
C   *.dgr       13    LOCAL       SEQUENTIAL  IN     DANGER AREA POINTS
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C..............MAINTENANCE SECTION...............................
C
C  MODULES CALLED: 
C
C  LOCAL VARIABLES AND STRUCTURES:
C
C  METHOD:
C
C  COMPILER DEPENDENCES:  FORTRAN 77 
C
C  COMPILER OPTIONS:  NONE
C
C  RECORD OF CHANGES:
C
      INTEGER       LAT, LON
      INTEGER       ISEC, ICHK 
      INTEGER       INUM(500)
      INTEGER       NDANG
      CHARACTER*8   DDTG
      CHARACTER*18  DAREA(500)
      COMMON /DANGER/ DDTG, NDANG, DAREA, INUM
      ISEC = 0
      ICHK = 1
      NDANG = 0
      PRINT *, "IN READDGR"
      READ (13, '(2X,A8)', END = 300) DDTG
      DO 100 I = 1, 500
       DAREA(I)="                  "
       READ (13,'(I4,A1,1X,I5,A1)' , END = 300) LAT, NS, LON, EW
       CALL TRLLCH ( LAT, NS, LON, EW, ISEC, ICHK, DAREA(I), INUM(I))
       PRINT *, I, DAREA(I)
      NDANG = I
  100 CONTINUE
  300 CONTINUE
      RETURN
      END

      SUBROUTINE TRWDGR 
C
C..............START PROLOGUE....................................
C
C  MODULE NAME:                   TRWDGR 
C
C  DESCRIPTION:  SUBR TO WRITE DANGER AREA POINTS TO FILE.     
C
C  CLASSIFICATION:                UNCLASSIFIED
C
C  RESTRICTIONS:                  NONE 
C
C  ORIGINAL PROGRAMMER, DATE:     B. SAMPSON, NRL (JUN 1999)
C
C  USAGE:  CALL TRWDGR
C
C  PARAMETERS:  NONE
C
C  COMMON BLOCKS:  SEE MAIN PROGRAM
C
C  FILES:
C    NAME      UNIT   FILE TYPE   ATTRIBUTE  USAGE   DESCRIPTION
C  ----------  ----   ---------   ---------  -----  -----------------
C   TROUT       13    LOCAL       SEQUENTIAL  IN     DANGER AREA POINTS
C
C  ERROR CONDITIONS:  NONE
C
C  ADDITIONAL COMMENTS:
C
C..............MAINTENANCE SECTION...............................
C
C  MODULES CALLED: 
C
C  LOCAL VARIABLES AND STRUCTURES:
C
C  METHOD:
C
C  COMPILER DEPENDENCES:  FORTRAN 77 
C
C  COMPILER OPTIONS:  NONE
C
C  RECORD OF CHANGES:
C
      INTEGER       INUM(500)
      INTEGER       NDANG
      CHARACTER*8   WDTG
      CHARACTER*8   DDTG
      CHARACTER*18  DAREA(500)
      CHARACTER     CHRLIN*69
      COMMON /DANGER/ DDTG, NDANG, DAREA, INUM
      COMMON /TRDATC/ WDTG,CYCID,STNAME,MOVDIR,MOVSPD,
     *                NS(4),EW(4),STG(4),BASIN,COLC,PRODNM,COMMENT
      COMMON /USR/ MTF,IFORM,ICHK,IMSG,NUNIT
      ISEC = 0
      ICHK = 1
      PRINT *, "IN TRWDGR"

      IF (DDTG .NE. WDTG) THEN
	PRINT *, "DANGER AREA DATA OUT OF DATE.",DDTG, " VS ", WDTG
	RETURN

      ELSE
        DO 100 I = 1, NDANG-1
         PRINT *, "I=", I, "DAREA=", DAREA(I), " INUM=", INUM
         WRITE (NUNIT,619) DAREA(I)(1:INUM(I)), DAREA(I+1)(1:INUM(I+1))
  619    FORMAT ('LINE/2','//G','/',A,'/',A)
         PRINT *, "I=", I, "DAREA=", DAREA(I), " INUM=", INUM
  100   CONTINUE
CX   LAST LINE CLOSES THE DANGER AREA
      WRITE (NUNIT,619) DAREA(NDANG)(1:INUM(NDANG)), DAREA(1)(1:INUM(1))
      ENDIF

      RETURN
      END
