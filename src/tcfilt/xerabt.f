      subroutine xerabt(messg,nmessg)
c***begin prologue  xerabt
c***date written   790801   (yymmdd)
c***revision date  820801   (yymmdd)
c***category no.  r3c
c***keywords  error,xerror package
c***author  jones, r. e., (snla)
c***purpose  aborts program execution and prints error message.
c***description
c     abstract
c        ***note*** machine dependent routine
c        xerabt aborts the execution of the program.
c        the error message causing the abort is given in the calling
c        sequence, in case one needs it for printing on a dayfile,
c        for example.
c
c     description of parameters
c        messg and nmessg are as in xerror, except that nmessg may
c        be zero, in which case no message is being supplied.
c
c     written by ron jones, with slatec common math library subcommittee
c     latest revision ---  19 mar 1980
c***references  jones r.e., kahaner d.k., "xerror, the slatec error-
c                 handling package", sand82-0800, sandia laboratories,
c                 1982.
c***routines called  (none)
c***end prologue  xerabt
      character*(*) messg
c***first executable statement  xerabt
      stop
      end
