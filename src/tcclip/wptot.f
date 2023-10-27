      program wptot
c
c ....................... start prolog ..........................
c
c  program name: wptot
c  
c  description:  Computes extrapolation, cliper, and stifor
c		 forecasts for a storm in the western
c		 North Pacific. Extrapolation is computed 
c                from the current and 12 hour old positions.
c                Cliper is a statistical forecast track model
c		 based on the track and intensity data.
c
c  original programmer, date: unknown (probably Ron Miller)
c
c  current programmer:        buck sampson, nrl
c
c  usage:                     wptot wp0190 >wptot.txt
c
c  input files:
c    b????.dat - tropical cyclone present and past locations
c
c  output files:
c    wptot.dat - xtrp, clip and stifor forecasts in adeck (ccrs) format
c    wptot.txt - textual output of wptot.dat
c
c  error conditions: no cliper forecast if storm is not within
c                    the western North Pacific basin.
c                   
c                    abort program if input file not in b deck
c                    format
c
c ............. maintenance section ................................
c
c  brief description of program modules:
c     dirdst   - computes direction and distance from one point to another
c     extrap   - computes extrapolation position forecast
c     icrdtg   - creates new dtg given old one and time difference
c     locase   - puts character string in lower case 
c     openfile - opens a given file (different on Concurrent)
c     rhdst    - computes distance and direction given lats and lons
c                (rhumb-line)
c     rltlg    - computes lat and lon given lat,lon,direction and distance
c                by moving along a rhumb line
c     stif     - computes stifor intensity forecast
c     wpclpr   - computes cliper position forecast
c     wpstif5d - computes stifor intensity forecast out to 5 days
c
c  principal variables and arrays:
c     clalo    - array of cliper forecast lats,lons
c     filename - location of the output file
c     int12 ...- 12 hr stifor forecast intensity
c     la0      - current latitude
c     lo0      - current longitude
c     lam06 ...- 6 hr old latitude
c     lom06 ...- 6 hr old longitude
c     lam12 ...- 12 hr old latitude
c     lom12 ...- 12 hr old longitude
c     strmid   - storm id (e.g., wp0190)
c     storms   - location of the storms directory
c     wind     - current intensity
c     wind12   - 12 hr old intensity
c     xp       - extrapolation forecast data
c     ymdh     - date (YYMMDDHH)
c
c
c  references:
c     Xu, Y. and C.J. Neumann, 1985: A Statistical Model for the 
c     Prediction of Western North Pacific Tropical Cyclone Motion
c     (WPCLPR).  NOAA Technical Memorandum NWS NHC 28, 30 pp.
c
c     Chu, J.H., 1994: A Regression Model for the Western North
c     Pacific Tropical Cyclone Intensity Forecast. Naval Res. Lab.,
c     Monterey, CA. NRL/MR/7541--94-7215
c
C     SAIC Final Report on the Southwest Pacific CLIPER Model (SWCLP)
C     October, 2000
C
C     SAIC Final Report on the CLIPER Model for the Australia/Southeast Indian Ocean Tropical Cyclone Basin
C     October, 2000
C
C     5 Day STIFOR (yet to be published, John Knaff CIRA)                                           
c
c  method:
c     The working best track is read in and models (clipers,
c     stifor and extrapolation) are run.  Results of the models
c     are then written to a file in the "adeck" format.
c     
c  language: FORTRAN 77
c
c  record of changes:
c
c     Modified to use new data format,  6/98   A. Schrader
c     Included intensity extrapolation (12 hour trend) ... sampson nrl, Aug 98
c     Included SWPCLP                                  ... sampson nrl, May 01
c     Included SEICLP                                  ... sampson nrl, May 01
c     Included 5 DAY STIFOR                            ... sampson nrl, May 01
c
      include 'dataioparms.inc'

      common/xtrp/ xp(2,10)
      common /stifr5d/ istifr5d( 10, 3 )
      integer ymdh,wind,wind06,wind12,wind18,wind24
      integer ltlnwnd(numtau,llw)
      integer ltlnwn1(numtau,llw)
      integer ii, iarg
      integer ibtwind, ios
      real la0,lo0,lam06,lom06,lam12,lom12,lam18,lom18,lam24,lom24
      real cnmis(12),clalo(12),p1top8(8)
      real cll120(20)
      real int12, int24, int36, int48, int60, int72
      real btlat, btlon
      character*8 idtg,fstdtg,dtgm06,dtgm12,dtgm18,dtgm24
      character*8 tdtg
      character*8 btdtg
      character*6 strmid
      character*4 aidid
      character*2 century
      character*2 cent
      character*1 ns,ew
      character*30 bname
      character*100 storms,filename
      character*25 line
      logical fstclp
      logical fstst5d
      logical tswpclp
      logical tseiclp
c
      data fstclp  /.true./
      data fstst5d /.true./
      data tswpclp /.true./
      data tseiclp /.true./
      data aidid   /"    "/
      data igt0,igtm12,igtm24 /3*0/     

      print *,' '
      print *,' '
      print *,' '
      print *,'*************************************************** '
      print *,'                OBJECTIVE AIDS                      '
c
c  open files
c
c   2 - best track
c   7 - cliper and extrapolation forecasts in ccrs format
c
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
      call getarg(iarg,century)
      iarg = iarg + 1
      write(filename,'(a,a,a,a,a,a)') storms(1:ind), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      open (2,file=filename,status='old',err=9001)
      write(filename,'(a,a)')storms(1:ind),"/wptot.dat"
      call openfile( 7, filename, 'unknown', ioerror )
      rewind 1
      rewind 2
      rewind 7
c
c  make the basin of the storm id upper case
c
      if (ichar(strmid(1:1)) .gt. 96) strmid(1:1) = 
     &         char(ichar(strmid(1:1))-32)
      if (ichar(strmid(2:2)) .gt. 96) strmid(2:2) = 
     &         char(ichar(strmid(2:2))-32)

      print *,'*************************************************** '
      write (6,6000) strmid
c
c  the technique numbers for CLIP and XTRP
c
      iclip=3
      ixtrp=3
c
c  find the last dtg in the best track file
c
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 2,cent,tdtg,btlat,ns,btlon,ew,ibtwind,ios )
         if (tdtg.ne.'        ') fstdtg=tdtg
      enddo
c
c
c  now find the current, -6, -12, -18, and -24 hr positions
c
      call icrdtg (fstdtg,dtgm06,-06)
      call icrdtg (fstdtg,dtgm12,-12)
      call icrdtg (fstdtg,dtgm18,-18)
      call icrdtg (fstdtg,dtgm24,-24)
      rewind 2
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 2,century,btdtg,btlat,ns,btlon,ew,ibtwind,ios )
         if( ios .eq. 0 ) then
            if( btdtg .eq. dtgm24 ) then
               lam24 = btlat
               lom24 = btlon
               wind24 = ibtwind
               if (ns .eq. 'S') lam24 = -lam24
               if (ew .eq. 'W') lom24 = 360.0 - lom24
               igtm24 = 1
            else if( btdtg .eq. dtgm18 ) then
               lam18 = btlat
               lom18 = btlon
               wind18 = ibtwind
               if (ns .eq. 'S') lam18 = -lam18
               if (ew .eq. 'W') lom18 = 360.0 - lom18
               igtm18 = 1
            else if( btdtg .eq. dtgm12 ) then
               lam12 = btlat
               lom12 = btlon
               wind12 = ibtwind
               if (ns .eq. 'S') lam12 = -lam12
               if (ew .eq. 'W') lom12 = 360.0 - lom12
               igtm12 = 1
            else if( btdtg .eq. dtgm06 ) then
               lam06 = btlat
               lom06 = btlon
               wind06 = ibtwind
               if (ns .eq. 'S') lam06 = -lam06
               if (ew .eq. 'W') lom06 = 360.0 - lom06
               igtm06 = 1
            else if( btdtg .eq. fstdtg ) then
               read( btdtg, '(i8)' ) ymdh
               la0 = btlat
               lo0 = btlon
               wind = ibtwind
               if (ns .eq. 'S') la0 = -la0
               if (ew .eq. 'W') lo0 = 360.0 - lo0
               igt0 = 1
            endif
         endif
      enddo
      close (2)
c
c  we must have at least a current and -12 position.  we can extrapolate
c  a -24 posit if necessary
c
      if (igt0 .eq. 0) then
        write (6,6006)
        stop 'WPCLIP: MUST HAVE VALID CURRENT AND -12 POSITS'
      endif
      if (igtm12 .eq. 0) then
        write (6,6007)
        stop 'WPCLIP: MUST HAVE VALID CURRENT AND -12 POSITS'
      endif
      if (igtm24 .eq. 0) then
        write (6,6008)
        call rhdst (la0,lo0,lam12,lom12,dir,dst)
        call rltlg (lam12,lom12,lam24,lom24,dir,dst)
      endif
c
c  check to make sure intensity is ok
c
      if (wind .le. 0) then
         write (6,6009)
         fstclp =  .false.
         fstst5d = .false.
         tswpclp = .false.
         tseiclp = .false.
      endif
c
c  wpcliper can only run between 6n and 45n and between 100e and 180e.
c
      if (la0 .lt. 3. .or. la0 .gt. 45.) then
         write (6,6003) la0,lo0
         fstclp = .false.
      else if (lo0 .gt. 180. .or. lo0 .lt. 100.) then
         write (6,6003) la0,lo0
         fstclp = .false.
      endif
c
c  swpclp can only run between 3s and 45s and between 140e and 135w.
c
      if (la0 .gt. -3. .or. la0 .lt. -45.) then
         write (6,6004) la0,lo0
         tswpclp = .false.
      else if (lo0 .lt. 140. .or. lo0 .gt. 225.) then
         write (6,6004) la0,lo0
         tswpclp = .false.
      endif
c
c  seiclp can only run between 3s and 45s and between 140e and 100e.
c
      if (la0 .gt. -3. .or. la0 .lt. -45.) then
         write (6,6005) la0,lo0
         tseiclp = .false.
      else if (lo0 .gt. 140. .or. lo0 .lt. 100.) then
         write (6,6005) la0,lo0
         tseiclp = .false.
      endif
c
c  stifor-5day only runs between 0n and 45n and between 80e and 180e.
c
      if (la0 .lt. 0. .or. la0 .gt. 45.) then
         write (6,6010) la0,lo0
         fstst5d = .false.
      else if (lo0 .gt. 180. .or. lo0 .lt. 80.) then
         write (6,6010) la0,lo0
         fstst5d = .false.
      endif
c
c  write input to screen
c
        print*,'   date:',ymdh
        print*,'   -24 hr  pos:',lam24,'N',lom24,'E',wind24,'kts'
        print*,'   -18 hr  pos:',lam18,'N',lom18,'E',wind18,'kts'
        print*,'   -12 hr  pos:',lam12,'N',lom12,'E',wind12,'kts'
        print*,'   -06 hr  pos:',lam06,'N',lom06,'E',wind06,'kts'
        print*,'   current pos:',la0,'N',lo0,'E',wind,'kts'

c
c  compute wp cliper forecasts
c
      if (fstclp) then
        rwind=float(wind)
        call wpclpr (ymdh,la0,lo0,lam12,lom12,lam24,
     &          lom24,rwind,cnmis,clalo,p1top8)
c
c  compute stifor intensity
c
	call stif(ymdh,la0,lo0,lam12,lom12,wind,wind12,
     &          int12, int24, int36, int48, int60, int72)
      endif
c
c  compute extrapolation
c
      call extrap (la0,lo0,lam12,lom12)
      dir = 1.0
      call dirdst (lam12,(360.0-lom12),la0,(360.0-lo0),dir,dst)
      idir = dir + 0.5
cx    ispd = (dst / 12.0) * 10.0
      ispd = (dst / 12.0) 
c
c   don't care about 60 hr cliper forecast, assign to 72
c
      clalo(9)=clalo(11)
      clalo(10)=clalo(12)

c  print the cliper/stifor output for 12,24,36,48, and 72 hrs
      if (fstclp) then
     
        print *, '   WPCLIPER/STIFOR FCST is:'
        print *,'   +12 hr pos:',clalo(1),'N',clalo(2),'E',int12,'kts'
        print *,'   +24 hr pos:',clalo(3),'N',clalo(4),'E',int24,'kts'
        print *,'   +36 hr pos:',clalo(5),'N',clalo(6),'E',int36,'kts'
        print *,'   +48 hr pos:',clalo(7),'N',clalo(8),'E',int48,'kts'
        print *,'   +72 hr pos:',clalo(9),'N',clalo(10),'E',int72,'kts'
     
        do ii=1, 5
           ltlnwnd(ii,1) = int(clalo(2*ii-1)*10.+0.5)
           ltlnwnd(ii,2) = int((360.0-clalo(2*ii))*10.+0.5)
        enddo
        ltlnwnd(1,3) = int(int12)
        ltlnwnd(2,3) = int(int24)
        ltlnwnd(3,3) = int(int36)
        ltlnwnd(4,3) = int(int48)
        ltlnwnd(5,3) = int(int72)
        call writeAid( 7, strmid, cent, fstdtg, 'CLIP', ltlnwnd )
      endif 
     
c  extrapolation
     
        do ii=1, 10
           ltlnwn1(ii,1) = int(xp(1,ii)*10.+0.5)
           ltlnwn1(ii,2) = int((360.0-xp(2,ii))*10.+0.5)
	   iwnd = (wind + (wind-wind12)*ii)
           ltlnwn1(ii,3) = max( 0, iwnd )
        enddo

        print *, '   EXTRAPOLATION FCST is:'
        print *,'  +12 hr pos:',xp(1,1),'N',xp(2,1),'E ',ltlnwn1(1,3)
        print *,'  +24 hr pos:',xp(1,2),'N',xp(2,2),'E ',ltlnwn1(2,3)
        print *,'  +36 hr pos:',xp(1,3),'N',xp(2,3),'E ',ltlnwn1(3,3)
        print *,'  +48 hr pos:',xp(1,4),'N',xp(2,4),'E ',ltlnwn1(4,3)
        print *,'  +60 hr pos:',xp(1,5),'N',xp(2,5),'E ',ltlnwn1(5,3)
        print *,'  +72 hr pos:',xp(1,6),'N',xp(2,6),'E ',ltlnwn1(6,3)
        print *,'  +84 hr pos:',xp(1,7),'N',xp(2,7),'E ',ltlnwn1(7,3)
        print *,'  +96 hr pos:',xp(1,8),'N',xp(2,8),'E ',ltlnwn1(8,3)
        print *,' +108 hr pos:',xp(1,9),'N',xp(2,9),'E ',ltlnwn1(9,3)
        print *,' +120 hr pos:',xp(1,10),'N',xp(2,10),'E ',ltlnwn1(10,3)
        call writeAid( 7, strmid, cent, fstdtg, 'XTRP', ltlnwn1 )
     
c
c  compute 120 hour cliper forecast
c
      if (fstclp) then
        ibtwind=wind
	print *, 'CLIP120 Input:'
	print *, 'ymdh, la0, lo0, ibtwind, idir, ispd'
	print *, ymdh, la0, lo0, ibtwind, idir, ispd
        call wpclip120 (ymdh,la0,lo0,ibtwind,idir,ispd,ltlnwn1)

     
        print *, '   120 HR CLIPER FCST is:'
        print *,'   +12 hr pos:',ltlnwn1(1,1),'N',ltlnwn1(1,2),'E'
        print *,'   +24 hr pos:',ltlnwn1(2,1),'N',ltlnwn1(2,2),'E'
        print *,'   +36 hr pos:',ltlnwn1(3,1),'N',ltlnwn1(3,2),'E'
        print *,'   +48 hr pos:',ltlnwn1(4,1),'N',ltlnwn1(4,2),'E'
        print *,'   +60 hr pos:',ltlnwn1(5,1),'N',ltlnwn1(5,2),'E'
        print *,'   +72 hr pos:',ltlnwn1(6,1),'N',ltlnwn1(6,2),'E'
        print *,'   +84 hr pos:',ltlnwn1(7,1),'N',ltlnwn1(7,2),'E'
        print *,'   +96 hr pos:',ltlnwn1(8,1),'N',ltlnwn1(8,2),'E'
        print *,'   +108hr pos:',ltlnwn1(9,1),'N',ltlnwn1(9,2),'E'
        print *,'   +120hr pos:',ltlnwn1(10,1),'N',ltlnwn1(10,2),'E'
        do ii=1, 10
           ltlnwn1(ii,2) = (3600-ltlnwn1(ii,2))
        enddo
        call writeAid( 7, strmid, cent, fstdtg, 'C120', ltlnwn1 )
      endif
c
c  compute swpclp or seiclp forecasts
c
      if (tswpclp .or. tseiclp) then
	la0=-la0
	lam12=-lam12
	lam24=-lam24
        rwind=float(wind)

	if (tswpclp) then
            call swpclp (ymdh,la0,lo0,lam12,lom12,lam24,
     &                  lom24,rwind,cnmis,clalo,p1top8)
	    aidid="CLSW"
            print *, '   SW Pacific CLIPER (CLSW) FCST is:'
	elseif (tseiclp) then
            call seiclp (ymdh,la0,lo0,lam12,lom12,lam24,
     &                  lom24,rwind,cnmis,clalo,p1top8)
	    aidid="CLAU"
            print *, '   SE Indian/Aus CLIPER (CLAU) FCST is:'
        endif

        clalo(9)=clalo(11)
        clalo(10)=clalo(12)
        print *,'   +12 hr pos:',clalo(1),'S',clalo(2),'E'
        print *,'   +24 hr pos:',clalo(3),'S',clalo(4),'E'
        print *,'   +36 hr pos:',clalo(5),'S',clalo(6),'E'
        print *,'   +48 hr pos:',clalo(7),'S',clalo(8),'E'
        print *,'   +72 hr pos:',clalo(9),'S',clalo(10),'E'
     
        do ii=1, 5
           ltlnwnd(ii,1) = -int(clalo(2*ii-1)*10.+0.5)
           ltlnwnd(ii,2) = int((360.0-clalo(2*ii))*10.+0.5)
        enddo
        call writeAid( 7, strmid, cent, fstdtg, aidid, ltlnwnd )
      endif

c*
c*  compute wpstif5d forecasts
c*
      latdum=0 ! dummy variable for printing the 0 longitude to
c              ! standard out.  The value sent to WriteAid is
c              ! 3600 which will cause 0E to be used in the atcf
c
      if(fstst5d)then
         rwind  =float(wind)
         rwind12=float(wind12)
         call wpstif5d(ymdh,la0,lo0,lam12,lom12,rwind,rwind12)
         print *, ' 5-Day STIFOR (ST5D) FCST is:'
         print *,'  +12 hr pos:',istifr5d(1,1),'N',latdum,
     .       'E ',istifr5d(1,3)
         print *,'  +24 hr pos:',istifr5d(2,1),'N',latdum,
     .       'E ',istifr5d(2,3)
         print *,'  +36 hr pos:',istifr5d(3,1),'N',latdum,
     .       'E ',istifr5d(3,3)
         print *,'  +48 hr pos:',istifr5d(4,1),'N',latdum,
     .       'E ',istifr5d(4,3)
         print *,'  +60 hr pos:',istifr5d(5,1),'N',latdum,
     .       'E ',istifr5d(5,3)
         print *,'  +72 hr pos:',istifr5d(6,1),'N',latdum,
     .       'E ',istifr5d(6,3)
         print *,'  +84 hr pos:',istifr5d(7,1),'N',latdum,
     .       'E ',istifr5d(7,3)
         print *,'  +96 hr pos:',istifr5d(8,1),'N',latdum,
     .       'E ',istifr5d(8,3)
         print *,' +108 hr pos:',istifr5d(9,1),'N',latdum,
     .       'E ',istifr5d(9,3)
         print *,' +120 hr pos:',istifr5d(10,1),'N',latdum,
     .       'E ',istifr5d(10,3)
         call writeAid( 7, strmid, cent, fstdtg, 'ST5D', istifr5d )
      endif
      goto 9999
c
c
 5000 format (6x,i8,6f4.1,i3,10x,a6)
6000  format(10x,'cliper/stifor/extrap forecasts for ',a6//) 
6001  format(' ',' warning dtg (year = ',i2,') (month = ',i2,') (day =',
     1  i3,') (hour = ',i2,')'/)
6002  format(' ',10x,'tau = ',f5.1,'    lat = ',f5.1,'n',
     1  '   long = ',f6.1,'e'/)
6003  format(' ** no wpcliper forecast **    current position:',2f6.1,
     1 '  is outside domain (3n-45n,180e-100e).')
6004  format(' ** no swpclp   forecast **    current position:',2f6.1,
     1 '  is outside domain (3s-45s,140e-135w).')
6005  format(' ** no seiclp   forecast **    current position:',2f6.1,
     1 '  is outside domain (3s-45s,100e-140e).')
6006  format(' **** cliper stop **** must have valid current posit.')
6007  format(' **** cliper stop **** -12hr bad or missing.')
6008  format(' -24hr posit does not exist.  will extrapolate backward',
     &    ' from 00 and -12')
6009  format(' ** no cliper forecast ** storm intensity <= 0.')
6010  format(' ** no st5d forecast **    current position:',2f6.1,
     1 '  is outside domain (0n-45n,80e-180e).')
7000  format(i8)
7001  format(4i2)
 7900 format (i2.2,'CLIP',a8,10i4,5i3,' ',a6)
 8000 format (i2.2,'XTRP',a8,10i4,'  0  0  0  0  0 ',a6)
c
 9000 continue
      print*,' error opening techlist.dat file'
      stop 'WPCLIP: error opening techlist.dat file'
 9001 continue
      print*,' error opening best track data file'
      stop 'WPCLIP: error opening best track data file'
 9002 continue
      print*,' error unexpected eof in techlist.dat '
      stop 'WPCLIP: unexpected eof in techlist.dat'
 9003 continue
      print*,' error unexpected eof in best track data file'
      stop 'WPCLIP: unexpected eof in best track data file'

 9999 continue
      stop 'WPCLIP: GOOD STOP'
      end
c
c 
      subroutine extrap (la0,lo0,lam12,lom12)
      common/xtrp/ xp(2,10)
      real la0,lo0,lam12,lom12
c
c  this routine computes the extrapolation forecast using the past 
c  12 hr motion
c
      call rhdst (lam12,lom12,la0,lo0,dir,dst)
      call rltlg (la0,lo0,xp(1,1),xp(2,1),dir,dst*1.)
      call rltlg (la0,lo0,xp(1,2),xp(2,2),dir,dst*2.)
      call rltlg (la0,lo0,xp(1,3),xp(2,3),dir,dst*3.)
      call rltlg (la0,lo0,xp(1,4),xp(2,4),dir,dst*4.)
      call rltlg (la0,lo0,xp(1,5),xp(2,5),dir,dst*5.)
      call rltlg (la0,lo0,xp(1,6),xp(2,6),dir,dst*6.)
      call rltlg (la0,lo0,xp(1,7),xp(2,7),dir,dst*7.)
      call rltlg (la0,lo0,xp(1,8),xp(2,8),dir,dst*8.)
      call rltlg (la0,lo0,xp(1,9),xp(2,9),dir,dst*9.)
      call rltlg (la0,lo0,xp(1,10),xp(2,10),dir,dst*10.)
      return
      end
