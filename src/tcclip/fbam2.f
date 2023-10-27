      
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  FBAM2
C
C  DESCRIPTION:     FBAM2 IS THE SECOND PROGRAM OF THE FNOC BETA AND
C                   ADVECTION MODEL (FBAM) FOR PREDICTION OF TROPICAL
C                   CYCLONE MOVEMENT. IT IS BASED UPON THE JOINT TYPHOON
C                   WARNING CENTER (JTWC) JBAM, BY LT MICHAEL FIORINO,
C                   WHICH IN TURN IS BASED UPON THE NATIONAL
C                   METEOROLOGICAL CENTER (NMC) ORIGINAL VERSION OF BAM,
C                   BY MR. DONALD MARKS
C
C  ORIGINAL PROGRAMMER, DATE:  HARRY D. HAMILTON    (MM -GSA)  OCT 89
c  current programmer, date:   buck sampson         (nrl)      aug 95
C
C  COMPUTER/OPERATING SYSTEM:  Concurrent
C
C  LIBRARIES OF RESIDENCE:     
C
C  CLASSIFICATION:             UNCLASSIFIED
C
C  USAGE:                      fbam2 wp0195
C                                    where wp0195 is the storm id
C
C  INPUT FILES:    sbam.flds  (TAPE31)- SHALLOW REGIONAL FIELDS
C                  mbam.flds  (TAPE32)- MEDIUM REGIONAL FIELDS
C                  fbam.flds  (TAPE33)- DEEP REGIONAL FIELDS
C                  ??????.dat         - tropical cyclone data
C
C  OUTPUT FILES:   to screen          - HIGH LEVEL DIAGNOSTICS
C                  fbam.dbg           - LOW LEVEL DIAGNOSTICS
C                  wptot.dat          - TROPICAL CYCLONE FORECAST
C
C........................MAINTENANCE SECTION............................
C
C  BRIEF DESCRIPTION OF PROGRAM MODULES:
C
C     EFFRAD - ADJUSTS THE EFFECTIVE RADIUS AND INFLOW ANGLE SO AS TO
C              PROVIDE THE BEST MATCH OF THE CYCLONE MOTION WITH THE
C              LARGE-SCALE FLOW.
C
C     FLDINT - INTERPOLATES IN THE REGIONAL GRID, A SUBSET OF THE LARGE-
C              SCALE WIND FIELD ON A 2.5 DEGREE SPHERICAL GRID (BUT NOT
C              IN ORIENTATION).
C
C     LSFCST - UPDATES THE LARGE-SCALE WIND FIELD AT EACH TIME STEP IN
C              THE MODEL.
C
C     LSTEND - CALCULATES THE RATE OF CHANGE OF THE LARGE-SCALE FLOW PER
C              TIME STEP OF THE MODEL, EACH 12 HOURS.
C
C     RDLSUV - DIRECT ACCESS READ OF REGIONAL LARGE-SCALE FIELDS CREATED
C              BY FBAM1.
C
C
C     STHETA - SOLVES THE BAM EQUATIONS TO PREDICT DIRECTION AND SPEED
C              OF MOVEMENT.
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C
C        THETAI - INITIAL BIASED DIRECTION OF CYCLONE MOTION, RADIANS
C        SPDI   - INITIAL SPEED OF CYCLONE MOTION, M/S
C        THETAM - MODIFIED BIASED DIRECTION OF CYCLONE MOTION, RADIANS
C        SPDM   - MODIFIED SPEED OF CYCLONE, M/S
C        THETAF - FORECAST BIASED DIRECTION OF CYCLONE MOTION, RADIANS
C        SPDF   - FORECAST SPEED OF CYCLONE MOTION, M/S
C
C  COMMON BLOCKS:
C
C     COMMON /CONST/:
C           DEGRAD - DEGREE TO RADIAN CONVERSION FACTOR
C           HPI    - RADIANS IN  90 DEGREES
C           PI     - RADIANS IN 180 DEGREES
C           TPI    - RADIANS IN 360 DEGREES
C           RADDEG - RADIAN TO DEGREE CONVERSION FACTOR
C           RKT2MS - KNOTS TO M/S CONVERSION FACTOR
C           RMS2KT - M/S TO KNOTS CONVERSION FACTOR
C
C     COMMON /DTGS/
C           DTGFLD - BASE DTG OF FIELDS (00 OR 12Z FOR HOUR)
C           DTGSYP - SYNOPTIC DTG OF COMPUTER (00 OR 12Z FOR HOUR)
C           DTGFIX - DTG OF LAST FIX LOCATION (00, 06, 12 OR 18Z FOR HR)
C
C     COMMON /FCST/
C           FTIME  - FORECAST TIME, HOURS (0,1,2,3,....)
C           CLAT   - FORECAST LATITUDE, DEGREES (+N, -S)
C           CLON   - FORECAST LONGITUDE, DEGREES WEST
C           CTHETA - FORECAST CYCLONE COURSE, DEGREES
C           ETHETA - FORECAST ENVIRONMENTAL STEERING COURSE, DEGREES
C           DTHETA - CTHETA -ETHETA
C           CSPEED - FORECAST CYCLONE SPEED, M/S
C           ESPEED - FORECAST ENVIRONMENTAL STEERING SPEED, M/S
C           DSPEED - CSPEED -ESPEED
C
C     COMMON /GRID/:
C           IDTFLD - TIME DIFFERENCE BETWEEN TIME OF FIX AND VERIFYING
C                    TIME OF FIRST LARGE-SCALE WIND FIELDS, HOURS
C           ISBIG  - FIRST DIMENSION IN FNOC SPHERICAL GRID OF UPPER
C                    LEFT CORNER OF REGIONAL GRID
C           JSBIG  - SECOND DIMENSION IN FNOC SPHERICAL GRID OF LEFT
C                    EDGE OF REGIONAL GRID
C           MBYN   - LENGTH OF REGIONAL GRID
C           MGRD   - FIRST  DIMENSION OF REGIONAL GRID
C           NGRD   - SECOND DIMENSION OF REGIONAL GRID
C
C     COMMON /OBSV/:
C           ALPHA  - BIASED DIRECTION OF LARGE SCALE FLOW, RADIANS
C           BETA   - RELATED TO CORIOLIS PARAMETER
C           C      - STRENGTH OF VORTEX
C           GAMMA  - INFLOW ANGLE AT EFFECTIVE RADIUS, RADIANS
C           REFF   - EFFECTIVE RADIUS OF CYCLONE, M
C           REDEG  - EFFECTIVE RADIUS OF CYCLONE, DEGREES
C           SPD    - SPEED OF MOTION OF CYCLONE, M/S
C           VB     - AVERAGE WIND SPEED OF LARGE-SCALE FLOW, M/S
C           VEB    - AVERAGE EAST-WEST COMPONENT OF LS FLOW, M/S
C           VNB    - AVERAGE NORTH-SOUTH COMPONENT OF LS FLOW, M/S
C           VS     - TANGENTIAL SPEED OF CYCLONE AT REFF, M/S
C           XI     - VORTEX SHAPE PARAMETER
C           XLATC  - LATITUDE OF CYCLONE
C
C     COMMON /PRNT/
C           IPRNT  - PRINT FLAG, THE HIGHER THE NUMBER THE MORE
C                    DIAGNOSTICS ARE PRINTED
C
C     COMMON /TEND/
C           UTEND  - CHANGE OF U-COMPONENT PER TIME STEP OF MODEL
C           VTEND  - CHANGE OF V-COMPONENT PER TIME STEP OF MODEL
C
C     COMMON /WIND/
C           U1     - PRESENT  U-COMPONENT OF LARGE SCALE FLOW, M/S
C           U2     - FORECAST U-COMPONENT OF LARGE SCALE FLOW, M/S
C           V1     - PRESENT  V-COMPONENT OF LARGE SCALE FLOW, M/S
C           V2     - FORECAST V-COMPONENT OF LARGE SCALE FLOW, M/S
C
C  LANGUAGE:                   FORTRAN 77
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  FBAM2*01  (14 AUG 91) -- HAMILTON,H.
C           PROVIDE FOR PROCESSING SHALLOW AND MEDIUM LAYER FIELDS
C           IN ADDITION TO ORIGINAL DEEP LAYER MEANS - JTWC REQUEST
C
C  <<CHANGE NOTICE>>  FBAM2*02  (18 SEP 1991)  -- HAMILTON,H.
C           ELIMINATE ATAN2 PROBLEM
C
C  <<CHANGE NOTICE>>  02 AUG 1995  -- SAMPSON,B.
C           CONVERT TO RUN UNDER ATCF 3.0
c
c     Modified to use new data format,  6/98   A. Schrader
c     Added cent - century of current posit,  11/98   B. Sampson
C
C
C........................END PROPLOGUE..................................
C
      include 'dataioparms.inc'

C                   SET MAXIMUM LIMITS ON FIELDS
cx    PARAMETER (MG = 69,  NG = 45,  MGBYNG = MG*NG)
      parameter (mg = 144,  ng = 73,  mgbyng = mg*ng)
      PARAMETER (MH = 72)
C
      CHARACTER*1 CHEMNS,CHEMEW,HEMNS0,HEMEW0
      CHARACTER*3 STRMID
      CHARACTER*4 AIDNAM(3)
      CHARACTER*8 DTGFLD,DTGSYP,DTGFIX
C
      character*100 filename,storms
      character*80  card
      character*8   dtgfix12
      character*8   dtgck
      character*6   stormid
      character*1   cdummy,chem12ns,chem12ew
      character*2   century
      character*2   cent
      character*8   btdtg
      character     btns*1, btew*1
      integer       ltlnwnd(numtau,llw)
      integer       ibtwind, ios
      integer       ii, jj, iarg
      real          btlat, btlon

      LOGICAL BLEND
C
      COMMON/CONST/ HPI,PI,TPI,DEGRAD,RADDEG,RMS2KT,RKT2MS
      COMMON/DTGS/  DTGFLD,DTGSYP,DTGFIX,STRMID
      COMMON/FCST/  FTIME(0:MH),  CLAT(0:MH),  CLON(0:MH),
     .             CTHETA(0:MH),ETHETA(0:MH),DTHETA(0:MH),
     .             CSPEED(0:MH),ESPEED(0:MH),DSPEED(0:MH)
      COMMON/GRID/ MGRD,NGRD,MBYN,ISBIG,JSBIG,IDTFLD
      COMMON/OBSV/ BETA,GAMMA,REFF,REDEG,VS,C,XI,ALPHA,VB,VEB,VNB,
     .             SPDM,XLATC
      COMMON/PRNT/ IPRNT
      COMMON/WIND/ U1(MGBYNG),V1(MGBYNG),U2(MGBYNG),V2(MGBYNG)
      COMMON/TEND/ UTEND(MGBYNG),VTEND(MGBYNG)
C
      DATA VRAD2/34.0/, RAD2/150.0/
cx                  set blending on (blend persistence and 12 hr fcst)
      data blend/.true./
C                   SET BLEND HR, REAL AND INTEGER
      DATA BLNDHR/12.0/, IBLNDH/12/
C                   SET TIME STEP OF LARGE-SCALE WIND FIELDS
      DATA DTFLDS/12.0/
C                   SET LAST ITERATION FOR 72 HOUR FORECAST
      DATA LSTITR/72/
CCC   DATA REFFIN/300.0/, GAMAIN/30.0/
C                   SET UNIT NUMBERS FOR INPUT AND OUTPUT
      DATA IOFBAM/44/, IOFCST/19/
      DATA AIDNAM/'SBAM', 'MBAM', 'FBAM'/
      DATA EPSLON/0.00001/
C
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
cx
cx  open the output file for low level diagnostics
cx
      call openfile (7,'fbam.dbg','UNKNOWN',ierr)
c
c*************  This code added to read best track ...bs 8/4/95 *******
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
      call getarg(iarg,stormid)
      iarg = iarg + 1
      call locase (stormid,6)
c
c  get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
c
c  write heading on output
c
      print *,'********************************************************'
      print *,'          fbam forecast for ',stormid
c
c  set the filenames and open the input and output files
c
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     stormid(1:4), century, stormid(5:6), ".dat"
      open (44,file=filename,status='old',err=700)
c
c  convert the 1st two characters of stormid to uppercase
c
      call upcase(stormid,6)
      strmid(1:2)=stormid(3:4)
      strmid(3:3)=stormid(1:1)
c
c  find the last dtg in the best track file
c
      ios = 0
      do while ( ios .eq. 0 )
         call readBT(44,cent,dtgfix,btlat,btns,btlon,btew,ibtwind,ios)
      enddo
cx    print *, 'dtgfix:',dtgfix
c
c  now find the  current and -12 hr positions
c
      call icrdtg (dtgfix,dtgfix12,-12)
      rewind 44

      ios = 0
      do while ( ios .eq. 0 )
         call readBT(44,cent,btdtg,btlat,btns,btlon,btew,ibtwind,ios)
         if( ios .eq. 0 ) then
            if( btdtg .eq. dtgfix ) then
               rlatin = btlat
               chemns = btns
               rlonin = btlon
               chemew = btew
            else if( btdtg .eq. dtgfix12 ) then
               rlat12 = btlat
               chem12ns = btns
               rlon12 = btlon
               chem12ew = btew
            endif
         endif
      enddo
      close (44)
c
c  compute the 12 hour speed and direction of motion
c
      alatin=rlatin
      if(chemns.eq.'S')alatin=-rlatin
      alat12=rlat12
      if(chem12ns.eq.'S')alat12=-rlat12
      alonin=rlonin
      if(chemew.eq.'E')alonin=360.0 - rlonin
      alon12=rlon12
      if(chem12ew.eq.'E')alon12=360.0 - rlon12
      print *, '-12 hr  posit:',alat12,alon12
      print *, 'current posit:',alatin,alonin
      crsin=1.0
      spdin=1.0
      call dirdst(alat12,alon12,alatin,alonin,crsin,distance)
      spdin=distance/12.0
cx    print *, crsin,spdin

c********************************************************
c  set these for now, may need to figure them out later
c********************************************************
c  tau of base field for fcst 
      itau=0
c  difference between last track position time and base field time ?
      nhrdif=0
c  number of fields (taus) for each set of fields
      nrecs=14
      nrecm=14
      nrecf=14
c  dtg of the field,synoptic time of computer (00,12Z)
      dtgfld=dtgfix
      dtgsyp=dtgfix
c  radius of 30 kt winds
      k30rad=120
c  mgrd and ngrd are the dimensions of the whole spherical field
      mgrd=144
      ngrd=73
c  isbig and jsbig are the starting point of the sub-grid on the 
c  master grid
      isbig=1
      jsbig=1

cx    OPEN (UNIT=IOFBAM,FILE='TAPE44',IOSTAT=IOE,ERR=700,
cx   .      STATUS='UNKNOWN',ACCESS='SEQUENTIAL',FORM='UNFORMATTED')
cx    REWIND IOFBAM
cx
cx                  INPUT CYCLONE INFO
cx    READ (IOFBAM,IOSTAT=IOE,ERR=705,END=707) RLATIN,CHEMNS,RLONIN,
cx   .      CHEMEW,CRSIN,SPDIN
cx
cx                  INPUT DTG OF CYCLONE AND FIELD, AND TIME DIFFERENCE
cx    READ (IOFBAM,IOSTAT=IOE,ERR=705,END=707) DTGFLD,DTGSYP,DTGFIX,
cx   .      STRMID,ITAU,NHRDIF
cx
cx                  INPUT WIND RADIUS, GRID INFO AND BLEND INDICATOR
cx    READ (IOFBAM,IOSTAT=IOE,ERR=705,END=707) K30RAD,MGRD,NGRD,
cx   .      ISBIG,JSBIG,BLEND
cx    READ (IOFBAM,IOSTAT=IOE,ERR=705,END=707) NRECS,NRECM,NRECF
cx    CLOSE (IOFBAM)
C
      PRINT *, 'FBAM2, PRINTING FBAM1 VALUES FROM TAPE44'
      WRITE (*,610) RLATIN,CHEMNS, RLONIN,CHEMEW, CRSIN, SPDIN
  610 FORMAT(' ','RLATIN = ',F4.1,A1,/
     1       ' ','RLONIN = ',F5.1,A1,/
     1       ' ','COURSE = ',F5.1,' DEG'/
     1       ' ',' SPEED = ',F4.1,' KTS'//)
C
C                   DEFINE CYCLONE LAT/LON IN DEG N AND DEG W
      IF (CHEMNS.EQ.'S' .OR. CHEMNS.EQ.'S') RLATIN = -RLATIN
      IF (CHEMEW.EQ.'E' .OR. CHEMEW.EQ.'E') RLONIN = 360.0 -RLONIN
C
      WRITE (*,620) DTGFIX,DTGSYP,NHRDIF,BLEND,MGRD,NGRD,ISBIG,JSBIG
  620 FORMAT (' ','DTGFIX = ',A,/
     1        ' ','DTGSYP = ',A,/
     1        ' ','NHRDIF = ',I3,/
     1        ' ',' BLEND = ',L1,/
     1        ' ','  MGRD = ',I3,/
     1        ' ','  NGRD = ',I3,/
     1        ' ',' ISBIG = ',I3,/
     1        ' ',' JSBIG = ',I3,/)
      WRITE (*,621) NRECS,NRECM,NRECF
  621 FORMAT (' FBAM2, PROCESSING ',I2,' SHALLOW ',I2,' MEDIUM AND ',
     .         I2,' DEEP LAYER WIND RECORDS')
c
c open the three input files (fbam.dat,mbam.dat,sbam.dat)
c
      write(filename,'(a,a,a)')storms(1:ind),"/sbam.",dtgfix   
      open (31,file=filename,err=740,access='direct',
     &         recl=42048,status='old')
      read (31,rec=1)dtgck
      if (dtgck.ne.dtgfix) then
          print *, filename,':',dtgck,' is wrong date-time-group'
          stop 'FBAM2: ABORT, WRONG FIELD DTG FOR SBAM'
      endif
      write(filename,'(a,a,a)')storms(1:ind),"/mbam.",dtgfix   
      open (32,file=filename,err=740,access='direct',
     &         recl=42048,status='old')
      read (32,rec=1)dtgck
      if (dtgck.ne.dtgfix) then
          print *, filename,':',dtgck,' is wrong date-time-group'
          stop 'FBAM2: ABORT, WRONG FIELD DTG FOR MBAM'
      endif
      write(filename,'(a,a,a)')storms(1:ind),"/fbam.",dtgfix   
      open (33,file=filename,err=740,access='direct',
     &         recl=42048,status='old')
      read (33,rec=1)dtgck
      if (dtgck.ne.dtgfix) then
          print *, filename,':',dtgck,' is wrong date-time-group'
          stop 'FBAM2: ABORT, WRONG FIELD DTG FOR FBAM'
      endif
C
C                   DEFINE CONSTANTS AND MODEL PARAMETERS
C
      PI     = ACOS (-1.0)
      HPI    = 0.5*PI
      TPI    = 2.0*PI
      DEGRAD = PI/180.0
      RADDEG = 180.0/PI
      RMS2KT = 3600.0/1852.0
      RKT2MS = 1.0/RMS2KT
      IDTFLD = ANINT (DTFLDS)
C                   SET PRINT DIAGNOSTIC FLAG VALUE
      IPRNT  = 0
cx    IPRNT  = 5
cx    IPRNT  = 11
      MBYN   = MGRD*NGRD
      IF (MBYN .GT. MGBYNG) GOTO 710
C
C                   CONVERT FROM KTS TO M/S AND N.MI. TO M
      VRAD2 = VRAD2*RKT2MS
      RAD2  = RAD2*1852.0
C
      DO 290 J=1, 3
        IF (J .EQ. 1) THEN
          IOFLD = 31
          NRECL = NRECS
        ELSEIF (J .EQ. 2) THEN
          IOFLD = 32
          NRECL = NRECM
        ELSE
          IOFLD = 33
          NRECL = NRECF
        ENDIF
        WRITE (*,625) AIDNAM(J)
  625   FORMAT (//,21X,'FOLLOWING DIAGNOSTICS FOR ',A4,//)
        IF (NRECL .LT. 10) THEN
          PRINT*,'FBAM2, NOT ENOUGH WIND FIELDS FOR FORECAST'
          GOTO 290
C
        ENDIF
C                   INITIALIZE STORM POSITIONS
      DO 110 I=1, MH
         FTIME(I) = -I
         CLAT(I)  =  99.9
         CLON(I)  = 999.9
  110 CONTINUE
C
C                   ESTABLISH INITIAL THETA AND SPEED, CHANGE CYCLONE
C                   COURSE FOR TRIGONOMETRIC REASONS AND SPEED FROM KTS
C                   TO M/S
      THETAI = (360.0 -CRSIN)*DEGRAD
      SPDI   = SPDIN*RKT2MS
C                   LOAD VALUES FOR MODEL USE
      THETAM = THETAI
      SPDM   = SPDI
C
C                   INITIALIZE BASIC VORTEX PARAMETERS
      XI = 0.5
      C  = 0.5*(VRAD2*(RAD2**XI) +7460.0)
      IF (RLATIN .LT. 0.0) C = -C
C
C                   INITIALIZE EFFECTIVE RADIUS ,REFF, TO 280 KM AND
C                   INFLOW ANGLE, GAMMA, TO ZERO.
C                   BOTH WILL BE CALCULATED LATER
      REFF  = 280000.0
      GAMMA = 0.0
C
C                   INITIALIZE REDEG FOR INITIAL SAMPLING OF LARGE-
C                   SCALE FLOW
      RAD30 = 1852.0*FLOAT (K30RAD)
C                   ASSUME THERE ARE 111,137 M PER DEGREE OF LATITUDE
C                   AS G. HOLLAND DID IN 1983 PAPER
      REDEG = AMAX1 (0.8*RAD30,400.E3)/111137.0
C
C                   INITIALIZE THE CYCLONE POSITION IN THE MODEL
      XLATC = RLATIN
      XLONC = RLONIN
C
C                   INITIALIZE HOUR AND ITERATION COUNTERS
      IHR   = 0
      ITER  = 0
      IREFF = 0
C
C                   INITIALIZE LTLNWND ARRAY
      do ii=1,numtau
         ltlnwnd(ii,1) = 0
         ltlnwnd(ii,2) = 0
         ltlnwnd(ii,3) = 0
      enddo
C
C                   ***** START THE MODEL *****
C
C READ IN THE FIRST TWO LARGE-SCALE WIND FIELDS
      CALL RDLSUV (U1,IOFLD,IERU)
C                   ABORT IF NO LARGE-SCALE DATA
      IF (IERU .NE. 0) GOTO 720
C
      CALL RDLSUV (V1,IOFLD,IERV)
C                   ABORT IF NO LARGE-SCALE DATA
      IF (IERV .NE. 0) GOTO 720
C
      NREC = 2
C*********************************************************************
C******
C******     RETURN POINT FOR READING IN AND PROCESSING NEW WIND FIELDS
C******
C***********+**********************************************************
C
  115 CONTINUE
      IF (NREC +2 .GT. NRECL) GOTO 125
C
      CALL RDLSUV (U2,IOFLD,IERU)
C                   ABORT IF NO SECOND LARGE-SCALE WIND DATA
      IF (IERU.NE.0 .AND. ITER.EQ.0) GOTO 720
C
      CALL RDLSUV (V2,IOFLD,IERV)
C                   ABORT IF NO SECOND LARGE-SCALE WIND DATA
      IF (IERV.NE.0 .AND. ITER.EQ.0) GOTO 720
C
      NREC = NREC +2
      IF (IERU.EQ.0 .AND. IERV.EQ.0)
C                   CALCULATE LARGE-SCALE TENDENCIES
     .   CALL LSTEND (U1,V1,U2,V2,UTEND,VTEND)
C     ELSE
C        USE PERSISTANCE OF LAST TENDENCY
C
      IF (ITER.EQ.0 .AND. NHRDIF.NE.0) THEN
C                   ADJUST TIME OF WIND FIELD TO TIME OF CYCLONE
C                   BY UPDATING WIND FIELD
         DO 120 N=1, NHRDIF
            CALL LSFCST (UTEND,VTEND,U1,V1)
            IHR = IHR +1
  120    CONTINUE
      ENDIF
C
C*********************************************************************
C******
C****** ITERATION ZERO RETURN POINT FOR MAKING THE TRACK FORECAST
C******
C*********************************************************************
C
  125 CONTINUE
C
C                   FIND U,V LARGE-SCALE WIND COMPONENTS IN VICINITY
C                   OF THE TROPICAL CYCLONE
C
      TOPLAT = XLATC +REDEG
      BOTLAT = XLATC -REDEG
      SCLI   = 1.0/COS (XLATC*DEGRAD)
      EASTLN = XLONC -REDEG*SCLI
      WESTLN = XLONC +REDEG*SCLI
C
C                   INTERPOLATE FOR NORTH POINT VALUES
      CALL FLDINT (U1,TOPLAT,XLONC,UTOP,IERR)
      IF (IERR .NE. 0) GOTO 130
C
      CALL FLDINT (V1,TOPLAT,XLONC,VTOP,IERR)
C
C                   INTERPOLATE FOR SOUTH POINT VALUES
      CALL FLDINT (U1,BOTLAT,XLONC,UBOT,IERR)
      IF (IERR .NE. 0) GOTO 130
C
      CALL FLDINT (V1,BOTLAT,XLONC,VBOT,IERR)
C
C                   INTERPOLATE FOR EAST POINT VALUES
      CALL FLDINT (U1,XLATC,EASTLN,UEAST,IERR)
      IF (IERR .NE. 0) GOTO 130
C
      CALL FLDINT (V1,XLATC,EASTLN,VEAST,IERR)
C
C                   INTERPOLATE FOR WEST POINT VALUES
      CALL FLDINT (U1,XLATC,WESTLN,UWEST,IERR)
      IF (IERR .NE. 0) GOTO 130
C
      CALL FLDINT (V1,XLATC,WESTLN,VWEST,IERR)
  130 CONTINUE
      IF (IERR .NE. 0) THEN
        PRINT*,'FBAM2,FORECAST TERMINATED BECAUSE EXTRACTION POINT IS',
     .        ' OFF THE GRID'
        IF (ITER .GE. 24) GOTO 200
C
        GOTO 290
C
      ENDIF
C
C                   OBTAIN AVERAGE STEERING FLOW
      VEB = 0.25*(UTOP +UEAST +UBOT +UWEST)
      VNB = 0.25*(VTOP +VEAST +VBOT +VWEST)
      VB  = SQRT (VEB*VEB +VNB*VNB)
      IF (ABS (VEB).LT.EPSLON .AND. ABS (VNB).LT.EPSLON) THEN
         ALPHA = 0.0
      ELSE
C                   THIS PROVIDES SAME BIAS AS THETAM
         ALPHA = ATAN2 (-VEB,VNB)
      ENDIF
      BETA = 7.292E-5*(2.0*COS (XLATC*DEGRAD)/(111137.0*RADDEG))
      VS   = C/(REFF**XI)
C
cx    IF (IPRNT.GT.10) WRITE (6,630) ITER,TOPLAT,EASTLN,BOTLAT,WESTLN,
      IF (IPRNT.GT.10) WRITE (7,630) ITER,TOPLAT,EASTLN,BOTLAT,WESTLN,
     .                     UTOP,VTOP,UEAST,VEAST,UBOT,VBOT,UWEST,VWEST,
     .                     VEB,VNB,ALPHA*RADDEG,VB
 630  FORMAT (' ',/,' ',' ***** LARGE-SCALE BAM PARAMETERS ',
     1 'AT ITER = ',I4,' *****',//
     1 ' ','N LAT (TLAT) = ',F5.1,' N',/
     1 ' ','E LONG  (EP) = ',F6.1,' W',/
     1 ' ','S LAT (BLAT) = ',F5.1,' N',/
     1 ' ','W LONG  (WP) = ',F6.1,' W',/
     1 ' ','N LARGE-SCALE U,V (UT,VT) = ',2(F6.2,1X),' M/SEC',/
     1 ' ','E LARGE-SCALE U,V (UE,VE) = ',2(F6.2,1X),' M/SEC',/
     1 ' ','S LARGE-SCALE U,V (UL,VL) = ',2(F6.2,1X),' M/SEC',/
     1 ' ','W LARGE-SCALE U,V (UW,VW) = ',2(F6.2,1X),' M/SEC',/
     1 ' ','TOTAL LS U,V (VEB,VNB)    = ',2(F6.2,1X),' M/SEC',/
     1 ' ','         LS ALPHA (ALPHA) = ',F6.1,' DEG',/
     1 ' ','      TOTAL LS SPEED (VB) = ',F6.2,' M/SEC',/)
C
      IF (IREFF .EQ. 0) THEN
C
C                   CALCULATE EFFECTIVE RADIUS, REFF, AND IN FLOW ANGLE,
C                   GAMMA, FROM CYCLONE MOTION AND AVERAGE LARGE-SCALE
C                   STEERING FLOW, THEN RETURN TO LABEL 125
C
         IREFF = -1
cx       WRITE (6,640)
         WRITE (7,640)
  640    FORMAT (' ',/,' ','MODIFY EFFECTIVE RADIUS ACCORDING TO',
     1           ' THE CURRENT MOTION',//)
C
C                   CALCULATE THE U (WESTWARD DIRECTION POSITIVE)
C                   AND V OF CYCLONE MOTION
         VOW = SPDM*SIN (THETAM)
         VON = SPDM*COS (THETAM)
C                   SAVE VALUES FOR COMPARISIONS
         VONOLD = VON
         VOWOLD = VOW
         SPDOLD = SPDM
         THETAO = THETAM
         REFOLD = REFF
C
C                   MODIFY THE U,V OF THE INITIAL CYCLONE MOTION
C                   ACCORDING TO THE AVERAGE LARGE-SCALE FLOW
C
C                   ENSURE CYCLONE V-COMPONENT IS BETWEEN LIMITS, M/S
         IF (VS .GT. 0.0) THEN
            VON = AMAX1 (VON,VNB -ABS (0.2*VNB))
            VON = AMIN1 (VON,(VNB +1.5))
         ELSE
            VON = AMAX1 (VON,VNB +ABS(0.2*VNB))
            VON = AMIN1 (VON,(VNB -1.5))
         ENDIF
C
C                   ENSURE CYCLONE U-COMPONENT IS BETWEEN LIMITS, M/S
         VOW = AMAX1 (VOW,-VEB -ABS (0.15*VEB))
         VOW = AMIN1 (VOW,(-VEB +2.0))
C
C                   RECALCULATE CYCLONE SPEED AND DIRECTION OF MOTION
         SPDM = SQRT (VOW*VOW +VON*VON)
         IF (SPDM .GT. 0.0001) THETAM = ATAN2 (VOW,VON)
C                   WHY IS REDEG MADE CORRECT AT THIS POINT?????
         REDEG = REFF/111137.0
C
C                   ON OUTPUT CHANGE SIGN OF U COMPONENT TO
C                   CONFORM TO CONVENTIONAL SENSE
cx       WRITE (6,641) REFOLD*0.001,-VOWOLD,VONOLD,SPDOLD,THETAO*RADDEG,
         WRITE (7,641) REFOLD*0.001,-VOWOLD,VONOLD,SPDOLD,THETAO*RADDEG,
     .                 -VOW,VON,SPDM,THETAM*RADDEG
  641    FORMAT (' ',/,' ','**** BEFORE RUNNING RADIUS: ',//
     .      ' ','          OLD REFF = ',F6.1,' KM',/
     .      ' ','OLD CYCLONE U COMP = ',F6.2,' M/SEC',/
     .      ' ','OLD CYCLONE V COMP = ',F6.2,' M/SEC',/
     .      ' ',' OLD CYCLONE SPEED = ',F6.2,' M/SEC',/
     .      ' ','OLD CYCLONE THETAM = ',F5.1,' DEG',/
     .      ' ','NEW CYCLONE U COMP = ',F6.2,' M/SEC',/
     .      ' ','NEW CYCLONE V COMP = ',F6.2,' M/SEC',/
     .      ' ',' NEW CYCLONE SPEED = ',F6.2,' M/SEC',/
     .      ' ','NEW CYCLONE THETAM = ',F5.1,' DEG',/)
C
C                   MODIFY THE REFF AND GAMMA TO BEST MATCH THE
C                   CYCLONE MODIFIED DIRECTION OF MOTION, THETAM
         CALL EFFRAD (THETAM)
C
cx       WRITE (6,642) REFF*0.001,SPDM,THETAM*RADDEG
         WRITE (7,642) REFF*0.001,SPDM,THETAM*RADDEG
  642    FORMAT (' ',/,' ','**** AFTER RUNNING RADIUS: ',//
     .      ' ','           REFF = ',F6.0,' KM',/
     .      ' ','  CYCLONE SPEED = ',F6.2,' M/SEC',/
     .      ' ',' CYCLONE THETAM = ',F5.1,' DEG',/)
C
C                   ENSURE NEW REFF BETWEEN 60 TO 500 KM
         REFF = AMAX1 (REFF,60000.0)
         REFF = AMIN1 (REFF,AMAX1 (RAD2,500.E3))
C
C*****       (A BUG??) REDEG FOR FINDING THE LS U,V MUST .GT. 400 KM
C*****       AND THE RADIUS OF 30 KT WINDS (THE V2,R2 PAIR)
C
         REDEG  = AMAX1 (REFF,RAD2,400.E3)/111137.0
C
cx       WRITE (6,643) REFF*0.001,THETAM*RADDEG
         WRITE (7,643) REFF*0.001,THETAM*RADDEG
  643    FORMAT (' ',/,' ','**** FINAL EFFECTIVE RADIUS VALUES: ',//
     .         ' ','           REFF = ',F6.0,' KM',/
     .         ' ',' CYCLONE THETAM = ',F5.1,' DEG',/)
C
C                   LOAD THETAF AND SPDF WITH FINAL VALUES OF
C                   THETAM AND SPDM
         THETAF = THETAM
         SPDF   = SPDM
C                   JUMP BACK TO RESTART TRACK FORECAST
         GOTO 125
C
      ENDIF
C
C                   STORE DATA IN ARRAYS FOR POST PROCESSING
      FTIME(ITER)  = IHR
      CLAT(ITER)   = XLATC
      CLON(ITER)   = XLONC
      CSPEED(ITER) = SPDF
      CTHETA(ITER) = 360.0 -THETAF*RADDEG
      ESPEED(ITER) = VB
      ETHETA(ITER) = 360.0 -ALPHA*RADDEG
      DSPEED(ITER) = SPDF -VB
      DTHETA(ITER) = ETHETA(ITER) -CTHETA(ITER)
      CTHETA(ITER) = AMOD (CTHETA(ITER),360.0)
      ETHETA(ITER) = AMOD (ETHETA(ITER),360.0)
C
C                   IF TRUE CALCULATIONS ARE OVER, SO JUMP
      IF (ITER .EQ. LSTITR) GOTO 200
C
      IF (ITER.EQ.0 .AND. IPRNT.GT.0)
C                   OUTPUT FINAL CYCLONE PARAMETERS BEFORE THE FORECAST
cx   .   WRITE (6,650) GAMMA,ATAN(GAMMA)*RADDEG,C,REFF*0.001,
     .   WRITE (7,650) GAMMA,ATAN(GAMMA)*RADDEG,C,REFF*0.001,
     .                 XI,VS,VRAD2,RAD2*0.001
  650    FORMAT (' ',/,' ',' ***** FINAL BAM CYCLONE PARAMETERS ',//
     .    ' ','TAN(INFLOW ANGLE) (GAMMA) = ',F5.3,/
     .    ' ','             INFLOW ANGLE = ',F5.1,' DEG',/
     .    ' ','             STRENGTH (C) = ',E13.5,/
     .    ' ','  EFFECTIVE RADIUS (REFF) = ',F6.1,' KM',/
     .    ' ','               SHAPE (XI) = ',F5.3,/
     .    ' ','   CYCLONE V AT REFF (VS) = ',F6.2,' M/SEC',/
     .    ' ','       CYCLONE V2,R2 PAIR = ',F6.2,1X,F5.1,/)
C
C   ***** MAKE THE BAM FORECAST OF CYCLONE MOTION (THETAM,SPEED) *****
C
      CALL STHETA (THETAF,SPDF)
C
C                   INCREMENT TIME AND ITERATION COUNTERS
      IHR  = IHR +1
      ITER = ITER +1
C
cx    IF (IPRNT .GT. 5) WRITE (6,680) ITER,THETAF*RADDEG,SPDF,XLATC,
      IF (IPRNT .GT. 5) WRITE (7,680) ITER,THETAF*RADDEG,SPDF,XLATC,
     .                        XLONC
  680    FORMAT (' ',/,' ','***** BAM MOTION DIR/SPEED FORECAST:',//
     .    ' ','   FORECAST ITERATION = ',I4,/
     .    ' ','                THETA = ',F6.1,' DEG',/
     .    ' ','                SPEED = ',F8.2,' M/SEC',/
     .    ' ','LAT,LON (XLATC,XLONC) = ',2F8.2,/)
C
      IF (ITER.LT.IBLNDH .AND. BLEND) THEN
C                   BLEND THE FBAM PREDICTED MOTION WITH THE INITIAL
C                   CYCLONE MOTION USING A COSINE WEIGHTING FUNCTION
         UCFBAM = SPDF*SIN (THETAF)
         VCFBAM = SPDF*COS (THETAF)
         UCOBS  = SPDI*SIN (THETAI)
         VCOBS  = SPDI*COS (THETAI)
         BFAC   = COS ((HPI/BLNDHR)*IHR)
         BFAC1  = 1.0 -BFAC
         UC0    = BFAC1*UCFBAM +BFAC*UCOBS
         VC0    = BFAC1*VCFBAM +BFAC*VCOBS
         SPDF   = SQRT (UC0*UC0 +VC0*VC0)
         IF (SPDF .GT. 0.0001) THETAF = ATAN2 (UC0,VC0)
      ENDIF
C
      IF (IPRNT.GT.5) THEN
         IF (XLONC .GT. 180.0) THEN
            PLONC  = 360.0 -XLONC
            CHEMEW = 'E'
         ELSE
            PLONC  = XLONC
            CHEMEW = 'W'
         ENDIF
         PLATC = XLATC
         IF (XLATC .GE. 0.0) THEN
            CHEMNS = 'N'
         ELSE
            CHEMNS = 'S'
         ENDIF
C
cx       WRITE (6,660) ITER,PLATC,CHEMNS,PLONC,CHEMEW,
         WRITE (7,660) ITER,PLATC,CHEMNS,PLONC,CHEMEW,
     1                          VEB,VNB,VB,ALPHA*RADDEG,BETA,
     2                          THETAF*RADDEG,SPDF
  660    FORMAT (' ',/,' ',' ***** BAM FORECAST PARAMETERS ',
     1    'AT ITER = ',I4,' *****',//
     1    ' ','      CYCLONE LAT (XLATC) = ',F5.1,1X,A1,/
     1    ' ','     CYCLONE LONG (XLONC) = ',F5.1,1X,A1,/
     1    ' ',' LARGE-SCALE U COMP (VEB) = ',F6.2,' M/SEC',/
     1    ' ',' LARGE-SCALE V COMP (VNB) = ',F6.2,' M/SEC',/
     1    ' ','   LARGE-SCALE SPEED (VB) = ',F6.2,' M/SEC',/
     1    ' ','LARGE-SCALE ALPHA (ALPHA) = ',F5.1,' DEG',/
     1    ' ','                   (BETA) = ',E13.5,/
     1    ' ','     CYCLONE DIR (THETAM) = ',F5.1,' DEG'/
     1    ' ','    CYCLONE SPEED (SPEED) = ',F6.2,' M/SEC'/)
C
         IF (MOD (ITER,12) .EQ. 0) THEN
            CRSLS = 360.0 -ALPHA*RADDEG
            IF (CRSLS .GT. 360.0) CRSLS = CRSLS -360.0
            CRSCYC = 360.0 -THETAF*RADDEG
            IF (CRSCYC .GT. 360.0) CRSCYC = CRSCYC -360.0
            SPDLS  = VB*RMS2KT
            SPDCYC = SPDF*RMS2KT
cx          WRITE (6,670) ITER,AIDNAM,PLATC,CHEMNS,
cx          WRITE (7,670) ITER,AIDNAM,PLATC,CHEMNS,
cx   .                        PLONC,CHEMEW,CRSCYC,SPDCYC,CRSLS,SPDLS
  670       FORMAT (1X,'ITER = ',I2,1X,A4,' : ',F4.1,A1,1X,F5.1,A1,
     .    '  TC MOTN: ',F5.1,1X,F5.1,' KTS;  LS FLOW: ',
     .       F5.1,1X,F5.1,' KTS')
         ENDIF
      ENDIF
C
C   ***** MAKE THE BAM FORECAST OF LATITUDE AND LONGITUDE *****
C
C                   EXTRAPOLATE FOR FORECAST POSITION USING
C                   RHUMB LINE CALCULATION
      XLONC =XLONC +SPDF*3600.0*SIN(THETAF)/(111137.0*COS(XLATC*DEGRAD))
      XLATC =XLATC +SPDF*3600.0*COS(THETAF)/111137.0
C
C                   CHECK ON STOPPING THE FORECAST
      IF (ITER .LE. LSTITR) THEN
C
C                   UPDATE THE WIND FIELDS IN TIME
         CALL LSFCST (UTEND,VTEND,U1,V1)
         IF (MOD (IHR,IDTFLD).NE.0 .OR. ITER.EQ.LSTITR) THEN
C                   CONTINUE WITH UPDATED FIELDS
C                   NOTE: IF ITER .EQ. LSTITR FORECASTS ARE OVER, BUT
C                         GET DATA FOR DIAGNOSTICS, A JUMP TO 200
C                         WILL BE TAKEN ABOVE
            GOTO 125
C
         ELSE
C                   CONTINUE WITH NEW FIELDS
            GOTO 115
C
         ENDIF
      ENDIF
C
C           ***** ALL DONE:  OUTPUT THE FORECAST *****
C
  200 CONTINUE
      IF (IPRNT .GT. 0) THEN
C                   WRITE HIGH LEVEL DIAGNOSTICS
         WRITE (*,690)
         DO 210 I=0, ITER
            WRITE (*,691) I,FTIME(I),CLAT(I),CLON(I),CSPEED(I),CTHETA(I)
     .                    ,ESPEED(I),ETHETA(I),DSPEED(I),DTHETA(I)
  210    CONTINUE
      ENDIF
  690 FORMAT (//,1X,'**** HOUR BY HOUR CYCLONE AND LARGE-SALE INFORMATIO
     .N ****')
  691 FORMAT (I3,1X,F5.1,1X,F5.1,1X,F6.1,1X,F5.2,1X,F7.2,
     .           3X,F5.2,1X,F7.2,3X,F6.2,1X,F7.2)
C
      WRITE (*,991) AIDNAM(J),STRMID,DTGFIX,AIDNAM(J),AIDNAM(J)
  991 FORMAT (//,1X,
     2   '     FNOC VERSION OF THE BAM MODEL (',A,') FORECAST',//,
     3   '   STORM ID = ',A,'  DTG = ',A,'  ADECK NAME = ',A,//,
     4   '    TIME     ',A,' FORECAST    CYCLONE    LARGE-SCALE',/,
     5   '   (HOUR)      (LAT,LON)      MOTION        FLOW'/,
     6   '                             (DEG,KTS)    (DEG,KTS)'/)
C
      DO 220 I=0, ITER, 6
         IF (CLAT(I) .NE. 0.0) THEN
            HEMNS0 = 'N'
            HEMEW0 = 'W'
            RLONOT = CLON(I)
            RLATOT = CLAT(I)
            IF (I .NE. 0) THEN
               CYCDIR = CTHETA(I)
               CYCSPD = CSPEED(I)*RMS2KT
            ELSE
               CYCDIR = CRSIN
               CYCSPD = SPDIN
            ENDIF
            RLSDIR = ETHETA(I)
            RLSSPD = ESPEED(I)*RMS2KT
C
            IF (CLAT(I) .LT. 0.0) THEN
               RLATOT = ABS (RLATOT)
               HEMNS0  = 'S'
            ENDIF
C
            IF (CLON(I) .GT. 180.0) THEN
               RLONOT = 360 -RLONOT
               HEMEW0  = 'E'
            ENDIF
C
            WRITE (*,693) IFIX(FTIME(I)),RLATOT,HEMNS0,RLONOT,HEMEW0,
     .                    CYCDIR,CYCSPD,RLSDIR,RLSSPD
      ENDIF
  220 CONTINUE
  693 FORMAT (4X,I2,6X,F4.1,A1,2X,F5.1,A1,
     1        3X,F5.1,1X,F4.1,3X,F5.1,1X,F4.1)
C
C                   WRITE OUT A FILE FOR ARQ USER
C
cx    IF (J .EQ. 1) OPEN (UNIT=IOFCST,IOSTAT=IOE,ERR=740,
cx   .       STATUS='UNKNOWN',ACCESS='SEQUENTIAL',FORM='FORMATTED')
c
c  open the ccrs output file
c
      filename=storms(1:ind)//'/wptot.dat'
cx    print *, filename
      call openfile (iofcst,filename,'unknown',ioerror)
      if (ioerror .lt. 0) go to 740
c
c  go to end of output file
c
  240 continue
      read(iofcst,'(a1)',end=250)cdummy
      go to 240
  250 continue
C
      do ii=1, 5
         jj = ii * 12
         if( jj .eq. 60 ) jj = 72
         ltlnwnd(ii,1) = nint(clat(jj)*10.0)
         ltlnwnd(ii,2) = nint(clon(jj)*10.0)
         ltlnwnd(ii,3) = 0
      enddo
      call writeAid( iofcst, stormid, cent, dtgfix, aidnam(j), 
     1              ltlnwnd )
  290 CONTINUE
C
      STOP 'FBAM2: NORMAL FINISH'
C
C                   ******    ERRORS     ******
C
  700 CONTINUE
      PRINT *, 'FBAM2, OPEN ERROR ON IOFBAM TAPE44 IS ',IOE
      GOTO 777
C
  705 CONTINUE
      PRINT *, 'FBAM2, READ  ERROR ON IOFBAM TAPE44 IS ',IOE
      GOTO 777
C
  707 CONTINUE
      PRINT *, 'FBAM2, EARLY EOF ON IOFBAM TAPE44'
      GOTO 777
C
  710 CONTINUE
      PRINT *, 'FBAM2, GRID FROM FBAM2 TOO LARGE'
      GOTO 777
C
  720 CONTINUE
      PRINT *, 'FBAM2, NO LARGE-SCALE WIND FIELDS FROM TAPE33'
      GOTO 777
C
  740 CONTINUE
cx    PRINT *, 'FBAM2, OPEN ERROR ON IOFCST TAPE19 IS ',IOE
      print *, 'fbam2, open error on ',filename
C
  777 CONTINUE
      PRINT *, 'FBAM2, ABORTING'
cx    CALL REMARK ('  FBAM2 ABORTING ')
cx    CALL SYSTEM (0)
cx    CALL ABORT
      close (44)
      close (7)
      close (iofcst)
      stop 'FBAM2:  ABORTED RUN'
C
      END
      SUBROUTINE RDLSUV (RFLD,IOFLD,IERR)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  RDLSUV
C
C  DESCRIPTION:      READ LARGE-SCALE WIND FIELDS WRITTEN BY FBAM1
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:          
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL RDLSUV (RFLD,IERR)
C
C  INPUT PARAMETERS:
C        RFLD - FWA OF DATA ARRAY
C       IOFLD - UNIT AND TAPE NUMBER OF INPUT FIELDS
C
C  OUTPUT PARAMETERS:
C         IERR - ERROR FLAG, ZERO NO ERROR, -1 OPEN OR READ FILE ERROR
C
C  INPUT FILE:                   TAPE31 - SHALLOW REGIONAL FIELDS
C                                TAPE32 - MEDIUM REGIONAL FIELDS
C                                TAPE33 - DEEP REGIONAL FIELDS
C
C  OUTPUT FILE:                  NONE
C
C  COMMON BLOCK:
C           MBYN   - LENGTH OF REGIONAL GRID (RFLD)    /GRID/
C
C  ERROR CONDITIONS:
C        OPEN FILE OR READ FILE ERRORS, SEE 7XX LABELS BELOW
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C      INIL  - OPEN FILE WHEN ZERO, DATA STATEMENT
C      IOFLD - UNIT AND TAPE NUMBER OF INPUT DATA FILE, DATA STATEMENT
C      NEND  - READ, NO READ FLAG - READ WHEN NEND IS 1, DATA STATEMENT
C      NREC  - NUMBER OF RECORD TO READ FROM TAPE33, DATA STATEMENT
C
C  METHOD:               NOT APPLICABLE
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  RDLSUV*01  (14 AUG 91) -- HAMILTON,H.
C           PROVIDE FOR PROCESSING SHALLOW AND MEDIUM LAYER FIELDS
C           IN ADDITION TO ORIGINAL DEEP LAYER MEANS - JTWC REQUEST
C
C........................END PROPLOGUE..................................
C
      DIMENSION RFLD(MBYN)
C
      COMMON/GRID/ MGRD,NGRD,MBYN,ISBIG,JSBIG,IDTFLD
C
      SAVE LIOFLD,NEND,NREC
      DATA LIOFLD/-1/, NEND/1/, NREC/0/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C

      IF (IOFLD .NE. LIOFLD) THEN
         LIOFLD = IOFLD
         NEND   = 1
cx  field data actually starts with second record ... bs 9/8/95
cx       NREC   = 0
         NREC   = 1
cx       OPEN (IOFLD,IOSTAT=IOS,ERR=700,ACCESS='DIRECT',RECL=MBYN)
      ENDIF
C
      IF (NEND .EQ. 1) THEN
         NREC = NREC +1
         READ (IOFLD,IOSTAT=IOS,ERR=710,REC=NREC) RFLD
         IERR = 0
      ELSE
         IERR = -1
      ENDIF
  100 CONTINUE
      RETURN
C
  700 CONTINUE
      PRINT *, ' $$$ RDLSUV, OPEN ERROR ',IOS,' ON TAPE',IOFLD
      GOTO 770
C
  710 CONTINUE
      PRINT *, ' $$$ RDLSUV, READ ERROR ',IOS,' ON TAPE',IOFLD
      NEND = 0
C
  770 CONTINUE
      IERR = -1
      GOTO 100
C
      END
      SUBROUTINE LSTEND (U1,V1,U2,V2,UTEND,VTEND)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  LSTEND
C
C  DESCRIPTION:      CALCULATE THE LARGE-SCALE WIND COMPONENT TENDENCY
C                    PER TIME STEP IN THE MODEL, FOR UPDATING OF FIELDS
C                    BY LSFCST
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:          
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL LSTEND (U1,V1,U2,V2,UTEND,VTEND)
C
C  INPUT PARAMETERS:
C    U1    - U-WIND COMPONENT AT TIME 1
C    V1    - V-WIND COMPONENT AT TIME 1
C    U2    - U-WIND COMPONENT AT TIME 2
C    V2    - V-WIND COMPONENT AT TIME 2
C
C  OUTPUT PARAMETERS:
C    UTEND - CHANGE OF U (M/S) PER TIME STEP (ONE-HOUR) OF MODEL
C    VTEND - CHANGE OF V (M/S) PER TIME STEP (ONE-HOUR) OF MODEL
C
C  INPUT FILE:                   NONE
C
C  OUTPUT FILE:                  NONE
C
C  COMMON BLOCK:
C    IDTFLD - TIME DIFFERENCE IN HOURS BETWEEN REGIONAL FIELDS  /GRID/
C    MBYN   - LENGTH OF REGIONAL GRIDS (U1,U2,V1,V2)             /GRID/
C
C  ERROR CONDITIONS:             NONE
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:
C      DTFAC  - TIME DIFFERENCE FACTOR FOR CALCULATION OF TENDENCY
C
C  METHOD:               LINEAR RATE OF CHANGE
C
C  ADDITIONAL COMMEMT:
C           IF TIME STEP OF MODEL IS CHANGED FROM ONE HOUR, ADJUST
C           DTFAC FOR CALCULATION OF UTEND AND VTEND.
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      DIMENSION U1(MBYN), V1(MBYN), U2(MBYN), V2(MBYN)
      DIMENSION UTEND(MBYN), VTEND(MBYN)
C
      COMMON/GRID/ MGRD,NGRD,MBYN,ISBIG,JSBIG,IDTFLD
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      DTFAC = 1.0/FLOAT (IDTFLD)
      DO 110 N=1, MBYN
         UTEND(N) = DTFAC*(U2(N) -U1(N))
         VTEND(N) = DTFAC*(V2(N) -V1(N))
  110 CONTINUE
      RETURN
C
      END
      SUBROUTINE LSFCST (UTEND,VTEND,U1,V1)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  LSFCST
C
C  DESCRIPTION:      UPDATE THE LARGE-SCALE WIND FORECAST IN TIME
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:          
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL LSFCST (UTEND,VTEND,U1,V1)
C
C  INPUT PARAMETERS:
C    UTEND - CHANGE OF U (M/S) PER TIME STEP (ONE-HOUR) OF MODEL
C    U1    - LARGE SCALE U-COMPONENT, INITIAL
C    VTEND - CHANGE OF V (M/S) PER TIME STEP (ONE-HOUR) OF MODEL
C    V1    - LARGE SCALE V-COMPONENT, INITIAL
C
C  OUTPUT PARAMETERS:
C    U1 - LARGE SCALE U-COMPONENT, UPDATED
C    V1 - LARGE SCALE V-COMPONENT, UPDATED
C
C  INPUT FILE:                   NONE
C
C  OUTPUT FILE:                  NONE
C
C  COMMON BLOCK:
C    MBYN   - LENGTH OF REGIONAL GRIDS (U1,U2,V1,V2)             /GRID/
C
C  ERROR CONDITIONS:             NONE
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:  NO OTHER
C
C  METHOD:               ADD CHANGE/TIME-STEP-OF-MODEL
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      DIMENSION UTEND(MBYN),VTEND(MBYN),U1(MBYN),V1(MBYN)
C
      COMMON/GRID/ MGRD,NGRD,MBYN,ISBIG,JSBIG,IDTFLD
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C                   "FORECAST" THE LARGE-SCALE FLOW
C
      DO 110 N=1, MBYN
         U1(N) = U1(N) +UTEND(N)
         V1(N) = V1(N) +VTEND(N)
  110 CONTINUE
      RETURN
C
      END
      SUBROUTINE EFFRAD (THETAM)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  EFFRAD
C
C  DESCRIPTION:      FIND THE EFFECTIVE RADIUS (REFF) AND INFLOW ANGLE
C                    (GAMMA) WHICH GENERATES A BAM MOTION VECTOR
C                    PREDICTION THAT IS CLOSEST TO THE AVERAGE
C                    LARGE-SCALE FLOW
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:         
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL EFFRAD (THETAM)
C
C  INPUT PARAMETERS:
C    THETAM - BIASED DIRECTION OF CYCLONE MOTION, RADIANS
C
C  OUTPUT PARAMETERS:
C    REFF  - EFFECTIVE RADIUS OF CYCLONE, M                     /OBSV/
C    GAMMA - INFLOW ANGLE AT EFFECTIVE RADIUS, RADIANS          /OBSV/
C
C  INPUT FILE:                   NONE
C
C  OUTPUT FILE:                  NONE
C
C  COMMON BLOCK:
C     COMMON /CONST/:
C           HPI    - RADIANS IN  90 DEGREES
C           PI     - RADIANS IN 180 DEGREES
C           TPI    - RADIANS IN 360 DEGREES
C           RADDEG - RADIAN TO DEGREE CONVERSION FACTOR
C
C     COMMON /OBSV/:
C           BETA   - RELATED TO CORIOLIS PARAMETER
C           C      - VORTEX STRENGTH FACTOR
C           GAMMA  - INFLOW ANGLE AT EFFECTIVE RADIUS, RADIANS
C           REFF   - EFFECTIVE RADIUS OF CYCLONE, M
C           SPDM   - SPEED OF MOTION OF CYCLONE, M/S
C           VEB    - AVERAGE EAST-WEST COMPONENT OF LS FLOW, M/S
C           VNB    - AVERAGE NORTH-SOUTH COMPONENT OF LS FLOW, M/S
C           VS     - TANGENTIAL SPEED OF CYCLONE AT REFF, M/S
C           XI     - VORTEX SHAPE PARAMETER
C
C     COMMON /PRNT/
C           IPRNT  - PRINT FLAG, THE HIGHER THE NUMBER THE MORE
C                    DIAGNOSTICS ARE PRINTED
C
C
C  ERROR CONDITIONS:             NONE
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:  NO OTHER
C
C  METHOD:               ITERATION
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      COMMON/CONST/ HPI,PI,TPI,DEGRAD,RADDEG,RMS2KT,RKT2MS
      COMMON/OBSV/ BETA,GAMMA,REFF,REDEG,VS,C,XI,ALPHA,VB,VEB,VNB,
     .             SPDM,XLATC
      COMMON/PRNT/ IPRNT
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C                   BASE FIRST GUESS VALUE OF REFF ON BETA
      REFF = SQRT (1.2/BETA)
      VX   = ABS (C/SQRT (REFF))
C                   CALCULATE EAST-WEST FACTOR OF MOTION
      IF (VEB .GT. 0.0) THEN
         FACTW = 0.75*VX/(0.75*VX -1.0)
      ELSE
         FACTW = 0.75*VX/(0.75*VX +1.0)
      ENDIF
C                   CALCULATE NORTH-SOUTH FACTOR OF MOTION
      FACTN = 1.0 -2.0/(VX*PI)
C                   CALCULATE THE DIFFERENCE BETWEEN LARGE-SCALE FLOW
C                   AND INITIAL WEIGHTED VALUES OF CYCLONE SPEED
      DVW = SPDM*SIN (THETAM)/FACTW +VEB
      DVN = SPDM*COS (THETAM)/FACTN -VNB
C
C                   INITIAL GAMMA IS RELATED TO THE DIFFERENCE
C                   BETWEEN THE LS FLOW AND CYCLONE MOTION
      IF (DVW.NE.0.0 .OR. DVN.NE.0.0) THEN
         GAMMA = 0.6285 -ATAN2 (DVW,DVN)
      ELSE
         GAMMA = 0.0
      ENDIF
      IF (C.LT.0.0 .AND. (DVW.NE.0.0.AND.DVN.NE.0.0)) THEN
C                   MODIFY FIRST GUESS GAMMA FOR SHEM
         DVN   = -DVN
         GAMMA = ATAN2 (DVW,DVN) +TPI
      ENDIF
C
C                   PERFORM BOUNDS CHECK ON FIRST GUESS GAMMA
      IF (GAMMA .GT. PI) THEN
         GAMMA = TPI -GAMMA
      ELSEIF (GAMMA .LT. -PI) THEN
         GAMMA = TPI +GAMMA
      ELSEIF (GAMMA .GT. HPI) THEN
         GAMMA =  0.1
      ELSEIF (GAMMA .LT. -HPI) THEN
         GAMMA = -0.1
      ENDIF
      GAMMA = AMIN1 (GAMMA,+0.5)
      GAMMA = AMAX1 (GAMMA,-0.5)
      IF (VS .GT. 0.0) THEN
C                   FOR NHEM CYCLONES, GAMMA MUST BE GREATER THAN -0.3
         GAMMA = AMAX1 (GAMMA,-0.3)
      ELSEIF (VS .LT. 0.0) THEN
C                   FOR SHEM CYCLONES, GAMMA MUST BE LESS THAN 0.3
         GAMMA = AMIN1 (GAMMA,0.3)
      ENDIF
C
C                   ADJUST REFF BASED ON BETA AND DEVIATION
C                   OF CYCLONE DIR/SPD FROM LS (X1,X2)
      DVW   = AMAX1 (DVW,0.0)
      DVN   = AMAX1 (DVN,0.0)
      REFF = SQRT (SQRT (DVW*DVW +DVN*DVN)/(BETA*0.63662))
C
C                   FIRST GUESS OF REFF MUST BE BETWEEN 110 AND 350 KM
      REFF = AMAX1 (REFF,110000.0)
      REFF = AMIN1 (REFF,350000.0)
C
      DELR   = 50000.0
      REFSTP = 5.0
C
cx    IF (IPRNT.GT.5) WRITE (6,610) DELR*0.001,REFSTP
      IF (IPRNT.GT.5) WRITE (7,610) DELR*0.001,REFSTP
  610 FORMAT(' ',/,' ','***** STARTING REFF ITERATION ******',//
     1   ' ','DELR    = ',F5.1,' KM'/
     2   ' ','REFSTP  = ',F4.1,/)
C
      DO 120 KR=1, 4
         RX     = 1.0E10
         GF     = GAMMA
         DELR   = DELR/REFSTP
         REFF   = REFF -REFSTP*DELR
C                   MINIMUM REFF IS 60 KM
         REFF   = AMAX1 (REFF,60000.0)
         RF     = REFF
         THETA1 = THETAM
         DO 110 I=1, 11
C                   REVISE CYCLONE TANGENTIAL FLOW AT REFF
            VS = C/(REFF**XI)
C                CALCULATE NEW THETA (THETA1) AND SPEED (SPD1) OF MOTION
            CALL STHETA (THETA1,SPD1)
            TH1 = THETAM -THETA1
            R1  = (SPD1*SIN (TH1))**2 +(SPDM -SPD1*COS (TH1))**2
C
cx          IF (IPRNT.GT.5) WRITE (6,620) KR,I,REFF*0.001,GAMMA,
            IF (IPRNT.GT.5) WRITE (7,620) KR,I,REFF*0.001,GAMMA,
     .                      THETA1*RADDEG,SPD1,TH1*RADDEG,R1
C
            IF (R1 .LT. RX) THEN
C                   FIND THE REFF THAT MINIMIZES THE DIFFERENCE BETWEEN
C                   THE BAM DIR/SPD OF CYCLONE MOTION AND THE INITIAL
C                   OBSERVED CYCLONE DIR/SPD
               RX = R1
               RF = REFF
               GF = GAMMA
            ENDIF
C
            REFF = REFF +DELR
  110    CONTINUE
         REFF  = RF
C                   REVISE CYCLONE TANGENTIAL FLOW AT REFF
         VS = C/(REFF**XI)
C
C                   NOW FINE TUNE GAMMA WITH TWO VALUES
C                   SMALLER AND LARGER THAN ABOVE GAMMA (GF)
         GF1   = 0.75*GF
         GAMMA = GF1
         CALL STHETA (THETA1,SPD1)
         TH1 = THETAM -THETA1
         R1  = (SPD1*SIN(TH1))**2 +(SPDM -SPD1*COS (TH1))**2
C
         GF2   = 1.25*GF
         GAMMA = GF2
         CALL STHETA (THETA1,SPD1)
         TH1 = THETAM -THETA1
         R2  = (SPD1*SIN(TH1))**2 +(SPDM -SPD1*COS (TH1))**2
C
C                   SELECT THE GAMMA WHICH MINIMIZES THE DIFFERENCE
C                   BETWEEN BAM FORECAST AND CYCLONE DIR/SPD
         GAMMA = GF
         IF (R1 .LT. RX) GAMMA = GF1
         IF ((R2.LT.RX) .AND. (R2.LT.R1)) GAMMA = GF2
C
C                   PERFORM FINAL BOUNDS CHECK ON GAMMA
         GAMMA = AMIN1 (GAMMA,+0.5)
         GAMMA = AMAX1 (GAMMA,-0.5)
         IF (VS .GE. 0.0) THEN
C                   FOR NHEM CYCLONES, GAMMA MUST BE GREATER THAN -0.3
            GAMMA = AMAX1 (GAMMA,-0.3)
         ELSE
C                   FOR SHEM CYCLONES, GAMMA MUST BE LESS THAN 0.3
            GAMMA = AMIN1 (GAMMA,0.3)
         ENDIF
C
  120 CONTINUE
      RETURN
C
  620 FORMAT(' ','REFF ITER = ',I3,' REFF STEP = ',I3,/
     1     ' ','REFF = ',F5.1,' KM  GAMMA = ',F5.2,/
     2     ' ','THETA1 = ',F6.1,' DEG SPD1 = ',F5.2,' M/SEC'/
     2     ' ','DEL THETA = ',F7.2,' DEG  DEL SPD = ',F5.2,' M/SEC'/)
C
      END
      SUBROUTINE STHETA (TACT,SPEED)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  STHETA
C
C  DESCRIPTION:      MAKE THE BAM FORECAST OF TROPICAL CYCLONE MOTION
C                    IN TERMS OF DIRECTION (TACT) AND SPEED.
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:          
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL STHETA (TACT,SPEED)
C
C  INPUT PARAMETERS:
C    TACT   - BIASED DIRECTION OF CYCLONE MOTION, RADIANS
C
C  OUTPUT PARAMETERS:
C    TACT   - BIASED DIRECTION OF CYCLONE MOTION, RADIANS
C    SPEED  - SPEED OF MOTION OF CYCLONE, M/S
C
C  INPUT FILE:                   NONE
C
C  OUTPUT FILE:                  NONE
C
C  COMMON BLOCK:
C     COMMON /CONST/:
C           DEGRAD - DEGREE TO RADIAN CONVERSION FACTOR
C           PI     - RADIANS IN 180 DEGREES
C           TPI    - RADIANS IN 360 DEGREES
C           RADDEG - RADIAN TO DEGREE CONVERSION FACTOR
C
C     COMMON /OBSV/:
C           ALPHA  - BIASED DIRECTION OF LARGE SCALE FLOW, RADIANS
C           BETA   - RELATED TO CORIOLIS PARAMETER
C           GAMMA  - INFLOW ANGLE AT EFFECTIVE RADIUS, RADIANS
C           REFF   - EFFECTIVE RADIUS OF CYCLONE, M
C           VB     - AVERAGE WIND SPEED OF LARGE-SCALE FLOW, M/S
C           VS     - TANGENTIAL SPEED OF CYCLONE AT REFF, M/S
C           XI     - VORTEX SHAPE PARAMETER
C           XLATC  - LATITUDE OF CYCLONE
C
C  ERROR CONDITIONS:             NONE
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:  NO OTHER
C
C  METHOD:               SEARCH FOR MAXIMUM RATE OF CHANGE OF VORTICITY
C                        ADJUST BASED UPON BETA DRIFT
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  STHETA*01  (06 NOV 1989)  HAMILTON, H.
C                     CORRECT SEARCH FOR MAXIMUM RATE OF CHANGE OF
C                     VORTICITY (ERROR CARRIED OVER FROM JBAM)
C
C  <<CHANGE NOTICE>>  STHETA*02  (12 FEB 1992)  --  HAMILTON,H.
C                     CORRECT INTERMITTENT ATAN2 PROBLEM
C
C
C........................END PROPLOGUE..................................
C
      COMMON/CONST/ HPI,PI,TPI,DEGRAD,RADDEG,RMS2KT,RKT2MS
      COMMON/OBSV/ BETA,GAMMA,REFF,REDEG,VS,C,XI,ALPHA,VB,VEB,VNB,
     .             SPDM,XLATC
C
C                   SET MINIMUM SEARCH ANGLE, IN RADIANS
      DATA DRNGMN/0.523598776/
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C                   DRIFT VALUES
      GANGLE = ATAN (GAMMA)
      UDRFT  = BETA*REFF*REFF
C
C                   FUNCTIONS OF LAT
      XLATR  = ABS (XLATC*DEGRAD)
      WNRTH2 = 0.06/TAN (XLATR)
      WWEST2 = WNRTH2*1.414
C
C                   FUNCTIONS OF REFF
      AFACT1 = UDRFT/((1.0 -XI*XI)*VS)
      WNRTH1 = UDRFT*0.4627
      WWEST1 = UDRFT*0.6366
      DZSDR  = VS*(1.0 -XI*XI)/(REFF*REFF)
C
C                   INITIALIZE MAX RATE OF CHANGE IN VORTICITY (DV/DT)
      DVDTX = 0.0
C
C                   SET ANGLUAR RANGE FOR MAX DVDT SEARCH
      DRMN = AMIN1 (TACT,ALPHA)
      DRMX = AMAX1 (TACT,ALPHA)
      DRDF = DRMX -DRMN
      IF (DRDF .GT. PI) THEN
C               360 DEGREES (TWO PI RADIANS) IS BETWEEN TACT AND ALPHA
         DRMN = DRMN +TPI
         DRDF = DRMN -DRMX
      ENDIF
      RADRNG = AMIN1 (TPI,AMAX1 (2.0*DRDF,DRNGMN))
      T1     = 0.5*(DRMN +DRMX) -0.5*RADRNG -DEGRAD
      IEND   = ANINT (RADRNG*RADDEG)
C
C                   SEARCH FOR MAX DVDT
      DO 110 I=1, IEND
         T1  = T1 +DEGRAD
         CT1 = COS (T1)
         ST1 = SIN (T1)
         ST  = SIN (T1 +GANGLE)
         CT  = COS (T1 +GANGLE)
         IF (VS .LT. 0.0) THEN
C                   SOUTHERN HEMSPHERE, REVERSE THE SIGN OF CT1 AND CT
            CT1 = -CT1
            CT  = -CT
         ENDIF
C
C                 WNORTH = UDRFT*0.4627*CT +0.06*CT1*COTAN (XLATR)
C                 WWEST  = UDRFT*0.6366*ST +0.06*1.414*ST1*COTAN (XLATR)
         WNORTH = WNRTH1*CT +WNRTH2*CT1
         WWEST  = WWEST1*ST +WWEST2*ST1
         DZDT   = (VB*COS (T1 -ALPHA) +WNORTH +WWEST)*DZSDR
C
C                   MAX(MIN) DVDT TEST
         IF (VS.LT.0 .AND. DZDT.LT.DVDTX) THEN
C                   SOUTHERN HEMISPHERE
            DVDTX = DZDT
            TF    = T1
            SF    = ST
            CF    = CT1
         ELSEIF (VS.GT.0.0 .AND. DZDT.GT.DVDTX) THEN
C                   NORTHERN HEMISPHERE
            DVDTX = DZDT
            TF    = T1
            SF    = ST
            CF    = CT1
         ENDIF
  110 CONTINUE
C
C                   CALCULATE SPEED AND DIRECTION
      IF (VS .GT. 0.0) THEN
C                   NORTHERN HEMISPHERE
         SPEED = DVDTX/(DZSDR +BETA*SF*1.27)
      ELSE
C                   SOUTHERN HEMISPHERE
         SPEED = DVDTX/(DZSDR -BETA*SF*1.27)
      ENDIF
C                   CALCULATE NORTHWARD AND WESTWARD COMPONENTS OF
C                   BETA DRIFT AND ADVECTION
      VFN   = SPEED*CF
      AFACT = AFACT1*(VFN/VS)
      VCN   = VFN*(1.0/(1.0 +ABS (AFACT)))
      VCW   = SPEED*SIN (TF) +AFACT*VCN
      SPEED = SQRT (VCW*VCW +VCN*VCN)
      IF (VS .LT. 0.0) VCN = -VCN
      IF (SPEED .GT. 0.0001) THEN
         TACT = ATAN2 (VCW,VCN)
      ELSE
         TACT  = 0.0
         SPEED = 0.0
      ENDIF
      RETURN
C
      END
      SUBROUTINE FLDINT (FLD,RLAT,RLON,FVAL,IERR)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  FLDINT
C
C  DESCRIPTION:      INTERPOLATE FOR FIELD VALUE LOCATED AT RLAT,RLON
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:          
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL FLDINT (FLD,RLAT,RLON,FVAL,IERR)
C
C  INPUT PARAMETERS:
C    FLD    - FWA OF FIELD VALUES
C    RLAT   - LATITUDE OF POINT, +N, -S
C    RLON   - LONGITUDE OF POINT, ALL WEST LONGITUDE (360.0 DEGREES)
C
C  OUTPUT PARAMETERS:
C    FVAL   - INTERPOLATED FIELD VALUE AT RLAT,RLON
C    IERR   - ERROR FLAG, ZERO GOOD VALUE, -1 POINT IS OFF GRID
C
C  INPUT FILE:                   NONE
C
C  OUTPUT FILE:                  NONE
C
C  COMMON BLOCK:    /GRID/
C           ISBIG  - FIRST DIMENSION IN FNOC SPHERICAL GRID OF UPPER
C                    LEFT CORNER OF REGIONAL GRID
C           JSBIG  - SECOND DIMENSION IN FNOC SPHERICAL GRID OF LEFT
C                    EDGE OF REGIONAL GRID
C           MGRD   - FIRST  DIMENSION OF REGIONAL GRID
C           NGRD   - SECOND DIMENSION OF REGIONAL GRID
C
C  ERROR CONDITIONS:    SET ERROR FLAG IF POINT OFF REGIONAL GRID
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:  NO OTHER
C
C  METHOD:        ASSUME REGIONAL GRID IS SUBSET OF 2.5 DEGREE SPHERICAL
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C
C........................END PROPLOGUE..................................
C
      DIMENSION FLD (MGRD,NGRD)
C
      COMMON/GRID/ MGRD,NGRD,MBYN,ISBIG,JSBIG,IDTFLD
C
      DATA BLONW/300.0/, INIL/-1/
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
cx    IF (INIL .EQ. -1) THEN
cx       INIL = 0
C                   CALCULATE THE WEST LONGITUDE OF LEFT EDGE
C                   OF REGIONAL GRID
cx       BLONW = BLONW -2.5*(JSBIG -1)
cx       IF (BLONW .LT. 0.0) BLONW = 360.0 +BLONW
C                   CALCULATE THE LATITUDE OF THE BOTTOM EDGE
C                   OF REGIONAL GRID
cx       BLAT = 95.0 -2.5*(ISBIG +NGRD)
cx       PRINT *, 'FBAM2, FLDINT BLAT ',BLAT,' BLONW ',BLONW
cx    ENDIF
C
C                   CALCULATE GRID LOCATION OF RLAT,RLON
C
C                   FIRST DIMENSION OF GRID INCREASES TO THE EAST
C                          NOTE, 1.0/2.5 = 0.4
cx    IF (RLON .LE. BLONW) THEN
C                   NORMAL CASE
cx       XM = 1.0 +0.4*(BLONW -RLON)
cx    ELSE
C                   ALLOW GRID TO CROSS GREENWICH, SHOULD NOT HAPPEN
cx       XM = 1.0 +0.4*(360.0 +BLONW -RLON)
cx    ENDIF
C                   SECOND DIMENSION OF GRID INCREASES TO THE NORTH
cx    YN = 1.0 +0.4*(RLAT -BLAT)
C
cx    IF ((YN.GE.1.0 .AND. YN.LE.NGRD) .AND.
cx   .    (XM.GE.1.0 .AND. XM.LE.MGRD)) THEN
C                   INTERPOLATE FOR FIELD VALUE, FVAL, AT XM,YN
cx       FVAL = CNTRP5 (XM,YN,FLD,MGRD,NGRD)
cx       IERR = 0
cx    ELSE
C                   REQUESTED POINT IS OFF GRID
cx       IERR = -1
cx    ENDIF
c
cx the grid is set up so that the starting point is at -90 lat
cx and 0W lon. The first dimension of the grid is x (lon), and 
cx increases east.  The second dimension is y (lat) and increases north.

cx	 xm = 1.0  + rlon*0.4
         xm = 1.0 + (360.0-rlon)*0.4
	 yn = (rlat+92.5)*0.4 
         call cycint(xm,yn,fld,mgrd,ngrd,fval,ierr)
      RETURN
C
      END
      SUBROUTINE FCTOUT (IOFCST,ITAU,LSTITR,AIDNAM)
C
C........................START PROLOGUE.................................
C
C  SUBPROGRAM NAME:  FCTOUT
C
C  DESCRIPTION:      WRITE FORECAST ON FILE IOFCST
C
C  ORIGINAL PROGRAMMER, DATE:    HARRY D. HAMILTON    (MM -GSA)  OCT 89
C
C  LIBRARY OF RESIDENCE:          
C
C  CLASSIFICATION:               UNCLASSIFIED
C
C  USAGE (CALLING SEQUENCE):     CALL FCTOUT (IOFCST,ITAU,LSTITR)
C
C  INPUT PARAMETERS:
C    IOFCST - UNIT AND TAPE NUMBER OF OUTPUT FILE
C    ITAU   - TAU OF BASE FIELD AT LAST FIX POSITION
C    LSTITR - LAST ITERATION OF MODEL, EACH ITERATION IS ONE HOUR
C    AIDNAM - SBAM, MBAM OR FBAM
C
C  OUTPUT PARAMETERS:
C    N      - HOUR OF FORECAST CYCLONE POSITION
C    PLAT   - LATITUDE OF FORECAST POSITION
C    CNS    - CHARACTER, EITHER "N", OR "S"
C    PLON   - LONGITUDE OF FORECAST POSITION
C    CEW    - CHARACTER, EITHER "E", OR "W"
c
c
C
C  INPUT FILE:                   NONE
C
C  OUTPUT FILE:   TAPE"IOFCST", FORECAST TROPICAL CYCLONE POSITIONS
C
C  COMMON BLOCK:
C
C     COMMON /DTGS/
C           DTGFLD - BASE DTG OF FIELDS (00 OR 12Z FOR HOUR)
C           DTGFIX - DTG OF LAST FIX LOCATION (00, 06, 12 OR 18Z FOR HR)
C
C     COMMON /FCST/
C           CLAT   - FORECAST LATITUDE, DEGREES (+N, -S)
C           CLON   - FORECAST LONGITUDE, DEGREES WEST
C
C
C  ERROR CONDITIONS:    SET ERROR FLAG IF POINT OFF REGIONAL GRID
C
C........................MAINTENANCE SECTION............................
C
C  DATA FILES:           NO OTHER
C
C  TEMPORARY FILES:      NONE
C
C  PRINCIPAL VARIABLES AND ARRAYS:  NO OTHER
C
C  METHOD:        ASSUME REGIONAL GRID IS SUBSET OF 2.5 DEGREE SPHERICAL
C
C  LANGAUGE:             CDC FTN5 (FORTRAN 77)
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  FCTOUT*01  (14 AUG 91) -- HAMILTON,H.
C           PROVIDE FOR PROCESSING SHALLOW AND MEDIUM LAYER FIELDS
C           IN ADDITION TO ORIGINAL DEEP LAYER MEANS - JTWC REQUEST
C
C........................END PROPLOGUE..................................
C
      PARAMETER (MH = 72)
C
      CHARACTER*1 CNS, CEW
      CHARACTER*3 STRMID
      CHARACTER*4 AIDNAM
      CHARACTER*8 DTGFLD,DTGSYP,DTGFIX
C
      COMMON/DTGS/  DTGFLD,DTGSYP,DTGFIX,STRMID
      COMMON/FCST/  FTIME(0:MH),  CLAT(0:MH),  CLON(0:MH),
     .             CTHETA(0:MH),ETHETA(0:MH),DTHETA(0:MH),
     .             CSPEED(0:MH),ESPEED(0:MH),DSPEED(0:MH)
C
      PLON = CLON(0)
      IF (PLON .LT. 180.0) THEN
         WRITE (IOFCST,601) STRMID
         CEW = 'W'
      ELSEIF (PLON .LT. 260.0) THEN
         WRITE (IOFCST,602) STRMID
         PLON = 360.0 -PLON
         CEW = 'E'
      ELSE
         WRITE (IOFCST,603) STRMID
         PLON = 360.0 -PLON
         CEW = 'E'
      ENDIF
      WRITE (IOFCST,610)
      WRITE (IOFCST,620) DTGFIX(1:2), DTGFIX(3:4), DTGFIX(5:6),
     .                   DTGFIX(7:8)
      WRITE (IOFCST,630) AIDNAM, ITAU, DTGFLD
      WRITE (IOFCST,640)
      PLAT = CLAT(0)
      IF (PLAT .GE. 0.0) THEN
         CNS = 'N'
      ELSE
         PLAT = ABS (PLAT)
         CNS = 'S'
      ENDIF
      WRITE (IOFCST,645) PLAT, CNS, PLON, CEW
      WRITE (IOFCST,650)
      DO 110 N=6, LSTITR, 6
         PLAT = CLAT(N)
         IF (PLAT .GE. 0.0) THEN
            CNS = 'N'
         ELSE
            PLAT = ABS (PLAT)
            CNS = 'S'
         ENDIF
         PLON = CLON(N)
         IF (PLON .LT. 180.0) THEN
            CEW = 'W'
         ELSE
            PLON = 360.0 -PLON
            CEW = 'E'
         ENDIF
      WRITE (IOFCST,660) AIDNAM, N, PLAT, CNS, PLON, CEW
  110 CONTINUE
      RETURN
C
  601 FORMAT (3X,'HURRICANE',9X,A3)
  602 FORMAT (3X,'TYPHOON',11X,A3)
  603 FORMAT (3X,'TROPICAL CYCLONE',2X,A3)
  610 FORMAT (3X,'ARQ VERSION *** FBAM ***',//)
  620 FORMAT (3X,'WARNING DTG (YEAR =',A2,') (MONTH =',A2,') (DAY =',A2,
     .        ') (HOUR =',A2,')',//)
  630 FORMAT (3X,A4,' INPUT TAU',I3,' FIELDS FROM ',A8,//)
  640 FORMAT (3X,'ANALYSIS POSITION',//)
  645 FORMAT (11X,'LATITUDE=',F5.1,A1,2X,'LONGITUDE=',F6.1,A1,//)
  650 FORMAT (3X,'FORECAST POSITIONS',//)
  660 FORMAT (3X,A4,'  TAU=',I3,2X,'LATITUDE=',F5.1,A1,2X,
     .       'LONGITUDE=',F6.1,A1)
C
      END
