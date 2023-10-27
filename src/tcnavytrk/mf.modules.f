cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
      module const

        real, save :: pi =  4. * atan(1.)
        real, save :: dtr =  (4. * atan(1.))/180.0
        real, save :: dtk = 111.1949     ! Dist (km) over 1 deg lat
                           ! using erad=6371.0e+3
        real, save :: erad = 6371.0e+3   ! Earth's radius (m)
        real, save :: ecircum = 40030.2  ! Earth's circumference
                           ! (km) using erad=6371.e3
        real, save :: omega = 7.292e-5

        real, save :: rkm2nm=(60.0/111.1949)
        real, save :: rnm2km=(111.1949/60.0)

        real, save :: rearth=6371.0

        end module const

cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
       module mfutils


       contains


c         
c$$$      subprogram documentation block
c         .      .    .                                       .
c         subprogram:    distsp      distance on great circle
c         prgmmr: s. j. lord       org: w/nmc22    date: 91-06-06
c         
c         abstract: calculates distance on great circle between two lat/lon
c         points.
c         
c         program history log:
c         91-06-06  s. j. lord
c         yy-mm-dd  modifier1   description of change
c         yy-mm-dd  modifier2   description of change
c         
c         usage:    dxy=distsp(dlat1,dlon1,dlat2,dlon2)
c         input argument list:
c         dlat1    - latitude of point 1 (-90<=lat<=90)
c         dlon1    - longitude of point 1 (-180 to 180 or 0 to 360)
c         dlat2    - latitude of point 2 (-90<=lat<=90)
c         dlon1    - longitude of point 2
c         
c         
c         remarks: distance is in nm
c         
c         attributes:
c         language: indicate extensions, compiler options
c         machine:  nas, cyber, whatever
c         
c$$$      


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      function distsp(dlat1,dlon1,dlat2,dlon2)

      USE const
      
      implicit integer(i-n)
      implicit real (a-h,o-z)

      xxd=cos((dlon1-dlon2)*dtr)*cos(dlat1*dtr)*cos(dlat2*dtr)+
     1     sin(dlat1*dtr)*sin(dlat2*dtr)
         
      xxm=min(1.0d0,max(-1.0d0,xxd))
         
      distsp=acos(xxm)*rearth*rkm2nm
      return
      end function distsp

      subroutine bssl5(xi,xj,f,m,n,res)
c
c  general purpose two dimensional bessel interpolation
c
c  d. henson  --  april, 1987
c
c  arguments --
c
c   xi  -- i coordinate (real) 1.le.i.le.m
c   xj  -- j coordinate (real) 1.le.j.le.n
c   f   -- array to be interpolated
c   m   -- number of columns in f
c   n   -- number of rows in f
c   res -- returned interpolated value at f(xi,xj)
c
c   note----xi and xj are not tested for legal range
c
      dimension f(m,n)
      dimension fr(4)
c
      mm1 = m-1
      nm1 = n-1
      ii = xi
      j = xj
      r = xi-ii
      s = xj-j
c
c   r and s are the fractional parts of xi and xj respectively
c
c   test for top/right edge, border, or interior 
c
      if(ii.ge.2 .and. j.ge.2 .and. ii.lt.mm1 .and. j.lt.nm1)
     $  go to 10
c
      if(ii.lt.m.and. j.lt.n) go to 5 
c
c   top or right edge
c         

c--       cyclic continuity in x
      if(ii.gt.m) then
        ii=ii-m
      endif

      if(ii.eq.m .and. j.eq.n) then
        res = f(m,n)

c--       cyclic continuity in x
      else if(ii.le.m) then
        res = (1.-s)*f(ii,j)+s*f(ii,j+1)

      else if(j.eq.n) then
        res = (1.-r)*f(ii,j)+r*f(ii+1,j)
      endif
      return


 5    continue

c
c   border zone -- use bilinear interpolation
c         
      iip1=ii+1
      if(iip1.gt.m) iip1=iip1-m
      if(iip1.lt.1) iip1=m-iip1
      res = (1.-s)*((1.-r)*f(ii,j)+r*f(iip1,j))
     $  +s*((1.-r)*f(ii,j+1)+r*f(iip1,j+1))

      return
c
 10   continue
c   interior zone
c
c   interpolate 4 columns (i-1,i,i+1,i+2) to j+s and store in fr(1)
c   through fr(4)
c
      r1 = r-0.5
      r2 = r*(r-1.)*0.5
      r3 = r1*r2*0.3333333333334
      s1 = s-0.5
      s2 = s*(s-1.)*0.5
      s3 = s1*s2*0.3333333333334
c
      k = 0
      im1 = ii-1
      ip2 = ii+2
c
      do 20 i = im1,ip2
        k = k+1
        i2=i

        if(i2.gt.m) i2=m-i2
        if(i2.lt.1) i2=m+i2

        u = (f(i2,j)+f(i2,j+1))*0.5
        del = f(i2,j+1)-f(i2,j)
        udel2 = (f(i2,j+2)-f(i2,j+1)+f(i2,j-1)-f(i2,j))*0.5
        del3 = f(i2,j+2)-f(i2,j+1)-2.*del+f(i2,j)-f(i2,j-1)
        fr(k) = u+s1*del+s2*udel2+s3*del3

 20   continue

c
c   interpolate the fr row to ii+r
c
      u = (fr(2)+fr(3))*0.5
      del = fr(3)-fr(2)
      udel2 = (fr(4)-fr(3)+fr(1)-fr(2))*0.5
      del3 = fr(4)-fr(3)-2.*del+fr(2)-fr(1)
c
      res = u+r1*del+r2*udel2+r3*del3
c
      return
      end subroutine bssl5
      
      subroutine indexx(n,arrin,indx)
      dimension arrin(n),indx(n)
      do 11 j=1,n
        indx(j)=j
 11   continue
      l=n/2+1
      ir=n
10    continue
        if(l.gt.1)then
          l=l-1
          indxt=indx(l)
          q=arrin(indxt)
        else
          indxt=indx(ir)
          q=arrin(indxt)
          indx(ir)=indx(1)
          ir=ir-1
          if(ir.eq.1)then
            indx(1)=indxt
            return
          endif
        endif
        i=l
        j=l+l
20      if(j.le.ir)then
          if(j.lt.ir)then
            if(arrin(indx(j)).lt.arrin(indx(j+1)))j=j+1
          endif
          if(q.lt.arrin(indx(j)))then
            indx(i)=indx(j)
            i=j
            j=j+j
          else
            j=ir+1
          endif
        go to 20
        endif
        indx(i)=indxt
      go to 10
      end subroutine indexx

      function ichar_len(c,imax)
      character*1 c(imax)
      iend=-1
      ii=imax
      do while (iend.eq.-1.and.ii.le.imax)
        if(c(ii).ne.' ') iend=ii
        ii=ii-1
      end do  
      if(ii.gt.imax) then
        ichar_len=imax
      else
        ichar_len=iend-1
      end if
      return
      end function ichar_len



      subroutine qprntn(a,qtitle,ibeg,jbeg,m,n,iskip,iunit)
c
c**********	12 APR 91 this version outputs to iunit 
c**********	using write on the Cray Y/MP 
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****       qprint output routine (corrected 4/26/86)     *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
c a= fwa of m x n array
c qtitle - title
c ibeg,jbeg=lower left corner coords to be printed
c up to 43 x 83 points printed
c         
      dimension a(m,n),ix(81)
      character qtitle*24
c
c  determine grid limits
c
      if(iskip.eq.0) iskip=1
      iend=min0(ibeg+79*iskip,m)
      jend=min0(jbeg+79*iskip,n)
c
   24 continue
c
c  index backwards checking for max
c
   11 xm=0.
      jendsc=min0(jend,n)
      do j=jbeg,jendsc,iskip
      jend_qp = j
      do i=ibeg,iend,iskip
        xm=amax1(xm,abs(a(i,j)))
      end do
      end do
c
c  determine scaling factor limits
c
      if(xm.lt.1.0e-32.or.xm.eq.0.0) xm=99.0
      xm=alog10(99.0/xm)
      kp=xm
      if(xm.lt.0.0)kp=kp-1
c
c  print scaling constants
c
   12 write(iunit,1) qtitle,kp,iskip,(i,i=ibeg,iend,2*iskip)

    1 format('0',a,'   k=',i3,' iskip=',i2,/,' ',41i6) 
      fk=10.0**kp
c
c  quickprint field
c
      do 2 jli=jend_qp,jbeg,-iskip
        ii= 0
        if(kp.eq.0) then 
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)+sign(.5,a(i,jli))
          end do
        else
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)*fk+sign(.5,a(i,jli))
          end do
        end if
        write(iunit,'(i4,81i3)') jli,(ix(i),i=1,ii),jli
2     continue
      return
      end subroutine qprntn


      subroutine qprntu(a,qtitle,ibeg,jbeg,m,n,iskip,iunit,undef)
c
c**********	12 APR 91 this version outputs to iunit 
c**********	using write on the Cray Y/MP 
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****       qprint output routine (corrected 4/26/86)     *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
c a= fwa of m x n array
c qtitle - title
c ibeg,jbeg=lower left corner coords to be printed
c up to 43 x 83 points printed
c         
      dimension a(m,n),ix(81)
      character qtitle*24
c
c  determine grid limits
c
      if(iskip.eq.0) iskip=1
      iend=min0(ibeg+79*iskip,m)
      jend=min0(jbeg+79*iskip,n)
c
   24 continue
c
c  index backwards checking for max
c
   11 xm=0.
      jendsc=min0(jend,n)
      do j=jbeg,jendsc,iskip
      jend_qp = j
      do i=ibeg,iend,iskip
        if(a(i,j) /= undef)   xm=amax1(xm,abs(a(i,j)))
      end do
      end do
c
c  determine scaling factor limits
c
      if(xm.lt.1.0e-32.or.xm.eq.0.0) xm=99.0
      xm=alog10(99.0/xm)
      kp=xm
      if(xm.lt.0.0)kp=kp-1
c
c  print scaling constants
c
   12 write(iunit,1) qtitle,kp,iskip,(i,i=ibeg,iend,2*iskip)

    1 format('0',a,'   k=',i3,' iskip=',i2,/,' ',41i6) 
      fk=10.0**kp
c
c  quickprint field
c
      do 2 jli=jend_qp,jbeg,-iskip
        ii= 0
        if(kp.eq.0) then 
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)+sign(.5,a(i,jli))
          end do
        else
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)*fk+sign(.5,a(i,jli))
          end do
        end if
        write(iunit,'(i4,81i3)') jli,(ix(i),i=1,ii),jli
2     continue
      return
      end subroutine qprntu


      function ichlen(c,imax)
      integer imax,iend,ii,ichlen
      character*1 c(imax)

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


      subroutine setundef0(a,ni,nj,undef,ierr)

      real undef
      real*4 a
      integer i,j,ierr

      dimension a(ni,nj)
      ierr=0
      do i=1,ni
        do j=1,nj
          if(abs(a(i,j)).ge.undef) a(i,j)=0.0
        end do
      end do
      return
      end subroutine setundef0
            

      end module mfutils



cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
      module trkParams

      
      integer, parameter :: np=1000        ! max # of extrema points
      integer, parameter :: nc=100         ! max # of final center points
      integer, save :: ihl(np),jhl(np)     ! i,j index of extrema
      real,    save :: vhl(np)             ! value at extrema


      real,    save  :: vortcrit=7.5
      real,    save  :: vmaxweak=30.0
      real,    save  :: vortadjfact=0.60

      logical, save  :: doGdatCon=.true.
      logical, save  :: vortcritadjust=.true.
      logical, save  :: doSpeedBrake=.true.
      logical, save  :: doAccelBrake=.true.

      integer, save  :: ktauMaxInitialMotion=12

      logical, save  :: dosmthMotion=.true.
      real,    save  :: smthMotionTauPeriod=18.0

c--       set search radius by max forward speed
c
      real,    save  :: forspdMax=35.0
      real,    save  :: forspdAdjfact=1.5
      real,    save  :: forspdMaxTau0=24

      real,    save  :: forspdLatET=37.5
      real,    save  :: congdatET=37.5
      real,    save  :: forspdMaxET=45.0

      real,    save  :: accelMax=25.0

      logical, save  :: doInitialSpdMaxAdj=.true.


      real,    save  :: rfindPsl=0.5
      real,    save  :: rfindVrt850=1.0
      real,    save  :: rfindGen=0.75

      real,    save  :: sdistpsl=180.0    ! scale of max diff between center and field within sdistpsl
      real,    save  :: rminPsldef=-0.5   ! minimum pressure deficit [mb]

      real,    save  :: sdistmin
      real,    save  :: rmaxConSep=120.0


      integer, save  :: dtau=6
      real,    save  :: dlonmax
      real,    save  :: rlatmax=60.0

      real,    save  :: undef=1e20

      real,    parameter :: eps=1e-7
      real,    parameter :: dseps=1e-3

      integer,  save      :: maxhour,maxhr

      integer,  parameter :: maxtc=18
      integer,  parameter :: numvar=10
      integer,  parameter :: maxfix=3
      integer,  parameter :: iunitnl=55


      logical,  save :: distnm=.false.

      logical,  save :: verbConGdat=.false.
      logical,  save :: verbGrhiloPsl=.false.
      logical,  save :: verbGrhiloVrt850=.false.	

      logical,  save :: verbMfTrack=.false.	
      logical,  save :: verbMfTrackem=.false.
      logical,  save :: verbTrackem=.false.


      real, allocatable, dimension(:,:,:,:) :: gdat

      contains


      subroutine inittrkParams(nlpath)

      use mfutils
      character*128 nlpath

      namelist /trkParamsNL/
     $     vortcrit,
     $     vmaxweak,
     $     vortadjfact,
     $     doGdatCon,
     $     vortcritadjust,
     $     doSpeedBrake,
     $     doAccelBrake,
     $     forspdMax,
     $     forspdLatET,
     $     forspdMaxET,
     $     congdatET,
     $     forspdAdjfact,
     $     forspdMaxTau0,
     $     accelMax,
     $     doInitialSpdMaxAdj,
     $     rfindPsl,
     $     rfindVrt850,
     $     rfindGen,
     $     sdistpsl,
     $     rminPsldef,
     $     ktauMaxInitialMotion,
     $     dosmthMotion,
     $     smthMotionTauPeriod,
     $     rlatmax,
     $     rmaxConSep,
     $     undef

      namelist /verbOse/
     $     verbConGdat,
     $     verbGrhiloPsl,
     $     verbGrhiloVrt850,
     $     verbMfTrack,
     $     verbMfTrackem,
     $     verbTrackem


      open(iunitnl,file=nlpath(1:ichlen(nlpath,128)),
     $     status='old',err=810)

      read (iunitnl,nml=trkParamsNL,end=801)
      write(*,nml=trkParamsNL)

      read (iunitnl,nml=verbOse,end=801)
      write(*,nml=verbOse)

      dlonmax=forspdmax*(dtau/60.0)
      sdistmin=dlonmax*60.0

      return

 801  continue
      print*,'EEE premature end of file in reading trkParamsNL'
      stop 801

 810  continue
      print*,'EEE in open of ',nlpath
      stop 'nlpath'

      end subroutine inittrkParams

cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
c--       con of fixes
c
      subroutine conGdat(fixlat,fixlon,
     $     fglat,fglon,rmaxConSepMX,
     $     conLat,conLon,ifixbase,npcon)


      use mfutils

      real fixlat(maxfix),fixlon(maxfix)
      logical valid(maxfix),verb

      verb=verbConGdat

c--       need a base lat/lon, assume the first valid is the best estimate
c         then calc distance from this point; will be 0.0 for one point,
c         insuring one fix gets into the con

      baselat=999.0
      nvalid=0
      ifixbase=0


      do i=1,maxfix
        valid(i)=.false.

        if(fixlat(i) .lt. 90.0) then
          nvalid=nvalid+1
          valid(i)=.true.
          if(baselat .gt. 90.0) then
            baselat=fixlat(i)
            baselon=fixlon(i)
            ifixbase=i
          endif
        endif
      enddo

c--       use first guess for baselat/lon vice first valid
c         
      if(fglat.gt.-80.0 .and. fglat.lt.80 .and. fglat.ne.0. ) then
        if(verb) then
          print*,'CCC using fglat/fglon:',fglat,fglon
        endif
        baselat=fglat
        baselon=fglon
      endif


      conLat=0.0
      conLon=0.0
      npcon=0
      nvalid=0
      
      do i=1,maxfix

        if(valid(i)) then
          nvalid=nvalid+1

c--       dist from the first guess
c
          dist=distsp(baselat,baselon,fixlat(i),fixlon(i))

c--       if < rmaxConSepMX : close to first
c
          if(dist < rmaxConSepMX) then
            conLat=conLat+fixlat(i)
c--       crossing the 0E
            if(fixlon(i).lt.20.0) fixlon(i)=fixlon(i)+360.0
            conLon=conLon+fixlon(i)
            npcon=npcon+1
            if(verb) then
              print*,'CCC conGdat(fix): i: ',i,' dist: ',dist,' rmaxConSepMX: ',rmaxConSepMX,
     $             ' fixlat/lon: ',fixlat(i),fixlon(i),
     $             ' baselat/lon: ',baselat,baselon,' ifixbase: ',ifixbase
            endif

          else

c--       if > rmaxConSepMX : too fast, e.g., in midlats
c
            print*,'CCC conGdat(WWW-OB): i: ',i,' dist: ',dist,' rmaxConSepMX: ',rmaxConSepMX,
     $           ' fixlat/lon: ',fixlat(i),fixlon(i),
     $           ' baselat/lon: ',baselat,baselon,' ifixbase: ',ifixbase
            
          endif

        endif

      enddo
      
      if(npcon.gt.0) then 
        fact=1.0/float(npcon)
        conLat=conLat*fact
        conLon=conLon*fact
      endif

c--       if all fixes are too fast
c         
      if(npcon.eq.0) then

c--       check pressure fix first, if in midlats
c
        if(valid(3) .and. fixlat(3) >= congdatET) then
          conLat=fixlat(3)
          conLon=fixlon(3)
          npcon=15

        elseif( valid(2) .and. valid(3) ) then
          conLat=( fixlat(2) + fixlat(3) )*0.5
          conLon=( fixlon(2) + fixlon(3) )*0.5
          npcon=14

        elseif( valid(2) .and. .not.valid(3) ) then
          conLat=fixlat(2)
          conLon=fixlon(2)
          npcon=12

c--       really are no vort/psl fixes, set to undef
c
        elseif( .not.valid(2) .and. .not.valid(3) ) then
          conLat=99.9
          conLon=999.9
          npcon=0

        elseif( valid(3) .and. .not.valid(2) ) then
          conLat=fixlat(3)
          conLon=fixlon(3)
          npcon=13

        else

          print*, 'EEE unable to set conlat/lon in mf.modules.conGdat()'
          stop 'conGdat failure'

        endif

      endif

c--       make sure 0-360E

      if( (conLon.ge.360.0) .and. (conLon.lt.900.0) ) conLon=conLon-360.0

      if(verb) then
        print*,'CCC conGdat(III): npcon,ifixbase,conLat,conLon: ',npcon,ifixbase,conLat,conLon
      endif
      return

      end subroutine conGdat

      end module trkParams


cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
      module f77OutputMeta

      integer, save :: 
     $     ni,nj,nk,nt,ntf,
     $     nvarsfc,nvarua,
     $     lups,lupf

      real,                              save :: blat,blon,elat,elon,dlat,dlon
      real,   allocatable, dimension(:), save :: xgrd,ygrd,coslatI

      character(len=128), allocatable, dimension(:) :: DataPaths

      character(len=10),  allocatable, dimension(:) :: varsfc,varua
      integer, allocatable, dimension(:) :: iplevs
      integer, allocatable, dimension(:) :: itaus
      real*4,  allocatable, dimension(:) :: plevs


      contains

      subroutine readFldMeta(tcmetapath,ierr)

      use mfutils
      use const
      use trkParams

      integer*4 ios,pos,i,j,k,l,n,m,nlevs

      character*128 tcmetapath

      character(len=512) :: buffer
      logical verb

      verb=.false.
ccc      verb=.true.

      open( unit=1, file=tcmetapath(1:ichlen(tcmetapath,128)), form='formatted',action='read',err=812)

      ios=0

      do while ( ios == 0 )

 5      continue
        read( 1, '(a)', iostat=ios ) buffer

        print*,'buffer: ',buffer(1:128)
 
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
            read(buffer(pos:pos+3),'(f6.2)') blon
            if(verb) print*,'blon---------------------- ',pos,blon
          end if


          pos = index(buffer, "lonE:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+3),'(f6.2)') elon
            if(verb) print*,'elon---------------------- ',pos,elon
            goto 5
          end if

          pos = index(buffer, "latS:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') blat
            if(verb) print*,'blat---------------------- ',pos,blat
          end if

          pos = index(buffer, "latN:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') elat
            if(verb) print*,'elat---------------------- ',pos,elat
            goto 5
          end if

          pos = index(buffer, "dlon:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') dlon
            if(verb) print*,'dlon---------------------- ',pos,dlon
          end if

          pos = index(buffer, "dlat:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') dlat
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
              allocate(DataPaths(nt),STAT=istat)
              do i=1,nt
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:3),'(i3,1x,a128)') itaus(i)
                read(buffer(5:128+5),'(a)') DataPaths(i)
                if(verb) print*,'itaus---------------------- ',itaus(i),DataPaths(i)
              enddo

c--       set vars in trkParams from input, taus, and the gdat array
c
              
              dtau=6
              maxhour=itaus(nt)
              if(nt > 1) dtau=itaus(2)-itaus(1)
              maxhr=((maxhour/dtau)+1)
              allocate(gdat(numvar,0:maxhr,maxtc,0:maxfix),stat=istat)
              if(istat.gt.0) go to 814

c--       initialize to 0
c         
              do i=1,numvar
                do j=0,maxhr
                  do k=1,maxtc
                    do l=0,maxfix
                      gdat(i,j,k,l)=0.0
                    enddo
                  enddo
                enddo
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
            print*, buffer
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

        end if

      end do


C         
C..       define the grid; now from input
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
      

      return

 812  continue

      print*,'error opening input field file'
      print*,tcmetapath
      stop 812

 814  continue
      print*,'error in allocate...readFldMeta'
      stop 814


      end subroutine readFldMeta

c--       routines for tracker

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c--       find extrema in a box ib,ie->jb,je, return the the i,j, then pass to 
c         getExtremaProps

      subroutine findExtrema(fld,
     $     ib,ie,jb,je,ctype,
     $     rfind,
     $     nhl)

      use const
      use trkParams

      integer i,j,ib,ie,jb,je
      
      integer np0undef,np0print,np1357undef,np2468undef

      character*1 ctype

      real*4 fld(ni,nj)
      real   rfind

      integer i0,j0,i0m1,i0p1,j0p1,j0m1

      real p0,p1,p2,p3,p4,p5,p6,p7,p8,p0l,p0h

      integer nhl

      logical verb
      logical tough

      logical hi,lo,
     $     hi_closed1,lo_closed1,hi_closed2,lo_closed2
      
      character*1 chl

cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

      tough=.false.

      nhl=0
      verb=.false.
ccc      verb=.true.

      np0undef=0
      np1357undef=0
      np2468undef=0
      np0print=2
      do i=ib,ie

        do j=jb,je

          i0=i
          j0=j
          i0p1=i0+1
          i0m1=i0-1
          j0p1=j0+1
          j0m1=j0-1

          p0=fld(i0,j0)
      
c--         check for undefined points;, cycle
          
          if(p0 == undef .and. np0undef .le. np0print) then
            print*,'ngtrk.findExtrema() p0 undef i0,j0: ',i0,j0
            np0undef=np0undef+1
            cycle
          endif     

          p0l=p0-p0*eps
          p0h=p0+p0*eps
      
          p3=fld(i0,j0p1)
          p7=fld(i0,j0m1)
          p1=fld(i0p1,j0)
          p5=fld(i0m1,j0)
          
          if( (p3 == undef .or. p7 == undef .or. p1 == undef .or. p5 == undef) .and. (np1357undef .le. np0print) ) then 
            print*,'ngtrk.findExtrema() p1,3,5,7 undef i0,j0: ',i0,j0
            np1357undef=np1357undef+1
            cycle
          endif
      
          p2=fld(i0p1,j0p1)
          p4=fld(i0p1,j0m1)
          p6=fld(i0m1,j0p1)
          p8=fld(i0m1,j0m1)

          if(( tough .and. (p2 == undef .or. p4 == undef .or. p6 == undef .or. p8 == undef) ) .and. 
     $         (np2468undef .le. np0print) ) then
            print*,'ngtrk.findExtrema() p2,4,6,8 undef i0,j0: ',i0,j0
            np2468undef=np2468undef+1
            cycle
          endif

          if(verb) then
            write(*,'(a,2i5,4(1pe20.7))') '000',i0,j0,p0,p0l,p0h,eps
            write(*,'(a,8i5,4(1pe20.7))') '111',i0,j0p1,i0,j0m1,i0p1,i0,i0m1,j0,p3,p7,p1,p5
            write(*,'(a,8i5,5(1pe20.7))') '222',i0p1,j0p1,i0p1,j0m1,i0m1,j0p1,i0m1,j0m1,p2,p4,p6,p1,p8
          endif
          
         
c         test if a relative hi or lo using two levels of "closedness"
c         

          lo_closed1=.false.
          lo_closed2=.false.
          hi_closed1=.false.
          hi_closed2=.false.

          if(tough) then 
            lo=p0l.lt.p1.and.p0l.lt.p3.and.
     1           p0l.lt.p5.and.p0l.lt.p7.and.
     2           p0l.lt.p2.and.p0l.lt.p4.and.
     3           p0l.lt.p6.and.p0l.lt.p8
            
            hi=p0h.gt.p1.and.p0h.gt.p3.and.
     1           p0h.gt.p5.and.p0h.gt.p7.and.
     2           p0h.gt.p2.and.p0h.gt.p4.and.
     3           p0h.gt.p6.and.p0h.gt.p8
            
          else

            p0h=p0
            p0l=p0

            lo=p0l.lt.p1.and.p0l.lt.p3.and.
     1           p0l.lt.p5.and.p0l.lt.p7
            
            hi=p0h.gt.p1.and.p0h.gt.p3.and.
     1           p0h.gt.p5.and.p0h.gt.p7
          endif

          if(verb) then 
            write(*,'(a,2(i5),3(f7.2))') 'iiiiiiiiiii ',i0,j0,fld(i0m1,j0),fld(i0,j0),fld(i0p1,j0)
            write(*,'(a,2(i5),3(f7.2))') 'jjjjjjjjjjj ',i0,j0,fld(i0,j0m1),fld(i0,j0),fld(i0,j0p1)
            print*,'hhhh', hi,lo,ctype
            print*
          endif

          select case (ctype)

             case('h')
                lo=.false.

             case('l')
                hi=.false.
             
          
          end select


          if(hi.or.lo) then

            call checkExtrema(fld,i0,j0,rfind,ishilo)
            if(verb) print*,'aaaaaaaaaaaaaaaaaa',i0,j0,rfind,fld(i0,j0),ishilo

            if(ishilo.eq.1 .or. ishilo.eq.-1 ) then
              nhl=nhl+1
              ihl(nhl)=i0
              jhl(nhl)=j0
              vhl(nhl)=p0
            endif

          endif

        enddo

      enddo

      if(verb) print*,'NNNNNNNNNNNN ',nhl,rfind
      return

      end subroutine findExtrema


      
      subroutine setBounds(i,j,ni,nj)
      if(i.lt.1) i=1
      if(i.gt.ni) i=ni
      if(j.lt.1) j=1
      if(j.gt.nj) j=nj
      return
      end subroutine setBounds



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      subroutine getExtremaProps(fld,
     $     i0,j0,flat,flon,
     $     xhl,yhl,ahl,ghl,lhl,dhl)

      use trkParams

      real*4 fld(ni,nj)

      real flat,flon

      integer i0m1,i0p1,j0p1,j0m1
      integer nhl,nh,nl

      real p0,p1,p2,p3,p4,p5,p6,p7,p8,p0l,p0h
      real xhl,yhl,ahl,ghl,lhl,dhl
      real dr,r0,ds,s0,rihl,rjhl
      real thead


      logical verb

      verb=.false.
ccc      verb=.true.

c--       cyclic continuity 

      i0p1=i0+1
      if(i0p1.gt.ni) i0p1=i0p1-ni

      i0m1=i0-1
      if(i0m1.lt.1) i0m1=ni-i0m1

      j0p1=j0+1
      j0m1=j0-1

      p0=fld(i0,j0)
      p3=fld(i0,j0p1)
      p7=fld(i0,j0m1)
      p1=fld(i0p1,j0)
      p5=fld(i0m1,j0)
          

c--       don't need to check for undef here because done before calling
c
      ahl=-9999.
      xhl=-9999.
      yhl=-9999.
      ghl=-9999.
      lhl=-9999.
      dhl=-9999.
      
c--       use sterling's formula to locate the critical
c         point between grid points
c         
c         dr and ds are the 2nd derivatives in x and y
c         
c         ghl is the mag of the gradient

      ghl=sqrt((p1-p5)*(p1-p5)+(p3-p7)*(p3-p7))

      r0=0.5*(p1-p5)
      dr = -(p1-2.0*p0+p5)
C--       correctform? yes; from steve lords clhilo.f            dr = -(p1-2.0*(p0+p5)) is not

      if(abs(dr).ge.dseps) then        
        r0=r0/dr
      else
        r0 = 0.0
      endif
      
      if(r0.gt. 1.0) r0= 1.0
      if(r0.lt.-1.0) r0=-1.0
      
      s0=0.5*(p3-p7)
      ds= -(p3-2.0*p0+p7)
c--       correct form? yes; from steve lords clhilo.f            ds= -(p3-2.0*(p0+p7)) is not...
      
      if(abs(ds).ge.dseps) then
        s0=s0/ds
      else
        s0 = 0.0
      endif
      
      if(s0.gt. 1.0) s0= 1.0
      if(s0.lt.-1.0) s0=-1.0
      
      lhl=sqrt(dr*dr+ds*ds)
      
      rihl=i0+r0
      rjhl=j0+s0
      
      if(verb) then
        print*,'xgrd...',xgrd(i0m1),xgrd(i0),xgrd(i0p1)
        print*,'i0 ',i0m1,i0,i0p1,r0,p5,p0,p1
        print*,'ygrd...',ygrd(j0m1),ygrd(j0),ygrd(j0p1)
        print*,'j0 ',j0m1,j0,j0p1,s0,p7,p0,p3
      endif
      
      if(r0.ge.0.0) then
        xhl= xgrd(i0) + r0*(xgrd(i0p1)-xgrd(i0))
      else
        xhl= xgrd(i0) + r0*(xgrd(i0)-xgrd(i0m1))
      endif
      
      if(s0.ge.0.0) then
        yhl= ygrd(j0) + s0*(ygrd(j0p1)-ygrd(j0))
      else
        yhl= ygrd(j0) + s0*(ygrd(j0)-ygrd(j0m1))
      endif
      
c--    find the value of the max using 2-d bessel interp
c         
      call bssl5(rihl,rjhl,fld,ni,nj,ahl)
      
      dhl=0
      call rumdirdist(yhl,xhl,flat,flon,thead,dhl)
      if(.not.distnm) then
        dhl=dhl/60.0
      endif
      
      return

      end subroutine getExtremaProps


c--       find range of indices given a dlonmax box, assumes uniform lat/lon grid

      subroutine getIJrange(egyy,egxx,
     $     dlonmax,
     $     ib,ie,jb,je)

      ib=-999
      ie=-999
      jb=-999
      je=-999

c--       main size of box in x(i) depend on central latitude up to 50% bigger
c
      coslatMax=1.5
      coslatFact=coslatI(nint(egyy))
      if(coslatFact >= coslatMax) coslatFact=coslatMax

ccc      print*,'IIIIIIIIIIIIIIIIIIIIIIIII ',nint(egyy),coslatI(nint(egyy)),coslatFact
ccc       coslatFact=1.0

      ib=nint(egxx-((dlonmax*coslatFact)/dlon))
      ie=nint(egxx+((dlonmax*coslatFact)/dlon)*2)
      idx=ie-ib

c--       cyclic continuity

      if(ib.lt.0) ib=ib+ni+1
      if(ib.gt.ni) ib=ib-ni+1
      ie=ib+idx
      
      jb=nint(egyy-dlonmax/dlat)
      je=nint(egyy+(dlonmax/dlat)*2)
      jdx=je-jb
      
      if(jb.le.0) jb=1
      je=jb+jdx
      if(je.ge.nj-1) je=nj-1
      
      return

      end subroutine getIJrange


      subroutine checkExtrema(fld,i0,j0,rfind,ishilo)

      use const

      real*4 fld(ni,nj)
      real   dist2(ni,nj)

      ishilo=0

c--       define a search radius and locate

      if(i0 >= ni) i0=ni
      if(i0 <= 1)  i0=1

      if(j0 >= nj) j0=nj
      if(j0 <= 1)  j0=1

c--       find x limit

      dx=rfind*coslatI(j0)
ccc      dx=rfind*2
      dy=rfind

      dxg=dx/dlon
      dyg=dy/dlat


      idx=int(dxg)+1
      jdy=int(dyg)+1

      ib=i0-idx
      ie=i0+idx

      jb=j0-jdy
      je=j0+jdy

      call setBounds(ib,jb,ni,nj)
      call setBounds(ie,je,ni,nj)

cccc      print*,'i0,j0: ',i0,j0,'ib,ie: ',ib,ie,' jb,je: ',jb,je

      fmin=1e20
      fmax=-1e20

      rmax2=dxg*dxg + dyg*dyg

ccc      print*,'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII ',i0,j0,xgrd(i0),ygrd(j0),' rrr ',rfind,rmax2,2*idx,2*jdy
      do i=ib,ie
        do j=jb,je
          dist2(i,j)=(i-i0)*(i-i0) + (j-j0)*(j-j0)
        enddo
      enddo

c--       get the max/min in the search circle
c         
      np=0
      npmin=4

      do i=ib,ie
        do j=jb,je

          if(dist2(i,j) <= rmax2) then

            np=np+1

            if(fld(i,j) .gt. fmax ) then
              fmax=fld(i,j)
              imx=i
              jmx=j
            endif

            if(fld(i,j) .lt. fmin) then
              fmin=fld(i,j)
              imn=i
              jmn=j
            endif

          endif

        enddo
      enddo

c--       now see if it's a local extrema
c         
      if( (imx.eq.i0 .and. jmx.eq.j0) .and. (fmax.gt.-1e20) ) then
cc        print*,'local MAX: ',fmax,i0,j0,fmax,imx,jmx
        ishilo=1
      endif

      if( (imn.eq.i0 .and. jmn.eq.j0) .and. (fmin.lt.+1e20)  ) then
cc        print*,'local min: ',fmin,i0,j0,fmin,imn,jmn
        ishilo=-1
      endif


      return

      end subroutine checkExtrema

      end module f77OutputMeta




