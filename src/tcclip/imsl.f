C-----------------------------------------------------------------------
C  IMSL Name:  ALBETA (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the natural logarithm of the complete beta
C              function for positive arguments.
C
C  Usage:      ALBETA(A, B)
C
C  Arguments:
C     A      - The first argument of the BETA function.  (Input)
C     B      - The second argument of the BETA function.  (Input)
C     ALBETA - Function value.  (Output)
C
C  Remarks:
C  1. ALBETA returns the natural log of
C     BETA(A,B) = ALOG (GAMMA(A)*GAMMA(B))/GAMMA(A+B)
C
C  2. Note than the natural log of BETA(A,B) equals the natural log
C     of BETA(B,A).
C
C  3. ALBETA (A,B) returns accurate results even when A or B is very
C     small.
C
C  4. The arguments, A and B, must be greater than 0.
C
C  GAMS:       C7b
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION ALBETA (A, B)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       A, B
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      REAL       CORR, P, Q, TEMP
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       SQ2PIL
      SAVE       SQ2PIL
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ALOG,AMAX1,AMIN1
      INTRINSIC  ALOG, AMAX1, AMIN1
      REAL       ALOG, AMAX1, AMIN1
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   ALNGAM, ALNREL, AMACH, GAMMA, N1RCD, R9LGMC
      INTEGER    N1RCD
      REAL       ALNGAM, ALNREL, AMACH, GAMMA, R9LGMC
C
      DATA SQ2PIL/.91893853320467274E0/
C
      CALL E1PSH ('ALBETA')
      ALBETA = AMACH(6)
C
      P = AMIN1(A,B)
      Q = AMAX1(A,B)
C
      IF (P .LE. 0.0) THEN
         CALL E1MES (5, 5, 'Both arguments for the function '//
     &               'must be greater than zero.')
C
      ELSE IF (P .GE. 10.0) THEN
C                                  P AND Q ARE BIG
         CORR = R9LGMC(P) + R9LGMC(Q) - R9LGMC(P+Q)
C                                  CHECK FOR UNDERFLOW FROM R9LGMC
         IF (N1RCD(1) .EQ. 1) CALL E1MES (0, 0, ' ')
         TEMP = ALNREL(-P/(P+Q))
         ALBETA = -0.5*ALOG(Q) + SQ2PIL + CORR +
     &            (P-0.5)*ALOG(P/(P+Q)) + Q*TEMP
C
      ELSE IF (Q .GE. 10.0) THEN
C                                  P IS SMALL, BUT Q IS BIG
         CORR = R9LGMC(Q) - R9LGMC(P+Q)
C                                  CHECK FOR UNDERFLOW FROM R9LGMC
         IF (N1RCD(1) .EQ. 1) CALL E1MES (0, 0, ' ')
         ALBETA = ALNGAM(P) + CORR + P - P*ALOG(P+Q) +
     &            (Q-0.5)*ALNREL(-P/(P+Q))
C
      ELSE
C                                  P AND Q ARE SMALL
         ALBETA = ALOG(GAMMA(P)*(GAMMA(Q)/GAMMA(P+Q)))
      END IF
C
      CALL E1POP ('ALBETA')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  ALNGAM (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the logarithm of the absolute value of the
C              gamma function.
C
C  Usage:      ALNGAM(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     ALNGAM - Function value.  (Output)
C
C  Remark:
C     Informational error:
C     Type Code
C       3   2  Result of ALNGAM(X) is accurate to less than one half
C              precision because X is too near a negative integer.
C
C  GAMS:       C7a
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION ALNGAM (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      REAL       SINPIY, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       DXREL, PI, SQ2PIL, SQPI2L, XMAX
      SAVE       DXREL, PI, SQ2PIL, SQPI2L, XMAX
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,AINT,ALOG,SIN,SQRT
      INTRINSIC  ABS, AINT, ALOG, SIN, SQRT
      REAL       ABS, AINT, ALOG, SIN, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, GAMMA, R9LGMC
      REAL       AMACH, GAMMA, R9LGMC
C
      DATA PI/3.14159265358979324E0/
C                                  SQ2PIL = ALOG(SQRT(2.*PI))
C                                  SQPI2L = ALOG (SQRT(PI/2.))
      DATA SQ2PIL/0.91893853320467274E0/
      DATA SQPI2L/0.22579135264472743E0/
C
      DATA XMAX/0.0/, DXREL/0.0/
C
      CALL E1PSH ('ALNGAM')
      ALNGAM = AMACH(6)
C
      IF (XMAX .EQ. 0.0) THEN
         XMAX = AMACH(2)/ALOG(AMACH(2))
         DXREL = SQRT(AMACH(4))
      END IF
C
      Y = ABS(X)
C                                  ALOG (ABS (GAMMA(X))) FOR
C                                  ABS(X) .LE. 10.0
      IF (Y .LE. 10.0) THEN
         ALNGAM = ALOG(ABS(GAMMA(X)))
C                                  ALOG (ABS (GAMMA(X))) FOR
C                                  ABS(X) .GT. 10.0
      ELSE IF (Y .GT. XMAX) THEN
         CALL E1STR (1, X)
         CALL E1STR (2, XMAX)
         CALL E1MES (5, 4, 'The function overflows because '//
     &               'ABS(%(R1)) is greater than %(R2).')
C
      ELSE IF (X .GT. 0.0) THEN
         ALNGAM = SQ2PIL + (X-0.5)*ALOG(X) - X + R9LGMC(Y)
C
      ELSE
         SINPIY = ABS(SIN(PI*Y))
         IF (SINPIY .EQ. 0.0) THEN
            CALL E1STR (1, X)
            CALL E1MES (5, 5, 'The argument for the function can '//
     &                  'not be a negative integer. Argument X = '//
     &                  '%(R1).')
C
         ELSE
            ALNGAM = SQPI2L + (X-0.5)*ALOG(Y) - X - ALOG(SINPIY) -
     &               R9LGMC(Y)
C
            IF (ABS((X-AINT(X-0.5))*ALNGAM/X) .LT. DXREL) THEN
               CALL E1STR (1, X)
               CALL E1MES (3, 2, 'The result is accurate to less '//
     &                     'than one half precision because X = '//
     &                     '%(R1) is too close to a negative '//
     &                     'integer.')
            END IF
         END IF
      END IF
C
      CALL E1POP ('ALNGAM')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  ALNREL (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the natural logarithm of one plus the argument.
C
C  Usage:      ALNREL(X)
C
C  Arguments:
C     X      - Argument for the function.  (Input)
C     ALNREL - Function value.  (Output)
C
C  Remarks:
C  1. Informational error
C     Type Code
C       3   2  Result of ALNREL(X) is accurate to less than one half
C              precision because X is too near -1.0.
C
C  2. ALNREL evaluates the natural logarithm of (1+X) accurate in
C     the sense of relative error even when X is very small. This
C     routine (as opposed to ALOG) should be used to maintain relative
C     accuracy whenever X is small and accurately known.
C
C  GAMS:       C4b
C
C  Chapter:    SFUN/LIBRARY Elementary Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION ALNREL (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NLNREL
      REAL       ALNRCS(23), XMIN
      SAVE       ALNRCS, NLNREL, XMIN
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,ALOG,SQRT
      INTRINSIC  ABS, ALOG, SQRT
      REAL       ABS, ALOG, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, CSEVL, INITS
      INTEGER    INITS
      REAL       AMACH, CSEVL
C
C                                  SERIES FOR ALNR ON THE INTERVAL
C                                  -3.75000E-01 TO  3.75000E-01
C                                  WITH WEIGHTED ERROR        1.93E-17
C                                  LOG WEIGHTED ERROR        16.72
C                                  SIGNIFICANT FIGURES REQD. 16.44
C                                  DECIMAL PLACES REQUIRED   17.40
C
      DATA ALNRCS(1)/.1037869356274377E1/
      DATA ALNRCS(2)/-.13364301504908918E0/
      DATA ALNRCS(3)/.019408249135520563E0/
      DATA ALNRCS(4)/-.003010755112753577E0/
      DATA ALNRCS(5)/.000486946147971548E0/
      DATA ALNRCS(6)/-.000081054881893175E0/
      DATA ALNRCS(7)/.000013778847799559E0/
      DATA ALNRCS(8)/-.000002380221089435E0/
      DATA ALNRCS(9)/.000000416404162138E0/
      DATA ALNRCS(10)/-.000000073595828378E0/
      DATA ALNRCS(11)/.000000013117611876E0/
      DATA ALNRCS(12)/-.000000002354670931E0/
      DATA ALNRCS(13)/.000000000425227732E0/
      DATA ALNRCS(14)/-.000000000077190894E0/
      DATA ALNRCS(15)/.000000000014075746E0/
      DATA ALNRCS(16)/-.000000000002576907E0/
      DATA ALNRCS(17)/.000000000000473424E0/
      DATA ALNRCS(18)/-.000000000000087249E0/
      DATA ALNRCS(19)/.000000000000016124E0/
      DATA ALNRCS(20)/-.000000000000002987E0/
      DATA ALNRCS(21)/.000000000000000554E0/
      DATA ALNRCS(22)/-.000000000000000103E0/
      DATA ALNRCS(23)/.000000000000000019E0/
C
      DATA NLNREL/0/, XMIN/0.0/
C
      CALL E1PSH ('ALNREL')
      ALNREL = AMACH(6)
C
      IF (NLNREL .EQ. 0) THEN
         NLNREL = INITS(ALNRCS,23,0.1*AMACH(3))
         XMIN = -1.0 + SQRT(AMACH(4))
      END IF
C
      IF (X .LE. -1.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (5, 5, 'The argument X = %(R1) must be '//
     &               'greater than -1.0.')
C
      ELSE
         IF (ABS(X) .LE. 0.375) THEN
            ALNREL = X*(1.0-X*CSEVL(X/.375,ALNRCS,NLNREL))
         ELSE
            ALNREL = ALOG(1.0+X)
         END IF
C
         IF (X .LT. XMIN) THEN
            CALL E1STR (1, X)
            CALL E1STR (2, XMIN)
            CALL E1MES (3, 2, 'The result is accurate to less '//
     &                  'than one half precision because X = %(R1) '//
     &                  'is too close to -1.0. X must be greater '//
     &                  'than %(R2).')
         END IF
      END IF
C
      CALL E1POP ('ALNREL')
      RETURN
      END

C-----------------------------------------------------------------------
C  IMSL Name:  AMACH (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 15, 1984
C
C  Purpose:    Retrieve single-precision machine constants.
C
C  Usage:      AMACH(N)
C
C  Arguments:
C     N      - Index of desired constant.  (Input)
C     AMACH  - Machine constant.  (Output)
C              AMACH(1) = B**(EMIN-1), the smallest positive magnitude.
C              AMACH(2) = B**EMAX*(1 - B**(-T)), the largest magnitude.
C              AMACH(3) = B**(-T), the smallest relative spacing.
C              AMACH(4) = B**(1-T), the largest relative spacing.
C              AMACH(5) = LOG10(B), the log, base 10, of the radix.
C              AMACH(6) = not-a-number.
C              AMACH(7) = positive machine infinity.
C              AMACH(8) = negative machine infinity.
C
C  GAMS:       R1
C
C  Chapters:   MATH/LIBRARY Reference Material
C              STAT/LIBRARY Reference Material
C              SFUN/LIBRARY Reference Material
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION AMACH (N)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       RMACH(8)
      SAVE       RMACH
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STI
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IRMACH(8)
C
      EQUIVALENCE (RMACH, IRMACH)
C                                  DEFINE CONSTANTS
      DATA RMACH(1)/1.17577E-38/
      DATA RMACH(2)/3.40204E38/
      DATA RMACH(3)/5.96184E-8/
      DATA RMACH(4)/1.19237E-7/
      DATA RMACH(5)/.301029995663981195E0/
      DATA IRMACH(6)/2139091960/
      DATA RMACH(7)/3.40204E38/
      DATA RMACH(8)/-3.40204E38/
C
      IF (N.LT.1 .OR. N.GT.8) THEN
         CALL E1PSH ('AMACH ')
         AMACH = RMACH(6)
         CALL E1STI (1, N)
         CALL E1MES (5, 5, 'The argument must be between 1 '//
     &               'and 8 inclusive. N = %(I1)')
         CALL E1POP ('AMACH ')
      ELSE
         AMACH = RMACH(N)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  BETAI (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the incomplete beta function ratio.
C
C  Usage:      BETAI(X, PIN, QIN)
C
C  Arguments:
C     X      - Upper limit of integration.  (Input)
C              X must be in the interval (0.0,1.0) inclusive.
C     PIN    - First beta distribution parameter.  (Input)
C     QIN    - Second beta distribution parameter.  (Input)
C     BETAI  - Probability that a random variable from a beta
C              distribution having parameters PIN and QIN will be
C              less than or equal to X.  (Output)
C
C  Remarks:
C  1. PIN and QIN must both be positive.
C
C  2. Based on Bosten and Battiste, Remark on Algorithm 179, Comm. ACM,
C     V 17, P 153, (1974).
C
C  GAMS:       C7b
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION BETAI (X, PIN, QIN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X, PIN, QIN
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IB, N
      REAL       C, FINSUM, P, P1, PS, Q, TERM, XB, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       ALNEPS, ALNSML, EPS, SML
      SAVE       ALNEPS, ALNSML, EPS, SML
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  AINT,ALOG,AMAX1,AMIN1,EXP,FLOAT,MAX1
      INTRINSIC  AINT, ALOG, AMAX1, AMIN1, EXP, FLOAT, MAX1
      INTEGER    MAX1
      REAL       AINT, ALOG, AMAX1, AMIN1, EXP, FLOAT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   ALBETA, AMACH, N1RTY
      INTEGER    N1RTY
      REAL       ALBETA, AMACH
C
      DATA EPS/0.0/, ALNEPS/0.0/, SML/0.0/, ALNSML/0.0/
C
      CALL E1PSH ('BETAI ')
      BETAI = AMACH(6)
C
      IF (EPS .EQ. 0.0) THEN
         EPS = AMACH(3)
         ALNEPS = ALOG(EPS)
         SML = AMACH(1)
         ALNSML = ALOG(SML)
      END IF
C
      IF (X.LT.0.0 .OR. X.GT.1.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (5, 5, 'X = %(R1) is not in the range (0.0,1.0).')
      END IF
      IF (PIN.LE.0.0 .OR. QIN.LE.0.0) THEN
         CALL E1STR (1, PIN)
         CALL E1STR (2, QIN)
         CALL E1MES (5, 6, 'Both PIN = %(R1) and QIN = %(R2) '//
     &               'must be greater than 0.0.')
      END IF
      IF (N1RTY(0) .EQ. 5) GO TO 9000
C
      Y = X
      P = PIN
      Q = QIN
      IF (Q.LE.P .AND. X.LT.0.8) GO TO 10
      IF (X .LT. 0.2) GO TO 10
      Y = 1.0 - Y
      P = QIN
      Q = PIN
C
   10 IF ((P+Q)*Y/(P+1.0) .LT. EPS) GO TO 70
C                                  EVALUATE THE INFINITE SUM FIRST.
C                                  TERM WILL EQUAL Y**P/BETA(PS,P) *
C                                  (1.0-PS)I * Y**I / FAC(I)
      PS = Q - AINT(Q)
      IF (PS .EQ. 0.0) PS = 1.0
      XB = P*ALOG(Y) - ALBETA(PS,P) - ALOG(P)
      BETAI = 0.0
      IF (XB .LT. ALNSML) GO TO 30
C
      BETAI = EXP(XB)
      TERM = BETAI*P
      IF (PS .EQ. 1.0) GO TO 30
C
      N = MAX1(ALNEPS/ALOG(Y),4.0)
      DO 20  I=1, N
         TERM = TERM*(FLOAT(I)-PS)*Y/FLOAT(I)
         BETAI = BETAI + TERM/(P+FLOAT(I))
   20 CONTINUE
C                                  NOW EVALUATE THE FINITE SUM, MAYBE.
   30 IF (Q .LE. 1.0) GO TO 60
C
      XB = P*ALOG(Y) + Q*ALOG(1.0-Y) - ALBETA(P,Q) - ALOG(Q)
      IB = MAX1(XB/ALNSML,0.0)
      TERM = EXP(XB-FLOAT(IB)*ALNSML)
      C = 1.0/(1.0-Y)
      P1 = Q*C/(P+Q-1.0)
C
      FINSUM = 0.0
      N = Q
      IF (Q .EQ. FLOAT(N)) N = N - 1
      DO 40  I=1, N
         IF (P1.LE.1.0 .AND. TERM/EPS.LE.FINSUM) GO TO 50
         TERM = (Q-FLOAT(I-1))*C*TERM/(P+Q-FLOAT(I))
C
         IF (TERM .GT. 1.0) THEN
            IB = IB - 1
            TERM = TERM*SML
         END IF
C
         IF (IB .EQ. 0) FINSUM = FINSUM + TERM
   40 CONTINUE
C
   50 BETAI = BETAI + FINSUM
   60 IF (Y.NE.X .OR. P.NE.PIN) BETAI = 1.0 - BETAI
      BETAI = AMAX1(AMIN1(BETAI,1.0),0.0)
      GO TO 9000
C
   70 BETAI = 0.0
      XB = P*ALOG(AMAX1(Y,SML)) - ALOG(P) - ALBETA(P,Q)
      IF (XB.GT.ALNSML .AND. Y.NE.0.0) BETAI = EXP(XB)
      IF (Y.NE.X .OR. P.NE.PIN) BETAI = 1.0 - BETAI
C
 9000 CALL E1POP ('BETAI ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  BETDF/DBETDF (Single/Double precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    February 28, 1985
C
C  Purpose:    Evaluate the beta probability distribution function.
C
C  Usage:      BETDF(X, PIN, QIN)
C
C  Arguments:
C     X      - Argument for which the beta distribution function is to
C              be evaluated.  (Input)
C     PIN    - First beta distribution parameter.  (Input)
C              PIN must be positive.
C     QIN    - Second beta distribution parameter.  (Input)
C              QIN must be positive.
C     BETDF  - Probability that a random variable from a beta
C              distribution having parameters PIN and QIN will be
C              less than or equal to X.  (Output)
C
C  Keywords:   P-value; Probability integral
C
C  GAMS:       L5a1b; C7b
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION BETDF (X, PIN, QIN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X, PIN, QIN
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, BETAI
      REAL       AMACH, BETAI
C
      CALL E1PSH ('BETDF ')
C
      IF (PIN.LE.0.0 .OR. QIN.LE.0.0) THEN
         CALL E1STR (1, PIN)
         CALL E1STR (2, QIN)
         CALL E1MES (5, 6, 'Both PIN = %(R1) and QIN = %(R2) '//
     &               'must be greater than 0.0.')
         BETDF = AMACH(6)
C
      ELSE IF (X .LE. 0.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (1, 7, 'Since X = %(R1) is less than or '//
     &               'equal to zero, the distribution function is '//
     &               'zero at X.')
         BETDF = 0.0
C
      ELSE IF (X .GE. 1.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (1, 8, 'Since X = %(R1) is greater than or '//
     &               'equal to one, the distribution function is one '//
     &               'at X.')
         BETDF = 1.0
C
      ELSE
         BETDF = BETAI(X,PIN,QIN)
      END IF
C
      CALL E1POP ('BETDF ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  BETIN/DBETIN (Single/Double precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the inverse of the beta distribution function.
C
C  Usage:      BETIN(P, PIN, QIN)
C
C  Arguments:
C     P      - Probability for which the inverse of the beta
C              distribution function is to be evaluated.  (Input)
C              P must be in the open interval (0.0, 1.0).
C     PIN    - First beta distribution parameter.  (Input)
C              PIN must be positive.
C     QIN    - Second beta distribution parameter.  (Input)
C              QIN must be positive.
C     BETIN  - Function value.  (Output)
C              The probability that a beta random variable takes a value
C              less than or equal to BETIN is P.
C
C  Remark:
C     Informational error
C     Type Code
C       3   1  The value for the inverse Beta distribution could not be
C              found in 100 iterations. The best approximation is used.
C
C  Keyword:    Percentage point
C
C  GAMS:       L5a2b; C7b
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION BETIN (P, PIN, QIN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       P, PIN, QIN
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IC, NC
      REAL       A, AFN, ALNSML, B, C, DTEMP, EPS, FCS, FN, FXL, FXR,
     &           P1, Q0, QX, SIG, TEMP, X, XC, XL, XR, XRMXL, XT, ZI,
     &           ZZ
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,AINT,ALOG,AMAX1,AMIN1,SQRT
      INTRINSIC  ABS, AINT, ALOG, AMAX1, AMIN1, SQRT
      REAL       ABS, AINT, ALOG, AMAX1, AMIN1, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, ALNGAM, BETDF
      REAL       AMACH, ALNGAM, BETDF
C                                  NOTE:  Upper bounds and lower bounds
C                                  of P, PIN, QIN in relation to one
C                                  another may have to be investigated
C                                  when testing is done.  (To avoid
C                                  computational overflow)
C
      CALL E1PSH ('BETIN ')
      BETIN = AMACH(6)
C                                  Check PIN.
      IF (PIN .LE. 0.0E0) THEN
         CALL E1STR (1, PIN)
         CALL E1MES (5, 1, 'The first parameter of the beta '//
     &               'distribution, PIN = %(R1), must be positive.')
         GO TO 9000
      END IF
C                                  Check QIN.
      IF (QIN .LE. 0.0E0) THEN
         CALL E1STR (1, QIN)
         CALL E1MES (5, 2, 'The second parameter of the beta '//
     &               'distribution, QIN = %(R1), must be positive.')
         GO TO 9000
      END IF
C                                  Check P.
      IF (P.LE.0.0E0 .OR. P.GE.1.0E0) THEN
         CALL E1STR (1, P)
         CALL E1MES (5, 3, 'The probability which the inverse of '//
     &               'the beta distribution is based on, P = %(R1), '//
     &               'must be in the exclusive interval (0.0, 1.0).')
         GO TO 9000
      END IF
C
      EPS = 0.0001E0
      SIG = 1.0E-5
      ALNSML = ALOG(AMACH(1)) + 10.0
      XL = AMIN1(PIN,QIN)
      IF (XL .GT. 1.0E0) THEN
         XR = AMAX1(PIN,QIN)
         IF (10.0E0*XL .GT. XR) THEN
            IC = 0
            XL = 0.0E0
            XR = 1.0E0
            FXL = -P
            FXR = 1.0E0 - P
C                                  Bisection method.
   10       X = (XL+XR)*0.5E0
            P1 = BETDF(X,PIN,QIN)
            FCS = P1 - P
            IF (FCS*FXL .LE. 0.0E0) THEN
               XR = X
               FXR = FCS
            ELSE
               XL = X
               FXL = FCS
            END IF
            XRMXL = XR - XL
            IF (XRMXL.LE.SIG .AND. ABS(FCS).LE.EPS) GO TO 40
            IC = IC + 1
            IF (IC .LE. 30) GO TO 10
         END IF
      END IF
C                                  Use Newtons method for skewed cases.
      IF (P .LE. 0.5E0) THEN
         A = PIN
         B = QIN
         Q0 = ALOG(P)
      ELSE
         Q0 = ALOG(1.0E0-P)
         A = QIN
         B = PIN
      END IF
      XT = A/(A+B)
      DTEMP = ALNGAM(A+B) - ALNGAM(A) - ALNGAM(B)
      DTEMP = DTEMP - (A+B)*ALOG(A+B) + (A-0.5E0)*ALOG(A) +
     &        (B-0.5E0)*ALOG(B)
      DTEMP = DTEMP + 0.5E0*ALOG(B/A) + A*ALOG(1.0E0+B/A) +
     &        B*ALOG(1.0+A/B)
      DO 30  NC=1, 100
         TEMP = ALOG(15.0E0+A+B)
         FN = 0.7E0*TEMP*TEMP + AMAX1(XT*(A+B)-A,0.0E0)
         TEMP = A + FN + FN
         AFN = AINT(FN) + 1.0E0
         C = 1.0E0 - (A+B)*XT/TEMP
         ZI = 2.0E0/(C+SQRT(C*C-4.0E0*FN*(FN-B)*XT/(TEMP*TEMP)))
   20    AFN = AFN - 1.0E0
         IF (AFN .GE. 0.5E0) THEN
            TEMP = A + AFN + AFN
            ZI = (TEMP-2.0E0)*(TEMP-1.0E0-AFN*(AFN-B)*XT*ZI/TEMP)
            TEMP = A + AFN - 1.0E0
            ZI = 1.0E0/(1.0E0-TEMP*(TEMP+B)*XT/ZI)
            GO TO 20
         END IF
         ZZ = ZI
         TEMP = ALOG(XT)
         IF (TEMP .LE. ALNSML) THEN
            IF (P .LE. 0.5E0) THEN
               X = 0.0E0
            ELSE
               X = 1.0E0
            END IF
            GO TO 40
         END IF
         QX = DTEMP + A*TEMP + B*ALOG(1.0E0-XT) + ALOG(ZZ)
         XC = (Q0-QX)*(1.0E0-XT)*ZZ/A
         XC = AMAX1(XC,-0.99E0)
         TEMP = 0.5E0/XT - 0.5E0
         XC = AMIN1(XC,TEMP)
         XT = XT*(1.0E0+XC)
         IF (ABS(XC) .LT. SIG) THEN
            IF (P .LE. 0.5E0) THEN
               X = XT
            ELSE
               X = 1.0E0 - XT
            END IF
            GO TO 40
         END IF
   30 CONTINUE
C
      IF (P .LE. 0.5E0) THEN
         X = XT
      ELSE
         X = 1.0E0 - XT
      END IF
      CALL E1STR (1, P)
      CALL E1STR (2, X)
      CALL E1MES (3, 1, 'BETIN for the value P = %(R1) could '//
     &            'not be found in 100 iterations of Newton''s '//
     &            'method.  The best approximation calculated is '//
     &            'BETIN = %(R2).')
C
   40 BETIN = X
 9000 CALL E1POP ('BETIN ')
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  C1TCI
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 13, 1984
C
C  Purpose:    Convert character string into corresponding integer
C              form.
C
C  Usage:      CALL C1TCI (CHRSTR, SLEN, NUM, IER)
C
C  Arguments:
C   CHRSTR  - Character array that contains the number description.
C             (Input)
C   SLEN    - Length of the character array.  (Input)
C   NUM     - The answer.  (Output)
C   IER     - Completion code.  (Output)  Where
C                IER =-2  indicates that the number is too large to
C                         be converted;
C                IER =-1  indicates that SLEN <= 0;
C                IER = 0  indicates normal completion;
C                IER > 0  indicates that the input string contains a
C                         nonnumeric character.  IER is the index of
C                         the first nonnumeric character in CHRSTR.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE C1TCI (CHRSTR, SLEN, NUM, IER)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    SLEN, NUM, IER
      CHARACTER  CHRSTR(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    COUNT, I, IMACH5, J, N, S, SIGN
      CHARACTER  ZERO
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      CHARACTER  BLANK, DIGIT*10, MINUS, PLUS
      SAVE       BLANK, DIGIT, MINUS, PLUS
C                                  SPECIFICATIONS FOR EQUIVALENCE
      EQUIVALENCE (DIGIT, ZERO)
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  INDEX
      INTRINSIC  INDEX
      INTEGER    INDEX
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   IMACH
      INTEGER    IMACH
C
      DATA DIGIT/'0123456789'/
      DATA BLANK/' '/, MINUS/'-'/, PLUS/'+'/
C
C                                  CHECK SLEN
      NUM = 0
      IF (SLEN .LE. 0) THEN
         IER = -1
         GO TO 50
      END IF
C                                  HANDLE LEADING BLANKS
      SIGN = 1
      I = 1
   10 IF (I .LE. SLEN) THEN
         IF (CHRSTR(I) .EQ. BLANK) THEN
            I = I + 1
            GO TO 10
         END IF
      ELSE
         IER = 1
         GO TO 50
      END IF
C                                  CHECK FOR SIGN, IF ANY
      S = I
      IF (CHRSTR(I) .EQ. MINUS) THEN
         SIGN = -1
         I = I + 1
      ELSE IF (CHRSTR(I) .EQ. PLUS) THEN
         I = I + 1
      END IF
   20 IF (I .LE. SLEN) THEN
         IF (CHRSTR(I) .EQ. BLANK) THEN
            I = I + 1
            GO TO 20
         END IF
      ELSE
         IER = S
         GO TO 50
      END IF
C                                  SKIP LEADING ZERO
      J = I
   30 IF (I .LE. SLEN) THEN
         IF (CHRSTR(I) .EQ. ZERO) THEN
            I = I + 1
            GO TO 30
         END IF
      ELSE
         IER = 0
         GO TO 50
      END IF
C                                  CHECK FIRST NONBLANK CHARACTER
      COUNT = 0
C                                  CHECK NUMERIC CHARACTERS
      IMACH5 = IMACH(5)
   40 N = INDEX(DIGIT,CHRSTR(I))
      IF (N .NE. 0) THEN
         COUNT = COUNT + 1
         IF (NUM .GT. ((IMACH5-N)+1)/10) THEN
            IER = -2
            GO TO 50
         ELSE
            NUM = NUM*10 - 1 + N
            I = I + 1
            IF (I .LE. SLEN) GO TO 40
         END IF
      END IF
C
      IF (COUNT .EQ. 0) THEN
         IF (I .GT. J) THEN
            IER = I
         ELSE
            IER = S
         END IF
      ELSE IF (I .GT. SLEN) THEN
         NUM = SIGN*NUM
         IER = 0
      ELSE
         NUM = SIGN*NUM
         IER = I
      END IF
C
   50 CONTINUE
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  C1TIC
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 9, 1984
C
C  Purpose:    Convert an integer to its corresponding character form.
C              (Right justified)
C
C  Usage:      CALL C1TIC(NUM, CHRSTR, SLEN, IER)
C
C  Arguments:
C     NUM    - Integer number.  (Input)
C     CHRSTR - Character array that receives the result.  (Output)
C     SLEN   - Length of the character array.  (Input)
C     IER    - Completion code.  (Output) Where
C                 IER < 0  indicates that SLEN <= 0,
C                 IER = 0  indicates normal completion,
C                 IER > 0  indicates that the character array is too
C                       small to hold the complete number.  IER
C                       indicates how many significant digits are
C                       being truncated.
C
C  Remarks:
C  1. The character array is filled in a right justified manner.
C  2. Leading zeros are replaced by blanks.
C  3. Sign is inserted only for negative number.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE C1TIC (NUM, CHRSTR, SLEN, IER)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    NUM, SLEN, IER
      CHARACTER  CHRSTR(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, J, K, L
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      CHARACTER  BLANK(1), DIGIT(10), MINUS(1)
      SAVE       BLANK, DIGIT, MINUS
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  IABS
      INTRINSIC  IABS
      INTEGER    IABS
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   M1VE
C
      DATA DIGIT/'0', '1', '2', '3', '4', '5', '6', '7', '8',
     &     '9'/
      DATA BLANK/' '/, MINUS/'-'/
C                                  CHECK SLEN
      IF (SLEN .LE. 0) THEN
         IER = -1
         RETURN
      END IF
C                                  THE NUMBER IS ZERO
      IF (NUM .EQ. 0) THEN
         CALL M1VE (BLANK, 1, 1, 1, CHRSTR, 1, SLEN-1, SLEN, I)
         CHRSTR(SLEN) = DIGIT(1)
         IER = 0
         RETURN
      END IF
C                                  CONVERT NUMBER DIGIT BY DIGIT TO
C                                  CHARACTER FORM
      J = SLEN
      K = IABS(NUM)
   10 IF (K.GT.0 .AND. J.GE.1) THEN
         L = K
         K = K/10
         L = L - K*10
         CHRSTR(J) = DIGIT(L+1)
         J = J - 1
         GO TO 10
      END IF
C
   20 IF (K .EQ. 0) THEN
         IF (NUM .LT. 0) THEN
            CALL M1VE (MINUS, 1, 1, 1, CHRSTR, J, J, SLEN, I)
            IF (I .NE. 0) THEN
               IER = 1
               RETURN
            END IF
            J = J - 1
         END IF
         IER = 0
         CALL M1VE (BLANK, 1, 1, 1, CHRSTR, 1, J, SLEN, I)
         RETURN
      END IF
C                                  DETERMINE THE NUMBER OF SIGNIFICANT
C                                  DIGITS BEING TRUNCATED
      I = 0
   30 IF (K .GT. 0) THEN
         K = K/10
         I = I + 1
         GO TO 30
      END IF
C
      IF (NUM .LT. 0) I = I + 1
      IER = I
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  CSET (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 9, 1986
C
C  Purpose:    Set the components of a vector to a scalar, all complex.
C
C  Usage:      CALL CSET (N, CA, CX, INCX)
C
C  Arguments:
C     N      - Length of vector X.  (Input)
C     CA     - Complex scalar.  (Input)
C     CX     - Complex vector of length N*INCX.  (Input/Output)
C              CSET replaces X(I) with CA for I=1,...,N. X(I) refers to
C              a specific element of CX. See INCX argument description.
C     INCX   - Displacement between elements of CX.  (Input)
C              X(I) is defined to be CX(1+(I-1)*INCX). INCX must be
C              greater than zero.
C
C  GAMS:       D1a1
C
C  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
C              STAT/LIBRARY Mathematical Support
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE CSET (N, CA, CX, INCX)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX
      COMPLEX    CA, CX(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, NINCX
C
      IF (N .GT. 0) THEN
         IF (INCX .NE. 1) THEN
C                                  CODE FOR INCREMENT NOT EQUAL TO 1
            NINCX = N*INCX
            DO 10  I=1, NINCX, INCX
               CX(I) = CA
   10       CONTINUE
         ELSE
C                                  CODE FOR INCREMENT EQUAL TO 1
C                                    CLEAN-UP LOOP
            DO 20  I=1, N
               CX(I) = CA
   20       CONTINUE
         END IF
      END IF
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  CSEVL (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the N-term Chebyshev series.
C
C  Usage:      CSEVL(X, CS, N)
C
C  Arguments:
C     X      - Argument at which the series is to be evaluated.  (Input)
C     CS     - Vector of length N containing the terms of a Chebyshev
C              series.  (Input)
C              In evaluating CS, only half of the first coefficient is
C              summed.
C     N      - Number of terms in the vector CS.  (Input)
C     CSEVL  - Function value.  (Output)
C
C  Remark:
C     Informational error:
C     Type Code
C       3   7  X is outside the interval (-1.1,+1.1)
C
C  GAMS:       C19
C
C  Chapter:    SFUN/LIBRARY Fundamental Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION CSEVL (X, CS, N)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N
      REAL       X, CS(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, NI
      REAL       B0, B1, B2, TWOX
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STI, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH
      REAL       AMACH
C
      CALL E1PSH ('CSEVL ')
      CSEVL = AMACH(6)
C
      IF (N .LT. 1) THEN
         CALL E1STI (1, N)
         CALL E1MES (5, 5, 'The number of terms in the series is '//
     &               'not positive. N = %(I1).')
C
      ELSE IF (N .GT. 1000) THEN
         CALL E1STI (1, N)
         CALL E1MES (5, 6, 'The number of terms in the series is '//
     &               'greater than 1000. N = %(I1).')
C
      ELSE
         IF (X.LT.-1.1 .OR. X.GT.1.1) THEN
            CALL E1STR (1, X)
            CALL E1MES (3, 7, 'The argument X = %(R1) is outside '//
     &                  'the interval (-1.1,+1.1).')
         END IF
C
         B1 = 0.0
         B0 = 0.0
         TWOX = 2.0*X
         DO 10  I=1, N
            B2 = B1
            B1 = B0
            NI = N + 1 - I
            B0 = TWOX*B1 - B2 + CS(NI)
   10    CONTINUE
C
         CSEVL = 0.5*(B0-B2)
      END IF
C
      CALL E1POP ('CSEVL ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  D9GAML (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Compute the underflow and overflow limits for the gamma
C              function and several related functions.
C
C  Usage:      CALL D9GAML (XMIN, XMAX)
C
C  Arguments:
C     XMIN   - Underflow limit.  (Output)
C     XMAX   - Overflow limit.  (Output)
C
C  Remark:
C     XMIN and XMAX are not the only bounds for the function, but they
C     are the only nontrivial ones to calculate.
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE D9GAML (XMIN, XMAX)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION XMIN, XMAX
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I
      DOUBLE PRECISION ALNBIG, ALNSML, XLN, XOLD
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DLOG,DMAX1
cx    INTRINSIC  DABS, DLOG, DMAX1
      DOUBLE PRECISION DABS, DLOG, DMAX1
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH
      DOUBLE PRECISION DMACH
C
      CALL E1PSH ('D9GAML')
      XMIN = DMACH(6)
      XMAX = DMACH(6)
C
      ALNSML = DLOG(DMACH(1))
      XMIN = -ALNSML
      DO 10  I=1, 10
         XOLD = XMIN
         XLN = DLOG(XMIN)
         XMIN = XMIN - XMIN*((XMIN+0.5D0)*XLN-XMIN-.2258D0+ALNSML)/
     &          (XMIN*XLN+0.5D0)
         IF (DABS(XMIN-XOLD) .LT. 0.005D0) GO TO 20
   10 CONTINUE
      CALL E1MES (5, 5, 'Unable to determine the value of XMIN.')
      XMIN = DMACH(6)
      GO TO 9000
C
   20 XMIN = -XMIN + 0.01D0
C
      ALNBIG = DLOG(DMACH(2))
      XMAX = ALNBIG
      DO 30  I=1, 10
         XOLD = XMAX
         XLN = DLOG(XMAX)
         XMAX = XMAX - XMAX*((XMAX-0.5D0)*XLN-XMAX+.9189D0-ALNBIG)/
     &          (XMAX*XLN-0.5D0)
         IF (DABS(XMAX-XOLD) .LT. 0.005D0) GO TO 40
   30 CONTINUE
      CALL E1MES (5, 6, 'Unable to determine the value of XMAX.')
      XMAX = DMACH(6)
      GO TO 9000
C
   40 XMAX = XMAX - 0.01D0
      XMIN = DMAX1(XMIN,-XMAX+1.0D0)
C
 9000 CALL E1POP ('D9GAML')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  D9LGMC (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the log gamma correction term for argument
C              values greater than or equal to 10.0.
C
C  Usage:      D9LGMC(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     D9LGMC - Function value.  (Output)
C
C  Remarks:
C  1. Informational error:
C     Type Code
C       2   1  The function underflows because X is too large.
C
C  2. D9LGMC calculates the log gamma correction factor such that
C     ALOG (GAMMA(X)) = ALOG(SQRT(2*PI))+(X-.5)*ALOG(X)-X+D9LGMC(X).
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION D9LGMC (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NALGM
      DOUBLE PRECISION ALGMCS(15), XBIG, XMAX
      SAVE       ALGMCS, NALGM, XBIG, XMAX
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DEXP,DLOG,DMIN1,DSQRT,SNGL
cx    INTRINSIC  DEXP, DLOG, DMIN1, DSQRT, SNGL
      REAL       SNGL
      DOUBLE PRECISION DEXP, DLOG, DMIN1, DSQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DCSEVL, DMACH, INITDS
      INTEGER    INITDS
      DOUBLE PRECISION DCSEVL, DMACH
C
C                                  SERIES FOR ALGM ON THE INTERVAL
C                                  0.0 TO  1.00000D-02
C                                  WITH WEIGHTED ERROR        1.28D-31
C                                  LOG WEIGHTED ERROR        30.89
C                                  SIGNIFICANT FIGURES REQD. 29.81
C                                  DECIMAL PLACES REQUIRED   31.48
C
      DATA ALGMCS(1)/.166638948045186324720572965082D+0/
      DATA ALGMCS(2)/-.138494817606756384073298605914D-4/
      DATA ALGMCS(3)/.981082564692472942615717154749D-8/
      DATA ALGMCS(4)/-.180912947557249419426330626672D-10/
      DATA ALGMCS(5)/.622109804189260522712601554342D-13/
      DATA ALGMCS(6)/-.339961500541772194430333059967D-15/
      DATA ALGMCS(7)/.268318199848269874895753884667D-17/
      DATA ALGMCS(8)/-.28680424353346432841446224D-19/
      DATA ALGMCS(9)/.396283706104643480367930666667D-21/
      DATA ALGMCS(10)/-.6831888753985766870112D-23/
      DATA ALGMCS(11)/.142922735594249814757333333333D-24/
      DATA ALGMCS(12)/-.35475981581010705472D-26/
      DATA ALGMCS(13)/.1025680058010470912D-27/
      DATA ALGMCS(14)/-.34011022543167488D-29/
      DATA ALGMCS(15)/.127664219563006293333333333333D-30/
C
      DATA NALGM/0/, XBIG/0.0D0/, XMAX/0.0D0/
C
      CALL E1PSH ('D9LGMC')
      D9LGMC = DMACH(6)
C
      IF (NALGM .EQ. 0) THEN
         NALGM = INITDS(ALGMCS,15,SNGL(DMACH(3)))
         XBIG = 1.0D0/DSQRT(DMACH(3))
         XMAX = DEXP(DMIN1(DLOG(DMACH(2)/12.0D0),-DLOG(12.0D0*DMACH(1))
     &          ))
      END IF
C
      IF (X .LT. 10.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (5, 5, 'The argument X = %(D1) must be '//
     &               'greater than or equal to 10.0.')
C
      ELSE IF (X .LT. XMAX) THEN
         IF (X .GE. XBIG) THEN
            D9LGMC = 1.0D0/(12.0D0*X)
         ELSE
            D9LGMC = DCSEVL(2.0D0*(10.0D0/X)**2-1.0D0,ALGMCS,NALGM)/X
         END IF
C
      ELSE
         D9LGMC = 0.0D0
         CALL E1STD (1, X)
         CALL E1STD (2, XMAX)
         CALL E1MES (2, 1, 'The function underflows because '//
     &               'X = %(D1) is greater than %(D2). The result is '//
     &               'set to zero.')
      END IF
C
      CALL E1POP ('D9LGMC')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DBETAI (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the incomplete beta function ratio.
C
C  Usage:      DBETAI(X, PIN, QIN)
C
C  Arguments:
C     X      - Upper limit of integration.  (Input)
C              X must be in the interval (0.0,1.0) inclusive.
C     PIN    - First beta distribution parameter.  (Input)
C     QIN    - Second beta distribution parameter.  (Input)
C     DBETAI - Probability that a random variable from a beta
C              distribution having parameters PIN and QIN will be
C              less than or equal to X.  (Output)
C
C  Remarks:
C  1. PIN and QIN must both be positive.
C
C  2. Based on Bosten and Battiste, Remark on Algorithm 179, Comm. ACM,
C     V 17, P 153, (1974).
C
C  GAMS:       C7b
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DBETAI (X, PIN, QIN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X, PIN, QIN
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IB, N
      DOUBLE PRECISION C, FINSUM, P, P1, PS, Q, TERM, XB, XI, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      DOUBLE PRECISION ALNEPS, ALNSML, EPS, SML
      SAVE       ALNEPS, ALNSML, EPS, SML
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DBLE,DEXP,DINT,DLOG,DMAX1,DMIN1,FLOAT,MAX1,SNGL
cx    INTRINSIC  DBLE, DEXP, DINT, DLOG, DMAX1, DMIN1, FLOAT, MAX1,
cx   &           SNGL
      INTEGER    MAX1
      REAL       FLOAT, SNGL
      DOUBLE PRECISION DBLE, DEXP, DINT, DLOG, DMAX1, DMIN1
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DLBETA, DMACH, N1RTY
      INTEGER    N1RTY
      DOUBLE PRECISION DLBETA, DMACH
C
      DATA EPS/0.0D0/, ALNEPS/0.0D0/, SML/0.0D0/, ALNSML/0.0D0/
C
      CALL E1PSH ('DBETAI')
      DBETAI = DMACH(6)
C
      IF (EPS .EQ. 0.0D0) THEN
         EPS = DMACH(3)
         ALNEPS = DLOG(EPS)
         SML = DMACH(1)
         ALNSML = DLOG(SML)
      END IF
C
      IF (X.LT.0.0D0 .OR. X.GT.1.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (5, 5, 'X = %(D1) is not in the range (0.0,1.0).')
      END IF
      IF (PIN.LE.0.0D0 .OR. QIN.LE.0.0D0) THEN
         CALL E1STD (1, PIN)
         CALL E1STD (2, QIN)
         CALL E1MES (5, 6, 'Both PIN = %(D1) and QIN = %(D2) '//
     &               'must be greater than 0.0.')
      END IF
      IF (N1RTY(0) .EQ. 5) GO TO 9000
C
      Y = X
      P = PIN
      Q = QIN
      IF (Q.LE.P .AND. X.LT.0.8D0) GO TO 10
      IF (X .LT. 0.2D0) GO TO 10
      Y = 1.0D0 - Y
      P = QIN
      Q = PIN
C
   10 IF ((P+Q)*Y/(P+1.0D0) .LT. EPS) GO TO 70
C                                  EVALUATE THE INFINITE SUM FIRST.
C                                  TERM WILL EQUAL Y**P/BETA(PS,P) *
C                                  (1.0-PS)-SUB-I * Y**I / FAC(I)
      PS = Q - DINT(Q)
      IF (PS .EQ. 0.0D0) PS = 1.0D0
      XB = P*DLOG(Y) - DLBETA(PS,P) - DLOG(P)
      DBETAI = 0.0D0
      IF (XB .LT. ALNSML) GO TO 30
C
      DBETAI = DEXP(XB)
      TERM = DBETAI*P
      IF (PS .EQ. 1.0D0) GO TO 30
      N = MAX1(SNGL(ALNEPS/DLOG(Y)),4.0)
      DO 20  I=1, N
         XI = I
         TERM = TERM*(XI-PS)*Y/XI
         DBETAI = DBETAI + TERM/(P+XI)
   20 CONTINUE
C                                  NOW EVALUATE THE FINITE SUM, MAYBE.
   30 IF (Q .LE. 1.0D0) GO TO 60
C
      XB = P*DLOG(Y) + Q*DLOG(1.0D0-Y) - DLBETA(P,Q) - DLOG(Q)
      IB = MAX1(SNGL(XB/ALNSML),0.0)
      TERM = DEXP(XB-DBLE(FLOAT(IB))*ALNSML)
      C = 1.0D0/(1.0D0-Y)
      P1 = Q*C/(P+Q-1.0D0)
C
      FINSUM = 0.0D0
      N = Q
      IF (Q .EQ. DBLE(FLOAT(N))) N = N - 1
      DO 40  I=1, N
         IF (P1.LE.1.0D0 .AND. TERM/EPS.LE.FINSUM) GO TO 50
         XI = I
         TERM = (Q-XI+1.0D0)*C*TERM/(P+Q-XI)
C
         IF (TERM .GT. 1.0D0) THEN
            IB = IB - 1
            TERM = TERM*SML
         END IF
C
         IF (IB .EQ. 0) FINSUM = FINSUM + TERM
   40 CONTINUE
C
   50 DBETAI = DBETAI + FINSUM
   60 IF (Y.NE.X .OR. P.NE.PIN) DBETAI = 1.0D0 - DBETAI
      DBETAI = DMAX1(DMIN1(DBETAI,1.0D0),0.0D0)
      GO TO 9000
C
   70 DBETAI = 0.0D0
      XB = P*DLOG(DMAX1(Y,SML)) - DLOG(P) - DLBETA(P,Q)
      IF (XB.GT.ALNSML .AND. Y.NE.0.0D0) DBETAI = DEXP(XB)
      IF (Y.NE.X .OR. P.NE.PIN) DBETAI = 1.0D0 - DBETAI
C
 9000 CALL E1POP ('DBETAI')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  BETDF/DBETDF (Single/Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    February 28, 1985
C
C  Purpose:    Evaluate the beta probability distribution function.
C
C  Usage:      BETDF(X, PIN, QIN)
C
C  Arguments:
C     X      - Argument for which the beta distribution function is to
C              be evaluated.  (Input)
C     PIN    - First beta distribution parameter.  (Input)
C              PIN must be positive.
C     QIN    - Second beta distribution parameter.  (Input)
C              QIN must be positive.
C     BETDF  - Probability that a random variable from a beta
C              distribution having parameters PIN and QIN will be
C              less than or equal to X.  (Output)
C
C  Keywords:   P-value; Probability integral
C
C  GAMS:       L5a1b; C7b
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DBETDF (X, PIN, QIN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X, PIN, QIN
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH, DBETAI
      DOUBLE PRECISION DMACH, DBETAI
C
      CALL E1PSH ('DBETDF ')
C
      IF (PIN.LE.0.0D0 .OR. QIN.LE.0.0D0) THEN
         CALL E1STD (1, PIN)
         CALL E1STD (2, QIN)
         CALL E1MES (5, 6, 'Both PIN = %(D1) and QIN = %(D2) '//
     &               'must be greater than 0.0.')
         DBETDF = DMACH(6)
C
      ELSE IF (X .LE. 0.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (1, 7, 'Since X = %(D1) is less than or '//
     &               'equal to zero, the distribution function is '//
     &               'zero at X.')
         DBETDF = 0.0D0
C
      ELSE IF (X .GE. 1.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (1, 8, 'Since X = %(D1) is greater than or '//
     &               'equal to one, the distribution function is one '//
     &               'at X.')
         DBETDF = 1.0D0
C
      ELSE
         DBETDF = DBETAI(X,PIN,QIN)
      END IF
C
      CALL E1POP ('DBETDF ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  BETIN/DBETIN (Single/Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the inverse of the beta distribution function.
C
C  Usage:      BETIN(P, PIN, QIN)
C
C  Arguments:
C     P      - Probability for which the inverse of the beta
C              distribution function is to be evaluated.  (Input)
C              P must be in the open interval (0.0, 1.0).
C     PIN    - First beta distribution parameter.  (Input)
C              PIN must be positive.
C     QIN    - Second beta distribution parameter.  (Input)
C              QIN must be positive.
C     BETIN  - Function value.  (Output)
C              The probability that a beta random variable takes a value
C              less than or equal to BETIN is P.
C
C  Remark:
C     Informational error
C     Type Code
C       3   1  The value for the inverse Beta distribution could not be
C              found in 100 iterations. The best approximation is used.
C
C  Keyword:    Percentage point
C
C  GAMS:       L5a2b; C7b
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DBETIN (P, PIN, QIN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION P, PIN, QIN
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IC, NC
      DOUBLE PRECISION A, AFN, ALNSML, B, C, DTEMP, EPS, FCS, FN, FXL,
     &           FXR, P1, Q0, QX, SIG, TEMP, X, XC, XL, XR, XRMXL, XT,
     &           ZI, ZZ
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DINT,DLOG,DMAX1,DMIN1,DSQRT
cx    INTRINSIC  DABS, DINT, DLOG, DMAX1, DMIN1, DSQRT
      DOUBLE PRECISION DABS, DINT, DLOG, DMAX1, DMIN1, DSQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH, DLNGAM, DBETDF
      DOUBLE PRECISION DMACH, DLNGAM, DBETDF
C                                  NOTE:  Upper bounds and lower bounds
C                                  of P, PIN, QIN in relation to one
C                                  another may have to be investigated
C                                  when testing is done.  (To avoid
C                                  computational overflow)
C
      CALL E1PSH ('DBETIN ')
      DBETIN = DMACH(6)
C                                  Check PIN.
      IF (PIN .LE. 0.0D0) THEN
         CALL E1STD (1, PIN)
         CALL E1MES (5, 1, 'The first parameter of the beta '//
     &               'distribution, PIN = %(D1), must be positive.')
         GO TO 9000
      END IF
C                                  Check QIN.
      IF (QIN .LE. 0.0D0) THEN
         CALL E1STD (1, QIN)
         CALL E1MES (5, 2, 'The second parameter of the beta '//
     &               'distribution, QIN = %(D1), must be positive.')
         GO TO 9000
      END IF
C                                  Check P.
      IF (P.LE.0.0D0 .OR. P.GE.1.0D0) THEN
         CALL E1STD (1, P)
         CALL E1MES (5, 3, 'The probability which the inverse of '//
     &               'the beta distribution is based on, P = %(D1), '//
     &               'must be in the exclusive interval (0.0, 1.0).')
         GO TO 9000
      END IF
C
      EPS = 0.0001D0
      SIG = 1.0D-5
      ALNSML = DLOG(DMACH(1)) + 10.0D0
      XL = DMIN1(PIN,QIN)
      IF (XL .GT. 1.0D0) THEN
         XR = DMAX1(PIN,QIN)
         IF (10.0D0*XL .GT. XR) THEN
            IC = 0
            XL = 0.0D0
            XR = 1.0D0
            FXL = -P
            FXR = 1.0D0 - P
C                                  Bisection method.
   10       X = (XL+XR)*0.5D0
            P1 = DBETDF(X,PIN,QIN)
            FCS = P1 - P
            IF (FCS*FXL .LE. 0.0D0) THEN
               XR = X
               FXR = FCS
            ELSE
               XL = X
               FXL = FCS
            END IF
            XRMXL = XR - XL
            IF (XRMXL.LE.SIG .AND. DABS(FCS).LE.EPS) GO TO 40
            IC = IC + 1
            IF (IC .LE. 30) GO TO 10
         END IF
      END IF
C                                  Use Newtons method for skewed cases.
      IF (P .LE. 0.5D0) THEN
         A = PIN
         B = QIN
         Q0 = DLOG(P)
      ELSE
         Q0 = DLOG(1.0D0-P)
         A = QIN
         B = PIN
      END IF
      XT = A/(A+B)
      DTEMP = DLNGAM(A+B) - DLNGAM(A) - DLNGAM(B)
      DTEMP = DTEMP - (A+B)*DLOG(A+B) + (A-0.5D0)*DLOG(A) +
     &        (B-0.5D0)*DLOG(B)
      DTEMP = DTEMP + 0.5D0*DLOG(B/A) + A*DLOG(1.0D0+B/A) +
     &        B*DLOG(1.0D0+A/B)
      DO 30  NC=1, 100
         TEMP = DLOG(15.0D0+A+B)
         FN = 0.7D0*TEMP*TEMP + DMAX1(XT*(A+B)-A,0.0D0)
         TEMP = A + FN + FN
         AFN = DINT(FN) + 1.0D0
         C = 1.0D0 - (A+B)*XT/TEMP
         ZI = 2.0D0/(C+DSQRT(C*C-4.0D0*FN*(FN-B)*XT/(TEMP*TEMP)))
   20    AFN = AFN - 1.0D0
         IF (AFN .GE. 0.5D0) THEN
            TEMP = A + AFN + AFN
            ZI = (TEMP-2.0D0)*(TEMP-1.0D0-AFN*(AFN-B)*XT*ZI/TEMP)
            TEMP = A + AFN - 1.0D0
            ZI = 1.0D0/(1.0D0-TEMP*(TEMP+B)*XT/ZI)
            GO TO 20
         END IF
         ZZ = ZI
         TEMP = DLOG(XT)
         IF (TEMP .LE. ALNSML) THEN
            IF (P .LE. 0.5D0) THEN
               X = 0.0D0
            ELSE
               X = 1.0D0
            END IF
            GO TO 40
         END IF
         QX = DTEMP + A*TEMP + B*DLOG(1.0D0-XT) + DLOG(ZZ)
         XC = (Q0-QX)*(1.0D0-XT)*ZZ/A
         XC = DMAX1(XC,-0.99D0)
         TEMP = 0.5D0/XT - 0.5D0
         XC = DMIN1(XC,TEMP)
         XT = XT*(1.0D0+XC)
         IF (DABS(XC) .LT. SIG) THEN
            IF (P .LE. 0.5D0) THEN
               X = XT
            ELSE
               X = 1.0D0 - XT
            END IF
            GO TO 40
         END IF
   30 CONTINUE
C
      IF (P .LE. 0.5D0) THEN
         X = XT
      ELSE
         X = 1.0D0 - XT
      END IF
      CALL E1STD (1, P)
      CALL E1STD (2, X)
      CALL E1MES (3, 1, 'DBETIN for the value P = %(D1) could '//
     &            'not be found in 100 iterations of Newton''s '//
     &            'method.  The best approximation calculated is '//
     &            'DBETIN = %(D2).')
C
   40 DBETIN = X
 9000 CALL E1POP ('DBETIN ')
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DCSEVL (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the N-term Chebyshev series.
C
C  Usage:      DCSEVL(X, CS, N)
C
C  Arguments:
C     X      - Argument at which the series is to be evaluated.  (Input)
C     CS     - Vector of length N containing the terms of a Chebyshev
C              series.  (Input)
C              In evaluating CS, only half of the first coefficient is
C              summed.
C     N      - Number of terms in the vector CS.  (Input)
C     DCSEVL - Function value.  (Output)
C
C  Remark:
C     Informational error:
C     Type Code
C       3   7  X is outside the interval (-1.1,+1.1)
C
C  GAMS:       C19
C
C  Chapter:    SFUN/LIBRARY Fundamental Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DCSEVL (X, CS, N)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N
      DOUBLE PRECISION X, CS(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, NI
      DOUBLE PRECISION B0, B1, B2, TWOX
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD, E1STI
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH
      DOUBLE PRECISION DMACH
C
      CALL E1PSH ('DCSEVL')
      DCSEVL = DMACH(6)
C
      IF (N .LT. 1) THEN
         CALL E1STI (1, N)
         CALL E1MES (5, 5, 'The number of terms in the series is '//
     &               'not positive. N = %(I1).')
C
      ELSE IF (N .GT. 1000) THEN
         CALL E1STI (1, N)
         CALL E1MES (5, 6, 'The number of terms in the series is '//
     &               'greater than 1000. N = %(I1).')
C
      ELSE
         IF (X.LT.-1.1D0 .OR. X.GT.1.1D0) THEN
            CALL E1STD (1, X)
            CALL E1MES (3, 7, 'The argument X = %(D1) is outside '//
     &                  'the interval (-1.1,+1.1).')
         END IF
C
         B1 = 0.0D0
         B0 = 0.0D0
         TWOX = 2.0D0*X
         DO 10  I=1, N
            B2 = B1
            B1 = B0
            NI = N + 1 - I
            B0 = TWOX*B1 - B2 + CS(NI)
   10    CONTINUE
C
         DCSEVL = 0.5D0*(B0-B2)
      END IF
C
      CALL E1POP ('DCSEVL')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DERFC (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the complementary error function.
C
C  Usage:      DERFC(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     DERFC  - Function value.  (Output)
C
C  Remark:
C     Informational error:
C     Type Code
C       2   1  The function underflows because X is too large.
C
C  GAMS:       C8a
C
C  Chapter:    SFUN/LIBRARY Error Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DERFC (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      REAL       ETA
      DOUBLE PRECISION Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NTERC2, NTERF, NTERFC
      DOUBLE PRECISION ERC2CS(49), ERFCCS(59), ERFCS(21), SQEPS,
     &           SQRTPI, XMAX, XSML
      SAVE       ERC2CS, ERFCCS, ERFCS, NTERC2, NTERF, NTERFC, SQEPS,
     &           SQRTPI, XMAX, XSML
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DEXP,DLOG,DSQRT,SNGL
cx    INTRINSIC  DABS, DEXP, DLOG, DSQRT, SNGL
      REAL       SNGL
      DOUBLE PRECISION DABS, DEXP, DLOG, DSQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DCSEVL, DMACH, INITDS
      INTEGER    INITDS
      DOUBLE PRECISION DCSEVL, DMACH
C
C                                  SERIES FOR ERF ON THE INTERVAL
C                                  0.0  TO  1.00000D+00
C                                  WITH WEIGHTED ERROR        1.28D-32
C                                  LOG WEIGHTED ERROR        31.89
C                                  SIGNIFICANT FIGURES REQD. 31.05
C                                  DECIMAL PLACES REQUIRED   32.55
C
      DATA ERFCS(1)/-.490461212346918080399845440334D-1/
      DATA ERFCS(2)/-.142261205103713642378247418996D+0/
      DATA ERFCS(3)/.100355821875997955757546767129D-1/
      DATA ERFCS(4)/-.576876469976748476508270255092D-3/
      DATA ERFCS(5)/.274199312521960610344221607915D-4/
      DATA ERFCS(6)/-.110431755073445076041353812959D-5/
      DATA ERFCS(7)/.384887554203450369499613114982D-7/
      DATA ERFCS(8)/-.118085825338754669696317518016D-8/
      DATA ERFCS(9)/.323342158260509096464029309534D-10/
      DATA ERFCS(10)/-.799101594700454875816073747086D-12/
      DATA ERFCS(11)/.179907251139614556119672454866D-13/
      DATA ERFCS(12)/-.371863548781869263823168282095D-15/
      DATA ERFCS(13)/.710359900371425297116899083947D-17/
      DATA ERFCS(14)/-.126124551191552258324954248533D-18/
      DATA ERFCS(15)/.209164069417692943691705002667D-20/
      DATA ERFCS(16)/-.3253973102931407298236416D-22/
      DATA ERFCS(17)/.476686720979767483323733333333D-24/
      DATA ERFCS(18)/-.659801207828513431552D-26/
      DATA ERFCS(19)/.865501146996376261973333333333D-28/
      DATA ERFCS(20)/-.107889251774980642133333333333D-29/
      DATA ERFCS(21)/.128118839930170026666666666667D-31/
C
C                                  SERIES FOR ERC2 ON THE INTERVAL
C                                  2.50000D-01 TO  1.00000D+00
C                                  WITH WEIGHTED ERROR        2.67D-32
C                                  LOG WEIGHTED ERROR        31.57
C                                  SIGNIFICANT FIGURES REQD. 30.31
C                                  DECIMAL PLACES REQUIRED   32.42
C
      DATA ERC2CS(1)/-.69601346602309501127391508262D-1/
      DATA ERC2CS(2)/-.411013393626208934898221208467D-1/
      DATA ERC2CS(3)/.391449586668962688156114370524D-2/
      DATA ERC2CS(4)/-.490639565054897916128093545077D-3/
      DATA ERC2CS(5)/.715747900137703638076089414183D-4/
      DATA ERC2CS(6)/-.115307163413123283380823284791D-4/
      DATA ERC2CS(7)/.199467059020199763505231486771D-5/
      DATA ERC2CS(8)/-.364266647159922287393611843071D-6/
      DATA ERC2CS(9)/.694437261000501258993127721463D-7/
      DATA ERC2CS(10)/-.137122090210436601953460514121D-7/
      DATA ERC2CS(11)/.278838966100713713196386034809D-8/
      DATA ERC2CS(12)/-.581416472433116155186479105032D-9/
      DATA ERC2CS(13)/.123892049175275318118016881795D-9/
      DATA ERC2CS(14)/-.269063914530674343239042493789D-10/
      DATA ERC2CS(15)/.594261435084791098244470968384D-11/
      DATA ERC2CS(16)/-.133238673575811957928775442057D-11/
      DATA ERC2CS(17)/.30280468061771320171736972433D-12/
      DATA ERC2CS(18)/-.696664881494103258879586758895D-13/
      DATA ERC2CS(19)/.162085454105392296981289322763D-13/
      DATA ERC2CS(20)/-.380993446525049199987691305773D-14/
      DATA ERC2CS(21)/.904048781597883114936897101298D-15/
      DATA ERC2CS(22)/-.2164006195089607347809812047D-15/
      DATA ERC2CS(23)/.522210223399585498460798024417D-16/
      DATA ERC2CS(24)/-.126972960236455533637241552778D-16/
      DATA ERC2CS(25)/.310914550427619758383622741295D-17/
      DATA ERC2CS(26)/-.766376292032038552400956671481D-18/
      DATA ERC2CS(27)/.190081925136274520253692973329D-18/
      DATA ERC2CS(28)/-.474220727906903954522565599997D-19/
      DATA ERC2CS(29)/.118964920007652838288068307845D-19/
      DATA ERC2CS(30)/-.300003559032578025684527131307D-20/
      DATA ERC2CS(31)/.76029934530432461730193852771D-21/
      DATA ERC2CS(32)/-.193590944760687288156981104913D-21/
      DATA ERC2CS(33)/.495139912477333788100004238677D-22/
      DATA ERC2CS(34)/-.127180748133637187960862198989D-22/
      DATA ERC2CS(35)/.328004960046951304331584165205D-23/
      DATA ERC2CS(36)/-.84923201768228965689247924224D-24/
      DATA ERC2CS(37)/.22069178928075602235198799872D-24/
      DATA ERC2CS(38)/-.57556172456965284983128195072D-25/
      DATA ERC2CS(39)/.15061915336392342503541440512D-25/
      DATA ERC2CS(40)/-.3954502959018796953104285696D-26/
      DATA ERC2CS(41)/.104152970415150097998464505173D-26/
      DATA ERC2CS(42)/-.275148779527876507945017890133D-27/
      DATA ERC2CS(43)/.729005820549755740899770368D-28/
      DATA ERC2CS(44)/-.193693964591594780407750109867D-28/
      DATA ERC2CS(45)/.516035711205148729837005482667D-29/
      DATA ERC2CS(46)/-.13784193221930940993896448D-29/
      DATA ERC2CS(47)/.369132679310706904225109333333D-30/
      DATA ERC2CS(48)/-.990938959062436542065322666667D-31/
      DATA ERC2CS(49)/.266649170519538841332394666667D-31/
C
C                                  SERIES FOR ERFC ON THE INTERVAL
C                                  0.0  TO  2.50000D-01
C                                  WITH WEIGHTED ERROR        1.53D-31
C                                  LOG WEIGHTED ERROR        30.82
C                                  SIGNIFICANT FIGURES REQD. 29.47
C                                  DECIMAL PLACES REQUIRED   31.70
C
      DATA ERFCCS(1)/.715179310202924774503697709496D-1/
      DATA ERFCCS(2)/-.265324343376067157558893386681D-1/
      DATA ERFCCS(3)/.171115397792085588332699194606D-2/
      DATA ERFCCS(4)/-.163751663458517884163746404749D-3/
      DATA ERFCCS(5)/.198712935005520364995974806758D-4/
      DATA ERFCCS(6)/-.284371241276655508750175183152D-5/
      DATA ERFCCS(7)/.460616130896313036969379968464D-6/
      DATA ERFCCS(8)/-.822775302587920842057766536366D-7/
      DATA ERFCCS(9)/.159214187277090112989358340826D-7/
      DATA ERFCCS(10)/-.329507136225284321486631665072D-8/
      DATA ERFCCS(11)/.72234397604005554658126115389D-9/
      DATA ERFCCS(12)/-.166485581339872959344695966886D-9/
      DATA ERFCCS(13)/.401039258823766482077671768814D-10/
      DATA ERFCCS(14)/-.100481621442573113272170176283D-10/
      DATA ERFCCS(15)/.260827591330033380859341009439D-11/
      DATA ERFCCS(16)/-.699111056040402486557697812476D-12/
      DATA ERFCCS(17)/.192949233326170708624205749803D-12/
      DATA ERFCCS(18)/-.547013118875433106490125085271D-13/
      DATA ERFCCS(19)/.158966330976269744839084032762D-13/
      DATA ERFCCS(20)/-.47268939801975548392036958429D-14/
      DATA ERFCCS(21)/.14358733767849847867287399784D-14/
      DATA ERFCCS(22)/-.444951056181735839417250062829D-15/
      DATA ERFCCS(23)/.140481088476823343737305537466D-15/
      DATA ERFCCS(24)/-.451381838776421089625963281623D-16/
      DATA ERFCCS(25)/.147452154104513307787018713262D-16/
      DATA ERFCCS(26)/-.489262140694577615436841552532D-17/
      DATA ERFCCS(27)/.164761214141064673895301522827D-17/
      DATA ERFCCS(28)/-.562681717632940809299928521323D-18/
      DATA ERFCCS(29)/.194744338223207851429197867821D-18/
      DATA ERFCCS(30)/-.682630564294842072956664144723D-19/
      DATA ERFCCS(31)/.242198888729864924018301125438D-19/
      DATA ERFCCS(32)/-.869341413350307042563800861857D-20/
      DATA ERFCCS(33)/.315518034622808557122363401262D-20/
      DATA ERFCCS(34)/-.115737232404960874261239486742D-20/
      DATA ERFCCS(35)/.428894716160565394623737097442D-21/
      DATA ERFCCS(36)/-.160503074205761685005737770964D-21/
      DATA ERFCCS(37)/.606329875745380264495069923027D-22/
      DATA ERFCCS(38)/-.231140425169795849098840801367D-22/
      DATA ERFCCS(39)/.888877854066188552554702955697D-23/
      DATA ERFCCS(40)/-.344726057665137652230718495566D-23/
      DATA ERFCCS(41)/.134786546020696506827582774181D-23/
      DATA ERFCCS(42)/-.531179407112502173645873201807D-24/
      DATA ERFCCS(43)/.210934105861978316828954734537D-24/
      DATA ERFCCS(44)/-.843836558792378911598133256738D-25/
      DATA ERFCCS(45)/.339998252494520890627359576337D-25/
      DATA ERFCCS(46)/-.13794523880732420900223837711D-25/
      DATA ERFCCS(47)/.563449031183325261513392634811D-26/
      DATA ERFCCS(48)/-.2316490434477065448234277527D-26/
      DATA ERFCCS(49)/.958446284460181015263158381226D-27/
      DATA ERFCCS(50)/-.399072288033010972624224850193D-27/
      DATA ERFCCS(51)/.167212922594447736017228709669D-27/
      DATA ERFCCS(52)/-.704599152276601385638803782587D-28/
      DATA ERFCCS(53)/.297976840286420635412357989444D-28/
      DATA ERFCCS(54)/-.126252246646061929722422632994D-28/
      DATA ERFCCS(55)/.539543870454248793985299653154D-29/
      DATA ERFCCS(56)/-.238099288253145918675346190062D-29/
      DATA ERFCCS(57)/.10990528301027615735972668375D-29/
      DATA ERFCCS(58)/-.486771374164496572732518677435D-30/
      DATA ERFCCS(59)/.152587726411035756763200828211D-30/
C
      DATA SQRTPI/1.77245385090551602729816748334D0/
      DATA NTERF/0/, NTERFC/0/, NTERC2/0/, XSML/0.0D0/, XMAX/0.0D0/,
     &     SQEPS/0.0D0/
C
      CALL E1PSH ('DERFC ')
      DERFC = DMACH(6)
C
      IF (NTERF .EQ. 0) THEN
         ETA = 0.1*SNGL(DMACH(3))
         NTERF = INITDS(ERFCS,21,ETA)
         NTERFC = INITDS(ERFCCS,59,ETA)
         NTERC2 = INITDS(ERC2CS,49,ETA)
C
         XSML = -DSQRT(-DLOG(SQRTPI*DMACH(3)))
         XMAX = DSQRT(-DLOG(SQRTPI*DMACH(1)))
         XMAX = XMAX - 0.5D0*DLOG(XMAX)/XMAX - 0.01D0
         SQEPS = DSQRT(2.0D0*DMACH(3))
      END IF
C                                  ERFC(X) = 1.0 - ERF(X)  FOR
C                                  X .LT. XSML
      IF (X .LE. XSML) THEN
         DERFC = 2.0D0
C
      ELSE IF (X .LE. XMAX) THEN
         Y = DABS(X)
C                                  ERFC(X) = 1.0 - ERF(X)  FOR
C                                  ABS(X) .LE. 1.0
         IF (Y .LE. 1.0D0) THEN
            IF (Y .LT. SQEPS) THEN
               DERFC = 1.0D0 - 2.0D0*X/SQRTPI
            ELSE
               DERFC = 1.0D0 - X*(1.0D0+DCSEVL(2.0D0*X*X-1.0D0,ERFCS,
     &                 NTERF))
            END IF
C                                  ERFC(X) = 1.0 - ERF(X)  FOR
C                                  1.0 .LT. ABS(X) .LE. XMAX
         ELSE
            Y = Y*Y
            IF (Y .LE. 4.0D0) THEN
               DERFC = DEXP(-Y)/DABS(X)*(0.5D0+DCSEVL((8.0D0/Y-5.0D0)/
     &                 3.0D0,ERC2CS,NTERC2))
            ELSE
               DERFC = DEXP(-Y)/DABS(X)*(0.5D0+DCSEVL(8.0D0/Y-1.0D0,
     &                 ERFCCS,NTERFC))
            END IF
            IF (X .LT. 0.0D0) DERFC = 2.0D0 - DERFC
         END IF
C
      ELSE
         CALL E1STD (1, X)
         CALL E1STD (2, XMAX)
         CALL E1MES (2, 1, 'The function underflows because '//
     &               'X = %(D1) is greater than %(D2). The result is '//
     &               'set to zero.')
         DERFC = 0.0D0
      END IF
C
      CALL E1POP ('DERFC ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  GAMDF/DGAMDF (Single/Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the gamma distribution function.
C
C  Usage:      GAMDF(X, A)
C
C  Arguments:
C     X      - Argument for which the gamma distribution function is to
C              be evaluated.  (Input)
C     A      - The shape parameter of the gamma distribution.  (Input)
C              This parameter must be positive.
C     GAMDF  - Function value, the probability that a gamma random
C              variable takes a value less than or equal to X.  (Output)
C
C  Remark:
C     Informational error
C     Type Code
C       1   1  The input argument, X, is less than zero.
C
C  Keywords:   P-value; Probability integral; Erlang distribution
C
C  GAMS:       L5a1g; C7e
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DGAMDF (X, A)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X, A
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I
      DOUBLE PRECISION AX, BIG, CNT, CUT, D1, D2, P, PNLG, RATIO,
     &           REDUC, V(6), V1(6), XMIN, Y, YCNT, Z
C                                  SPECIFICATIONS FOR EQUIVALENCE
      EQUIVALENCE (V(3), V1(1))
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DLOG,DEXP
cx    INTRINSIC  DABS, DLOG, DEXP
      DOUBLE PRECISION DABS, DLOG, DEXP
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH, DLNGAM
      DOUBLE PRECISION DMACH, DLNGAM
C
      CALL E1PSH ('DGAMDF ')
      DGAMDF = DMACH(6)
C                                  Check X
      IF (X .LT. 0.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (1, 1, 'Since X = %(D1) is less than zero, '//
     &               'the distribution function is zero at X. ')
         DGAMDF = 0.0D0
         GO TO 9000
      END IF
C                                  Check A
      IF (A .LE. 0.0D0) THEN
         CALL E1STD (1, A)
         CALL E1MES (5, 2, 'The shape parameter of the gamma '//
     &               'distribution must be positive.')
         GO TO 9000
      END IF
C
      IF (DLOG(X) .GE. 0.5D0*DLOG(DMACH(2))) THEN
         IF (A .GE. 0.5D0*X) THEN
            CALL E1STD (1, X)
            CALL E1STD (2, A)
            CALL E1MES (5, 3, 'Since X = %(D1) and A = %(D2) are '//
     &                  'so large, the algorithm would overflow. ')
            GO TO 9000
         ELSE
            DGAMDF = 1.0D0
            GO TO 9000
         END IF
      END IF
C
      XMIN = DLOG(DMACH(1)) + DMACH(4)
      IF (X .EQ. 0.0D0) THEN
         P = 0.0D0
      ELSE
C                                  Define LOG-GAMMA and initialize
         PNLG = DLNGAM(A)
         CNT = A*DLOG(X)
         YCNT = X + PNLG
         IF ((CNT-YCNT) .LE. XMIN) THEN
            AX = 0.0D0
         ELSE
            AX = DEXP(CNT-YCNT)
         END IF
         BIG = 1.0D35
         CUT = 1.0D-8
C                                  Choose algorithmic method
         IF ((X.GT.1.0D0) .AND. (X.GE.A)) THEN
C                                  Continued fraction expansion
            Y = 1.0D0 - A
            Z = X + Y + 1.0D0
            CNT = 0.0D0
            V(1) = 1.0D0
            V(2) = X
            V(3) = X + 1.0D0
            V(4) = Z*X
            P = V(3)/V(4)
   10       CNT = CNT + 1.0D0
            Y = Y + 1.0D0
            Z = Z + 2.0D0
            YCNT = Y*CNT
            V(5) = V1(1)*Z - V(1)*YCNT
            V(6) = V1(2)*Z - V(2)*YCNT
            IF (V(6) .EQ. 0.0D0) THEN
               DO 20  I=1, 4
                  V(I) = V1(I)
   20          CONTINUE
               IF (DABS(V(5)).LT.BIG .AND. DABS(V(6)).LT.BIG) GO TO 10
C                                  Scale terms down to prevent overflow
               DO 30  I=1, 4
                  V(I) = V(I)/BIG
   30          CONTINUE
               GO TO 10
            END IF
            RATIO = V(5)/V(6)
            REDUC = DABS(P-RATIO)
            IF (REDUC.LE.RATIO*CUT .AND. REDUC.LE.CUT) THEN
               P = 1.0D0 - P*AX
            ELSE
               P = RATIO
               DO 40  I=1, 4
                  V(I) = V1(I)
   40          CONTINUE
               IF (DABS(V(5)).LT.BIG .AND. DABS(V(6)).LT.BIG) GO TO 10
C                                  Scale terms down to prevent overflow
               DO 50  I=1, 4
                  V(I) = V(I)/BIG
   50          CONTINUE
               GO TO 10
            END IF
         ELSE
C                                  Series expansion
            RATIO = A
            CNT = 1.0D0
            P = 1.0D0
   60       RATIO = RATIO + 1.0D0
            CNT = CNT*X/RATIO
            P = P + CNT
            IF (CNT .GT. CUT) GO TO 60
            P = P*AX/A
         END IF
      END IF
C
      DGAMDF = P
 9000 CALL E1POP ('DGAMDF ')
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  GAMMA/DGAMMA (Single/Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    June 23, 1986
C
C  Purpose:    Evaluate the complete gamma function.
C
C  Usage:      GAMMA(X)
C
C  Arguments:
C     X      - Argument for which the complete gamma function is
C              desired.  (Input)
C     GAMMA  - Function value.  (Output)
C
C  Remark:
C     Informational errors
C     Type Code
C       2   1  The function underflows because X is too small.
C       3   2  Result is accurate to less than one half precision
C              because X is too near a negative integer.
C
C  GAMS:       C7a
C
C  Chapters:   SFUN/LIBRARY Gamma Function and Related Functions
C              STAT/LIBRARY Mathematical Support
C              MATH/LIBRARY Utilities
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DGAMMA (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, N
      DOUBLE PRECISION SINPIY, XI, XN, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NGAMCS
      DOUBLE PRECISION DXREL, GAMCS(42), PI, SQ2PIL, XMAX, XMIN, XSML
      SAVE       DXREL, GAMCS, NGAMCS, PI, SQ2PIL, XMAX, XMIN, XSML
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DINT,DLOG,DMAX1,DEXP,DSIN,DSQRT
cx    INTRINSIC  DABS, DINT, DLOG, DMAX1, DEXP, DSIN, DSQRT
      DOUBLE PRECISION DABS, DINT, DLOG, DMAX1, DEXP, DSIN, DSQRT
C     INTRINSIC  SNGL
      INTRINSIC  SNGL
      REAL       SNGL
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD, D9GAML
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH, DCSEVL, INITDS, D9LGMC
      INTEGER    INITDS
      DOUBLE PRECISION DMACH, DCSEVL, D9LGMC
C
C                                  SERIES FOR GAMMA ON THE INTERVAL
C                                  0.0 TO 1.00000D+00
C                                  WITH WEIGHTED ERROR         5.79D-32
C                                  LOG WEIGHTED ERROR         31.24
C                                  SIGNIFICANT FIGURES REQD.  30.00
C                                  DECIMAL PLACES REQUIRED    32.05
C
      DATA GAMCS(1)/.857119559098933142192006239994D-2/
      DATA GAMCS(2)/.441538132484100675719131577165D-2/
      DATA GAMCS(3)/.568504368159936337863266458879D-1/
      DATA GAMCS(4)/-.421983539641856050101250018662D-2/
      DATA GAMCS(5)/.132680818121246022058400679635D-2/
      DATA GAMCS(6)/-.189302452979888043252394702389D-3/
      DATA GAMCS(7)/.360692532744124525657808221723D-4/
      DATA GAMCS(8)/-.605676190446086421848554829037D-5/
      DATA GAMCS(9)/.105582954630228334473182350909D-5/
      DATA GAMCS(10)/-.181196736554238404829185589117D-6/
      DATA GAMCS(11)/.311772496471532227779025459317D-7/
      DATA GAMCS(12)/-.535421963901968714087408102435D-8/
      DATA GAMCS(13)/.919327551985958894688778682594D-9/
      DATA GAMCS(14)/-.157794128028833976176742327395D-9/
      DATA GAMCS(15)/.270798062293495454326654043309D-10/
      DATA GAMCS(16)/-.464681865382573014408166105893D-11/
      DATA GAMCS(17)/.797335019200741965646076717536D-12/
      DATA GAMCS(18)/-.136807820983091602579949917231D-12/
      DATA GAMCS(19)/.234731948656380065723347177169D-13/
      DATA GAMCS(20)/-.40274326149490669327665705347D-14/
      DATA GAMCS(21)/.691005174737210091213833697526D-15/
      DATA GAMCS(22)/-.118558450022199290705238712619D-15/
      DATA GAMCS(23)/.203414854249637395520102605193D-16/
      DATA GAMCS(24)/-.349005434171740584927401294911D-17/
      DATA GAMCS(25)/.598799385648530556713505106603D-18/
      DATA GAMCS(26)/-.102737805787222807449006977843D-18/
      DATA GAMCS(27)/.176270281606052982494275966075D-19/
      DATA GAMCS(28)/-.302432065373530626095877211204D-20/
      DATA GAMCS(29)/.518891466021839783971783355051D-21/
      DATA GAMCS(30)/-.890277084245657669244925160107D-22/
      DATA GAMCS(31)/.152747406849334260227459689131D-22/
      DATA GAMCS(32)/-.26207312561873629002573283328D-23/
      DATA GAMCS(33)/.449646404783053867033104657067D-24/
      DATA GAMCS(34)/-.771471273133687791170390152533D-25/
      DATA GAMCS(35)/.132363545312604403648657271467D-25/
      DATA GAMCS(36)/-.227099941294292881670231381333D-26/
      DATA GAMCS(37)/.389641899800399144932081664D-27/
      DATA GAMCS(38)/-.6685198115125953327792128D-28/
      DATA GAMCS(39)/.114699866314002438434761386667D-28/
      DATA GAMCS(40)/-.1967938586345134677295104D-29/
      DATA GAMCS(41)/.337644881658533809033489066667D-30/
      DATA GAMCS(42)/-.579307033578213578462549333333D-31/
C
      DATA PI/3.14159265358979323846264338328D0/
C                                  SQ2PIL IS 0.5*ALOG(2*PI) =
C                                  ALOG(SQRT(2*PI))
      DATA SQ2PIL/0.918938533204672741780329736406D0/
      DATA NGAMCS/0/, XMIN/0.0D0/, XMAX/0.0D0/, DXREL/0.0D0/,
     &     XSML/0.0D0/
C
      CALL E1PSH ('DGAMMA ')
      DGAMMA = DMACH(6)
C
      IF (NGAMCS .EQ. 0) THEN
C                                  INITIALIZE. FIND LEGAL BOUNDS FOR X,
C                                  AND DETERMINE THE NUMBER OF TERMS IN
C                                  THE SERIES REQUIRED TO ATTAIN AN
C                                  ACCURACY TEN TIMES BETTER THAN
C                                  MACHINE PRECISION.
         NGAMCS = INITDS(GAMCS,42,0.1*SNGL(DMACH(3)))
         CALL D9GAML (XMIN, XMAX)
         DXREL = DSQRT(DMACH(4))
         XSML = DEXP(DMAX1(DLOG(DMACH(1)),-DLOG(DMACH(2)))+0.01D0)
      END IF
C                                  START EVALUATING GAMMA(X)
      Y = DABS(X)
C
      IF (Y .GT. 10.0D0) GO TO 40
C                                  COMPUTE GAMMA(X) FOR ABS(X).LE.10.0.
C                                  REDUCE INTERVAL AND FIND GAMMA(1+Y)
C                                  FOR 0.0 .LE. Y .LT. 1.0 FIRST OF ALL.
      N = X
      IF (X .LT. 0.0D0) N = N - 1
      XN = N
      Y = X - XN
      N = N - 1
      DGAMMA = 0.9375D0 + DCSEVL(2.0D0*Y-1.0D0,GAMCS,NGAMCS)
      IF (N .EQ. 0) GO TO 9000
C
      IF (N .GT. 0) GO TO 20
C                                  COMPUTE GAMMA(X) FOR X .LT. 1.
      N = -N
C
      IF (X .EQ. 0.0D0) THEN
         CALL E1MES (5, 5, 'The argument for the function can '//
     &               'not be zero.')
         DGAMMA = DMACH(6)
         GO TO 9000
      END IF
C
      IF (Y .LT. XSML) THEN
         CALL E1STD (1, X)
         CALL E1MES (5, 4, 'The function overflows because '//
     &               'X = %(D1) is too close to zero.')
         DGAMMA = DMACH(6)
         GO TO 9000
      END IF
C
      XN = N - 2
      IF (X.LT.0.0D0 .AND. X+XN.EQ.0.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (5, 6, 'The argument for the function can '//
     &               'not be a negative integer. Argument X = %(D1).')
         DGAMMA = DMACH(6)
         GO TO 9000
      END IF
C
      IF (X.LT.-0.5D0 .AND. DABS((X-DINT(X-0.5D0))/X).LT.DXREL) THEN
         CALL E1STD (1, X)
         CALL E1MES (3, 2, 'The result is accurate to less than '//
     &               'one half precision because X = %(D1) is too '//
     &               'close to a negative integer.')
      END IF
C
      XI = 0.0D0
      DO 10  I=1, N
         DGAMMA = DGAMMA/(X+XI)
         XI = XI + 1.0D0
   10 CONTINUE
      GO TO 9000
C                                  GAMMA(X) FOR X .GE. 2.0
   20 XI = 1.0D0
      DO 30  I=1, N
         DGAMMA = (Y+XI)*DGAMMA
         XI = XI + 1.0D0
   30 CONTINUE
      GO TO 9000
C                                  GAMMA(X) FOR ABS(X) .GT. 10.0.
C                                  RECALL Y = ABS(X).
   40 IF (X .GT. XMAX) THEN
         CALL E1STD (1, X)
         CALL E1STD (2, XMAX)
         CALL E1MES (5, 4, 'The function overflows because '//
     &               'X = %(D1) is greater than %(D2).')
         DGAMMA = DMACH(6)
         GO TO 9000
      END IF
C
      DGAMMA = 0.0D0
      IF (X .LT. XMIN) THEN
         CALL E1STD (1, X)
         CALL E1STD (2, XMIN)
         CALL E1MES (2, 1, 'The function underflows because '//
     &               'X = %(D1) is less than %(D2). The result is '//
     &               'set to zero.')
         GO TO 9000
      END IF
C
      DGAMMA = DEXP((Y-0.5D0)*DLOG(Y)-Y+SQ2PIL+D9LGMC(Y))
      IF (X .GT. 0.0D0) GO TO 9000
C
      IF (DABS((X-DINT(X-0.5D0))/X) .LT. DXREL) THEN
         CALL E1STD (1, X)
         CALL E1MES (3, 2, 'The result is accurate to less than '//
     &               'one half precision because X = %(D1) is too '//
     &               'close to a negative integer.')
      END IF
C
      SINPIY = DSIN(PI*Y)
      IF (SINPIY .EQ. 0.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (5, 7, 'The argument for the function can '//
     &               'not be a negative integer. Argument X = %(D1).')
         DGAMMA = DMACH(6)
         GO TO 9000
      END IF
C
      DGAMMA = -PI/(Y*SINPIY*DGAMMA)
C
 9000 CALL E1POP ('DGAMMA ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DLBETA (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the natural logarithm of the complete beta
C              function for positive arguments.
C
C  Usage:      DLBETA(A, B)
C
C  Arguments:
C     A      - The first argument of the BETA function.  (Input)
C     B      - The second argument of the BETA function.  (Input)
C     DLBETA - Function value.  (Output)
C
C  Remarks:
C  1. DLBETA returns the natural log of
C     BETA(A,B) = DLOG (GAMMA(A)*GAMMA(B))/GAMMA(A+B)
C
C  2. Note than the natural log of BETA(A,B) equals the natural log
C     of BETA(B,A).
C
C  3. DLBETA (A,B) returns accurate results even when A or B is very
C     small.
C
C  4. The arguments, A and B, must both be greater than 0.
C
C  GAMS:       C7b
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DLBETA (A, B)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION A, B
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      DOUBLE PRECISION CORR, P, Q
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      DOUBLE PRECISION SQ2PIL
      SAVE       SQ2PIL
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DLOG,DMAX1,DMIN1
cx    INTRINSIC  DLOG, DMAX1, DMIN1
      DOUBLE PRECISION DLOG, DMAX1, DMIN1
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   D9LGMC, DGAMMA, DLNGAM, DLNREL, DMACH, N1RCD
      INTEGER    N1RCD
      DOUBLE PRECISION D9LGMC, DGAMMA, DLNGAM, DLNREL, DMACH
C
      DATA SQ2PIL/.918938533204672741780329736406D0/
C
      CALL E1PSH ('DLBETA')
      DLBETA = DMACH(6)
C
      P = DMIN1(A,B)
      Q = DMAX1(A,B)
C
      IF (P .LE. 0.0D0) THEN
         CALL E1MES (5, 5, 'Both arguments for the function '//
     &               'must be greater than zero.')
C
      ELSE IF (P .GE. 10.0D0) THEN
C                                  P AND Q ARE BIG.
         CORR = D9LGMC(P) + D9LGMC(Q) - D9LGMC(P+Q)
C                                  CHECK FOR UNDERFLOW FROM D9LGMC
         IF (N1RCD(0) .EQ. 1) CALL E1MES (0, 0, ' ')
         DLBETA = -0.5D0*DLOG(Q) + SQ2PIL + CORR +
     &            (P-0.5D0)*DLOG(P/(P+Q)) + Q*DLNREL(-P/(P+Q))
C
      ELSE IF (Q .GE. 10.0D0) THEN
C                                  P IS SMALL, BUT Q IS BIG.
         CORR = D9LGMC(Q) - D9LGMC(P+Q)
C                                  CHECK FOR UNDERFLOW FROM D9LGMC
         IF (N1RCD(0) .EQ. 1) CALL E1MES (0, 0, ' ')
         DLBETA = DLNGAM(P) + CORR + P - P*DLOG(P+Q) +
     &            (Q-0.5D0)*DLNREL(-P/(P+Q))
C
      ELSE
C                                  P AND Q ARE SMALL.
         DLBETA = DLOG(DGAMMA(P)*(DGAMMA(Q)/DGAMMA(P+Q)))
      END IF
C
      CALL E1POP ('DLBETA')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DLNGAM (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the logarithm of the absolute value of the
C              gamma function.
C
C  Usage:      DLNGAM(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     DLNGAM - Function value.  (Output)
C
C  Remark:
C     Informational error:
C     Type Code
C       3   2  Result of DLNGAM(X) is accurate to less than one half
C              precision because X is too near a negative integer.
C
C  GAMS:       C7a
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DLNGAM (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      DOUBLE PRECISION SINPIY, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      DOUBLE PRECISION DXREL, PI, SQ2PIL, SQPI2L, XMAX
      SAVE       DXREL, PI, SQ2PIL, SQPI2L, XMAX
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DINT,DLOG,DSIN,DSQRT
cx    INTRINSIC  DABS, DINT, DLOG, DSIN, DSQRT
      DOUBLE PRECISION DABS, DINT, DLOG, DSIN, DSQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   D9LGMC, DGAMMA, DMACH
      DOUBLE PRECISION D9LGMC, DGAMMA, DMACH
C
      DATA PI/3.14159265358979323846264338328D0/
C                                  SQ2PIL = ALOG (SQRT(2*PI))
C                                  SQPI2L = ALOG(SQRT(PI/2))
      DATA SQ2PIL/0.918938533204672741780329736406D0/
      DATA SQPI2L/.225791352644727432363097614947D0/
C
      DATA XMAX/0.0D0/, DXREL/0.0D0/
C
      CALL E1PSH ('DLNGAM')
      DLNGAM = DMACH(6)
C
      IF (XMAX .EQ. 0.0D0) THEN
         XMAX = DMACH(2)/DLOG(DMACH(2))
         DXREL = DSQRT(DMACH(4))
      END IF
C
      Y = DABS(X)
C                                  DLOG (DABS (DGAMMA(X)) )
C                                  FOR DABS(X) .LE. 10.0
      IF (Y .LE. 10.0D0) THEN
         DLNGAM = DLOG(DABS(DGAMMA(X)))
C                                  DLOG ( DABS (DGAMMA(X)) )
C                                  FOR DABS(X) .GT. 10.0
      ELSE IF (Y .GT. XMAX) THEN
         CALL E1STD (1, X)
         CALL E1STD (2, XMAX)
         CALL E1MES (5, 4, 'The function overflows because '//
     &               'ABS(%(D1)) is greater than %(D2).')
C
      ELSE IF (X .GT. 0.0D0) THEN
         DLNGAM = SQ2PIL + (X-0.5D0)*DLOG(X) - X + D9LGMC(Y)
C
      ELSE
         SINPIY = DABS(DSIN(PI*Y))
         IF (SINPIY .EQ. 0.0D0) THEN
            CALL E1STD (1, X)
            CALL E1MES (5, 5, 'The argument for the function can '//
     &                  'not be a negative integer. Argument X = '//
     &                  '%(D1).')
C
         ELSE
            DLNGAM = SQPI2L + (X-0.5D0)*DLOG(Y) - X - DLOG(SINPIY) -
     &               D9LGMC(Y)
C
            IF (DABS((X-DINT(X-0.5D0))*DLNGAM/X) .LT. DXREL) THEN
               CALL E1STD (1, X)
               CALL E1MES (3, 2, 'The result is accurate to '//
     &                     'less than one half precision because X = '//
     &                     '%(D1) is too close to a negative '//
     &                     'integer.')
            END IF
         END IF
      END IF
C
      CALL E1POP ('DLNGAM')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DLNREL (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the natural logarithm of one plus the argument.
C
C  Usage:      DLNREL(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     DLNREL - Function value.  (Output)
C
C  Remarks:
C  1. Informational error:
C     Type Code
C       3   2  Result of DLNREL(X) is accurate to less than one half
C              precision because X is too near -1.0.
C
C  2. DLNREL evaluates the natural logarithm of (1+X) accurate in
C     the sense of relative error even when X is very small. This
C     routine (as opposed to DLOG) should be used to maintain relative
C     accuracy whenever X is small and accurately known.
C
C  GAMS:       C4b
C
C  Chapter:    SFUN/LIBRARY Elementary Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DLNREL (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION X
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NLNREL
      DOUBLE PRECISION ALNRCS(43), XMIN
      SAVE       ALNRCS, NLNREL, XMIN
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DABS,DLOG,DSQRT,SNGL
cx    INTRINSIC  DABS, DLOG, DSQRT, SNGL
      REAL       SNGL
      DOUBLE PRECISION DABS, DLOG, DSQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DCSEVL, DMACH, INITDS
      INTEGER    INITDS
      DOUBLE PRECISION DCSEVL, DMACH
C
C                                  SERIES FOR ALNR ON THE INTERVAL
C                                  -3.75000D-01 TO  3.75000D-01
C                                  WITH WEIGHTED ERROR         6.35D-32
C                                  LOG WEIGHTED ERROR         31.20
C                                  SIGNIFICANT FIGURES REQD.  30.93
C                                  DECIMAL PLACES REQUIRED    32.01
C
      DATA ALNRCS(1)/.103786935627437698006862677191D+1/
      DATA ALNRCS(2)/-.133643015049089180987660415531D+0/
      DATA ALNRCS(3)/.194082491355205633579261993748D-1/
      DATA ALNRCS(4)/-.301075511275357776903765377766D-2/
      DATA ALNRCS(5)/.486946147971548500904563665091D-3/
      DATA ALNRCS(6)/-.810548818931753560668099430086D-4/
      DATA ALNRCS(7)/.137788477995595247829382514961D-4/
      DATA ALNRCS(8)/-.238022108943589702513699929149D-5/
      DATA ALNRCS(9)/.41640416213865183476391859902D-6/
      DATA ALNRCS(10)/-.73595828378075994984266837032D-7/
      DATA ALNRCS(11)/.13117611876241674949152294345D-7/
      DATA ALNRCS(12)/-.235467093177424251366960923302D-8/
      DATA ALNRCS(13)/.425227732760349977756380529626D-9/
      DATA ALNRCS(14)/-.771908941348407968261081074933D-10/
      DATA ALNRCS(15)/.140757464813590699092153564722D-10/
      DATA ALNRCS(16)/-.257690720580246806275370786276D-11/
      DATA ALNRCS(17)/.473424066662944218491543950059D-12/
      DATA ALNRCS(18)/-.872490126747426417453012632927D-13/
      DATA ALNRCS(19)/.161246149027405514657398331191D-13/
      DATA ALNRCS(20)/-.298756520156657730067107924168D-14/
      DATA ALNRCS(21)/.554807012090828879830413216973D-15/
      DATA ALNRCS(22)/-.103246191582715695951413339619D-15/
      DATA ALNRCS(23)/.192502392030498511778785032449D-16/
      DATA ALNRCS(24)/-.359550734652651500111897078443D-17/
      DATA ALNRCS(25)/.672645425378768578921945742268D-18/
      DATA ALNRCS(26)/-.126026241687352192520824256376D-18/
      DATA ALNRCS(27)/.236448844086062100449161589555D-19/
      DATA ALNRCS(28)/-.444193770508079368988783891797D-20/
      DATA ALNRCS(29)/.835465944640342590162412939947D-21/
      DATA ALNRCS(30)/-.157315594164795625748992535211D-21/
      DATA ALNRCS(31)/.296531287402474226861543697067D-22/
      DATA ALNRCS(32)/-.559495834818159472921560132267D-23/
      DATA ALNRCS(33)/.105663542688356810481872841387D-23/
      DATA ALNRCS(34)/-.199724836806702045483149994667D-24/
      DATA ALNRCS(35)/.37782977818839361421049856D-25/
      DATA ALNRCS(36)/-.715315868890817403450381653333D-26/
      DATA ALNRCS(37)/.135524884636742136465020245333D-26/
      DATA ALNRCS(38)/-.256946730484875674300798293333D-27/
      DATA ALNRCS(39)/.4874775606621694907645952D-28/
      DATA ALNRCS(40)/-.925421125308497153211323733333D-29/
      DATA ALNRCS(41)/.1757859784176023923326976D-29/
      DATA ALNRCS(42)/-.334100266777310103513770666667D-30/
      DATA ALNRCS(43)/.635339361802361873541802666667D-31/
C
      DATA NLNREL/0/, XMIN/0.0D0/
C
      CALL E1PSH ('DLNREL')
      DLNREL = DMACH(6)
C
      IF (NLNREL .EQ. 0) THEN
         NLNREL = INITDS(ALNRCS,43,0.1*SNGL(DMACH(3)))
         XMIN = -1.0D0 + DSQRT(DMACH(4))
      END IF
C
      IF (X .LE. -1.0D0) THEN
         CALL E1STD (1, X)
         CALL E1MES (5, 5, 'The argument X = %(D1) must be '//
     &               'greater than -1.0.')
C
      ELSE
         IF (DABS(X) .LE. 0.375D0) THEN
            DLNREL = X*(1.0D0-X*DCSEVL(X/.375D0,ALNRCS,NLNREL))
         ELSE
            DLNREL = DLOG(1.0D0+X)
         END IF
C
         IF (X .LT. XMIN) THEN
            CALL E1STD (1, X)
            CALL E1STD (2, XMIN)
            CALL E1MES (3, 2, 'The result is accurate to less '//
     &                  'than one half precision because X = %(D1) '//
     &                  'is too close to -1.0. X must be greater '//
     &                  'than %(D2).')
         END IF
      END IF
C
      CALL E1POP ('DLNREL')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  DMACH (Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    March 15, 1984
C
C  Purpose:    Generate double precision machine constants.
C
C  Usage:      DMACH(N)
C
C  Arguments:
C     N      - Index of desired constant.  (Input)
C     DMACH  - Machine constant.  (Output)
C              DMACH(1) = B**(EMIN-1), the smallest positive magnitude.
C              DMACH(2) = B**EMAX*(1 - B**(-T)), the largest magnitude.
C              DMACH(3) = B**(-T), the smallest relative spacing.
C              DMACH(4) = B**(1-T), the largest relative spacing.
C              DMACH(5) = LOG10(B), the log, base 10, of the radix.
C              DMACH(6) = not-a-number.
C              DMACH(7) = positive machine infinity.
C              DMACH(8) = negative machine infinity.
C
C  GAMS:       R1
C
C  Chapters:   MATH/LIBRARY Reference Material
C              STAT/LIBRARY Reference Material
C              SFUN/LIBRARY Reference Material
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DMACH (N)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      DOUBLE PRECISION RMACH(8)
      SAVE       RMACH
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STI
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IRMACH(16)
C
      EQUIVALENCE (RMACH, IRMACH)
C                                  DEFINE CONSTANTS
      DATA RMACH(1)/2.22559D-308/
      DATA RMACH(2)/1.79728D308/
      DATA RMACH(3)/1.11048D-16/
      DATA RMACH(4)/2.22096D-16/
      DATA RMACH(5)/.3010299956639811952137388947245D0/
      DATA IRMACH(11)/0/
      DATA IRMACH(12)/1206910591/
      DATA RMACH(7)/1.79728D308/
      DATA RMACH(8)/-1.79728D308/
C
      IF (N.LT.1 .OR. N.GT.8) THEN
         CALL E1PSH ('DMACH ')
         DMACH = RMACH(6)
         CALL E1STI (1, N)
         CALL E1MES (5, 5, 'The argument must be between 1 '//
     &               'and 8 inclusive. N = %(I1)')
         CALL E1POP ('DMACH ')
      ELSE
         DMACH = RMACH(N)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  TDF/DTDF (Single/Double precision version)
C
C  Computer:   PCDSMS/DOUBLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the Student's t distribution function.
C
C  Usage:      TDF(T, DF)
C
C  Arguments:
C     T      - Argument for which the Student's t distribution function
C              is to be evaluated.  (Input)
C     DF     - Degrees of freedom.  (Input)
C              DF must be greater than or equal to 1.0.
C     TDF    - Function value, the probability that a Student's t random
C              variable takes a value less than or equal to the input T.
C              (Output)
C
C  Keywords:   P-value; Probability integral
C
C  GAMS:       L5a1t
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      DOUBLE PRECISION FUNCTION DTDF (T, DF)
C                                  SPECIFICATIONS FOR ARGUMENTS
      DOUBLE PRECISION T, DF
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    N
      DOUBLE PRECISION A, AN, B, Q, TEMP, W, XJ, Y, Z
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      DOUBLE PRECISION CON1
      SAVE       CON1
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DLOG,DATAN,DSQRT
cx    INTRINSIC  DLOG, DATAN, DSQRT
      DOUBLE PRECISION DLOG, DATAN, DSQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STD
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   DMACH, DBETDF, DERFC
      DOUBLE PRECISION DMACH, DBETDF, DERFC
C
      DATA CON1/0.63661977236758D0/
C
      CALL E1PSH ('DTDF   ')
      DTDF = DMACH(6)
C                                  Check DF
      IF (DF .LT. 1.0D0) THEN
         CALL E1STD (1, DF)
         CALL E1MES (5, 1, 'The input number of degrees of freedom, '//
     &               'DF = %(D1), must be at least 1.')
         GO TO 9000
      END IF
C
      TEMP = T*T
      IF (DF .GT. TEMP) THEN
         TEMP = T
         AN = DF
         N = AN
         TEMP = TEMP*TEMP
         Y = TEMP/AN
         B = 1.0D0 + Y
         IF (AN.NE.N .OR. AN.GE.20.0D0 .OR. AN.GT.200.0D0) THEN
C                                  Asymptotic series for large AN
            W = B - 1.0D0
            IF (W .NE. 0.0D0) Y = Y*(DLOG(B)/W)
            A = AN - 0.5D0
            B = 48.0D0*A*A
            Y = Y*A
            Y = (((((-0.4D0*Y-3.3D0)*Y-24.0D0)*Y-85.5D0)/(0.8D0*(Y*Y)+
     &          100.0D0+B)+Y+3.0D0)/B+1.0D0)*DSQRT(Y)
            IF (Y .LT. 18.8125D0) THEN
C                                  Overflow (or underflow?) could occur
C                                  on some machines on call to ERFC
               Q = DERFC(Y*DSQRT(0.5D0))
            ELSE
               Q = 0.0D0
            END IF
         ELSE
            IF (AN.LT.20.0D0 .AND. TEMP.LT.4.0D0) THEN
C                                  Nested summation of *COSINE* series
               Y = DSQRT(Y)
               A = Y
               IF (AN .EQ. 1.0D0) A = 0.0D0
   10          AN = AN - 2.0D0
               IF (AN .GT. 1.0D0) THEN
                  A = (AN-1.0D0)/(B*AN)*A + Y
                  GO TO 10
               END IF
               IF (AN .EQ. 0.0D0) A = A/DSQRT(B)
               IF (AN .NE. 0.0D0) A = (DATAN(Y)+A/B)*CON1
               Q = 1.0D0 - A
            ELSE
C                                  *TAIL* series expansion for large
C                                  T-values
               A = 1.0D0
               Y = AN
               XJ = 0.0D0
               Z = 0.0D0
   20          IF (A .NE. Z) THEN
                  XJ = XJ + 2.0D0
                  Z = A
                  Y = Y*(XJ-1.0D0)/(B*XJ)
                  A = A + Y/(AN+XJ)
                  GO TO 20
               END IF
   30          IF (AN.GT.1.0D0 .AND. A.GE.1.0D-30) THEN
C                                  NOTE:  The conditional, A.GE.1.0E-30,
C                                  included above is needed for the
C                                  division by A below (overflow).
C                                  According to the original basis deck,
C                                  some machines require a less
C                                  restriction on A or none at all.
                  A = (AN-1.0D0)/(B*AN)*A
                  AN = AN - 2.0D0
                  GO TO 30
               END IF
               IF (AN .NE. 0.0D0) A = DSQRT(B)*CON1*A/B
               Q = A
            END IF
         END IF
      ELSE
         TEMP = DF/(DF+TEMP)
         A = 0.5D0*DF
         B = 0.5D0
         Q = DBETDF(TEMP,A,B)
      END IF
C
      IF (T .GT. 0.0D0) THEN
         DTDF = 1.0D0 - 0.5D0*Q
      ELSE
         DTDF = 0.5D0*Q
      END IF
C
 9000 CALL E1POP ('DTDF   ')
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1INIT
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 13, 1984
C
C  Purpose:    Initialization.
C
C  Usage:      CALL E1INIT
C
C  Arguments:  None
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1INIT
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    L
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    ISINIT
      SAVE       ISINIT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                              SPECIFICATIONS FOR COMMON /ERCOM8/
      INTEGER    PROLVL, XXLINE(10), XXPLEN(10), ICALOC(10), INALOC(10)
      COMMON     /ERCOM8/ PROLVL, XXLINE, XXPLEN, ICALOC, INALOC
      SAVE       /ERCOM8/
C                              SPECIFICATIONS FOR COMMON /ERCOM9/
      CHARACTER  XXPROC(10)*31
      COMMON     /ERCOM9/ XXPROC
      SAVE       /ERCOM9/
C
      DATA ISINIT/0/
C
      IF (ISINIT .EQ. 0) THEN
C                                  INITIALIZE
         CALLVL = 1
         ERCODE(1) = 0
         ERTYPE(1) = 0
         IALLOC(1) = 0
         ISUSER(1) = .TRUE.
         IFERR6 = 0
         IFERR7 = 0
         PLEN = 1
         MAXLEV = 50
         DO 10  L=2, 51
            ERTYPE(L) = -1
            ERCODE(L) = -1
            IALLOC(L) = 0
            ISUSER(L) = .FALSE.
   10    CONTINUE
         DO 20  L=1, 7
            HDRFMT(L) = 1
            TRACON(L) = 1
   20    CONTINUE
         PROLVL = 1
         DO 30  L=1, 10
   30    ICALOC(L) = 0
         XXLINE(1) = 0
         XXPLEN(1) = 1
         XXPROC(1) = '?'
         RNAME(1) = 'USER'
         PRINTB(1) = 0
         PRINTB(2) = 0
         DO 40  L=3, 7
   40    PRINTB(L) = 1
         STOPTB(1) = 0
         STOPTB(2) = 0
         STOPTB(3) = 0
         STOPTB(4) = 1
         STOPTB(5) = 1
         STOPTB(6) = 0
         STOPTB(7) = 1
         ERCKSM = 0.0D0
C                                  SET FLAG TO INDICATE THAT
C                                    INITIALIZATION HAS OCCURRED
         ISINIT = 1
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1INPL
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 2, 1984
C
C  Purpose:    To store a character string in the parameter list PLIST
C              for use by the error message handler.
C
C  Usage:      CALL E1INPL(FORM,NUM,SLEN,STRUP)
C
C  Arguments:
C     FORM   - A character string of length one to be inserted into
C              PLIST which specifies the form of the string.  (Input)
C              For example, 'L' for string, 'A' for character array,
C              'I' for integer, 'K' for keyword (PROTRAN only).  An
C              asterisk is inserted into PLIST preceding FORM.
C     NUM    - Integer to be inserted as a character into PLIST
C              immediately following FORM.  (Input)  NUM must be between
C              1 and 9.
C     SLEN   - The number of characters in STRUP.  (Input)  LEN must be
C              less than or equal to 255.  The character representation
C              of SLEN is inserted into PLIST after NUM and an asterisk.
C     STRUP  - A character string of length LEN which is to be inserted
C              into PLIST.  (Input)  Trailing blanks are ignored.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1INPL (FORM, NUM, SLEN, STRUP)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    NUM, SLEN
      CHARACTER  FORM, STRUP(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IER, L, LEN2, LENCK, LOC, NLEN, NNUM
      CHARACTER  STRNCH(3)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      CHARACTER  BLANK, PRCNT(1), TEMP(4)
      SAVE       BLANK, PRCNT, TEMP
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  IABS
      INTRINSIC  IABS
      INTEGER    IABS
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   C1TIC, M1VE
C
      DATA TEMP/'*', ' ', ' ', '*'/, PRCNT/'%'/, BLANK/' '/
C
      NNUM = IABS(NUM)
      LENCK = PLEN + SLEN + 8
      IF (NNUM.GE.1 .AND. NNUM.LE.9 .AND. LENCK.LE.300) THEN
         TEMP(2) = FORM
         CALL C1TIC (NNUM, TEMP(3), 1, IER)
         LOC = PLEN + 1
         IF (LOC .EQ. 2) LOC = 1
         CALL M1VE (TEMP, 1, 4, 4, PLIST(LOC), 1, 4, 262, IER)
         LOC = LOC + 4
         IF (NUM .LT. 0) THEN
            LEN2 = SLEN
         ELSE
            DO 10  L=1, SLEN
               LEN2 = SLEN - L + 1
               IF (STRUP(LEN2) .NE. BLANK) GO TO 20
   10       CONTINUE
            LEN2 = 1
   20       CONTINUE
         END IF
         NLEN = 1
         IF (LEN2 .GE. 10) NLEN = 2
         IF (LEN2 .GE. 100) NLEN = 3
         CALL C1TIC (LEN2, STRNCH, NLEN, IER)
         CALL M1VE (STRNCH, 1, NLEN, 3, PLIST(LOC), 1, NLEN, 262, IER)
         LOC = LOC + NLEN
         CALL M1VE (PRCNT, 1, 1, 1, PLIST(LOC), 1, 1, 262, IER)
         LOC = LOC + 1
         CALL M1VE (STRUP, 1, LEN2, LEN2, PLIST(LOC), 1, LEN2, 262,
     &              IER)
         PLEN = LOC + LEN2 - 1
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1MES
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 2, 1984
C
C  Purpose:    Set an error state for the current level in the stack.
C              The message is printed immediately if the error type is
C              5, 6, or 7 and the print attribute for that type is YES.
C
C  Usage:      CALL E1MES(IERTYP,IERCOD,MSGPKD)
C
C  Arguments:
C     IERTYP - Integer specifying the error type.  (Input)
C                IERTYP=1,  informational/note
C                IERTYP=2,  informational/alert
C                IERTYP=3,  informational/warning
C                IERTYP=4,  informational/fatal
C                IERTYP=5,  terminal
C                IERTYP=6,  PROTRAN/warning
C                IERTYP=7,  PROTRAN/fatal
C     IERCOD - Integer specifying the error code.  (Input)
C     MSGPKD - A character string containing the message.
C              (Input)  Within the message, any of following may appear
C                %(A1),%(A2),...,%(A9) for character arrays
C                %(C1),%(C2),...,%(C9) for complex numbers
C                %(D1),%(D2),...,%(D9) for double precision numbers
C                %(I1),%(I2),...,%(I9) for integer numbers
C                %(K1),%(K2),...,%(K9) for keywords
C                %(L1),%(L2),...,%(L9) for literals (strings)
C                %(R1),%(R2),...,%(R9) for real numbers
C                %(Z1),%(Z2),...,%(Z9) for double complex numbers
C              This provides a way to insert character arrays, strings,
C              numbers, and keywords into the message.  See remarks
C              below.
C
C  Remarks:
C     The number of characters in the message after the insertion of
C     the corresponding strings, etc. should not exceed 255.  If the
C     limit is exceeded, only the first 255 characters will be used.
C     The appropriate strings, etc. need to have been previously stored
C     in common via calls to E1STA, E1STD, etc.  Line breaks may be
C     specified by inserting the two characters '%/' into the message
C     at the desired locations.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1MES (IERTYP, IERCOD, MSGPKD)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    IERTYP, IERCOD
      CHARACTER  MSGPKD*(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    ERTYP2, I, IER, IPLEN, ISUB, LAST, LEN2, LOC, M, MS,
     &           NLOC, NUM, PBEG
      CHARACTER  MSGTMP(255)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IFINIT, NFORMS
      CHARACTER  BLNK, DBB(3), FIND(4), FORMS(9), INREF(25), LPAR,
     &           NCHECK(3), PERCNT, RPAR
      SAVE       BLNK, DBB, FIND, FORMS, IFINIT, INREF, LPAR, NCHECK,
     &           NFORMS, PERCNT, RPAR
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  LEN,MIN0
      INTRINSIC  LEN, MIN0
      INTEGER    LEN, MIN0
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   C1TCI, E1INIT, E1PRT, E1UCS, M1VE, M1VECH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1DX
      INTEGER    I1DX
C
      DATA FORMS/'A', 'C', 'D', 'I', 'K', 'L', 'R', 'S', 'Z'/,
     &     NFORMS/9/
      DATA PERCNT/'%'/, LPAR/'('/, RPAR/')'/, BLNK/' '/
      DATA INREF/' ', 'i', 'n', ' ', 'r', 'e', 'f', 'e', 'r',
     &     'e', 'n', 'c', 'e', ' ', 't', 'o', ' ', 'k', 'e',
     &     'y', 'w', 'o', 'r', 'd', ' '/
      DATA NCHECK/'N', '1', '*'/, DBB/'.', ' ', ' '/
      DATA FIND/'*', ' ', ' ', '*'/
      DATA IFINIT/0/
C                                  INITIALIZE ERROR TABLE IF NECESSARY
      IF (IFINIT .EQ. 0) THEN
         CALL E1INIT
         IFINIT = 1
      END IF
C                                  CHECK AND SET ERROR TYPE IF NECESSARY
      IF (IERTYP .NE. -1) THEN
         ERTYPE(CALLVL) = IERTYP
      ELSE IF (IERTYP.LT.-1 .OR. IERTYP.GT.7) THEN
         MSGLEN = 51
         CALL M1VECH ('.  Error from E1MES.  Illegal error type'//
     &                ' specified. ', MSGLEN, MSGSAV, MSGLEN)
         CALL E1PRT
         STOP
      END IF
C
      ERTYP2 = ERTYPE(CALLVL)
C                                  SET ERROR CODE IF NECESSARY
      IF (IERCOD .GT. -1) ERCODE(CALLVL) = IERCOD
      LEN2 = LEN(MSGPKD)
C
      IF (IERTYP.EQ.0 .OR. IERCOD.EQ.0) THEN
C                                  REMOVE THE ERROR STATE
         MSGLEN = 0
      ELSE IF (LEN2.EQ.0 .OR. (LEN2.EQ.1.AND.MSGPKD(1:1).EQ.BLNK)) THEN
         IF (ERTYP2 .EQ. 6) IFERR6 = 1
         IF (ERTYP2 .EQ. 7) IFERR7 = 1
C                                  UPDATE CHECKSUM PARAMETER ERCKSM
         CALL E1UCS
C                                  PRINT MESSAGE IF NECESSARY
         IF (ERTYP2.GE.5 .AND. PRINTB(ERTYP2).EQ.1) CALL E1PRT
      ELSE
C                                  FILL UP MSGSAV WITH EXPANDED MESSAGE
         LEN2 = MIN0(LEN2,255)
         DO 10  I=1, LEN2
            MSGTMP(I) = MSGPKD(I:I)
   10    CONTINUE
         MS = 0
         M = 0
C                                  CHECK PLIST FOR KEYWORD NAME
         NLOC = I1DX(PLIST,PLEN,NCHECK,3)
         IF (NLOC.GT.0 .AND. HDRFMT(ERTYP2).EQ.3) THEN
C                                  M1VE INREF INTO MSGSAV
            CALL M1VE (INREF, 1, 25, 25, MSGSAV, 1, 25, 25, IER)
C                                  GET LENGTH OF KEYWORD NAME
            CALL C1TCI (PLIST(NLOC+3), 3, IPLEN, IER)
            PBEG = NLOC + 3 + IER
C                                  M1VE KEYWORD NAME INTO MSGSAV
            CALL M1VE (PLIST, PBEG, PBEG+IPLEN-1, PLEN, MSGSAV, 26,
     &                 IPLEN+25, 255, IER)
C                                  UPDATE POINTER
            MS = IPLEN + 25
         END IF
C                                  INSERT DOT, BLANK, BLANK
         CALL M1VE (DBB, 1, 3, 3, MSGSAV, MS+1, MS+3, 255, IER)
         MS = MS + 3
C                                  LOOK AT NEXT CHARACTER
   20    M = M + 1
         ISUB = 0
         IF (M .GT. LEN2-4) THEN
            LAST = LEN2 - M + 1
            DO 30  I=1, LAST
   30       MSGSAV(MS+I) = MSGTMP(M+I-1)
            MSGLEN = MS + LAST
            GO TO 40
         ELSE IF (MSGTMP(M).EQ.PERCNT .AND. MSGTMP(M+1).EQ.LPAR .AND.
     &           MSGTMP(M+4).EQ.RPAR) THEN
            CALL C1TCI (MSGTMP(M+3), 1, NUM, IER)
            IF (IER.EQ.0 .AND. NUM.NE.0 .AND. I1DX(FORMS,NFORMS,
     &          MSGTMP(M+2),1).NE.0) THEN
C                                  LOCATE THE ITEM IN THE PARAMETER LIST
               CALL M1VE (MSGTMP(M+2), 1, 2, 2, FIND, 2, 3, 4, IER)
               LOC = I1DX(PLIST,PLEN,FIND,4)
               IF (LOC .GT. 0) THEN
C                                  SET IPLEN = LENGTH OF STRING
                  CALL C1TCI (PLIST(LOC+4), 4, IPLEN, IER)
                  PBEG = LOC + 4 + IER
C                                  ADJUST IPLEN IF IT IS TOO BIG
                  IPLEN = MIN0(IPLEN,255-MS)
C                                  M1VE STRING FROM PLIST INTO MSGSAV
                  CALL M1VE (PLIST, PBEG, PBEG+IPLEN-1, PLEN, MSGSAV,
     &                       MS+1, MS+IPLEN, 255, IER)
                  IF (IER.GE.0 .AND. IER.LT.IPLEN) THEN
C                                  UPDATE POINTERS
                     M = M + 4
                     MS = MS + IPLEN - IER
C                                  BAIL OUT IF NO MORE ROOM
                     IF (MS .GE. 255) THEN
                        MSGLEN = 255
                        GO TO 40
                     END IF
C                                  SET FLAG TO SHOW SUBSTITION WAS MADE
                     ISUB = 1
                  END IF
               END IF
            END IF
         END IF
         IF (ISUB .EQ. 0) THEN
            MS = MS + 1
            MSGSAV(MS) = MSGTMP(M)
         END IF
         GO TO 20
   40    ERTYP2 = ERTYPE(CALLVL)
         IF (ERTYP2 .EQ. 6) IFERR6 = 1
         IF (ERTYP2 .EQ. 7) IFERR7 = 1
C                                  UPDATE CHECKSUM PARAMETER ERCKSM
         CALL E1UCS
C                                  PRINT MESSAGE IF NECESSARY
         IF (ERTYP2.GE.5 .AND. PRINTB(ERTYP2).EQ.1) CALL E1PRT
      END IF
C                                  CLEAR PARAMETER LIST
      PLEN = 1
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1POP
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 13, 1984
C
C  Purpose:    To pop a subroutine name from the error control stack.
C
C  Usage:      CALL E1POP(NAME)
C
C  Arguments:
C     NAME   - A character string of length six specifying the name
C              of the subroutine.  (Input)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1POP (NAME)
C                                  SPECIFICATIONS FOR ARGUMENTS
      CHARACTER  NAME*(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IERTYP, IR
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1PRT, E1PSH, E1STI, E1STL, I1KRL
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1KST
      INTEGER    I1KST
C
      IF (CALLVL .LE. 1) THEN
         CALL E1PSH ('E1POP ')
         CALL E1STL (1, NAME)
         CALL E1MES (5, 1, 'Error condition in E1POP.  Cannot pop '//
     &               'from %(L1) because stack is empty.')
         STOP
      ELSE IF (NAME .NE. RNAME(CALLVL)) THEN
         CALL E1STL (1, NAME)
         CALL E1STL (2, RNAME(CALLVL))
         CALL E1MES (5, 2, 'Error condition in E1POP.  %(L1) does '//
     &               'not match the name %(L2) in the stack.')
         STOP
      ELSE
         IERTYP = ERTYPE(CALLVL)
         IF (IERTYP .NE. 0) THEN
C                                  M1VE ERROR TYPE AND ERROR CODE TO
C                                    PREVIOUS LEVEL FOR ERROR TYPES 2-7
            IF (IERTYP.GE.2 .AND. IERTYP.LE.7) THEN
               ERTYPE(CALLVL-1) = ERTYPE(CALLVL)
               ERCODE(CALLVL-1) = ERCODE(CALLVL)
            END IF
C                                  CHECK PRINT TABLE TO DETERMINE
C                                    WHETHER TO PRINT STORED MESSAGE
            IF (IERTYP .LE. 4) THEN
               IF (ISUSER(CALLVL-1) .AND. PRINTB(IERTYP).EQ.1)
     &             CALL E1PRT
            ELSE
               IF (PRINTB(IERTYP) .EQ. 1) CALL E1PRT
            END IF
C                                  CHECK STOP TABLE AND ERROR TYPE TO
C                                    DETERMINE WHETHER TO STOP
            IF (IERTYP .LE. 4) THEN
               IF (ISUSER(CALLVL-1) .AND. STOPTB(IERTYP).EQ.1) THEN
                  STOP
               END IF
            ELSE IF (IERTYP .EQ. 5) THEN
               IF (STOPTB(IERTYP) .EQ. 1) THEN
                  STOP
               END IF
            ELSE IF (HDRFMT(IERTYP) .EQ. 1) THEN
               IF (ISUSER(CALLVL-1)) THEN
                  IF (N1RGB(0) .NE. 0) THEN
                     STOP
                  END IF
               END IF
            END IF
         END IF
C                                  SET ERROR TYPE AND CODE
         IF (CALLVL .LT. MAXLEV) THEN
            ERTYPE(CALLVL+1) = -1
            ERCODE(CALLVL+1) = -1
         END IF
C                                  SET IR = AMOUNT OF WORKSPACE
C                                  ALLOCATED AT THIS LEVEL
         IR = I1KST(1) - IALLOC(CALLVL-1)
         IF (IR .GT. 0) THEN
C                                  RELEASE WORKSPACE
            CALL I1KRL (IR)
            IALLOC(CALLVL) = 0
         ELSE IF (IR .LT. 0) THEN
            CALL E1STI (1, CALLVL)
            CALL E1STI (2, IALLOC(CALLVL-1))
            CALL E1STI (3, I1KST(1))
            CALL E1MES (5, 3, 'Error condition in E1POP. '//
     &                  ' The number of workspace allocations at '//
     &                  'level %(I1) is %(I2).  However, the total '//
     &                  'number of workspace allocations is %(I3).')
            STOP
         END IF
C                                  DECREASE THE STACK POINTER BY ONE
         CALLVL = CALLVL - 1
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1PRT
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 14, 1984
C
C  Purpose:    To print an error message.
C
C  Usage:      CALL E1PRT
C
C  Arguments:  None
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1PRT
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    ALL, I, IBEG, IBLOC, IBLOC2, IEND, IER, IHDR, J,
     &           LERTYP, LOC, LOCM1, LOCX, MAXLOC, MAXTMP, MLOC, MOD,
     &           NCBEG, NLOC, NOUT
      CHARACTER  MSGTMP(70), STRING(10)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      CHARACTER  ATLINE(9), BLANK(1), DBB(3), FROM(6), MSGTYP(8,7),
     &           PERSLA(2), QMARK, UNKNOW(8)
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                              SPECIFICATIONS FOR COMMON /ERCOM8/
      INTEGER    PROLVL, XXLINE(10), XXPLEN(10), ICALOC(10), INALOC(10)
      COMMON     /ERCOM8/ PROLVL, XXLINE, XXPLEN, ICALOC, INALOC
      SAVE       /ERCOM8/
C                              SPECIFICATIONS FOR COMMON /ERCOM9/
      CHARACTER  XXPROC(10)*31
      COMMON     /ERCOM9/ XXPROC
      SAVE       /ERCOM9/
      SAVE       ATLINE, BLANK, DBB, FROM, MSGTYP, PERSLA, QMARK,
     &           UNKNOW
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  MIN0
      INTRINSIC  MIN0
      INTEGER    MIN0
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   C1TIC, M1VE, UMACH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1DX, I1ERIF
      INTEGER    I1DX, I1ERIF
C
      DATA MSGTYP/'N', 'O', 'T', 'E', ' ', ' ', ' ', ' ', 'A',
     &     'L', 'E', 'R', 'T', ' ', ' ', ' ', 'W', 'A', 'R',
     &     'N', 'I', 'N', 'G', ' ', 'F', 'A', 'T', 'A', 'L',
     &     ' ', ' ', ' ', 'T', 'E', 'R', 'M', 'I', 'N', 'A',
     &     'L', 'W', 'A', 'R', 'N', 'I', 'N', 'G', ' ', 'F',
     &     'A', 'T', 'A', 'L', ' ', ' ', ' '/
      DATA UNKNOW/'U', 'N', 'K', 'N', 'O', 'W', 'N', ' '/
      DATA ATLINE/' ', 'a', 't', ' ', 'l', 'i', 'n', 'e', ' '/
      DATA BLANK/' '/, FROM/' ', 'f', 'r', 'o', 'm', ' '/
      DATA DBB/'.', ' ', ' '/, PERSLA/'%', '/'/
      DATA QMARK/'?'/
C
      IF (MSGLEN .LE. 0) RETURN
      CALL UMACH (2, NOUT)
      MAXTMP = 70
      MOD = 0
      LERTYP = ERTYPE(CALLVL)
      IHDR = HDRFMT(LERTYP)
      IF (IHDR .EQ. 3) THEN
         IF (XXPROC(PROLVL)(1:1).EQ.QMARK .AND. XXLINE(PROLVL).EQ.0)
     &       THEN
            IHDR = 1
         END IF
      END IF
      IEND = 0
      IF (IHDR.EQ.1 .AND. ERTYPE(CALLVL).LE.4) THEN
         MSGTMP(1) = BLANK(1)
         IEND = 1
C                                  CONVERT ERROR CODE INTO CHAR STRING
         CALL C1TIC (ERCODE(CALLVL), STRING, 10, IER)
C                                  LOCATE START OF NON-BLANK CHARACTERS
         IBEG = I1ERIF(STRING,10,BLANK,1)
C                                  M1VE IT TO MSGTMP
         CALL M1VE (STRING, IBEG, 10, 10, MSGTMP, IEND+1,
     &              IEND+11-IBEG, MAXTMP, IER)
         IEND = IEND + 11 - IBEG
      END IF
      IF (IHDR .NE. 2) THEN
         CALL M1VE (FROM, 1, 6, 6, MSGTMP, IEND+1, IEND+6, MAXTMP, IER)
         IEND = IEND + 6
      END IF
      IF (IHDR .EQ. 3) THEN
C                                  THIS IS A PROTRAN RUN TIME ERROR MSG.
C                                  RETRIEVE THE PROCEDURE NAME
         CALL M1VE (XXPROC(PROLVL), 1, XXPLEN(PROLVL), 31, MSGTMP,
     &              IEND+1, IEND+XXPLEN(PROLVL), MAXTMP, IER)
         MLOC = IEND + XXPLEN(PROLVL) + 1
         MSGTMP(MLOC) = BLANK(1)
         IEND = IEND + I1DX(MSGTMP(IEND+1),XXPLEN(PROLVL)+1,BLANK,1) -
     &          1
         IF (XXLINE(PROLVL) .GT. 0) THEN
C                                  INSERT ATLINE
            CALL M1VE (ATLINE, 1, 9, 9, MSGTMP, IEND+1, IEND+9,
     &                 MAXTMP, IER)
            IEND = IEND + 9
C                                  CONVERT PROTRAN GLOBAL LINE NUMBER
            CALL C1TIC (XXLINE(PROLVL), STRING, 10, IER)
C                                  LOCATE START OF NON-BLANK CHARACTERS
            IBEG = I1ERIF(STRING,10,BLANK,1)
C                                  M1VE GLOBAL LINE NUMBER TO MSGTMP
            CALL M1VE (STRING, IBEG, 10, 10, MSGTMP, IEND+1,
     &                 IEND+11-IBEG, MAXTMP, IER)
            IEND = IEND + 11 - IBEG
         END IF
      ELSE
C                                  THIS IS EITHER A LIBRARY ERROR MSG
C                                  OR A PROTRAN PREPROCESSOR ERROR MSG
         IF (IHDR .EQ. 1) THEN
C                                  THIS IS A LIBRARY ERROR MESSAGE.
C                                  RETRIEVE ROUTINE NAME
            CALL M1VE (RNAME(CALLVL), 1, 6, 6, MSGTMP, IEND+1, IEND+6,
     &                 MAXTMP, IER)
            MSGTMP(IEND+7) = BLANK(1)
            IEND = IEND + I1DX(MSGTMP(IEND+1),7,BLANK,1) - 1
         END IF
C                                  ADD DOT, BLANK, BLANK IF NEEDED
         IF (I1DX(MSGSAV,3,DBB,3) .NE. 1) THEN
            CALL M1VE (DBB, 1, 3, 3, MSGTMP, IEND+1, IEND+3, MAXTMP,
     &                 IER)
            IEND = IEND + 3
            MOD = 3
         END IF
      END IF
C                                  MSGTMP AND MSGSAV NOW CONTAIN THE
C                                   ERROR MESSAGE IN FINAL FORM.
      NCBEG = 59 - IEND - MOD
      ALL = 0
      IBLOC = I1DX(MSGSAV,MSGLEN,PERSLA,2)
      IF (IBLOC.NE.0 .AND. IBLOC.LT.NCBEG) THEN
         LOCM1 = IBLOC - 1
         LOC = IBLOC + 1
      ELSE IF (MSGLEN .LE. NCBEG) THEN
         LOCM1 = MSGLEN
         ALL = 1
      ELSE
         LOC = NCBEG
C                                  CHECK FOR APPROPRIATE PLACE TO SPLIT
   10    CONTINUE
         IF (MSGSAV(LOC) .NE. BLANK(1)) THEN
            LOC = LOC - 1
            IF (LOC .GT. 1) GO TO 10
            LOC = NCBEG + 1
         END IF
         LOCM1 = LOC - 1
      END IF
C                                  NO BLANKS FOUND IN FIRST NCBEG CHARS
      IF (LERTYP.GE.1 .AND. LERTYP.LE.7) THEN
         WRITE (NOUT,99995) (MSGTYP(I,LERTYP),I=1,8),
     &                     (MSGTMP(I),I=1,IEND), (MSGSAV(I),I=1,LOCM1)
      ELSE
         WRITE (NOUT,99995) (UNKNOW(I),I=1,8), (MSGTMP(I),I=1,IEND),
     &                     (MSGSAV(I),I=1,LOCM1)
      END IF
      IF (ALL .EQ. 0) THEN
C                                  PREPARE TO WRITE CONTINUATION OF
C                                    MESSAGE
C
C                                  FIND WHERE TO BREAK MESSAGE
C                                    LOC = NUMBER OF CHARACTERS OF
C                                          MESSAGE WRITTEN SO FAR
   20    LOCX = LOC + 64
         NLOC = LOC + 1
         IBLOC2 = IBLOC
         MAXLOC = MIN0(MSGLEN-LOC,64)
         IBLOC = I1DX(MSGSAV(NLOC),MAXLOC,PERSLA,2)
         IF (MSGSAV(NLOC).EQ.BLANK(1) .AND. IBLOC2.EQ.0) NLOC = NLOC +
     &       1
         IF (IBLOC .GT. 0) THEN
C                                  PAGE BREAK FOUND AT IBLOC
            LOCX = NLOC + IBLOC - 2
            WRITE (NOUT,99996) (MSGSAV(I),I=NLOC,LOCX)
            LOC = NLOC + IBLOC
            GO TO 20
C                                  DON'T BOTHER LOOKING FOR BLANK TO
C                                    BREAK AT IF LOCX .GE. MSGLEN
         ELSE IF (LOCX .LT. MSGLEN) THEN
C                                  CHECK FOR BLANK TO BREAK THE LINE
   30       CONTINUE
            IF (MSGSAV(LOCX) .EQ. BLANK(1)) THEN
C                                  BLANK FOUND AT LOCX
               WRITE (NOUT,99996) (MSGSAV(I),I=NLOC,LOCX)
               LOC = LOCX
               GO TO 20
            END IF
            LOCX = LOCX - 1
            IF (LOCX .GT. NLOC) GO TO 30
            LOCX = LOC + 64
C                                  NO BLANKS FOUND IN NEXT 64 CHARS
            WRITE (NOUT,99996) (MSGSAV(I),I=NLOC,LOCX)
            LOC = LOCX
            GO TO 20
         ELSE
C                                  ALL THE REST WILL FIT ON 1 LINE
            LOCX = MSGLEN
            WRITE (NOUT,99996) (MSGSAV(I),I=NLOC,LOCX)
         END IF
      END IF
C                                  SET LENGTH OF MSGSAV AND PLEN
C                                    TO SHOW THAT MESSAGE HAS
C                                    ALREADY BEEN PRINTED
 9000 MSGLEN = 0
      PLEN = 1
      IF (TRACON(LERTYP).EQ.1 .AND. CALLVL.GT.2) THEN
C                                  INITIATE TRACEBACK
         WRITE (NOUT,99997)
         DO 9005  J=CALLVL, 1, -1
            IF (J .GT. 1) THEN
               IF (ISUSER(J-1)) THEN
                  WRITE (NOUT,99998) RNAME(J), ERTYPE(J), ERCODE(J)
               ELSE
                  WRITE (NOUT,99999) RNAME(J), ERTYPE(J), ERCODE(J)
               END IF
            ELSE
               WRITE (NOUT,99998) RNAME(J), ERTYPE(J), ERCODE(J)
            END IF
 9005    CONTINUE
      END IF
C
      RETURN
99995 FORMAT (/, ' *** ', 8A1, ' ERROR', 59A1)
99996 FORMAT (' *** ', 9X, 64A1)
99997 FORMAT (14X, 'Here is a traceback of subprogram calls',
     &       ' in reverse order:', /, 14X, '      Routine    Error ',
     &       'type    Error code', /, 14X, '      -------    ',
     &       '----------    ----------')
99998 FORMAT (20X, A6, 5X, I6, 8X, I6)
99999 FORMAT (20X, A6, 5X, I6, 8X, I6, 4X, '(Called internally)')
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1PSH
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 2, 1984
C
C  Purpose:    To push a subroutine name onto the error control stack.
C
C  Usage:      CALL E1PSH(NAME)
C
C  Arguments:
C     NAME   - A character string of length six specifing the name of
C              the subroutine.  (Input)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1PSH (NAME)
C                                  SPECIFICATIONS FOR ARGUMENTS
      CHARACTER  NAME*(*)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IFINIT
      SAVE       IFINIT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1INIT, E1MES, E1STI
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1KST
      INTEGER    I1KST
C
      DATA IFINIT/0/
C                                  INITIALIZE ERROR TABLE IF NECESSARY
      IF (IFINIT .EQ. 0) THEN
         CALL E1INIT
         IFINIT = 1
      END IF
      IF (CALLVL .GE. MAXLEV) THEN
         CALL E1STI (1, MAXLEV)
         CALL E1MES (5, 1, 'Error condition in E1PSH.  Push would '//
     &               'cause stack level to exceed %(I1). ')
         STOP
      ELSE
C                                  STORE ALLOCATION LEVEL
         IALLOC(CALLVL) = I1KST(1)
C                                  INCREMENT THE STACK POINTER BY ONE
         CALLVL = CALLVL + 1
C                                  PUT SUBROUTINE NAME INTO STACK
         RNAME(CALLVL) = NAME
C                                  SET ERROR TYPE AND ERROR CODE
         ERTYPE(CALLVL) = 0
         ERCODE(CALLVL) = 0
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1STD
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 6, 1984
C
C  Purpose:    To store a real number for subsequent use within an error
C              message.
C
C  Usage:      CALL E1STD(ID, DVALUE)
C
C  Arguments:
C     ID     - Integer specifying the substitution index.  ID must be
C              between 1 and 9.  (Input)
C     DVALUE - The double precision number to be stored.  (Input)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1STD (ID, DVALUE)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    ID
      DOUBLE PRECISION DVALUE
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IBEG, ILEN
      CHARACTER  ARRAY(24), SAVE*24
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IFINIT
      CHARACTER  BLANK(1)
      SAVE       BLANK, IFINIT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1INIT, E1INPL
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1ERIF
      INTEGER    I1ERIF
C
      DATA BLANK/' '/, IFINIT/0/
C                                  INITIALIZE IF NECESSARY
      IF (IFINIT .EQ. 0) THEN
         CALL E1INIT
         IFINIT = 1
      END IF
      IF (DVALUE .EQ. 0.0D0) THEN
         WRITE (SAVE,'(D24.15)') DVALUE
      ELSE
         WRITE (SAVE,'(1PD24.15)') DVALUE
      END IF
      DO 40  I=1, 24
   40 ARRAY(I) = SAVE(I:I)
      IBEG = I1ERIF(ARRAY,24,BLANK,1)
      IF (ID.GE.1 .AND. ID.LE.9) THEN
         ILEN = 25 - IBEG
         CALL E1INPL ('D', ID, ILEN, ARRAY(IBEG))
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1STI
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 6, 1984
C
C  Purpose:    To store an integer for subsequent use within an error
C              message.
C
C  Usage:      CALL E1STI(II, IVALUE)
C
C  Arguments:
C     II     - Integer specifying the substitution index.  II must be
C              between 1 and 9.  (Input)
C     IVALUE - The integer to be stored.  (Input)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1STI (II, IVALUE)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    II, IVALUE
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IBEG, IER, ILEN
      CHARACTER  ARRAY(14)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IFINIT
      CHARACTER  BLANK(1)
      SAVE       BLANK, IFINIT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   C1TIC, E1INIT, E1INPL
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1ERIF
      INTEGER    I1ERIF
C
      DATA BLANK/' '/, IFINIT/0/
C                                  INITIALIZE IF NECESSARY
      IF (IFINIT .EQ. 0) THEN
         CALL E1INIT
         IFINIT = 1
      END IF
      CALL C1TIC (IVALUE, ARRAY, 14, IER)
      IBEG = I1ERIF(ARRAY,14,BLANK,1)
      IF (II.GE.1 .AND. II.LE.9 .AND. IER.EQ.0) THEN
         ILEN = 15 - IBEG
         CALL E1INPL ('I', II, ILEN, ARRAY(IBEG))
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1STL
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    November 8, 1985
C
C  Purpose:    To store a string for subsequent use within an error
C              message.
C
C  Usage:      CALL E1STL(IL,STRING)
C
C  Arguments:
C     IL     - Integer specifying the substitution index.  IL must be
C              between 1 and 9.  (Input)
C     STRING - A character string.  (Input)
C
C  Copyright:  1985 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1STL (IL, STRING)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    IL
      CHARACTER  STRING*(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, LEN2
      CHARACTER  STRGUP(255)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IFINIT
      SAVE       IFINIT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  IABS,LEN,MIN0
      INTRINSIC  IABS, LEN, MIN0
      INTEGER    IABS, LEN, MIN0
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1INIT, E1INPL
C
      DATA IFINIT/0/
C                                  INITIALIZE IF NECESSARY
      IF (IFINIT .EQ. 0) THEN
         CALL E1INIT
         IFINIT = 1
      END IF
      LEN2 = LEN(STRING)
      LEN2 = MIN0(LEN2,255)
      DO 10  I=1, LEN2
         STRGUP(I) = STRING(I:I)
   10 CONTINUE
      IF (IABS(IL).GE.1 .AND. IABS(IL).LE.9) THEN
         CALL E1INPL ('L', IL, LEN2, STRGUP)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1STR
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 2, 1984
C
C  Purpose:    To store a real number for subsequent use within an error
C              message.
C
C  Usage:      CALL E1STR(IR,RVALUE)
C
C  Arguments:
C     IR     - Integer specifying the substitution index.  IR must be
C              between 1 and 9.  (Input)
C     RVALUE - The real number to be stored.  (Input)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1STR (IR, RVALUE)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    IR
      REAL       RVALUE
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IBEG, ILEN
      CHARACTER  ARRAY(14), SAVE*14
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IFINIT
      CHARACTER  BLANK(1)
      SAVE       BLANK, IFINIT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1INIT, E1INPL
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1ERIF
      INTEGER    I1ERIF
C
      DATA BLANK/' '/, IFINIT/0/
C                                  INITIALIZE IF NECESSARY
      IF (IFINIT .EQ. 0) THEN
         CALL E1INIT
         IFINIT = 1
      END IF
      IF (RVALUE .EQ. 0.0) THEN
         WRITE (SAVE,'(E14.6)') RVALUE
      ELSE
         WRITE (SAVE,'(1PE14.6)') RVALUE
      END IF
      DO 40  I=1, 14
   40 ARRAY(I) = SAVE(I:I)
      IBEG = I1ERIF(ARRAY,14,BLANK,1)
      IF (IR.GE.1 .AND. IR.LE.9) THEN
         ILEN = 15 - IBEG
         CALL E1INPL ('R', IR, ILEN, ARRAY(IBEG))
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  E1UCS
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 8, 1984
C
C  Purpose:    To update the checksum number for error messages.
C
C  Usage:      CALL E1UCS
C
C  Arguments:  None
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE E1UCS
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IBEG, IBEG2, IEND, ILOC, IPOS, JLOC, NCODE, NLEN
      DOUBLE PRECISION DNUM
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      DOUBLE PRECISION DMAX
      CHARACTER  BLANK(1), COMMA(1), EQUAL(1), LPAR(1)
      SAVE       BLANK, COMMA, DMAX, EQUAL, LPAR
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  DMOD
cx    INTRINSIC  DMOD
      DOUBLE PRECISION DMOD
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   S1ANUM
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   ICASE, I1X
      INTEGER    ICASE, I1X
C
      DATA BLANK(1)/' '/, COMMA(1)/','/, LPAR(1)/'('/
      DATA EQUAL(1)/'='/, DMAX/1.0D+9/
C
      IF (MSGLEN .GT. 1) THEN
         IPOS = 0
         IBEG2 = 1
   10    IBEG = IBEG2
         IEND = MSGLEN
C                                  LOOK FOR BLANK, COMMA, LEFT PAREN.,
C                                  OR EQUAL SIGN
         ILOC = I1X(MSGSAV(IBEG),IEND-IBEG+1,BLANK,1)
         JLOC = I1X(MSGSAV(IBEG),IEND-IBEG+1,COMMA,1)
         IF (ILOC.EQ.0 .OR. (JLOC.GT.0.AND.JLOC.LT.ILOC)) ILOC = JLOC
         JLOC = I1X(MSGSAV(IBEG),IEND-IBEG+1,LPAR,1)
         IF (ILOC.EQ.0 .OR. (JLOC.GT.0.AND.JLOC.LT.ILOC)) ILOC = JLOC
         JLOC = I1X(MSGSAV(IBEG),IEND-IBEG+1,EQUAL,1)
         IF (ILOC.EQ.0 .OR. (JLOC.GT.0.AND.JLOC.LT.ILOC)) ILOC = JLOC
         IF (ILOC .GE. 1) THEN
            CALL S1ANUM (MSGSAV(IBEG+ILOC), IEND-IBEG-ILOC+1, NCODE,
     &                   NLEN)
            IF (NCODE.EQ.2 .OR. NCODE.EQ.3) THEN
C                                  FLOATING POINT NUMBER FOUND.
C                                  SET POINTERS TO SKIP OVER IT
               IBEG2 = IBEG + ILOC + NLEN
               IF (IBEG2 .LE. MSGLEN) THEN
                  CALL S1ANUM (MSGSAV(IBEG2), IEND-IBEG2+1, NCODE,
     &                         NLEN)
                  IF ((MSGSAV(IBEG2).EQ.'+'.OR.MSGSAV(IBEG2).EQ.
     &                '-') .AND. NCODE.EQ.1) THEN
C                                  INTEGER IMMEDIATELY FOLLOWS A REAL AS
C                                  WITH SOME CDC NOS. LIKE 1.2345678+123
C                                  SET POINTERS TO SKIP OVER IT
                     IBEG2 = IBEG2 + NLEN
                  END IF
               END IF
            ELSE
               IBEG2 = IBEG + ILOC
            END IF
            IEND = IBEG + ILOC - 1
         END IF
C                                  UPDATE CKSUM USING PART OF MESSAGE
         DO 20  I=IBEG, IEND
            IPOS = IPOS + 1
            DNUM = ICASE(MSGSAV(I))
            ERCKSM = DMOD(ERCKSM+DNUM*IPOS,DMAX)
   20    CONTINUE
C                                  GO BACK FOR MORE IF NEEDED
         IF (IEND.LT.MSGLEN .AND. IBEG2.LT.MSGLEN) GO TO 10
C                                  UPDATE CKSUM USING ERROR TYPE
         DNUM = ERTYPE(CALLVL)
         ERCKSM = DMOD(ERCKSM+DNUM*(IPOS+1),DMAX)
C                                  UPDATE CKSUM USING ERROR CODE
         DNUM = ERCODE(CALLVL)
         ERCKSM = DMOD(ERCKSM+DNUM*(IPOS+2),DMAX)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  ERFC (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the complementary error function.
C
C  Usage:      ERFC(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     ERFC   - Function value.  (Output)
C
C  Remark:
C     Informational error:
C     Type Code
C       2   1  The function underflows because X is too large.
C
C  GAMS:       C8a
C
C  Chapter:    SFUN/LIBRARY Error Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION ERFC (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      REAL       ETA, TEMP, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NTERC2, NTERF, NTERFC
      REAL       ERC2CS(23), ERFCCS(24), ERFCS(13), SQEPS, SQRTPI,
     &           XMAX, XSML
      SAVE       ERC2CS, ERFCCS, ERFCS, NTERC2, NTERF, NTERFC, SQEPS,
     &           SQRTPI, XMAX, XSML
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,ALOG,EXP,SQRT
      INTRINSIC  ABS, ALOG, EXP, SQRT
      REAL       ABS, ALOG, EXP, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, CSEVL, INITS
      INTEGER    INITS
      REAL       AMACH, CSEVL
C
C                                  SERIES FOR ERF ON THE INTERVAL
C                                  0.0  TO  1.00000E+00
C                                  WITH WEIGHTED ERROR        7.10E-18
C                                  LOG WEIGHTED ERROR        17.15
C                                  SIGNIFICANT FIGURES REQD. 16.31
C                                  DECIMAL PLACES REQUIRED   17.71
C
      DATA ERFCS(1)/-.049046121234691808E0/
      DATA ERFCS(2)/-.14226120510371364E0/
      DATA ERFCS(3)/.010035582187599796E0/
      DATA ERFCS(4)/-.000576876469976748E0/
      DATA ERFCS(5)/.000027419931252196E0/
      DATA ERFCS(6)/-.000001104317550734E0/
      DATA ERFCS(7)/.00000003848875542E0/
      DATA ERFCS(8)/-.000000001180858253E0/
      DATA ERFCS(9)/.000000000032334215E0/
      DATA ERFCS(10)/-.000000000000799101E0/
      DATA ERFCS(11)/.00000000000001799E0/
      DATA ERFCS(12)/-.000000000000000371E0/
      DATA ERFCS(13)/.000000000000000007E0/
C
C                                  SERIES FOR ERC2 ON THE INTERVAL
C                                  2.50000E-01 TO  1.00000E+00
C                                  WITH WEIGHTED ERROR        5.22E-17
C                                  LOG WEIGHTED ERROR        16.28
C                                  APPROX SIGNIFICANT FIGURES
C                                  REQUIRED                  15.0
C                                  DECIMAL PLACES REQUIRED   16.96
C
      DATA ERC2CS(1)/-.069601346602309501E0/
      DATA ERC2CS(2)/-.041101339362620893E0/
      DATA ERC2CS(3)/.003914495866689626E0/
      DATA ERC2CS(4)/-.000490639565054897E0/
      DATA ERC2CS(5)/.00007157479001377E0/
      DATA ERC2CS(6)/-.000011530716341312E0/
      DATA ERC2CS(7)/.000001994670590201E0/
      DATA ERC2CS(8)/-.000000364266647159E0/
      DATA ERC2CS(9)/.0000000694437261E0/
      DATA ERC2CS(10)/-.000000013712209021E0/
      DATA ERC2CS(11)/.000000002788389661E0/
      DATA ERC2CS(12)/-.000000000581416472E0/
      DATA ERC2CS(13)/.000000000123892049E0/
      DATA ERC2CS(14)/-.000000000026906391E0/
      DATA ERC2CS(15)/.000000000005942614E0/
      DATA ERC2CS(16)/-.000000000001332386E0/
      DATA ERC2CS(17)/.000000000000302804E0/
      DATA ERC2CS(18)/-.000000000000069666E0/
      DATA ERC2CS(19)/.000000000000016208E0/
      DATA ERC2CS(20)/-.000000000000003809E0/
      DATA ERC2CS(21)/.000000000000000904E0/
      DATA ERC2CS(22)/-.000000000000000216E0/
      DATA ERC2CS(23)/.000000000000000052E0/
C
C                                  SERIES FOR ERFC ON THE INTERVAL
C                                  0.0  TO  2.50000E-01
C                                  WITH WEIGHTED ERROR        4.81E-17
C                                  LOG WEIGHTED ERROR        16.32
C                                  APPROX SIGNIFICANT FIGURES
C                                  REQUIRED                  15.0
C                                  DECIMAL PLACES REQUIRED   17.01
C
      DATA ERFCCS(1)/.0715179310202925E0/
      DATA ERFCCS(2)/-.026532434337606719E0/
      DATA ERFCCS(3)/.001711153977920853E0/
      DATA ERFCCS(4)/-.000163751663458512E0/
      DATA ERFCCS(5)/.000019871293500549E0/
      DATA ERFCCS(6)/-.000002843712412769E0/
      DATA ERFCCS(7)/.000000460616130901E0/
      DATA ERFCCS(8)/-.000000082277530261E0/
      DATA ERFCCS(9)/.000000015921418724E0/
      DATA ERFCCS(10)/-.000000003295071356E0/
      DATA ERFCCS(11)/.000000000722343973E0/
      DATA ERFCCS(12)/-.000000000166485584E0/
      DATA ERFCCS(13)/.000000000040103931E0/
      DATA ERFCCS(14)/-.000000000010048164E0/
      DATA ERFCCS(15)/.000000000002608272E0/
      DATA ERFCCS(16)/-.000000000000699105E0/
      DATA ERFCCS(17)/.000000000000192946E0/
      DATA ERFCCS(18)/-.000000000000054704E0/
      DATA ERFCCS(19)/.000000000000015901E0/
      DATA ERFCCS(20)/-.000000000000004729E0/
      DATA ERFCCS(21)/.000000000000001432E0/
      DATA ERFCCS(22)/-.000000000000000439E0/
      DATA ERFCCS(23)/.000000000000000138E0/
      DATA ERFCCS(24)/-.000000000000000048E0/
C
      DATA SQRTPI/1.772453850905516E0/
      DATA NTERF/0/, NTERFC/0/, NTERC2/0/, XSML/0.0/, XMAX/0.0/,
     &     SQEPS/0.0/
C
      CALL E1PSH ('ERFC  ')
      ERFC = AMACH(6)
C
      IF (NTERF .EQ. 0) THEN
         ETA = 0.1*AMACH(3)
         NTERF = INITS(ERFCS,13,ETA)
         NTERFC = INITS(ERFCCS,24,ETA)
         NTERC2 = INITS(ERC2CS,23,ETA)
C
         XSML = -SQRT(-ALOG(SQRTPI*AMACH(3)))
         XMAX = SQRT(-ALOG(SQRTPI*AMACH(1)))
         XMAX = XMAX - 0.5*ALOG(XMAX)/XMAX - 0.01
         SQEPS = SQRT(2.0*AMACH(3))
      END IF
C                                  ERFC(X) = 1.0 - ERF(X) FOR
C                                  X .LT. XSML
      IF (X .LE. XSML) THEN
         ERFC = 2.0
C
      ELSE IF (X .LE. XMAX) THEN
         Y = ABS(X)
C                                  ERFC(X) = 1.0 - ERF(X) FOR
C                                  -1. .LE. X .LE. 1.
         IF (Y .LE. 1.0) THEN
            IF (Y .LT. SQEPS) THEN
               ERFC = 1.0 - 2.0*X/SQRTPI
            ELSE
               TEMP = CSEVL(2.0*X*X-1.0,ERFCS,NTERF)
               ERFC = 1.0 - X*(1.0+TEMP)
            END IF
C                                  ERFC(X) = 1.0 - ERF(X) FOR
C                                  1.0 .LT. ABS(X) .LE. XMAX
         ELSE
            Y = Y*Y
            IF (Y .LE. 4.0) THEN
               TEMP = CSEVL((8.0/Y-5.0)/3.0,ERC2CS,NTERC2)
               ERFC = EXP(-Y)/ABS(X)*(0.5+TEMP)
            ELSE
               TEMP = CSEVL(8.0/Y-1.0,ERFCCS,NTERFC)
               ERFC = EXP(-Y)/ABS(X)*(0.5+TEMP)
            END IF
            IF (X .LT. 0.0) ERFC = 2.0 - ERFC
         END IF
C
      ELSE
         CALL E1STR (1, X)
         CALL E1STR (2, XMAX)
         CALL E1MES (2, 1, 'The function underflows because '//
     &               'X = %(R1) is greater than %(R2). The result is '//
     &               'set to zero.')
         ERFC = 0.0
      END IF
C
      CALL E1POP ('ERFC  ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  GAMDF/DGAMDF (Single/Double precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the gamma distribution function.
C
C  Usage:      GAMDF(X, A)
C
C  Arguments:
C     X      - Argument for which the gamma distribution function is to
C              be evaluated.  (Input)
C     A      - The shape parameter of the gamma distribution.  (Input)
C              This parameter must be positive.
C     GAMDF  - Function value, the probability that a gamma random
C              variable takes a value less than or equal to X.  (Output)
C
C  Remark:
C     Informational error
C     Type Code
C       1   1  The input argument, X, is less than zero.
C
C  Keywords:   P-value; Probability integral; Erlang distribution
C
C  GAMS:       L5a1g; C7e
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION GAMDF (X, A)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X, A
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I
      REAL       AX, BIG, CNT, CUT, D1, D2, P, PNLG, RATIO, REDUC,
     &           V(6), V1(6), XMIN, Y, YCNT, Z
C                                  SPECIFICATIONS FOR EQUIVALENCE
      EQUIVALENCE (V(3), V1(1))
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,ALOG,EXP
      INTRINSIC  ABS, ALOG, EXP
      REAL       ABS, ALOG, EXP
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, ALNGAM
      REAL       AMACH, ALNGAM
C
      CALL E1PSH ('GAMDF ')
      GAMDF = AMACH(6)
C                                  Check X
      IF (X .LT. 0.0E0) THEN
         CALL E1STR (1, X)
         CALL E1MES (1, 1, 'Since X = %(R1) is less than zero, '//
     &               'the distribution function is zero at X. ')
         GAMDF = 0.0
         GO TO 9000
      END IF
C                                  Check A
      IF (A .LE. 0.0E0) THEN
         CALL E1STR (1, A)
         CALL E1MES (5, 2, 'The shape parameter of the gamma '//
     &               'distribution must be positive.')
         GO TO 9000
      END IF
C
      IF (ALOG(X) .GE. 0.5*ALOG(AMACH(2))) THEN
         IF (A .GE. 0.5*X) THEN
            CALL E1STR (1, X)
            CALL E1STR (2, A)
            CALL E1MES (5, 3, 'Since X = %(R1) and A = %(R2) are '//
     &                  'so large, the algorithm would overflow. ')
            GO TO 9000
         ELSE
            GAMDF = 1.0
            GO TO 9000
         END IF
      END IF
C
      XMIN = ALOG(AMACH(1)) + AMACH(4)
      IF (X .EQ. 0.0E0) THEN
         P = 0.0E0
      ELSE
C                                  Define LOG-GAMMA and initialize
         PNLG = ALNGAM(A)
         CNT = A*ALOG(X)
         YCNT = X + PNLG
         IF ((CNT-YCNT) .LE. XMIN) THEN
            AX = 0.0E0
         ELSE
            AX = EXP(CNT-YCNT)
         END IF
         BIG = 1.0E35
         CUT = 1.0E-8
C                                  Choose algorithmic method
         IF ((X.GT.1.0E0) .AND. (X.GE.A)) THEN
C                                  Continued fraction expansion
            Y = 1.0E0 - A
            Z = X + Y + 1.0E0
            CNT = 0.0E0
            V(1) = 1.0E0
            V(2) = X
            V(3) = X + 1.0E0
            V(4) = Z*X
            P = V(3)/V(4)
   10       CNT = CNT + 1.0E0
            Y = Y + 1.0E0
            Z = Z + 2.0E0
            YCNT = Y*CNT
            V(5) = V1(1)*Z - V(1)*YCNT
            V(6) = V1(2)*Z - V(2)*YCNT
            IF (V(6) .EQ. 0.0E0) THEN
               DO 20  I=1, 4
                  V(I) = V1(I)
   20          CONTINUE
               IF (ABS(V(5)).LT.BIG .AND. ABS(V(6)).LT.BIG) GO TO 10
C                                  Scale terms down to prevent overflow
               DO 30  I=1, 4
                  V(I) = V(I)/BIG
   30          CONTINUE
               GO TO 10
            END IF
            RATIO = V(5)/V(6)
            REDUC = ABS(P-RATIO)
            IF (REDUC.LE.RATIO*CUT .AND. REDUC.LE.CUT) THEN
               P = 1.0E0 - P*AX
            ELSE
               P = RATIO
               DO 40  I=1, 4
                  V(I) = V1(I)
   40          CONTINUE
               IF (ABS(V(5)).LT.BIG .AND. ABS(V(6)).LT.BIG) GO TO 10
C                                  Scale terms down to prevent overflow
               DO 50  I=1, 4
                  V(I) = V(I)/BIG
   50          CONTINUE
               GO TO 10
            END IF
         ELSE
C                                  Series expansion
            RATIO = A
            CNT = 1.0E0
            P = 1.0E0
   60       RATIO = RATIO + 1.0E0
            CNT = CNT*X/RATIO
            P = P + CNT
            IF (CNT .GT. CUT) GO TO 60
            P = P*AX/A
         END IF
      END IF
C
      GAMDF = P
 9000 CALL E1POP ('GAMDF ')
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  GAMMA/DGAMMA (Single/Double precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    June 23, 1986
C
C  Purpose:    Evaluate the complete gamma function.
C
C  Usage:      GAMMA(X)
C
C  Arguments:
C     X      - Argument for which the complete gamma function is
C              desired.  (Input)
C     GAMMA  - Function value.  (Output)
C
C  Remark:
C     Informational errors
C     Type Code
C       2   1  The function underflows because X is too small.
C       3   2  Result is accurate to less than one half precision
C              because X is too near a negative integer.
C
C  GAMS:       C7a
C
C  Chapters:   SFUN/LIBRARY Gamma Function and Related Functions
C              STAT/LIBRARY Mathematical Support
C              MATH/LIBRARY Utilities
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION GAMMA (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, N
      REAL       SINPIY, XI, XN, Y
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NGAMCS
      REAL       DXREL, GAMCS(42), PI, SQ2PIL, XMAX, XMIN, XSML
      SAVE       DXREL, GAMCS, NGAMCS, PI, SQ2PIL, XMAX, XMIN, XSML
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,AINT,ALOG,AMAX1,EXP,SIN,SQRT
      INTRINSIC  ABS, AINT, ALOG, AMAX1, EXP, SIN, SQRT
      REAL       ABS, AINT, ALOG, AMAX1, EXP, SIN, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR, R9GAML
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, CSEVL, INITS, R9LGMC
      INTEGER    INITS
      REAL       AMACH, CSEVL, R9LGMC
C
C                                  SERIES FOR GAMMA ON THE INTERVAL
C                                  0.0 TO 1.00000D+00
C                                  WITH WEIGHTED ERROR         5.79D-32
C                                  LOG WEIGHTED ERROR         31.24
C                                  SIGNIFICANT FIGURES REQD.  30.00
C                                  DECIMAL PLACES REQUIRED    32.05
C
      DATA GAMCS(1)/.857119559098933142192006239994D-2/
      DATA GAMCS(2)/.441538132484100675719131577165D-2/
      DATA GAMCS(3)/.568504368159936337863266458879D-1/
      DATA GAMCS(4)/-.421983539641856050101250018662D-2/
      DATA GAMCS(5)/.132680818121246022058400679635D-2/
      DATA GAMCS(6)/-.189302452979888043252394702389D-3/
      DATA GAMCS(7)/.360692532744124525657808221723D-4/
      DATA GAMCS(8)/-.605676190446086421848554829037D-5/
      DATA GAMCS(9)/.105582954630228334473182350909D-5/
      DATA GAMCS(10)/-.181196736554238404829185589117D-6/
      DATA GAMCS(11)/.311772496471532227779025459317D-7/
      DATA GAMCS(12)/-.535421963901968714087408102435D-8/
      DATA GAMCS(13)/.919327551985958894688778682594D-9/
      DATA GAMCS(14)/-.157794128028833976176742327395D-9/
      DATA GAMCS(15)/.270798062293495454326654043309D-10/
      DATA GAMCS(16)/-.464681865382573014408166105893D-11/
      DATA GAMCS(17)/.797335019200741965646076717536D-12/
      DATA GAMCS(18)/-.136807820983091602579949917231D-12/
      DATA GAMCS(19)/.234731948656380065723347177169D-13/
      DATA GAMCS(20)/-.40274326149490669327665705347D-14/
      DATA GAMCS(21)/.691005174737210091213833697526D-15/
      DATA GAMCS(22)/-.118558450022199290705238712619D-15/
      DATA GAMCS(23)/.203414854249637395520102605193D-16/
      DATA GAMCS(24)/-.349005434171740584927401294911D-17/
      DATA GAMCS(25)/.598799385648530556713505106603D-18/
      DATA GAMCS(26)/-.102737805787222807449006977843D-18/
      DATA GAMCS(27)/.176270281606052982494275966075D-19/
      DATA GAMCS(28)/-.302432065373530626095877211204D-20/
      DATA GAMCS(29)/.518891466021839783971783355051D-21/
      DATA GAMCS(30)/-.890277084245657669244925160107D-22/
      DATA GAMCS(31)/.152747406849334260227459689131D-22/
      DATA GAMCS(32)/-.26207312561873629002573283328D-23/
      DATA GAMCS(33)/.449646404783053867033104657067D-24/
      DATA GAMCS(34)/-.771471273133687791170390152533D-25/
      DATA GAMCS(35)/.132363545312604403648657271467D-25/
      DATA GAMCS(36)/-.227099941294292881670231381333D-26/
      DATA GAMCS(37)/.389641899800399144932081664D-27/
      DATA GAMCS(38)/-.6685198115125953327792128D-28/
      DATA GAMCS(39)/.114699866314002438434761386667D-28/
      DATA GAMCS(40)/-.1967938586345134677295104D-29/
      DATA GAMCS(41)/.337644881658533809033489066667D-30/
      DATA GAMCS(42)/-.579307033578213578462549333333D-31/
C
      DATA PI/3.14159265358979323846264338328D0/
C                                  SQ2PIL IS 0.5*ALOG(2*PI) =
C                                  ALOG(SQRT(2*PI))
      DATA SQ2PIL/0.918938533204672741780329736406D0/
      DATA NGAMCS/0/, XMIN/0.0/, XMAX/0.0/, DXREL/0.0/, XSML/0.0/
C
      CALL E1PSH ('GAMMA ')
      GAMMA = AMACH(6)
C
      IF (NGAMCS .EQ. 0) THEN
C                                  INITIALIZE. FIND LEGAL BOUNDS FOR X,
C                                  AND DETERMINE THE NUMBER OF TERMS IN
C                                  THE SERIES REQUIRED TO ATTAIN AN
C                                  ACCURACY TEN TIMES BETTER THAN
C                                  MACHINE PRECISION.
         NGAMCS = INITS(GAMCS,23,0.1*AMACH(3))
         CALL R9GAML (XMIN, XMAX)
         DXREL = SQRT(AMACH(4))
         XSML = EXP(AMAX1(ALOG(AMACH(1)),-ALOG(AMACH(2)))+0.01)
      END IF
C                                  START EVALUATING GAMMA(X)
      Y = ABS(X)
C
      IF (Y .GT. 10.0) GO TO 40
C                                  COMPUTE GAMMA(X) FOR ABS(X).LE.10.0.
C                                  REDUCE INTERVAL AND FIND GAMMA(1+Y)
C                                  FOR 0.0 .LE. Y .LT. 1.0 FIRST OF ALL.
      N = X
      IF (X .LT. 0.0) N = N - 1
      XN = N
      Y = X - XN
      N = N - 1
      GAMMA = 0.9375 + CSEVL(2.0*Y-1.0,GAMCS,NGAMCS)
      IF (N .EQ. 0) GO TO 9000
C
      IF (N .GT. 0) GO TO 20
C                                  COMPUTE GAMMA(X) FOR X .LT. 1.
      N = -N
C
      IF (X .EQ. 0.0) THEN
         CALL E1MES (5, 5, 'The argument for the function can '//
     &               'not be zero.')
         GAMMA = AMACH(6)
         GO TO 9000
      END IF
C
C                                  PREVENT UNDERFLOW IN COMPARISON
C                                  ON CDC
      IF (1.0E20*Y .LT. 1.0E20*XSML) THEN
         CALL E1STR (1, X)
         CALL E1MES (5, 4, 'The function overflows because '//
     &               'X = %(R1) is too close to zero.')
         GAMMA = AMACH(6)
         GO TO 9000
      END IF
C
      XN = N - 2
      IF (X.LT.0.0 .AND. X+XN.EQ.0.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (5, 6, 'The argument for the function can '//
     &               'not be a negative integer. Argument X = %(R1).')
         GAMMA = AMACH(6)
         GO TO 9000
      END IF
C
      IF (X.LT.-0.5 .AND. ABS((X-AINT(X-0.5))/X).LT.DXREL) THEN
         CALL E1STR (1, X)
         CALL E1MES (3, 2, 'The result is accurate to less than '//
     &               'one half precision because X = %(R1) is too '//
     &               'close to a negative integer.')
      END IF
C
      XI = 0.0
      DO 10  I=1, N
         GAMMA = GAMMA/(X+XI)
         XI = XI + 1.0
   10 CONTINUE
      GO TO 9000
C                                  GAMMA(X) FOR X .GE. 2.0
   20 XI = 1.0
      DO 30  I=1, N
         GAMMA = (Y+XI)*GAMMA
         XI = XI + 1.0
   30 CONTINUE
      GO TO 9000
C                                  GAMMA(X) FOR ABS(X) .GT. 10.0.
C                                  RECALL Y = ABS(X).
   40 IF (X .GT. XMAX) THEN
         CALL E1STR (1, X)
         CALL E1STR (2, XMAX)
         CALL E1MES (5, 4, 'The function overflows because '//
     &               'X = %(R1) is greater than %(R2).')
         GAMMA = AMACH(6)
         GO TO 9000
      END IF
C
      GAMMA = 0.0
      IF (X .LT. XMIN) THEN
         CALL E1STR (1, X)
         CALL E1STR (2, XMIN)
         CALL E1MES (2, 1, 'The function underflows because '//
     &               'X = %(R1) is less than %(R2). The result is '//
     &               'set to zero.')
         GO TO 9000
      END IF
C
      GAMMA = EXP((Y-0.5)*ALOG(Y)-Y+SQ2PIL+R9LGMC(Y))
      IF (X .GT. 0.0) GO TO 9000
C
      IF (ABS((X-AINT(X-0.5))/X) .LT. DXREL) THEN
         CALL E1STR (1, X)
         CALL E1MES (3, 2, 'The result is accurate to less than '//
     &               'one half precision because X = %(R1) is too '//
     &               'close to a negative integer.')
      END IF
C
      SINPIY = SIN(PI*Y)
      IF (SINPIY .EQ. 0.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (5, 7, 'The argument for the function can '//
     &               'not be a negative integer. Argument X = %(R1).')
         GAMMA = AMACH(6)
         GO TO 9000
      END IF
C
      GAMMA = -PI/(Y*SINPIY*GAMMA)
C
 9000 CALL E1POP ('GAMMA ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  I1CSTR (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    September 10, 1985
C
C  Purpose:    Case insensitive comparison of two character arrays.
C
C  Usage:      I1CSTR(STR1, LEN1, STR2, LEN2)
C
C  Arguments:
C     STR1   - First character array.  (Input)
C     LEN1   - Length of STR1.  (Input)
C     STR2   - Second character array.  (Input)
C     LEN2   - Length of STR2.  (Input)
C     I1CSTR - Integer function.  (Output) Where
C              I1CSTR = -1  if STR1 .LT. STR2,
C              I1CSTR =  0  if STR1 .EQ. STR2,
C              I1CSTR =  1  if STR1 .GT. STR2.
C
C  Remarks:
C  1. If the two arrays, STR1 and STR2,  are of unequal length, the
C     shorter array is considered as if it were extended with blanks
C     to the length of the longer array.
C
C  2. If one or both lengths are zero or negative the I1CSTR output is
C     based on comparison of the lengths.
C
C  GAMS:       N5c
C
C  Chapter:    MATH/LIBRARY Utilities
C
C  Copyright:  1985 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION I1CSTR (STR1, LEN1, STR2, LEN2)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    LEN1, LEN2
      CHARACTER  STR1(LEN1), STR2(LEN2)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IC1, IC2, ICB, IS, L, LENM
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ISIGN,MIN0
      INTRINSIC  ISIGN, MIN0
      INTEGER    ISIGN, MIN0
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   ICASE
      INTEGER    ICASE
C
      IF (LEN1.GT.0 .AND. LEN2.GT.0) THEN
C                                  COMPARE FIRST LENM CHARACTERS
         LENM = MIN0(LEN1,LEN2)
         DO 10  L=1, LENM
            IC1 = ICASE(STR1(L))
            IC2 = ICASE(STR2(L))
            IF (IC1 .NE. IC2) THEN
               I1CSTR = ISIGN(1,IC1-IC2)
               RETURN
            END IF
   10    CONTINUE
      END IF
C                                  COMPARISON BASED ON LENGTH OR
C                                  TRAILING BLANKS
      IS = LEN1 - LEN2
      IF (IS .EQ. 0) THEN
         I1CSTR = 0
      ELSE
         IF (LEN1.LE.0 .OR. LEN2.LE.0) THEN
C                                  COMPARISON BASED ON LENGTH
            I1CSTR = ISIGN(1,IS)
         ELSE
C                                  COMPARISON BASED ON TRAILING BLANKS
C                                  TO EXTEND SHORTER ARRAY
            LENM = LENM + 1
            ICB = ICASE(' ')
            IF (IS .GT. 0) THEN
C                                  EXTEND STR2 WITH BLANKS
               DO 20  L=LENM, LEN1
                  IC1 = ICASE(STR1(L))
                  IF (IC1 .NE. ICB) THEN
                     I1CSTR = ISIGN(1,IC1-ICB)
                     RETURN
                  END IF
   20          CONTINUE
            ELSE
C                                  EXTEND STR1 WITH BLANKS
               DO 30  L=LENM, LEN2
                  IC2 = ICASE(STR2(L))
                  IF (ICB .NE. IC2) THEN
                     I1CSTR = ISIGN(1,ICB-IC2)
                     RETURN
                  END IF
   30          CONTINUE
            END IF
C
            I1CSTR = 0
         END IF
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  I1DX (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    September 9, 1985
C
C  Purpose:    Determine the array subscript indicating the starting
C              element at which a key character sequence begins.
C              (Case-insensitive version)
C
C  Usage:      I1DX(CHRSTR, I1LEN, KEY, KLEN)
C
C  Arguments:
C     CHRSTR - Character array to be searched.  (Input)
C     I1LEN  - Length of CHRSTR.  (Input)
C     KEY    - Character array that contains the key sequence.  (Input)
C     KLEN   - Length of KEY.  (Input)
C     I1DX   - Integer function.  (Output)
C
C  Remarks:
C  1. Returns zero when there is no match.
C
C  2. Returns zero if KLEN is longer than ISLEN.
C
C  3. Returns zero when any of the character arrays has a negative or
C     zero length.
C
C  GAMS:       N5c
C
C  Chapter:    MATH/LIBRARY Utilities
C
C  Copyright:  1985 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION I1DX (CHRSTR, I1LEN, KEY, KLEN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    I1LEN, KLEN
      CHARACTER  CHRSTR(*), KEY(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, II, J
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   ICASE, I1CSTR
      INTEGER    ICASE, I1CSTR
C
      I1DX = 0
      IF (KLEN.LE.0 .OR. I1LEN.LE.0) GO TO 9000
      IF (KLEN .GT. I1LEN) GO TO 9000
C
      I = 1
      II = I1LEN - KLEN + 1
   10 IF (I .LE. II) THEN
         IF (ICASE(CHRSTR(I)) .EQ. ICASE(KEY(1))) THEN
            IF (KLEN .NE. 1) THEN
               J = KLEN - 1
               IF (I1CSTR(CHRSTR(I+1),J,KEY(2),J) .EQ. 0) THEN
                  I1DX = I
                  GO TO 9000
               END IF
            ELSE
               I1DX = I
               GO TO 9000
            END IF
         END IF
         I = I + 1
         GO TO 10
      END IF
C
 9000 RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  I1ERIF
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 13, 1984
C
C  Purpose:    Return the position of the first element of a given
C              character array which is not an element of another
C              character array.
C
C  Usage:      I1ERIF(STR1, LEN1, STR2, LEN2)
C
C  Arguments:
C     STR1   - Character array to be searched.  (Input)
C     LEN1   - Length of STR1.  (Input)
C     STR2   - Character array to be searched for.  (Input)
C     LEN2   - Length of STR2.  (Input)
C     I1ERIF - Integer function.  (Output)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION I1ERIF (STR1, LEN1, STR2, LEN2)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    LEN1, LEN2
      CHARACTER  STR1(*), STR2(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1X
      INTEGER    I1X
C                              FIRST EXECUTABLE STATEMENT
      IF (LEN1.LE.0 .OR. LEN2.LE.0) THEN
         I1ERIF = 1
      ELSE
         DO 10  I=1, LEN1
            IF (I1X(STR2,LEN2,STR1(I),1) .EQ. 0) THEN
               I1ERIF = I
               RETURN
            END IF
   10    CONTINUE
         I1ERIF = 0
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  I1KRL
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 9, 1983
C
C  Purpose:    Deallocate the last N allocations made in the workspace.
C              stack by I1KGT
C
C  Usage:      CALL I1KRL(N)
C
C  Arguments:
C     N      - Number of allocations to be released top down (Input)
C
C  Copyright:  1983 by IMSL, Inc.  All Rights Reserved
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE I1KRL (N)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IN, LALC, LBND, LBOOK, LMAX, LNEED, LNOW, LOUT,
     &           LUSED, NDX, NEXT
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      LOGICAL    FIRST
      SAVE       FIRST
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                                  SPECIFICATIONS FOR COMMON /WORKSP/
      REAL       RWKSP(5000)
      REAL       RDWKSP(5000)
      DOUBLE PRECISION DWKSP(2500)
      COMPLEX    CWKSP(2500)
      COMPLEX    CZWKSP(2500)
      COMPLEX    *16 ZWKSP(1250)
      INTEGER    IWKSP(5000)
      LOGICAL    LWKSP(5000)
      EQUIVALENCE (DWKSP(1), RWKSP(1))
      EQUIVALENCE (CWKSP(1), RWKSP(1)), (ZWKSP(1), RWKSP(1))
      EQUIVALENCE (IWKSP(1), RWKSP(1)), (LWKSP(1), RWKSP(1))
      EQUIVALENCE (RDWKSP(1), RWKSP(1)), (CZWKSP(1), RWKSP(1))
      COMMON     /WORKSP/ RWKSP
C                                  SPECIFICATIONS FOR EQUIVALENCE
      EQUIVALENCE (LOUT, IWKSP(1))
      EQUIVALENCE (LNOW, IWKSP(2))
      EQUIVALENCE (LUSED, IWKSP(3))
      EQUIVALENCE (LBND, IWKSP(4))
      EQUIVALENCE (LMAX, IWKSP(5))
      EQUIVALENCE (LALC, IWKSP(6))
      EQUIVALENCE (LNEED, IWKSP(7))
      EQUIVALENCE (LBOOK, IWKSP(8))
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1STI, IWKIN
C
      DATA FIRST/.TRUE./
C
      IF (FIRST) THEN
C                                  INITIALIZE WORKSPACE IF NEEDED
         FIRST = .FALSE.
         CALL IWKIN (0)
      END IF
C                                  CALLING I1KRL(0) WILL CONFIRM
C                                  INTEGRITY OF SYSTEM AND RETURN
      IF (N .LT. 0) THEN
         CALL E1MES (5, 10, 'Error from subroutine I1KRL:  Attempt'//
     &               ' to release a negative number of workspace'//
     &               ' allocations. ')
         GO TO 9000
      END IF
C                                  BOOKKEEPING OVERWRITTEN
      IF (LNOW.LT.LBOOK .OR. LNOW.GT.LUSED .OR. LUSED.GT.LMAX .OR.
     &    LNOW.GE.LBND .OR. LOUT.GT.LALC) THEN
         CALL E1MES (5, 11, 'Error from subroutine I1KRL:  One or '//
     &               'more of the first eight bookkeeping locations '//
     &               'in IWKSP have been overwritten.  ')
         GO TO 9000
      END IF
C                                  CHECK ALL THE POINTERS IN THE
C                                  PERMANENT STORAGE AREA.  THEY MUST
C                                  BE MONOTONE INCREASING AND LESS THAN
C                                  OR EQUAL TO LMAX, AND THE INDEX OF
C                                  THE LAST POINTER MUST BE LMAX+1.
      NDX = LBND
      IF (NDX .NE. LMAX+1) THEN
         DO 10  I=1, LALC
            NEXT = IWKSP(NDX)
            IF (NEXT .EQ. LMAX+1) GO TO 20
C
            IF (NEXT.LE.NDX .OR. NEXT.GT.LMAX) THEN
               CALL E1MES (5, 12, 'Error from subroutine I1KRL:  '//
     &                     'A pointer in permanent storage has been '//
     &                     ' overwritten. ')
               GO TO 9000
            END IF
            NDX = NEXT
   10    CONTINUE
         CALL E1MES (5, 13, 'Error from subroutine I1KRL:  A '//
     &               'pointer in permanent storage has been '//
     &               'overwritten. ')
         GO TO 9000
      END IF
   20 IF (N .GT. 0) THEN
         DO 30  IN=1, N
            IF (LNOW .LE. LBOOK) THEN
               CALL E1MES (5, 14, 'Error from subroutine I1KRL:  '//
     &                     'Attempt to release a nonexistant '//
     &                     'workspace  allocation. ')
               GO TO 9000
            ELSE IF (IWKSP(LNOW).LT.LBOOK .OR. IWKSP(LNOW).GE.LNOW-1)
     &              THEN
C                                  CHECK TO MAKE SURE THE BACK POINTERS
C                                  ARE MONOTONE.
               CALL E1STI (1, LNOW)
               CALL E1MES (5, 15, 'Error from subroutine I1KRL:  '//
     &                     'The pointer at IWKSP(%(I1)) has been '//
     &                     'overwritten.  ')
               GO TO 9000
            ELSE
               LOUT = LOUT - 1
               LNOW = IWKSP(LNOW)
            END IF
   30    CONTINUE
      END IF
C
 9000 RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  I1KST
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 9, 1983
C
C  Purpose:    Return control information about the workspace stack.
C
C  Usage:      I1KST(NFACT)
C
C  Arguments:
C     NFACT  - Integer value between 1 and 6 inclusive returns the
C                 following information: (Input)
C                   NFACT = 1 - LOUT: number of current allocations
C                               excluding permanent storage. At the
C                               end of a run, there should be no
C                               active allocations.
C                   NFACT = 2 - LNOW: current active length
C                   NFACT = 3 - LTOTAL: total storage used thus far
C                   NFACT = 4 - LMAX: maximum storage allowed
C                   NFACT = 5 - LALC: total number of allocations made
C                               by I1KGT thus far
C                   NFACT = 6 - LNEED: number of numeric storage units
C                               by which the stack size must be
C                               increased for all past allocations
C                               to succeed
C     I1KST  - Integer function. (Output) Returns a workspace stack
C              statistic according to value of NFACT.
C
C  Copyright:  1983 by IMSL, Inc.  All Rights Reserved
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION I1KST (NFACT)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    NFACT
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    ISTATS(7)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      LOGICAL    FIRST
      SAVE       FIRST
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                                  SPECIFICATIONS FOR COMMON /WORKSP/
      REAL       RWKSP(5000)
      REAL       RDWKSP(5000)
      DOUBLE PRECISION DWKSP(2500)
      COMPLEX    CWKSP(2500)
      COMPLEX    CZWKSP(2500)
      COMPLEX    *16 ZWKSP(1250)
      INTEGER    IWKSP(5000)
      LOGICAL    LWKSP(5000)
      EQUIVALENCE (DWKSP(1), RWKSP(1))
      EQUIVALENCE (CWKSP(1), RWKSP(1)), (ZWKSP(1), RWKSP(1))
      EQUIVALENCE (IWKSP(1), RWKSP(1)), (LWKSP(1), RWKSP(1))
      EQUIVALENCE (RDWKSP(1), RWKSP(1)), (CZWKSP(1), RWKSP(1))
      COMMON     /WORKSP/ RWKSP
C                                  SPECIFICATIONS FOR EQUIVALENCE
      EQUIVALENCE (ISTATS(1), IWKSP(1))
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, IWKIN
C
      DATA FIRST/.TRUE./
C
      IF (FIRST) THEN
C                                  INITIALIZE WORKSPACE IF NEEDED
         FIRST = .FALSE.
         CALL IWKIN (0)
      END IF
C
      IF (NFACT.LE.0 .OR. NFACT.GE.7) THEN
         CALL E1MES (5, 9, 'Error from subroutine I1KST:  Argument'//
     &               ' for I1KST must be between 1 and 6 inclusive.')
      ELSE IF (NFACT .EQ. 1) THEN
C                                  LOUT
         I1KST = ISTATS(1)
      ELSE IF (NFACT .EQ. 2) THEN
C                                  LNOW + PERMANENT
         I1KST = ISTATS(2) + (ISTATS(5)-ISTATS(4)+1)
      ELSE IF (NFACT .EQ. 3) THEN
C                                  LUSED + PERMANENT
         I1KST = ISTATS(3) + (ISTATS(5)-ISTATS(4)+1)
      ELSE IF (NFACT .EQ. 4) THEN
C                                  LMAX
         I1KST = ISTATS(5)
      ELSE IF (NFACT .EQ. 5) THEN
C                                  LALC
         I1KST = ISTATS(6)
      ELSE IF (NFACT .EQ. 6) THEN
C                                  LNEED
         I1KST = ISTATS(7)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  I1X (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 30, 1985
C
C  Purpose:    Determine the array subscript indicating the starting
C              element at which a key character sequence begins.
C              (Case-sensitive version)
C
C  Usage:      I1X(CHRSTR, I1LEN, KEY, KLEN)
C
C  Arguments:
C     CHRSTR - Character array to be searched.  (Input)
C     I1LEN  - Length of CHRSTR.  (Input)
C     KEY    - Character array that contains the key sequence.  (Input)
C     KLEN   - Length of KEY.  (Input)
C     I1X    - Integer function.  (Output)
C
C  Remarks:
C  1. Returns zero when there is no match.
C
C  2. Returns zero if KLEN is longer than ISLEN.
C
C  3. Returns zero when any of the character arrays has a negative or
C     zero length.
C
C  GAMS:       N5c
C
C  Chapter:    MATH/LIBRARY Utilities
C
C  Copyright:  1985 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION I1X (CHRSTR, I1LEN, KEY, KLEN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    I1LEN, KLEN
      CHARACTER  CHRSTR(*), KEY(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, II, J
C
      I1X = 0
      IF (KLEN.LE.0 .OR. I1LEN.LE.0) GO TO 9000
      IF (KLEN .GT. I1LEN) GO TO 9000
C
      I = 1
      II = I1LEN - KLEN + 1
   10 IF (I .LE. II) THEN
         IF (CHRSTR(I) .EQ. KEY(1)) THEN
            DO 20  J=2, KLEN
               IF (CHRSTR(I+J-1) .NE. KEY(J)) GO TO 30
   20       CONTINUE
            I1X = I
            GO TO 9000
   30       CONTINUE
         END IF
         I = I + 1
         GO TO 10
      END IF
C
 9000 RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  IACHAR (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    September 9, 1985
C
C  Purpose:    Return the integer ASCII value of a character argument.
C
C  Usage:      IACHAR(CH)
C
C  Arguments:
C     CH     - Character argument for which the integer ASCII value
C              is desired.  (Input)
C     IACHAR - Integer ASCII value for CH.  (Output)
C              The character CH is in the IACHAR-th position of the
C              ASCII collating sequence.
C
C  GAMS:       N3
C
C  Chapter:    MATH/LIBRARY Utilities
C              STAT/LIBRARY Utilities
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION IACHAR (CH)
C                                  SPECIFICATIONS FOR ARGUMENTS
      CHARACTER  CH
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      IACHAR = ICHAR(CH)
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  ICASE (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    September 9, 1985
C
C  Purpose:    Convert from character to the integer ASCII value without
C              regard to case.
C
C  Usage:      ICASE(CH)
C
C  Arguments:
C     CH     - Character to be converted.  (Input)
C     ICASE  - Integer ASCII value for CH without regard to the case
C              of CH.  (Output)
C              ICASE returns the same value as IMSL routine IACHAR for
C              all but lowercase letters.  For these, it returns the
C              IACHAR value for the corresponding uppercase letter.
C
C  GAMS:       N3
C
C  Chapter:    MATH/LIBRARY Utilities
C              STAT/LIBRARY Utilities
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION ICASE (CH)
C                                  SPECIFICATIONS FOR ARGUMENTS
      CHARACTER  CH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   IACHAR
      INTEGER    IACHAR
C
      ICASE = IACHAR(CH)
      IF (ICASE.GE.97 .AND. ICASE.LE.122) ICASE = ICASE - 32
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  IERCD (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 6, 1986
C
C  Purpose:    Retrieve the code for an informational error.
C
C  Usage:      IERCD()
C
C  GAMS:       R3
C
C  Chapters:   MATH/LIBRARY Reference Material
C              STAT/LIBRARY Reference Material
C              SFUN/LIBRARY Reference Material
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION IERCD ()
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   N1RCD, N1RTY
      INTEGER    N1RCD, N1RTY
C
      IF (N1RTY(1).GE.1 .AND. N1RTY(1).LE.4) THEN
         IERCD = N1RCD(1)
      ELSE
         IERCD = 0
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  IMACH (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 26, 1984
C
C  Purpose:    Retrieve integer machine constants.
C
C  Usage:      IMACH(N)
C
C  Arguments:
C     N      - Index of desired constant.  (Input)
C     IMACH  - Machine constant.  (Output)
C
C  Remark:
C     Following is a description of the assorted integer machine
C     constants.
C
C     Words
C
C        IMACH( 1) = Number of bits per integer storage unit.
C        IMACH( 2) = Number of characters per integer storage unit.
C
C     Integers
C
C        Assume integers are represented in the S-DIGIT, BASE-A form
C        SIGN ( X(S-1)*A**(S-1) + ... + X(1)*A + X(0) )
C        where 0 .LE. X(I) .LT. A for I=0,...,S-1.  Then
C
C        IMACH( 3) = A, the base.
C        IMACH( 4) = S, number of BASE-A digits.
C        IMACH( 5) = A**S - 1, largest magnitude.
C
C     Floating-point numbers
C
C        Assume floating-point numbers are represented in the T-DIGIT,
C        BASE-B form SIGN (B**E)*( (X(1)/B) + ... + (X(T)/B**T) )
C        where 0 .LE. X(I) .LT. B for I=1,...,T,
C        0 .LT. X(1), and EMIN .LE. E .LE. EMAX.  Then
C
C        IMACH( 6) = B, the base.
C
C        Single precision
C
C           IMACH( 7) = T, number of BASE-B digits.
C           IMACH( 8) = EMIN, smallest exponent E.
C           IMACH( 9) = EMAX, largest exponent E.
C
C        Double precision
C
C           IMACH(10) = T, number of BASE-B digits.
C           IMACH(11) = EMIN, smallest exponent E.
C           IMACH(12) = EMAX, largest exponent E.
C
C  GAMS:       R1
C
C  Chapters:   MATH/LIBRARY Reference Material
C              STAT/LIBRARY Reference Material
C              SFUN/LIBRARY Reference Material
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION IMACH (N)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    NOUT
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    IMACHV(12)
      SAVE       IMACHV
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   UMACH
C                                  DEFINE CONSTANTS
      DATA IMACHV(1)/32/
      DATA IMACHV(2)/4/
      DATA IMACHV(3)/2/
      DATA IMACHV(4)/31/
      DATA IMACHV(5)/2147483647/
      DATA IMACHV(6)/2/
      DATA IMACHV(7)/24/
      DATA IMACHV(8)/-125/
      DATA IMACHV(9)/128/
      DATA IMACHV(10)/53/
      DATA IMACHV(11)/-1021/
      DATA IMACHV(12)/1024/
C
      IF (N.LT.1 .OR. N.GT.12) THEN
C                                  ERROR.  INVALID RANGE FOR N.
         CALL UMACH (2, NOUT)
         WRITE (NOUT,99999) N
99999    FORMAT (/, ' *** TERMINAL ERROR 5 from IMACH.  The argument',
     &          /, ' ***          must be between 1 and 12 inclusive.'
     &          , /, ' ***          N = ', I6, '.', /)
         IMACH = 0
         STOP
C
      ELSE
         IMACH = IMACHV(N)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  INITDS (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Initialize the orthogonal series so the function value
C              is the number of terms needed to insure the error is no
C              larger than the requested accuracy.
C
C  Usage:      INITDS(DOS, NOS, ETA)
C
C  Arguments:
C     DOS    - Double precision vector of length NOS containing
C              coefficients in an orthogonal series.  (Input)
C     NOS    - Number of coefficients in OS.  (Input)
C     ETA    - Requested accuracy of the series.  (Input)
C     INITDS - Number of terms needed to insure the error is no larger
C              than ETA.  (Output)
C
C  Remark:
C     ETA will usually be chosen to be one tenth of machine precision.
C
C  GAMS:       C7b
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION INITDS (DOS, NOS, ETA)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    NOS
      REAL       ETA
      DOUBLE PRECISION DOS(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, II
      REAL       ERR
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,SNGL
      INTRINSIC  ABS, SNGL
      REAL       ABS, SNGL
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STI
C                                  SPECIFICATIONS FOR SUBROUTINES
C
      CALL E1PSH ('INITDS')
      INITDS = 0
C
      IF (NOS .LT. 1) THEN
         CALL E1STI (1, NOS)
         CALL E1MES (5, 5, 'The number of coefficients is less '//
     &               'than 1. NOS = %(I1).')
C
      ELSE
         ERR = 0.0
         DO 10  II=1, NOS
            I = NOS + 1 - II
            ERR = ERR + ABS(SNGL(DOS(I)))
            IF (ERR .GT. ETA) GO TO 20
   10    CONTINUE
C
   20    IF (I .EQ. NOS) THEN
            CALL E1MES (5, 6, 'Too much accuracy may be requested. '//
     &                  'ETA should be increased.')
         ELSE
            INITDS = I
         END IF
      END IF
C
      CALL E1POP ('INITDS')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  INITS (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Initialize the orthogonal series so the function value
C              is the number of terms needed to insure the error is no
C              larger than the requested accuracy.
C
C  Usage:      INITS(OS, NOS, ETA)
C
C  Arguments:
C     OS     - Vector of length NOS containing coefficients in an
C              orthogonal series.  (Input)
C     NOS    - Number of coefficients in OS.  (Input)
C     ETA    - Requested accuracy of the series.  (Input)
C     INITS  - Number of terms needed to insure the error is no larger
C              than ETA.  (Output)
C
C  Remark:
C     ETA will usually be chosen to be one tenth of machine precision.
C
C  GAMS:       C7b
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION INITS (OS, NOS, ETA)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    NOS
      REAL       ETA, OS(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, II
      REAL       ERR
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS
      INTRINSIC  ABS
      REAL       ABS
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STI
C                                  SPECIFICATIONS FOR SUBROUTINES
C
      CALL E1PSH ('INITS ')
      INITS = 0
C
      IF (NOS .LT. 1) THEN
         CALL E1STI (1, NOS)
         CALL E1MES (5, 5, 'The number of coefficients is less '//
     &               'than 1. NOS = %(I1).')
C
      ELSE
         ERR = 0.0
         DO 10  II=1, NOS
            I = NOS + 1 - II
            ERR = ERR + ABS(OS(I))
            IF (ERR .GT. ETA) GO TO 20
   10    CONTINUE
C
   20    IF (I .EQ. NOS) THEN
            CALL E1MES (5, 6, 'Too much accuracy may be requested. '//
     &                  'ETA should be increased.')
         ELSE
            INITS = I
         END IF
      END IF
C
      CALL E1POP ('INITS ')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  IWKIN (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 17, 1984
C
C  Purpose:    Initialize bookkeeping locations describing the
C              workspace stack.
C
C  Usage:      CALL IWKIN (NSU)
C
C  Argument:
C     NSU    - Number of numeric storage units to which the workspace
C              stack is to be initialized
C
C  GAMS:       N4
C
C  Chapters:   MATH/LIBRARY Reference Material
C              STAT/LIBRARY Reference Material
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE IWKIN (NSU)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    NSU
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    ISIZE(6), LALC, LBND, LBOOK, LMAX, LNEED, LNOW, LOUT,
     &           LUSED, MELMTS, MTYPE
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      LOGICAL    FIRST
      SAVE       FIRST
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                                  SPECIFICATIONS FOR COMMON /WORKSP/
      REAL       RWKSP(5000)
      REAL       RDWKSP(5000)
      DOUBLE PRECISION DWKSP(2500)
      COMPLEX    CWKSP(2500)
      COMPLEX    CZWKSP(2500)
      COMPLEX    *16 ZWKSP(1250)
      INTEGER    IWKSP(5000)
      LOGICAL    LWKSP(5000)
      EQUIVALENCE (DWKSP(1), RWKSP(1))
      EQUIVALENCE (CWKSP(1), RWKSP(1)), (ZWKSP(1), RWKSP(1))
      EQUIVALENCE (IWKSP(1), RWKSP(1)), (LWKSP(1), RWKSP(1))
      EQUIVALENCE (RDWKSP(1), RWKSP(1)), (CZWKSP(1), RWKSP(1))
      COMMON     /WORKSP/ RWKSP
C                                  SPECIFICATIONS FOR EQUIVALENCE
      EQUIVALENCE (LOUT, IWKSP(1))
      EQUIVALENCE (LNOW, IWKSP(2))
      EQUIVALENCE (LUSED, IWKSP(3))
      EQUIVALENCE (LBND, IWKSP(4))
      EQUIVALENCE (LMAX, IWKSP(5))
      EQUIVALENCE (LALC, IWKSP(6))
      EQUIVALENCE (LNEED, IWKSP(7))
      EQUIVALENCE (LBOOK, IWKSP(8))
      EQUIVALENCE (ISIZE(1), IWKSP(11))
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  MAX0
      INTRINSIC  MAX0
      INTEGER    MAX0
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1STI
C
      DATA FIRST/.TRUE./
C
      IF (.NOT.FIRST) THEN
         IF (NSU .NE. 0) THEN
            CALL E1STI (1, LMAX)
            CALL E1MES (5, 100, 'Error from subroutine IWKIN:  '//
     &                  'Workspace stack has previously been '//
     &                  'initialized to %(I1). Correct by making the '//
     &                  'call to IWKIN the first executable '//
     &                  'statement in the main program.  ')
C
            STOP
C
         ELSE
            RETURN
         END IF
      END IF
C
      IF (NSU .EQ. 0) THEN
C                                  IF NSU=0 USE DEFAULT SIZE 5000
         MELMTS = 5000
      ELSE
         MELMTS = NSU
      END IF
C                                  NUMBER OF ITEMS .LT. 0
      IF (MELMTS .LE. 0) THEN
         CALL E1STI (1, MELMTS)
         CALL E1MES (5, 1, 'Error from subroutine IWKIN:  Number '//
     &               'of numeric storage units is not positive. NSU '//
     &               '= %(I1) ')
      ELSE
C
         FIRST = .FALSE.
C                                  HERE TO INITIALIZE
C
C                                  SET DATA SIZES APPROPRIATE FOR A
C                                  STANDARD CONFORMING FORTRAN SYSTEM
C                                  USING THE FORTRAN
C                                  *NUMERIC STORAGE UNIT* AS THE
C                                  MEASURE OF SIZE.
C
C                                  TYPE IS REAL
         MTYPE = 3
C                                  LOGICAL
         ISIZE(1) = 1
C                                  INTEGER
         ISIZE(2) = 1
C                                  REAL
         ISIZE(3) = 1
C                                  DOUBLE PRECISION
         ISIZE(4) = 2
C                                  COMPLEX
         ISIZE(5) = 2
C                                  DOUBLE COMPLEX
         ISIZE(6) = 4
C                                  NUMBER OF WORDS USED FOR BOOKKEEPING
         LBOOK = 16
C                                  CURRENT ACTIVE LENGTH OF THE STACK
         LNOW = LBOOK
C                                  MAXIMUM VALUE OF LNOW ACHIEVED THUS
C                                  FAR
         LUSED = LBOOK
C                                  MAXIMUM LENGTH OF THE STORAGE ARRAY
         LMAX = MAX0(MELMTS,((LBOOK+2)*ISIZE(2)+ISIZE(3)-1)/ISIZE(3))
C                                  LOWER BOUND OF THE PERMANENT STORAGE
C                                  WHICH IS ONE WORD MORE THAN THE
C                                  MAXIMUM ALLOWED LENGTH OF THE STACK
         LBND = LMAX + 1
C                                  NUMBER OF CURRENT ALLOCATIONS
         LOUT = 0
C                                  TOTAL NUMBER OF ALLOCATIONS MADE
         LALC = 0
C                                  NUMBER OF WORDS BY WHICH THE ARRAY
C                                  SIZE MUST BE INCREASED FOR ALL PAST
C                                  ALLOCATIONS TO SUCCEED
         LNEED = 0
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  M1VE
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 5, 1984
C
C  Purpose:    Move a subset of one character array to another.
C
C  Usage:      CALL M1VE(INSTR, INBEG, INEND, INLEN, OUTSTR, OUTBEG,
C                         OUTEND, OUTLEN, IER)
C
C  Arguments:
C     INSTR  - Source character array.  (Input)
C     INBEG  - First element of INSTR to be moved.  (Input)
C     INEND  - Last element of INSTR to be moved.  (Input)
C              The source subset is INSTR(INBEG),...,INSTR(INEND).
C     INLEN  - Length of INSTR.  (Input)
C     OUTSTR - Destination character array.  (Output)
C     IUTBEG - First element of OUTSTR destination.  (Input)
C     IUTEND - Last element of OUTSTR  destination.  (Input)
C              The destination subset is OUTSRT(IUTBEG),...,
C              OUTSTR(IUTEND).
C     IUTLEN - Length of OUTSTR.  (Input)
C     IER    - Completion code.  (Output)
C              IER = -2  indicates that the input parameters, INBEG,
C                        INEND, INLEN, IUTBEG, IUTEND are not
C                        consistent.  One of the conditions
C                        INBEG.GT.0, INEND.GE.INBEG, INLEN.GE.INEND,
C                        IUTBEG.GT.0, or IUTEND.GE.IUTBEG is not
C                        satisfied.
C              IER = -1  indicates that the length of OUTSTR is
C                        insufficient to hold the subset of INSTR.
C                        That is, IUTLEN is less than IUTEND.
C              IER =  0  indicates normal completion
C              IER >  0  indicates that the specified subset of OUTSTR,
C                        OUTSTR(IUTBEG),...,OUTSTR(IUTEND) is not long
C                        enough to hold the subset INSTR(INBEG),...,
C                        INSTR(INEND) of INSTR.  IER is set to the
C                        number of characters that were not moved.
C
C  Remarks:
C  1. If the subset of OUTSTR is longer than the subset of INSTR,
C     trailing blanks are moved to OUTSTR.
C  2. If the subset of INSTR is longer than the subset of OUTSTR,
C     the shorter subset is moved to OUTSTR and IER is set to the number
C     of characters that were not moved to OUTSTR.
C  3. If the length of OUTSTR is insufficient to hold the subset,
C     IER is set to -2 and nothing is moved.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE M1VE (INSTR, INBEG, INEND, INLEN, OUTSTR, IUTBEG,
     &                 IUTEND, IUTLEN, IER)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    INBEG, INEND, INLEN, IUTBEG, IUTEND, IUTLEN, IER
      CHARACTER  INSTR(*), OUTSTR(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    IUTLAS, KI, KO
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      CHARACTER  BLANK
      SAVE       BLANK
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  MIN0
      INTRINSIC  MIN0
      INTEGER    MIN0
C
      DATA BLANK/' '/
C                                  CHECK INBEG, INEND, INLEN, IUTBEG,
C                                  AND IUTEND
C
      IF (INBEG.LE.0 .OR. INEND.LT.INBEG .OR. INLEN.LT.INEND .OR.
     &    IUTBEG.LE.0 .OR. IUTEND.LT.IUTBEG) THEN
         IER = -2
         RETURN
      ELSE IF (IUTLEN .LT. IUTEND) THEN
         IER = -1
         RETURN
      END IF
C                                  DETERMINE LAST CHARACTER TO M1VE
      IUTLAS = IUTBEG + MIN0(INEND-INBEG,IUTEND-IUTBEG)
C                                  M1VE CHARACTERS
      KI = INBEG
      DO 10  KO=IUTBEG, IUTLAS
         OUTSTR(KO) = INSTR(KI)
         KI = KI + 1
   10 CONTINUE
C                                   SET IER TO NUMBER OF CHARACTERS THAT
C                                   WHERE NOT MOVED
      IER = KI - INEND - 1
C                                   APPEND BLANKS IF NECESSARY
      DO 20  KO=IUTLAS + 1, IUTEND
         OUTSTR(KO) = BLANK
   20 CONTINUE
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  M1VECH
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    December 31, 1984
C
C  Purpose:    Character substring assignment.
C
C  Usage:      CALL M1VECH (STR1, LEN1, STR2, LEN2)
C
C  Arguments:
C     STR1   - Source substring.  (Input)
C              The source substring is STR1(1:LEN1).
C     LEN1   - Length of STR1.  (Input)
C     STR2   - Destination substring.  (Output)
C              The destination substring is STR2(1:LEN2).
C     LEN2   - Length of STR2.  (Input)
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE M1VECH (STR1, LEN1, STR2, LEN2)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    LEN1, LEN2
      CHARACTER  STR1*(*), STR2*(*)
C
      STR2(1:LEN2) = STR1(1:LEN1)
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  N1RCD
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 6, 1984
C
C  Purpose:    Retrieve an error code.
C
C  Usage:      N1RCD(IOPT)
C
C  Arguments:
C     IOPT   - Integer specifying the level.  (Input)
C              If IOPT=0 the error code for the current level is
C              returned.  If IOPT=1 the error code for the most
C              recently called routine (last pop) is returned.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION N1RCD (IOPT)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    IOPT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1PRT, M1VECH
C
      IF (IOPT.NE.0 .AND. IOPT.NE.1) THEN
         ERTYPE(CALLVL) = 5
         ERCODE(CALLVL) = 1
         MSGLEN = 47
         CALL M1VECH ('.  The argument passed to N1RCD must be 0 or '//
     &                '1. ', MSGLEN, MSGSAV, MSGLEN)
         CALL E1PRT
         STOP
      ELSE
         N1RCD = ERCODE(CALLVL+IOPT)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  N1RGB
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 2, 1984
C
C  Purpose:    Return a positive number as a flag to indicated that a
C              stop should occur due to one or more global errors.
C
C  Usage:      N1RGB(IDUMMY)
C
C  Arguments:
C     IDUMMY - Integer scalar dummy argument.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION N1RGB (IDUMMY)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    IDUMMY
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  INITIALIZE FUNCTION
      N1RGB = 0
C                                  CHECK FOR GLOBAL ERROR TYPE 6
      IF (IFERR6 .GT. 0) THEN
         N1RGB = STOPTB(6)
         IFERR6 = 0
      END IF
C                                  CHECK FOR GLOBAL ERROR TYPE 7
      IF (IFERR7 .GT. 0) THEN
         N1RGB = STOPTB(7)
         IFERR7 = 0
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  N1RTY
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 6, 1984
C
C  Purpose:    Retrieve an error type.
C
C  Usage:      N1RTY(IOPT)
C
C  Arguments:
C     IOPT   - Integer specifying the level.  (Input)
C              If IOPT=0 the error type for the current level is
C              returned.  If IOPT=1 the error type for the most
C              recently called routine (last pop) is returned.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      INTEGER FUNCTION N1RTY (IOPT)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    IOPT
C                                  SPECIFICATIONS FOR SPECIAL CASES
C                              SPECIFICATIONS FOR COMMON /ERCOM1/
      INTEGER    CALLVL, MAXLEV, MSGLEN, ERTYPE(51), ERCODE(51),
     &           PRINTB(7), STOPTB(7), PLEN, IFERR6, IFERR7,
     &           IALLOC(51), HDRFMT(7), TRACON(7)
      COMMON     /ERCOM1/ CALLVL, MAXLEV, MSGLEN, ERTYPE, ERCODE,
     &           PRINTB, STOPTB, PLEN, IFERR6, IFERR7, IALLOC, HDRFMT,
     &           TRACON
      SAVE       /ERCOM1/
C                              SPECIFICATIONS FOR COMMON /ERCOM2/
      CHARACTER  MSGSAV(255), PLIST(300), RNAME(51)*6
      COMMON     /ERCOM2/ MSGSAV, PLIST, RNAME
      SAVE       /ERCOM2/
C                              SPECIFICATIONS FOR COMMON /ERCOM3/
      DOUBLE PRECISION ERCKSM
      COMMON     /ERCOM3/ ERCKSM
      SAVE       /ERCOM3/
C                              SPECIFICATIONS FOR COMMON /ERCOM4/
      LOGICAL    ISUSER(51)
      COMMON     /ERCOM4/ ISUSER
      SAVE       /ERCOM4/
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1PRT, M1VECH
C
      IF (IOPT.NE.0 .AND. IOPT.NE.1) THEN
         ERTYPE(CALLVL) = 5
         ERCODE(CALLVL) = 1
         MSGLEN = 47
         CALL M1VECH ('.  The argument passed to N1RTY must be 0 or '//
     &                '1. ', MSGLEN, MSGSAV, MSGLEN)
         CALL E1PRT
         STOP
      ELSE
         N1RTY = ERTYPE(CALLVL+IOPT)
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  R9GAML (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Compute the underflow and overflow limits for the gamma
C              function and several related functions.
C
C  Usage:      CALL R9GAML (XMIN, XMAX)
C
C  Arguments:
C     XMIN   - Underflow limit.  (Output)
C     XMAX   - Overflow limit.  (Output)
C
C  Remark:
C     XMIN and XMAX are not the only bounds for the function, but they
C     are the only nontrivial ones to calculate.
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE R9GAML (XMIN, XMAX)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       XMIN, XMAX
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I
      REAL       ALNBIG, ALNSML, XLN, XOLD
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ABS,ALOG,AMAX1
      INTRINSIC  ABS, ALOG, AMAX1
      REAL       ABS, ALOG, AMAX1
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH
      REAL       AMACH
C
      CALL E1PSH ('R9GAML')
      XMIN = AMACH(6)
      XMAX = AMACH(6)
C
      ALNSML = ALOG(AMACH(1))
      XMIN = -ALNSML
      DO 10  I=1, 10
         XOLD = XMIN
         XLN = ALOG(XMIN)
         XMIN = XMIN - XMIN*((XMIN+0.5)*XLN-XMIN-0.2258+ALNSML)/(XMIN*
     &          XLN+0.5)
         IF (ABS(XMIN-XOLD) .LT. 0.005) GO TO 20
   10 CONTINUE
      CALL E1MES (5, 5, 'Unable to determine the value of XMIN.')
      XMIN = AMACH(6)
      GO TO 9000
C
   20 XMIN = -XMIN + 0.01
C
      ALNBIG = ALOG(AMACH(2))
      XMAX = ALNBIG
      DO 30  I=1, 10
         XOLD = XMAX
         XLN = ALOG(XMAX)
         XMAX = XMAX - XMAX*((XMAX-0.5)*XLN-XMAX+0.9189-ALNBIG)/(XMAX*
     &          XLN-0.5)
         IF (ABS(XMAX-XOLD) .LT. 0.005) GO TO 40
   30 CONTINUE
      CALL E1MES (5, 6, 'Unable to determine the value of XMAX.')
      XMAX = AMACH(6)
      GO TO 9000
C
   40 XMAX = XMAX - 0.01
      XMIN = AMAX1(XMIN,-XMAX+1.0)
C
 9000 CALL E1POP ('R9GAML')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  R9LGMC (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the log gamma correction term for argument
C              values greater than or equal to 10.0.
C
C  Usage:      R9LGMC(X)
C
C  Arguments:
C     X      - Argument for which the function value is desired.
C              (Input)
C     R9LGMC - Function value.  (Output)
C
C  Remarks:
C  1. Informational error:
C     Type Code
C       2   1  The function underflows because X is too large.
C
C  2. R9LGMC calculates the log gamma correction factor such that
C     ALOG (GAMMA(X)) = ALOG(SQRT(2*PI))+(X-.5)*ALOG(X)-X+R9LGMC(X).
C
C  Chapter:    SFUN/LIBRARY Gamma Function and Related Functions
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION R9LGMC (X)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       X
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    NALGM
      REAL       ALGMCS(6), XBIG, XMAX
      SAVE       ALGMCS, NALGM, XBIG, XMAX
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ALOG,AMIN1,EXP,SQRT
      INTRINSIC  ALOG, AMIN1, EXP, SQRT
      REAL       ALOG, AMIN1, EXP, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, CSEVL, INITS
      INTEGER    INITS
      REAL       AMACH, CSEVL
C
C                                  SERIES FOR ALGM ON THE INTERVAL
C                                  0.0 TO 1.00000E-02
C                                  WITH WEIGHTED ERROR        3.40E-16
C                                  LOG WEIGHTED ERROR        15.47
C                                  SIGNIFICANT FIGURES REQD. 14.39
C                                  DECIMAL PLACES REQUIRED   15.86
C
      DATA ALGMCS(1)/.166638948045186E0/
      DATA ALGMCS(2)/-.0000138494817606E0/
      DATA ALGMCS(3)/.0000000098108256E0/
      DATA ALGMCS(4)/-.0000000000180912E0/
      DATA ALGMCS(5)/.0000000000000622E0/
      DATA ALGMCS(6)/-.0000000000000003E0/
C
      DATA NALGM/0/, XBIG/0.0/, XMAX/0.0/
C
      CALL E1PSH ('R9LGMC')
      R9LGMC = AMACH(6)
C
      IF (NALGM .EQ. 0) THEN
         NALGM = INITS(ALGMCS,6,AMACH(3))
         XBIG = 1.0/SQRT(AMACH(3))
         XMAX = EXP(AMIN1(ALOG(AMACH(2)/12.0),-ALOG(12.0*AMACH(1))))
      END IF
C
      IF (X .LT. 10.0) THEN
         CALL E1STR (1, X)
         CALL E1MES (5, 5, 'The argument X = %(R1) must be '//
     &               'greater than or equal to 10.0.')
C
      ELSE IF (X .LT. XMAX) THEN
         IF (X .GE. XBIG) THEN
            R9LGMC = 1.0/(12.0*X)
         ELSE
            R9LGMC = CSEVL(2.0*(10.0/X)**2-1.0,ALGMCS,NALGM)/X
         END IF
C
      ELSE
         R9LGMC = 0.0
         CALL E1STR (1, X)
         CALL E1STR (2, XMAX)
         CALL E1MES (2, 1, 'The function underflows because '//
     &               'X = %(R1) is greater than %(R2). The result is '//
     &               'set to zero.')
      END IF
C
      CALL E1POP ('R9LGMC')
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  S1ANUM
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 28, 1984
C
C  Purpose:    Scan a token and identify it as follows: integer, real
C              number (single/double), FORTRAN relational operator,
C              FORTRAN logical operator, or FORTRAN logical constant.
C
C  Usage:      CALL S1ANUM(INSTR, SLEN, CODE, OLEN)
C
C  Arguments:
C     INSTR  - Character string to be scanned.  (Input)
C     SLEN   - Length of INSTR.  (Input)
C     CODE   - Token code.  (Output)  Where
C                 CODE =  0  indicates an unknown token,
C                 CODE =  1  indicates an integer number,
C                 CODE =  2  indicates a (single precision) real number,
C                 CODE =  3  indicates a (double precision) real number,
C                 CODE =  4  indicates a logical constant (.TRUE. or
C                               .FALSE.),
C                 CODE =  5  indicates the relational operator .EQ.,
C                 CODE =  6  indicates the relational operator .NE.,
C                 CODE =  7  indicates the relational operator .LT.,
C                 CODE =  8  indicates the relational operator .LE.,
C                 CODE =  9  indicates the relational operator .GT.,
C                 CODE = 10  indicates the relational operator .GE.,
C                 CODE = 11  indicates the logical operator .AND.,
C                 CODE = 12  indicates the logical operator .OR.,
C                 CODE = 13  indicates the logical operator .EQV.,
C                 CODE = 14  indicates the logical operator .NEQV.,
C                 CODE = 15  indicates the logical operator .NOT..
C     OLEN   - Length of the token as counted from the first character
C              in INSTR.  (Output)  OLEN returns a zero for an unknown
C              token (CODE = 0).
C
C  Remarks:
C  1. Blanks are considered significant.
C  2. Lower and upper case letters are not significant.
C
C  Copyright:  1984 by IMSL, Inc.  All rights reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE S1ANUM (INSTR, SLEN, CODE, OLEN)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    SLEN, CODE, OLEN
      CHARACTER  INSTR(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IBEG, IIBEG, J
      LOGICAL    FLAG
      CHARACTER  CHRSTR(6)
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    TABPTR(16), TDCNST, TICNST, TOKEN(13), TRCNST, TZERR
      CHARACTER  DIGIT(10), LETTER(52), MINUS, PERIOD, PLUS, TABLE(38)
      SAVE       DIGIT, LETTER, MINUS, PERIOD, PLUS, TABLE, TABPTR,
     &           TDCNST, TICNST, TOKEN, TRCNST, TZERR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   I1X, I1CSTR
      INTEGER    I1X, I1CSTR
C
      DATA TOKEN/5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 4, 4/
      DATA TABLE/'D', 'E', 'E', 'Q', 'N', 'E', 'L', 'T', 'L',
     &     'E', 'G', 'T', 'G', 'E', 'A', 'N', 'D', 'O', 'R',
     &     'E', 'Q', 'V', 'N', 'E', 'Q', 'V', 'N', 'O', 'T',
     &     'T', 'R', 'U', 'E', 'F', 'A', 'L', 'S', 'E'/
      DATA TABPTR/1, 2, 3, 5, 7, 9, 11, 13, 15, 18, 20, 23, 27, 30,
     &     34, 39/
      DATA DIGIT/'0', '1', '2', '3', '4', '5', '6', '7', '8',
     &     '9'/
      DATA LETTER/'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
     &     'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
     &     'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c',
     &     'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
     &     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
     &     'x', 'y', 'z'/
      DATA PERIOD/'.'/, PLUS/'+'/, MINUS/'-'/
      DATA TZERR/0/, TICNST/1/
      DATA TRCNST/2/, TDCNST/3/
C
      IF (SLEN .LE. 0) THEN
         CODE = 0
         OLEN = 0
         RETURN
      END IF
C                                  STATE 0 - ASSUME ERROR TOKEN
      IBEG = 1
      CODE = TZERR
C                                  CHECK SIGN
      IF (INSTR(IBEG).EQ.MINUS .OR. INSTR(IBEG).EQ.PLUS) THEN
         FLAG = .TRUE.
         IIBEG = IBEG
         IBEG = IBEG + 1
      ELSE
         FLAG = .FALSE.
      END IF
C                                  STATE 1 - ASSUME INTEGER CONSTANT
      IF (I1X(DIGIT,10,INSTR(IBEG),1) .NE. 0) THEN
         CODE = TICNST
         IIBEG = IBEG
         IBEG = IBEG + 1
C
   10    IF (IBEG .LE. SLEN) THEN
C
            IF (I1X(DIGIT,10,INSTR(IBEG),1) .NE. 0) THEN
               IIBEG = IBEG
               IBEG = IBEG + 1
               GO TO 10
C
            END IF
C
         ELSE
            GO TO 80
C
         END IF
C
         IF (INSTR(IBEG) .NE. PERIOD) GO TO 80
      END IF
C                                  STATE 2 - ASSUME REAL CONSTANT
      IF (CODE .EQ. TICNST) THEN
         CODE = TRCNST
         IIBEG = IBEG
         IBEG = IBEG + 1
         IF (IBEG .GT. SLEN) GO TO 80
      ELSE IF (INSTR(IBEG).EQ.PERIOD .AND. SLEN.GE.2) THEN
         IF (I1X(DIGIT,10,INSTR(IBEG+1),1) .NE. 0) THEN
            CODE = TRCNST
            IIBEG = IBEG + 1
            IBEG = IBEG + 2
            IF (IBEG .GT. SLEN) GO TO 80
         END IF
      END IF
C
      IF (I1X(DIGIT,10,INSTR(IBEG),1) .NE. 0) THEN
         CODE = TRCNST
         IIBEG = IBEG
         IBEG = IBEG + 1
C
   20    IF (IBEG .LE. SLEN) THEN
C
            IF (I1X(DIGIT,10,INSTR(IBEG),1) .NE. 0) THEN
               IIBEG = IBEG
               IBEG = IBEG + 1
               GO TO 20
C
            END IF
C
         ELSE
            GO TO 80
C
         END IF
C
      END IF
C
      IF (CODE .EQ. TZERR) THEN
         IF (INSTR(IBEG) .NE. PERIOD) GO TO 80
         IBEG = IBEG + 1
         IF (IBEG .GT. SLEN) GO TO 80
      END IF
C
      IF (I1X(LETTER,52,INSTR(IBEG),1) .EQ. 0) GO TO 80
      CHRSTR(1) = INSTR(IBEG)
C
      DO 30  I=2, 6
         IBEG = IBEG + 1
         IF (IBEG .GT. SLEN) GO TO 80
         IF (I1X(LETTER,52,INSTR(IBEG),1) .EQ. 0) GO TO 40
         CHRSTR(I) = INSTR(IBEG)
   30 CONTINUE
C
      GO TO 80
C
   40 CONTINUE
C
      DO 50  J=1, 15
         IF (I1CSTR(CHRSTR,I-1,TABLE(TABPTR(J)),TABPTR(J+1)-TABPTR(J))
     &        .EQ. 0) GO TO 60
   50 CONTINUE
C
      GO TO 80
C                                  STATE 4 - LOGICAL OPERATOR
   60 IF (J .GT. 2) THEN
C
         IF (CODE .EQ. TRCNST) THEN
C
            IF (INSTR(IBEG) .EQ. PERIOD) THEN
               CODE = TICNST
               IIBEG = IIBEG - 1
            END IF
C
            GO TO 80
C
         ELSE IF (INSTR(IBEG) .NE. PERIOD) THEN
            GO TO 80
C
         ELSE IF (FLAG) THEN
            GO TO 80
C
         ELSE
            CODE = TOKEN(J-2)
            IIBEG = IBEG
            GO TO 80
C
         END IF
C
      END IF
C                                  STATE 5 - DOUBLE PRECISION CONSTANT
      IF (CODE .NE. TRCNST) GO TO 80
      IF (INSTR(IBEG).EQ.MINUS .OR. INSTR(IBEG).EQ.PLUS) IBEG = IBEG +
     &    1
      IF (IBEG .GT. SLEN) GO TO 80
C
      IF (I1X(DIGIT,10,INSTR(IBEG),1) .EQ. 0) THEN
         GO TO 80
C
      ELSE
         IIBEG = IBEG
         IBEG = IBEG + 1
C
   70    IF (IBEG .LE. SLEN) THEN
C
            IF (I1X(DIGIT,10,INSTR(IBEG),1) .NE. 0) THEN
               IIBEG = IBEG
               IBEG = IBEG + 1
               GO TO 70
C
            END IF
C
         END IF
C
      END IF
C
      IF (J .EQ. 1) CODE = TDCNST
C
   80 CONTINUE
C
      IF (CODE .EQ. TZERR) THEN
         OLEN = 0
C
      ELSE
         OLEN = IIBEG
      END IF
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  SCOPY (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    August 9, 1986
C
C  Purpose:    Copy a vector X to a vector Y, both single precision.
C
C  Usage:      CALL SCOPY (N, SX, INCX, SY, INCY)
C
C  Arguments:
C     N      - Length of vectors X and Y.  (Input)
C     SX     - Real vector of length MAX(N*IABS(INCX),1).  (Input)
C     INCX   - Displacement between elements of SX.  (Input)
C              X(I) is defined to be.. SX(1+(I-1)*INCX) if INCX .GE. 0
C              or SX(1+(I-N)*INCX) if INCX .LT. 0.
C     SY     - Real vector of length MAX(N*IABS(INCY),1).  (Output)
C              SCOPY copies X(I) to Y(I) for I=1,...,N. X(I) and Y(I)
C              refer to specific elements of SX and SY, respectively.
C              See INCX and INCY argument descriptions.
C     INCY   - Displacement between elements of SY.  (Input)
C              Y(I) is defined to be.. SY(1+(I-1)*INCY) if INCY .GE. 0
C              or SY(1+(I-N)*INCY) if INCY .LT. 0.
C
C  GAMS:       D1a
C
C  Chapters:   MATH/LIBRARY Basic Matrix/Vector Operations
C              STAT/LIBRARY Mathematical Support
C
C  Copyright:  1986 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE SCOPY (N, SX, INCX, SY, INCY)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, INCX, INCY
      REAL       SX(*), SY(*)
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    I, IX, IY, M, MP1
C                                  SPECIFICATIONS FOR SPECIAL CASES
C     INTRINSIC  MOD
      INTRINSIC  MOD
      INTEGER    MOD
C
      IF (N .GT. 0) THEN
         IF (INCX.NE.1 .OR. INCY.NE.1) THEN
C                                  CODE FOR UNEQUAL INCREMENTS
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
C                                  CODE FOR BOTH INCREMENTS EQUAL TO 1
            M = MOD(N,7)
C                                  CLEAN-UP LOOP
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
C-----------------------------------------------------------------------
C  IMSL Name:  TDF/DTDF (Single/Double precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    January 1, 1984
C
C  Purpose:    Evaluate the Student's t distribution function.
C
C  Usage:      TDF(T, DF)
C
C  Arguments:
C     T      - Argument for which the Student's t distribution function
C              is to be evaluated.  (Input)
C     DF     - Degrees of freedom.  (Input)
C              DF must be greater than or equal to 1.0.
C     TDF    - Function value, the probability that a Student's t random
C              variable takes a value less than or equal to the input T.
C              (Output)
C
C  Keywords:   P-value; Probability integral
C
C  GAMS:       L5a1t
C
C  Chapters:   STAT/LIBRARY Probability Distribution Functions and
C                           Inverses
C              SFUN/LIBRARY Probability Distribution Functions and
C                           Inverses
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      REAL FUNCTION TDF (T, DF)
C                                  SPECIFICATIONS FOR ARGUMENTS
      REAL       T, DF
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    N
      REAL       A, AN, B, Q, TEMP, W, XJ, Y, Z
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      REAL       CON1
      SAVE       CON1
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  ALOG,ATAN,SQRT
      INTRINSIC  ALOG, ATAN, SQRT
      REAL       ALOG, ATAN, SQRT
C                                  SPECIFICATIONS FOR SUBROUTINES
      EXTERNAL   E1MES, E1POP, E1PSH, E1STR
C                                  SPECIFICATIONS FOR FUNCTIONS
      EXTERNAL   AMACH, BETDF, ERFC
      REAL       AMACH, BETDF, ERFC
C
      DATA CON1/0.63661977236758/
C
      CALL E1PSH ('TDF   ')
      TDF = AMACH(6)
C                                  Check DF
      IF (DF .LT. 1.0) THEN
         CALL E1STR (1, DF)
         CALL E1MES (5, 1, 'The input number of degrees of freedom, '//
     &               'DF = %(R1), must be at least 1.')
         GO TO 9000
      END IF
C
      TEMP = T*T
      IF (DF .GT. TEMP) THEN
         TEMP = T
         AN = DF
         N = AN
         TEMP = TEMP*TEMP
         Y = TEMP/AN
         B = 1.0 + Y
         IF (AN.NE.N .OR. AN.GE.20.0 .OR. AN.GT.200.0) THEN
C                                  Asymptotic series for large AN
            W = B - 1.0
            IF (W .NE. 0.0) Y = Y*(ALOG(B)/W)
            A = AN - 0.5
            B = 48.0*A*A
            Y = Y*A
            Y = (((((-0.4*Y-3.3)*Y-24.0)*Y-85.5)/(0.8*(Y*Y)+100.0+B)+Y+
     &          3.0)/B+1.0)*SQRT(Y)
            IF (Y .LT. 18.8125) THEN
C                                  Overflow (or underflow?) could occur
C                                  on some machines on call to ERFC
               Q = ERFC(Y*SQRT(0.5))
            ELSE
               Q = 0.0
            END IF
         ELSE
            IF (AN.LT.20.0 .AND. TEMP.LT.4.0) THEN
C                                  Nested summation of *COSINE* series
               Y = SQRT(Y)
               A = Y
               IF (AN .EQ. 1.0) A = 0.0
   10          AN = AN - 2.0
               IF (AN .GT. 1.0) THEN
                  A = (AN-1.0)/(B*AN)*A + Y
                  GO TO 10
               END IF
               IF (AN .EQ. 0.0) A = A/SQRT(B)
               IF (AN .NE. 0.0) A = (ATAN(Y)+A/B)*CON1
               Q = 1.0 - A
            ELSE
C                                  *TAIL* series expansion for large
C                                  T-values
               A = 1.0
               Y = AN
               XJ = 0.0
               Z = 0.0
   20          IF (A .NE. Z) THEN
                  XJ = XJ + 2.0
                  Z = A
                  Y = Y*(XJ-1.0)/(B*XJ)
                  A = A + Y/(AN+XJ)
                  GO TO 20
               END IF
   30          IF (AN.GT.1.0 .AND. A.GE.1.0E-30) THEN
C                                  NOTE:  The conditional, A.GE.1.0E-30,
C                                  included above is needed for the
C                                  division by A below (overflow).
C                                  According to the original basis deck,
C                                  some machines require a less
C                                  restriction on A or none at all.
                  A = (AN-1.0)/(B*AN)*A
                  AN = AN - 2.0
                  GO TO 30
               END IF
               IF (AN .NE. 0.0) A = SQRT(B)*CON1*A/B
               Q = A
            END IF
         END IF
      ELSE
         TEMP = DF/(DF+TEMP)
         A = 0.5*DF
         B = 0.5
         Q = BETDF(TEMP,A,B)
      END IF
C
      IF (T .GT. 0.0) THEN
         TDF = 1.0 - 0.5*Q
      ELSE
         TDF = 0.5*Q
      END IF
C
 9000 CALL E1POP ('TDF   ')
C
      RETURN
      END
C-----------------------------------------------------------------------
C  IMSL Name:  UMACH (Single precision version)
C
C  Computer:   PCDSMS/SINGLE
C
C  Revised:    March 21, 1984
C
C  Purpose:    Set or retrieve input or output device unit numbers.
C
C  Usage:      CALL UMACH (N, NUNIT)
C
C  Arguments:
C     N      - Index of desired unit.  (Input)
C              The values of N are defined as follows:
C              N = 1, corresponds to the standard input unit.
C              N = 2, corresponds to the standard output unit.
C     NUNIT  - I/O unit.  (Input or Output)
C              If the value of N is negative, the unit corresponding
C              to the index is reset to the value given in NUNIT.
C              Otherwise, the value corresponding to the index is
C              returned in NUNIT.
C
C  GAMS:       R1
C
C  Chapters:   MATH/LIBRARY Reference Material
C              STAT/LIBRARY Reference Material
C              SFUN/LIBRARY Reference Material
C
C  Copyright:  1984 by IMSL, Inc.  All Rights Reserved.
C
C  Warranty:   IMSL warrants only that IMSL testing has been applied
C              to this code.  No other warranty, expressed or implied,
C              is applicable.
C
C-----------------------------------------------------------------------
C
      SUBROUTINE UMACH (N, NUNIT)
C                                  SPECIFICATIONS FOR ARGUMENTS
      INTEGER    N, NUNIT
C                                  SPECIFICATIONS FOR LOCAL VARIABLES
      INTEGER    NN, NOUT
C                                  SPECIFICATIONS FOR SAVE VARIABLES
      INTEGER    UNIT(2)
      SAVE       UNIT
C                                  SPECIFICATIONS FOR INTRINSICS
C     INTRINSIC  IABS
      INTRINSIC  IABS
      INTEGER    IABS
C
      DATA UNIT(1)/5/
      DATA UNIT(2)/6/
C
      NN = IABS(N)
      IF (NN.NE.1 .AND. NN.NE.2) THEN
C                                  ERROR.  INVALID RANGE FOR N.
         NOUT = UNIT(2)
         WRITE (NOUT,99999) NN
99999    FORMAT (/, ' *** TERMINAL ERROR 5 from UMACH.  The absolute',
     &          /, ' ***          value of the index variable must be'
     &          , /, ' ***          1 or 2.  IABS(N) = ', I6,
     &          '.', /)
         STOP
C                                  CHECK FOR RESET OR RETRIEVAL
      ELSE IF (N .LT. 0) THEN
C                                  RESET
         UNIT(NN) = NUNIT
      ELSE
C                                  RETRIEVE
         NUNIT = UNIT(N)
      END IF
C
      RETURN
      END
