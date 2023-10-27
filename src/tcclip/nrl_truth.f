      PROGRAM TRUTH
C
C**   THIS PROGRAM CALCULATES THE ERRORS FROM A GIVEN SET OF
C**   TRACK FORECAST MODELS USING DATA FROM THE AALNNYR.DAT AND
C**   BALNNYR.DAT FILES.  IT ALSO YIELDS THE AVERAGE ERRORS COMPARED
C**   TO ANY OTHER MODEL.  THIS VERSION IS MODIFIED TO INCLUDE INTENSITY
C**   VERIFICATION.
C
C**   JAMES GROSS DEVELOPED THIS CODE WHICH IS BASED ON THE PROGRAM
C**   QKVER ORIGINATED BY MARK DEMARIA
C
C**   12/1/97
C
C***********************************************************************
C
C**   THIS VERSION WAS MODIFIED FOR JIM GROSS ON 1/8/92.  THE UNIRAS
C**   GRAPHICS WAS REMOVED AND THE DIRECTORY INFORMATION FROM THE
C**   ATCF INPUT FILES WAS REMOVED.
C
C**   THIS VERSION OF QKVER WAS MODIFIED BY JIM GROSS TO RUN ON THE NAS
C**     COMPUTER 1/23/92
C
C**   THIS VERSION OF TRUTH WAS MODIFIED BY JIM GROSS TO RUN ON A PC AND
C**     A WORKSTATION USING A INPUT FILE TO DETERMINE THE RUN PARAMETERS
C**     AND THE STORMS ON WHICH TO RUN  -- 10/19/93
C
C**   PROGRAM CHANGES TO USE HP FEATURE OF INPUTING FLNAME NAME FROM THE
C**     COMMAND LINE.  ALSO MADE OUTPUT FILE NAME RELATE TO INPUT FLIE
C**     NAME.  -- 11/07/94
C
C**   ADDED THE INITIAL POSITION ERROR AND THE PRODUCTION OF A HARVARD
C**     GRAPHICS FILE FOR PROCESSING.  ALSO MADE THE CLIPER FORMULATION
C**     A SEPARATE SUBROUTINE -- 9/25/95
C
C**     GIVE CREDIT TO ALL MODELS IN CASE OF TIE FOR "SUPERIOR PERFORMANCE"
C**     SAMPSON, NRL 3/15/01               
C
C**     CONVERTED TO RUN IN ATCF3.5 OFF CONFIGURATION FILE SUPPLIED BY GUI 
C**     SAMPSON, NRL 4/10/01               
C
C**     INCLUDED MORE NHC IMPROVEMENTS AS PER JIM GROSS
C**     SAMPSON, NRL 5/01/01               
C
C**   0:7 (00, 12, 24, 36, 48, 72, 96, 120) THE MAXIMUM NUMBER OF 
c**       FORECAST PERIODS
C
C**   MXNMD IS THE MAXIMUM NUMBER OF FORECAST MODELS
C**   MXNST IS THE MAXIMUM NUMBER OF STORMS
C**   MXCS  IS THE MAXIMUM NUMBER OF CASES
C**   MXCSS IS THE MAXIMUM NUMBER OF CASES PER STORM
c**   mtau  is the maximum number of forecast periods per DTG (max = 7)
c
      include 'dataformats.inc'
C
cx    These should be adjusted higher if more data to be analyzed.
cx    Watch out for memory problems if set too high.
cx    PARAMETER (MXNMD=10,MXNST=212,MXCS= 500,MXCSS=100,mtau=7,
cx   & mtaup1=mtau + 1)
      PARAMETER (MXNMD=10,MXNST=212,MXCS= 3500,MXCSS=100,mtau=7,
     & mtaup1=mtau + 1)
C
      PARAMETER (MXDTI=MXNMD*MXCS*mtaup1,MXPBI=MXNMD*MXNMD*mtaup1)
C
      REAL BTLAT(MXCS,0:mtau),BTLON(MXCS,0:mtau),BTVMAX(MXCS,0:mtau)
cx
      character*1  btns(MXCS,0:mtau),BTew(MXCS,0:mtau)
      character*1  ns,ew
      REAL BHLAT(MXCS),BHLON(MXCS),BHVMAX(MXCS)
      REAL XLON(MXNMD,MXCS,0:mtau),YLAT(MXNMD,MXCS,0:mtau),
     & VMAX(MXNMD,MXCS,0:mtau)
      REAL ERR(MXNMD,MXCS,0:mtau),XBIAS(MXNMD,MXCS,0:mtau),
     & YBIAS(MXNMD,MXCS,0:mtau)
      REAL ERRM(MXNMD,0:mtau),STDEV(MXNMD,0:mtau),XBIASM(MXNMD,0:mtau),
     & YBIASM(MXNMD,0:mtau),RECLIP(MXNMD,MXNMD,0:mtau)
      REAL FSP(MXNMD,0:mtau),ERRS(MXNMD,MXCS,0:mtau),ERROR(MXNMD,0:mtau)
      REAL PROB(MXNMD,MXNMD,0:mtau),PROBA(MXNMD,MXNMD,0:mtau),
     & RNHAA(0:mtau)
      REAL*8 TDF,TSTAT,TSTATA,RNH,RNHA
      real flat(0:mtau),flon(0:mtau),fvmax(0:mtau)
C
      EQUIVALENCE (YBIAS,ERRS),(YBIASM,ERROR)
C
      INTEGER NDMO(12),NHCASE(0:mtau),IDEL(0:mtau),NFSP(MXNMD,0:mtau),
     & ICASECT(0:mtau),KTIME(0:7),NDMOS(12),nfcase(0:mtau)
      INTEGER GETARG, result
C
      LOGICAL INT00,INT06,INT12,INT18
C
      CHARACTER*1   FRCSTR
      CHARACTER*2   CENT
      CHARACTER*3   FCSTPD(0:7)
      CHARACTER*4   MNAME(MXNMD),MNAMEF
      CHARACTER*8   FNAME(MXCS),FHNAME(MXCS),FNNEW,FNOLD
      CHARACTER*8   STRMID,flname(mxnst)
      CHARACTER*10  CDATE,BDATE,CCDATE(MXCS),CHDATE(MXCS)
      CHARACTER*10  dtgnext,dtgcur,btdtg
      CHARACTER*10  SFNAME(MXNST),SNAME(MXCS),SHNAME(MXCS)
      CHARACTER*18  STRMPATH
cx    CHARACTER*13  FILEA,FILEB
cx    CHARACTER*25  INPUT
cx    CHARACTER*30  OUTPUT
      character*120 filea,fileb
      character*120 input
      character*120 output
      character*124 outtxt
      character*124 outhvd
      character*120 storms
      character*200 bline
      integer       ninput
      integer       noutpt
      integer       nstdir
      character*10  startdtg
      character*10  enddtg
      integer       ind
      character*2   unitch(2)
C
      type ( BIG_AID_DATA ) aidsData
      type ( AID_DATA )     aidData, tauData
c
      DATA IERRPR    /0/
      DATA ISTMPR    /1/
      DATA ITRKPR    /0/
      DATA LULG,LUHR,LUAA,LUBA  /31,32,21,22/
      DATA NCASE     /0/
      DATA NDMO      /31,28,31,30, 31, 30, 31, 31, 30, 31, 30, 31/
      DATA NDMOS     / 0,31,59,90,120,151,181,212,243,273,304,334/
      DATA NHCASE    /mtaup1*0/
      DATA PI        /3.141593/
cx  no longer required, set in subroutine ... sampson
cx    DATA RLATHI    /  90.0/
cx    DATA RLATLO    / -90.0/
cx    DATA RLONHI    / 180.0/
cx    DATA RLONLO    /-180.0/
cx    DATA VMHI      /999.0/
cx    DATA VMLO      /34.0/
cx    DATA VMVER     /34.0/
cx    DATA VMVER1    /250.0/
cx    DATA INTENS    /0/
      DATA XLON      /MXDTI*-99.0/
      DATA YLAT      /MXDTI*-99.0/
      DATA VMAX      /MXDTI*-99.0/
      DATA SAMADJ    / 30.0/
C
      DATA KTIME     /0,12,24,36,48,72,96,120/
      DATA FCSTPD    /' 00',' 12',' 24',' 36',' 48',' 72',' 96','120'/
      DATA PROB,PROBA/MXPBI*0.0,MXPBI*0.0/
      data unitch    /'NM','KM'/
C
C**   SET VMVER TO RESTRICT CASES TO THOSE WITH BEST TRACK MAX WINDS
C**     GREATER THAN VMVER (KTS). ENTIRE CASE IS REMOVED IF INITIAL
C**     VMAX IS .LE. VMVER. FORECAST CASE IS REMOVED IF VMAX AT FORECAST
C**     TIME IS .LE. VMVER. THIS PARAMETER IS USEFUL FOR ELIMINATING ALL
C**     DEPRESSION CASES.
cxx   set vmver1 to restrict cases to max winds less than vmver1 (kts).
cxx     similar to vmver. this parameter would be useful for eliminating
cxx     all hurricane or typhoon cases.
C**
C**   SET VMLO TO RESTRICT CASES WITH INITIAL VMAX .GT. VMLO.
C**   SET VMHI TO RESRTICT CASES WITH INITIAL VMAX .LT. VMHI.
C**
C**   SET RLATLO, RLATHI FOR LATITUDE  SIMILAR TO VMLO, VMHI
C**   SET RLONLO, RLONHI FOR LONGITUDE SIMILAR TO VMLO, VMHI
C**
C**   SET IERRPR=1 TO PRINT ALL ERRORS FOR HOMOGENEOUS SAMPLE  (ELSE=0)
C**
C**   SET ISTMPR=1 TO PRINT STORM ERRORS FOR HOMOGENEOUS SAMPLE  (ELSE=0)
C**
C**   SET ITRKPR=1 TO PRINT TRACKS (OR INTENSITY) OF ALL CASES (ELSE=0)
C**
C**   SET INTENS =0 FOR TRACK OR =1 FOR INTENSITY VERIFICATION
C
CC    NAMELIST/INFO/NDATAF,SFNAME,NMODEL,MNUMC,MNAME,VMVER,VMLO,VMHI,
CC   &              RLATLO,RLATHI,RLONLO,RLONHI,ITRKPR,IERRPR,IYR,
CC   &              INT00,INT06,INT12,INT18,
CC   &              SAMADJ,INTENS,INCFSP
C
C**   INITIALIZE VALUES
C
      DTR = PI/180.0
C
cx    RLATLO =  -90.0
cx    RLATHI =   90.0
cx    RLONLO = -180.0
cx    RLONHI =  180.0
C
      INT00 = .TRUE.
      INT06 = .TRUE.
      INT12 = .TRUE.
      INT18 = .TRUE.
C
      VMHI  = 999.0
C
C**   CHECK NUMBER OF COMMAND LINE ARGUMENTS AND READ ONE ARGUMENT
C
cx    NARG = IARGC()
cx    IF (NARG.NE.1) THEN
cx       STOP ' PROGRAM REQUIRES INPUT FILE NAME ON THE COMMAND LINE'
cx    ENDIF
      narg = iargc()
      if (narg.lt.2) then
         stop ' Requires three arguments (input, output, storms dir)'
      endif
C
      NINPUT = GETARG(1,INPUT)
      NOUTPT = GETARG(2,OUTPUT)
      nstdir = 0
      storms = ''
      nstdir = getarg(3,storms)
C
C**   OPEN THE INPUT CONTROL FILE, CREATE THE OUTPUT FILE NAMES AND OPEN
C
      OPEN (11,FILE=INPUT,STATUS='OLD',IOSTAT=IOS,ERR=1010)
C
cx    OUTPUT = INPUT(1:NINPUT)//'.out'
cx    OPEN (UNIT=LULG,FILE=OUTPUT,STATUS='UNKNOWN',IOSTAT=IOS,ERR=1020)
      outtxt = output(1:noutpt)//'.out'
      open (unit=lulg,file=outtxt,status='unknown',iostat=ios,err=1020)
C
cx    OUTPUT = INPUT(1:NINPUT)//'.hvd'
cx    OPEN (UNIT=LUHV,FILE=OUTPUT,STATUS='UNKNOWN',IOSTAT=IOS,ERR=1020)
      outhvd = output(1:noutpt)//'.hvd'
      open (unit=luhv,file=outhvd,status='unknown',iostat=ios,err=1020)
C
C**   READ IN THE CONTROL PARAMETERS
C
cx    READ (11,'(12X,I1,15X,I1,19X,I1)') IERRPR,ISTMPR,ITRKPR
cx    WRITE (*,'('' IERRPR, ISTMPR ,ITRKPR = '',3I5)')
cx   & IERRPR,ISTMPR,ITRKPR
cx    READ (11,'(12X,I1,2(15X,F5.1))') INTENS,VMLO,VMVER
cx    WRITE (*,'('' INTENS, VMAXLO, VMAXVER = '',I5,2F5.1)')
cx   & INTENS,VMLO,VMVER
C
C**   READ THE NUMBER OF MODELS AND MODEL IDS TO VERIFY
C
cx    READ (11,'(11X,I2,12((1X,A4)))') NMODEL,(MNAME(I), I = 1,NMODEL)
cx    WRITE (*,'('' NMODEL = '',I5)') NMODEL
C
CC    INTENS = 0
CC    INTENS = 1
cxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcx
cx
cx  read the data at the top of the input file, individual storms (bottom)
cx  are read in loop below
cx
      call readin ( lulg, mxnmd, intens, metric, ierrpr, istmpr, itrkpr,
     &              vmhi, vmlo, vmver1, vmver, 
     &              rlathi, rlatlo, rlonlo, rlonhi, startdtg, enddtg, 
     &              int00, int06, int12, int18, nmodel, mname )
cxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcx

C
C**   SET INCFSP=1 TO INCLUDE NO CHANGE FORECAST IN FREQUENCY OF
C**   SUPERIOR PERFORMANCE FOR INTENSITY VERIFICATION
C
      INCFSP = 0
C
CC    IERRPR = 1
CC    IERRPR = 0
CC    ISTMPR = 1
CC    ISTMPR = 0
CC    ITRKPR = 1
CC    ITRKPR = 0
C
CC    VMVER =   0.0
CC    VMVER =  34.0
CC    VMLO  =   0.0
CC    VMLO  =  34.0
C
C**   SET TIME IN HOURS FOR NO SERIAL CORRELATION. USED FOR
C**   DETERMINING ADJUSTED SAMPLE SIZE FOR SIGNIFICANCE TESTING
C
      SAMADJ = 30.0
C
C**   DO A BEST TRACK CLIPER OR NOT?
C
      IXCLIP = 0
CC    IXCLIP = 1
C
C**   READ THE STORM IDS FROM THE INPUT FILE
C
      II = 0
   10 READ (11,'(A)',END=100) STRMID
      WRITE (*,'('' STRMID = '',A)') STRMID
      II = II + 1
C
      NTIME = 0
      NCASEI = NCASE + 1
C
C**   Create the adeck and bdeck file names for the storm
C
      FILEA = 'a'//STRMID//'.dat'
      FILEB = 'b'//STRMID//'.dat'
      if (nstdir.gt.0) then
	  filea = storms(1:nstdir)//'/a'//strmid//'.dat'
	  fileb = storms(1:nstdir)//'/b'//strmid//'.dat'
      endif
      
C  
cx    WRITE (*,'('' FILEA, FILEB = '',A16,1X,A16)') FILEA,FILEB
      write (*,*)'adeck=', filea
      write (*,*)'bdeck=', fileb
      
cx    write storms attempted to output
      write (lulg, * ) 'using ', strmid
      
C
C**   OPEN A-DECK AND B-DECK FOR A PARTICULAR STORM
C
      OPEN (LUAA,FILE=FILEA,STATUS='OLD',IOSTAT=IOS,ERR=1030)
      OPEN (LUBA,FILE=FILEB,STATUS='OLD',IOSTAT=IOS,ERR=1040)
C
C**   Process the storm's a-deck by obtaining the first DTG
C
      read ( luaa, '( 8x, a10 )' ) dtgcur
      backspace ( luaa )
c
c     ***  Ann   ***
      nbadcnt = 0
c     ***  Ann   ***
   20 continue
c
c**   Read in all the aids associated with that DTG or the next DTG until
c**     end-of-file is reached
c
      call getBigAidDTG ( luaa, dtgcur, aidsData, result )
      if ( result .le. 0 ) then
         if ( result .eq. 0 ) then
c           ***  Ann   ***
            nbadcnt = nbadcnt + 1
cx try and rewind the file, so that a few dtgs can be skipped
            write (*,*)nbadcnt,' failed search for dtg:',dtgcur
            write (*,*)' rewind file for next dtg'
	    rewind ( luaa )
            if ( nbadcnt .gt. 8 )  goto 50
c           ***  Ann   ***
            goto 45
cxjim    elseif ( result .lt. 0 ) then   
         else   
            goto 50
         endif
      endif   
c     ***  Ann   ***
      nbadcnt = 0
c     ***  Ann   ***
c
c**   Process the model initial conditions from the TAU = 0 CARQ card
c 
      call getTech ( aidsData, "CARQ", aidData, result )
cxjim if ( result .ne. 1 ) goto 45
      if ( result .eq. 0 ) goto 45
c
      call getSingleTAU ( aidData, 0, tauData, result )
cxjim if ( result .ne. 1 ) goto 45
      if ( result .eq. 0 ) goto 45
c
      cdate = tauData%aRecord(1)%DTG
C
C**   Check the synoptic hour
C
      READ ( cdate, '(8x,i2)' ) ITM
c
cx    IF (ITM.EQ. 0.AND..NOT.INT00) GOTO 20
cx    IF (ITM.EQ. 6.AND..NOT.INT06) GOTO 20
cx    IF (ITM.EQ.12.AND..NOT.INT12) GOTO 20
cx    IF (ITM.EQ.18.AND..NOT.INT18) GOTO 20
      if (itm.eq. 0.and..not.int00) goto 45
      if (itm.eq. 6.and..not.int06) goto 45
      if (itm.eq.12.and..not.int12) goto 45
      if (itm.eq.18.and..not.int18) goto 45
c
      flat(0)  = tauData%aRecord(1)%lat
      flon(0)  = tauData%aRecord(1)%lon
      fvmax(0) = tauData%aRecord(1)%vmax
c
      PRINT * , ' CENTER INFO = ', dtgcur, fLAT(0),fLON(0),fVMAX(0)
c
      FLNAME(II) = strmid
c
      NCASE = NCASE + 1
cx    stop the program if NCASE goes beyond MXCS (array problems)
      if (ncase .gt. mxcs) then
           print *, 'Maximum number of cases (',mxcs,') exceeded'
           stop ' TRUTH PROGRAM ABORTED'
      endif
	      
      NTIME = NTIME + 1
c
      WRITE (*,'('' NCASE = '',I5,'' NTIME = '',I5,'' NSTORMS = '',
     & I5,'' ID = '',A8)') NCASE, NTIME, II, FLNAME(II)
c
      CCDATE(NCASE) = CDATE
      FNAME(NCASE)  = FLNAME(II)
      SFNAME(II)    = tauData%aRecord(1)%stormname
      SNAME(NCASE)  = SFNAME(II)
C
C**   PROCESS THE AIDS for the models read in
C
      DO 40 JJ = 1,NMODEL
C
         call getTech ( aidsData, mname(jj), aidData, result )
cxjim    if ( result .ne. 1 ) go to 40
         if ( result .eq. 0 ) go to 40
c
         call getSingleTAU ( aidData, 0, tauData, result )
c
c**   See if the model has a TAU = 0 entry.  If it does, use it,
c**    otherwise use the initial position from the CARQ card.
c
cxjim    if ( result .eq. 1 ) then
         if ( result .eq. 0 ) then
c
            XLON(JJ,NCASE,0) = tauData%aRecord(1)%lon
            IF (XLON(JJ,NCASE,0).LE.0.0) XLON(JJ,NCASE,ITM) = -99.0
C
            YLAT(JJ,NCASE,0) = tauData%aRecord(1)%lat
            IF (YLAT(JJ,NCASE,0).LE.0.0) YLAT(JJ,NCASE,ITM) = -99.0
C
            VMAX(JJ,NCASE,0) = tauData%aRecord(1)%vmax
            IF (VMAX(JJ,NCASE,0).LE.0.0) VMAX(JJ,NCASE,ITM) = -99.0
c
         else   
c
            XLON(JJ,NCASE,0) = flon(0)
            IF (XLON(JJ,NCASE,0).LE.0.0) XLON(JJ,NCASE,ITM) = -99.0
C
            YLAT(JJ,NCASE,0) = flat(0)
            IF (YLAT(JJ,NCASE,0).LE.0.0) YLAT(JJ,NCASE,ITM) = -99.0
C
            VMAX(JJ,NCASE,0) = fvmax(0)
            IF (VMAX(JJ,NCASE,0).LE.0.0) VMAX(JJ,NCASE,ITM) = -99.0
c
         endif   
c
c**   Obtain the 12, 24, 36, 48 and 72 hour forecast information, 
c**    if it exists. 
c
         do itm = 1, mtau
c
            call getSingleTAU ( aidData, ktime(itm), tauData, result )
cxjim       if ( result .ne. 1 ) goto 40
cxbuck ... do all cases (even when missing tau12), next if caused program
cxbuck ... to skip all 
cxbuck      if ( result .eq. 0 ) goto 40
            if ( result .ne. 0 ) then   
c
               XLON(JJ,NCASE,itm) = tauData%aRecord(1)%lon
               IF (XLON(JJ,NCASE,itm).LE.0.0) XLON(JJ,NCASE,ITM) = -99.0
C
               YLAT(JJ,NCASE,itm) = tauData%aRecord(1)%lat
               IF (YLAT(JJ,NCASE,itm).LE.0.0) YLAT(JJ,NCASE,ITM) = -99.0
C
               VMAX(JJ,NCASE,itm) = tauData%aRecord(1)%vmax
               IF (VMAX(JJ,NCASE,itm).LE.0.0) VMAX(JJ,NCASE,ITM) = -99.0
cxbuck ... do all cases (even when missing tau12)
          endif
c
          enddo
c
   40 continue
c
   45 continue
c
c**   Increment the current DTG by 6 hours and then read the next DTG block
c**    of forecasts
c 
      call dtgmod ( dtgcur, 6, dtgnext, result )
      dtgcur = dtgnext
c
      goto 20
c
C**   PROCESS THE A FORECASTER'S VERIFICATION
C
CC        IF (CLINE(1:2).EQ.'01'.AND.FRCSTR.NE.'J') GO TO 40
CC        IF (CLINE(1:2).EQ.'01'.AND.(FRCSTR.EQ.' '.OR.FRCSTR.EQ.'J'))
CC   &      GO TO 40
c
   50 CONTINUE
C
C**   PROCESS THE STORM'S B-DECK
C
      DO 85 N = NCASEI,NCASE
C
         CDATE = CCDATE(N)
c
         do 85 i = 0, mtau
c
            call dtgmod ( cdate, ktime(i), dtgnext, result )
c
            rewind ( luba )
c
            blat  = -99.0
            blon  = -99.0
            bvmax = -99.0
c
   80       read ( luba, '(a)', end=83, iostat=ios, err=1060 ) bline
c
            if ( bline(9:18) .ne. dtgnext ) goto 80

c
C**   INCLUDE THIS LINE IF YOU WANT THE VERIFICATION PERFORMED OVER
C**      A SPECIFIED PERIOD OF TIME (YYYYMMDDHR)
C
cc          IF ( bline(9:18) .lt. '2000080112' .OR. 
cc   &           bline(9:18) .gt. '2000093012' ) GO TO 80
cx    included check permanently ... sampson, nrl     
	    if ( bline(13:18) .lt. startdtg(1:6) .or.
     &           bline(13:18) .gt. enddtg(1:6) ) go to 80
c
c23456789012345678901234567890123456789012345678901234567890123456789012
cx          read ( bline, '(35x,f3.1,3x,f4.1,3x,f3.0)' ) blat,blon,bvmax  
            read ( bline, '(35x,f3.1,a1,2x,f4.1,a1,2x,f3.0)' ) 
     &	    blat,ns,blon,ew,bvmax  
c
   83       continue
c
            BTLAT(N,I)  = BLAT
            BTLON(N,I)  = BLON
            BTVMAX(N,I) = BVMAX
cx
	    btns(n,i)   = ns
	    btew(n,i)   = ew
c
   85    continue
C
      CLOSE ( LUAA )
      CLOSE ( LUBA )
C
      GO TO 10
C
  100 NDATAF = II
C
C**   IF DESIRED, ADD ATLANTIC BEST TRACK CLIPER TO THE SET OF FORECASTS
C
      IF (INTENS.EQ.0.AND.IXCLIP.EQ.1) THEN
C
          NMODEL = NMODEL + 1
          MNAME(NMODEL) = 'BCLP'
C
cc        CALL ABCLIP (BTLAT,BTLON,BTVMAX,XLON,YLAT,VMAX,CCDATE,FNAME,
cc   & MXCS,MXNMD,NCASE,NMODEL)
C
      ENDIF
C
C**   ADD NO CHANGE FORECAST AS EXTRA MODEL FOR INTENSITY FORECASTS
C
      IF (INTENS.EQ.1.AND.IXCLIP.EQ.0) THEN
C
         NMODEL = NMODEL + 1
         MNAME(NMODEL) = 'NCHG'
C
         DO N = 1, NCASE
            DO K = 0, mtau
               VMAX(NMODEL,N,K) = BTVMAX(N,0)
            enddo   
         enddo
C
      ENDIF
C
C**   ZERO OUT THE MEAN ARRAYS
C
      DO K = 0, mtau
         DO J = 1, NMODEL
            ERRM(J,K)   = 0.0
            STDEV(J,K)  = 0.0
            XBIASM(J,K) = 0.0
            YBIASM(J,K) = 0.0
         enddo   
      enddo
C
C**   CALCULATE ERRORS FOR HOMOGENEOUS SAMPLE
C
      DO 260 N = 1, NCASE
c
         IF (BTVMAX(N,0) .LE. VMVER ) GO TO 260
cx   vmver1 is the upper restriction comparable to vmver
         if (btvmax(n,0) .ge. vmver1) go to 260
         IF (BTVMAX(N,0) .LE. VMLO  ) GO TO 260
         IF (BTVMAX(N,0) .GE. VMHI  ) GO TO 260
cx   account for SH, WP and IO  ... sampson, nrl 
cx       IF (BTLAT(N,0)  .LE. RLATLO) GO TO 260
cx       IF (BTLAT(N,0)  .GE. RLATHI) GO TO 260
cx       IF (BTLON(N,0)  .LE. RLONLO) GO TO 260
cx       IF (BTLON(N,0)  .GE. RLONHI) GO TO 260
cx     
         if (btns(n,0) .eq. 'N') btlatchk =  btlat(n,0)
         if (btns(n,0) .eq. 'S') btlatchk = -btlat(n,0)
	 if (btew(n,0) .eq. 'W') btlonchk =  btlon(n,0)
	 if (btew(n,0) .eq. 'E') btlonchk =  360-btlon(n,0)
	 if (btlatchk  .le. rlatlo)   go to 260
	 if (btlatchk  .ge. rlathi)   go to 260
	 if (btlonchk  .le. rlonlo)   go to 260
	 if (btlonchk  .ge. rlonhi)   go to 260
	  
         IDELT = 0
C
         DO K = 0,mtau
            IDEL(K) = 0
         enddo
C
C**   WEED OUT MISSING CASES
C
         DO 230 K = 1, mtau
cx          IF ( BTVMAX(N,K) .LE. VMVER ) THEN
cxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcx
            if ( btvmax(n,k).le.vmver .or. btvmax(n,k).ge.vmver1 ) then
                IDEL(K) = 1
                IDELT = IDELT + 1
                 GO TO 230
            ENDIF
C
            IF ( INTENS .EQ. 0 ) THEN
                IF ( BTLAT(N,K) .LE. 0.0 .OR.BTLON(N,K).LE.0.0) THEN
                    IDEL(K) = 1
                    IDELT = IDELT + 1
                    GO TO 230
                ENDIF
C
                DO J = 1, NMODEL
                   IF (XLON(J,N,K).LE.0.0.OR.YLAT(J,N,K).LE.0.0) THEN
                       IDEL(K) = 1
                       IDELT = IDELT + 1
                       GO TO 230
                   ENDIF
                enddo
            ELSE
                IF ( BTVMAX(N,K) .LE. 0.0 ) THEN
                    IDEL(K) = 1
                    IDELT = IDELT + 1
                    GO TO 230
                ENDIF
C
                DO J = 1, NMODEL
                   IF ( VMAX(J,N,K) .LE. 0.0 ) THEN
                       IDEL(K) = 1
                       IDELT = IDELT + 1
                       GO TO 230
                   ENDIF
               enddo
            ENDIF
  230    CONTINUE
C
         IF ( IDELT .GE. mtau ) GO TO 260
C
C**   CASE HAS AT LEAST ONE VALID FORECAST TIME
C
         DO K = 0, mtau
C
            IF (IDEL(K).EQ.0) NHCASE(K) = NHCASE(K) + 1
C
            IF (K.EQ.0) THEN
                NH         = NHCASE(0)
                FHNAME(NH) = FNAME(N)
                SHNAME(NH) = SNAME(N)
                CHDATE(NH) = CCDATE(N)
                BHLAT(NH)  = BTLAT(N,0)
                BHLON(NH)  = BTLON(N,0)
                BHVMAX(NH) = BTVMAX(N,0)
            ENDIF
C
            DO J = 1,NMODEL
               IF ( IDEL(K) .EQ. 1 ) THEN
                  ERR(J,NH,K)   = 9999.0
                  XBIAS(J,NH,K) = 9999.0
                  YBIAS(J,NH,K) = 9999.0
               ELSE
                  IF ( INTENS .EQ. 0 ) THEN
                     CAVGL = COS(0.5*DTR*(BTLAT(N,K) + YLAT(J,N,K)))
cx
cx*   POSITION ERROR IN KILOMETERS
cx
cx                   DX =   111.0*(BTLON(N,K) - XLON(J,N,K))*CAVGL
cx                   DY = - 111.0*(BTLAT(N,K) - YLAT(J,N,K))
cx
cx*   POSITION ERROR IN NAUTICAL MILES
cx
cx                   DX =    60.0*(BTLON(N,K) - XLON(J,N,K))*CAVGL
cx                   DY = -  60.0*(BTLAT(N,K) - YLAT(J,N,K))
cx
cx*   POSITION ERROR IN KILOMETERS
cx
                     if ( metric .eq. 1 ) then
		        DX =   111.0*(BTLON(N,K) - XLON(J,N,K))*CAVGL
                        DY = - 111.0*(BTLAT(N,K) - YLAT(J,N,K))
C
C**   POSITION ERROR IN NAUTICAL MILES
C
		     else
                        DX =    60.0*(BTLON(N,K) - XLON(J,N,K))*CAVGL
                        DY = -  60.0*(BTLAT(N,K) - YLAT(J,N,K))
		     endif
C
                  ELSE
                     DX    = VMAX(J,N,K) - BTVMAX(N,K)
                     DY    = 0.0
                  ENDIF
C
                  RERR          = SQRT(DX*DX + DY*DY)
                  ERR(J,NH,K)   = RERR
                  XBIAS(J,NH,K) = DX
                  YBIAS(J,NH,K) = DY
                  ERRM(J,K)     = ERRM(J,K)   + RERR
                  STDEV(J,K)    = STDEV(J,K)  + RERR*RERR
                  XBIASM(J,K)   = XBIASM(J,K) + DX
                  YBIASM(J,K)   = YBIASM(J,K) + DY
C
               ENDIF
            enddo
         enddo
  260 CONTINUE
C
C**   CALCULATE AVERAGE ERRORS
C
      DO K = 0, mtau
         CASES  = FLOAT(MAX(NHCASE(K),1))
         SCASES = FLOAT(MAX((NHCASE(K) - 1),1))
         DO J = 1, NMODEL
            STDEV(J,K) = SQRT((STDEV(J,K) - (ERRM(J,K)*ERRM(J,K)/CASES))
     &                                /SCASES)
            ERRM(J,K)   = ERRM(J,K)/CASES
            XBIASM(J,K) = XBIASM(J,K)/CASES
            YBIASM(J,K) = YBIASM(J,K)/CASES
         enddo   
      enddo
C
C**   CALCULATE ERRORS RELATIVE TO THE DIFFERENT MODELS
C
      DO JK = 1, NMODEL
         DO K = 0, mtau
            DO J = 1, NMODEL
               IF ( ERRM(JK,K) .GT. 0.0 ) THEN
                  RECLIP(J,JK,K) = 100.0*( ERRM(J,K) - ERRM(JK,K) )
     &                                         /ERRM(JK,K)
               ELSE
                  RECLIP(J,JK,K) = 9999.0
               ENDIF
            enddo
         enddo   
      enddo
C
C**   CALCULATE FREQUENCIES OF SUPERIOR PERFORMANCE
C
      IF ( INCFSP .EQ. 1 .AND. INTENS .EQ. 1 ) THEN
	  NMFSP = NMODEL - 1
      ELSE
	  NMFSP = NMODEL
      ENDIF
C
C** C
c**   Originally only last tie counted.  Now all ties counted.
c**      Due to Sampson 01/04/26
c
      DO 330 K = 0, mtau
         DO 330 N = 1, NHCASE(0)
c
            DO J = 1, NMFSP
               IF (ERR(J,N,K) .GT. 9000.0) GO TO 330
            enddo
c
c**   Find the minimum value
c
            EMIN = 10000.0
            DO J = 1, NMFSP
               IF (ERR(J,N,K) .LT. EMIN) THEN
                  EMIN = ERR(J,N,K)
               ENDIF
            enddo
c
c**   Count all ties of minimum value
c
            do j = 1, nmfsp
               if ( err(j,n,k) .eq. emin ) then
                  NFSP(J,K) = NFSP(J,K) + 1
                  nfcase(k) = nfcase(k) + 1
               endif
            enddo
c
  330 CONTINUE
      DO J = 1, NMFSP
         DO K = 0, mtau        
            FSP(J,K) = 100.0*FLOAT(NFSP(J,K))/FLOAT(MAX(1,nfcase(K)))
cc            FSP(J,K) = 100.0*FLOAT(NFSP(J,K))/FLOAT(MAX(1,NHCASE(K)))
         enddo   
      enddo
C
C**   CALCULATE PROBABILITIES FOR SIGNIFICANCE TESTING
C
      NMAX = NHCASE(0)
      DO 430 K = 0, mtau
         RNH  = AMAX1(2.0,FLOAT(NHCASE(K)))
         RNHM = RNH - 1.0
C
         DO 420 J = 1, NMODEL - 1
         DO 420 JJ = J + 1,NMODEL
            RNHA  = 0.0
            TOLD  = -2.0*SAMADJ
            FNOLD = 'NONE'
            VAR   = 0.0
            DBAR  = ERRM(JJ,K) - ERRM(J,K)
C
            DO 410 N = 1, NMAX
               E1   = ERR(J,N,K)
               E2   = ERR(JJ,N,K)
               DIFF = E2-E1
               IF (E1 .GT. 9000.0 .OR. E2 .GT. 9000.0) GO TO 410
               VAR = VAR + (DIFF - DBAR)**2
C
C**   SAMPLE SIZE ADJUSTMENT CALCULATION
C
               READ (CHDATE(N),'(i4,3I2)') IYR,IMO,IDA,ITM
               TNEW = FLOAT(24*(IDA + NDMOS(IMO)) + ITM)
               IF (MOD(IYR,4).EQ.0 .AND. IMO.GT.2) TNEW = TNEW + 24.0
C
C**   RESET TOLD IF A NEW STORM STARTS
C
               FNNEW = FHNAME(N)
               IF (FNNEW .NE. FNOLD) TOLD = -2.0*SAMADJ
C
               DELT = TNEW - TOLD
               IF (DELT .GE. SAMADJ) THEN
                  RNHA = RNHA + 1.0
               ELSE
                  RNHA = RNHA + DELT/SAMADJ
               ENDIF
               TOLD  = TNEW
               FNOLD = FNNEW
 410        continue
C
            VAR = VAR/RNHM
            SIGMA = SQRT(VAR)
C
            IF (SIGMA .GT. 0.0) THEN
                TSTAT  = ABS(DBAR)/(SIGMA/SQRT(RNH ))
                TSTATA = ABS(DBAR)/(SIGMA/SQRT(RNHA))
                PROB(J,JJ,K)  = TDF(TSTAT ,RNH )
                PROBA(J,JJ,K) = TDF(TSTATA,RNHA)
            ELSE
                PROB(J,JJ,K)  = 0.0
                PROBA(J,JJ,K) = 0.0
            ENDIF
C
  420    CONTINUE
C
         RNHAA(K) = RNHA
C
  430 CONTINUE
C
C**   PRINT VERIFICATION SPECIFICATIONS
C
cx  other parameters added to specs ... sampson, nrl 
cx  
cx    WRITE (LULG,1) INPUT,VMVER
cx    WRITE (LULG,2) VMLO,VMHI
cx    WRITE (LULG,3) RLATLO,RLATHI
cx    WRITE (LULG,4) RLONLO,RLONHI
cx  1 FORMAT (' FORECAST VERIFICATION RESULTS FOR ',A,//,
cx   &         ' CASES ELIMINATED WITH VMAX .LE.' ,F5.0,
cx   &            ' AT INITIAL OR FORECAST TIME')
cx  2 FORMAT (/,' CASES RESTRICTED TO INITIAL VMAX IN THE INTERVAL: ',
cx   &         F6.1,' TO ',F6.1)
cx  3 FORMAT (' CASES RESTRICTED TO INITIAL LAT  IN THE INTERVAL: ',
cx   &         F6.1,' TO ',F6.1)
cx  4 FORMAT (' CASES RESTRICTED TO INITIAL LON  IN THE INTERVAL: ',
cx   &         F6.1,' TO ',F6.1)
cx  
cx    write (lulg,1) input,vmver,vmver1
cx    write (lulg,2) vmlo,vmhi
cx    nslo = 'N'
cx    nshi = 'N'
cx    if (rlatlo .lt. 0) nslo = 'S'
cx    if (rlathi .lt. 0) nshi = 'S'
cx    ewlo1 = 'W'
cx    ewhi1 = 'W'
cx    if (rlonlo .gt. 180.0) then
cx      ewlo1 = 'E'
cx      lonlo1 = 360 - rlonlo
cx    endif
cx    if (rlonhi .gt. 180.0) then
cx      ewhi1 = 'E'
cx	rlonhi1 = 360 - rlonhi
cx    endif
cx    write (lulg,3) abs(rlatlo),nslo,abs(rlathi),nshi
cx    write (lulg,4) rlonlo1,ewlo1,rlonhi1,ewhi1
cx  1 format (' FORECAST VERIFICATION RESULTS FOR ',A,//,
cx   &         ' CASES ELIMINATED WITH VMAX .LE.' ,F5.0,
cx   &         ' AND VMAX .GE.' ,F5.0, ' AT INITIAL OR FORECAST TIME')
cx  2 format (/,' CASES RESTRICTED TO INITIAL VMAX IN THE INTERVAL: ',
cx   &         F6.1,' TO ',F6.1)
cx  3 format (' CASES RESTRICTED TO INITIAL LAT  IN THE INTERVAL: ',
cx   &         F6.1,A1,' TO ',F6.1,A1)
cx  4 format (' CASES RESTRICTED TO INITIAL LON  IN THE INTERVAL: ',
cx   &         F6.1,A1,' TO ',F6.1,A1)
C
C**   PRINT AVERAGE ERRORS
C
      IF ( INTENS .EQ. 0 ) THEN
cx       WRITE ( LULG, 5 )
CC  5 FORMAT(//,' AVERAGE TRACK ERRORS (KM) FOR HOMOGENEOUS SAMPLE')
cx  5 FORMAT(//,' AVERAGE TRACK ERRORS (NM) FOR HOMOGENEOUS SAMPLE')
         write ( lulg, 5 ) unitch( metric+1 )
    5 format(//,' average track errors (',a2,') FOR HOMOGENEOUS SAMPLE')
      ELSE
         WRITE (LULG,6)
    6 FORMAT(//,' AVERAGE INTENSITY ERRORS (KT) FOR HOMOGENEOUS SAMPLE'
     &)
      ENDIF
C
      WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
      DO J = 1,NMODEL
         WRITE ( LULG, 8 ) MNAME(J), ( ERRM(J,K), K = 0, mtau )
    8 FORMAT (1X,A4,4X,8(F6.1,1X))
      enddo
C
      WRITE (LULG,9) (NHCASE(K),K = 0,mtau)
    9 FORMAT (1X,'#CASES   ',8(I4,3X))
C
C**   PRINT spreadsheet FORM OF THE AVERAGE ERRORS
C
      IF (INTENS .EQ. 0) THEN
         WRITE (LUHV,5)
      ELSE
         WRITE (LUHV,6)
      ENDIF
C
      WRITE (LUHV,11) (MNAME(J), J = 1,NMODEL)
   11 FORMAT (/,'    #, FPD,',2X,15(a4,',  '))
cc   11 FORMAT (/,' FPD   #',3X,15(2X,A4))
C
      DO K = 0, mtau
c
         WRITE (LUHV,12) nhcase(k),FCSTPD(K),(ERRM(J,K), J = 1,NMODEL)
   12    FORMAT (1X,i4,', ',a3,',',15(F6.1,','))
cc   12    FORMAT (1X,A3,1x,i4,2X,15(F6.1))
c
         IF ( K .gt. 3 ) WRITE (LUHV,'('' '')')

      enddo
C
cc      WRITE (LUHV,'('' n = '',I4,'' at T = 0...n = '',I4,
cc     & '' at T = '',a3)') NHCASE(0),NHCASE(mtau),fcstpd(mtau)
C
C**   PRINT ERROR STANDARD DEVIATION
C
cx    WRITE (LULG,801)
cx801 FORMAT(//,' ERROR STANDARD DEVIATION (NM) FOR HOMOGENEOUS SAMPLE')
      write (lulg,801) unitch( metric + 1 )
  801 FORMAT(//,' ERROR STANDARD DEVIATION (',a2,
     &') FOR HOMOGENEOUS SAMPLE')
C
      WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
      DO J = 1, NMODEL
         WRITE ( LULG, 8 ) MNAME(J), ( STDEV(J,K), K = 0, mtau )
      enddo
C
      WRITE (LULG,9) (NHCASE(K),K = 0, mtau)
C
C**   PRINT HARVARD GRAPHICS FORM OF THE AVERAGE ERRORS
C
cc      WRITE (LUHV,801)
C
cc      WRITE (LUHV,11) (MNAME(J), J = 1,NMODEL)
C
cc      DO K = 0, mtau
c
cc         WRITE (LUHV,12) FCSTPD(K),nhcase(k),(stdev(J,K), J = 1,NMODEL)
c
cc         IF ( K .gt. 3 ) WRITE (LUHV,'('' '')')

cc      enddo
C
cc      WRITE (LUHV,'('' n = '',I4,'' at T = 0...n = '',I4,
cc     & '' at T = '',a3)') NHCASE(0),NHCASE(mtau),fcstpd(mtau)
C
C**   PRINT AVERAGE XBIAS FOR THE FORECASTS
C
      IF (INTENS .EQ. 0) THEN
CC        WRITE (LULG,'(/,'' AVERAGE XBIAS (KM) FOR HOMOGENEOUS SAMPLE''
CC   &     )')
cx        WRITE (LULG,'(/,'' AVERAGE XBIAS (NM) FOR HOMOGENEOUS SAMPLE''
cx   &     )')
          WRITE (LULG, 711) unitch( metric + 1 )
  711 FORMAT (/,' AVERAGE XBIAS (',a2,') FOR HOMOGENEOUS SAMPLE')
      ELSE
          WRITE (LULG,'(/,'' AVERAGE INTENSITY BIAS (KT) FOR HOMOGENEOUS
     & SAMPLE'')')
C
C**   PRINT OUT spreadsheet FORM FOR THE INTENSITY BIAS
C
          WRITE (LUHV,'(/,'' AVERAGE INTENSITY BIAS (KT) FOR HOMOGENEOUS
     & SAMPLE'')')
C
          WRITE (LUHV,11) (MNAME(J), J = 1,NMODEL)
C
C
          DO K = 0, mtau
c
             WRITE (LUHV,12) nhcase(k),FCSTPD(K),
     &                       (xbiasm(J,K), J = 1,NMODEL)
c
             IF ( K .gt. 3 ) WRITE (LUHV,'('' '')')

          enddo
C
cc          WRITE (LUHV,'('' n = '',I4,'' at T = 0...n = '',I4,
cc     &     '' at T = '',a3)') NHCASE(0),NHCASE(mtau),fcstpd(mtau)
C
      ENDIF
C
      WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
      DO J = 1, NMODEL
         WRITE ( LULG,8 ) MNAME(J), ( XBIASM(J,K), K = 0, mtau )
      enddo
C
      WRITE (LULG,9) (NHCASE(K),K = 0,mtau)
C
      IF ( INTENS .EQ. 0 ) THEN
C
C**   PRINT AVERAGE YBIAS FOR THE FORECASTS
C
cx       WRITE ( LULG, 511 )
CC511    FORMAT(/,1X,'AVERAGE YBIAS (KM) FOR HOMOGENEOUS SAMPLE')
cx511    FORMAT(/,1X,'AVERAGE YBIAS (NM) FOR HOMOGENEOUS SAMPLE')
         write ( lulg, 511 ) unitch( metric + 1 )
  511    format(/,1X,'AVERAGE YBIAS (',a2,') FOR HOMOGENEOUS SAMPLE')
C
C
         WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
         DO J = 1, NMODEL
            WRITE ( LULG, 8 ) MNAME(J), ( YBIASM(J,K), K = 0, mtau )
         enddo
C
         WRITE ( LULG, 9 ) ( NHCASE(K), K = 0, mtau )
C
      ENDIF
C
C**   PRINT ERRORS RELATIVE TO EACH MODEL
C
      DO NN = 1,NMODEL
        WRITE (LULG,521) MNAME(NN)
  521   FORMAT(//,1X,'AVERAGE ERRORS RELATIVE TO ',A,' (%)')
C
        WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
        DO J = 1, NMODEL
          WRITE ( LULG, 8 ) MNAME(J), ( RECLIP(J,NN,K), K = 0, mtau )
        enddo
C
        WRITE ( LULG, 9 ) ( NHCASE(K), K = 0, mtau )
C
      enddo
C
C**   PRINT spreadsheet FORM OF ERRORS RELATIVE TO EACH MODEL
C
      DO 543 NN = 1,NMODEL
C
        IF (INTENS.EQ.0.AND.MNAME(NN).NE.'CLIP') GO TO 543
        IF (INTENS.EQ.1.AND.MNAME(NN).NE.'SHFR') GO TO 543
C
        WRITE (LUHV,521) MNAME(NN)
C
        WRITE (LUHV,11) (MNAME(J), J = 1,NMODEL)
C
        DO K = 0, mtau
c
           WRITE (LUHV,12) nhcase(k),FCSTPD(K),
     &                     (RECLIP(J,NN,K), J = 1,NMODEL)
c
           IF ( K .gt. 3 ) WRITE (LUHV,'('' '')')

        enddo
C
cc        WRITE (LUHV,'('' n = '',I4,'' at T = 0...n = '',I4,
cc     &   '' at T = '',a3)') NHCASE(0),NHCASE(mtau),fcstpd(mtau)
c
  543 CONTINUE
C
C**   PRINT FREQUENCIES OF SUPERIOR PERFORMANCE by percent
C
      WRITE (LULG,'(/,'' FREQUENCY OF SUPERIOR PERFORMANCE (%)'')')
C
C
      WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
      DO J = 1, NMFSP
         WRITE ( LULG, 8 ) MNAME(J), ( FSP(J,K), K = 0, mtau )
      enddo
C
C**   PRINT FREQUENCIES OF SUPERIOR PERFORMANCE by number
C
      WRITE (LULG,'(/,'' FREQUENCY OF SUPERIOR PERFORMANCE (number)'')')
C
      WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
      DO J = 1, NMFSP
         WRITE ( LULG, 548 ) MNAME(J), (NFSP(J,K), K = 0, mtau )
 548     FORMAT (1X,A4,3X,8(i6,1X))
      enddo
C
      WRITE ( LULG, 549 ) ( nfcase(K), K = 0, mtau )
 549  FORMAT (1X,'#TOTAL   ',8(I4,3X))
      WRITE ( LULG, 9 ) ( NHCASE(K), K = 0, mtau )

C
C**   PRINT PROBABILITIES FOR SIGNIFICANCE TESTS
C
      DO K = 0, mtau
c
         WRITE (LULG,551) KTIME(K),NHCASE(K)
  551    FORMAT (/,1X,'PROBABILITIES FOR MODEL DIFFERENCES AT T= ',
     &             I3,'  SAMPLE SIZE=',I4)
         WRITE (LULG,552) (MNAME(JJ),JJ = 2,NMODEL)
  552    FORMAT (6X,10(A4,2X))
c
         DO J = 1, NMODEL - 1
            WRITE (LULG,553) MNAME(J),(PROB(J,JJ,K),JJ = 2,NMODEL)
  553       FORMAT (1X,A4,1X,10(F5.3,1X))
         enddo
c
      enddo
C
C**   PRINT PROBABILITIES WITH ADJUSTED SAMPLE SIZE
C
      WRITE(LULG,571) SAMADJ
  571 FORMAT (//,1X,' SAMPLE SIZE ADJUSTED FOR ',F5.1,
     &              ' HOUR SERIAL CORRELATION')
      DO K = 0, mtau
c
         RNHA = RNHAA(K)
         WRITE (LULG,572) KTIME(K),RNHA
  572    FORMAT (/,1X,'ADJUSTED PROBABILITIES AT T= ',
     &             I3,' ADJUSTED SAMPLE SIZE=',F6.1)
         WRITE (LULG,552) (MNAME(JJ),JJ=2,NMODEL)
c
         DO J = 1, NMODEL - 1
            WRITE (LULG,553) MNAME(J),(PROBA(J,JJ,K),JJ = 2,NMODEL)
         enddo
      enddo
C
C**   PRINT AVERAGE ERRORS FOR THE INDIVIDUAL CASES
C
      IF ( IERRPR .EQ. 1 ) THEN
c
         IF ( INTENS .EQ. 0 ) THEN
CC           WRITE (LULG,'(//,'' TRACK ERRORS (KM) FOR HOMOGENEOUS SAMPL
CC   &E'')')
cx           WRITE (LULG,'(//,'' TRACK ERRORS (NM) FOR HOMOGENEOUS SAMPL
cx   &E'')')
             write (lulg, 573) unitch ( metric + 1 ) 
  573        format(//,' TRACK ERRORS (',a2,') FOR HOMOGENEOUS SAMPLE ')
         ELSE
             WRITE (LULG,'(//,'' INTENSITY ERRORS (KTS) FOR HOMOGENEOUS
     &SAMPLE'')')
         ENDIF
C
         DO I = 1, NHCASE(0)
            WRITE (LULG,'(/,1X,A8,2X,A10,2X,A10,3(2X,F6.1))') FHNAME(I),
     &       SHNAME(I),CHDATE(I),BHLAT(I),BHLON(I),BHVMAX(I)
C
            WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
            DO J = 1, NMODEL
               IF ( INTENS .EQ. 0 ) THEN
                  WRITE ( LULG, 8 ) MNAME(J), ( ERR(J,I,K), K = 0,mtau)
               ELSE
                  WRITE ( LULG, 8 ) MNAME(J), (XBIAS(J,I,K),K = 0,mtau)
               ENDIF
            enddo
         enddo
C
      ENDIF
C
C**   CALCULATE AND PRINT THE AVERAGE ERRORS FOR EACH STORM
C
      IF ( ISTMPR .EQ. 1 ) THEN
         ISTORM = 0
c
         IF ( INTENS .EQ. 0 ) THEN
CC           WRITE (LULG,'(//,'' TRACK ERRORS (KM) FOR HOMOGENEOUS SAMPL
CC   &E'')')
cx           WRITE (LULG,'(//,'' TRACK ERRORS (NM) FOR HOMOGENEOUS SAMPL
cx   &E'')')
             write (lulg,574)unitch( metric + 1)
  574        format(//,' TRACK ERRORS (',a2,') FOR HOMOGENEOUS SAMPLE')
         ELSE
             WRITE (LULG,'(//,'' INTENSITY ERRORS (KTS) FOR HOMOGENEOUS
     &SAMPLE'')')
         ENDIF
C
         DO I = 1, NDATAF
            ICASE = 0
C
            DO J = 1, NHCASE(0)
               IF ( FLNAME(I). EQ. FHNAME(J) ) THEN
                   ICASE = ICASE + 1
                   DO K = 1, NMODEL
                      DO L = 0, mtau
                         ERRS(K,ICASE,L) = ERR(K,J,L)
                      enddo   
                   enddo
               ENDIF
            enddo
C
            DO L = 0, mtau
               ICASECT(L) = ICASE
               DO K = 1, NMODEL
                  ERROR(K,L) = 0.0
               enddo   
            enddo
C
            DO J = 1, ICASE
               DO K = 1, NMODEL
                  DO L = 0, mtau
                     IF ( ERRS(K,J,L) .NE. 9999.0 ) THEN
                        ERROR(K,L) = ERROR(K,L) + ERRS(K,J,L)
                     ELSE
                        IF (K.EQ.1) ICASECT(L) = ICASECT(L) - 1
                     ENDIF
                  enddo
               enddo   
            enddo
C
            DO L = 0, mtau
               DO K = 1, NMODEL
                  IF ( ICASECT(L) .NE. 0.0 ) THEN
                     ERROR(K,L) = ERROR(K,L)/ICASECT(L)
                  ELSE
                     ERROR(K,L) = 9999.0
                  ENDIF
               enddo   
            enddo
C
            IF ( INTENS .EQ. 0 ) THEN
cx              WRITE (LULG,61) FLNAME(I),SFNAME(I)
cx 61           FORMAT(//,' FORECAST ERRORS (KM) FOR ',A8,2X,A10)
cx 61           FORMAT(//,' FORECAST ERRORS (NM) FOR ',A8,2X,A10)
                write (lulg,61) unitch( metric + 1 ),flname(i),sfname(i)
   61           format(//,' forecast errors (',a2,') FOR ',A8,2X,A10)
            ELSE
                WRITE (LULG,62) FLNAME(I),SFNAME(I)
   62           FORMAT(//,' FORECAST ERRORS (KT) FOR ',A8,2X,A10)
            ENDIF
C
            WRITE ( LULG, '(7x,8(4x,a3))' ) ( fcstpd(k), k = 0, mtau )
C
            DO K = 1, NMODEL
               WRITE ( LULG, 8 ) MNAME(K), (ERROR(K,L), L = 0, mtau )
            enddo
C
            WRITE ( LULG, 9 ) ( ICASECT(L), L = 0, mtau )
C
        enddo
C
      ENDIF
C
C**   PRINT TRACKS OF ALL POSSIBLE CASES
C
      IF ( ITRKPR .EQ. 1 ) THEN
C
         IF ( INTENS .EQ. 0 ) THEN
            WRITE ( LULG, '(//,'' TRACKS FOR ALL CASES'')' )
         ELSE
            WRITE ( LULG, '(//,'' INTENSITY FOR ALL CASES'')' )
         ENDIF
C
         DO I = 1, NCASE
c
            IF ( INTENS .EQ. 0 ) THEN
c
               WRITE (LULG,71) FNAME(I),SNAME(I),CCDATE(I)
   71          FORMAT (/,1X,A8,2X,A10,2X,A10)
C
               WRITE ( LULG, '(8x,a3,7(10x,a3))' ) 
     &               ( fcstpd(k), k = 0, mtau )
C
               WRITE (LULG,72) (BTLAT(I,K),BTLON(I,K), K=0,mtau)
   72          FORMAT('BTRK',8(F5.1,1X,F5.1,2X))
C
               DO J = 1, NMODEL
                  WRITE (LULG,73) MNAME(J),
     &                             (YLAT(J,I,K),XLON(J,I,K), K = 0,mtau)
   73             FORMAT (A4,8(F5.1,1X,F5.1,2X))
               enddo
c
            ELSE
c
               WRITE (LULG,71) FNAME(I),SNAME(I),CCDATE(I)
C
               WRITE ( LULG, '(7x,a3,7(6x,a3))' ) 
     &               ( fcstpd(k), k = 0, mtau )
C
               WRITE (LULG,74) (BTVMAX(I,K), K = 0,mtau)
   74          FORMAT('BTRK',8(F7.1,2X))
               DO J = 1, NMODEL
                  WRITE (LULG,75) MNAME(J),(VMAX(J,I,K),K = 0,mtau)
   75             FORMAT (A4,8(F7.1,2X))
               enddo
c
            ENDIF
c
         enddo
C
      ENDIF
C
      CLOSE (LULG)
      CLOSE (LUHV)
C
      STOP ' NORMAL END TO THE TRUTH'
C
C**   ERROR MESSAGES
C
 1010 WRITE (*,*) ' ERROR OPENING input DATA FILE = ',IOS
      STOP
C
 1020 WRITE (*,*) ' ERROR OPENING output DATA FILE = ',IOS
      STOP
C
 1030 WRITE (*,*) ' ERROR OPENNING THE A-DECK = ',IOS
      STOP
C
 1040 WRITE (*,*) ' ERROR OPENNING THE B-DECK = ',IOS
      STOP
C
 1050 WRITE (*,*) ' ERROR READING THE A-DECK (MAYBE NO COMB) = ',IOS
      STOP
C
 1060 WRITE (*,*) ' ERROR READING THE B-DECK = ',IOS
      STOP
C
      END
C***********************************************************************
      FUNCTION TDF (T,DF)
C
      IMPLICIT REAL*8 (A-H,O-Z)
CC    REAL*8 PROB,BETAI,TDF,T,DF
C
      B = 0.5
      PROB = BETAI (0.5 * DF,B,DF / (DF + T**2))
C
      TDF = (PROB - 2.0) / (-2.0)
C
      RETURN
      END
C***********************************************************************
      FUNCTION BETAI(A,B,X)
C
C**   RETURNS THE INCOMPLETE BETA FUNCTION IX(A,B).
C
C**   TAKEN FROM PRESS ET AL., NUMERICAL RECIPES, PP 166FF
C
      IMPLICIT REAL*8 (A-H,O-Z)
CC    REAL*8 BETAI,BT,A,B,X,GAMMLN,BETACF
C
      IF (X.LT.0.0.OR.X.GT.1.0) WRITE (6,'('' BAD ARGUMENT X IN BETAI'')
     & ')
      IF (X.EQ.0.0.OR.X.EQ.1.0) THEN
          BT = 0.0
      ELSE
C
C**   FACTORS IN FORM OF THE CONTINUED FRACTION
C
          BT = EXP (GAMMLN(A + B) - GAMMLN(A) - GAMMLN(B)
     &     + A*LOG(X) + B*LOG(1.0 - X))
        END IF
C
      IF (X.LT.(A + 1.0)/(A + B + 2.0)) THEN
C
C**   USE CONTINUED FRACTION DIRECTLY
C
          BETAI = BT*BETACF(A,B,X)/A
C
          RETURN
      ELSE
C
C**   USE CONTINUED FRACTION AFTER MAKING THE SYMMETRY TRANSFORMATION
C
          BETAI = 1.0 - BT*BETACF(B,A,1.0 - X)/B
C
          RETURN
C
      END IF
C
      END
C***********************************************************************
      FUNCTION BETACF(A,B,X)
C
C**   CONTINUED FRACTION FOR INCOMPLETE BETA FUNCTION, BETAI
C
C**   TAKEN FROM PRESS ET AL., NUMERICAL RECIPES, P. 168
C
      IMPLICIT REAL*8 (A-H,O-Z)
C
      PARAMETER (ITMAX = 100)
      PARAMETER (EPS = 3.E-27)
C
      AM = 1.0
      BM = 1.0
      AZ = 1.0
C
C**   THESE Q'S WILL BE USED IN FACTORS WHICH OCCUR IN THE
C**     COEFFICIENTS (6.3.6)
C
      QAB = A + B
      QAP = A + 1.0
      QAM = A - 1.0
      BZ  = 1.0 - QAB*X/QAP
C
C**   CONTINUED FRACTION EVALUATION BY THE RECURRENCE METHOD (5.2.5)
C
      DO 10 M = 1,ITMAX
         EM  = M
         TEM = EM + EM
         D   = EM*(B - M)*X/((QAM + TEM)*(A + TEM))
C
C**   ONE STEP (THE EVEN ONE) OF THE RECURRENCE
C
        AP = AZ + D*AM
        BP = BZ + D*BM
        D  = - (A + EM)*(QAB + EM)*X/((A + TEM)*(QAP + TEM))
C
C**   NEXT STEP OF THE RECURRENCE (THE ODD ONE)
C
        APP = AP + D*AZ
        BPP = BP + D*BZ
C
C**   SAVE THE OLD ANSWER
C
        AOLD = AZ
C
C**   RENORMALITIES TO PREVENT OVERFLOWS
C
        AM = AP/BPP
        BM = BP/BPP
        AZ = APP/BPP
        BZ = 1
C
C**   ARE WE DONE?
C
        IF (ABS(AZ - AOLD).LT.EPS*ABS(AZ)) GO TO 20
C
   10 CONTINUE
C
      WRITE (6,'('' A OR B TOO BIG, OR ITMAX TOO SMALL'')')
C
   20 BETACF = AZ
C
      RETURN
      END
C***********************************************************************
      FUNCTION GAMMLN (XX)
C
C**   RETURNS THE VALUE OF LN [GAMMA (XX)] FOR XX > 0
C**     FULL ACCURACY IS OBTAINED FOR XX > 1
C**     FOR 0 < XX < 1, THE REFLECTION FORMULA 6.1.4 CAN BE USED FIRST
C**     TAKEN FROM PRESS ET AL., NUMERICAL RECIPES, PP 156FF
C
      IMPLICIT REAL*8 (A-H,O-Z)
      REAL*8 XX,GAMMLN
      REAL*8 COF(6),STP,HALF,ONE,FPF,X,TMP,SER
C
C**   INTERNAL ARITHMETIC WILL BE DONE IN DOUBLE PRECISION, A NICETY
C**     THAT YOU CAN OMIT IF FIVE-FIGURE ACCURACY IS GOOD ENOUGH.
C
      DATA COF /76.18009173D0 ,-86.50532033D0,  24.01409822D0,
     &          -1.231739516D0,   .120858003D-2, -.536382D-5/
      DATA STP / 2.50662827465D0/
      DATA HALF /0.5D0/, ONE /1.0D0/, FPF /5.5D0/
C
      X   = XX - ONE
      TMP = X + FPF
      TMP = (X + HALF)*LOG(TMP) - TMP
      SER = ONE
C
      DO 10 J = 1,6
         X = X + ONE
         SER = SER + COF(J)/X
   10 CONTINUE
C
      GAMMLN = TMP + LOG(STP*SER)
C
      RETURN
      END
cx
cxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcxcx
cx
      subroutine readin(lulg,mxnmd,intens,metric,ierrpr,istmpr,itrkpr,
     &                 vmhi, vmlo, vmver1, vmver, 
     &                 rlathi, rlatlo, rlonlo, rlonhi, startdtg, enddtg, 
     &                 int00, int06, int12, int18, nmodel, mname )
cx
cx  Read the data at the top of the configuration file.
cx  Individual storms are read in a loop within the main program.
cx
cx  input parameters:
cx                    lulg  - integer, output file lu for run.
cx                    mxnmd - integer, maximum number of fcst models
cx  passed back to main:
cx                    intens - integer, 1=do intensity, 0=do track
cx                    metric - integer, 1=metric, 0=english
cx                    ierrpr - integer, 1=individual storm averages
cx                    istmpr - integer, 1=all storm errors processed
cx                    itrkpr - integer, 1=all lat/lon values processed
cx                    vmhi   - real, upper limit of initial vmax
cx                    vmlo   - real, lower limit of initial vmax
cx                    vmver1 - restrict cases to those verifying best track
cx                             max winds lower than vmver1 (kts).
cx                    vmver -  restrict cases to those verifying best track
cx                             max winds greater than vmver (kts).
cx                    rlathi - real, northern limit of verifying latitude
cx                    rlatlo - real, southern limit of verifying latitude
cx                    rlonlo - real, eastern limit of verifying longitude
cx                    rlonhi - real, western limit of verifying longitude
cx                    startdtg - character*10, starting dtg (MMDDHH) of evaluation
cx                    enddtg - character*10, ending dtg (MMDDHH) of evaluation
cx                    int00  - boolean, .true.=include 00 forecasts in evaluation
cx                    int06  - boolean, .true.=include 06 forecasts in evaluation
cx                    int12  - boolean, .true.=include 12 forecasts in evaluation
cx                    int18  - boolean, .true.=include 18 forecasts in evaluation
cx                    nmodel - integer, number of models to evaluate
cx                    mname -  char array,  model ids to evaluate
      integer        intens 
      integer        metric 
      integer        ierrpr, istmpr, itrkpr
      real           vmhi, vmlo, vmver1, vmver 
      real           rlathi, rlatlo
      character*10   startdtg, enddtg
      logical        int00, int06, int12, int18
      integer        nmodel 
      character*4    mname(mxnmd)
      character*80   line
      integer        ind
      integer        i
      
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
cx    parameter (track or intensity)
      ind = index(line,':')
      intens = 0
      if (line(ind:ind+10) .eq. ': intensity') intens = 1
cx    units (english or metric)
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      metric = 0
      if (line(ind:ind+7) .eq. ': metric') metric = 1
cx    individual storm averages
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      istmpr = 0
      if (line(ind:ind+7) .eq. ': .true.') istmpr = 1
cx    all storm errors processed
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      ierrpr = 0
      if (line(ind:ind+7) .eq. ': .true.') ierrpr = 1
cx    all lat/lon values processed
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      itrkpr = 0
      if (line(ind:ind+7) .eq. ': .true.') itrkpr = 1
cx    initial vmax must be below ....
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      vmhi = 250.0
      read(line(ind+1:ind+4), *) vmhi
cx    initial vmax must be above ....
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      vmlo = 0.0
      read(line(ind+1:ind+4), *) vmlo
cx    verifying vmax must be below vmver1
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      vmver1 = 250.0
      read(line(ind+1:ind+4), *,err=1015) vmver1
cx    verifying vmax must be above vmver
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      vmver = 0.0
      read(line(ind+1:ind+4), *) vmver
cx    verifying lat must be below ....
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      rlathi = 90.0
      read(line(ind+1:ind+4), '(f4.0)',err=1015) rlathi
      if (line(ind+5:ind+5) .eq. 'S') rlathi = -rlathi
cx    verifying lat must be above ....
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      rlatlo = 0.0
      read(line(ind+1:ind+4), '(f4.0)',err=1015) rlatlo
      if (line(ind+5:ind+5) .eq. 'S') rlatlo = -rlatlo
cx    verifying lon must be above (west) of this lon
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      rlonlo = 0.0
      read(line(ind+1:ind+4), '(f4.0)',err=1015) rlonlo
      if (line(ind+5:ind+5) .eq. 'E') rlonlo = 360-rlonlo
cx    verifying lon must be below (east) of this lon
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      rlonhi = 0.0
      read(line(ind+1:ind+4), '(f4.0)',err=1015) rlonhi
      if (line(ind+5:ind+5) .eq. 'E') rlonhi = 360-rlonhi
cx    no dates before this date...
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      startdtg = line(ind+2:ind+7)
cx    no dates after this date...
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      enddtg = line(ind+2:ind+7)
cx    process errors for initial 00 hr
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      int00 = .true.
      read (line(ind+2:ind+7), '(l6)',err=1015) int00
cx    process errors for initial 06 hr
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      int06 = .true.
      read (line(ind+2:ind+7), '(l6)',err=1015) int06
cx    process errors for initial 12 hr
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      int12 = .true.
      read (line(ind+2:ind+7), '(l6)',err=1015) int12
cx    process errors for initial 18 hr
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      int18 = .true.
      read (line(ind+2:ind+7), '(l6)',err=1015) int18
cx    read the number of models        
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      ind = index(line,':')
      read (line(ind+2:ind+4), *,err=1015) nmodel
cx    read the model ids     
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      read(11,'(a80)',err=1015)line
      write (lulg,'(a80)') line
      read(line,'(10(a4,1x))',err=1015) (mname(i), i = 1, nmodel)
      ind = index(line,':')
cx    read a blank line. read specific storm ids later in code
      read(11,'(a80)',err=1015)line
      return
 1015 continue
      write (lulg, *) ' Unexpected line in configuration file:',line
      stop
      end
