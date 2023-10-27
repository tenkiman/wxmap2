!  SCCS IDENTIFICATION:  @(#)isoc.inc	1.1 6/14/96
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
!    Initial installation on OASIS
!
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
!
      integer iter, nc1, nc2
      real rh
!
!
!                   common isoc variable definitions
!
!           rh - true value of isogon, in degrees
!         iter - iteration number, either 1 or 2
!          nc1 - number of isogon points for first  iteration
!          nc2 - number of isogon points for second iteration
!
      common/isoc/ rh,iter,nc1,nc2
