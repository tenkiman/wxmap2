      subroutine rcaltln (slat,slon,head,dist,flat,flon)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)rcaltln.f	1.1 12/15/94
C                        22:44:15 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C
C  MODULE NAME:  rcalltln
C
C  DESCRIPTION:  use rhumb line to calculate ending lat,lon given
C                starting lat,lon, heading and distance
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
C  USAGE:  call rcaltln (slat,slon,head,dist,flat,flon)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C      slat         real         in     starting latitude
C      slon         real         in     starting longitude
C      head         real         in     heading (deg)
C      dist         real         in     distance (nm)
C      flat         real         out    ending latitude
C      flon         real         out    ending longitude
C
C  COMMON BLOCKS:  none
C
C  FILES:  none
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:  none
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  none
C
C  LOCAL VARIABLES:
C          NAME      TYPE                DESCRIPTION
C         ------     ----      ----------------------------------
C           crhd     real      heading converted to radians
C         degrad     real      conversion factor, deg to radians
C           dlat     real      distance in terms of latitude
C           dlon     real      distance in terms of longitude
C         hdgrad     real      half of degrad
C           icrs      int      integer value of heading
C           inil      int      initialization flag
C         raddeg     real      conversion factor, radian to degrees
C         rad045     real      radians in 45 degrees
C           rdst     real      absolute distance, nm
C           rhed     real      local copy of heading
C           tiny     real      small number
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
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      real slat, slon, head, dist, flat, flon
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
        if (abs (head -270.0) .le. tiny .or.
     &      abs (head  -90.0) .le. tiny) then
          dlon = rdst/(60.0*cos (slat*degrad))
c                 longitude is in degrees east, 0.0 to 360.0
          if (icrs .eq. 270) then
            flon = slon -dlon
          else
            flon = slon +dlon
          endif
          flat = slat
        elseif (abs (rhed -360.0) .le. tiny .or.
     &          abs (head -180.0) .le. tiny) then
          dlat = rdst/60.0
          if (icrs .eq. 360) then
            flat = slat +dlat
          else
            flat = slat -dlat
          endif
          flon = slon
        else
          crhd = head*degrad
          flat = slat +(rdst*cos (crhd)/60.0)
          flon = slon +raddeg*(alog (tan (rad045 +hdgrad*flat))
     .          -alog (tan (rad045 +hdgrad*slat)))*tan (crhd)
        endif
      else
        flon = slon
        flat = slat
      endif

c--       if going from > E deg to <E check...and put back on right side

      if(flon.lt.0.0) then
        flon=360.0+flon

      endif
      return
c
      end
