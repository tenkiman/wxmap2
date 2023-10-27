      subroutine symasym(totfld,symcmp,symfld,asymfld,
     1      fxx,fyy,tp3,dout,xin,yin,pix,pjy,tp1,tp2,
     2      ipt,jpt,work1,work2,ibitc,xint,uint,gint,
     3      m,n,mc,nc,mx,nx,mcnc,rimax,rjmax,
     4      dx,dxc,dtheta,ibsub,iesub,jbsub,jesub)
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****      routine to find the symmetric/asymmetric       *****
c*****               component of a field                  *****
c*****                                                     *****
c*****     method:                                         *****
c*****                                                     *****
c*****   1)  interpolate to a cylindrical grid using       *****
c*****       bicubic splines;                              *****
c*****                                                     *****
c*****   2)  average in theta to get the symmetric         *****
c*****       component as a function of radius;            *****
c*****                                                     *****
c*****   3)  subtract from the input field grid            *****
c*****       for the asymmetric component                  *****
c*****                                                     *****
c*****   4)  specify the symmetric and asymmetric          *****
c*****       components on a cartesian subgrid             *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
c...        input/output arrays
c
      dimension totfld(m,n),symcmp(mc),symfld(mx,nx),asymfld(mx,nx)
c
c...        arrays for the bicubic spline
c
      dimension fxx(m,n),fyy(m,n),tp3(m,n),dout(mc,nc),
     1          xin(mcnc),yin(mcnc),pix(mcnc,4), 
     1          pjy(mcnc,4),tp1(mcnc,4),tp2(mcnc,4),
     2          ipt(mcnc),jpt(mcnc),work1(2*n),work2(2*m)
c
c...        arrays for the bessel interpolator
c
      dimension ibitc(mc,nc),xint(mc),uint(1),gint(1)
c
c...        arrays for 1-d smoother and ncar interpolator
c
      dimension anu(4),vtempc(250),tempc(250),yp(250)
c
c...        constants
c
      pi=4.0*atan(1.0)
      deg2rad=pi/180.0
      dxfac=dx/dxc 
c
      mn=m*n
      mxnx=mx*nx
c
c*****      define the cylindral coordinate grid 
c
c...        find the location of the points on the
c...        cylindrical grid w.r.t. the cartisean grid
c
c...        (1,1) of the cylindrical grid is the center
c
      icnt=0
      do 100 j=1,nc
      do 100 i=1,mc
      icnt=icnt+1
      radius=(i-1)*dxc
      theta=(j-1)*dtheta
      xi=radius*cos(theta*deg2rad)
      yj=radius*sin(theta*deg2rad)
      xi=xi/dx
      yj=yj/dx
c
c...      limit checks
c
      ibitc(i,j)=1 
      imaxcg=m/2-3 
      jmaxcg=n/2-3 
      ixi=ifix(xi) 
      iyj=ifix(yj) 
      if(abs(ixi).gt.imaxcg.or.abs(iyj).gt.jmaxcg) then
      ibitc(i,j)=0 
      xi=0.0
      jy=0.0
      end if
c
c...      add in center position and put in appropriate array
c
      xin(icnt)=xi+rimax
      yin(icnt)=yj+rjmax
100   continue
c
c*******    interpolate from the input cartesian grid
c*******    to the cyclindrical grid using
c*******    the bicubic spline interpolator
c
c...        ibd is set to 2 in bicubk because we used
c...        cyclic continuity in the i direction 
c
      ibd=2
      ikeep=0
c
      call bicubk(totfld,m,n,dout,mc,nc,mcnc,xin,yin,pix,pjy,
     1        tp1,tp2,tp3,fxx,fyy,ipt,jpt,work1,work2,ibd,ikeep)
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****        radially symmetric part of the field         *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
      do 200 i=1,mc
      atot=0.0
      icnt=0
      do 210 j=1,nc
      if(ibitc(i,j).eq.1) then
      icnt=icnt+1
      atot=atot+dout(i,j)
      end if
210   continue
c
c...     define the x coordinate for ncar interoplating routines
c
      xint(i)=i-1
      if(icnt.ne.0) then
      symcmp(i)=atot/icnt
      else
      symcmp(i)=0.0
      end if
c
      rad=dxc*(i-1)
c      print 206,i,icnt,rad,symcmp(i)
206   format(' ',' i = ',i3,'  icnt = ',i4,'  rad = ',1pe10.3,
     1  '  sym comp = ',1pe10.3)
200   continue
c
c******     smooth the symmetric psi at the outer boundary 
c
c...        limits of the smoothing
c
      ilsmth=8
      ibsmth=mc-ilsmth-1
      iesmth=mc-1
c
c...        set the outer psi to a value in the interior
c
      symcmp(mc)=symcmp(ibsmth+(ilsmth/2))
      anu(1)=0.5
      anu(1)=0.5
      numbnu=2
      npass=50
      iosmth=0
      call smth1d(symcmp,mc,ibsmth,iesmth,anu,npass,numbnu,
     1  iosmth,vtempc)
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****   symmetric and asymmetric component of the field   *****
c*****             on the cartesian subgrid                *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
      symfld(1,1;mxnx)=0.0
      asymfld(1,1;mxnx)=0.0
c
c...        set up the ncar interpolator
c
      sigma=-1.0
      call curv1(mc,xint,symcmp,slp1,slph,yp,tempc,sigma)
      do 300 i=ibsub,iesub
      do 300 j=jbsub,jesub
      ii=i-ibsub+1 
      jj=j-jbsub+1 
c
c...      total field
c
      dumtot=totfld(i,j)
c
c*******  asymmetric component
c
      radius=sqrt((i-rimax)**2+(j-rjmax)**2)
      radius=radius*dxfac
      if(radius.ge.mc) radius=mc-1
c
c...        curvd
c
      if(radius.ne.0.0) then 
      fr=curv2(radius,mc,xint,symcmp,yp,sigma,1) 
      else
      fr=symcmp(1) 
      end if
c
c...        zero out symmetric component
c..         way outside the max r
c
      rmclim=mc+999.0
      if(radius.ge.rmclim) fr=0.0
      symfld(ii,jj)=fr
      asymfld(ii,jj)=dumtot-fr
300   continue
      return
      end
