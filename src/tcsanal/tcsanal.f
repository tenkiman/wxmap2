      program tcscanal

      integer ni, nj, maxtc, numvar, maxhr, dtau, maxhour
      integer iflg
      real dlat,dlon,rearth

      parameter (ni=360,nj=181,nk=2,ntcf=13,ntcs=12)
      parameter(dlat=1.0,dlon=1.0,rearth=6363*1e3)

      parameter(dphi=10.0,nphi=nint(360.0/dphi))
      parameter(dr=10.0,rmax=1000.0,nr=nint(rmax/dr)+1,dt=12.0,speed=dr/dt)
      parameter(nq=5)

      real tclat,tclon,tcstruct

      common /struct/ 
     $     tclat(ntcf),tclon(ntcf),tcstruct(ntcs)

      include 'params.h'

      namelist /parameters/ spdcrit,vcrit,levwind,verb
      namelist /paths/ tcapath,tcspath,tcfpath,tcopath,tcdpath,tcppath

      integer iunittca,iunittcs,iunittcf,iunittco,iunittcd
      integer narg
      integer ichlen,iargc

      character*16 cdtg
      character tcapath*128,tcspath*128,tcfpath*128,
     $     tcmpath*128,tcopath*128,tcdpath*128,tcppath*128,
     $     nlpath*128
      character copt*2
      character id*8
c
      real ua(ni,nj,nk),va(ni,nj,nk),dum(ni,nj)

      character*10 dlonmaxopt,vortcritopt
C         
C         tca - adeck input
C         tcs - structure input
C         tcf - field input
C         tco - obs output (grads station data)
C         tcd - diag output
C         tcp - radial profiles (grads gridded data)
C


      iunittca=10
      iunittcs=12
      iunittcf=14
      iunittco=16
      iunittcd=18
      iunittcp=20
      iunitnl=11

      call cmdline(nlpath,copt)

Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C         namelist
Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

      open(iunitnl,file=nlpath(1:ichlen(nlpath,128)),
     $     status='old',err=802)

      read(11,parameters)
      read(11,paths)

      call ofiles(iunittca,iunittcs,iunittcf,iunittco,iunittcd,iunittcp,
     $     ni,nj,tcapath,tcspath,tcfpath,tcopath,tcdpath,tcppath)

      call readadeck(iunittca,tclat,tclon,ntcf,nposits)

      call readtcstruct(iunittcs,tcstruct,ntcs)

      if(verb) then
        print*,'spdcrit = ',spdcrit
        print*,'  vcrit = ',vcrit
        print*,'nposits = ',nposits
      endif

      do nt=1,nposits
        call readfld(iunittcf,ua,va,ni,nj,nk,nt,ierr)
        call analtc(ua,va,nt,iunittco,iunittcd,iunittcp)
      end do

C         
C         write out end of time record
C         
      write(id,'(i7,a1)') -999,'\0'
      rlon=0.0
      rlat=0.0
      rt=0.0
      nlev=0
      write(iunittco) id,tclat(1),tclon(1),rt,nlev,iflag

      close(iunittco)

      go to 999

 802  continue
      print*,'error opening input namelist file'
      print*,nlpath
      stop 802


 999  continue
      stop
      end




      function ichlen(c,imax)
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
      end
