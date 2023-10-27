      SUBROUTINE CYCINT (RML,RNL,BFLD,MGRD,NGRD,VALI,IERR)
C
C                   INTERPOLATE FIELD, BFLD, WHICH IS CYCLIC IN THE
C                   SECOND DIMENSION, BASED UPON AYRES CENTRAL
C                   DIFFERENCE FORMULA WHICH PRODUCES VALUES THAT
C                   ARE CONTINUOUS IN THE FIRST DERIVATIVE.
C
C                   PROGRAMMER:   HARRY D. HAMILTON   (MMDS)  JUN 89
C
C                   INPUT:  (FORMAL PARAMETERS)
C                         RML  - REAL FIRST  DIMENSION LOCATION
C                         RNL  - REAL SECOND DIMENSION LOCATION
C                         BFLD - ARRAY OF VALUES FOR INTERPOLATION
C                         MGRD - FIRST  DIMENSION OF BFLD
C                         NGRD - SECOND DIMENSION OF BFLD
C
C                  OUTPUT:  (FORMAL PARAMETERS)
C                         VALI - INTERPOLATED VALUE
C                         IERR - ERROR FLAG, 0 - NO ERROR
C                                           -1 - OUT OF BOUNDS OF
C                                                INTERPOLATION AREA
C
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      DIMENSION BFLD(MGRD,NGRD)
      DIMENSION ECV(4), VFLD(16)
C
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
      IERR = 0
      M2   = RML
      IF (M2.LT.2 .OR. M2.GT.(MGRD -2)) IERR = -1
      IF (IERR .NE. 0) RETURN
C
C                   LOAD 4-BY-4 ARRAY, VFLD, FOR INTERPOLATION
      MS = M2 -1
      MT = M2 +2
      K  = 0
      N2 = RNL
      NS = N2 -1
      NT = N2 +2
      DO 120 N=NS, NT
      J = N
C                    ASSUME CYCLIC BOUNDARY CONDITIONS
      IF (J .LE. 0)    J = NGRD +J
      IF (J .GT. NGRD) J = J -NGRD
      DO 110 M=MS, MT
      K = K +1
      VFLD(K) = BFLD(M,J)
  110 CONTINUE
  120 CONTINUE
C
C                   PERFORM AYRES CENTRAL DIFFERENCES AND INTERPOLATION,
C                   FOUR TIMES
      F = RNL -N2
      DO 130 K=1, 4
      EV3M1  = VFLD(K+8) -VFLD(K)
      EV3M2  = VFLD(K+8) -VFLD(K+4)
      EV4M2  = 0.5*(VFLD(K+12) -VFLD(K+4))
      AA     = 0.5*EV3M1
      BB     = 3.0*EV3M2 -EV3M1 -EV4M2
      CC     = AA +EV4M2 -EV3M2 -EV3M2
      ECV(K) = VFLD(K+4) +F*(AA +F*(BB +F*CC))
  130 CONTINUE
C
C                   PERFORM AYRES CENTRAL DIFFERENCES
      EV3M1 = ECV(3) -ECV(1)
      EV3M2 = ECV(3) -ECV(2)
      EV4M2 = 0.5*(ECV(4) - ECV(2))
      AA    = 0.5*EV3M1
      BB    = 3.0*EV3M2 -EV3M1 -EV4M2
      CC    = AA +EV4M2 -EV3M2 -EV3M2
C
C                   PERFORM FINAL INTERPOLATION
      F    = RML -M2
      VALI = ECV(2) +F*(AA +F*(BB +F*CC))
C
      RETURN
C
      END
