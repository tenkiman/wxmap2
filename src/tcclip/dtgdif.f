C
C ********************************************************************
C
      SUBROUTINE DTGDIF (DTG1,DTG2,IDIF)
C
      DIMENSION INID(12)
      CHARACTER DTG1*8,DTG2*8
      DATA INID /0,31,59,90,120,151,181,212,243,273,304,334/
C
      READ (DTG1,1000) IYR,IMO,IDA,IHR
 1000 FORMAT (4I2)
      LEAP = MOD(IYR,4)
      ID = IYR*365.25 + 1
      IF (LEAP .EQ. 0) ID = ID - 1
      IADD = 0
      IF (LEAP .EQ. 0 .AND. IMO .GT. 2) IADD=1
      JULDA = INID(IMO) + IDA + IADD
      JULHR1 = 24. * (ID + JULDA) + IHR + 0.5
      READ (DTG2,1000) IYR,IMO,IDA,IHR
      LEAP = MOD(IYR,4)
      ID = IYR*365.25 + 1
      IF (LEAP .EQ. 0) ID = ID - 1
      IADD = 0
      IF(LEAP .EQ. 0 .AND. IMO .GT. 2) IADD=1
      JULDA = INID(IMO) + IDA + IADD
      JULHR2 = 24. * (ID + JULDA) + IHR + 0.5
      IDIF = JULHR2 - JULHR1
C
      RETURN
      END
