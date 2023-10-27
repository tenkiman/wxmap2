      subroutine isocnt (dfld,mgrd,ngrd,mgbyng,kntr,iunit)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)isocnt.f	1.1 12/15/94
C                        22:43:55 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  isocnt
C
C  DESCRIPTION:  driver for producing isogons in pairs, 90 degrees
C                apart, and solving for the intersection of each pair
C
C  COPYRIGHT:                  (C) 1994 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:
C    CONTOURING AND HIDDEN-LINE ALGORITHMS FOR VECTOR GRAPHIC DISPLAYS.
C    AFAPL-TR-77-3, JANUARY 1977.                      DDC: AD A040530
C    AIR FORCE AERO-PROPULSION LABORATORY
C    AIR FORCE WRIGHT AERONAUTICAL LABORATORIES
C    AIR FORCE SYSTEMS COMMAND
C    WRIGHT-PATTERSON AIR FORCE BASE, OHIO 45433
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
C  USAGE:  call isocnt (dfld,mgrd,ngrd,mgbyng,kntr)
C
C  PARAMETERS:
C     NAME         TYPE     USAGE             DESCRIPTION
C   --------      ------    -----    ------------------------------
C     dfld         real       in     wind direction field
C     mgrd          int       in     first  dimension of field
C     ngrd          int       in     second dimension of field
C   mgbyng          int       in     total length of field
C     kntr          int      out     number of isogons
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE   USAGE              NOTES
C     --------  --------   ----   -----   ------------------------
C       isoc        rh     real    out    real value of isogon, deg
C                 iter      int    out    iteration number
C                  nc1      int    out    isogon count first  iteration
C                  nc2      int    out    isogon count second iteration
C       isol     first      log    out    flag, true if start
C                 last      log    out    flag, true if end
C                 open      log    out    flag, true if open contour
C               backwd      log    out    flag, true if backward contour
C      mndir        ii      int    out    starting minimum first dim of
C                                         contouring block
C                   jj      int    out    starting minimum second dim of
C                                         contouring block
C                   iv      int    out    starting first dim contour
C                                         direction vector
C                   jv      int    out    starting second dim contour
C                                         direction vector
C       view      mini      int     in    starting first dim of box
C                 maxi      int     in    ending first dim of box
C                 minj      int     in    starting second dim of box
C                 maxj      int     in    ending second dim of box
C      zoomv      rint     real    out    first dim resolution of zoomed
C                                         block
C                 sint     real    out    second dim resolution of
C                                         zoomed block
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
C     wrong dimensions of      error diagnostics and exit
C     zoomed block
C
C  ADDITIONAL COMMENTS:
C     No closed contours are allowed, so this code has been removed.
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         iostrc      traces isogons through field
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----    ----------------------------------
C            brh     real    base real "height" value
C           cint     real    contour interval
C           cntr     real    starting contour value
C            dtr     real    degree-to-radian conversion factor
C             hc     real    "height" value being contoured
C          ijtoi      int    double to single index function
C             jp      int    second index point
C           kzlk      int    first dimension of zoomed block
C           lzlk      int    secomd dimension of zoomed block
C           lfld      log    array for contour flags
C         maxim1      int    maxi -1
C         maxjm1      int    maxj -1
C         minip1      int    mini +1
C         minjp1      int    minj +1
C           mxnc      int    maximum number of contours
C            nij      int    single index for i,j location
C           nijp      int    nij of "upper" grid point
C             nr      int    number of contours
C           rdmn     real    minimum value of contour
C           rdmx     real    maximum value of contour
C             rh     real    real "height" value of contour
C             ru     real    "upper" value at grid point
C             rl     real    "lower" value at grid point
C           sfld     real    sine of (dd -rh)
C           zblk     real    zoomed block array
C
C  METHOD:
C    1.  Modification of contouring routines previously developed by
C        H. D. Hamilton for FNOC program CODEDEF.
C    2.  The trick in generating isogons is to trace the zero value of
C        sine (wind direction minus desired isogon direction).
C        Note that sine (0) equals sine (180).  Therefore, if the isogon
C        spacing is 10 degrees, only 10 through 180 degrees is required
C        to provide complete coverage.
C    3.  In order to improve the quality of the intersection point,
C        isogons are produced sequentially in pairs, 90 degrees apart.
C        Therefore, if the 10 degree isogon is not produced, the 100
C        degree isogon is not attempted.
C    4.  Since a complete field of isogons is not desired, only one
C        isogon is allowed for each direction.
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          ----------     ----------------------------------------------
C            box.inc      common block
C           isoc.inc      common block
C           isol.inc      common block
C          isoxy.inc      common block
C          mndir.inc      common block
C           view.inc      common block
C           zoom.inc      common block
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
      integer mgrd, ngrd, mgbyng, kntr
      integer iunit
      real dfld(mgrd,ngrd)
c
c         local variables
      integer kzlk,lzlk
      parameter (kzlk = 11,  lzlk = 11)
c
      logical lfld(mgbyng)
      integer ijtoi, i, j, minip1, minjp1, maxim1, maxjm1, nr
      integer mxnc, k, mn, nij, nijp, jp
      real hc, dtr, rdmn, rdmx, cint, cntr, brh, ru, rl
      real sfld(mgbyng), zblk(kzlk,lzlk)
c
      INCLUDE 'view.inc'
c
      INCLUDE 'isol.inc'
c
      INCLUDE 'isoc.inc'
c
      INCLUDE 'mndir.inc'
c
      INCLUDE 'zoomv.inc'
c
      data hc/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c         integer statement function:
      ijtoi(i,j) = (j-1)*mz +i
c
c - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
c
      dtr    = acos (-1.0)/180.0
      mz     = mgrd
      nz     = ngrd
      mbyn   = mgbyng
      kzlt   = kzlk
      lzlt   = lzlk
      rint   = 1.0/(kzlt -1)
      sint   = 1.0/(lzlt -1)
      minip1 = mini +1
      minjp1 = minj +1
      maxim1 = maxi -1
      maxjm1 = maxj -1
      nr     = 0
c
c           contouring is accomplished at one value, hc, at a time,
c           and one contour at a time.  true value of isogon is rh.
c
      rdmn =   1.0
      rdmx = 360.0
      cint =  10.0
      cntr = cint
      mxnc = anint (180.0/cint)
      brh  = cntr -cint
      do 490 k=1, mxnc
        if (mod (k,2) .ne. 0) then
          brh  = brh +cint
          rh   = brh
          iter = 1
          nc1  = 0
          nc2  = 0
        else
c                   check that first contour has more than one point
          if (nc1 .lt. 5) goto 490
c
          rh   = rh +90.0
          iter = 2
        endif
        write(iunit,*) ' isocnt, k ',k,' iter ',iter,' rh ',rh
        if (rh.lt.rdmn .or. rh.gt.rdmx) goto 490
c
        write(iunit,9010) rh
 9010   format (1x,'contouring all contours of value ',g11.5)
c
c                   field to be contoured, sfld, must be the sine of the
c                   difference between the true wind direction and the
c                   true value of the direction to be contoured, rh.
c                   note, the actual value of the contour being traced,
c                   hc, is always zero.
c
c                   initailize sfld and lfld
c
          do mn=1, mbyn
            lfld(mn) = .false.
            sfld(mn) = sin ((dfld(mn,1) -rh)*dtr)
          enddo
c
c               set edge bits for backward scan
c
c                        bottom row
        nij = ijtoi(mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          rl  = ru
          ru  = sfld(nij+1)
          if (rl.ge.hc .and. ru.lt.hc) lfld(nij) = .true.
          nij = nij +1
        enddo
c                        right side
        nij = ijtoi (maxi,minj)
        ru  = sfld(nij)
        do j=minjp1, maxj
          rl   = ru
          nijp = ijtoi (maxi,j)
          ru   = sfld(nijp)
          if (rl.ge.hc .and. ru.lt.hc) lfld(nij) = .true.
          nij = nijp
        enddo
c                        top row
        nij = ijtoi (maxi,maxj)
        ru  = sfld(nij)
        do i=maxim1, mini, -1
          rl  = ru
          ru  = sfld(nij-1)
          if (rl.ge.hc .and. ru.lt.hc) lfld(nij) = .true.
          nij = nij -1
        enddo
c                        left side
        nij = ijtoi (mini,maxj)
        ru  = sfld(nij)
        do j=maxjm1, minj, -1
          rl   = ru
          nijp = ijtoi (mini,j)
          ru   = sfld(nijp)
          if (rl.ge.hc .and. ru.lt.hc) lfld(nij) = .true.
          nij = nijp
        enddo
c
        backwd = .false.
        open   = .true.
        first  = .true.
        last   = .false.
        kkk    = 0
c
c               the boundary of the array is scanned for the
c               beginning of any open contour of value hc, forward mode.
c
c                   scan bottom
        iv  = -1
        jv  =  0
        jj  = minj
        nij = ijtoi (mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          ii  = i
          rl  = ru
          nij = nij +1
          ru  = sfld(nij)
          if (rl.lt.hc .and. ru.ge.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c                   scan right side
        iv =  0
        jv = -1
        ii = maxi
        ru = sfld(ijtoi (maxi,minj))
        do j=minjp1, maxj
          rl = ru
          jj = j
          ru = sfld(ijtoi (maxi,j))
          if (rl.lt.hc .and. ru.ge.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   scan top
c
        iv  = 1
        jv  = 0
        jj  = maxj
        nij = ijtoi(maxi,jj)
        ru  = sfld(nij)
        do i=maxim1, mini, -1
          ii  = i
          rl  = ru
          nij = nij -1
          ru  = sfld(nij)
          if (rl.lt.hc .and. ru.ge.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   scan left side
c
        iv = 0
        jv = 1
        ii = mini
        j  = maxj
        ru = sfld(ijtoi(mini,j))
        do j=maxjm1, minj, -1
          rl = ru
          jj = j
          ru = sfld(ijtoi (mini,j))
          if (rl.lt.hc .and. ru.ge.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   rescan edges, using backward mode
c
        backwd = .true.
c
c                   scan bottom
c
        write(iunit,*) 'isocnt, starting open backwards'
        iv  = 1
        jv  = 0
        jj  = minj
        nij = ijtoi (mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          ii   = i -1
          rl   = ru
          ru   = sfld(nij+1)
          if (lfld(nij) .and. rl.ge.hc .and. ru.lt.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          nij = nij +1
        enddo
c
c                    scan right side
c
        ii  = maxi
        iv  = 0
        jv  = 1
        nij = ijtoi (maxi,minj)
        ru  = sfld(nij)
        jj  = minj
        do j=minjp1, maxj
          rl   = ru
          jp   = j
          nijp = ijtoi (maxi,jp)
          ru   = sfld(nijp)
          if (lfld(nij) .and. rl.ge.hc .and. ru.lt.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          jj  = jp
          nij = nijp
        enddo
c
c                   scan top
c
        iv  = -1
        jv  =  0
        jj  = maxj
        nij = ijtoi (maxi,jj)
        ru  =  sfld(nij)
        do i=maxim1, mini, -1
          ii  = i +1
          rl  = ru
          ru  = sfld(nij-1)
          if (lfld(nij) .and. rl.ge.hc .and. ru.lt.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          nij = nij -1
        enddo
c
c                   scan left side
c
        ii  =  mini
        iv  =  0
        jv  = -1
        jj  = maxj
        nij = ijtoi (mini,jj)
        ru  = sfld(nij)
        do j=maxjm1, minj, -1
          rl   = ru
          jp   = j
          nijp = ijtoi (mini,jp)
          ru   = sfld(nijp)
          if (lfld(nij) .and. rl.ge.hc .and. ru.lt.hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(iunit,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          jj  = jp
          nij = nijp
        enddo
  450   continue
        if (kkk .ne. 0) nr = nr +1
  490 continue
      if (nr .gt. 0) then
        write(iunit,9020) nr
      else
        write(iunit,9030)
      endif
 9020 format(' found about ',i3,' different valued contours')
 9030 format('   *** no contours ***')
      kntr = nr
      return
c
      end
