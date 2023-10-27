      subroutine clltxy (flat,flon,
     $     blat,blon,dlat,dlon,igrdx,jgrdy,
     $     xgrd,ygrd,
     $     ierr)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)clltxy.f	1.1 12/15/94
C                        22:43:19 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  clltxy
C
C  DESCRIPTION:  convert lat,lon to x,y grid locations for FNMOC global
C                one-degree grid
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
C  USAGE:  call clltxy (flat,flon,xgrd,ygrd,ierr)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     flat         real          in     latitude, deg  +NH, -SH
C     flon         real          in     longitude, deg (0 - 360E)
C     xgrd         real          out    first  dimension location
C     ygrd         real          out    second dimension location
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
C   invalid lat,lon point    set error flag to -1 and write diagnostic
C
C  ADDITIONAL COMMENTS:
C     Note: grid coordinates are traditional 1-based NOT 0-based
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  none
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          clon      real       working longitude
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
      real flat,flon,xgrd,ygrd

      integer igrdx,jgrdy
      real blat,blon,dlat,dlon

c         local variables

      real clon
      logical verb
      verb=.false.
ccc      verb=.true.
      
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = 0
      clon = flon

      if(verb) print*,'xxxxxxxxxxxxxxxbbbbbbbbbbbbbbbbbb ',flon,flat

      if (clon .eq. 360.0) clon = 0.0
      if (clon .ge. 360.0) clon = clon - 360.0
      xgrd = (clon-blon)/dlon + 1.0 
      if(verb) print*,'xxxxxxxxxxxxxxxaaaaaaaaaaaaaaaaaa ',xgrd,blon,clon,dlon,float(igrdx)+1.0
      if (xgrd.lt.1.0 .or. xgrd.ge.(float(igrdx)+1.0) ) then
        write (33,*) 'clltxy, longitude error, lon = ',clon
        write (*,*) 'clltxy, longitude error, lon = ',clon,xgrd,igrdx
        ierr = -1
ccc        stop 'clltxy'
      endif
      ygrd = (flat-blat)/dlat + 1.0 
      if(verb)  print*,'yyyyyyyyyyyyyyyy',ygrd,flat,blat,dlat
      if (ygrd.lt.1.0 .or. ygrd.gt.(float(jgrdy)+1.0) ) then
        write (33,*) 'clltxy, latitude error, lat = ',flat
        ierr = -1
      endif
      end
