      PROGRAM tc_messages
C
C**   PREFORMATS THE tropical cyclone messages
C
      CHARACTER*2  basin, ADAY
      CHARACTER*3  type, DAY(7), MONTH(12)
      CHARACTER*4  AYEAR
      character*50 msg_path
      CHARACTER*68 LINE(75)
      character*75 file_name
C
      DATA DAY/'SUN','MON','TUE','WED','THU','FRI','SAT'/
      DATA MONTH/'JAN','FEB','MAR','APR','MAY','JUN',
     &           'JUL','AUG','SEP','OCT','NOV','DEC'/
c
c**   Get the command line arguments:  basin and message type
c
      call getarg ( 2, basin )
      call getarg ( 3, type )
c
      n = 0
c 
      if ( type .eq. 'two') then
c
c**   Preformat the Tropical Weather Outlook
C
C**   PREPARE THE HEADER RECORDS
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'ZCZC MIATWOAT ALL'
         if ( basin .eq. 'ep' ) LINE(n) = 'ZCZC MIATWOEP ALL'
         if ( basin .eq. 'cp' ) line(n) = 'ZCZC HNLTWOCP ALL'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'TTAA00 KNHC DDHHMM'
         else
            LINE(n) = 'TTAA00 PHNL DDHHMM'
         endif      
         n = n + 1
         LINE(n) = 'TROPICAL WEATHER OUTLOOK'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         else   
            LINE(n) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
         endif
C
C**   PREPARE THE TIME AND DATE RECORD
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'xx30 xM ExT day mon dy year'
         if ( basin .eq. 'ep' ) LINE(n) = 'xx xM PxT day mon dy year'
         if ( basin .eq. 'cp' ) LINE(n) = 'xx xM HST day mon dy year'
C
cc    CALL GETDAT (IYEAR,IMONTH,IDAY)
cc    WRITE (AYEAR,'(I4)') IYEAR
cc    WRITE (ADAY,'(I2)') IDAY
C
cc    LINE(5) = 'XX30 XM EXT '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
cc    LINE(5) = 'XX XM PXT '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
cc    LINE(5) = 'XX XM HST '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
C
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'FOR THE NORTH ATLANTIC...CARI
     &BBEAN SEA AND THE GULF OF MEXICO...'
         if ( basin .eq. 'ep' ) LINE(n) = 'FOR THE EAST NORTH PACIFIC...
     &EAST OF 140 DEGREES WEST LONGITUDE...'
         if ( basin .eq. 'cp' ) LINE(n) = 'FOR THE CENTRAL NORTH PACIFIC
     & OCEAN BETWEEN 140W AND THE DATELINE...'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '******** C-41 EXAMPLE ********'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'TROPICAL WEATHER OUTLOOK'
         n = n + 1
         LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         n = n + 1
         LINE(n) = '530 AM EDT TUE SEP 11 1983'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'FOR THE NORTH ATLANTIC...CARIBBEAN SEA AND THE GULF
     &OF MEXICO...'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'INFORMATION ON TROPICAL STORM LINDA...LOCATED IN THE
     &'
         n = n + 1
         LINE(n) = 'NORTHWESTERN CARIBBEAN...AND HURRICANE KEITH...ABOUT
     &'
         n = n + 1
         LINE(n) = '400 MILES SOUTH OF NEWFOUNDLAND...IS CONTAINED IN'
         n = n + 1
         LINE(n) = 'ADVISORIES BEING ISSUED BY THE NATIONAL HURRICANE'
         n = n + 1
         LINE(n) = 'CENTER.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'AN AREA OF DISTURBED WEATHER IS LOCATED IN THE'
         n = n + 1
         LINE(n) = 'EASTERN ATLANTIC SEVERAL HUNDRED MILES WEST OF'
         n = n + 1
         LINE(n) = 'AFRICA.  UPPER LEVEL WIND PATTERNS HAVE BECOME MORE'
         n = n + 1
         LINE(n) = 'FAVORABLE FOR THIS SYSTEM TO BECOME BETTER ORGANIZED
     &'
         n = n + 1
         LINE(n) = 'DURING THE NEXT SEVERAL DAYS.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'A WELL ORGANIZED CLOUD SYSTEM EAST OF THE BAHAMAS IS
     &'
         n = n + 1
         LINE(n) = 'ASSOCIATED WITH AN UPPER LEVEL LOW PRESSURE AREA.'
         n = n + 1
         LINE(n) = 'TEMPERATURES IN THE UPPER ATMOSPHERE REMAIN COLD AND
     &'
         n = n + 1
         LINE(n) = 'THEREFORE DEVELOPMENT IF ANY WILL BE SLOW TO OCCUR.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'ELSEWHERE OVER THE TROPICS CONDITIONS DO NOT FAVOR'
         n = n + 1
         LINE(n) = 'TROPICAL STORM DEVELOPMENT TODAY OR WEDNESDAY.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'GROSS'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '************END OF EXAMPLE ****************'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = '*** USE THE CORRECT EASTERN T
     &IME, TIME ZONE, DAY OF'
         if ( basin .eq. 'ep' ) LINE(n) = '*** USE THE CORRECT PACIFIC T
     &IME, TIME ZONE, DAY OF'
         if ( basin .eq. 'cp' ) LINE(n) = '*** USE THE CORRECT HONOLULU
     & TIME, TIME ZONE, DAY OF'
         n = n + 1
         LINE(n) = 'WEEK AND DATE IN THE HEADER AND SIGN YOUR NAME ***'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'YOUR NAME'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'NNNN'
c
      elseif ( type .eq. 'tce' ) then
c
c**   Preformat the Tropical Cyclone Position Estimate
C
C**   PREPARE THE HEADER RECORDS
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'ZCZC MIATCEAT ALL'
         if ( basin .eq. 'ep' ) LINE(n) = 'ZCZC MIATCEEP ALL'
         if ( basin .eq. 'cp' ) LINE(n) = 'ZCZC MIATCECP ALL'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'TTAA00 KNHC DDHHMM'
         else
            LINE(n) = 'TTAA00 PHNL DDHHMM'
         endif   
         n = n + 1
         LINE(n) = '(system type and number or name) POSITION ESTIMATE'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         else   
            LINE(n) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
         endif   
C
C**   PREPARE THE TIME AND DATE RECORD
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'xxxx xM xxT day mon dy year'
         if ( basin .eq. 'ep' ) LINE(n) = 'xxxx xM PxT day mon dy year'
         if ( basin .eq. 'cp' ) LINE(n) = 'xxxx xM HST day mon dy year'
C
cc    CALL GETDAT (IYEAR,IMONTH,IDAY)
cc    WRITE (AYEAR,'(I4)') IYEAR
cc    WRITE (ADAY,'(I2)') IDAY
C
cc    LINE(5) = 'XXXX XM XXT '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
C
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '******** C-41 EXAMPLE ********'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'HURRICANE GLORIA...POSITION ESTIMATE'
         n = n + 1
         LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         n = n + 1
         LINE(n) = '1100 AM EDT FRI SEP 27 1985'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'AT 11 AM EDT THE CENTER OF HURRICANE GLORIA WAS'
         n = n + 1
         LINE(n) = 'ESTIMATED NEAR LATITUDE 40.6 NORTH...LONGITUDE'
         n = n + 1
         LINE(n) = '73.2 WEST OR ABOUT 25 MILES SOUTH OF FIRE ISLAND'
         n = n + 1
         LINE(n) = 'NEW YORK.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'GERRISH'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '************* END OF EXAMPLE *************'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = '*** USE THE CORRECT CYCLONE T
     &YPE, NAME, TIME'
         if ( basin .eq. 'ep' ) LINE(n) = '*** USE THE CORRECT CYCLONE T
     &YPE, NAME, PACIFIC,'
         if ( basin .eq. 'cp' ) LINE(n) = '*** USE THE CORRECT CYCLONE T
     &YPE, NAME, HONOLULU'
         n = n + 1
         LINE(n) = 'TIME ZONE, DAY OF WEEK AND DATE IN THE HEADER AND'
         n = n + 1
         LINE(n) = 'SIGN YOUR NAME *** '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'YOUR NAME'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'NNNN'
C
      elseif ( type .eq. 'tcu' ) then
c
c**   Preformat the Tropical Cyclone Update
C
C**   PREPARE THE HEADER RECORDS
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'ZCZC MIATCUAT ALL'
         if ( basin .eq. 'ep' ) LINE(n) = 'ZCZC MIATCUEP ALL'
         if ( basin .eq. 'cp' ) LINE(n) = 'ZCZC MIATCUCP ALL'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'TTAA00 KNHC DDHHMM'
         else   
            LINE(n) = 'TTAA00 PHNL DDHHMM'
         endif   
         n = n + 1
         LINE(n) = 'BULLETIN'
         n = n + 1
         LINE(n) ='(system type and number or name) TROPICAL CYCLONE UPD
     &ATE'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         else
            LINE(n) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
         endif
C
C**   PREPARE THE TIME AND DATE RECORD
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'xxxx xM xxT day mon dy year'
         if ( basin .eq. 'ep' ) LINE(n) = 'xxxx xM PxT day mon dy year'
         if ( basin .eq. 'cp' ) LINE(n) = 'xxxx xM HST day mon dy year'
C
cc    CALL GETDAT (IYEAR,IMONTH,IDAY)
cc    WRITE (AYEAR,'(I4)') IYEAR
cc    WRITE (ADAY,'(I2)') IDAY
C
cc    LINE(6) = 'XXXX XM XXT '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
C
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '********  TCU C-41 EXAMPLE ********'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'HURRICANE ALICIA TROPICAL CYCLONE UPDATE'
         n = n + 1
         LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         n = n + 1
         LINE(n) = '600 PM CDT TUE AUG 16 1983'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '...RECONNAISSANCE AIRCRAFT INDICATE IN TROPICAL STOR
     &M'
         n = n + 1
         LINE(n) = 'ALICIA HAS REACHED HURRICANE STRENGTH...'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'SHORTLY BEFORE 6 PM CDT...RECONNAISSANCE AIRCRAFT'
         n = n + 1
         LINE(n) = 'INDICATED THAT MAXIMUM SUSTAINED WINDS IN TROPICAL'
         n = n + 1
         LINE(n) = 'STORM ALICIA HAD INCREASED TO HURRICANE FORCE.'
         n = n + 1
         LINE(n) = 'DETAILS WILL FOLLOW IN A SPECIAL HURRICANE ADVISORY'
         n = n + 1
         LINE(n) = 'AT 7 PM CDT.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'SHEETS'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '************* END OF EXAMPLE *************'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = '*** USE THE CORRECT CYCLONE T
     &YPE, NAME, TIME, TIME'
         if ( basin .eq. 'ep' ) LINE(n) = '*** USE THE CORRECT CYCLONE T
     &YPE, NAME, PACIFIC'
         if ( basin .eq. 'cp' ) LINE(n) = '*** USE THE CORRECT CYCLONE T
     &YPE, NAME, HONOLULU'
         n = n + 1
         LINE(n) = 'ZONE, DAY OF WEEK AND DATE IN THE HEADER AND'
         n = n + 1
         LINE(n) = 'SIGN YOUR NAME *** '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'YOUR NAME'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'NNNN'
c
      elseif ( type .eq. 'dsa' ) then
c
c**   Preformat the Tropical Disturbance Statement
C
C**   PREPARE THE HEADER RECORDS
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'ZCZC MIADSAAT ALL'
         if ( basin .eq. 'ep' ) LINE(n) = 'ZCZC MIADSAEP ALL'
         if ( basin .eq. 'cp' ) LINE(n) = 'ZCZC MIADSACP ALL'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'TTAA00 KNHC DDHHMM'
         else
            LINE(n) = 'TTAA00 PHNL DDHHMM'
         endif
         n = n + 1
         LINE(n) = 'SPECIAL TROPICAL DISTURBANCE STATEMENT'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         else
            LINE(n) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
         endif   
C
C**   PREPARE THE TIME AND DATE RECORD
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'xxxx xM xxT day mon dy year'
         if ( basin .eq. 'ep' ) LINE(n) = 'xxxx xM PxT day mon dy year'
         if ( basin .eq. 'cp' ) LINE(n) = 'xxxx xM HST day mon dy year'
c
cc    CALL GETDAT (IYEAR,IMONTH,IDAY)
cc    WRITE (AYEAR,'(I4)') IYEAR
cc    WRITE (ADAY,'(I2)') IDAY
C
cc    LINE(5) = 'XXXX XM XXT '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
C
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '******** DSA C-41 INFORMATION ********'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'SPECIAL TROPICAL DISTURBANCE STATEMENTS ARE ISSUED T
     &O'
         n = n + 1
         LINE(n) = 'FURNISH INFORMATION ON STRONG FORMATIVE,'
         n = n + 1
         LINE(n) = 'NONDEPRESSION SYSTEMS.  THESE STATEMENTS SHOULD FOCU
     &S'
         n = n + 1
         LINE(n) = 'ON THE MAJOR THREATS OF THE DISTURBANCE, SUCH AS THE
     &'
         n = n + 1
         LINE(n) = 'POTENTIAL FOR TORRENTIAL RAINS ON ISLAND OR INLAND'
         n = n + 1
         LINE(n) = 'AREAS, AND SHOULD BE COORDINATED WITH THE'
         n = n + 1
         LINE(n) = 'APPROPIATE WSFO.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '******** END OF INFORMATION ********'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = '*** USE THE CORRECT TIME, TIM
     &E ZONE, DAY OF WEEK'
         if ( basin .eq. 'ep' ) LINE(n) = '*** USE THE CORRECT PACIFIC T
     &IME, TIME ZONE, DAY OF'
         if ( basin .eq. 'cp' ) LINE(n) = '*** USE THE CORRECT HONOLULU 
     &TIME, DAY OF WEEK'
         n = n + 1
         LINE(n) = 'AND DATE IN THE HEADER AND SIGN YOUR NAME *** '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'YOUR NAME'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'NNNN'
c
      elseif ( type .eq. 'tws' ) then      
c
c**   Preformat the Tropical Weather Summary
C
C**   PREPARE THE HEADER RECORDS
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'ZCZC MIATWSAT ALL'
         if ( basin .eq. 'ep' ) LINE(n) = 'ZCZC MIATWSEP ALL'
         if ( basin .eq. 'cp' ) LINE(n) = 'ZCZC MIATWSCP ALL'
         n = n + 1

         if ( basin .ne. 'cp' ) then
            LINE(n) = 'TTAA00 KNHC DDHHMM'
         else
            LINE(n) = 'TTAA00 PHNL DDHHMM'
         endif
         n = n + 1
         LINE(n) = 'MONTHLY TROPICAL WEATHER SUMMARY'
         n = n + 1
         if ( basin .ne. 'cp' ) then
            LINE(n) = 'NATIONAL WEATHER SERVICE MIAMI FL'
         else
            LINE(n) = 'NATIONAL WEATHER SERVICE HONOLULU HI'
         endif
C
C**   PREPARE THE TIME AND DATE RECORD
C
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'xx AM ExT day mon dy year'
         if ( basin .eq. 'ep' ) LINE(n) = 'xx AM PxT day mon dy year'
         if ( basin .eq. 'cp' ) LINE(n) = 'xx AM HST day mon dy year'
C
cc    CALL GETDAT (IYEAR,IMONTH,IDAY)
cc    WRITE (AYEAR,'(I4)') IYEAR
cc    WRITE (ADAY,'(I2)') IDAY
C
cc    LINE(5) = 'XX AM EXT '//DAY(IWKDAY(IYEAR,IMONTH,IDAY))//' '//
cc   & MONTH(IMONTH)//' '//ADAY//' '//AYEAR
C
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = 'FOR THE NORTH ATLANTIC...CARI
     &BBEAN SEA AND THE GULF OF MEXICO...'
         if ( basin .eq. 'ep' ) LINE(n) = 'FOR THE EAST NORTH PACIFIC...
     &EAST OF 140 DEGREES WEST LONGITUDE...'
         if ( basin .eq. 'cp' ) LINE(n) = 'FOR THE CENTRAL NORTH PACIFIC
     & OCEAN BETWEEN 140W AND THE DATELINE...'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '******** TWS C-41 INFORMATION ********'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'THIS PRODUCT IS PREPARED AFTER EACH MONTH TO'
         n = n + 1
         LINE(n) = 'SUMMARIZE THE PREVIOUS MONTHS TROPICAL CYCLONE'
         n = n + 1
         LINE(n) = 'ACTIVITY OR LACK OF ACTIVITY AND THE REASON(S) WHY.'
         n = n + 1
         LINE(n) = 'THE LAST TWS OF THE SEASON WILL SUMMARIZE THE'
         n = n + 1
         LINE(n) = 'ACTIVITY FOR NOVEMBER PLUS THE ACTIVITY FOR THE'
         n = n + 1
         LINE(n) = 'SEASON AS A WHOLE.'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = '*************** END OF INFORMATION ****************'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         if ( basin .eq. 'at' ) LINE(n) = '*** USE THE CORRECT EASTERN T
     &IME, TIME ZONE, DAY OF'
         if ( basin .eq. 'ep' ) LINE(n) = '*** USE THE CORRECT PACIFIC T
     &IME, TIME ZONE, DAY OF'
         if ( basin .eq. 'cp' ) LINE(n) = '*** USE THE CORRECT HONOLULU 
     &TIME, DAY OF WEEK AND'
         n = n + 1
         LINE(n) = 'WEEK AND DATE IN THE HEADER AND SIGN YOUR NAME *** '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'YOUR NAME'
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = ' '
         n = n + 1
         LINE(n) = 'NNNN'
c
      endif
c
c**   Get the environmental variable for the message directory and
c**     create the message file name.
c
      call getenv ( "NHCMESSAGES", msg_path )
      file_name = msg_path(1:lastch( msg_path ))//"/"//type//basin//
     & ".msg"
cc      file_name = type//basin//".msg"
C
C**   OPEN, WRITE, AND CLOSE THE TWOAT FILE
C
      OPEN ( 21, FILE=file_name, STATUS='UNKNOWN', IOSTAT=IOS, ERR=1010)
C
      DO I = 1, n
C
      LNEND = LASTCH( LINE(I) )
      IF ( LNEND .EQ. 0 ) LNEND = 1
C
      WRITE ( 21, '(A)' ) LINE(I)(1:LNEND)
C
      enddo
C
      CLOSE (21)
C
      STOP
C
 1010 PRINT *, ' ERROR OPENING FILE, ', file_name, ', IOS = ', IOS
      STOP
C
      END
C**********************************************************************
        FUNCTION LASTCH (STRING)
C
C**     RETURNS THE POSITION OF THE LAST NON-BLANK CHARACTER OF A
C**             STRING
C
        CHARACTER*(*) STRING
C
        LAST = LEN(STRING)
C
        DO 10 I = LAST,1,-1
        IF (STRING(I:LAST).NE.' ') GO TO 20
   10   CONTINUE
C
        LASTCH = 0
        RETURN
C
   20   LASTCH = I
        RETURN
C
        END
