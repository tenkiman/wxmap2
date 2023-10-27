!  SCCS IDENTIFICATION:  @(#)mndir.inc	1.1 6/14/96
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
!    Initial installation on OASIS
!
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
!
      integer ii, jj, iv, jv, kkk
!
!                   common mndir variable definitions
!
!           ii - starting minimum first  dimension of contouring block
!           jj - starting minimum second dimension of contouring block
!           iv - starting first  dimension contour direction vector
!           jv - starting second dimension contour direction vector
!          kkk - contour generation indicator
!
      common/mndir/ ii,jj,iv,jv,kkk
