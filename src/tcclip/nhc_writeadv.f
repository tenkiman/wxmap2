      program nhc_writeadv
c
c**   This program creates all NWS tropical cyclone advisory products
c
c================================================================
c
c**   command line input:
c**                    arg1=storm id
c
c**   files: 
c**                    unit21: strmid.fst file
c
c  variables:
c
c  current programmer:  gross, nhc  
c  
c
c  change record:
c
c================================================================
      INCLUDE  'dataformats.inc'
c
      common /title/   STRMID, stname, BASIN, YMDH, basin2
      common /timing/  special, sptau, sptime, timezn, daylite, pubfreq
      common /heading/ advnum, afosbin, ADNAME, CLASS, ends(5), msg_path
      common /ending/  accuracy, end_type, end_time, lastadv, fstr_name
c
      integer pvsg( 25, 150 ), arrayp( 96, 60 )
c
      character*1  afosbin, timezn, pubfreq, basin
      character*2  sptau, end_type, fsttp, basin2
      character*3  fstr_initials, special, advnum, daylite, accuracy
      character*3  end_time, lastadv
      character*4  sptime
      character*8  strmid
      character*10 ymdh, stname
      character*15 fstr_name
      character*16 adname, ends, stanam(150)
      character*24 class
      character*25 line
      character*50 msg_path, stm_path
      character*75 file_name
c
      type (AID_DATA) fstRcd
c
c**   Get the command line parameters
c
      call getarg ( 2, strmid )
      call getarg ( 3, stname )
c
c**   Determine the message directory's path
c
      call getenv ( "NHCMESSAGES", msg_path )
c
      file_name = msg_path(1:lastch(msg_path))//"/"//strmid//".adv"
c
c**   Open, read a AID_DATA record and close the strmid.fst file.  This
c**     is the entire file.
c
      open ( 21, file=file_name, status='old', iostat=ios, err=1010 )
c
   10 read ( 21, '(a)', end=20) line
c
      if ( line(1:17) .eq. 'special        : ' ) special  = line(18:20)
      if ( line(1:17) .eq. 'special_HHMM   : ' ) sptime   = line(18:21)
      if ( line(1:17) .eq. 'special_TAU    : ' ) sptau    = line(18:19)
      if ( line(1:17) .eq. 'advisory#      : ' ) advnum   = line(18:20)
      if ( line(1:17) .eq. 'AWIPS_bin#     : ' ) afosbin  = line(18:18)
      if ( line(1:17) .eq. 'time_zone      : ' ) timezn   = line(18:18)
      if ( line(1:17) .eq. 'daylight_saving: ' ) daylite  = line(18:20)
      if ( line(1:17) .eq. 'center_accuracy: ' ) accuracy = line(18:20) 
      if ( line(1:17) .eq. 'forecast_type  : ' ) end_type = line(18:19)
      if ( line(1:17) .eq. 'change_TAU     : ' ) end_time = line(18:20)
      if ( line(1:17) .eq. 'public_freq    : ' ) pubfreq  = line(18:18)
      if ( line(1:17) .eq. 'final_advisory : ' ) lastadv  = line(18:20)
c
      goto 10
c 
   20 close ( 21 )
c
cc      write (*, '('' '')')
cc      write (*, '(a3,3x,a4,3x,a2)') special, sptime, sptau
cc      write (*, '(a3,3x,a1,3x,a1)') advnum, afosbin, timezn
cc      write (*, '(a3,3x,a3,3x,a2)') daylite, accuracy, fsttp
cc      write (*, '(a3,3x,a1,3x,a3)') fsttptime, pubfreq, lastadv
c
c**   Open, read a AID_DATA record and close the strmid.fst file.  This
c**     is the entire file.
c
c**   Determine the storms directory path
c
      call getenv ( "ATCFSTRMS", stm_path )
c
      file_name = stm_path(1:lastch(stm_path))//"/"//strmid//".fst"
c
      open ( 22, file=file_name, status='old', iostat=ios, err=1020 )
c
      call readARecord ( 22, fstRcd, istat )
      if ( istat .eq. 0 ) go to 1030
c 
      close (22)
c
c**   Determine all the time parameters for all the advisory products
c
      call timer ( fstRcd )
c
c**   Create the forecast/advisory
c
      call fstadv ( fstRcd )
c
c**   Create the tropical cyclone discussion
c
      call discuss ( fstRcd )
c
c**   Create the public advisory
c
      call public ( fstRcd )
c
c**   If it's an Atlantic storm, generate the probability values and
c**     create the probability message.
c
c
      if ( strmid(1:2) .eq. 'al' ) then
c
         call probability  ( fstRcd,    nsta, stanam, pvsg, arrayp, 
     &                       iprob_stat )
c
         if ( iprob_stat .eq. 1 ) then
c
            call problty_msg ( fstRcd, nsta, stanam, pvsg )
c
            call problty_tbl ( arrayp )
c
         endif   
c
      endif
c
      stop
c
 1010 print *, ' ERROR - opening file = ', file_name, ' ios = ', ios
      stop
c
 1020 print *, ' ERROR - opening file = ', file_name, ' ios = ', ios
      stop
c
 1030 print *, ' ERROR - reading file = ', file_name, ' istat = ', istat
      stop
c
      end
c****************************************************************
      SUBROUTINE TIMER ( fstRcd )
C
C**   DETERMINES THE DATES AND TIMES USED IN ALL THE PRODUCTS
C
      INCLUDE  'dataformats.inc'
c
      common /TITLE/   STRMID, stname, BASIN, YMDH, basin2
      common /timing/  special, sptau, sptime, timezn, daylite, pubfreq
      common /MMTIME/  MTIME, MDAYWK, MMONTH, MDAY, MYEAR, MXDYTM
      common /DDTIME/  DTLINE, DIDYTM
      common /PPTIME/  PTIME, PTIMZN, PDAYWK, PMONTH, PDAY, PYEAR,
     &                 PIDYTM(3), PXDYTM, PZTIME
      common /pbtimes/ pbyear(4), pbmonth(4), pbdate(4), pbday(4),
     &                 pbhour(4), pbampm(4), pbtimzn(4)
C
      INTEGER AYEAR, AMONTH, ADAY, DELTIM
      integer advtau(5),pbtau(4)
C
      CHARACTER*1   BASIN, DAYSTD, TIMEZN, ew, pubfreq
      CHARACTER*2   sptau, temp_basin, ADDAY, ZTIME, ADSPD, basin2
      character*2   pbdate, pbhour, pbampm
      character*3   daylite, special, pbday, pbmonth, pbtimzn
      CHARACTER*3   advnum, MONTH(12), MDAY, DDAY, DMDIEM, PDAY
      CHARACTER*3   PMDIEM
      CHARACTER*4   SPTIME,MTIME,TIMED,TIMEP,MDAYWK,DDAYWK,PDAYWK,XDAYWK
      CHARACTER*4   DMONTH,PMONTH,DTIMZN,PTIMZN,PZTIME,PXTIME,PXDIEM
      CHARACTER*4   MMONTH,PITIME,PIDIEM,pbyear
      CHARACTER*5   MYEAR,DYEAR,PYEAR,TIMEDD,TIMEPP,TIMEXX,TIMEYY
      CHARACTER*8   STRMID
      CHARACTER*10  MYMDH,M2YMDH,M3YMDH,M4YMDH,MXYMDH,DYMDH,PYMDH
      CHARACTER*10  PIYMDH(3),PXYMDH,SPYMDH
      CHARACTER*9   MXDYTM,DIDYTM
      character*10  ymdh, times(5), pbymdh, pbtime(4), stname
      CHARACTER*10  WKDAY(7),PTIME,PXTMNG,DTIME,XTIME,YTIME
      CHARACTER*13  XDAY,YDAY
      CHARACTER*15  fstr_name
      CHARACTER*17  DIRSPD
      CHARACTER*21  WIND48,WIND72
      CHARACTER*25  PXDYTM,PIDYTM
      CHARACTER*43  ADVPAR
      CHARACTER*45  WIND12,WIND24,WIND36
      CHARACTER*57  WINDAD
      CHARACTER*68  DTLINE
      CHARACTER*70  LATLON
c
      type (AID_DATA) fstRcd, tauData
c
      DATA WKDAY/'SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY',
     & 'FRIDAY','SATURDAY'/
      DATA MONTH/'JAN','FEB','MAR','APR','MAY','JUN',
     &           'JUL','AUG','SEP','OCT','NOV','DEC'/
c
      data advtau / 3, 5, 6, 7, 9 /
      data pbtau  / 24, 36, 48, 72 /
c
cc      read ( sptau, '(i2)' ) advtau(1)
c
      temp_basin = fstRcd%aRecord(1)%basin
      ymdh       = fstRcd%aRecord(1)%DTG
c
      bstlon = fstRcd%aRecord(1)%lon
      ew     = fstRcd%aRecord(1)%EW
      if( fstRcd%aRecord(1)%EW .eq. 'E' ) bstlon = 360.0 - bstlon
c
      do i = 1, 5
         call dtgmod ( ymdh, advtau(i), times(i), istat )
         if ( istat .ne. 0 ) stop ' Bad times generated!'
      enddo
c
cc      write (*,'('' '')')
cc      write (*,'(i10,5x,a10)') (advtau(i), times(i), i = 1, 5)
c
      MYMDH   = times(1)
      M2YMDH  = times(2)
      M3YMDH  = times(3)
      M4YMDH  = times(4)
      MXYMDH  = times(5)
      MTIME   = times(1)(9:10)//'00'
C
C**   IF THERE IS A SPECIAL TIME, CHANGE MARINE TIME TO SPECIAL TIME
C**     AND CHANGE THE CURRENT MARINE TIME TO THE NEXT MARINE
C
      IF ( special .eq. 'YES' ) THEN
         read ( ymdh(9:10), '(i2)' ) ihour
         read ( sptime, '(2i2)' ) jhour, jmin
         if ( jmin .ge. 30 ) jhour = jhour + 1
         lhour = jhour - ihour
         call dtgmod ( ymdh, lhour, spymdh, istat )
         IF ( SPYMDH .LT. MYMDH ) MXYMDH = MYMDH
         MYMDH  = SPYMDH
         MTIME  = SPTIME
      ENDIF
C
C**   DETERMINE THE MARINE DATES AND TIMES
C
      READ (MYMDH,'(i4,2I2,2X)') AYEAR, AMONTH, ADAY
C
      MDAYWK  = ' '//WKDAY(IWKDAY(AYEAR,AMONTH,ADAY))(1:3)
      MMONTH  = ' '//MONTH(AMONTH)
      MYEAR   = ' '//MYMDH(1:4)
      MDAY    = ' '//MYMDH(7:8)
      MXDYTM  = MXYMDH(7:8)//'/'//MXYMDH(9:10)//'00Z'
C
C**   DETERMINE THE DISCUSSION DATES AND TIMES
C
C**   INITIALIZE COMMON PARAMETERS
C
      daystd = 'D'
      if (daylite(1:2) .eq. 'NO') daystd = 'S'
c
      IF ( temp_basin .eq. 'AL' ) then
         BASIN  = 'A'
         basin2 = 'AT'
      endif
      IF ( temp_basin .EQ. 'EP' .AND. BSTLON .LE. 140.0 ) then
         BASIN  = 'P'
         basin2 = 'EP'
         TIMEZN = 'P'
      endif
      IF ( temp_basin .EQ. 'CP' .OR.  BSTLON .GT. 140.0) THEN
          BASIN  = 'C'
          basin2 = 'CP'
          TIMEZN = 'H'
          DAYSTD = 'S'
      ENDIF
C
C**   CHECK FOR DAYLIGHT SAVINGS TIME FOR EACH BASIN.  NOTE ALL ATLANTIC
C**      DISCUSSIONS ARE EASTERN TIME ZONE AND ALL PACIFIC DISCUSSIONS ARE
C**      PACIFIC TIME ZONE.
C
      IF (BASIN.EQ.'A') THEN
         IF (DAYSTD.EQ.'D') THEN
            call dtgmod ( mymdh, -4, dymdh, istat )
         ELSE
            call dtgmod ( mymdh, -5, dymdh, istat )
         ENDIF
c
      ELSEIF (BASIN.EQ.'P') THEN
         IF (DAYSTD.EQ.'D') THEN
            call dtgmod ( mymdh, -7, dymdh, istat )
         ELSE
            call dtgmod ( mymdh, -8, dymdh, istat )
         ENDIF
c
      ELSEIF (BASIN.EQ.'C') THEN
         call dtgmod ( mymdh, -10, dymdh, istat )
c
      ENDIF
C
      IF ( special .eq. 'NO' ) THEN
          DIDYTM = MYMDH(7:8)//'/'//MYMDH(9:10)//'00Z '
      ELSE
          DIDYTM = MYMDH(7:8)//'/'//SPTIME//'Z '
      ENDIF
C
C**   DETERMINE THE DISCUSSION DATE
C
      READ (DYMDH,'(i4,2I2,2X)') AYEAR,AMONTH,ADAY
C
      DDAYWK = ' '//WKDAY(IWKDAY(AYEAR,AMONTH,ADAY))(1:3)
      DMONTH = ' '//MONTH(AMONTH)
      DYEAR  = ' '//DYMDH(1:4)
      DDAY   = ' '//DYMDH(7:8)
      IF (BASIN.EQ.'A') THEN
          DTIMZN = ' E'//DAYSTD//'T'
      ELSEIF (BASIN.EQ.'P') THEN
          DTIMZN = ' P'//DAYSTD//'T'
      ELSEIF (BASIN.EQ.'C') THEN
          DTIMZN = ' HST'
      ENDIF
C
C**   DETERMINE THE DISCUSSION MINUTES
C
      IF ( special .eq. 'NO' ) THEN
          TIMED = DYMDH(9:10)//'00'
      ELSE
          TIMED = DYMDH(9:10)//SPTIME(3:4)
      ENDIF
C
C**   DETERMINE IF DISCUSSION TIME AM OR PM
C
      READ (TIMED,'(I4)') ITIME
      IF (ITIME.LT.1200) THEN
          DMDIEM = ' AM'
      ELSE
          DMDIEM = ' PM'
          ITIME = ITIME - 1200
          IF (ITIME.LT.100) ITIME = ITIME + 1200
      ENDIF
C
C**   STRIP A LEADING ZERO OR TWO LAGING ZEROS FROM THE TIME
C
      WRITE (TIMED,'(I4.4)') ITIME
      IF (TIMED(3:4).EQ.'00') TIMED(3:4) = '  '
      IF (TIMED(1:1).EQ.'0' ) TIMED = TIMED(2:4)//' '
      TIMEDD = TIMED(1:4)
C
C**   DETERMINE IF TIME IS NOON OR MIDNIGHT
C
      DTIME = TIMEDD(1:INDEX(TIMEDD,' ') - 1)//DMDIEM
      IF (DTIME(1:4).EQ. '0 AM') DTIME = 'MIDNIGHT '
      IF (DTIME(1:5).EQ.'12 PM') DTIME = 'NOON '
C
C**   COMPOSE THE DISCUSSION TIME LINE
C
      DTLINE = DTIME(1:INDEX(DTIME,'  ') - 1)//DTIMZN//DDAYWK//
     & DMONTH//DDAY//DYEAR
C
C**   DETERMINE THE PUBLIC TIMES
C
C**   CHECK FOR DAYLIGHT SAVINGS TIME AND TIME ZONE FOR EACH BASIN
C**      FOR THIS ADVISORY AND THE NEXT
C
      IF (BASIN.EQ.'A') THEN
          IF (DAYSTD.EQ.'D') THEN
              IF (TIMEZN.EQ.'A') THEN
                 call dtgmod (  mymdh, -4,     pymdh, istat )
                 call dtgmod ( m2ymdh, -4, piymdh(1), istat )
                 call dtgmod ( m3ymdh, -4, piymdh(2), istat )
                 call dtgmod ( m4ymdh, -4, piymdh(3), istat )
                 call dtgmod ( mxymdh, -4,    pxymdh, istat )
              ELSEIF (TIMEZN.EQ.'E') THEN
                 call dtgmod (  mymdh, -4,     pymdh, istat )
                 call dtgmod ( m2ymdh, -4, piymdh(1), istat )
                 call dtgmod ( m3ymdh, -4, piymdh(2), istat )
                 call dtgmod ( m4ymdh, -4, piymdh(3), istat )
                 call dtgmod ( mxymdh, -4,    pxymdh, istat )
              ELSEIF (TIMEZN.EQ.'C') THEN
                 call dtgmod (  mymdh, -5,     pymdh, istat )
                 call dtgmod ( m2ymdh, -5, piymdh(1), istat )
                 call dtgmod ( m3ymdh, -5, piymdh(2), istat )
                 call dtgmod ( m4ymdh, -5, piymdh(3), istat )
                 call dtgmod ( mxymdh, -5,    pxymdh, istat )
              ENDIF
          ELSE
              IF (TIMEZN.EQ.'A') THEN
                 call dtgmod (  mymdh, -4,     pymdh, istat )
                 call dtgmod ( m2ymdh, -4, piymdh(1), istat )
                 call dtgmod ( m3ymdh, -4, piymdh(2), istat )
                 call dtgmod ( m4ymdh, -4, piymdh(3), istat )
                 call dtgmod ( mxymdh, -4,    pxymdh, istat )
              ELSEIF (TIMEZN.EQ.'E') THEN
                 call dtgmod (  mymdh, -5,     pymdh, istat )
                 call dtgmod ( m2ymdh, -5, piymdh(1), istat )
                 call dtgmod ( m3ymdh, -5, piymdh(2), istat )
                 call dtgmod ( m4ymdh, -5, piymdh(3), istat )
                 call dtgmod ( mxymdh, -5,    pxymdh, istat )
              ELSEIF (TIMEZN.EQ.'C') THEN
                 call dtgmod (  mymdh, -6,     pymdh, istat )
                 call dtgmod ( m2ymdh, -6, piymdh(1), istat )
                 call dtgmod ( m3ymdh, -6, piymdh(2), istat )
                 call dtgmod ( m4ymdh, -6, piymdh(3), istat )
                 call dtgmod ( mxyxdh, -6,    pxymdh, istat )
              ENDIF
          ENDIF
      ELSEIF (BASIN.EQ.'P') THEN
          IF (DAYSTD.EQ.'D') THEN
             call dtgmod (  mymdh, -7,     pymdh, istat )
             call dtgmod ( m2ymdh, -7, piymdh(1), istat )
             call dtgmod ( m3ymdh, -7, piymdh(2), istat )
             call dtgmod ( m4ymdh, -7, piymdh(3), istat )
             call dtgmod ( mxymdh, -7,    pxymdh, istat )
          ELSE
             call dtgmod (  mymdh, -8,     pymdh, istat )
             call dtgmod ( m2ymdh, -8, piymdh(1), istat )
             call dtgmod ( m3ymdh, -8, piymdh(2), istat )
             call dtgmod ( m4ymdh, -8, piymdh(3), istat )
             call dtgmod ( mxymdh, -8,    pxymdh, istat )
          ENDIF
      ELSEIF (BASIN.EQ.'C') THEN
         call dtgmod (  mymdh, -10,     pymdh, istat )
         call dtgmod ( m2ymdh, -10, piymdh(1), istat )
         call dtgmod ( m3ymdh, -10, piymdh(2), istat )
         call dtgmod ( m4ymdh, -10, piymdh(3), istat )
         call dtgmod ( mxymdh, -10,    pxymdh, istat )
      ENDIF
C
CC    PRINT *, ' CURRENT AND NEXT DATES = ',MYMDH,PYMDH,MXYMDH,PXYMDH
CC    PAUSE
C
C**   DETERMINE THE PUBLIC DATE
C
      READ (PYMDH,'(i4,2I2,2X)') AYEAR,AMONTH,ADAY
C
      PDAYWK = ' '//WKDAY(IWKDAY(AYEAR,AMONTH,ADAY))(1:3)
      PMONTH = ' '//MONTH(AMONTH)
      PYEAR  = ' '//PYMDH(1:4)
      PDAY   = ' '//PYMDH(7:8)
      PTIMZN = ' '//TIMEZN//DAYSTD//'T'
      IF (PTIMZN.EQ.' ADT') PTIMZN = ' AST'
C
C**   DETERMINE THE PUBLIC MINUTES
C
      PZTIME = MTIME
C
      IF ( special .eq. 'NO' ) THEN
          TIMEP = PYMDH(9:10)//'00'
      ELSE
          TIMEP = PYMDH(9:10)//SPTIME(3:4)
      ENDIF
C
C**   DETERMINE THE PUBLIC AM OR PM
C
      READ (TIMEP,'(I4)') ITIME
      IF (ITIME.LT.1200) THEN
          PMDIEM = ' AM'
      ELSE
          PMDIEM = ' PM'
          ITIME = ITIME - 1200
          IF (ITIME.LT.100) ITIME = ITIME + 1200
      ENDIF
C
C**   STRIP A LEADING ZERO OR TWO LAGGING ZEROS
C
      WRITE (TIMEP,'(I4.4)') ITIME
      IF (TIMEP(3:4).EQ.'00') TIMEP(3:4) = '  '
      IF (TIMEP(1:1).EQ.'0' ) TIMEP = TIMEP(2:4)//' '
      TIMEPP = TIMEP(1:4)
C
C**   DETERMINE IF THE PUBLIC TIME IS NOON OR MIDNIGHT
C
      PTIME = TIMEPP(1:INDEX(TIMEPP,' ') - 1)//PMDIEM
      IF (PTIME(1:4).EQ. '0 AM') PTIME = 'MIDNIGHT '
      IF (PTIME(1:5).EQ.'12 PM') PTIME = 'NOON '
C
C**   DETERMINE THE INTERMEDIATE TIMES
C
C**   DETERMINE THE INTERMEDIATE PUBLIC ADVISORY MINUTES
C
      DO I = 1, 3
C
         PITIME = PIYMDH(I)(9:10)//'00'
C
C**   DETERMINE THE INTERMEDIATE PUBLIC ADVISORY AM OR PM
C
         READ (PITIME,'(I4)') LTIME
         IF ( LTIME .LT. 1200 ) THEN
            PIDIEM = ' AM'
         ELSE
            PIDIEM = ' PM'
            LTIME = LTIME - 1200
            IF ( LTIME .LT. 100 ) LTIME = LTIME + 1200
         ENDIF
C
C**   STRIP A LEADING ZERO OR TWO LAGGING ZEROS
C
         WRITE (PITIME,'(I4.4)') LTIME
         IF ( PITIME(3:4) .EQ. '00' ) PITIME(3:4) = '  '
         IF ( PITIME(1:1) .EQ.  '0' ) PITIME = PITIME(2:4)//' '
         TIMEYY = PITIME(1:4)
C
C**   DETERMINE IF INTERMEDIATE PUBLIC ADVISORY IS NOON OR MIDNIGHT
C
         YTIME = TIMEYY(1:INDEX(TIMEYY,' ') - 1)//PIDIEM
         IF ( YTIME(1:4) .EQ.  '0 AM' ) YTIME = 'MIDNIGHT '
         IF ( YTIME(1:5) .EQ. '12 PM' ) YTIME = 'NOON '
C
C**   COMPOSE THE INTERMEDIATE ADVISORY TIME SEGMENT
C
         PIDYTM(I) = YTIME(1:INDEX(YTIME,'  ') - 1)//PTIMZN
C
      enddo
C
C**   DETERMINE THE NEXT PUBLIC ADVISORY MINUTES
C
      PXTIME = PXYMDH(9:10)//'00'
C
C**   DETERMINE THE NEXT PUBLIC ADVISORY AM OR PM
C
      READ (PXTIME,'(I4)') ITIME
      IF (ITIME.LT.1200) THEN
          PXDIEM = ' AM'
      ELSE
          PXDIEM = ' PM'
          ITIME = ITIME - 1200
          IF (ITIME.LT.100) ITIME = ITIME + 1200
      ENDIF
C
C**   STRIP A LEADING ZERO OR TWO LAGGING ZEROS
C
      WRITE (PXTIME,'(I4.4)') ITIME
      IF (PXTIME(3:4).EQ.'00') PXTIME(3:4) = '  '
      IF (PXTIME(1:1).EQ.'0' ) PXTIME = PXTIME(2:4)//' '
      TIMEXX = PXTIME(1:4)
C
C**   DETERMINE IF NEXT PUBLIC ADVISORY IS NOON OR MIDNIGHT
C
      XTIME = TIMEXX(1:INDEX(TIMEXX,' ') - 1)//PXDIEM
      IF (XTIME(1:4).EQ. '0 AM') XTIME = 'MIDNIGHT '
      IF (XTIME(1:5).EQ.'12 PM') XTIME = 'NOON '
C
C**   DETERMINE THE DAY OF THE WEEK OF THE NEXT PUBLIC ADVISORY
C
      READ (PXYMDH,'(i4,2I2,2X)') AYEAR,AMONTH,ADAY
C
      IDAY   = IWKDAY(AYEAR,AMONTH,ADAY)
      XDAYWK = ' '//WKDAY(IDAY)(1:3)
      IF (XDAYWK.EQ.PDAYWK) THEN
          XDAY = '.'
      ELSE
          XDAY = '...'//WKDAY(IDAY)(1:INDEX(WKDAY(IDAY),' ') - 1)//'.'
      ENDIF
C
C**   COMPOSE THE NEXT PUBLIC ADVISORY TIME LINE
C
      PXDYTM = XTIME(1:INDEX(XTIME,'  ') - 1)//PTIMZN//XDAY
C
c**   Determine the probability times.  (Note header information is
c**     identical to public advisory.  It's the probability accumulation
c**     times that must be calculated.)
c
      IF (DAYSTD.EQ.'D') THEN
         IF (TIMEZN.EQ.'A') THEN
            call dtgmod ( ymdh, -4, pbymdh, istat )
         ELSEIF (TIMEZN.EQ.'E') THEN
            call dtgmod ( ymdh, -4, pbymdh, istat )
         ELSEIF (TIMEZN.EQ.'C') THEN
            call dtgmod ( ymdh, -5, pbymdh, istat )
         ENDIF
      ELSE
         IF (TIMEZN.EQ.'A') THEN
            call dtgmod ( ymdh, -4, pbymdh, istat )
         ELSEIF (TIMEZN.EQ.'E') THEN
            call dtgmod ( ymdh, -5, pbymdh, istat )
         ELSEIF (TIMEZN.EQ.'C') THEN
            call dtgmod ( ymdh, -6, pbymdh, istat )
         ENDIF
      ENDIF
c
c**   Determine the probability times, if it's an Atlantic storm
c
      if ( basin .ne. 'A' ) return
c
      do i = 1, 4
         call dtgmod ( pbymdh, pbtau(i), pbtime(i), istat )
         if ( istat .ne. 0 ) stop ' Bad times generated!'
C
C**   DETERMINE THE probability dates
C
         READ (pbtime(i),'(i4,2I2,2X)') AYEAR,AMONTH,ADAY
C
         pbday(i)   = WKDAY(IWKDAY(AYEAR,AMONTH,ADAY))(1:3)
         pbmonth(i) = MONTH(AMONTH)
         pbyear(i)  = pbtime(i)(1:4)
         write (pbdate(i), '(i2)' ) aday
         pbTIMZN(i) = TIMEZN//DAYSTD//'T'
         IF ( pbTIMZN(i) .EQ. 'ADT' ) pbTIMZN(i) = 'AST'
C
C**   DETERMINE THE probability hours and if AM or PM
C
         READ ( pbtime(i)(9:10), '(I2)' ) ITIME
c
         IF ( ITIME .LT. 12 ) THEN
            pbampm(i) = 'AM'
         ELSE
            pbampm(i) = 'PM'
            ITIME = ITIME - 12
            IF ( ITIME .LT. 1 ) ITIME = ITIME + 12
         ENDIF
c
         WRITE (pbhour(i),'(I2)') ITIME
c
      enddo
c
      RETURN
      END
c****************************************************************
      SUBROUTINE fstadv ( fstRcd )
C
C**   THIS SUBROUTINE CREATES THE forecast/advisory product
C
      INCLUDE  'dataformats.inc'
c
      common /title/   STRMID, stname, BASIN, ymdh, basin2
      common /timing/  special, sptau, sptime, timezn, daylite, pubfreq
      common /heading/ advnum, afosbin, ADNAME, CLASS, ends(5), msg_path
      common /ending/  accuracy, end_type, end_time, lastadv, fstr_name
c
      common /lines/   MLINE(150),WLINE(25)
      common /warn/    WEND, current_tau
      common /mmtime/  MTIME,MDAYWK,MMONTH,MDAY,MYEAR,MXDYTM
C
      INTEGER WEND, current_tau, martau(5)
      LOGICAL PRTRAD, FSTAT, LSTAT, LETTER
C
      CHARACTER*1   BASIN,afosbin,timezn,pubfreq
      CHARACTER*1   WESN,WEAD,WE12,WE24,WE36,WE48,WE72
      CHARACTER*2   sptau, TAU(5),ADSPD,SNDAY,end_type, basin2
      CHARACTER*3   advnum, accuracy, MDAY, lastadv
      character*3   special, daylite, end_time
      CHARACTER*4   SPTIME,SNTIME,MTIME,MDAYWK,MMONTH,sfcprs
      CHARACTER*3   ADWIN,FWIN12,FWIN24,FWIN36,FWIN48,FWIN72
      CHARACTER*3   ADGUS,FGUS12,FGUS24,FGUS36,FGUS48,FGUS72
      CHARACTER*4   SNLAT
      CHARACTER*5   MYEAR,adlat
      CHARACTER*6   SNLON,ADLON
      CHARACTER*8   STRMID
      CHARACTER*10  ymdh, stname, times(5)
      CHARACTER*9   MXDYTM
      CHARACTER*15  fstr_name
      CHARACTER*16  ends
      CHARACTER*17  DIRSPD,DIRECT,CURDIR
      CHARACTER*16  ADNAME
      CHARACTER*24  CLASS
      CHARACTER*21  OMFILE,NMFILE,MARBAT
      CHARACTER*43  ADVPAR
      character*50  msg_path
      character*75  file_name
      CHARACTER*68  MLINE,WLINE,OLINE,RLINE
      CHARACTER*70  LATLON
      CHARACTER*80  HOLDER
C
      DATA TAU / '12', '24', '36', '48', '72'/
      DATA martau / 12, 24, 36, 48, 72 /
c
      type (AID_DATA) fstRcd, tauData
C
C**   BLANK NEW MESSAGE ARRAY
C
      DO I = 1,150
        MLINE(I) = ' '
      enddo
c
      do i = 1, 5
         call dtgmod ( ymdh, martau(i), times(i), istat )
         if ( istat .ne. 0 ) stop ' Bad times generated!'
      enddo
c
c**   Get the current advisory data by using the special tau (default = 3)
c
      read ( sptau, '(i2)' ) current_tau
c
cc    write (*,'(i5,5(i10,5x,a10))') current_tau, ( martau(i), 
cc   &                               times(i), i = 1, 5 )
c
      call getSingleTAU ( fstRcd, current_tau, tauData, istat )
      if ( istat .ne. 1) stop 'ERROR - cannot get current_tau data!'
c
c**   Get the forecaster name from his initials
c
      call namer ( tauData%atcfRcd(1)%initials, fstr_name )
C
C**   COMPOSE THE HEADER RECORDS
C
      LINENM = 0
C
      LINENM = LINENM + 1
      IF ( BASIN .NE . 'C' ) THEN
         MLINE(LINENM) = 'ZCZC MIATCM'//BASIN2//afosbin//' ALL'
      ELSE
         MLINE(LINENM) = 'ZCZC HFOTCM'//BASIN2//afosbin//' ALL'
      ENDIF
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
          MLINE(LINENM) = 'TTAA00 KNHC DDHHMM'
      ELSE
          MLINE(LINENM) = 'TTAA00 PHFO DDHHMM'
      ENDIF
C
C**   DETERMINE THE SYSTEM NUMBER OR NAME
C
      ADNAME = '                '
      ADNAME(1:10) = stname
      IF (ADNAME.EQ.' ') ADNAME = 'TEST'
C
C**   TAKE CARE OF LONG NUMBER NAMES
C
      IF (ADNAME(7:10).EQ.'-THR') ADNAME(11:12) = 'EE'
      IF (ADNAME(7:10).EQ.'-FOU') ADNAME(11:11) = 'R'
      IF (ADNAME(7:10).EQ.'-FIV') ADNAME(11:11) = 'E'
      IF (ADNAME(7:10).EQ.'-SEV') ADNAME(11:12) = 'EN'
      IF (ADNAME(7:10).EQ.'-EIG') ADNAME(11:12) = 'HT'
      IF (ADNAME(7:10).EQ.'-NIN') ADNAME(11:11) = 'E'
C
C**   ADD '-E' FOR EAST OR -C FOR CENTRAL INITIAL PACIFIC DEPRESSIONS
C
      LETTER = .FALSE.
      IF ( tauData%atcfRcd(1)%ty .EQ. 'TD' .OR.
     &     tauData%atcfRcd(1)%ty .EQ. 'SD') THEN
          IF (ADNAME(1:3).EQ.'ONE')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'TWO')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'THR')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'FOU')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'FIV')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'SIX')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'SEV')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'EIG')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'NIN')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'TEN')  LETTER = .TRUE.
          IF (ADNAME(1:4).EQ.'ELEV') LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'TWE')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'THI')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'FIF')  LETTER = .TRUE.
          IF (ADNAME(1:3).EQ.'TWE')  LETTER = .TRUE.
      ENDIF
      IF ( BASIN .EQ. 'P' .AND. LETTER ) ADNAME =
     & ADNAME(1:INDEX(ADNAME,' ') - 1)//'-E'
      IF ( BASIN .EQ. 'C' .AND. LETTER ) ADNAME =
     & ADNAME(1:INDEX(ADNAME,' ') - 1)//'-C'
C
C**   DETERMINE THE CLASS
C
      IF ( tauData%atcfRcd(1)%ty .EQ. 'TD' ) 
     & CLASS = 'TROPICAL DEPRESSION '
      IF ( tauData%atcfRcd(1)%ty .EQ. 'SD' ) 
     & CLASS = 'SUBTROPICAL DEPRESSION '
      IF ( tauData%atcfRcd(1)%ty .EQ. 'TS' ) 
     & CLASS = 'TROPICAL STORM '
      IF ( tauData%atcfRcd(1)%ty .EQ. 'SS' ) 
     & CLASS = 'SUBTROPICAL STORM '
      IF ( tauData%atcfRcd(1)%ty .EQ. 'HU' ) 
     & CLASS = 'HURRICANE '
C
C**   DETERMINE IF A SPECIAL ADVISORY OR NOT
C
      LINENM = LINENM + 1
      IF ( special .eq. 'NO' ) THEN
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//'FORECAST/ADVISORY NUMBER '//
     &       advnum
      ELSE
          HOLDER = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//
     &       'SPECIAL FORECAST/ADVISORY NUMBER '//advnum
          IF (LASTCH(HOLDER).GT.68)
     &       HOLDER = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//
     &       'SP FORECAST/ADVISORY NUMBER '//advnum
          MLINE(LINENM) = HOLDER(1:LASTCH(HOLDER))
      ENDIF
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
          MLINE(LINENM) = 'NATIONAL WEATHER SERVICE MIAMI FL   '//
     &        STRMID(1:4)//strmid(7:8)
      ELSE
          MLINE(LINENM) = 'NATIONAL WEATHER SERVICE HONOLULU HI   '//
     &        STRMID(1:4)//strmid(7:8)
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = MTIME//'Z'//MDAYWK//MMONTH//MDAY//MYEAR
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   BLANK WARNING ARRAY, create the warning file name, THEN OPEN,
c**     READ, FILL WARNING message ARRAY AND CLOSE *.warn FILE, IF ANY
C
      DO I = 1, 25
         WLINE(I) = ' '
      enddo
C
c**   Determine the warning message directory path
c
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//".warn"
c
      wend = 0
c
      OPEN ( 23, FILE=file_name, STATUS='OLD', ERR=50)
C
      WEND = 1
   30 READ ( 23, '(A)', END=40 ) WLINE(WEND)
      LINENM = LINENM + 1
      MLINE(LINENM) = WLINE(WEND)
      WEND = WEND + 1
      GO TO 30
C
   40 WEND = WEND - 1
      CLOSE ( 23 )
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
   50 CONTINUE
C
C**   DETERMINE THE CURRENT POSITION LINE
C
      adlat = tauData%atcfRcd(1)%latns(1:2)//'.'
     &      //tauData%atcfRcd(1)%latns(3:4)
      adlon = tauData%atcfRcd(1)%lonew(1:3)//'.'
     &      //tauData%atcfRcd(1)%lonew(4:5)
c
      LINENM = LINENM + 1
      MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//'CENTER LOCATED NEAR '
     & //adlat//' '//adlon//' AT'//MDAY//'/'//MTIME//'Z'
C
C**   DETERMINE THE ACCURACY LINE
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'POSITION ACCURATE WITHIN '//accuracy//' NM'
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE CURRENT MOVEMENT LINE
C
      CURDIR = DIRECT(tauData%aRecord(1)%dir)
c
      LINENM = LINENM + 1
      MLINE(LINENM) = 'PRESENT MOVEMENT TOWARD THE '//
     & CURDIR(1:INDEX(CURDIR,'  '))//'OR '//tauData%atcfRcd(1)%dir//
     &' DEGREES AT '//tauData%atcfRcd(1)%speed//' KT'
c
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE ESTIMATED MINIMUM CENTRAL PRESSURE LINE
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'ESTIMATED MINIMUM CENTRAL PRESSURE '//
     & tauData%atcfRcd(1)%mslp//' MB'
C
C**   DETERMINE THE EYE DIAMETER LINE
C
      IF ( tauData%aRecord(1)%eye .NE. 0) THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'EYE DIAMETER '//tauData%atcfRcd(1)%eye//
     & ' NM'
      ENDIF
C
C**   DETERMINE THE CURRENT WIND, AND WIND AND SEA RADII LINES
C
      IF (tauData%aRecord(1)%vmax .gt. 0 ) THEN
c
          LINENM = LINENM + 1
          MLINE(LINENM) = 'MAX SUSTAINED WINDS '//
     &     tauData%atcfRcd(1)%vmax//' KT WITH GUSTS TO '//
     &     tauData%atcfRcd(1)%gusts//' KT.'
c
          do i = tauData%numrcrds, 1, -1
C
C**   DO THE 64 KNOT RADII, IF ANY
C
             IF ( i .eq. 3 ) THEN
                CALL RDLINE ( tauData, 3, 4, RLINE)
                LINENM = LINENM + 1
                MLINE(LINENM) = RLINE
             ENDIF
C
C**   DO THE 50 KNOT RADII, IF ANY
C
             IF ( i .eq. 2 ) THEN
                CALL RDLINE ( tauData, 2, 5, RLINE)
                LINENM = LINENM + 1
                MLINE(LINENM) = RLINE
             ENDIF
C
C**   DO THE 34 KNOT RADII, IF ANY
C
             IF ( i .eq. 1 ) THEN
                if ( tauData%aRecord(i)%radii(1) .gt. 0.1 .or.
     &               tauData%aRecord(i)%radii(2) .gt. 0.1 .or.
     &               tauData%aRecord(i)%radii(3) .gt. 0.1 .or.
     &               tauData%aRecord(i)%radii(4) .gt. 0.1 ) then
c
                   CALL RDLINE ( tauData, 1, 6, RLINE)
                   LINENM = LINENM + 1
                   MLINE(LINENM) = RLINE
c
                endif   
C
C**   DO THE 12 FOOT SEAS RADII, IF ANY
C
                if ( tauData%aRecord(i)%seasrad(1) .gt. 0.1 .or.
     &               tauData%aRecord(i)%seasrad(2) .gt. 0.1 .or.
     &               tauData%aRecord(i)%seasrad(3) .gt. 0.1 .or.
     &               tauData%aRecord(i)%seasrad(4) .gt. 0.1 ) then
c
                   CALL RDLINE ( tauData, 1, 7, RLINE)
                   LINENM = LINENM + 1
                   MLINE(LINENM) = RLINE
c
                endif   
             ENDIF
          enddo
      ENDIF
C
cc      PRTRAD = .FALSE.
cc      IF (WINDAD(10:21).NE.'  0  0  0  0') PRTRAD = .TRUE.
cc      IF (WINDAD(22:33).NE.'  0  0  0  0') PRTRAD = .TRUE.
cc      IF (WIND12(10:21).NE.'  0  0  0  0') PRTRAD = .TRUE.
cc      IF (WIND24(10:21).NE.'  0  0  0  0') PRTRAD = .TRUE.
cc      IF (WIND36(10:21).NE.'  0  0  0  0') PRTRAD = .TRUE.
cc      IF (WIND48(10:21).NE.'  0  0  0  0') PRTRAD = .TRUE.
cc      IF (WIND72(10:21).NE.'  0  0  0  0') PRTRAD = .TRUE.
C
cc      IF (PRTRAD) THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'WINDS AND SEAS VARY GREATLY IN EACH QUADRANT.
     &  RADII IN NAUTICAL'
          LINENM = LINENM + 1
          MLINE(LINENM) = 'MILES ARE THE LARGEST RADII EXPECTED ANYWHERE
     & IN THAT QUADRANT.'
cc      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE REPEAT CENTER AND GIVE THE SYNOPTIC POSITION
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'REPEAT...CENTER LOCATED NEAR '
     & //adlat//' '//adlon//' AT'//MDAY//'/'//MTIME//'Z'
C
c**   Get the best track data
c
      call getSingleTAU ( fstRcd, 0, tauData, istat )
c
      if ( istat .eq. 1) then
C
        LINENM = LINENM + 1
        MLINE(LINENM) = 'AT '//ymdh(7:8)//'/'//ymdh(9:10)
     &   //'00Z CENTER WAS LOCATED NEAR '
     &   //tauData%atcfRcd(1)%latns(1:2)//'.'
     &   //tauData%atcfRcd(1)%latns(3:4)//' '
     &   //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &   //tauData%atcfRcd(1)%lonew(4:5)
C
        LINENM = LINENM + 1
        MLINE(LINENM) = ' '
      endif
C
C**   DETERMINE THE RIGHT ENDING, IF NOT A NORMAL ENDING
C
      DO I = 1,5
        ends(I) = ' '
        IF ( TAU(I) .GE. end_time(2:3) ) THEN
           IF ( end_type .EQ.'IN') ends(I) = '...INLAND'
           IF ( end_type .EQ.'DS') ends(I) = '...DISSIPATING'
           IF ( end_type .EQ.'EX') ends(I) = '...EXTRATROPICAL'
        ENDIF
      enddo
C
C**   DETERMINE THE 12 HOUR FORECAST POSITION, WIND, AND WIND FIELDS
C
      call getSingleTAU ( fstRcd, 12, tauData, istat )
c
      if ( istat .eq. 1) then
c
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(1)(7:8)//'/'//
     &     times(1)(9:10)//'00Z '
     &     //tauData%atcfRcd(1)%latns(1:2)//'.'
     &     //tauData%atcfRcd(1)%latns(3:4)//' '
     &     //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &     //tauData%atcfRcd(1)%lonew(4:5)//ends(1)
C
          IF (tauData%aRecord(1)%vmax .gt. 0 ) THEN
c
            LINENM = LINENM + 1
            MLINE(LINENM) = 'MAX WIND '//
     &       tauData%atcfRcd(1)%vmax//' KT...GUSTS '//
     &       tauData%atcfRcd(1)%gusts//' KT.'
c
            do i = tauData%numrcrds, 1, -1
C
C**   DO THE 64 KNOT RADII, IF ANY
C
               IF ( i .eq. 3 ) THEN
                 CALL RDLINE ( tauData, 3, 1, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 50 KNOT RADII, IF ANY
C
               IF ( i .eq. 2 ) THEN
                 CALL RDLINE ( tauData, 2, 2, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 34 KNOT RADII, IF ANY
C
               IF ( i .eq. 1 ) THEN
                 if ( tauData%aRecord(i)%radii(1) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(2) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(3) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(4) .gt. 0.1 ) then
c
                   CALL RDLINE ( tauData, 1, 3, RLINE)
                   LINENM = LINENM + 1
                   MLINE(LINENM) = RLINE
c
                 endif  
               ENDIF
            enddo
          ENDIF
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
C
      ELSEIF (ends(1).NE.' ') THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(1)(7:8)//'/'//
     &     times(1)(9:10)//'00Z'//ends(3)
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
      ENDIF
C
C**   DETERMINE THE 24 HOUR FORECAST POSITION, WIND, AND WIND FIELDS
C
      call getSingleTAU ( fstRcd, 24, tauData, istat )
c
      if ( istat .eq. 1) then
c
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(2)(7:8)//'/'//
     &     times(2)(9:10)//'00Z '
     &     //tauData%atcfRcd(1)%latns(1:2)//'.'
     &     //tauData%atcfRcd(1)%latns(3:4)//' '
     &     //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &     //tauData%atcfRcd(1)%lonew(4:5)//ends(2)
C
          IF (tauData%aRecord(1)%vmax .gt. 0 ) THEN
c
            LINENM = LINENM + 1
            MLINE(LINENM) = 'MAX WIND '//
     &       tauData%atcfRcd(1)%vmax//' KT...GUSTS '//
     &       tauData%atcfRcd(1)%gusts//' KT.'
c
            do i = tauData%numrcrds, 1, -1
C
C**   DO THE 64 KNOT RADII, IF ANY
C
               IF ( i .eq. 3 ) THEN
                 CALL RDLINE ( tauData, 3, 1, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 50 KNOT RADII, IF ANY
C
               IF ( i .eq. 2 ) THEN
                 CALL RDLINE ( tauData, 2, 2, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 34 KNOT RADII, IF ANY
C
               IF ( i .eq. 1 ) THEN
                 if ( tauData%aRecord(i)%radii(1) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(2) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(3) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(4) .gt. 0.1 ) then
c
                   CALL RDLINE ( tauData, 1, 3, RLINE)
                   LINENM = LINENM + 1
                   MLINE(LINENM) = RLINE
c
                 endif  
               ENDIF
            enddo
          ENDIF
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
C
      ELSEIF (ends(2).NE.' ') THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(2)(7:8)//'/'//
     &     times(2)(9:10)//'00Z'//ends(2)
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
      ENDIF
C
C**   DETERMINE THE 36 HOUR FORECAST POSITION, WIND, AND WIND FIELDS
C
      call getSingleTAU ( fstRcd, 36, tauData, istat )
c
      if ( istat .eq. 1) then
c
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(3)(7:8)//'/'//
     &     times(3)(9:10)//'00Z '
     &     //tauData%atcfRcd(1)%latns(1:2)//'.'
     &     //tauData%atcfRcd(1)%latns(3:4)//' '
     &     //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &     //tauData%atcfRcd(1)%lonew(4:5)//ends(3)
C
          IF (tauData%aRecord(1)%vmax .gt. 0 ) THEN
c
            LINENM = LINENM + 1
            MLINE(LINENM) = 'MAX WIND '//
     &       tauData%atcfRcd(1)%vmax//' KT...GUSTS '//
     &       tauData%atcfRcd(1)%gusts//' KT.'
c
            do i = tauData%numrcrds, 1, -1
C
C**   DO THE 64 KNOT RADII, IF ANY
C
               IF ( i .eq. 3 ) THEN
                 CALL RDLINE ( tauData, 3, 1, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 50 KNOT RADII, IF ANY
C
               IF ( i .eq. 2 ) THEN
                 CALL RDLINE ( tauData, 2, 2, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 34 KNOT RADII, IF ANY
C
               IF ( i .eq. 1 ) THEN
                 if ( tauData%aRecord(i)%radii(1) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(2) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(3) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(4) .gt. 0.1 ) then
c
                   CALL RDLINE ( tauData, 1, 3, RLINE)
                   LINENM = LINENM + 1
                   MLINE(LINENM) = RLINE
c
                 endif  
               ENDIF
            enddo
          ENDIF
c
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
C
      ELSEIF (ends(3).NE.' ') THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(3)(7:8)//'/'//
     &     times(3)(9:10)//'00Z'//ends(3)
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
      ENDIF
C
C**   SHIP OBSERVATION LINE
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'REQUEST FOR 3 HOURLY SHIP REPORTS WITHIN 300 MILE
     &S OF '//ADLAT//' '//ADLON
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE 48 HOUR FORECAST POSITION, WIND, AND WIND FIELDS
C
      call getSingleTAU ( fstRcd, 48, tauData, istat )
c
      if ( istat .eq. 1) then
c
          LINENM = LINENM + 1
          MLINE(LINENM) = 'EXTENDED OUTLOOK...USE FOR GUIDANCE ONLY...ER
     &RORS MAY BE LARGE'
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
C
          LINENM = LINENM + 1
          MLINE(LINENM) = 'OUTLOOK VALID '//times(4)(7:8)//'/'//
     &     times(4)(9:10)//'00Z '
     &     //tauData%atcfRcd(1)%latns(1:2)//'.'
     &     //tauData%atcfRcd(1)%latns(3:4)//' '
     &     //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &     //tauData%atcfRcd(1)%lonew(4:5)//ends(4)
C
          IF (tauData%aRecord(1)%vmax .gt. 0 ) THEN
c
            LINENM = LINENM + 1
            MLINE(LINENM) = 'MAX WIND '//
     &       tauData%atcfRcd(1)%vmax//' KT...GUSTS '//
     &       tauData%atcfRcd(1)%gusts//' KT.'
c
            do i = tauData%numrcrds, 1, -1
C
C**   DO THE 50 KNOT RADII, IF ANY
C
               IF ( i .eq. 2 ) THEN
                 CALL RDLINE ( tauData, 2, 2, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 34 KNOT RADII, IF ANY
C
               IF ( i .eq. 1 ) THEN
                 if ( tauData%aRecord(i)%radii(1) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(2) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(3) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(4) .gt. 0.1 ) then
c
                    CALL RDLINE ( tauData, 1, 3, RLINE)
                    LINENM = LINENM + 1
                    MLINE(LINENM) = RLINE
c
                 endif  
               ENDIF
            enddo
          ENDIF
c
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
c
      ELSEIF (ends(4).NE.' ') THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'EXTENDED OUTLOOK...USE FOR GUIDANCE ONLY...ER
     &RORS MAY BE LARGE'
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
C
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(4)(7:8)//'/'//
     &     times(4)(9:10)//'00Z'//ends(4)
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
      ENDIF
C
C**   DETERMINE THE 72 HOUR FORECAST POSITION, WIND, AND WIND FIELDS
c
      call getSingleTAU ( fstRcd, 72, tauData, istat )
c
      if ( istat .eq. 1) then
c
          LINENM = LINENM + 1
          MLINE(LINENM) = 'OUTLOOK VALID '//times(5)(7:8)//'/'//
     &     times(5)(9:10)//'00Z '
     &     //tauData%atcfRcd(1)%latns(1:2)//'.'
     &     //tauData%atcfRcd(1)%latns(3:4)//' '
     &     //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &     //tauData%atcfRcd(1)%lonew(4:5)//ends(5)
C
C
          IF (tauData%aRecord(1)%vmax .gt. 0 ) THEN
c
            LINENM = LINENM + 1
            MLINE(LINENM) = 'MAX WIND '//
     &       tauData%atcfRcd(1)%vmax//' KT...GUSTS '//
     &       tauData%atcfRcd(1)%gusts//' KT.'
c
            do i = tauData%numrcrds, 1, -1
C
C**   DO THE 50 KNOT RADII, IF ANY
C
               IF ( i .eq. 2 ) THEN
                 CALL RDLINE ( tauData, 2, 2, RLINE)
                 LINENM = LINENM + 1
                 MLINE(LINENM) = RLINE
               ENDIF
C
C**   DO THE 34 KNOT RADII, IF ANY
C
               IF ( i .eq. 1 ) THEN
                 if ( tauData%aRecord(i)%radii(1) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(2) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(3) .gt. 0.1 .or.
     &                tauData%aRecord(i)%radii(4) .gt. 0.1 ) then
c
                   CALL RDLINE ( tauData, 1, 3, RLINE)
                   LINENM = LINENM + 1
                   MLINE(LINENM) = RLINE
c
                 endif  
               ENDIF
            enddo
          ENDIF
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
C
      ELSEIF (ends(5).NE.' ') THEN
          LINENM = LINENM + 1
          MLINE(LINENM) = 'FORECAST VALID '//times(5)(7:8)//'/'//
     &     times(5)(9:10)//'00Z'//ends(5)
C
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
      ENDIF
C
C**   DO THE END OF MESSAGE
C
      LINENM = LINENM + 1
      IF ( lastadv(1:2) .EQ. 'NO' ) THEN
          MLINE(LINENM) = 'NEXT ADVISORY AT '//MXDYTM
      ELSE
          MLINE(LINENM) = 'THIS IS THE LAST FORECAST/ADVISORY ISSUED BY
     &THE'
          LINENM = LINENM + 1
          IF (BASIN.NE.'C') THEN
              MLINE(LINENM) = 'NATIONAL HURRICANE CENTER ON THIS SYSTEM'
          ELSE
              MLINE(LINENM) = 'CENTRAL PACIFIC HURRICANE CENTER ON THIS
     &SYSTEM'
          ENDIF
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   WRITE THE FORECAST'S NAME AND ENDING
c
      LINENM = LINENM + 1
      MLINE(LINENM) = 'FORECASTER '//fstr_name
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
      LINENM = LINENM + 1
      MLINE(LINENM) = 'NNNN'
c
C**   OPEN THE MARINE FILE AND WRITE OUT THE MARINE ADVISORY
C
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//
     &            ".fstadv.new"
c
      OPEN ( 31, FILE=file_name, STATUS='UNKNOWN' )
C
      DO I = 1, LINENM
C
         LNEND = LASTCH( MLINE(I) )
         IF ( LNEND .EQ. 0 ) LNEND = 1
C
         WRITE ( 31, '(A)' ) MLINE(I)(1:LNEND)
C
      enddo
C
      CLOSE (31)
C
      RETURN
      END
C*************************************************************
      SUBROUTINE discuss ( fstRcd )
C
C**   THIS SUBROUTINE CREATES THE TROPICAL CYCLONE DISCUSSION
C
      INCLUDE  'dataformats.inc'
c
      common /title/   STRMID, stname, BASIN, ymdh, basin2
      common /timing/  special, sptau, sptime, timezn, daylite, pubfreq
      common /heading/ advnum, afosbin, ADNAME, CLASS, ends(5), msg_path
      common /ending/  accuracy, end_type, end_time, lastadv, fstr_name
c
      common /lines/   MLINE(150),WLINE(25)
      common /warn/    wend, current_tau
      common /ddtime/  DTLINE,DIDYTM
C
      LOGICAL STATUS
c
      integer martau(5), wend, current_tau
C
      CHARACTER*1  BASIN, afosbin, timezn, pubfreq
      character*2  sptau, tau(5), end_type, basin2 
      character*3  advnum, accuracy, lastadv
      CHARACTER*3  special, daylite, end_time, DDAY, DMDIEM
      CHARACTER*4  SPTIME,DTIME,DDAYWK,DMONTH,DTIMZN
      CHARACTER*5  DYEAR
      CHARACTER*8  strmid
      CHARACTER*10 ymdh, stname, fcst_time
      CHARACTER*9  DIDYTM
      CHARACTER*15 fstr_name
      CHARACTER*17 DIRSPD
      CHARACTER*16 ends
      CHARACTER*16 ADNAME
      CHARACTER*24 CLASS
      CHARACTER*21 EDFILE,NDFILE,DISBAT,WIND48,WIND72
      CHARACTER*32 FTITLE
      character*50 msg_path
      character*75 file_name
      CHARACTER*68 MLINE,WLINE,OLINE,DTLINE
C
      DATA FTITLE / 'FORECAST POSITIONS AND MAX WINDS' /
      DATA tau    / '12', '24', '36', '48', '72'/
      data martau / 12, 24, 36, 48, 72 /
c
      type (AID_DATA) fstRcd, tauData
C
C**   BLANK NEW MESSAGE ARRAYS
C
      DO I = 1,150
        MLINE(I) = ' '
      enddo
c
C**   COMPOSE THE HEADER RECORDS
C
      LINENM = 0
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
         MLINE(LINENM) = 'ZCZC MIATCD'//BASIN2//afosbin//' ALL'
      ELSE
         MLINE(LINENM) = 'ZCZC HFOTCD'//BASIN2//afosbin//' ALL'
      ENDIF
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
         MLINE(LINENM) = 'TTAA00 KNHC DDHHMM'
      ELSE
         MLINE(LINENM) = 'TTAA00 PHFO DDHHMM'
      ENDIF
C
C**   IF SPECIAL, DETERMINE THE PROPER NAME AND NUMBER LINE
C
      LINENM = LINENM + 1
      IF ( special .eq. 'NO' ) THEN
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//'DISCUSSION NUMBER '//advnum
      ELSE
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//
     &       'SPECIAL DISCUSSION NUMBER '//advnum
      ENDIF
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
          MLINE(LINENM) = 'NATIONAL WEATHER SERVICE MIAMI FL'
      ELSE
          MLINE(LINENM) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = DTLINE
C
C**   Open, read into memory and close the previous discussion,
c**     IF IT EXISTS
C
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//
     &            ".discus.tmp"
c
      OPEN ( 24, FILE=file_name, STATUS='OLD', ERR=30)
C
C**   FIND, READ, AND WRITE THE OLD DISCUSSION, IF THERE IS ONE
C
      STATUS = .FALSE.
   10 READ ( 24, '(A)', END=20 ) OLINE
      IF (STATUS) THEN
         LINENM = LINENM + 1
         MLINE(LINENM) = OLINE
      ENDIF
      IF ( OLINE(1:32) .EQ. ' ' .AND. (.NOT.STATUS) ) THEN
         STATUS = .TRUE.
         LINENM = LINENM + 1
         MLINE(LINENM) = OLINE
      ENDIF
      IF ( OLINE(1:32) .EQ. FTITLE .AND. STATUS ) go to 20
      GO TO 10
C
   20 CLOSE ( 24 )
      go to 40
C
C**   IF THERE IS NO PREVIOUS DISCUSSION OR IT CANNOT BE READ, INSERT
C**     THREE BLANK LINES
C
   30 CONTINUE
C
      DO I = 1,3
         LINENM = LINENM + 1
         MLINE (LINENM) = ' '
      enddo
C
C**   WRITE THE FORECAST'S NAME
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'FORECASTER '//fstr_name
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
      LINENM = LINENM + 1
      MLINE(LINENM) = FTITLE
C
   40 LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE CURRENT POSITION, IF THERE IS ONE
C
      call getSingleTAU ( fstRcd, current_tau, tauData, istat )
c
      if ( istat .eq. 1) then
c
         LINENM = LINENM + 1
         MLINE(LINENM) = 'INITIAL     '//DIDYTM
     &    //tauData%atcfRcd(1)%latns(1:2)//'.'
     &    //tauData%atcfRcd(1)%latns(3:4)//' '
     &    //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &    //tauData%atcfRcd(1)%lonew(4:5)//'   '
     &    //tauData%atcfRcd(1)%vmax//' KTS'

      ELSE
          GO TO 100
      ENDIF
C
C**   Create each forecast line for the discussion
C
      do i = 1, 5
c
        call dtgmod ( ymdh, martau(i), fcst_time, istat )
c
        call getSingleTAU ( fstRcd, martau(i), tauData, istat )
c
        if ( istat .eq. 1) then
c
           LINENM = LINENM + 1
           MLINE(LINENM) = tau(i)//'HR VT     '//fcst_time(7:8)//
     &      '/'//fcst_time(9:10)//'00Z '
     &      //tauData%atcfRcd(1)%latns(1:2)//'.'
     &      //tauData%atcfRcd(1)%latns(3:4)//' '
     &      //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &      //tauData%atcfRcd(1)%lonew(4:5)//'   '
     &      //tauData%atcfRcd(1)%vmax//' KTS'//ends(i)
c
        ELSE
            IF ( ends(i) .NE. ' ' ) THEN
               LINENM = LINENM + 1
               MLINE(LINENM) = tau(i)//'HR VT     '//fcst_time(7:8)//
     &          '/'//fcst_time(9:10)//'00Z'//ends(i)
            ENDIF
c
            GO TO 100
c
        ENDIF
      enddo
C
  100 CONTINUE
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'NNNN'
C
C**   OPEN, WRITE out THE NEW TROPICAL CYCLONE DISCUSSION and close the file
C
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//
     &            ".discus.new"
c
      OPEN ( 32, FILE=file_name, STATUS='UNKNOWN' )
C
      DO I = 1, LINENM
C
         LNEND = LASTCH( MLINE(I) )
         IF ( LNEND .EQ. 0 ) LNEND = 1
C
         WRITE ( 32, '(A)' ) MLINE(I)(1:LNEND)
C
      enddo
C
      CLOSE ( 32 )
C
      RETURN
      END
C*************************************************************
      SUBROUTINE PUBLIC ( fstRcd )
C
C**   THIS SUBROUTINE CREATES THE PUBLIC ADVISORY
C
      INCLUDE  'dataformats.inc'
c
      COMMON /title/   STRMID, stname, BASIN, YMDH, basin2
      common /timing/  special, sptau, sptime, timezn, daylite, pubfreq
      COMMON /heading/ advnum, afosbin, ADNAME, CLASS, ends(5), msg_path
      common /ending/  accuracy, end_type, end_time, lastadv, fstr_name
c
      COMMON /LINES/   MLINE(150),WLINE(25)
      COMMON /WARN/    WEND, current_tau
      COMMON /PPTIME/  PTIME,PTIMZN,PDAYWK,PMONTH,PDAY,PYEAR,PIDYTM(3),
     & PXDYTM,PZTIME
c
      INTEGER SPDAD,WINAD,FORWIN,RADWIN(4),WINRAD,WNRDMI,WNRDKM,WEND
      INTEGER MPHSPD,KPHSPD,vmax_cur,vmax_24, current_tau
      LOGICAL STATUS,HURWIN
C
      character*1  afosbin, timezn, pubfreq, basin
      character*2  sptau, end_type, fsttp, basin2
      character*3  fstr_initials, special, advnum, daylite, accuracy
      character*3  end_time, lastadv
      character*4  sptime
      character*8  strmid
      character*10 ymdh, stname
      character*15 fstr_name
      character*16 adname, ends
      character*24 class
      character*25 line
      character*50 msg_path
      character*75 file_name
C
      CHARACTER*2   ADSPD,SPDMPH,SPDKPH
      CHARACTER*3   WINMPH,WINKPH,RADMI,RADKM
      CHARACTER*3   PDAY,PMDIEM
      CHARACTER*4   SFCPRS,PDAYWK,PMONTH,PTIMZN,PZTIME
      CHARACTER*5   INPRS,PYEAR,LONG
      CHARACTER*10  PTIME
      CHARACTER*17  DIRSPD,DIRECT,CURDIR
      CHARACTER*21  PUBBAT
      CHARACTER*22  OPFILE,NPFILE
      CHARACTER*25  PXDYTM,PIDYTM
      CHARACTER*68  MLINE,WLINE,OLINE
c
      type (AID_DATA) fstRcd, tauData
C
C**   BLANK MESSAGE ARRAY
C
      DO I = 1,150
        MLINE(I) = ' '
      enddo
C
C**   COMPOSE THE HEADER RECORDS
C
      LINENM = 0
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
         MLINE(LINENM) = 'ZCZC MIATCP'//BASIN2//afosbin//' ALL'
      ELSE
         MLINE(LINENM) = 'ZCZC HFOTCP'//BASIN2//afosbin//' ALL'
      ENDIF
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
          MLINE(LINENM) = 'TTAA00 KNHC DDHHMM'
      ELSE
          MLINE(LINENM) = 'TTAA00 PHFO DDHHMM'
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'BULLETIN'
C
C**   IF SPECIAL, DETERMINE THE NAME AND NUMBER LINE
C
      LINENM = LINENM + 1
      IF ( special .eq. 'NO' ) THEN
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//'ADVISORY NUMBER '//advnum
      ELSE
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &       ADNAME(1:INDEX(ADNAME,'  '))//'SPECIAL ADVISORY NUMBER '//
     &       advnum
      ENDIF
C
      LINENM = LINENM + 1
      IF ( BASIN .NE. 'C' ) THEN
          MLINE(LINENM) = 'NATIONAL WEATHER SERVICE MIAMI FL'
      ELSE
          MLINE(LINENM) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = PTIME(1:INDEX(PTIME,'  ') - 1)//PTIMZN//PDAYWK//
     & PMONTH//PDAY//PYEAR
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   ADD WARNING MESSAGE, IF THERE IS ONE
C
      IF (WEND.GT.0) THEN
          DO I = 1,WEND
             LINENM = LINENM + 1
             MLINE(LINENM) = WLINE(I)
          enddo
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
      ENDIF
C
C**   DETERMINE THE 24-hour forecast maximum wind speed
C
      call getSingleTAU ( fstRcd, 24, tauData, istat )
c
      if ( istat .eq. 1) then
         vmax_24 = tauData%aRecord(1)%vmax
      else
         vmax_24 = 0
      endif   
C
C**   DETERMINE THE CURRENT values
C
      call getSingleTAU ( fstRcd, current_tau, tauData, istat )
      if ( istat .ne. 1) stop 'There is no current_tau data'
c
C**   CURRENT POSITION LINES
C
        LINENM = LINENM + 1
        MLINE(LINENM) = 'AT '//PTIME(1:INDEX(PTIME,'  ') - 1)
     &   //PTIMZN//'...'//PZTIME//'Z...THE CENTER OF '
     &   //CLASS(1:INDEX(CLASS,'  '))
C
        LINENM = LINENM + 1
        MLINE(LINENM) = ADNAME(1:INDEX(ADNAME,'  '))//
     &   'WAS LOCATED NEAR LATITUDE '
     &   //tauData%atcfRcd(1)%latns(1:2)//'.'
     &   //tauData%atcfRcd(1)%latns(3:3)
     &   //' NORTH...'
C
        LONG = ' WEST'
        IF ( tauData%atcfRcd(1)%lonew(5:5) .LT. 'E' ) LONG = ' EAST'
c
        LINENM = LINENM + 1
        MLINE(LINENM) = 'LONGITUDE '
     &   //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &   //tauData%atcfRcd(1)%lonew(4:4)//long//
     &   ' OR ABOUT XXX MILES...XXX KM...'
c
        LINENM = LINENM + 1
        MLINE(LINENM) = ' '
C
C**   DETERMINE THE CURRENT MOVEMENT LINES
C
        MPHSPD = INT(tauData%aRecord(1)%speed*1.1516 + 0.5)
        WRITE (SPDMPH,'(I2)') MPHSPD
        KPHSPD = INT(tauData%aRecord(1)%speed*1.8533 + 0.5)
        WRITE (SPDKPH,'(I2)') KPHSPD
        CURDIR = DIRECT ( tauData%aRecord(1)%dir )
C
        LINENM = LINENM + 1
C
        IF ( tauData%atcfRcd(1)%ty .EQ. 'TD' .OR. 
     &       tauData%atcfRcd(1)%ty .EQ. 'SD' ) MLINE(LINENM) =
     &   'THE DEPRESSION IS MOVING TOWARD THE '
     &   //CURDIR(1:INDEX(CURDIR,'  '))//'NEAR '//SPDMPH//' MPH'
C
        IF ( tauData%atcfRcd(1)%ty .EQ. 'SS' ) MLINE(LINENM) =
     &   'THE STORM IS MOVING TOWARD THE '
     &   //CURDIR(1:INDEX(CURDIR,'  '))//'NEAR '//SPDMPH//' MPH'
C
        IF ( tauData%atcfRcd(1)%ty .EQ. 'TS' .OR.
     &       tauData%atcfRcd(1)%ty .EQ. 'HU' ) MLINE(LINENM) =
     &   ADNAME(1:INDEX(ADNAME,'  '))//'IS MOVING TOWARD THE '
     &   //CURDIR(1:INDEX(CURDIR,'  '))//'NEAR '//SPDMPH//' MPH'
C
        LINENM = LINENM + 1
        MLINE(LINENM) = '...'//SPDKPH//' KM/HR...AND THIS MOTION IS EXPE
     &CTED TO '
c
        LINENM = LINENM + 1
        MLINE(LINENM) = ' '
C
C**   DETERMINE THE CURRENT INTENSITY LINES
C
        vmax_cur = tauData%aRecord(1)%vmax
c
        MPHSPD = INT((vmax_cur*1.1516 + 2.5)/5.0)*5
c
c**   Correction to force 115kt to be 135mph (i.e. Cat 4)
c
        if ( mphspd .eq. 130 ) mphspd = 135
        WRITE (WINMPH,'(I3)') MPHSPD
        KPHSPD = INT((vmax_cur*1.8533 + 2.5)/5.0)*5
        WRITE (WINKPH,'(I3)') KPHSPD
c
        LINENM = LINENM + 1
        MLINE(LINENM) = 'MAXIMUM SUSTAINED WINDS ARE NEAR '//WINMPH//
     & ' MPH...'//WINKPH//' KM/HR...WITH HIGHER'
C
        linenm = linenm + 1
        if ( vmax_24 .eq. 0) then
           mline(linenm) = 'GUSTS.'
c
           else
           IF ( (vmax_24  - vmax_cur) .GT. 5 ) THEN
              MLINE(LINENM) = 'GUSTS.  SOME STRENGTHENING IS FORECAST DU
     &RING THE NEXT 24 HOURS.'
c
           ELSEIF ( (vmax_24 - vmax_cur) .LT. -5 ) THEN
              MLINE(LINENM) = 'GUSTS.  SOME WEAKENING IS FORECAST DURING
     & THE NEXT 24 HOURS.'
c
           ELSE
              MLINE(LINENM) = 'GUSTS.  LITTLE CHANGE IN STRENGTH IS FORE
     &CAST DURING THE NEXT'
              LINENM = LINENM + 1
              MLINE(LINENM) = '24 HOURS.'
c
           ENDIF
        endif
c  
        LINENM = LINENM + 1
        MLINE(LINENM) = ' '
C
C**   DETERMINE THE CURRENT WIND RADII LINES FOR HURRICANE AND TROPICAL
C**     STORM FORCE WINDS
C
        HURWIN = .FALSE.
        IF ( vmax_cur .GT. 64) THEN
           HURWIN = .TRUE.
c
           WINRAD = 0
           DO I = 1,4
             IF ( tauData%aRecord(3)%radii(i) .GT. WINRAD )
     &        WINRAD = tauData%aRecord(3)%radii(i)
           enddo
c
           WNRDMI = INT((WINRAD*1.1516 + 2.5)/5.0)*5
           WRITE (RADMI,'(I3)') WNRDMI
           WNRDKM = INT((WINRAD*1.8533 + 2.5)/5.0)*5
           WRITE (RADKM,'(I3)') WNRDKM
c
           LINENM = LINENM + 1
           MLINE(LINENM) = 'HURRICANE FORCE WINDS EXTEND OUTWARD UP TO '
     &      //RADMI//' MILES...'//RADKM//' KM...'
        ENDIF
C
        IF ( vmax_cur .GT. 34) THEN
c
          WINRAD = 0
          DO I = 1,4
            IF ( tauData%aRecord(1)%radii(i) .GT. WINRAD ) 
     &       WINRAD = tauData%aRecord(1)%radii(i)
          enddo
c
          WNRDMI = INT((WINRAD*1.1516 + 2.5)/5.0)*5
          WRITE (RADMI,'(I3)') WNRDMI
          WNRDKM = INT((WINRAD*1.8533 + 2.5)/5.0)*5
          WRITE (RADKM,'(I3)') WNRDKM
c
          IF (HURWIN) THEN
              LINENM = LINENM + 1
              MLINE(LINENM) = 'FROM THE CENTER...AND TROPICAL STORM FORC
     &E WINDS EXTEND OUTWARD UP '
              LINENM = LINENM + 1
              MLINE(LINENM) = 'TO '//RADMI//' MILES...'//RADKM//' KM.'
          ELSE
              LINENM = LINENM + 1
C
              IF ( tauData%atcfRcd(1)%ty .NE. 'SS') THEN
                  MLINE(LINENM) = 'TROPICAL STORM FORCE WINDS EXTEND OUT
     &WARD UP TO '//RADMI//' MILES'
                  LINENM = LINENM + 1
                  MLINE(LINENM) = '...'//RADKM//' KM FROM THE CENTER.'
              ELSE
                  MLINE(LINENM) = 'WINDS OF 40 MPH EXTEND OUTWARD UP TO
     &'//RADMI//' MILES...'//RADKM//' KM'
                  LINENM = LINENM + 1
                  MLINE(LINENM) = 'FROM THE CENTER.'
              ENDIF
C
          ENDIF
c
          LINENM = LINENM + 1
          MLINE(LINENM) = ' '
c
      ENDIF
C
C**   DETERMINE THE ESTIMATED MINIMUM CENTRAL PRESSURE LINE
C
      PRSIN = tauData%aRecord(1)%mslp*0.02953
      WRITE (INPRS,'(F5.2)') PRSIN
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'ESTIMATED MINIMUM CENTRAL PRESSURE IS '
     & //tauData%atcfrcd(1)%mslp//' MB...'//INPRS//' INCHES.'
c
c**   Add the old public advisory query
c
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
      LINENM = LINENM + 1
      MLINE(LINENM) = '*****************************************'
      LINENM = LINENM + 1
      MLINE(LINENM) = 'Are any blocks of text required from the previous
     & Public Advisory'
      LINENM = LINENM + 1
      MLINE(LINENM) = 'attached below????  If so, move the blocks of tex
     &t and delete all'
      LINENM = LINENM + 1
      MLINE(LINENM) = 'lines past the NNNN line.'
      LINENM = LINENM + 1
      MLINE(LINENM) = '*****************************************'
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE REPEAT SECTION
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'REPEATING THE '//PTIME(1:INDEX(PTIME,'  ') - 1)
     & //PTIMZN//' POSITION...'
     & //tauData%atcfRcd(1)%latns(1:2)//'.'
     & //tauData%atcfRcd(1)%latns(3:3)//' '
     & //tauData%atcfRcd(1)%latns(4:4)//'...'
     & //tauData%atcfRcd(1)%lonew(1:3)//'.'
     & //tauData%atcfRcd(1)%lonew(4:4)//' '
     & //tauData%atcfRcd(1)%lonew(5:5)//'.  MOVEMENT'
c
      LINENM = LINENM + 1
      MLINE(LINENM) = 'TOWARD...'//CURDIR(1:INDEX(CURDIR,'  '))//'NEAR '
     &//SPDMPH//' MPH.  MAXIMUM SUSTAINED'
c
      LINENM = LINENM + 1
      MLINE(LINENM) = 'WINDS...'//WINMPH//' MPH.  MINIMUM CENTRAL PRESSU
     &RE...'//tauData%atcfRcd(1)%mslp//' MB.'
C
C**   IF THERE'S A WARNING, WRITE THESE LINES TO THE PUBLIC ADVISORY
C
      IF ( WEND .GT. 0 .AND. LASTCH( WLINE(1) ) .GT. 0 ) THEN
         LINENM = LINENM + 1
         MLINE(LINENM) = ' '
C
         LINENM = LINENM + 1
         MLINE(LINENM) = 'FOR STORM INFORMATION SPECIFIC TO YOUR AREA...
     &PLEASE MONITOR'
         LINENM = LINENM + 1
         MLINE(LINENM) = 'PRODUCTS ISSUED BY YOUR LOCAL WEATHER OFFICE.'
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   DETERMINE THE END OF MESSAGE LINES
C
      LINENM = LINENM + 1
      IF ( lastadv .EQ. 'NO' ) THEN
          IF ( pubfreq .EQ. '3' ) THEN
              IF (BASIN.NE.'C') THEN
                  MLINE(LINENM) = 'AN INTERMEDIATE ADVISORY WILL BE ISSU
     &ED BY THE NATIONAL'
              ELSE
                  MLINE(LINENM) = 'AN INTERMEDIATE ADVISORY WILL BE ISSU
     &ED BY THE CENTRAL PACIFIC'
              ENDIF
              LINENM = LINENM + 1
              MLINE(LINENM) = 'HURRICANE CENTER AT '//PIDYTM(2)
     &         (1:INDEX(PIDYTM(2),'  ') - 1)//
     &         ' FOLLOWED BY THE NEXT'
              LINENM = LINENM + 1
              MLINE(LINENM) = 'COMPLETE ADVISORY AT '//PXDYTM
          ELSE IF (pubfreq .eq. '2' ) THEN
              IF (BASIN.NE.'C') THEN
                  MLINE(LINENM) = 'INTERMEDIATE ADVISORIES WILL BE ISSUE
     &D BY THE NATIONAL'
              ELSE
                  MLINE(LINENM) = 'INTERMEDIATE ADVISORIES WILL BE ISSUE
     &D BY THE CENTRAL PACIFIC'
              ENDIF
              LINENM = LINENM + 1
              MLINE(LINENM) = 'HURRICANE CENTER AT '//PIDYTM(1)
     &         (1:INDEX(PIDYTM(1),'  ') - 1)//' AND '//PIDYTM(3)
     &         (1:INDEX(PIDYTM(3),'  ') - 1)//
     &         ' FOLLOWED'
              LINENM = LINENM + 1
              MLINE(LINENM) = 'BY THE NEXT COMPLETE ADVISORY AT '//
     &         PXDYTM
          ELSE
              IF (BASIN.NE.'C') THEN
                  MLINE(LINENM) = 'THE NEXT ADVISORY WILL BE ISSUED BY T
     &HE NATIONAL'
              ELSE
                  MLINE(LINENM) = 'THE NEXT ADVISORY WILL BE ISSUED BY T
     &HE CENTRAL PACIFIC'
              ENDIF
              LINENM = LINENM + 1
              MLINE(LINENM) = 'HURRICANE CENTER AT '//PXDYTM
          ENDIF
      ELSE
          MLINE(LINENM) = 'THIS IS THE LAST PUBLIC ADVISORY ISSUED BY TH
     &E'
          LINENM = LINENM + 1
          IF (BASIN.NE.'C') THEN
              MLINE(LINENM) = 'NATIONAL HURRICANE CENTER ON THIS SYSTEM.
     &'
          ELSE
              MLINE(LINENM) = 'CENTRAL PACIFIC HURRICANE CENTER ON THIS
     &SYSTEM.'
          ENDIF
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   WRITE THE FORECAST'S NAME AND ENDING
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'FORECASTER '//fstr_name
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
      LINENM = LINENM + 1
      MLINE(LINENM) = 'NNNN'
C
C**   OPEN THE PUBLIC FILE AND WRITE OUT THE NEW PUBLIC ADVISORY
C
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//
     &            ".public.new"
c
      OPEN ( 33, FILE=file_name, STATUS='UNKNOWN' )
C
      DO I = 1, LINENM
C
         LNEND = LASTCH( MLINE(I) )
         IF ( LNEND .EQ. 0 ) LNEND = 1
C
         WRITE ( 33, '(A)' ) MLINE(I)(1:LNEND)
C
      enddo
C
      CLOSE (33)
C
      RETURN
      END
C*************************************************************
      SUBROUTINE problty_msg ( fstRcd, nsta, stanam, psvg )
C
C**   THIS SUBROUTINE CREATES THE STRIKE PROBABILITY MESSAGE
C
      include 'dataformats.inc'
c
      COMMON /lines/   MLINE(150),WLINE(25)
      COMMON /title/   STRMID, stname, BASIN, YMDH, basin2
      common /timing/  special, sptau, sptime, timezn, daylite, pubfreq
      COMMON /heading/ advnum, afosbin, ADNAME, CLASS, ends(5), msg_path
      common /ending/  accuracy, end_type, end_time, lastadv, fstr_name
      common /warn/    wend, current_tau
      COMMON /pptime/  PTIME, PTIMZN, PDAYWK, PMONTH, PDAY, PYEAR,
     &                 PIDYTM(3), PXDYTM, PZTIME
      common /pbtimes/ pbyear(4), pbmonth(4), pbdate(4), pbday(4),
     &                 pbhour(4), pbampm(4), pbtimzn(4)
c
cc      COMMON /head1i/NDTG,NUMBA,MXW
cc      common /head2i/ITD(7),IDA,IMO,IYR
cc      COMMON /head3c/ZONE,SNAME
cc      common /head4c/AP(7),DW(7),TYPE
cc      COMMON /S/STANAM(150),latlon(7)
c
      integer wend, current_tau
      INTEGER PDA,PDB,PDC
      INTEGER PSVG(25,150)
c
      character*1  afosbin, timezn, pubfreq, basin
      character*2  sptau, end_type, fsttp, basin2
      character*2  pbdate, pbhour, pbampm
      CHARACTER*2  PR1,PRA,PRB,PRC,PRD,AP
      character*3  fstr_initials, special, advnum, daylite, accuracy
      character*3  end_time, lastadv
      character*3  pbmonth, pbday, pbtimzn
      character*4  sptime, pbyear
      character*8  strmid
      character*10 ymdh, stname
      character*15 fstr_name
      character*16 adname, ends
      character*24 class
      character*25 line
      character*50 msg_path
      character*75 file_name
C
      CHARACTER*3  PDAY,PMDIEM
      CHARACTER*4  PDAYWK,PMONTH,PTIMZN,PZTIME
      CHARACTER*5  PYEAR,LONG
      CHARACTER*10 PTIME
      CHARACTER*25 PXDYTM,PIDYTM
      CHARACTER*68 MLINE,wline
C
      CHARACTER*1  TYPE
      CHARACTER*3  ZONE,AMON(12),DW
      character*4  simp
      CHARACTER*10 SNAME
      CHARACTER*16 STANAM(150)
C
      DATA AMON/'JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP',
     & 'OCT','NOV','DEC'/
      data SIMP/'SIMP'/
c
      type (AID_DATA) fstRcd, tauData
C
C**   BLANK MESSAGE ARRAY
C
      DO I = 1,150
         MLINE(I) = ' '
      enddo
C
C**   COMPOSE THE HEADER RECORDS
C
      LINENM = 0
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'ZCZC MIASPFAT'//afosbin//' ALL'
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'TTAA00 KNHC DDHHMM'
C
C**   IF SPECIAL, DETERMINE THE NAME AND NUMBER LINE
C
      LINENM = LINENM + 1
      IF ( special .EQ. 'NO') THEN
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &        ADNAME(1:INDEX(ADNAME,'  '))//
     &        'PROBABILITIES NUMBER '//advnum
      ELSE
          MLINE(LINENM) = CLASS(1:INDEX(CLASS,'  '))//
     &        ADNAME(1:INDEX(ADNAME,'  '))//
     &        'SPECIAL PROBABILITIES NUMBER'//advnum
      ENDIF
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'NATIONAL WEATHER SERVICE MIAMI FL'
C
      LINENM = LINENM + 1
      MLINE(LINENM) = PTIME(1:INDEX(PTIME,'  ') - 1)//PTIMZN//PDAYWK//
     & PMONTH//PDAY//PYEAR
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   PLANNING STATEMENT
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'PROBABILITIES FOR GUIDANCE IN HURRICANE PROTECTIO
     &N'
      LINENM = LINENM + 1
      MLINE(LINENM) = 'PLANNING BY GOVERNMENT AND DISASTER OFFICIALS'
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
c
c**   Determine the current values
c
      call getSingleTAU ( fstRcd, current_tau, tauData, istat )
      if (istat .ne. 1 ) stop 'There is no current_tau data'
C
C**   CURRENT POSITION LINE
C
      LINENM = LINENM + 1
C
      IF ( tauData%atcfRcd(1)%ty .eq. 'TD' .or. 
     &     tauData%atcfRcd(1)%ty .eq. 'SD' ) MLINE(LINENM) = 'AT '//
     & PTIME(1:INDEX(PTIME,'  ') - 1)//PTIMZN//'...'//PZTIME//
     & 'Z...THE DEPRESSION CENTER WAS LOCATED NEAR'
C
      IF ( tauData%atcfRcd(1)%ty .eq. 'SS' ) MLINE(LINENM) = 'AT '//
     & PTIME(1:INDEX(PTIME,'  ') - 1)//PTIMZN//'...'//PZTIME//
     & 'Z...THE STORM CENTER WAS LOCATED NEAR'
C
      IF ( tauData%atcfRcd(1)%ty .EQ. 'TS' .OR.
     &     tauData%atcfRcd(1)%ty .EQ. 'HU' ) MLINE(LINENM) = 'AT '//
     & PTIME(1:INDEX(PTIME,'  ') - 1)//PTIMZN//'...'//PZTIME//
     & 'Z...THE CENTER OF '//ADNAME(1:INDEX(ADNAME,'  '))//
     & 'WAS LOCATED NEAR'
C
      LONG = ' WEST'
      if (tauData%atcfRcd(1)%lonew(5:5) .eq. 'E' ) long = ' EAST'
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'LATITUDE '
     &     //tauData%atcfRcd(1)%latns(1:2)//'.'
     &     //tauData%atcfRcd(1)%latns(3:3)//' NORTH...LONGITUDE '
     &     //tauData%atcfRcd(1)%lonew(1:3)//'.'
     &     //tauData%atcfRcd(1)%lonew(4:4)//long
c
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   GET THE SECOND VARIABLE TITLE RIGHT FOR THE RIGHT INTENSITY
C
      linenm = linenm + 1
      IF ( tauData%atcfRcd(1)%ty .eq. 'TD' .or.
     &     tauData%atcfRcd(1)%ty .eq. 'SD' ) WRITE ( mLINE(linenm), 1)
    1 FORMAT ('CHANCES OF CENTER OF THE DEPRESSION PASSING WITHIN 65 NAU
     &TICAL MILES')
      IF ( tauData%atcfRcd(1)%ty .eq. 'TS' .or.
     &     tauData%atcfRcd(1)%ty .eq. 'SS' ) WRITE ( mLINE(linenm), 2)
    2 FORMAT ('CHANCES OF CENTER OF THE STORM PASSING WITHIN 65 NAUTICAL
     & MILES')
      IF (tauData%atcfRcd(1)%ty .eq. 'HU' ) WRITE ( mLINE(linenm), 3)
    3 FORMAT ('CHANCES OF CENTER OF THE HURRICANE PASSING WITHIN 65 NAUT
     &ICAL MILES')
c
      LINEnm = LINEnm + 1
      WRITE (mLINE(linenm),109) pbhour(4),pbampm(4),pbtimzn(4),pbday(4),
     & pbmonth(4),pbdate(4),pbyear(4)
  109 FORMAT ('OF LISTED LOCATIONS THROUGH ',a2,A2,1X,A3,1X,A3,1X,A3,1X,
     & a2,1X,a4)
c
      LINEnm = LINEnm + 1
      WRITE (mLINE(linenm),'('' '')')
      LINEnm = LINEnm + 1
      WRITE (mLINE(linenm),'(''LOCATION           A  B  C  D  E   '',
     &                       ''LOCATION           A  B  C  D  E'')')
      LINEnm = LINEnm + 1
      WRITE (mLINE(linenm),'('' '')')
C
      DO 120 K = 1,nsta
      DO 120 J = 2,25
         IF (PSVG(J,K).LT.PSVG(J - 1,K)) PSVG(J,K) = PSVG(J - 1,K)
 120  CONTINUE
C
      kend = 0
      DO K = 1, nsta
C
C**   CHANGED .LT. TO .LE. TO ELIMINATE CASES OF 1% PROB.
C
      IF (PSVG(25,K).GT.1.AND.STANAM(K)(1:4).NE.SIMP) THEN
C
          LPDA = PSVG(13,K) - PSVG(9,K)
          WRITE (PRA,'(I2)') LPDA
          IF (LPDA.LT.1) PRA = ' X'
C
          LPDB = PSVG(17,K) - PSVG(13,K)
          WRITE (PRB,'(I2)') LPDB
          IF (LPDB.LT.1) PRB = ' X'
C
          LPDC = PSVG(25,K) - PSVG(17,K)
          WRITE (PRC,'(I2)') LPDC
          IF (LPDC.LT.1) PRC = ' X'
C
          WRITE (PR1,'(I2)') PSVG(9,K)
          IF (PSVG(9,K).LT.1) PR1 = ' X'
C
          WRITE (PRD,'(I2)') PSVG(25,K)
          IF (PSVG(25,K).LT.1) PRD = ' X'
C
          LINEnm = LINEnm + 1
          WRITE ( mLINE(LINEnm), 4 ) STANAM(K), PR1, PRA, PRB, PRC, PRD
    4     FORMAT( A16, 2X, 4( A2, 1X ), A2 )
c
          if ( k .eq. 1 ) lbegin = linenm
          kend = kend + 1
C
      ENDIF
C
      enddo
c
c**   Make two columns of probabilities
c
      nhalf = kend/2
      lend  = lbegin + nhalf + jmod(kend,2) - 1
c
      do kk = lbegin, lend
         mline(kk)(36:67) = mline(kk + nhalf + jmod(kend,2))(1:32)
      enddo
c
      linenm = lend
C
c**   Write out the column definitions
c
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'('' '')')
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''COLUMN DEFINITION   PROBABILITIES IN PERC
     &ENT'')')
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''A IS PROBABILITY FROM NOW TO '',a2,A2,1X,
     & A3)') pbhour(1),pbampm(1),pbday(1)
      LINEnm = LINEnm + 1
      WRITE (mlINE(LINEnm),'(''FOLLOWING ARE ADDITIONAL PROBABILITIES'')
     &')
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''B FROM '',a2,A2,1X,A3,'' TO '',a2,A2,1X,
     & A3)') pbhour(1),pbampm(1),pbday(1),pbhour(2),pbampm(2),pbday(2)
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''C FROM '',a2,A2,1X,A3,'' TO '',a2,A2,1X,
     & A3)') pbhour(2),pbampm(2),pbday(2),pbhour(3),pbampm(3),pbday(3)
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''D FROM '',a2,A2,1X,A3,'' TO '',a2,A2,1X,
     & A3)') pbhour(3),pbampm(3),pbday(3),pbhour(4),pbampm(4),pbday(4)
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''E IS TOTAL PROBABILITY FROM NOW TO '',a2,
     & A2,1X,A3)') pbhour(4),pbampm(4),pbday(4)
      LINEnm = LINEnm + 1
      WRITE (mLINE(LINEnm),'(''X MEANS LESS THAN ONE PERCENT'')')
c
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
C**   WRITE THE FORECAST'S NAME AND FOUR NNNN'S
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'FORECASTER '//fstr_name
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
      LINENM = LINENM + 1
      MLINE(LINENM) = ' '
C
      LINENM = LINENM + 1
      MLINE(LINENM) = 'NNNN'
C
C**   Open the problty file and write out the new problty message
C
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//
     &            ".prblty.new"
c
      open ( 34, file=file_name, status='unknown' )
c
      DO I = 1, LINENM
C
         LNEND = LASTCH( MLINE(I) )
         IF ( LNEND .EQ. 0 ) LNEND = 1
C
         WRITE ( 34, '(A)' ) MLINE(I)(1:LNEND)
c
      enddo
C
      CLOSE ( 34 )
C
      RETURN
      END
C*************************************************************
      SUBROUTINE problty_tbl ( arrayp )
C
C**   THIS SUBROUTINE CREATES THE STRIKE PROBABILITY TABLE
C
      COMMON /title/   STRMID, stname, BASIN, YMDH, basin2
      COMMON /heading/ advnum, afosbin, ADNAME, CLASS, ends(5), msg_path
c
      real arrayp( 96, 60 )
c
      character*1  afosbin, basin
      character*2  basin2
      character*3  advnum
      character*8  strmid
      character*10 ymdh, stname
      character*16 adname, ends
      character*24 class
      character*50 msg_path
      character*75 file_name
c
C**   Open the probability table file and write it out.
C
      file_name = msg_path(1:lastch( msg_path ))//"/"//strmid//
     &            ".prblty_tbl.new"
c
      open ( 35, file=file_name, status='unknown' )
c
      DO j = 1, 60
C
         WRITE ( 35, '(16f5.1)' ) ( arrayp( i, j ), i = 1, 96 )
c
      enddo
C
      CLOSE ( 35 )
C
      RETURN
      END
C**************************************************************************
        FUNCTION LASTCH ( STRING )
C
C**     RETURNS THE POSITION OF THE LAST NON-BLANK CHARACTER OF A
C**             STRING
C
        CHARACTER*(*) STRING
C
        LAST = LEN(STRING)
C
        DO 10 I = LAST,1,-1
C
        IF (STRING(I:LAST).NE.' ') THEN
            LASTCH = I
            RETURN
        ENDIF
C
   10   CONTINUE
C
        LASTCH = 0
C
        RETURN
        END
C*********************************************************************
        FUNCTION IWKDAY ( IYEAR, IMONTH, IDAY )
C
C*      THIS FUNCTION RETURNS THE DAY OF THE WEEK.
C*      INPUT THE CENTURY (FIRST TWO DIGITS OF THE YEAR), THE YEAR (THE
C*      LAST TWO DIGITS OF THE YEAR), THE MONTH, AND THE DAY.  THE YEAR
C*      MUST BE DIMINISHED BY ONE IF THE MONTH IS JANUARY OR FEBRUARY.
C
C*      THE FORMULA WAS DEVELOPED BY KARL FRIEDRICH GAUSS AND IS
C
C*      W = (D + M +C + Y) MODULO 7
C
C*      WHERE W IS THE DAY OF THE WEEK (SUNDAY = 1), D IS THE DAY OF THE
C*      MONTH, AND M, C, AND Y ARE NUMBERS DEPENDING ON THE MONTH, THE
C*      CENTURY, AND THE YEAR, RESPECTIVELY.  THESE VALUES ARE INCLUDED
C*      AS TABLES IN THE PROGRAM.
C
C*      REFERENCE:  MAURICE KRAITCHIK, MATHEMATICAL RECREATIONS, W. W.
C*      NORTON & COMPANY, INC., NEW YORK, 1942; DOVER PUBLICATIONS,
C*      INC., NEW YORK, 1953 (2ND REVISED ED.), PP. 110-111.
C
        DIMENSION KCNTY(24),MNTH(24),IYR(200)
C
        DATA KCNTY/15,1,16,0,17,5,18,3,19,1,20,0,21,5,22,3,23,1,24,0,
     1 25,5,26,3/
        DATA MNTH/1,1,2,4,3,3,4,6,5,1,6,4,7,6,8,2,9,5,10,0,11,3,12,5/
        DATA IYR/00,0,01,1,02,2,03,3,     04,5,05,6,
     1           06,0,07,1,     08,3,09,4,10,5,11,6,
     2                12,1,13,2,14,3,15,4,     16,6,
     3           17,0,18,1,19,2,     20,4,21,5,22,6,
     4           23,0,     24,2,25,3,26,4,27,5,
     5           28,0,29,1,30,2,31,3,     32,5,33,6,
     6           34,0,35,1,     36,3,37,4,38,5,39,6,
     7                40,1,41,2,42,3,43,4,     44,6,
     8           45,0,46,1,47,2,     48,4,49,5,50,6,
     9           51,0,     52,2,53,3,54,4,55,5,
     1           56,0,57,1,58,2,59,3,     60,5,61,6,
     2           62,0,63,1,     64,3,65,4,66,5,67,6,
     3                68,1,69,2,70,3,71,4,     72,6,
     4           73,0,74,1,75,2,     76,4,77,5,78,6,
     5           79,0,     80,2,81,3,82,4,83,5,
     6           84,0,85,1,86,2,87,3,     88,5,89,6,
     7           90,0,91,1,     92,3,93,4,94,5,95,6,
     8                96,1,97,2,98,3,99,4/
C
C*      PROCESSES ONLY THE 20TH (IC = 5) AND 21TH (IC = 6) CENTURIES
C
        IF ( IYEAR .LT. 1900 .OR. IYEAR .GT. 2099 ) THEN
           WRITE( *, '(A)' ) ' YEAR ',IYEAR,' IS NOT IN THE LIST'
           RETURN
        ENDIF
C
        ICENT = 1
        JYEAR = IYEAR - 1900
        IF ( JYEAR .GT. 99 ) THEN
           ICENT = 0
           JYEAR = JYEAR - 100
        ENDIF
C
        IF ( IMONTH .LT. 1 .OR. IMONTH .GT. 12 ) THEN
           WRITE( *, '(A,I3,A)' ) ' MONTH ',IMONTH,' IS NOT IN THE LIST'
           RETURN
        ENDIF
C
        IF ( IMONTH .EQ. 1 .OR. IMONTH .EQ. 2 ) JYEAR = JYEAR - 1
        IF ( JYEAR .LT. 0 ) THEN
           ICENT = 1
           JYEAR = JYEAR + 100
        ENDIF
C
        IF ( IDAY .LT. 1 .OR. IDAY .GT. 31 ) THEN
           WRITE( *, '(A,I3,A)' ) ' DAY ',IDAY,' IS NOT IN THE LIST'
        END IF
C
        IDAYWK = ICENT + IYR(JYEAR*2 + 2) + MNTH(IMONTH*2) + IDAY
        IWKDAY = MOD(IDAYWK,7)
        IF ( IWKDAY .EQ. 0 ) IWKDAY = 7
C
        RETURN
        END
c***********************************************************************
       FUNCTION DIRECT ( IDIR )
C
C**    CONVERT DIRECTION (IDIR) INTO ONE OF THE
C**         SIXTEEN POINTS OF COMPASS
C
       CHARACTER*17 DIRECT
C
        DIRECT = ' '
C
        IF(IDIR.GE.12.AND.IDIR.LE.33) THEN
           DIRECT = 'NORTH NORTHEAST'
        ELSEIF(IDIR.GE.34.AND.IDIR.LE.56) THEN
           DIRECT = 'NORTHEAST'
        ELSEIF(IDIR.GE.57.AND.IDIR.LE.78) THEN
           DIRECT = 'EAST NORTHEAST'
        ELSEIF(IDIR.GE.79.AND.IDIR.LE.101) THEN
           DIRECT = 'EAST'
        ELSEIF(IDIR.GE.102.AND.IDIR.LE.123) THEN
           DIRECT = 'EAST SOUTHEAST'
        ELSEIF(IDIR.GE.124.AND.IDIR.LE.146) THEN
           DIRECT = 'SOUTHEAST'
        ELSEIF(IDIR.GE.147.AND.IDIR.LE.168) THEN
           DIRECT = 'SOUTH SOUTHEAST'
        ELSEIF(IDIR.GE.169.AND.IDIR.LE.191) THEN
           DIRECT = 'SOUTH'
        ELSEIF(IDIR.GE.192.AND.IDIR.LE.213) THEN
           DIRECT = 'SOUTH SOUTHWEST'
        ELSEIF(IDIR.GE.214.AND.IDIR.LE.236) THEN
           DIRECT = 'SOUTHWEST'
        ELSEIF(IDIR.GE.237.AND.IDIR.LE.258) THEN
           DIRECT = 'WEST SOUTHWEST'
        ELSEIF(IDIR.GE.259.AND.IDIR.LE.281) THEN
           DIRECT = 'WEST'
        ELSEIF(IDIR.GE.282.AND.IDIR.LE.303) THEN
           DIRECT = 'WEST NORTHWEST'
        ELSEIF(IDIR.GE.304.AND.IDIR.LE.326) THEN
           DIRECT = 'NORTHWEST'
        ELSEIF(IDIR.GE.327.AND.IDIR.LE.348) THEN
           DIRECT = 'NORTH NORTHWEST'
        ELSEIF(IDIR.GE.349.OR.IDIR.LE.011) THEN
           DIRECT = 'NORTH'
       END IF
C
       RETURN
       END
C*********************************************************************
      SUBROUTINE RDLINE ( tauData, indice, ITYPE, RLINE )
C
C**   DETERMINES THE RADIUS LINE FOR THE MARINE ADVISORY
C
      INCLUDE  'dataformats.inc'
c
      CHARACTER*(*) RLINE
      CHARACTER*12  PREFIX(7)
      CHARACTER*24  RDPART
c
      type (AID_DATA) tauData
C
      DATA PREFIX/'64 KT...    ',
     &            '50 KT...    ',
     &            '34 KT...    ',
     &            '64 KT.......',
     &            '50 KT.......',
     &            '34 KT.......',
     &            '12 FT SEAS..'/
C
      if ( itype .ne. 7 ) then
c
         if ( tauData%atcfRcd(indice)%windcode .eq. 'AAA' ) rdpart =
     &        tauData%atcfRcd(indice)%radii(1)(2:4)//'NE '//
     &        tauData%atcfRcd(indice)%radii(1)(2:4)//'SE '//
     &        tauData%atcfRcd(indice)%radii(1)(2:4)//'SW '//
     &        tauData%atcfRcd(indice)%radii(1)(2:4)//'NW.'
c 
         if ( tauData%atcfRcd(indice)%windcode .eq. 'NEQ' ) rdpart =
     &        tauData%atcfRcd(indice)%radii(1)(2:4)//'NE '//
     &        tauData%atcfRcd(indice)%radii(2)(2:4)//'SE '//
     &        tauData%atcfRcd(indice)%radii(3)(2:4)//'SW '//
     &        tauData%atcfRcd(indice)%radii(4)(2:4)//'NW.'
c
      else
c
         if ( tauData%atcfRcd(indice)%seascode .eq. 'AAA' ) rdpart =
     &        tauData%atcfRcd(indice)%seasrad(1)(1:3)//'NE '//
     &        tauData%atcfRcd(indice)%seasrad(1)(1:3)//'SE '//
     &        tauData%atcfRcd(indice)%seasrad(1)(1:3)//'SW '//
     &        tauData%atcfRcd(indice)%seasrad(1)(1:3)//'NW.'
c 
         if ( tauData%atcfRcd(indice)%seascode .eq. 'NEQ' ) rdpart =
     &        tauData%atcfRcd(indice)%seasrad(1)(1:3)//'NE '//
     &        tauData%atcfRcd(indice)%seasrad(2)(1:3)//'SE '//
     &        tauData%atcfRcd(indice)%seasrad(3)(1:3)//'SW '//
     &        tauData%atcfRcd(indice)%seasrad(4)(1:3)//'NW.'
c
      endif
c 
      RLINE = PREFIX(ITYPE)(1:LASTCH(PREFIX(ITYPE)))//RDPART
C
      RETURN
      END
C********************************************************************
      SUBROUTINE NAMER ( FSTINI, NAME )
C
C**   DETERMINE THE FORECASTER'S NAME AND LETTER FROM HIS INITIALS
C
      CHARACTER*3  FSTINI
      CHARACTER*15 NAME
C
C**   NHC FORECASTERS  00/02/08
C
      IF ( FSTINI .EQ. 'JMG' ) THEN
          NAME = 'GROSS'
c
      ELSEIF ( FSTINI .EQ. 'LAA' ) THEN
          NAME = 'AVILA'
c
      ELSEIF ( FSTINI .EQ. 'MBL' ) THEN
          NAME = 'LAWRENCE'
c
      ELSEIF ( FSTINI .EQ. 'ENR' ) THEN
          NAME = 'RAPPAPORT'
c
      ELSEIF ( FSTINI .EQ. 'RJP' ) THEN
          NAME = 'PASCH'
c
      ELSEIF ( FSTINI .EQ. 'BMM' ) THEN
          NAME = 'MAYFIELD'
c
      ELSEIF ( FSTINI .EQ. 'BRJ' ) THEN
          NAME = 'JARVINEN'
c
      ELSEIF ( FSTINI .EQ. 'JLB' ) THEN
          NAME = 'BEVEN'
c
      ELSEIF ( FSTINI .EQ. 'JLF' ) THEN
          NAME = 'FRANKLIN'
c
      ELSEIF ( FSTINI .EQ. 'SRS' ) THEN
          NAME = 'STEWART'

C
C**   CPHC FORECASTERS  00/02/08
C
      ELSEIF ( FSTINI .EQ. 'RWF' ) THEN
          NAME = 'FARRELL'
c
      ELSEIF ( FSTINI .EQ. 'TAC' ) THEN
          NAME = 'CRAIG'
c
      ELSEIF ( FSTINI .EQ. 'JDP' ) THEN
          NAME = 'POWELL'
c
      ELSEIF ( FSTINI .EQ. 'TAH' ) THEN
          NAME = 'HEFFNER'
c
      ELSEIF ( FSTINI .EQ. 'JDH' ) THEN
          NAME = 'HOAG'
c
      ELSEIF ( FSTINI .EQ. 'RTM' ) THEN
          NAME = 'MATSUDA'
c
      ELSEIF ( FSTINI .EQ. 'HER' ) THEN
          NAME = 'ROSENDAL'
c
      ELSEIF ( FSTINI .EQ. 'RWK' ) THEN
          NAME = 'KELLY'
c
      ELSEIF ( FSTINI .EQ. 'SHH' ) THEN
          NAME = 'HOUSTON'
c
C
C**   HPC FORECASTERS    00/02/08
C
      ELSEIF ( FSTINI .EQ. 'NMC' ) THEN
          NAME = 'HPC FORECASTER'
c
C
C**   MYSTERY FORECASTER
C
      ELSE
          NAME = 'UNKNOWN'
c
      ENDIF
C
      RETURN
      END

