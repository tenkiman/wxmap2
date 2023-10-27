      subroutine cirloc (dfld,ixgrd,jygrd,imin,jmin,imax,jmax,nhsh,
     &                   kccf,kuvs,kint,xc,yc,iunit)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)cirloc.f	1.2 8/1/95
C                        16:16:08 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  cirloc
C
C  DESCRIPTION:  driver routine for locating circulation with isogons
C
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
C  USAGE:  call cirloc (dfld,ixgrd,jygrd,imin,jmin,imax,jmax,nhsh,
C                       kccf,kuvs,kint,xc,yc)
C
C  PARAMETERS:
C     NAME        TYPE      USAGE             DESCRIPTION
C   --------     ------     ------   ------------------------------
C      dfld       real        in     wind direction field, deg
C     ixgrd        int        in     first  dimension of field
C     jygrd        int        in     second dimension of field
C      imin        int        in     first  dimension start of window
C      jmin        int        in     second dimension start of window
C      imax        int        in     first  dimension end of window
C      jmax        int        in     second dimension end of window
C      kccf        int       out     number of cyclones found
C      kuvs        int       out     wind support factor
C                                      0 - no circulation, col
C                                      3 - three quads, cyclonic
C                                      4 - four quads, cyclonic
C      kint        int       out     number of isogons
C                                    1 - 9 - cyclone found
C                                      -77 - no intersection found
C                                      -88 - no isogons produced
C        xc       real       out     x-grid (lon) cyclone location
C        yc       real       out     y-grid (lat) cyclone location
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              COMMON BLOCKS:
C
C      BLOCK    NAME    TYPE   USAGE              NOTES
C     -------  ------   ----   ------   -------------------------------
C       box     lbox     int    out     output unit number
C                 xs    real    out     starting first dim of isogon box
C                 xl    real    out     ending first dim of isogon box
C                 ys    real    out     starting second dim isogon box
C                 yl    real    out     ending second dim of isogon box
C                rxc    real    out     running x-grid location
C                ryc    real    out     running y-grid location
C                nip     int    out     number of intersections
C      view     mini     int    out     starting first dim of isogon box
C               maxi     int    out     ending first dim of isogon box
C               minj     int    out     starting second dim isogon box
C               maxj     int    out     ending second dim of isogon box
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
C     bad  first dimension     write diagnostic, correct error
C     bad second dimension     write diagnostic, correct error
C     no isogons produced      set flag, write diagnostic and return
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C          isocnt     driver routine for producing isogons
C         calcntr     calculate centroid of isogon intersections
C          chkcir     check type of circulation found
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C           ixg       int       first  dimension of windowed dd-field
C           jyg       int       second dimension of windowed dd-field
C           ncc       int       number of cyclonic circulations found
C
C  METHOD:  1) Establish size and location of local grid for
C              constructing isogons.
C           2) Load grid with wind direction values.
C           3) Load common blocks for constructing isogons.
C           4) Construct isogons and determine if there are
C              intersections within the box.
C           5) If one or more systems of intersections are found,
C              determine center of each and the synoptic system that
C              the center(s) represent.
C           6) For each, cyclonic center found load the following:
C              a.   wind support by quadrants (must be 3 or 4)
C              b.   number of intersections used to determine location
C              c.   global grid location of cyclone
C           7) Pass on the number of cyclones found.
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          -----------    ---------------------------------------
C             box.inc     common block
C            view.inc     common block
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
C    Make changes to accomodate capability to find more than one
C    system of intersections per iosgon field.
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      integer ixgrd, jygrd, imin, jmin, imax, jmax, nhsh
      integer kccf, kuvs(4), kint(4)
      integer iunit
      real dfld(ixgrd,jygrd), xc(4), yc(4)
c
c         local variables
      integer ixg, jyg
      parameter (ixg = 7, jyg = 7)
c
      integer is, ie, js, je, n, j, m, i, ii, ix, jy, ibyj, kntr
      integer ncc, nn, k
      integer ktyp(4), kcc(4)
      real ddgrd(ixg,jyg)
c
      INCLUDE 'view.inc'
c
      INCLUDE 'box.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   load local grid, ddgrd, with wind directions.
c                   allow for crossing 0 longitude, which will probably
c                   never happen, for software engineering's sake.
c
      is = imin -1
      if (is .lt. 1) is = ixgrd +is
      ie = imax +2
      if (ie .lt. is) ie = ixgrd +ie
      if (ie -is .gt. ixg -1) then
        ie = is +ixg -1
        write(33,*) ' CIRLOC, warning -- first dimension too big.'
      endif
      js = jmin -1
      je = jmax +2
      if (je -js .gt. jyg -1) then
        je = js +jyg -1
        write(33,*) ' CIRLOC, warning -- second dimension too big.'
      endif
c
      n = 0
      do j=js, je
        n = n +1
        m = 0
        do i=is, ie
          ii = i
          if (ii .gt. ixgrd) ii = ii -ixgrd
          m = m +1
          ddgrd(m,n) = dfld(ii,j)
        enddo
      enddo
c
c                   load isogon common blocks
c
      mini = 2
      xs   = 2.0
      maxi = 5
      xl   = 5.0
      minj = 2
      ys   = 2.0
      maxj = 5
      yl   = 5.0
      ix   = ixg
      jy   = jyg
      ibyj = ix*jy
      nsys = 0
      do n=1, 4
        rxc(n)  = 0.0
        ryc(n)  = 0.0
        nip(n)  = 0
        ktyp(n) = 0
        do m=1, 10
          cx(n,m) = 0.0
          cy(n,m) = 0.0
        enddo
      enddo
ccc      lbox =  9
ccc      open (lbox,file='xyboxd',form='formatted')

      write(33,*) ' cirloc, x-box, fm ',mini,' to ',maxi,' y-box, fm '
     .            ,minj,' to ',maxj,' for cntr near ',xc(1),' ',yc(1)
c
c                   calculate isogons and determine if there is an
c                   intersection(s) within the box, if there is an
c                   interection determine the type of flow depicted
c                   by the isogons for each.
c
      kntr = 0
      call isocnt (ddgrd,ix,jy,ibyj,kntr,iunit)
      if (kntr .gt. 0) then
c
c                   isogons were created
c
        if (nsys .gt. 0) then
c
c                     nsys isogon centers were found
c
          ncc = 0
          do n=1, nsys
            kcc(n) = 0
            if (rxc(n).gt.0.0 .and. ryc(n).gt.0.0) then
c
c                   running intersection is available, if there are
c                   more than 2 intersections, locate centroid
c
              nn = n
              if (nip(n) .gt. 2) call calcntr (nn)
              write(33,*) 'cirloc, intersection at ',rxc(n),' ',ryc(n)
c
c                   check type of circulation found with isogons
c
              call chkcir (ddgrd,ix,jy,nn,ktyp(n))
c
c                   evaluate output from isogons
c
              if (ktyp(n) .ne. 0)  then
                write(33,*) 'cirloc, found circulation, type ',ktyp(n)
              endif
              if (iabs (ktyp(n)) .ge. 3) then
                if (nhsh.gt.0 .and. ktyp(n).gt.0) then
c
c                   closed cyclonic circulation found in NH
c
                  ncc    = ncc +1
                  kcc(n) = -1
                elseif (nhsh.lt.0 .and. iabs (ktyp(n)).le.4) then
c
c                   closed cyclonic circulation found in SH
c
                  ncc    = ncc +1
                  kcc(n) = -1
                endif
              else
                write(33,*) 'cirloc, found a col for location ',n
              endif
            endif
          enddo
          if (ncc .gt. 0) then
            k = 0
            do n=1, nsys
              if (kcc(n) .lt. 0) then
c
c                   good cyclonic circulation found
c
                k = k +1
                kuvs(k) = iabs (ktyp(n))
                kint(k) = nip(n)
                xc(k)   = float (is -1) +rxc(n)
                yc(k)   = float (js -1) +ryc(n)
                write(33,*) 'cirloc, ',k,' qds ',kuvs(k),' int ',kint(k)
              endif
            enddo
            kccf = k
          else
            kccf = -1
            write(33,*) 'circloc, no cyclones found near ',xc(1),' ',
     &                   yc(1)
          endif
        else
          kccf = -77
          write(33,*) 'cirloc, no intersection found near ',xc(1),' ',
     &                 yc(1)
        endif
      else
        kccf = -88
        write(33,*) 'cirloc, no isogons produced $$$$$'
      endif
      return
c
      end
