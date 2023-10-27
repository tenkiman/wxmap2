
module const

real, parameter :: pi=3.1415926535897931
real, parameter :: pi4=pi/4.0
real, parameter :: pi2=pi/2.0
real, parameter :: deg2rad=pi/180.0
real, parameter :: rad2deg=1.0/deg2rad

real, parameter :: rearth=6371.0
real, parameter :: earthcircum=2.0*pi*rearth
real, parameter :: earthomega=7.292e-5

real, parameter :: km2nm=60.0/(2*pi*rearth/360.0)
real, parameter :: nm2km=1.0/km2nm
real, parameter :: deglat2km=((2.0*pi*rearth)/360.0)
real, parameter :: deglat2nm=60.0
real, parameter :: km2deglat=1.0/deglat2km
real, parameter :: nm2deglat=1.0/deglat2nm
real, parameter :: knots2ms=1000.0/(km2nm*3600.0)
real, parameter :: yms2knots=1.0/knots2ms
real, parameter :: epsilonm5=1.0e-5
real, parameter :: gravity=9.80665

end module const

module libmf

contains

subroutine stat2(a,m,n,amin,amax,amean,avar,asigma)

  real(kind=4) :: a(m,n)

  amean = 0.0
  amin = 9.9e25
  amax = -9.9e25
  avar = 0.0
  asigma = 0.0
  do i=1,m
     do j=1,n
        if(a(i,j).lt.amin) amin=a(i,j)
        if(a(i,j).gt.amax) amax=a(i,j)
        amean=amean+a(i,j)
     end do
  end do
  amean = amean/m*n
  do i=1,m
     do j=1,n
        avar = avar + (a(i,j)-amean)**2
     end do
  end do
  avar = avar/(m*n-1)
  asigma=sqrt(avar)
  return
  
end subroutine stat2

subroutine qprntn(a,qtitle,ibeg,jbeg,m,n,iskip,iunit)
      
!
!**********	12 APR 91 this version outputs to iunit 
!**********	using write on the Cray Y/MP 
!
!***************************************************************
!***************************************************************
!*****                                                     *****
!*****       qprint output routine (!orrected 4/26/86)     *****
!*****                                                     *****
!***************************************************************
!***************************************************************
!
! a= fwa of m x n array
! qtitle - title
! ibeg,jbeg=lower left corner coords to be printed
! up to 43 x 83 points printed
!
      real(kind=4) a(m,n),ix(81)
      real(kind=4) xm
      character qtitle*24
!
!  determine grid limits
!
      if(iskip.eq.0) iskip=1
      iend=min0(ibeg+79*iskip,m)
      jend=min0(jbeg+79*iskip,n)

      half=0.5
!
   24 continue
!
!  index backwards checking for max
!
   11 xm=0.
      jendsc=min0(jend,n)
      do j=jbeg,jendsc,iskip
      jend_qp = j
      do i=ibeg,iend,iskip
        xm=max(xm*1.d0,abs(a(i,j)))
      end do
      end do
!
!  determine scaling factor limits
!
      if(xm.lt.1.0e-32.or.xm.eq.0.0) xm=99.0
      xm=alog10(99.0/xm)
      kp=xm
      if(xm.lt.0.0)kp=kp-1
!
!  print scaling constants
!
   12 write(iunit,1) qtitle,kp,iskip,(i,i=ibeg,iend,2*iskip)

    1 format('0',a,'   k=',i3,' iskip=',i2,/,' ',41i6) 
      fk=10.0**kp
!
!  quickprint field
!
      do  jli=jend_qp,jbeg,-iskip
         ii= 0
         if(kp.eq.0) then 
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)+sign(half,a(i,jli))
          end do
        else
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)*fk+sign(half,a(i,jli))
          end do
        end if
        write(iunit,'(i4,81i3)') jli,(ix(i),i=1,ii),jli
     enddo
     return
     
end subroutine qprntn

subroutine smth2d(a,ni,nj,ib,ie,jb,je, &
     anu,npass,nnu,ioresp,io,iskip,dx,b,undef)

!...      routine to smooth a 2-d field at subsection of interior points
!...      using a noncomplex shuman (1957) smoother-desmoother 

      real (kind=4) a(ni,nj),b(ni,nj),anu(nnu)
      real (kind=4) pi,rlambda,dx,undef

      logical ioresp,io
      character qtitle*24
      
!...     output unsmoothed field if io.ne.0

      if(io) then
        call stat2(a,ni,nj,amin,amax,amean,avar,asd)
        write(6,12) amean,amin,amax,avar,asd
12      format(' ',/,' ',' input field mean = ',1pe13.4,/ &
            ' ','             amin = ',1pe13.4,/ &
            ' ','             amax = ',1pe13.4,/ &
            ' ','         variance = ',1pe13.4,/ &
            ' ','         stnd dev = ',1pe13.4,//) 
        qtitle='raw field                '
        call qprntn(a,qtitle,1,1,ni,nj,iskip,6)

      end if

!         mmmmmmmmmmmmmmmmm main loops, npass, the nus 

      do nn=1,npass

        do l=1,nnu

          do i=ib,ie
            do j=jb,je

              if( &
                  a(i,j).eq.undef.or. &
                  a(i+1,j).eq.undef.or. &
                  a(i-1,j).eq.undef.or. &
                  a(i,j-1).eq.undef.or. &
                  a(i,j+1).eq.undef.or. &
                  a(i+1,j+1).eq.undef.or. &
                  a(i+1,j-1).eq.undef.or. &
                  a(i-1,j-1).eq.undef.or. &
                  a(i-1,j+1).eq.undef &
                  ) then
                b(i,j)=a(i,j)

              else

                b(i,j)=a(i,j)*(1.0-anu(l))**2 &
                    + 0.5*anu(l)*(1.0-anu(l))* &
                    (a(i+1,j)+a(i-1,j)+a(i,j+1)+a(i,j-1)) &
                    + 0.25*(anu(l)**2)* &
                    (a(i-1,j-1)+a(i-1,j+1)+a(i+1,j-1)+a(i+1,j+1))
             endif
            end do
          end do

          do i=ib,ie
            do j=jb,je
              a(i,j)=b(i,j)
            end do
          end do

        end do 

      end do

      if(ioresp) then

        write(6,200) npass,nnu 
200     format(' ',//,' ','smoothing function analysis'/ &
         ' ',5x,'number of passes = ',i2/ &
         ' ',5x,'number of elements per pass = ',i2)
        do k=1,nnu
          write(6,201) k,anu(k)
201       format(' ',7x,'k = ',i2, &
       '  smoothing coefficient nu = ',f6.3)
        end do

        pi=4.0*atan(1.0)

        do i=2,ni
          b(i,1)=float(i)
          b(i,2)=1.0
          do mm=1,nnu
            b(i,2)=b(i,2)*(1.0-anu(mm)*(1.0-cos(2.0*pi/float(i))))
          end do

          b(i,2)=b(i,2)**npass
        end do

!
        write(6,222)
222     format(' ','response function as a function of wavelength ', &
         'in grid units*dx',//, &
         ' ','  lambda  response  ',//)
!
        do i=2,ni
          rlambda=dx*i
          write(6,225) rlambda,b(i,2)
225       format(' ',f7.1,3x,f6.3)
        end do

      end if 

      return

end subroutine smth2d

end module libmf


program rdovar

  use const
  use libmf

  character(120)           :: glvldir,gpath,dfile,dpath
  character(16)            :: gheader
  character(80)            :: header(10)
  character                :: VarName*4,dtg*12


  real(kind=4), allocatable :: lat(:),lon(:)
  real(kind=4), allocatable :: out_var(:,:)

  integer                  :: iunitglvl,its,time,dim1,nip,ipt

  namelist /RDOVARnamelist/ glvldir,dfile

  integer        :: glvl                                   ! The grid level defined in the Makefile
  integer        :: SubdivNum(20)                          ! Subdivision numbers for each recursive refinement(2: bisection, 3: trisection, etc.)
  integer        :: nvl                                    ! Number of vertical native levels

  namelist /CNTLnamelist/ glvl, SubdivNum, nvl


  OPEN(12,file="rdovar.nl")
  read(12, nml=RDOVARnamelist)
  write(*,nml=RDOVARnamelist)
  close(12)

  print*,trim(glvldir)//'FIMnamelist'
  OPEN (10,file=trim(glvldir)//'FIMnamelist')
  READ (10,NML=CNTLnamelist)
  close(10)

  iunitglvl=10
  
  gpath=trim(glvldir)//'glvl.dat'
  dpath=trim(glvldir)//trim(dfile)

  print*,'dddddd ',dpath

  open(12,file=dpath,form='unformatted',status='old',err=800)
  read(12) header

  do i=1,10
     print*,i,header(i)
  enddo

  

read(header(1),'(4x,a4,36x,A12)') VarName,dtg
read(header(2),'(6x,I2,8x,i1,7x,I1,2x,i1,6x,i1)') nvl,glvl,its,time
read(header(3),'(5x,i2,6x,i6)') dim1,nip
print*,VarName,dtg,nvl,glvl,its,time
print*,'dim1,nip ',dim1,nip

  allocate (out_var(dim1,nip),stat=irc)
  print*, 'out_var allocate irc = ',irc,' dim1,nip: ',dim1,nip

  read(12) out_var
  close(12)

  

  print*,'gggggg ',gpath

  allocate (lat(nip),lon(nip),stat=irc)
  print*, 'lat,lon allocate irc = ',irc,' nip: ',nip


  !
  !  read in the glvl.dat for lat/lons
  !
  open(iunitglvl,file=gpath,form='unformatted',status='old',err=800)
  
  read(iunitglvl) gheader
  print*,'h1 ',gheader
  read(iunitglvl) gheader

  print*,'h2 ',gheader
  read(iunitglvl) lat
  read(iunitglvl) lon
  close(iunitglvl)

  print*,'HHHHHHHHHHHHHHHHH ',gheader

  do i=1,10
     write(*,'(i3,2x,2(g13.8,1x,g13.8))') i,lat(i),lon(i)
  enddo
  

ipt=1

  print*,' ipt: ',ipt,' lat/lon: ',lat(ipt)*rad2deg,lon(ipt)*rad2deg
  do k=1,dim1
     write(*,'(i3,2x,f13.3)') k,out_var(k,ipt)
  enddo


  stop

  goto 900
800 continue
  print*,'error in open of g?glvl.dat'
  
801 continue
  print*,'error in open of topo.dat'
  
  
802 continue
  print*,'read end'
  
803 continue
  print*,'read err'
  
900 continue
  stop

end program rdovar






