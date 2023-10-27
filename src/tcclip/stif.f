      subroutine stif(ymdh, lat0, lon0, lat12, lon12, wind, wind12,
     &          int12, int24, int36, int48, int60, int72)
c
c    Driver routine for statistical typhoon intensity forecast (STIFOR)
c                                 statistics by Chu (1992)
c
c     Input:
c       ymdh            year-month-day-hr (92010100)
c       lat0            latitude at ymdh (0-90N)
c       lon0            longitude at ymdh (0-180E)
c       lat12           latitude at ymdh -12 hours
c       lon12           longitude at ymdh -12 hours
c       wind            windspeed in knots
c       wind12          12 hour old windspeed in knots
c
c     Output:
c       int12           12 hour forecast intensity (knots)
c       int24           24 hour forecast intensity (knots)
c       int36           36 hour forecast intensity (knots)
c       int48           48 hour forecast intensity (knots)
c       int60           60 hour forecast intensity (knots)
c       int72           72 hour forecast intensity (knots)
c
c
c
c
c
      character*8 jan1st,curdtg
      integer ymdh
      real    jday, lat0,lon0, lat12,lon12, tcu0,tcv0
      integer wind,wind12
      real    vmax0,vmax12, dvmax0
      real int12, int24, int36, int48, int60, int72
c
      int12=0.
      int24=0.
      int36=0.
      int48=0.
      int72=0.
c
c  check input data for problems
c
      if(lat0.lt.0.0 .or. lat0.gt.45.0) then
         print*,'latitude=',lat0
         print*,'stifor: latitude out of range, should be 0N to 45N'
cx         pause
         return
      elseif(lon0.lt.110.0 .or. lon0.gt.170.0) then
         print*,'longitude=',lon0
         print*,'stifor: longitude out of range, should be 110E to 170E'
cx         pause
         return
      endif
      if(wind.lt.0.0 .or. wind.gt.200.0 .or.
     1   wind12.lt.0.0 .or. wind12.gt.200.0) then
         print*,'stifor: intensity values out of range'
cx         pause
         return
      endif
c
c  assign data before stifor call
c
cx      jan1st(1:8)='00010100'
cx      write(curdtg,'(i8)')ymdh
cx      curdtg(1:2)='00'
cx      call dtgdif(jan1st,curdtg,ihour)
cx      jday=float(ihour/24)
c
c  f2 gets julian day
        jday=f2(ymdh)
c
c  get latitude in radians
      rad=lat0*3.14159/180.0
c  compute tropical cyclone u and v motion (knots)
      tcu0=(lon0-lon12)*60.0*cos(rad)/12.0
      tcv0=(lat0-lat12)*60.0/12.0
      vmax0=wind
      dvmax0=wind-wind12
cx      print*, 'before stifor, jday,lat0,lon0'
cx      print *, jday,lat0,lon0
cx      print*, 'tcu0,tcv0,vmax0,dvmax0'
cx      print *, tcu0,tcv0, vmax0,dvmax0
cx      pause
c
      call stifhh(jday, lat0,lon0, tcu0,tcv0, vmax0,dvmax0,
     &            int12, int24, int36, int48, int60, int72)
cx     print*,'stifor output:'
cx     print*,int12,int24,int36,int48,int60,int72
cx      pause
      if(int12.lt.0. .or. int12.gt.200.)int12=0.
      if(int24.lt.0. .or. int24.gt.200.)int24=0.
      if(int36.lt.0. .or. int36.gt.200.)int36=0.
      if(int48.lt.0. .or. int48.gt.200.)int48=0.
      if(int72.lt.0. .or. int72.gt.200.)int72=0.
      return
      end
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
      Subroutine stifhh(jday, lat0,lon0, tcu0,tcv0, vmax0,dvmax0,
     &                  int12, int24, int36, int48, int60, int72)
C     jday: integer julian day.
C     lat0, lon0: lat. and lon. of current tropical cyclone center.
C     tcu0, tcv0: the 12-hour tropical cyclone motion speeds in u and
C             v components.  The 12-hour t.c. speed change.
C             u is positive towards EAST, v is positive towards NORTH.
C     vmax0: max. speed or intensity at current time.
C     dvmax0: the difference between max. speeds at current and
C             12 hours ago.  The 12-hour t.c. intensity change.
C     intHH: the predicted intensity at HH hour.  HH=12, 24, 36, 48,
C            60 and 72.
C
      real jday
      real coef12(8),coef24(8),coef36(8),coef48(8),coef60(8),coef72(8)
      real lat0,lon0, tcu0,tcv0, vmax0,dvmax0
      real int12, int24, int36, int48, int60, int72
C     Clear.
         int12 = -99.9
         int24 = -99.9
         int36 = -99.9
         int48 = -99.9
         int60 = -99.9
         int72 = -99.9
C     Check for missing input data.
      if(jday .eq. -999  .or. lat0 .eq. -99.9 .or. lon0 .eq. -999.9 .or.
     &   tcu0 .eq. -99.9 .or. tcv0 .eq. -99.9 .or. vmax0 .eq. -99.9 .or.
     &   dvmax0 .eq. -99.9) return
C
      data coef12/3.97e-3, -1.48e-1,  7.72e-2, -5.30e-2, -1.94e-2
     &,           9.08e-1,  4.96e-1, -4.09 /
      int12 =  coef12(1)*jday + coef12(2)*lat0 + coef12(3)*lon0
     &       + coef12(4)*tcu0        + coef12(5)*tcv0 + coef12(6)*vmax0
     &       + coef12(7)*dvmax0      + coef12(8)

      data coef24/1.11e-2, -3.46e-1,  1.65e-1, -2.13e-1, -7.43e-2
     &,           7.75e-1,  7.15e-1, -6.93 /
      int24 =  coef24(1)*jday + coef24(2)*lat0 + coef24(3)*lon0
     &       + coef24(4)*tcu0        + coef24(5)*tcv0 + coef24(6)*vmax0
     &       + coef24(7)*dvmax0      + coef24(8)

      data coef36/1.85e-2, -5.32e-1,  2.44e-1, -3.63e-1, -2.37e-1
     &,           6.33e-1,  7.96e-1, -7.87 /
      int36 =  coef36(1)*jday + coef36(2)*lat0 + coef36(3)*lon0
     &       + coef36(4)*tcu0        + coef36(5)*tcv0 + coef36(6)*vmax0
     &       + coef36(7)*dvmax0      + coef36(8)

      data coef48/2.59e-2, -6.96e-1,  3.15e-1, -4.57e-1, -6.67e-1
     &,           4.98e-1,  7.97e-1, -8.25 /
      int48 =  coef48(1)*jday + coef48(2)*lat0 + coef48(3)*lon0
     &       + coef48(4)*tcu0        + coef48(5)*tcv0 + coef48(6)*vmax0
     &       + coef48(7)*dvmax0      + coef48(8)

      data coef60/3.29e-2, -8.11e-1,  3.78e-1, -6.25e-1, -1.39
     &,           3.74e-1,  7.81e-1, -8.92 /
      int60 =  coef60(1)*jday + coef60(2)*lat0 + coef60(3)*lon0
     &       + coef60(4)*tcu0        + coef60(5)*tcv0 + coef60(6)*vmax0
     &       + coef60(7)*dvmax0      + coef60(8)

      data coef72/3.88e-2, -9.03e-1,  4.33e-1, -7.17e-1, -2.25
     &,           2.60e-1,  7.42e-1, -9.56 /
      int72 =  coef72(1)*jday + coef72(2)*lat0 + coef72(3)*lon0
     &       + coef72(4)*tcu0        + coef72(5)*tcv0 + coef72(6)*vmax0
     &       + coef72(7)*dvmax0      + coef72(8)

      return
      end
