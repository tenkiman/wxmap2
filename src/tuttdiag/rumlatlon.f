      subroutine rumlatlon (head,dist,slat,slon,flat,flon)
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
c  USAGE:  call expltln (head,dist,slat,slon,flat,flon)
c
c  PARAMETERS:
c     NAME       TYPE      USAGE             DESCRIPTION
c   --------    -------    ------    ------------------------------
c     head       real      input     rhumb-line heading in degrees from
c                                    slat/slon
c     dist       real      input     distance from slat/slon to flat/flon (nm)
c     slat       real      input     starting latitude, negative if South
c     slon       real      input     startint longitude, in degrees East
c     flat       real      output    extrapolated latitude, negative if South
c     flon       real      output    extrapolated longitude, in degrees East
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
c     dlon       real     delta longitude from slon to flon for
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
      real  head, dist, slat, slon, flat, flon
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
          flon = slon -dlon
        else
          flon = slon +dlon
        endif
        flat = slat
      else
        rdhd = head*degrad
        flat = slat +(dist*cos(rdhd)/60.0d0)
        if (icrs .eq. 180 .and. abs (head -180.0) .gt. tiny) then
          icrs = 181
        elseif (icrs .eq. 360 .and. abs (head -360.0) .gt. tiny) then
          icrs = 359
        endif
        if (mod (icrs,180) .ne. 0) then
c
c                   Following test NOT required for tropical cyclones
c!!       IF (ABS (FLAT) .GT. 89.0) FLAT = SIGN (89.0,FLAT)
c
          flon = slon +raddeg*(log (tan (rad045 +hdgrad*flat))
     &          -log (tan (rad045 +hdgrad*slat)))*tan (rdhd)
        else
          flon = slon
        endif
      endif
      return
c
      end
