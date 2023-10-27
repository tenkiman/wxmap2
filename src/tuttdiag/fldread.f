      subroutine fldread (iunit,
     $     igrdx,jgrdy,
     $     cdtg,rtau,dtau,ddfld,fffld,vvfld,pslfld,
     $     ierr)
C
      implicit none
c
      integer igrdx, jgrdy
      integer iunit

      logical verb

c
c         formal parameters
      integer ierr,dtau,irecu,irecv,irecvv
      integer ierrfld
      
      character*16 cdtg
      real rtau,rlvl(2)
      real ddfld(igrdx,jgrdy),fffld(igrdx,jgrdy),vvfld(igrdx,jgrdy),pslfld(igrdx,jgrdy)
      real undef
      
c
c         local variables
      integer idgrid, irecnum, istatus, len
c
      character*8  seclvl
      character*24 dsetnam, dsets(2), typlvl
      character*32 typmodl, geonam, params(2), units
      character*80 title
      character*24 qtitle

c
c
c                   ISIS parameters
      data typmodl/'/a/jgoerss/tropflds'/, geonam/'glob360x181'/
      data params/'uuwind', 'vvwind'/
      data dsets/'analfld', 'fcstfld'/
      data rlvl/1000.0,0.0/
      data units/'m/s'/
      data typlvl/'pre'/

      verb=.false.
ccc      verb=.true.


c
c                   read 1000 mb u-wind - into ddfld
c         
      irecu=int(rtau/dtau)*3+1
      irecv=irecu+1
      irecvv=irecu+2


ccc      read(iunit,rec=irecu,err=810) ddfld
      read(iunit,err=810) ddfld

      undef=1e10
      call chkfld(ddfld,igrdx,jgrdy,undef,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        write (*,*) 'Reading U-wind for ',cdtg,' tau ',rtau,
     $       ' irecu = ',irecu
        qtitle='ddfld input            '
        call qprntn(ddfld,qtitle,1,1,igrdx,jgrdy,10,6)
      endif

c
c         read 1000 mb v-wind
c         


ccc      read(iunit,rec=irecv,err=810) fffld
      read(iunit,err=810) fffld
      call chkfld(fffld,igrdx,jgrdy,undef,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        write (*,*) 'Reading V-wind for ',cdtg,' tau ',rtau,
     $       ' irecv = ',irecv
        qtitle='fffld input            '
        call qprntn(fffld,qtitle,1,1,igrdx,jgrdy,10,6)

        print*,'Reading rel vort for ',cdtg,' tau ',rtau,
     $       'irecvv = ',irecvv

      endif

         
C  --         read 925 rel vort
C

ccc      read(iunit,rec=irecvv,err=810) vvfld
      read(iunit,err=810) vvfld

c --- set undef to 0 for vort

      call setundef0(vvfld,igrdx,jgrdy,undef,ierrfld)

      call chkfld(vvfld,igrdx,jgrdy,undef,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        write (*,*) 'Reading vort8 ',cdtg,' tau ',rtau,
     $       ' irecv = ',irecvv
        qtitle='vvfld input            '
        call qprntn(vvfld,qtitle,1,1,igrdx,jgrdy,10,6)
      endif


C  --         read slp (mb)
C

      read(iunit,err=810) pslfld
      call chkfld(pslfld,igrdx,jgrdy,undef,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        write (*,*) 'Reading vort8 ',cdtg,' tau ',rtau,
     $       ' irecv = ',irecvv
        qtitle='psl(mb) input          '
        call qprntn(pslfld,qtitle,1,1,igrdx,jgrdy,10,6)
      endif



C
C                   calculate direction of wind, towards - ddfld
C
      call calddto (ddfld,fffld,igrdx,jgrdy)
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


      subroutine setundef0(a,ni,nj,undef,ierr)
      dimension a(ni,nj)
      ierr=0
      do i=1,ni
        do j=1,nj
          if(abs(a(i,j)).ge.undef) a(i,j)=0.0
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
