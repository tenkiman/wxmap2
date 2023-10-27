      subroutine calcntr (nc)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)calcntr.f	1.2 8/1/95
C                        16:15:57 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  calcntr
C
C  DESCRIPTION:  calculate centroid of intersections
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
C  USAGE:  call calcntr (nc)
C
C  PARAMETERS:
C     NAME        TYPE      USAGE             DESCRIPTION
C   --------     ------     ------   ------------------------------
C      nc         int         in     index to systems
C
C  COMMON BLOCKS:            COMMON BLOCKS ARE DOCUMENTED WHERE THEY ARE
C                            DEFINED IN THE CODE WITHIN INCLUDE FILES.
C                            THIS MODULE USES THE FOLLOWING VARIABLES OF
C                            THE LISTED COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C      /BOX/      lbox      int      in     unit number for diagnostics
C                   xs     real      in     starting first dimension of
C                                           isogon box
C                   xl     real      in     ending first dimension of
C                                           isogon box
C                   ys     real      in     starting second dimension of
C                                           isogon box
C                   yl     real      in     ending second dimension of
C                                           isogon box
C                  nip      int      in     count of intersection points
C                   cx     real      in     array of first dimension
C                                           intersection points
C                   cy     real      in     array of second dimension
C                                           intersection points
C                  rxc     real      in     running average of first
C                                           dimension intersection point
C                  ryc     real      in     running average of second
C                                           dimension intersection point
C                  rxc     real     out     first dimension of cyclone
C                                           location
C                  ryc     real     out     second dimension of cyclone
C                                           location
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
C           diff     real       maximum x or y difference from estimated
C                               centroid
C             dr     real       radial distance from centroid
C         epslon     real       small number
C              k      int       number of iterations
C             rr     real       radial distance from centroid
C             sx     real       sum of x-coord of centroid
C             sy     real       sum of y-coord of centroid
C            ttt     real       temporary variable
C
C  METHOD:  calculate centroid based upon intersections closest to the
C           running centroid position, for index nc.
C           note: nip(nc) must be 3 or greater before calling calcntr
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          -----------    ---------------------------------------
C           box.inc       common block
C
C  COMPILER DEPENDENCIES:  Cray UNICOS
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
C    Make changes to allow for more than one system per "box", by
C    introducing the index nc.
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameter
      integer nc
c
c         local variables
      integer k,m,n
      real diff,rxl,ryl,dx,dy,dr,rr,ttt,sx,sy,epslon
c
      INCLUDE 'box.inc'
c
      data epslon/1.0e-03/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (33,*) ' calcntr, running avg xc ',rxc(nc),' yc ',ryc(nc),
     & ' with ',nip(nc),' intersections'
c
      k    = 0
      diff = 99.9
      do while (nip(nc).gt.2 .and. diff.gt.epslon)
        rxl = rxc(nc)
        ryl = ryc(nc)
c
c                   sort on difference from last estimate of location,
c                   least to most
c
        do m=1, nip(nc) -1
          dx = rxl -cx(nc,m)
          dy = ryl -cy(nc,m)
          dr = dx*dx +dy*dy
          do n=m+1, nip(nc)
            dx = rxl -cx(nc,n)
            dy = ryl -cy(nc,n)
            rr = dx*dx +dy*dy
            if (rr .lt. dr) then
              ttt      = cx(nc,n)
              cx(nc,n) = cx(nc,m)
              cx(nc,m) = ttt
              ttt      = cy(nc,n)
              cy(nc,n) = cy(nc,m)
              cy(nc,m) = ttt
              dr       = rr
            endif
          enddo
        enddo
c
c                   calculate new estimate, w/o worst case
c
        sx = 0.0
        sy = 0.0
        nip(nc) = nip(nc) -1
        do n=1, nip(nc)
          sx = sx +cx(nc,n)
          sy = sy +cy(nc,n)
        enddo
        rxc(nc) = sx/nip(nc)
        ryc(nc) = sy/nip(nc)
        k = k +1
        diff = amax1 (abs (rxl -rxc(nc)), abs (ryl -ryc(nc)))
      enddo
      write (33,*) ' calcntr, with ',k,' iterations: x= ',rxc(nc),
     &             ' y= ',ryc(nc),' with ',nip(nc),' intersections'
      return
c
      end
