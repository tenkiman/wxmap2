      subroutine fdump
c***begin prologue  fdump
c***date written   790801   (yymmdd)
c***revision date  820801   (yymmdd)
c***category no.  z
c***keywords  error,xerror package
c***author  jones, r. e., (snla)
c***purpose  symbolic dump (should be locally written).
c***description
c        ***note*** machine dependent routine
c        fdump is intended to be replaced by a locally written
c        version which produces a symbolic dump.  failing this,
c        it should be replaced by a version which prints the
c        subprogram nesting list.  note that this dump must be
c        printed on each of up to five files, as indicated by the
c        xgetua routine.  see xsetua and xgetua for details.
c
c     written by ron jones, with slatec common math library subcommittee
c     latest revision ---  23 may 1979
c***routines called  (none)
c***end prologue  fdump
c***first executable statement  fdump
      return
      end
