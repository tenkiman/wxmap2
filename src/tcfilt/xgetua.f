      subroutine xgetua(iunita,n)
c***begin prologue  xgetua
c***date written   790801   (yymmdd)
c***revision date  820801   (yymmdd)
c***category no.  r3c
c***keywords  error,xerror package
c***author  jones, r. e., (snla)
c***purpose  returns unit number(s) to which error messages are being
c            sent.
c***description
c     abstract
c        xgetua may be called to determine the unit number or numbers
c        to which error messages are being sent.
c        these unit numbers may have been set by a call to xsetun,
c        or a call to xsetua, or may be a default value.
c
c     description of parameters
c      --output--
c        iunit - an array of one to five unit numbers, depending
c                on the value of n.  a value of zero refers to the
c                default unit, as defined by the i1mach machine
c                constant routine.  only iunit(1),...,iunit(n) are
c                defined by xgetua.  the values of iunit(n+1),...,
c                iunit(5) are not defined (for n .lt. 5) or altered
c                in any way by xgetua.
c        n     - the number of units to which copies of the
c                error messages are being sent.  n will be in the
c                range from 1 to 5.
c
c     latest revision ---  19 mar 1980
c     written by ron jones, with slatec common math library subcommittee
c***references  jones r.e., kahaner d.k., "xerror, the slatec error-
c                 handling package", sand82-0800, sandia laboratories,
c                 1982.
c***routines called  j4save
c***end prologue  xgetua
      dimension iunita(5)
c***first executable statement  xgetua
      n = j4save(5,0,.false.)
      do 30 i=1,n
         index = i+4
         if (i.eq.1) index = 3
         iunita(i) = j4save(index,0,.false.)
   30 continue
      return
      end
