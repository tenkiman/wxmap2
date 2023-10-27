!  SCCS IDENTIFICATION:  @(#)zoomv.inc	1.1 6/14/96
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
!    Initial installation on OASIS
!
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
!
      integer mi, nj, kzlt, lzlt, mz, nz, mbyn
      real rint, sint
!
!
!                   common zoomv variable definitions
!
!           mi - starting minimum first  dimension of contouring block
!           nj - starting minimum second dimension of contouring block
!         rint - first  dimension resolution of zoomed block
!         sint - second dimension resolution of zoomed block
!         kzlt - first  dimension of zoomed block
!         lzlt - second dimension of zoomed block
!           mz - first  dimension of field being contoured
!           nz - second dimension of field being contoured
!         mbyn - total size of field being contoured (mz*nz)
!
      common/zoomv/ mi,nj,rint,sint,kzlt,lzlt,mz,nz,mbyn
