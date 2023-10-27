      subroutine bogread (tcyc,
     $     blat,blon,dlat,dlon,igrdx,jgrdy,
     $     gdat,numv,mxhr,mxtc,maxfix,rdtg,nbog,iunit)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)bogread.f	1.1 12/15/94
C                        22:42:53 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  bogread
C
C  DESCRIPTION:  process NOGAPS bogus data file
C
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
C  USAGE:  call bogread (tcyc,gdat,numv,mxhr,mxtc,rdtg,nbog)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     tcyc         char         out     bogus data in character form
C     gdat         real         out     bogus data in real form
C     numv          int          in     first dimension of gdat, number
C                                       of variables in gdat
C     mxhr          int          in     limit second dimension of gdat,
C                                       max number of tracking positions
C     mxtc          int          in     third dimension of gdat, max
C                                       number of cyclones to track
C     rdtg         char         out     starting dtg of tracking, in
C                                       YYYYMMDDHH format
C     nbog          int         out     number of cyclones to track
C
C  COMMON BLOCKS:  none
C
C  FILES:
C    NAME     UNIT  FILE TYPE  ATTRIBUTE  USAGE         DESCRIPTION
C   -------  -----  ---------  ---------  ------   ---------------------
C    ngtrp    10    permanent  sequential   in     NOGAPS tropical
C                                                  cyclone bogus file
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C    read error                diagnostic
C    bad bogus data            diagnostic
C    number of cyclones to     diagnostic
C      process does not
C      match number read
C
C  ADDITIONAL COMMENTS:
C    1.  Do not read the bogus file to EOF, there may be additional
C        information that is not relevant to tracking.
C    2.  The format of part 1 of bogus file is:
C
C                 1         2         3         4
C        1234567890123456789012345678901234567890
C        1  94100600                                 first line
C        137N 1359E 075 32 W  060 140  2954 140      second & subsequent
C         A    B     C  D  E  F    G    H    I
C
C      first line:
C        col 1    - number of tropical cyclones, max is 9
C            4-11 - dtg in YYMMDDHH format
C
C      second & following lines of part 1:
C        A - latitude  times 10 and hemisphere indicator
C        B - longitude times 10 and hemisphere indicator
C        C - maximum wind speed, kts
C        D - cyclone number
C        E - basin indicator of origin
C        F - radius of 50 kt winds, nm
C        G - radius of 30 kt winds, nm  (this is really 35 kt)
C        H - heading times 10, deg
C        I - speed of movement times 10, kts
C
C    3.  The format of the tcyc array is:
C                  1         2
C         123456789012345678901234
C         12W 123N 1234E  1234 123
C          A   B     C      D   E
C
C         where:
C         A - cyclone number and original basin identification
C         B - latitude  times 10, with hemipshere indicator
C         C - longitude times 10, with hemipshere indicator
C         D - forecast heading times 10, deg
C         E - forecast speed times 10, kts
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         bdtgchk     check that bogus dtg is the same as the computer's
C         valinp      validate input data
C         clltxy      convert from lat,lon to x,y grid co-ords
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C           card     char       working string
C            cns     char       north/south hemisphere indicator
C            cew     char       east/west hemisphere indicator
C            ioe     int        I/O error flag
C            iok     int        good/bad dtg flag, -1 - good
C           ierr     int        conversion error flag, 0 - good
c              k     int        number of good cyclones
C            ntc     int        number of cyclone data to read
C            nrd     int        number of cyclones read
C           shed     real       heading of cyclone, deg
C           slat     real       latitude  of cyclone, deg
C           slon     real       longitude of cyclone, deg
C           sspd     real       speed of movement of cyclone, kts
C           xgrd     real       first x-dimension of grid (lon)
C                               location of cyclone
C           ygrd     real       second y-dimension of grid (lat)
C                               location of cyclone
C
C           Note, grid location 1,1 is 90.0S and 0.0 longitude
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  none
C
C  COMPILER DEPENDENCIES:
C
C  COMPILE OPTIONS:
C
C  MAKEFILE:
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
      implicit none


c
c         formal parameters
      integer numv, mxhr, mxtc, nbog,maxfix

      integer iunit

      integer igrdx,jgrdy
      real blat,blon,dlat,dlon

      character*28 tcyc(mxtc+1), rdtg*16
      real*4 gdat(numv,0:mxhr,mxtc,0:maxfix)
c
c         local variables
      integer ioe, ntc, iok, nrd, k, n, j, ierr
      character card*40, cns*1, cew*1
      real slat, slon, shed, sspd, xgrd, ygrd,vmax
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nrd = 0
      read(iunit,'(a11)',iostat=ioe) card

      if (ioe .eq. 0) then
        if (card(1:1).ge.'0' .and. card(1:1).le.'9') then
c
c                   obtain number of tropical cyclones to process
c         
C         mf 20020511 -- change to handle 10 or more storms!!!
C         

          read (card(1:2),'(i2)') ntc
          rdtg = ' '
c                   first two digits of year are missing from ngtrp
          rdtg(3:10) = card(4:11)
CCCC
CCCC mf 980903 - bypass dtg checking; this is done at a higher level
CCCCc
CCCCc     check that dtg of ngtrp file is correct
CCCC
CCCCc
CCCC          call bdtgchk (rdtg,iok)
          iok=-1
          if (iok .eq. -1) then
c
c                   dtg of bogus is the same as the cumputer's
c
            if (ntc .gt. 0) then
c
c                   there are cyclone positions to process
c
              ntc = min0 (ntc,mxtc)

              do while (ioe .eq. 0)
                read(iunit,'(a40)',iostat=ioe) card
                print*,'bogcard: ',card

C031N 0909E 015 90 B -999 -999 2600 030         
C1234567890123456789012345678901234567890
                if (ioe .eq. 0) then
                  nrd = nrd +1
                  tcyc(nrd)        = ' '
                  tcyc(nrd)(1:2)   = card(16:17)
                  tcyc(nrd)(3:3)   = card(19:19)
                  tcyc(nrd)(5:8)   = card(1:4)
                  tcyc(nrd)(10:14) = card(6:10)
                  tcyc(nrd)(17:24) = card(31:38)
                  tcyc(nrd)(25:28) = card(11:14)
Cmfmfmfmfmfmfmf         
C         
C  if dir/spd 999 then set to climo value         
C         
Cmfmfmfmfmfmfmf
                  if(tcyc(nrd)(17:24).eq.'9999 999') then
                    write(*,*) 'WWWWWWWWWWWWWWWWW - setting'//
     $                   'dir/spd to climo'
                    tcyc(nrd)(17:24)='2850 050'
                  endif

c         warning, do not read to EOF

                  if (nrd .eq. ntc) ioe = -1
                elseif (ioe .ne. -1) then
                  write (*,*) ' $$$ tctrack, bogus read error is ',ioe
                endif
              enddo
              if (nrd .ne. ntc) then
                write (*,*) ' $$$ tctrack, not all cyclones were read'
                write (*,*) '     only read ',nrd,' of ',ntc
              endif
            else
              nbog = 0  
            endif
          else
c
c                   wrong dtg for tracking, so tell driver there are
c                   no cyclones to track
c
            nbog = -1
            write (*,*) ' $$$ wrong ngtrp dtg is ',rdtg
          endif
        else
          nbog = -1
          write (*,*) ' $$$ tctrack, bad input data ',card(1:1)
        endif
      else
        nbog = -1
        write (*,9010) ioe
        write (*,9010) ioe
 9010   format (' $$$ tctrack, read error on input is ',i10)
      endif
      close (10)
c
c                   if there is data, validate it in valinp
c
      if (nrd .gt. 0) call valinp (tcyc,nrd)
      if (nrd .gt. 0) then
c
c                   convert from character mode to real mode
c                   for latitude, longitude, heading and speed
c                   and load gdat array with starting values
c
        k = 0
        do n=1, nrd

          read (tcyc(n),'(4x,f3.1,a1,1x,f4.1,a1,2x,f4.1,1x,f3.1,1x,f3.0)')
     &        slat, cns, slon, cew, shed, sspd, vmax

          if (cns .eq. 'S') slat = -slat
c                   note: longitude is 0 - 360 EAST
          if (cew .eq. 'W') slon = 360.0 -slon
c                   convert lat,lon to grid co-ordinates

CCC       call clltxy (slat,slon,xgrd,ygrd,ierr)

          call clltxy (slat,slon,
     $         blat,blon,dlat,dlon,igrdx,jgrdy,
     $         xgrd,ygrd,ierr)

cccc          print*,'bbbbbbbbbbbbbbbbbbbbbbbbbbbbb ',n,tcyc(n),slat,slon,xgrd,ygrd,ierr

          if (ierr .eq. 0) then
            k = k +1

            gdat(1,0,k,0) = slat
            gdat(2,0,k,0) = slon
            gdat(3,0,k,0) = xgrd
            gdat(4,0,k,0) = ygrd
c                   store heading (deg)
            gdat(5,0,k,0) = shed
c                   store distance (nm) in 6 hours vice speed (kt)
            gdat(6,0,k,0) = 6.0*sspd
            gdat(7,0,k,0) = 0.0
            gdat(8,0,k,0) = 0.0
            gdat(9,0,k,0) = 0.0
            gdat(10,0,k,0) = vmax
c                   put missing lat to all following positions
            do j=1, mxhr
              gdat(1,j,k,0) = 99.9
            enddo
          else
            write (*,*) ' $$$ initial lat,lon conversion error for'
            write (*,*) ' lat ',slat,' lon ',slon
          endif
        enddo
c
c                   re-set nbog to number of cyclones to track
c
        nbog = k
      elseif (nbog .ne. 0) then
        nbog = -1
      endif

      return

 810  continue
      print*,'unable to open ngtrp.txt, ja sayoonara'
      stop 810

      return
c
      end
