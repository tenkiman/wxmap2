C
C **************************************************************
C
cx    SUBROUTINE HOUR(X,Y,Z,M)
      SUBROUTINE HOUR(X,Y,Z,MM)
C
C  THIS ROUTINE 'HOUR' CALCULATES THE TROPICAL CYCLONE
C   POSITIONS BY EVERY DELTA INCREMENT AND STORE THEM IN
C   HRLNG,HRLAT ARRAYS.   'HOUR' CALLS 'SLOP' TO CALCULATE 
C   THE SLOP OF EACH EXISTING POINTS.
C
      DIMENSION X(200),T(200),Y(200),Z(1201)
      integer*2 m
C
C FUNCTIONS
      PLT(Y0,T0,P2,P3,DD) = Y0 + (T0 + (P2 + P3*DD) * DD) * DD
      SLP2(T0,T1,DY,DX) = (3.*DY*DX - 2.*T0 - T1) * DX
      SLP3(T0,T1,DY,DX) = (T0 + T1 - 2.*DY*DX) *DX *DX

c m must be integer*2, I don't know what mm is coming in
      m=mm
C
      DELTA=1.
      XX=X(1)
      DO 50 I=1,M
      X(I)=X(I)-XX 
50    CONTINUE
C
      IF(M-2) 100,120,140
C
C100   WRITE(*,6001)
100   CONTINUE
      RETURN
C
C120   WRITE(*,6002)
120   CONTINUE
      DX=1./(X(2)-X(1))
      T(1)=(Y(2)-Y(1))*DX
      K=0
      XX=X(1)-DELTA
127   IF(XX.GE.X(M)) RETURN
      K=K+1
      XX=XX+DELTA
      DD=XX-X(1)
      P2=0.
      P3=0.
      Z(K)=PLT(Y(1),T(1),P2,P3,DD)
      GO TO 127
C
C  CALCULATE THE SLOPES
140   CALL SLOP(Y,X,T,M)
C
C  INTERPOLATION:  X(I-1) .LT. XX .LT. X(I)
C   X(I-1) .LT. X(I); XX=X(I-1), IF ABS(XX-X(I-1)) .LT. CRIT
C
175   K=0
      XX=X(1)-DELTA
C
      DO 200 I=2,M 
C
      DX=1./(X(I)-X(I-1))
250   IF(XX.GE.X(I)) GO TO 200
      K=K+1
      XX=XX+DELTA
      DD=XX-X(I-1) 
C
      DY=Y(I)-Y(I-1)
      P2=SLP2(T(I-1),T(I),DY,DX)
      P3=SLP3(T(I-1),T(I),DY,DX)
      Z(K)=PLT(Y(I-1),T(I-1),P2,P3,DD) 
C
      GO TO 250
C
200   CONTINUE
C
      RETURN
C
6001  FORMAT(' NO INTERPOLATION!')
6002  FORMAT('  LINEAR INTERPOLATION!')
      END
