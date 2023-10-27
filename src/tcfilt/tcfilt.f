      program tcfilt
c         
      include 'params.h'
      include 'tctype.h'

      parameter (kmax=18,lgi=20)
      parameter (iblkmx=lgi*ni+4*kmax*ni)
      parameter (jblkmx=ni+14*kmax*ni)
      parameter (mxtim=7,mxprm=10,mxlvl=18)
      parameter (imin=0,jmin=0)

      common /winds/ dmmm(ni,nj,2),tang(ni,nj),
     $     del(ni,nj),tha(ni,nj),tanp(ni,nj),ds(ni,nj)

      common /gdinf/ ngd,ngr,ntr,dt,js,jn,ie,iw,iimax,imax,jjmax,
     $     jmax,nstflg,icx,icy,ihx,ihy,dftx,dfty

      common /pass/ rtani(ini,nmx),disti(nmx)

      common /var/  dist,nn1,nn2,nn3,nn4,ifl

      common /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,ix,iy

      common /total/ ddel,dtha

      common /ifact/ nnn,r0vect(nmx),rb,ienv

      common /matrix/ a(nmx,nmx),capd2

      dimension facg1(ni),facg2(ni)
      dimension filc(iblkmx),fact1(ni),fact2(ni)
      dimension diag(jblkmx),u(ni,nj),v(ni,nj)
      dimension xxd(ni,nj),us(ni,nj),vs(ni,nj), xxdu(ni,nj)
      dimension uall(ni,nj),vall(ni,nj)
      dimension xhu(ni,nj),xzerou(ni,nj)
      dimension xhv(ni,nj),xzerov(ni,nj)
      dimension up(ni,nj),vp(ni,nj)
      dimension ufils(ni,nj),vfils(ni,nj)
      dimension ufil(ni,nj),vfil(ni,nj)
      dimension ufilp(ni,nj),vfilp(ni,nj)
      dimension uf850(ni,nj),vf850(ni,nj)

      dimension zmattemp(imin:ni,jmin:nj)

      dimension ivrbl(22)
c         
      character*4 iblock, parm
      character*4 param4(mxprm)
      character*7 level(kmax)

      character tcppath*128,tcvpath*128,tcipath*128,tcopath*128
      character copt1*8,copt2*8,copt3*8,capdopt*8

      logical verb,finalonly,maxr0,meanr0

      type (TC) , dimension(10) :: TCs

      data level /'1000 mb',' 975 mb',' 925 mb',' 900 mb',' 850 mb',
     1     ' 700 mb',' 500 mb',' 400 mb',' 300 mb',' 250 mb',
     2     ' 200 mb',' 150 mb',' 100 mb','  70 mb','  50 mb',
     3     '  30 mb','  20 mb','  10 mb'/
c         
c         
      data param4 /'pmsl','tmpc','vapr','uwnd','vwnd',
     1     'hght','tmpc','vapr','uwnd','vwnd'/

      data ivrbl /1,1,6,6,6,6,6,6,6,6,6,5,6,5,5,5,5,5,2,2,2,2/

C         
C         constants 
C
      include 'const.h'

c         
c######################################################################
c         
c         the following is the code to remove the hurricane component of the
c         disturbance field from a given wind field.
c         the resulting field is called the "environmental field"
c         in the gfdl bogus system,  the specified vortex is added to this
c         resulting wind field to optain the final initial field.
c         
c         first, input the center of the storm called xv ,yv which is
c         defined in lines 86-87 of the code.
c         this will center an 11 x 11 degree gridpoint square within which
c         the global center will be defined (in routine "center").
c         this routine will determine the global center, first based on the
c         centroid center, as defined in:  kurihara, bender, and ross (1993)
c         mwr, page 2039, equation (6.1).
c         
c         next, the global center is redefined as the gridpoint with the
c         largest azimuthally-averaged wind maximum.
c         
c         next, the parameter dist(ir) is defined, as the starting location
c         of the search for r0 (the filter domain) in the various aximuthal
c         directions.
c         lastly, the non-hurricane wind within ro is determined from an
c         optimum interpolation approach.
c         
c         
c         important: we assume that the grid spacing of the grid points is
c         one degree (dlon,dlat).
c         
c#######################################################################

C         
C         defaults
C

      verb=.false.
      finalonly=.false.
      finalonly=.true.
      maxr0=.false.

      ifl=3
      copt1=''
      copt2=''
      copt3=''
      capdopt=''
      capddefault=12.0

      iunittcp=10
      iunittcv=12
      iunittco=14

Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
C         
C         command line processing
C
Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      call getarg(1,tcppath)
      call getarg(2,tcvpath)
      call getarg(3,tcipath)
      call getarg(4,tcopath)
      call getarg(5,capdopt)
      call getarg(6,copt1) 
      call getarg(7,copt2) 
      call getarg(8,copt3) 

      narg=iargc()
      
      if(narg.lt.5) then

        print*,'Arguments to tcfilt.x:'
        print*,' '
        print*,'     tcppath : path to input TC posit namelist data file (w2.tc.tc.filt.py)'
        print*,'     tcvpath : path to input wind field data file (850 wind)'
        print*,'     tcipath : path to input field to be vortectomised'
        print*,'     tcopath : path to output filtered fields file'
        print*,'        capd : D in wij = kuri et al 1995 p.2793'
        print*,' '
        print*,' [copt1,2,3] : -ifl=   ; basic field filter strengh default is: ',ifl
        print*,' [copt1,2,3] : -v      ; set verb=.true. '
        print*,' [copt1,2,3] : -oa     ; set finalonly=.false :: output all fields not just vortectomised'
        print*,' [copt1,2,3] : -maxr0  ; use max r0 vice local value; max vortex removald'
        print*,' [copt1,2,3] : -meanr0 ; use mean r0 vice max r0 to initialise in separ.f'
        print*,' '
        print*,'Example'
        print*,' '
        print*,'tcfilt.x /tmp/n.txt uv.850.dat psl.dat uv.850.tcfilt.dat -ifl=4 -oa'
        print*,' '
        stop 

      endif

      if(copt1(1:5).eq.'-ifl='.or.copt2(1:5).eq.'-ifl='.or.
     $     copt3(1:5).eq.'-ifl=') then
        read(copt1(6:6),'(i1)') ifl
        print*,'WWWWW setting ifl at command line'
        print*,'WWWWW ifl = ',ifl
      endif

      if(copt1(1:2).eq.'-v'.or.copt2(1:2).eq.'-v'.or.
     $     copt3(1:2).eq.'-v') then
        print*,'WWWWW setting verbose to true'
        verb=.true.
      endif

      if(copt1(1:3).eq.'-oa'.or.copt2(1:3).eq.'-oa'.or.
     $     copt3(1:3).eq.'-oa') then
        print*,'WWWWW setting to output all fields, not just the vortectomised'
        finalonly=.false.
      endif
      if(copt1(1:6).eq.'-maxr0'.or.copt2(1:6).eq.'-maxr0'.or.
     $     copt3(1:6).eq.'-maxr0') then
        print*,'WWWWW setting to r0 to maxr0 to maximise vortex removal'
        maxr0=.true.
      endif

      if(copt1(1:7).eq.'-meanr0'.or.copt2(1:7).eq.'-meanr0'.or.
     $     copt3(1:7).eq.'-meanr0') then
        print*,'WWWWW setting to r0 to meanr0 vice maxr0'
        meanr0=.true.
      endif

      if(capdopt.ne.''.and.capdopt.ne.'def') then
        read(capdopt,'(f8.1)') capd
        print*,'capdopt = ',capdopt,capd
      else
        capd=capddefault
      endif

      capd2=capd*capd

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C         
C         open files
C
Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

      open(iunittcp,file=tcppath(1:ichlen(tcppath,128)),
     $     status='old',err=810)

      open(iunittcv,file=tcvpath(1:ichlen(tcvpath,128)),
     $     status='old',access='direct',recl=ni*nj*4,err=820)

      open(iunittci,file=tcipath(1:ichlen(tcipath,128)),
     $     status='old',access='direct',recl=ni*nj*4,err=830)

      open(iunittco,file=tcopath(1:ichlen(tcopath,128)),
     $     status='unknown',access='direct',recl=ni*nj*4,err=840)

Ctttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
C
C         read in tcs
C         
Ctttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt

      call tcread(iunittcp,ntc,TCs,verb)
      if(verb) then
        do i=1,ntc
          print*,'i = ',i,TCs(i)%stmid,TCs(i)%lat,TCs(i)%lon
        end do
      endif

c         
cc****************setup the filter strength you want***************
c         
c         this is the first filter, which seperates the disturbance wind
c         field from the basic flow.  the basic flow will be defined as
c         (us, vs).
c         
cc        see the subroutine phase for details.
cc        
cc        ifl=1   is the weak    filter
cc        ifl=2   is the regular filter
cc        ifl=3   is the strong  filter DEFAULT
cc        ifl=4   is very strong filter
cc        
cc        filter is defined in mwr paper of kurihara, et.all, 1990:
C
c**************************************************************
c         
c         ddel, dtha is the grid spacing (should be 1 degree for the filter
c         characteristics to properly work)
c         these are inputed in radians !!!!
c         
c         del : is the 2-d array containing longtitude in radians of the gr
c         tha : is the 2-d array containing latitude   in radians
c         
c         ds :  is the area contained with one grid point
c         this is used in routine ....center.... for the first guess
c         of the global center (which is a centroid calculation).
c         
c         u :  is the u component of the wind used to define ro
c         v :  is the v component of the wind used to define ro
c         ufil :      u component of the wind used to be filtered
c         vfil :      v component of the wind used to be filtered
c         
c**************************************************************

      dr=0.1

C        
C         input wind field to calc TC/nonTC region
C         

      read(iunittcv,rec=1,err=860) ufil
      read(iunittcv,rec=2,err=860) vfil

      close (iunittcv)

      j=0
      rlon11=0.0
      rlat11=-90.0

      do jj=1,nj
        j=j+1
        ddel=pi180
        dtha=pi180

        do i=1,ni
          ds(i,j)=1.0
          del(i,j)=(rlon11 + (float(i-1))) * ddel
          tha(i,j)=(rlat11 + (float(j-1))) * dtha

          u(i,j)  =ufil(i,j)
          uall(i,j)  =ufil(i,j)
          v(i,j)  =vfil(i,j)
          vall(i,j)  =vfil(i,j)

        end do
      end do

      xcorn=del(1,1)/pi180
      ycorn=tha(1,1)/pi180


c         
c         obtain the basic flow field for the wind (u,v)
c         

      call phase(ifl,ufil,vfil,ufils,vfils)

      
      if(verb) then
        call findmx2(ufil,rmax,rmin,ni,nj,maxi,maxj,mini,minj)
        print *,'max ufil ',rmax,' at ',maxi,maxj
        print *,'min ufil ',rmin,' at ',mini,minj

        call findmx2(vfil,rmax,rmin,ni,nj,maxi,maxj,mini,minj)
        print *,'max vfil ',rmax,' at ',maxi,maxj
        print *,'min vfil ',rmin,' at ',mini,minj

        call findmx2(ufils,rmax,rmin,ni,nj,maxi,maxj,mini,minj)
        print *,'max ufils ',rmax,' at ',maxi,maxj
        print *,'min ufils ',rmin,' at ',mini,minj

        call findmx2(vfils,rmax,rmin,ni,nj,maxi,maxj,mini,minj)
        print *,'max vfils ',rmax,' at ',maxi,maxj
        print *,'min vfils ',rmin,' at ',mini,minj
      endif


c         
c         preserve 850 mb vortex structure
c         

      do j=1,nj
        do i =1,ni
          uf850(i,j)=ufil(i,j)-ufils(i,j)
          vf850(i,j)=vfil(i,j)-vfils(i,j)
        end do
      end do

C         
C...      create 0.0 array to save only non-hurr part of disturbance
C..       only around the TCs
C
      do j=1,nj
        do i=1,ni
          xzerou(i,j)=0.0
        end do
      end do
      
      ireco=1

c####################################################################################
c         
c         next find the center position of the global vortex and r0vect
c         
c         obtain the total disturbance field:
c         

      nfld=0

      do while(nfld.lt.999999)

        nfld=nfld+1
ccc        read(iunittci,rec=nfld,err=900,end=900) ufil
        read(iunittci,rec=nfld,err=850) ufil

        print*,'PPPPPPPPPPPPP nfld = ',nfld

        call bsmooth(ifl,ufil,ufils)
        
        do l=1,ntc

          xv=TCs(l)%lon
          yv=TCs(l)%lat

          xc=xv*pi180
          yc=yv*pi180


          do j=1,nj
            do i=1,ni
              ufilp(i,j)=ufil(i,j) - ufils(i,j)
            end do
          end do

          if(l.eq.1.and.(.not.finalonly)) then
            write(iunittco,rec=ireco) ufil
            ireco=ireco+1
          endif

          if(l.eq.1.and.(.not.finalonly)) then
            write(iunittco,rec=ireco) ufils
            ireco=ireco+1
            write(iunittco,rec=ireco) ufilp
            ireco=ireco+1
          end if

          
c         first find the center position of the global vortex
c         this is the centroid calculation...........
c         
c----------------------------------------------------------

          call center(uf850,vf850,xcg,ycg)

          if(verb) print *,'--- locating center, xcf,ycg=',xcg,ycg

          xcg850=xcg
          ycg850=ycg

          xold=xcg
          yold=ycg

c         
c         adjust the center position of the global vortex
c         
          if(verb) print*,'before maxth', xold,yold

          call maxth(uf850,vf850,xcg850,ycg850,rmxlim,tanp)
          xcgnew=xcg850
          ycgnew=ycg850

          if(verb) then
            print *,'after maxth...'
            print *,'xcgnew=',xcgnew,'ycgnew=',ycgnew
            print *,'rmxlim=',rmxlim

            call findmx2(tanp,rmax,rmin,ni,nj,maxi,maxj,mini,minj)
            print *,'max tanp ',rmax,' at ',maxi,maxj
            print *,'min tanp ',rmin,' at ',mini,minj
          endif

          xold=xcgnew+xcorn
          yold=ycgnew+ycorn

          dist=rmxlim

          xcp=xold*pi180
          ycp=yold*pi180

c         now determine the r0vect of the global vortex
c         
c         loop over nmx azimuthal directions
c         first compute the radial profiles of tangential wind for the
c         nmx  azimuthal angles
c         

          dxc=xold-xcorn
          dyc=yold-ycorn

c-----------------------------------------------------------
c         save 850 mb vortex representation
c-------------------------------------------------------------

c         
c         calculate the radial profile of tangential wind for 24 axumuthal
c         angles
c         
          call calct(dr,dxc,dyc,ycp,tanp,rmxlim)

          if(verb) print *,'**** checking for r0 ****'

          do 10 iang=1,nmx

            x1=0.0
            rtan1=100000.
            r=1.0
            dist=disti(iang)
            if(verb) print *,'iang=',iang,' dist=',dist
c         
c         only return to 666 if rtan > 6m/s
c         
 666        continue

            rtan1=100000.0
c         
c         return to 777 if dist or grad condition not met
c         

 777        continue

            irdex=int(r/dr)
            rtan=rtani(irdex,iang)
            r=r+dr

            rtan2=rtan

            if(rtan.gt.3.0) go to 666
            
            if(verb) then
              print*,'a-rtan1=',rtan1,' rtan=',rtan,' dist=',dist,' x1=',x1
            endif

            if(rtan2.ge.rtan1.and.r.gt.dist.and.x1.gt.0.5) go to 669

            if(rtan2.ge.rtan1.and.r.gt.dist)then
              x1=1.0
            endif

            if(rtan.lt.3..and.r.gt.dist) go to 669
            rtan1=rtan -4.0

            if(verb) then
              print *,'reduced rtan1 to ',rtan1,' r=',r
            endif
            
            if(r.lt.10.8) go to 777

 669        continue

            if(x1.eq.1.0) then
              r0vect(iang)=(r-0.1)/0.8
            else
              r0vect(iang)= r/0.8
            endif

            rzr=dist

 1999       continue

            rzr=rzr + dr

            irdex=int(rzr/dr)
            rtan=rtani(irdex,iang)
            if(rtan.gt.0.0) go to 1999
c         
            rzrn=rzr
            rzr=rzr*111.19493

            rrdd=r0vect(iang)*111.19493
            
            if(rrdd.gt.rzr) then
              if(verb) then
                print*,'r0 has a negative tangential component'
                print*,'r0 was defined as:  ',rrdd
                print*,'r0 will be modified to: ',rzr
              endif
              rrdd=rzr
              r0vect(iang)=rzrn
            endif

            r0maxkm=1600.0

            if(rrdd.gt.r0maxkm) then
              if(verb) print*,'wwwww r0 > r0vectmax resetting....'
              rrdd=r0maxkm
              r0vect(iang)=rrdd/111.19493
            endif

            r0fact=1.0
            r0vect(iang)=r0vect(iang)*r0fact
            rrdd=r0vect(iang)*111.19493

            if(nfld.eq.1.and.mod(iang,6).eq.0.or.verb) then
              write(*,'(a,2x,i5,2x,i5,2x,f5.1,2x,a3,2x,i3)') 
     $             'FINAL r0 in km:  ',
     $             nint(rrdd),iang,r0vect(iang),TCs(l)%stmid,TCs(l)%vmax
            endif

 10       continue

c################################################################
c         
c         
c         do the optimum interpolation......>>>>>
c         
          call rodist
c         
c         
c         create matrix  [a]  containing the distance-related correlations
c         between the 24 boundary points just outside of the filter domain
c         r0......
c         
c         
          call amatrix

          if(verb) then
            call findmx2(a,rmax,rmin,nmx,nmx,maxi,maxj,mini,minj)
            print *,'max a ',rmax,' at ',maxi,maxj
            print *,'min a ',rmin,' at ',mini,minj
          endif

c         
c         seperate the disturbance into the hurricane and non-hurricane
c         components
c         

          do j=1,nj
            do i=1,ni
              xxd(i,j)=ufil(i,j) - ufils(i,j)
            end do
          end do

          call separ(xxd,xhu,xzerou,maxr0,meanr0)

          do j=1,nj
            do i=1,ni
              ufil(i,j) = ufils(i,j) +  xxd(i,j)
              xxdu(i,j)=xxd(i,j)
            end do
          end do

          if(l.eq.ntc.and.(.not.finalonly)) then
            write(iunittco,rec=ireco) xxd
            ireco=ireco+1
            write(iunittco,rec=ireco) xhu
            ireco=ireco+1
            write(iunittco,rec=ireco) xzerou
            ireco=ireco+1
          endif

          if(l.eq.ntc) then
            write(iunittco,rec=ireco) ufil
            ireco=ireco+1
          endif

          if(verb) then
            call findmx2(ufil,rmax,rmin,ni,nj,maxi,maxj,mini,minj)
            print *,'max ufil ',rmax,' at ',maxi,maxj
            print *,'min ufil ',rmin,' at ',mini,minj
          end if

        end do                  ! end of TC loop

      end do                    ! end of field loop


 850  continue
      if(nfld.gt.1) go to 900
      print*,'EEEE reading input fields to vortectomise: ',tcipath(1:ichlen(tcipath,128))
      stop '850'

 860  continue
      if(nfld.gt.1) go to 900
      print*,'EEEE reading input fields to vortectomise: ',tcipath(1:ichlen(tcipath,128))
      stop '860'


 900  continue
C         
C         all done!!
C         
      nfld=nfld-1
      print*,'PPPPPPPPPPPPP nfld= ',nfld

      go to 999

 810  continue
      print*,'EEEE unable to open TC posit input: ',tcppath
      stop '810'
      go to 999

 820  continue
      print*,'EEEE unable to open wind input: ',tcvpath
      stop '820'
      go to 999

 830  continue
      print*,'EEEE unable to open field input: ',tcipath(1:ichlen(tcipath,128))
      stop '830'
      go to 999

 840  continue
      print*,'EEEE unable to open field output: ',tcopath
      stop '830'
      go to 999


 999  continue

      stop
      end

