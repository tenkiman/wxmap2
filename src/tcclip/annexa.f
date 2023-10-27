      program annexa
c
c     this program calculates the wind intensity and forecast track erro
c     for taus 0, 12, 24, 36, 48 and 72.  the indut data sets required 
c     are the ccrs a-deck,b-deck and the  obdat.  the output produced is
c     a formatted tabular listing.
c
cx  converted to ATCF 3.0         sampson,nrl        may 96
cx  added intensity (wind) bias   sampson,nrl        jan 98
cx  added cent variable           sampson,nrl        nov 98
cx  Attempted some cleanup of spaghetti code.  schrader,saic   june 99
cx    (Made the subroutines, readastorm, getacarq and getobjaid.  
cx     Substituted do-endo's and if-endif's for some goto's.)
cx  Modified to include errors for tau's 96 and 120.  schrader,saic  june 99
cx  Added pre-warning posits to table  sampson,nrl        june 99
cx                                
c
c
      INCLUDE  'dataformats.inc'
c
c
      character*100 btrk,adec,obdat,outfil,storms,filename
      character*8 wdtg,odtg,bdtg(200),prtdtg
      character cyyr*4,strmid*6,pltfrm*6,ns*1,ew*1
      character trkerr(7)*6,interr(8)*3,tab*1,objaid*4
      character iposit(2)*4
      character*1 indat
      real blat(200),blon(200),bvmax(200),jlat(7),jlon(7),jwnd(7)
      real errsum(8,2),intsum(8),intbia(8)
      real btlat, btlon
      logical endb,odexist,endo,samestorm,endcarqs
      integer ios, iresult, itau, nb, ireadstat, itech, iarg
      logical iwarn1
      type (AID_DATA) aidRcd
      type (A_RECORD) aRecord
  
      data iposit /'CARQ','WRNG'/

c***********************************************************************
      iwarn1 = .TRUE.
 
c  get i/o files from command line (or shell script)
c  arg1=btrk, arg2=adeck, arg3=obdat, arg4=outfil
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg(iarg,btrk)
      iarg = iarg + 1
      call getarg(iarg,adec)
      iarg = iarg + 1
      call getarg(iarg,obdat)
      iarg = iarg + 1
      call getarg(iarg,outfil)
c  get user options from command line (or shell script)
c  arg5=4 letter objective aid identifier, arg6=1 (CARQ) or 2 (WARNING)
      iarg = iarg + 1
      call getarg(iarg,objaid)
      iarg = iarg + 1
      call getarg(iarg,indat)
      read(indat,'(i1)',err=9051)init
cx     print*,'the current storm is:',strmid
cx     print*,'the input file1 is:',btrk
cx     print*,'the input file2 is:',adec
cx     print*,'the input file3 is:',obdat
cx     print*,'the output file8 is:',outfil

c  the following line is required for sco-xenix (lpi)
c  dont use it with the hp-fortran compiler;
c      open (7, file='stderr')
c      inquire (file='stderr',number=num)
c      print*,'number associated with stderr is:',num

c  define unit numbers-
c  unit2 = best track (btrk)
c  unit3 = obj aids file (adec)
c  unit4 = obj data file (obdat)
c  unit5 = fortran standard input (keyboard)
c  unit6 (or *) = fortran standard output (terminal screen)
c  unit17= debugging output 
c  unit8 = table output (outfil)
c  unit9 = tab-delimited output (tab.out)

c  open files
cx  TAC IV requirement
      call openfile (17, 'annexa.dbg', 'unknown', ioerror )
      open (2,file=btrk,status='old',iostat=ios,err=9021)
      open (3,file=adec,status='old',iostat=ios,err=9031)

c  check to see if the obdat exists. if not, we can still run without it
c
      open (4,file=obdat,status='old',iostat=ios,err=9041)
 9041 if (ios .eq. 0) then
         odexist = .true.
      else
         write (17,'(''WARNING 9041 in ANNEXA.F - '',
     &        '' obdat file not found: '',/,2x,a)') obdat
         write (17,'(''   continuing without it. '')')
cx       write (*,'(''ANNEXA.F: obdat file not found: '')')
cx       write (*,'(''     will continue without it '')')
         odexist = .false.
      endif

      call openfile ( 8, outfil, 'unknown', ioerror )
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
      write(filename,'(a,a)')storms(1:ind),'/tab.out'
      call openfile ( 9, filename, 'unknown', ioerror )
c
      tab = char(9)
      endb = .false.
      endo = .false.
c
c  get the obj aid that the user wishes to run the program for
c  make sure technique name is upper case
c
      do i=1,4
         n = ichar(objaid(i:i))
         if (n .ge. 97 .and. n .le. 122) objaid(i:i) = char(n-32)
      enddo
c
c
c  begin loop
c
 60   continue
c
      do i=1,8
         do j=1,2
            errsum(i,j) = 0.0
         enddo
         intsum(i) = 0.0
         intbia(i) = 0.0
      enddo
c
c  read one storm from the best track file
c
      call readastorm( bdtg, cyyr, nb, endb, blat, blon, bvmax )

      nwrng = 0
c
c      read a-deck until a carq or wrng card is read. 
c
 100  call getacarq( strmid,cyyr,iposit(init),endcarqs,aidRcd,
     &               ireadstat )
      if( ireadstat .ne. 1 ) goto 9998
      if (endcarqs) then
cx          print *,'before totals, wdtg:',wdtg
cx          print *,'before totals also, strmid, cyyr',strmid,cyyr
         call totals (errsum,intsum,intbia)
         if (endb) then
            goto 9999
         else
            goto 60
         endif
      endif

c     get TAU 0 carq or wrng data
      call getAidTAU( aidRcd, 0, aRecord, iresult )
      if( iresult .eq. 1 ) then
         wdtg = aRecord%DTG(3:10)
         wrlat = aRecord%lat
         if( aRecord%NS .eq. 'S' ) wrlat = -wrlat
         wrlon = aRecord%lon
         if( aRecord%EW .eq. 'E' ) wrlon = 360.0 - wrlon
         wrwnd = aRecord%vmax
      endif
      if (nwrng .eq. 0) then
         write (8,'(/20x,''Statistics for '',a4,'' on storm '',a6)')
     &    objaid,strmid
         write (8,150) 
  150    format(/'          WRN      BEST TRACK           POSITION',
     &           ' ERRORS                         WIND ERRORS       ',
     &           '           PLATFORM',/
     &           '   DTG    NO.   LAT   LONG  wind  00   12   24   36',
     &           '   48   72   96  120   00  12  24  36  48  72   96',
     &           '  120')
      endif
 
      nwrng = nwrng + 1
c
c     read the rest of the dtg in the a-deck, searching for the
c     obj aid forecast
c
      call getobjaid( objaid,wdtg,cyyr,itech,jlat,jlon,jwnd,ireadstat )
      if( ireadstat .ne. 1 ) goto 9998
c
c  read obdat file 
c
      pltfrm = '      '
      if ( .not. endo .and. odexist ) then
         idiff = -1
         samestorm = .true.
c        loop on reading until end-of-file or find (or pass) dtg 
c        or read record for different storm
         do while ( .not. endo .and. idiff .lt. 0 .and. samestorm ) 
            read (4,3000,iostat=ios) strmid,odtg,pltfrm
 3000       format (a6,a8,6x,a6)
            if( ios .eq. 0 ) then    ! good read
               if (strmid(3:6) .ne. cyyr) then   ! new storm
                  pltfrm = '      '
                  backspace 4
                  samestorm = .false.
               else
                  call dtgdif (wdtg,odtg,idiff)
                  if (idiff .gt. 0) then   ! passed the dtg
                     pltfrm = '      '
                     backspace 4
                  endif
               endif
            else if( ios .lt. 0 ) then   ! end-of-file
               endo = .true.
            endif
         enddo
      endif

      call dtgdif (bdtg(1),wdtg,idiff)
      idiff = idiff / 6 + 1
      if( idiff .lt. 1 ) goto 100           ! skip if no bt for this dtg
cx.....  preliminary track posits to output as requested by JTWC Jun 99 .. sampson
      if( iwarn1 .eq. .TRUE. ) then
	   do iptrk = 1, idiff-1
              btlat = abs(blat(iptrk))
              ns = 'N'
              if (blat(iptrk) .lt. 0.0) ns = 'S'
              btlon = blon(iptrk)
              ew = 'W'
              if (btlon .gt. 180.0) then
                 ew = 'E'
                 btlon = 360.0 - btlon
              endif
	      prtdtg = bdtg(iptrk)
              write (8,2000)prtdtg,btlat,ns,btlon,ew,int(bvmax(iptrk))
 2000         format(1x,a8,4x,2x,f4.1,a1,1x,f5.1,a1,i4)
	   enddo
	   iwarn1 = .FALSE.
      endif
cx........end of prelimary track posit code.......................................
      if (blat(idiff) .eq. 0.0) goto 100    ! skip if no bt for this dtg
c
c     figure and sum the errors for tau 0
c
      call dirdst (blat(idiff),blon(idiff),wrlat,wrlon,dir,dst)
c
c  sum the warning errors
c
      errsum(1,1) = errsum(1,1) + dst
      errsum(1,2) = errsum(1,2) + 1.
c
      if (wrwnd .gt. 0.0 .and. bvmax(idiff) .gt. 0.0) then
         iwwrer = wrwnd - bvmax(idiff)
         write (interr(1),'(i3)') iwwrer
         intsum(1) = intsum(1) + iabs(iwwrer)
         intbia(1) = intbia(1) + iwwrer
cx       print *, 'iwwrer...:',iwwrer,wrwnd,bvmax(idiff),intbia(1)
      else
         interr(1) = '   '
      endif
c 
c     figure and sum the errors for taus 12 - 120
c
      do i=1,7
         itau = idiff + i*2
         if (i .ge. 5) itau = idiff + ((i-2)*4)
         if (itau .le. nb .and. jlat(i) .ne. 0.0 .and. jlon(i) .ne. 0.0
     &        .and. blat(itau) .ne. 0.0 .and. blon(itau) .ne. 0.0 .and.
     &        itech .ne. 0) then
            if (jwnd(i) .ne. 0 .and. bvmax(itau) .gt. 0.0) then 
               ifwder = jwnd(i) - bvmax(itau)
cx             write (8,*) 'i,jwnd(i), bvmax(itau),itau'
cx             write (8,*) i,jwnd(i), bvmax(idiff),idiff
               write (interr(i+1),'(i3)') ifwder
               intsum(i+1) = intsum(i+1) + iabs(ifwder)
               intbia(i+1) = intbia(i+1) + ifwder
cx             print *,ifwrer,jwnd(i),bvmax(itau),intbia(i+1)
            else
               interr(i+1) = '   '
            endif
            call dirdst (blat(itau),blon(itau),jlat(i),jlon(i),dir,
     &           fdst)
cx          write (trkerr(i),'(i4)') int(fdst)
            write (trkerr(i),'(i4)') nint(fdst)
c     
c     sum the errors
c     
            errsum (i+1,1) = errsum (i+1,1) + fdst
            errsum (i+1,2) = errsum (i+1,2) + 1.
         else
            trkerr(i) = '    '
            interr(i+1) = '   '
         endif
      enddo
   
      btlat = abs(blat(idiff))
      ns = 'N'
      if (blat(idiff) .lt. 0.0) ns = 'S'
      btlon = blon(idiff)
      ew = 'W'
      if (btlon .gt. 180.0) then
         ew = 'E'
         btlon = 360.0 - btlon
      endif
      write (8,5000) wdtg,nwrng,btlat,ns,btlon,ew,
     & int(bvmax(idiff)),int(dst),(trkerr(i),i=1,7),
     &  (interr(i),i=1,8),pltfrm
 5000 format(1x,a8,1x,i3,2x,f4.1,a1,1x,f5.1,a1,i4,1x,i4,7(1x,a4),
     &  1x,8(1x,a3),3x,a6)
      write (9,6000) strmid,wdtg,nwrng,btlat,ns,btlon,ew,
     &   int(bvmax(idiff)),int(dst),(trkerr(i),i=1,7),
     &   (interr(i),i=1,8),pltfrm(1:2),pltfrm(3:4),pltfrm(5:6)
 6000 format(a6,a8,i3,f4.1,a1,f5.1,a1,i4,i4,7a4,8a3,3a2)
      goto 100          ! go read another carq or wrng

 9998 continue
cx.....  post-warning track posits to output as requested by JTWC Jun 99 .. sampson
	   do iptrk = idiff+1, nb
              btlat = abs(blat(iptrk))
              ns = 'N'
              if (blat(iptrk) .lt. 0.0) ns = 'S'
              btlon = blon(iptrk)
              ew = 'W'
              if (btlon .gt. 180.0) then
                 ew = 'E'
                 btlon = 360.0 - btlon
              endif
	      prtdtg = bdtg(iptrk)
              write (8,7000)prtdtg,btlat,ns,btlon,ew,int(bvmax(iptrk))
 7000         format(1x,a8,4x,2x,f4.1,a1,1x,f5.1,a1,i4)
	   enddo
cx........end of post-warning track posit code.......................................
c
      call totals (errsum,intsum,intbia)

 9999 continue
      close (4)
      close (5)
      close (6)
      close (17)
      close (8)
      stop

 9021 write (17,'(''Error 9021 in ANNEXA.F - '',
     &  '' bestrack file not found: '',/,2x,a)') btrk
      write (*,'(''ANNEXA.F: bestrack file not found:'',/,2x,a)')btrk
      stop 1
 9031 write (17,'(''Error 9031 in ANNEXA.F - '',
     &  '' adeck file not found: '',/,2x,a)') adec
      write (*,'(''ANNEXA.F: adeck file not found: '',/,2x,a)') adec
      stop 1
 9051 write (17,'(''Error 9051 in ANNEXA.F - '',
     &  '' problem reading init (1=CARQ,2=WRNG): '',/,2x,a)') indat
      write (*,'(''ANNEXA.F: problem with indat (1=CARQ,2=WRNG): ''
     &       ,2x,a)') indat
      stop 1

      end

c-----------------------------------------------------------------------
      subroutine getobjaid (objaid,wdtg,cyyr,itech,jlat,jlon,jwnd,istat)
c
c      Read the rest of the dtg in the a-deck, searching for the
c      obj aid forecast.
c
c  Passed parameters:
c     objaid - the obj aid that the user wishes to run the program for
c     wdtg - the dtg of the CARQ or WRNG, YYMMDDHH
c     cyyr - cyclone number and year
c  Returned parameters:
c     itech - returns 1 if the objaid was found, 0 if not found
c     jlat, jlon, jwnd - obj aid forecast data
c     istat - return 1 for success, 0 for fail
c
c-----------------------------------------------------------------------
c
      INCLUDE  'dataformats.inc'
c
      character objaid*4
      character*8 wdtg,dtg
      character cycnum*2
      character cyyr*4,crdtp*4,strmid*6
      real jlat(7),jlon(7),jwnd(7)
      logical toofar
      integer istat, ii, itau, iresult, itech
      type (AID_DATA) aidRcd
      type (A_RECORD) aRecord

      itech = 0
      istat = 1
      crdtp = '    '
      toofar = .false.
      do while (crdtp .ne. objaid .and. .not. toofar .and. istat .eq. 1)
         call readARecord( 3, aidRcd, istat )
         if( istat .eq. 1 ) then
            crdtp = aidRcd%aRecord(1)%tech
cx  watch for objaids 3 characters, if first is missing then move over
	    if (crdtp(1:1).eq.' ') then
		    crdtp(1:3) = crdtp(2:4)
		    crdtp(4:4) = ' '
            endif
cx  watch for objaids 2 characters, if first is missing then move over again
	    if (crdtp(1:1).eq.' ') then
		    crdtp(1:2) = crdtp(2:3)
		    crdtp(3:4) = ' '
            endif
            dtg = aidRcd%aRecord(1)%DTG(3:10)
            write( cycnum, '(i2)' ) aidRcd%aRecord(1)%cyNum
            if( cycnum(1:1) .eq. ' ' ) cycnum(1:1) = '0'
            strmid = aidRcd%aRecord(1)%basin//cycnum//
     &           aidRcd%aRecord(1)%DTG(3:4)
c           check for new dtg or new cyclone number (new storm)
            if (dtg .gt. wdtg .or. strmid(3:4) .ne. cyyr(1:2)) then
               do ii=1,aidRcd%numrcrds
                  backspace 3
               enddo
               toofar = .true.
            endif
         endif
      enddo

      do ii=1,7
         jlat(ii) = 0.0
         jlon(ii) = 0.0
         jwnd(ii) = 0.0
      enddo

      if( crdtp .eq. objaid ) then
         do ii=1,7
            if( ii .lt. 5 ) then
               itau = ii*12
            else if( ii .eq. 5 ) then
               itau = 72
            else if( ii .eq. 6 ) then
               itau = 96
            else if( ii .eq. 7 ) then
               itau = 120
            endif
            call getAidTAU( aidRcd, itau, aRecord, iresult )
            if( iresult .eq. 1 ) then
               jlat(ii) = aRecord%lat
               if( aRecord%NS .eq. 'S' ) jlat(ii) = -jlat(ii)
               jlon(ii) = aRecord%lon
               if( aRecord%EW .eq. 'E' ) jlon(ii) = 360.0 - jlon(ii)
               jwnd(ii) = aRecord%vmax
            endif
         enddo
         itech = 1
      endif
      end

c-----------------------------------------------------------------------
      subroutine getacarq (strmid,cyyr,initaid,endcarqs,aidRcd,istat)
c
c  Loop until a carq or wrng card is read. 
c
c  Passed parameters:
c     cyyr - cyclone number and year
c     initaid - 'CARQ' or 'WRNG'
c  Returned parameters:
c     strmid - stormid, eg wp0198
c     endcarqs - flags a read of an aid record for another storm
c     aidRcd - the carq or wrng data
c     istat - return 1 for success, 0 for fail
c
c-----------------------------------------------------------------------
c
      INCLUDE  'dataformats.inc'
c
      character cycnum*2
      character cyyr*4,crdtp*4,strmid*6
      character initaid*4
      integer istat, ii
      logical endcarqs, found
      type (AID_DATA) aidRcd
c
c      loop until a carq or wrng card is read. 
c
      endcarqs = .false.
      found = .false.
      istat = 1
      do while (.not. found .and. .not. endcarqs .and. istat .eq. 1)   
         call readARecord( 3, aidRcd, istat )
         if( istat .eq. 1 ) then
            crdtp = aidRcd%aRecord(1)%tech
            write( cycnum, '(i2)' ) aidRcd%aRecord(1)%cyNum
            if( cycnum(1:1) .eq. ' ' ) cycnum(1:1) = '0'
            strmid = aidRcd%aRecord(1)%basin//cycnum//
     &           aidRcd%aRecord(1)%DTG(3:4)
c
c           check for different storm number
            if (strmid(3:4) .ne. cyyr(1:2)) then
               do ii=1,aidRcd%numrcrds
                  backspace 3
               enddo
               endcarqs = .true.
            endif
c     if record read is a carq or wrng then found is true and fall
c     out of loop.
            if (crdtp .eq. initaid) found = .true.
         endif
      enddo
cx   finally, adjust the storm year for sh storms ... sampson nrl, June 99
cx   should actually be passed to annexa routine instead of this way.
      if (strmid(1:2) .eq. 'SH') then
          read (aidRcd%aRecord(1)%DTG,'(i4,i2)',err = 999) iyear, imonth
	  if (imonth.gt.6) then
	     newyear = mod((iyear+1),100)
	     write (strmid(5:6),'(i2.2)') newyear
          endif
      endif
      return
  999 continue
      print *, "Error extracting year out of stormid=",stormid
      return
      end

c-----------------------------------------------------------------------
      subroutine readastorm (bdtg,cyyr,nb,endb,blat,blon,bvmax)
c
c  Read one storm from the best track file
c
c  Passed parameters:
c       none
c  Returned parameters:
c       bdtg - best track dtg, YYMMDDHH
c       cyyr - cyclone number and year
c       nb - number of best track positions read
c       endb - end-of-file flag
c       blat, blon and bvmax arrays - best track data
c
c-----------------------------------------------------------------------
c
      character*8 bdtg(200)
      character*8 btrkdtg
      character basin*2, cycnum*2
      character cent*2
      character cyyr*4,ns*1,ew*1
      real blat(200),blon(200),bvmax(200)
      real btlat, btlon
      logical endb,samestorm
      integer iwind, ios, nb
c
c  read one storm from the best track file
c
      
      do i=1,200
         blat(i) = 0.0
         blon(i) = 0.0
         bvmax(i) = 0.0
      enddo

      nb = 1
      samestorm = .true.
      ios = 0
      do while (ios .eq. 0 .and. samestorm)   ! do while not end-of-file
         call readBest( 2, basin, cycnum, cent, btrkdtg, btlat, ns, 
     &        btlon, ew, iwind, ios )
         if( ios .eq. 0 ) then  ! if not end-of-file
            if (nb .eq. 1) then
               cyyr = cycnum//btrkdtg(1:2)
               write (8,'(1x)')
            endif
            if (cycnum .eq. cyyr(1:2)) then  ! check for same cycnum
               bdtg(nb) = btrkdtg
               blat(nb) = btlat
               blon(nb) = btlon
               bvmax(nb) = iwind
               if (ns .eq. 's' .or. ns .eq. 'S') blat(nb) = -blat(nb)
               if (ew .eq. 'e' .or. ew .eq. 'E') 
     &             blon(nb) = 360. - blon(nb)
               nb = nb + 1
            else
               backspace (2)
               samestorm = .false.
            endif
         endif
      enddo
      if( ios .ne. 0 ) endb = .true.
      nb = nb - 1
      end

c-----------------------------------------------------------------------
      subroutine totals (errsum,intsum,intbia)
c-----------------------------------------------------------------------
c
      real errsum (8,2), intsum(8), intbia(8)
      character sumout(8,2)*5, intout(8)*5, intbout(8)*5
c
c  write the totals
c
cx    print *,'in totals'
      do i=1,8
         if (errsum (i,2) .ne. 0.0) then 
            errsum (i,1) = errsum (i,1)/errsum(i,2)
cx          write (sumout(i,1),'(i5)') int(errsum(i,1) + 0.5)
cx          write (sumout(i,2),'(i5)') int(errsum(i,2))
            write (sumout(i,1),'(i5)') nint(errsum(i,1))
            write (sumout(i,2),'(i5)') nint(errsum(i,2))
            intsum(i) = intsum(i) / errsum(i,2)
            intbia(i) = intbia(i) / errsum(i,2)
            write (intout(i), '(i3)') nint(intsum(i))
            write (intbout(i),'(i3)') nint(intbia(i))
         else
            sumout(i,1) = '     '
            sumout(i,2) = '     '
            intout(i) = '   '
            intbout(i) = '   '
         endif
      enddo
      write (8,6500) (sumout(i,1),i=1,8), (intout(i),i=1,8)
 6500 format (/22x,'AVERAGE  ',8a5,t74,8(a3,1x))
      write (8,6550) (intbout(i),i=1,8)
 6550 format (22x,'BIAS     ',t74,8(a3,1x))
      write (8,6600) (sumout(i,2),i=1,8), (sumout(i,2)(3:5),i=1,8)
 6600 format (22x,'# CASES  ',8a5,t74,8(a3,1x))
      return
      end
