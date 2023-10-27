      SUBROUTINE QPRNTN(A,T1,T2,IBEG,JBEG,M,N)
C
C**********	May 17, 1988, THIS VERSION OUTPUTS TO UNIT 6
C**********	USING WRITE VICE PRINT
C
C***************************************************************
C***************************************************************
C*****                                                     *****
C*****       QPRINT OUTPUT ROUTINE (CORRECTED 4/26/86)     *****
C*****                                                     *****
C***************************************************************
C***************************************************************
C
C A= FWA OF M X N ARRAY
C T1,T2 = TITLE (2 8-CHARACTER WORDS)
C IBEG,JBEG=LOWER LEFT CORNER COORDS TO BE PRINTED
C UP TO 43 X 83 POINTS PRINTED
C
      DIMENSION A(M,N),IX(43)
      CHARACTER*8 T1,T2
C
C  DETERMINE GRID LIMITS
C
      IEND=MIN0(IBEG+42,M)
      JEND=MIN0(JBEG+82,N)
C
   24 CONTINUE
C
C  INDEX BACKWARDS CHECKING FOR MAX
C
   11 XM=0.
      JENDSC=MIN0(JEND,N)
      DO 14 J=JBEG,JENDSC
      DO 14 I=IBEG,IEND
   14 XM=AMAX1(XM,ABS(A(I,J)))
C
C  DETERMINE SCALING FACTOR LIMITS
C
      IF(XM.LT.1.E-200) XM=99.0
      XM=ALOG10(99.0/XM)
      KP=XM
      IF(XM.LT.0.)KP=KP-1
C
C  PRINT SCALING CONSTANTS
C
   12 WRITE(6,1) T1,T2,KP,(I,I=IBEG,IEND,2)
    1 FORMAT('0',A8,A8,'   K=',I3,
     2  /' ',22I6) 
      FK=10.0**KP
C
C  QUICKPRINT FIELD
C
      DO 2 J=JBEG,JEND
      JLI=JEND-J+JBEG
      IF(JLI.GT.N) GO TO 2
      II= 0
      IF(KP.NE.0) GO TO 8
      DO 9 I=IBEG,IEND
      II=II+1
    9 IX(II)=A(I,JLI)+SIGN(.5,A(I,JLI))
      GO TO 10
    8 DO 7 I=IBEG,IEND
      II=II+1
    7 IX(II)=A(I,JLI)*FK+SIGN(.5,A(I,JLI))
   10 WRITE(6,6) JLI,(IX(I),I=1,II),JLI
    6 FORMAT(I4,44I3)
    2 CONTINUE
      RETURN
      END