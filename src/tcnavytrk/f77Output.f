cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c
      module f77Output

      use f77OutputMeta
      use mfutils
      
      implicit none

      real*4, allocatable, dimension(:,:) :: ddfld
      real*4, allocatable, dimension(:,:) :: fffld
      real*4, allocatable, dimension(:,:) :: vvfld
      real*4, allocatable, dimension(:,:) :: pslfld
        
      contains

      subroutine initFlds

      integer istat

      allocate(ddfld(ni,nj),stat=istat)
      if(istat.gt.0) go to 814

      allocate(fffld(ni,nj),stat=istat)
      if(istat.gt.0) go to 814

      allocate(vvfld(ni,nj),stat=istat)
      if(istat.gt.0) go to 814

      allocate(pslfld(ni,nj),stat=istat)
      if(istat.gt.0) go to 814

      return

 814  continue
      print*,'error in allocate... '
      stop 814
      
      return
      end subroutine initFlds


      subroutine readFlds(ntau)

      integer ntau,iunittcf,ierr,ierrfld,itau,irecvv

      real undef

      character*24 qtitle

      logical verb

c--  initialize variables
c
      verb=.false.
ccccc      verb=.true.
      undef=1e10
      iunittcf=99

      if(ntf == 1) then
        open(iunittcf,file=DataPaths(ntf)(1:ichlen(DataPaths(ntf),128)),
     $       form='unformatted',
     $       status='old',err=805)

      else

        open(iunittcf,file=DataPaths(ntau)(1:ichlen(DataPaths(ntau),128)),
     $       form='unformatted',
     $       status='old',err=805)
      endif

c--       read ddfld
c         
      read(iunittcf,err=810,end=810) ddfld

      call chkfld(ddfld,ni,nj,undef,10.000000,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        qtitle='ddfld  input           '
        call qprntn(ddfld,qtitle,1,1,ni,nj,10,6)
      endif

c--       read fffld
c         
      read(iunittcf,err=810,end=810) fffld

      call chkfld(fffld,ni,nj,undef,10.000000,ierrfld)
      call setundef0(fffld,ni,nj,undef,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        qtitle='fffld  input           '
        call qprntn(fffld,qtitle,1,1,ni,nj,10,6)
      endif

c--       read vvfld
c         
      read(iunittcf,err=810,end=810) vvfld

      call chkfld(vvfld,ni,nj,undef,10.000000,ierrfld)
      call setundef0(vvfld,ni,nj,undef,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        qtitle='vvfld  input           '
        call qprntn(vvfld,qtitle,1,1,ni,nj,10,6)
      endif

c--       read pslfld
c         
      read(iunittcf,err=810,end=810) pslfld

      call chkfld(pslfld,ni,nj,undef,10.000000,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verb) then
        qtitle='pslfld input           '
        call qprntn(pslfld,qtitle,1,1,ni,nj,10,6)
      endif
      return

 805  continue
      ierr=1
      print*,'EEEEE: error opening file in readFlds'

 810  continue
      ierr=1
      print*,'EEEEE: error reading field in readFlds'
      return

 820  continue
      ierr=1
      print*,'UUUUU: field undefined ntau: ',ntau

      return

      end subroutine readFlds


      subroutine chkfld(a,ni,nj,undef,pcntundefMax,ierr)

      real undef
      real*4 a,pcntundef,pcntundefMax
      integer i,j,ierr,nundef,ntot,ni,nj

      dimension a(ni,nj)

      ntot=ni*nj
      ierr=0
      nundef=0
      do i=1,ni
        do j=1,nj
          if(abs(a(i,j)).ge.undef) then
            nundef=nundef+1
          endif
        end do
      end do

      pcntundef=float(nundef)/float(ntot)

      
      if(pcntundef >= pcntundefMax) ierr=1
      
      return
      
      end subroutine chkfld


      end module f77Output
