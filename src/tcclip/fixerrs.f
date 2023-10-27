      PROGRAM DET1FIX
c
c
c   This program computes fix errors given the best track and 
c   fixes for a storm.
c
c   command line input:
c               arg1=strmid  (wp0399)
c               arg2=century (19)
c
c   files:
c               unit1 = best track
c               unit2 = fixes
c               unit3 = output
c               unit4 = fixerrs.in (options for execution - see file)
c
c  variables:
c
c  original programmer:  unknown
c  current programmer:   sampson, nrl
c
c
c  change record:
c                  converted to ATCF 3.0     sampson, nrl Nov 95
c
c    Modified to use new data format   A. Schrader, SAIC  7/98
c    Modified to use cent - current posit century  B. Sampson, NRL 11/98
c    Modified to compute stats for scatterometer fixes, Schrader, 7/99
c    Attempted some cleanup of old code.  Schrader, 7/99  
c      (Made the subroutines: fileopener, readinput, satdecode, 
c       scatdecode, and interpBT.  Substituted do-enddo's and if-endif's
c       for some goto's.)
c
c
c
      common /pcn/ npcn(3),nflag(3),plimit(3)

      DIMENSION YB(300),XB(300),TB(300),ER(4,5)
      DIMENSION NO(4),TC(10)
cx    CHARACTER*20 BSTFIL,FIXFIL
      CHARACTER*14 SITETYPE(3)
      INTEGER*4 MDHM

c     KPD  JH experienced an integer overflow without this next line.

      integer*4 JH

c     KPD  Toss these in for good measure.

      integer*4 JD
      integer*4 itothr
      integer*4 idayhr


      CHARACTER*1 IX,LATNS,LONGEW,IPCN,ACC,RR,A
      CHARACTER*1 CONF
      CHARACTER*4 SITE(20),TYPE,SATLITE,ISITE,RACC,RT,
     &            RX,RY,RZ
      CHARACTER*4 SCATSITE
      CHARACTER*8 SCTX,SCTY,SCTZ
      CHARACTER*8 SCTCONF
      CHARACTER   TC*14,FIX*78,SATNUM*2,BIRD*2
      CHARACTER   fixrecd*80
      CHARACTER*1 SAT,AIR,RAD,SCAT,INDIVD,flag,GMSFLG
      CHARACTER*2 XL
      character*6    strmid
      character*2    cent
      character*8    btdtg
      integer        iwind, ios
      integer        ioerror
      real           btlat, btlon
      LOGICAL        BTeof
      logical        skip
	    
C INITIALIZE ALL VARIABLES
      DATA EGNUM,EGSUM,YSQEG,XSQEG,EGNAN,EGSAN,EGNDN,EGSDN /8*0.0/
      DATA EENUM,EESUM,YSQEE,XSQEE,EENAN,EESAN,EENDN,EESDN /8*0.0/
      DATA CGNUM,CGSUM,YSQCG,XSQCG,CGNAN,CGSAN,CGNDN,CGSDN /8*0.0/      
      DATA CENUM,CESUM,YSQCE,XSQCE,CENAN,CESAN,CENDN,CESDN /8*0.0/
      DATA BGNUM,BGSUM,YSQBG,XSQBG,BGNAN,BGSAN,BGNDN,BGSDN /8*0.0/
      DATA BENUM,BESUM,YSQBE,XSQBE,BENAN,BESAN,BENDN       /7*0.0/
      DATA AC,RG,RF,RP,AC2,RG2,RF2,RP2 /8*0.0/
      DATA SCTG,SCTF,SCTP,SCTG2,SCTF2,SCTP2 /6*0.0/
      DATA IAC,IRG,IRF,IRP,IGMS,IGMSE,IGMSC,IGMSO /8*0/
      DATA ISCTG,ISCTF,ISCTP /3*0/
      DATA OTHER /0.0/, IOTHER /0/
      DATA GMS,GMSS,GMSE,GMSC,GMSO,GMSESQ,GMSCSQ,GMSOSQ /8*0.0/
      DATA STDEV0,STDEV1,STDEV2,STDEV3 /4*0.0/
      DATA ICHECK,IFWFS /2*0/
      DATA SAT,SCAT,RAD,AIR,INDIVD,GMSFLG /6*' '/
      DATA SITE /20*'    '/
      DATA SITETYPE /'SELECTED SITE','DMSP SITES','ALL SITES'/
C      DATA SITETYPE /'SELECTED SITES','DMSP SITES','ALL SITES'/

c***********************************************************************
      plimit(1) = 30.0
      plimit(2) = 45.0
      plimit(3) = 60.0

      DEGRAD=3.14159/180.

      J=1
      TYPE = '    '
      SATNUM = '  '
C 
C
C  1 = BEST TRACK
C  2 = FIXES
C  3 = OUTPUT
C  4 = INPUT PARAMETERS
C
cx
cx  Get command line arguements and
cx  open best track, fixes, output and input files.
cx
      call fileopener( strmid, ioerror )
      if( ioerror .ne. 0 ) goto 9000


cx   Read input parameter file.

      call readinput( sat,scat,air,rad,nsite,numsite,site,type,satnum,
     &     indivd,gmsflg,ioerror )
      if( ioerror .gt. 0 ) goto 9000

      BTeof = .FALSE.
 9999 CONTINUE
C
      do i=1,3
         npcn(i) = 0
         nflag(i) = 0
      enddo
      DO I=1,300
         TB(I)=-99
         XB(I)=-99
         YB(I)=-99
      enddo
      N=0
      IYEAR=0
      IYR=0
      NYR=IYR
c
c     Read the storm number from the best-track file
      read( 1, '(4x,i2)' ) ISTRM
      backspace 1
    2 CONTINUE
C READ AND STORE BEST TRACK
      ios = 0
      call readBT( 1,cent,btdtg,btlat,LATNS,btlon,LONGEW,iwind,ios )
      if( ios .lt. 0 ) goto 5
      if( ios .eq. 0 ) then
         read( btdtg, '(i2,i6)' ) IYR, MDHM
         LAT = anint( btlat*10.0 )
         LONG = anint( btlon*10.0 )
C
C  IF THIS IS THE FIRST BEST TRACK POSIT FOR THE STORM, SAVE THE STORM
C  NUMBER INTO ISTRM
C
         IF(LATNS.EQ.'S') LAT=-LAT
         IF(LONGEW.EQ.'W') LONG=3600-LONG 
         N=N+1
         CALL JUDA(NYR,IYR,MDHM,MN,TB(N))
         JH=TB(N)+.5
         JD=JH/24
         YB(N)=FLOAT(LAT)/10.
         XB(N)=FLOAT(LONG)/10.
C     
C     WRITE HEADER FOR INDIVIDUAL STATS IF THEY WERE REQUESTED
C     
         IF (N .EQ. 1 .AND. INDIVD .EQ. 'Y') THEN 
            call upcase (strmid,6)
            WRITE (3,'(/''  *** STORM '',a6,'' ***''/)') strmid
            call locase (strmid,6)
            WRITE (3,76)
 76         FORMAT(/,4X,'FIX     SITE    TYPE   PCN  MMDDHHMM     AZ'
     &           '     DST     N-S     E-W',/)
         ENDIF
      endif
      GO TO 2
C
C   READ FIX THEN COMPARE TO BEST TRACK.
C
 5    BTeof = .TRUE.
C
 9007 READ(2,63,END=21) IX,fixrecd
   63 FORMAT(A1,A80)
cajs   Assign fixes to be the old style record format,
c      with 2 digit vs 4 digit year.  10/98  ajs 
      FIX(1:2) = fixrecd(1:2)
      FIX(3:78) = fixrecd(5:80)
C
C  COMPARE THE LINE JUST READ TO THE STORM NUMBER WE ARE WORKING ON
C  RIGHT NOW (ISTRM).  IF IT'S DIFFERENT, BACKSPACE THE FIXES FILE
C  AND GO READ THE NEXT BEST TRACK.
C
      READ (FIX,'(I2)') IFSTRM
      IF (IFSTRM .NE. ISTRM) THEN
         IF ( BTeof ) GOTO 21
         BACKSPACE 2
         call pcnstat
         GOTO 9999
      ENDIF
      K=0
C
      IF(IX.EQ.'1'.OR.IX.EQ.'A') K=1
      IF(IX.EQ.'2'.OR.IX.EQ.'B') K=2
      IF(IX.EQ.'3'.OR.IX.EQ.'C') K=3
      IF(IX.EQ.'5'.OR.IX.EQ.'E') K=5
      IF(K.EQ.0) GO TO 9007
C
C     Decode the fix record.
C
      IF(SAT.EQ.'Y'.AND.K.EQ.1) then
         call satdecode( fix,site,numsite,type,satnum,kind,jyr,mdhm,mn,
     &        lat,latns,long,longew,ipcn,satlite,bird,isite,ifwfs,skip )
         if( .not.skip ) goto 7
      ELSE IF(AIR.EQ.'Y'.AND.K.EQ.2) then
C       AIRCRAFT DECODE SECTION
         KIND=2
         READ (FIX,35) JYR,MDHM,MN,LAT,LATNS,LONG,LONGEW,IFT,MB,MSN
 35      FORMAT(2X,I2,I6,I2,I3,A1,I4,A1,I2,I3,50X,I2)
         GO TO 7
      ELSE IF(RAD.EQ.'Y'.AND.K.EQ.3) then
C       RADAR DECODE SECTION
         KIND=3
         READ (FIX,37) JYR,MDHM,MN,LAT,LATNS,LONG,LONGEW,RR,ACC
 37      FORMAT(2X,I2,I6,I2,I3,A1,I4,3A1) 
         GO TO 7
      ELSE IF(SCAT.EQ.'Y'.AND.K.EQ.5) then 
         call scatdecode( fix,site,numsite,kind,jyr,mdhm,mn,
     &        lat,latns,long,longew,conf,scatsite,ifwfs,skip )
         if( .not.skip ) goto 7
      endif
      GO TO 9007
C
C
    7 CALL JUDA(NYR,JYR,MDHM,MN,TX)
      JH = TX+.5
      JD = JH/24+1 
C   MAKE SURE FIX TIME IS WITHIN BEST TRACK TIME PERIOD.
      IF(TX.LT.TB(1).OR.TX.GT.TB(N)) THEN
         NO(KIND)=NO(KIND)+1
         GOTO 9007
      ENDIF
C
      IF(LATNS.EQ.'S') LAT=-LAT
      IF(LONGEW.EQ.'W') LONG=3600-LONG 

C   INTERPOLATE A BEST TRACK POINT AS A FUNCTION OF FIX TIME BY MEANS
C   OF A 2ND ORDER LAGRANGIAN POLYNOMIAL ABOUT TIME TB(IT).
      call interpBT( n,tx,tb,xb,yb,x,y )

      XLAT=LAT   
      XLONG=LONG
      YS=XLAT/10.   
      XS=XLONG/10.
      AZ=1.0
C
C COMPUTE ERROR
C
      CALL DIRDST(Y,X,YS,XS,AZ,DST)
      ER(1,J)=AZ
      ER(2,J)=DST
      ER(3,J)=DST*COS(AZ*DEGRAD)
      ER(4,J)=DST*SIN(AZ*DEGRAD)
C
C   GO TO STATISTICS SECTION - BASED ON FIX TYPE (KIND)
      GO TO (81,82,83,84), KIND 
C
C   SATELLITE STATISTICS SECTION
C
   81 CONTINUE

c  check to see if the user wants to compute gms stats separately

      if (GMSFLG .eq. 'Y') THEN
         IF(SATLITE.NE.'DMSP'.AND.SATLITE.NE.'NOAA'.AND.SATLITE.NE.
     1        'TIRO') GOTO 51 
      ENDIF
      ITOTHR = ( JD - 1 ) * 24

      IDAYHR=JH-ITOTHR
      IF(IDAYHR.LT.7.OR.IDAYHR.GT.18) THEN
         KORBT=1
      ELSE
         KORBT=2
      ENDIF
C   KORBT=1 DENOTES AN, KORBT=2 DENOTES DN
C     EG=EYE,GEOGRAPHICAL GRIDDING (PCN 1)
C     EE=EYE,EPHEMERIS GRIDDING (PCN 2)
C     CG=WELL DEFINED CIRCULATION CENTER, GEOGRAPHICAL GRIDDING (PCN 3)
C     CE=WELL DEFINED CIRCULATION CENTER, EPHEMERIS GRIDDING (PCN(4) 
C     BG=POORLY DEFINED CIRCULATION CENTER,GEOGRAPHICAL GRIDDING(PCN 5)
C     BE=POORLY DEFINED CIRCULATION CENTER,EPHEMERIS GRIDDING (PCN 6)
C
      IF(IPCN.EQ.'1') GOTO 301 
      IF(IPCN.EQ.'2') GOTO 302 
      IF(IPCN.EQ.'3') GOTO 303 
      IF(IPCN.EQ.'4') GOTO 304 
      IF(IPCN.EQ.'5') GOTO 305
      GOTO 306 
 301  EGNUM=EGNUM+1.0
      EGSUM=EGSUM+DST
      YSQEG=YSQEG+ER(3,J)**2 
      XSQEG=XSQEG+ER(4,J)**2 
      GO TO (370,371)KORBT
 370  EGNAN=EGNAN+1.
      EGSAN=EGSAN+DST
      GO TO 251
 371  EGNDN=EGNDN+1.
      EGSDN=EGSDN+DST
      GO TO 251
 302  EENUM=EENUM+1.
      EESUM=EESUM+DST
      YSQEE=YSQEE+ER(3,J)**2 
      XSQEE=XSQEE+ER(4,J)**2 
      GO TO (372,373)KORBT
 372  EENAN=EENAN+1.
      EESAN=EESAN+DST
      GO TO 251
 373  EENDN=EENDN+1.
      EESDN=EESDN+DST
      GO TO 251
 303  CGNUM=CGNUM+1.
      CGSUM=CGSUM+DST
      YSQCG=YSQCG+ER(3,J)**2 
      XSQCG=XSQCG+ER(4,J)**2 
      GO TO (374,375)KORBT
 374  CGNAN=CGNAN+1.
      CGSAN=CGSAN+DST
      GO TO 251
 375  CGNDN=CGNDN+1.
      CGSDN=CGSDN+DST
      GO TO 251
 304  CENUM=CENUM+1
      CESUM=CESUM+DST
      YSQCE=YSQCE+ER(3,J)**2 
      XSQCE=XSQCE+ER(4,J)**2 
      GO TO (376,377)KORBT
 376  CENAN=CENAN+1.
      CESAN=CESAN+DST
      GO TO 251
 377  CENDN=CENDN+1.
      CESDN=CESDN+DST
      GO TO 251
 305  BGNUM=BGNUM+1.
      BGSUM=BGSUM+DST
      YSQBG=YSQBG+ER(3,J)**2 
      XSQBG=XSQBG+ER(4,J)**2 
      GO TO (378,379)KORBT
 378  BGNAN=BGNAN+1.
      BGSAN=BGSAN+DST
      GO TO 251
 379  BGNDN=BGNDN+1.
      BGSDN=BGSDN+DST
      GO TO 251
 306  BENUM=BENUM+1.
      BESUM=BESUM+DST
      YSQBE=YSQBE+ER(3,J)**2 
      XSQBE=XSQBE+ER(4,J)**2 
      GO TO (380,381)KORBT
 380  BENAN=BENAN+1.
      BESAN=BESAN+DST
      GO TO 251
 381  BENDN=BENDN+1.
      BESDN=BESDN+DST
  251 CONTINUE
      ICHECK=1
      GO TO 53
C
C   NON-DMSP SATELLITE SECTION (OTHER) 
C
   51 IOTHER=IOTHER+1   
      OTHER=OTHER+DST
      OTHER2=OTHER2+DST*DST
      IF(SATLITE.EQ.'GMS ') THEN
         IGMS=IGMS+1   
         GMS=GMS+DST
         GMSS=GMSS+DST*DST
         IF(IPCN.EQ.'E'.OR.IPCN.EQ.'1'.OR.IPCN.EQ.'2') THEN
            IGMSE=IGMSE+1
            GMSE=GMSE+DST
            GMSESQ=GMSESQ+DST*DST
         ELSE IF(IPCN.EQ.'C'.OR.IPCN.EQ.'3'.OR.IPCN.EQ.'4') THEN
            IGMSC=IGMSC+1
            GMSC=GMSC+DST
            GMSCSQ=GMSCSQ+DST*DST
         ELSE IF(IPCN.EQ.'O'.OR.IPCN.EQ.'5'.OR.IPCN.EQ.'6') THEN
            IGMSO=IGMSO+1
            GMSO=GMSO+DST
            GMSOSQ=GMSOSQ+DST*DST
         ELSE
            GOTO 9007
         ENDIF
      ENDIF
   53 IF(IYEAR.EQ.1) GOTO 9007

c  check for fixes outside of pcn limits

      flag = ' '
      IF(IPCN.EQ.'E'.OR.IPCN.EQ.'1'.OR.IPCN.EQ.'2') ip = 1
      IF(IPCN.EQ.'C'.OR.IPCN.EQ.'3'.OR.IPCN.EQ.'4') ip = 2
      IF(IPCN.EQ.'O'.OR.IPCN.EQ.'5'.OR.IPCN.EQ.'6') ip = 3

      npcn(ip) = npcn(ip) + 1
      if (er(2,1) .gt. plimit(ip)) then
         flag = '*'
         nflag(ip) = nflag(ip) + 1
      endif

      IF (INDIVD .EQ. 'Y') WRITE (3,64) flag,ISITE,SATLITE,BIRD,IPCN,
     &   MDHM,MN,(ER(I,1),I=1,4)
   64 FORMAT(a1,'SATELLITE',2X,A4,4X,A4,A2,2X,a1,3x,I6.6,I2.2,4X,F4.0,
     &  2X,F5.1,2(2X,f6.1))
      GO TO 9007
C
C   AIRCRAFT STATISTICS SECTION
C
   82 IAC=IAC+1   
      AC=AC+DST
      AC2=AC2+DST*DST
      IF(IFT.LE.0) THEN
         XL='MB'   
         IHGT=MB
      ELSE
         XL='FT'   
         IHGT=IFT*100
      ENDIF
      IF(IYEAR.EQ.1) GOTO 9007
      IF (INDIVD .EQ. 'Y') WRITE (3,95) MSN,IHGT,XL,MDHM,MN,
     &   (ER(I,1),I=1,4)
   95 FORMAT(1X,'AIRCRAFT ','MSN',I3,3X,I4,A2,7X,I6.6,I2.2,4X,F4.0,2X,
     &  f5.1,2(2X,F6.1))
      GO TO 9007
C
C   RADAR STATISTICS SECTION 
C
   83 A=ACC
      IF(A.EQ.'G'.OR.A.EQ.'1'.OR.A.EQ.'4') THEN 
        IRG=IRG+1   
         RG=RG+DST
         RG2=RG2+DST*DST
         RACC='GOOD'
      ELSE IF(A.EQ.'F'.OR.A.EQ.'2'.OR.A.EQ.'5') THEN
         IRF=IRF+1   
         RF=RF+DST
         RF2=RF2+DST*DST
         RACC='FAIR'
      ELSE
         IRP=IRP+1   
         RP=RP+DST
         RP2=RP2+DST*DST
         RACC='POOR'
      ENDIF
      IF(RR.EQ.'L') RT='LAND'
      IF(RR.EQ.'S') RT='SHIP'
      IF(RR.EQ.'A') RT='ACFT'
      IF(IYEAR.EQ.1) GOTO 9007
      IF (INDIVD .EQ. 'Y') WRITE (3,93) RT,RACC,MDHM,MN,
     &         (ER(I,1),I=1,4)
   93 FORMAT(3X,'RADAR',4X,A4,4X,A4,8X,I6.6,I2.2,4X,F4.0,2X,F5.1,
     &   2(2X,F6.1))
      GO TO 9007
C
C   SCATTEROMETER STATISTICS SECTION 
C
 84   IF(CONF.EQ.'1') THEN 
         ISCTG=ISCTG+1   
         SCTG=SCTG+DST
         SCTG2=SCTG2+DST*DST
         SCTCONF='BULLSEYE'
      ELSE IF(CONF.EQ.'2') THEN
         ISCTF=ISCTF+1   
         SCTF=SCTF+DST
         SCTF2=SCTF2+DST*DST
         SCTCONF='FAIR'
      ELSE
         ISCTP=ISCTP+1   
         SCTP=SCTP+DST
         SCTP2=SCTP2+DST*DST
         SCTCONF='PARTIAL'
      ENDIF
      IF(IYEAR.EQ.1) GOTO 9007
      IF (INDIVD .EQ. 'Y') WRITE (3,92) SCATSITE,SCTCONF,MDHM,MN,
     &         (ER(I,1),I=1,4)
 92   FORMAT(1X,'SCATTEROM',2X,A4,4X,A8,4X,I6.6,I2.2,4X,F4.0,2X,
     &   F5.1,2(2X,F6.1))
      GO TO 9007
C
C ALL STORMS READ, COMPUTE STATISTICS
C
   21 CONTINUE
c
c  print pcn error stats
c
      call pcnstat
C
C  SATELLITE SECTION FINAL
C
      IF(IYEAR.EQ.1) GOTO 551
  551 IF(SAT.EQ.'N') GOTO 96
      IF(ICHECK.EQ.0) GO TO 56
      IF (EGNUM .NE. 0.0) EGBAR=EGSUM/EGNUM
      IF (EENUM .NE. 0.0) EEBAR=EESUM/EENUM
      IF (CGNUM .NE. 0.0) CGBAR=CGSUM/CGNUM
      IF (CENUM .NE. 0.0) CEBAR=CESUM/CENUM
      IF (BGNUM .NE. 0.0) BGBAR=BGSUM/BGNUM
      IF (BENUM .NE. 0.0) BEBAR=BESUM/BENUM
      ETNUM=EGNUM+EENUM
      IF (ETNUM .NE. 0.0) ETBAR=(EGSUM+EESUM)/ETNUM
      CTNUM=CGNUM+CENUM
      IF (CTNUM .NE. 0.0) CTBAR=(CGSUM+CESUM)/CTNUM
      BTNUM=BGNUM+BENUM
      IF (BTNUM .NE. 0.0) BTBAR=(BGSUM+BESUM)/BTNUM
      ECGNUM=EGNUM+CGNUM
      IF (ECGNUM .NE. 0.0) ECGBAR=(EGSUM+CGSUM)/ECGNUM
      ECENUM=EENUM+CENUM
      IF (ECENUM .NE. 0.0) ECEBAR=(EESUM+CESUM)/ECENUM
      ECTNUM=ETNUM+CTNUM
      IF (ECTNUM .NE. 0.0) ECTBAR=(EGSUM+EESUM+CGSUM+CESUM)/ECTNUM
      CBGNUM=CGNUM+BGNUM
      IF (CBGNUM .NE. 0.0) CBGBAR=(CGSUM+BGSUM)/CBGNUM
      CBENUM=CENUM+BENUM
      IF (CBENUM .NE. 0.0) CBEBAR=(CESUM+BESUM)/CBENUM
      CBTNUM=CTNUM+BTNUM
      IF (CBTNUM .NE. 0.0) CBTBAR=(CGSUM+CESUM+BGSUM+BESUM)/CBTNUM
      TGNUM=EGNUM+CBGNUM
      IF (TGNUM .NE. 0.0) TGBAR=(EGSUM+CGSUM+BGSUM)/TGNUM
      TENUM=EENUM+CBENUM
      IF (TENUM .NE. 0.0) TEBAR=(EESUM+CESUM+BESUM)/TENUM
      TOTNUM=TGNUM+TENUM
      IF (TOTNUM .NE. 0.0) TOTBAR=(EGSUM+EESUM+CGSUM+CESUM+BGSUM+
     &   BESUM)/TOTNUM
      IF (EGNAN .NE. 0.0) EGANBR=EGSAN/EGNAN
      IF (EGNDN .NE. 0.0) EGDNBR=EGSDN/EGNDN
      IF (EENAN .NE. 0.0) EEANBR=EESAN/EENAN
      IF (EENDN .NE. 0.0) EEDNBR=EESDN/EENDN
      IF (CGNAN .NE. 0.0) CGANBR=CGSAN/CGNAN
      IF (CGNDN .NE. 0.0) CGDNBR=CGSDN/CGNDN
      IF (CENAN .NE. 0.0) CEANBR=CESAN/CENAN
      IF (CENDN .NE. 0.0) CEDNBR=CESDN/CENDN
      IF (BGNAN .NE. 0.0) BGANBR=BGSAN/BGNAN
      IF (BGNDN .NE. 0.0) BGDNBR=BGSDN/BGNDN
      IF (BENAN .NE. 0.0) BEANBR=BESAN/BENAN
      IF (BENDN .NE. 0.0) BEDNBR=BESDN/BENDN
      IF ((EGNAN+EENAN) .NE. 0.0) EANBAR=(EGSAN+EESAN)/
     &  (EGNAN+EENAN)
      IF ((EGNDN+EENDN) .NE. 0.0) EDNBAR=(EGSDN+EESDN)/
     &  (EGNDN+EENDN)
      IF ((CGNAN+CENAN) .NE. 0.0) CANBAR=(CGSAN+CESAN)/
     &  (CGNAN+CENAN)
      IF ((CGNDN+CENDN) .NE. 0.0) CDNBAR=(CGSDN+CESDN)/
     &  (CGNDN+CENDN)
      IF ((BGNAN+BENAN) .NE. 0.0) BANBAR=(BGSAN+BESAN)/
     &  (BGNAN+BENAN)
      IF ((BGNDN+BENDN) .NE. 0.0) BDNBAR=(BGSDN+BESDN)/
     &  (BGNDN+BENDN)
      IF ((EGNAN+CGNAN+BGNAN) .NE. 0.0) ANGBAR=(EGSAN+CGSAN+BGSAN)/
     &  (EGNAN+CGNAN+BGNAN)
      IF ((EENAN+CENAN+BENAN) .NE. 0.0) ANEBAR=(EESAN+CESAN+BESAN)/
     &  (EENAN+CENAN+BENAN)
      IF ((EGNAN+EENAN+CGNAN+CENAN+BGNAN+BENAN) .NE. 0.0) 
     &  ANTBAR=(EGSAN+EESAN+CGSAN+CESAN+BGSAN+BESAN)/
     &  (EGNAN+EENAN+CGNAN+CENAN+BGNAN+BENAN)
      IF ((EGNDN+CGNDN+BGNDN) .NE. 0.0) DNGBAR=(EGSDN+CGSDN+BGSDN)/
     &  (EGNDN+CGNDN+BGNDN)
      IF ((EENDN+CENDN+BENDN) .NE. 0.0) DNEBAR=(EESDN+CESDN+BESDN)/
     &  (EENDN+CENDN+BENDN)
      IF ((EGNDN+EENDN+CGNDN+CENDN+BGNDN+BENDN) .NE. 0.0) 
     &  DNTBAR=(EGSDN+EESDN+CGSDN+CESDN+BGSDN+BESDN)/
     &  (EGNDN+EENDN+CGNDN+CENDN+BGNDN+BENDN)
      IF ((EGNAN+CGNAN) .NE. 0.0) ECGANBR=(EGSAN+CGSAN)/
     &  (EGNAN+CGNAN)
      IF ((EENAN+CENAN) .NE. 0.0) ECEANBR=(EESAN+CESAN)/
     &  (EENAN+CENAN)
      IF ((EGNAN+EENAN+CGNAN+CENAN) .NE. 0.0)  ECTANBR=(EGSAN+
     &  EESAN+CGSAN+CESAN)/(EGNAN+EENAN+CGNAN+CENAN)
      IF ((EGNDN+CGNDN) .NE. 0.0) ECGDNBR=(EGSDN+CGSDN)/
     &  (EGNDN+CGNDN)
      IF ((EENDN+CENDN) .NE. 0.0) ECEDNBR=(EESDN+CESDN)/
     &  (EENDN+CENDN)
      IF ((EGNDN+EENDN+CGNDN+CENDN) .NE. 0.0) ECTDNBR=(EGSDN+
     &  EESDN+CGSDN+CESDN)/(EGNDN+EENDN+CGNDN+CENDN)
      IF ((CGNAN+BGNAN) .NE. 0.0) CBGANBR=(CGSAN+BGSAN)/
     &  (CGNAN+BGNAN)
      IF ((CENAN+BENAN) .NE. 0.0) CBEANBR=(CESAN+BESAN)/
     &  (CENAN+BENAN)
      IF ((CGNAN+CENAN+BGNAN+BENAN) .NE. 0.0) CBTANBR=(CGSAN+
     &  CESAN+BGSAN+BESAN)/(CGNAN+CENAN+BGNAN+BENAN)
      IF ((CGNDN+BGNDN) .NE. 0.0) CBGDNBR=(CGSDN+BGSDN)/
     &  (CGNDN+BGNDN)
      IF ((CENDN+BENDN) .NE. 0.0) CBEDNBR=(CESDN+BESDN)/
     &  (CENDN+BENDN)
      IF ((CGNDN+CENDN+BGNDN+BENDN) .NE. 0.0) CBTDNBR=(CGSDN+
     &  CESDN+BGSDN+BESDN)/(CGNDN+CENDN+BGNDN+BENDN)
      EANUM=EGNAN+EENAN
      EDNUM=EGNDN+EENDN
      CANUM=CGNAN+CENAN
      CDNUM=CGNDN+CENDN
      BANUM=BGNAN+BENAN
      BDNUM=BGNDN+BENDN
      ANGNUM=EGNAN+CGNAN+BGNAN
      ANENUM=EENAN+CENAN+BENAN
      DNGNUM=EGNDN+CGNDN+BGNDN
      DNENUM=EENDN+CENDN+BENDN
      ECGANUM=EGNAN+CGNAN
      ECEANUM=EENAN+CENAN
      ECTANUM=EGNAN+EENAN+CGNAN+CENAN
      ECGDNUM=EGNDN+CGNDN
      ECEDNUM=EENDN+CENDN
      ECTDNUM=EGNDN+EENDN+CGNDN+CENDN
      CBGANUM=CGNAN+BGNAN
      CBEANUM=CENAN+BENAN
      CBTANUM=CGNAN+CENAN+BGNAN+BENAN
      CBGDNUM=CGNDN+BGNDN
      CBEDNUM=CENDN+BENDN
      CBTDNUM=CGNDN+CENDN+BGNDN+BENDN
      ANTNUM=EGNAN+EENAN+CGNAN+CENAN+BGNAN+BENAN 
      DNTNUM=EGNDN+EENDN+CGNDN+CENDN+BGNDN+BENDN 
      IF(EGNUM.LE.1) THEN
         SIGEG=0
      ELSE
         SIGEG=SQRT((YSQEG+XSQEG)/EGNUM)
      ENDIF
      IF(EENUM.LE.1) THEN 
         SIGEE=0
      ELSE
         SIGEE=SQRT((YSQEE+XSQEE)/EENUM)
      ENDIF
      IF(CGNUM.LE.1) THEN
         SIGCG=0
      ELSE
         SIGCG=SQRT((YSQCG+XSQCG)/CGNUM)
      ENDIF
      IF(CENUM.LE.1) THEN
         SIGCE=0
      ELSE
         SIGCE=SQRT((YSQCE+XSQCE)/CENUM)
      ENDIF
      IF(BGNUM.LE.1) THEN
         SIGBG=0
      ELSE
         SIGBG=SQRT((YSQBG+XSQBG)/BGNUM)
      ENDIF
      IF(BENUM.LE.1) THEN 
         SIGBE=0
      ELSE
         SIGBE=SQRT((YSQBE+XSQBE)/BENUM)
      ENDIF
      IF(ETNUM.LE.1) THEN 
         SIGET=0
      ELSE
         SIGET=SQRT((YSQEG+YSQEE+XSQEG+XSQEE)/ETNUM)
      ENDIF
      IF(CTNUM.LE.1) THEN
         SIGCT=0
      ELSE
         SIGCT=SQRT((YSQCG+YSQCE+XSQCG+XSQCE)/CTNUM)
      ENDIF
      IF(BTNUM.LE.1) THEN 
         SIGBT=0
      ELSE
         SIGBT=SQRT((YSQBG+YSQBE+XSQBG+XSQBE)/BTNUM)
      ENDIF
      IF(TOTNUM.LE.1) THEN
         SIGTOT=0
      ELSE
         SIGTOT=SQRT((YSQEG+YSQEE+YSQCG+YSQCE+YSQBG+YSQBE+XSQEG+
     &          XSQEE+XSQCG+XSQCE+XSQBG+XSQBE)/TOTNUM)
      ENDIF
C
      WRITE (3,50) SITETYPE(NSITE),TYPE,SATNUM
   50 FORMAT(//,10X,'THE SATELLITE REQUESTS WERE FOR ',A14,3X,A
     *4,1X,A2,/)
Cajs      if (nsite .gt. 1) then
Cajs         write (3,'(20x,a4)') (site(i),i=1,numsite)
Cajs      endif
      write (3,'(20x,a4)') (site(i),i=1,numsite)
      IF (IFWFS .GT. 0) THEN
         WRITE (3,11) IFWFS
   11    FORMAT(10X,'NOTE ',I3,' FWFS FIXES WERE NOT USED',//)
      ENDIF
      if (gmsflg .eq. 'Y') then
         WRITE (3,61)
      else
         write (3,65)
      endif
   61 FORMAT(//26X,' STATISTICAL SUMMARY OF DMSP/NOAA/TIROS TROPICAL',
     &  ' CYCLONE POSITIONS ',/)
   65 FORMAT(//26X,' STATISTICAL SUMMARY OF ALL SATELLITE TROPICAL',
     &  ' CYCLONE POSITIONS ',/)
      WRITE (3,66)
 66   FORMAT( 1X,27X,' EYE',9X,' WELL DEFINED',5X,' POORLY DEFINED',3X
     &  ,' EYE + WELL DEF',2X,' WELL + POOR DEF',4X,' TOTAL CASES') 
      WRITE (3,67) EGANBR,int(EGNAN),CGANBR,int(CGNAN),BGANBR,
     &  int(BGNAN),ECGANBR,int(ECGANUM),CBGANBR,int(CBGANUM),ANGBAR,
     &  int(ANGNUM)
      WRITE (3,68) EGDNBR,int(EGNDN),CGDNBR,int(CGNDN),BGDNBR,
     &  int(BGNDN),ECGDNBR,int(ECGDNUM),CBGDNBR,int(CBGDNUM),DNGBAR,
     &  int(DNGNUM)
      WRITE (3,69) EGBAR,int(EGNUM),CGBAR,int(CGNUM),BGBAR,int(BGNUM),
     &  ECGBAR,int(ECGNUM),CBGBAR,int(CBGNUM),TGBAR,int(TGNUM)
      WRITE (3,70) EEANBR,int(EENAN),CEANBR,int(CENAN),BEANBR,
     &  int(BENAN),ECEANBR,int(ECEANUM),CBEANBR,int(CBEANUM),ANEBAR,
     &  int(ANENUM)
      WRITE (3,71) EEDNBR,int(EENDN),CEDNBR,int(CENDN),BEDNBR,
     &  int(BENDN),ECEDNBR,int(ECEDNUM),CBEDNBR,int(CBEDNUM),DNEBAR,
     &  int(DNENUM)
 67   FORMAT(1X,'GEOG GRID(DAY)',7X,6(F6.1,' NM (',i5,') '))
 68   FORMAT(1X,'GEOG GRID(NITE)',6X,6(F6.1,' NM (',i5,') '))
 69   FORMAT(1X,'TOTAL GEOG GRID',6X,6(F6.1,' NM (',i5,') '))
 70   FORMAT(1X,'EPHEM GRID(DAY)',6X,6(F6.1,' NM (',i5,') '))
 71   FORMAT(1X,'EPHEM GRID(NITE)',5X,6(F6.1,' NM (',i5,') '))
      WRITE (3,72) EEBAR,int(EENUM),CEBAR,int(CENUM),BEBAR,int(BENUM),
     &  ECEBAR,int(ECENUM),CBEBAR,int(CBENUM),TEBAR,int(TENUM)
 72   FORMAT(1X,'TOTAL EPHEM GRID',5X,6(F6.1,' NM (',i5,') '))
      WRITE (3,73) EANBAR,int(EANUM),CANBAR,int(CANUM),BANBAR,
     &  int(BANUM),ECTANBR,int(ECTANUM),CBTANBR,int(CBTANUM),ANTBAR,
     &  int(ANTNUM)
 73   FORMAT(1X,'GEOG + EPH GRID(DAY) ',6(F6.1,' NM (',i5,') '))
      WRITE (3,74) EDNBAR,int(EDNUM),CDNBAR,int(CDNUM),BDNBAR,
     &  int(BDNUM),ECTDNBR,int(ECTDNUM),CBTDNBR,int(CBTDNUM),DNTBAR,
     &  int(DNTNUM)
 74   FORMAT(1X,'GEO + EPH GRID(NITE) ',6(F6.1,' NM (',i5,') '))
      WRITE (3,75) ETBAR,int(ETNUM),CTBAR,int(CTNUM),BTBAR,int(BTNUM),
     &  ECTBAR,int(ECTNUM),CBTBAR,int(CBTNUM),TOTBAR,int(TOTNUM)
 75   FORMAT(1X,'TOTAL GEO + EPH GRID ',6(F6.1,' NM (',i5,') '))
      WRITE (3,500) int(EGNUM),SIGEG
  500 FORMAT(/1X,'    THE RMS ERROR FOR ',i5,' GEOGRAPHICALLY GRIDDE',
     1 'D EYE CASES IS ',F7.2)
      WRITE (3,501) int(EENUM),SIGEE
  501 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' EPHEMERIS GRIDDED EYE',
     & ' CASES IS ',F7.2)
      WRITE (3,502) int(CGNUM),SIGCG
  502 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' GEOGRAPHICALLY GRIDDE',
     1 'D WELL DEFINED CIRCULATION CENTER CASES IS ',F7.2)
      WRITE (3,503) int(CENUM),SIGCE
  503 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' EPHEMERIS GRIDDED WEL',
     1 'L DEFINED CIRCULATION CENTER CASES IS ',F7.2)
      WRITE (3,504) int(BGNUM),SIGBG
  504 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' GEOGRAPHICALLY GRIDDE',
     1 'D POORLY DEFINED CIRCULATION CENTER CASES IS ',F7.2)
      WRITE (3,505) int(BENUM),SIGBE
  505 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' EPHEMERIS GRIDDED POO',
     1 'RLY DEFINED CIRCULATION CENTER CASES IS ',F7.2)
      WRITE (3,506) int(ETNUM),SIGET
  506 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' TOTAL EYE CASES IS ',F
     17.2)
      WRITE (3,507) int(CTNUM),SIGCT
  507 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' TOTAL WELL DEFINED CI',
     1 'RCULATION CENTER CASES IS ',F7.2) 
      WRITE (3,508) int(BTNUM),SIGBT
  508 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' TOTAL POORLY DEFINED',
     1 ' CIRCULATION CENTER CASES IS ',F7.2)
      WRITE (3,509) int(TOTNUM),SIGTOT
  509 FORMAT(1X,'    THE RMS ERROR FOR ',i5,' TOTAL CASES IS ',F7.2)
C
C   NON-DMSP FINAL SECTION
C
   56 CONTINUE
      IF(IOTHER.GT.0) THEN
         IF(IOTHER.EQ.1) SD=0.001
         IF(SD.NE..001) THEN
            OTHER=OTHER/IOTHER
            SD=SQRT(OTHER2/IOTHER-OTHER*OTHER)
         ENDIF
         WRITE (3,54)
 54      FORMAT(//,30X,'OTHER FIX ERRORS',/)
         WRITE (3,55) OTHER,IOTHER,SD
 55      FORMAT(10X,'OTHER AVERAGE ERROR ',f5.1,' NM',3X,'FOR',I5,
     1        ' CASES',',    STANDARD DEVIATION',F6.1)
         IF(IGMS.EQ.0) GOTO 96
         IF(IGMS.EQ.1) STDEV0=0.001
         IF(STDEV0.NE..001) THEN
            GMS=GMS/IGMS 
            STDEV0=SQRT(GMSS/IGMS-GMS*GMS)
            IF(IGMSE.NE.0) THEN
               IF(IGMSE.EQ.1) STDEV1=0.001
               IF(STDEV1.NE..001) THEN
                  GMSE=GMSE/IGMSE
                  STDEV1=SQRT(GMSESQ/IGMSE-GMSE*GMSE)
               ENDIF
            ENDIF
            IF(IGMSC.NE.0) THEN
               IF(IGMSC.EQ.1) STDEV2=0.001
               IF(STDEV2.NE..001) THEN
                  GMSC=GMSC/IGMSC
                  STDEV2=SQRT(GMSCSQ/IGMSC-GMSC*GMSC)
               ENDIF
            ENDIF
            IF(IGMSO.NE.0) THEN
               IF(IGMSO.EQ.1) STDEV3=0.001
               IF(STDEV2.NE..001) THEN
                  GMSO=GMSO/IGMSO
                  STDEV3=SQRT(GMSOSQ/IGMSO-GMSO*GMSO)
               ENDIF
            ENDIF
            WRITE (3,161)
 161        FORMAT(///,30X,'GMS FIX ERRORS',/)
            WRITE (3,162) GMSE,IGMSE,STDEV1
 162        FORMAT(/,24X,'EYE   ',F5.1,' NM',3X,'FOR',I5,' CASES',
     1           ',    STANDARD DEVIATION',F6.1)
            WRITE (3,163) GMSC,IGMSC,STDEV2
 163        FORMAT(/,24X,'CC    ',F5.1,' NM',3X,'FOR',I5,' CASES',
     1           ',    STANDARD DEVIATION',F6.1)
            WRITE (3,164) GMSO,IGMSO,STDEV3
 164        FORMAT(/,24X,'OTHER ',F5.1,' NM',3X,'FOR',I5,' CASES',
     1           ',    STANDARD DEVIATION',F6.1)
         ENDIF
         WRITE (3,165) GMS,IGMS,STDEV0
 165     FORMAT(/,24X,'TOTAL ',F5.1,' NM',3X,'FOR',I5,' CASES',
     1        ',    STANDARD DEVIATION',F6.1)
      ENDIF
C     
C  AIRCRAFT SECTION FINAL
C
   96 IF(AIR.EQ.'Y') THEN
         IF(IAC.GT.0) THEN
            IF(IAC.EQ.1) SD=0.001
            IF(SD.NE..001) THEN
               AC=AC/IAC
               SD=SQRT(AC2/IAC-AC*AC) 
            ENDIF
            WRITE (3,98)
 98         FORMAT(//,30X,'AIRCRAFT FIX ERRORS',/)
            WRITE (3,99) AC,IAC,SD
 99         FORMAT(10X,'AIRCRAFT AVERAGE ERROR ',F5.1,' NM',3X,'FOR',
     *           I5,' CA','SES',',    STANDARD DEVIATION',F6.1)
         ENDIF
      ENDIF
C
C  RADAR SECTION FINAL
C
      IF(RAD.EQ.'Y') THEN
         IJK=IRG+IRF+IRP
         IF(IJK.EQ.0) STOP
         IF(IRG.LE.1) THEN
            IF(IRG.EQ.0) RG=0.0
            SDG=0.0
         ELSE
            RG=RG/IRG
            SDG=SQRT(RG2/IRG-RG*RG)
         ENDIF
         IF(IRF.LE.1) THEN
            IF(IRF.EQ.0) RF=0.0
            SDF=0.0
         ELSE
            RF=RF/IRF
            SDF=SQRT(RF2/IRF-RF*RF)
         ENDIF
         IF(IRP.LE.1) THEN   
            IF(IRP.EQ.0) RP=0.0
            SDP=0.0
         ELSE
            RP=RP/IRP
            SDP=SQRT(RP2/IRP-RP*RP)
         ENDIF
         WRITE (3,40)
 40      FORMAT(//,30X,'RADAR FIX ERRORS',/)
         RX='GOOD' 
         RY='FAIR'  
         RZ='POOR'
         WRITE (3,41) RX,RG,IRG,SDG
         WRITE (3,41) RY,RF,IRF,SDF
         WRITE (3,41) RZ,RP,IRP,SDP
 41      FORMAT(10X,A4,' AVERAGE ERROR ',F5.1,' NM',3X,'FOR',I5,
     *        ' CASES,    STANDARD DEVIATION',F6.1)
      ENDIF
C
C  SCATTEROMETER SECTION FINAL
C
      IF(SCAT.EQ.'Y') THEN
         IJK=ISCTG+ISCTF+ISCTP
         IF(IJK.EQ.0) STOP
         IF(ISCTG.LE.1) THEN
            IF(ISCTG.EQ.0) SCTG=0.0
            SDG=0.0
         ELSE
            SCTG=SCTG/ISCTG
            SDG=SQRT(SCTG2/ISCTG-SCTG*SCTG)
         ENDIF
         IF(ISCTF.LE.1) THEN
            IF(ISCTF.EQ.0) SCTF=0.0
            SDF=0.0
         ELSE
            SCTF=SCTF/ISCTF
            SDF=SQRT(RSCT2/ISCTF-SCTF*SCTF)
         ENDIF
         IF(ISCTP.LE.1) THEN   
            IF(ISCTP.EQ.0) SCTP=0.0
            SDP=0.0
         ELSE
            SCTP=SCTP/ISCTP
            SDP=SQRT(SCTP2/ISCTP-SCTP*SCTP)
         ENDIF
         WRITE (3,39)
 39      FORMAT(//,30X,'SCATTEROMETER FIX ERRORS',/)
         SCTX='BULLSEYE' 
         SCTY='    FAIR'  
         SCTZ=' PARTIAL'
         WRITE (3,38) SCTX,SCTG,ISCTG,SDG
         WRITE (3,38) SCTY,SCTF,ISCTF,SDF
         WRITE (3,38) SCTZ,SCTP,ISCTP,SDP
 38      FORMAT(6X,A8,' AVERAGE ERROR ',F5.1,' NM',3X,'FOR',I5,
     *        ' CASES,    STANDARD DEVIATION',F6.1)
      ENDIF
C
 9998 CONTINUE
      TC(1)='  SATELLITE  '
      TC(2)='   AIRCRAFT  '  
      TC(3)='    RADAR    '
      TC(4)='SCATTEROMETER'
      WRITE(3,'(//)')
      DO I=1,4
         WRITE (3,15) NO(I),TC(I)
      ENDDO
   15 FORMAT(20X,I3,1X,A13,' FIXES WERE OUTSIDE THE TIME LIMITS OF ',
     &   'THE BEST TRACK')
      WRITE (3,12)
   12 FORMAT(34X,' SYNOPTIC FIXES ARE NOT USED BY THIS PROGRAM')
C      WRITE (3,13)
C   13 FORMAT(34X,' SCATTEROMETER FIXES ARE NOT USED BY THIS PROGRAM')
      STOP
c
 9000 PAUSE 'ERROR OPENING INPUT FILES'
      STOP 1
      END

c-----------------------------------------------------------------------
      SUBROUTINE PCNSTAT
c
c      Print pcn error stats.
c
c  Passed parameters:
c     none
c  Returned parameters:
c     none
c  common parameters:
c     npcn - number of fixes for each of the 3 pcn codes
c     nflag - number of fixes exceeding each of the 3 pcn limits
c     plimit - array of 3 pcn limits
c
c-----------------------------------------------------------------------
c
      COMMON /PCN/ NPCN(3),NFLAG(3),PLIMIT(3)

      IF (NPCN(1) .EQ. 0) THEN
         PRCNT = 0.0
      ELSE
         PRCNT = FLOAT(NFLAG(1))/FLOAT(NPCN(1))*100.0
      ENDIF

      WRITE (3,'(//5X,I4,'' OF '',I4,'' ('',F5.1,''%) PCN 1 & 2 '',
     &    ''FIXES EXCEEDED ERROR LIMIT ('',I2,'' NMI.)'')') 
     &    NFLAG(1),NPCN(1),prcnt,INT(PLIMIT(1))

      IF (NPCN(2) .EQ. 0) THEN
         PRCNT = 0.0
      ELSE
         PRCNT = FLOAT(NFLAG(2))/FLOAT(NPCN(2))*100.0
      ENDIF

      WRITE (3,'(5X,I4,'' OF '',I4,'' ('',F5.1,''%) PCN 3 & 4 '',
     &    ''FIXES EXCEEDED ERROR LIMIT ('',I2,'' NMI.)'')') 
     &    NFLAG(2),NPCN(2),prcnt,INT(PLIMIT(2))

      IF (NPCN(3) .EQ. 0) THEN
         PRCNT = 0.0
      ELSE
         PRCNT = FLOAT(NFLAG(3))/FLOAT(NPCN(3))*100.0
      ENDIF

      WRITE (3,'(5X,I4,'' OF '',I4,'' ('',F5.1,''%) PCN 5 & 6 '',
     &    ''FIXES EXCEEDED ERROR LIMIT ('',I2,'' NMI.)'')') 
     &    NFLAG(3),NPCN(3),prcnt,INT(PLIMIT(3))

      RETURN
      END

c-----------------------------------------------------------------------
      subroutine fileopener (strmid, ioerror)
c
c  Open the input and output files required for fixerrs.
c
c  1 = BEST TRACK
c  2 = FIXES
c  3 = OUTPUT (fixerrs.txt)
c  4 = INPUT PARAMETERS (fixerrs.in)
c
c
c  Passed parameters:
c       none
c  Returned parameters:
c       strmid - storm id, eg. wp0399
c       ioerror - file open status, 0 = no error, non-zero = error
c
c-----------------------------------------------------------------------
c
      character*120  storms,fields,include,filename
      character*2    century
      character*6    strmid
      integer        ind
      integer        ioerror, iarg
C 
cx    OPEN (1,FILE=' ',STATUS='OLD',ERR=9000)
cx    OPEN (2,FILE=' ',STATUS='OLD',ERR=9000)
cx    OPEN (3,FILE=' ',STATUS='UNKNOWN',ERR=9000)
cx    OPEN (4,FILE=' ',STATUS='OLD',ERR=9000)
cx
cx  Get the storms directory from environment, 
cx  open best track, fixes and output files.
cx  Get the atcffls directory from environment, 
cx  open input file.
cx
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c  get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
      write(filename,'(6a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      open(1,file=filename,status='old',iostat=ioerror)
      if( ioerror .eq. 0 ) then
         write(filename,'(6a)') storms(1:ind), "/f", 
     1        strmid(1:4), century, strmid(5:6), ".dat"
         open(2,file=filename,status='old',iostat=ioerror)
      endif
      if( ioerror .eq. 0 ) then
         write(filename,'(a,a)')storms(1:ind),"/fixerrs.txt"
         call openfile(3,filename,'unknown',ioerror)
      endif
      if( ioerror .eq. 0 ) then
         call getenv("ATCFINC",include)
         ind=index(include," ")-1
         write(filename,'(a,a)')include(1:ind),"/fixerrs.in"
         open(4,file=filename,status='old',iostat=ioerror)
      endif

      return
      end


c-----------------------------------------------------------------------
      subroutine readinput (sat,scat,air,rad,nsite,numsite,site,
     &     type,satnum,indivd,gmsflg,ioerror)
c
c  Read the input parameter file, return the user specified parameters.
c
c
c  Passed parameters:
c       none
c  Returned parameters:
c       sat - flag to compute satellite stats
c       scat - flag to compute scatterometer stats
c       air - flag to compute aircraft stats
c       rad - flag to compute radar stats
c       nsite - 1=one or more sites, 2=DMSP network sites, 3=all sites
c       numsite - number of sites selected, 0 means all sites
c       site - satellite fix site, defined if nsite equals 1
c       type - satellite bird type, blank means all types
c       satnum - satellite number, blank means all numbers
c       indivd - flag to compute individual fix stats
c       gmsflag - flag to compute GMS stats separately
c       ioerror - read status, 0 = successful, 
c                              negative = end-of-file, 
c                              positive = error.
c
c-----------------------------------------------------------------------
c
      integer        ioerror
      integer        nsite, numsite, net
      LOGICAL        YNCHCK
      CHARACTER*1    SAT,AIR,RAD,SCAT,INDIVD,GMSFLG
      CHARACTER*4    TYPE
      CHARACTER*4    SITE(20),NETSITE(6)
      CHARACTER      SATNUM*2

      DATA NETSITE /'PGTW','RODN','RPMK','RKSZ','KGWC','PGUA'/
      DATA NET /6/


c1000 WRITE (*,'(/'' COMPUTE SATELLITE STATS? (Y OR N, <CR>=Y) '',\)')
cx    READ (*,'(A1)') SAT
cx    IF (SAT .EQ. ' ') SAT = 'Y'
cx    IF (.NOT. YNCHCK(SAT)) THEN
cx       WRITE (*,'('' *** ERROR *** INVALID ENTRY'')')
cx       GOTO 1000
cx    ENDIF
c1010 WRITE (*,'(/'' COMPUTE AIRCRAFT STATS? (Y OR N, <CR>=Y) '',\)')
cx    READ (*,'(A1)') AIR
cx    IF (AIR .EQ. ' ') AIR = 'Y'
cx    IF (.NOT. YNCHCK(AIR)) THEN
cx       WRITE (*,'('' *** ERROR *** INVALID ENTRY'')')
cx       GOTO 1010
cx    ENDIF
c1020 WRITE (*,'(/'' COMPUTE RADAR STATS? (Y OR N, <CR>=Y) '',\)')
cx    READ (*,'(A1)') RAD
cx    IF (RAD .EQ. ' ') RAD = 'Y'
cx    IF (.NOT. YNCHCK(RAD)) THEN
cx       WRITE (*,'('' *** ERROR *** INVALID ENTRY'')')
cx       GOTO 1020
cx    ENDIF
cx    IF(SAT.EQ.'N'.AND.AIR.EQ.'N'.AND.RAD.EQ.'N') THEN
cx       WRITE (*,'(//'' *** ERROR *** YOU MUST REQUEST AT LEAST ONE'')
cx   &            ')
cx       GOTO 1000
cx    ENDIF
C
      
cx    IF (SAT .EQ. 'N') GOTO 1060
cx
cx    WRITE (*,'(/''          1 - ONE OR MORE SITES'')')
cx    WRITE (*,'( ''          2 - DMSP NETWORK SITES'')')
cx    WRITE (*,'( ''          3 - ALL SITES'')')

c1030 CONTINUE
cx    WRITE (*,'('' ENTER SELECTION '')')
cx    READ (*,'(I1)',ERR=1030) NSITE
cx    IF (NSITE .EQ. 1) THEN
cx       NUMSITE = 1
c1040    WRITE (*,'(/,'' ENTER SITE (OR <CR> TO END INPUT: '',\)')
cx       READ (*,'(A4)',ERR=1040) SITE(NUMSITE)
cx       IF (SITE(NUMSITE) .NE. '    ') THEN    
cx          CALL UPCASE (SITE(NUMSITE),4)
cx          NUMSITE = NUMSITE + 1
cx          GOTO 1040
cx       ELSE
cx          NUMSITE = NUMSITE - 1
cx       ENDIF
cx       IF (NUMSITE .LE. 0) THEN
cx          WRITE (*,'(/'' ERROR.  YOU MUST SELECT AT LEAST ONE SITE.''
cx   &                 )')
cx          NUMSITE = 1
cx          GOTO 1040
cx       ENDIF
cx    ELSE IF (NSITE .EQ. 2) THEN
cx       DO 1050 I = 1,NET
cx       SITE(I) = NETSITE(I)
c1050    CONTINUE
cx       NUMSITE = NET
cx    ELSE IF (NSITE .EQ. 3) THEN
cx       NUMSITE = 0
cx    ELSE
cx       GOTO 1030
cx    ENDIF

cx    WRITE (*,'(/'' ENTER SAT BIRD TYPE (<CR> FOR ALL) '',\)')
cx    READ (*,'(A4)') TYPE
cx    CALL UPCASE (TYPE,4)
cx    WRITE (*,'(/'' ENTER SAT NUMBER (<CR> FOR ALL) '',\)')
cx    READ (*,'(A2)') SATNUM

c1060 CONTINUE
cx    WRITE (*,'(/'' DO YOU WANT INDIVIDUAL FIX STATS (Y OR N,'',
cx   &    '' <CR>=Y) '',\)')
cx    READ (*,'(A1)') INDIVD
cx    IF (INDIVD .EQ. ' ') INDIVD = 'Y'
cx    IF (.NOT. YNCHCK(INDIVD)) THEN
cx       WRITE (*,'('' *** ERROR *** INVALID ENTRY'')')
cx       GOTO 1060
cx    ENDIF
cx
c1061 CONTINUE
cx    WRITE (*,'(/'' DO YOU WANT TO COMPUTE GMS STATS SEPARATELY?'',
cx   &    '' (Y OR N, <CR>=Y) '',\)')
cx    READ (*,'(A1)') GMSFLG
cx    IF (GMSFLG .EQ. ' ') GMSFLG = 'Y'
cx    IF (.NOT. YNCHCK(GMSFLG)) THEN
cx       WRITE (*,'('' *** ERROR *** INVALID ENTRY'')')
cx       GOTO 1061
cx    ENDIF
C

      ioerror=0
cx    ' COMPUTE SATELLITE STATS? (Y OR N) '
      read (4,'(a1)',err=8000) sat
      if (sat .eq. ' ') sat = 'y'
      if (.not. ynchck(sat))go to 8000 
cx    ' COMPUTE SCATTEROMETER STATS? (Y OR N) '
      read (4,'(a1)',err=8000) scat
      if (scat .eq. ' ') scat = 'y'
      if (.not. ynchck(scat))go to 8000 
cx    ' COMPUTE AIRCRAFT STATS? (Y OR N) '
      read (4,'(a1)',err=8000) air
      if (air .eq. ' ') air = 'y'
      if (.not. ynchck(air))go to 8000 
cx    ' COMPUTE RADAR STATS? (Y OR N) '
      read (4,'(a1)',err=8000) rad
      if (rad .eq. ' ') rad = 'y'
      if (.not. ynchck(rad))go to 8000 
cx    ' Satellite sites (1=single site, 2= DMSP network sites, 3=all sites)
      read (4,'(i1)',err=8000) nsite
      NUMSITE = 1
cx    ' SAT SINGLE SITE (4 chars) '
      read (4,'(a4)',err=8000) SITE(NUMSITE)
      if( nsite .eq. 2 ) then
         do i=1, net 
            site(i) = netsite(i)
         enddo
         numsite = net
      else if( nsite .eq. 3 ) then
         numsite = 0
      endif
cx    ' SAT BIRD TYPE (4 chars) '
      read (4,'(a4)',err=8000) type
cx    ' SAT NUMBER (2 chars) '
      read (4,'(a2)',err=8000) satnum
cx    ' DO YOU WANT INDIVIDUAL FIX STATS (Y OR N) '
      read (4,'(a1)',err=8000) indivd
      if (indivd .eq. ' ') indivd = 'y'
      if (.not. ynchck(indivd))go to 8000 
cx    ' DO YOU WANT TO COMPUTE GMS STATS SEPARATELY? (Y OR N) '
      read (4,'(a1)',err=8000) gmsflg
      if (gmsflg .eq. ' ') gmsflg = 'y'
      if (.not. ynchck(gmsflg)) go to 8000
      return
cx

 8000 ioerror = 1
      return
      end


c-----------------------------------------------------------------------
      subroutine satdecode ( fix,site,numsite,type,satnum,kind,jyr,mdhm,
     &     mn,lat,latns,long,longew,ipcn,satlite,bird,isite,ifwfs,skip )
c
c  SATELLITE DECODE SECTION
c
c
c  Passed parameters:
c       fix - fix record
c       site - user selected site(s) to compute for
c       numsite - number of sites selected, 0 means all sites
c       type - satellite bird type, blank means all types
c       satnum - satellite number, blank means all numbers
c  Returned parameters:
c       kind - fix type
c       jyr - year
c       mdhm - month/day/hour
c       mn - minute
c       lat - latitude
c       latns - north/south indicator
c       long - longitude
c       longew - east/west indicator
c       ipcn - pcn code
c       satlite - 1st 4 chars of satellite type
c       bird - last 2 chars of satellite type
c       isite - fix site
c       ifwfs - count of FWFS fixes
c       skip - skip (don't process) this fix
c
c-----------------------------------------------------------------------
c
      character      fix*78, satnum*2, bird*2
      character*1    latns, longew, ipcn
      character*4    site(20), type, satlite, isite
      logical        skip
      integer        kind, jyr, mn, lat, long, numsite, ifwfs
      integer*4      mdhm

C   SATELLITE DECODE SECTION 
C
      skip = .false.
      KIND=1
      READ (FIX,34) JYR,MDHM,MN,LAT,LATNS,LONG,LONGEW,IPCN,SATLITE,
     *BIRD,ISITE
 34   FORMAT(2X,I2,I6,I2,I3,A1,I4,2A1,13X,A4,A2,33X,A4)

C  CHECK THE FIX SITE AGAINST THE USER REQUEST.  IF NUMSITE = 0, USER
C  WANTED ALL SITES.  EVEN SO, DON'T INCLUDE SUITLAND (FWFS).  IF 
C  NUMSITE <> 0, LOOP THRU THE LIST OF REQUESTED SITES TO SEE IF THIS
C  IS ONE OF THEM

      IF (NUMSITE .EQ. 0) THEN
         IF (ISITE .EQ. 'FWFS') THEN
            IFWFS = IFWFS + 1
            GOTO 8001
         ENDIF
      ELSE
         DO I=1,NUMSITE
            IF (ISITE .EQ. SITE(I)) GOTO 712
         ENDDO        
         GOTO 8001
      ENDIF

  712 IF(TYPE.EQ.'    ') return
C      IF(TYPE.EQ.'DMSP') THEN
C        IF(SATLITE.NE.'DMSP'.AND.SATLITE.NE.'NOAA'.AND.
C     &       SATLITE.NE.'TIRO') GOTO 8001
C      ELSE
C         IF(TYPE.NE.SATLITE) GOTO 8001
C      ENDIF
Cajs  substituted next line for above commented out lines
      IF(TYPE.NE.SATLITE) GOTO 8001
      IF(SATNUM.EQ.'  ') return
      IF(SATNUM.NE.BIRD) GOTO 8001
      return

 8001 skip = .true.
      return
      end


c-----------------------------------------------------------------------
      subroutine scatdecode ( fix,site,numsite,kind,jyr,mdhm,mn,
     &     lat,latns,long,longew,conf,scatsite,ifwfs,skip )
c
c  SCATTEROMETER DECODE SECTION
c
c
c  Passed parameters:
c       fix - fix record
c       site - user selected site(s) to compute for
c       numsite - number of sites selected, 0 means all sites
c  Returned parameters:
c       kind - fix type
c       jyr - year
c       mdhm - month/day/hour
c       mn - minute
c       lat - latitude
c       latns - north/south indicator
c       long - longitude
c       longew - east/west indicator
c       conf - confidence code, 1=bullseye, 2=fair, 3=partial
c       scatsite - fix site
c       ifwfs - count of FWFS fixes
c       skip - skip (don't process) this fix
c
c-----------------------------------------------------------------------
c
      character      fix*78
      character*1    latns, longew, conf
      character*4    site(20), scatsite
      logical        skip
      integer        kind, jyr, mn, lat, long, numsite, ifwfs
      integer*4      mdhm

C   SCATTEROMETER DECODE SECTION 
C
      skip = .false.
      KIND=4
      READ (FIX,36) JYR,MDHM,MN,LAT,LATNS,LONG,LONGEW,CONF,SCATSITE
 36   FORMAT(2X,I2,I6,I2,I3,A1,I4,2A1,52X,A4)

C  CHECK THE FIX SITE AGAINST THE USER REQUEST.  IF NUMSITE = 0, USER
C  WANTED ALL SITES.  EVEN SO, DON'T INCLUDE SUITLAND (FWFS).  IF 
C  NUMSITE <> 0, LOOP THRU THE LIST OF REQUESTED SITES TO SEE IF THIS
C  IS ONE OF THEM

      IF (NUMSITE .EQ. 0) THEN
         IF (SCATSITE .EQ. 'FWFS') THEN
            IFWFS = IFWFS + 1
            GOTO 8001
         ENDIF
      ELSE
         DO I=1,NUMSITE
            IF (SCATSITE .EQ. SITE(I)) return
         ENDDO        
         GOTO 8001
      ENDIF
      return

 8001 skip = .true.
      return
      end


c-----------------------------------------------------------------------
      subroutine interpBT ( n,tx,tb,xb,yb,x,y )
c
C   INTERPOLATE A BEST TRACK POINT AS A FUNCTION OF FIX TIME BY MEANS
C   OF A 2ND ORDER LAGRANGIAN POLYNOMIAL ABOUT TIME TB(IT).
c
c
c  Passed parameters:
c       n - best track posit counter
c       tx - fix time
c       tb - array of best track times
c       xb - array of best track x's
c       yb - array of best track y's
c  Returned parameters:
c       x - interpolated best track x posit
c       y - interpolated best track y posit
c
c-----------------------------------------------------------------------
c
      real      yb(300), xb(300), tb(300)
      real      tx
      real      x, y
      real      t1, t2, t3
      real      z1, z2, z3, z4, z5, z6, z7, z8, z9
      real      zz1, zz2, zz3
      real      bt1, bt2
      integer   it, i, m

C
C   SET FIX COUNTER (IT) TO EQUAL NEAREST BEST TRACK TIME
C   FOR NONUNIFORMLY SPACED BEST TRACK POINTS
      IT=0
      IF(TX.LE.TB(2)) IT=2
      IF(TX.GE.TB(N-1)) IT=N-1
      IF(IT.NE.2.AND.IT.NE.(N-1)) THEN
         M=N-2
         DO I=2,M
            IF(TX.GE.TB(I).AND.TX.LE.TB(I+1)) GO TO 9
         ENDDO
 9       BT1=TX-TB(I) 
         BT2=TB(I+1)-TX
         IF(BT1.GT.BT2) I=I+1
         IT=I
      ENDIF
C   INTERPOLATE A BEST TRACK POINT AS A FUNCTION OF FIX TIME BY MEANS
C   OF A 2ND ORDER LAGRANGIAN POLYNOMIAL ABOUT TIME TB(IT).
      T1=TB(IT-1)
      T2=TB(IT)
      T3=TB(IT+1)
      Z1=TX-T2
      Z2=TX-T3
      Z3=T1-T2
      Z4=T1-T3
      Z5=TX-T1
      Z6=T2-T1
      Z7=T2-T3
      Z8=T3-T1
      Z9=T3-T2
      IF(ABS(Z3).LT..001) Z3=.001
      IF(ABS(Z4).LT..001) Z4=.001
      IF(ABS(Z6).LT..001) Z6=.001
      IF(ABS(Z7).LT..001) Z7=.001
      IF(ABS(Z8).LT..001) Z8=.001
      IF(ABS(Z9).LT..001) Z9=.001
      ZZ1=(Z1*Z2)/(Z3*Z4)
      ZZ2=(Z5*Z2)/(Z6*Z7)
      ZZ3=(Z5*Z1)/(Z8*Z9)
      X=ZZ1*XB(IT-1)+ZZ2*XB(IT)+ZZ3*XB(IT+1)
      Y=ZZ1*YB(IT-1)+ZZ2*YB(IT)+ZZ3*YB(IT+1)

      return
      end
