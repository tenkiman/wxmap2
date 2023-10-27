      program otcm
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  otcm
c
c  DESCRIPTION:  One-way-influence Tropical Cyclone Model (OTCM)
c                ATCF's One-way-influence Tropical Cyclone Revised (OTCR)
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  earlier versions of OTCM
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  otcm97 $STRMID
c
c  PARAMETERS:
c       Name         Type         Usage            Description
c    ----------    ----------    -------  ----------------------------
c    STRMID          char         input    ID of cyclone to forecast
c                                          exp: WP0997
c  COMMON BLOCKS:
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c                 20                        output    diagnostic
c                 30                        input     input data
c                 40                        output    output data
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c                    For 00/12 Z starting hours of forecast
c    NOGAPS tau:  12  24  36  48  60  72  84
c      OTCM tau:   0  12  24  36  48  60           <- starting tau
c
c                    For 06/18 Z starting hours of forecast
c    NOGAPS tau:   6  12  24  36  48  60  72  84
c      OTCM tau:   0   6  18  30  42  54  68       <- starting tau
c
c    Note:  OTCM for 06 or 18 Z should not be started before the NOGAPS
c           tau 12 fields are available.  It MUST not be started before
c           the tau 06 fields are available.  Other taus may be made from
c           12 hour older fields with the tau moved out 12 hours.
c
c    The following fields are required for OTCM to run:
c
c      -1 - 1000 u-wind (m/s)  <- one time, at start of file
c       0 - 1000 v-wind (m/s)  <- one time, at start of file
c       1 - 1000 temp   (K)
c       2 - 1000 height (m)
c       3 - 850  u-wind (m/s)
c       4 - 850  v-wind (m/s)
c       5 - 850  temp   (k)
c       6 - 500  u-wind (m/s)
c       7 - 500  v-wind (m/s)
c       8 - 500  temp   (k)
c       9 - 250  u-wind (m/s)
c      10 - 250  v-wind (m/s)
c      11 - 250  temp   (K)
c
c    The fields 1 through 11 are needed for each subsequent NOGAPS tau.
c    All the fields MUST be in the above sequential order, in unformatted
c    format.
c
c    MODIFICATIONS TO PRIOR FNMOC OPERATIONAL VERSION OF OTCM
c      (1) No 700 hPa fields are used
c      (2) 550 hPa winds based upon uniform turning of winds
c      (3) Reanalysis replaced with grid transposition
c      (4) 1000 hPa height based upon balance Eq.
c      (5) One pass through balance S/R, no feed-back from forecast
c      (7) Dynamic persistence applied to forecast positions
c          becomes OTCM output
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c       Name           Description
c     --------     --------------------------------------------------
c     balance      calculate initial model winds, temperatures and heights
c                  based upon nondivergent winds and balance equation
c     cyctrack     convert forecast track from grid coordinates to lat/lon and
c                  make ATCF A-deck and plain language output message
c     fakeflds     when fields are missing, set future boundary values if
c                  model has forecast the 48 hour position
c     forecast     forecast model variables
c     getarg       obtain command line argument
c     getenv       obtain contents of named environment variable
c     get_idat     obtain more parameters and initial conditions
c     locase       change all characters to lower case
c     mgrdvals     set Mercator extraction and grid related values
c     setngcnt     obtain NOGAPS location of cyclone and set modified
c                  Mercator grid extraction points, as required
c     sph2mer      driver program to extract Mercator grid points from
c                  NOGAPS spherical (lat/lon) grid
c     upcase       change all characters to upper case
c
c  LOCAL VARIABLES:
c         name       type               description
c         ------     ----       -----------------------------------------
c         nogo       int        continuation flag, -1 abort
c         ioe        int        I/O error flag, 0 no error
c         lbp        int        character count of given path
c         ioer       int        I/O error flag, 0 no error
c         kstp       int        index for model taus
c         ierr       int        S/R error return flag, 0 no error
c         ihc        int        dynamic location of first dimension of heat
c                               source in model
c         jhc        int        dynamic location of second dimension of heat
c                               source in model
c         ihci       int        initial location of ihc
c         jhci       int        initial location of jhc
c         ivrad      int        radius of model cyclone
c         kht        int        flag for type of heating desired
c         ktau       int        array of starting model taus, depending upon
c                               starting NOGAPS tau
c         mtau       int        starting model tau in hours
c         ntau       int
c         ndiag      int        I/O unit number for diagnostics
c         nuin       int        I/O unit number for inout data
c         nout       int        I/O unit number for output data
c
c  METHOD:
c
c  INCLUDE FILES:
c
c  COMPILER DEPENDENCIES:  f77 with enhancements
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c     Modified to use new data format,  6/98   A. Schrader
c     Modified to use bt posit century  11/98  Sampson     
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_ng.inc'
      INCLUDE 'par_mer.inc'
c
      integer  nogo, ioe, lbp, ioer, kstp
      integer  k, ierr, ihc, jhc, mtau, ntau 
      integer  kht, lhr, klmt
      integer  ktau(8,2)
      integer  ndiag, nuin, nout
      integer  ibtwind, ios, iarg
c
      real     btlat, btlon
c
      character*1   cdummy
      character*6   strmid
      character*2   century
      character*2   cent
      character*8   cpdtg, cfdtg
      character*8   tdtg
      character*8   btdtg
      character*100 storms
      character*132 filename
      character*1   btns, btew
c
      INCLUDE 'cyc_c_com.inc'
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'cyc_v_com.inc'
      INCLUDE 'fltln_com.inc'
      INCLUDE 'minmax_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr1_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'mstrls_com.inc'
      INCLUDE 'stat3_com.inc'
      INCLUDE 'stat4_com.inc'
      INCLUDE 'vort_com.inc'
c
c              set input and output unit numbers
      data ndiag/20/, nuin /30/, nout/40/
c              set starting model taus for 06/18 & 00/12 Z runs
      data ktau /0, 6,18,30,42,54,66,78,
     &           0,12,24,36,48,60,72,84/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nogo = 0
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c                              get cyclone to forecast (WP0497)
      call getarg (iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c  get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
c
c  write heading on output
c
      print *,'********************************************************'
      print *,' '
      print *,'          otcm forecast for ',strmid
      print *,' '

c                              get path to cyclone data
      call getenv ("ATCFSTRMS",storms)
c                              get length of base path to cyclone data
      lbp = index (storms," ") -1
c
c                   all filenames must be lower case,
c                   set the filenames and open the input and output files
c
      filename = ' '
      write(filename,'(a,a,a,a,a,a)') storms(1:lbp), "/b", 
     1     strmid(1:4), century, strmid(5:6), ".dat"
      open (nuin,file=filename,status='old',iostat=ioer)
      if (ioer .ne. 0) then
	write (*,*) 'OPEN ERROR is ',ioer,' ',filename
	goto 766
c
      endif
c
      filename = ' '
      filename = storms(1:lbp) // "/wptot.dat"
      open (nout,file=filename,status='unknown',iostat=ioer)
      if (ioer .lt. 0) then
	write (*,*) 'OPEN ERROR is ',ioer,' ',filename
	goto 766
c
      endif
      rewind (nuin)
      rewind (nout)
c
c                   go to the end of the output file
c
   20 continue
      read (nout,'(a1)',end=25) cdummy
      go to 20
c
   25 continue
c
c                   convert the 1st two characters of stormid to uppercase
c
      call upcase (strmid,6)
      cycid(1:2) = strmid(3:4)
      cycid(3:3) = strmid(1:1)
cx  In this model, the 3 character id is used.  al0197 becomes 01L,
cx  and io0197 becomes 01A or 01B - we can just set to 01A  ... bs 10/8/97
      if (cycid(3:3) .eq. 'A') cycid(3:3) = 'L'
      if (cycid(3:3) .eq. 'I') cycid(3:3) = 'A'
c
c                   find the last dtg in the working best track file
c
      ios = 0
      do while ( ios .eq. 0 )
         call readBT(nuin,cent,tdtg,btlat,btns,btlon,btew,ibtwind,ios)
         if (tdtg.ne.'        ') cpdtg=tdtg
      enddo
c
   35 continue
      rewind (nuin)
      write (*,*) 'FORECAST cyclone ',cycid,' from ',cpdtg
c
c                   obtain other parameters and initial conditions
c
      call get_idat (nuin,cpdtg,kht,nogo)
      close (nuin)
c     if (nogo .eq. 0) then
c
c                   open diagnostic file
c
c       open (ndiag,file='otcm97.diag',form='formatted',iostat=ioe)
c       if (ioe .ne. 0) then
c         nogo = -1
c         write (*,*) 'OPEN diagnostic file error is ',ioe
c       endif
c     else
c       write (*,*) ' ***** Cant start OTCM77, otcmdat file error'
c     endif
      if (nogo .eq. 0) then
c
c                   open file which has all the global fields
c
c              (2.5 degree 144 by 73 - pt1 South pole, 0 Longitude)
c            first  dimension (144) are longitude points with fixed lat
c           second dimension (73) goes from South pole to North Pole
c
        filename = ' '
        filename = storms(1:lbp) // "/otcm." // cpdtg
        open (nuin,file=filename,status='old',form='unformatted',
     &        access='sequential',err=744,iostat=ioe)
	read (nuin,err=745,iostat=ioe) cfdtg
	if (cfdtg .ne. cpdtg) then
	  write (*,*) 'FIELDS are for ',cfdtg,' NEED ',cpdtg
	  goto 600
c
	endif
        ntau = 0
c                       calculate Mercator grid extraction values
        call mgrdvals
c                       set modified extraction points, as required
        call setngcnt (ierr)
c                       obtain initial fields
        if (ierr .eq. 0) then
	  rewind (nuin)
	  read (nuin,err=745,iostat=ioe) cfdtg
	  call sph2mer (ntau,ierr)
	endif 
        if (ierr .eq. 0) then
c         write (*,*) 'OTCM Processing fields for model tau ',mtau
c
c                       modify initial fields for model
c
          call balance
          ihc = icyc
          jhc = jcyc
          if (cpdtg(7:8) .eq. '00' .or. cpdtg(7:8) .eq. '12') then
            kstp = 2
          else
            kstp = 1
          endif
          lhr = kstp
          if (lhr .eq. 1) then
            klmt = 7
          else
            klmt = 6
          endif
          do k=1, klmt
            mtau = ktau(k,lhr)
            ntau = ktau(k+1,lhr)
c                            read in new boundary values
            call sph2mer (ntau,ierr)
            if (ierr .ne. 0) then
              write (*,*) 'Missing tau ',ntau,' from ',cfdtg
              if (mtau .gt. 48) then
                write (*,*) 'Continue w/o boundary update'
                call fakeflds
              else
                write (*,*) 'ABORT - MISSING fields for mtau ',mtau
c               write (20,*) '**** OTCM MISSING fields for mtau ',
c    &                        ntau
                nogo = -55
                goto 100
c
              endif
            endif
c                            forecast
            call forecast (mtau,kstp,kht,ihc,jhc,nogo)
            if (nogo .ne. 0) goto 100
c
            kstp = 2
          enddo
  100     continue
c
c                       generate A-Deck and plain language output
c
          call cyctrack (nout,nogo)
          if (nogo .eq. -66) then
            goto 766
c
          elseif (nogo .ne. 0) then
            goto 777
c
          endif
        else
          write (*,*) 'NO INITIAL FIELDS'
c         write (20,*) '***** OTCM MISSING fields for tau ',ntau
          goto 755
c
        endif
      endif
  600 continue
      rewind (nout)
      close  (nout)
      close  (nuin)
      stop
c
  744 continue
      write (*,*) 'FIELD open error ',ioe,' ABORT'
      write (*,*) 'on file:',filename
      goto 600
c
  745 continue
      write (*,*) 'INITIAL FIELD read error ',ioe,' ABORT'
      write (*,*) 'on file:',filename
      goto 600
c
  755 continue
      write (*,*) 'FIELD read error, ABORT'
      write (*,*) 'on file:',filename
      goto 600
c
  766 continue
      write (*,*) 'I/O type error, ABORT'
      write (*,*) 'on file:',filename
      goto 600
c
  777 continue
      write (*,*) 'OTCM97 finished with an ERROR'
      goto 600
c
      end
      subroutine adjpot (gz,ixm,jym,pot)
c
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  adjpot
c
c  DESCRIPTION:  adjust potential temperature 850 thru 250 hPa, based
c                upon differences in height and potential temperature of
c                lower level
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call adjpot (gz,ixm,jym,pot)
c
c  PARAMETERS:
c       Name         Type         Usage            Description
c    ----------   ----------     -------  ----------------------------
c      gz           real          input    matrix of gz fields
c      ixm          int           input    first  dimension of fields
c      jym          int           input    second dimension of fields
c      pot          real          in/out   matrix of potential temps
c
c  CALLED BY:  balance
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c       name                  Description
c      ------               ----------------------------------------------
c      ptstab               establish static stability
c
c  LOCAL VARIABLES:
c      Name      Type                 Description
c     ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.0  (05 SEP 1997)  Hamilton, H.
c    initial installation on ATCF
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c     formal parameters
      integer           ixm, jym
      double precision  pot(ixm,jym,4), gz(ixm,jym,4)
c
c     local variables
      integer           i, j, k, nadj, nfor, kode
      double precision  con1
c
      INCLUDE 'stat2_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do k=2, 4
        nadj = 0
        nfor = 0
        con1 = -502.0d0*(piup(k) -pilo(k))
        do j=1, jym
          do i=1, ixm
            pot(i,j,k) = (gz(i,j,k) -gz(i,j,k-1))/con1 -pot(i,j,k-1)
            if (pot(i,j,k) .lt. pot(i,j,k-1))
     &         call ptstab (i,j,k,pot,nadj,nfor)
          enddo
        enddo
        if (nadj .ne. 0 .or. nfor .ne. 0)
     &   write(*,*) 'ADJPOT, Level ',k,' ADJUSTED ',nadj,' FORCED ',nfor
      enddo
c
      end
      subroutine adjxtrc (xlat,xlon)
c
c
c
c  CALLED BY:  setngcnt & setxltln
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      real xlat, xlon
c
c         local variables
      integer i, j
      real    gdlns, gdlnp, gdln
      double precision  dxlat, d2eq, gdis, grlat, gdltj, re_tlat
c
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'ngfld_p_com.inc'
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat4_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   compute distance from cyclone latitude to equator
c
      re_tlat = 1.0d0/re_tlat_i
      dxlat   = xlat
      d2eq    = re_tlat*log ((1.0d0 +sin (dxlat*deg2rad))
     &           /cos(dxlat*deg2rad))
      do j=jym, 1, -1
        gdis  = (d2eq +(j -jcyc)*del)*re_tlat_i
        grlat = 2.0d0*atan (exp (gdis)) - 0.5d0*pi
        gdltj = rad2deg*grlat
c                         for 144 by 73  2.5 deg lat/lon grid
        bjng(j) = 1.0 +(gdltj +90.0)/2.5
c       write (20,9020) j, bjng(j), gdltj
c9020   format (i5,3x,f7.3,3x,f6.2,3x,f7.5,3x,e15.9)
      enddo
      gdlns = xlon -real (icyc -1)
      gdlnp = gdlns
c                             for 144 by  73 2.5 deg lat/lon grid
      bing(1) = 1.0 +gdlnp/2.5
      do i=2, ixm
        gdln    = gdlnp +real (mg_deg)
        bing(i) = 1.0 +gdln/2.5
        gdlnp   = gdln
      enddo
c     write (20,9030) mg_deg, gdlns, gdlnp
c9030 format (1x,'longitude - left to right at ',i1,' degree interval',
c    &        /,3x,f10.3,5x,f10.3)
c
      end
      real function avgddt (dd1,dd2,f1)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)avgddt.f90	1.1  3/31/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  avgddt
c
c  DESCRIPTION:  calculate weighted average wind direction
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  avgdd = avgddt (dd1,dd2,f1)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     dd1          real          in     wind direction at point 1, deg
c     dd2          real          in     wind direction at point 2, deg
c      f1          real          in     fraction of grid length from pt1
c                                       to "center-line", which is
c                                       between pt 1 and pt 2
c  avgddt          real         out     weighted average wind direction
c                                       on "center-line", degrees
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          dds       real       copy of dd1 or dd2
c          ddl       real       copy of dd2 or dd1
c           fs       real       fractional part of grid length
c           fl       real       fractional part of grid length
c
c  METHOD:  simple weighted average
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real dd1, dd2, f1
c
c         local variables
      real dds, ddl, fl, fs
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (dd1 .ne. dd2) then
        if (dd1 .lt. dd2) then
          dds = dd1
          ddl = dd2
           fl = f1
           fs = 1.0 -f1
        else
          dds = dd2
          ddl = dd1
          fs  = f1
          fl  = 1.0 -f1
        endif
        if (ddl -dds .gt. 180.0) dds = dds +360.0
        avgddt = amod ((fs*dds +fl*ddl), 360.0)
      else
        avgddt = dd1
      endif
      if (avgddt .eq. 0.0) avgddt = 360.0
c
      end
      subroutine avgval (i,j,fld,avg,est)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)avgval.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  avgval
c
c  DESCRIPTION:  calculate average and estimated value of field at i,j
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call avgval (i,j,fld,avg,est)
c
c  PARAMETERS:
c     Name       Type       Usage            Description
c  ----------  --------    -------  ----------------------------
c     i          int        input   first  dimension location of point
c     j          int        input   second dimension location of point
c     fld        real       input   field array
c     avg        real       output  average value of adjacent points
c     est        real       output  average value of extrapolations
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c      Name      Type                 Description
c     ------     ----       -----------------------------------------
c
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      integer           i, j
      double precision  avg, est, fld(ixm,jym)
c
c     local variables
      double precision  p1, p2, p3, p4
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (i.gt.2 .and. i.lt.ixm-1 .and. j.gt.2 .and. j.lt.jym-1) then
        avg = 0.25d0*(fld(i-1,j) +fld(i+1,j) +fld(i,j-1) +fld(i,j+1))
        p1  = 2.0d0*fld(i-1,j) -fld(i-2,j)
        p2  = 2.0d0*fld(i+1,j) -fld(i+2,j)
        p3  = 2.0d0*fld(i,j-1) -fld(i,j-2)
        p4  = 2.0d0*fld(i,j+1) -fld(i,j+2)
        est = 0.25d0*(p1 +p2 +p3 +p4)
      else
        if (i.gt.1 .and. i.lt.ixm .and. j.gt.1 .and. j.lt.jym) then
          avg = 0.25d0*(fld(i-1,j) +fld(i+1,j) +fld(i,j-1) +fld(i,j+1))
        elseif (i .eq. 1 .or. i .eq. ixm) then
          if (j .gt. 1 .and. j .lt. jym) then
            avg = 0.5d0*(fld(i,j-1) +fld(i+1,j+1))
          elseif (j .eq. 1) then
            if (i .eq. 1) then
              avg = 0.5d0*(2.0d0*fld(1,2) -fld(1,3) +2.0d0*fld(2,1)
     &             -fld(3,1))
            else
              avg = 0.5d0*(2.0d0*fld(ixm,2) -fld(ixm,3)
     &                    +2.0d0*fld(ixm-1,1) -fld(ixm-2,1))
            endif
          else
            if (i .eq. 1) then
              avg = 0.5d0*(2.0d0*fld(1,jym-1) -fld(1,jym-2)
     &                    +2.0d0*fld(2,jym) -fld(3,jym))
            else
              avg = 0.5d0*(2.0d0*fld(ixm,jym-1) -fld(ixm,jym-2)
     &                    +2.0d0*fld(ixm-1,jym) -fld(ixm-2,jym))
            endif
          endif
        else
          avg = 0.5d0*(fld(i-1,j) +fld(i+1,j))
        endif
        est = avg
      endif
c
      end
      subroutine badvec (uu,vv,uv,flux)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)badvec.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  badvec
c
c  DESCRIPTION:  compute advection in flux form for wind component in uv
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call badvec (uu,vv,uv,flux)
c
c  PARAMETERS:
c     Name            Type         Usage            Description
c  ----------      ----------     -------  ----------------------------
c     uu              real         input   u-component of wind
c     vv              real         input   v-component of wind
c     uv              real         input   u or v wind component
c     flux            real         output  advection in flux form
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c        Name      Type                 Description
c       ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal arguments
      double precision  uu(ixm,jym), vv(ixm,jym), uv(ixm,jym),
     &                flux(ixm,jym)
c
c     local variables
      integer i, j
      double precision  a1, a2
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      flux = 0.0d0
      do j=2, jym-1
        i  = 2
        a2 = (uu(i,j) +uu(i-1,j))*emi(j)*(uv(i,j) +uv(i-1,j))
        do i=2, ixm-1
          a1 = (uu(i+1,j) +uu(i,j))*emi(j)*(uv(i+1,j) +uv(i,j))
          flux(i,j) = a1 -a2
          a2 = a1
        enddo
      enddo
c
      do i=2, ixm-1
        j  = 2
        a2 = (vv(i,j)*emi(j) +vv(i,j-1)*emi(j-1))*(uv(i,j) +uv(i,j-1))
        do j=2, jym-1
          a1 = (vv(i,j+1)*emi(j+1) +vv(i,j)*emi(j))*(uv(i,j+1) +uv(i,j))
          flux(i,j) = -(flux(i,j) +a1 -a2)*em(j)*em(j)/(4.0d0*del)
          a2 = a1
        enddo
      enddo
c
      end
      subroutine balance 
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  balance
c
c  DESCRIPTION:  calculate nondivergent winds with model cyclone inserted,
c                solve balance equation to obtain geopotential fields,
c                calculate upper air potential temperatures with
c                hydrostatic equation
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES: 1) NCAR Technical Note - NCAR-TN/IA-109, July 1975
c                 Efficient FORTRAN Subprograms for the Solution of
c                 Elliptic Partial Differential Equations
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call balance
c
c  PARAMETERS:  none
c
c  COMMON BLOCKS:
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c    First dimension of fields may be any reasonable number.
c    Second dimension of vort field MUST be (2**p * 3**q * 5**r) -1,
c    second dimension of fields are second dimension of vort +2.
c    Where: p, q and r may be any non-negative integers;
c    when Dirichlet boundary conditions are selected for the solution
c    of the resulting elliptic partial differential equation.
c    These boundary conditions are used in these routines.
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c        Name           Description
c      ---------     --------------------------------------------------------
c      caluphi       calculate the phi (gz) values for 850, 550 & 250
c      prep1000      calculate phi at 1000 based upon balance eqation
c      setbstrmf     set the boundary stream function values
c      calvort       insert tropical cyclone, and calculate vorticity
c      calstrmf      calculate the internal stream function values
c      calwndc       calculate the non-divergent wind components
c      calphk        solve balance equation for phi at 850, 550 & 250
c      adjpot        adjust potential temperatures at 850, 550 & 250
c
c      uvrng3a       calculate max, avg & min of winds
c                    internal grid points - diagnostic routine.
c      ptrng4a       calculate max, avg & min potential temps
c                    over internal grid points - diagnostic routine.
c      gzrng4a       calculate max, avg & min of geopotential
c                    internal grid points - diagnostic routine.
c
c  LOCAL VARIABLES:
c      Name      Type                 Description
c     ------     ----       -----------------------------------------
c      nfor      int        working array for caluphi
c      wt        real       weighting function for maximum model vorticity
c
c  METHOD:  The descriptions listed above for the routines called explains the
c           methods employed and are in the proper sequence.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f77 with some f90 enhancements
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters:  none
c
c         local variables
      integer  m, i, j, nfor(4)
      real    wt(3)
      double precision  vortmx
      double precision  strmf(ixm,jym), vort(ixm-2,jym-2)
c
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat2_com.inc'
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr1_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'mstrls_com.inc'
      INCLUDE 'works_com.inc'
c
      equivalence (wrk81(1,1),strmf(1,1)), (wrk82(1,1),vort(1,1))
c
      data wt/1.0, 0.8, 0.5/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (*,*) 'starting BALANCE routine'
c
c                   calculate maximum vorticity for model cyclone
c
      vortmx = sign (dble (mwndmx)/120000.0d0,dble (rlat))
c
c                   move 1000 geopotential to computational grid
c
      z110 = zls10
c
c                   calculate upper air geopotentials
c
      call caluphi (tls,ixm,jym,gz1,nfor)
c
c     write(20,*) 'INITIAL VALUES.....'
c     call uvrng3a (uls,vls,ixm,jym,-1)
c     call ptrng4a (tls,ixm,jym,1,-1)
c     call gzrng4a (gz1,ixm,jym,-1)
c
c                   calculate gz at 1000 based upon balance eq.
c
      call prep1000 (vortmx)
c
c     **********  calculate non-divergent winds for 850, 550 & 250
c
      do m=1, 3
c       write (20,*) ' BALANCE processing level ',m
c
c                   calculate estimate of streamfunction on boundary
c
        call setbstrm (uls(1,1,m),vls(1,1,m),strmf)
c
c                  move winds to computational grids 
c
        do j=1, jym
          do i=1, ixm
            uu1(i,j,m) = uls(i,j,m)
            vv1(i,j,m) = vls(i,j,m)
          enddo
        enddo
c
c                   insert model cyclone and calculate vorticity
c
        call calvort (uu1(1,1,m),vv1(1,1,m),icyc,jcyc,vortmx,wt(m),vort)
c    &                ,vort)
c
c                   calculate interior streamfunction values
c
        call calstrmf (vort,ixm,jym,del,em,strmf,wrk83)
c
c                   calculate non-divergent wind components
c
        call calwndc (strmf,uu1(1,1,m),vv1(1,1,m))
c
      enddo
c     write (20,*) ' Initial nondivergent winds with cyclone'
c     call uvdisp (uu1,vv1,ixm,jym,icyc,jcyc,wrk41,wrk42)
c     call uvrng3a (uu1,vv1,ixm,jym,-1)
c
c     write(20,*) 'END of wind processing in balance ********'
c     write (*,*) 'END of wind processing in balance ********'
c
c     *********  calculate gz fields based upon balance eq., 850 to 250
c
      call calphk (uu1,vv1,gz1,wrk81,wrk82,wrk83,wrk84,wrk85)
c
c     *********  adjust 850, 550 and 250 potential temps, as required
c
      call adjpot (gz1,ixm,jym,tls)
c
c     write(20,*) 'AFTER all adjustments in balance *************'
c     call ptrng4a (tls,ixm,jym,1,-1)
c     call gzrng4a (gz1,ixm,jym,-1)
c
c     **************** load initial environment fields for S/R forecast
c
      pt1 = tls
      pt2 = tls
      gz2 = gz1
      uu2 = uu1
      vv2 = vv1
c     write (20,*) 'END of BALANCE, forecast fields loaded'
      write (*,*)  'end of BALANCE, forecast fields loaded'
c
      end
      subroutine bldmer (gnfld,lev,npar,ierr)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)bldmer.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  bldmer
c
c  DESCRIPTION:  driver routine for building Mercator fields from NOGAPS
c                global fields
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call bldmer (gnfld,lev,npar,ierr)
c
c  PARAMETERS:
c     Name        Type      Usage            Description
c  ---------    --------   -------    ----------------------------
c   gnfld         real      input     global NOGAP field
c   lev           int       input     level indicator of input field
c   npar          int       input     parameter flag
c   ierr          int       output    error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     field dimensions         signal error and return
c     in error
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c     Name           Description
c   -------     ----------------------
c   merlod8     load Mercator grid with interpolated values
c   setbwnd     adjust boundary winds for no net inflow/outflow
c   avgval      calculate average values at given point in grid
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:  Obtain the 1000 phi (gz) value based upon potential temperatures
c           at 1000 and 850, and the phi value of the 850.
c           Obtain the 550 hPa values from the 850 and 500 hPa NOGAPS fields.
c              Level    phi (gz)  potential temp   u-wind   v-wind
c               250                   X               X        X
c               550                   X               X        X
c               850        X          X               X        X
c              1000                   X
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f77 with extensions
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_ng.inc'
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      integer  lev, npar, ierr
      real     gnfld(ixng,jyng)
c
c     local variables
      integer           inil, i, j
      real              az10, wt55
      double precision  rd_div_cp
c
      save az10, wt55, inil
c
      INCLUDE 'stat2_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstrls_com.inc'
      INCLUDE 'mstr2_com.inc'
c
      data inil/0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (lev .eq. 1) then
        if (inil .eq. 0) then
c
c              Note:  these values MUST be used on the first call
c
c                 calculate saved and common values
c
          az10  = 9.8
c                          0.1796176 =  (ln550 -ln500)/(ln850 -ln500)
          wt55  = 0.1796176
c                          1.0/3.5   = 0.068557/0.24 = Rd/cp
          rd_div_cp = 1.0/3.5
          piup(1) = 1.0
          piup(2) = (850.0/1000.0)**rd_div_cp
          piup(3) = (550.0/1000.0)**rd_div_cp
          piup(4) = (250.0/1000.0)**rd_div_cp
c         write (20,*) ' piup ',(piup(k),k=1,4)
          pilo(1) = 0.0
          pilo(2) = piup(1)
          pilo(3) = piup(2)
          pilo(4) = piup(3)
c         write (20,*) ' pilo ',(pilo(k),k=1,4)
          pic(1)  = 1.0
          pic(2)  = (1000.0/850.0)**rd_div_cp
          pic(3)  = (1000.0/550.0)**rd_div_cp
          pic(4)  = (1000.0/250.0)**rd_div_cp
c         write (20,*) ' pic ',(pic(k),k=1,4)
          inil = -1
        endif
c
c               process the 1000 hPa fields
c
	if (npar .eq. 1) then
c
c               process 1000 hPa u-wind field  (m/s)
c
	  call merlod8 (gnfld,u285,ixm,jym,ierr)
	  if (ierr .eq. 0) then
            write(*,*) 'u1000 loaded'
          else
	    write(*,*) 'error loading u1000'
          endif
        elseif (npar .eq. 2) then
c
c               process 1000 hPa v-wind field  (m/s)
c
	  call merlod8 (gnfld,v285,ixm,jym,ierr)
	  if (ierr .eq. 0) then
	    write(*,*) 'v1000 loaded'
            call setbwnd (ixm,jym,emi,u285,v285)
          else
	    write(*,*) 'error loading v1000'
          endif
	elseif (npar .eq. 3) then
c
c               process 1000 hPa temperature field  (K)
c
          call merlod8 (gnfld,tls10,ixm,jym,ierr)
        elseif (npar .eq. 4) then
c
c               process 1000 hPa height field  (m)
c
          call merlod8 (gnfld,zls10,ixm,jym,ierr)
	  if (ierr .eq. 0) then
	    do j=1, jym
	      do i=1, ixm
		zls10(i,j) = zls10(i,j)*az10
              enddo
	    enddo
	  endif 
	endif
      elseif (lev .eq. 2) then
c
c               process 850 hPa fields
c
        if (npar .eq. 1) then
c               u-wind (m/s)
          call merlod8 (gnfld,uls85,ixm,jym,ierr)
        elseif (npar .eq. 2) then
c               v-wind (m/s)
          call merlod8 (gnfld,vls85,ixm,jym,ierr)
c
c                   adjust boundary winds for no net inflow/outflow
c                   after 550 winds are determined
c
        elseif (npar .eq. 3) then
c               T (K)
          call merlod8 (gnfld,tls85,ixm,jym,ierr)
c               convert temperature (K) to potential temperature
          if (ierr .eq. 0) tls85 = tls85*pic(2)
        endif
      elseif (lev .eq. 3) then
c
c               process 500 hPa fields and obtain the 550 hPa fields
c
        if (npar .eq. 1) then
c               u-wind (m/s)
          call merlod8 (gnfld,uls55,ixm,jym,ierr)
        elseif (npar .eq. 2) then
c               v-wind (m/s)
          call merlod8 (gnfld,vls55,ixm,jym,ierr)
        elseif (npar .eq. 3) then
c               t (K)
          call merlod8 (gnfld,tls55,ixm,jym,ierr)
          if (ierr .eq. 0) then
c
c               calculate 550 hPa values from 850 & 500 hPa levels
c
c                 calculate temperature (K)
            tls55 = tls55 +(tls85/pic(2) -tls55)*wt55
c                   convert temperature (K) to potential temperature
            tls55 = tls55*pic(3)
c                 calculate 550 hPa u & v winds
            uls55 = uls55 +(uls85 -uls55)*wt55
            vls55 = vls55 +(vls85 -vls55)*wt55
c
c                   adjust boundary winds for no net inflow/outflow
c                   both 850 and 550
c
            call setbwnd (ixm,jym,emi,uls85,vls85)
            call setbwnd (ixm,jym,emi,uls55,vls55)
          endif
        endif
      elseif (lev .eq. 4) then
c                   process 250 hPa fields
        if (npar .eq. 1) then
c               process u-wind  (m/s)
          call merlod8 (gnfld,uls25,ixm,jym,ierr)
        elseif (npar .eq. 2) then
c               process v-wind  (m/s)
          call merlod8 (gnfld,vls25,ixm,jym,ierr)
c
c                   adjust boundary winds for no net inflow/outflow
c
          call setbwnd (ixm,jym,emi,uls25,vls25)
        elseif (npar .eq. 3) then
c               process temperature (K)
          call merlod8 (gnfld,tls25,ixm,jym,ierr)
c               convert temperature (K) to potential temperature
          if (ierr .eq. 0) tls25 = tls25*pic(4)
        endif
      endif
c
      end
      subroutine calcntr (nc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)calcntr.f90	1.1 3/31/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calcntr
c
c  DESCRIPTION:  calculate centroid of intersections
c
c  COPYRIGHT:                  (C) 1994 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Cray UNICOS
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calcntr (nc)
c
c  PARAMETERS:
c     NAME        TYPE      USAGE             DESCRIPTION
c   --------     ------     ------   ------------------------------
c      nc         int         in     index to systems
c
c  COMMON BLOCKS:            COMMON BLOCKS ARE DOCUMENTED WHERE THEY ARE
c                            DEFINED IN THE CODE WITHIN INCLUDE FILES.
c                            THIS MODULE USES THE FOLLOWING VARIABLES OF
c                            THE LISTED COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c      /BOX/      lbox      int      in     unit number for diagnostics
c                   xs     real      in     starting first dimension of
c                                           isogon box
c                   xl     real      in     ending first dimension of
c                                           isogon box
c                   ys     real      in     starting second dimension of
c                                           isogon box
c                   yl     real      in     ending second dimension of
c                                           isogon box
c                  nip      int      in     count of intersection points
c                   cx     real      in     array of first dimension
c                                           intersection points
c                   cy     real      in     array of second dimension
c                                           intersection points
c                  rxc     real      in     running average of first
c                                           dimension intersection point
c                  ryc     real      in     running average of second
c                                           dimension intersection point
c                  rxc     real     out     first dimension of cyclone
c                                           location
c                  ryc     real     out     second dimension of cyclone
c                                           location
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           diff     real       maximum x or y difference from estimated
c                               centroid
c             dr     real       radial distance from centroid
c         epslon     real       small number
c              k      int       number of iterations
c             rr     real       radial distance from centroid
c             sx     real       sum of x-coord of centroid
c             sy     real       sum of y-coord of centroid
c            ttt     real       temporary variable
c
c  METHOD:  calculate centroid based upon intersections closest to the
c           running centroid position, for index nc.
c           note: nip(nc) must be 3 or greater before calling calcntr
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          -----------    ---------------------------------------
c           box.inc       common block
c
c  COMPILER DEPENDENCIES:  Cray UNICOS
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (02 APR 1997) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameter
      integer nc
c
c         local variables
      integer  k,m,n
      real     diff,rxl,ryl,dx,dy,dr,rr,ttt,sx,sy,epslon
c
      INCLUDE 'box.inc'
c
      data epslon/1.0e-03/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c     write (33,*) ' calcntr, running avg xc ',rxc(nc),' yc ',ryc(nc),
c    &             ' with ',nip(nc),' intersections'
c
      k    = 0
      diff = 99.9
      do while (nip(nc) .gt. 2 .and. diff .gt. epslon)
        rxl = rxc(nc)
        ryl = ryc(nc)
c
c                   sort on difference from last estimate of location,
c                   least to most
c
        do m=1, nip(nc) -1
          dx = rxl -cx(nc,m)
          dy = ryl -cy(nc,m)
          dr = dx*dx +dy*dy
          do n=m+1, nip(nc)
            dx = rxl -cx(nc,n)
            dy = ryl -cy(nc,n)
            rr = dx*dx +dy*dy
            if (rr .lt. dr) then
              ttt      = cx(nc,n)
              cx(nc,n) = cx(nc,m)
              cx(nc,m) = ttt
              ttt      = cy(nc,n)
              cy(nc,n) = cy(nc,m)
              cy(nc,m) = ttt
              dr       = rr
            endif
          enddo
        enddo
c
c                   calculate new estimate, w/o worst case
c
        sx = 0.0
        sy = 0.0
        nip(nc) = nip(nc) -1
        do n=1, nip(nc)
          sx = sx +cx(nc,n)
          sy = sy +cy(nc,n)
        enddo
        rxc(nc) = sx/nip(nc)
        ryc(nc) = sy/nip(nc)
        k = k +1
        diff = amax1 (abs (rxl -rxc(nc)), abs (ryl -ryc(nc)))
      enddo
c     write (33,*) ' calcntr, with ',k,' iterations: x= ',rxc(nc),
c    &             ' y= ',ryc(nc),' with ',nip(nc),' intersections'
c
      end
      subroutine calddto (ddfld,vvfld,igrdx,jgrdy,umx,vmx)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)calddto.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calddto
c
c  DESCRIPTION:  calculate wind direction, towards, with u,v components
c                and maximum component wind speeds
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  SUN/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calddto (ddfld,vvfld,igrdx,jgrdy,umx,vmx)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c    ddfld         real        in/out   u-component array, m/s
c                                       /wind direction, deg (towards)
c    vvfld         real         in      v-component array, m/s
c    igrdx          int         in      first  dimension of fields
c    jgrdy          int         in      second dimension of fields
c    umx           real         out     maximum u-component wind speed (m/s)
c    vmx           real         out     maximum v-component wind speed (m/s)
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           ddto     real       grid point wind direction
c          epsln     real       small number
c           inil      int       flag for initial calculation
c            rtd     real       radian-to-degree conversion factor
c             uu     real       u-wnd at grid point
c             vv     real       v-wnd at grid point
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Cray Fortran 77
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation, with OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer  igrdx, jgrdy
      real     ddfld(igrdx*jgrdy,1), vvfld(igrdx*jgrdy,1)
c
c         local variables
      integer  inil, n
      real     ddto, umx, vmx
      real     epsln, uu, vv, rtd
c
      save inil, rtd
c
      data epsln/0.0001/
      data inil/0/, rtd/57.2958279/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .eq. 0) then
        inil = -1
        rtd  = 180.0d0/acos (-1.0d0)
      endif
      umx = 0.0
      vmx = 0.0
      do n=1, igrdx*jgrdy
        uu  = ddfld(n,1)
        umx = max (umx,abs (umx))
        vv  = vvfld(n,1)
        vmx = max (vmx,abs (vmx))
        if (abs (uu) .lt. epsln) uu = 0.0
        if (abs (vv) .lt. epsln) vv = 0.0
        if (uu.ne.0.0 .or. vv.ne.0.0) then
          ddto = amod (450.0 - (rtd*atan2 (vv,uu)),360.0)
          if (ddto .lt. 0.0) ddto = 360.0 +ddto
          if (ddto .eq. 0.0) ddto = 360.0
        else
          ddto = 360.0
        endif
        ddfld(n,1) = ddto
      enddo
      return
c
      end
      subroutine calint
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)calint.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calint
c
c  DESCRIPTION:  calculate point(s) of intersection of two isogons
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calint
c
c  PARAMETERS:  none
c
c  CALLED BY:  isotrc.f
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c      box       cx        real     out     new x-intercept
c      box       cy        real     out     new y-intercept
c      box       lbox       int      in     diagnostic unit number
c      box       nip        int    in/out   count of intersections
c      box       rxc       real    in/out   running x-intercept
c      box       ryc       real    in/out   running y-intercept
c      box       xs        real      in     x-start of isogon box
c      box       xl        real      in     x-end of isogon box
c      box       ys        real      in     y-start of isogon box
c      box       yl        real      in     y-end of isogon box
c
c      isoxy     xx1       real      in     x-values of rh1
c      isoxy     yy1       real      in     y-values of rh1
c      isoxy     xx2       real      in     x-values of rh2
c      isoxy     yy2       real      in     y-values of rh2
c      isoxy     nxy1       int      in     number of rh1 points
c      isoxy     nxy2       int      in     number of rh2 points
c      isoxy     rh1       real      in     value of first  isogon
c      isoxy     rh2       real      in     value of second isogon
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c    1.  The old method of locating the system assumed that only a
c        cyclone or col would be located within each box.  However,
c        testing found that both the col and the cyclone may be found
c        within the box.  Since the old method allowed only one system
c        per box, if the col were found rather than the cyclone the
c        tracking would stop.  90+% of the time, the cyclone was found
c        rather than the col, so this oversite went undetected.
c    2.  During testing so far, the maximum number of systems found has
c        been 2, one col
c        designed to accommodate up to 4 systems per box.
c    3.  Likewise, 10 segments is more than twice the number of segments
c        found thus far during testing.
c    4.  The method of finding the "second" point has also been revised
c        and improved.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c      name              description
c   ------------       --------------------------------------------
c     evaliso          evaluate possible intersection(s)
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c            a1      real       y-coefficient of rh1
c            a2      real       y-coefficient of rh2
c            b1      real       x-coefficient of rh1
c            b2      real       x-coefficient of rh2
c            c1      real       constant of rh1
c            c2      real       constant of rh2
c           cxl      real       array of last x-locations of cx
c           cyl      real       array of last y-locations of cy
c            dd      real       value of determinant
c            d1      real       value of determinant
c            d2      real       value of determinant
c           dx1      real       delta-x of rh1 near intersection
c           dx2      real       delta-x of rh2 near intersection
c           dy1      real       delta-y of rh1 near intersection
c           dy2      real       delta-y of rh2 near intersection
c          dydx      real       slope of rh1 or rh2 near intersection
c           jdd       int       direction of first isogon
c          jj11       int       primary index of rh1
c          jj12       int       secondary index of rh1
c          jj21       int       primary index of rh2
c          jj22       int       secondary index of rh2
c           kdd       int       direction of second isogon
c         maxpc       int       maximum number of prospective
c                               circulations for S/R evaliso
c           ms1       int       starting segmnet index, rh1
c           me1       int       ending segment index, rh1
c            nn       int       running index to system
c            np       int       index to prospective segments
c           npc       int       max allowed prospective systems (out)/
c                               number of prospective systems (in)
c           n1s       int       starting index to rh1 segment
c           n1e       int       ending index to rh1 segment
c           n2s       int       starting index to rh2 segment
c           n2e       int       ending index to rh2 segment
c           ns2       int       starting segment index, rh2
c           ne2       int       ending segment index, rh2
c             r      real       working distance between rh1
c          rmin      real       working minimum distance
c           rmm      real       distance between rh1
c           rmp      real       distance between rh1
c           rpm      real       distance between rh1
c           rpp      real       distance between rh1
c            x1      real       working x-point of rh1
c            xd      real       working x-distance between rh1
c         xx1mn      real       minimum x-distance of rh1 near
c                               intersection
c         xx2mn      real       minimum x-distance of rh2 near
c                               intersection
c            y1      real       working y-point of rh1
c            yd      real       working y-distance between rh1
c
c  METHOD:  1.  Call evaliso to establish the starting and ending
c               indecies to rh1 and rh2 of segments that may contain
c               intersections
c           2.  Evaluate each segment for an intersecion within the
c               regional area defined by the indicies
c           3.  For each intersection found, allowcate the intersection
c               to a system based upon the juxtaposition of the running
c               average location of the previously identified systems.
c               If none are found, start a new system.
c           4.  Maintain the count of intersections supporting each
c               system and the running average location of each system.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          -----------    ---------------------------------------
c           box.inc       common block
c           isoyx.inc     common block
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation with OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      integer maxpc
      parameter (maxpc = 10)
c
      integer jdd,jj11,jj12,jj21,jj22,j901,j902,j1801,j1802,kdd
      integer j1,j2,np,npc,n1s,n1e,n2s,n2e,nn
      integer ms1(maxpc), me1(maxpc), ns2(maxpc), ne2(maxpc)
c
      real a1,a2,b1,b2,c1,c2,c11,c12,c21,c22,dd,d1,d2,dx1,dx2,dy1,dy2
      real dydx,xc,x1,xd,xx1mn,xx2mn,yc,y1,yd,xxs,xxl,yys,yyl
      real r,rmin,rmm,rpm,rpp,rmp,cxl(4),cyl(4)
      real difx,dify,epsln
c
      INCLUDE 'box.inc'
      INCLUDE 'isoxy.inc'
c
      data epsln/0.1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c     write (lbox,*) ' calint, nxy1 ',nxy1,' rh1 ',rh1,' nxy2 ',nxy2,
c    &               ' rh2 ',rh2
c
      jdd = anint (rh1)
      kdd = anint (rh2)
      if (kdd -jdd .eq. 90) then
c
c                   isogons are for directions 90 degrees apart
c
c
c                      evaluate prospects for intersection(s)
c
        npc = maxpc
        call evaliso (nxy1,xx1,yy1, nxy2,xx2,yy2, ms1,me1,ns2,ne2,npc)
        if (npc .gt. 0) then
c
c                   set the last intersection points, for this call to
c                   the S/R, to zero
c
          do nn=1, 4
            cxl(nn) = 0.0
            cyl(nn) = 0.0
          enddo
c
          do np=1, npc
c
c                   extract prospective starting and ending points for
c                   rh1 and rh2 isogons
c
            n1s = ms1(np)
            n1e = me1(np)
            n2s = ns2(np)
            n2e = ne2(np)
c
            rmin = 99999.0
            jj11 = 0
            jj21 = 0
c
c                   locate the indicies to the nearest points of rh1
c                   and rh2 within the two segments defined above
c
            do j1=n1s, n1e
              x1 = xx1(j1)
              y1 = yy1(j1)
              do j2=n2s, n2e
                xd = x1 -xx2(j2)
                yd = y1 -yy2(j2)
                r  = xd*xd +yd*yd
                if (r .lt. rmin) then
c
c                        save the indicies
c
                  rmin = r
                  jj11 = j1
                  jj21 = j2
                endif
              enddo
            enddo
c
c                   the nearest point may not be the first or last point
c                   of the segments - if it is, there is not an
c                   intersection because of the way evaliso establishes
c                   these points
c
            if (jj11 .eq. nxy1) jj11 = -1
            if (jj21 .eq. nxy2) jj21 = -1
            if (jj11 .gt. 1 .and. jj21 .gt. 1) then
c
c                   find "second" point for rh1 and rh2
c                   by finding the next nearest point
c
              xd  = xx1(jj11-1) -xx2(jj21-1)
              yd  = yy1(jj11-1) -yy2(jj21-1)
              rmm = xd*xd +yd*yd
              xd  = xx1(jj11-1) -xx2(jj21+1)
              yd  = yy1(jj11-1) -yy2(jj21+1)
              rmp = xd*xd +yd*yd
              xd  = xx1(jj11+1) -xx2(jj21+1)
              yd  = yy1(jj11+1) -yy2(jj21+1)
              rpp = xd*xd +yd*yd
              xd  = xx1(jj11+1) -xx2(jj21-1)
              yd  = yy1(jj11+1) -yy2(jj21-1)
              rpm = xd*xd +yd*yd
              r   = amin1 (rmm,rmp,rpp,rpm)
              if (r .eq. rmm) then
                jj12 = jj11 -1
                jj22 = jj21 -1
              elseif (r .eq. rmp) then
                jj12 = jj11 -1
                jj22 = jj21 +1
              elseif (r .eq. rpp) then
                jj12 = jj11 +1
                jj22 = jj21 +1
              else
                jj12 = jj11 +1
                jj22 = jj21 -1
              endif
c
c                   assume isogons are straight lines at intersection,
c                   so calculate the a, b, c of equation ay +bx = c
c
c                     calculate for rh1
c
              xx1mn = amin1 (xx1(jj11),xx1(jj12))
              if (xx1mn .eq. xx1(jj11)) then
                j901 = jj11
                j902 = jj12
              else
                j901 = jj12
                j902 = jj11
              endif
              dx1 = xx1(j902) -xx1(j901)
              if (dx1 .ne. 0.0) then
                a1   = dx1
                dy1  = yy1(j902) -yy1(j901)
                b1   = -dy1
                dydx = dy1/dx1
                c11  = yy1(j901) -dydx*xx1(j901)
                c12  = yy1(j902) -dydx*xx1(j902)
                c1   = dx1*(0.5*(c11 +c12))
              else
                a1 = 1.0
                b1 = 0.0
                c1 = xx1(j901)
              endif
c
c                     calculate for rh2
c
              xx2mn = amin1 (xx2(jj21),xx2(jj22))
              if (xx2mn .eq. xx2(jj21)) then
                j1801 = jj21
                j1802 = jj22
              else
                j1801 = jj22
                j1802 = jj21
              endif
              dx2 = xx2(j1802) -xx2(j1801)
              if (dx2 .ne. 0.0) then
                a2   = dx2
                dy2  = yy2(j1802) -yy2(j1801)
                b2   = -dy2
                dydx = dy2/dx2
                c21  = yy2(j1801) -dydx*xx2(j1801)
                c22  = yy2(j1802) -dydx*xx2(j1802)
                c2   = dx2*(0.5*(c21 +c22))
              else
                a2 = 1.0
                b2 = 0.0
                c2 = xx2(j1801)
              endif
c
c                     check that lines intercept
c
              dd = a1*b2 -(b1*a2)
              if (dd .ne. 0.0) then
c
c                       calculate new intercept
c
                d1 = c1*b2 -(b1*c2)
                d2 = a1*c2 -(c1*a2)
                yc  = d1/dd
                xc  = d2/dd
c
c                        establish bounds of regional area
c
                xxs = amin1 (xx1(n1s),xx1(n1e),xx2(n2s),xx2(n2e))
                xxl = amax1 (xx1(n1s),xx1(n1e),xx2(n2s),xx2(n2e))
                yys = amin1 (yy1(n1s),yy1(n1e),yy2(n2s),yy2(n2e))
                yyl = amax1 (yy1(n1s),yy1(n1e),yy2(n2s),yy2(n2e))
c
                if (xc.ge.xxs .and. xc.le.xxl .and. yc.ge.yys .and.
     &              yc.le.yyl) then
c
c                          intercept is within regional area
c
                  if (nsys .eq. 0) then
c
c                          start first system for this box
c
                    nsys    = 1
                    nn      = 1
                    rxc(1)  = xc
                    ryc(1)  = yc
                    nip(1)  = 1
                    cx(1,1) = xc
                    cxl(1)  = xc
                    cy(1,1) = yc
                    cyl(1)  = yc
                  else
c
c                         load intersection in proper system
c
                    do nn=1, nsys
c
c                           ensure same position is not loaded again
c
                      difx = abs (cxl(nn) -xc)
                      dify = abs (cyl(nn) -yc)
                      if (difx.le.epsln .and. dify.le.epsln) goto 220
c
                      difx = abs (rxc(nn) -xc)
                      dify = abs (ryc(nn) -yc)
                      if (difx.le.epsln .and. dify.le.epsln) goto 210
c
                    enddo
c
c                      start new system
c
                    nn = nsys +1
                    if (nn .gt. 4) then
                      write (*,*) ' $ $ calint, ERROR more than 4 cc'
c                     write (33,*) '$ $ calint, ERROR more than 4 cc'
                      goto 900
c
                    endif
 210               continue
                    if (nip(nn) .eq. nint) then
                      write (*,*) ' $ $ calint, ERROR in allocations'
c                     write (33,*) '$ $ calint, ERROR in allocations'
                      goto 220
c
                    endif
                    nip(nn) = nip(nn) +1
                    if (nip(nn) .gt. 1) then
c
c                           calculate running average location
c
                      rxc(nn) = (rxc(nn)*(nip(nn) -1) +xc)/nip(nn)
                      ryc(nn) = (ryc(nn)*(nip(nn) -1) +yc)/nip(nn)
                      cx(nn,nip(nn)) = xc
                      cy(nn,nip(nn)) = yc
                    else
c
c                           load inital position
c
                      rxc(nn) = xc
                      ryc(nn) = yc
                      cx(nn,nip(nn)) = xc
                      cy(nn,nip(nn)) = yc
                      nsys = nn
                    endif
c
c                             load last position to check for duplicates
c
                    cxl(nn) = xc
                    cyl(nn) = yc
                  endif
c                 write (lbox,*) 'calint, ',nn,' ',nip(nn),
c    &              ' intersection at ',xc,' ',yc,' for ',rh1,' ',rh2
c               else
c                 write (lbox,*) ' calint, intersection outside of',
c    &                           ' local region'
                endif
c             else
c               write (lbox,*) ' calint, no intercept'
              endif
c           else
c             write (lbox,*) ' calint, no calculations'
            endif
 220       continue
          enddo
c       else
c         write (lbox,*) 'calint, NO PROSPECTIVE intersections'
        endif
c     else
c       write (lbox,9010) rh1, rh2
c       write (33,9010) rh1, rh2
c9010   format (' rh"s not 90 degreees for ',f7.2,' ',f7.2)
      endif
 900  continue
c     do nn=1, nsys
c       write (33,*) 'CALINT, system ',nn,' intersections ',nip(nn)
c     enddo
c
      end
      subroutine calomega (uu,vv,ratio,ww)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)calomega.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calomega
c
c  DESCRIPTION:  calculate the vertical wind (m/s)
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calomega (uu,vv,ratio,ww)
c
c  PARAMETERS:
c     Name            Type         Usage            Description
c   ---------      ----------     -------  ----------------------------
c      uu            real           input  u-wind component
c      vv            real           input  v-wind component
c      ratio         real           input  delta-p / (2 * grid length)
c      ww            real          in/out  vertical wind
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      double precision  ratio, uu(ixm,jym), vv(ixm,jym), ww(ixm,jym)
c
c         local variables
      integer           i, j
      double precision  emsqr, dudx, dvdy
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do j=2, jym-1
        emsqr = em(j)*em(j)
        do i=2, ixm-1
          dudx    = em(j)*(uu(i+1,j) -uu(i-1,j))
          dvdy    = emsqr*(emi(j+1)*vv(i,j+1) -emi(j-1)*vv(i,j-1))
          ww(i,j) = ww(i,j) -(dudx +dvdy)*ratio
        enddo
      enddo
c
      end
      subroutine calph1 (uu,vv,gz,fphi,phi,u_adv,v_adv,uv)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calph1
c
c  DESCRIPTION:  Use balance equation to calculate phi (gz) field
c                at 1000 hPa
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      double precision  uu(ixm,jym), vv(ixm,jym), gz(ixm,jym)
c
c                  all the following "input" arrays are work arrays
c
      double precision phi(ixm,jym), u_adv(ixm,jym), v_adv(ixm,jym),
     &                 uv(ixm,jym), fphi(ixm-2,jym-2)
c
c     local variables
      integer           i, j, ixs, jys
      double precision  z1, z2, z3, fmax, fmin, adj_f, adj_e, vrt, bet
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ixs = ixm -2
      jys = jym -2
      do j=1, jym
	do i=1, ixm
	  uv(i,j) = uu(i,j)
        enddo
      enddo
c
c               compute advection of u-comp in flux form, in u_adv
c
      call badvec (uu,vv,uv,u_adv)
c
c               compute advection of v-comp in flux form, in v_adv
c
      do j=1, jym
	do i=1, ixm
	  uv(i,j) = vv(i,j)
        enddo
      enddo
      call badvec (uu,vv,uv,v_adv)
c
c               use balance equation
c                   first process advective terms
c
	do j=1, jym-2
	  do i=1, ixm-2
            fphi(i,j) = 0.0d0
	  enddo
	enddo 
        adj_f = 1.0d0/twodel
        do j=3, jym-2
          do i=3, ixm-2
            fphi(i-1,j-1) = adj_f*((u_adv(i+1,j) -u_adv(i-1,j))*em(j)
     &                     +v_adv(i,j+1)*em(j+1) -v_adv(i,j-1)*em(j-1))
          enddo
        enddo
c
c            extrapolate the advective terms to the boundaries
c
        do i=2, ixs-1
          fphi(i,1)   = 2.0d0*fphi(i,2) -fphi(i,3)
          fphi(i,jys) = 2.0d0*fphi(i,jys-1) -fphi(i,jys-2)
        enddo
        do j=2, jys-1
          fphi(1,j)   = 2.0d0*fphi(2,j) -fphi(3,j)
          fphi(ixs,j) = 2.0d0*fphi(ixs-1,j) -fphi(ixs-2,j)
        enddo
c
c            now the corners
c
        z1 = 2.0d0*fphi(2,1) -fphi(3,1)
        z2 = 2.0d0*fphi(1,2) -fphi(1,3)
        z3 = 2.0d0*fphi(2,2) -fphi(3,3)
        fphi(1,1) = 0.25d0*(z1 +z2 +z3 +z3)
c
        z1 = 2.0d0*fphi(ixs-1,1) -fphi(ixs-2,1)
        z2 = 2.0d0*fphi(ixs,2) -fphi(ixs,3)
        z3 = 2.0d0*fphi(ixs-1,2) -fphi(ixs-2,3)
        fphi(ixs,1) = 0.25d0*(z1 +z2 +z3 +z3)
c
        z1 = 2.0d0*fphi(ixs,jys-1) -fphi(ixs,jys-2)
        z2 = 2.0d0*fphi(ixs-1,jys) -fphi(ixs-2,jys)
        z3 = 2.0d0*fphi(ixs-1,jys-1) -fphi(ixs-2,jys-2)
        fphi(ixs,jys) = 0.25d0*(z1 +z2 +z3 +z3)
c
        z1 = 2.0d0*fphi(2,jys) -fphi(3,jys)
        z2 = 2.0d0*fphi(1,jys-1) -fphi(1,jys-2)
        z3 = 2.0d0*fphi(2,jys-1) -fphi(3,jys-2)
        fphi(1,jys) = 0.25d0*(z1 +z2 +z3 +z3)
c
c            add remaining terms of balance equation
c
        do j=2, jym-1
          adj_e = adj_f*em(j)
          do i=2, ixm-2
            vrt = f(j)*adj_f*((vv(i+1,j) -vv(i-1,j))*em(j)
     &               -(uu(i,j+1)*em(j+1) -uu(i,j-1)*em(j-1)))
            bet = adj_e*(uu(i,j)*(f(j+1) -f(j-1)))
            fphi(i-1,j-1) = fphi(i-1,j-1) +vrt -bet
          enddo
        enddo
c
        fmax = -9999.9d0
        fmin = -fmax
        do j=2, jys -1
          do i=2, ixs -1
            fmax = max (fmax,fphi(i,j))
            fmin = min (fmin,fphi(i,j))
          enddo
        enddo
c
        fmax = -9999.9d0
        fmin = -fmax
        do j=1, jys
          do i=1, ixs
            fmax = max (fmax,fphi(i,j))
            fmin = min (fmin,fphi(i,j))
          enddo
        enddo
c
c         Load edges of phi with boundary values
c
	do j=1, jym
	  do i=1, ixm
	    phi(i,j) = 0.0d0
          enddo
	enddo
        do i=1, ixm
          phi(i,1)   = gz(i,1)
          phi(i,jym) = gz(i,jym)
        enddo
        do j=2, jym-1
          phi(1,j)   = gz(1,j)
          phi(ixm,j) = gz(ixm,j)
        enddo
c
c         Use direct solver to obtain balanced mass field in phi
c             note: u_adv is a work array for calstrmf
c
        call calstrmf (fphi,ixm,jym,del,em,phi,u_adv)
c
c         load mass field values back to the real world
c
        do j=1, jym
	  do i=1, ixm
            gz(i,j) = phi(i,j)
	  enddo 
        enddo
c
      end
      subroutine calphk (uu,vv,gz,fphi,phi,u_adv,v_adv,uv)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calphi
c
c  DESCRIPTION:  Use balance equation to calculate phi (gz) fields
c                at the 850, 550
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      double precision  uu(ixm,jym,3), vv(ixm,jym,3), gz(ixm,jym,4)
c
c                  all the following "input" arrays are work arrays
c
      double precision phi(ixm,jym), u_adv(ixm,jym), v_adv(ixm,jym),
     &                 uv(ixm,jym), fphi(ixm-2,jym-2)
c
c     local variables
      integer           i, j, k, ixs, jys
      double precision  z1, z2, z3, fmax, fmin, adj_f, adj_e, vrt, bet
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ixs = ixm -2                 !  k      1     2     3     4
      jys = jym -2                 !  u/v   850   550   250
      do k=1, 3                    !  gz   1000   850   550   250
c
c               compute advection of u-comp in flux form, in u_adv
c
	do j=1, jym
	  do i=1, ixm
            uv(i,j) = uu(i,j,k)
          enddo
        enddo
        call badvec (uu(1,1,k),vv(1,1,k),uv,u_adv)
c
c               compute advection of v-comp in flux form, in v_adv
c
	do j=1, jym
	  do i=1, ixm
            uv(i,j) = vv(i,j,k)
          enddo
        enddo
        call badvec (uu(1,1,k),vv(1,1,k),uv,v_adv)
c
c               use balance equation
c                   first process advective terms
c
	do j=1, jym-2
	  do i=1, ixm-2
            fphi(i,j) = 0.0d0
          enddo
        enddo
        adj_f = 1.0d0/twodel
        do j=3, jym-2
c     adj_e = adj_f*em(j)
          do i=3, ixm-2
            fphi(i-1,j-1) = adj_f*((u_adv(i+1,j) -u_adv(i-1,j))*em(j)
     &                     +v_adv(i,j+1)*em(j+1) -v_adv(i,j-1)*em(j-1))
          enddo
        enddo
c
c            extrapolate the advective terms to the boundaries
c
        do i=2, ixs-1
          fphi(i,1)   = 2.0d0*fphi(i,2) -fphi(i,3)
          fphi(i,jys) = 2.0d0*fphi(i,jys-1) -fphi(i,jys-2)
        enddo
        do j=2, jys-1
          fphi(1,j)   = 2.0d0*fphi(2,j) -fphi(3,j)
          fphi(ixs,j) = 2.0d0*fphi(ixs-1,j) -fphi(ixs-2,j)
        enddo
c
c            now the corners
c
        z1 = 2.0d0*fphi(2,1) -fphi(3,1)
        z2 = 2.0d0*fphi(1,2) -fphi(1,3)
        z3 = 2.0d0*fphi(2,2) -fphi(3,3)
        fphi(1,1) = 0.25d0*(z1 +z2 +z3 +z3)
c
        z1 = 2.0d0*fphi(ixs-1,1) -fphi(ixs-2,1)
        z2 = 2.0d0*fphi(ixs,2) -fphi(ixs,3)
        z3 = 2.0d0*fphi(ixs-1,2) -fphi(ixs-2,3)
        fphi(ixs,1) = 0.25d0*(z1 +z2 +z3 +z3)
c
        z1 = 2.0d0*fphi(ixs,jys-1) -fphi(ixs,jys-2)
        z2 = 2.0d0*fphi(ixs-1,jys) -fphi(ixs-2,jys)
        z3 = 2.0d0*fphi(ixs-1,jys-1) -fphi(ixs-2,jys-2)
        fphi(ixs,jys) = 0.25d0*(z1 +z2 +z3 +z3)
c
        z1 = 2.0d0*fphi(2,jys) -fphi(3,jys)
        z2 = 2.0d0*fphi(1,jys-1) -fphi(1,jys-2)
        z3 = 2.0d0*fphi(2,jys-1) -fphi(3,jys-2)
        fphi(1,jys) = 0.25d0*(z1 +z2 +z3 +z3)
c
c            add remaining terms of balance equation
c
        do j=2, jym-1
          adj_e = adj_f*em(j)
          do i=2, ixm-2
            vrt = f(j)*adj_f*((vv(i+1,j,k) -vv(i-1,j,k))*em(j)
     &               -(uu(i,j+1,k)*em(j+1) -uu(i,j-1,k)*em(j-1)))
            bet = adj_e*(uu(i,j,k)*(f(j+1) -f(j-1)))
            fphi(i-1,j-1) = fphi(i-1,j-1) +vrt -bet
          enddo
        enddo
c
        fmax = -9999.9d0
        fmin = -fmax
        do j=2, jys -1
          do i=2, ixs -1
            fmax = max (fmax,fphi(i,j))
            fmin = min (fmin,fphi(i,j))
          enddo
        enddo
c
        fmax = -9999.9d0
        fmin = -fmax
        do j=1, jys
          do i=1, ixs
            fmax = max (fmax,fphi(i,j))
            fmin = min (fmin,fphi(i,j))
          enddo
        enddo
c
c         Load edges of phi with boundary values
c
	do j=1, jym
	  do i=1, ixm
	    phi(i,j) = 0.0d0
          enddo
        enddo
        do i=1, ixm
          phi(i,1)   = gz(i,1,k+1)
          phi(i,jym) = gz(i,jym,k+1)
        enddo
        do j=2, jym-1
          phi(1,j)   = gz(1,j,k+1)
          phi(ixm,j) = gz(ixm,j,k+1)
        enddo
c
c         Use direct solver to obtain balanced mass field in phi
c             note: u_adv is a work array for calstrmf
c
        call calstrmf (fphi,ixm,jym,del,em,phi,u_adv)
c
c         load mass field values back to the real world
c
        do j=1, jym
	  do i= 1, ixm
            gz(i,j,k+1) = phi(i,j)
          enddo
        enddo
      enddo
c
      end
      subroutine calstrmf (vort,ixm,jym,del,em,strmf,work)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)calstrmf.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calstrmf
c
c  DESCRIPTION:  calculate stream function values, interior
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c         formal parameters
      integer   ixm, jym
      double precision  del, em(jym)
      double precision  vort(ixm-2,jym-2), strmf(ixm,jym), work(ixm*jym)
c
c         local variables
      integer i, j, ixv, jyv, lenwk
      double precision  a(ixm -2), b(ixm -2), c(ixm -2)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ixv = ixm -2
      jyv = jym -2
c
c                    apply weight for solution of Poission
c
      do j=1, jyv
        do i=1, ixv
          vort(i,j) = vort(i,j)*del*del/(em(j+1)*em(j+1))
        enddo
      enddo
c
c                   adjust the boundary values to agree with Dirichlet
c                   conditions for the solution of the streamfunction
c
      do j=2, jym-1
        vort(1,j-1)   = vort(1,j-1)   -strmf(1,j)
        vort(ixv,j-1) = vort(ixv,j-1) -strmf(ixm,j)
      enddo
      do i=2, ixm-1
        vort(i-1,1)   = vort(i-1,1)   -strmf(i,1)
        vort(i-1,jyv) = vort(i-1,jyv) -strmf(i,jym)
      enddo
      a      =  1.0d0
      a(1)   =  0.0d0
      b      = -2.0d0
      c      =  1.0d0
      c(ixv) =  0.0d0
      lenwk  =  ixm*jym
c
c                   Use a direct solver to obtain the solution with
c                       Dirichlet conditions on all four boundaries.
c
      call pois2 (ixv,jyv,a,b,c,vort,work,lenwk)
c
c                 Load center section of input field with solution
c
      do j=2, jym-1
        do i=2, ixm-1
          strmf(i,j) = vort(i-1,j-1)
        enddo
      enddo
c
      end
      subroutine caluphi (pot,ixm,jym,phi,nfor)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)caluphi.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  caluphi
c
c  DESCRIPTION:  calculate phi (gz) for upper levels by hydrostatic Eq.
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c     formal parameters
      integer          ixm, jym, nfor(4)
      double precision pot(ixm,jym,4), phi(ixm,jym,4)
c
c     local variables
      integer          k, i, j, nadj, nfrc
      double precision con 
c
      INCLUDE 'stat2_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nfor(1) = 0
      do k=2, 4
        nadj    = 0
        nfrc    = 0
        nfor(k) = 0
        con     = 502.0d0*(piup(k) -pilo(k))
        do j=1, jym
          do i=1, ixm
c
c                   CHECK STATIC STABILITY
c
            if (pot(i,j,k-1) .gt. pot(i,j,k))
     &          call ptstab (i,j,k,pot,nadj,nfrc)
            phi(i,j,k) = phi(i,j,k-1) -con*(pot(i,j,k-1) +pot(i,j,k))
          enddo
        enddo
        if (nadj .ne. 0 .or. nfrc .ne. 0) then
c         write (20,*) 'CALUPHI, lev ',k,' adj ',nadj,' force ',nfrc
          nfor(k) = nfrc
        endif
      enddo
      nfor(1) = nfor(2)
c
      end
      subroutine calvort (uu,vv,icyc,jcyc,vortmx,wt,vort)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)calvort.f90	1.2  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calvort
c
c  DESCRIPTION:  calcualte vorticity - winds
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      integer icyc, jcyc
      real    wt
      double precision  vortmx, uu(ixm,jym), vv(ixm,jym)
      double precision  vort(ixm-2,jym-2)
c
c         local variables
      integer   i, j, jdis, len
      real      dmod, dist
      double precision  dvdx, dudy, adj_fac
      double precision  wtvort, vortval
c
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'vort_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   base vorticty on winds
c
      vort    = 0.0d0
      adj_fac = 1.0d0/(2.0d0*del)
      do j=2, jym-1
c       adj_emf = em(j)*adj_fac
        do i=2, ixm-1
          dvdx = em(j)*(vv(i+1,j) -vv(i-1,j))
          dudy = em(j+1)*uu(i,j+1) -em(j-1)*uu(i,j-1)
          vort(i-1,j-1) = adj_fac*(dvdx -dudy)
        enddo
      enddo
      if (wt .gt. 0.0) then
c
c                   insert vorticity of model tropical cyclone
c
        dmod   = -2.5
        wtvort = wt*vortmx
        write (*,*) 'calvort, weight ',wt,' IC ',icyc,' JC ',jcyc
c       write(20,*) 'calvort, weight ',wt,' ic ',icyc,' jc ',jcyc
c       write(20,*) 'calvort, max weighted vorticity ',wtvort
c       write(20,*) 'calvort, ijoff ',ijoff,'  rmx ',radmx,'  norm ',
c    &               dnorm
        do j=jcyc-ijoff, jcyc+ijoff
          jdis = (j -jcyc)*(j -jcyc)
          do i=icyc-ijoff, icyc+ijoff
            len  = jdis +(i -icyc)*(i -icyc)
            dist = sqrt (real (len))
            if (dist .lt. radmx) then
              vortval = wtvort*exp (dmod*dist*dnorm)
              if (vortval .gt. 0.0d0) then
                if (vortval .gt. vort(i-1,j-1)) vort(i-1,j-1) = vortval
              else
                if (vortval .lt. vort(i-1,j-1)) vort(i-1,j-1) = vortval
              endif
            endif
          enddo
        enddo
c
c                  establish a uniform rotation representation
c
	call unirota (icyc-1,jcyc-1,ixm-2,jym-2,vort)
      endif
c
      end
      subroutine calwndc (strmf,uu,vv)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)calwndc.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calwndc
c
c  DESCRIPTION:  calculate wind components with stream function values
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      double precision  uu(ixm,jym), vv(ixm,jym), strmf(ixm,jym)
c
c         local varaiables
      integer           i, j, ii, jj
      double precision  twodeli, adj_fac, div, divmx, divmxl
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   compute the non-divergent wind components
c
      twodeli  = 1.0d0/(2.0d0*del)
      do j=2, jym-1
        adj_fac = twodeli*em(j)
        do i=2, ixm-1
c         uu(i,j) = -adj_fac*(strmf(i,j+1) -strmf(i,j-1))
          uu(i,j) = -twodeli*(strmf(i,j+1)*em(j+1)
     &              -strmf(i,j-1)*em(j-1))
          vv(i,j) =  adj_fac*(strmf(i+1,j) -strmf(i-1,j))
        enddo
      enddo
c
c                   check:
c
      twodeli = 1.0d0/twodel
      divmxl = 0.0d0
      divmx  = 0.0d0
      do j=3, jym-2
        do i=3, ixm-2
          div = (uu(i+1,j) -uu(i-1,j))*em(j)
          div = (div +(vv(i,j+1)*em(j+1) -vv(i,j-1)*em(j-1)))*twodeli
          divmx = max (divmx,abs (div))
          if (divmx .gt. divmxl) then
            ii = i
            jj = j
            divmxl = divmx
          endif
        enddo
      enddo
c     write(20,*) 'Max DIV= ',divmx,' I ',ii,' J ',jj,' last ',divmxl
c
      end
      subroutine chkcir (dfld,igx,jgy,nc,isotyp)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)chkcir.f90	1.2  4/3/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  chkcir
c
c  DESCRIPTION:  determine type of circulation
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call chkcir (dfld,igx,jgy,nc,isotyp)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     dfld         real         in      wind direction (to) array
c      igx          int         in      first  dimension of dfld
c      jgy          int         in      second dimension of dfld
c       nc          int         in      index to intersection
c   isotyp         real         out     type of circulation found
c                                         4 - ccw flow 4 out of 4
c                                         3 - ccw flow 3 out of 4
c                                         0 - col or no evaluation
c                                        -4 - cw flow 4 out of 4
c                                        -3 - cw flow 3 out of 4
c
c  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
c                              ARE DEFINED IN THE CODE WITHIN INCLUDE
c                              FILES.  THIS MODULE USES THE FOLLOWING
c                              VARIABLES FROM THESE COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c       box       rxc      real      in     x-location of intersection
c       box       ryc      real      in     y-location of intersection
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c    Name          Description
c   --------       -----------------------------------------------------
c   avgddt         calculate weighted average wind
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dde        real       wind direction at East-point
c         ddn        real       wind direction at North-point
c         dds        real       wind direction at South-point
c         ddw        real       wind direction at West-point
c         fi         real       fractional i grid-length to "center line"
c         fj         real       fractional j grid-length to "center line"
c         ichk        int       sum of winds within window
c         ixce        int       eastern-edge index
c         jycn        int       northern-edge index
c         jycs        int       southern-edge index
c         ixcw        int       western-edge index
c
c  METHOD:  1.  Check wind direction at cardinal points about
c               intersection.
c           2.  If 3 or 4 agree with cw or ccw flow
c               assign isotyp +sum for ccw and -sum for cw flow.
c           3.  Else, assign isotyp a 0
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------    ---------------------------------------
c           box.inc        common block
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation with OTCM
c
c  <<CHANGE NOTICE>>  Version 1.2  (09 APR 1997) -- Hamilton, H.
c    Modify how representative winds are selected
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer igx, jgy, nc, isotyp
      real    dfld(igx,jgy)
c
c         local variables
      integer ixcw, ixce, jycs, jycn, ichk
      real    fi, fj, ddn,dds,dde,ddw, avgddt
c
      include 'box.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   obtain north, south, west and east indicies
c                   about isogon intersection
c
      isotyp = 1
      ixcw   = anint (rxc(nc))
      if (ixcw .gt. rxc(nc)) ixcw = ixcw -1
      ixce = ixcw +1
      if (ixcw .lt. 1 .or. ixce .gt. igx) isotyp = 0
      fi   = rxc(nc) -ixcw
      jycs = anint (ryc(nc))
      if (jycs .gt. ryc(nc)) jycs = jycs -1
      jycn = jycs +1
      fj   = ryc(nc) -jycs
      if (jycs .lt. 1 .or. jycn .gt. jgy) isotyp = 0
      if (isotyp .eq. 1) then
c
c                   obtain wind directions north, south, west and east
c                   of isogon intersection
c                   note, directions are toward not from.
c
        if (fi .ge. 0.2 .and. fi .le. 0.8 .and.
     &      fj .ge. 0.2 .and. fj .le. 0.8) then
            ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),fi)
          dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),fi)
          ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),fj)
          dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),fj)
        elseif (fj .ge. 0.2 .and. fj .le. 0.8) then
          if (fi .lt. 0.2) then
            ddn = dfld(ixcw,jycn)
            dds = dfld(ixcw,jycs)
            ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),fj)
            dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),fj)
          else
            ddn = dfld(ixce,jycn)
            dds = dfld(ixce,jycs)
            ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),fj)
            dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),fj)
          endif
        elseif (fi .ge. 0.2 .and. fi .le. 0.8) then
          if (fj .lt. 0.2) then
            ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),fi)
            dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),fi)
            ddw = dfld(ixcw,jycs)
            dde = dfld(ixce,jycs)
          else
            ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),fi)
            dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),fi)
            ddw = dfld(ixcw,jycn)
            dde = dfld(ixce,jycn)
          endif
        elseif (fi .lt. 0.2) then
          if ( fj .lt. 0.2) then
            if (jycs .gt. 1 .and. ixcw .gt. 1) then
              ddn = dfld(ixcw,jycn)
              dds = dfld(ixcw,jycs-1)
              ddw = dfld(ixcw-1,jycs)
              dde = dfld(ixce,jycs)
            else
              isotyp = 0
            endif
          else
            if (ixcw .gt. 1 .and. jycn .lt. jgy) then
              ddn = dfld(ixcw,jycn+1)
              dds = dfld(ixcw,jycs)
              ddw = dfld(ixcw-1,jycn)
              dde = dfld(ixce,jycn)
            else
              isotyp = 0
            endif
          endif
        elseif (fj .lt. 0.2) then
          if (jycs .gt. 1 .and. ixce .lt. igx) then
            ddn = dfld(ixce,jycn)
            dds = dfld(ixce,jycs-1)
            ddw = dfld(ixcw,jycs)
            dde = dfld(ixce+1,jycs)
          else
            isotyp = 0
          endif
        else
          if (ixce .lt. igx .and. jycn .lt. jgy) then
            ddn = dfld(ixce,jycn+1)
            dds = dfld(ixce,jycs)
            ddw = dfld(ixcw,jycn)
            dde = dfld(ixce+1,jycn)
          else
            isotyp = 0
          endif
        endif
      endif
      if (isotyp .eq. 1) then
c
c                   check the type of flow pattern associated with
c                   isogon intersection
c
c                     check for:  cyclonic circulation, nh
c                                 anticyclonic circulation, sh
c
        ichk = 0
        if (ddn  .ge. 210.0 .and. ddn .le. 315.0) ichk = ichk +1
        if (ddw  .ge. 120.0 .and. ddw .le. 225.0) ichk = ichk +1
        if (dds  .ge. 030.0 .and. dds .le. 135.0) ichk = ichk +1
        if ((dde .ge. 000.0 .and. dde .le. 045.0) .or.
     &    (dde .ge. 300.0 .and. dde .le. 360.0)) ichk = ichk +1
c
        if (ichk .ge. 3) then
c                   closed circulation found
          isotyp = ichk
        else
c
c                   check for anticyclonic circulation, nh
c                                 cyclonic circulation, sh
c
          ichk = 0
          if (ddn  .ge. 045.0 .and. ddn .le. 150.0) ichk = ichk +1
          if (dde  .ge. 135.0 .and. dde .le. 240.0) ichk = ichk +1
          if (dds  .ge. 225.0 .and. dds .le. 330.0) ichk = ichk +1
          if ((ddw .ge. 000.0 .and. ddw .le. 060.0) .or.
     &        (ddw .ge. 315.0 .and. ddw .le. 360.0)) ichk = ichk +1
          if (ichk .ge. 3) then
c                   closed circulation found
            isotyp = -ichk
          else
c
c                   flow appears to be a col
c
            isotyp = 0
          endif
        endif
      endif
c
      end
      subroutine chkdat (nrk,mxk,cline,kk)
c
c
c
      implicit none
c
c         formal parameters
      integer nrk, mxk, kk
      character*80 cline
c
c         local variables
      integer ks, kc, k, j
      character*1  cx
      character*10 strng
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ks = 0
      kk = 0
      kc = 0
      do k=1, mxk
        cx = cline(k:k)
        if (cx .ne. ' ') then
          if (ks .eq. 0) ks = k
          kk = k
          kc = kc +1
        elseif (ks .ne. 0) then
          goto 100
c
        endif
      enddo
  100 continue
      if (nrk .le. 10) then
        if (kc .lt. nrk) then
c
c                   load output with leading zeros
c
          strng = ' '
          j     = nrk +1
          do k=kk, ks, -1
            j = j -1
            strng(j:j) = cline(k:k)
          enddo
          do k=1, j-1
            strng(k:k) = '0'
          enddo
          kk    = nrk
          cline = ' '
          cline(1:kk) = strng(1:kk)
        endif
      endif
c
      end
      subroutine cirloc (dfld,ixgrd,jygrd,imin,jmin,imax,jmax,nhsh,
     &                   kccf,kuvs,kint,xc,yc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)cirloc.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cirloc
c
c  DESCRIPTION:  driver routine for locating circulation with isogons
c
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call cirloc (dfld,ixgrd,jygrd,imin,jmin,imax,jmax,nhsh,
c                       kccf,kuvs,kint,xc,yc)
c
c  PARAMETERS:
c     NAME        TYPE      USAGE             DESCRIPTION
c   --------     ------     ------   ------------------------------
c      dfld       real        in     wind direction field, deg
c     ixgrd        int        in     first  dimension of field
c     jygrd        int        in     second dimension of field
c      imin        int        in     first  dimension start of window
c      jmin        int        in     second dimension start of window
c      imax        int        in     first  dimension end of window
c      jmax        int        in     second dimension end of window
c      kccf        int       out     number of cyclones found
c      kuvs        int       out     wind support factor
c                                      0 - no circulation, col
c                                      3 - three quads, cyclonic
c                                      4 - four quads, cyclonic
c      kint        int       out     number of isogons
c                                    1 - 9 - cyclone found
c                                      -77 - no intersection found
c                                      -88 - no isogons produced
c        xc       real       out     x-grid (lon) cyclone location
c        yc       real       out     y-grid (lat) cyclone location
c
c  CALLED BY:  cirloc.f
c
c  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
c                              ARE DEFINED IN THE CODE WITHIN INCLUDE
c                              FILES.  THIS MODULE USES THE FOLLOWING
c                              COMMON BLOCKS:
c
c      BLOCK    NAME    TYPE   USAGE              NOTES
c     -------  ------   ----   ------   -------------------------------
c       box     lbox     int    out     output unit number
c                 xs    real    out     starting first dim of isogon box
c                 xl    real    out     ending first dim of isogon box
c                 ys    real    out     starting second dim isogon box
c                 yl    real    out     ending second dim of isogon box
c                rxc    real    out     running x-grid location
c                ryc    real    out     running y-grid location
c                nip     int    out     number of intersections
c      view     mini     int    out     starting first dim of isogon box
c               maxi     int    out     ending first dim of isogon box
c               minj     int    out     starting second dim isogon box
c               maxj     int    out     ending second dim of isogon box
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     bad  first dimension     write diagnostic, correct error
c     bad second dimension     write diagnostic, correct error
c     no isogons produced      set flag, write diagnostic and return
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c          isocnt     driver routine for producing isogons
c         calcntr     calculate centroid of isogon intersections
c          chkcir     check type of circulation found
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           ixg       int       first  dimension of windowed dd-field
c           jyg       int       second dimension of windowed dd-field
c           ncc       int       number of cyclonic circulations found
c
c  METHOD:  1) Establish size and location of local grid for
c              constructing isogons.
c           2) Load grid with wind direction values.
c           3) Load common blocks for constructing isogons.
c           4) Construct isogons and determine if there are
c              intersections within the box.
c           5) If one or more systems of intersections are found,
c              determine center of each and the synoptic system that
c              the center(s) represent.
c           6) For each, cyclonic center found load the following:
c              a.   wind support by quadrants (must be 3 or 4)
c              b.   number of intersections used to determine location
c              c.   global grid location of cyclone
c           7) Pass on the number of cyclones found.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          -----------    ---------------------------------------
c             box.inc     common block
c            view.inc     common block
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation with OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer ixgrd, jygrd, imin, jmin, imax, jmax, nhsh
      integer kccf, kuvs(4), kint(4)
      real dfld(ixgrd,jygrd), xc(4), yc(4)
c
c         local variables
      integer ixg, jyg
      parameter (ixg = 7, jyg = 7)
c
      integer is, ie, js, je, n, j, m, i, ii, ix, jy, ibyj, kntr
      integer ncc, nn, k
      integer ktyp(4), kcc(4)
      real    ddgrd(ixg,jyg)
c
      INCLUDE 'view.inc'
c
      INCLUDE 'box.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   load local grid, ddgrd, with wind directions.
c                   allow for crossing 0 longitude, which will probably
c                   never happen, for software engineering's sake.
c
      is = imin -1
      if (is .lt. 1) is = ixgrd +is
      ie = imax +2
      if (ie .lt. is) ie = ixgrd +ie
      if (ie -is .gt. ixg -1) then
        ie = is +ixg -1
        write (20,*) ' CIRLOC, warning -- first dimension too big.'
      endif
      js = jmin -1
      je = jmax +2
      if (je -js .gt. jyg -1) then
        je = js +jyg -1
        write (20,*) ' CIRLOC, warning -- second dimension too big.'
      endif
c
      n = 0
      do j=js, je
        n = n +1
        m = 0
        do i=is, ie
          ii = i
          if (ii .gt. ixgrd) ii = ii -ixgrd
          m = m +1
          ddgrd(m,n) = dfld(ii,j)
        enddo
      enddo
c
c                   load isogon common blocks
c
      mini = 2
      xs   = 2.0
      maxi = 5
      xl   = 5.0
      minj = 2
      ys   = 2.0
      maxj = 5
      yl   = 5.0
      ix   = ixg
      jy   = jyg
      ibyj = ix*jy
      nsys = 0
      do n=1, 4
        rxc(n)  = 0.0
        ryc(n)  = 0.0
        nip(n)  = 0
        ktyp(n) = 0
        do m=1, 10
          cx(n,m) = 0.0
          cy(n,m) = 0.0
        enddo
      enddo
c     lbox =  9
c     open (lbox,file='xyboxd',form='formatted')
c     write (9,*) ' cirloc, x-box, fm ',mini,' to ',maxi,' y-box, fm '
c    &            ,minj,' to ',maxj,' for cntr near ',xc(1),' ',yc(1)
c
c                   calculate isogons and determine if there is an
c                   intersection(s) within the box, if there is an
c                   interection determine the type of flow depicted
c                   by the isogons for each.
c
      kntr = 0
      call isocnt (ddgrd,ix,jy,ibyj,kntr)
      if (kntr .gt. 0) then
c
c                   isogons were created
c
        if (nsys .gt. 0) then
c
c                     nsys isogon centers were found
c
          ncc = 0
          do n=1, nsys
            kcc(n) = 0
            if (rxc(n).gt.0.0 .and. ryc(n).gt.0.0) then
c
c                   running intersection is available, if there are
c                   more than 2 intersections, locate centroid
c
              nn = n
              if (nip(n) .gt. 2) call calcntr (nn)
c             write (9,*) 'cirloc, intersection at ',rxc(n),' ',ryc(n)
c
c                   check type of circulation found with isogons
c
              call chkcir (ddgrd,ix,jy,nn,ktyp(n))
c
c                   evaluate output from isogons
c
              if (ktyp(n) .ne. 0)  then
c               write (9,*) 'cirloc, found circulation, type ',ktyp(n)
c               write(33,*) 'cirloc, found circulation, type ',ktyp(n)
              endif
              if (iabs (ktyp(n)) .ge. 3) then
                if (nhsh.gt.0 .and. ktyp(n).gt.0) then
c
c                   closed cyclonic circulation found in NH
c
                  ncc    = ncc +1
                  kcc(n) = -1
c                 write(33,*) 'cirloc, found cyclone for location ',n
                elseif (nhsh.lt.0 .and. ktyp(n).le.-3) then
c
c                   closed cyclonic circulation found in SH
c
                  ncc    = ncc +1
                  kcc(n) = -1
c                 write(33,*) 'cirloc, found cyclone for location ',n
c               else
c                 write(33,*) 'cirloc, found anti-cyclone for ',
c    &                        'location ',n
                endif
c             else
c               write (9,*) 'cirloc, found a col for location ',n
c               write(33,*) 'cirloc, found a col for location ',n
              endif
            endif
          enddo
          if (ncc .gt. 0) then
            k = 0
            do n=1, nsys
              if (kcc(n) .lt. 0) then
c
c                   good cyclonic circulation found
c
                k = k +1
                kuvs(k) = iabs (ktyp(n))
                kint(k) = nip(n)
                xc(k)   = float (is -1) +rxc(n)
                yc(k)   = float (js -1) +ryc(n)
c               write(33,*) 'cirloc, ',k,' qds ',kuvs(k),' int ',kint(k)
              endif
            enddo
            kccf = k
          else
            kccf = -1
c           write (9,*) 'circloc, no cyclones found near ',xc(1),' ',
c    &                   yc(1)
c           write(33,*) 'circloc, no cyclones found near ',xc(1),' ',
c    &                   yc(1)
c           write(20,*) 'circloc, NO CYCLONES found near ',xc(1),' ',
c    &                   yc(1)
          endif
        else
          kccf = -77
c         write (9,*) 'cirloc, no intersection found near ',xc(1),' ',
c    &                 yc(1)
c         write(33,*) 'cirloc, no intersection found near ',xc(1),' ',
c    &                 yc(1)
c         write(20,*) 'cirloc, NO INTERSECTION found near ',xc(1),' ',
c    &                 yc(1)
        endif
      else
        kccf = -88
c       write (9,*) 'cirloc, no isogons produced $$$$$'
c       write(33,*) 'cirloc, no isogons produced $$$$$'
c       write(20,*) 'cirloc, NO ISOGONS produced $$$$$'
      endif
c     close (lbox)
c
      end
      subroutine confirm (nhsh,ddfld,ixgd,jygd,mxptc,cirdat,nccf)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)confirm.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  confirm
c
c  DESCRIPTION:  driver to track tropical cyclones
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call confirm (nhsh,ddfld,ixgd,jygd,mxptc,cirdat,nccf)
c
c  PARAMETERS:
c     NAME       TYPE     USAGE           DESCRIPTION
c   --------    ------    ------    ------------------------------
c     nhsh        int       in      hemisphere flag, +NH, - SH
c    ddfld       real       in      wind direction field, deg
c     ixgd        int       in      first  dimension of ddfld
c     jygd        int       in      second dimension of ddfld
c   cirdat       real     in/out    circulation data
c                                     (1, first  dimension location
c                                     (2, second dimension location
c                                     (3, wind support factor, 3 or 4
c                                     (4, intersection support, 2 - 8
c     nccf        int     in/out    number of prospective cc's/
c                                   number of verified cc's
c
c  CALL BY:  setngcnt.f
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         isofnd      driver routine for locating cyclone with isogons
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          ccvdat    real       working array of cirdat
c          exc       real       estimated first  dimension location
c          eyc       real       estimated second dimension location
c          iadd       int       flag for keeping cyclone
c          iloc       int       cyclone location flag, 0 not found
c          kc         int       total count of verified cyclones
c          kccf       int       count of verified cc's per area
c          kint       int       array of intersection counts
c          kuvs       int       array of quadrant wind support counts
c          xc        real       array of x-grid location of cyclone(s)
c          yc        real       array of y-grid location of cyclone(s)
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (19 MAR 1997) -- Hamilton, H.
c    Initial installation in OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c     formal argumnets
      integer nhsh, ixgd, jygd, mxptc, nccf
      real    ddfld(ixgd,jygd), cirdat(4,mxptc)
c
c     local variables
      integer n, k, kk, kccf, kc, iadd
      integer kuvs(4), kint(4)
      real    exc, eyc, xc(4), yc(4), ccvdat(2,mxptc)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do n=1, nccf
        ccvdat(1,n) = cirdat(1,n)
        ccvdat(2,n) = cirdat(2,n)
        cirdat(1,n) = 0.0
        cirdat(2,n) = 0.0
        cirdat(3,n) = 0.0
        cirdat(4,n) = 0.0
      enddo
c
c               search for cyclonic centers based upon isogons
c
      kc = 0
      do n=1, nccf
        exc = ccvdat(1,n)
        eyc = ccvdat(2,n)
        call isofnd (exc,eyc,nhsh,ddfld,ixgd,jygd,kccf,kuvs,kint,xc,yc)
        if (kccf .gt. 0) then
c
c                 circulation center found with isogons
c
c         write (20,*) ' isofnd found ',kccf,' cyclones for area ',n
          do k=1, kccf
c           write (20,*) 'cyclone ',k,' is at ',xc(k),'  ',yc(k)
            if (kc .eq. 0) then
              kc = 1
              cirdat(1,1) = xc(k)
              cirdat(2,1) = yc(k)
              cirdat(3,1) = kuvs(k)
              cirdat(4,1) = kint(k)
            else
c
c                 do not add duplicate position
c
              iadd = -1
              do kk=1, kc
                if (abs (cirdat(1,kk) -xc(k)) .le. 0.1) then
                  if (abs (cirdat(2,kk) -yc(k)) .le. 0.1) iadd = 0
                endif
              enddo
              if (iadd .eq. -1) then
c
c                 add new cyclone location to cirdat
c
                kc = kc +1
                if (kc .le. mxptc) then
                  cirdat(1,kc) = xc(k)
                  cirdat(2,kc) = yc(k)
                  cirdat(3,kc) = kuvs(k)
                  cirdat(4,kc) = kint(k)
                endif
              endif
            endif
          enddo
        endif
      enddo
      if (kc .gt. mxptc) then
c       write (*,*) 'ERROR: confirm, cirdat too small, needed = ',kc
        kc = mxptc
      endif
      nccf = kc
c     write (20,*) 'Confirm, retained ',nccf,' cyclones'
c
      end
      subroutine cosgen (n,m1,m2,pi,tcos,n2)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)cosgen.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cosgen
c
c  DESCRIPTION:  generate cosine terms
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c         formal parameters
      integer           n, m1, m2, n2
      double precision  TCOS(n2), pi
c
c         local variables
      integer           kkk, kk, k, i
      double precision  x
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      KK = 0
      DO K=1, N
        DO I=1, M1
          X   = real (K) -float (I)/(real (M1) +1.0)
          KKK = KK +I
          TCOS(KKK) = 2.0d0*cos (X*PI/N)
        enddo
        KK = KK +M1
      enddo
      IF (M2 .gt. 0) then
        DO K=1, N
          DO I=1, M2
            X   = real (K) -real (I)/(real (M2) +1.0d0)
            KKK = KK +I
c           if (kkk > n2) write (*,*) 'cosgen, over index of tcos= ',kkk -n2
            TCOS(KKK) = 2.0d0*cos (X*PI/N)
          enddo
          KK = KK + M2
        enddo
      endif
c
      end
      REAL FUNCTION CYCIT1 (RML,RNL,BFLD,MGRD,NGRD)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)cycit1.f	1.1 12/22/93 
C                        23:21:46 /home/library/util/cycit1/src/SCCS/s.cycit1.f
C
C  CONFIGURATION IDENTIFICATION: NONE
C
C  MODULE NAME: CYCIT1
C
C  DESCRIPTION:  INTERPOLATE FIELD, BFLD, WHICH IS CYCLIC IN THE FIRST
C                DIMENSION, BASED UPON AYRES CENTRAL DIFFERENCE FORMULA
C                WHICH PRODUCES VALUES THAT ARE CONTINUOUS IN THE FIRST
C                DERIVATIVE, EXCEPT NEAR LIMITS OF SECOND DIMENSION,
C                WHERE BILINEAR INTERPOLATION IS USED.
C
C  COPYRIGHT:                  (C) 1993 FLENUMMETOCCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  NONE
C
C  REFERENCES: NONE
C  
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  BFLD MUST BE 4 BY 4 OR LARGER FIELD AND CYCLIC IN
C                 FIRST DIMENSION
C
C  COMPUTER/OPERATING SYSTEM 
C               DEPENDENCIES:  UNIX Operating System
C
C  LIBRARIES OF RESIDENCE: /usr/local/fnoc/lib/libfnoc.a
C
C  USAGE:  VAL = CYCIT1 (RML,RNL,BFLD,MGRD,NGRD)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       RML         REAL         IN     FIRST  DIMENSION POINT LOCATION
C       RNL         REAL         IN     SECOND DIMENSION POINT LOCATION
C       BFLD        REAL         IN     FIELD  FOR INTERPOLATION
C       MGRD         INT         IN     FIRST  DIMENSION OF BFLD
C       NGRD         INT         IN     SECOND DIMENSION OF BFLD
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C    NONE     
C
C  ERROR CONDITIONS:
C    Since cycit1 is a function, the out-of-bounds error condition re-
C    turns a large negative number (-999999999.00).
C
C  ADDITIONAL COMMENTS:
C           1.  IF SECOND DIMENSION LOCATION IS OUT-OF-BOUNDS,
C               IT'S REPRESENTATIVE IS MADE IN BOUNDS.
C           2.  NO CHECK IS MADE ON IN-BOUNDS FOR FIRST DIMENSION
C               LOCATION.  APPROX. RANGE: (-MGRD < RmL < 2*MGRD)
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C             AA     REAL       INTERPOLATION FACTOR
C             BB     REAL       INTERPOLATION FACTOR
C             BV     REAL       Temporary store of array value
C             CC     REAL       INTERPOLATION FACTOR
C          EV3M1     REAL       INTERPOLATION FACTOR
C          EV3M2     REAL       INTERPOLATION FACTOR
C          EV4M2     REAL       INTERPOLATION FACTOR
C            ECV     REAL       INTERPOLATED ROW OR COLUMN VALUES
C                               FOR FINAL INTERPOLATION
C             M2      INT       TRUNCATED FIRST DIMENSION POINT LOCATION
C             M3      INT       M2 +1
C             N2      INT       TRUNCATED SECOND DIMENSION LOCATION
C             N3      INT       N2 +1
C              R     REAL       FRACTION OF FIRST DIMENSION OF GRID
C                               POINT IS LOCATED FROM M2
C             RN     REAL       REAL REPRESENTATIVE OF RNL
C             RM     REAL       REAL REPRESENTATIVE OF RML
C              S     REAL       FRACTION OF SECOND DIMENSION OF GRID
C                               POINT IS LOCATED FROM N2
C           VFLD     REAL       BLOCK OF VALUES USED FOR INTERPOLATION
C
C  METHOD:  AYRES CENTRAL DIFFERENCE FORMULA USED IN TWO DIMENSIONS
C
C  INCLUDE FILES: NONE
C
C  COMPILER DEPENDENCIES:  NONE
C
C  COMPILE OPTIONS:  NONE
C
C  MAKEFILE:  */cycit1/src/makefile
C
C  RECORD OF CHANGES: NONE
C
C
C...................END PROLOGUE.......................................
C
C         FORMAL PARAMETERS
C
      IMPLICIT NONE

      INTEGER MGRD,NGRD
      REAL RML, RNL, BFLD(MGRD,NGRD)
C
C         LOCAL VARIABLES
C
      INTEGER M2, N2, M3, N3, K, N, M, I
      REAL EV3M1, EV3M2, EV4M2, AA, BB, CC, RN, RM, R, S
      REAL ECV(4), VFLD(16), BV
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C
      IF (MGRD.GE.4 .AND. NGRD.GE.4) THEN
C
        Rn = RnL
        n2 = Rnl
C                   MAKE second DIMENSION LOCATION IN BOUNDS
        IF (n2 .LT. 1) THEN
          n2 = 1
          Rn = 1.0
        ELSEIF (n2 .GT. nGRD) THEN
          n2 = nGRD
          Rn = nGRD
        ENDIF
C
        rm = rml
        m2 = rml
        R  = RM -M2
        S  = RN -N2
        IF (n2.GE.2 .AND. n2.LT.(nGRD -1)) THEN
C
C                   PERFORM INTERPOLATION BASED UPON AYRES
C
          K  = 0
C                   LOAD 4-BY-4 ARRAY, VFLD, FOR INTERPOLATION
          DO 120 n=n2-1, n2+2, 1
            DO 110 m=m2-1, m2+2, 1
              i = m
              IF (i .LE. 0) THEN
                i = mGRD +i
              ELSEIF (i .GT. mGRD) THEN
                i = i -mGRD
              ENDIF
              K = K +1
              VFLD(K) = BFLD(i,n)
  110       CONTINUE
  120     CONTINUE
C
C                   PERFORM AYRES CENTRAL DIFFERENCES AND INTERPOLATION,
C                   FOUR TIMES TO LOAD ECV
C
          DO 130 K=1, 4
            EV3M1  = VFLD(K+8) -VFLD(K)
            EV3M2  = VFLD(K+8) -VFLD(K+4)
            EV4M2  = 0.5*(VFLD(K+12) -VFLD(K+4))
            AA     = 0.5*EV3M1
            BB     = 3.0*EV3M2 -EV3M1 -EV4M2
            CC     = AA +EV4M2 -EV3M2 -EV3M2
            ECV(K) = VFLD(K+4) +S*(AA +S*(BB +S*CC))
  130     CONTINUE
C
C                   PERFORM AYRES CENTRAL DIFFERENCES WITH ECV
C
          EV3M1  = ECV(3) -ECV(1)
          EV3M2  = ECV(3) -ECV(2)
          EV4M2  = 0.5*(ECV(4) - ECV(2))
          AA     = 0.5*EV3M1
          BB     = 3.0*EV3M2 -EV3M1 -EV4M2
          CC     = AA +EV4M2 -EV3M2 -EV3M2
          CYCIT1 = ECV(2) +R*(AA +R*(BB +R*CC))
C
        ELSE
C
C                   PERFORM BILINEAR INTERPOLATION
C                   BUT USE CYCLIC CONDITIONS OF FIRST DIMENSION
C
          IF (m2 .LE. 0) THEN
            m2 = mGRD +m2
          ELSEIF (m2 .GT. mGRD) THEN
            m2 = m2 -mGRD
          ENDIF
          M3 = M2 +1
          IF (m3 .LE. 0) THEN
            m3 = mGRD +m3
          ELSEIF (m3 .GT. mGRD) THEN
            m3 = m3 -mGRD
          ENDIF
          BV = BFLD(M2,N2)
          IF (Rn.EQ.1.0 .OR. n2.EQ.nGRD) THEN
            CYCIT1 = BV +R*(BFLD(M3,N2) -BV)
          ELSE
            N3 = N2 +1
            CYCIT1 = BV +R*(BFLD(M3,N2) -BV) +S*(BFLD(M2,N3) -BV)
     .              +R*S*(BFLD(M3,N3) +BV -BFLD(M3,N2) -BFLD(M2,N3))
          ENDIF
        ENDIF
      ELSE
C
C                   ERROR VALUE RETURNED, BFLD MUST BE 4 BY 4 OR LARGER
C
        CYCIT1 = -999999999.0
      ENDIF
      RETURN
C
      END
      double precision function cycitr8 (rml,rnl,bfld,ix,jy)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION: @(#)cycitr8.f90	1.1  6/3/96
c
c  MODULE NAME:  CYCITR8
c
c  DESCRIPTION:  INTERPOLATE FIELD, BFLD, WHICH IS A REGION FIELD OF
c                (KIND = 8) VALUES.
c                BASED UPON AYRES CENTRAL DIFFERENCE FORMULA WHICH
c                PRODUCES VALUES THAT ARE CONTINUOUS IN THE FIRST
c                DERIVATIVE, EXCEPT NEAR LIMITS OF THE GRID,
c                WHERE BILINEAR INTERPOLATION IS USED.
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  FNMOC SUBROUTINE WRITEUP FOR CYCIT1
c
c  CLASSIFICATION:  UNCLASSIFIED
c
c  RESTRICTIONS:  BFLD MUST BE 4 BY 4 OR LARGER FIELD
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  NONE
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  VAL = CYCITR8 (RML,RNL,BFLD,MGRD,NGRD)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c       RML         REAL         IN     FIRST  DIMENSION POINT LOCATION
c       RNL         REAL         IN     SECOND DIMENSION POINT LOCATION
c       BFLD        REAL         IN     FIELD  FOR INTERPOLATION
c       MGRD         INT         IN     FIRST  DIMENSION OF BFLD
c       NGRD         INT         IN     SECOND DIMENSION OF BFLD
c
c  COMMON BLOCKS:  NONE
c
c  FILES:  NONE
c
c  DATA BASES:  NONE
c
c  NON-FILE INPUT/OUTPUT:  NONE
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     BFLD TOO SMALL           SET CYCITR8 TO ERROR VALUE
c     OUT-OF-BOUNDS            SET CYCITR8 TO ERROR VALUE
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  NONE
c
c  LOCAL VARIABLES:
c
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c             AA     REAL       INTERPOLATION FACTOR
c             BB     REAL       INTERPOLATION FACTOR
c             CC     REAL       INTERPOLATION FACTOR
c          EV3M1     REAL       INTERPOLATION FACTOR
c          EV3M2     REAL       INTERPOLATION FACTOR
c          EV4M2     REAL       INTERPOLATION FACTOR
c            ECV     REAL       INTERPOLATED ROW OR COLUMN VALUES
c                               FOR FINAL INTERPOLATION
c             M2      INT       TRUNCATED FIRST DIMENSION POINT LOCATION
c             M3      INT       M2 +1
c             N2      INT       TRUNCATED SECOND DIMENSION LOCATION
c             N3      INT       N2 +1
c              R     REAL       FRACTION OF FIRST DIMENSION OF GRID
c                               POINT IS LOCATED FROM M2
c             RN     REAL       REAL REPRESENTATIVE OF RNL
c             RM     REAL       REAL REPRESENTATIVE OF RML
c              S     REAL       FRACTION OF SECOND DIMENSION OF GRID
c                               POINT IS LOCATED FROM N2
c           VFLD     REAL       BLOCK OF VALUES USED FOR INTERPOLATION
c
c  METHOD:  AYRES CENTRAL DIFFERENCE FORMULA USED IN TWO DIMENSIONS
c
c  INCLUDE FILES: NONE
c
c  COMPILER DEPENDENCIES:  FORTRAN 90
c
c  COMPILE OPTIONS:  STANDARD FNOC OPERATIONAL OPTIONS
c
c  MAKEFILE:  N/A
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1   (05 JUN 1996)   H. Hamilton
c    initial installation of software on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c     formal parameters
c
      integer           ix, jy
      double precision  rml, rnl, bfld(ix,jy)
c
c     local variables
c
      integer           m2, n2, m3, n3, k, n, m
      double precision  ev3m1, ev3m2, ev4m2, aa, bb, cc, rn, rm, r, s
      double precision  bv, ecv(4), vfld(16)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (ix .ge. 4 .and. jy .ge. 4) then
c
        rm = rml
        m2 = rml
        r  = rm -m2
        rn = rnl
        n2 = rnl
        s  = rn -n2
        if (m2.ge.2 .and. m2.lt.(ix-1) .and.
     &      n2.ge.2 .and. n2.lt.(jy-1)) then
c
c                   PERFORM INTERPOLATION BASED UPON AYRES
c
          k = 0
c                   LOAD 4-BY-4 ARRAY, VFLD, FOR INTERPOLATION
          do n=n2-1, n2+2, 1
            do m=m2-1, m2+2, 1
              k = k +1
              vfld(k) = bfld(m,n)
            enddo
          enddo
c
c                   PERFORM AYRES CENTRAL DIFFERENCES AND INTERPOLATION,
c                           FOUR TIMES TO LOAD ECV
c
          do k=1, 4
            ev3m1  = vfld(k+8) -vfld(k)
            ev3m2  = vfld(k+8) -vfld(k+4)
            ev4m2  = 0.5d0*(vfld(k+12) -vfld(k+4))
            aa     = 0.5d0*ev3m1
            bb     = 3.0d0*ev3m2 -ev3m1 -ev4m2
            cc     = aa +ev4m2 -ev3m2 -ev3m2
            ecv(k) = vfld(k+4) +s*(aa +s*(bb +s*cc))
          enddo
c
c                   PERFORM AYRES CENTRAL DIFFERENCES WITH ECV
c
          ev3m1   = ecv(3) -ecv(1)
          ev3m2   = ecv(3) -ecv(2)
          ev4m2   = 0.5d0*(ecv(4) -ecv(2))
          aa      = 0.5d0*ev3m1
          bb      = 3.0d0*ev3m2 -ev3m1 -ev4m2
          cc      = aa +ev4m2 -ev3m2 -ev3m2
          cycitr8 = ecv(2) +r*(aa +r*(bb +r*cc))
c
        elseif (m2.ge.1 .and. m2.le.ix .and.
     &          n2.ge.1 .and. n2.le.jy) then
c
c                   PERFORM BILINEAR INTERPOLATION
c
          if (m2 .lt. ix ) then
            m3 = m2 +1
            bv = bfld(m2,n2)
            if (n2 .eq. 1 .or. n2 .eq. jy) then
              cycitr8 = bv +r*(bfld(m3,n2) -bv)
            else
              n3 = n2 +1
              cycitr8 = bv +r*(bfld(m3,n2) -bv) +s*(bfld(m2,n3) -bv)
     &              +r*s*(bfld(m3,n3) +bv -bfld(m3,n2) -bfld(m2,n3))
            endif
          elseif (n2 .lt. jy) then
            n3 = n2 +1
            bv = bfld(m2,n2)
            cycitr8 = bv +s*(bfld(m2,n3) -bv)
          else
            cycitr8 = bfld(m2,n2)
          endif
        else
c
c                   ERROR VALUE RETURNED, REQUESTED POINT NOT IN BOUNDS
c
          cycitr8 = -999999999.0d0
        endif
      else
c
c                   ERROR VALUE RETURNED, BFLD MUST BE 4 BY 4 OR LARGER
c
        cycitr8 = -999999999.0d0
      endif
c
      end
      subroutine cycloc (kout,itc,jtc,nogo)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)cycloc.f90	1.2  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cycloc
c
c  DESCRIPTION:  locate cyclone with isogons
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c         calddto     calculate wind direction, towards
c         isofnd      driver routine to use isogons to locate cyclone
c
c  LOCAL VARIABLES:
c    Name        Type                 Description
c   ------       ----       -----------------------------------------
c   cirdat       real       circulation data
c                             (1, first  dimension location
c                             (2, second dimension location
c                             (3, wind support factor, 3 or 4
c                             (4, intersection support, 2 - 8
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (26 MAR 1997)  Hamilton, H.
c    make changes to use isogons to locate wind center of cyclone
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      integer    nval
      parameter (nval = 10)
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      integer kout, itc, jtc, nogo
c
c     local variables
      integer  n, ncyc
      integer  kccf, kc, nhsh, k, iadd, kk, ktry
      integer  kuvs(4), kint(4)
      real     ritc, rjtc, di, dj, posit, dist, rin, rjn
      real     rtci, rtcj
      real     umx, vmx
      real     xc(4), yc(4), cirdat(4,nval)
      real     uus(ixm,jym), vvs(ixm,jym)
c
      save ixl, jyl, rtcil, rtcjl
      integer  ixl, jyl
      real     rtcil, rtcjl
c
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'works_com.inc'
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat4_com.inc'
      INCLUDE 'fltln_com.inc'
c
      equivalence (wrk83(1,1),uus(1,1)), (wrk84(1,1),vvs(1,1))
c
      data ixl /0/, jyl /0/
      data rtcil/0.0/, rtcjl/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c write(*,*) 'INTO cycloc, ix ',itc,'   jy ',jtc
c
      if (kout .lt. 0) then
        ixl   = itc
        rtcil = real (itc)
        jyl   = jtc
        rtcjl = real (jtc)
        write (*,*) 'CYCLOC, inital ri ',rtcil,'  rj ',rtcjl
        write (*,*) 'CYCLOC, requested lt ',flat(0),'  ln ',flon(0)
      endif
c
      uus = real (u285)
      vvs = real (v285)
c
c                   calculate wind direction (towards) in uu
c
      call calddto (uus,vvs,ixm,jym,umx,vmx)
      if (umx .le. 100.0 .and. vmx .le. 100.0) then
c
c                   max wind speed OK, so set hemisphere flag
c
        if (flat(0) .gt. 0.0) then
          nhsh = 1
        else
          nhsh = -1
        endif
        kc   = 0
        ktry = 0
        ritc = rtcil
        rjtc = rtcjl
c
  100   continue
        ktry = ktry +1
        call isofnd (ritc,rjtc,nhsh,uus,ixm,jym,kccf,kuvs,kint,xc,yc)
        if (kccf .gt. 0) then
c
c                 circulation center found with isogons
c
c         if (kccf .gt. 1) write (20,*) ' isofnd found ',kccf,
c    &       ' cyclones'
c         if (kccf .gt. 1) write  (*,*) ' isofnd found ',kccf,
c    &       ' cyclones'
          do k=1, kccf
c           write (20,*) 'cyclone ',k,' is at ',xc(k),'  ',yc(k)
            if (kc .eq. 0) then
              if (xc(k) .ne. 0.0 .and. yc(k) .ne. 0.0) then
                kc = 1
                cirdat(1,1) = xc(k)
                cirdat(2,1) = yc(k)
                cirdat(3,1) = kuvs(k)
                cirdat(4,1) = kint(k)
              endif
            else
c
c                 do not add duplicate position
c
              iadd = -1
              do kk=1, kc
                if (xc(k) .eq. 0.0 .or. yc(k) .eq. 0.0) iadd = 0
                if (abs (cirdat(1,kk) -xc(k)) .le. 0.1) then
                  if (abs (cirdat(2,kk) -yc(k)) .le. 0.1) iadd = 0
                endif
              enddo
              if (iadd .eq. -1) then
c
c                 add new cyclone location to cirdat
c
                kc = kc +1
                if (kc .le. nval) then
                  cirdat(1,kc) = xc(k)
                  cirdat(2,kc) = yc(k)
                  cirdat(3,kc) = kuvs(k)
                  cirdat(4,kc) = kint(k)
                endif
              else
c               write (20,*) ' found duplicate cyclone at ',xc(k),'  ',
c    &                         yc(k)
              endif
            endif
          enddo
          if (kc .eq. 1) then
            ncyc = 1
            nogo = 0
          else
            posit = 500.0
            do n=1, kc
              rin  = cirdat(1,n)
              rjn  = cirdat(2,n)
              di   = rin -rtcil
              dj   = rjn -rtcjl
              dist = sqrt (di*di +dj*dj)
              if (dist .lt. posit) then
                posit = dist
                ncyc  = n
              endif
            enddo
            rin  = cirdat(1,ncyc)
            rjn  = cirdat(2,ncyc)
            di   = rin -rtcil
            dj   = rjn -rtcjl
            dist = sqrt (di*di +dj*dj)
            if (dist .gt. 1.1) then
c             write (20,*) 'Lost initial cyclone, dist= ',dist
c             write  (*,*) 'Lost initial cyclone, dist= ',dist
              nogo = -1
            endif
          endif
        elseif (ktry .eq. 1) then
          ritc = itc
          rjtc = jtc
          goto 100
c
        elseif (ktry .eq. 2) then
          ritc = 0.5*(float (itc) +rtcil)
          rjtc = 0.5*(float (jtc) +rtcjl)
          goto 100
c
        else
c         write (20,*) ' cyclone lost - NO CENTER from isogons'
c         write (*,*)  ' cyclone lost - NO CENTER from isogons'
          nogo = -1
        endif
      else
        write (*,*)  'cyclon, Model is unstable - ABORT uu ',umx,
     &               '  vv ',vmx
c       write (20,*) 'cyclon, Model is unstable - ABORT uu ',umx,
c    &               '  vv ',vmx
        nogo = -1
      endif
      if (nogo .eq. 0) then
        rtci  = cirdat(1,ncyc)
        itc   = nint (rtci)
        rtcil = rtci
        rtcj  = cirdat(2,ncyc)
        jtc   = nint (rtcj)
        rtcjl = rtcj
c
c                Record position every 6-hours, in grid co-ords
c
        if (kout .lt. 0) then
c
c                record initial location of cyclone in model
c
          flat(1) = rtcj               !  Convert to LAT/LON in cyctrack
          flon(1) = rtci
          kout    = 0
	  write (*,*) 'INITIAL GRID I ',rtci,'  J ',rtcj
        elseif (kout .gt. 0) then
c         write(*,*) 'KOUT=',kout,'  rtcj ',rtcj,'  rtci ',rtci
c         write(20,*) 'KOUT=',kout,'  rtcj ',rtcj,'  rtci ',rtci
          flat(kout) = rtcj            !  Convert to LAT/LON in cyctrack
          flon(kout) = rtci
        endif
      endif
c
      end
      subroutine cyctrack (nout,nogo)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cyctrack
c
c  DESCRIPTION:  produce cyclone track in A-deck
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c     Example of A-deck format:
c          1         2         3         4         5         6         7
c 1234567890123456789012345678901234567890123456789012345678901234567890123456
c 03OTCR97051212 1382328 1472337 1532346 1632353 1862372  0  0  0  0  0 WP0497
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      include 'dataioparms.inc'
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      integer       nout, nogo
c
c         local variables
      integer  ktau, j, irtc, jt, k, ioe, mon, iyr
      integer  lat(5), lon(5)
      integer  ltlnwnd(numtau,llw)
      integer  ii, iarg
      character*1    enh, eew, cs
      character*2    cb, cayr
      character*4    cfyr
c     character*24   fname
c     character*240  pfname
      character*6    strmid
      character*2    century
      real  plat, plon, dist, bhead, bsped, gicor, gjcor, xplt, xpln
      real  fwgt(13), pwgt(13)
      real  pflt(0:13), pfln(0:13)
      double precision  ydis
c
      INCLUDE 'cyc_c_com.inc'
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat4_com.inc'
      INCLUDE 'fltln_com.inc'
c
c       TAU:     0   6   12  18  24  30  36  42  48  54  60  66  72
      data fwgt/ 0.0,0.5,1.0,1.5,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0/
      data pwgt/10.0,9.5,9.0,8.5,8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0, 0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      gicor = ricyc -flon(1)  ! initial i-grid correction
      gjcor = rjcyc -flat(1)  ! initial j-grid correction
      bhead = head
      bsped = speed
      jt    = 0
      ktau  = 0
      do j=1, 13
        if (flat(j) .gt. -90.0) then
	  flat(j) = flat(j) +gjcor  ! apply grid correction NOT lat
	  flon(j) = flon(j) +gicor  ! apply grid correction NOT lon
          ktau  = (j -1)*6
c                     change from Mercator grid co-ord to lat/lon
          ydis    = (y2eq +(flat(j) -rjcyc)*del)*re_tlat_i
          flat(j) = rad2deg*(2.0d0*atan (exp (ydis)) -0.5d0*pi)
          pflt(j) = flat(j)
          irtc    = int (flon(j))
          flon(j) = gdlon(irtc) +(flon(j) -irtc)*mg_deg
          pfln(j) = flon(j)
c         write (20,*) 'Cyclone at tau ',ktau,' Lat ',flat(j),' Lon ',
c    &                  flon(j)
          write ( *,*) 'Cyclone at tau ',ktau,' Lat ',flat(j),' Lon ',
     &                  flon(j)
          jt = j
        else
c         write (20,*) 'Cyclone lost prior tau ',ktau +6
          write  (*,*) 'Cyclone lost prior tau ',ktau +6
          exit
        endif
      enddo
c
c                   prepare OTCM forecast with dynamic persistence
c
      call dirdist (pflt(1),pfln(1),pflt(jt),pfln(jt),head,dist)
      speed = dist/((jt -1)*6.0)
      dist  = 6.0*speed
      do j=2, jt-1
        call rcaltln (pflt(j-1),pfln(j-1),head,dist,pflt(j),pfln(j))
      enddo
      if (bhead .gt. 0.0) then
        head = bhead
      else
        bhead = head
        bsped = speed
      endif
      dist = 6.0*bsped
      do j=2, jt-1
        call rcaltln (pflt(j-1),pfln(j-1),head,dist,xplt,xpln)
        pflt(j) = 0.1*(fwgt(j)*pflt(j) +pwgt(j)*xplt)
        pfln(j) = 0.1*(fwgt(j)*pfln(j) +pwgt(j)*xpln)
        call dirdist (pflt(1),pfln(1),pflt(j),pfln(j),head,dist)
	dist=dist/(j-1)
      enddo
c
c                   Prepare for CCRS output
c
      k   = 0
      lat = 0
      lon = 0
      do j=3, jt, 2
        if (j .ne. 11) then
          k = k +1
          lat(k) = anint (10.0*pflt(j))
          lon(k) = anint (10.0*pfln(j))
          lon(k) = 3600 -lon(k)
        endif
      enddo
c                   set A-DECK year
      cayr = cycdtg(3:4)
c
c     KEY CCRS TWO LETTER BASIN CODES OFF STANDARD ONE LETTER BASIN CODE
c
      cs = cycid(3:3)
      if (cs.eq.'A' .or. cs.eq.'B') then
c                   ARABIAN SEA AND BAY OF BENGAL, NORTH INDIAN OCEAN
        cb = 'IO'
      elseif (cs .eq. 'W') then
c                   WESTERN PACIFIC OCEAN
        cb = 'WP'
      elseif (cs .eq. 'C') then
c                   CENTRAL PACIFIC OCEAN
        cb = 'CP'
      elseif (cs .eq. 'E') then
c                   EASTERN PACIFIC OCEAN
        cb = 'EP'
      elseif (cs.eq.'S' .or. cs.eq.'P') then
c                   SOUTH INDIAN AND SOUTH PACIFIC OCEANS
        cb = 'SH'
        read (cycdtg(5:6),'(i2)') mon
        if (mon .gt. 6) then
c                   correct A-DECK year for SH cyclones
          read (cycdtg(1:4),'(i4)') iyr
          iyr = iyr +1
          write (cfyr,'(i4)') iyr
          cayr = cfyr(3:4)
        endif
      elseif (cs .eq. 'L') then
c                   NORTH ATLANTIC OCEAN
        cb = 'AL'
      else
c                   UNKNOWN OCEAN BASIN
        cb = 'XX'
      endif
c
c                   A-DECK FORMAT WRITE
c
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c     get cyclone to forecast (WP0497)
      call getarg (iarg,strmid)
      iarg = iarg + 1
c
c     get the first two digits of the year
      call getarg(iarg,century)
      iarg = iarg + 1
      do ii=1,numtau
         ltlnwnd(ii,1) = 0
         ltlnwnd(ii,2) = 0
         ltlnwnd(ii,3) = 0
      enddo
      do ii=1, 5
         ltlnwnd(ii,1) = lat(ii)
         ltlnwnd(ii,2) = lon(ii)
         ltlnwnd(ii,3) = 0
      enddo
      call writeAid( nout, strmid, cycdtg(1:2), cycdtg(3:10), 'OTCR', 
     &              ltlnwnd )
c
c                   PLAIN TEXT WRITE
c
      if (bhead .ge. 0.0) then
cx      write (nout,920) cycid, cycdtg, bhead, speed
        write (*,920) cycid, cycdtg, bhead, bsped
      else
cx      write (nout,921) cycid, cycdtg
        write (*,921) cycid, cycdtg
      endif
 920  format ('  OTCR INITIAL AND FORECAST POSITIONS OF ',a3,' AT ',
     &         a10,/,'  BASED UPON:  HEADING ',f5.1,' SPEED ',f4.1)
 921  format ('  OTCR INITIAL AND FORECAST POSITIONS OF ',a3,' AT ',
     &         a10,/,'  BASED UPON:  NO PRIOR HEADING/SPEED')
      ktau = -6
      do j=1, jt
        enh  = 'N'
        plat = pflt(j)
        if (plat .lt. 0.0) enh  = 'S'
        plat = abs (plat)
        eew  = 'E'
        plon = pfln(j)
        if (plon .gt. 180.0) then
          plon = 360.0 -plon
          eew  = 'W'
        endif
        ktau = ktau +6
cx      write (nout,930,err=710,iostat=ioe) ktau,plat,enh,plon,eew
        write (*,930,err=710,iostat=ioe) ktau,plat,enh,plon,eew
      enddo
  930 format ('  TAU ',i2.2,2x,f4.1,a1,2x,f5.1,a1)
c
      return
c
  710 continue
      write (*,*) 'OTCR, WRITE ERROR UNIT ',nout,' is ',ioe
      if (nogo .eq. 0) nogo = -66
      return
c
      end
      subroutine dirdist (sl,sg,el,eg,head,dist)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)dirdist.f90	1.1 6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  dirspd
c
c  DESCRIPTION:  Calculate heading and speed from "sl,sg" to "el,eg",
c                in "time" hours for the tropics and sub-tropics
c
c  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  None
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  None
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:   None
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call dirspd (sl,sg,el,eg,head,dist)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c        sl        real        input    starting latitude, -SH
c        sg        real        input    starting longitude, (0 - 360 E,
c                                       or -W)
c        el        real        input    ending latitude, -SH
c        eg        real        input    ending longitude, (0 - 360 E,
c                                       or -W)
c      head        real        output   heading (deg)
c      dist        real        output   distance (nm)
c
c  COMMON BLOCKS:  None
c
c  FILES:  None
c
c  DATA BASES:  None
c
c  NON-FILE INPUT/OUTPUT:  None
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c    negative time             return negative speed
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         a45r       real       radians in 45 degrees
c         dist       real       distance between sl,sg and el,eg (nm)
c         eln1       real       calculation factor
c         eln2       real       calculation factor
c         ihead      int        integer of head times 10
c         inil       int        flag for initial calculations
c         ispd       int        integer of spd times 10
c         rad        real       degrees per radian
c         radi       real       radinas per degree
c         rdi2       real       0.5 times radi
c         tiny       real       tiny number, hardware dependent
c         xg         real       local copy of sg
c         xl         real       local copy of sl
c         xr         real       calculation factor
c         yr         real       calculation factor
c         yg         real       local copy of eg
c         yl         real       local copy of el
c
c  METHOD:  Based upon rhumb line calculations from Texas Instruments
c           navigation package for hand held calculator
c
c  INCLUDE FILES:  None
c
c  COMPILER DEPENDENCIES:  F77 with F90 extentions or F90
c
c  COMPILE OPTIONS:  Standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  H. Hamilton
c    initial installation of software on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real  sl, sg, el, eg, head, dist
c
c         local variables
      integer           inil
      double precision  a45r, eln1, eln2, rad, radi, rdi2, headd, distd
      double precision  xg, xl, yg, yl, xr, yr, tiny
c
      save inil, rad, radi, rdi2, a45r
c
      data inil/-1/, tiny/0.1e-8/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .ne. 0) then
        inil = 0
        rad  = 180.0d0/acos (-1.0d0)
        radi = 1.0d0/rad
        rdi2 = 0.5d0*radi
        a45r = 45.0d0*radi
      endif
c
c                   pre-set heading and distance, for same point input
c
      head = 0.0
      dist = 0.0
      if (abs (sl -el).gt.tiny .or. abs (sg -eg).gt.tiny) then
        xl = sl
        xg = sg
c
c                   if longitude is west, convert to 0-360 East
c
c       if (xg .lt. 0.0d0) xg = xg +360.0d0
        yl = el
        yg = eg
c
c                   if longitude is west, convert to 0-360 East
c
c       if (yg .lt. 0.0d0) yg = yg +360.0d0
c
c                    check for shortest angular distance
c
        if (xg.gt.270.0d0 .and. yg.lt.90.0d0) yg = yg +360.0d0
        if (yg.gt.270.0d0 .and. xg.lt.90.0d0) xg = xg +360.0d0
c
        if (abs (xl -yl) .le. tiny) then
c
c                    resolve 90 or 270 heading
c
          head = 90.0
          if (yg .lt. xg) head = 270.0
          dist = 60.0d0*(yg -xg)*cos (xl*radi)
        else
          distd = 60.0d0*(xl -yl)
          if (abs (xg -yg) .le. tiny) then
c
c                  resolve 0 or 180 heading, note head is preset to zero
c
            if (yl .lt. xl) head = 180.0
            dist = distd
          else
c                   CHECK FOR POSITIONS POLEWARD OF 89+ DEGREES LATITUDE
cCC         IF (ABS (XL).GT.PLMX .OR. ABS (YL).GT.PLMX) THEN
c           (HARDWARE DEPENDENT - NOT REQUIRED FOR TROPICAL CYCLONES)
cCC           XLT = XL
cCC           IF (ABS (XLT) .GT. PLMX) XLT = SIGN (PLMX,XL)
cCC           YLT = YL
cCC           IF (ABS (YLT) .GT. PLMX) YLT = SIGN (PLMX,YL)
cCC           XR = TAN (XLT*RDI2 +SIGN (A45R,XL))
cCC           YR = TAN (YLT*RDI2 +SIGN (A45R,YL))
cCC         ELSE
              xr = tan (xl*rdi2 +sign (a45r,xl))
              yr = tan (yl*rdi2 +sign (a45r,yl))
cCC         ENDIF
            eln1  = sign (log (abs (xr)),xr)
            eln2  = sign (log (abs (yr)),yr)
            headd = rad*(atan ((xg -yg)/(rad*(eln1 -eln2))))
            if (yl    .lt. xl)  headd = headd +180.0d0
            if (headd .lt. 0.0) headd = headd +360.0d0
c
c                   correct initial distance, based only on latitude
c
            dist = distd/cos (headd*radi)
            head = headd
          endif
        endif
        dist = abs (dist)
      endif
      return
c
      end
      subroutine evaliso (md1,fx1,fy1,nd2,fx2,fy2,m1s,m1e,n2s,n2e,npc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)evaliso.f90	1.1  3/31/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  evaliso
c
c  DESCRIPTION:  evaluate isogons for segments that may intersect
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call evaliso (md1,fx1,fy1,nd2,fx2,fy2,m1s,m1e,n2s,n2e,npc)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      md1          int         in      dimension of fx1
c      fx1         real         in      array of x-values of isogon rh1
c      fy1         real         in      array of y-values of isogon rh1
c      nd2          int         in      dimension of fx2
c      fx2         real         in      array of x-values of isogon rh2
c      fy2         real         in      array of y-values of isogon rh2
c      m1s          int         out     array of rh1 start points
c      m1e          int         out     array of rh1 end points
c      n2s          int         out     array of rh2 start points
c      n2e          int         out     array of rh2 end points
c      npc          int        in/out   maximum size of m1s, m1e, n2s
c                                       n2e / count of segments that
c                                       contain potential centers
c
c  CALLED BY:  evaliso.f
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dx         real       working difference in x
c         dy         real       working difference in x
c         epsilon    real       minimum value of distance
c         ddw        real       wind direction at West-point
c         mm          int       working index to rh1 values
c         mxpc        int       maximum number of segments
c         nn          int       working index to rh2 values
c         x1         real       working x location of rh1
c         y1         real       working y location of rh1
c
c  METHOD:  1.  Initialize starting and ending points to zero.
c           2.  Iteratively search rh1 and rh2 isogon locations for a
c               gap less than or equal to epsilon.  Mark the starting
c               indicies in m1s and n2s.
c           3.  Continue iterative search for a gap greater than
c               epsilon.  Mark the ending inicies in m1e and n2e.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (02 APR 1997) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer md1, nd2, npc
      integer m1s(npc), m1e(npc), n2s(npc), n2e(npc)
      real    fx1(md1), fy1(md1), fx2(nd2), fy2(nd2)
c
c         local variables
      integer m, mm, ms, mxpc, n, nn
      real    x1, y1, dx, dy
      real    epsilon
c
      data epsilon/0.1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   initialize prospective locations
c
      mxpc = npc
      do n=1, npc
        m1s(n) = 0
        m1e(n) = 0
        n2s(n) = 0
        n2e(n) = 0
      enddo
      npc = 0
c
c                   look for prospective starting and ending points
c
      ms = 1
  110 continue
      do m=ms, md1
        x1 = fx1(m)
        y1 = fy1(m)
        do n=1, nd2
          dx = abs (x1 -fx2(n))
          dy = abs (y1 -fy2(n))
          if (dx .le. epsilon .and. dy .le. epsilon) then
            npc = npc +1
            if (npc .le. mxpc) then
              m1s(npc) = m
              n2s(npc) = n
            else
              npc = mxpc
              goto 200
c
            endif
            mm   = m
            nn   = n
c
c                   top of internal loop to find ending point
c
  120       continue
            mm = mm +1
            nn = nn +1
            if (mm .le. md1 .and. nn .le. nd2) then
              dx = abs (fx1(mm) -fx2(nn))
              dy = abs (fy1(mm) -fy2(nn))
              if (dx .gt. epsilon .and. dy .gt. epsilon) then
c
c                     found ending point
c
                m1e(npc) = mm
                ms       = mm +1
                n2e(npc) = nn
                goto 110
c
              elseif (mm .lt. md1 .and. nn .lt. nd2) then
c
c                       jump to top of internal loop
c
                  goto 120
c
              else
                m1e(npc) = mm
                n2e(npc) = nn
                if (mm .lt. md1) then
                  ms = mm +1
                  goto 110
c
                else
c
c                       finished searches
c
                  goto 200
c
                endif
              endif
            else
              if (m1s(npc) .eq. m -1 .and. n2s(npc) .eq. n -1) then
c
c                   too close to the edge for find ending point
c
                npc = npc -1
              else
c
c                   at the edge, so assume this is the end
c
                m1e(npc) = mm -1
                n2e(npc) = nn -1
              endif
              goto 130
c
            endif
          endif
        enddo
  130   continue
      enddo
  200 continue
c
      end
      subroutine expltln (head,dist,slat,slon,elat,elon)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)expltln.f90	1.1 6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  expltln
c
c  DESCRIPTION:  extraplolate lat/lon based upon starting lat/lon,
c                heading and distance
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  None
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:
c    Restricted to tropics and sub-tropics - latitudes of tropical cyclones
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:   None
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call expltln (head,dist,slat,slon,elat,elon)
c
c  PARAMETERS:
c     NAME       TYPE      USAGE             DESCRIPTION
c   --------    -------    ------    ------------------------------
c     head       real      input     rhumb-line heading in degrees from
c                                    slat/slon
c     dist       real      input     distance from slat/slon to elat/elon (nm)
c     slat       real      input     starting latitude, negative if South
c     slon       real      input     startint longitude, in degrees East
c     elat       real      output    extrapolated latitude, negative if South
c     elon       real      output    extrapolated longitude, in degrees East
c
c  COMMON BLOCKS:  None
c
c  FILES:  None
c
c  DATA BASES:  None
c
c  NON-FILE INPUT/OUTPUT:  None
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c     Uses rhumb-line approximations.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED: none
c
c  LOCAL VARIABLES:
c      NAME      TYPE               DESCRIPTION
c     ------     ----     ----------------------------------
c     degrad     real     degrees to radians conversion factor
c     dlon       real     delta longitude from slon to elon for
c                         090 or 270 heading
c     hdgrad     real     half of degrad
c     icrs        int     nearest integer of heading (deg)
c     inil        int     initialization flag, 0 - not initialized
c     raddeg     real     radian to degrees conversion factor
c     rad045     real     45 degrees expressed in radians
c     rdhd       real     heading in radians
c
c  METHOD:  Based upon rhumb-line calculations frpm Texas Instruments
c           Navigation Psckage for hand-held calculator
c
c  INCLUDE FILES:  None
c
c  COMPILER DEPENDENCIES:  F90
c
c  COMPILE OPTIONS:  Standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)   H. Hamilton
c    initial installation of software on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real  head, dist, slat, slon, elat, elon
c
c         local variables
      integer  icrs, inil
      real     tiny
      double precision  dlon, rdhd, raddeg, degrad, hdgrad, rad045
c
      save inil, raddeg, degrad, hdgrad, rad045
c
      data inil/-1/, tiny/0.1e-6/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .ne. 0) then
        inil   = 0
        degrad = acos (-1.0d0)/180.0d0
        hdgrad = 0.5d0*degrad
        rad045 = 45.0d0*degrad
        raddeg = 1.0d0/degrad
      endif
c
c         latitude, minus for South, longitude, degrees East (0 - 360)
c
      icrs = nint (head)
      if (abs (head -90.0) .lt. tiny .or. abs (head -270.0) .lt. tiny)
     &  then
        dlon = dist/(60.0*cos (slat*degrad))
        if (icrs .eq. 270) then
          elon = slon -dlon
        else
          elon = slon +dlon
        endif
        elat = slat
      else
        rdhd = head*degrad
        elat = slat +(dist*cos(rdhd)/60.0d0)
        if (icrs .eq. 180 .and. abs (head -180.0) .gt. tiny) then
          icrs = 181
        elseif (icrs .eq. 360 .and. abs (head -360.0) .gt. tiny) then
          icrs = 359
        endif
        if (mod (icrs,180) .ne. 0) then
c
c                   Following test NOT required for tropical cyclones
c!!       IF (ABS (ELAT) .GT. 89.0) ELAT = SIGN (89.0,ELAT)
c
          elon = slon +raddeg*(log (tan (rad045 +hdgrad*elat))
     &          -log (tan (rad045 +hdgrad*slat)))*tan (rdhd)
        else
          elon = slon
        endif
      endif
      return
c
      end
      subroutine fadvec (u,v,ni,nj,nt,kl,dum1,dum2,dum3,advec_q,dummy)
c                        1 2  3  4  5  6  7    8    9     10     11
c                                        kl-1  kl  kl+1
c                                         km   k    kp
c
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)fadvec.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  fadvec
c
c  DESCRIPTION:  calculate advection in flux form of dumX values
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      integer           ni, nj, nt, kl
      double precision  u(ni,nj), v(ni,nj), dum1(ni,nj), dum2(ni,nj),
     &                  dum3(ni,nj), advec_q(ni,nj), dummy(ni,nj)
c
c     local variables
      integer           i, j, ni1, nj1
c     integer           kk
      double precision  delp, v_adv_b, v_adv_t
      double precision  adj, cons 
c
      INCLUDE 'stat2_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'omega_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      advec_q = 0.0d0
      dummy   = 0.0d0
      ni1     = ni -1
      nj1     = nj -1
c
c        *****      COMPUTE HORIZONTAL ADVECTION     *****
c
      do j=2,  nj1
        do i=1,  ni1
          dummy(i,j) = (u(i+1,j) +u(i,j)) * (dum2(i+1,j)
     &                +dum2(i,j))*emi(j)
        enddo
      enddo
      do j=2, nj1
        do i=2, ni1
          advec_q(i,j) = dummy(i,j) -dummy(i-1,j)
        enddo
      enddo
      do j=1, nj1
        do i=2, ni1
          dummy(i,j) = (v(i,j+1)*emi(j+1) +v(i,j)*emi(j))*(dum2(i,j+1)
     &                +dum2(i,j))
        enddo
      enddo
      do j=2, nj1
        adj = em(j)*em(j)/(4.0d0*del)
        do i=2, ni1
          advec_q(i,j) = advec_q(i,j) +dummy(i,j) -dummy(i,j-1)
          advec_q(i,j) = -advec_q(i,j)*adj
        enddo
      enddo
c
c             *****    ADD VERTICAL ADVECTION      *****
c
c                        general equations
c        v_adv_b = ((d1(i,j) +d2(i,j))*(w1(i,j) +w2(i,j)))/(4.0d0*dp(1-2))
c        v_adv_t = ((d2(i,j) +d3(i,j))*(w2(i,j) +w3(i,j)))/(4.0d0*dp(2-3))
c        v_advec = -(v_adv_b -v_adv_t)
c
      if (kl .eq. 4) then
c
c                   COMPUTE VERTICAL ADVECTION AT 250 MB
c
        delp = dp(3)
        do j=2, nj1                            ! w00 = w at 100 mb = 0.0
          do i=2, ni1
            v_adv_b = ((dum1(i,j) +dum2(i,j))*w40(i,j))/(2.0d0*delp)
            advec_q(i,j) = advec_q(i,j) -v_adv_b
          enddo
        enddo
      elseif (kl .eq. 3) then
c
c                   COMPUTE VERTICAL ADVECTION AT 550 MB
c
c    kk = kl
c    if (nt == 1) kk = kk -1
c    delp = 0.5d0*(dp(kk) +dp(kk+1))
        delp = 300.0d0
        do j=2, nj1
          do i=2, ni1
            v_adv_b = ((dum1(i,j) +dum2(i,j))*w70(i,j))/(2.0d0*delp)
            v_adv_t = ((dum2(i,j) +dum3(i,j))*w40(i,j))/(2.0d0*delp)
            advec_q(i,j) = advec_q(i,j) -(v_adv_b -v_adv_t)
c                              OLD CODE
c       advec_q(i,j) = advec_q(i,j) -((dum1(i,j) +dum2(i,j))*www(i,j,kk)
c                     -(dum2(i,j) +dum3(i,j))*www(i,j,kk+1))/(2.0d0*delp)
          enddo
        enddo
      elseif (kl .eq. 2) then
c
c                   COMPUTE VERTICAL ADVECTION AT 850 MB
c
        if (nt .eq. 2) then
c
c                   process wind component
c
c     delp = dp(1) +0.5*dp(2)
          delp = 300.0
          do j=2, nj1
            do i=2, ni1              ! dum1 is unknown
c         v_adv_b = ((0.5d0*dum1(i,j) +dum2)*(w92(i,j))/(2.0d0*150.0)
c         v_adv_t = ((dum2(i,j) +dum3(i,j))*w70(i,j))/(2.0d0*delp)
c         advec_q(i,j) = advec_q(i,j) +(v_adv_b -v_adv_t)
c                                 OLD CODE
              advec_q(i,j) = advec_q(i,j) -(dum1(i,j)*w10(i,j)
     &                      -(dum2(i,j) +dum3(i,j))*w70(i,j)/2.0)/delp
            enddo
          enddo
        elseif (nt .eq. 1) then
c
c                   process theta
c
          delp = dp(1) +0.5*dp(2)
          do j=2, nj1
            do i=2, ni1
c         v_adv_b = ((dum1(i,j) +dum2(i,j))*w92(i,j))/(2.0d0*dp(1))
c         v_adv_t = ((dum2(i,j) +dum3(i,j))*w70(i,j))/(2.0d0*dp(2))
c         advec_q(i,j) = advec_q(i,j) -(v_adv_b -v_adv_t)
c                                 OLD CODE
              advec_q(i,j) = advec_q(i,j) -(dum1(i,j)*w10(i,j)
     &                  -(dum2(i,j) +dum3(i,j))*w70(i,j)/2.0)/delp
            enddo
          enddo
        else
          write(*,*) 'ERROR, wrong nt ',nt,' OR kl ',kl
          pause
        endif
      elseif (kl .eq. 1) then
c
c                   COMPUTE VERTICAL ADVECTION AT 1000 MB
c
        if (nt .eq. 1) then
c
c                           process theta
c
          delp = 150.0d0
          do j=2, nj1
            do i=2, ni1
c         v_adv_b = dum2(i,j)*w10(i,j)
c         v_adv_t = ((dum2(i,j) +dum3(i,j))*w92(i,j))/(2.0d0*delp)
c         advec_q(i,j) = advec_q(i,j) +v_adv_t
c                                 OLD CODE
              advec_q(i,j) = advec_q(i,j) -(dum2(i,j)*w10(1,j)
     &                      -dum3(i,j)*(w70(i,j) +w10(i,j))/2.0)/dp(1)
            enddo
          enddo
        elseif (nt .eq. 0) then
c
c                        process geopotential
c
          cons = 100.0d0/1.19d0
c     dummy = 0.0d0
c     write(*,*) 'HORIZ GZ advec values prior to VERT'
          do j=2, nj1
            do i=2, ni1
              advec_q(i,j) = advec_q(i,j) +w10(i,j)*cons
c         advec_q(i,j) = advec_q(i,j) +w10(i,j)
c         dummy(i,j)   = w10(i,j)*cons
            enddo
          enddo
        else
          write (*,*) 'WRONG nt ',nt,'  OR kl ',kl
          pause
        endif
      else
        write (*,*) 'WRONG kl ',kl
        pause
      endif
c
      end
      subroutine fakeflds
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)fakeflds.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  fakeflds
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'mstrls_com.inc'
c
      write(*,*) 'INTO fakeflds ...loading xx2 fields for new fields'
      uls   = uu2
      vls   = vv2
      tls   = pt2
      zls10 = z210
c
      end
      subroutine filter (nx,ny,dum,fld)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)filter.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  filter
c
c  DESCRIPTION:  filter "noise" from field
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      implicit none
c
c     formal parameters
      integer           nx, ny
      double precision  dum(nx,ny), fld(nx,ny)
c
c     local variables
      integer           nx1, ny1, i, j, m
      double precision  alf
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nx1 = nx -1
      ny1 = ny -1
      alf = 0.25d0
      do m=1, 2
        if (m .eq. 2) alf = -alf
c
        dum = fld
c
        do j=2, ny1
          do i=2, nx1
            dum(i,j) = fld(i,j) +alf*(fld(i+1,j) -2.0d0*fld(i,j)
     &                +fld(i-1,j))
          enddo
        enddo
c
        fld = dum
c
        do j=2, ny1
          do i=2, nx1
            fld(i,j) = dum(i,j) +alf*(dum(i,j+1) -2.0d0*dum(i,j)
     &                +dum(i,j-1))
          enddo
        enddo
      enddo
c
      end
      subroutine fldread (mtau,ityp,ilev,rfld,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  fldread
c
c  DESCRIPTION:  driver routine for reading fields
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Cray UNICOS
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call fldread (cdtg,rtau,ityp,ilev,ierr)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c       cdtg       char          in     date_time_group of field
c       rtau       real          in     forecast period
c       ityp        int          in     parameter type index
c       ilev        int          in     level index
c     itrunc        int          in     max wave number to be retained, if
c                                       truncation; no truncation if < 18
c       ierr        int         out     error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:
c     NAME          TABLE      USAGE       DESCRIPTION
c    --------     -----------  ------  --------------------
c      ISIS         NOGAPS       in    forecast fields
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     missing field or         set error flag to non-zero
c        read error
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dsetnam    char       data set name
c         geonam     char       geometry name
c         idgrid      int       internal dataset identifier number
c         igrdx       int       first  dimension of fields
c         irecnum     int       internal record sequence number
c         istatus     int       status of ISIS request
c         jgrdy       int       second dimension of fields
c         params     char       parameter names
c         rlvl1      real       level 1 value
c         rlvl2      real       level 2 value
c         seclvl     char       security level
c         title      char       title of field
c         typlvl     char       type of level
c         typmodl    char       type of model
c         units      char       units of fields
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      INCLUDE 'par_ng.inc'
c
c         formal parameters
      integer      mtau, ityp, ilev, ierr
      real         rfld(ixng,jyng)
c
c         local variables
      integer      ioe
      character*24 dsetnam, typlvl
      character*32 typmodl, geonam, params(4), units(4)
      real         rlvl1(4), rlvl2
c
c                   ISIS parameters
      data typmodl/'NOGAPS'/, geonam/'global_360x181'/
      data dsetnam/'fcst_ops'/
      data rlvl1/1000.0, 850.0, 500.0, 250.0/
      data rlvl2/0.0/
      data params/'wnd_ucmp', 'wnd_vcmp', 'air_temp', 'geop_ht'/
      data units /'m/s',      'm/s',      'deg_K',    'gpm'/
      data typlvl/'isbr_lvl'/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = 0
c
c                   read NOGAPS field
c
c     write (20,*) 'Reading par_type ',ityp,' level ',ilev,' tau ',mtau
c     write (20,*) 'PAR ',params(ityp),' UNITS ',units(ityp),' LEV ',
c    &              rlvl1(ilev)
c
      read (30,iostat=ioe) rfld
c     write(*,*) 'fldread (1,1) ',rfld(1,1)
      if (ioe .ne. 0) then
	write (*,*) 'READ ERROR of field, LEV ',ilev,' TYPE ',ityp
	write (*,*) 'ERROR is: ',ioe
        ierr = -1
      endif
c
      return
c
      end
      subroutine fndpcir (ddfld,ixgrd,jygrd,mni,mxi,mnj,mxj,nhsh,mxcc,
     &                    cirdat,nccf)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)fndpcir.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  fndpcir
c
c  DESCRIPTION:  determine approximate location of cyclonic
c                circulation(s) in both NH and SH
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call fndpcir (ddfld,igrdx,jgrdy,mni,mxi,mnj,mxj,nhsh,mxcc,
c                        cirdat,nccf)
c
c  PARAMETERS:
c     NAME        TYPE        USAGE             DESCRIPTION
c   --------     -------      ------   ------------------------------
c    ddfld        real         in      wind direction (to) field
c    igrdx         int         in      first  dimension of ddfld
c    jgrdy         int         in      second dimension of ddfld
c      mni         int         in      first  dimension start of window
c      mxi         int         in      first  dimension end of window
c      mnj         int         in      second dimension start of window
c      mxj         int         in      second dimension end of window
c     nhsh         int         in      north/south hemisphere indicator
c     mxcc         int         in      maximum number of cyclonic
c                                      circulations (cc) allowed
c   cirdat        real         out     array for circulation data
c                                        (1,  first  dimension estimate
c                                        (2,  second dimension estimate
c                                        (3,  wind support factor
c     nccf         int         out     number of cc found
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c    Name          Description
c   --------       -----------------------------------------------------
c   avgddt         calculate weighted average wind direction
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dde        real       wind direction at East-point
c         ddn        real       wind direction at North-point
c         dds        real       wind direction at South-point
c         ddw        real       wind direction at West-point
c         f1         real       fractional grid-length to "center line"
c         ichk        int       sum of winds within window
c         ixce        int       eastern-edge index
c         jycn        int       northern-edge index
c         jycs        int       southern-edge index
c         ixcw        int       western-edge index
c          rxc       real       approximate first  dimension location
c          ryc       real       approximate second dimension location
c
c  METHOD:  1.  Check wind direction at cardinal points about
c               central point.
c           2.  If 3 or 4 agree with cyclonic flow
c               assign cirdat sum of agreement.
c           3.  Replace duplicates when sum is 4.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation in OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer  ixgrd, jygrd, mni, mxi, mnj, mxj, nhsh, mxcc, nccf
      real     ddfld(ixgrd,jygrd), cirdat(4,mxcc)
c
c         local variables
      integer  i, j, n, ixcw, ixce, jycs, jycn, ichk
      real     f1, ddn,dds,dde,ddw, rxc, ryc
c         real function
      real avgddt
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nccf = 0
      do j=mnj, mxj-1
        ryc  = j +0.5
        jycs = j
        jycn = j +1
        do i=mni, mxi-1
          rxc  = i +0.5
          ixcw = i
          ixce = i +1
          if (ixce .gt. ixgrd) ixce = ixce -ixgrd
c
c                   obtain wind directions north, south, west and east
c                   note, directions are to not from.
c
          f1  = rxc -i
          ddn = avgddt (ddfld(ixcw,jycn),ddfld(ixce,jycn),f1)
          dds = avgddt (ddfld(ixcw,jycs),ddfld(ixce,jycs),f1)
          f1  = ryc -j
          ddw = avgddt (ddfld(ixcw,jycs),ddfld(ixcw,jycn),f1)
          dde = avgddt (ddfld(ixce,jycs),ddfld(ixce,jycn),f1)
c
c                   check the type of flow pattern associated with
c                   this grid block
          ichk = 0
          if (nhsh .gt. 0) then
c
c                     check for:  cyclonic circulation, nh
c
            if (ddn .ge. 210.0 .and. ddn .le. 315.0) ichk = 1
            if (ddw .ge. 120.0 .and. ddw .le. 225.0) ichk = ichk +1
            if (dds .ge. 030.0 .and. dds .le. 135.0) ichk = ichk +1
            if ((dde .ge. 000.0 .and. dde .le. 045.0) .or.
     &          (dde .ge. 300.0 .and. dde .le. 360.0)) ichk = ichk +1
          else
c
c                                 cyclonic circulation, sh
c
            if (ddn .ge. 045.0 .and. ddn .le. 150.0) ichk = 1
            if (dde .ge. 135.0 .and. dde .le. 240.0) ichk = ichk +1
            if (dds .ge. 225.0 .and. dds .le. 330.0) ichk = ichk +1
            if ((ddw .ge. 000.0 .and. ddw .le. 060.0) .or.
     &          (ddw .ge. 315.0 .and. ddw .le. 360.0)) ichk = ichk +1
          endif
          if (ichk .ge.  3) then
c
c                   cyclonic circulation found, see if this is a
c                   new or "duplicate" circulation
c
            if (nccf .gt. 0) then
              n = 0
              do while (ichk.gt.0 .and. n.lt.nccf)
                n = n +1
                if (abs (cirdat(1,n) -rxc) .lt. 1.8) then
                  if (abs (cirdat(2,n) -ryc) .lt. 1.8) then
c
c                       "duplicate" found, keep 4 over 3
c
                    if (ichk .gt. nint (cirdat(3,n))) then
c                         replace old with new location
                      cirdat(1,n) = rxc
                      cirdat(2,n) = ryc
                      cirdat(3,n) = 4.0
                    endif
                    ichk = 0
                  endif
                endif
              enddo
              if (ichk .gt. 0) then
c                   new point was not absorbed above
                nccf = nccf +1
                if (nccf .lt. mxcc) then
c                       add new cyclonic circulation
                  cirdat(1,nccf) = rxc
                  cirdat(2,nccf) = ryc
                  cirdat(3,nccf) = ichk
                endif
              endif
            else
              nccf = 1
              cirdat(1,nccf) = rxc
              cirdat(2,nccf) = ryc
              cirdat(3,nccf) = ichk
            endif
          endif
        enddo
      enddo
      do j=mnj+1, mxj-1
        ryc = j
        do i=mni+1, mxi-1
c
c                   obtain wind directions north, south, west and east
c                   note, directions are to not from.
c
          ddn = ddfld(i,j+1)
          dds = ddfld(i,j-1)
          ddw = ddfld(i-1,j)
          dde = ddfld(i+1,j)
c
c                   check the type of flow pattern associated with
c                   this grid block
          ichk = 0
          if (nhsh .gt. 0) then
c
c                     check for:  cyclonic circulation, nh
c
            if (ddn .ge. 210.0 .and. ddn .le. 315.0) ichk = 1
            if (ddw .ge. 120.0 .and. ddw .le. 225.0) ichk = ichk +1
            if (dds .ge. 030.0 .and. dds .le. 135.0) ichk = ichk +1
            if ((dde .ge. 000.0 .and. dde .le. 045.0) .or.
     &          (dde .ge. 300.0 .and. dde .le. 360.0)) ichk = ichk +1
          else
c
c                                 cyclonic circulation, sh
c
            if (ddn .ge. 045.0 .and. ddn .le. 150.0) ichk = 1
            if (dde .ge. 135.0 .and. dde .le. 240.0) ichk = ichk +1
            if (dds .ge. 225.0 .and. dds .le. 330.0) ichk = ichk +1
            if ((ddw .ge. 000.0 .and. ddw .le. 060.0) .or.
     &          (ddw .ge. 315.0 .and. ddw .le. 360.0)) ichk = ichk +1
          endif
          if (ichk .ge. 3) then
c
c                   cyclonic circulation found, see if this is a
c                   new or "duplicate" circulation
c
            rxc = i
            if (nccf .gt. 0) then
              n = 0
              do while (ichk.gt.0 .and. n.lt.nccf)
                n = n +1
                if (abs (cirdat(1,n) -rxc) .lt. 1.1) then
                  if (abs (cirdat(2,n) -ryc) .lt. 1.1) then
c
c                       "duplicate" found, keep 4 over 3
c
                    if (ichk .gt. nint (cirdat(3,n))) then
c                        replace old with new location
                      cirdat(1,n) = rxc
                      cirdat(2,n) = ryc
                      cirdat(3,n) = 4.0
                    endif
                    ichk = 0
                  endif
                endif
              enddo
              if (ichk .gt. 0) then
c                   new point was not absorbed above
                nccf = nccf +1
                if (nccf .lt. mxcc) then
c                       add new cyclonic circulation
                  cirdat(1,nccf) = rxc
                  cirdat(2,nccf) = ryc
                  cirdat(3,nccf) = ichk
                endif
              endif
            else
              nccf = 1
              cirdat(1,nccf) = rxc
              cirdat(2,nccf) = ryc
              cirdat(3,nccf) = ichk
            endif
          endif
        enddo
      enddo
c
      end
      subroutine forecast (mtau,kstp,kht,itc,jtc,nogo)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  forecast
c
c  DESCRIPTION:  forecast location of topical cyclone
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  see main driver program otcm
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call forecast (mtau,kstp,kht,itc,jtc,nogo)
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c     mtau             int           input   starting model tau (hr)
c     kstp             int           input   index for 6 or 12 hour run
c     kht              int           input   heating index
c     itc              int          in/out   i-th location of cyclone
c     jtc              int          in/out   j-th location of cyclone
c     nogo             int          output   continue processing flag
c
c  COMMON BLOCKS:
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      integer  mtau, kstp, kht, itc, jtc, nogo
c
c     local variables
      integer  ihour, itime, into, ismthb, nk, nkw
      integer  i, j, ni, ni1, ni2, nj, nj1, nj2, istop, iloc
      integer  lstep, i1, i2, ij, j1, j2, k, nflt, iloc6
      integer  nfor(4), ifcst(2)
      real     robert, qq, htadj
      double precision  ek, ekm
c
      save kout, kount, tendit, time, twotim, ismth, ekm, htadj
c
      integer  ismth, kount, kout, khr
      real     tendit, time, twotim
c
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr1_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'mstrls_com.inc'
      INCLUDE 'omega_com.inc'
      INCLUDE 'stat2_com.inc'
      INCLUDE 'stat3_com.inc'
      INCLUDE 'works_com.inc'
c
      data  ihour/3600/, ismthb/5/, itime/150/, into/6/, nk/4/, nkw/3/
      data  ifcst/6,12/, ismth/24/
      data robert/0.1/, qq/100.0/
c
c      data heat/0.0,0.3,1.0,0.3/
c!!!!  data p/1000.0,850.0,550.0,250.0/
c      data dp/150.0,300.0,300.0,150.0/
c      data qq/100.0/  ! heating value
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (*,*) 'INTO forecast, tau=',mtau,' I=',itc,' J=',jtc
c     write (20,*) 'INTO forecast, tau=',mtau,' I=',itc,' J=',jtc
c
      if (mtau .eq. 0) then
c       robert = 0.1               ! time filter
c       ihour  = 3600              ! hour in seconds
c       ifcst  = 12                ! forecast limit in hours
c       tendit = ifcst*ihour
c       itime  = 225               ! time step in seconds
        time   = itime             ! time-step in seconds
        twotim = 2.0*time
c       into   = 6                 ! number of edge values used in filter
cx      ismth  = 3*ihour/itime
c       ismthb = 5                 ! index to smooth boundaries only
        ekm    = 0.0d0             ! KE of system
c
c                   calculate modified PERKEY-KREITZBERG weighting function
c                   values for the time-dependent boundary conditions
c
        tend = 1.00
        do j=1, jym
          j1 = j -1
          j2 = jym -j
          do i=1, ixm
            i1 = i -1
            i2 = ixm -i
            ij = min (i1, i2, j1, j2)
            if (ij .eq. 0) then
              tend(i,j) = 0.0
            elseif (ij .eq. 1) then
              tend(i,j) = 0.05
            elseif (ij .eq. 2) then
              tend(i,j) = 0.25
            elseif (ij .eq. 3) then
              tend(i,j) = 0.45
            elseif (ij .eq. 4) then
              tend(i,j) = 0.65
            elseif (ij .eq. 5) then
              tend(i,j) = 0.85
            endif
          enddo
        enddo
c
c                   Start with all omega values set to zero
c
	www = 0.0d0
c
c                   set heating factors
c
        if (kht .ne. 0) then
          heat(1) = 0.0
          heat(2) = 0.3
          heat(3) = 1.0
          heat(4) = 0.3
c
c               multiply heating factors by estimated values for step 1
c
          do k=2, 4
            heat(k) = heat(k)*0.432*qq*pic(k)*time/86400.0
          enddo
        else
          heat = 0.0
        endif
        kout  = -1
        kount = 0
      endif
c
c                   other initial, every call
c
      if (kout .gt. 0) kout = 0
      ni  = ixm
      ni1 = ni -1
      ni2 = ni -2
      nj  = jym
      nj1 = nj -1
      nj2 = nj -2
      tendit = ifcst(kstp)*ihour
      iloc6  = ifcst(1)*ihour/itime
      istop  = ifcst(kstp)*ihour/itime
      if (mtau .eq. 66) istop  = 6*ihour/itime
      iloc  = ihour/itime
c                   count of time-steps for this run
      lstep = 0
c
c         change new values placed in xxs to change values per time-step,
c         based upon differences between new values and old xx2 values;
c         controlled by factors in tend
c
      do j=1, nj
        do i=1, ni
          zls10(i,j) = (zls10(i,j) -z210(i,j)) * (1.0 -tend(i,j))/tendit
        enddo
      enddo
      do k=1, nk
        do j=1, nj
          do i=1, ni
            tls(i,j,k) = (tls(i,j,k) -pt2(i,j,k)) * (1.0 -tend(i,j))
     &                   /tendit
          enddo
        enddo
      enddo
      do k=1, nkw
        do j=1, nj
          do i=1, ni
            uls(i,j,k) = (uls(i,j,k) -uu2(i,j,k)) * (1.0 -tend(i,j))
     &                   /tendit
            vls(i,j,k) = (vls(i,j,k) -vv2(i,j,k)) * (1.0 -tend(i,j))
     &                   /tendit
          enddo
        enddo
      enddo
c     call uvrng3a (uu2,vv2,ixm,jym,kount)
c     call ptrng4a (pt2,ixm,jym,2,kount)
c     call gzrng4a (gz2,ixm,jym,kount)
c     call ptgzrng1 (pt1(1,1,1),pt2(1,1,1),gz1(1,1,1),gz2(1,1,1),
c    &               ixm,jym)
c
c            *****  COMMENCE FORECASTING  *****
c
      nflt = 0
      do
        if (kount .ne. 0) then
c
c         use leapfrog technique to generate all subsequent forecast values
c
          call ptgzrng1 (pt1(1,1,1),pt2(1,1,1),gz1(1,1,1),gz2(1,1,1),
     &                   ixm,jym)
          kount = kount +1
          call step2 (time,robert,kount,kht,htadj,itc,jtc,nflt)
          lstep = lstep +1
          if (nflt .gt. 0) then
            write (*,*) 'MODEL UNSTABLE - ABORT, step ',kount,' ',lstep
            nogo = -1
            goto 399
c
          endif
        else
c
c           take initial time step of first forecast for tau = 0
c
c             first, locate wind center of cyclone at 850
c
          call cycloc (kout,itc,jtc,nogo)
          if (nogo .ne. 0) then
            write (*,*) 'NO INITIAL CIRCULATIION'
            goto 399
c
          endif
          call step1 (time,kht,itc,jtc)
          kount = 1
          lstep = 1
c
c           double heating for centered time steps to follow
c
          heat = 2.0*heat
        endif
c
        if (mod (kount,ismth) .eq. 0 .or. nflt .lt. 0) then
c
c                   FILTER ALL FIELDS
c
          if (nflt .lt. 0) write (20,*) 'FORCED FILTER'
          do k=1, nk
            if (k .lt. nk) then
              call filter (ni,nj,wrk81,uu1(1,1,k))
              call filter (ni,nj,wrk81,vv1(1,1,k))
              call filter (ni,nj,wrk81,uu2(1,1,k))
              call filter (ni,nj,wrk81,vv2(1,1,k))
            endif
            call filter (ni,nj,wrk81,pt1(1,1,k))
            call filter (ni,nj,wrk81,pt2(1,1,k))
          enddo
          call filter (ni,nj,wrk81,gz1(1,1,1))
          call filter (ni,nj,wrk81,gz2(1,1,1))
c
        elseif (mod (kount,ismthb) .eq. 0) then
c
c                   FILTER BOUNDARIES
c
          do k=1, nk
            if (k .lt. nk) then
              call smthbd (ni,nj,into,wrk81,uu1(1,1,k))
              call smthbd (ni,nj,into,wrk81,uu2(1,1,k))
              call smthbd (ni,nj,into,wrk81,vv1(1,1,k))
              call smthbd (ni,nj,into,wrk81,vv2(1,1,k))
            endif
            call smthbd (ni,nj,into,wrk81,pt1(1,1,k))
            call smthbd (ni,nj,into,wrk81,pt2(1,1,k))
          enddo
          call smthbd (ni,nj,into,wrk81,gz1(1,1,1))
          call smthbd (ni,nj,into,wrk81,gz2(1,1,1))
        endif
c
c                   calculate upper mass fields based upon hydrostatic Eq.
c
        call caluphi (pt1,ni,nj,gz1,nfor)
c
        call caluphi (pt2,ni,nj,gz2,nfor)
c
c                   compute omega values
c
        call omega (uu2,vv2,www)
c
c                   compute the kinetic energy of inner system
c
        ek = 0.0d0
        do k=1, nkw
          do j=3, nj -2
            do i=3, ni -2
              ek = ek +(0.5*(uu1(i,j,k)*uu2(i,j,k)) +0.5*(vv1(i,j,k)
     &             *vv2(i,j,k)))
            enddo
          enddo
        enddo
        if (kount .gt. 1) then
          if (kht .eq. 0) then
            htadj = 0.0
          elseif (kht .lt. 3) then
            htadj = ekm/ek
            if (kht .eq. 1) then
              if (htadj .lt. 1.0) htadj = 0.0
            endif
          else
            htadj = 1.0
          endif
        else
          ekm   = ek
          htadj = 1.0
        endif
c
c       write (20,900) kount, lstep, mtau, ek, htadj
c900    format(' *** step total ',i5,' loc ',i2,' fm tau ',i2,' ke is '
c    &  ,e15.7,' rate ',f10.6,' itc ',i2,' jtc ',i2)
c       call uvrng3a (uu2,vv2,ixm,jym,kount)
c       call ptrng4a (pt1,ixm,jym,1,kount)
c       call ptrng4a (pt2,ixm,jym,2,kount)
c       call gzrng4a (gz2,ixm,jym,kount)
c
        if (mod (kount,istop) .eq. 0) then
c         write (20,900) kount, lstep, mtau, ek, htadj
c         call uvrng3a (uu2,vv2,ixm,jym,kount)
c         call ptrng4a (pt1,ixm,jym,1,kount)
c         call ptrng4a (pt2,ixm,jym,2,kount)
c         call gzrng4a (gz2,ixm,jym,kount)
          kout = (kount*itime)/21600 +1
          write (*,*) 'CALL cycloc - finish'
          call cycloc (kout,itc,jtc,nogo)
          if (nogo .eq. 0)  then
	    khr = ifcst(kstp)
	    if (mtau +khr .gt. 72) khr = 6
            write (*,*)  'FINI TAU ',mtau+khr,' KE ',ek,' itc ',itc,
     &                   ' jtc ',jtc
c           write (20,*) 'FINI TAU ',mtau+khr,' KE ',ek,' itc ',itc,
c    &                   ' jtc ',jtc,' K ',kount
          endif
          goto 399
c
	elseif (mod (kount,iloc6) .eq. 0) then
c         write (20,900) kount, lstep, mtau, ek, htadj
c         call uvrng3a (uu2,vv2,ixm,jym,kount)
c         call ptrng4a (pt1,ixm,jym,1,kount)
c         call ptrng4a (pt2,ixm,jym,2,kount)
c         call gzrng4a (gz2,ixm,jym,kount)
	  kout = (kount*itime)/21600 +1
	  write (*,*) 'Call cycloc - tau ',mtau+6,' positioning'
	  call cycloc (kout,itc,jtc,nogo)
	  if (nogo .eq. 0) then
c           call ptgzrng1 (pt1(1,1,1),pt2(1,1,1),gz1(1,1,1),gz2(1,1,1),
c    &                     ixm,jym)
	    kout = 0
          else
	    goto 399
c
	  endif
        elseif (mod (kount,iloc) .eq. 0) then
c
c                locate tropical cyclone every hour with isogons
c
          call cycloc (kout,itc,jtc,nogo)
c         if (nogo .eq. 0) then
c           call ptgzrng1 (pt1(1,1,1),pt2(1,1,1),gz1(1,1,1),gz2(1,1,1),
c    &                     ixm,jym)
c         else
          if (nogo .ne. 0) then
c           write (20,900) kount, lstep, mtau, ek, htadj
c           call uvrng3a (uu2,vv2,ixm,jym,kount)
c           call ptrng4a (pt1,ixm,jym,1,kount)
c           call ptrng4a (pt2,ixm,jym,2,kount)
c           call gzrng4a (gz2,ixm,jym,kount)
	    goto 399
c
	  endif
        endif
      enddo
c
  399 continue
c
      end
      subroutine get_idat (nuin,cpdtg,kht,nogo)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  get_idat
c
c  DESCRIPTION:  get initial cyclone data to start model run
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE: call get_idat (nuin,cpdtg,kht,nogo)
c
c  PARAMETERS:
c       Name          Type       Usage            Description
c    ----------    --------     -------   ----------------------------
c      nuin          int         input    input unit number
c      cpdtg         char        input    cyclone position dtg
c      kht           int         output   heating flag
c      nogo          int         output   flag for continued processing
c                                            0 - continue processing
c                                           -1 - stop processing
c
c  COMMON BLOCKS:
c     name      variable        description
c   ---------  -----------    -----------------------------------------
c    vort_c     ijoff         ij-offset for model cyclone
c               radmx         maximum radius of model cyclone
c               dnorm         normalizing factor in wind calculation
c
c   i_cyclone   iwndmx        maximum wind of cyclone
c               mwndmx        maximum wind of model cyclone
c
c   r_cyclone   rlat          latitude  of cyclone (- SH)
c               rlon          longitude of cyclone (0 -> 359.9) E
c               head          heading of cyclone (deg)
c               speed         speed of cyclone (kts)
c
c   c_cyclone   cycdtg        dtg of starting cyclone position
c
c   latlon      flat          array of cyclone latitudes
c               flon          array of cyclone longitudes
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c    otcmdat      10                                  optional
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     unknown input            set nogo to -1 and exit
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  CALLED BY:  otcm
c
c  MODULES CALLED:
c      Name           Description
c     -------     ----------------------
c      chkdat     check validity of file input data
c      icrdtg     calculate other dtg's
c      dirdist    given starting and ending lat/lon's calculate heading
c                 and distance - rhumb line method
c
c  LOCAL VARIABLES:
c      Name      Type                 Description
c     ------     ----       -----------------------------------------
c     ivrad      int        optional input - integer radius of model cyclone
c     olat       real       12 hr old latitude
c     olon       real       12 hr old longitude
c     plat       real       06 hr old latitude
c     plon       real       06 hr old longitude
c
c  METHOD:
c
c  INCLUDE FILES:
c
c  COMPILER DEPENDENCIES:  f77
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      integer maxchr
      parameter (maxchr = 3)
      INCLUDE 'par_wind.inc'
c
c         formal parameters
      integer nuin, kht,  nogo
      character*8 cpdtg
c
c         local variables
      integer ioe, mxk, n, ior, kk, indx, ivrad
      integer icrlng(2), iparms(2), mnoff(10)
      integer ios, ibtwind
c
      character*1 cns, cew, cnsp, cewp, cnso, cewo
      character*8 dtgm6, dtgm12
      character*8 btdtg
      character*2 cent
      character*80 cline
      character*1 btns, btew
      real plat, plon, olat, olon, dist, vrad
      real dvrad(10)
      real btlat, btlon
c
c                   cyclone parameters
c
      INCLUDE 'cyc_c_com.inc'
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'fltln_com.inc'
      INCLUDE 'vort_com.inc'
c
      data icrlng/1,1/, iparms/0,0/
      data mnoff/ 8,  8,  7,  7,  6,  6,  5,  5,  4,   4/
      data dvrad/8.1,7.6,7.1,6.6,6.1,5.6,5.1,4.6,4.25,4.25/
c
c       Number of characters for each parameter:
c
c          1 -  1  vortex radius flag, (4 < > 8) or 0, grid length
c                                    0 - flag for automatic calculation
c          2 -  1  heating factor (0, 1, 2, or 3)
c                                    2 - default value
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   obtain optional input data
c
      nogo  = 0
      ivrad = 0  ! default value
      kht   = 2  ! default value
      open (10,file='otcmdat',iostat=ioe)
      if (ioe .eq. 0) then
        mxk = maxchr
        do n=1, 2
          cline = ' '
          read (10,'(a)',iostat=ior,end=200) cline
          if (ior .eq. 0) then
            call chkdat (icrlng(n),mxk,cline,kk)
            if (kk .eq. icrlng(n)) then
              if (n .eq. 1) then
                read (cline(1:kk),'(i1)') ivrad
                iparms(1) = -1
              else
                read (cline(1:kk),'(i1)') kht
		if (kht .lt. 0) then
		  write (*,*) 'WARNING kht < 0, set to 2'
		  kht = 2
		elseif (kht .gt. 3) then
		  write (*,*) 'WARNING kht > 3, set to 3'
		  kht = 3
                endif
                iparms(2) = -1
              endif
            else
              write (*,*) 'UNKNOWN input is ',cline(1:kk)
              nogo = -1
            endif
          else
	    write (*,*) 'OK, missing optional input ',n
	  endif
        enddo
  200   continue
      else
        write (*,*) 'OK, optional otcmdat file not found'
      endif
      if (nogo .eq. 0) then
c
c                   now find the current, -6 hr and -12 hr positions
c
        call icrdtg (cpdtg,dtgm6,-6)
        call icrdtg (cpdtg,dtgm12,-12)
        rewind (nuin)
	olat = 0.0
	plat = 0.0
        rlat = 0.0
        ios = 0
        do while (ios .eq. 0)
           call readBT(nuin,cent,btdtg,btlat,btns,btlon,btew,ibtwind,
     &                 ios)
           if( ios.eq.0 .and. btdtg .eq. dtgm12 ) then
c                   12-hr old position
              olat = btlat
              cnso = btns
              olon = btlon
              cewo = btew
              if (cnso .eq. 'S') olat = -olat
              if (cewo .eq. 'W') olon = 360.0 -olon
           else if( ios.eq.0 .and. btdtg .eq. dtgm6 ) then
c                   6-hr old position
              plat = btlat
              cnsp = btns
              plon = btlon
              cewp = btew
              if (cnsp .eq. 'S') plat = -plat
              if (cewp .eq. 'W') plon = 360.0 -plon
           else if( ios.eq.0 .and. btdtg .eq. cpdtg ) then
c                   present position and maximum sustained wind speed
              rlat = btlat
              cns = btns
              rlon = btlon
              cew = btew
              iwndmx = ibtwind
              write(*,900) rlat,cns, rlon,cew
 900          format(' START: ',f4.1,a1,2x,f5.1,a1)
              if (cns .eq. 'S') rlat = -rlat
              if (cew .eq. 'W') rlon = 360.0 -rlon
              if (ivrad .eq. 0) then
                 indx = (iwndmx -25)/5
                 if (indx .lt. 1) then
                    indx = 1
                 elseif (indx .gt. 10) then
                    indx = 10
                 endif
                 ijoff = mnoff(indx)
                 radmx = dvrad(indx)
                 write (*,*) 
     &                 'RADMX set to ',radmx,' for max wind of ',iwndmx
              else
                 ivrad = max0 (4,ivrad)
                 ivrad = min0 (8,ivrad)
                 ijoff = ivrad
                 radmx = float(ijoff) +0.1
              endif
              vrad = radmx -0.1
              if (vrad .gt. 4.4) then
                 dnorm = 4.0/vrad
              else
                 dnorm = 1.0
              endif
           endif
        enddo
c
   60   continue
        if (olat .ne. 0.0) then
          call dirdist (olat,olon,rlat,rlon,head,dist)
          speed = dist/12.0
        elseif (plat .ne. 0.0) then
          call dirdist (plat,plon,rlat,rlon,head,dist)
          speed = dist/6.0
        else
          head = -9999.9
        endif
c
c                   set reported location of cyclone
c
        flat(0) = rlat
        flon(0) = rlon
c
c                   set analysis and forecast positions to missing
c
        do n=1, 13
          flat(n) = -99.99
          flon(n) = -99.99
        enddo
c
c                   calculate model cyclone wind speed
c
        mwndmx = iwndmx
        if (mwndmx .lt. min_wnd_spd) then
          mwndmx = min_wnd_spd
        elseif (mwndmx .gt. max_wnd_spd) then
          mwndmx = max_wnd_spd
        endif
c
c                   set cyclone position dtg
c
        cycdtg(3:10) = cpdtg
	cycdtg(1:2) = cent
      endif
c
      write (*,*) 'get_dat: ijoff ',ijoff,'  radmx ',radmx,'  dnorm ',
     &              dnorm
c
      end
      double precision function gzptint8 (i,j,bfld,ix,jy)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)gzptint8.f90	1.1  6/1/96
c
c  MODULE NAME:  CYCITR8
c
c  DESCRIPTION:  INTERPOLATE FIELD, BFLD, WHICH IS A REGIONAL FIELD OF
c                DOUBLE PRECISION VALUES.
c
c                BASED UPON AYRES CENTRAL DIFFERENCE FORMULA WHICH
c                PRODUCES VALUES THAT ARE CONTINUOUS IN THE FIRST
c                DERIVATIVE, EXCEPT NEAR LIMITS OF THE GRID,
c                WHERE BILINEAR INTERPOLATION IS USED.
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  FNOC SUBROUTINE WRITEUP FOR CYCIT5
c
c  CLASSIFICATION:  UNCLASSIFIED
c
c  RESTRICTIONS:  BFLD MUST BE 4 BY 4 OR LARGER FIELD
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  NONE
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  VAL = GZPTINT8 (I,J,BFLD,IX,JY)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c        I          INT          IN     FIRST  DIMENSION POINT LOCATION
c        J          INT          IN     SECOND DIMENSION POINT LOCATION
c     BFLD         REAL          IN     FIELD  FOR INTERPOLATION
c       IX          INT          IN     FIRST  DIMENSION OF BFLD
c       JY          INT          IN     SECOND DIMENSION OF BFLD
c
c  COMMON BLOCKS:  NONE
c
c  FILES:  NONE
c
c  DATA BASES:  NONE
c
c  NON-FILE INPUT/OUTPUT:  NONE
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     BFLD TOO SMALL           SET CYCITR8 TO ERROR VALUE
c     OUT-OF-BOUNDS            SET CYCITR8 TO ERROR VALUE
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  NONE
c
c  LOCAL VARIABLES:
c
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c             AA     REAL       INTERPOLATION FACTOR
c             BB     REAL       INTERPOLATION FACTOR
c             CC     REAL       INTERPOLATION FACTOR
c          EV3M1     REAL       INTERPOLATION FACTOR
c          EV3M2     REAL       INTERPOLATION FACTOR
c          EV4M2     REAL       INTERPOLATION FACTOR
c            ECV     REAL       INTERPOLATED ROW OR COLUMN VALUES
c                               FOR FINAL INTERPOLATION
c             M2      INT       TRUNCATED FIRST DIMENSION POINT LOCATION
c             M3      INT       M2 +1
c             N2      INT       TRUNCATED SECOND DIMENSION LOCATION
c             N3      INT       N2 +1
c              R     REAL       FRACTION OF FIRST DIMENSION OF GRID
c                               POINT IS LOCATED FROM M2
c             RN     REAL       REAL REPRESENTATIVE OF RNL
c             RM     REAL       REAL REPRESENTATIVE OF RML
c              S     REAL       FRACTION OF SECOND DIMENSION OF GRID
c                               POINT IS LOCATED FROM N2
c           VFLD     REAL       BLOCK OF VALUES USED FOR INTERPOLATION
c
c  METHOD:  1.  AYRES CENTRAL DIFFERENCE FORMULA USED IN TWO DIMENSIONS
c           2.  Assume grid has double grid length, and interpolate at
c               the grid point (i,j) as though it were at .5 from m2,n2.
c
c  INCLUDE FILES: NONE
c
c  COMPILER DEPENDENCIES:  FORTRAN 90
c
c  COMPILE OPTIONS:  STANDARD FNOC OPERATIONAL OPTIONS
c
c  MAKEFILE:  N/A
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  H. Hamilton
c    initial installation on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c     formal parameters
c
      integer           i, j, ix, jy
      double precision  bfld(ix,jy)
c
c     local variables
c
      integer          m2, n2, m3, n3, k, n, m
      double precision ev3m1, ev3m2, ev4m2, aa, bb, cc, r, s
      double precision ecv(4), vfld(16), error
c
      data error/-999999999.9d0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (ix .ge. 7 .and. jy .ge. 7) then
c
        m2 = i -1
        n2 = j -1
        if (m2.ge.3 .and. m2.lt.(ix-4) .and. n2.ge.3 .and. n2.lt.(jy-4))
     &    then
c
c                   PERFORM INTERPOLATION BASED UPON AYRES
c
          k = 0
c                   LOAD 4-BY-4 ARRAY, VFLD, FOR INTERPOLATION
          do n=n2-2, n2+4, 2
            do m=m2-2, m2+4, 2
              k = k +1
              vfld(k) = bfld(m,n)
            enddo
          enddo
c
c                   PERFORM AYRES CENTRAL DIFFERENCES AND INTERPOLATION,
c                           FOUR TIMES TO LOAD ECV
c
          r = 0.5d0
          s = 0.5d0
c
          do k=1, 4
            ev3m1  = vfld(k+8) -vfld(k)
            ev3m2  = vfld(k+8) -vfld(k+4)
            ev4m2  = 0.5d0*(vfld(k+12) -vfld(k+4))
            aa     = 0.5d0*ev3m1
            bb     = 3.0d0*ev3m2 -ev3m1 -ev4m2
            cc     = aa +ev4m2 -ev3m2 -ev3m2
            ecv(k) = vfld(k+4) +s*(aa +s*(bb +s*cc))
          enddo
c
c                   PERFORM AYRES CENTRAL DIFFERENCES WITH ECV
c
          ev3m1 = ecv(3) -ecv(1)
          ev3m2 = ecv(3) -ecv(2)
          ev4m2 = 0.5d0*(ecv(4) -ecv(2))
          aa    = 0.5d0*ev3m1
          bb    = 3.0d0*ev3m2 -ev3m1 -ev4m2
          cc    = aa +ev4m2 -ev3m2 -ev3m2
          gzptint8 = ecv(2) +r*(aa +r*(bb +r*cc))
c
        elseif (m2.ge.1 .and. m2.lt.ix-1 .and. n2.ge.1 .and. n2.lt.jy-1)
     &   then
c
c                   DOUBLE LINEAR
c
          m3 = m2 +2
          n3 = n2 +2
          gzptint8 = 0.25d0*(bfld(m2,n2) +bfld(m3,n2) +bfld(m2,n3)
     &              +bfld(m3,n3))
c
        else
c
c                   TOO NEAR EDGE, RETURN ERROR VALUE
c
          gzptint8 = error
        endif
      else
c
c                   ERROR VALUE RETURNED, BFLD MUST BE 7 BY 7 OR LARGER
c
        gzptint8 = error
c
      endif
c
      end
      subroutine gzrng4a (gz,ix,jy,kkk)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)gzrng4a.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  gzrng4a
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      integer           kkk
      double precision  gz(ix,jy,4)
c
      integer           kk
      double precision  sum, gzx(4), gzn(4), gza(4)
c
c . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do k=1, 4
        gzx(k) = -999999.9d0
        gzn(k) = -gzx(k)
        sum    = 0.0d0
        kk     = 0
        do j=1, jy
          do i=1, ix
            gzx(k) = max (gzx(k),gz(i,j,k))
            gzn(k) = min (gzn(k),gz(i,j,k))
            sum    = sum +gz(i,j,k)
            kk     = kk +1
          enddo
        enddo
        gza(k) = sum/kk
      enddo
c
      write(20,900) kkk,gzx(1),gzx(2),gzx(3),gzx(4)
  900 format ('Step ',i4,' A-GZ mx 1-4 ',4f12.3)
c     write(*,910) kkk,gza(1),gza(2),gza(3),gza(4)
      write(20,910) kkk,gza(1),gza(2),gza(3),gza(4)
  910 format ('Step ',i4,' A-GZ av 1-4 ',4f12.3)
c     write(*,920) kkk,gzn(1),gzn(2),gzn(3),gzn(4)
      write(20,920) kkk,gzn(1),gzn(2),gzn(3),gzn(4)
  920 format ('Step ',i4,' A-GZ mn 1-4 ',4f12.3)
c
      end
      subroutine isocnt (dfld,mgrd,ngrd,mgbyng,kntr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)isocnt.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isocnt
c
c  DESCRIPTION:  driver for producing isogons in pairs, 90 degrees
c                apart, and solving for the intersection of each pair
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:
c    CONTOURING AND HIDDEN-LINE ALGORITHMS FOR VECTOR GRAPHIC DISPLAYS.
c    AFAPL-TR-77-3, JANUARY 1977.                      DDC: AD A040530
c    AIR FORCE AERO-PROPULSION LABORATORY
c    AIR FORCE WRIGHT AERONAUTICAL LABORATORIES
c    AIR FORCE SYSTEMS COMMAND
c    WRIGHT-PATTERSON AIR FORCE BASE, OHIO 45433
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call isocnt (dfld,mgrd,ngrd,mgbyng,kntr)
c
c  PARAMETERS:
c     NAME         TYPE     USAGE             DESCRIPTION
c   --------      ------    -----    ------------------------------
c     dfld         real       in     wind direction field
c     mgrd          int       in     first  dimension of field
c     ngrd          int       in     second dimension of field
c   mgbyng          int       in     total length of field
c     kntr          int      out     number of isogons
c
c  CALLED BY:  cirloc.f
c
c  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
c                              ARE DEFINED IN THE CODE WITHIN INCLUDE
c                              FILES.  THIS MODULE USES THE FOLLOWING
c                              COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE   USAGE              NOTES
c     --------  --------   ----   -----   ------------------------
c       isoc        rh     real    out    real value of isogon, deg
c                 iter      int    out    iteration number
c                  nc1      int    out    isogon count first  iteration
c                  nc2      int    out    isogon count second iteration
c       isol     first      log    out    flag, true if start
c                 last      log    out    flag, true if end
c                 open      log    out    flag, true if open contour
c               backwd      log    out    flag, true if backward contour
c      mndir        ii      int    out    starting minimum first dim of
c                                         contouring block
c                   jj      int    out    starting minimum second dim of
c                                         contouring block
c                   iv      int    out    starting first dim contour
c                                         direction vector
c                   jv      int    out    starting second dim contour
c                                         direction vector
c       view      mini      int     in    starting first dim of box
c                 maxi      int     in    ending first dim of box
c                 minj      int     in    starting second dim of box
c                 maxj      int     in    ending second dim of box
c      zoomv      rint     real    out    first dim resolution of zoomed
c                                         block
c                 sint     real    out    second dim resolution of
c                                         zoomed block
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     wrong dimensions of      error diagnostics and exit
c     zoomed block
c
c  ADDITIONAL COMMENTS:
c     No closed contours are allowed, so this code has been removed.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         iostrc      traces isogons through field
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----    ----------------------------------
c            brh     real    base real "height" value
c           cint     real    contour interval
c           cntr     real    starting contour value
c            dtr     real    degree-to-radian conversion factor
c             hc     real    "height" value being contoured
c          ijtoi      int    double to single index function
c             jp      int    second index point
c           kzlk      int    first dimension of zoomed block
c           lzlk      int    secomd dimension of zoomed block
c           lfld      log    array for contour flags
c         maxim1      int    maxi -1
c         maxjm1      int    maxj -1
c         minip1      int    mini +1
c         minjp1      int    minj +1
c           mxnc      int    maximum number of contours
c            nij      int    single index for i,j location
c           nijp      int    nij of "upper" grid point
c             nr      int    number of contours
c           rdmn     real    minimum value of contour
c           rdmx     real    maximum value of contour
c             rh     real    real "height" value of contour
c             ru     real    "upper" value at grid point
c             rl     real    "lower" value at grid point
c           sfld     real    sine of (dd -rh)
c           zblk     real    zoomed block array
c
c  METHOD:
c    1.  Modification of contouring routines previously developed by
c        H. D. Hamilton for FNOC program CODEDEF.
c    2.  The trick in generating isogons is to trace the zero value of
c        sine (wind direction minus desired isogon direction).
c        Note that sine (0) equals sine (180).  Therefore, if the isogon
c        spacing is 10 degrees, only 10 through 180 degrees is required
c        to provide complete coverage.
c    3.  In order to improve the quality of the intersection point,
c        isogons are produced sequentially in pairs, 90 degrees apart.
c        Therefore, if the 10 degree isogon is not produced, the 100
c        degree isogon is not attempted.
c    4.  Since a complete field of isogons is not desired, only one
c        isogon is allowed for each direction.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------     ----------------------------------------------
c           isoc.inc      common block
c           isol.inc      common block
c          mndir.inc      common block
c           view.inc      common block
c           zoom.inc      common block
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation, with OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      integer kzlk,lzlk
      parameter (kzlk = 11,  lzlk = 11)
c
c         formal parameters
      integer mgrd, ngrd, mgbyng, kntr
      real dfld(mgrd,ngrd)
c
c         local variables
      logical lfld(mgbyng)
      integer ijtoi, i, j, minip1, minjp1, maxim1, maxjm1, nr
      integer mxnc, k, mn, nij, nijp, jp
      real    hc, rdmn, rdmx, cint, cntr, brh, ru, rl
      real    sfld(mgbyng), zblk(kzlk,lzlk)
      double precision dtr, ddval
c
      INCLUDE 'view.inc'
      INCLUDE 'isol.inc'
      INCLUDE 'isoc.inc'
      INCLUDE 'mndir.inc'
      INCLUDE 'zoomv.inc'
c
      data hc/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c         integer statement function:
      ijtoi(i,j) = (j-1)*mz +i
c
c - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
c
      dtr    = acos (-1.0d0)/180.0d0
      mz     = mgrd
      nz     = ngrd
      mbyn   = mgbyng
      kzlt   = kzlk
      lzlt   = lzlk
      rint   = 1.0/(kzlt -1)
      sint   = 1.0/(lzlt -1)
      minip1 = mini +1
      minjp1 = minj +1
      maxim1 = maxi -1
      maxjm1 = maxj -1
      nr     = 0
c
c           contouring is accomplished at one value, hc, at a time,
c           and one contour at a time.  true value of isogon is rh.
c
      rdmn =   1.0
      rdmx = 360.0
      cint =  10.0
      cntr = cint
      mxnc = anint (180.0/cint)
      brh  = cntr -cint
      do 490 k=1, mxnc
        if (mod (k,2) .ne. 0) then
          brh  = brh +cint
          rh   = brh
          iter = 1
          nc1  = 0
          nc2  = 0
        else
c                   check that first contour has more than one point
          if (nc1 .lt. 5) goto 490
c
          rh   = rh +90.0
          iter = 2
        endif
c       write (9,*) ' isocnt, k ',k,' iter ',iter,' rh ',rh
        if (rh .lt. rdmn .or. rh .gt. rdmx) goto 490
c
c       write (9,9010) rh
c9010   format (1x,'contouring all contours of value ',g11.5)
c
c                   field to be contoured, sfld, must be the sine of the
c                   difference between the true wind direction and the
c                   true value of the direction to be contoured, rh.
c                   note, the actual value of the contour being traced,
c                   hc, is always zero.
c
c                   initailize sfld and lfld
c
          do mn=1, mbyn
            lfld(mn) = .false.
	    ddval    = dfld(mn,1) -rh
            sfld(mn) = sin (ddval*dtr)
          enddo
c
c               set edge bits for backward scan
c
c                        bottom row
        nij = ijtoi(mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          rl  = ru
          ru  = sfld(nij+1)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nij +1
        enddo
c                        right side
        nij = ijtoi (maxi,minj)
        ru  = sfld(nij)
        do j=minjp1, maxj
          rl   = ru
          nijp = ijtoi (maxi,j)
          ru   = sfld(nijp)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nijp
        enddo
c                        top row
        nij = ijtoi (maxi,maxj)
        ru  = sfld(nij)
        do i=maxim1, mini, -1
          rl  = ru
          ru  = sfld(nij-1)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nij -1
        enddo
c                        left side
        nij = ijtoi (mini,maxj)
        ru  = sfld(nij)
        do j=maxjm1, minj, -1
          rl   = ru
          nijp = ijtoi (mini,j)
          ru   = sfld(nijp)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nijp
        enddo
c
        backwd = .false.
        open   = .true.
        first  = .true.
        last   = .false.
        kkk    = 0
c
c               the boundary of the array is scanned for the
c               beginning of any open contour of value hc, forward mode.
c
c                   scan bottom
        iv  = -1
        jv  =  0
        jj  = minj
        nij = ijtoi (mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          ii  = i
          rl  = ru
          nij = nij +1
          ru  = sfld(nij)
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c                   scan right side
        iv =  0
        jv = -1
        ii = maxi
        ru = sfld(ijtoi (maxi,minj))
        do j=minjp1, maxj
          rl = ru
          jj = j
          ru = sfld(ijtoi (maxi,j))
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   scan top
c
        iv  = 1
        jv  = 0
        jj  = maxj
        nij = ijtoi(maxi,jj)
        ru  = sfld(nij)
        do i=maxim1, mini, -1
          ii  = i
          rl  = ru
          nij = nij -1
          ru  = sfld(nij)
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   scan left side
c
        iv = 0
        jv = 1
        ii = mini
        j  = maxj
        ru = sfld(ijtoi(mini,j))
        do j=maxjm1, minj, -1
          rl = ru
          jj = j
          ru = sfld(ijtoi (mini,j))
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   rescan edges, using backward mode
c
        backwd = .true.
c
c                   scan bottom
c
c       write(9,*) 'isocnt, starting open backwards'
        iv  = 1
        jv  = 0
        jj  = minj
        nij = ijtoi (mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          ii   = i -1
          rl   = ru
          ru   = sfld(nij+1)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          nij = nij +1
        enddo
c
c                    scan right side
c
        ii  = maxi
        iv  = 0
        jv  = 1
        nij = ijtoi (maxi,minj)
        ru  = sfld(nij)
        jj  = minj
        do j=minjp1, maxj
          rl   = ru
          jp   = j
          nijp = ijtoi (maxi,jp)
          ru   = sfld(nijp)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          jj  = jp
          nij = nijp
        enddo
c
c                   scan top
c
        iv  = -1
        jv  =  0
        jj  = maxj
        nij = ijtoi (maxi,jj)
        ru  =  sfld(nij)
        do i=maxim1, mini, -1
          ii  = i +1
          rl  = ru
          ru  = sfld(nij-1)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          nij = nij -1
        enddo
c
c                   scan left side
c
        ii  =  mini
        iv  =  0
        jv  = -1
        jj  = maxj
        nij = ijtoi (mini,jj)
        ru  = sfld(nij)
        do j=maxjm1, minj, -1
          rl   = ru
          jp   = j
          nijp = ijtoi (mini,jp)
          ru   = sfld(nijp)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
c             write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          jj  = jp
          nij = nijp
        enddo
  450   continue
        if (kkk .ne. 0) nr = nr +1
  490 continue
c     if (nr .gt. 0) then
c       write (9,9020) nr
c     else
c       write (9,9030)
c     endif
c9020 format(' found about ',i3,' different valued contours')
c9030 format('   *** no contours ***')
      kntr = nr
c
      end
      subroutine isofnd (exc,eyc,nhsh,ddfld,igrdx,jgrdy,kccf,kuvs,kint,
     &                   xc,yc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)isofnd.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isofnd
c
c  DESCRIPTION:  driver routine to locate tropical cyclone with isogons
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  isofnd (exc,eyc,nhsh,ddfld,igrdx,jgrdy,kccf,kuvs,kint,xc,yc)
c
c  PARAMETERS:
c     NAME         TYPE      USAGE             DESCRIPTION
c   --------      -------    ------   ------------------------------
c       exc        real        in     x-location, estimated
c       eyc        real        in     y-location, estimated
c      nhsh         int        in     north/south indicator, +nh -sh
c     ddfld        real        in     wind direction global field, deg
c     igrdx         int        in     first  (x-lon) dimension of fields
c     jgrdy         int        in     second (y-lat) dimension of fields
c      kccf         int       out     cyclonic circulations found
c      kuvs         int       out     code of wind support
c                                          0 - no cyclone
c                                          3 - wind support in 3 quads
c                                          4 - wind support in 4 quads
c      kint         int       out     count of intersection support
c        xc        real       out     x-location of tropical cyclone
c        yc        real       out     y-location of tropical cyclone
c
c  CALLED BY:  confirm.f & cycloc.f
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c          cirloc     driver routine to locate circulation center
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----     ----------------------------------
c           imax      int     maximum x-edge of isogon window
c           imin      int     minimum x-edge of isogon window
c           isx       int     x-truncated point of search
c           ixgd      int     first dimension of global fields
c           jmax      int     maximum y-edge of isogon window
c           jmin      int     minimum y-edge of isogon window
c           jsy       int     y-truncated point of search
c           jygd      int     second dimension of global fileds
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997)  Hamilton, H.
c    Initial installation, with OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer nhsh, igrdx, jgrdy, kccf, kuvs(4), kint(4)
      real exc, eyc, xc(4), yc(4)
      real ddfld(igrdx,jgrdy)
c
c         local variables
      integer isx, jsy, imin, imax, jmin, jmax, ixgd, jygd
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      kccf  = 0
      xc(1) = exc
      isx   = exc
      yc(1) = eyc
      jsy   = eyc
      ixgd  = igrdx
      jygd  = jgrdy
c
c                   establish isogon window for search
c
      imin = isx  -1
      imax = imin +3
      jmin = jsy  -1
      jmax = jmin +3
c
c                   call driver for using isogon routines
c
      call cirloc (ddfld,ixgd,jygd,imin,jmin,imax,jmax,nhsh,kccf,kuvs,
     &             kint,xc,yc)
c     if (kccf .le. 0) write (20,*) ' $ $ $ ISOFND, CYCLONE NOT FOUND'
c
      end
      subroutine isotrc (sfld,lfld,zblk)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)isotrc.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isotrc
c
c  DESCRIPTION:  routine to trace isogons through field sfld via zoomed
c                grid blocks
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  see isocnt for references
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call isotrc (sfld,lfld,zblk)
c
c  PARAMETERS:
c     NAME         TYPE       USAGE             DESCRIPTION
c   --------      -------     ------   ------------------------------
c     sfld           real       in     field to be contoured
c     lfld        logical       in     field with contour flags set
c     zblk           real       in     working array for zooming
c
c  CALLED BY:  isocnt.f
c
c  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
c                              ARE DEFINED IN THE CODE WITHIN INCLUDE
c                              FILES.  THIS MODULE USES THE FOLLOWING
c                              VARIABLES IN NAMED BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c        box      lbox      int     in    unit number for diagnostics
c                   xs     real     in    starting first dimension of
c                                         isogon box
c                   xl     real     in    ending first dimension of
c                                         isogon box
c                   ys     real     in    starting second dimension of
c                                         isogon box
c                   yl     real     in    ending second dimension of
c                                         isogon box
c
c       view      mini      int     in    starting first dim of box
c                 maxi      int     in    ending first dim of box
c                 minj      int     in    starting second dim of box
c                 maxj      int     in    ending second dim of box
c
c       isoc        rh     real     in    real value of isogon, deg
c                 iter      int     in    iteration number
c                  nc1      int    out    isogon count first  iteration
c                  nc2      int    out    isogon count second iteration
c
c       isol     first      log    out    flag, true if start
c                 last      log    out    flag, true if end
c                 open      log     in    flag, true if open contour
c               backwd      log     in    flag, true if backward contour
c
c      mndir        ii      int     in    starting minimum first dim of
c                                         contouring block
c                   jj      int     in    starting minimum second dim of
c                                         contouring block
c                   iv      int     in    starting first dim contour
c                                         direction vector
c                   jv      int     in    starting second dim contour
c                                         direction vector
c                  kkk      int    out    contour generation indicator
c
c     zoomv       kzlt      int     in    first  dim of zoomed block
c                 lzlt      int     in    second dim of zoomed block
c                 mbyn      int     in    length of sfld
c                   mi      int    out    starting minimum first dim of
c                                         contouring block
c                   mz      int     in    first dimension of sfld
c                   nj      int    out    starting minimum second dim of
c                                         contouring block
c                   nz      int     in    second dimension of sfld
c                 rint     real     in    first dim resolution of zoomed
c                                         block
c                 sint     real     in    second dim resolution of
c                                         zoomed block
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                       ACTION
c     -----------------             ----------------------------
c     bad interpolation             error diagnostic and exit
c     no start-point in block       error diagnostic and exit
c     too many contour points       error diagnostic and exit
c
c  ADDITIONAL COMMENTS:
c     No closed contours are allowed - some code commented out
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         calint      calculate intersection of two isogons
c         isovzm      zoom grid square values into zblk
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c             hc     real       value of contour being contoured
c           ierr      int       interpolation flag, 0 no error
c          ijtoi      int       two dimension to one dimension function
c            ija      int       single index of point a
c            ijb      int       single index of point b
c            ijc      int       single index of point c
c            ijo      int       single index of point o
c             ka      int       first dim of point a in block
c             kb      int       first dim of point b in block
c             kc      int       first dim of point c in block
c             kf      int       first dim of point f in block
c            klt      int       temp storage
c             kv      int       first dim vector in block
c             la      int       second dim of point a in block
c             lb      int       second dim of point b in block
c             lc      int       second dim of point c in block
c             lf      int       second dim of point f in block
c             lv      int       second dim vector in block
c            mim      int       mi -1
c            mip      int       mi +1
c            njm      int       nj -1
c            njp      int       nj +1
c           nval      int       number of points in contour
c         nxylmt      int       error flag, 0 no error
c              t     real       grid length fraction
c            xus     real       x-grid point values of contour
c            yus     real       y-grid point values of contour
c             za     real       "height" value at point a
c             zb     real       "height" value at point b
c             zc     real       "height" value at point c
c             zf     real       "height" value at point f
c
c  METHOD:  see isocnt method and reference
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------     ----------------------------------------------
c            box.inc      common block
c           isoc.inc      common block
c           isol.inc      common block
c          isoxy.inc      common block
c          mndir.inc      common block
c           view.inc      common block
c          zoomv.inc      common block
c
c  COMPILER DEPENDENCIES:  Fortran 77
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation, with OTCM
c
c...................END PROLOGUE.......................................
c
c
      implicit none
c
      integer ncnt
      parameter (ncnt = 51)
c
      INCLUDE 'zoomv.inc'
c
      logical lfld(mbyn)
      real    sfld(mz,nz), zblk(kzlt,lzlt)
c
      integer ijtoi, i, j, ka, la, ierr, kv, lv, nt, n, kf, lf, njp
      integer ija, ijo, ijb, ijc, nval, kb, lb, klt, kc, lc
      integer mim, njm, mip, nn, nxylmt
      real    hc, zf, za, t, zb, zc
      real    xus(ncnt), yus(ncnt)
c
      INCLUDE 'view.inc'
      INCLUDE 'box.inc'
      INCLUDE 'isol.inc'
      INCLUDE 'isoc.inc'
      INCLUDE 'mndir.inc'
      INCLUDE 'isoxy.inc'
c
      data hc/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c         integer function:
      ijtoi(i,j) = (j -1)*mz +i
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c              initialize conturing variables
c                     mi  i-value in sfld of lower left point
c                     nj  j-value in sfld of lower left point
c                     ka  k-value in grid point block of point a
c                     la  l-value in grid point block of point a
c
      mi = ii
      nj = jj
      if (.not. backwd) then
        if (iv .eq. -1) then
          mi = mi -1
          ka = 1
          la = 1
        elseif (jv .eq. -1) then
          mi = mi -1
          nj = nj -1
          ka = kzlt
          la = 1
        elseif (iv .eq. 1) then
          nj = nj -1
          ka = kzlt
          la = lzlt
        elseif (jv .eq. 1) then
          ka = 1
          la = lzlt
        endif
c
      else
        if (iv .eq. 1) then
          ka = kzlt
          la = 1
        elseif (jv .eq. 1) then
          mi = mi -1
          ka = kzlt
          la = lzlt
        elseif (iv .eq. -1) then
          mi = mi -1
          nj = nj -1
          ka = 1
          la = lzlt
        elseif (jv .eq. -1) then
          nj = nj -1
          ka = 1
          la = 1
        endif
      endif
c
c              remove flag set in subroutine isocnt
      lfld(ijtoi(ii,jj)) = .false.
c
c                   zoom grid into zblk
      call isovzm (sfld,zblk,ierr)
      if (ierr .ne. 0) then
c       write ( *,*) ' $$$ isotrc, initial mi ',mi,' nj ',nj,
c    &               ' out of bounds'
        goto 300
c
      endif
c
c              determine start point of contour in grid block
      kv = iv
      lv = jv
      nt = kzlt -1
      do n=1, nt
        kf = ka -kv
        lf = la -lv
        if (zblk(ka,la) .lt. hc  .and.  zblk(kf,lf) .ge. hc) goto 120
c
        ka = kf
        la = lf
      enddo
c     write (33,9010) hc, kf, lf
c     write (lbox,9010) hc, kf, lf
c9010 format (' $$$$$ no start point for contour ',g11.5,2(2x,i3))
      njp = nj +1
c     write (33,9020) mi,njp, mi+1,njp, mi,nj, mi+1,nj
c     write (lbox,9020) mi,njp, mi+1,njp, mi,nj, mi+1,nj
c9020 format (1x,'c ',i2,',',i3,5x,'b ',i2,',',i3,/,
c    &        1x,'a ',i2,',',i3,5x,'o ',i2,',',i3)
      ija = ijtoi (mi,nj)
      ijo = ijtoi (mi+1,nj)
      ijb = ijtoi (mi+1,njp)
      ijc = ijtoi (mi,njp)
c     write(33,9030) lfld(ijc),sfld(mi,njp), lfld(ijb),sfld(mi+1,njp)
c     write(33,9030) lfld(ija),sfld(mi,nj),  lfld(ijo),sfld(mi+1,nj)
c     write(lbox,9030) lfld(ijc),sfld(mi,njp), lfld(ijb),sfld(mi+1,njp)
c     write(lbox,9030) lfld(ija),sfld(mi,nj),  lfld(ijo),sfld(mi+1,nj)
c9030 format (1x,l1,2x,g11.5,5x,l1,2x,g11.5)
      goto 300
c
 120  continue
c
c              initialize starting values
      first = .true.
      last  = .false.
      nval  = 1
      zf    = zblk(kf,lf)
      za    = zblk(ka,la)
c                   find first point of contour
      t = 0.0
      if (zf .ne. za) t = (zf -hc)/(zf -za)
      xus(1) = mi +rint*((kf -1) +t*kv)
      yus(1) = nj +sint*((lf -1) +t*lv)
ccc   if (.not. open) then
c                   save starting location
ccc     mif  = mi
ccc     njf  = nj
ccc     xusf = xus(1)
ccc     yusf = yus(1)
ccc   endif
c
 200  continue
      if (.not. backwd) then
c                   initialize values for forward trace
        kb = kf +lv
        lb = lf -kv
        zb = zblk(kb,lb)
        if (zb .lt. hc) then
c                      turn right
          za  =  zb
          klt =  kv
          kv  =  lv
          lv  = -klt
c
        else
          kc = kf +kv +lv
          lc = lf +lv -kv
          zc = zblk(kc,lc)
          if (zc .lt. hc) then
c                        go straight ahead
            zf = zb
            za = zc
            kf = kf +lv
            lf = lf -kv
          else
c                        turn left
            zf  =  zc
            kf  =  kc
            lf  =  lc
            klt =  lv
            lv  =  kv
            kv  = -klt
          endif
        endif
c
      else
c                   initialize values for backward trace
        kb = kf -lv
        lb = lf +kv
        zb = zblk(kb,lb)
        if (zb .lt. hc) then
c                      turn left
          za  =  zb
          klt =  kv
          kv  = -lv
          lv  = klt
c
        else
          kc = kf +kv -lv
          lc = lf +kv +lv
          zc = zblk(kc,lc)
          if (zc .lt. hc) then
c                        go straight
             zf = zb
             za = zc
             kf = kf -lv
             lf = lf +kv
c
          else
c                        turn right
            zf  =  zc
            kf  =  kc
            lf  =  lc
            klt =  lv
            lv  = -kv
            kv  =  klt
          endif
        endif
      endif
c
c             interpolate for next location of contour
      t = 0.0
      if (zf .ne. za)  t = (zf -hc)/(zf -za)
      nval = nval +1
      if (nval .gt. ncnt) then
c       write (lbox,*) ' isotrc, aborting - too many one block points'
        nc1 = 0
        nc2 = 0
        goto 300
c
      endif
      xus(nval) = mi +rint*((kf -1) +t*kv)
      yus(nval) = nj +sint*((lf -1) +t*lv)
c
c              check to see if edge of zoomed block has been reached
c
      if (lv .eq. 0) then
        if (lf .gt. 1 .and. lf .lt. lzlt) goto 200
c
      else
        if (kf .gt. 1 .and. kf .lt. kzlt) goto 200
c
      endif
 210  continue
c
c                   determine if contour is finished and
c                   if contouring continuing,
c                   location of next block to be zoomed.
c
      if (.not.backwd) then
c
c                   setup forward contouring values
c
        if (kv .eq. -1) then
          njp = nj +1
          if (njp .ge. maxj) then
            last = .true.
          else
            nj = njp
            lf = 1
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi+1,nj)) = .false.
c
c                   determine if closed contour is finished
c
ccc         if (.not.open .and. mi.eq.mif .and. nj.eq.njf) then
ccc           last      = .true.
ccc           nval      = nval +1
ccc           xus(nval) = xusf
ccc           yus(nval) = yusf
ccc         endif
          endif
        elseif (lv .eq. -1) then
          mim = mi -1
          if (mim .lt. mini) then
            last = .true.
          else
            mi = mim
            kf = kzlt
          endif
        elseif (kv .eq. 1) then
          njm = nj -1
          if (njm .lt. minj) then
            last = .true.
          else
            lf = lzlt
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi,nj)) = .false.
            nj = njm
          endif
        elseif (lv .eq. 1) then
          mip = mi +1
          if (mip .ge. maxi) then
            last = .true.
          else
            mi = mip
            kf = 1
          endif
        endif
c
      else
c                   setup backward contouring values
        if (kv .eq. 1) then
          njp = nj +1
          if (njp .ge. maxj) then
            last = .true.
          else
            nj = njp
            lf = 1
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi,nj)) = .false.
c
c                   determine if closed contour is finished
c
ccc         if (.not.open .and. mi.eq.mif .and. nj.eq.njf) then
ccc           last      = .true.
ccc           nval      = nval +1
ccc           xus(nval) = xusf
ccc           yus(nval) = yusf
ccc         endif
          endif
        elseif (lv .eq. 1) then
          mim = mi -1
          if (mim .lt. mini) then
            last = .true.
          else
            mi = mim
            kf = kzlt
          endif
        elseif (kv .eq. -1) then
          njm = nj -1
          if (njm .lt. minj) then
            last = .true.
          else
            nj = njm
            lf = lzlt
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi+1,nj+1)) = .false.
          endif
        elseif (lv .eq. -1) then
          mip = mi +1
          if (mip .ge. maxi) then
            last = .true.
          else
            mi = mip
            kf = 1
          endif
        endif
      endif
c
c                   output contour points for one block
c
c     write (lbox,*) 'isotrc, nval ',nval,' ncnt ',ncnt,' last ',last
      if (first) then
        nn     = 0
        nxylmt = 0
      endif
      do n=1, nval
        if (xus(n) .ge. xs .and. xus(n) .le. xl .and. yus(n) .ge. ys
     &       .and. yus(n).le.yl) then
          if (iter .eq. 1) then
            if (nn .eq. 0) then
              nn     = 1
              xx1(1) = xus(n)
              yy1(1) = yus(n)
            else
              if (xus(n) .ne. xx1(nn) .and. yus(n) .ne. yy1(nn)) then
                nn = nn +1
                if (nn .le. npts) then
                  xx1(nn) = xus(n)
                  yy1(nn) = yus(n)
                else
                  nxylmt = -1
                endif
              endif
            endif
          else
            if (nn .eq. 0) then
              nn     = 1
              xx2(1) = xus(n)
              yy2(1) = yus(n)
            else
              if (xus(n).ne.xx2(nn) .and. yus(n).ne.yy2(nn)) then
                nn = nn +1
                if (nn .le. npts) then
                  xx2(nn) = xus(n)
                  yy2(nn) = yus(n)
                else
                  nxylmt = -1
                endif
              endif
            endif
          endif
        endif
      enddo
      first = .false.
      nval  = 0
      if (nxylmt .lt. 0) then
c       write (33,*) ' $$$$ isotrc, too many total pts ',nn
        last = .true.
      endif
  240 continue
      if (last) then
        if (iter .eq. 1) then
          nxy1 = min0 (nn,npts)
          nc1  = nxy1
          rh1  = rh
          kkk  = kkk +1
        else
          nxy2 = min0 (nn,npts)
          nc2  = nxy2
          rh2  = rh
          kkk  = kkk +1
          if (nxy1 .gt. 1 .and. nxy2 .gt. 1) then
            call calint
          else
c           write (33,*) ' isotrc, no calint for ',rh1,'  ',rh2
            nc2 = 0
          endif
        endif
      else
c                   zoom grid into zblk
        call isovzm (sfld,zblk,ierr)
c                   jump to continue isogon
        if (ierr .eq. 0) goto 200
c
c       write (33,*) ' $$$ isotrc, mi ',mi,' nj ',nj,
c    &               ' driven out of bounds'
        last = .true.
        goto 240
c
      endif
  300 continue
c
      end
      subroutine isovzm (bfld,zblk,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:  @(#)isovzm.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isovzm
c
c  DESCRIPTION:  zoom grid square into block of interpoalted values,
c                no interpolation on edges (it is not required)
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call isovzm (bfld,zblk,ierr)
c
c  PARAMETERS:
c     NAME         TYPE      USAGE             DESCRIPTION
c   --------      ------     -----    ----------------------------------
c     bfld         real        in     base field
c     zblk         real       out     zoomed block of data
c     ierr          int       out     error flag, 0 no error
c
c  CALLED BY:  isotrc.f
c
c  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
c                              ARE DEFINED IN THE CODE WITHIN INCLUDE
c                              FILES.  THIS MODULE USES THE FOLLOWING
c                              COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c     zoomv       kzlt      int     in    first  dim of zoomed block
c                 lzlt      int     in    second dim of zoomed block
c                   mi      int     in    starting minimum first dim of
c                                         contouring block
c                   mz      int     in    first dimension of sfld
c                   nj      int     in    starting minimum second dim of
c                                         contouring block
c                   nz      int     in    second dimension of sfld
c                 rint     real     in    first dim resolution of zoomed
c                                         block
c                 sint     real     in    second dim resolution of
c                                         zoomed block
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     request interpolation    output diagnostic and return error flag
c     in edges of base field
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c              a     real       interpoation factors
c             ar     real       interpoation factor
c              b     real       interpolation factors
c             br     real       interpolation factor
c              c     real       interpolation factors
c             cr     real       interpolation factor
c            ecv     real       first set of interpolated values
c          ec3m1     real       interpolation factor
c          ec3m2     real       interpolation factor
c          ec4m2     real       interpolation factor
c           efld     real       environment base field values
c          er3m1     real       interpolation factor
c          er3m2     real       interpolation factor
c          er4m2     real       interpolation factor
c            im       int       starting first  dim grid point
c            jn       int       starting second dim grid point
c             r      real       first  dimension index of block
c             s      real       second dimension index of block
c
c  METHOD:  Apply Ayres' central difference formula in two dimensions
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------     ----------------------------------------------
c          zoomv.inc      common block
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (26 MAR 1997) -- Hamilton, H.
c    Initial installation, with OTCM
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      include 'zoomv.inc'
c
c         formal parameters
      integer ierr
      real bfld(mz,nz), zblk(kzlt,lzlt)
c
c         local variables
      integer im, jn, k, n, m, i, l
      real ar, br, cr, r, s
      real er3m1, er3m2, er4m2, ec3m1, ec3m2, ec4m2
      real efld(16), a(4), b(4), c(4), ecv(4)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      im = mi
      jn = nj
c
c                  check that lower left hand point is an interior point
c
      if (im.ge.2 .and. im.lt.mz-1 .and. jn.ge.2 .and. jn.lt.nz-1) then
c
c                   load 4-by-4 array, efld, for interpolation
c
        k = 0
        do n=jn-1, jn+2, 1
          do m=im-1, im+2, 1
            k = k +1
            efld(k) = bfld(m,n)
          enddo
        enddo
c
c                   load four corners of zblk
c
          zblk(1,1)       = efld(6)
          zblk(kzlt,1)    = efld(7)
          zblk(1,lzlt)    = efld(10)
          zblk(kzlt,lzlt) = efld(11)
c
          if (kzlt .gt. 2 .or. lzlt .gt. 2) then
c
c                   perform interpolation of efld block to load zblk
c
            do i=1, 4
              er3m1 = efld(8+i) -efld(i)
              er3m2 = efld(8+i) -efld(4+i)
              er4m2 = 0.5*(efld(12+i) -efld(4+i))
              a(i)  = 0.5*er3m1
              b(i)  = 3.0*er3m2 -er3m1 -er4m2
              c(i)  = a(i) +er4m2 -er3m2 -er3m2
            enddo
c
            s = -sint
            do l=1, lzlt
              s = s +sint
              do i=1, 4
                ecv(i) = efld(4+i) +s*(a(i) +s*(b(i) +s*c(i)))
              enddo
c
              ec3m1 = ecv(3) -ecv(1)
              ec3m2 = ecv(3) -ecv(2)
              ec4m2 = 0.5*(ecv(4) - ecv(2))
              ar    = 0.5*ec3m1
              br    = 3.0*ec3m2 -ec3m1 -ec4m2
              cr    = ar +ec4m2 -ec3m2 -ec3m2
              r     = -rint
              do k=1, kzlt
                r = r +rint
c
c                   if (true) fill block with interpolated values
c
                if ((l.ne.1 .and. l.ne.lzlt) .or. (k.ne.1 .and.
     &             k.ne.kzlt))  zblk(k,l) = ecv(2) +r*(ar +r*(br +r*cr))
              enddo
            enddo
          endif
          ierr = 0
      else
c
c                   no edge interpolation allowed in this version,
c                   so set ierr to error value.
c
         ierr = -1
         write (*,*) '$$$$$ warning:  error return in isovzm  $$$$$'
      endif
c
      end
      subroutine merlod4 (gfld,rfld,ixmg,jymg,ierr)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)merlod8.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  merlod4
c
c  DESCRIPTION:  load regional Mercator field based upon global field
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_ng.inc'
      INCLUDE 'par_mer.inc'
c
      integer  ixmg, jymg, ierr
      real     gfld(ixng,jyng)
      real     rfld(ixmg,jymg)
c
c         local varaiables
      integer  i, j
      real     cycit1
c
c                   grid parameters
c
      INCLUDE 'ngfld_p_com.inc'
c
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (ixm.eq.ixmg .and. jym.eq.jymg) then
        do j=1, jym
          do i=1, ixm
            rfld(i,j) = cycit1 (bing(i),bjng(j),gfld,ixng,jyng)
          enddo
        enddo
        ierr = 0
      else
        ierr = -1
      endif
c
      end
      subroutine merlod8 (gfld,rfld,ixmg,jymg,ierr)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)merlod8.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  merlod8
c
c  DESCRIPTION:  load regional Mercator field based upon global field
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_ng.inc'
      INCLUDE 'par_mer.inc'
c
      integer           ixmg, jymg, ierr
      real              gfld(ixng,jyng)
      double precision  rfld(ixmg,jymg)
c
c         local varaiables
      integer  i, j
      real     cycit1
c
c                   grid parameters
c
      INCLUDE 'ngfld_p_com.inc'
c
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (ixm.eq.ixmg .and. jym.eq.jymg) then
        do j=1, jym
          do i=1, ixm
            rfld(i,j) = cycit1 (bing(i),bjng(j),gfld,ixng,jyng)
          enddo
        enddo
        ierr = 0
      else
        ierr = -1
      endif
c
      end
      subroutine mgrdvals
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)mgrdvals.f90	1.2  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  mgrdvals
c
c  DESCRIPTION:  calculate Mercator grid values
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (26 MAR 1997)  Hamilton, H.
c    install changes to go from 2-deg to 1-degree Mercater grid
c
c..............................END PROLOGUE.............................
c
c     implicit none
c
      INCLUDE 'par_mer.inc'
c
c         local variables
      integer           i, j
      integer           ioff(2), joff(2)
      double precision  rctlat, re_tlat, grlat, ydis
c
c                   grid parameters
c
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'ngfld_p_com.inc'
      INCLUDE 'stat1_com.inc'
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'stat4_com.inc'
c
      data ioff/34, 30/
      data joff/21, 26/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   calculate static1 values with accuracy of computer
c
      pi      = acos (-1.0d0)
      rad2deg = 180.0d0/pi
      deg2rad = pi/180.0d0
      del     = deg2m*mg_deg
      rctlat  = cos (22.5d0*deg2rad)
c                   re_tlat = (360.0*102677.2)/(2.0*pi) = re at 22.5
      re_tlat = 180.0*deg2m/pi
c
c                   compute distance from cyclone latitude to equator
c
      y2eq = re_tlat*log ((1.0d0 +sin (rlat*deg2rad))
     &       /cos(rlat*deg2rad))
c
c                   set grid location of cyclone
c
      icyc = ioff(1)
      if (rlat .gt. 0.0) then
        if (rlat.gt.25.0 .and. head.le.90.0) icyc = ioff(2)
        jcyc = joff(1)
      else
        if (rlat.lt.-25.0 .and. (head.ge.90.0 .and. head.le.180.0))
     &      icyc = ioff(2)
        jcyc = joff(2)
      endif
      rjcyc = jcyc
c     rcycj = rjcyc
      ricyc = icyc
c     write(20,*) 'Cyclone TAU 0, Lat ',rlat,'  Lon ',rlon
c     write(20,*) 'Locate cyclone in grid at i=',ricyc,'  j=',rjcyc
c     write(20,*) 'Cyclone max wind speed ',iwndmx,' model max ',mwndmx
c
      re_tlat_i = 1.0/re_tlat
c     write (20,9010)
c9010 format (' index',3x,'global-ind',2x,'lat',5x,'em',10x,'f')
      do j=jym, 1, -1
        ydis     = (y2eq +(j -jcyc)*del)*re_tlat_i
        grlat    = 2.0d0*atan (exp (ydis)) - 0.5d0*pi
        em(j)    = rctlat/cos (grlat)
        emi(j)   = 1.0d0/em(j)
        f(j)     = twomega*sin (grlat)
        gdlat(j) = rad2deg*grlat
c       rjng(j)  = 91.0d0 +gdlat(j) for 360 by 181 1.0 deg lat/lon grid
c                                   for 144 by 73  2.5 deg lat/lon grid
	rjng(j)  = 1.0 +(gdlat(j) +90.0)/2.5
        bjng(j)  = rjng(j)
c       write (20,9020) j, rjng(j), gdlat(j), em(j), f(j)
c9020   format (i5,3x,f7.3,3x,f6.2,3x,f7.5,3x,e15.9)
      enddo
      gdlon(1) = rlon -real (icyc -1)
c     ring(1)  = 1.0 +gdlon(1)      for 360 by 181 1.0 deg lat/lon grid
c                                   for 144 by  73 2.5 deg lat/lon grid
      ring(1)  = 1.0 +gdlon(1)/2.5
      bing(1)  = ring(1)
      do i=2, ixm
        gdlon(i) = gdlon(i-1) +real (mg_deg)
        ring(i)  = 1.0 +gdlon(i)/2.5
        bing(i)  = ring(i)
      enddo
c     write (20,9030) mg_deg, gdlon(1), gdlon(ixm)
c9030 format (1x,'longitude - left to right at ',i1,' degree interval',
c    &        /,3x,f10.3,5x,f10.3)
      twodel = 2.0d0*del
c
      end
      subroutine omega (uu,vv,ww)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  omega
c
c  DESCRIPTION:  set/compute omega fields
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call omega (uu,vv,ww)
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c       uu              real         input    matric of u-wind
c       vv              real         input    matrix of v-wind
c       ww              real         output   matric of vertical wind
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      double precision  uu(ixm,jym,3), vv(ixm,jym,3), ww(ixm,jym,4)
c
c         local variables
      integer           i, j, k
      double precision  delp, ratio
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c
c                   Note:    k  (  4,   3,   2,   1   )
c                         wind  (      250, 550, 850  )
c                        omega  ( 100, 400, 700, 1000 )
c
      delp  = 300.0d0
      ratio = delp/twodel
      do j=1, jym
        do i=1, ixm
          ww(i,j,4) = 0.0d0
        enddo
      enddo
c
      do k=3, 1, -1
        do j=1, jym
          do i=1, ixm
            ww(i,j,k) = ww(i,j,k+1)
          enddo
        enddo
        call calomega (uu(1,1,k),vv(1,1,k),ratio,ww(1,1,k))
      enddo
c
      end
      block data one
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)one.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  block data one
c
c  DESCRIPTION:  Fortran block data routine
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat2_com.inc'
c
      data pi/3.1415926536/, rad2deg/0.017453293/, deg2rad/53.29252/
      data twomega/1.4584E-4/
      data pilo/4*0.0/, piup/4*0.0/, pic/4*0.0/
      data dp/150.0, 300.0, 300.0, 150.0/

      end
      subroutine pois2 (m,n,a,b,c,y,w,lw)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)pois2.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  pois2
c
c  DESCRIPTION:  solve elliptic partial differential equation
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
c
c     THIS SUBROUTINE SOLVES THE LINEAR SYSTEM OF EQUATIONS
c
c        A(I)*X(I-1,J) + B(I)*X(I,J) + C(I)*X(I+1,J) +
c             X(I,J-1) - 2*X(I,J) + X(I,J+1)  =  Y(I,J) ,
c
c                  FOR I = 1,2, . . . , M , AND
c                      J = 1,2, . . . , N ,
c
c     WHERE
c
c        X(I,0) = X(I,N+1) = 0  FOR ALL I, AND
c        X(0,J) = X(M+1,J) = 0  FOR ALL J.
c
c * * * * * * * * * * * *   RESTRICTIONS   * * * * * * * * * * * * * *
c
c     M AND N MUST BE GREATER THAN 1.
c     W MUST BE DIMENSIONED AT LEAST 2*N + 4*M + M*(ALOG(N) +1).
c
c * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
c
      implicit none
c
c         formal parameters
      integer           m, n, lw
      double precision  y(m,n), a(m), b(m), c(m), w(lw)
c
c         local variables
      integer  i, i1, i2, i3, i4, i5, kw
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      w  = 0.0d0
      i1 = 2*n +1
      i2 = i1 +m
      i3 = i2 +m
      i4 = i3 +m
      i5 = i4 +m
      do i=1, m
        w(i4+i-1) = b(i) -2.0d0
      enddo
      kw = lw -i5 +1
      call posgn3 (m,n,a,w(i4),c,y,w(1),w(i1),w(i2),w(i3),w(i5),kw)
c
      end
      subroutine posgn3 (m,n,ba,bb,bc,q,tcos,b,d,w,p,lp)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION  @(#)posgn3.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  posgn3
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      implicit none
c
c         formal parameters
      integer           m, n, lp
      double precision  q(m,n), ba(m), bb(m), bc(m), b(m), d(m), w(m)
      double precision  tcos(2*n), p(lp)
c
c         local variables
      integer  n0
      integer  jsh, idegbr, idegcr, ip, nun, jsp, jst, irreg, nodd
      integer  i,j,l
      integer  ideg, jdeg, kk, jstsav, n2
      double precision  pi, t
c
      data n0/0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      PI     = acos (-1.0d0)
      JSH    = 99999
      IDEGBR = 0
      IDEGCR = 0
      IP     = 0
      N2     = N +N
      NUN    = N
      JSP    = N
      JST    = 1
      JSTSAV = 1
c                   set irreg to 1, it will retain this value if no
c                   irregularities occurr, otherwise it will be set to 2
      IRREG  = 1
      do
        L = 2*JST
c                     NODD is 1 WHEN NUN IS ODD, and 0 when NUN is even.
        NODD = mod (nun,2)
        IF (NODD .eq. 0) then
          JSP = JSP -L
        else
          JSP = JSP -JST
          IF (IRREG .ne. 1) JSP = JSP -L
        endif
c
c                     REGULAR REDUCTION
c
        DO I=1, JST
          TCOS(I) = 2.0d0*COS ((2*I -1)*PI/L)
        enddo
        IF (L .le. JSP) then
          DO J=L, JSP, L
            IF (JST .eq. 1)  then
              DO I=1, M
                B(I)   = 2.0d0*Q(I,J)
                Q(I,J) = Q(I,J-1) +Q(I,J+1)
              enddo
              CALL TRIX (JST,n0,M,N,BA,BB,BC,B,TCOS,D,W)
              DO I=1, M
                Q(I,J) = Q(I,J) +B(I)
              enddo
            else
              DO I=1, M
                T = Q(I,J) -Q(I,J-JSH) -Q(I,J+JSH) +Q(I,J-JST)
     &             +Q(I,J+JST)
                B(I)   = T +Q(I,J) -Q(I,J-3*JSH) -Q(I,J+3*JSH)
                Q(I,J) = T
              enddo
              CALL TRIX (JST,n0,M,N,BA,BB,BC,B,TCOS,D,W)
              DO I=1, M
                Q(I,J) = Q(I,J) +B(I)
              enddo
            endif
          enddo
        endif
c
c                     REDUCTION FOR LAST UNKNOWN
c
        IF (NODD .ne. 0) then
          IF (IRREG .ne. 1) then
            JSP = JSP +L
            J   = JSP
            DO I=1, M
              B(I) = 0.5*(Q(I,J-JSH) +Q(I,J-3*JSH) -Q(I,J-JST))
     &              +P(IP*M+I) -Q(I,J)
            enddo
            CALL TRIX (JST,n0,M,N,BA,BB,BC,B,TCOS,D,W)
            IP = IP +1
            if (ip*2*m .gt. lp) then
              write (*,*) 'posgn3, array too small, need=',ip*2*m,
     &                    ' have ',lp
              call exit (77)
c
            endif
            DO I=1, M
              P(IP*M+I) = 0.5d0*(Q(I,J-JSH) +Q(I,J+JSH) -Q(I,J)) +B(I)
              B(I)      = Q(I,J+JST) -P(IP*M+I)
            enddo
            CALL COSGEN (JSTSAV,IDEGBR,IDEGCR,PI,TCOS,n2)
            KK = JSTSAV*(IDEGBR +IDEGCR)
            DO I=1, JST
              TCOS(KK+I) = 2.0d0*COS ((2*I -1)*PI/L)
            enddo
            CALL TRIX (IDEGBR*JSTSAV,IDEGCR*JSTSAV+JST,M,N,BA,BB,BC,B,
     &                 TCOS,D,W)
            DO I=1, M
              Q(I,J) = Q(I,J-JST) +B(I) -P(IP*M+I)
            enddo
            IDEGCR = IDEGBR
            IDEGBR = IDEGBR +2*JST/JSTSAV
          endif
        else
          JSP = JSP +L
          IP  = IP +1
          IF (IRREG .ne. 2) then
            IRREG  = 2
            JSTSAV = JST
            IDEG   = JST
            IDEGBR = 2
            IF (JST .eq. 1) then
              DO I=1, M
                B(I) = Q(I,J)
              enddo
            else
              DO I=1, M
                B(I) =  Q(I,J) +0.5d0*(Q(I,J-JST) -Q(I,J-JSH)
     &                 -Q(I,J-3*JSH))
                P(M*(IP-1)+I) = 0.5d0*(Q(I,J-JSH) +Q(I,J+JSH) -Q(I,J))
              enddo
            endif
          else
            CALL COSGEN (JSTSAV,IDEGBR,IDEGCR,PI,TCOS,n2)
            IDEG   = IDEGBR*JSTSAV
            IDEGBR = IDEGBR +JST/JSTSAV
            DO I=1, M
              B(I) = Q(I,J) +0.5d0*(Q(I,J-JST) -Q(I,J-JSH)
     &              -Q(I,J-3*JSH))
            enddo
          endif
          CALL TRIX (IDEG,IDEGCR*JSTSAV,M,N,BA,BB,BC,B,TCOS,D,W)
          DO I=1, M
            P(M*IP+I) = P(M*(IP-1)+I) -B(I)
            Q(I,J)    = Q(I,J-JST) -P(M*IP+I)
          enddo
        endif
        JSH = JST
        JST = 2*JST
        nun = nun/2
        if (nun .lt. 2) exit
c
      enddo
c
      J = JSP
      DO I=1, M
        B(I) = Q(I,J)
      enddo
      IF (IRREG .eq. 1) then
        DO I=1, JST
          TCOS(I) = 2.0d0*COS ((2*I -1)*PI/(2*JST))
        enddo
        IDEG = JST
      else
        IDEGBR = IDEGCR +JST/JSTSAV
        CALL COSGEN (JSTSAV,IDEGBR,IDEGCR,PI,TCOS,n2)
        IDEG = JSTSAV*IDEGBR
      endif
      CALL TRIX (IDEG,IDEGCR*JSTSAV,M,N,BA,BB,BC,B,TCOS,D,W)
      IF (IRREG .eq. 1) then
        DO I=1, M
          Q(I,J) = 0.5d0*(Q(I,J-JSH) +Q(I,J+JSH) -Q(I,J)) -B(I)
        enddo
      else
        DO I=1,M
          Q(I,J) = P(IP*M+I) -B(I)
        enddo
        IP = IP -1
      endif
      do
        NUN = 2*NUN
        IF (NUN .gt. N) exit
c
        JST = JST/2
        JSH = JST/2
        DO J=JST, N, L
          IF (J .le. JST) then
            DO I=1, M
              B(I)= Q(I,J) -Q(I,J+JST)
            enddo
          else
            IF (J +JST .gt. N) then
              DO I=1, M
                B(I)= Q(I,J) -Q(I,J-JST)
              enddo
              IF (JST .lt. JSTSAV) then
                IRREG = 1
              else
                IF (J+L .gt. N)  IDEGCR = IDEGCR -JST/JSTSAV
                IDEGBR = JST/JSTSAV +IDEGCR
                CALL COSGEN (JSTSAV,IDEGBR,IDEGCR,PI,TCOS,n2)
                IDEG = IDEGBR*JSTSAV
                JDEG = IDEGCR*JSTSAV
                goto 721
c
              endif
            else
              DO I=1, M
                B(I) = Q(I,J) -Q(I,J-JST) -Q(I,J+JST)
              enddo
            endif
          endif
          DO I=1, JST
            TCOS(I) = 2.0d0*COS ((2*I -1)*PI/L)
          enddo
          IDEG = JST
          JDEG = 0
 721     CONTINUE
          CALL TRIX (IDEG,JDEG,M,N,BA,BB,BC,B,TCOS,D,W)
          IF (JST .le. 1)  then
            DO I=1, M
              Q(I,J) = -B(I)
            enddo
          else
            IF (J+JST .le. N .OR. irreg .eq. 1) then
              DO I=1, M
                Q(I,J) = 0.5d0*(Q(I,J-JSH) +Q(I,J+JSH) -Q(I,J)) -B(I)
              enddo
            else
              DO I=1, M
                Q(I,J) = P(IP*M+I) -B(I)
              enddo
            endif
          endif
        enddo
        IP = IP -1
        L  = L/2
      enddo
c
      end
      subroutine prep1000 (vortmx)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  prep1000
c
c  DESCRIPTION:  Solve balance equation to initialize 1000 hPa height field
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES: 1) NCAR Technical Note - NCAR-TN/IA-109, July 1975
c                 Efficient FORTRAN Subprograms for the Solution of
c                 Elliptic Partial Differential Equations
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call prep1000 (vortmx)
c
c  PARAMETERS:  none
c     Name        Type      Usage            Description
c  ---------    --------   -------    ----------------------------
c   vortmx       dble        in       maximum model vorticity
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c    First dimension of fields may be any reasonable number.
c    Second dimension of vort field MUST be (2**p * 3**q * 5**r) -1,
c    second dimension of fields are second dimension of vort +2.
c    Where: p, q and r may be any non-negative integers;
c    when Dirichlet boundary conditions are selected for the solution
c    of the resulting elliptic partial differential equation.
c    These boundary conditions are used in these routines.
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c        Name           Description
c      ---------     --------------------------------------------------------
c      setbstrmf     set the boundary stream function values
c      calvort       insert tropical cyclone
c      calstrmf      calculate the internal stream function values
c      calwndc       calculate the non-divergent wind components
c      calph1        solve balance equation to obtain phi at 1000
c
c      uvrng3a       calculate max, avg and min field values of
c                    internal grid points - diagnostic routine.
c      ptrng4a       calculate max, avg and min field values of
c                    over internal grid points - diagnostic routine.
c      gzrng4a       calculate max, avg and min field values of
c                    internal grid points - diagnostic routine.
c
c  LOCAL VARIABLES:
c     Name      Type                 Description
c    ------     ----       -----------------------------------------
c    wtone      real       weighting applied to vortmx in S/R calvort 
c
c  METHOD:  The descriptions listed above for the routines called explains the
c           methods employed and are in the proper sequence.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c         formal parameters
      double precision  vortmx
c
c         local variables
      real    wtone
      double precision  strmf(ixm,jym), vort(ixm-2,jym-2)
c
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat2_com.inc'
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr1_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'works_com.inc'
c
      equivalence (wrk81(1,1),strmf(1,1)), (wrk82(1,1),vort(1,1))
c
      data wtone/1.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c     **********  calculate non-divergent winds for 1000
c
c                   calculate estimate of streamfunction on boundary
c
      call setbstrm (u285,v285,strmf)
c
c                   calculate vorticity over interior of grid of base winds
c
      call calvort (u285,v285,icyc,jcyc,vortmx,wtone,vort)
c
c                   calculate interior streamfunction values
c
      call calstrmf (vort,ixm,jym,del,em,strmf,wrk83)
c
c                   calculate non-divergent wind components
c
      call calwndc (strmf,u285,v285)
c
c     **********  calculate gz 1000 based upon balance eq.
c
      call calph1 (u285,v285,z110,wrk81,wrk82,wrk83,wrk84,wrk85)
c
      end
      subroutine ptgzchk (i,j,kchk,fld,nadj)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)ptgzchk.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  ptgzchk
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c          formal parameters
      integer           i, j, kchk, nadj
      double precision  fld(ixm,jym)
c
c          local variables
      integer           kint
      double precision  vl, vlavg, vlest, vlint, gzptint8
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      kint = 0
      if (i .ge.4 .and. i .le. ixm-3) then
        if (j .ge. 4 .and. j .le. jym-3) kint = -1
      endif
      vl = fld(i,j)
      call avgval (i,j,fld,vlavg,vlest)
      if (kint .ne. 0) then
        vlint = gzptint8 (i,j,fld,ixm,jym)
      else
        vlint = vlest
      endif
c
c                   ESTABLISH VALUE
c
      if (kchk .gt. 0) then
        fld(i,j) = min (vl,vlest,vlint)
      elseif (kchk .lt. 0) then
        fld(i,j) = max (vl,vlest,vlint)
      else
        write (*,*) 'WRONG kchk is ',kchk
      endif
      if (vl .ne. fld(i,j)) nadj = nadj +1
c
      end
      subroutine ptgzrng1 (pta,ptb,gza,gzb,ix,jy)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  ptgzrng1
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c..............................END PROLOGUE.............................
c
c
      integer           ix, jy
      double precision  pta(ix,jy), ptb(ix,jy), gza(ix,jy), gzb(ix,jy)
c
      double precision  ptxa, ptxb, gzxa, gzxb, ptma, ptmb, gzma, gzmb
c
      INCLUDE 'minmax_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ptxa = -999999.9d0
      ptxb = -999999.9d0
      gzxa = -999999.9d0
      gzxb = -999999.9d0
      ptma = -gzxb
      ptmb = -gzxb
      gzma = -gzxb
      gzmb = -gzxb
      do j=1, jy
        do i=1, ix
          ptxa = max (ptxa,pta(i,j))
          ptma = min (ptma,pta(i,j))
          ptxb = max (ptxb,ptb(i,j))
          ptmb = min (ptmb,ptb(i,j))
          gzxa = max (gzxa,gza(i,j))
          gzma = min (gzma,gza(i,j))
          gzxb = max (gzxb,gzb(i,j))
          gzmb = min (gzmb,gzb(i,j))
        enddo
      enddo
      pt1mn = ptma
      pt1mx = ptxa
      pt2mn = ptmb
      pt2mx = ptxb
      gz1mn = gzma
      gz1mx = gzxa
      gz2mn = gzmb
      gz2mx = gzxb
c
      end
      subroutine ptrng4a (pt,ix,jy,kn,kkk)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)ptrng4a.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  ptrng4a
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      integer           kn, kkk
      double precision  pt(ix,jy,4)
c
      integer           kk
      double precision  sum, ptx(4), ptn(4), pta(4)
c
c . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do k=1, 4
        ptx(k) = -999999.9d0
        ptn(k) = -ptx(k)
        sum    = 0.0d0
        kk     = 0
        do j=1, jy
          do i=1, ix
            ptx(k) = max (ptx(k),pt(i,j,k))
            ptn(k) = min (ptn(k),pt(i,j,k))
            sum    = sum +pt(i,j,k)
            kk     = kk +1
          enddo
        enddo
        pta(k) = sum/kk
      enddo
c
      write(20,900) kkk,ptx(1),ptx(2),ptx(3),ptx(4)
  900 format ('Step ',i4,' A-PT mx 1-4 ',4f12.3)
c     write(*,910) kkk,pta(1),pta(2),pta(3),pta(4)
      write(20,910) kkk,pta(1),pta(2),pta(3),pta(4)
  910 format ('Step ',i4,' A-PT av 1-4 ',4f12.3)
c     write(*,920) kkk,ptn(1),ptn(2),ptn(3),ptn(4)
      write(20,920) kkk,ptn(1),ptn(2),ptn(3),ptn(4)
  920 format ('Step ',i4,' A-PT mn 1-4 ',4f12.3)
c
      end
      subroutine ptstab (i,j,lev,pot,nadj,nfor)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)ptstab.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  ptstab
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     formal parameters
      integer           i, j, lev, nadj, nfor
      double precision  pot(ixm,jym,4)
c
c     local variables
      integer           k, km, kint, kode
      double precision  ptlo, ploavg, ploest, diflo, difmx, ptst, pthi
      double precision  phiavg, phiest, difhi, diff, gzptint8
c
      data difmx/0.2d0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      k    = lev
      km   = lev -1
      kint = 0
      if (i .ge.4 .and. i .le. ixm-3) then
        if (j .ge. 4 .and. j .le. jym-3) kint = -1
      endif
c
c                   CORRECT STATIC STABILITY
c
      kode = 0
      ptlo = pot(i,j,km)
      call avgval (i,j,pot(1,1,km),ploavg,ploest)
      pthi = pot(i,j,k)
      call avgval (i,j,pot(1,1,k),phiavg,phiest)
      difhi = abs (phiavg -pthi)
      diflo = abs (ploavg -ptlo)
      if (difhi .le. diflo) then
c
c               try to correct ptlo first
c
        if (ploavg .le. pthi) then
          ptlo = ploavg
          kode = -1
        elseif (ploest .le. pthi) then
          ptlo = ploest
          kode = -1
        else
          if (kint .ne. 0) then
            ptst = gzptint8 (i,j,pot(1,1,km),ixm,jym)
          else
            ptst = ploavg
          endif
          ptlo = min (ptlo,ploavg,ploest,ptst)
          if (ptlo .le. pthi) then
            kode = -1
          elseif (phiavg .ge. ptlo) then
            pthi = phiavg
            kode = -1
          elseif (phiest .ge. ptlo) then
            pthi = phiest
            kode = -1
          else
            if (kint .ne. 0) then
              ptst = gzptint8 (i,j,pot(1,1,k),ixm,jym)
            else
              ptst = phiavg
            endif
            pthi = max (pthi,phiavg,phiest,ptst)
            if (pthi .ge. ptlo) kode = -1
          endif
        endif
      else
c
c                   try to correct pthi first
c
        if (phiavg .ge. ptlo) then
          pthi = phiavg
          kode = -1
        elseif (phiest .ge. ptlo) then
          pthi = phiest
          kode = -1
        else
          if (kint .ne. 0) then
            ptst = gzptint8 (i,j,pot(1,1,k),ixm,jym)
          else
            ptst = phiavg
          endif
          pthi = max (pthi,phiavg,phiest,ptst)
          if (pthi .ge. ptlo) then
            kode = -1
          elseif (ploavg .le. pthi) then
            ptlo = ploavg
            kode = -1
          elseif (ploest .le. pthi) then
            ptlo = ploest
            kode = -1
          else
            if (kint .ne. 0) then
              ptst = gzptint8 (i,j,pot(1,1,km),ixm,jym)
            else
              ptst = ploavg
            endif
            ptlo = min (ptlo,ploavg,ploest,ptst)
            if (pthi .ge. ptlo) kode = -1
          endif
        endif
      endif
      if (kode .ne. 0) then
        nadj = nadj +1
      else
c
c               force a correction
c
        diff = ptlo -pthi
        if (diff .le. difmx) kode = -1
        ptlo = ptlo -0.5d0*diff
        if (k .gt. 2 .and. ptlo .lt. pot(i,j,k-2)) ptlo = pot(i,j,k-2)
        pthi = ptlo +diff
        if (kode .eq. 0) then
          nfor = nfor +1
        else
          nadj = nadj +1
        endif
      endif
      pot(i,j,km) = ptlo
      pot(i,j,k)  = pthi
c
      end
      subroutine rcaltln (slat,slon,head,dist,elat,elon)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c
c  MODULE NAME:  rcalltln
c
c  DESCRIPTION:  use rhumb line to calculate ending lat,lon given
c                starting lat,lon, heading and distance
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call rcaltln (slat,slon,head,dist,elat,elon)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      slat         real         in     starting latitude
c      slon         real         in     starting longitude
c      head         real         in     heading (deg)
c      dist         real         in     distance (nm)
c      elat         real         out    ending latitude
c      elon         real         out    ending longitude
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                DESCRIPTION
c         ------     ----      ----------------------------------
c           crhd     real      heading converted to radians
c         degrad     real      conversion factor, deg to radians
c           dlat     real      distance in terms of latitude
c           dlon     real      distance in terms of longitude
c         hdgrad     real      half of degrad
c           icrs      int      integer value of heading
c           inil      int      initialization flag
c         raddeg     real      conversion factor, radian to degrees
c         rad045     real      radians in 45 degrees
c           rdst     real      absolute distance, nm
c           rhed     real      local copy of heading
c           tiny     real      small number
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real slat, slon, head, dist, elat, elon
c
c         local variables
      integer icrs, inil
      real crhd, degrad, dlat, dlon, hdgrad, raddeg, rad045, rdst, rhed
      real tiny
c
      save raddeg, degrad, hdgrad, rad045, inil
      data inil/0/
      data tiny/1.0e-3/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .eq. 0) then
        inil   = -1
        degrad = acos (-1.0)/180.0
        hdgrad = 0.5*degrad
        rad045 = 45.0*degrad
        raddeg = 1.0/degrad
      endif
c
      rdst = abs (dist)
      if (rdst .gt. tiny) then
        rhed = head
        if (rhed .lt. 0.0) then
          rhed = rhed +360.0
        elseif (rhed .gt. 360.0) then
          rhed = rhed -360.0
        endif
        if (abs (rhed -360.0) .le. tiny) rhed = 0.0
        icrs = nint (rhed)
        if (abs (head -270.0) .le. tiny .or. abs (head  -90.0) .le.
     &    tiny) then
          dlon = rdst/(60.0*cos (slat*degrad))
c                 longitude is in degrees east, 0.0 to 360.0
          if (icrs .eq. 270) then
            elon = slon -dlon
          else
            elon = slon +dlon
          endif
          elat = slat
        elseif (abs (rhed -360.0) .le. tiny .or. abs (head -180.0) .le.
     &    tiny) then
          dlat = rdst/60.0
          if (icrs .eq. 360) then
            elat = slat +dlat
          else
            elat = slat -dlat
          endif
          elon = slon
        else
          crhd = head*degrad
          elat = slat +(rdst*cos (crhd)/60.0)
          elon = slon +raddeg*(alog (tan (rad045 +hdgrad*elat))
     &          -alog (tan (rad045 +hdgrad*slat)))*tan (crhd)
        endif
      else
        elon = slon
        elat = slat
      endif
      return
c
      end
      double precision function rnlint (dd,rval,nl)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:
C
C  CONFIGURATION IDENTIFICATION: NONE
C
C  MODULE NAME: rnlint
C
C  DESCRIPTION:  INTERPOLATE FIELD, BFLD, WHICH IS CYCLIC IN THE FIRST
C                DIMENSION, BASED UPON AYRES CENTRAL DIFFERENCE FORMULA
C                WHICH PRODUCES VALUES THAT ARE CONTINUOUS IN THE FIRST
C                DERIVATIVE, EXCEPT NEAR LIMITS OF SECOND DIMENSION,
C                WHERE BILINEAR INTERPOLATION IS USED.
C
C  COPYRIGHT:                  (C) 1997 FLENUMMETOCCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  NONE
C
C  REFERENCES: NONE
C
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  BFLD MUST BE 4 BY 4 OR LARGER FIELD AND CYCLIC IN
C                 FIRST DIMENSION
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  UNIX Operating System
C
C  LIBRARIES OF RESIDENCE: /usr/local/fnoc/lib/libfnoc.a
C
C  USAGE:  VAL = CYCIT1 (RML,RNL,BFLD,MGRD,NGRD)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       RML         REAL         IN     FIRST  DIMENSION POINT LOCATION
C       RNL         REAL         IN     SECOND DIMENSION POINT LOCATION
C       BFLD        REAL         IN     FIELD  FOR INTERPOLATION
C       MGRD         INT         IN     FIRST  DIMENSION OF BFLD
C       NGRD         INT         IN     SECOND DIMENSION OF BFLD
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C    NONE
C
C  ERROR CONDITIONS:
C    Since cycit1 is a function, the out-of-bounds error condition re-
C    turns a large negative number (-999999999.00).
C
C  ADDITIONAL COMMENTS:
C           1.  IF SECOND DIMENSION LOCATION IS OUT-OF-BOUNDS,
C               IT'S REPRESENTATIVE IS MADE IN BOUNDS.
C           2.  NO CHECK IS MADE ON IN-BOUNDS FOR FIRST DIMENSION
C               LOCATION.  APPROX. RANGE: (-MGRD < RmL < 2*MGRD)
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C             AA     REAL       INTERPOLATION FACTOR
C             BB     REAL       INTERPOLATION FACTOR
C             BV     REAL       Temporary store of array value
C             CC     REAL       INTERPOLATION FACTOR
C          EV3M1     REAL       INTERPOLATION FACTOR
C          EV3M2     REAL       INTERPOLATION FACTOR
C          EV4M2     REAL       INTERPOLATION FACTOR
C            ECV     REAL       INTERPOLATED ROW OR COLUMN VALUES
C                               FOR FINAL INTERPOLATION
C             M2      INT       TRUNCATED FIRST DIMENSION POINT LOCATION
C             M3      INT       M2 +1
C             N2      INT       TRUNCATED SECOND DIMENSION LOCATION
C             N3      INT       N2 +1
C              R     REAL       FRACTION OF FIRST DIMENSION OF GRID
C                               POINT IS LOCATED FROM M2
C             RN     REAL       REAL REPRESENTATIVE OF RNL
C             RM     REAL       REAL REPRESENTATIVE OF RML
C              S     REAL       FRACTION OF SECOND DIMENSION OF GRID
C                               POINT IS LOCATED FROM N2
C           VFLD     REAL       BLOCK OF VALUES USED FOR INTERPOLATION
C
C  METHOD:  AYRES CENTRAL DIFFERENCE FORMULA USED IN TWO DIMENSIONS
C
C  INCLUDE FILES: NONE
C
C  COMPILER DEPENDENCIES:  NONE
C
C  COMPILE OPTIONS:  NONE
C
C  MAKEFILE:  */cycit1/src/makefile
C
C  RECORD OF CHANGES: NONE
C
C
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
c
      integer nl
      real              dd
      double precision  rval(0:nl)
c
c         local variables
c
      integer  k2
      real     rl, rs
      double precision  v3m1, v3m2, v4m2, aa, bb, cc, rd
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c
      rl = nl
      if (dd .gt. 1.0 .and. dd .lt. (rl -1.0)) then
c
c                   perform Ayres central differences interpolation
c
        k2 = dd
        rs = dd -k2
        rd = rs
        v3m1 = rval(k2+1) -rval(k2-1)
        v3m2 = rval(k2+1) -rval(k2)
        v4m2 = 0.5d0*(rval(k2+2) -rval(2))
        aa   = 0.5d0*v3m1
        bb   = 3.0d0*v3m2 -v3m1 -v4m2
        cc   = aa +v4m2 -v3m2 -v3m2
        rnlint = rval(k2) +rd*(aa +rd*(bb +rd*cc))
      elseif (dd .ge. rl -0.5) then
	rnlint = rval(nl)
      elseif (dd .ge. rl -1.0) then
	rnlint = rval(nl -1)
      elseif (dd .gt. 0.5) then
	rnlint = rval(1)
      else
	rnlint = rval(0)
      endif
c
      end
      subroutine setbstrm (uu,vv,strmf)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)setbstrm.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  setbstrm
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c     integer           ixm, jym
      double precision  uu(ixm,jym), vv(ixm,jym), strmf(ixm,jym)
c
      integer           i, j
      double precision  cor, cor_br, cor_lt, cor1, cor2
      double precision  sum_d, dist, cor_d, diff, strmfbr
      double precision  strmf21, strmflt, strmf12, strmf22
      double precision  adj_b, adj_t, ab_tot, cd_tot
      double precision  vb_run, ul_run
      double precision  cor_21, cor_22_br, cor_12, cor_22_lt
      double precision  cor_vb, cor_ur, cor_ul, cor_vt
      double precision  sum_vb, sum_vt, avb, avt, delemib, delemit
      double precision  sum_ul, sum_ur, aul, aur, avgdel
c
      INCLUDE 'grid_p_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   the inner edge values have been made non-divergent
c                   now make the corner winds non-divergent
c
      sum_d = (vv(1,jym) +vv(ixm,jym))*emi(jym) -(vv(1,1) +vv(ixm,1))
     &         *emi(1)
      dist  = emi(1) +emi(1) +emi(jym) +emi(jym)
      sum_d = sum_d +emi(1)*(uu(ixm,1)   -uu(1,1))
     &            +emi(jym)*(uu(ixm,jym) -uu(1,jym))
      dist  = dist +emi(1) +emi(1) +emi(jym) +emi(jym)
      cor_d = -sum_d/dist
c     write(20,*) 'INITIAL corner DIV error ',sum_d,' cor ',cor_d
c
      vv(1,1)     = vv(1,1) -cor_d
      vv(ixm,1)   = vv(ixm,1) -cor_d
      vv(1,jym)   = vv(1,jym) +cor_d
      vv(ixm,jym) = vv(ixm,jym) +cor_d
      uu(1,1)     = uu(1,1) -cor_d
      uu(1,jym)   = uu(1,jym) -cor_d
      uu(ixm,1)   = uu(ixm,1) +cor_d
      uu(ixm,jym) = uu(ixm,jym) +cor_d
      sum_d = vv(1,jym)*emi(jym) -vv(1,1)*emi(1) +vv(ixm,jym)*emi(jym)
     &       -vv(ixm,1)*emi(1)
      sum_d = sum_d +emi(1)*(uu(ixm,1) -uu(1,1))
     &              +emi(jym)*(uu(ixm,jym) -uu(1,jym))
c     write(20,*) 'FINAL corner DIV error =',sum_d
c
c                   use the non-divergent winds to estimate
c                   streamfunction values on the boundaries
c
c                         Estimate the corners first
c
      adj_b   = emi(1)
      ab_tot  = 0.5d0*abs (vv(1,1)*adj_b)
      strmfbr = 0.5d0*vv(1,1)*adj_b
      do i=2, ixm-1
        ab_tot  = ab_tot +abs (vv(i,1)*adj_b)
        strmfbr = strmfbr +vv(i,1)*adj_b
      enddo
      ab_tot  = ab_tot +0.5d0*abs (vv(ixm,1)*adj_b)
      strmfbr = strmfbr +0.5d0*vv(ixm,1)*adj_b
      vb_run  = ab_tot
      strmf21 = strmfbr
c
      cd_tot  =  0.5d0*abs (uu(1,1)*emi(1))
      strmflt = -0.5d0*uu(1,1)*emi(1)
      ab_tot  =  ab_tot +0.5d0*abs (uu(ixm,1)*emi(1))
      strmfbr = strmfbr -0.5d0*uu(ixm,1)*emi(1)
      do j=2, jym -1
        cd_tot  = cd_tot +abs (uu(1,j)*emi(j))
        strmflt = strmflt -uu(1,j)*emi(j)
        ab_tot  = ab_tot +abs (uu(ixm,j)*emi(j))
        strmfbr = strmfbr -uu(ixm,j)*emi(j)
      enddo
      cd_tot  = cd_tot +0.5d0*abs (uu(1,jym)*emi(jym))
      strmflt = strmflt -0.5d0*uu(1,jym)*emi(jym)
      ul_run  = cd_tot
      strmf12 = strmflt
c
      ab_tot  = ab_tot  +0.5d0*abs (uu(ixm,jym)*emi(jym))
      strmfbr = strmfbr -0.5d0*uu(ixm,jym)*emi(jym)
c
      adj_t   = emi(jym)
      cd_tot  = cd_tot  +0.5d0*abs (vv(1,jym)*adj_t)
      strmflt = strmflt +0.5d0*vv(1,jym)*adj_t
      do i=2, ixm-1
        cd_tot  = cd_tot +abs (vv(i,jym)*adj_t)
        strmflt = strmflt +vv(i,jym)*adj_t
      enddo
      cd_tot  = cd_tot +0.5d0*abs (vv(ixm,jym)*emi(jym))
      strmflt = strmflt +0.5d0*vv(ixm,jym)*adj_t
      cor     = strmflt -strmfbr
      cor_br  = (ab_tot/(ab_tot +cd_tot))*cor
      cor_lt  = cor_br -cor
c     write(20,*) 'STRMF initial total error ',cor
c     write(20,*) 'STRMF cor_br ',cor_br,' cor_lt ',cor_lt
c
c                   Apply corrections, and convert to full values
c                   at the corners
c
      cor_21    = (vb_run/ab_tot)*cor_br
      strmf21   = (strmf21 +(vb_run/ab_tot)*cor_br)*del
      cor_22_br = cor_br -cor_21
      strmf22   = (strmfbr +cor_br)*del
      cor_12    = (ul_run/cd_tot)*cor_lt
      strmf12   = (strmf12 +(ul_run/cd_tot)*cor_lt)*del
      cor_22_lt = cor_lt -cor_12
      cor       = strmf22 -(strmflt +cor_lt)*del
c
c                   fill edges of array strmf, do corners first
c
      strmf = 0.0d0
      if (cor .eq. 0.0) then
        strmf(ixm,jym) = strmf22
      else
        strmf(ixm,jym) = 0.5d0*strmf22 +0.5d0*(strmflt +cor_lt)*del
        strmf22 = strmf(ixm,jym)
      endif
      strmf(1,jym) = strmf12
      strmf(ixm,1) = strmf21
c
c                   calculate aplha correction factors, top
c
      sum_vb = 0.0d0
      sum_vt = 0.0d0
      do i=1, ixm-1
        sum_vb = sum_vb +0.5d0*(vv(i,1) +vv(i+1,1))
        sum_vt = sum_vt +0.5d0*(vv(i,jym) +vv(i+1,jym))
      enddo
      avb = strmf21/(sum_vb*del*emi(1)) -1.0d0
      avt = (strmf22 -strmf12)/(sum_vt*del*emi(jym)) -1.0d0
c     write(20,*) 'ALPHAs vb ',avb,'  vt ',avt
c
c                   Load edge values between corners, top
c
      delemib = del*emi(1)
      delemit = del*emi(jym)
      do i=2, ixm
        strmf(i,1) = strmf(i-1,1) +(1.0d0 +avb)*(0.5d0*(vv(i-1,1)
     &               +vv(i,1)))*delemib
        strmf(i,jym) = strmf(i-1,jym) +(1.0d0 +avt)*(0.5d0*(vv(i-1,jym)
     &                 +vv(i,jym)))*delemit
      enddo
      cor_vb = strmf(ixm,1) -strmf21
      cor_vt = strmf(ixm,jym) -strmf22
c
c     write(20,*) 'ERROR cor_vb ',cor_vb,'  cor_vt ',cor_vt
c
c                   calculate aplha correction factors, left
c
      sum_ul = 0.0d0
      sum_ur = 0.0d0
      do j=1, jym-1
        avgdel = del*0.5d0*(emi(j) +emi(j+1))
        sum_ul = sum_ul -0.5d0*(uu(1,j) +uu(1,j+1))*avgdel
        sum_ur = sum_ur -0.5d0*(uu(ixm,j) +uu(ixm,j+1))*avgdel
      enddo
      aul = strmf12/sum_ul -1.0d0
      aur = (strmf22 -strmf21)/sum_ur -1.0d0
c     write(20,*) 'ALPHAs ul ',aul,'  ur ',aur
c
c                   Load edge values between corners, left
c
      strmf(ixm,1) = strmf21
      do j=2, jym
        avgdel = del*0.5d0*(emi(j-1) +emi(j))
        strmf(1,j) = strmf(1,j-1) -(1.0d0 +aul)*(0.5d0*(uu(1,j-1)
     &              +uu(1,j)))*avgdel
        strmf(ixm,j) = strmf(ixm,j-1) -(1.0d0 +aur)*(0.5d0*(uu(ixm,j-1)
     &                 +uu(ixm,j)))*avgdel
      enddo
      cor_ul = strmf(1,jym) -strmf12
      cor_ur = strmf(ixm,jym) -strmf22
c
c     write(20,*) 'ERROR cor_ul ',cor_ul,'  cor_ur ',cor_ur
c
c                   Check total inner winds represented by streamfunction
c                   using standard wind speed calculation
c
      cor1   = 0.0d0
      cor2   = 0.0d0
      do i=2, ixm-1
        diff = ((strmf(i+1,1) -strmf(i-1,1))*em(1))/twodel -vv(i,1)
        cor1 = cor1 +diff*diff
        diff = ((strmf(i+1,jym) -strmf(i-1,jym))*em(jym))/twodel
     &           -vv(i,jym)
        cor2    = cor2 +diff*diff
      enddo
      cor1 = (sqrt (cor1))/(ixm-2)
      cor2 = (sqrt (cor2))/(ixm-2)
c     write(20,*) 'RMS V - B ',cor1,'  T ',cor2
c
      cor1 = 0.0d0
      cor2 = 0.0d0
      do j=2, jym-1
        diff = -(em(j)*(strmf(1,j+1) -strmf(1,j-1)))/twodel -uu(1,j)
        cor1 = cor1 +diff*diff
        diff = -(em(j)*(strmf(ixm,j+1) -strmf(ixm,j-1)))/twodel
     &         -uu(ixm,j)
        cor2 = cor2 +diff*diff
      enddo
      cor1 = (sqrt (cor1))/(ixm-2)
      cor2 = (sqrt (cor2))/(ixm-2)
c     write(20,*) 'RMS U - L ',cor1,'  R ',cor2
c
      end
      subroutine setbwnd (ixm,jym,emi,uu,vv)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)setbwnd.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  setbwnd
c
c  DESCRIPTION:  set boundary winds: eliminate net horizontal flow into
c                out of grid
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      integer           ixm, jym
      double precision  emi(jym), uu(ixm,jym), vv(ixm,jym)
c
      integer           i, j
      double precision  sum_d, dist, cor_d
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      sum_d = 0.0d0
c     dist  = 0.0d0
      do i=2, ixm-1
        sum_d = sum_d +vv(i,jym)*emi(jym) -vv(i,1)*emi(1)
c       dist = dist +emi(jym) +emi(1)
      enddo
      dist = (ixm -2)*(emi(jym) +emi(1))
c
      do j=2, jym-1
        sum_d = sum_d +emi(j)*(uu(ixm,j) -uu(1,j))
        dist  = dist +emi(j) +emi(j)
      enddo
      cor_d = -sum_d/dist
c     write (*,*) 'INNER DIV error ',sum_d,' correction ',cor_d
c     write (20,*) 'INNER DIV error ',sum_d,' correction ',cor_d
c
c                   apply corrections
c
      sum_d = 0.0d0
      do i=2, ixm-1
        vv(i,1)   = vv(i,1) -cor_d
        vv(i,jym) = vv(i,jym) +cor_d
        sum_d    = sum_d +vv(i,jym)*emi(jym) -vv(i,1)*emi(1)
      enddo
c
      do j=2, jym-1
        uu(1,j)   = uu(1,j) -cor_d
        uu(ixm,j) = uu(ixm,j) +cor_d
        sum_d    = sum_d +emi(j)*(uu(ixm,j) -uu(1,j))
      enddo
c     write(*,*) 'FINAL DIV error ',sum_d
c     write(20,*) 'FINAL DIV error ',sum_d
c
      end
      subroutine setngcnt (ierr)
c
      implicit none
c
      INCLUDE 'par_ng.inc'
      INCLUDE 'par_mer.inc'
c
c         formal parameter
      integer ierr
c
c         local variables
      integer ncyc, ioe, nsh, nccf, kc, n, irtc, nogo
      integer ijoff, mxcc
      real    posit, rin, rjn, di, dj, dist, ritc, rjtc, rdis
      double precision umx, vmx
      real     cirdat(4,10)
c
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'cyc_i_com.inc'
      INCLUDE 'cyc_v_com.inc'
      INCLUDE 'stat1_com.inc'
      INCLUDE 'stat4_com.inc'
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'comfldio.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'works_com.inc'
c
      data ijoff/5/, mxcc/10/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = 0
      ncyc = 0
c
c                   set flag for hemisphere of cyclone
c
      if (rlat .gt. 0.0) then
        nsh = 1
      else
        nsh = -1
      endif
c
c                   read 1000 hPa global u-wind field
      read (30, iostat=ioe) rfld
      if (ioe .eq. 0) then
c                   load 1000 hPa u-wind in wrk41 as Mercator field
        call merlod4 (rfld,wrk41,ixm,jym,ierr)
        if (ierr .eq. 0) then
c                     read 1000 hPa global v-wind field
          read (30, iostat=ioe) rfld
          if (ioe .eq. 0) then
c
c                     load 1000 hPa v-wind in wrk42 as Mercator field
            call merlod4 (rfld,wrk42,ixm,jym,ierr)
            if (ierr .eq. 0) then
c
c                     load wrk41 with wind direction field
c
              call calddto (wrk41,wrk42,ixm,jym,umx,vmx)
c
c                  look for possible circulation center in wrk41
c
              call fndpcir (wrk41,ixm,jym,icyc-ijoff,icyc+ijoff,
     &                      jcyc-ijoff,jcyc+ijoff,nsh,mxcc,cirdat,nccf)
              if (nccf .gt. 0) then
c
c                   determine hemisphere of cyclone
c
                if (rlat .gt. 0.0) then
                  nsh = 1
                else
                  nsh = -1
                endif
c
c                    confirm circulation center(s) in wrk41 with isogons
c
                call confirm (nsh,wrk41,ixm,jym,mxcc,cirdat,nccf)
                kc = nccf
              else
		write (*,*) 'FOUND zero possible vortex'
                kc = 0
              endif
              write (*,*) 'setngcnt ',kc,' wind center(s) at 1000'
c             write(20,*) 'setngcnt ',kc,' wind center(s) at 1000'
              if (kc .eq. 1) then
                ncyc = 1
              elseif (kc .gt. 1) then
                ncyc  = 0
                posit = 500.0
                do n=1, kc
                  rin  = cirdat(1,n)
                  rjn  = cirdat(2,n)
                  di   = rin -icyc
                  dj   = rjn -jcyc
                  dist = sqrt (di*di +dj*dj)
                  if (dist .lt. posit) then
                    posit = dist
                    ncyc  = n
                  endif
                enddo
              else
                ncyc = 0
              endif
            else
              ierr = -1
            endif
          else
            write (*,*) '1000 hPa v-wind read error is ', ioe
            ierr = -1
          endif
        else
          ierr = -1
        endif
      else
        write (*,*) '1000 hPa u-wind read error is ', ioe
        ierr = -1
      endif
      if (ncyc .gt. 0) then
c
c                   obtain lat/lon of cyclonic circulation
c
        ritc = cirdat(1,ncyc)
        rjtc = cirdat(2,ncyc)
c                     change from Mercator grid co-ord to lat/lon
        rdis = (y2eq +(rjtc -rjcyc)*del)*re_tlat_i
        vlat = rad2deg*(2.0d0*atan (exp (rdis)) -0.5d0*pi)
        irtc = int (ritc)
        vlon = gdlon(irtc) +(ritc -irtc)*mg_deg
        write (*,9010) vlat, vlon
 9010   format (' NOGAPS vortex found at ',f6.2,' lat ',f6.2,' lon')
	nogo = 0
        if (vlat .lt. rlat -5.0 .or. vlat .gt. rlat +5.0) nogo = -1
	if (vlon .lt. rlon -5.0 .or. vlon .gt. rlon +5.0) nogo = -1
c
c                   adjust extraction points of NOGAPS fields
c
        if (nogo .eq. 0) then
	  call adjxtrc (vlat,vlon)
        else
	  vlat = rlat
	  vlon = rlon
	  write (*,*) 'NOGAPS circulation too far away - NO VORTEX'
        endif
      elseif (ierr .eq. 0) then
        vlat = rlat
        vlon = rlon
        write (*,*) 'NO cyclone center found in NOGAPS 1000 hpa winds'
c       write(20,*) 'NO cyclone center found in NOGAPS 1000 hpa winds'
      else
        write (*,*) 'ERROR in setngcnt ..... ABORT'
      endif
c
      end
      subroutine setxltln (mtau)
c
c
c
      implicit none
c
c         formal parameter
      integer mtau
c
c         local variables
      integer nadj
      real    alat, alon, dlat, dlon
c
      INCLUDE 'cyc_r_com.inc'
      INCLUDE 'cyc_v_com.inc'
c
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nadj = 0
      if (mtau .eq. 6) then
        alat = 0.5
        alon = 0.5
      else
        alat = 1.0
        alon = 1.0
      endif
      if (vlat .ne. rlat) then
        nadj = -1
        dlat = rlat -vlat
        if (abs (dlat) .gt. alat) then
          alat = sign (alat,-dlat)
          vlat = vlat +alat
        else
          vlat = rlat
        endif
      endif
      if (vlon .ne. rlon) then
        nadj = -1
        dlon = rlon -vlon
        if (abs (dlon) .gt. alon) then
          alon = sign (alon,-dlon)
          vlon = vlon +alon
        else
          vlon = rlon
        endif
      endif
      if (nadj .eq. -1) call adjxtrc (vlat,vlon)
c
      end
      subroutine smthbd (ni,nj,ijbd,dum,fld)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)smthbd.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  smthbd
c
c  DESCRIPTION:  smooth boundary zone
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
c
      implicit none
c
c          formal parameters
      integer           ni, nj, ijbd
      double precision  dum(ni,nj), fld(ni,nj)
c
c          local variables
      integer           ij, ir, jt, ju, jb, ii, jj, i, j, m
      double precision  alf
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c                      old:
      ij = ijbd
      ir = ni +1 -ij
      jt = nj +1 -ij
      ju = jt -1
      jb = ij +1
      ii = ni -1
      jj = nj -1
c
      alf = 0.25d0
      do m=1, 2
        if (m .eq. 2) alf = -alf
c
        dum = fld
c
        do j=2, ij
          do i=2,ii
            dum(i,j) = fld(i,j) +alf*(fld(i+1,j) -2.0d0*fld(i,j)
     &                +fld(i-1,j))
          enddo
        enddo
        do j=jt, jj
          do i=2, ii
            dum(i,j) = fld(i,j) +alf*(fld(i+1,j) -2.0d0*fld(i,j)
     &                +fld(i-1,j))
          enddo
        enddo
        do j=jb, ju
          do i=2, ij
           dum(i,j) = fld(i,j) +alf*(fld(i+1,j) -2.0d0*fld(i,j)
     &               +fld(i-1,j))
          enddo
        enddo
        do j=jb, ju
          do i=ir, ii
            dum(i,j) = fld(i,j) +alf*(fld(i+1,j) -2.0d0*fld(i,j)
     &                +fld(i-1,j))
          enddo
        enddo
c
        fld = dum
c
        do j=2,ij
          do i=2, ii
            fld(i,j) = dum(i,j) +alf*(dum(i,j+1) -2.0d0*dum(i,j)
     &                +dum(i,j-1))
          enddo
        enddo
        do j=jt, jj
          do i=2, ii
            fld(i,j) = dum(i,j) +alf*(dum(i,j+1) -2.0d0*dum(i,j)
     &                +dum(i,j-1))
          enddo
        enddo
        do j=jb, ju
          do i=2, ij
            fld(i,j) = dum(i,j) +alf*(dum(i,j+1) -2.0d0*dum(i,j)
     &                +dum(i,j-1))
          enddo
        enddo
        do j=jb, ju
          do i=ir, ii
            fld(i,j) = dum(i,j) +alf*(dum(i,j+1) -2.0d0*dum(i,j)
     &                +dum(i,j-1))
          enddo
        enddo
      enddo
c
      end
      subroutine sph2mer (mtau,ierr)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)sph2mer.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  sph2mer
c
c  DESCRIPTION:  driver for loading Mercator grid
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call sph2mer (mtau,ierr)
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c     mtau            int            in      model tau
c     ierr            int            out     error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_ng.inc'
c
c         formal parameters
      integer      mtau, ierr
c
c         local variables
      integer  l, n, ns, nt
c
      INCLUDE 'comfldio.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (mtau .eq. 0) then
	ns = 1
        nt = 4
      else
	ns = 3
	nt = 4
      endif
      do l=1, 4
c                            1    2    3    4
c                   levels 1000, 850, 500, 250
c
        if (l .eq. 2) then
          ns = 1
          nt = 3
        endif
        do n=ns, nt
c                            n = 1  2  3  4
c                     fields of: u, v, t, z
c
          call fldread (mtau,n,l,rfld,ierr)
          if (ierr .ne. 0) then
            write(*,*) 'READ ERROR for tau ',mtau,' L ',l,' N ',n
            goto 399
c
          endif
          if (mtau .gt. 0) call setxltln (mtau)
          call bldmer (rfld,l,n,ierr)
          if (ierr .ne. 0) then
            write(*,*) 'bldmer error ',ierr,' l ',l,' n ',n
            goto 399
c
          endif
        enddo
      enddo
  399 continue
c
      end
      subroutine step1 (time,kht,ihc,jhc)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)step1.f90	1.2  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  step1
c
c  DESCRIPTION:  perform step1 of forecast
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (62 MAR 1997)  Hamilton, H.
c    relocate convective heating to before potential temperature forecast
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c          formal parameters
      integer  kht, ihc, jhc
      real     time
c
c          local variables
      integer           ni, nj, nk, nkw, nn, kl, i, j, k, km, kp, nadj
      integer           nfor(4)
      double precision  dphidx, dphidy, con
c
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr1_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'mstrls_com.inc'
      INCLUDE 'stat2_com.inc'
      INCLUDE 'stat3_com.inc'
      INCLUDE 'works_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ni  = ixm
      nj  = jym
      nk  = 4
      nkw = 3
c
c                   FORECAST U- AND V- COMPONENTS
c
      nn   = 2
      do k=1, nkw
        kl = k +1
        km = max (1,k-1)
        kp = min (nkw,kl)
c
        call fadvec (uu1(1,1,k),vv1(1,1,k),ni,nj,nn,kl,
     &               uu1(1,1,km),uu1(1,1,k),uu1(1,1,kp),
     &               wrk84,wrk86)
c
        call fadvec (uu1(1,1,k),vv1(1,1,k),ni,nj,nn,kl,
     &               vv1(1,1,km),vv1(1,1,k),vv1(1,1,kp),
     &               wrk85,wrk86)
c
        do j=1, nj
          if (j .gt. 1 .and. j .lt. nj) then
            con = em(j)/twodel
            do i=1, ni
              if (i .gt. 1 .and. i .lt. ni) then
                dphidx     = (gz1(i+1,j,kl) -gz1(i-1,j,kl))*con
                uu2(i,j,k) = uu1(i,j,k) +time*((wrk84(i,j)
     &                  +f(j)*vv1(i,j,k) -dphidx)*tend(i,j) +uls(i,j,k))
                dphidy     = (gz1(i,j+1,kl) -gz1(i,j-1,kl))*con
                vv2(i,j,k) = vv1(i,j,k) +time*((wrk85(i,j)
     &                  -f(j)*uu1(i,j,k) -dphidy)*tend(i,j) +vls(i,j,k))
              else
                uu2(i,j,k) = uu1(i,j,k) +time*uls(i,j,k)
                vv2(i,j,k) = vv1(i,j,k) +time*vls(i,j,k)
              endif
            enddo
          else
            do i=1, ni
              uu2(i,j,k) = uu1(i,j,k) +time*uls(i,j,k)
              vv2(i,j,k) = vv1(i,j,k) +time*vls(i,j,k)
            enddo
          endif
        enddo
      enddo
c
      if (kht .ne. 0) then
c
c               SIMULATE CONVECTIVE HEATING at 850
c
        do k=2, nk
          pt1(ihc,jhc,k)   = pt1(ihc,jhc,k)   +heat(k)
          pt1(ihc+1,jhc,k) = pt1(ihc+1,jhc,k) +0.08*heat(k)
          pt1(ihc-1,jhc,k) = pt1(ihc-1,jhc,k) +0.08*heat(k)
          pt1(ihc,jhc+1,k) = pt1(ihc,jhc+1,k) +0.08*heat(k)
          pt1(ihc,jhc-1,k) = pt1(ihc,jhc-1,k) +0.08*heat(k)
        enddo
      endif
c
c               FORECAST POTENTIAL TEMPERATURE
c
      nn = 1
      do k=1, nk
        kl = k
        km = max (1,k-1)
        kp = min (nk,kl)
        call fadvec (uu1(1,1,km),vv1(1,1,km),ni,nj,nn,kl,
     &               pt1(1,1,km),pt1(1,1,k),pt1(1,1,kp),
     &               wrk85,wrk86)
c
        nadj = 0
        nfor = 0
        do j=1, nj
          do i=1, ni
            pt2(i,j,k) = pt1(i,j,k) +time*(wrk85(i,j)*tend(i,j)
     &                  +tls(i,j,k))
            if (k .gt. 1) then
              if (pt2(i,j,k-1) .gt. pt2(i,j,k))
     &               call ptstab (i,j,k,pt2,nadj,nfor(k))
            endif
          enddo
        enddo
        if (nfor(k) .ne. 0) then
          write  (*,*) 'STEP1, BAD INITIAL PT CONDITIONS LEVS ',km,' ',k
          write (20,*) 'STEP1, BAD INITIAL PT CONDITIONS LEVS ',km,' ',k
        endif
      enddo
c
c                   FORECAST 1000 MB GEOPOTENTIAL
c
      nn = 0
      kl = 1
      call fadvec (uu1(1,1,1),vv1(1,1,1),ni,nj,nn,kl,
     &             gz1(1,1,1),gz1(1,1,1),gz1(1,1,2),
     &             wrk85,wrk86)
      do j=1, nj
        do i=1, ni
          gz2(i,j,1) = gz1(i,j,1) +time*(wrk85(i,j)*tend(i,j)
     &                +zls10(i,j))
        enddo
      enddo
c
c                   CALCULATE REMAINING GEOPOTENTIALS
c
      call caluphi (pt2,ni,nj,gz2,nfor)
      do k=2, nk
        if (nfor(k) .ne. 0) then
          write  (*,*) 'BAD STEP1 INITIAL CONDITIONS LEV ',k
          write (20,*) 'BAD STEP1 INITIAL CONDITIONS LEV ',k
        endif
      enddo
c
      end
      subroutine step2 (time,robert,kkk,kht,htadj,itc,jtc,nflt)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)step2.f90	1.2  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  step2
c
c  DESCRIPTION:  perform each forecast, except step1
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (26 MAR 1997)  Hamilton, H.
c    relocate convective heating to before potential temperature forecast
c    and eliminate call to zmin
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      INCLUDE 'par_mer.inc'
c
c          formal parameters
      integer  kkk, kht, itc, jtc, nflt
      real     time, robert, htadj
c
c          local variables
      integer  ni, ni1, nj, nj1, k, kl, nn, j, i, km, kp
      integer  nfix1, nfix2, nadj1, nadj2, nfor1, nfor2, kmin, kmax
c                   use ihc & jhc when call to zmin is used
c     integer           ihc, jhc
      integer           nk, nkw
      real              twotim, fac, b
      double precision  con, wrku3(ixm,jym), wrkv3(ixm,jym)
c
      INCLUDE 'grid_p_com.inc'
      INCLUDE 'mstr1_com.inc'
      INCLUDE 'mstr2_com.inc'
      INCLUDE 'mstrls_com.inc'
      INCLUDE 'omega_com.inc'
      INCLUDE 'minmax_com.inc'
      INCLUDE 'stat2_com.inc'
      INCLUDE 'stat3_com.inc'
      INCLUDE 'works_com.inc'
c
      equivalence (wrk81,wrku3), (wrk82,wrkv3)
c
      data nk/4/, nkw/3/, b/0.2/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ni   = ixm
      ni1  = ixm -1
      nj   = jym
      nj1  = jym -1
      nflt = 0
      fac    = 1.0 -2.0*b
      twotim = 2.0*time
      if (kht .ne. 0) then
c
c                     SIMULATE CONVECTIVE HEATING AT 850
c
        do k=2, nk
          pt2(itc,jtc,k)   = max (pt2(itc,jtc,k) +heat(k)*htadj,
     &                            pt2(itc,jtc,k-1))
          pt2(itc-1,jtc,k) = max (pt2(itc-1,jtc,k) +0.08*heat(k)*htadj,
     &                            pt2(itc-1,jtc,k-1))
          pt2(itc+1,jtc,k) = max (pt2(itc+1,jtc,k) +0.08*heat(k)*htadj,
     &                            pt2(itc+1,jtc,k-1))
          pt2(itc,jtc+1,k) = max (pt2(itc,jtc+1,k) +0.08*heat(k)*htadj,
     &                            pt2(itc,jtc+1,k-1))
          pt2(itc,jtc-1,k) = max (pt2(itc,jtc-1,k) +0.08*heat(k)*htadj,
     &                            pt2(itc,jtc-1,k-1))
        enddo
      endif
c
c                   FORECAST POTENTIAL TEMPERATURE
c
      nfix1 = 0
      nfix2 = 0
      kmin  = -1
      kmax  =  1
c
      nn    = 1
c
      do k=1, nk
        kl = k
        km = max (1, k -1)
        kp = min (nk, k +1)
        call fadvec (uu2(1,1,km),vv2(1,1,km),ni,nj,nn,kl,
     &               pt2(1,1,km),pt2(1,1,k),pt2(1,1,kp),
     &               wrk85,wrk86)
        nadj1 = 0
        nadj2 = 0
        nfor1 = 0
        nfor2 = 0
        do j=1, nj
          do i=1, ni
            wrk86(i,j) = pt1(i,j,k) +twotim*(wrk85(i,j)*tend(i,j)
     &                  +tls(i,j,k))
            pt1(i,j,k) = pt2(i,j,k) +robert*(pt1(i,j,k)
     &                  -2.0d0*pt2(i,j,k) +wrk86(i,j))
            pt2(i,j,k) = wrk86(i,j)
            if (k .gt. 1) then
              if (pt1(i,j,k) .lt. pt1(i,j,km))
     &                call ptstab (i,j,k,pt1,nadj1,nfor1)
              if (pt2(i,j,k) .lt. pt2(i,j,km))
     &                call ptstab (i,j,k,pt2,nadj2,nfor2)
            else
              if (pt1(i,j,1) .lt. pt1mn) then
                call ptgzchk (i,j,kmin,pt1(1,1,1),nadj1)
              elseif (pt1(i,j,1) .gt. pt1mx) then
                call ptgzchk (i,j,kmax,pt1(1,1,1),nadj1)
              endif
              if (pt2(i,j,1) .lt. pt2mn) then
                call ptgzchk (i,j,kmin,pt2(1,1,1),nadj2)
              elseif (pt2(i,j,1) .gt. pt2mx) then
                call ptgzchk (i,j,kmax,pt2(1,1,1),nadj2)
              endif
            endif
          enddo
        enddo
      enddo
c
c                   FORECAST 1000 MB GEOPOTENTIAL
c
      nn = 0
c
      kl = 1
      call fadvec (uu2(1,1,1),vv2(1,1,1),ni,nj,nn,kl,
     &             gz2(1,1,1),gz2(1,1,1),gz2(1,1,2),
     &             wrk85,wrk86)
c
      do j=1, nj
        do i=1, ni
          wrk83(i,j) = gz2(i,j,1)
          gz2(i,j,1) = gz1(i,j,1) +twotim*(wrk85(i,j)*tend(i,j)
     &                +zls10(i,j))
        enddo
      enddo
c
      nadj1 = 0
      nadj2 = 0
      do j=2, nj-1
        do i=2, ni -1
          if (wrk83(i,j) .lt. gz1mn) then
            call ptgzchk (i,j,kmin,wrk83(1,1),nadj1)
          elseif (wrk83(i,j) .gt. gz1mx) then
            call ptgzchk (i,j,kmax,wrk83(1,1),nadj2)
          endif
          if (gz2(i,j,1) .lt. gz2mn) then
            call ptgzchk (i,j,kmin,gz2(1,1,1),nadj1)
          elseif (gz2(i,j,1) .gt. gz2mx) then
            call ptgzchk (i,j,kmax,gz2(1,1,1),nadj2)
          endif
        enddo
      enddo
c     if (nadj1 .gt. 0 .or. nadj2 .gt. 0)
c    &  write(20,*) ' gz2, step ',kkk,' adj ',nadj1,' mins and ',nadj2,
c    &              ' maxs'
c
      do j=1, nj
        do i=1, ni
          gz1(i,j,1) = wrk83(i,j)
        enddo
      enddo
c
c                   FORECAST U- AND V- COMPONENTS USING SHUMAN PRESSURE-
c                   AVERAGING TECHNIQUE AND THE ROBERT TIME FILTER
c
      nn   = 2
c
      do k=1, nkw
        kl = k +1
        km = max (1, k -1)
        kp = min (nkw, kl)
        con = 502.0*(piup(kl) -pilo(kl))
        do j=1, nj
          do i=1, ni
            wrk85(i,j) = gz2(i,j,k) -(pt2(i,j,k) +pt2(i,j,kl))*con
          enddo
        enddo
        call fadvec (uu2(1,1,k),vv2(1,1,k),ni,nj,nn,kl,
     &               uu2(1,1,km),uu2(1,1,k),uu2(1,1,kp),
     &               wrk84,wrk86)
        do j=1, nj
          do i=1, ni
            wrku3(i,j) = uu1(i,j,k) +twotim*uls(i,j,k)
          enddo
        enddo
c
        do j=2, nj1
          do i=2, ni1
            wrku3(i,j) = wrku3(i,j) +twotim*tend(i,j)*(wrk84(i,j)
     &                   +f(j)*vv2(i,j,k))
          enddo
        enddo
        continue
c
        do j=2, nj1
          do i=2, ni1
            wrk83(i,j) = b*(gz1(i+1,j,kl) -gz1(i-1,j,kl) +wrk85(i+1,j)
     &              -wrk85(i-1,j)) +fac*(gz2(i+1,j,kl) -gz2(i-1,j,kl))
          enddo
        enddo
c
        do j=2, nj1
          do i=2, ni1
            wrku3(i,j) = wrku3(i,j) -twotim*tend(i,j)*wrk83(i,j)
     &                   *em(j)/twodel
          enddo
        enddo
c
        call fadvec (uu2(1,1,k),vv2(1,1,k),ni,nj,nn,kl,
     &               vv2(1,1,km),vv2(1,1,k),vv2(1,1,kp),
     &               wrk84,wrk86)
        do j=1, nj
          do i=1, ni
            wrkv3(i,j) = vv1(i,j,k) +twotim*vls(i,j,k)
          enddo
        enddo
c
        do j=2, nj1
          do i=2, ni1
            wrkv3(i,j) = wrkv3(i,j) +twotim*tend(i,j)*(wrk84(i,j)
     &                   -f(j)*uu2(i,j,k))
          enddo
        enddo
c
        do j=2, nj1
          do i=2, ni1
            wrk83(i,j) = b*(gz1(i,j+1,kl) -gz1(i,j-1,kl) +wrk85(i,j+1)
     &              -wrk85(i,j-1)) +fac*(gz2(i,j+1,kl) -gz2(i,j-1,kl))
          enddo
        enddo
c
        do j=2,nj1
          do i=2,ni1
            wrkv3(i,j) = wrkv3(i,j) -twotim*tend(i,j)*wrk83(i,j)*em(j)
     &                  /twodel
          enddo
        enddo
        do j=1, nj
          do i=1, ni
            uu1(i,j,k) = uu2(i,j,k) +robert*(uu1(i,j,k)
     &                  -2.0d0*uu2(i,j,k) +wrku3(i,j))
            vv1(i,j,k) = vv2(i,j,k) +robert*(vv1(i,j,k)
     &                  -2.0d0*vv2(i,j,k) +wrkv3(i,j))
            if ((uu1(i,j,k)*uu1(i,j,k) +vv1(i,j,k)*vv1(i,j,k)) .gt.
     &                   20000.0d0) nflt = 99
            uu2(i,j,k) = wrku3(i,j)
            vv2(i,j,k) = wrkv3(i,j)
            if ((uu2(i,j,k)*uu2(i,j,k) +vv2(i,j,k)*vv2(i,j,k)) .gt.
     &                   20000.0d0) nflt = 99
          enddo
        enddo
        do j=1, nj
          do i=1, ni
            gz1(i,j,kl) = gz2(1,j,kl)
            gz2(i,j,kl) = wrk85(i,j)
          enddo
        enddo
      enddo
c
      end
      subroutine trix (idegbr,idegcr,m,n,a,b,c,y,tcos,d,w)
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)trix.f90	1.2  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  trix
c
c  DESCRIPTION:  solve tridiagonal systems
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (26 MAR 1997)  Hamiltonm, H.
c    speed up algorithm a little
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c          formal parameters
      integer           idegbr, idegcr, m, n
      double precision  a(m), b(m), c(m), y(m), d(m), w(m), tcos(2*n)
c
c          local variables
      integer           mm1, l, k, kkk, lint, i, ip
      double precision  x, xx, z, rl
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      mm1   = m -1
      rl    = (dble (idegbr) +1.0d0)/(dble (idegcr) +1.0d0)
      l     = int (rl)
      lint  = 1
      do k=1, idegbr
        x =  tcos(k)
        if (k .eq. l) then
          kkk = idegbr +lint
          xx  = tcos(kkk) -x
          do i=1, m
            w(i) = y(i)
            y(i) = xx*y(i)
          enddo
        endif
        d(1) = 1.0d0/(x +4.0d0)
        y(1) = y(1)*d(1)
        do i=2, m
          z    = x +4.0d0 -d(i-1)
          d(i) = 1.0d0/z
          y(i) = (y(i) +y(i-1))/z
        enddo
        do ip=1, mm1
          i    = m -ip
          y(i) = y(i) +d(i)*y(i+1)
        enddo
        if (k .eq. l) then
          do i=1, m
            y(i) = y(i) +w(i)
          enddo
          lint = lint +1
          l    = int (dble (lint)*rl)
        endif
      enddo
      return
c
      end
      subroutine unirota (iv,jv,ixg,jyg,vfld)
c
c
c
      integer           iv, jv, ixg, jyg
      double precision  vfld(ixg,jyg)
c
      integer k, n9, i, ii, j, jj, kk, kl
      real    rjsq, risq, dd
      double precision  vmx, tv
      double precision  rnlint
      double precision  vals(0:9)
c
      INCLUDE 'vort_com.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   load vals with average abs relative vorticity
c
      vals(0) = abs (vfld(iv,jv))
      do k=1, 9
        vals(k) = abs (vfld(iv+k,jv)) + abs (vfld(iv-k,jv))
     &          + abs (vfld(iv,jv+k)) + abs (vfld(iv,jv-k))
        vals(k) = 0.25d0 *vals(k)
      enddo
c
c                   ensure voriticy decreases as k increases
c
      do k=1, 8
        vmx = vals(k)
        do kk=k+1, 9
          if (vmx .lt. vals(kk)) then
            tv       = vmx
            vals(k)  = vals(kk)
	    vmx      = vals(k)
            vals(kk) = tv
          endif
        enddo
      enddo
c
c                   backload new values into field
c
      kl = radmx
      vals(0) = sign (vals(0),vfld(iv,jv))
      do k=1,  8
        vals(k) = sign (vals(k),vfld(iv,jv))
	if (k .le. kl) then
          vfld(iv+k,jv) = vals(k)
          vfld(iv-k,jv) = vals(k)
          vfld(iv,jv+k) = vals(k)
          vfld(iv,jv-k) = vals(k)
        endif
      enddo
      vals(9) = sign (vals(9),vfld(iv,jv))
c
c                   load field with interpolated values
c
      n9 = 9
      do j=jv -ijoff, jv +ijoff
        jj   = jv -j
        rjsq = jj*jj
        do i=iv -ijoff, iv +ijoff
          ii   = iv -i
          risq = ii*ii
          dd   = sqrt (rjsq +risq)
          if (dd .gt. 1.0 .and. dd .le. radmx)
     &        vfld(i,j) = rnlint (dd,vals,n9)
        enddo
      enddo
c
      end
      subroutine uvdisp (uu,vv,ixm,jym,icyc,jcyc,wrk1,wrk2)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)uvdisp.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  uvdisp
c
c  DESCRIPTION:  display u
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call uvdisp (uu,vv,ixm,jym,icyc,jcyc,wrk1,wrk2)
c
c  PARAMETERS:
c       Name      Type     Usage           Description
c    --------  ---------  -------  ----------------------------
c      uu         dble      in     array of u-wind components
c      vv         dble      in     array of v-wind components
c      ixm        int       in     first  dimension of fields
c      jym        int       in     second dimension of fields
c      icyc       int       in     location of cyclone, first dimension
c      jcyc       int       in     location of cyclone, second dimension
c      wrk1       real     N/A     work array
c      wrk2       real     N/A     work array
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c         calddto     calculate wind direction,  towards
c
c  LOCAL VARIABLES:  none
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (26 MAR 1997)  Hamilton, H.
c    initial installation in OTCM96
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c          formal arguments
      integer           ixm, jym, icyc, jcyc
      real              wrk1(ixm,jym), wrk2(ixm,jym)
      double precision  uu(ixm,jym,3), vv(ixm,jym,3)
c
c          local variables
      integer  i, j, m
      real     umx, vmx
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do m=1, 3
        write (20,*) ' U-wind for level ',m
        do j=jcyc+10, jcyc-10, -1
          write (20,'(11(f5.0,2x))') (uu(i,j,m),i=icyc-5, icyc+5)
        enddo
        write (20,*) ' V-wind for level ',m
        do j=jcyc+10, jcyc-10, -1
          write (20,'(11(f5.0,2x))') (vv(i,j,m),i=icyc-5, icyc+5)
        enddo
	do j=1, jym
	  do i=1, ixm
            wrk1(i,j) = real (uu(i,j,m))
            wrk2(i,j) = real (vv(i,j,m))
          enddo
	enddo 
        call calddto (wrk1,wrk2,ixm,jym,umx,vmx)
        write (20,*) ' Wind Direction, towards in degrees'
        do j=jcyc+10, jcyc-10, -1
          write (20,'(11(f5.0,2x))') (wrk1(i,j),i=icyc-5, icyc+5)
        enddo
      enddo
      return
c
      end
      subroutine uvrng3a (uu,vv,ix,jy,kkk)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)uvrng3a.f90	1.1  6/1/96
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  uvrng3a
c
c  DESCRIPTION:
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:
c       Name            Type         Usage            Description
c    ----------      ----------     -------  ----------------------------
c
c
c  COMMON BLOCKS:  none
c
c  FILES:
c       Name     Unit    Type    Attribute   Usage   Description
c   -----------  ----  --------  ---------  -------  ------------------
c
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          Name           Description
c         -------     ----------------------
c
c
c  LOCAL VARIABLES:
c          Name      Type                 Description
c         ------     ----       -----------------------------------------
c
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c..............................END PROLOGUE.............................
c
      implicit none
c
      integer           ix, jy, kkk
      double precision  uu(ix,jy,3), vv(ix,jy,3)
c
      integer           i, j, k, kk
      double precision  sumuu, sumvv
      double precision  uux(3), uun(3), uua(3), vvx(3), vvn(3), vva(3)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do k=1, 3
        uux(k) = -999999.9d0
        vvx(k) = -999999.9d0
        uun(k) = -vvx(k)
        vvn(k) =  uun(k)
        sumuu  = 0.0d0
        sumvv  = 0.0d0
        kk     = 0
        do j=1, jy
          do i=1, ix
            if (uu(i,j,k) .gt. uux(k)) uux(k) = uu(i,j,k)
            if (uu(i,j,k) .lt. uun(k)) uun(k) = uu(i,j,k)
            sumuu  = sumuu +uu(i,j,k)
            if (vv(i,j,k) .gt. vvx(k)) vvx(k) = vv(i,j,k)
            if (vv(i,j,k) .lt. vvn(k)) vvn(k) = vv(i,j,k)
            sumvv  = sumvv +vv(i,j,k)
            kk     = kk +1
          enddo
        enddo
        uua(k) = sumuu/kk
        vva(k) = sumvv/kk
      enddo
      write(20,*) 'WIND A-values for step ',kkk
c
c write(*,900) kkk,uux(1),uux(2),uux(3)
      write(20,900) kkk,uux(1),uux(2),uux(3)
  900 format (' Step ',i4,' A-U mx 1-3 ',3f15.5)
c write(*,910) kkk,uua(1),uua(2),uua(3)
      write(20,910) kkk,uua(1),uua(2),uua(3)
  910 format (' Step ',i4,' A-U av 1-3 ',3f15.5)
c write(*,920) kkk,uun(1),uun(2),uun(3)
      write(20,920) kkk,uun(1),uun(2),uun(3)
  920 format (' Step ',i4,' A-U mn 1-3 ',3f15.5)
c
c write(*,930) kkk,vvx(1),vvx(2),vvx(3)
      write(20,930) kkk,vvx(1),vvx(2),vvx(3)
  930 format (' Step ',i4,' A-V mx 1-3 ',3f15.5)
c write(*,940) kkk,vva(1),vva(2),vva(3)
      write(20,940) kkk,vva(1),vva(2),vva(3)
  940 format (' Step ',i4,' A-V av 1-3 ',3f15.5)
c write(*,950) kkk,vvn(1),vvn(2),vvn(3)
      write(20,950) kkk,vvn(1),vvn(2),vvn(3)
  950 format (' Step ',i4,' A-V mn 1-3 ',3f15.5)
c
      end
      subroutine uvstats (u2,v2,u1,v1,ixm,jym)
c
c.............................START PROLOGUE............................
c
c  SCCS IDENTIFICATION:  @(#)uvstats.f90	1.1  3/20/97
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  uvstats
c
c  DESCRIPTION:  display statistics, row by row of u
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  Unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM DEPENDENCIES:  none
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call uvdisp (u2,v2,u1,v1,ixm,jym)
c
c  PARAMETERS:
c       Name      Type     Usage           Description
c    --------  ---------  -------  ----------------------------
c      u2         dble      in     array of modified u-wind components
c      v2         dble      in     array of modified v-wind components
c      u1         dble      in     array of original u-wind components
c      v1         dble      in     array of original v-wind components
c      ixm        int       in     first  dimension of fields
c      jym        int       in     second dimension of fields
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c  ADDITIONAL COMMENTS:
c
c
c....................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c      Name       Type               Description
c    --------   ---------    ----------------------------
c      du         dble       difference in u
c      duavg      dble       average difference in u
c      dumx       dble       maximum difference in u
c      dumn       dble       minimum difference in u
c      dus        dble       sum of differences squared in u
c      duu        dble       sum of differences in u
c      dv         dble       difference in v
c      dvavg      dble       average difference in v
c      dvmx       dble       maximum difference in v
c      dvmn       dble       minimum difference in v
c      dvs        dble       sum of differences squared in v
c      dvv        dble       sum of differences in v
c      urms       dble       rms of u differences
c      vrms       dble       rms of v differences
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  f90
c
c  COMPILE OPTIONS:  standard operational settings
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (26 MAR 1997)  Hamilton, H.
c    initial installation in OTCM
c
c..............................END PROLOGUE.............................
c
      implicit none
c
c          formal parameters
      integer           ixm, jym
      double precision  u2(ixm,jym), v2(ixm,jym), u1(ixm,jym),
     &                  v1(ixm,jym)
c
c          local variables
      integer           i, j
      double precision  du, dumx, dumn, duu, dus, duavg, urms
      double precision  dv, dvmx, dvmn, dvv, dvs, dvavg, vrms
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      do j=jym-1, 2, -1
        dumx = -999999.9d0
        dumn = -dumx
        duu  = 0.0d0
        dus  = 0.0d0
        do i=2, ixm-1
          du   = u2(i,j) -u1(i,j)
          duu  = duu +du
          dus  = dus +du*du
          dumx = max (du,dumx)
          dumn = min (du,dumn)
        enddo
        duavg = duu/(ixm -2)
        urms  = sqrt (dus/(ixm -2) -(duavg*duavg))
        write (20,*) 'U ',j,' rms ',urms,' avg ',duavg,' mx ',dumx,
     &               ' mn ',dumn
      enddo
c
        write (20,*) ' * * * * * * * * * * * * * * * * * * * * * * '
      do j=jym-1, 2, -1
        dvmx = -999999.9d0
        dvmn = -dvmx
        dvv  = 0.0d0
        dvs  = 0.0d0
        do i=2, ixm-1
          dv   = v2(i,j) -v1(i,j)
          dvv  = dvv +dv
          dvs  = dvs +dv*dv
          dvmx = max (dv,dvmx)
          dvmn = min (dv,dvmn)
        enddo
        dvavg = dvv/(ixm -2)
        vrms  = sqrt (dvs/(ixm -2) -(dvavg*dvavg))
        write (20,*) 'V ',j,' rms ',vrms,' avg ',dvavg,' mx ',dvmx,
     &               ' mn ',dvmn
      enddo
c
      end
