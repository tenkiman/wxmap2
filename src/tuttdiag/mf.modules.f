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

c--       set search radius by max forward speed
c
      real,    save  :: forspdMax=40.0
      real,    save  :: forspdAdjfact=1.5
      real,    save  :: forspdMaxTau0=24
      logical, save  :: doInitialSpdMaxAdj=.true.


      real,    save  :: rfindPsl=0.5
      real,    save  :: rfindVrt925=1.0
      real,    save  :: rfindGen=0.75

      real,    save  :: sdistpsl=180.0 ! scale of max diff between center and field within sdistpsl
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
      logical,  save :: verbGrhiloVrt925=.false.	

      logical,  save :: verbMfTrack=.false.	
      logical,  save :: verbMfTrackem=.false.
      logical,  save :: verbTrackem=.false.


      real, allocatable, dimension(:,:,:,:) :: gdat

      contains

      subroutine inittrkParams

      namelist /trkParamsNL/
     $     vortcrit,
     $     vmaxweak,
     $     vortadjfact,
     $     doGdatCon,
     $     vortcritadjust,
     $     doSpeedBrake,
     $     forspdMax,
     $     forspdAdjfact,
     $     forspdMaxTau0,
     $     doInitialSpdMaxAdj,
     $     rfindPsl,
     $     rfindVrt925,
     $     rfindGen,
     $     sdistpsl,
     $     rlatmax,
     $     rmaxConSep,
     $     undef

      namelist /verbOse/
     $     verbConGdat,
     $     verbGrhiloPsl,
     $     verbGrhiloVrt925,
     $     verbMfTrack,
     $     verbMfTrackem,
     $     verbTrackem


      read (iunitnl,nml=trkParamsNL,end=801)
      write(*,nml=trkParamsNL)
 801  continue

      read (iunitnl,nml=verbOse,end=802)
      write(*,nml=verbOse)
 802  continue

      dlonmax=forspdmax*(dtau/60.0)
      sdistmin=dlonmax*60.0

      return
      end subroutine inittrkParams

      end module trkParams

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

      end module f77OutputMeta

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


cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmfffffffffffffffffffffffffffffffffffffffffffff
c         
c--       routines for tracker

c--       find range of indices given a dlonmax box, assumes uniform lat/lon grid

      subroutine getIJrange(egyy,egxx,
     $     dlonmax,
     $     ib,ie,jb,je)

      use f77outputmeta

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


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c--       find extrema in a box ib,ie->jb,je, return the the i,j, then pass to 
c         getExtremaProps

      subroutine findExtrema(fld,
     $     ib,ie,jb,je,ctype,
     $     rfind,
     $     nhl)

      use trkParams
      use f77OutputMeta

      integer i,j,ib,ie,jb,je

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
         
          if(p0 == undef) then
            print*,'p0 undef'
            cycle
          endif     

          p0l=p0-p0*eps
          p0h=p0+p0*eps
      
          p3=fld(i0,j0p1)
          p7=fld(i0,j0m1)
          p1=fld(i0p1,j0)
          p5=fld(i0m1,j0)
          
          if(p3 == undef .or. p7 == undef .or. p1 == undef .or. p5 == undef) then 
            print*,'p1,5,3,7 undef'
            cycle
          endif
      
          p2=fld(i0p1,j0p1)
          p4=fld(i0p1,j0m1)
          p6=fld(i0m1,j0p1)
          p8=fld(i0m1,j0m1)

          if(tough .and. p2 == undef .or. p4 == undef .or. p6 == undef .or. p8 == undef) then
            print*,'p2,4,6,8 undef'
            cycle
          endif

          if(verb) then
            write(*,'(a,2i5,3(1pe20.7))') '000',i0,j0,p0,p0l,p0h,eps
            write(*,'(a,8i5,4(1pe20.7))') '111',i0,j0p1,i0,j0m1,i0p1,i0,i0m1,j0,p3,p7,p1,p5
            write(*,'(a,8i5,4(1pe20.7))') '222',i0p1,j0p1,i0p1,j0m1,i0m1,j0p1,i0m1,j0m1,p2,p4,p6,p1,p8
          endif
          
         
c         test if a relative hi or lo using two levels of "closedness"
c         

          lo_closed1=.false.
          lo_closed2=.false.
          hi_closed1=.false.
          hi_closed2=.false.
          
          lo_closed1=p0l.lt.p1.and.p0l.lt.p3.and.
     1         p0l.lt.p5.and.p0l.lt.p7.and.
     2         p0l.lt.p2.and.p0l.lt.p4.and.
     3         p0l.lt.p6.and.p0l.lt.p8
          
          hi_closed1=p0h.gt.p1.and.p0h.gt.p3.and.
     1         p0h.gt.p5.and.p0h.gt.p7.and.
     2         p0h.gt.p2.and.p0h.gt.p4.and.
     3         p0h.gt.p6.and.p0h.gt.p8
          
          if(.not.tough) then
            lo_closed2=p0l.lt.p1.and.p0l.lt.p3.and.
     1           p0l.lt.p5.and.p0l.lt.p7
            
            hi_closed2=p0h.gt.p1.and.p0h.gt.p3.and.
     1           p0h.gt.p5.and.p0h.gt.p7
          endif
        
          if(tough) then 
            hi=hi_closed1
            lo=lo_closed1
          else
            hi=hi_closed2
            lo=lo_closed2
          endif

          if(verb) then
            print*,'hhh',hi,hi_closed1,hi_closed1,hi_closed2,hi_closed2,tough
            print*,'lll',lo,hi_closed1,lo_closed1,hi_closed2,lo_closed2,tough
          endif
          
          select case (ctype)

             case('h')

                lo=.false.
                hi=.false.
                if(tough) then 
                   hi=hi_closed1
                else
                   hi=hi_closed2
                endif

             case('l')
             
                lo=.false.
                hi=.false.
                if(tough) then 
                   lo=lo_closed1
                else
                   lo=lo_closed2
                endif
             
             case default

                lo=.false.
                hi=.false.

          
          end select

          if(hi.or.lo) then

            call checkExtrema(fld,i0,j0,rfind,ishilo)

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


      subroutine checkExtrema(fld,i0,j0,rfind,ishilo)

      use const
      use f77OutputMeta

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
ccc       print*,'iiiii',i,j,i-i0,j-j0,dist2(i,j),rmax2

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
ccc        print*,'local MAX: ',fmax,i0,j0,fmax,imx,jmx
        ishilo=1
      endif

      if( (imn.eq.i0 .and. jmn.eq.j0) .and. (fmin.lt.+1e20)  ) then
ccc        print*,'local min: ',fmin,i0,j0,fmin,imn,jmn
        ishilo=-1
      endif


      return

      end subroutine checkExtrema
      
      subroutine setBounds(i,j,ni,nj)
      if(i.lt.1) i=1
      if(i.gt.ni) i=ni
      if(j.lt.1) j=1
      if(j.gt.nj) j=nj
      return
      end subroutine setBounds



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      subroutine getExtremaProps(fld,
     $     i0,j0,
     $     xhl,yhl,ahl,ghl,lhl,dhl)

      use trkParams
      use f77OutputMeta

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
      



      subroutine conGdat(fixlat,fixlon,
     $     flat,flon,ifixbase,npcon)

      use trkParams

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


      flat=0.0
      flon=0.0
      npcon=0
      
      do i=1,maxfix

        if(valid(i)) then

          dist=distsp(baselat,baselon,fixlat(i),fixlon(i))

          if(dist .lt. rmaxConSep) then
            flat=flat+fixlat(i)
c--       crossing the 0E
            if(fixlon(i).lt.20.0) fixlon(i)=fixlon(i)+360.0
            flon=flon+fixlon(i)
            npcon=npcon+1
          else
            if(verb) then
              print*,'WWW conGdat i: ',i,' dist: ',dist,' fixlat/lon: ',fixlat(i),fixlon(i),
     $             ' baselat/lon: ',baselat,baselon,' ifixbase: ',ifixbase
            endif
          endif

        endif

      enddo
      
      if(npcon.gt.0) then 
        fact=1.0/float(npcon)
        flat=flat*fact
        flon=flon*fact
      endif

      if(npcon.eq.0) then
        flat=fixlat(1)
        flon=fixlon(1)
      endif

c--       make sure 0-360E

      if(flon.ge.360.0) flon=flon-360.0

      if(verb) then
        print*,'CCCCCCCCCCCCCCCCCCC ',npcon,ifixbase,flat,flon
      endif
      return

      end subroutine conGdat

      end module mfutils


