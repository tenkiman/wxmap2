!  SCCS IDENTIFICATION:  @(#)isol.inc	1.1 6/14/96
!
!  RECORD OF CHANGES:
!
!  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
!    Initial installation on OASIS
!
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
!
      logical first, last, open, backwd
!
!                   common isol variable definitions
!
!        first - logical flag indicating start of isogon, if true
!         last - logical flag indicating end of isogon, if true
!         open - logical flag indicating open isogon, if true
!       backwd - logical flag indicating trace direction, backward if
!                true
!
      common/isol/ first,last,open,backwd
