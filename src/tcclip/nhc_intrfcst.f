      program intrfcst
c
c**   This program interpolates and extrapolates the official and model
c**      in time and space
c
c**   Remove the "cloop" comments to allow the program to interpolate
c**     an entire adeck
c
c**   Remove the "clocal" comments to allow the program to work in 
c**      local directory
c
      include 'dataformats.inc'
c
      parameter ( nmodel=16, ntau=11 )
c
      common /initial/ latcur, loncur, spdcur
      common /intrp/   intlat(ntau,nmodel), intlon(ntau,nmodel),
     &     intspd(ntau,nmodel)
c
      real intlat, intlon, intspd
      real offset_lat, offset_lon, offset_spd
      real latcur, loncur, spdcur
      real latm06, lonm06, spdm06
      real latm12, lonm12, spdm12
c
      real intrlat(41), intrlon(41), intrspd(41)
c
      real fst06lat(ntau,nmodel), fst06lon(ntau,nmodel), 
     &     fst06spd(ntau,nmodel), fst06tau(ntau,nmodel)
      real fst12lat(ntau,nmodel), fst12lon(ntau,nmodel), 
     &     fst12spd(ntau,nmodel), fst12tau(ntau,nmodel)
      integer tau(ntau), last_tau06(nmodel), last_tau12(nmodel)
      integer result
c
      character*4   fst_tech(nmodel), new_tech(nmodel)
      character*8   strmid
      character*10  ymdh(150), dtgcur, dtgm06, dtgm12
      character*100 stm_path, output_file
      character*150 bstrk_name, aids_name, adeck_name
c
      type ( BIG_AID_DATA ) aidsData
      type ( AID_DATA )     aidData, tauData
c
      data tau / 0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120 /
c
      data fst_tech /'OFCL','AVNO','GFDL','VBAR','NGPS',' UKM',
     &               ' UKX',' EMX',' NGX',' ETA',' NGM','GFDN',
     &               'GFD2','MM36','GFDU','GFDC'/
c
      data new_tech /'OFCI','AVNI','GFDI','VBRI','NGPI','UKMI',
     &               'UKXI','EMXI','NGXI','ETAI','NGMI','GFNI',
     &               'GF2I','M36I','GFUI','GFCI'/
c
C**   DEFINE INTERNAL FUNCTION for extrapolation
C
      FI(T,A,B,C) = (2.0*A + T*(4.0*B - C - 3.0*A +
     & T*(C - 2.0*B + A)))/2.0
c
c**   Get the strmid from the command line
c
      strmid = '        '
      call getarg ( 2, strmid )
      
      if (strmid .ne. '        ' ) then
	 print *, ' nhc_intrfcst: Storm ID = ', strmid
      else
	 print *, ' USAGE: nhc_intrfcst wp012000 adeck.txt'
	 stop
      endif
c
c**   Get the output file name from the command line
c
      output_file = ' '
      call getarg ( 3, output_file )
      
      if (output_file .ne. ' ' ) then
	 print *, ' nhc_intrfcst: output file = ', output_file
      else
	 print *, ' USAGE: nhc_intrfcst wp012000 adeck.txt'
	 stop
      endif
c
c**   Create the best track and adeck file names and open the files
c
cc      call getenv ( "ATCFSTRMS", stm_path )
cc      ind = index( stm_path, " " ) - 1
c
cc      bstrk_name = stm_path( 1:ind)//"/b"//strmid//".dat"
cc      aids_name  = stm_path( 1:ind)//"/a"//strmid//".dat"
cc      adeck_name = stm_path( 1:ind)//"/"//output_file
c
      bstrk_name = "b"//strmid//".dat"         !clocal
      aids_name  = "a"//strmid//".dat"         !clocal
      adeck_name = output_file                 !clocal
c
cc      print *, ' Best track file = ', bstrk_name
cc      print *, ' Aids file       = ', aids_name
cc      print *, ' Adeck file      = ', adeck_name
c
      open ( 21, file=bstrk_name, status='old', iostat=ios, err=1010 )
      open ( 22, file=aids_name,  status='old', iostat=ios, err=1020 )
c
c**   Open an output adeck
c
      open ( 31, file=adeck_name, status='unknown',
     &       iostat=ios, err=1030 )
c
C**   Read the best track file and store the date/time group in an array
C
      isave = 1
   10 read ( 21, '( 8x, a10 )', end=20 ) ymdh(isave)
      isave = isave + 1
      go to 10
c
   20 close ( 21 )
      last = isave - 1
c
cc      do 200 loop = 1, last                       !cloop
c
         latcur = 0.0
         loncur = 0.0
         spdcur = 0.0
         latm06 = 0.0
         lonm06 = 0.0
         spdm06 = 0.0
         latm12 = 0.0
         lonm12 = 0.0
         spdm12 = 0.0
c      
         call zero ( fst06lat )
         call zero ( fst06lon )
         call zero ( fst06spd )
         call zero ( fst06tau )
         call zero ( fst12lat )
         call zero ( fst12lon )
         call zero ( fst12spd )
         call zero ( fst12tau )
         call zero ( intlat )
         call zero ( intlon )
         call zero ( intspd )
c
c**   Find the current, past 6-hour and past 12-hour forecast times
c
         dtgcur = ymdh(last)
cc         dtgcur = ymdh(loop)                   !cloop
c
         call dtgmod ( dtgcur,  -6, dtgm06 , result )
         call dtgmod ( dtgcur, -12, dtgm12 , result )
c
cc         rewind ( 22 )                         !cloop 
c
c**   Get the minus 12-hour initial data from the CARQ
c
         call getBigAidDTG ( 22, dtgm12, aidsData, result )
         if ( result .eq. 0 ) goto 50
c
         call getTech ( aidsData, "CARQ", aidData, result )
         if ( result .eq. 0) goto 50
c
         call getSingleTAU ( aidData, 0, tauData, result )
         if ( result .eq. 0 ) goto 50
c
         latm12 = alat180(tauData%aRecord(1)%lat, tauData%aRecord(1)%NS)
         lonm12 = alon360(tauData%aRecord(1)%lon, tauData%aRecord(1)%EW)
         spdm12 = tauData%aRecord(1)%vmax
c
c**   Get the forecast data for desired techinques for all TAUs
c
         do 40 i = 1, nmodel
c
            last_tau12(i) = 0
c
            call getTech ( aidsData, fst_tech(i), aidData, result )
            if ( result .eq. 0 ) goto 40
c
            do 30 j = 1, ntau
c
               call getSingleTAU ( aidData, tau(j), tauData, result )
               if ( result .eq. 0 ) then
c
c**   If there is no initial 0 TAU for the technique, use the CARQ data
c
                  if ( tau(j) .eq. 0 ) then
                     last_tau12(i) = last_tau12(i) + 1
                     fst12lat( last_tau12(i), i ) = latm12
                     fst12lon( last_tau12(i), i ) = lonm12
                     fst12spd( last_tau12(i), i ) = spdm12
                     fst12tau( last_tau12(i), i ) = float( tau(j) )
                     go to 30
                  else
                     go to 30
                  endif
c   
               endif      
c
               last_tau12(i) = last_tau12(i) + 1
               fst12lat( last_tau12(i), i ) = 
     &	         alat180( tauData%aRecord(1)%lat, tauData%aRecord(1)%NS)
               fst12lon( last_tau12(i), i ) = 
     &	         alon360( tauData%aRecord(1)%lon, tauData%aRecord(1)%EW)
               fst12spd( last_tau12(i), i ) = tauData%aRecord(1)%vmax
               fst12tau( last_tau12(i), i ) = float( tau(j) )
c
 30         continue
 40      continue
c
 50      continue 
c
c**   Get the minus 6-hour initial data from the CARQ
c
         call getBigAidDTG ( 22, dtgm06, aidsData, result )
         if ( result .eq. 0 ) goto 80
c
         call getTech ( aidsData, "CARQ", aidData, result )
         if ( result .eq. 0 ) goto 80
c
         call getSingleTAU ( aidData, 0, tauData, result )
         if ( result .eq. 0 ) goto 80
c
         latm06 = alat180(tauData%aRecord(1)%lat, tauData%aRecord(1)%NS)
         lonm06 = alon360(tauData%aRecord(1)%lon, tauData%aRecord(1)%EW)
         spdm06 = tauData%aRecord(1)%vmax
c
c**   Get the forecast data for desired techinques all TAUs
c
         do 70 i = 1, nmodel
c
            last_tau06(i) = 0
c
            call getTech ( aidsData, fst_tech(i), aidData, result )
            if ( result .eq. 0 ) goto 70
c
            do 60 j = 1, ntau
               call getSingleTAU ( aidData, tau(j), tauData, result )
               if ( result .eq. 0 ) then
c
c**   If there is no initial 0 TAU for the technique, use the CARQ data
c
                  if ( tau(j) .eq. 0 ) then
                     last_tau06(i) = last_tau06(i) + 1
                     fst06lat( last_tau06(i), i ) = latm06
                     fst06lon( last_tau06(i), i ) = lonm06
                     fst06spd( last_tau06(i), i ) = spdm06
                     fst06tau( last_tau06(i), i ) = float( tau(j) )
                     go to 60
                  else
                     go to 60
                  endif   
               endif      
c
               last_tau06(i) = last_tau06(i) + 1
               fst06lat( last_tau06(i), i ) = 
     &	         alat180( tauData%aRecord(1)%lat, tauData%aRecord(1)%NS)
               fst06lon( last_tau06(i), i ) = 
     &	         alon360( tauData%aRecord(1)%lon, tauData%aRecord(1)%EW)
               fst06spd( last_tau06(i), i ) = tauData%aRecord(1)%vmax
               fst06tau( last_tau06(i), i ) = float( tau(j) )
c
 60         continue
 70      continue
c
 80      continue
c
c**   Get the current initial data from the CARQs
c
         call getBigAidDTG ( 22, dtgcur, aidsData, result )
         if ( result .eq. 0 ) then
            print *, ' No initial objective aid data for: ', dtgcur
	    goto 200
         endif
c
         call getTech ( aidsData, "CARQ", aidData, result )
         if ( result .eq. 0 ) then
            print *, ' No CARQ in initial objective aid data: ', dtgcur
	    goto 200
         endif
c
         call getSingleTAU ( aidData, 0, tauData, result )
         if ( result .eq. 0 ) then 
            print *, ' No initial position from CARQ for: ', dtgcur
	    goto 200
         endif
c
         latcur = alat180(tauData%aRecord(1)%lat, tauData%aRecord(1)%NS)
         loncur = alon360(tauData%aRecord(1)%lon, tauData%aRecord(1)%EW)
         spdcur = tauData%aRecord(1)%vmax
c
c**   Write out the input for interpolation
c
         nowrite = 1
         if ( nowrite .eq. 1 ) goto 90
         write (*,'('' '')')
         write (*,'(9f6.1)') latm12, lonm12, spdm12, latm06, lonm06, 
     &                       spdm06, latcur, loncur, spdcur
         write (*,'('' '')')
         do i = 1, nmodel
            write (*,'(a4,2i10,5x,a10)') fst_tech(i), last_tau12(i), 
     &           last_tau06(i), dtgcur
            write (*,'('' '')')
            write (*,'(a10)') dtgm12
            write (*,'(7f6.1)') (fst12lat(j,i), j = 1, 7)
            write (*,'(7f6.1)') (fst12lon(j,i), j = 1, 7)
            write (*,'(7f6.1)') (fst12spd(j,i), j = 1, 7)
            write (*,'(7f6.1)') (fst12tau(j,i), j = 1, 7)
            write (*,'('' '')')
            write (*,'(a10)') dtgm06
            write (*,'(7f6.1)') (fst06lat(j,i), j = 1, 7)
            write (*,'(7f6.1)') (fst06lon(j,i), j = 1, 7)
            write (*,'(7f6.1)') (fst06spd(j,i), j = 1, 7)
            write (*,'(7f6.1)') (fst06tau(j,i), j = 1, 7)
            write (*,'('' '')')
         enddo
 90      continue
c
c**   Interpolate the non-blank forecasts
c
         iflag = 1
         lflag = 1
c
c**   Do the 12-hour interpolation, first
c
         do i = 1, nmodel
c
            if ( last_tau12(i) .gt. 3 ) then
c
               last_tau = int( fst12tau( last_tau12(i), i ) )
               j = 0
c
               do k = 0, last_tau, 3
c
                  j = j + 1
c
                  call mspline ( fst12tau( 1, i ), fst12lat( 1, i ), 
     &                 last_tau12(i), iflag, lflag, float(k), 
     &                 intrlat(j), ierror )
                  if ( ierror .ne. 0 ) print *, 'ERROR..lat12..',
     &                 dtgcur, fst_tech(i), k
c
                  call mspline ( fst12tau( 1, i ), fst12lon( 1, i ), 
     &                 last_tau12(i), iflag, lflag, float(k), 
     &                 intrlon(j), ierror )
                  if ( ierror .ne. 0 ) print *, 'ERROR..lon12..',
     &                 dtgcur, fst_tech(i), k
c
                  call mspline ( fst12tau( 1, i ), fst12spd( 1, i ), 
     &                 last_tau12(i), iflag, lflag, float(k), 
     &                 intrspd(j), ierror )
                  if ( ierror .ne. 0 ) print *, 'ERROR..spd12..',
     &                 dtgcur, fst_tech(i), k
c
               enddo
c
               jlast = j
c
c**   Filter interpolated points
c
               ntimes = 10
c
               call filter ( ntimes, jlast, intrlat )
               call filter ( ntimes, jlast, intrlon )
               call filter ( ntimes, jlast, intrspd )
c
c**   Offset the filtered interpolated forecast for the current 
c*       initial values
c
               l = 0
c
               do k = 5, jlast, 4
c
                  if ( k .eq. 5 ) then
                     offset_lat = latcur - intrlat(k)
                     offset_lon = loncur - intrlon(k)
                     offset_spd = spdcur - intrspd(k)
                  endif
c
                  l = l + 1
c
                  intlat ( l, i ) = offset_lat + intrlat(k)
                  intlon ( l, i ) = offset_lon + intrlon(k)
                  intspd ( l, i ) = offset_spd + intrspd(k)
c
               enddo    
c
c**   Extrapolate the offset interpolated forecast 12 hours
c
               intlat( l + 1, i) = fi( 3.0, intlat( l - 2, i ),
     &              intlat( l - 1, i ), intlat( l, i ) )
               intlon( l + 1, i) = fi( 3.0, intlon( l - 2, i ),
     &              intlon( l - 1, i ), intlon( l, i ) )
               intspd( l + 1, i) = fi( 3.0, intspd( l - 2, i ),
     &              intspd( l - 1, i ), intspd( l, i ) )
c
c**   Check 12-hour original 12-hour and 24-hour intensity forecasts.  
c**      If zero, except for the initial point, the interpolated 
c**      intensities are bad.  Zero them out.
c
               if ( fst12spd( 2, i ) .lt. 0.01 .and. 
     &              fst12spd( 3, i ) .lt. 0.01 ) then
                  do m = 2, ntau
                     intspd( m, i ) = 0.0
                  enddo
               endif
c
c**   Write out the 12-hour interpolated forecast
c
cc               write ( *, '(''This is a 12-hour interpolation.'')')
cc               call write_out ( strmid, dtgcur, new_tech(i), 
cc     &           intlat(1,i), intlon(1,i), intspd(1,i) )
c
            endif
         enddo
c
c**   Do the 6-hour interpolation, second
c
         do i = 1, nmodel
c
            if ( last_tau06(i) .gt. 3 ) then
c
c**   There maybe a 12-hour interpolation for this technique, so zero it
c
               do kk = 1, ntau
                  intlat( kk, i ) = 0.0
                  intlon( kk, i ) = 0.0
                  intspd( kk, i ) = 0.0
               enddo   
c
               last_tau = int( fst06tau( last_tau06(i), i ) )
               j = 0
c
               do k = 0, last_tau, 3
c
                  j = j + 1
c
                  call mspline ( fst06tau( 1, i ), fst06lat( 1, i ), 
     &                 last_tau06(i), iflag, lflag, float(k), 
     &                 intrlat(j), ierror )
                  if ( ierror .ne. 0 ) print *, 'ERROR..lat06..',
     &                 dtgcur, fst_tech(i), k
c
                  call mspline ( fst06tau( 1, i ), fst06lon( 1, i ), 
     &                 last_tau06(i), iflag, lflag, float(k), 
     &                 intrlon(j), ierror )
                  if ( ierror .ne. 0 ) print *, 'ERROR..lon06..',
     &                 dtgcur, fst_tech(i), k
c
                  call mspline ( fst06tau( 1, i ), fst06spd( 1, i ), 
     &                 last_tau06(i), iflag, lflag, float(k), 
     &                 intrspd(j), ierror )
                  if ( ierror .ne. 0 ) print *, 'ERROR..spd06..',
     &                 dtgcur, fst_tech(i), k
c
               enddo
c
               jlast = j
c
c**   Filter interpolated points
c
               call filter ( ntimes, jlast, intrlat )
               call filter ( ntimes, jlast, intrlon )
               call filter ( ntimes, jlast, intrspd )
c
c**   Offset the filtered interpolated forecast for the current 
c**      initial values
c
               l = 0
c
               do k = 3, jlast, 4

                  if ( k .eq. 3 ) then
                     offset_lat = latcur - intrlat(k)
                     offset_lon = loncur - intrlon(k)
                     offset_spd = spdcur - intrspd(k)
                  endif
c
                  l = l + 1
c
                  intlat ( l, i ) = offset_lat + intrlat(k)
                  intlon ( l, i ) = offset_lon + intrlon(k)
                  intspd ( l, i ) = offset_spd + intrspd(k)
c
               enddo    
c
c**   Extrapolate the offset interpolated forecast 6 hours
c
               intlat( l + 1, i) = fi( 3.0, intlat( l - 2, i ),
     &              intlat( l - 1, i ), intlat( l, i ) )
               intlon( l + 1, i) = fi( 3.0, intlon( l - 2, i ),
     &              intlon( l - 1, i ), intlon( l, i ) )
               intspd( l + 1, i) = fi( 3.0, intspd( l - 2, i ),
     &              intspd( l - 1, i ), intspd( l, i ) )
c
c**   Check 6-hour original 12-hour and 24-hour intensity forecasts.  
c**      If zero, except for the initial point, the interpolated 
c**      intensities are bad.  Zero them out.
c
               if ( fst06spd( 2, i ) .lt. 0.01 .and. 
     &              fst06spd( 3, i ) .lt. 0.01 ) then
                  do m = 2, ntau
                     intspd( m, i ) = 0.0
                  enddo
               endif
c
c**   Write out the 6-hour interpolated forecast
c
cc               write ( *, '(''This is a 6-hour interpolation.'')')
cc               call write_out ( strmid, dtgcur, new_tech(i), 
cc     &              intlat(1,i), intlon(1,i), intspd(1,i) )
c
            endif
c
cc            write ( *, '(''This is a 12- or 6-hour interpolation.'')')
            call write_out ( strmid, dtgcur, new_tech(i), 
     &              intlat(1,i), intlon(1,i), intspd(1,i) )
c
         enddo
c
c**   Compute and write out the GUNS forecast
c
         call guns ( strmid, dtgcur, 'GUNS' )
c
c**   Compute and write out the GUNA forecast
c
         call guna ( strmid, dtgcur, 'GUNA' )
c
  200 continue
c
      close ( 22 )
      close ( 31 )
c
      stop ' Interpolation of forecasts are finished'
c
c**   Error messages
c
 1010 print *, ' Error opening b-deck of current storm - ios = ',ios
      print *, ' Filename:', bstrk_name
      stop
c
 1020 print *, ' Error opening a-deck of current storm - ios = ',ios
      print *, ' Filename:', aids_name
      stop
c
 1030 print *, ' Error opening temporary adeck for output - ios = ',ios
      print *, ' Filename:', guns_name
      stop
c
      end
c******************************************************************
      subroutine zero ( array )
c
c**   Zeros out a two dimensional array
c
cc      parameter ( nmodel=1, ntau=11 )
      parameter ( nmodel=6, ntau=11 )
c
      real array( ntau, nmodel )
c
      do  j = 1, nmodel
         do  i = 1, ntau
c
            array( i, j ) = 0.0
         end do
      end do
c
      return
      end
c
c********1*********2*********3*********4*********5*********6*********7**
      function alat180 ( alat90, ns )
c
c**   Transforms given latitude from 0 to 90 degrees to -90 to 90 degrees
c
      real alat90
c 
      character*1 ns
c
      alat180 = alat90
c 
      if ( ns .eq. "S" ) alat180 = - alat90
c
      return
      end
c
c********1*********2*********3*********4*********5*********6*********7**
      function alon360 ( alon180, ew )
c
c**   Transforms given longitude from 0 to 180 degrees to 0 to 360 degrees
c**       ( East > 180 )
c
      real alon180
c
      character*1 ew
c
      alon360 = alon180
c
      if ( ew .eq. "E" ) alon360 = 360.0 - alon180
c
      return
      end
c
c********1*********2*********3*********4*********5*********6*********7**
      subroutine filter ( ntimes, last, array )
c
c**   Use a three-point center weighted filter on an array, any 
c**      number of times
c
      dimension array(100), filter_array(100)
c
c**   Fix the end points
c
      filter_array(1) = array(1)
      filter_array(last) = array(last)
c
c**   Filter the array the number if times specified
c
      do ntime = 1, ntimes
c
c**   Do the filtering
c
         do n = 2, last - 1
            filter_array(n) = 0.25*array(n - 1) + 0.5*array(n) +
     &                        0.25*array(n + 1)
         enddo
c
c**   Replace the original array with the filtered array
c
         do n = 2, last - 1
            array(n)= filter_array(n)
         enddo
c   
      enddo
c
      return
      end
c
c********1*********2*********3*********4*********5*********6*********7**
      subroutine write_out ( strmid, dtgcur, new_tech, 
     &     intlat, intlon, intspd )
c
c**   Put the new objective aid in a writeable format
c
      parameter ( ntau=11 )
c
      real     intlat(ntau), intlon(ntau), intspd(ntau)
      integer  newfst(ntau,3)
c
      character*2  tech
      character*4  new_tech
      character*8  strmid
      character*10 dtgcur
      character*76 chfcst
c
c**   Zero the output array
c
      do ii = 1, ntau
         do jj = 1, 3
            newfst( ii, jj ) = 0
         enddo
      enddo
c   
      do j = 1, ntau
c
         newfst( j, 1 ) = int ( intlat( j )*10.0 + 0.5 )
         newfst( j, 2 ) = int ( intlon( j )*10.0 + 0.5 )
         if ( intspd( j ) .lt. 0 ) intspd( j ) = 0
         newfst( j, 3 ) = int ( intspd( j ) )

      enddo
c
      call newWriteAidRcd ( 31,  strmid, dtgcur, new_tech, newfst )
cc      call newWriteAidRcd (  6,  strmid, dtgcur, new_tech, newfst )
c
      return
      end
c
c********1*********2*********3*********4*********5*********6*********7**
      subroutine mspline ( x, f, n, iflag, lflag, xi, fi, ierr )
c
c     This routine applies a quadratic interpolation procedure
c     to f(x) between x(1) and x(n). f(x) is assumed to be
c     represented by quadratic polynomials between the points
c     x(i). The polynomials are chosen so that they equal f(i)
c     at the points x(i), the first derviatives on either
c     side of the interior x(i) match at x(i), and the second
c     derivative of the approximated function integrated
c     over the domain is minimized.
c
c     This version is for interpolating longitude
c
c     Input:  x(1),x(2) ... x(n)      The x values (must be sequential)
c             f(1),f(2) ... f(n)      The function values
c             n                       The number of x,f pairs
c             iflag                   Flag for initialization
c                                      =1 for coefficient calculation
c                                      =0 to use previous coefficients
c             lflag                   Flag for linear interpolation
c                                      =0 to perform linear interpolation 
c                                      =1 to perform quadratic interpolation
c             xi                      The x value at which to interpolate f
c
c     Output: fi                      The interpolated function value
c             ierr                    Error flag
c                                      =0  Normal return
c                                      =1  Parameter nmax is too small or n<2
c                                      =2  The x values are not sequential
c                                      =3  Coefficient iteration did not
c                                          converge
c                                      =4  Mix-up finding coefficients
c                                      =5  if xi .gt. x(n) or .lt. x(1),
c                                          xi is set to nearest endpoint
c                                          before the interpolation
c
c                                     Note: fi is set to -99.9 if
c                                           ierr=1,2,3 or 4
c
      parameter (nmax=100)
c
      dimension x(n),f(n)
c
c     Save variables
      dimension ax(nmax),bx(nmax),cx(nmax)
c
c     Temporary local variables
      dimension df(nmax),dx(nmax),gm(nmax),ct(nmax)
c
      save ax,bx,cx
c
c     Specify unit number for debug write statements
c     and debug flag
      idbug  = 0
      lutest = 6
c
c     Specify minimum reduction in cost function for convergence
      thresh = 1.0e-10
c
c     Check to make sure nmax is large enough, and n is .gt. 1 
      if (n .gt. nmax .or. n .lt. 2) then
         ierr=1
         fi = -99.9
         return
      endif
c
      if (iflag .eq. 1) then
c        Perform the initialization for later interpolation
c
c        Check to make sure x is sequential
         do 10 i=1,n-1
            if (x(i) .ge. x(i+1)) then
               ierr=2
               fi = -99.9
               return
            endif
   10    continue
c
c        Check for special case where n=2. Only linear interpolation
c        is possible.
         if (n .eq. 2) then
            cx(1) = 0.0
            bx(1) = (f(2)-f(1))/(x(2)-x(1))
            ax(1) = f(1) - bx(1)*x(1)
            go to 1500
         endif
c
c        Calculate x and f differences
         do 15 i=1,n-1
            df(i) = f(i+1)-f(i)
            dx(i) = x(i+1)-x(i)
   15    continue
c
c        Calculate domain size
         d = x(n) - x(1)
c
c        Check for linearity of input points
         eps = 1.0e-10
         bb = (f(2)-f(1))/(x(2)-x(1))
         aa = f(1) - bb*x(1)
         dev = 0.0
         do 12 i=3,n
            dev = dev + abs(aa + bb*x(i) - f(i))
   12    continue
c
         if (dev .lt. eps .or. lflag .eq. 0) then
            do 13 i=1,n-1
               cx(i) = 0.0
   13       continue
            go to 1000
         endif
c
c        Iterate to find the c-coefficients
         cx(1) = 0.0
         nit  = 100
         slt  = 0.01
         cfsave = 1.0e+10
c
         do 20 k=1,nit
c           Calculate c values
            do 25 i=2,n-1
               cx(i) = -cx(i-1)*dx(i-1)/dx(i) 
     +                -df(i-1)/(dx(i)*dx(i-1))
     +                +df(i  )/(dx(i)*dx(i  ))
   25       continue
c
c           Calculate current value of cost function
            cf0 = 0.0
            do 26 i=1,n-1
               cf0 = cf0 + cx(i)*cx(i)*dx(i)
   26       continue
            cf0 = 0.5*cf0/d
c
            if (idbug .ne. 0) then
               write(lutest,101) cf0
  101          format(/,' cf0=',e13.6)
            endif
c
c           Check for convergence
            rel = abs(cf0 - cfsave)/abs(cfsave)
            if (rel .lt. thresh) go to 1000
            cfsave = cf0
c
c           Calculate values of Lagrange multipliers
            gm(n-1) = cx(n-1)*dx(n-1)/d
c
            if (n .gt. 3) then
               do 30 i=n-2,2,-1
                  gm(i) = cx(i)*dx(i)/d - gm(i+1)*dx(i)/dx(i+1)
   30          continue
            endif
c
c           Calculate gradient of cost function with respect to c1
            dsdc1 =  dx(1)*(cx(1)/d - gm(2)/dx(2))
c
c           Adjust cx(1) using trial step
            ct(1) = cx(1) - slt*dsdc1
c
c           Calculate remaining c values at trial step
            do 33 i=2,n-1
               ct(i) = -ct(i-1)*dx(i-1)/dx(i) 
     +                 -df(i-1)/(dx(i)*dx(i-1))
     +                 +df(i  )/(dx(i)*dx(i  ))
   33       continue
c
c           Calculate cost function at trial step
            cft = 0.0
            do 31 i=1,n-1
               cft = cft + ct(i)*ct(i)*dx(i)
   31       continue
            cft = 0.5*cft/d
c
c            write(6,*) 'dsdc1,cft,cf0',dsdc1,cft,cf0
c           Calculate optimal step length and re-adjust cx(1)
            den = 2.0*((cft-cf0) + slt*dsdc1*dsdc1)
            if (den .ne. 0.0) then
               slo = dsdc1*dsdc1*slt*slt/den
            else
               slo =0.0
            endif
c
c           Adjust slo if desired
            slo = 1.0*slo
c
            cx(1) = cx(1) - slo*dsdc1
c
            if (idbug .ne. 0) then
               write(lutest,100) k,cft,slt,slo
  100          format(' Iteration=',i4,'  cf1=',e11.4,' slt=',e11.4,
     +                                                ' slo=',e11.4)
c     
               do 99 j=1,n-1
                  write(lutest,102) j,cx(j)
  102             format('    i=',i2,' c=',f8.4)
   99          continue
            endif
c
c           Calculate trial step for next time step
            slt = 0.5*slo
   20    continue
c
c        Iteration did not converge
         ierr=3
         fi=-99.9
         return
c
c        Iteration converged
 1000    continue
c
         if (idbug .ne. 0) then
            write(lutest,104)
  104       format(/,' Iteration converged')
         endif
c
c        Calculate b and a coefficients
         do 40 i=1,n-1
            bx(i) = df(i)/dx(i) - cx(i)*(x(i+1) + x(i))
            ax(i) = f(i) - bx(i)*x(i) - cx(i)*x(i)*x(i)
   40    continue        
      endif
c
 1500 continue
c     Interpolate the function
c
c     Check for xi out of bounds
      if (xi .lt. x(1)) then
         xi = x(1)
         ierr = 5
      endif
c
      if (xi .gt. x(n)) then
         xi = x(n)
         ierr = 5
      endif
c
c     Find the interval for the interpolation
      ii = 1
      do 50 i=2,n
         if (xi .le. x(i)) then
            ii = i-1
            go to 2000
         endif
   50 continue
c
      fi = -99.9
      ierr=4
      return
c
 2000 continue
      fi = ax(ii) + bx(ii)*xi + cx(ii)*xi*xi
c
      return
      end
c
c********1*********2*********3*********4*********5*********6*********7**
      subroutine guns ( strmid, dtgcur, new_tech )
c
c**   Do the GUNS - GFDI, NGPI, and UKMI, if possible
c
      parameter ( nmodel=16, ntau=11 )
c
      common /intrp/ intlat(ntau,nmodel), intlon(ntau,nmodel),
     &               intspd(ntau,nmodel)
c
      real intlat, intlon, intspd
      real newlat(ntau), newlon(ntau), newspd(ntau)
c
      character*4  new_tech
      character*8  strmid
      character*10 dtgcur
c      
      do j = 1, ntau
c
         newlat(j) = 0.0
         newlon(j) = 0.0
         newspd(j) = 0.0
c
         if ( intlat(j,3) .gt. 0.01 .and. intlon(j,3) .gt. 0.01 .and.
     &        intlat(j,5) .gt. 0.01 .and. intlon(j,5) .gt. 0.01 .and.
     &        intlat(j,6) .gt. 0.01 .and. intlon(j,6) .gt. 0.01 ) 
     &        then
c
            newlat(j) = (intlat(j,3) + intlat(j,5) + intlat(j,6))/3.0
            newlon(j) = (intlon(j,3) + intlon(j,5) + intlon(j,6))/3.0
c
         endif
c
      enddo
c
c**   Write out the new forecast
c
      call write_out ( strmid, dtgcur, new_tech, 
     &                 newlat, newlon, newspd )
c 
      return
      end
c********1*********2*********3*********4*********5*********6*********7**
c
      subroutine guna ( strmid, dtgcur, new_tech )
c
c**   Do the GUNA - AVNI, GFDI, NGPI, and UKMI, if possible
c
      parameter ( nmodel=16, ntau=11 )
c
      common /intrp/ intlat(ntau,nmodel), intlon(ntau,nmodel),
     &               intspd(ntau,nmodel)
c
      real intlat, intlon, intspd
      real newlat(ntau), newlon(ntau), newspd(ntau)
c
      character*4  new_tech
      character*8  strmid
      character*10 dtgcur
c      
      do j = 1, ntau
c
         newlat(j) = 0.0
         newlon(j) = 0.0
         newspd(j) = 0.0
c
         if ( intlat(j,2) .gt. 0.01 .and. intlon(j,2) .gt. 0.01 .and.
     &        intlat(j,3) .gt. 0.01 .and. intlon(j,3) .gt. 0.01 .and.
     &        intlat(j,5) .gt. 0.01 .and. intlon(j,5) .gt. 0.01 .and.
     &        intlat(j,6) .gt. 0.01 .and. intlon(j,6) .gt. 0.01 ) 
     &        then
c
            newlat(j) = (intlat(j,2) + intlat(j,3) + 
     &                   intlat(j,5) + intlat(j,6))/4.0
            newlon(j) = (intlon(j,2) + intlon(j,3) + 
     &                   intlon(j,5) + intlon(j,6))/4.0
            newspd(j) = 0.0
c
         endif
c
      enddo
c
c**   Write out the new forecast
c
      call write_out ( strmid, dtgcur, new_tech,
     &                 newlat, newlon, newspd )
c 
      return
      end
