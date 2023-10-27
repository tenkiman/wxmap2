      subroutine isofnd (exc,eyc,nhsh,ddfld,igrdx,jgrdy,kccf,kuvs,kint,
     &                   xc,yc,iunit)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)isofnd.f	1.2 8/1/95
C                        16:16:14 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  isofnd
C
C  DESCRIPTION:  driver routine to locate tropical cyclone with isogons
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
C  USAGE:  isofnd (exc,eyc,nhsh,ddfld,igrdx,jgrdy,kccf,kuvs,kint,xc,yc)
C
C  PARAMETERS:
C     NAME         TYPE      USAGE             DESCRIPTION
C   --------      -------    ------   ------------------------------
C       exc        real        in     x-location, estimated
C       eyc        real        in     y-location, estimated
C      nhsh         int        in     north/south indicator, +nh -sh
C     ddfld        real        in     wind direction global field, deg
C     igrdx         int        in     first  (x-lon) dimension of fields
C     jgrdy         int        in     second (y-lat) dimension of fields
C      kccf         int       out     cyclonic circulations found
C      kuvs         int       out     code of wind support
C                                          0 - no cyclone
C                                          3 - wind support in 3 quads
C                                          4 - wind support in 4 quads
C      kint         int       out     count of intersection support
C        xc        real       out     x-location of tropical cyclone
C        yc        real       out     y-location of tropical cyclone
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
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C          cirloc     driver routine to locate circulation center
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----     ----------------------------------
C           imax      int     maximum x-edge of isogon window
C           imin      int     minimum x-edge of isogon window
C           isx       int     x-truncated point of search
C           ixgd      int     first dimension of global fields
C           jmax      int     maximum y-edge of isogon window
C           jmin      int     minimum y-edge of isogon window
C           jsy       int     y-truncated point of search
C           jygd      int     second dimension of global fileds
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
C    Make changes to allow processing of up to four isogon intersection
C    centers.
C
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      integer nhsh, igrdx, jgrdy, kccf, kuvs(4), kint(4)
      integer iunit
      real exc, eyc, xc(4), yc(4)
      real ddfld(igrdx,jgrdy)
c
c         local variables
      integer isx, jsy, imin, imax, jmin, jmax, ixgd, jygd
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      kccf  = 0
      xc(1) = exc
      isx   = exc
      yc(1) = eyc
      jsy   = eyc
      ixgd  = igrdx
      jygd  = jgrdy
c
c                   establish isogon window for search
c
      imin = isx  -1
      imax = imin +3
      jmin = jsy  -1
      jmax = jmin +3
c
c                   call driver for using isogon routines
c
      call cirloc (ddfld,ixgd,jygd,imin,jmin,imax,jmax,nhsh,kccf,kuvs,
     &             kint,xc,yc,iunit)
      if (kccf .le. 0)
     &     write (33,*) ' $ $ $ ISOFND, CYCLONE NOT FOUND $ $ $'
      return
c
      end
