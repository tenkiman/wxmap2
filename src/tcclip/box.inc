!  SCCS IDENTIFICATION:  @(#)box.inc	1.1 6/14/96
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
!    Initial installation on OASIS
!
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
!
      integer nint
      parameter (nint = 9)
!
      integer lbox, nsys, nip
      real xs,xl, ys,yl, rxc,ryc, cx,cy
!
!                   common box variable definitions
!
!         lbox - unit number for diagnostics
!           xs - real starting first dimension of isogon box
!           xl - real ending first dimension of isogon box
!           ys - real starting second dimension of isogon box
!           yl - real ending second dimension of isogon box
!         nsys - number of systems being processed
!          rxc - array of running averages, first dimension intersection
!                points
!          ryc - array of running averages second dimension intersection
!                points
!          nip - array of number of intersection points
!           cx - array of first  dimension intersection points
!           cy - array of second dimension intersection points
!
      common/box/ lbox,xs,xl,ys,yl,nsys,rxc(4),ryc(4),nip(4),
     &            cx(4,nint),cy(4,nint)
