      real function avgddt (dd1,dd2,f1)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)avgddt.f	1.1 12/15/94
C                        22:42:38 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  avgddt
C
C  DESCRIPTION:  calculate weighted average wind direction
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
C  USAGE:  avgdd = avgddt (dd1,dd2,f1)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     dd1          real          in     wind direction at point 1, deg
C     dd2          real          in     wind direction at point 2, deg
C      f1          real          in     fraction of grid length from pt1
C                                       to "center-line", which is
C                                       between pt 1 and pt 2
C  avgddt          real         out     weighted average wind direction
C                                       on "center-line", degrees
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
C          dds       real       copy of dd1 or dd2
C          ddl       real       copy of dd2 or dd1
C           fs       real       fractional part of grid length
C           fl       real       fractional part of grid length
C
C  METHOD:  simple weighted average
C
C  INCLUDE FILES:  none
C
C  COMPILER DEPENDENCIES:  Fortran 77 or 90
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
      return
c
      end
