      subroutine trackem (ddfld,fffld,
     $     igrdx,jgrdy,
     $     blat,blon,dlat,dlon,
     $     ktau,dtau,gdat,numv,
     &     mxhr,maxtc,nbog,maxfix,ntrk,iunit,
     $     verb)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)trackem.f	1.2 8/1/95
C                        16:16:19 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  trackem
C
C  DESCRIPTION:  driver to track tropical cyclones
C
C  COPYRIGHT:                  (C) 1994 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  none
C
C  CLASSIFICATION:  unclassified
C
C  RESTRICTIONS:  none
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  Cray UNICOS
C
C  LIBRARIES OF RESIDENCE:
C
C  USAGE:  call trackem (ddfld,fffld,igrdx,jgrdy,ktau,gdat,numv,
C                        mxhr,nbog,ntrk)
C
C  PARAMETERS:
C     NAME       TYPE     USAGE           DESCRIPTION
C   --------    ------    ------    ------------------------------
C    ddfld       real       in      wind direction field, deg
C    fffld       real       in      wind speed squared, (m/s)**2
C     igrdx        int       in      first  dimension of ddfld
C     jgrdy        int       in      second dimension of ddfld
C     ktau        int       in      forecast period index
C     gdat       real     in/out    bogus data in real form / new
C                                   position data
C    numv         int       in      first dimension of gdat, number of
C                                   variables
C    mxhr         int       in      second dimension of gdat, maximum
C                                   number of forecast periods
C    nbog         int       in      third diemsnsion of gdat, number of
C                                   valid bogus positions to track
C    ntrk         int       out     number of cyclones being tracked
C
C  COMMON BLOCKS:  none
C
C  FILES:  none
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C
C
C
C
C  ADDITIONAL COMMENTS:
C         contents of gdat array
C           (1,n,m) - latitude of cyclone m, +NH -SH
C           (2,n,m) - longitude of cyclone m, 0 - 360 E
C           (3,n,m) - x-grid (lon) of cyclone m
C           (4,n,m) - y-grid (lat) of cyclone m
C           (5,n,m) - heading  from last location of cyclone m, deg
C           (6,n,m) - distance from last location of cyclone m, nm
C           (7,n,m) - confidence factor of location of cyclone m
C                        0 - cyclone lost or not rated
C                        1 - excellant
C                        2 - good
C                        3 - fair
C                        4 - poor
C                        5 - poorer
C                        6 - poorest
C           (8,n,m) - cyclonic wind support, 3 or 4
C           (9,n,m) - intersection support, 2 - 9
C
C           note: n goes from 0 to mxhr,  0   is bogus position
C                                         1   analysis position
C           forecast period = (n-1)*dtau  2   6-hr forecast period
C                                         3  12-hr forecast period
C                                        --  - - - - - - - - - - -
C                                        25 144-hr forecast period
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         chkfcir     locate initial potential areas for cyclones
C         clltxy      convert lat,lon to x,y grid location
C         cxytll      convert x,y grid location to lat,lon
C         fndcyc      driver routine for finding which cyclone to locate
C         selcyc      select best cyclone for each one being tracked
C         rcalhdst    calculate heading and distance from old lat,lon to
C                     new lat,lon
C         rcalltln    calculate new lat,lon, given old lat, lon, heading
C                     and distance
C         verify      locate cyclones based upon isogons
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          cirdat    real       array of cyclone values
C                                 (1 - x-grid location
C                                 (2 - y-grid location
C                                 (3 - quadrant wind support
C                                 (4 - final intersection count
C          clat      real       cyclone latitude, deg (+NH, -SH)
C          clon      real       cyclone longitude, deg (0 - 360E)
C          dist      real       distance traveled between taus (nm)
C          egxx      real       estimated grid location, first dimension
C          egyy      real       estimated grid location, second dimension
C          elat      real       estimated future latitude (degrees)
C          flon      real       estimated future longitude (degrees)
C          head      real       cyclone heading between taus, (degrees)
C          ierr       int       error flag, 0 no error
C          iloc       int       cyclone location flag, 0 not found
C          indx       int       index to selected cyclone data in cirdat
C          kc         int       present second index to gdat
C          kcl        int       last second index to gdat
C          kint       int       count of intersections used to produce location
C          konf       int       confidence factor of selected cyclone
C          ltrk       int       last number of cyclones being tracked
C          maxptc     int       maximum number of prospective cyclones
C                               to process
C          mbd        int       minimum/maximum boundary of search window
C          mni        int       minimum first dimension of search window
C          mnj        int       minimum second dimension of search window
C          mxi        int       maximum first dimension of search window
C          mxj        int       maximum second dimension of search window
C          mxptc      int       working number of maximum allowed
C                               prospective cyclones to process
C          nccf       int       number of closed circulations found
C          ndup       int       duplicate cyclone indicator
C          nhsh       int       north/south hemisphere indicator
C          sgxx      real       starting grid location, first dimension
C          sgyy      real       starting grid location, second dimension
C          slat      real       starting latitude, deg
C          slon      real       starting longitude, deg
C          xc        real       x-grid location of cyclone
C          yc        real       y-grid location of cyclone
C
C  METHOD:
C
C  INCLUDE FILES:  none
C
C  COMPILER DEPENDENCIES:  Fortran 77
C
C  COMPILE OPTIONS:
C
C  MAKEFILE:
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
C    Make changes for the use of wind speed field, fffld, and allow for up to
C    four centers of intersections to be found for each prospective area
C    selected for a cyclone search.
C
C...................END PROLOGUE.......................................
C

      use mfutils

      integer maxptc
      parameter (maxptc = 27)


c         formal parameters:

      integer numv, mxhr, maxtc, nbog, ktau, ntrk, dtau

      integer igrdx,jgrdy
      real blat,blon,dlat,dlon

      real*4 ddfld(igrdx,jgrdy), fffld(igrdx,jgrdy)
      real*4 gdat(numv,0:mxhr,maxtc,0:maxfix)

c         local variables

      integer n, j, iloc, kc, kcl, nhsh, ierr, ltrk, ndup, indx
      integer mni, mxi, mnj, mxj, mxptc, nccf, konf, kint, mbd
      integer mbdmin,mbdmax

      integer iunit

      real cirdat(4,maxptc), slat, slon, sgxx, sgyy, head, dist
      real flat, flon, egxx, egyy, xc, yc, clat, clon

      character*24 qtitle
      logical verb

      verb=.false.
ccc      verb=.true.

      if(verb) then
        qtitle='ddfld                  '
        call qprntn(ddfld,qtitle,1,1,igrdx,jgrdy,10,6)
        qtitle='fffld                  '
        call qprntn(fffld,qtitle,1,1,igrdx,jgrdy,10,6)
      endif

      iunit=33
      if(verb) iunit=6

      mxptc = maxptc
      ntrk  = 0
      kc    = 1+ktau/dtau
      kcl   = kc-1

      do n=1,nbog

        iloc=0

C......................................................................         
C         
C         only track if previous position exists and
C         the track was not done by vorticity (by mftrack_backup)
C
C......................................................................
C
        itestvort=gdat(7,kcl,n,0)

c--       why?  try to get sfc wind fix anyway
c
        itestvort=1

        if(verb) then
          print*,'TRACKEM n,gdat(1,kcl,n,0),itestvort ',
     $         n,gdat(1,kcl,n,0),itestvort
        endif

        if ( (abs(gdat(1,kcl,n,0)).lt.90.0)
     $       .and.
     $       (itestvort.ge.0) ) then
c
c                   last position is valid, so calculate extrapolated
c                   location for tracking
c
          slat = gdat(1,kcl,n,0)
          slon = gdat(2,kcl,n,0)
          sgxx = gdat(3,kcl,n,0)
          sgyy = gdat(4,kcl,n,0)
          head = gdat(5,kcl,n,0)
          dist = gdat(6,kcl,n,0)


          if(verb) then
            write(*,'(a)') ' '
            write(*,'(a)') 'sssssssssssssssssssssssssssssssssssssssss'
            write(*,'(a)') ' '
            write(*,'(a,2x,2(f7.2,1x),2x,2(i3,1x))') 
     $           'IIIII    slat,slon,kcl,n  ',slat,slon,kcl,n
            write(*,'(a,2x,4(f7.2,1x))') 
     $           'IIIII sgxx,sgyy,head,dist ',sgxx,sgyy,head,dist
          endif

c         use rhumb line in calculations of flat,flon

          call rcaltln (slat,slon,head,dist,flat,flon)


Cmf 20000824 - use initial position vice interpolated for tau = 0         
C         
            if((slat.lt.90.).and.(slon.lt.900).and.ktau.eq.0) then
              flat=slat
              flon=slon
            endif

c         convert to grid co-ordinates

CCCCC     call clltxy (flat,flon,egxx,egyy,ierr)

          call clltxy (flat,flon,
     $         blat,blon,dlat,dlon,igrdx,jgrdy,
     $         egxx,egyy,
     $         ierr)


          if (ierr .eq. 0) then

            if (slat .gt. 0) then
              nhsh =  1
            else
              nhsh = -1
            endif

c--       change search box depending on grid dx -- assumes dlon=dlat

            mbdmin=int((1.0/dlon)+0.0001)*2 + 1
            mbdmax=int((1.0/dlon)+0.0001)*4 + 1
c
c                   set window dimensions for searching for cyclonic
c                   circulations within ddfld
c         
            mni = amin1 (sgxx,egxx)
            mxi = 1.0 +amax1 (sgxx,egxx)
            mbd = (mxi -mni)/2

C!!!!!!!!!!!!!!!                   set minimum and max boundary

            if (mbd.lt.mbdmin) then
              mbd = mbdmin
            elseif (mbd.gt.mbdmax) then
              mbd = mbdmax
            endif
cccc      mbd=5

c         set min and max x-grid window

            mni = mni-mbd
            mxi = mxi+mbd

c         repeat for y-grid window

            mnj = amin1  (sgyy,egyy)
            mxj = 1.0 +amax1 (sgyy,egyy)
            mbd = (mxj -mnj)/2

            if (mbd .lt. mbdmin) then
              mbd = mbdmin
            elseif (mbd .gt. mbdmax) then
              mbd = mbdmax
            endif

c--       disable these checks -- based on 1deg global data
c--           if (nhsh .ge. 0) mnj = max0 (mnj, (jgrdy +1)/2)

            mnj = mnj - mbd
            if(mnj.lt.1) mnj=1

            mxj = mxj + mbd
            if(mxj.gt.jgrdy) mxj=jgrdy

c--            if (nhsh .lt. 0) mxj = min0 (mxj, (jgrdy +1)/2)


c
c                   locate cyclonic circulation(s) within window
c
            call chkfcir (ddfld,fffld,igrdx,jgrdy,
     $           mni,mxi,mnj,mxj,nhsh,mxptc,
     $           cirdat,nccf)

            write(iunit,*) 'CHKFCIR found ',nccf,' possible cyclonic',
     $           ' centers'
c
c                   verify that all prospective cc's are wind centers
c
            call verify (nhsh,ddfld,igrdx,jgrdy,mxptc,cirdat,nccf,iunit)
            write(iunit,'(a,2x,i2,2x,a)')
     $           'VERIFY  found',nccf,'valid centers'

            if (nccf .gt. 1) then
c
c                   select best cyclonic center for cyclone
c
              call selcyc (sgxx,sgyy,egxx,egyy,
     $             igrdx,jgrdy,
     $             blat,blon,dlat,dlon,
     $             cirdat,nccf,fffld,igrdx,
     &             jgrdy,konf,indx)

            elseif (nccf .eq. 1) then
              konf = 1
              indx = 1
            else
              indx = 0
            endif
            if (indx .gt. 0) then
              xc   = cirdat(1,indx)
              yc   = cirdat(2,indx)
              iloc = nint (cirdat(3,indx))
              kint = nint (cirdat(4,indx))
            else
              iloc = 0
            endif
            if (iloc .gt. 0) then
c
c                   cyclone found, convert grid co-ordinates to lat,lon
c
              write (iunit,*) 'TRACKEM, center found at ',xc,'  ',yc
              if (konf .ne. 1) then
c
c                   check for duplicate positions
c
                j    = 0
                ndup = 0
                do while (j.lt.n-1 .and. ndup.eq.0)
                  j = j +1
                  if (abs (gdat(1,kc,j,0)) .lt. 90.0) then
c                         valid values for comparision
                    if (abs (gdat(3,kc,j,0) -xc) .le. 1.0) then
                      if (abs (gdat(4,kc,j,0) -yc) .le. 1.0) then
c                               duplicate found
                        ndup = -1
                      endif
                    endif
                  endif
                enddo
                if (ndup .ne. 0) then
c
c                           duplicate found from above
c
                  write (iunit,*) ' trackem, duplicate position found!!!'
                  if (nint (gdat(7,kc,j,0)) .lt. konf) then
c                         this will drop this new position
                    iloc = 0
                  elseif (nint (gdat(7,kc,j,0)) .gt. konf) then
c                         replace old position with missing values
                    gdat(1,kc,j,0) =  99.9
                    gdat(2,kc,j,0) = 999.9
                    gdat(3,kc,j,0) = -99.9
                    gdat(4,kc,j,0) = -99.9
                    gdat(5,kc,j,0) = 999.99
                    gdat(6,kc,j,0) =  99.99*dtau
                    gdat(7,kc,j,0) =   0.0
                    gdat(8,kc,j,0) =   0.0
                    gdat(9,kc,j,0) =   0.0
                    ntrk         = ntrk -1
                  else
                    write (iunit,*) ' trackem, duplicate position not ',
     &                           'resolved'
                  endif
                endif
              endif
              if (iloc .gt. 0) then
c                     obtain latitude and longitude
cccccccccccccccccc                call cxytll (xc,yc,clat,clon,ierr)

                call cxytll (xc,yc,
     $               blat,blon,dlat,dlon,igrdx,jgrdy,
     $               clat,clon,
     $               ierr)


                if (ierr .eq. 0) then
c                     sum cyclones to be tracked next
                  ntrk = ntrk +1
                else
c                     bad conversion, so indicate cyclone not found
c                           (this should not happen)
                  iloc = 0
                  write (iunit,*) 'BAD CONVERSION for ',xc,'  ',yc
                endif
              endif
            endif
          endif
        else
          mni = -1
          mxi =  0
          mnj = -1
          mxj =  0
        endif

        if (iloc .eq. 0) then
c
c                   cyclone not found, so set values to missing
c
          clat =  99.9
          clon = 999.9
          xc   = -99.9
          yc   = -99.9
          write (iunit,*) 'NO CYCLONE ',mni,' to ',mxi,' fm ',mnj,' to ',
     &                  mxj
        endif
c
c                   load new position values
c
        gdat(1,kc,n,0) = clat
        gdat(2,kc,n,0) = clon
        gdat(3,kc,n,0) = xc
        gdat(4,kc,n,0) = yc


        if (iloc .gt. 0) then
c                   load confidence factor of cyclone location, 1 - 3
          gdat(7,kc,n,0) = konf
c                   load wind support, 3 or 4
          gdat(8,kc,n,0) = iloc
c                   load intersection support, 2 - 8
          gdat(9,kc,n,0) = kint
        else
          gdat(5,kc,n,0) = 999.99
          gdat(6,kc,n,0) =  99.99*dtau
          gdat(7,kc,n,0) = 0.0
          gdat(8,kc,n,0) = 0.0
          gdat(9,kc,n,0) = 0.0
        endif
        if (kcl.ne.0 .and. clat.lt.90.0) then
c
c                   calculate heading and distance from last location
c                   to new location, use rhumb line
c
          call rcalhdst (slat,slon,clat,clon,head,dist)
          headnew=head
          distnew=dist
          gdat(5,kc,n,0) = head
          gdat(6,kc,n,0) = dist
        elseif (kcl .eq. 0) then
c
c                   transfer initial heading and distance
c
          gdat(5,kc,n,0)  = gdat(5,kcl,n,0)
          gdat(6,kc,n,0)  = gdat(6,kcl,n,0)
          gdat(7,kcl,n,0) = 0.0
          gdat(8,kcl,n,0) = 0.0
          gdat(9,kcl,n,0) = 0.0
        endif
        
C         
C         detect crossing 0
C         
        if( (abs(headold-headnew).ge.180.0) .and.
     $       (abs(headnew-headold).ge.180.0) ) then
          deltahead=360-abs(headnew-headold)
        else
          deltahead=abs(headold-headnew)
        endif


        if(verb) then
          write(*,'(a,2x,2(f7.2,1x),2x,2(i3,1x),2x,2(f7.2,1x))') 
     $       'FFFFF    clat,clon  ',clat,clon,kc,kclf,head,dist
          write(*,'(a)') ' '
          write(*,'(a)') 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
          write(*,'(a)') ' '
        endif

      enddo
c
c                 load ltrk with number of cyclones still being tracked
c
      ltrk = ntrk
c
      end
