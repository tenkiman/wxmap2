      program lsdiagdriver

      use module_control     
      use f77OutputMeta
      use tcTrkMeta
      use tcTrkDiag

      implicit none

      logical verb

      integer*4 :: ios,pos,i,j,k,l,n,m,
     $     mx,my,mp,nx,ny,np,
     $     nargs,
     $     lups,lupf,ludf

      real*4 :: 
     $     clat,clon,cbearing,cspeed

      real*4, parameter :: rmiss = -1e20

      integer :: ierr,ierrc, istat, irepos, inest, inestuse
      integer :: nxp, nyp, nxn, nyn
      integer :: ilatc, ilonc, ivmax, ipmin

      integer :: itau
      
      integer, parameter :: imiss = -9999, imissd = 9999
      integer, parameter :: ms = 16

      real*4 :: usfc=rmiss, vsfc=rmiss, tsfc=rmiss
      real*4 :: rhsfc=rmiss, psfc=rmiss
      real*4 :: usfct=rmiss, vsfct=rmiss, tsfct=rmiss
      real*4 :: rhsfct=rmiss, psfct=rmiss
      integer :: nvart,nkcps
      real*4 :: otsfc,orhsfc,opsfc,ousfc,ovsfc

 
c--       Variables for storm data section
c
      integer, parameter :: nvar=16
      real*4, dimension(nvar) :: diagvar = rmiss, diagvart = rmiss
      integer, dimension(nvar) :: idiagvar = imissd
      character(len=50), dimension(nvar)  :: diaglab

c--       forced to set here and in mf.modules.f
c

      character qtitle*24
 
c--       allocatable sounding arrays
c         

c         in f77OutputMeta
c      character(len=10),  allocatable, dimension(:) :: varsfc,varua
c      integer, allocatable, dimension(:) :: iplevs
c      integer, allocatable, dimension(:) :: itaus
c         real*4, allocatable, dimension(:) :: plevs

      real*4, allocatable, dimension(:) :: usnd, vsnd
      real*4, allocatable, dimension(:) :: tsnd, zsnd, rhsnd
      real*4, allocatable, dimension(:) :: usndt, vsndt
      real*4, allocatable, dimension(:) :: tsndt, zsndt, rhsndt
 
c--       start the allocatable arrays for the parent grid
c

      real*4, allocatable, dimension(:) :: rlat, rlon

!  varsfc---------------------- uas       
!  varsfc---------------------- vas       
!  varsfc---------------------- psl       
!  varsfc---------------------- prw       
!  varsfc---------------------- pr        
!  varsfc---------------------- prc
!  varsfc---------------------- vrt925    
!  varsfc---------------------- vrt850    
!  varsfc---------------------- vrt700    
!  varsfc---------------------- zthklo    
!  varsfc---------------------- zthkup    
!  varsfc---------------------- z900      
!  varsfc---------------------- z850      
!  varsfc---------------------- z800      
!  varsfc---------------------- z750      
!  varsfc---------------------- z700      
!  varsfc---------------------- z650      
!  varsfc---------------------- z600      
!  varsfc---------------------- z550      
!  varsfc---------------------- z500      
!  varsfc---------------------- z450      
!  varsfc---------------------- z400      
!  varsfc---------------------- z350      
!  varsfc---------------------- z300      


      real*4, allocatable, dimension(:,:) :: us,vs,ts,rhs,ps
      real*4, allocatable, dimension(:,:) :: vrt850,zthklo,zthkhi
      real*4, allocatable, dimension(:,:) :: sst,sstall,sstanom,ohc,tpw

c--       extras
      real*4, allocatable, dimension(:,:) :: vrt925,vrt700,pr,prc


      real*4, allocatable, dimension(:,:,:) :: u, v, t, rh, z
      real*4, allocatable, dimension(:) :: plevcps

      real*4, allocatable, dimension(:,:,:) :: zcps

 
c--       set up additional allocatable arrays for the nested grid
c
      real*4, allocatable, dimension(:) :: rlatn, rlonn
      real*4, allocatable, dimension(:,:) :: usn, vsn, tsn, rhsn, psn
      real*4, allocatable, dimension(:,:) :: sstn, ohcn, tpwn
      real*4, allocatable, dimension(:,:,:) :: un, vn, tn, rhn, zn

      real*4, allocatable, dimension(:,:) :: dum

      character(len=512) :: metapath,trkmetapath,sstpath,outpath


c--       get the include path
c         
      call control()
c--       ssssssssssssssssssssssssssssssssssssssssssssssssss
c         
      verb=.true.
ccc      verb=.false.

      lups=2
      lupf=3
      ludf=11

      nkcps=13

      diaglab( 1) = 'LATITUDE  (DEG)'
      diaglab( 2) = 'LONGITUDE (DEG)'
      diaglab( 3) = 'MAX WIND   (KT)'
      diaglab( 4) = 'RMW        (KM)'    
      diaglab( 5) = 'MIN SLP    (MB)'
      diaglab( 6) = 'SHR MAG    (KT)'
      diaglab( 7) = 'SHR DIR   (DEG)'
      diaglab( 8) = 'STM SPD    (KT)'
      diaglab( 9) = 'STM HDG   (DEG)'
      diaglab(10) = 'SST       (10C)'
      diaglab(11) = 'OHC    (KJ/CM2)'
      diaglab(12) = 'TPW        (MM)'
      diaglab(13) = 'LAND       (KM)'
      diaglab(14) = '850TANG (10M/S)'
      diaglab(15) = '850VORT    (/S)'
      diaglab(15) = '200DVRG    (/S)'

      ios = 0
      nargs = iargc()
      
      if ( nargs .ne. 4 ) then
        write(*,*) "lsdiag.x run with 4 command line args:"
        write(*,*)
        write(*,*) "1)   metapath -- metapath with grid/var fields meta data"
        write(*,*) "2) trkmetpath -- tc track including dir/spd of motion"
        write(*,*) "3)    sstpath -- oisst field"
        write(*,*) "4)    outpath -- txt output"
        write(*,*) "e.g., lsdiag.x mftrk/meta.txt mftrk/sst.dat mftrk/meteo.f000.dat mftrk/test.out"
        stop 'set 4 command lines args'
      else
        call getarg( 1, metapath )
        call getarg( 2, trkmetapath )
        call getarg( 3, sstpath )
        call getarg( 4, outpath  )
      end if

      call readFldMeta(metapath,ierr)
cc      if(verb) print*,'ierr=',ierr,' readFldMeta'
      if(ierr > 0) stop 'readFldMeta'

      call readTctrkMeta(trkmetapath,ierr)
cc      if(verb) print*,'ierr=',ierr,' readTctrkMeta'
      if(ierr > 0) stop 'readTctrkdMeta'

      nxp=ni
      nyp=nj
      nlevs=nk

c--       allocate and initialize sounding arrays
c         

      allocate(usnd(nlevs),STAT=istat)
      allocate(vsnd(nlevs),STAT=istat)
      allocate(tsnd(nlevs),STAT=istat)
      allocate(zsnd(nlevs),STAT=istat)
      allocate(rhsnd(nlevs),STAT=istat)

      allocate(usndt(nlevs),STAT=istat)
      allocate(vsndt(nlevs),STAT=istat)
      allocate(tsndt(nlevs),STAT=istat)
      allocate(zsndt(nlevs),STAT=istat)
      allocate(rhsndt(nlevs),STAT=istat)

      usnd=rmiss
      vsnd=rmiss
      tsnd=rmiss
      zsnd=rmiss
      rhsnd=rmiss
      usndt=rmiss
      vsndt=rmiss
      tsndt=rmiss
      zsndt=rmiss
      rhsndt=rmiss

      !allocate and calculate rlat, rlon
      allocate(rlat(nyp),STAT=istat)
      allocate(rlon(nxp),STAT=istat)
      rlat=rmiss
      rlon=rmiss

c--       222222222222222222222222222222D grids

      allocate(us(nxp,nyp),STAT=istat)
      allocate(vrt850(nxp,nyp),STAT=istat)
      allocate(zthklo(nxp,nyp),STAT=istat)
      allocate(zthkhi(nxp,nyp),STAT=istat)
      allocate(vs(nxp,nyp),STAT=istat)
      allocate(ts(nxp,nyp),STAT=istat)
      allocate(rhs(nxp,nyp),STAT=istat)
      allocate(ps(nxp,nyp),STAT=istat)
      allocate(pr(nxp,nyp),STAT=istat)
      allocate(prc(nxp,nyp),STAT=istat)
      allocate(sst(nxp,nyp),STAT=istat)
      allocate(sstall(nxp,nyp),STAT=istat)
      allocate(sstanom(nxp,nyp),STAT=istat)
      allocate(ohc(nxp,nyp),STAT=istat)
      allocate(tpw(nxp,nyp),STAT=istat)

c--       dummy
      allocate(dum(nxp,nyp),STAT=istat)

c--       extras
      allocate(vrt925(nxp,nyp),STAT=istat)
      allocate(vrt700(nxp,nyp),STAT=istat)

c--       333333333333333333333333333333D grids (sounding data)

      allocate(u(nxp,nyp,nlevs),STAT=istat)
      allocate(v(nxp,nyp,nlevs),STAT=istat)
      allocate(t(nxp,nyp,nlevs),STAT=istat)
      allocate(rh(nxp,nyp,nlevs),STAT=istat)
      allocate(z(nxp,nyp,nlevs),STAT=istat)

      allocate(zcps(nxp,nyp,nkcps),STAT=istat)
      allocate(plevcps(nkcps),STAT=istat)

c--       define grid lat/lon from f77OutputMeta module
c

      do i = 1,ni,1
        rlon(i) = xgrd(i)
      end do
      do j = 1,nj,1
        rlat(j) = ygrd(j)
      end do


c--       irepos not used
c--       inest = 0 for global model
c--       inest = 1 for hi-res grids

      irepos=0
      inest=0

c--       setup the vars in the tcTrkDiag module in mf.modules.f
c         
c         
      call setTrkdiag(plevs,nlevs,ntauTC)


      open( unit = lups, file=sstpath, form='unformatted',
     +     access='sequential', action='read', status='old')

      open( unit = ludf, file=outpath, form='formatted', status='unknown')

c--       cycle by TC taus vice fld taus
c         
      do itau=1,ntauTC

        rewind(lups)

c--       initialize to undef for each TC tau
c         

        us=rmiss
        vs=rmiss
        ts=rmiss
        rhs=rmiss
        ps=rmiss
        
        vrt850=rmiss
        zthklo=rmiss
        zthkhi=rmiss
        
        sst=rmiss
        ohc=rmiss
        tpw=rmiss
        
        vrt925=rmiss
        vrt700=rmiss
        pr=rmiss
        prc=rmiss

        u=rmiss
        v=rmiss
        t=rmiss
        rh=rmiss
        z=rmiss
        zcps=rmiss
        plevcps=rmiss

        clon=clonTC(itau)
        clat=clatTC(itau)
        cbearing=cdirTC(itau)
        cspeed=cspdTC(itau)

        if(verb) then
          write(*,'(a,i3,a,i3,a,4(f7.1),a,a)') 'TTTT: itau: ',itau,' tausTC(itau): ',tausTC(itau),
     $         '   SSSS: lat/lon/dir/spd: ',clat,clon,cbearing,cspeed,'   fldpath: ',DataPaths(tausTC(itau))
        endif

        open( unit = lupf, file=DataPaths(tausTC(itau)), form='unformatted',
     +     access='sequential', action='read', status='old',err=800)
      
        call readgrid(lups,lupf,
     $       nvarsfc,nvarua,varsfc,varua,
     $       nxp,nyp,nlevs,nkcps,
     $       iplevs,rmiss,ierrc,
     $       u,v,t,rh,z,zcps,plevcps,
     $       us,vs,ts,rhs,ps,pr,prc,
     $       vrt850,zthklo,zthkhi,
     $       sst,sstall,sstanom,ohc,tpw)

        goto 810

 800    continue
cc        print*,'WWWWWWWWWWWWWWWWWWWWWWWWWWW no data for TC tau: ',tausTC(itau)


 810    continue

        call lsdiags(nxp,nyp,nlevs,
     $       nxp,nyp,nlevs,nkcps,
     $       inest,itau,tausTC(itau),
     $       u,v,t,z,rh,zcps,plevcps,
     $       us,vs,ts,ps,rhs,tpw,
     $       sst,sstanom,ohc,pr,
     $       zthklo,
     $       rlon,rlat,plevs,
     $       clon,clat,cbearing,cspeed,
     $       irepos,rmiss,
     $       usnd,vsnd,tsnd,zsnd,rhsnd,
     $       usfc,vsfc,tsfc,psfc,rhsfc,
     $       nvar,nvart,diagvar,diaglab,
     $       nvaru,nvarut,udiagvar,udiaglab,
     $       ierrc)
        
        call loadTrkDiag(itau,tausTC(itau),
     $       rmiss,imissd,
     $       nvar,diagvar,idiagvar,
     $       nvaru,udiagvar,iudiagvar,
     $       usfc,vsfc,tsfc,rhsfc,psfc,
     $       nlevs,usnd,vsnd,tsnd,rhsnd,zsnd)

        
c        call writeparams(6,ierrc,rmiss,imiss,imissd,
c     $       nvar,diagvar,idiagvar,
c     $       nvaru,udiagvar,iudiagvar,
c     $       nlevs,usnd,vsnd,tsnd,rhsnd,zsnd,
c     $       usfc,vsfc,tsfc,rhsfc,psfc)

        close(lupf)

      enddo

      close(lups)

      call makeDiagCards(ntauTC,ludf)
        
      end program lsdiagdriver

