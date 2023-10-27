c.. imslscopy.for         2956
c..-----------------------------------------------------------------------
c..  IMSL Name:  SCOPY (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Copy a vector X to a vector Y, both single precision.
c..
c..  Usage:      CALL SCOPY (N, SX, INCX, SY, INCY)
c..
c..  Arguments:
c..     N      - Length of vectors X and Y.  (Input)
c..     SX     - Real vector of length MAX(N*IABS(INCX),1).  (Input)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be.. SX(1+(I-1)*INCX) if INCX .GE. 0
c..              or SX(1+(I-N)*INCX) if INCX .LT. 0.
c..     SY     - Real vector of length MAX(N*IABS(INCY),1).  (Output)
c..              SCOPY copies X(I) to Y(I) for I=1,...,N. X(I) and Y(I)
c..              refer to specific elements of SX and SY, respectively.
c..              See INCX and INCY argument descriptions.
c..     INCY   - Displacement between elements of SY.  (Input)
c..              Y(I) is defined to be.. SY(1+(I-1)*INCY) if INCY .GE. 0
c..              or SY(1+(I-N)*INCY) if INCY .LT. 0.
c..
c..  Keywords:   Level 1 BLAS; SCOPY
c..
c..  GAMS:       D1a5
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      SUBROUTINE SCOPY (N, SX, INCX, SY, INCY)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX, INCY
      REAL       SX(*), SY(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IX, IY, M, MP1
c..                                  SPECIFICATIONS FOR SPECIAL CASES
c..     INTRINSIC  MOD
      INTRINSIC  MOD
      INTEGER    MOD
c..
      IF (N .GT. 0) THEN
         IF (INCX.NE.1 .OR. INCY.NE.1) THEN
c..                                  CODE FOR UNEQUAL INCREMENTS
            IX = 1
            IY = 1
            IF (INCX .LT. 0) IX = (-N+1)*INCX + 1
            IF (INCY .LT. 0) IY = (-N+1)*INCY + 1
            DO 10  I=1, N
               SY(IY) = SX(IX)
               IX = IX + INCX
               IY = IY + INCY
   10       CONTINUE
         ELSE
c..                                  CODE FOR BOTH INCREMENTS EQUAL TO 1
            M = MOD(N,7)
c..                                  CLEAN-UP LOOP
            DO 30  I=1, M
               SY(I) = SX(I)
   30       CONTINUE
            MP1 = M + 1
            DO 40  I=MP1, N, 7
               SY(I) = SX(I)
               SY(I+1) = SX(I+1)
               SY(I+2) = SX(I+2)
               SY(I+3) = SX(I+3)
               SY(I+4) = SX(I+4)
               SY(I+5) = SX(I+5)
               SY(I+6) = SX(I+6)
   40       CONTINUE
         END IF
      END IF
      RETURN
      END
c.. imslsnrm2.for         3967
c..-----------------------------------------------------------------------
c..  IMSL Name:  SNRM2 (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    November 24, 1991
c..
c..  Purpose:    Compute the Euclidean length or L2 norm of a
c..              single-precision vector.
c..
c..  Usage:      SNRM2(N, SX, INCX)
c..
c..  Arguments:
c..     N      - Length of vector X.  (Input)
c..     SX     - Real vector of length N*INCX.  (Input)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be SX(1+(I-1)*INCX). INCX must be
c..              positive.
c..     SNRM2  - Square root of the sum from I=1 to N of X(I)**2.
c..              (Output)
c..              X(I) refers to a specific element of SX. See INCX
c..              argument description.
c..
c..  Keywords:   Level 1 BLAS; SNRM2
c..
c..  GAMS:       D1a3b
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      REAL FUNCTION SNRM2 (N, SX, INCX)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX
      REAL       SX(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, J, NEXT, NN
      REAL       HITEST, SUM, XMAX
c..                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       CUTHI, CUTLO, ONE, ZERO
      SAVE       CUTHI, CUTLO, ONE, ZERO
c..                                  SPECIFICATIONS FOR INTRINSICS
c..     INTRINSIC  ABS,SQRT
      INTRINSIC  ABS, SQRT
      REAL       ABS, SQRT
c..
      DATA ZERO/0.0E0/, ONE/1.0E0/
      DATA CUTLO/4.441E-16/, CUTHI/1.304E19/
c..
      IF (N .GT. 0) GO TO 10
      SNRM2 = ZERO
      GO TO 140
c..
   10 ASSIGN 30 TO NEXT
      SUM = ZERO
      NN = N*INCX
c..                                  BEGIN MAIN LOOP
      I = 1
   20 GO TO NEXT, (30, 40, 70, 80)
   30 IF (ABS(SX(I)) .GT. CUTLO) GO TO 110
      ASSIGN 40 TO NEXT
      XMAX = ZERO
c..                                  PHASE 1. SUM IS ZERO
   40 IF (SX(I) .EQ. ZERO) GO TO 130
      IF (ABS(SX(I)) .GT. CUTLO) GO TO 110
c..                                  PREPARE FOR PHASE 2.
      ASSIGN 70 TO NEXT
      GO TO 60
c..                                  PREPARE FOR PHASE 4.
   50 I = J
      ASSIGN 80 TO NEXT
      SUM = (SUM/SX(I))/SX(I)
   60 XMAX = ABS(SX(I))
      GO TO 90
c..                                  PHASE 2. SUM IS SMALL. SCALE TO
c..                                  AVOID DESTRUCTIVE UNDERFLOW.
   70 IF (ABS(SX(I)) .GT. CUTLO) GO TO 100
c..                                  COMMON CODE FOR PHASES 2 AND 4. IN
c..                                  PHASE 4 SUM IS LARGE. SCALE TO
c..                                  AVOID OVERFLOW.
   80 IF (ABS(SX(I)) .LE. XMAX) GO TO 90
      SUM = ONE + SUM*(XMAX/SX(I))**2
      XMAX = ABS(SX(I))
      GO TO 130
c..
   90 SUM = SUM + (SX(I)/XMAX)**2
      GO TO 130
c..                                  PREPARE FOR PHASE 3.
  100 SUM = (SUM*XMAX)*XMAX
c..                                  FOR REAL OR D.P. SET HITEST =
c..                                  CUTHI/N FOR COMPLEX SET HITEST =
c..                                  CUTHI/(2*N)
  110 HITEST = CUTHI/N
c..                                  PHASE 3. SUM IS MID-RANGE. NO
c..                                  SCALING.
      DO 120  J=I, NN, INCX
         IF (ABS(SX(J)) .GE. HITEST) GO TO 50
  120 SUM = SUM + SX(J)*SX(J)
      SNRM2 = SQRT(SUM)
      GO TO 140
c..
  130 CONTINUE
      I = I + INCX
      IF (I .LE. NN) GO TO 20
c..                                  END OF MAIN LOOP. COMPUTE SQUARE
c..                                  ROOT AND ADJUST FOR SCALING.
      SNRM2 = XMAX*SQRT(SUM)
  140 CONTINUE
      RETURN
      END

c.. imslsscal.for         2407
c..-----------------------------------------------------------------------
c..  IMSL Name:  SSCAL (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Multiply a vector by a scalar, y = ay, both single
c..              precision.
c..
c..  Usage:      CALL SSCAL (N, SA, SX, INCX)
c..
c..  Arguments:
c..     N      - Length of vector X.  (Input)
c..     SA     - Real scalar.  (Input)
c..     SX     - Real vector of length N*INCX.  (Input/Output)
c..              SSCAL replaces X(I) with SA*X(I) for I=1,...,N. X(I)
c..              refers to a specific element of SX. See INCX argument
c..              description.
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be SX(1+(I-1)*INCX). INCX must be
c..              greater than zero.
c..
c..  Keywords:   Level 1 BLAS; SSCAL
c..
c..  GAMS:       D1a6
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      SUBROUTINE SSCAL (N, SA, SX, INCX)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX
      REAL       SA, SX(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, M, MP1, NS
c..
      IF (N .GT. 0) THEN
         IF (INCX .NE. 1) THEN
c..                                  CODE FOR INCREMENTS NOT EQUAL TO 1.
            NS = N*INCX
            DO 10  I=1, NS, INCX
               SX(I) = SA*SX(I)
   10       CONTINUE
         ELSE
c..                                  CODE FOR INCREMENTS EQUAL TO 1.
c..                                  CLEAN-UP LOOP SO REMAINING VECTOR
c..                                  LENGTH IS A MULTIPLE OF 5.
            M = N - (N/5)*5
            DO 30  I=1, M
               SX(I) = SA*SX(I)
   30       CONTINUE
            MP1 = M + 1
            DO 40  I=MP1, N, 5
               SX(I) = SA*SX(I)
               SX(I+1) = SA*SX(I+1)
               SX(I+2) = SA*SX(I+2)
               SX(I+3) = SA*SX(I+3)
               SX(I+4) = SA*SX(I+4)
   40       CONTINUE
         END IF
      END IF
      RETURN
      END

c.. imslisamax.for        2699
c..-----------------------------------------------------------------------
c..  IMSL Name:  ISAMAX (Single precision version)
c..
c..  Computer:   pcdsms/SINGLE
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Find the smallest index of the component of a
c..              single-precision vector having maximum absolute value.
c..
c..  Usage:      ISAMAX(N, SX, INCX)
c..
c..  Arguments:
c..     N      - Length of vector X.  (Input)
c..     SX     - Real vector of length N*INCX.  (Input)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be SX(1+(I-1)*INCX). INCX must be
c..              greater than zero.
c..     ISAMAX - The smallest index I such that ABS(X(I)) is the maximum
c..              of ABS(X(J)) for J=1 to N.  (Output)
c..              X(I) refers to a specific element of SX. see INCX
c..              argument description.
c..
c..  Keywords:   Level 1 BLAS; ISAMAX
c..
c..  GAMS:       D1a2; D1a3c
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      INTEGER FUNCTION ISAMAX (N, SX, INCX)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX
      REAL       SX(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, II, NS
      REAL       SMAX, XMAG
c..                                  SPECIFICATIONS FOR INTRINSICS
c..     INTRINSIC  ABS
      INTRINSIC  ABS
      REAL       ABS
c..
      ISAMAX = 0
      IF (N .GE. 1) THEN
         ISAMAX = 1
         IF (N .GT. 1) THEN
            IF (INCX .NE. 1) THEN
c..                                  CODE FOR INCREMENTS NOT EQUAL TO 1.
               SMAX = ABS(SX(1))
               NS = N*INCX
               II = 1
               DO 10  I=1, NS, INCX
                  XMAG = ABS(SX(I))
                  IF (XMAG .GT. SMAX) THEN
                     ISAMAX = II
                     SMAX = XMAG
                  END IF
                  II = II + 1
   10          CONTINUE
            ELSE
c..                                  CODE FOR INCREMENTS EQUAL TO 1.
               SMAX = ABS(SX(1))
               DO 20  I=2, N
                  XMAG = ABS(SX(I))
                  IF (XMAG .GT. SMAX) THEN
                     ISAMAX = I
                     SMAX = XMAG
                  END IF
   20          CONTINUE
            END IF
         END IF
      END IF
      RETURN
      END

c.. imslsswap.for         3110
c..-----------------------------------------------------------------------
c..  IMSL Name:  SSWAP (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Interchange vectors X and Y, both single precision.
c..
c..  Usage:      CALL SSWAP (N, SX, INCX, SY, INCY)
c..
c..  Arguments:
c..     N      - Length of vectors X and Y.  (Input)
c..     SX     - Real vector of length MAX(N*IABS(INCX),1).
c..              (Input/Output)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be
c..                 SX(1+(I-1)*INCX) if INCX.GE.0  or
c..                 SX(1+(I-N)*INCX) if INCX.LT.0.
c..     SY     - Real vector of length MAX(N*IABS(INCY),1).
c..              (Input/Output)
c..     INCY   - Displacement between elements of SY.  (Input)
c..              Y(I) is defined to be
c..                 SY(1+(I-1)*INCY) if INCY.GE.0  or
c..                 SY(1+(I-N)*INCY) if INCY.LT.0.
c..
c..  Keywords:   Level 1 BLAS; SSWAP; Swap; Exchange
c..
c..  GAMS:       D1a5
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      SUBROUTINE SSWAP (N, SX, INCX, SY, INCY)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX, INCY
      REAL       SX(*), SY(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IX, IY, M, MP1
      REAL       STEMP
c..                                  SPECIFICATIONS FOR SPECIAL CASES
c..     INTRINSIC  MOD
      INTRINSIC  MOD
      INTEGER    MOD
c..
      IF (N .GT. 0) THEN
         IF (INCX.NE.1 .OR. INCY.NE.1) THEN
c..                                  CODE FOR UNEQUAL INCREMENTS OR EQUAL
c..                                    INCREMENTS NOT EQUAL TO 1
            IX = 1
            IY = 1
            IF (INCX .LT. 0) IX = (-N+1)*INCX + 1
            IF (INCY .LT. 0) IY = (-N+1)*INCY + 1
            DO 10  I=1, N
               STEMP = SX(IX)
               SX(IX) = SY(IY)
               SY(IY) = STEMP
               IX = IX + INCX
               IY = IY + INCY
   10       CONTINUE
         ELSE
c..                                  CODE FOR BOTH INCREMENTS EQUAL TO 1
            M = MOD(N,3)
c..                                  CLEAN-UP LOOP
            DO 30  I=1, M
               STEMP = SX(I)
               SX(I) = SY(I)
               SY(I) = STEMP
   30       CONTINUE
            MP1 = M + 1
            DO 40  I=MP1, N, 3
               STEMP = SX(I)
               SX(I) = SY(I)
               SY(I) = STEMP
               STEMP = SX(I+1)
               SX(I+1) = SY(I+1)
               SY(I+1) = STEMP
               STEMP = SX(I+2)
               SX(I+2) = SY(I+2)
               SY(I+2) = STEMP
   40       CONTINUE
         END IF
      END IF
      RETURN
      END
c.. imslsrotmg.for        6760
c..-----------------------------------------------------------------------
c..  IMSL Name:  SROTMG (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Construct a modified Givens plane rotation in single
c..              precision.
c..
c..  Usage:      CALL SROTMG (SD1, SD2, SX1, SY1, SPARAM)
c..
c..  Arguments:
c..     SD1    - Scale factor.  (Input/Output)
c..              On input, SD1 contains the first scale factor.  On
c..              output, SD1 contains the updated scale factor.
c..     SD2    - Scale factor.  (Input/Output)
c..              On input, SD2 contains the second scale factor.  On
c..              output, SD2 contains the updated scale factor.
c..     SX1    - On input, SX1 contains the first component of the vector
c..              to be rotated.  On output SX1 contains the rotated value
c..              of the first component .  (Input/Output)
c..     SY1    - Second component of the vector to be rotated.  (Input)
c..              Since this component is zeroed by the rotation, it is
c..              left unchanged in storage.
c..     SPARAM - Real vector of length 5 which defines the rotation matrix
c..              H.  (Input/Output)
c..              See remark.
c..
c..  Remark:
c..     SROTMG constructs a modified Givens rotation H and updates the
c..     scale factors SD1 and SD2 which zero SY1. The transformed value of
c..     SD1 replaces SD1, i.e.
c..     On input,  SW1  =  SQRT(SD1)*SX1
c..                SZ1  =  SQRT(SD2)*SY1.
c..     On output, ( C  S ) (SW1) = (C*SW1 + S*SZ1) = (SQRT(SD1)*SX1)
c..                (-S  C ) (SZ1) = (      0      ) = (      0       )
c..     where C and S define a Givens rotation. H takes the form
c..     SPARAM(1) = -2.0
c..       SPARAM(2) = UNCHANGED   SPARAM(4) = UNCHANGED
c..       SPARAM(3) = UNCHANGED   SPARAM(5) = UNCHANGED
c..     SPARAM(1) = -1.0
c..       SPARAM(2) = H11         SPARAM(4) = H12
c..       SPARAM(3) = H21         SPARAM(5) = H22
c..     SPARAM(1) = 0.0
c..       SPARAM(2) = UNCHANGED   SPARAM(4) = H12
c..       SPARAM(3) = H21         SPARAM(5) = UNCHANGED
c..     SPARAM(1) = 1.0
c..       SPARAM(2) = H11         SPARAM(4) = UNCHANGED
c..       SPARAM(3) = UNCHANGED   SPARAM(5) = H22
c..
c..  Keywords:   Level 1 BLAS; SROTMG
c..
c..  GAMS:       D1b10
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      SUBROUTINE SROTMG (SD1, SD2, SX1, SY1, SPARAM)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       SD1, SD2, SX1, SY1, SPARAM(5)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IGO
      REAL       SFLAG, SH11, SH12, SH21, SH22, SP1, SP2, SQ1, SQ2,
     &           STEMP, SU
c..                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       GAM, GAMSQ, ONE, RGAMSQ, TWO, ZERO
      SAVE       GAM, GAMSQ, ONE, RGAMSQ, TWO, ZERO
c..                                  SPECIFICATIONS FOR INTRINSICS
c..     INTRINSIC  ABS
      INTRINSIC  ABS
      REAL       ABS
c..
      DATA ZERO, ONE, TWO/0.0E0, 1.0E0, 2.0E0/
      DATA GAM, GAMSQ, RGAMSQ/4096.0E0, 1.678E7, 5.96E-8/
c..
      IF (.NOT.SD1 .LT. ZERO) GO TO 10
c..                                  GO ZERO-H-D-AND-SX1..
      GO TO 60
   10 CONTINUE
c..                                  CASE-SD1-NONNEGATIVE
      SP2 = SD2*SY1
      IF (.NOT.SP2 .EQ. ZERO) GO TO 20
      SFLAG = -TWO
      GO TO 270
c..                                  REGULAR-CASE..
   20 CONTINUE
      SP1 = SD1*SX1
      SQ2 = SP2*SY1
      SQ1 = SP1*SX1
c..
      IF (.NOT.ABS(SQ1) .GT. ABS(SQ2)) GO TO 40
      SH21 = -SY1/SX1
      SH12 = SP2/SP1
c..
      SU = ONE - SH12*SH21
c..
      IF (.NOT.SU .LE. ZERO) GO TO 30
c..                                  GO ZERO-H-D-AND-SX1..
      GO TO 60
   30 CONTINUE
      SFLAG = ZERO
      SD1 = SD1/SU
      SD2 = SD2/SU
      SX1 = SX1*SU
c..                                  GO SCALE-CHECK..
      GO TO 100
   40 CONTINUE
      IF (.NOT.SQ2 .LT. ZERO) GO TO 50
c..                                  GO ZERO-H-D-AND-SX1..
      GO TO 60
   50 CONTINUE
      SFLAG = ONE
      SH11 = SP1/SP2
      SH22 = SX1/SY1
      SU = ONE + SH11*SH22
      STEMP = SD2/SU
      SD2 = SD1/SU
      SD1 = STEMP
      SX1 = SY1*SU
c..                                  GO SCALE-CHECK
      GO TO 100
c..                                  PROCEDURE..ZERO-H-D-AND-SX1..
   60 CONTINUE
      SFLAG = -ONE
      SH11 = ZERO
      SH12 = ZERO
      SH21 = ZERO
      SH22 = ZERO
c..
      SD1 = ZERO
      SD2 = ZERO
      SX1 = ZERO
c..                                  RETURN..
      GO TO 230
c..                                  PROCEDURE..FIX-H..
   70 CONTINUE
      IF (.NOT.SFLAG .GE. ZERO) GO TO 90
c..
      IF (.NOT.SFLAG .EQ. ZERO) GO TO 80
      SH11 = ONE
      SH22 = ONE
      SFLAG = -ONE
      GO TO 90
   80 CONTINUE
      SH21 = -ONE
      SH12 = ONE
      SFLAG = -ONE
   90 CONTINUE
      GO TO IGO, (130, 160, 190, 220)
c..                                  PROCEDURE..SCALE-CHECK
  100 CONTINUE
  110 CONTINUE
      IF (.NOT.SD1 .LE. RGAMSQ) GO TO 140
      IF (SD1 .EQ. ZERO) GO TO 170
      ASSIGN 130 TO IGO
c..                                  FIX-H..
      GO TO 70
  130 CONTINUE
      SD1 = SD1*GAM**2
      SX1 = SX1/GAM
      SH11 = SH11/GAM
      SH12 = SH12/GAM
      GO TO 110
  140 CONTINUE
  150 CONTINUE
      IF (.NOT.SD1 .GE. GAMSQ) GO TO 170
      ASSIGN 160 TO IGO
c..                                  FIX-H..
      GO TO 70
  160 CONTINUE
      SD1 = SD1/GAM**2
      SX1 = SX1*GAM
      SH11 = SH11*GAM
      SH12 = SH12*GAM
      GO TO 150
  170 CONTINUE
  180 CONTINUE
      IF (.NOT.ABS(SD2) .LE. RGAMSQ) GO TO 200
      IF (SD2 .EQ. ZERO) GO TO 230
      ASSIGN 190 TO IGO
c..                                  FIX-H..
      GO TO 70
  190 CONTINUE
      SD2 = SD2*GAM**2
      SH21 = SH21/GAM
      SH22 = SH22/GAM
      GO TO 180
  200 CONTINUE
  210 CONTINUE
      IF (.NOT.ABS(SD2) .GE. GAMSQ) GO TO 230
      ASSIGN 220 TO IGO
c..                                  FIX-H..
      GO TO 70
  220 CONTINUE
      SD2 = SD2/GAM**2
      SH21 = SH21*GAM
      SH22 = SH22*GAM
      GO TO 210
  230 CONTINUE
      IF (SFLAG) 260,240,250
  240 CONTINUE
      SPARAM(3) = SH21
      SPARAM(4) = SH12
      GO TO 270
  250 CONTINUE
      SPARAM(2) = SH11
      SPARAM(5) = SH22
      GO TO 270
  260 CONTINUE
      SPARAM(2) = SH11
      SPARAM(3) = SH21
      SPARAM(4) = SH12
      SPARAM(5) = SH22
  270 CONTINUE
      SPARAM(1) = SFLAG
      RETURN
      END
c.. imslsrotm.for         5623
c..-----------------------------------------------------------------------
c..  IMSL Name:  SROTM (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Apply a modified Givens plane rotation in single
c..              precision.
c..
c..  Usage:      CALL SROTM (N, SX, INCX, SY, INCY, SPARAM)
c..
c..  Arguments:
c..     N      - Length of vectors X and Y.  (Input)
c..     SX     - Real vector of length MAX(N*IABS(INCX),1).
c..              (Input/Output)
c..              SROTM replaces X(I) with H11*X(I)+H12*Y(I) for I=1,...,N.
c..              X(I) and Y(I) refer to specific elements of SX and SY.
c..              The H components refer to the rotation defined by SPARAM.
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be
c..                 SX(1+(I-1)*INCX) if INCX.GE.0  or
c..                 SX(1+(I-N)*INCX) if INCX.LT.0.
c..     SY     - Real vector of length MAX(N*IABS(INCY),1).
c..              (Input/Output)
c..              SROTM replaces Y(I) with H21*X(I)+H22*Y(I) for I=1,...,N.
c..              X(I) and Y(I) refer to specific elements of SX and SY.
c..              The H components refer to the rotation defined by SPARAM.
c..     INCY   - Displacement between elements of SY.  (Input)
c..              Y(I) is defined to be
c..                 SY(1+(I-1)*INCY) if INCY.GE.0  or
c..                 SY(1+(I-N)*INCY) if INCY.LT.0.
c..     SPARAM - Real vector of length 5 which defines the rotation matrix
c..              H.  (Input)
c..              See remark.
c..
c..  Remark:
c..     SROTM applies the modified Givens rotation H to the 2 by N matrix
c..                         ( X(1) ... X(N) )
c..                         ( Y(1) ... Y(N) )
c..     H takes one of the following forms,
c..     SPARAM(1) = -2.0
c..       H11 = 1.0        H12 = 0.0
c..       H21 = 0.0        H22 = 1.0
c..     SPARAM(1) = -1.0
c..       H11 = SPARAM(2)  H12 = SPARAM(4)
c..       H21 = SPARAM(3)  H22 = SPARAM(5)
c..     SPARAM(1) = 0.0
c..       H11 = 1.0        H12 = SPARAM(4)
c..       H21 = SPARAM(3)  H22 = 1.0
c..     SPARAM(1) = 1.0
c..       H11 = SPARAM(2)  H12 = 1.0
c..       H21 = -1.0       H22 = SPARAM(5)
c..
c..  Keywords:   Level 1 BLAS; SROTM
c..
c..  GAMS:       D1a8
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      SUBROUTINE SROTM (N, SX, INCX, SY, INCY, SPARAM)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX, INCY
      REAL       SX(*), SY(*), SPARAM(5)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, KX, KY
      REAL       SFLAG, SH11, SH12, SH21, SH22, W, Z
c..
      SFLAG = SPARAM(1)
      IF (N.GT.0 .AND. (SFLAG.NE.-2.0E0)) THEN
c..                                  CODE FOR BOTH INCREMENTS EQUAL TO 1
         IF (INCX.EQ.1 .AND. INCY.EQ.1) THEN
            IF (SFLAG .EQ. 0.0E0) THEN
               SH12 = SPARAM(4)
               SH21 = SPARAM(3)
               DO 10  I=1, N
                  W = SX(I)
                  Z = SY(I)
                  SX(I) = W + Z*SH12
                  SY(I) = W*SH21 + Z
   10          CONTINUE
            ELSE IF (SFLAG .GT. 0.0E0) THEN
               SH11 = SPARAM(2)
               SH22 = SPARAM(5)
               DO 20  I=1, N
                  W = SX(I)
                  Z = SY(I)
                  SX(I) = W*SH11 + Z
                  SY(I) = -W + SH22*Z
   20          CONTINUE
            ELSE IF (SFLAG .LT. 0.0E0) THEN
               SH11 = SPARAM(2)
               SH12 = SPARAM(4)
               SH21 = SPARAM(3)
               SH22 = SPARAM(5)
               DO 30  I=1, N
                  W = SX(I)
                  Z = SY(I)
                  SX(I) = W*SH11 + Z*SH12
                  SY(I) = W*SH21 + Z*SH22
   30          CONTINUE
            END IF
c..                                  CODE FOR UNEQUAL INCREMENTS OR EQUAL
c..                                    INCREMENTS NOT EQUAL TO 1
         ELSE
            KX = 1
            KY = 1
            IF (INCX .LT. 0) KX = 1 + (1-N)*INCX
            IF (INCY .LT. 0) KY = 1 + (1-N)*INCY
            IF (SFLAG .EQ. 0.0E0) THEN
               SH12 = SPARAM(4)
               SH21 = SPARAM(3)
               DO 40  I=1, N
                  W = SX(KX)
                  Z = SY(KY)
                  SX(KX) = W + Z*SH12
                  SY(KY) = W*SH21 + Z
                  KX = KX + INCX
                  KY = KY + INCY
   40          CONTINUE
            ELSE IF (SFLAG .GT. 0.0E0) THEN
               SH11 = SPARAM(2)
               SH22 = SPARAM(5)
               DO 50  I=1, N
                  W = SX(KX)
                  Z = SY(KY)
                  SX(KX) = W*SH11 + Z
                  SY(KY) = -W + SH22*Z
                  KX = KX + INCX
                  KY = KY + INCY
   50          CONTINUE
            ELSE IF (SFLAG .LT. 0.0E0) THEN
               SH11 = SPARAM(2)
               SH12 = SPARAM(4)
               SH21 = SPARAM(3)
               SH22 = SPARAM(5)
               DO 60  I=1, N
                  W = SX(KX)
                  Z = SY(KY)
                  SX(KX) = W*SH11 + Z*SH12
                  SY(KY) = W*SH21 + Z*SH22
                  KX = KX + INCX
                  KY = KY + INCY
   60          CONTINUE
            END IF
         END IF
      END IF
      RETURN
      END

c.. imslsaxpy.for         3204
c..-----------------------------------------------------------------------
c..  IMSL Name:  SAXPY (Single precision version)
c..
c..  Computer:   pcdsms/SINGLE
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Compute the scalar times a vector plus a vector,
c..              y = ax + y, all single precision.
c..
c..  Usage:      CALL SAXPY (N, SA, SX, INCX, SY, INCY)
c..
c..  Arguments:
c..     N      - Length of vectors X and Y.  (Input)
c..     SA     - Real scalar.  (Input)
c..     SX     - Real vector of length MAX(N*IABS(INCX),1).  (Input)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be
c..                 SX(1+(I-1)*INCX) if INCX.GE.0  or
c..                 SX(1+(I-N)*INCX) if INCX.LT.0.
c..     SY     - Real vector of length MAX(N*IABS(INCY),1).
c..              (Input/Output)
c..              SAXPY replaces Y(I) with SA*X(I) + Y(I) for I=1,...,N.
c..              X(I) and Y(I) refer to specific elements of SX and SY.
c..     INCY   - Displacement between elements of SY.  (Input)
c..              Y(I) is defined to be
c..                 SY(1+(I-1)*INCY) if INCY.GE.0  or
c..                 SY(1+(I-N)*INCY) if INCY.LT.0.
c..
c..  Keywords:   Level 1 BLAS; SAXPY
c..
c..  GAMS:       D1a7
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      SUBROUTINE SAXPY (N, SA, SX, INCX, SY, INCY)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX, INCY
      REAL       SA, SX(*), SY(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IX, IY, M, MP1
c..                                  SPECIFICATIONS FOR SPECIAL CASES
c..     INTRINSIC  MOD
      INTRINSIC  MOD
      INTEGER    MOD
c..
      IF (N .GT. 0) THEN
         IF (SA .NE. 0.0) THEN
            IF (INCX.NE.1 .OR. INCY.NE.1) THEN
c..                                  CODE FOR UNEQUAL INCREMENTS OR EQUAL
c..                                  INCREMENTS NOT EQUAL TO 1
               IX = 1
               IY = 1
               IF (INCX .LT. 0) IX = (-N+1)*INCX + 1
               IF (INCY .LT. 0) IY = (-N+1)*INCY + 1
               DO 10  I=1, N
                  SY(IY) = SY(IY) + SA*SX(IX)
                  IX = IX + INCX
                  IY = IY + INCY
   10          CONTINUE
            ELSE
c..                                  CODE FOR BOTH INCREMENTS EQUAL TO 1
               M = MOD(N,4)
c..                                  CLEAN-UP LOOP
               DO 30  I=1, M
                  SY(I) = SY(I) + SA*SX(I)
   30          CONTINUE
               MP1 = M + 1
               DO 40  I=MP1, N, 4
                  SY(I) = SY(I) + SA*SX(I)
                  SY(I+1) = SY(I+1) + SA*SX(I+1)
                  SY(I+2) = SY(I+2) + SA*SX(I+2)
                  SY(I+3) = SY(I+3) + SA*SX(I+3)
   40          CONTINUE
            END IF
         END IF
      END IF
      RETURN
      END
c.. imslsdot.for          2966
c..-----------------------------------------------------------------------
c..  IMSL Name:  SDOT (Single precision version)
c..
c..  Computer:   pcdsms/SINGLEX
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Compute the single-precision dot product x*y.
c..
c..  Usage:      SDOT(N, SX, INCX, SY, INCY)
c..
c..  Arguments:
c..     N      - Length of vectors X and Y.  (Input)
c..     SX     - Real vector of length MAX(N*IABS(INCX),1).  (Input)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be.. SX(1+(I-1)*INCX) if INCX .GE. 0
c..              or SX(1+(I-N)*INCX) if INCX .LT. 0.
c..     SY     - Real vector of length MAX(N*IABS(INCY),1).  (Input)
c..     INCY   - Displacement between elements of SY.  (Input)
c..              Y(I) is defined to be.. SY(1+(I-1)*INCY) if INCY .GE. 0
c..              or SY(1+(I-N)*INCY) if INCY .LT. 0.
c..     SDOT   - Sum from I=1 to N of X(I)*Y(I).  (Output)
c..              X(I) and Y(I) refer to specific elements of SX and SY,
c..              respectively.  See INCX and INCY argument descriptions.
c..
c..  Keywords:   Level 1 BLAS; SDOT; Inner product; Scalar product
c..
c..  GAMS:       D1a4
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      REAL FUNCTION SDOT (N, SX, INCX, SY, INCY)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX, INCY
      REAL       SX(*), SY(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IX, IY, M, MP1
c..                                  SPECIFICATIONS FOR SPECIAL CASES
c..     INTRINSIC  MOD
      INTRINSIC  MOD
      INTEGER    MOD
c..
      SDOT = 0.0E0
      IF (N .GT. 0) THEN
         IF (INCX.NE.1 .OR. INCY.NE.1) THEN
c..                                  CODE FOR UNEQUAL INCREMENTS
            IX = 1
            IY = 1
            IF (INCX .LT. 0) IX = (-N+1)*INCX + 1
            IF (INCY .LT. 0) IY = (-N+1)*INCY + 1
            DO 10  I=1, N
               SDOT = SDOT + SX(IX)*SY(IY)
               IX = IX + INCX
               IY = IY + INCY
   10       CONTINUE
         ELSE
c..                                  CODE FOR BOTH INCREMENTS EQUAL TO 1
            M = MOD(N,5)
c..                                  CLEAN-UP LOOP SO REMAINING VECTOR
            DO 30  I=1, M
               SDOT = SDOT + SX(I)*SY(I)
   30       CONTINUE
            MP1 = M + 1
            DO 40  I=MP1, N, 5
               SDOT = SDOT + SX(I)*SY(I) + SX(I+1)*SY(I+1) +
     &                SX(I+2)*SY(I+2) + SX(I+3)*SY(I+3) +
     &                SX(I+4)*SY(I+4)
   40       CONTINUE
         END IF
      END IF
      RETURN
      END
c.. imslsasum.for         2541
c..-----------------------------------------------------------------------
c..  IMSL Name:  SASUM (Single precision version)
c..
c..  Computer:   pcdsms/SINGLE
c..
c..  Revised:    August 9, 1986
c..
c..  Purpose:    Sum the absolute values of the components of a
c..              single precision vector.
c..
c..  Usage:      SASUM(N, SX, INCX)
c..
c..  Arguments:
c..     N      - Length of vectors X.  (Input)
c..     SX     - Real vector of length N*INCX.  (Input)
c..     INCX   - Displacement between elements of SX.  (Input)
c..              X(I) is defined to be SX(1+(I-1)*INCX). INCX must be
c..              greater than 0.
c..     SASUM  - Single precision sum from I=1 to N of ABS(X(I)).
c..              (Output)
c..              X(I) refers to a specific element of SX.
c..
c..  Keywords:   Level 1 BLAS; SASUM
c..
c..  GAMS:       D1a3a
c..
c..  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
c..              STAT/LIBRARY Mathematical Support
c..
c..  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
c..
c..  Warranty:   IMSL warrants only that IMSL testing has been applied
c..              to this code.  No other warranty, expressed or implied,
c..              is applicable.
c..
c..-----------------------------------------------------------------------
c..
      REAL FUNCTION SASUM (N, SX, INCX)
c..                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX
      REAL       SX(*)
c..                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, M, MP1, NINCX
c..                                  SPECIFICATIONS FOR SPECIAL CASES
c..     INTRINSIC  MOD
      INTRINSIC  MOD
      INTEGER    MOD
c..                                  SPECIFICATIONS FOR INTRINSICS
c..     INTRINSIC  ABS
      INTRINSIC  ABS
      REAL       ABS
c..
      SASUM = 0.0E0
      IF (N .GT. 0) THEN
         IF (INCX .NE. 1) THEN
c..                                  CODE FOR INCREMENT NOT EQUAL TO 1
            NINCX = N*INCX
            DO 10  I=1, NINCX, INCX
               SASUM = SASUM + ABS(SX(I))
   10       CONTINUE
         ELSE
c..                                  CODE FOR INCREMENT EQUAL TO 1
            M = MOD(N,6)
c..                                  CLEAN-UP LOOP
            DO 30  I=1, M
               SASUM = SASUM + ABS(SX(I))
   30       CONTINUE
            MP1 = M + 1
            DO 40  I=MP1, N, 6
               SASUM = SASUM + ABS(SX(I)) + ABS(SX(I+1)) +
     &                 ABS(SX(I+2)) + ABS(SX(I+3)) + ABS(SX(I+4)) +
     &                 ABS(SX(I+5))
   40       CONTINUE
         END IF
      END IF
      RETURN
      END

