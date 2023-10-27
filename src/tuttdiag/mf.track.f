      subroutine mftrack (spd,vort,psl,
     $     rtau,ktau,
     $     nwrt,tcyc,numv,
     &     mxhr,nbog,ntrk,ierr)

      use trkParams
      use mfutils
      use f77outputmeta

      implicit none

      real*4 spd(ni,nj),vort(ni,nj),psl(ni,nj),rtau

      real rlatc,rlonc,rdir,rspd

      integer numv, mxhr, nbog, ktau, ntrk

      character*28 tcyc(maxtc+1)

c
c         local variables

      integer idgrid, irecnum, istatus, len, nwrt
      integer ib,ie,jb,je
      integer i,j,n,kc,kcl,kclp1,ierr

      real pcntile

      real dlatlon
      real egxx,egyy


      character*8  seclvl
      character*24 dsetnam, dsets(2), typlvl
      character*32 typmodl, geonam, params(2), units
      character*80 title
      character*24 qtitle
      character oformat*24

      logical verb,toughpsl,tough

c--       closed extrema test

      tough=.true.
      toughpsl=.false.

      verb=verbMftrack

c--       expand the search grid
c
      dlatlon=dlonmax*1.00

      if(verb)  nwrt=6

      oformat="g10.4"
      pcntile=0.7



C         
C...      convert spd*spd to knot
C         
      do i=1,ni
        do j=1,nj
          if(spd(i,j).lt.0) go to 810
          spd(i,j)=sqrt(spd(i,j))*1.9454
        end do
      end do

      if(verb) then
        qtitle='spd in mftrack [kt]    '
        call qprntn(spd,qtitle,1,1,ni,nj,10,6)

        qtitle='vrt in mftrack [s-1]   '
        call qprntn(vort,qtitle,1,1,ni,nj,10,6)
      end if
      

      kc=1+ktau/dtau
      kcl=kc-1
      kclp1=kc

      if(rtau.eq.0.0) kclp1=0

      if(nbog.gt.0) then
        do n=1,nbog
          rlatc=gdat(1,kclp1,n,0)
          rlonc=gdat(2,kclp1,n,0)
          rdir=gdat(5,kclp1,n,0)
          rspd=gdat(6,kclp1,n,0)

          if((rlatc.lt.90).and.(rlonc.lt.900)) then

C--       set search limit +- 10 grid points
C

            ib=(rlonc-blon)/dlon - 10
            ie=ib+20
            jb=(rlatc-blat)/dlat - 10
            je=jb+20

c--       use search box; find x,y of rlatc,rlonc
c

            call clltxy (rlatc,rlonc,
     $           blat,blon,dlat,dlon,ni,nj,
     $           egxx,egyy,
     $           ierr)

c--       get box bounds
c         

            call getIJrange(egyy,egxx,
     $           dlonmax,
     $           ib,ie,jb,je)



            write(nwrt,
     $           '(a,f7.1,2x,2a,2x,2(f8.1,2x))')
     $           'SPD tau: ',rtau,
     $           'storm: ',tcyc(n)(1:3),
     $           rlonc,rlatc

            call grhilo_proc(spd,
     $           ib,ie,jb,je,
     $           rlatc,rlonc,tough,
     $           nwrt,oformat,pcntile)
            
            write(nwrt,
     $           '(a,f7.1,2x,2a,2x,2(f8.1,2x))')
     $           'VRT tau: ',rtau,
     $           'storm: ',tcyc(n)(1:3),
     $           rlonc,rlatc

            call grhilo_proc(vort,
     $           ib,ie,jb,je,
     $           rlatc,rlonc,tough,
     $           nwrt,oformat,pcntile)
            
            write(nwrt,
     $           '(a,f7.1,2x,2a,2x,2(f8.1,2x))')
     $           'PSL tau: ',rtau,
     $           'storm: ',tcyc(n)(1:3),
     $           rlonc,rlatc

c--       use a different extrema test for psl -- tough=.false.

            call grhilo_proc(psl,
     $           ib,ie,jb,je,
     $           rlatc,rlonc,toughpsl,
     $           nwrt,oformat,pcntile)
            
          end if

        end do
        
      end if
      
      ierr=0

      return

 810  continue
      print*, 'spd < 0 at i,j = ',i,j,' val = ',spd(i,j)
      stop 810
c
      end
