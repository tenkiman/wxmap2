      subroutine sortem2 (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,
     &                    jygd,jptsp,kptep,lptwd,sdist,edist,wndmx)
c
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION: @(#)sortem2.f	1.2  8/1/95 
C                       16:35:30  @(#)  
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  sortem2
C
C  DESCRIPTION:  sort on: 1) distance from last know location
C                         2) distance from estimated position
C                         3) wind speed
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
C  USAGE:  sortem2 (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,
C                   jygd,jptsp,kptep,lptwd,sdist,edist,wndmx)
C
C  PARAMETERS:
C     NAME         TYPE     USAGE             DESCRIPTION
C   --------      ------    -----    ------------------------------
C     sgxx         real       in     last known x-grid location
C     sgyy         real       in     last known y-grid location
C     egxx         real       in     estimated  x-grid location
C     egyy         real       in     estimated  y-grid location
C     cirdat       real       in     array of cyclonic circulation data
C                                      (1,n) appx. x-grid location
C                                      (2,n) appx. y-grid location
C                                      (3,n) circulation factor
C                                      (4,n) intersection factor
C     nccf          int       in     number of circulations
C     fffld        real       in     wind speed squared
C     ixgd          int       in     first  dimension of fffld
C     jygd          int       in     second dimension of fffld
C     jptsp         int       out    pointers for min distance from
C                                    last known location
C     kptep         int       out    pointers for min distance from
C                                    estimated position
C     lptwd         int       out    pointers for max wind speed
C     sdist        real       out    distance from last known location
C     edist        real       out    distance from estimated position
C     wndmx        real       out    maximum wind speed near center
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
C         imn         int       truncated grid position, first dimension
C         itemp       int       working temporary storage
C         jmn         int       truncated grid position, second dimension
C         dist       real       working distance storage
C         vormx      real       working vorticity storage
C         wnd1       real       wind speed, lower left corner
C         wnd2       real       wind speed, lower right corner
C         wnd3       real       wind speed, upper right corner
C         wnd4       real       wind speed, upper left corner
C         wind       real       working wind speed value
C         xdst       real       working x-distance storage
C         ydst       real       working y-distance storage
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
C  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
C    Add processing of wind speed arrays
C
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      integer nccf, ixgd, jygd
      integer jptsp(nccf), kptep(nccf), lptwd(nccf)
      real sgxx, sgyy, egxx, egyy
      real cirdat(4,nccf), sdist(nccf), edist(nccf), wndmx(nccf)
      real fffld(ixgd,jygd)
c
c         local variables
      integer n, j, k, itemp, imn, jmn
      real dist, xdst, ydst, wnd1, wnd2, wnd3, wnd4, wind
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   initialize arrays
c
c                         load pointer arrays
      do n=1, nccf
        jptsp(n) = n
        kptep(n) = n
        lptwd(n) = n
      enddo
c
c                         load distance and wind max arrays
c
      do j=1, nccf
c
c                   load sdist based on last known location
c
        xdst = cirdat(1,j) -sgxx
        if (abs (xdst) .gt. 180.0) then
          if (xdst .lt. 0.0) then
            xdst = 360.0 +cirdat(1,j) -sgxx
          else
            xdst = cirdat(1,j) -(sgxx +360.0)
          endif
        endif
        ydst = cirdat(2,j) - sgyy
        sdist(j) = xdst*xdst +ydst*ydst
c
c                   load edist based on estimated location
c
        xdst = cirdat(1,j) -egxx
        if (abs (xdst) .gt. 180.0) then
          if (xdst .lt. 0.0) then
            xdst = 360.0 +cirdat(2,j) -egxx
          else
            xdst = cirdat(2,j) -(egxx +360.0)
          endif
        endif
        ydst = cirdat(2,j) -egyy
        edist(j) = xdst*xdst +ydst*ydst
c
c                  load wndmx array
c
        imn  = cirdat(1,j)
        jmn  = cirdat(2,j)
        wnd1 = fffld(imn,jmn)
        wnd2 = fffld(imn+1,jmn)
        wnd3 = fffld(imn+1,jmn+1)
        wnd4 = fffld(imn,jmn+1)
c
c                   note: fffld values are squared (m/s)
c
        wndmx(j) = sqrt (amax1 (wnd1,wnd2,wnd3,wnd4))
      enddo
c
c               adjust pointer arrays, jptsp, kptep & lptwd
c
c                   sort on distance from past position, min to max
c                   adjust jptsp pointers
c
      do j=1, nccf-1
        dist = sdist(jptsp(j))
        do k=j+1, nccf
          if (sdist(jptsp(k)) .lt. dist) then
            itemp    = jptsp(j)
            jptsp(j) = jptsp(k)
            jptsp(k) = itemp
            dist     = sdist(jptsp(j))
          endif
        enddo
      enddo
c
c                   sort on distance from estimated position, min to max
c                   adjust kptep pointers
c
      do j=1, nccf-1
        dist = edist(kptep(j))
        do k=j+1, nccf
          if (edist(kptep(k)) .lt. dist) then
            itemp    = kptep(j)
            kptep(j) = kptep(k)
            kptep(k) = itemp
            dist     = edist(kptep(j))
          endif
        enddo
      enddo
c
c                   sort on maximum wind speed, max to min
c                   adjust lptwd pointers
c
      do j=1, nccf-1
        wind = wndmx(lptwd(j))
        do k=j+1, nccf
          if (wndmx(lptwd(k)) .gt. wind) then
            itemp    = lptwd(j)
            lptwd(j) = lptwd(k)
            lptwd(k) = itemp
            wind     = wndmx(lptwd(j))
          endif
        enddo
      enddo
      return
c
      end
