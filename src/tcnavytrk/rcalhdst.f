      subroutine rcalhdst (slat,slon,flat,flon,head,dist)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)rcalhdst.f	1.1 12/15/94
C                        22:44:12 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  rcalhdst
C
C  DESCRIPTION:  use rhumb line to calculate heading and distance from
C                slat,slon to flat,flon
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
C  USAGE:  call rcalhdst (slat,slon,flat,flon,head,dist)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C      slat         real         in     initial latitude
C      slon         real         in     initial longitude
C      flat         real         in     final latitude
C      flon         real         in     final longitude
C      head         real         out    heading (deg)
C      dist         real         out    distance (nm)
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
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C           a45r     real       radians per 45 degrees
C           eln1     real       intermediate calculation factor
C           eln2     real       intermediate calculation factor
C           inil      int       set-up caculation flag
C            rad     real       degrees per radian
C           radi     real       radians per degree
C           rai2     real       radians per two degrees
C           tiny     real       small real number, hardware dependent
C             xl     real       working initial latitude
C             xn     real       working initial longitude
C             xr     real       intermediate calculation factor
C             yl     real       working final latitude
C             yn     real       working final longitude
C             yr     real       intermediate calculation factor
C
C  METHOD:  standard calculations, with near pole point corrections
C           omitted - no tropical cyclones near the poles
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
      real slat, slon, flat, flon, head, dist
c
c         local variables
      integer inil
c
      real rad, radi, rdi2, a45r, tiny, xl, xn, yl, yn
      real eln1, eln2, xr, yr
c
      save rad,radi,rdi2,a45r
c
      data tiny/0.1e-6/
c                   maximum poleward latitude, hardware dependent
ccc   data plmx/89.99/
      data inil/-1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .ne. 0) then
         inil = 0
         rad  = 180.0/acos (-1.0)
         radi = 1/rad
         rdi2 = 0.5*radi
         a45r = 45.0*radi
      endif
c                    same point returns 0.0 head and 0.0 dist
      head = 0.0
      dist = 0.0
c                   southern hemisphere latitude is negative
      xl = slat
      yl = flat
c                   longitude is 0 -360 in degrees East or
c                             negative for West longitude
      xn = slon
      yn = flon
      if (xl.ne.yl .or. xn.ne.yn) then
c                   if longitude is west, convert to 0-360 east
        if (xn .lt. 0.0) xn = xn +360.0
c                   if longitude is west, convert to 0-360 east
        if (yn .lt. 0.0) yn = yn +360.0
c                    check for shortest angular distance
        if (xn.gt.270.0 .and. yn.lt.90.0) then
          yn = yn +360.0
        elseif (yn.gt.270.0 .and. xn.lt.90.0) then
          xn = xn +360.0
        endif
        if (abs (xl -yl) .gt. tiny) then
c                   calculate initial distance
          dist = 60.0*(xl -yl)
          if (abs (xn -yn) .gt. tiny) then
c                   check for positions poleward of 89+ degrees latitude
ccc         if (abs (xl).gt.plmx .or. abs (yl).gt.plmx) then
c              (hardware dependent - not required for tropical cyclones)
ccc           xlt = xl
ccc           if (abs (xlt) .gt. plmx) xlt = sign (plmx,xl)
ccc           ylt = yl
ccc           if (abs (ylt) .gt. plmx) ylt = sign (plmx,yl)
ccc           xr   = tan (xlt*rdi2 +sign (a45r,xl))
ccc           yr   = tan (ylt*rdi2 +sign (a45r,yl))
ccc         else
              xr   = tan (xl*rdi2 +sign (a45r,xl))
              yr   = tan (yl*rdi2 +sign (a45r,yl))
ccc         endif
            eln1 = sign (alog (abs (xr)),xr)
            eln2 = sign (alog (abs (yr)),yr)
            head = rad*(atan ((xn -yn)/(rad*(eln1 -eln2))))
            if (yl   .lt. xl)  head = head +180.0
            if (head .le. 0.0) head = head +360.0
c                   correct initial distance, based only on latitiude
            dist = dist/cos (head*radi)
          else
c                  resolve 0 or 180 heading, note head is preset to zero
            if (yl .lt. xl) head = 180.0
          endif
        else
c                    resolve 90 or 270 heading
          head = 90.0
          if (yn .lt. xn) head = 270.0
          dist = 60.0*(yn -xn)*cos (xl*radi)
        endif
        dist = abs (dist)
      endif
      return
c
      end
