      subroutine probability ( fstRcd, nsta, stanam, psvg, arrayp,
     &                         iprob_stat )
C
C**   Run the STRIKE probability program.
C
C**   THIS PROGRAM USES HISTORICAL STATISTICS TO ESTIMATE PROBABILITY
C**   OF A TROPICAL CYCLONE PASSING THRU AN AREA, GIVEN THE FORECAST.
C**   ***OUTPUT: INSTANTANEOUS AND TIME INTEGRATED (0-T) PROBABILITY
C**   ARE STORED IN POV(I),I=TIME=1,25=0,72,3 HOUR STEPS
C
C**   1998/05/17  REVISED TO INCLUDE 36 HR PROBABILITIES AND TO
C                 ELIMINATE PROBABILITIES OF 1%
C**   1989/06/05  MOVED LOCATION OF CALL TO STRIKE.  CJM.
c
c**   2000/02/10  Extensive revisions made to the strike probability
c**               program for the UNIX version of the ATCF System.
c**               the prestrik and strikp programs were combined and the 
c**               two probability message construct portions were also
c**               combined.  Much of the code was simplifed and it is now
c**               compiled under FORTRAN 90.
C
C
      INCLUDE  'dataformats.inc'
C
      COMMON /parameter/NDTG,MXW
      COMMON /ltlnint/ LAT00,LON00,LAT12,LON12,LAT24,LON24,
     & LAT36,LON36,LAT48,LON48,LAT72,LON72
      COMMON /ltlnchr/latlon(7)
      common /ltlnflt/ flat(7),flon(7)
C
      DIMENSION itau(7)
      REAL STD(5,5), arrayp(96,60)
      integer psvg(25,150)
C
      character*12 latlon
      CHARACTER*16  STANAM(150)
C
      data itau / 0, 3, 12, 24, 36, 48, 72 /
c
      type (AID_DATA) fstRcd, tauData
c
      iprob_stat = 0
C
C**   Read the initial position and current track forecast
C
      do i = 1, 7
c
         call getSingleTAU ( fstRcd, itau(i), tauData, istat )
c
         if ( istat .eq. 1 ) then
c
            flat(i) = tauData%aRecord(1)%lat
            flon(i) = tauData%aRecord(1)%lon
c
            latlon(i) = tauData%atcfRcd(1)%latns(1:2)//'.'//
     &                  tauData%atcfRcd(1)%latns(3:4)//' '//
     &                  tauData%atcfRcd(1)%lonew(1:3)//'.'//
     &                  tauData%atcfRcd(1)%lonew(4:5)
c
c**   Save the initial date/time group and maximum wind speed
c
            if ( i .eq. 1 ) then
               read ( tauData%aRecord(1)%DTG, '(i10)' ) NDTG
               MXW = tauData%aRecord(1)%vmax
            endif   
c
         else
c
            flat(i)   = 0.0
            flon(i)   = 0.0
            latlon(i) = ' '
c
         endif
      enddo
c
      LAT00 = FLAT(1)*10.0
      LON00 = 3600.0 - FLON(1)*10.0
      LAT12 = FLAT(3)*10.0
      LON12 = 3600.0 - FLON(3)*10.0
      LAT24 = FLAT(4)*10.0
      LON24 = 3600.0 - FLON(4)*10.0
      LAT36 = FLAT(5)*10.0
      LON36 = 3600.0 - FLON(5)*10.0
      LAT48 = FLAT(6)*10.0
      LON48 = 3600.0 - FLON(6)*10.0
      LAT72 = FLAT(7)*10.0
      LON72 = 3600.0 - FLON(7)*10.0
c
c**   Compute the newstd
C
      Y1 = LAT00/10.0
      X1 = LON00/10.0
      Y2 = LAT12/10.0
      X2 = LON12/10.0
      X1 = 360.0 - X1
      X2 = 360.0 - X2
C
      CALL DIRDST ( Y1, X1, Y2, X2, ANG, DST )
C
      ANG = ANG*0.0174533
      U   = DST*SIN(ANG)/8.0
      V   = DST*COS(ANG)/8.0
C
c**   Compute the new set of standard deviations of the errors
c
      CALL NEWSTD ( Y1, X1, U, V, STD)
C
C**   Dummy call to useary only to INITIALIZE THE PROBABILITY TABLE
C
      CALL USEARY ( X, X, X, X, X, X, X, X, X )
C
C**    SET CONSTANTS
C**    IRLF,IRRT = RADIUS (NM)LEFT AND RIGHT OF STATION (FACING DIRECTION
C**    OF CYCLONE MOTION) DEFINING AREA CONSIDERED TO CONSTITUTE A STRIKE.
C**    DEFAULTS OF 75 AND 50 NM ARE USED.
C
      IRLF = 75
      IRRT = 50
      RADU = FLOAT(IRLF)
      RADL = FLOAT(IRRT)
C
C**   INDATA FILLS ARRAY P(I,J) J=1,25 -- 3 HOUR TIME STEPS 0 TO 72 HOURS.
C**   AT EACH TIME STEP:
c**   P(1)  = E-W MEAN FCST ERROR
c**   P(2)  = E-W ERROR STDEV
C**   P(3)  = N-S MEAN FCST ERROR
c**   P(4)  = N-S ERROR STDEV
c**   P(5)  = CORRELATION COEFFICIENT E-W TO N-S ERROR.
c**   P(6)  = fcst lat in tenths of degrees
c**   P(7)  = FCST LON IN TENTHS OF DEGREES
c**   P(8)  = xds(e-w) distance in nmi 
c**   P(9)  = YDS(N-S) DISTance in NMI
C**      FROM POINT OF INTEREST TO CENTER OF CIRCLE OF INTEREST.
c**   P(10) = RADIUS OF CIRCLE OF INTEREST = ( RADLEFT + RADRIGHT )/2
C
      CALL INDATA ( MAXT, RADU, RADL, ANG, std )
c
c**   Return because of insufficient forecast data
c
      IF ( MAXT .LT. 12 ) return
C
C**   This subroutine reads in the station data and totals the 
c**     probabilities for each.
C
      CALL XTRAST ( maxt, ang, nsta, stanam, psvg )
c
      call parray ( maxt, ang, arrayp )
c
      iprob_stat = 1
c
      return
      END
C**********************************************************************
       SUBROUTINE NEWSTD(Y,X,U,V,STD)
C
C**
c
      REAL STD(5,5), RUNSM(5,6), PAR1(5,6), PAR2(5,6)
c
       data aa / 62.5 /

       call zero ( runsm, 5, 6 )

       CALL FIRSTGU ( X, Y, U, V, PAR2, RUNSM )
C
       CALL MKSTAT ( RUNSM, PAR2 )
C
       CALL CLS_STS ( Y, X, PAR1 )
C
       DO I = 1, 5
          PAR1(I,6) =  5
          PAR2(I,6) = 10
       enddo   
C
       CALL ZERO ( RUNSM, 5, 6 ) 
C
       CALL STONFLY ( Y, X, U, V, RUNSM )
C
       DO I = 1, 5
          IF ( RUNSM(I,6) .LT . 30 ) THEN
             CALL MKRNSM ( PAR1, RUNSM )
             CALL MKRNSM ( PAR2, RUNSM )
             GO TO 10
          ENDIF
       enddo
c
   10  CONTINUE
C
       CALL MKSTAT(RUNSM,PAR1)
C
       DO I = 1, 5
c
c**   this section causes total bias to be within 62.5 miles.  If bias is
c**   adjusted downward...std devs are udjusted upward accordingly.
c
          xb = par1(i,1)
          sx = par1(i,2)
          yb = par1(i,3)
          sy = par1(i,4)
c
          zz = sqrt( xb**2 + yb**2 )
c
          if (zz .gt. aa ) then
c
             axb = (aa/zz)*xb
             ayb = (aa/zz)*yb
c
             sx = sqrt ( sx**2 + ( axb - xb )**2 )
             sy = sqrt ( sy**2 + ( ayb - yb )**2 )
c
             par1(i,1) = axb
             par1(i,2) = sx
             par1(i,3) = ayb
             par1(i,4) = sy
c
          endif
c
c**   now store the final stats for return to indata
c
          DO J = 1, 5
             STD(I,J) = PAR1(I,J)
          enddo
C
      enddo
c
      RETURN
      END
C**********************************************************************
       SUBROUTINE FIRSTGU ( X, Y, U, V, PAR2, RUNSM )
c
c**    Generates the first guess
C
       COMMON /parameter/NDTG,MXW
c
       REAL RUNSM(5,6),STATS(7,6,5,21),PAR2(5,6)
       integer path_end
c
       CHARACTER*50 prob_path
       CHARACTER*75 file_name
C
       IYR  = NDTG/1000000
       MOYR = NDTG/10000
       IDA  = NDTG/100 - 100*MOYR
       XMO  = MOYR - 100*IYR + FLOAT(IDA)/30.0
c
       XMW = MXW
C
c**   Prepare the file name, open the file, read the data and 
c**     close the file
c
       call getenv ( "ATCFPROBLTY", prob_path )
       path_end  = index ( prob_path, " " ) - 1
       file_name = prob_path(1:path_end)//'/errparam.dat'
c
       OPEN ( 41, FILE=file_name, STATUS='OLD' )
C
       DO M = 1,999
          READ ( 41, 1, END=25 ) I, K, L, ( STATS(I,J,K,L), J = 1, 6 )
   1      FORMAT (3I3,4F7.1,F7.3,F5.0)
       enddo
C
  25   CLOSE ( 41 )
C
       IX = iKINDEX(  20.0, 100.0, 5.0,   X )
       IY = iKINDEX(   5.0,  50.0, 5.0,   Y )
       IU = iKINDEX( -20.0,  30.0, 5.0,   U )
       IV = iKINDEX(  -5.0,  30.0, 5.0,   V )
       IM = iKINDEX(   6.0,  12.0, 1.0, XMO )
       IW = iKINDEX(  25.0, 130.0, 5.0, XMW )
C
       DO II = 1, 5
          DO JJ = 1,6
             PAR2(II,JJ) = STATS(1,JJ,II,IX)
          enddo
       enddo
c
       CALL MKRNSM ( PAR2, RUNSM )
C
       DO II = 1, 5
          DO JJ = 1, 6
             PAR2(II,JJ) = STATS(2,JJ,II,IY)
          enddo
       enddo   
C
       CALL MKRNSM ( PAR2, RUNSM )
C
       DO II = 1, 5
          DO JJ = 1, 6
             PAR2(II,JJ) = STATS(3,JJ,II,IU)
          enddo
       enddo
c   
       CALL MKRNSM ( PAR2, RUNSM )
C
       DO II = 1, 5
          DO JJ = 1, 6
             PAR2(II,JJ) = STATS(4,JJ,II,IV)
          enddo
       enddo
c   
       CALL MKRNSM ( PAR2, RUNSM )
C
       DO II = 1, 5
          DO JJ = 1, 6
             PAR2(II,JJ) = STATS(5,JJ,II,IV)
          enddo
       enddo
c   
       CALL MKRNSM ( PAR2, RUNSM )
C
       DO II =1, 5
          DO JJ = 1,6
             PAR2(II,JJ) = STATS(6,JJ,II,IV)
          enddo
       enddo
c   
       CALL MKRNSM ( PAR2, RUNSM )
C
       RETURN
       END
C**********************************************************************
       SUBROUTINE CLS_STS ( Y, X, PAR1 )
C
C**
C
       REAL PAR1(5,6)
       integer path_end
c
       CHARACTER*50 prob_path
       CHARACTER*75 file_name
C
c**   Prepare the file name, open the file, read the data and 
c**     close the file
c
       call getenv ( "ATCFPROBLTY", prob_path )
       path_end  = index ( prob_path, " " ) - 1
       file_name = prob_path(1:path_end)//'/errparam.set'
c
       OPEN ( 42, FILE=file_name, STATUS='OLD' )
C
       IS = IGETST ( Y, X )
C
       DO L = 1, IS
          DO I = 1, 5
             READ ( 42, * ) IDUM, (PAR1(I,J), J = 1, 6 )
  35         FORMAT(3X,4F7.1,F7.3,F5.0)
          enddo
       enddo
C
       CLOSE ( 42 )
C
       RETURN
       END
c*********************************************************************
       subroutine stonfly ( y, x, u, v, runsm )
c
c**
c
       COMMON /parameter/NDTG,MXW
       common /sid/ ex(5,200),ey(5,200),meas(5,200),
     & tex(5,100),tey(5,100),tmeas(5,100),mcum(5,250),item(6,8)
c
       real runsm(5,6)
c
       real fla,flo,vla,vlo,wnd,prs,hdg,spd
       integer*2 ex,ey,meas,tex,tey,tmeas,nos(5),mcum,item
cc       integer*2 ex,ey,meas,tex,tey,tmeas,best,nos(5),mcum,item
       integer first,last,idatim,best
       real measur
       integer path_end
c
       character*1  stat(6)
       character*2  file_ndx
       character*8  name
       character*50 fname
       CHARACTER*50 prob_path
       CHARACTER*75 file_name1, file_name2
c
       data rpdg/.0174533/
C
       data nos/5*0/
c
       iyr  = ndtg/1000000
       moyr = ndtg/10000
       ida  = ndtg/100 - 100*moyr
       xmo  = moyr - 100*iyr + float(ida)/30.0
c
      yr   = iyr
      xmw  = mxw
      maxm = 250
c
c**   Prepare the file name, open the file, read the data and 
c**     close the file
c
      call getenv ( "ATCFPROBLTY", prob_path )
      path_end  = index ( prob_path, " " ) - 1
      is = igetst( y, x )
      write ( file_ndx, '(i2.2)' ) is
      file_name1 = prob_path(1:path_end)//'/errndx'//file_ndx//'.dat'
c
      OPEN ( 43, FILE=file_name1, STATUS='OLD' )
C
c**   Prepare the file name, open the file, read the data and 
c**     close the file
c
      file_name2 = prob_path(1:path_end)//'/err7098.dac'
c
      OPEN ( 44, FILE=file_name2, STATUS='OLD',
     & ACCESS='DIRECT', FORM='UNFORMATTED', RECL=114,
     & IOSTAT=IOS,ERR=1010)
C
       index1 = 2
c
       do 110 nost = 1, 9999
          read ( 43, 6, end=115 ) name, idatim, first, last
   6      format(a8,i11,2i5)
          nn=0
          best=1
          do 100 i = first, last
             nn =nn + 1
             read ( 44, rec=i, IOSTAT=IOS, ERR=1020) idatim, name,
     &            (( item(j,l), l= 1, 8 ), stat(j), j = 1, 6 )
c
              do j = 1, 5
                 tmeas(j,nn) = 999
              enddo
c
cajs  Tested with and w/o int4, no difference.  idatim is already i*4.
cajs              year = int4(idatim/1000000)
              year = idatim/1000000
              moyr = idatim/10000
              ida  = idatim/100 - 100*moyr
              cmo  = moyr - 100*year + float(ida)/30.0
c
              hdg = item(1,7)/10.0
              if ( hdg .lt. 0 ) goto 100
C
C**   LINE ADDED BY GROSS 3/20/96
C
               SPD = ITEM(1,8)/10.0
C
               w  = item(1,5)/10.0
               xc = item(1,4)/10.0
               yc = item(1,3)/10.0
               xf = item(1,2)/10.0
               yf = item(1,1)/10.0
c
               uc = spd*sin(hdg*rpdg)
               vc = spd*cos(hdg*rpdg)
c
               xx=measur(u,v,x,y,yr,xmo,xmw,uc,vc,xc,yc,year,cmo,w)
c
               mm = amin1( amax1( 1.0, Xx ), 250.0)
               if (mm .lt. tmeas(1,best) ) best = nn
c
               if (yc .gt. 0.0 .and. yf .gt. 0.0 ) then
                  do 90 j = 1, 6
                     jj=j
                     if ( j .eq. 4 ) goto 90             
                     if ( j .gt. 4 ) jj = j - 1
                     vla = item(j,3)/10.0
                     fla = item(j,1)/10.0
                     if ( fla .lt. 0.0 .or. vla .lt. 0.0 ) goto 90
                     vlo = item(j,4)/10.0
                     flo = item(j,2)/10.0
c
                     call errgc (yc,xc,yf,xf,vla,vlo,fla,flo,
     *                           xerr,yerr,verr,hdg,index1)
                     tex(jj,nn) = xerr
                     tey(jj,nn) = yerr
                     tmeas(jj,nn) = mm
  90              continue
               endif
 100      continue
c
c**      nn is # of cases this storm of which best is closest fit
c
c**      following section assures forecasts are not used from the same 
c**      storm unless they are at least 48-h apart.
c
          if (nn .eq. 0 ) goto 110
          first = jmod( best, 8 )
          if (first .eq. 0 ) first = 8
          last = nn
          if ( first .gt. nn ) then
             first = best
             last  = best
          endif
c
          do l = first, last, 8
             if ( l .gt. last ) goto 110
             do j = 1, 5
                if ( tmeas(j,l) .ne. 999 ) then
                   nos(j) = nos(j) + 1
                   nosj   = nos(j)
                   meas(j,nosj) = tmeas(j,l)

                   ex(j,nosj) = tex(j,l)
                   ey(j,nosj) = tey(j,l)
                   kk = tmeas(j,l)
                   if ( kk .lt. maxm ) mcum(j,kk) = mcum(j,kk) + 1
                endif
             enddo     
          enddo
c
 110   continue
 115   continue
c
       close ( 43 )
       close ( 44 )
c
       do 150 j=1,5
           last=maxm
           msum=0
           do 120 m=1,maxm
              msum=msum+mcum(j,m)
              if(msum.Ge.40)Then
                 last=m
                 goto 125
              endif
 120  continue
 125  continue
c
        nrec=nos(j)
      do 140 i=1,nrec
           if(meas(j,i).Le.Last)then
cc             write (27,130)j,i,meas(j,i),last,ey(j,i),ex(j,i)
cc 130            format(6i5)
              if(ey(j,i).Ne.-999)Then
                   runsm(j,1)=runsm(j,1)+ex(j,i)
                   runsm(j,2)=runsm(j,2)+ex(j,i)**2
                   runsm(j,3)=runsm(j,3)+ey(j,i)
                   runsm(j,4)=runsm(j,4)+ey(j,i)**2
                   runsm(j,5)=runsm(j,5)+ex(j,i)*ey(j,i)
                   runsm(j,6)=runsm(j,6)+1.
              endif
         endif
 140     continue
 150  continue
c
      return
C
C**   ERROR MESSAGES
C
 1010 PRINT *, ' *** ERROR *** OPENING ERR7097.DAC FILE...IOS = ',IOS
      STOP
C
 1020 PRINT *, ' *** ERROR *** READING ERR7097.DAC FILE...IOS = ',IOS
      STOP
C
      END
C*********************************************************************
      FUNCTION iKINDEX ( XMIN, XMAX, DEL, PARAM )
c
c**
c
      LIM  = (XMAX - XMIN)/DEL + 0.5
      XLIM = LIM
c
      iKINDEX = MIN1( XLIM, aMAX1( 1.0, 1.0 + (PARAM - XMIN)/DEL )) 
cc      KINDEX=AMIN0(XLIM,AMAX0(1.,1.+(PARAM-XMIN)/DEL))
c
      RETURN
      END
C*********************************************************************
      SUBROUTINE ZERO ( FIELD, IU, JU )
c
c**   zeros an array
c
      REAL FIELD(IU,JU)
c
      DO I = 1, IU
         DO J = 1, JU
            FIELD(I,J) = 0
         enddo
      enddo   
c
      RETURN
      END
C*********************************************************************
      SUBROUTINE MKRNSM ( STATS, RUNSM )
c
c**
c
      REAL STATS(5,6), RUNSM(5,6)
c
      DO I = 1, 5
c
         XB = STATS(I,1)
         SX = STATS(I,2)
         YB = STATS(I,3)
         SY = STATS(I,4)
         CC = STATS(I,5)
         XN = STATS(I,6)
c
         RUNSM(I,1) = RUNSM(I,1) + XN*XB
         RUNSM(I,2) = RUNSM(I,2) + XN*( SX**2 + XB**2 )
         RUNSM(I,3) = RUNSM(I,3) + XN*YB
         RUNSM(I,4) = RUNSM(I,4) + XN*( SY**2 + YB**2 )
         RUNSM(I,5) = RUNSM(I,5) + XN*( CC*SX*SY + XB*YB )
         RUNSM(I,6) = RUNSM(I,6) + XN
      enddo
c
      RETURN
      END
C*********************************************************************
      SUBROUTINE MKSTAT ( RUNSM, STATS )
c
c**
c
      REAL STATS(5,6), RUNSM(5,6)
c
      DO I = 1, 5
         XN = RUNSM(I,6)
         XB = RUNSM(I,1)/XN
c
         SX = SQRT( RUNSM(I,2)/XN - XB**2 )
         YB = RUNSM(I,3)/XN
         SY = SQRT( RUNSM(I,4)/XN - YB**2 )
         CC = ( RUNSM(I,5)/XN - YB*XB )/( SX*SY )
c
         STATS(I,1) = XB
         STATS(I,2) = SX
         STATS(I,3) = YB
         STATS(I,4) = SY
         STATS(I,5) = CC
         STATS(I,6) = XN
c
      enddo
c
      RETURN
      END
C***********************************************************************
      FUNCTION MEASUR ( U1, V1, X1, Y1, A1, M1, W1,
     &                  U2, V2, X2, Y2, A2, M2, W2 )
c                       u   v   x   y   yr  mo  wi
c
c**
c
      REAL EPS(7), M1, M2, MEASUR
c
      DATA EPS / 0.79, 0.82, -4.02, 0.68, -1.00, 0.21, -8.24 /
c
      D1 = (U1 - U2)/EPS(1)
      D2 = (V1 - V2)/EPS(2)
      D3 = (X1 - X2)/EPS(3)
      D4 = (Y1 - Y2)/EPS(4)
      D5 = (A1 - A2)/EPS(5)
      D6 = (M1 - M2)/EPS(6)
      D7 = (W1 - W2)/EPS(7)
c
      MEASUR = ABS( D1 + D2 + D3 + D4 + D5 + D6 + D7 )
c
      RETURN
      END
C***********************************************************************
      FUNCTION IGETST ( Y, X )
c
c**
c
      real ybar(12), xbar(12)
c
      data ybar/2*15.,17.,20.,27.5,26.,32.5,24.,22.,3*38./
      data xbar/35.,55.,72.,2*90.,77.,65.,55.,2*35.,55.,75./
C
      dmin = 99999.0
c
      do k = 1, 12
c
         call LL2DB ( Y, X, ybar(k), xbar(k), DIST, BEAR )
c
         if ( dist .lt. dmin ) then
            dmin = dist
            imin = k
         endif
c
      enddo
c 
      if ( imin .ge. 1 .and. imin .le. 12 ) IGETST = IMIN
c
      RETURN
      END
c*******************************************************************
      SUBROUTINE USEARY ( P, XCEN, YCEN, XOFF, YOFF, SX, SY, RHO, R )
C
C**   INTERGRATES BIVARIATE NORMAL OVER CIRCLE OF RADIUS
C**   CENTERED AT DISTANCE D FROM ORGIN BY TABLE LOOKUP
C**   D IS GIVEN BY VECTOR(XCEN-XOFF)+(YCEN+YOFF)
C**   XCEN IS DISTANCE OF FCST EAST OF POINT OF INTEREST(NMI)+
C**   THE MEAN W-E FCST ERROR. XOFF IS THE CIRCLE OFFSET
C**   TO ALLOW FOR ASSYMETRY ATTRIBUTED TO SPEED.
C**   SIMILARLY FOR YCEN AND YOFF IN NORTH DIRECTION
C**   ENTRY USEARY READS IN TABLE
C**   ENTRY NEWPT USED WHEN EITHER POINT OF INTEREST OR
C**   FORECAST TIME CHANGES FROM PREVIOUS CALL.
C**   ENTRY NEWRAD USED WHEN ONLY R CHANGES FROM LAST CALL.
C
c
      save pi
c
      DIMENSION PI(80,30)
      integer path_end
c
      CHARACTER*50 prob_path
      CHARACTER*75 file_name
C
C**   THE ONLY CALL TO THIS SUBROUTINE INITIALIZES THE PROBABILITY ARRAY
C**      ALL OTHER CALLS ARE THROUGH THE ENTRY POINTS:  NEWPT AND NEWRAD
C
c**   Prepare the file name, open the file, read the data and 
c**     close the file
c
      call getenv ( "ATCFPROBLTY", prob_path )
      path_end  = index ( prob_path, " " ) - 1
      file_name = prob_path(1:path_end)//'/problty.dat'
c
      OPEN  ( 45, FILE=file_name, STATUS='OLD', IOSTAT=IOS, ERR=1010)
C
      READ  ( 45, '(10F7.6)' ) (( PI(I,J), J = 1,30 ), I = 1,80 )
C
      CLOSE ( 45 )
C
      RETURN
C
 1010 PRINT *, ' *** ERROR *** OPENNING THE PROBABILITY DATA FILE = ',
     & IOS
      STOP
C
C**   ENTRY NEWPT USED WHEN EITHER POINT OF INTEREST OR
C**   FORECAST TIME CHANGES FROM PREVIOUS CALL.
C
      ENTRY NEWPT ( P, XCEN, YCEN, XOFF, YOFF, SX, SY, RHO, R )
C
      THETA = 0.5*ATAN(2.0*RHO*SX*SY/(SX*SX - SY*SY))
      SINT = SIN(THETA)
      COST = COS(THETA)
      TERM2 = 2.0*RHO*SY*SX*SINT*COST
      ST = (SY*SINT)**2 + TERM2 + (SX*COST)**2
      SS = (SY*COST)**2 - TERM2 + (SX*SINT)**2
C
C**   ENTRY NEWRAD USED WHEN ONLY R CHANGES FROM LAST CALL.
C
cc      ENTRY NEWRAD (P,XCEN,YCEN,XOFF,YOFF,SX,SY,RHO,R)
      DSTX = XCEN - XOFF
      DSTY = YCEN - YOFF
      DSTXY = SQRT(DSTX*DSTX + DSTY*DSTY)
      DSTT = DSTY*SINT + DSTX*COST
      DSTS = DSTY*COST - DSTX*SINT
      DST = SQRT(DSTT*DSTT/ST + DSTS*DSTS/SS)
      DST2 = 2.0*DST
C
      XJ = AMIN1(79.0,DST2 + 1.0)
      J = XJ
      D = (J - 1)*0.5
      RL = AMAX1(0.0,D - 3.5)
      RU = RL + 7.0
      DR = (RU - RL)/28.0
      DJ = D + 0.5
      RLJ = AMAX1(0.0,DJ - 3.5)
      RUJ = RLJ + 7.0
      DRJ = (RUJ - RLJ)/28.0
      WT = (DST - D)*2.0
      P1DF = PI(J,30)
      P2DF = PI(J + 1,30)
C
      DSTX = 1
      DSTY = 1
      DSTXY = 1.414214
      DSTT = SINT + COST
      DSTS = COST - SINT
      DST = SQRT(DSTT*DSTT/ST + DSTS*DSTS/SS)
C
      P = 0
      RIN = DST*R/DSTXY
      P1 = 0
      TI = 1 + (RIN - RL)/DR
C
      IF (TI.LT.1.0) GO TO 20
      P1 = P1DF
C
      IF (TI.GE.30.0) GO TO 20
      I = TI
      A = RL + (I - 1)*DR
      B = A + DR
      P1 = PI(J,I)
      P1 = P1 + (RIN - A)/(B - A)*(PI(J,I + 1) - P1)
C
  20  P2 = 0
      TI = 1 + (RIN - RLJ)/DRJ
C
      IF (TI.LT.1.0) GO TO 30
      P2 = P2DF
C
      IF (TI.GE.30) GO TO 30
      I = TI
      A = RLJ + (I - 1) * DRJ
      B = A + DRJ
      P2 = PI(J + 1,I)
      P2 = P2 + (RIN - A)/(B - A)*(PI(J + 1,I + 1) - P2)
C
   30 P = P1 + WT*(P2 - P1)
C
      RETURN
      END
C**********************************************************************
      SUBROUTINE INDATA ( MAXTIM, RADU, RADL, ANG, std )
C
C**
C
C**   17 MAY 1989  REVISED TO INCLUDE 36 HR PROBABILITIES.

C**   09 JUN 1989  ADDITIONAL REVISION WITHIN LOOP 600.  CJM.
C
      COMMON /parameter/NDTG,MXW
      COMMON /ltlnint/LAT00,LON00,LAT12,LON12,LAT24,LON24,
     & LAT36,LON36,LAT48,LON48,LAT72,LON72
      COMMON /Z/P(10,25)
C
      REAL STD(5,5),X(6)
C
C**   DEFINE INTERNAL FUNCTIONS
C
      FI(T,A,B,C) = (2.0*A + T*(4.0*B - C - 3.0*A +
     & T*(C - 2.0*B + A)))/2.0
      FD(T,A,B,C) = A*(T - 1.5) - 2.0*B*(T - 1.0) + C*(T - 0.5)
C
      RAD12B = 0.5*(RADU - RADL)
      RAD    = 0.5*(RADU + RADL)
C
C**   THE FOLLOWING SECTION ASSIGNS PROPER MEANS, STDEV + RHO
C
C**   P(1,I)  = EW MEAN ERROR,I=1,25=0,72 HRS, 3 HRS
C**   P(2,I)  = EW STDEV
C**   P(3,I)  = SN MEAN ERROR
C**   P(4,I)  = SN STDEV
C**   P(5,I)  = COR COEF EW ERROR TO NS ERROR
C**   P(6,I)  = LAT (TENTHS OF DEG. N)
C**   P(7,I)  = LONG (TENTHS OF DEG,. E)
C**   P(8,I)  = W-E OFFSET IN NMI
C**   P(9,I)  = S-N OFFSET IN NMI
C**   P(10,I) = MAGNITUDE OF THE OFFSET
C
c
      DO L = 1, 5
C
         DO JJ = 1, 5
            J = MAX0(1,JJ*8 - 15)
            IF (JJ.EQ.2) J = 5
            P(L,J) = STD(JJ,L)
         enddo
C
         X1 = P(L,1)
         X2 = P(L,5)
         X3 = P(L,9)
         DO J = 2, 8
            T = (J - 1.0)/4.0
            P(L,J)=FI(T,X1,X2,X3)
         enddo
C
         X1 = P(L,25)
         X2 = P(L,17)
         DO J = 10, 24
            T = (J - 9.0)/8.0
            P(L,J) = FI(T,X3,X2,X1)
         enddo
C
      enddo   
C
C**   THE FOLLOWING SECTION LOADS P(6-10,I) AT FORECAST TIMES
C**         I = 1 = O HRS, I = 5 = 12 HRS, I = 9 = 24 HRS ....
C
      P(6,1)  = LAT00
      P(7,1)  = LON00
      P(8,1)  = -RAD12B*COS(ANG)
      P(9,1)  =  RAD12B*SIN(ANG)
      P(10,1) = RAD
      MAXTIM  = 0
C
      IF ( LAT12 .le. 0 ) return
c
      P(6,5) = LAT12
      P(7,5) = LON12
      MAXTIM = 12
C
      IF ( LAT24 .gt. 0 ) then
         P(6,9) = LAT24
         P(7,9) = LON24
         MAXTIM = 24
C
C**                                       INSERTED 5/17/89  CJM
c
         IF ( LAT36 .gt. 0 ) then
            P(6,13) = LAT36
            P(7,13) = LON36
            MAXTIM = 36
C
C**                                                 END OF CHANGE
C
            IF ( LAT48 .gt. 0 ) then
               P(6,17) = LAT48
               P(7,17) = LON48
               MAXTIM = 48
C
               IF ( LAT72 .gt. 0 ) then
                  P(6,25) = LAT72
                  P(7,25) = LON72
                  MAXTIM = 72
c
               endif
            endif
         endif
      endif   
C
C**                                              INSERTED 5/17/89 CJM
C
  400 IF ( MAXTIM .GT. 0 ) GO TO 401
      P(6,5) = P(6,1)
      P(7,5) = P(7,1)
c
  401 IF ( MAXTIM .GT. 12 ) GO TO 402
      P(6,9) = 2.0*P(6,5) - P(6,1)
      P(7,9) = 2.0*P(7,5) - P(7,1)
C
C**   INTERPOLATE LAT, LON 3-18 HRS (3-21 IF NO 36H) USING 0, 12, 24
C
  402 Y1 = P(6,1)
      Y2 = P(6,5)
      Y3 = P(6,9)
      X1 = P(7,1)
      X2 = P(7,5)
      X3 = P(7,9)
      LOW = 2
      LAST = 7
      IF (MAXTIM .EQ. 24) LAST = 8
C
      DO J = LOW, LAST
         T = (J - 1.0)/4.0
         P(6,J) = FI(T,Y1,Y2,Y3)
         P(7,J) = FI(T,X1,X2,X3)
      enddo   
C
      IF (MAXTIM .LE. 24) GO TO 500
      LOW = LAST + 1
      LAST = 11
      IF (MAXTIM .EQ. 36) LAST = 12
C
C**   LOAD 36 HR POSIT INTO Y1, X1 REPLACING 0 HR POSIT
C
      Y1 = P(6,13)
      X1 = P(7,13)
C
      DO J = LOW, LAST
         T = (J - 5.0)/4.0
         P(6,J) = FI(T,Y2,Y3,Y1)
         P(7,J) = FI(T,X2,X3,X1)
      enddo   
C
      IF ( MAXTIM .EQ. 36 ) GO TO 500
      LOW = LAST + 1
      LAST = 15
      IF ( MAXTIM .EQ. 48 ) LAST = 16
C
C**   LOAD 48 HR POSIT INTO Y2, X2 REPLACING 12 HR POSIT
C
      Y2 = P(6,17)
      X2 = P(7,17)
C
      DO J = LOW, LAST
         T = (J - 9.0)/4.0
         P(6,J) = FI(T,Y3,Y1,Y2)
         P(7,J) = FI(T,X3,X1,X2)
      enddo   
C
      IF ( MAXTIM .EQ. 48 ) GO TO 500
      LOW = LAST + 1
      LAST = 24
C
C**   LOAD 72 HR POSIT INTO Y1, X1 REPLACING 36 HR POSIT
C
      Y1 = P(6,25)
      X1 = P(7,25)
C
      DO J = LOW, LAST
         T = (J - 9.0)/8.0
         P(6,J) = FI(T,Y3,Y2,Y1)
         P(7,J) = FI(T,X3,X2,X1)
      enddo
c
  500 continue 
C
      DO 600 J = 1, LAST
      P(10,J) = RAD
C
C**                                                 INSERT 6/9/89 CJM
C
      IF (J .EQ. 1) GO TO 600
      DY = FD(.5, P(6,J-1), P(6,J), P(6,J+1) )
      DX = FD(.5, P(7,J-1), P(7,J), P(7,J+1) )
      DST = SQRT(DY*DY + DX*DX)
C
C**   THE FOLLOWING PATCH WAS ADDED FOR STATIONARY SYSTEMS 99/10/05
C
      IF (DST .LE. 0.0) THEN
         P(8,J) = 0.0
         P(9,J) = 0.0
      ELSE
         P(8,J) = -RAD12B * DY/DST
         P(9,J) =  RAD12B * DX/DST
      ENDIF
C
C**   END OF PATCH 99/10/05
C
  600 CONTINUE
C
      DY = FD(1.0, P(6,LAST-1), P(6,LAST), P(6,LAST+1) )
      DX = FD(1.0, P(7,LAST-1), P(7,LAST), P(7,LAST+1) )
      DST = SQRT(DY*DY + DX*DX)
C
C**   THE FOLLOWING PATCH WAS ADDED FOR STATIONARY SYSTEMS 99/10/05
C
      IF (DST .LE. 0.0) THEN
         P(8,LAST + 1) = 0.0
         P(9,LAST + 1) = 0.0
      ELSE
         P(8,LAST + 1) = -RAD12B * DY/DST
         P(9,LAST + 1) =  RAD12B * DX/DST
      ENDIF
C
C**   END OF PATCH 99/10/05
C
      P(10,LAST+1) = P(10,LAST)
C
C**                                              END OF INSERT 6/9/89
C**                                              END OF CHANGE
C
   66 CONTINUE
C
      RETURN
      END
C**********************************************************************
      SUBROUTINE XTRAST ( maxt, ang, nsta, stanam, psvg )
C
C**   17 MAY 1989 CHANGED TO ELIMINATE OUTPUT OF CASES HAVING
C**                PROBABILITIES OF 1%.
C
      COMMON /ltlnchr/      latlon(7)
      common /ltlnflt/   flat(7), flon(7)
      COMMON /Z/      P(10,25)
c
      dimension IDEN2(150), IDEN4(150)
      dimension pov(25),psv(25)
c
      INTEGER PSV3(25),PSVG(25,150)
      integer path_end
c
C
      CHARACTER*1  EW,NS,E,iden3(150),iden5(150),xw
      character*4  iden1(150) 
      character*12 latlon
      character*16 stanam(150)
      CHARACTER*50 prob_path
      CHARACTER*75 file_name
C
      DATA  E / 'E' /
      data xw / 'W' /
C
      IUP = MAXT/3 + 1
c
c**   Prepare the probability forecast points and station list
c
      NSTA = 0
C
      DO I = 1, 3
         NSTA = NSTA + 1
         IDEN1(NSTA)  = 'XTRA'
         IDEN2(NSTA)  = FLAT(I + 3)*10.0
         IDEN3(NSTA)  = 'N'
         IDEN4(NSTA)  = FLON(I + 3)*10.0
         IDEN5(NSTA)  = 'W'
         STANAM(NSTA) = latlon(i + 3)
      enddo
C
C**   OPEN AND READ THE PROBABILITY STATION FILE
C
C
c**   Prepare the file name, open the file, read the data and 
c**     close the file
c
       call getenv ( "ATCFPROBLTY", prob_path )
       path_end  = index ( prob_path, " " ) - 1
       file_name = prob_path(1:path_end)//'/pstation.dat'
c
       OPEN ( 46, FILE=file_name, STATUS='OLD', IOSTAT=IOS, ERR=1010 )
C
 10   NSTA = NSTA + 1
      READ ( 46, '(A4,I4,A1,I4,A1,5X,A16)', END=20 ) IDEN1(NSTA),
     &        IDEN2(NSTA), IDEN3(NSTA), IDEN4(NSTA), IDEN5(NSTA),
     &        STANAM(NSTA)
      GO TO 10
C
 20   close ( 46 )
      NSTA = NSTA - 1
C
c**
c
      do K = 1, nsta
c
         IYP = IDEN2(K)
         NS  = IDEN3(K)
         IXP = IDEN4(K)
         EW  = IDEN5(K)
c
         IF (EW.EQ.E) go to 30
         IXP = 3600 - IXP
         EW = E
 30      CONTINUE
C
         DO I = 1, iup
            PSV3(I) = 0
         enddo
C
         YP = float(IYP)
         XP = float(IXP)
C
C**   INSERTED CALL TO STRIKE 5/17/89  CJM.
C**   CHANGED OUTPUT ARGUMENT FROM POUT TO PSV3 6/7/89  CJM.
C
         CALL DIRDST (    YP/10.0,     XP/10.0, 
     &                P(6,1)/10.0, P(7,1)/10.0, A, D1 )
         IF ( D1 .GT. 200.0 ) go to 40
C
         CALL DIRDST (    YP/10.0,     XP/10.0,
     &                P(6,2)/10.0, P(7,2)/10.0, A, D2 )
         IF ( D1 .GT. 62.5 .AND. D2 .GT. 62.5 ) go to 40
C
         DO J = 1, iup
            PSV3(J) = 99
         enddo
C
         go to 50
C
 40      IF ( EW .EQ. XW ) XP = 3600.0 - XP
C
         CALL PROVR ( MAXT, XP, YP, POV, PSV, ANG )
C
C**   POV(J), PSV(J) ARE INSTANTANEOUS AND TIME INTEG PROPS
C**   J=1, 25=0, 72 HOURS IN 3 HOUR STEPS.
C
         DO I = 1, IUP
            PSV3(I)= 100.0*PSV(I) + 0.5
         enddo   
C
 50      continue
c
         DO J = 1, iup
            PSVG(J,K) = PSV3(J)
         enddo
c
      enddo   
c
      return
c
 1010 print *, ' cannot open pstation data - error = ', ios
      stop
c
      END
C**********************************************************************
      SUBROUTINE PARRAY ( maxt, ang, arrayp )
C
C**   17 MAY 1989 CHANGED TO ELIMINATE OUTPUT OF CASES HAVING
C**                PROBABILITIES OF 1%.
C
      COMMON /Z/ P(10,25)
c
      dimension pov(25),psv(25)
c
      integer tout(20,12)
      real    arrayp(96,60)
c
      IUP = MAXT/3 + 1
C
c**   The following loop will calculate probabilities at 5 degree intervals
c**     to be used later as a test to avoid calculating essentially zero
c**     probabilities.  Values stored are truncated to 1/1000.
c
      jout = 0
c
      do jj = 5, 60, 5
c
	  jout = jout + 1
	  iyp = 10*jj
	  iout = 0
c
	  do ii = 15, 110, 5
c
	      iout = iout + 1
	      ixp = 3600 - ii*10
C
              i1000 = 0
c
              yp = float( iyp )
              xp = float( ixp )
c
              do i = 1, 25, 8
C
                 if ( p(6,i) .eq. 0 ) goto 10
c
                 CALL DIRDST (        YP/10.0, XP/10.0, P( 6, i )/10.0, 
     &                         P( 7, i )/10.0,       A, dst )
C
                 if ( dst .lt. 1000.0 ) then
                    i1000 = 1
                    goto 10
                 endif
c
              enddo
c
 10           continue
c
	      IF ( i1000 .eq. 1 ) then
		  tout( iout, jout ) = 1
	      else
		  CALL PROVR ( MAXT, XP, YP, POV, PSV, ANG )
		  if ( psv(IUP) .gt. 0.001 ) tout( iout, jout ) = 1
	      endif
C
   	  enddo
      enddo
c
      do jj = 1, 60
c
	 iYP = 10*jj
	 jblo = max0(  1, jint(   float(jj)/5.0 ) )
	 jabv = min0( 12, jint( ( float(jj) + 5.0 )/5.0 ) )
c
	 do 40 ii = 15, 110
c
	    iXP = 3600 - ii*10
	    iblo = max0(  1, jint( (float(ii) - 10.0 )/5.0 ) )
	    iabv = min0( 20, jint( (float(ii) -  5.0 )/5.0 ) )
c
            yp = float( iyp )
            xp = float( ixp )
c
	    iout = ii - 14
	    arrayp( iout, jj ) = 0.0
c
c**   Test to see if any of the four corner probabilities are
c**     greater than > 1/1000.
c
	    itest = tout( iabv, jabv ) + tout( iabv, jblo ) +
     &              tout( iblo, jblo ) + tout( iblo, jabv )
	    if ( itest .eq. 0 ) goto 40
C
            CALL DIRDST (     YP/10.0,     XP/10.0, 
     &                    P(6,1)/10.0, P(7,1)/10.0, A, D1 )
C
            IF ( D1 .GT. 200.0 ) goto 30
C
            CALL DIRDST (     YP/10.0,     XP/10.0, 
     &                    P(6,2)/10.0, P(7,2)/10.0, A, D2 )
C
            IF ( D1 .GT. 62.5 .AND. D2 .GT. 62.5 ) goto 30
C
            arrayp( iout, jj ) = 99.9
            goto 40

 30         continue
c
            CALL PROVR ( MAXT, XP, YP, POV, PSV, ANG )
c
            arrayp( iout, jj ) = 100.0*psv(IUP)
C
 40	continue
c
      enddo
c
      return
      end
C**********************************************************************
      SUBROUTINE PROVR ( MAXT, X0, Y0, POV, PSV, ANG )
C
C**   PROVR CALCULATES THE PROBABILITY OF WINDS OF AT LEAST VL AND VU
C**   IN KNOTS AT THREE HOUR TIME STEPS IN AN INSTANTANEOUS MODE (POV) AND
C**   A TIME SUMMED MODE (PSV).  REQUIRED ARE COEFFICIENTS OF
C**   REGRESSION EQUATIONS THAT PREDICT MAX WIND (STORED IN CV) AND
C**   RADIUS OF MAX WIND (STORED IN CR).  THE PREDICTIONS ARE
C**   PERFORMED BY SUBROUTINE EVREG.   THE TROPICAL CYCLONE
C**   FORECAST HAS BEEN INTERPOLATED TO 3 HOUR TIME STEPS AND
C**   TOGETHER WITH INTERPOLATED STATISTICAL INFORMATION IS STORED
C**   IN ARRAY P.
C
C**   17 MAY 1989  CHANGED DIMENSION OF W FROM 24 TO 26.  CJM.
C
      COMMON/Z/ P(10,25)
C
      REAL PSB4,PTP
      REAL POV(25),PSV(25),PB4
C
      DATA SMALL/1.E-4/
C
      IUP = 1 + MAXT / 3
C
C**   FOL LOOP INTEGRATES OVER SPACE IN THREE HOUR TIME STEPS AND
C**   SUMS OVER TIME.
C
      DO I = 1,IUP
c
         SX  = P(2,I)
         SY  = P(4,I)
         RHO = P(5,I)
         XM  = P(1,I)
         YM  = P(3,I)
         YF  = P(6,I)
         XF  = P(7,I)
c
         YB  = (YF - Y0)*6.0 + YM
         SCL = 6.0*COS(8.727E-4*(Y0 + YF))
         XB  = (XF - X0)*SCL + XM
c
         CALL XLATE(XB,YB,ANG)
c
         YP = P(9,I)
         XP = P(8,I)
c
         CALL XLATE(XP,YP,ANG)
c
         POV(I) = 0
         XPI    = XP
         YPI    = YP
C
C**
C
         CALL NEWPT ( PTP, XB, YB, XPI, YPI, SX, SY, RHO, P(10,I) )
C
         POV(I) = PTP
C
         IF (I .EQ. 1) THEN
            PSUM = PTP
         ELSE
C
C**
C
            CALL PINDW ( PSUM, PTP, A71, A61, XF, YF, A21, A41, SX, SY )
c
         ENDIF
C
         PSV(I) = PSUM
         A21 = SX
         A41 = SY
         A71 = XF
         A61 = YF
c
      enddo   
C
      RETURN
      END
C**********************************************************************
      SUBROUTINE PINDW ( PS, P2, X1, Y1, X2, Y2, EX1, EY1, EX2, EY2 )
C
C**   SUBROUTINE ESTIMATES PIN, THAT PORTION OF P2 WHISC IS INDEPENDENT
C**   OF P1.  P1 IS PROB OF BEING WITHIN CIRCLE CENTERED AT X1,Y1 WITH RAD
C**   RADIUS R1.  SAME RELATIONSHIP HOLDS FOR P2,X2,Y2,R2.  DF IS DIST
C**   BETWEEN CENTERS. DP = PROB EXCLUDED FROM P2: PIN=P2-DP=P2-PE1-PE2.
C**   DP IS PROB REPRESENTED BY OVERLAP OF CIRCLES.
C
      DATA PI,PIO/3.1415926,8.7266E-4/,PLOW,PTOP/.001,0.999/
C
      P1  = PS
      PST = 0
      PIN = P2
      IF (P2 - PTOP) 2,2,46
    2 IF (P1 - PTOP) 3,3,46
    3 IF (PLOW - P2) 4,4,44
    4 IF (PLOW - P1) 5,5,44
C
C**   FACT IS A CORRECTION THAT FORCES PIN TO APPROACH P2
C**   AS P1 APPROACHES ZERO.
C
    5 FACT = EXP(-13.86*P1)
      R1 = SQRT(-2.0*EX1*EY1*ALOG(1.0 - P1))
      R2 = SQRT(-2.0*EX2*EY2*ALOG(1.0 - P2))
      DX = (X2 - X1)*6.0*COS((Y2 + Y1)*PIO)
      DY = (Y2 - Y1)*6.0
      DF = SQRT(DX*DX + DY*DY)
C
C**   IF R1 + R2 .LT. DF  THEN THERE IS NO OVERLAP AND PIN=P2
C
      IF ((R1 + R2 - DF).LE.0.0) GO TO 40
C
C**   IF (ABS(R2 - R1).GT.DF) THEN ONE CIRCLE IS A SUBSET OF THE OTHER.
C**   THEN PIN = MAX(0,P2 - P1)
C
   10      IF ((ABS(R1 - R2) - DF).LT.0.0) THEN
C
                H1 = (DF + (R1*R1 - R2*R2)/DF)/2.0
                H2 = DF - H1
                PD2 = R2*R2*PI/2.0 - H2*SQRT(R2*R2 - H2*H2) -
     &           R2*R2*ASIN(H2/R2)
                PD1 = R1*R1*PI/2.0 - H1*SQRT(R1*R1 - H1*H1) -
     &           R1*R1*ASIN(H1/R1)
                R1SQ = 2.0*EX1*EY1
                R2SQ = 2.0*EX2*EY2
                HE1 = (R1*R1 - H1*H1)**1.5*2.0/3.0/PD1 - DF
                HE2 = (R2*R2 - H2*H2)**1.5*2.0/3.0/PD2 - DF
                PE1 = PD1/(PI*R2SQ)*EXP(-HE1*HE1/R2SQ)
                PE2 = PD2/(PI*R1SQ)*EXP(-HE2*HE2/R1SQ)
                PIN = AMAX1(0.0,(P2 - PE1 - PE2))
           ELSE
                PIN = AMAX1(0.0,(P2 - P1))
           ENDIF
C
   40 PIN = P2*FACT + PIN*(1.0 - FACT)
C
C**   PROBABILITIES ARE ADDED AS IF INDEPENDENT
C
CC    P(E1 + E2) = P(E1) + P(E2) - P(E1)*P(E2)
   44 PST = PS + PIN - PS*PIN
   46 PS = AMAX1(P1,P2,PS,PST)
C
      RETURN
      END
C**********************************************************************
      SUBROUTINE DIRDST ( YA, XA, YB, XB, AZ, DST )
C
C**
C
      DATA PIF,R/1.74533E-2,3422.2769/
C
      Y1 = YA * PIF
      X1 = XA * PIF
      Y2 = YB * PIF
      X2 = XB * PIF
      DX = X1 - X2
      DY = Y2 - Y1
      AY = Y2 + Y1
c
      IF ( DX .EQ. 0 .AND. DY .EQ. 0 ) DY = 0.001
      DX1 = DX*COS(AY/2.0)
      ANG = 450 - ATAN2(DY,DX1)/PIF
      AZ  = AMOD(ANG,360.0)
      U   = SIN(Y1)*SIN(Y2) + COS(Y1)*COS(Y2)*COS(DX)
c
      IF ( 1.0 - U*U ) 501,501,502
  501 DST = 0.0
      RETURN
C
  502 DST = R*ATAN( SQRT( 1.0 -U*U )/U )
      RETURN
C
      END
C**********************************************************************
      SUBROUTINE XLATE ( X, Y, ANG )
C
C  THIS ROUTINE WILL ROTATE COORDINATE SYSTEMS THROUGH AN ANGLE
C  OF ANG, MEASURED IN RADIANS CLOCKWISE FROM NORTH.
C
C  ON ENTRY, Y AND X ARE DISTANCES IN UNITS NORTH AND EAST OF SOME
C  ARBITRARY POINT.  ON EXIT, Y AND X ARE DISTANCES IN UNITS ALONG
C  AND TO THE RIGHT OF DIRECTION ANG.
C
      XT = X
      YT = Y
c
      X  = XT*SIN(ANG) + YT*COS(ANG)
      Y  = YT*SIN(ANG) - XT*COS(ANG)
c
      RETURN
      END
C***********************************************************************
      SUBROUTINE ERRGC(BTLATI,BTLONI,FCLATI,FCLONI,BTLATF,BTLONF,
     $FCLATF,FCLONF,XERR,YERR,VERR,HDNG,INDEX)
C
C RETURNS EXACT (GREAT CIRCLE) FORECAST ERROR IN USER SPECIFIED
C COORDINATE SYSTEM.  IF ZONAL AND MERIDIONAL SYSTEM IS WANTED,
C SPECIFY HEADING (IN ARGUMENT LIST) TO 360.  IF STORM ORIENTED
C ERROR IS WANTED, SPECIFY HDNG AS STORM DIRECTION TOWARDS.
C VECTOR ERROR IS RETURNED AS VERR,  AND COMPONENT ERRORS ARE
C RETURNED AS YERR AND XERR.
C LATTER TWO ERRORS ARE COMPUTED RELATIVE TO OBSERVED STORM POSITION
C AND IN ALGEBRAIC SENSE.
C
C CALLS AL TAYLOR SUBROUTINES STHGPR,LL2XYH AND LL2DB.
C*********************************
C BTLAT1, BTLONI ARE BEST-TRACK INITIAL POSITIONS
C FCLATI, FCLONI ARE FORECAST (OPERATIONAL) INITIAL POSITION
C BTLATF,BTLONF ARE BEST-TRACK OBSERVED POSITION
C FCLATF,FCLONF ARE FORECAST POSITIONS
C FINAL ARGUNEMT (INDEX) IS SET TO INTEGER 1 IF INITIAL POSITIONING
C ERROR (IPE) TO BE REMOVED; IT IS SET TO 2 IF IPE IS NOT TO BE REMOVED.
C*********************************
      IF(INDEX.EQ.1)GO TO 10
      IF(INDEX.EQ.2)GO TO 20
   10 FCLAT=FCLATF-FCLATI+BTLATI
      FCLON=FCLONF-FCLONI+BTLONI
      GO TO 30
   20 FCLAT=FCLATF
      FCLON=FCLONF
   30 CALL STHGPR(BTLATF,BTLONF,HDNG,1.,0.,0.)
      CALL LL2XYH(FCLAT,FCLON,XERR,YERR)
      CALL LL2DB(BTLATF,BTLONF,FCLAT,FCLON,VERR,BEAR)
      RETURN
      END
C***********************************************************************
      BLOCK DATA
C   ALBION D. TAYLOR, MARCH 19, 1982
C  THE HURRICANE GRID IS BASED ON AN OBLIQUE EQUIDISTANT CYLINDRICAL
C  MAP PROJECTION ORIENTED ALONG THE TRACK OF THE HURRICANE.
C
C    THE X (OR I) COORDINATE XI OF A POINT REPRESENTS THE DISTANCE
C  FROM THAT POINT TO THE GREAT CIRCLE THROUGH THE HURRICANE, IN
C  THE DIRECTION OF MOTION OF THE HURRICANE MOTION.  POSITIVE VALUES
C  REPRESENT DISTANCES TO THE RIGHT OF THE HURRICANE MOTION, NEGATIVE
C  VALUES REPRESENT DISTANCES TO THE LEFT.
C    THE Y (OR J) COORDINATE OF THE POINT REPRESENTS THE DISTANCE
C  ALONG THE GREAT CIRCLE THROUGH THE HURRICANE TO THE PROJECTION
C  OF THE POINT ONTO THAT CIRCLE.  POSITIVE VALUES REPRESENT
C  DISTANCE IN THE DIRECTION OF HURRICANE MOTION, NEGATIVE VALUES
C  REPRESENT DISTANCE IN THE OPPOSITE DIRECTION.
C
C     SCALE DISTANCES ARE STRICTLY UNIFORM IN THE I-DIRECTION ALWAYS.
C  THE SAME SCALE HOLDS IN THE J-DIRECTION ONLY ALONG THE HURRICANE TRACK
C  ELSEWHERE, DISTANCES IN THE J-DIRECTION ARE EXAGERATED BY A FACTOR
C  INVERSELY PROPORTIONAL TO THE COSINE OF THE ANGULAR DISTANCE FROM
C  THE TRACK.  THE SCALE IS CORRECT TO 1 PERCENT WITHIN A DISTANCE OF
C  480 NM OF THE STORM TRACK, 5 PERCENT WITHIN 1090 NM, AND
C  10 PERCENT WITHIN 1550 NM.
C
C  BIAS VALUES ARE ADDED TO THE XI AND YJ COORDINATES FOR CONVENIENCE
C  IN INDEXING.
C
C  A PARTICULAR GRID IS SPECIFIED BY THE USER BY MEANS OF A CALL
C  TO SUBROUTINE STHGPR (SET HURRICANE GRID PARAMETERS)
C  WITH ARGUMENTS (XLATH,XLONH,BEAR,GRIDSZ,XIO,YJO)
C   WHERE
C     XLATH,XLONH = LATITUDE, LONGITUDE OF THE HURRICANE
C     BEAR        = BEARING OF THE HURRICANE MOTION
C     GRIDSZ      = SIZE OF GRID ELEMENTS IN NAUTICAL MILES
C     XIO, YJO    = OFFSETS IN I AND J COORDINATES (OR I AND J
C                     COORDINATES OF HURRICANE)
C    AND WHERE
C     LATITUDES, LONGITUDES AND BEARINGS ARE GIVEN IN DEGREES,
C     POSITIVE VALUES ARE NORTH AND WEST, NEGATIVE SOUTH AND EAST,
C     BEARINGS ARE GIVEN CLOCKWISE FROM NORTH.
C
C  THE CALL TO STHGPR SHOULD BE MADE ONCE ONLY, AND BEFORE REFERENCE
C  TO ANY CALL TO LL2XYH OR XY2LLH.  IN DEFAULT, THE SYSTEM
C  WILL ASSUME A STORM AT LAT,LONG=0.,0., BEARING DUE NORTH,
C  WITH A GRIDSIZE OF 120 NAUTICAL MILES AND OFFSETS OF 0.,0. .
C
C  TO CONVERT FROM GRID COORDINATES XI AND YJ, USE A CALL TO
C    CALL XY2LLH(XI,YJ,XLAT,XLONG)

C  THE SUBROUTINE WILL RETURN THE LATITUDE AND LONGITUDE CORRESPONDING
C  TO THE GIVEN VALUES OF XI AND YJ.
C
C  TO CONVERT FROM LATITUDE AND LONGITUDE TO GRID COORDINATES, USE
C    CALL LL2XYH(XLAT,XLONG,XI,YJ)
C  THE SUBROUTINE WILL RETURN THE I-COORDINATE XI AND Y-COORDINATE
C  YJ CORRESPONDING TO THE GIVEN VALUES OF LATITUDE XLAT AND
C  LONGITUDE XLONG.
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DATA A /0.,-1.,0., 1.,0.,0.,  0.,0.,1./
      DATA RADPDG/1.745 3293 E-2/,RRTHNM /3 440.17/
      DATA DGRIDH/120./
      DATA HGRIDX,HGRIDY/0.,0./
      END
C***********************************************************************
      SUBROUTINE STHGPR(XLATH,XLONH,BEAR,GRIDSZ,XI0,YJ0)
C   ALBION D. TAYLOR, MARCH 19, 1982
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      CLAT=COS(RADPDG*XLATH)
      SLAT=SIN(RADPDG*XLATH)
      SLON=SIN(RADPDG*XLONH)
      CLON=COS(RADPDG*XLONH)
      SBEAR=SIN(RADPDG*BEAR)
      CBEAR=COS(RADPDG*BEAR)
      A(1,1)=   CLAT*SLON
      A(1,2)=   CLAT*CLON
      A(1,3)=   SLAT
      A(2,1)= - CLON*CBEAR + SLAT*SLON*SBEAR
      A(2,2)=   SLON*CBEAR + SLAT*CLON*SBEAR
      A(2,3)=              - CLAT*     SBEAR
      A(3,1)= - CLON*SBEAR - SLAT*SLON*CBEAR
      A(3,2)=   SLON*SBEAR - SLAT*CLON*CBEAR
      A(3,3)=                CLAT*     CBEAR
      DGRIDH=GRIDSZ
      HGRIDX=XI0
      HGRIDY=YJ0
      RETURN
      END
C***********************************************************************
      SUBROUTINE LL2XYH(XLAT,XLONG,XI,YJ)
C   ALBION D. TAYLOR, MARCH 19, 1982
      COMMON /HGRPRM/ A(3,3),RADPDG,RRTHNM,DGRIDH,HGRIDX,HGRIDY
      DIMENSION ZETA(3),ETA(3)
      CLAT=COS(RADPDG*XLAT)
      SLAT=SIN(RADPDG*XLAT)
      SLON=SIN(RADPDG*XLONG)
      CLON=COS(RADPDG*XLONG)
      ZETA(1)=CLAT*SLON
      ZETA(2)=CLAT*CLON
      ZETA(3)=SLAT
      DO 20 I=1,3
      ETA(I)=0.
      DO 20 J=1,3
      ETA(I)=ETA(I) + A(I,J)*ZETA(J)
   20 CONTINUE
      R=SQRT(ETA(1)*ETA(1) + ETA(3)*ETA(3))
      XI=HGRIDX+RRTHNM*ATAN2(ETA(2),R)/DGRIDH
      IF(R.LE.0.) GO TO 40
      YJ=HGRIDY+RRTHNM*ATAN2(ETA(3),ETA(1))/DGRIDH
      RETURN
   40 YJ=0.
      RETURN
      END
C***********************************************************************
      SUBROUTINE LL2DB(XLATO,XLONO,XLATT,XLONT,DIST,BEAR)
C      ALBION D. TAYLOR MARCH 18, 1981
      DATA RRTHNM/3 440.17/,RADPDG/1.745 3293 E-2/
C   RRTHNM=RADIUS OF EARTH IN NAUT. MILES, RADPDG==OF RADIANS
C   PER DEGREE
C*---------------------------------------------------------------------*
C* GIVEN AN ORIGIN AT LATITUDE, LONGITUDE=XLATO,XLONO, WILL LOCATE     *
C* A TARGET POINT AT LATITUDE, LONGITUDE = XLATT, XLONT.  RETURNS      *
C* DISTANCE DIST IN NAUTICAL MILES, AND BEARING BEAR (DEGREES CLOCKWISE*
C* FROM NORTH).                                                        *
C*                                                                     *
C* ALL LATITUDES ARE IN DEGREES, NORTH POSITIVE AND SOUTH NEGATIVE.    *
C* ALL LONGITUDES ARE IN DEGREES, WEST POSITIVE AND EAST NEGATIVE.     *
C*                                                                     *
C* NOTE-- WHEN ORIGIN IS AT NORTH OR SOUTH POLE, BEARING IS NO LONGER  *
C* MEASURED FROM NORTH.  INSTEAD, BEARING IS MEASURED CLOCKWISE        *
C* FROM THE LONGITUDE OPPOSITE THAT SPECIFIED IN XLONO.                *
C* EXAMPLE-- IF XLATO=90., XLONO=80., THE OPPOSITE LONGITUDE IS -100.  *
C* (100 EAST), AND A TARGET AT BEARING 30. WILL LIE ON THE -70.        *
C* (70 EAST) MERIDIAN                                                  *
C*---------------------------------------------------------------------*
      CLATO=COS(RADPDG*XLATO)
      SLATO=SIN(RADPDG*XLATO)
      CLATT=COS(RADPDG*XLATT)
      SLATT=SIN(RADPDG*XLATT)
      CDLON=COS(RADPDG*(XLONT-XLONO))
      SDLON=SIN(RADPDG*(XLONT-XLONO))
      Z=SLATT*SLATO + CLATT*CLATO*CDLON
      Y= - CLATT*SDLON
      X=CLATO*SLATT - SLATO*CLATT*CDLON
      R=SQRT(X*X+Y*Y)
      DIST=RRTHNM*ATAN2(R,Z)
      IF (R.LE.0.) GO TO 20
      BEAR=ATAN2(-Y,-X)/RADPDG + 180.
      RETURN
   20 BEAR=0.
      RETURN
      END
