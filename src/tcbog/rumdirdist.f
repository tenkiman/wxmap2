      subroutine rumdirdist (sl,sg,el,eg,head,dist)
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

      end

