      subroutine chkcir (dfld,igx,jgy,nc,isotyp)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)chkcir.f	1.2 8/1/95
C                        16:16:04 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  chkcir
C
C  DESCRIPTION:  determine type of circulation
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
C  USAGE:  call chkcir (dfld,igx,jgy,isotyp)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     dfld         real         in      wind direction (to) array
C      igx          int         in      first  dimension of dfld
C      jgy          int         in      second dimension of dfld
C       nc          int         in      index to intersection
C   isotyp         real         out     type of circulation found
C                                         4 - ccw flow 4 out of 4
C                                         3 - ccw flow 3 out of 4
C                                         0 - col
C                                        -4 - cw flow 4 out of 4
C                                        -3 - cw flow 3 out of 4
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES FROM THESE COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C       box       rxc      real      in     x-location of intersection
C       box       ryc      real      in     y-location of intersection
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
C  MODULES CALLED:
C    Name          Description
C   --------       -----------------------------------------------------
C   avgddt         calculate weighted average wind
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         dde        real       wind direction at East-point
C         ddn        real       wind direction at North-point
C         dds        real       wind direction at South-point
C         ddw        real       wind direction at West-point
C         f1         real       fractional grid-length to "center line"
C         ichk        int       sum of winds within window
C         ixce        int       eastern-edge index
C         jycn        int       northern-edge index
C         jycs        int       southern-edge index
C         ixcw        int       western-edge index
C
C  METHOD:  1.  Check wind direction at cardinal points about
C               intersection.
C           2.  If 3 or 4 agree with cw or ccw flow
C               assign isotyp +sum for ccw and -sum for cw flow.
C           3.  Else, assign isotyp a 0 for a col.
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          ----------    ---------------------------------------
C           box.inc        common block
C
C  COMPILER DEPENDENCIES:  Fortran 77
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
C     Increase turning angle of the wind by 15 degrees to further
C     compensate for 1000 mb flow in boundary layer.
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      integer igx, jgy, nc, isotyp
      real dfld(igx,jgy)
c
c         local variables
      integer ixcw, ixce, jycs, jycn, ichk
      real f1, ddn,dds,dde,ddw, avgddt
c
      INCLUDE 'box.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   obtain north, south, west and east indicies
c                   about isogon intersection
c
      ixcw = anint (rxc(nc))
      if (ixcw .ge. rxc(nc)) ixcw = ixcw -1
      ixce = ixcw +1
      jycs = anint (ryc(nc))
      if (jycs .ge. ryc(nc)) jycs = jycs -1
      jycn = jycs +1
c
c                   obtain wind directions north, south, west and east
c                   of isogon intersection
c                   note, directions are to not from.
c
      f1  = rxc(nc) -ixcw
      ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),f1)
      dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),f1)
      f1  = ryc(nc) -jycs
      ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),f1)
      dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),f1)
c
c                   check the type of flow pattern associated with
c                   isogon intersection
c
c                     check for:  cyclonic circulation, nh
c                                 anticyclonic circulation, sh
c
      ichk = 0
      if (ddn.ge.210.0 .and. ddn.le.315.0) ichk = ichk +1
      if (ddw.ge.120.0 .and. ddw.le.225.0) ichk = ichk +1
      if (dds.ge.030.0 .and. dds.le.135.0) ichk = ichk +1
      if ((dde.ge.000.0 .and. dde.le.045.0) .or.
     .    (dde.ge.300.0 .and. dde.le.360.0)) ichk = ichk +1
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
        if (ddn.ge.045.0 .and. ddn.le.150.0) ichk = ichk +1
        if (dde.ge.135.0 .and. dde.le.240.0) ichk = ichk +1
        if (dds.ge.225.0 .and. dds.le.330.0) ichk = ichk +1
        if ((ddw.ge.000.0 .and. ddw.le.060.0) .or.
     .      (ddw.ge.315.0 .and. ddw.le.360.0)) ichk = ichk +1
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
      return
c
      end
