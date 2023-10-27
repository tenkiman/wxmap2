      module module_control

      implicit none

      save

      character(len =120) :: include_path   ='/data/amb/users/fiorino/w21/dat/geog/coastlines'

      namelist /DIAGnamelist/
     $     include_path


      contains  

      subroutine control(quiet_arg)

      logical,optional,intent(in)   :: quiet_arg
      
      open  (22, file="./TCDnamelist", status='old', action='read', err=70)
      read  (22, NML=DIAGnamelist, err=90)
      close (22)

      return

 70   print *,'control: error opening ./TCDnamelist'
      call flush(6)
      stop
      
 90   print *,'control: error reading one of the namelists in ./TCDnamelist'
      call flush(6)
      stop
      
      end subroutine control
      
      end module module_control


cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c         const -- physical, math 
      module const

        real, save ::  pi = 4. * atan(1.)
        real, save :: dtr = (4. * atan(1.))/180.0

        real, save :: dtk = 111.1949     ! Dist (km) over 1 deg lat
                           ! using erad=6371.0e+3
        real, save :: erad = 6371.0e+3   ! Earth's radius (m)
        real, save :: ecircum = 40030.2  ! Earth's circumference
                           ! (km) using erad=6371.e3
        real, save :: omega = 7.292e-5

        real, save :: rkm2nm=(60.0/111.1949)
        real, save :: rnm2km=(111.1949/60.0)

        real, save :: rearth=6371.0

        real, save :: rkt2ms
        real, save :: rms2kt

      contains

      subroutine initConst(ierr)
      ierr=0
      dtr =  pi/180.0
      rkm2nm=(60.0/dtk)
      rnm2km=(dtk/60.0)
      rkt2ms=1000.0/(rkm2nm*3600.0)
      rms2kt=1.0/rkt2ms

      return

      end subroutine initConst


      end module const

cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c         radPlevParamsGlobal -- radii plevs for diag vars -- global

      module radPlevParamsGlobal

      real, save :: sstMinDegC = 5.0

c         Parent grid or global grid specified, use default radii
c++       Inner and outer radii (km) for area average of model sounding (thermo variables)

      real, save :: r1st = 200.0
      real, save :: r2st = 800.0

c++       Inner and outer radii (km) for area average of model sounding (wind variables)
c         and precip user vars

      real, save :: r1sw =   0.0
      real, save :: r2sw = 500.0

c++       Maximum search radius (km) for vortex parameters,
c         min sfc pressure, max winds and radius of maximum wind.
c         (suggest 500 km for global models, 200 km for regional models)

      real, save :: srmax = 250.0

c++       radius for precip water (prw)
         
      real, save :: radtpw=200.0

c++       Maximum radius for SST (km) and OHC (km) area averages

      real, save :: ssmax = 50.0
      real, save :: somax = 50.0

c++       Pressure levels for vertical shear calculation

      real, save :: psbot = 850.0
      real, save :: pstop = 200.0

c++       Pressure and radius (km) for area averaged vorticity

      real, save :: pva = 850.0
      real, save :: rva = 1000.0

c++       Pressure and radius (km) for area averaged divergence

      real, save :: pda = 200.0
      real, save :: rda = 1000.0

c++       Pressure and radius (km) for averaging tangential wind

      real, save :: pta = 850.0
      real, save :: rta = 600.0

c++       Cylindrical grid parameters (r0, dr in km, dtheta (dt) in deg, +x axis is east)
c         nr,nt = number of radial and azimuthal grid intervals. 
c         Note: dr should be .le. model grid spacing, radial domain should extend to at
c         least 1000 km. 

      integer, parameter :: nt=36
      real,    save :: r0=0.0

C -- 20200404 -- this must be old...lsdiag is not capturing the vmax/rmax as well as the tracker         
C
C      integer, save :: nr=150
C      real,    save :: dr=10.0

C -- make dr 5 km
C
      integer, save :: nr=300
      real,    save :: dr=5.0

      real,    save :: dt=360.0/float(nt)

      end module radPlevParamsGlobal


cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c         radPlevParamsLimitedArea -- radii plevs for diag vars -- global

      module radPlevParamsLimitedArea

c         Parent grid or global grid specified, use default radii
c++       Inner and outer radii (km) for area average of model sounding (thermo variables)

      real, save :: r1st = 200.0
      real, save :: r2st = 800.0

c++       Inner and outer radii (km) for area average of model sounding (wind variables)

      real, save :: r1sw =   0.0
      real, save :: r2sw = 500.0

c++       Maximum search radius (km) for vortex parameters,
c         min sfc pressure, max winds and radius of maximum wind.
c         (suggest 500 km for global models, 200 km for regional models)

      real, save :: srmax = 200.0

c++       radius for precip water
         
      real, save :: radtpw=200.0

c++       Maximum radius for SST (km) and OHC (km) area averages

      real, save :: ssmax = 50.0
      real, save :: somax = 50.0

c++       Pressure levels for vertical shear calculation

      real, save :: psbot = 850.0
      real, save :: pstop = 200.0

c++       Pressure and radius (km) for area averaged vorticity

      real, save :: pva = 850.0
      real, save :: rva = 1000.0

c++       Pressure and radius (km) for area averaged divergence

      real, save :: pda = 200.0
      real, save :: rda = 1000.0

c++       Pressure and radius (km) for averaging tangential wind

      real, save :: pta = 850.0
      real, save :: rta = 600.0

c++       Cylindrical grid parameters (r0, dr in km, dtheta (dt) in deg, +x axis is east)
c         nr,nt = number of radial and azimuthal grid intervals. 
c         Note: dr should be .le. model grid spacing, radial domain should extend to at
c         least 1000 km. 

      integer, save :: nr=150
      integer, parameter :: nt=16
      real,    save :: r0=0.0
      real,    save :: dr=2.0
      real,    save :: dt=360.0/float(nt)


      end module radPlevParamsLimitedArea



cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c         f77OutputMeta -- field output metadata

      module f77OutputMeta

      integer, save :: 
     $     ni,nj,nk,nt,ntf,
     $     nvarsfc,nvarua,
     $     nlevs

      real,                              save :: blat,blon,elat,elon,dlat,dlon
      real,   allocatable, dimension(:), save :: xgrd,ygrd,coslatI

      character(len=128), allocatable, dimension(:) :: DataPaths

      character(len=10),  allocatable, dimension(:) :: varsfc,varua
      integer, allocatable, dimension(:) :: iplevs
      integer, allocatable, dimension(:) :: itaus
      real*4,  allocatable, dimension(:) :: plevs

      integer, parameter :: maxTau=240

      contains

      subroutine readFldMeta(metapath,ierr)

      use const

      real*4 clat,clon,cbearing

      integer*4 ios,pos,i,j,k,l,n,m

      character(len=512) :: metapath

      character(len=512) :: buffer
      logical verb

      verb=.true.
      verb=.false.

ccc      open( unit=1, file=metapath(1:ichlen(metapath,128)), form='formatted',action='read',err=812)
      open( unit=1, file=metapath, form='formatted',action='read',err=812)

      ios=0

      do while ( ios == 0 )

 5      continue
        read( 1, '(a)', iostat=ios ) buffer

        if(verb) print*,'buffer: ',buffer(1:128)
 
        if ( ios == 0 ) then

          pos = index(buffer, 'ni:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+4),'(I4)') ni
            if(verb) print*,'ni---------------------- ',pos,ni
              allocate(xgrd(ni),STAT=istat)
          end if

         pos = index(buffer, 'nj:')
          if ( index(buffer, 'nj:') .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+4),'(I4)') nj
            if(verb) print*,'nj---------------------- ',pos,nj
            allocate(ygrd(nj),STAT=istat)
            allocate(coslatI(nj),STAT=istat)
            goto 5
          end if

          pos = index(buffer, "lonW:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f6.2)') blon
            if(verb) print*,'blon---------------------- ',pos,blon
          end if


          pos = index(buffer, "lonE:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f6.2)') elon
            if(verb) print*,'elon---------------------- ',pos,elon
            goto 5
          end if

          pos = index(buffer, "latS:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+5),'(f5.2)') blat
            if(verb) print*,'blat---------------------- ',pos,blat
          end if

          pos = index(buffer, "latN:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+5),'(f5.2)') elat
            if(verb) print*,'elat---------------------- ',pos,elat
            goto 5
          end if

          pos = index(buffer, "dlon:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+5),'(f5.2)') dlon
            if(verb) print*,'dlon---------------------- ',pos,dlon
          end if

          pos = index(buffer, "dlat:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+5),'(f5.2)') dlat
            if(verb) print*,'dlat---------------------- ',pos,dlat
            goto 5
          end if

          pos = index(buffer, 'nk:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I10)') nk
            if(verb) print*,'nk---------------------- ',pos,nk

            if(nk > 0) then
              nlevs=nk
              allocate(iplevs(nlevs),STAT=istat)
              allocate(plevs(nlevs),STAT=istat)
              do i=1,nlevs
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:7),'(f7.2)') plevs(i)
                iplevs(i)=nint(plevs(i))
                if(verb) print*,'plevs---------------------- ',iplevs(i),plevs(i)
              enddo
            endif
            goto 5
          endif

          pos = index(buffer, 'nt:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I4)') nt
            if(verb) print*,'nt---------------------- ',pos,nt

            if(nt > 0) then
              allocate(itaus(nt),STAT=istat)
              allocate(DataPaths(0:maxTau),STAT=istat)
              do i=1,nt
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:3),'(i3,1x,a128)') itaus(i)
                read(buffer(5:128+5),'(a)') DataPaths(itaus(i))

                if(verb) print*,'itaus---------------------- ',itaus(i),DataPaths(itaus(i))
              enddo

            endif
            goto 5
          endif

          pos = index(buffer, 'ntf:')
          if ( pos .ne. 0 ) then
            pos=pos+5
            read(buffer(pos:pos+3),'(I4)') ntf
            if(verb) print*,'ntf--------------------- ',pos,ntf

            if(nt > 0) then
              allocate(itaus(nt),STAT=istat)
              do i=1,nt
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:3),'(i3)') itaus(i)
                if(verb) print*,'itaus---------------------- ',itaus(i)
              enddo
            endif
            goto 5
          endif

          pos = index(buffer, 'nvarsSfc:')
          if ( pos .ne. 0 ) then
            pos=pos+9
            read(buffer(pos:pos+3),'(I10)') nvarsfc
            if(verb) print*,'nvarssfc---------------------- ',pos,nvarsfc

            pos = index(buffer, 'nvarsUA:')
            if ( pos .ne. 0 ) then
              pos=pos+9
              read(buffer(pos:pos+3),'(I10)') nvarua
              if(verb) print*,'nvarua ---------------------- ',pos,nvarua
            endif

c--       parse out the sfc and ua variable names
c
            if(nvarsfc > 0) then
              allocate(varsfc(nvarsfc),STAT=istat)
              do i=1,nvarsfc
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:10),'(a)') varsfc(i)
                if(verb) print*,'varsfc---------------------- ',varsfc(i)
              enddo
            endif

            if(nvarua > 0) then
              allocate(varua(nvarua),STAT=istat)
              do i=1,nvarua
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:10),'(a)') varua(i)
                if(verb) print*,'varua---------------------- ',varua(i)
              enddo
            endif

            goto 5

          end if

          pos = index(buffer, "lonC:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f6.2)') clon
            if(verb) print*,'clon---------------------- ',pos,clon
          end if

          pos = index(buffer, "latC:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f6.2)') clat
            if(verb) print*,'clat---------------------- ',pos,clat
          end if

          pos = index(buffer, "bearingC:")
          if ( pos .ne. 0 ) then
            pos=pos+10
            read(buffer(pos:pos+6),'(f6.2)') cbearing
            if(verb) print*,'cbearing---------------------- ',pos,cbearing
            goto 5
          end if

        end if

      end do


C--       define the grid; now from input
C
      do i=1,ni
        xgrd(i)=blon+dlon*(i-1)
      end do
      
      do j=1,nj
        ygrd(j)=blat+dlat*(j-1)
        clat=cos(ygrd(j)*dtr)
        coslatI(j)=1.0
        if(clat.ge.0.001) coslatI(j)=1.0/clat
      end do
      

      ierr=0
      return

 812  continue

      print*,'error opening input field file'
      print*,metapath
      ierr=1
      return

 814  continue
      print*,'error in allocate...readFldMeta'
      ierr=1
      return

      end subroutine readFldMeta



      function ichlen(c,imax)
      character c
      iend=-1
      ii=1
      do while (iend.eq.-1.and.ii.le.imax)
        if(c(ii).eq.' ') iend=ii
        ii=ii+1
      end do  
      if(ii.gt.imax) then
        ichlen=imax
      else
        ichlen=iend-1
      end if
      return
      end function ichlen

      end module f77OutputMeta


cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c         tcTrkMeta -- tc track metadata

      module tcTrkMeta

      integer, save :: ntauTC

      real,      allocatable, dimension(:), save :: clatTC,clonTC,cvmxTc,cpmnTc,cdirTC,cspdTC
      integer,   allocatable, dimension(:), save :: tausTC

      character(len=6),  save :: modelTC
      character(len=4),  save :: stm4idTC
      character(len=9),  save :: stmNameTC
      character(len=10), save :: dtgTC


      contains

      subroutine readTctrkMeta(metapath,ierr)


      character(len=512) :: metapath
      character(len=512) :: buffer

      integer pos,ios

      logical verb

      verb=.true.
      verb=.false.

      open( unit=1, file=metapath, form='formatted',action='read',err=812)

      ios=0
      ncards=0
      do while ( ios == 0 )

 5      continue
        read( 1, '(a)', iostat=ios ) buffer
        ncards=ncards+1
        if(ncards == 1) then
                                !ecm2   2011092300 09e.2011 ep09.2011 HILARY  
                                !123456789|123456789|123456789|123456789|123456789|

ccc          print*,'buffer: ',buffer(1:128)
          read(buffer( 1: 6),  '(a6)') modelTC
          read(buffer( 8:17), '(a10)') dtgTC
          read(buffer(28:31),  '(a4)') stm4idTC
          read(buffer(38:46),  '(a9)') stmNameTC
          print*,'model,dtg,stm4id,stmNameTC:',modelTC,' ',dtgTC,' ',stm4idTC,' ',stmNameTC

        endif

        if(verb) print*,'buffer: ',buffer(1:128)
 
        if ( ios == 0 ) then

          pos = index(buffer, 'nt:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I4)') ntauTC
            if(verb) print*,'nt---------------------- ',pos,ntauTC

            if(ntauTC > 0) then
              allocate(tausTC(ntauTC),STAT=istat)
              allocate(cvmxTC(ntauTC),STAT=istat)
              allocate(cpmnTC(ntauTC),STAT=istat)
              allocate(clatTC(ntauTC),STAT=istat)
              allocate(clonTC(ntauTC),STAT=istat)
              allocate(cdirTC(ntauTC),STAT=istat)
              allocate(cspdTC(ntauTC),STAT=istat)

              do i=1,ntauTC
C  0  13.9  310.7  37 284 12.0
C123456789|123456789|123456789|
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:3),'(i3,1x,a128)') tausTC(i)
                read(buffer(5:9),'(f5.1)') clatTC(i)
                read(buffer(11:16),'(f6.1)') clonTC(i)
                read(buffer(18:20),'(f3.0)') cvmxTC(i)
                read(buffer(22:25),'(f4.0)') cpmnTC(i)
                read(buffer(27:29),'(f3.0)') cdirTC(i)
                read(buffer(31:34),'(f4.1)') cspdTC(i)

                if(verb) print*,'posit---------------------- ',tausTC(i),clatTC(i),clonTC(i),cvmxTC(i),cpmnTC(i),cdirTC(i),cspdTC(i)
              enddo

            endif
            goto 5
          endif

        end if

      end do

      ierr=0
      return

 812  continue

      print*,'EEE error opening input TCmeta file: ',metapath
      ierr=1
      return

 814  continue
      print*,'error in allocate...readTctrkMeta'
      ierr=2
      return

      end subroutine readTctrkMeta

      end module tcTrkMeta

cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c         tcTrkDiag -- tc track diagnostic arrays and labels

      module tcTrkDiag

      integer, parameter :: nstmDiag=16
      integer, parameter :: nuserDiag=18
      integer, parameter :: nsfcDiag=5
      integer, parameter :: nuaDiag=5
      integer, save      :: nvaru
      integer, save      :: nvarut

c200DVRG    (/S)
c123456789012345

      character*16, dimension(nstmDiag),   save :: stmDiagLabels
      character*16, dimension(nuaDiag,2),  save :: baseuaDiagLabels
      character*16, dimension(nuserDiag),  save :: userDiagLabels
      character*16, dimension(nsfcDiag),   save :: sfcDiagLabels
      character*16, allocatable, dimension(:),   save :: uaDiagLabels

      real,         allocatable, dimension(:,:), save :: stmDiagVars
      real,         allocatable, dimension(:,:), save :: userDiagVars
      real,         allocatable, dimension(:,:), save :: sfcDiagVars

      integer,      allocatable, dimension(:,:), save :: istmDiagVars
      integer,      allocatable, dimension(:,:), save :: iuserDiagVars
      integer,      allocatable, dimension(:,:), save :: isfcDiagVars

      real,         allocatable, dimension(:,:,:), save :: uaDiagVars
      integer,      allocatable, dimension(:,:,:), save :: iuaDiagVars

      integer,      allocatable, dimension(:), save :: allTaus

      real,              allocatable, dimension(:), save :: udiagvar,udiagvart
      integer,           allocatable, dimension(:), save :: iudiagvar
      character(len=50), allocatable, dimension(:), save :: udiaglab


      contains

      subroutine setTrkDiag(plevs,nlevs,ntaus)

      real plevs(nlevs)

      stmDiagLabels( 1)  = 'LATITUDE   (DEG)'
      stmDiagLabels( 2)  = 'LONGITUDE  (DEG)'
      stmDiagLabels( 3)  = 'MAX WIND    (KT)'
      stmDiagLabels( 4)  = 'RMW         (KM)'    
      stmDiagLabels( 5)  = 'MIN SLP     (MB)'
      stmDiagLabels( 6)  = 'SHR MAG     (KT)'
      stmDiagLabels( 7)  = 'SHR DIR    (DEG)'
      stmDiagLabels( 8)  = 'STM SPD     (KT)'
      stmDiagLabels( 9)  = 'STM HDG    (DEG)'
      stmDiagLabels(10)  = 'SST        (10C)'
      stmDiagLabels(11)  = 'OHC     (KJ/CM2)'
      stmDiagLabels(12)  = 'TPW         (MM)'
      stmDiagLabels(13)  = 'LAND        (KM)'
      stmDiagLabels(14)  = '850TANG  (10M/S)'
      stmDiagLabels(15)  = '850VORT     (/S)'
      stmDiagLabels(16)  = '200DVRG     (/S)'

      n=1
      userDiagLabels( n) = 'ADECK  VMAX (KT)' ; n=n+1
      userDiagLabels( n) = 'DIAG   VMAX (KT)' ; n=n+1
      userDiagLabels( n) = 'ADECK  PMIN (MB)' ; n=n+1
      userDiagLabels( n) = 'DIAG   PMIN (MB)' ; n=n+1
      userDiagLabels( n) = 'SSTANOM    (10C)' ; n=n+1
      userDiagLabels( n) = 'PRECIP    (MM/D)' ; n=n+1
      userDiagLabels( n) = 'PR  ASYM/TOT (%)' ; n=n+1
      userDiagLabels( n) = 'TOTSHR MAG  (KT)' ; n=n+1
      userDiagLabels( n) = 'SHR/TOTSHR   (%)' ; n=n+1
      userDiagLabels( n) = 'SHR ASYM/TOT (%)' ; n=n+1
      userDiagLabels( n) = 'CPS  B(AROCLINC)' ; n=n+1
      userDiagLabels( n) = 'CPS   VTHERM(LO)' ; n=n+1
      userDiagLabels( n) = 'CPS   VTHERM(HI)' ; n=n+1
      userDiagLabels( n) = 'POCI        (MB)' ; n=n+1
      userDiagLabels( n) = 'ROCI        (KM)' ; n=n+1
      userDiagLabels( n) = 'R34mean     (KM)' ; n=n+1
      userDiagLabels( n) = 'R50mean     (KM)' ; n=n+1
      userDiagLabels( n) = 'R64mean     (KM)' ; n=n+1

      nvaru=nuserDiag      
      nvarut=nuserDiag      

      baseuaDiagLabels( 1,1) = 'T_'
      baseuaDiagLabels( 1,2) = '     (10C)'
      baseuaDiagLabels( 2,1) = 'R_'
      baseuaDiagLabels( 2,2) = '       (%)'
      baseuaDiagLabels( 3,1) = 'Z_'
      baseuaDiagLabels( 3,2) = '      (DM)'
      baseuaDiagLabels( 4,1) = 'U_'
      baseuaDiagLabels( 4,2) = '    (10KT)'
      baseuaDiagLabels( 5,1) = 'V_'
      baseuaDiagLabels( 5,2) = '    (10KT)'

      nuaDiagLabels=nlevs*nuaDiag

      allocate(uaDiagLabels(nuaDiagLabels),STAT=istat)

      allocate(stmDiagVars(nstmDiag,ntaus),STAT=istat)
      allocate(istmDiagVars(nstmDiag,ntaus),STAT=istat)

      allocate(uaDiagVars(nuaDiag,nlevs,ntaus),STAT=istat)
      allocate(iuaDiagVars(nuaDiag,nlevs,ntaus),STAT=istat)

      allocate(userDiagVars(nuserDiag,ntaus),STAT=istat)
      allocate(iuserDiagVars(nuserDiag,ntaus),STAT=istat)

      allocate(udiagvar(nuserDiag),STAT=istat)
      allocate(udiagvart(nuserDiag),STAT=istat)
      allocate(iudiagvar(nuserDiag),STAT=istat)
      allocate(udiaglab(nuserDiag),STAT=istat)

      allocate(sfcDiagVars(nsfcDiag,ntaus),STAT=istat)
      allocate(isfcDiagVars(nsfcDiag,ntaus),STAT=istat)
      allocate(allTaus(ntaus),STAT=istat)

      sfcDiagLabels( 1)  = 'T_SURF     (10C)'
      sfcDiagLabels( 2)  = 'R_SURF       (%)'
      sfcDiagLabels( 3)  = 'P_SURF      (MB)'
      sfcDiagLabels( 4)  = 'U_SURF      (KT)'    
      sfcDiagLabels( 5)  = 'V_SURF      (KT)'

      j=1
      do k=1,nlevs
        do i=1,nuaDiag
          write(uaDiagLabels(j), "(a2,i4.4,a10)") baseuaDiagLabels(i,1),int(plevs(k)),baseuaDiagLabels(i,2)
          j=j+1
        enddo
      enddo

      return

      end subroutine  setTrkDiag


      subroutine loadTrkDiag(itau,curtau,
     $     rmiss,imissd,
     $     nvar,diagvar,idiagvar,
     $     nvaru,udiagvar,iudiagvar,
     $     usfc,vsfc,tsfc,rhsfc,psfc,
     $     nlevs,usnd,vsnd,tsnd,rhsnd,zsnd)


      real*4, intent(in) :: rmiss
      integer, intent(in) :: itau,imissd,curtau

      integer, intent(in) :: nvar
      real*4, dimension(nvar), intent(in) :: diagvar
      integer, dimension(nvar), intent(inout) :: idiagvar

      integer, intent(in) :: nvaru
      real*4, dimension(nvaru), intent(in) :: udiagvar
      integer, dimension(nvaru), intent(inout) :: iudiagvar

      real*4, intent(in) :: usfc,vsfc,tsfc,rhsfc,psfc

      integer, intent(in) :: nlevs
      real*4, dimension(nlevs), intent(in) :: usnd, vsnd, tsnd, rhsnd, zsnd
      integer :: iusnd, ivsnd, itsnd, irhsnd, izsnd

      logical :: verb
      

      verb=.true.
      verb=.false.

      if(nvar .ne. nstmDiag .or.
     $     nvaru .ne. nuserDiag ) then
        print*,'EEE nvar        != nstmDiag or nvaru != nuserDiag'
        stop 'loadTrkDiag'
      endif

      
c--       set current tau
c         
      allTaus(itau)=curtau


c--       storm vars
c
      do n=1,nvar
        idiagvar(n)=nint(diagvar(n))
        if (diagvar(n) .le. rmiss) idiagvar(n)=imissd
        if (n .eq. 1) idiagvar(n)=nint(diagvar(n)*10.0)
        if (n .eq. 2) idiagvar(n)=nint(diagvar(n)*10.0)
      enddo
      
      do  n=1,nvar
        stmDiagVars(n,itau)=diagvar(n)
        istmDiagVars(n,itau)=idiagvar(n)
        if(verb) print*,stmDiagLabels(n),istmDiagVars(n,itau),stmDiagVars(n,itau)
      enddo
      
c--       user vars
c
      do n=1,nvaru
        iudiagvar(n)=nint(udiagvar(n))
        if (udiagvar(n) .le. rmiss) iudiagvar(n)=imissd
      enddo

      do n=1,nvaru
        userDiagVars(n,itau)=udiagvar(n)
        iuserDiagVars(n,itau)=iudiagvar(n)
        if(verb) print*,userDiagLabels(n),iuserDiagVars(n,itau),userDiagVars(n,itau)
      enddo


c--       sounding -- sfc & upper air
c--       sfc vars
c

      if (tsfc .le. rmiss) then
        otsfc=imissd
      else
        otsfc=nint((tsfc-273.15)*10.0)
      endif

      if (rhsfc .le. rmiss) then
        orhsfc=imissd
      else
        orhsfc=nint(rhsfc)
      endif

      if (psfc .le. rmiss) then
        opsfc=imissd
      else
        if(psfc.gt.10000.0) then
          opsfc=nint(psfc/100.0)
        else
          opsfc=nint(psfc)
        endif
      endif

      if (usfc .le. rmiss) then
        ousfc=imissd
      else
        ousfc=nint(usfc*10.0)
      endif

      if (vsfc .le. rmiss) then
        ovsfc=imissd
      else
        ovsfc=nint(vsfc*10.0)
      endif
      
      sfcDiagVars(1,itau)=tsfc
      isfcDiagVars(1,itau)=otsfc

      sfcDiagVars(2,itau)=rhsfc
      isfcDiagVars(2,itau)=orhsfc

      sfcDiagVars(3,itau)=psfc
      isfcDiagVars(3,itau)=opsfc

      sfcDiagVars(4,itau)=usfc
      isfcDiagVars(4,itau)=ousfc

      sfcDiagVars(5,itau)=vsfc
      isfcDiagVars(5,itau)=ovsfc


      j=1
      do k=1,nlevs
        do i=1,nuaDiag

          if (tsnd(k) .le. rmiss) then
            itsnd=imissd
          else
            itsnd=nint((tsnd(k)-273.15)*10.0)
          endif
          
          if (rhsnd(k) .le. rmiss) then
            irhsnd=imissd
          else
            irhsnd=nint(rhsnd(k))
          endif
          
          if (zsnd(k) .le. rmiss) then
            izsnd=imissd
          else
            izsnd=nint(zsnd(k)/10.0)
          endif
          
          if (usnd(k) .le. rmiss) then
            iusnd=imissd
          else
            iusnd=nint(usnd(k)*10.0)
          endif
          
          if (vsnd(k) .le. rmiss) then
            ivsnd=imissd
          else
            ivsnd=nint(vsnd(k)*10.0)
          endif
          
          if(verb) then
            if(i.eq.1)  print*, uaDiagLabels(j),itsnd,tsnd(k)
            if(i.eq.2)  print*, uaDiagLabels(j),irhsnd,rhsnd(k)
            if(i.eq.3)  print*, uaDiagLabels(j),izsnd,zsnd(k)
            if(i.eq.4)  print*, uaDiagLabels(j),iusnd,usnd(k)
            if(i.eq.5)  print*, uaDiagLabels(j),ivsnd,vsnd(k)
          endif

          if(i.eq.1) uaDiagVars(i,k,itau)=tsnd(k)
          if(i.eq.2) uaDiagVars(i,k,itau)=rhsnd(k)
          if(i.eq.3) uaDiagVars(i,k,itau)=zsnd(k)
          if(i.eq.4) uaDiagVars(i,k,itau)=usnd(k)
          if(i.eq.5) uaDiagVars(i,k,itau)=vsnd(k)

          if(i.eq.1) iuaDiagVars(i,k,itau)=itsnd
          if(i.eq.2) iuaDiagVars(i,k,itau)=irhsnd
          if(i.eq.3) iuaDiagVars(i,k,itau)=izsnd
          if(i.eq.4) iuaDiagVars(i,k,itau)=iusnd
          if(i.eq.5) iuaDiagVars(i,k,itau)=ivsnd

          j=j+1
        enddo
      enddo

      end subroutine  loadTrkDiag

      subroutine makeDiagCards(ntaus,ludf)

      use tcTrkMeta
      use f77OutputMeta

      integer ludf

      character(len=512) card


                                !               *   HWRF  2010090306   *
                                !123456789|123456789|123456789|123456789|
                                !               *   AL07  EARL         *

      
      write(card,'(512a1)') ' '
      write(card,'(a,a6,2x,a10,a)') '               *   ',modelTC,dtgTC,'   *'
      write(ludf,'(a)') card(1:41)

      write(card,'(512a1)') ' '
      write(card,'(a,a4,4x,a9,a)') '               *   ',stm4idTC,stmNameTC,'    *'
      write(ludf,'(a)') card(1:41)

      write(card,'(512a1)') ' '
      write(ludf,'(a)') card(1:128)

      write(card,'(512a1)') ' '
      write(card,'(a,a,a)') '                ------------------------------------------------------',
     $     '     STORM DATA     ','----------------------------------------------------------'
      write(ludf,'(a)') card(1:128)

c         NTIME 022
c         123456789

      write(card(1:9),'(a,i3.3)') 'NTIME ',ntaus
      write(ludf,'(a)') card(1:9)

      write(card,'(512a1)') ' '
      write(card(1:16),'(a16)') 'TIME        (HR)'
      il=6
      ib=17
      do l=1,ntaus
        ie=ib+il
        write(card(ib:ie),'(i6)') allTaus(l)
        ib=ib+il
      enddo
      write(ludf,'(a)') card(1:ie)


      do n=1,nstmDiag
        
        write(card(1:16),'(a16)') stmDiagLabels(n)

        il=6
        ib=17
        do l=1,ntaus
          ie=ib+il
          if(n .le. 2) then
            write(card(ib:ie),'(f6.1)') stmDiagVars(n,l)
          else
            write(card(ib:ie),'(i6)') istmDiagVars(n,l)
          endif

          ib=ib+il
        enddo

        write(ludf,'(a)') card(1:ie)

      enddo

      write(card,'(512a1)') ' '
      write(ludf,'(a)') card(1:128)

      write(card,'(512a1)') ' '
      write(card,'(a,a,a)') '                ------------------------------------------------------',
     $     '     CUSTOM DATA     ','----------------------------------------------------------'
      write(ludf,'(a)') card(1:128)

      write(card(1:9),'(a,i3.3)') 'NVAR ',nuserDiag
      write(ludf,'(a)') card(1:9)

      write(card,'(512a1)') ' '
      write(card(1:16),'(a16)') 'TIME        (HR)'
      il=6
      ib=17
      do l=1,ntaus
        ie=ib+il
        write(card(ib:ie),'(i6)') allTaus(l)
        ib=ib+il
      enddo
      write(ludf,'(a)') card(1:ie)


      do n=1,nuserDiag
        
        write(card(1:16),'(a16)') userDiagLabels(n)

        il=6
        ib=17
        do l=1,ntaus
          ie=ib+il
          write(card(ib:ie),'(i6)') iuserDiagVars(n,l)
          ib=ib+il
        enddo

        write(ludf,'(a)') card(1:ie)

      enddo


      write(card,'(512a1)') ' '
      write(ludf,'(a)') card(1:128)

      write(card,'(512a1)') ' '
      write(card,'(a,a,a)') '                ------------------------------------------------------',
     $     '     SOUNDING DATA     ','----------------------------------------------------------'
      write(ludf,'(a)') card(1:128)

      write(card,'(512a1)') ' '
      write(card(1:9),'(a,i3.3)') 'NLEVS ',nlevs+1
      ib=11
      il=5
      do l=1,nlevs+1
        ie=ib+il

        if(l == 1) then
          write(card(ib:ie),'(1x,a)') 'SURF'
        else
          write(card(ib:ie),'(1x,i4.4)') int(plevs(l-1))
        endif
        ib=ib+il
      enddo
      write(ludf,'(a)') card(1:ie)

      write(card,'(512a1)') ' '
      write(card(1:16),'(a16)') 'TIME        (HR)'
      il=6
      ib=17
      do l=1,ntaus
        ie=ib+il
        write(card(ib:ie),'(i6)') allTaus(l)
        ib=ib+il
      enddo
      write(ludf,'(a)') card(1:ie)

      do n=1,nsfcDiag
        
        write(card(1:16),'(a16)') sfcDiagLabels(n)

        il=6
        ib=17
        do l=1,ntaus
          ie=ib+il
          write(card(ib:ie),'(i6)') isfcDiagVars(n,l)
          ib=ib+il
        enddo

        write(ludf,'(a)') card(1:ie)

      enddo

      j=1
      do k=1,nlevs
        do n=1,nuaDiag
          write(card(1:16),'(a16)') uaDiagLabels(j)

          il=6
          ib=17
          do l=1,ntaus
            ie=ib+il
            write(card(ib:ie),'(i6)') iuaDiagVars(n,k,l)
            ib=ib+il
          enddo
          
          write(ludf,'(a)') card(1:ie)

          j=j+1

        enddo
      enddo

      return

      end subroutine makeDiagCards


      end module tcTrkDiag


      
