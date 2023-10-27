      subroutine xerctl(messg1,nmessg,nerr,level,kontrl)
c***begin prologue  xerctl
c***date written   790801   (yymmdd)
c***revision date  820801   (yymmdd)
c***category no.  r3c
c***keywords  error,xerror package
c***author  jones, r. e., (snla)
c***purpose  allows user control over handling of individual errors.
c***description
c     abstract
c        allows user control over handling of individual errors.
c        just after each message is recorded, but before it is
c        processed any further (i.e., before it is printed or
c        a decision to abort is made), a call is made to xerctl.
c        if the user has provided his own version of xerctl, he
c        can then override the value of kontrol used in processing
c        this message by redefining its value.
c        kontrl may be set to any value from -2 to 2.
c        the meanings for kontrl are the same as in xsetf, except
c        that the value of kontrl changes only for this message.
c        if kontrl is set to a value outside the range from -2 to 2,
c        it will be moved back into that range.
c
c     description of parameters
c
c      --input--
c        messg1 - the first word (only) of the error message.
c        nmessg - same as in the call to xerror or xerrwv.
c        nerr   - same as in the call to xerror or xerrwv.
c        level  - same as in the call to xerror or xerrwv.
c        kontrl - the current value of the control flag as set
c                 by a call to xsetf.
c
c      --output--
c        kontrl - the new value of kontrl.  if kontrl is not
c                 defined, it will remain at its original value.
c                 this changed value of control affects only
c                 the current occurrence of the current message.
c***references  jones r.e., kahaner d.k., "xerror, the slatec error-
c                 handling package", sand82-0800, sandia laboratories,
c                 1982.
c***routines called  (none)
c***end prologue  xerctl
      character*20 messg1
c***first executable statement  xerctl
      return
      end
