      subroutine isovzm (bfld,zblk,ierr)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)isovzm.f	1.1 12/15/94
C                        22:44:06 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  isovzm
C
C  DESCRIPTION:  zoom grid square into block of interpoalted values,
C                no interpolation on edges (it is not required)
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
C  USAGE:  call isovzm (bfld,zblk,ierr)
C
C  PARAMETERS:
C     NAME         TYPE      USAGE             DESCRIPTION
C   --------      ------     -----    ----------------------------------
C     bfld         real        in     base field
C     zblk         real       out     zoomed block of data
C     ierr          int       out     error flag, 0 no error
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              COMMON BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C     zoomv       kzlt      int     in    first  dim of zoomed block
C                 lzlt      int     in    second dim of zoomed block
C                   mi      int     in    starting minimum first dim of
C                                         contouring block
C                   mz      int     in    first dimension of sfld
C                   nj      int     in    starting minimum second dim of
C                                         contouring block
C                   nz      int     in    second dimension of sfld
C                 rint     real     in    first dim resolution of zoomed
C                                         block
C                 sint     real     in    second dim resolution of
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
C     request interpolation    output diagnostic and return error flag
C     in edges of base field
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
C              a     real       interpoation factors
C             ar     real       interpoation factor
C              b     real       interpolation factors
C             br     real       interpolation factor
C              c     real       interpolation factors
C             cr     real       interpolation factor
C            ecv     real       first set of interpolated values
C          ec3m1     real       interpolation factor
C          ec3m2     real       interpolation factor
C          ec4m2     real       interpolation factor
C           efld     real       environment base field values
C          er3m1     real       interpolation factor
C          er3m2     real       interpolation factor
C          er4m2     real       interpolation factor
C            im       int       starting first  dim grid point
C            jn       int       starting second dim grid point
C             r      real       first  dimension index of block
C             s      real       second dimension index of block
C
C  METHOD:  Apply Ayres' central difference formula in two dimensions
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          ----------     ----------------------------------------------
C          zoomv.inc      common block
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
      INCLUDE 'zoomv.inc'
c
c         formal parameters
      integer ierr
      real bfld(mz,nz), zblk(kzlt,lzlt)
c
c         local variables
      integer im, jn, k, n, m, i, l
      real ar, br, cr, r, s
      real er3m1, er3m2, er4m2, ec3m1, ec3m2, ec4m2
      real efld(16), a(4), b(4), c(4), ecv(4)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      im = mi
      jn = nj
c
c                  check that lower left hand point is an interior point
c
      if (im.ge.2 .and. im.lt. mz-1 .and. jn.ge.2 .and. jn.lt.nz-1) then
c
c                   load 4-by-4 array, efld, for interpolation
c
        k = 0
        do n=jn-1, jn+2, 1
          do m=im-1, im+2, 1
            k = k +1
            efld(k) = bfld(m,n)
          enddo
        enddo
c
c                   load four corners of zblk
c
          zblk(1,1)       = efld(6)
          zblk(kzlt,1)    = efld(7)
          zblk(1,lzlt)    = efld(10)
          zblk(kzlt,lzlt) = efld(11)
c
          if (kzlt.gt.2 .or. lzlt.gt.2) then
c
c                   perform interpolation of efld block to load zblk
c
            do i=1, 4
              er3m1 = efld(8+i) -efld(i)
              er3m2 = efld(8+i) -efld(4+i)
              er4m2 = 0.5*(efld(12+i) -efld(4+i))
              a(i)  = 0.5*er3m1
              b(i)  = 3.0*er3m2 -er3m1 -er4m2
              c(i)  = a(i) +er4m2 -er3m2 -er3m2
            enddo
c
            s = -sint
            do l=1, lzlt
              s = s +sint
              do i=1, 4
                ecv(i) = efld(4+i) +s*(a(i) +s*(b(i) +s*c(i)))
              enddo
c
              ec3m1 = ecv(3) -ecv(1)
              ec3m2 = ecv(3) -ecv(2)
              ec4m2 = 0.5*(ecv(4) - ecv(2))
              ar    = 0.5*ec3m1
              br    = 3.0*ec3m2 -ec3m1 -ec4m2
              cr    = ar +ec4m2 -ec3m2 -ec3m2
              r     = -rint
              do k=1, kzlt
                r = r +rint
                if ((l.ne.1.and.l.ne.lzlt) .or. (k.ne.1.and.k.ne.kzlt))
c
c                   fill block with interpolated values
c
     .            zblk(k,l) = ecv(2) +r*(ar +r*(br +r*cr))
              enddo
            enddo
          endif
          ierr = 0
      else
c
c                   no edge interpolation allowed in this version,
c                   so set ierr to error value.
c
         ierr = -1
         write (*,*) '$$$$$ warning:  error return in isovzm  $$$$$'
      endif
      return
c
      end
