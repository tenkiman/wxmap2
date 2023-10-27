!  SCCS IDENTIFICATION:  @(#)isoxy.inc	1.1 6/14/96
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
!    Initial installation on OASIS
!
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
!
      integer npts
      parameter (npts = 151)
!
      integer nxy1, nxy2
      real rh1,xx1,yy1, rh2,xx2,yy2
!
!                   common isoxy variable definitions
!
!         nxy1 - number of x,y points in first isogon
!          rh1 - value of first isogon, degrees
!          xx1 - first  dimension first isogon location values
!          yy1 - second dimension first isogon location values
!         nxy2 - number of x,y points in second isogon
!          rh2 - value of second isogon, degrees
!          xx2 - first  dimension second isogon location values
!          yy2 - second dimension second isogon location values
!
      common/isoxy/ nxy1,rh1,xx1(npts),yy1(npts),
     &              nxy2,rh2,xx2(npts),yy2(npts)
