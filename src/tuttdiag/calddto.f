      subroutine calddto (ddfld,fffld,igrdx,jgrdy)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)calddto.f	1.2 8/1/95
C                        16:15:59 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  calddto
C
C  DESCRIPTION:  calculate wind direction, towards, with u,v components
C                and wind speed
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
C  USAGE:  call calddto (ddfld,fffld,igrdx,jgrdy)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C    ddfld         real        in/out   u-component array, m/s
C                                       wind direction, deg (towards)
C    fffld         real         in      v-component array, m/s
C    igrdx          int         in      first  dimension of fields
C    jgrdy          int         in      second dimension of fields
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
C           ddto     real       grid point wind direction
C          epsln     real       small number
C           inil      int       flag for initial calculation
C            rtd     real       radian-to-degree conversion factor
C             uu     real       u-wnd at grid point
C             vv     real       v-wnd at grid point
C
C  METHOD:  N/A
C
C  INCLUDE FILES:  none
C
C  COMPILER DEPENDENCIES:  Cray Fortran 77
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
C    Add calculation of wind speed field.
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      integer igrdx, jgrdy
      real ddfld(igrdx*jgrdy,1), fffld(igrdx*jgrdy,1)
c
c         local variables
      integer inil, n
      real epsln, rtd, uu, vv, ddto
c
      save inil, rtd
c
      data epsln/0.0001/
      data inil/0/, rtd/57.2958279/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .eq. 0) then
        inil = -1
        rtd  = 180.0/acos (-1.0)
      endif
      do n=1, igrdx*jgrdy
        uu = ddfld(n,1)
        vv = fffld(n,1)
c                   note: wind speed is squared
        fffld(n,1) = uu*uu +vv*vv
        if (abs (uu) .lt. epsln) uu = 0.0
        if (abs (vv) .lt. epsln) vv = 0.0
        if (uu.ne.0.0 .or. vv.ne.0.0) then
          ddto = amod (450.0 -rtd*atan2 (vv,uu),360.0)
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
