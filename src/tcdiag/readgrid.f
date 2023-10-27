      subroutine readgrid(lups,lupf,
     $     nvarsfc,nvarua,varsfc,varua,
     $     nx,ny,nlevs,nkcps,
     $     iplevs,rmiss,ierrc,
     $     u,v,t,rh,z,zcps,plevcps,
     $     us,vs,ts,rhs,ps,pr,prc,
     $     vrt850,zthklo,zthkhi,
     $     sst,sstall,ssta,ohc,tpw)
      

c-----7---------------------------------------------------------------72
c     fills in the model fields from the grid.
c
c     ierrc returns 1 if file not read in correctly
c
c-----7---------------------------------------------------------------72
c 

      implicit none
 
      integer, intent(in) :: lups,lupf
      integer, intent(in) :: nx, ny, nlevs, nkcps
      integer, dimension(nlevs), intent(in) :: iplevs
      real, intent(in) :: rmiss

      integer, intent(in) :: nvarsfc,nvarua

      character(len=10), dimension(nvarsfc), intent(in) :: varsfc
      character(len=10), dimension(nvarua), intent(in) :: varua

      integer, intent(out) :: ierrc
      real, dimension(nx,ny,nlevs), intent(inout) :: u,v,t,rh,z

      real, dimension(nx,ny,nkcps), intent(inout) :: zcps
      real, dimension(nkcps),       intent(inout) :: plevcps

      real, dimension(nx,ny),       intent(inout) :: us,vs,ts,rhs,ps,pr,prc,vrt850,zthklo,zthkhi
      real tss(nx,ny)
      real, dimension(nx,ny),       intent(inout) :: sst,sstall,ssta,ohc,tpw

      real, allocatable, dimension(:,:) :: dum
 
c     local variables

      integer :: i,j,k,n,m,nxtemp,nytemp,ierr,numfields,iplevcurr,iskip,istat
      logical verb

      character(len=80) :: ctemp, cfield


      allocate(dum(nx,ny),STAT=istat)

      iskip=8

      verb=.true.
      verb=.false.

      if(verb) then
        print*,'RRR ',nvarsfc,varsfc
        print*,'RRR ',nvarua,varua
      endif

      

c--       initialize error flags
c

      ierrc = 0
      ierr=0
      numfields=0


c--       read sst (w/ land mask); sstall (filled over land); ssta (sst anom)
c
      read(lups) sst
      read(lups) sstall
      read(lups) ssta

      sst=sst+273.15
      sstall=sstall+273.15

      if(verb) call qprntn(sst,'sst   ',1,1,nx,ny,iskip,6)


c--       read in sfc vars
c
      do i=1,nvarsfc

        if(verb) print*,'SSSS: ',i,varsfc(i)

        select case (varsfc(i))

c--       prw(tpw) -- precip h2o

        case ('prw')
        read(lupf) tpw
        if(verb) call qprntn(tpw,'prw   ',1,1,nx,ny,iskip,6)


c--       ohc

        case ('ohc')            !ohc
                                !ohc not currently available, this is placeholder
                                !will need to double-check accuracy if added in

        do m=1,ny
          do n=1,nx
            read(lupf,*) ohc(n,m)
            if ((ohc(n,m) .le. rmiss) .or. 
     +           (ohc(n,m) .ge. (-rmiss))) ohc(n,m) = rmiss
          enddo
        enddo

c--       uas(us) -- sfc u

        case ('uas')
        read(lupf) us
        if(verb) call qprntn(us,'uas   ',1,1,nx,ny,iskip,6)

c--       vas(vs) -- sfc v

        case ('vas')             !v: surface, iplevs
        read(lupf) vs
        if(verb) call qprntn(vs,'vas   ',1,1,nx,ny,iskip,6)

c--       ts(tss) -- model sfc t

        case ('tas')             !t: surface, iplevs
        read(lupf) ts
        if(verb) call qprntn(tss,'tss   ',1,1,nx,ny,iskip,6)

!         case ('tas')             !t: surface, iplevs
!         do m=1,ny
!           do n=1,nx
!             read(lupf,*) ts(n,m)
!             if ((ts(n,m) .le. rmiss) .or. 
!      +           (ts(n,m) .ge. (-rmiss))) ts(n,m) = rmiss
!           enddo
!         enddo

        case ('hurs')             !rh: surface, iplevs
        read(lupf) rhs
        if(verb) call qprntn(rhs,'rhs   ',1,1,nx,ny,iskip,6)

        case ('psl')
        read(lupf) ps
        if(verb) call qprntn(ps,'psl   ',1,1,nx,ny,iskip,6)

        case ('pr')
        read(lupf) pr
        if(verb) call qprntn(pr,'precip',1,1,nx,ny,iskip,6)

        case ('prc')
        read(lupf) prc
        if(verb) call qprntn(prc,'conv_pr',1,1,nx,ny,iskip,6)

c--       vrt850 -- relative 850 vort 10^-5 s^-10

        case ('vrt925')
        read(lupf) dum
        if(verb) call qprntn(dum,'vrt925',1,1,nx,ny,iskip,6)

        case ('vrt850')
        read(lupf) vrt850
        if(verb) call qprntn(vrt850,'vrt850',1,1,nx,ny,iskip,6)

        case ('vrt700')
        read(lupf) dum
        if(verb) call qprntn(dum,'vrt700',1,1,nx,ny,iskip,6)

c--       zthklo -- 900-600 thk

        case ('zthklo')
        read(lupf) zthklo
        if(verb) call qprntn(zthklo,'zthklo',1,1,nx,ny,iskip,6)

c--       zthkup -- 600-300 thk

        case ('zthkup')
        read(lupf) zthkhi
        if(verb) call qprntn(zthkhi,'zthkhi',1,1,nx,ny,iskip,6)

c--       z900
        case ('z900')
        read(lupf) dum
        if(verb) call qprntn(dum,'z900  ',1,1,nx,ny,iskip,6)
        plevcps(1)=900.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,1)

c--       z850
        case ('z850')
        read(lupf) dum
        if(verb) call qprntn(dum,'z850  ',1,1,nx,ny,iskip,6)
        plevcps(2)=850.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,2)

c--       z800
        case ('z800')
        read(lupf) dum
        if(verb) call qprntn(dum,'z800  ',1,1,nx,ny,iskip,6)
        plevcps(3)=800.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,3)

c--       z750
        case ('z750')
        read(lupf) dum
        if(verb) call qprntn(dum,'z750  ',1,1,nx,ny,iskip,6)
        plevcps(4)=750.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,4)

c--       z700
        case ('z700')
        read(lupf) dum
        if(verb) call qprntn(dum,'z700  ',1,1,nx,ny,iskip,6)
        plevcps(5)=700.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,5)

c--       z650
        case ('z650')
        read(lupf) dum
        if(verb) call qprntn(dum,'dum',1,1,nx,ny,iskip,6)
        plevcps(6)=650.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,6)

c--       z600
        case ('z600')
        read(lupf) dum
        if(verb) call qprntn(dum,'z600',1,1,nx,ny,iskip,6)
        plevcps(7)=600.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,7)

c--       z550
        case ('z550')
        read(lupf) dum
        if(verb) call qprntn(dum,'z550  ',1,1,nx,ny,iskip,6)
        plevcps(8)=550.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,8)

c--       z500
        case ('z500')
        read(lupf) dum
        if(verb) call qprntn(dum,'z500  ',1,1,nx,ny,iskip,6)
        plevcps(9)=500.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,9)

c--       z450
        case ('z450')
        read(lupf) dum
        if(verb) call qprntn(dum,'z450  ',1,1,nx,ny,iskip,6)
        plevcps(10)=450.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,10)
        
c--       z400
        case ('z400')
        read(lupf) dum
        if(verb) call qprntn(dum,'z400  ',1,1,nx,ny,iskip,6)
        plevcps(11)=400.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,11)

c--       z350
        case ('z350')
        read(lupf) dum
        if(verb) call qprntn(dum,'z350  ',1,1,nx,ny,iskip,6)
        plevcps(12)=350.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,12)

c--       z300
        case ('z300')
        read(lupf) dum
        if(verb) call qprntn(dum,'z300  ',1,1,nx,ny,iskip,6)
        plevcps(13)=300.0
        call load3dfrom2d(dum,zcps,nx,ny,nkcps,13)



        end select
        numfields=numfields+1

      enddo


c--       uuuuuuuuuuuuuuuuuuuuuuuuuuu read in UA vars; grads ordering
c

      do i=1,nvarua

        do k=1,nlevs
        

          select case (varua(i))

          case ('ua')           !u ua

          read(lupf) dum
          call load3dfrom2d(dum,u,nx,ny,nlevs,k)
          if(verb) print*,'ua plevs: ',iplevs(k)
          if(verb) call qprntn(u(1,1,k),'uaplev',1,1,nx,ny,iskip,6)
          numfields=numfields+1

          case ('va')           !v ua
          read(lupf) dum
          call load3dfrom2d(dum,v,nx,ny,nlevs,k)
          if(verb) print*,'va plevs: ',iplevs(k)
          if(verb) call qprntn(v(1,1,k),'vaplev',1,1,nx,ny,iskip,6)
          numfields=numfields+1
          
          case ('ta')           !t ua
          read(lupf) dum
          call load3dfrom2d(dum,t,nx,ny,nlevs,k)
          if(verb) print*,'ta plevs: ',iplevs(k)
          if(verb) call qprntn(t(1,1,k),'taplev',1,1,nx,ny,iskip,6)
          numfields=numfields+1
          
          case ('hur')          !rh ua
          read(lupf) dum
          call load3dfrom2d(dum,rh,nx,ny,nlevs,k)
          if(verb) print*,'hur plevs: ',iplevs(k)
          if(verb) call qprntn(rh(1,1,k),'rhplev',1,1,nx,ny,iskip,6)
          numfields=numfields+1
          
          case ('zg')           !z ua
          read(lupf) dum
          call load3dfrom2d(dum,z,nx,ny,nlevs,k)
          if(verb) print*,'zg plevs: ',iplevs(k)
          if(verb) call qprntn(z(1,1,k),'zgplev',1,1,nx,ny,iskip,6)
          numfields=numfields+1
          endselect

        enddo

      enddo

      if(verb) print*,'NNNNNN numfields: ',numfields
      
      return
 

      !read in fields one at a time, starting with 2-line header

  100 continue
      read(lupf,'(a80)',iostat=ierr) cfield
      if (ierr .ne. 0) go to 120
c      write(*,*) cfield
      if (cfield(1:6) .ne. 'field:') go to 1004
  110 continue
      read(lupf,'(a80)',iostat=ierr) ctemp
      if (ierr .ne. 0) go to 120
      if (ctemp(1:6) .eq. 'field:') then
         cfield = ctemp
         go to 110
      endif
      select case (cfield(7:8))
      case ('ss')   !sst
         do m=1,ny
            do n=1,nx
               read(lupf,*) sst(n,m)
               if ((sst(n,m) .le. rmiss) .or. 
     +            (sst(n,m) .ge. (-rmiss))) sst(n,m) = rmiss
               !check for land mask -- sst set to 0k (<1k should work)
               if (sst(n,m) .lt. 273.15) sst(n,m) = rmiss
c               if ((sst(n,m) .lt. 250.0) .and.
c     +            (sst(n,m) .gt. rmiss)) write (*,*) sst(n,m)
            enddo
         enddo
      case ('tp')   !tpw
         do m=1,ny
            do n=1,nx
               read(lupf,*) tpw(n,m)
               if ((tpw(n,m) .le. rmiss) .or. 
     +            (tpw(n,m) .ge. (-rmiss))) tpw(n,m) = rmiss
            enddo
         enddo
      case ('oh')   !ohc
         !ohc not currently available, this is placeholder
         !will need to double-check accuracy if added in
         do m=1,ny
            do n=1,nx
               read(lupf,*) ohc(n,m)
               if ((ohc(n,m) .le. rmiss) .or. 
     +            (ohc(n,m) .ge. (-rmiss))) ohc(n,m) = rmiss
            enddo
         enddo
      case ('u_')   !u: surface, iplevs
         if (cfield(9:12) .eq. 'surf') then
            do m=1,ny
               do n=1,nx
                  read(lupf,*) us(n,m)
                  if ((us(n,m) .le. rmiss) .or. 
     +               (us(n,m) .ge. (-rmiss))) us(n,m) = rmiss
               enddo
            enddo
         else
            read(cfield(9:12), '(i4.4)') iplevcurr
            do k=1,nlevs
               if (iplevs(k) .eq. iplevcurr) then
                  do m=1,ny
                     do n=1,nx
                        read(lupf,*) u(n,m,k)
                        if ((u(n,m,k) .le. rmiss) .or. 
     +                  (u(n,m,k) .ge. (-rmiss))) u(n,m,k) = rmiss
                     enddo
                  enddo
               endif
            enddo
         endif
      case ('v_')   !v: surface, iplevs
         if (cfield(9:12) .eq. 'surf') then
            do m=1,ny
               do n=1,nx
                  read(lupf,*) vs(n,m)
                  if ((vs(n,m) .le. rmiss) .or. 
     +               (vs(n,m) .ge. (-rmiss))) vs(n,m) = rmiss
               enddo
            enddo
         else
            read(cfield(9:12), '(i4.4)') iplevcurr
            do k=1,nlevs
               if (iplevs(k) .eq. iplevcurr) then
                  do m=1,ny
                     do n=1,nx
                        read(lupf,*) v(n,m,k)
                        if ((v(n,m,k) .le. rmiss) .or. 
     +                  (v(n,m,k) .ge. (-rmiss))) v(n,m,k) = rmiss
                     enddo
                  enddo
               endif
            enddo
         endif
      case ('t_')   !t: surface, iplevs
         if (cfield(9:12) .eq. 'surf') then
            do m=1,ny
               do n=1,nx
                  read(lupf,*) ts(n,m)
                  if ((ts(n,m) .le. rmiss) .or. 
     +               (ts(n,m) .ge. (-rmiss))) ts(n,m) = rmiss
               enddo
            enddo
         else
            read(cfield(9:12), '(i4.4)') iplevcurr
            do k=1,nlevs
               if (iplevs(k) .eq. iplevcurr) then
                  do m=1,ny
                     do n=1,nx
                        read(lupf,*) t(n,m,k)
                        if ((t(n,m,k) .le. rmiss) .or. 
     +                  (t(n,m,k) .ge. (-rmiss))) t(n,m,k) = rmiss
                     enddo
                  enddo
               endif
            enddo
         endif
      case ('r_')   !rh: surface, iplevs
         if (cfield(9:12) .eq. 'surf') then
            do m=1,ny
               do n=1,nx
                  read(lupf,*) rhs(n,m)
                  if ((rhs(n,m) .le. rmiss) .or. 
     +               (rhs(n,m) .ge. (-rmiss))) rhs(n,m) = rmiss
               enddo
            enddo
         else
            read(cfield(9:12), '(i4.4)') iplevcurr
            do k=1,nlevs
               if (iplevs(k) .eq. iplevcurr) then
                  do m=1,ny
                     do n=1,nx
                        read(lupf,*) rh(n,m,k)
                        if ((rh(n,m,k) .le. rmiss) .or. 
     +                  (rh(n,m,k) .ge. (-rmiss))) rh(n,m,k) = rmiss
                     enddo
                  enddo
               endif
            enddo
         endif
      case ('z_')
         read(cfield(9:12), '(i4.4)') iplevcurr
         do k=1,nlevs
            if (iplevs(k) .eq. iplevcurr) then
               do m=1,ny
                  do n=1,nx
                     read(lupf,*) z(n,m,k)
                     if ((z(n,m,k) .le. rmiss) .or. 
     +               (z(n,m,k) .ge. (-rmiss*1000.0))) z(n,m,k) = rmiss
                  enddo
               enddo
            endif
         enddo
      case ('p_')
         if (cfield(9:12) .eq. 'surf') then
            do m=1,ny
               do n=1,nx
                  read(lupf,*) ps(n,m)
                  if ((ps(n,m) .le. rmiss) .or. 
     +            (ps(n,m) .ge. (-rmiss*1000.0))) ps(n,m) = rmiss
               enddo
            enddo
         endif
      end select
      numfields=numfields+1
      go to 100
  120 continue



c      debugging option, see number of fields read in
c       note: will include fields that had no match in the select case
c             but will not include empty fields
      write(*,*) numfields

      deallocate(dum,STAT=istat)

 
      return
 
 1004 continue
      ierrc = 1
      write(*,*) 'grid field read failure'
      return
 
      end subroutine readgrid

      subroutine load3dfrom2d(u2,u3,ni,nj,nk,k)
      dimension u2(ni,nj),u3(ni,nj,nk)
      do i=1,ni
        do j=1,nj
          u3(i,j,k)=u2(i,j)
        enddo
      enddo
      return
      end subroutine load3dfrom2d


      subroutine load2dfrom3d(u3,u2,ni,nj,nk,k)
      dimension u2(ni,nj),u3(ni,nj,nk)
      do i=1,ni
        do j=1,nj
          u2(i,j)=u3(i,j,k)
        enddo
      enddo
      return
      end subroutine load2dfrom3d


