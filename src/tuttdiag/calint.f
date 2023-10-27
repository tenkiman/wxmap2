      subroutine calint
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)calint.f	1.2 8/1/95
C                        16:16:01 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  calint
C
C  DESCRIPTION:  calculate point(s) of intersection of two isogons
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
C  USAGE:  call calint
C
C  PARAMETERS:  none
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES IN NAMED COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C      box       cx        real     out     new x-intercept
C      box       cy        real     out     new y-intercept
C      box       lbox       int      in     diagnostic unit number
C      box       nip        int    in/out   count of intersections
C      box       rxc       real    in/out   running x-intercept
C      box       ryc       real    in/out   running y-intercept
C      box       xs        real      in     x-start of isogon box
C      box       xl        real      in     x-end of isogon box
C      box       ys        real      in     y-start of isogon box
C      box       yl        real      in     y-end of isogon box
C
C      isoxy     xx1       real      in     x-values of rh1
C      isoxy     yy1       real      in     y-values of rh1
C      isoxy     xx2       real      in     x-values of rh2
C      isoxy     yy2       real      in     y-values of rh2
C      isoxy     nxy1       int      in     number of rh1 points
C      isoxy     nxy2       int      in     number of rh2 points
C      isoxy     rh1       real      in     value of first  isogon
C      isoxy     rh2       real      in     value of second isogon
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
C    1.  The old method of locating the system assumed that only a
C        cyclone or col would be located within each box.  However,
C        testing found that both the col and the cyclone may be found
C        within the box.  Since the old method allowed only one system
C        per box, if the col were found rather than the cyclone the
C        tracking would stop.  90+% of the time, the cyclone was found
C        rather than the col, so this oversite went undetected.
C    2.  During testing so far, the maximum number of systems found has
C        been 2, one col & one cyclone, however the software has been
C        designed to accommodate up to 4 systems per box.
C    3.  Likewise, 10 segments is more than twice the number of segments
C        found thus far during testing.
C    4.  The method of finding the "second" point has also been revised
C        and improved.
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C      name              description
C   ------------       --------------------------------------------
C     evaliso          evaluate possible intersection(s)
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C            a1      real       y-coefficient of rh1
C            a2      real       y-coefficient of rh2
C            b1      real       x-coefficient of rh1
C            b2      real       x-coefficient of rh2
C            c1      real       constant of rh1
C            c2      real       constant of rh2
C           cxl      real       array of last x-locations of cx
C           cyl      real       array of last y-locations of cy
C            dd      real       value of determinant
C            d1      real       value of determinant
C            d2      real       value of determinant
C           dx1      real       delta-x of rh1 near intersection
C           dx2      real       delta-x of rh2 near intersection
C           dy1      real       delta-y of rh1 near intersection
C           dy2      real       delta-y of rh2 near intersection
C          dydx      real       slope of rh1 or rh2 near intersection
C           jdd       int       direction of first isogon
C          jj11       int       primary index of rh1
C          jj12       int       secondary index of rh1
C          jj21       int       primary index of rh2
C          jj22       int       secondary index of rh2
C           kdd       int       direction of second isogon
C         maxpc       int       maximum number of prospective
C                               circulations for S/R evaliso
C           ms1       int       starting segmnet index, rh1
C           me1       int       ending segment index, rh1
C            nn       int       running index to system
C            np       int       index to prospective segments
C           npc       int       max allowed prospective systems (out)/
C                               number of prospective systems (in)
C           n1s       int       starting index to rh1 segment
C           n1e       int       ending index to rh1 segment
C           n2s       int       starting index to rh2 segment
C           n2e       int       ending index to rh2 segment
C           ns2       int       starting segment index, rh2
C           ne2       int       ending segment index, rh2
C             r      real       working distance between rh1 & rh2
C          rmin      real       working minimum distance
C           rmm      real       distance between rh1 & rh2, (-1,-1)
C           rmp      real       distance between rh1 & rh2, (-1,+1)
C           rpm      real       distance between rh1 & rh2, (+1,-1)
C           rpp      real       distance between rh1 & rh2, (+1,+1)
C            x1      real       working x-point of rh1
C            xd      real       working x-distance between rh1 & rh2
C         xx1mn      real       minimum x-distance of rh1 near
C                               intersection
C         xx2mn      real       minimum x-distance of rh2 near
C                               intersection
C            y1      real       working y-point of rh1
C            yd      real       working y-distance between rh1 & rh2
C
C  METHOD:  1.  Call evaliso to establish the starting and ending
C               indecies to rh1 and rh2 of segments that may contain
C               intersections
C           2.  Evaluate each segment for an intersecion within the
C               regional area defined by the indicies
C           3.  For each intersection found, allowcate the intersection
C               to a system based upon the juxtaposition of the running
C               average location of the previously identified systems.
C               If none are found, start a new system.
C           4.  Maintain the count of intersections supporting each
C               system and the running average location of each system.
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          -----------    ---------------------------------------
C           box.inc       common block
C           isoyx.inc     common block
C
C  COMPILER DEPENDENCIES:
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
C    Change tracking algorithm so more than one system may be tracked
C    within the "box".
C
C...................END PROLOGUE.......................................
C
      implicit none
c
      integer maxpc
      parameter (maxpc = 10)
c
      integer jdd,jj11,jj12,jj21,jj22,j901,j902,j1801,j1802,kdd
      integer j1,j2,np,npc,n1s,n1e,n2s,n2e,nn
      integer ms1(maxpc), me1(maxpc), ns2(maxpc), ne2(maxpc)
c
      real a1,a2,b1,b2,c1,c2,c11,c12,c21,c22,dd,d1,d2,dx1,dx2,dy1,dy2
      real dydx,xc,x1,xd,xx1mn,xx2mn,yc,y1,yd,xxs,xxl,yys,yyl
      real r,rmin,rmm,rpm,rpp,rmp,cxl(4),cyl(4)
      real difx,dify,epsln
c
      INCLUDE 'box.inc'
      INCLUDE 'isoxy.inc'
c
      data epsln/0.1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (33,*) ' calint, nxy1 ',nxy1,' rh1 ',rh1,' nxy2 ',nxy2,
     .               ' rh2 ',rh2
c
      jdd = anint (rh1)
      kdd = anint (rh2)
      if (kdd -jdd .eq. 90) then
c
c                   isogons are for directions 90 degrees apart
c
c
c                      evaluate prospects for intersection(s)
c
        npc = maxpc
        call evaliso (nxy1,xx1,yy1, nxy2,xx2,yy2, ms1,me1,ns2,ne2,npc)
        if (npc .gt. 0) then
c
c                   set the last intersection points, for this call to
c                   the S/R, to zero
c
          do nn=1, 4
            cxl(nn) = 0.0
            cyl(nn) = 0.0
          enddo
c
          do np=1, npc
c
c                   extract prospective starting and ending points for
c                   rh1 and rh2 isogons
c
            n1s = ms1(np)
            n1e = me1(np)
            n2s = ns2(np)
            n2e = ne2(np)
c
            rmin = 99999.0
            jj11 = 0
            jj21 = 0
c
c                   locate the indicies to the nearest points of rh1
c                   and rh2 within the two segments defined above
c
            do j1=n1s, n1e
              x1 = xx1(j1)
              y1 = yy1(j1)
              do j2=n2s, n2e
                xd = x1 -xx2(j2)
                yd = y1 -yy2(j2)
                r  = xd*xd +yd*yd
                if (r .lt. rmin) then
c
c                        save the indicies
c
                  rmin = r
                  jj11 = j1
                  jj21 = j2
                endif
              enddo
            enddo
c
c                   the nearest point may not be the first or last point
c                   of the segments - if it is, there is not an
c                   intersection because of the way evaliso establishes
c                   these points
c
            if (jj11 .eq. nxy1) jj11 = -1
            if (jj21 .eq. nxy2) jj21 = -1
            if (jj11.gt.1 .and. jj21.gt.1) then
c
c                   find "second" point for rh1 and rh2
c                   by finding the next nearest point
c
              xd  = xx1(jj11-1) -xx2(jj21-1)
              yd  = yy1(jj11-1) -yy2(jj21-1)
              rmm = xd*xd +yd*yd
              xd  = xx1(jj11-1) -xx2(jj21+1)
              yd  = yy1(jj11-1) -yy2(jj21+1)
              rmp = xd*xd +yd*yd
              xd  = xx1(jj11+1) -xx2(jj21+1)
              yd  = yy1(jj11+1) -yy2(jj21+1)
              rpp = xd*xd +yd*yd
              xd  = xx1(jj11+1) -xx2(jj21-1)
              yd  = yy1(jj11+1) -yy2(jj21-1)
              rpm = xd*xd +yd*yd
              r   = amin1 (rmm,rmp,rpp,rpm)
              if (r .eq. rmm) then
                jj12 = jj11 -1
                jj22 = jj21 -1
              elseif (r .eq. rmp) then
                jj12 = jj11 -1
                jj22 = jj21 +1
              elseif (r .eq. rpp) then
                jj12 = jj11 +1
                jj22 = jj21 +1
              else
                jj12 = jj11 +1
                jj22 = jj21 -1
              endif
c
c                   assume isogons are straight lines at intersection,
c                   so calculate the a, b, c of equation ay +bx = c
c
c                     calculate for rh1
c
              xx1mn = amin1 (xx1(jj11),xx1(jj12))
              if (xx1mn .eq. xx1(jj11)) then
                j901 = jj11
                j902 = jj12
              else
                j901 = jj12
                j902 = jj11
              endif
              dx1 = xx1(j902) -xx1(j901)
              if (dx1 .ne. 0.0) then
                a1   = dx1
                dy1  = yy1(j902) -yy1(j901)
                b1   = -dy1
                dydx = dy1/dx1
                c11  = yy1(j901) -dydx*xx1(j901)
                c12  = yy1(j902) -dydx*xx1(j902)
                c1   = dx1*(0.5*(c11 +c12))
              else
                a1 = 1.0
                b1 = 0.0
                c1 = xx1(j901)
              endif
c
c                     calculate for rh2
c
              xx2mn = amin1 (xx2(jj21),xx2(jj22))
              if (xx2mn .eq. xx2(jj21)) then
                j1801 = jj21
                j1802 = jj22
              else
                j1801 = jj22
                j1802 = jj21
              endif
              dx2 = xx2(j1802) -xx2(j1801)
              if (dx2 .ne. 0.0) then
                a2   = dx2
                dy2  = yy2(j1802) -yy2(j1801)
                b2   = -dy2
                dydx = dy2/dx2
                c21  = yy2(j1801) -dydx*xx2(j1801)
                c22  = yy2(j1802) -dydx*xx2(j1802)
                c2   = dx2*(0.5*(c21 +c22))
              else
                a2 = 1.0
                b2 = 0.0
                c2 = xx2(j1801)
              endif
c
c                     check that lines intercept
c
              dd = a1*b2 -(b1*a2)
              if (dd .ne. 0.0) then
c
c                       calculate new intercept
c
                d1 = c1*b2 -(b1*c2)
                d2 = a1*c2 -(c1*a2)
                yc  = d1/dd
                xc  = d2/dd
c
c                        establish bounds of regional area
c
                xxs = amin1 (xx1(n1s),xx1(n1e),xx2(n2s),xx2(n2e))
                xxl = amax1 (xx1(n1s),xx1(n1e),xx2(n2s),xx2(n2e))
                yys = amin1 (yy1(n1s),yy1(n1e),yy2(n2s),yy2(n2e))
                yyl = amax1 (yy1(n1s),yy1(n1e),yy2(n2s),yy2(n2e))
c
                if (xc.ge.xxs .and. xc.le.xxl .and. yc.ge.yys .and.
     &              yc.le.yyl) then
c
c                          intercept is within regional area
c
                  if (nsys .eq. 0) then
c
c                          start first system for this box
c
                    nsys    = 1
                    nn      = 1
                    rxc(1)  = xc
                    ryc(1)  = yc
                    nip(1)  = 1
                    cx(1,1) = xc
                    cxl(1)  = xc
                    cy(1,1) = yc
                    cyl(1)  = yc
                  else
c
c                         load intersection in proper system
c
                    do nn=1, nsys
c
c                           ensure same position is not loaded again
c
                      difx = abs (cxl(nn) -xc)
                      dify = abs (cyl(nn) -yc)
                      if (difx.le.epsln .and. dify.le.epsln) goto 220
c
                      difx = abs (rxc(nn) -xc)
                      dify = abs (ryc(nn) -yc)
                      if (difx.le.epsln .and. dify.le.epsln) goto 210
c
                    enddo
c
c                      start new system
c
                    nn = nsys +1
                    if (nn .gt. 4) then
                      write (*,*) ' $ $ calint, error more than 4 cc'
                      write (33,*) '$ $ calint, ERROR more than 4 cc'
                      goto 900
c
                    endif
  210               continue
                    if (nip(nn) .eq. nint) then
                      write (*,*) ' $ $ calint, error in allocations'
                      write (33,*) '$ $ calint, ERROR in allocations'
                      goto 220
c
                    endif
                    nip(nn) = nip(nn) +1
                    if (nip(nn) .gt. 1) then
c
c                           calculate running average location
c
                      rxc(nn) = (rxc(nn)*(nip(nn) -1) +xc)/nip(nn)
                      ryc(nn) = (ryc(nn)*(nip(nn) -1) +yc)/nip(nn)
                      cx(nn,nip(nn)) = xc
                      cy(nn,nip(nn)) = yc
                    else
c
c                           load inital position
c
                      rxc(nn) = xc
                      ryc(nn) = yc
                      cx(nn,nip(nn)) = xc
                      cy(nn,nip(nn)) = yc
                      nsys = nn
                    endif
c
c                             load last position to check for duplicates
c
                    cxl(nn) = xc
                    cyl(nn) = yc
                  endif
                  write (33,*) 'calint, ',nn,' ',nip(nn),
     &             ' intersection at ',xc,' ',yc,' for ',rh1,' ',rh2
                else
                  write (33,*) ' calint, intersection outside of',
     &                           ' local region'
                endif
              else
                write (33,*) ' calint, no intercept'
              endif
            else
              write (33,*) ' calint, no calculations'
            endif
  220       continue
          enddo
        else
          write (33,*) 'calint, NO PROSPECTIVE intersections'
        endif
      else
        write (33,9010) rh1, rh2
 9010   format (' rh"s not 90 degreees for ',f7.2,' ',f7.2)
      endif
  900 continue
      do nn=1, nsys
        write (33,*) 'CALINT, system ',nn,' intersections ',nip(nn)
      enddo
      return
c
      end
