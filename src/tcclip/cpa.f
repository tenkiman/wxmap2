      program cpa
c
c  this program computes the cpa from a lat,lon location to the forecast
c  track.  the user can enter a specific location, a lat/lon, or just ask 
c  for all entries.
c
c  command line input:
c                    arg1=storm id
c                    arg2=units
c                             1=nm
c                             2=mi
c                             3=km
c                    arg3=maximum tau, either 72 or 120
c                    arg4=location preference
c                             1=all locations
c                             2=location name
c                             3=location lat/lon
c                    arg5=max cpa distance or location name or latitude
c                    arg6=longitude (used only if line2=3)
c
c  files: 
c                    unit44: locations
c                    unit55: bstrk file
c                    unit66: forecast track file
c                    unit77: output file - cpa data
c                    unit88: output file - cpa data in label format
c
c  variables:
c
c  original programmer:  unknown
c  current programmer:   sampson, nrl  
c  
c
c  change record:
c                  converted to ATCF 3.0     sampson, nrl Nov 95
c    modified to read new *.fst file format  schrader, saic 12/98
c    modified cpa.out output file to print 3 digit tau  schrader, saic  12/98
c
      common /bestc/ hlat(1201),hlng(1201),n,idif,maxtau
      common /bstchr/ dtgb
      dimension alat(200),alon(200),name(200)
      character*30 name,request,name1
      character*100  storms,incdir,filename
      character*10 lat,lon
      character*8 dtg,dtgb
      character*8 strmid,max
      character*4 units
      character*2 units1
      character*1 nsew,answer,ns,ew
      logical ynchck
      integer iarg

      data iunit,junit /77,88/
c
c
cx    open(3,file='cpa.in',status='old',err=900)
      call getenv("ATCFINC",incdir)
      ind=index(incdir," ")-1
      write(filename,'(a,a)')incdir(1:ind),"/cpa.loc"
      open(44,file=filename,status='old',err=900)
      call getenv("ATCFSTRMS",storms)
      ind=index(storms," ")-1
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
      write(filename,'(a,a,a,a)')storms(1:ind),"/b",strmid,".dat"
      open(55,file=filename,status='old',err=910)
      write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".fst"

      call openfile( 66, filename, 'unknown', ioerror )
      if( ioerror .lt. 0 ) goto 920

cx    open(5,file=storms(1:ind)//"/b"//strmid//".dat",status='old',err=910)
cx    open(6,file=storms(1:ind)//"/"//strmid//".fst",status='old',err=920)

cx  open the two output files
      call openfile( iunit, 'cpa.out', 'unknown', ioerror )
      if( ioerror .lt. 0 ) goto 930
      write(filename,'(a,a,a,a)')storms(1:ind),"/",strmid,".cpa"
      call openfile( junit, filename, 'unknown', ioerror )
      if( ioerror .lt. 0 ) goto 940

      call upcase (strmid,6)

c
c  read maximum tau, either 72 or 120
c
      call getarg (iarg, max)
      iarg = iarg + 1
      read(max,'(i3)',err=945)maxtau

c
c  read the initial and forecast positions and then 
c  interpolate them to hourly posits
c
      call readtrk 
      close (55)
      close (66)
c
c  load the locations into arrays
c
      nloc = 1
  100 continue
cajs      read (44,'(f5.1,a1,f6.1,a1,1x,a20)',end=200) alat(nloc),ns,
cajs     &    alon(nloc),ew,name(nloc)
      ios = 0
      call readcpaloc( alat(nloc),ns,alon(nloc),ew,name(nloc),ios )
      if( ios .lt. 0 ) goto 200
      if (ns .eq. 'S') alat(nloc) = -alat(nloc)
      if (ew .eq. 'E') alon(nloc) = 360.0 - alon(nloc)
      nloc = nloc + 1
      goto 100
  200 continue
      nloc = nloc - 1
      write (iunit,'(//25x,''Forecast Track CPAs for '',a8)') 
     &     strmid
cx
cx   capability to choose units (nm, st mi, km) crs 6/11/92
cx
cx    read (3,*,err=945) ians
      call getarg (iarg, answer)
      iarg = iarg + 1
      read(answer,'(i1)',err=945)ians
      if (ians .lt. 1 .or. ians .gt. 4)then
          go to 800
      elseif (ians .eq.1)then
        convrsn=1.0
        units='(nm)'
        units1='NM'
      elseif (ians .eq.2)then
        convrsn=1.151
        units='(mi)'
        units1='MI'
      elseif (ians .eq.3)then
        convrsn=1.852
        units='(km)'
        units1='KM'
      elseif (ians .eq.4)then
        go to 800
      endif

      write (junit,'(''CPA TO:               '',
     1                 a2,''     DTG'')') units1

c
c  main loop.  user can request all locations, one location, or lat/lon
c
      call getarg (iarg, answer)
      iarg = iarg + 1
      read(answer,'(i1)',err=945)ians
cx    read (3,*,err=942) ians
      if (ians .lt. 1 .or. ians .gt. 4) goto 800

      goto (300,400,500,800) ians
c
c  loop thru each location in the location file 
c
  300 continue
      call getarg (iarg, max)
      iarg = iarg + 1
cx    read (3,'(a)',err=950) max
      if (max .eq. '      ') then
         cpamax = 999999.
      else
         read (max,'(f6.0)') cpamax
      endif

      write (iunit,1000) strmid,dtgb
      write (iunit,1100)
cx  crs 6/15/92
      write (iunit,'(52x,a4,/)')units
      do 350 i=1,nloc
      call calcpa (alat(i),alon(i),dir,dst,ihr)
cx  dst must be in desired units to compare with cpamax   crs 6/15/92
      if (dst*convrsn .gt. cpamax) goto 350
      call icrdtg (dtgb,dtg,ihr)
      olat = alat(i)
      ns = 'N'
      if (olat .lt. 0.0) then
         olat = -olat
         ns = 'S'
      endif
      olon = alon(i)
      ew = 'W'
      if (olon .gt. 180.0) then
         olon = 360.0 - olon
         ew = 'E'
      endif
      write (iunit,1200) name(i),olat,ns,olon,ew,int(dir),
     &  int(dst*convrsn),dtg,ihr
      write (junit,1300) name(i),int(dst*convrsn),dtg(5:6),dtg(7:8)
  350 continue
      goto 800
c
c  the location name
c
  400 continue
      call getarg (iarg, request)
      iarg = iarg + 1
cx    read (3,'(a30)',err=960) request

c  make the request all upper case

      call upcase (request,30)

c  check request against all locations in the file

      do 420 i=1,nloc
      name1 = name(i)
      call upcase (name1,30)
      if (request .eq. name1) goto 430
  420 continue
      goto 945

  430 continue
      write (iunit,1000) strmid,dtgb
      write (iunit,1100)
cx  crs 6/15/92
      write (iunit,'(52x,a4,/)')units
      call calcpa (alat(i),alon(i),dir,dst,ihr)
      call icrdtg (dtgb,dtg,ihr)
      olat = alat(i)
      ns = 'N'
      if (olat .lt. 0.0) then
         olat = -olat
         ns = 'S'
      endif
      olon = alon(i)
      ew = 'W'
      if (olon .gt. 180.0) then
         olon = 360.0 - olon
         ew = 'E'
      endif
      write (iunit,1200) name(i),olat,ns,olon,ew,int(dir),
     &      int(dst*convrsn),dtg,ihr
      write (junit,1300) name(i),int(dst*convrsn),dtg(5:6),dtg(7:8)

      go to 800

  500 continue
      call getarg (iarg, lat)
      iarg = iarg + 1
cx    read (3,'(a)',err=970) lat
      call decdll (lat,rlat,nsew)
      if (lcheck(nsew) .ne. 1) then
         go to 972
      endif
      if (nsew .eq. 's' .or. nsew .eq. 'S') rlat = -rlat

      call getarg (iarg, lon)
      iarg = iarg + 1
cx    read (3,'(a)',err=970) lon
      call decdll (lon,rlon,nsew)
      if (lcheck(nsew) .ne. 2) then
         go to 973
      endif
      if (nsew .eq. 'E' .or. nsew .eq. 'e') rlon = 360.0 - rlon

      request = 'REQUESTED POSITION'
      write (iunit,1000) strmid,dtgb
      write (iunit,1100)
cx  crs 6/15/92
      write (iunit,'(52x,a4,/)')units
      call calcpa (rlat,rlon,dir,dst,ihr)
      call icrdtg (dtgb,dtg,ihr)
      olat = rlat
      ns = 'N'
      if (olat .lt. 0.0) then
         olat = -olat
         ns = 'S'
      endif
      olon = rlon
      ew = 'W'
      if (olon .gt. 180.0) then
         olon = 360.0 - olon
         ew = 'E'
      endif
      write (iunit,1200) request,olat,ns,olon,ew,int(dir),
     &    int(dst*convrsn),dtg,ihr
      write (junit,1300) request(1:20),int(dst*convrsn),
     &    dtg(5:6),dtg(7:8)

  800 continue
      close (iunit)
      close (junit)
      stop
c
  900 stop ' error opening location file'
  910 stop ' error opening best track file'
  920 stop ' error opening forecast file'
  930 stop ' error cpa.out'
  940 stop ' error cpa output (??????.cpa)'
  942 stop ' error units data'
  945 stop ' error in option data'
  950 stop ' error in distance data'
  955 stop ' location not found'
  960 stop ' error in location data'
  970 stop ' error in lat/lon data'
  972 stop ' error in lat data'
  973 stop ' error in lon data'
c
 1000 format (//' CPA''s for storm ',a8,' at ',a8)
 1100 format (//' Location',22x,'  Lat   Long    Dir  Dist     Time',
     &    '      Tau')
 1200 format (1x,a30,2(f5.1,a1,1x),2x,i3.3,2x,i4,3x,a8,4x,i3.3)
c1200 format (1x,a30,2x,i3.3,2x,i4,3x,a8,4x,i2.2)
 1300 format (a20,i5,2x,a2,'/',a2,'Z')
c
      end
c
c  ****************************************************************
c
      subroutine calcpa (alat,alng,dir,dst,ihr)
      common /bestc/ hlat(1201),hlng(1201),n,idif,maxtau
c
c  subroutine to calculate the direction and distance of the cpa
c
      small=9999.
      do 200 j=1,idif
      dir=0.
      call dirdst(alat,alng,hlat(j),hlng(j),dir,dis) 
      if(dis.gt.small) go to 200
      small=dis
      j1=j
200   continue

      dir=1.
      call dirdst(alat,alng,hlat(j1),hlng(j1),dir,dis)
      dir=amod(dir,360.)
      dst = dis
      ihr = j1 - 1
      return
      end
c
c  ****************************************************************
c
      subroutine readtrk 
c
      INCLUDE  'dataformats.inc'
c
      common /bestc/ hlat(1201),hlng(1201),n,idif,maxtau
      common /bstchr/ dtgb
      dimension x(200),flat(200),flng(200)
      character fnam*11, l*1, g*1, dtgb*8
      character*2 century
      logical exst
      integer ii
      integer istat
      integer isavtau
      integer ibtwind, ios
      type (AID_DATA) fstRcd
c
c  this routine reads and interpolates the bstrk lat,lng to hourly
c  posits.
c               flat,flng  - current and forecast lat,long
c               hlat,hlng  - 1-hourly lat/long
c               idif       - number of hourly positions
c               maxtau     - maximum tau for cpa, either 72 or 120
c
c  reading bstrk file 
c
c150   continue
c      read  (55,'(2X,A8,F4.1,A1,F4.1,A1,F4.0)',end=200) 
c     &    dtgb,flat(1),l,flng(1),g
c  Changed this read to use the new besttrack data format, ajs  4/8/98
c      read  (55,'(10X,A8,16X,F4.1,A1,2X,F4.1,A1)',end=200) 
c     &    dtgb,flat(1),l,flng(1),g
c      go to 150
c  Changed this read to use the readBT routine to access the data
      ios = 0
      do while ( ios .eq. 0 )
         call readBT( 55,century,dtgb,flat(1),l,flng(1),g,ibtwind,ios )
      enddo
200   if(l .eq. 'S') flat(1) = -flat(1)
      if(g .eq. 'E') flng(1) = 360. - flng(1)
      x(1) = 0.0
c
c  read the forecast file
c
      n = 2
cajs  210 continue
cajs      read (66,'(16x,f3.0,4x,2f5.1)',end=300) x(n),flat(n),flng(n)
cajs  Read one AID_DATA record from forecast file, which happens to be
cajs  the whole file.
      call readARecord( 66, fstRcd, istat )
      isavtau = -1
      do ii=1, fstRcd%numrcrds
         if( (fstRcd%aRecord(ii)%tau .ne. 0) .and.
     &        (isavtau .ne. fstRcd%aRecord(ii)%tau) .and.
     &        (fstRcd%aRecord(ii)%tau .le. maxtau) ) then
            x(n) = fstRcd%aRecord(ii)%tau
            flat(n) = fstRcd%aRecord(ii)%lat
            if( fstRcd%aRecord(ii)%NS .eq. 'S' ) 
     &           flat(n) = -flat(n)
            flng(n) = fstRcd%aRecord(ii)%lon
            if( fstRcd%aRecord(ii)%EW .eq. 'E' ) 
     &           flng(n) = 360.0 - flng(n)
            n = n + 1
            isavtau = fstRcd%aRecord(ii)%tau
         endif
      enddo

cx  ATCF 3.0 fst files
cx  appear to have eastern longitudes 0-180, western 180-360
cajs      if(flng(n).gt.0.) flng(n) = 360. - flng(n)
cajs      if(flng(n).lt.0.) flng(n) = abs(flng(n))
cajs      n = n + 1
cajs      goto 210
c
c  interpolate the track to hourly positions
c
  300 continue
      n = n - 1
      call hour(x,flat,hlat,n)
      call hour(x,flng,hlng,n)
      idif = x(n) + 1
c
      return
      end
c
c  ****************************************************************
c
      subroutine readcpaloc (alat,ns,alon,ew,name,ios)
c
c  Subroutine to read in lines from the cpa.loc file.  This subroutine
c  is replacing the following read statement:
c      read (44,'(f5.1,a1,f6.1,a1,1x,a20)',end=200) alat(nloc),ns,
c     &    alon(nloc),ew,name(nloc)
c  This subroutine is necessary because tabs in the data cause the
c  above read statement to fail.
c  Note special compile flags are needed for this code.
c  The '\t' requires the +B compile option.  The '(<i+1>x,a20)'
c  requires the +E6 compile option.
c
      real         alat, alon
      integer      ios
      integer      i, isavi, j, idx
      character    cline*50
      character    aStr*10
      character*1  ns,ew
      character*30 name
c
c     Read the line into a character string and 
c     replace any tabs with spaces.       
      read (44,'(a50)',iostat=ios) cline
      if( ios .lt. 0 ) return
      do i=1, 50
         if( cline(i:i) .eq. '\t' ) cline(i:i) = ' '
      enddo
c
c     Acquire all characters until encounter N, n, S, or s.
c     That should be alat and the next character should be ns.
      aStr = '          '
      do i=1, 10
         if( cline(i:i) .ne. 'N' .and. cline(i:i) .ne. 'n' .and.
     &       cline(i:i) .ne. 'S' .and. cline(i:i) .ne. 's' ) then
            aStr(i:i) = cline(i:i)
         else
            exit
         endif
      enddo
      isavi = i + 1
      read( aStr, * ) alat
      ns = cline(i:i)
c
c     Acquire all characters until encounter E, e, W, or w.
c     That should be alon and the next character should be ew.
      aStr = '          '
      j = 1
      do i=isavi, isavi+10
         if( cline(i:i) .ne. 'E' .and. cline(i:i) .ne. 'e' .and.
     &       cline(i:i) .ne. 'W' .and. cline(i:i) .ne. 'w' ) then
            aStr(j:j) = cline(i:i)
            j = j + 1
         else
            exit
         endif
      enddo
      isavi = i + 2
      read( aStr, * ) alon
      ew = cline(i:i)
c
c     Read the next 20 characters into name
cajs      read( cline, '(<i+1>x,a20)' ) name  
cajs      /* The above is an f77 portability extension  */
      name = '                              '
      j = 1
      do idx=isavi, isavi+20
         name(j:j) = cline(idx:idx)
         j = j + 1
      enddo
c
      return
      end

