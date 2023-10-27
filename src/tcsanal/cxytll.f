      subroutine cxytll (xgrd,ygrd,clat,clon,ierr)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)cxytll.f	1.1 12/15/94
C                        22:43:22 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  cxytll
C
C  DESCRIPTION:  convert x,y grid locations of FNMOC global one-degree
C                grid to lat,lon
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
C  USAGE:  call cxytll (xgrd,ygrd,clat,clon,ierr)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     clat         real          out    latitude, deg  +NH, -SH
C     clon         real          out    longitude, deg (0 - 360E)
C     xgrd         real          in     first  dimension location
C     ygrd         real          in     second dimension location
C     ierr          int          out    error flag, 0 no error
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
C   invalid x,y grid point    set error flag to -1 and write diagnostic
C
C  ADDITIONAL COMMENTS:
C     Note: grid coordinates are traditional 1-based NOT 0-based
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  none
C
C  LOCAL VARIABLES:  none
C
C  METHOD:  N/A
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
      integer ierr
      real clat, clon, xgrd, ygrd
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = 0
      clon = xgrd  -1.0
      if (clon.lt.0.0 .or. clon.gt.360.0) then
        write (33,*) 'cxytll, x-grid error, x-grid = ',xgrd
        ierr = -1
      endif
      clat = ygrd -91.0
      if (clat.lt.-90.0 .or. clat.gt.90.0) then
        write (33,*) 'cxytll, y-grid error, y-grid = ',ygrd
        ierr = -1
      endif
      end
