      subroutine xerprt(messg,nmessg)
c***begin prologue  xerprt
c***date written   790801   (yymmdd)
c***revision date  820801   (yymmdd)
c***category no.  z
c***keywords  error,xerror package
c***author  jones, r. e., (snla)
c***purpose  prints error messages.
c***description
c     abstract
c        print the hollerith message in messg, of length nmessg,
c        on each file indicated by xgetua.
c     latest revision ---  19 mar 1980
c***references  jones r.e., kahaner d.k., "xerror, the slatec error-
c                 handling package", sand82-0800, sandia laboratories,
c                 1982.
c***routines called  i1mach,s88fmt,xgetua
c***end prologue  xerprt
      integer lun(5)
      character*(*) messg
c     obtain unit numbers and write line to each unit
c***first executable statement  xerprt
      call xgetua(lun,nunit)
      lenmes = len(messg)
      do 20 kunit=1,nunit
         iunit = lun(kunit)
         if (iunit.eq.0) iunit = i1mach(4)
         do 10 ichar=1,lenmes,72
            last = min0(ichar+71 , lenmes)
            write (iunit,'(1x,a)') messg(ichar:last)
   10    continue
   20 continue
      return
      end
