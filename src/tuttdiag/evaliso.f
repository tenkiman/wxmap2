      subroutine evaliso (md1,fx1,fy1,nd2,fx2,fy2,m1s,m1e,n2s,n2e,npc)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  %W% %G%
C                        %U% %Z%
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  evaliso
C
C  DESCRIPTION:  evaluate isogons for segments that may intersect
C
C  COPYRIGHT:                  (C) 1995 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
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
C  USAGE:  call evaliso (md1,fx1,fy1,nd2,fx2,fy2,m1s,m1e,n2s,n2e,npc)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C      md1          int         in      dimension of fx1 & fy1
C      fx1         real         in      array of x-values of isogon rh1
C      fy1         real         in      array of y-values of isogon rh1
C      nd2          int         in      dimension of fx2 & fy2
C      fx2         real         in      array of x-values of isogon rh2
C      fy2         real         in      array of y-values of isogon rh2
C      m1s          int         out     array of rh1 start points
C      m1e          int         out     array of rh1 end points
C      n2s          int         out     array of rh2 start points
C      n2e          int         out     array of rh2 end points
C      npc          int        in/out   maximum size of m1s, m1e, n2s &
C                                       n2e / count of segments that
C                                       contain potential centers
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
C         dx         real       working difference in x
C         dy         real       working difference in x
C         epsilon    real       minimum value of distance
C         ddw        real       wind direction at West-point
C         mm          int       working index to rh1 values
C         mxpc        int       maximum number of segments
C         nn          int       working index to rh2 values
C         x1         real       working x location of rh1
C         y1         real       working y location of rh1
C
C  METHOD:  1.  Initialize starting and ending points to zero.
C           2.  Iteratively search rh1 and rh2 isogon locations for a
C               gap less than or equal to epsilon.  Mark the starting
C               indicies in m1s and n2s.
C           3.  Continue iterative search for a gap greater than
C               epsilon.  Mark the ending inicies in m1e and n2e.
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
C  <<CHANGE NOTICE>>  Version 1.1  (09 AUG 1995) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (13 SEP 1995) -- Hamilton, H.
C    Remove data dependent problem to prevent over indexing
C
C...................END PROLOGUE.......................................
C
      implicit none
!
!         formal parameters
      integer md1, nd2, npc
      integer m1s(npc), m1e(npc), n2s(npc), n2e(npc)
      real fx1(md1), fy1(md1), fx2(nd2), fy2(nd2)
!
!         local variables
      integer m, mm, ms, mxpc, n, nn
      real x1, y1, dx, dy
      real epsilon
!
      data epsilon/0.1/
! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
!
!                   Initialize prospective locations
!
      mxpc = npc
      do n=1, npc
        m1s(n) = 0
        m1e(n) = 0
        n2s(n) = 0
        n2e(n) = 0
      enddo
      npc = 0
!
!                   Look for prospective starting and ending points
!
      ms = 1
  110 continue
      do m=ms, md1
        x1 = fx1(m)
        y1 = fy1(m)
        do n=1, nd2
          dx = abs (x1 -fx2(n))
          dy = abs (y1 -fy2(n))
          if (dx.le.epsilon .and. dy.le.epsilon) then
            npc = npc +1
            if (npc .le. mxpc) then
!
!                  Mark starting indicies for intersection
!
              m1s(npc) = m
              n2s(npc) = n
            else
              write (*,*) ' TCTRACK, evaliso, npc too small!!'
              npc = mxpc
              goto 200
!
            endif
            mm   = m
            nn   = n
!
!                   Top of internal loop to find ending point
!
  120       continue
            mm = mm +1
            nn = nn +1
            if (mm.le.md1 .and. nn.le.nd2) then
              dx = abs (fx1(mm) -fx2(nn))
              dy = abs (fy1(mm) -fy2(nn))
              if (dx.gt.epsilon .and. dy.gt.epsilon) then
!
!                     Mark ending indicies
!
                m1e(npc) = mm
                ms       = mm +1
                n2e(npc) = nn
                goto 110
!
              elseif (mm.lt.md1 .and. nn.lt.nd2) then
!
!                       Jump to top of internal loop
!
                  goto 120
!
              else
                m1e(npc) = mm
                n2e(npc) = nn
                if (mm .lt. md1) then
                  ms = mm +1
                  goto 110
!
                else
!
!                       Finished searches
!
                  goto 200
!
                endif
              endif
            else
              if (m1s(npc).eq.m -1 .and. n2s(npc).eq.n -1) then
!
!                   Too close to the edge for find ending point
!
                npc = npc -1
              else
!
!                   At the edge, so assume this is the end
!
                m1e(npc) = mm -1
                n2e(npc) = nn -1
              endif
              goto 130
!
            endif
          endif
        enddo
  130   continue
      enddo
  200 continue
      end
