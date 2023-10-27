      subroutine readfld (iunit,ua,va,ni,nj,nk,nt,ierr)

      real ua(ni,nj,nk),va(ni,nj,nk),dum(ni,nj)

      include 'params.h'

      character*24 qtitle

      undef=1e10

      irec=1+(nt-1)*nk*2

      do k=1,nk

        read(iunit,rec=irec,err=810) dum

        call chkfld(dum,ni,nj,undef,ierrfld)
        if(ierrfld.eq.1) go to 820

        call load23(dum,ua,ni,nj,nk,k)

        if(verb) then
          write(qtitle,'(a,i2)') 'uuuuuuuuuuuua k = ',k
          call qprntn(dum,qtitle,1,90,ni,nj,12,6)
        endif

        irec=irec+1

        read(iunit,rec=irec,err=810) dum
        call chkfld(dum,ni,nj,undef,ierrfld)
        if(ierrfld.eq.1) go to 820
        call load23(dum,va,ni,nj,nk,k)

        if(verb) then
          write(qtitle,'(a,i2)') 'vvvvvvvvvvvva k = ',k
          call qprntn(dum,qtitle,1,90,ni,nj,12,6)
        endif

        irec=irec+1

      end do

      ierr=0
      return


 810  continue
      ierr=1
      print*,'EEEEE: error reading field in fldread'
      return

 820  continue
      ierr=1
      print*,'UUUUU: field undefined tau = ',int(rtau)
      return

      end

      subroutine load23(a,b,ni,nj,nk,k)
      dimension a(ni,nj),b(ni,nj,nk)

      do i=1,ni
        do j=1,nj
          b(i,j,k)=a(i,j)
        end do
      end do

      return
      end

      subroutine chkfld(a,ni,nj,undef,ierr)
      dimension a(ni,nj)
      ierr=0
      do i=1,ni
        do j=1,nj
          if(abs(a(i,j)).ge.undef) then
            ierr=1
            return
          endif
        end do
      end do
            

      return
      end
