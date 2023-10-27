      subroutine lsdiags(mx,my,mp,
     $     nx,ny,np,nkcps,
     $     inest,itau,icurtau,
     $     u,v,t,z,rh,zcps,plevcps,
     $     us,vs,ts,ps,rhs,tpw,
     $     sst,sstanom,ohc,pr,
     $     zthklo,
     $     rlon,rlat,plev,
     $     clon,clat,cbearing,cspeed,
     $     irepos,rmiss,
     $     usnd,vsnd,tsnd,zsnd,rhsnd,
     $     usnds,vsnds,tsnds,psnds,rhsnds,
     $     ms,ns,diagvar,diaglab,
     $     msu,nsu,udiagvar,udiaglab,
     $     ierr)
c
c     This set of subroutines is for calculating large scale and vortex scale
c     diagnostics for tropical cyclone analysis. This code was adapted from the 
c     SHIPS model diagnostic code, and is designed for diagnostics at a single
c     time period. Model input is assumed to be on constant pressure levels with
c     on an evenly spaced lat/lon grid. Missing values are assumed to be .le. rmiss. 
c
c     Last Modified: 02/11/2011, version 1.1
c 
c     Input: 
c            mx,my,mp:   Maximum lon,lat,P array dimensions
c            nx,ny,np:   Usable lat,lon,P array dimensions
c            inest:      Flag for smaller or nested grids, uses smaller areas for averaging
c            u,v,t,z,rh: 3-D (lon,lat,P) arrays of wind components (m/s), 
c                        temperature (deg C), geopotential height (m) and 
c                        relative humidity (%)
c            us,vs:      2-D (lon,lat) surface or lowest model level horizontal winds (m/s)
c            ts:         2-D surface or lowest model level T (deg C)
c            ps:         2-D Sea-level pressure (hPa)     
c            rhs:        2-D surface or lowest model level relative humidity (%)
c            sst:        2-D sea surface temperature (deg C)
c            ssta:       2-D sea surface temperature anomaly (deg C)
c            ohc:        2-D oceanic heat content (kJ/cm2)
c            pr:         2-D total precip (mm/day)
c            tpw:        2-D total precipitable water (mm)
c            zthklo:     900-600 thickness for hart cps B param
c            rlon:       1-D array of model grid longitudes (deg E, 0 to 360 convention)
c            rlat:       1-D array of model grid latitudes  (deg N, -90 to 90 convention)
c            plev:       1-D Pressure levels of model grid (hPa)
c            clat:       Storm latitude  (deg N, -90 to 90 convention)
c         clon:       Storm longitude (deg E, 0 to 360 convention)
c         cbearing:   Storm bearing (default is 0)
c         irepos:     Flag for repositioning storm based on local center finding routine
c                        =1 to reposition, =0 for no repositioning
c         rmiss:      Value for missing values in model field arrays 
c                     (if field value .le. rmiss, it is considerd missing, 
c                    -999.9 is a good choice)
c         ms:         Max dimension of diagvar and diaglab arrays
c
c     Output: 
c            usnd,vnsd:       Sounding of area averaged u,v
c            tsnd,zsnd,rhsnd: Sounding of area average t,z,rh (note: area for TD variables can
c                                                                   be different than wind)
c            usnds,vnsds:        Area averaged surface u,v
c            tsnds,psnds,rhsnds: Area averaged surface t,p,rh (note: area for TD variables can
c                                                                   be different than wind)
c            tpwa:       Area averaged tpw
c            ns:         Number of variables in diagvar array
c            diagvar:    1-D array containing diagnostic variables
c            diaglab:    Labels (a50) for diagnostic variables
c            ierr:       Error flag (=0 for normal return)
c 
cccccccccccccccccccccccuse diag_util


c--       modlue form of 

      use dist2Coast
      use radPlevParamsGlobal
      use tcTrkMeta


c**       Passed variables
c++       Basic model fields and coordinates

      dimension u(mx,my,mp),v(mx,my,mp),z(mx,my,mp),
     $     t(mx,my,mp),rh(mx,my,mp),
     $     zcps(mx,my,nkcps),plevcps(nkcps)

      dimension us(mx,my),vs(mx,my),ts(mx,my),ps(mx,my),rhs(mx,my)

      dimension sst(mx,my),sstanom(mx,my),ohc(mx,my),tpw(mx,my),
     $     zthklo(mx,my),pr(mx,my)

      dimension rlon(mx),rlat(my),plev(mp)

      dimension dum(mx,my)

c++       Sounding variables

      dimension usnd(mp),vsnd(mp),tsnd(mp),zsnd(mp),rhsnd(mp)

c++       Diagnostic variables and labels

      dimension     diagvar(ms)
      character*50  diaglab(ms)

      dimension     udiagvar(msu)
      character*50  udiaglab(msu)

c**       Local variables
c++       Cylindrical grid variables (Note: mpl must be .ge. mp)

C  -- 20200404 -- coordinate with mr in mf.modules.f -- decrease dr to 5 km and nr to 300 (twice the res)
C      parameter (mr=150,mt=36,mpl=100)
      parameter (mr=300,mt=36,mpl=100)
      dimension r(0:mr),theta(0:mt)
      dimension xrt(0:mr,0:mt),yrt(0:mr,0:mt)
      dimension sinth(0:mt),costh(0:mt)

      real*4 zdiff(nkcps),dz(nkcps),dlnp(nkcps),dzdlnp(nkcps),lnp(nkcps)

      real totPrecip,totPrecipHemiR,totPrecipHemiL


c++       Arrays for interpolating fields to the cylindrical grid

      dimension uc(0:mr,0:mt,mpl),vc(0:mr,0:mt,mpl),tc(0:mr,0:mt,mpl)
      dimension zc(0:mr,0:mt,mpl),rhc(0:mr,0:mt,mpl)

c--       z for hart cps

      dimension zcpsc(0:mr,0:mt,mpl)
      dimension zthkloc(0:mr,0:mt)

      dimension urc(0:mr,0:mt,mpl),vtc(0:mr,0:mt,mpl)
      dimension urca(0:mr,mpl),vtca(0:mr,mpl)

      dimension usc(0:mr,0:mt),vsc(0:mr,0:mt),tsc(0:mr,0:mt)
      dimension psc(0:mr,0:mt),rhsc(0:mr,0:mt)
      dimension sstc(0:mr,0:mt),sstanomc(0:mr,0:mt),
     $     ohcc(0:mr,0:mt),tpwc(0:mr,0:mt),
     $     prc(0:mr,0:mt)

      dimension vmax(0:mt),rmw(0:mt)

c--       wind radii params
c         
      integer, parameter :: nRadii=3
      real wRadii(nRadii),rRadii(nRadii,2)

      logical verb

      wRadii(1)=34.0
      wRadii(2)=50.0
      wRadii(3)=64.0

      verb=.false.
ccc      verb=.true.

c++       Set defaults

      ierr = 0

c**       Begin specification of diagnostic calculation parameters

      if (inest.eq.0 .and. verb) print*,'PPPP using global settings in radPlevParamsGlobal'

      if(verb) print*,'TTTTTTTTTTTTTTTTTTTTTTTTTTT icurtau: ',icurtau


c**       End specification of diagnostic calculation parameters

c         Specify  physical and numerical constants

      pi = 3.14159265
      dtr = pi/180.0
      cctk = 273.15
      cmtk = 1.944

c         Check local array dimensions

      if (mp .gt. mpl) then
        ierr=1
        return
      endif

c         Calculate cylindrical grid info (r in km, theta in deg, +x axis is east)

      call cgcal(mr,mt,nr,nt,dr,dt,r0,dtr,r,
     $     theta,cbearing,
     $     xrt,yrt,sinth,costh)

c         Calculate parameters to convert between lat/lon and storm-centered
c         cylindrical grid. These must be recalculated if storm center is moved.

      call gridcon(mx,my,nx,ny,rlon,rlat,
     $     clon,clat,
     $     dtr,
     +     dlon,dlat,dx,dy,glon1,glat1,xg1,yg1)


c++       Interpolate 3D model fields to cylindrical grid

      call lltocg3(u,uc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(v,vc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(t,tc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(z,zc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg3(rh,rhc,mx,my,mp,mpl,nx,ny,np,mr,mt,nr,nt,
     +             dx,dy,xg1,yg1,xrt,yrt,rmiss)

c--       interpolate 3d z for hart cps to cylindrical grid

      
c      do k=1,nkcps
c        call load2dfrom3d(zcps,dum,mx,my,nkcps,k)
c        call qprntn(dum,'zcps',1,1,mx,my,6,6)
c      enddo
c      stop 'test'

      call lltocg3(zcps,zcpsc,mx,my,mp,mpl,
     $     nx,ny,nkcps,mr,mt,nr,nt,
     $     dx,dy,xg1,yg1,xrt,yrt,rmiss)


c++       Interpolate 2D model fields to cylindrical grid

      call lltocg2(us,usc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(vs,vsc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(ts,tsc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(ps,psc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(rhs,rhsc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(sst,sstc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(sstanom,sstanomc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(ohc,ohcc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(tpw,tpwc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)
      call lltocg2(pr,prc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)

      call lltocg2(zthklo,zthkloc,mx,my,nx,ny,mr,mt,nr,nt,
     +     dx,dy,xg1,yg1,xrt,yrt,rmiss)


c++       Calculate radial and tangential winds

      call uvtort(uc,vc,sinth,costh,mr,mt,mpl,nr,nt,np,urc,vtc,rmiss)

c++       Azimuthally average radial and tangential winds

      call azavg3(urc,urca,mr,mt,mpl,nr,nt,np,rmiss)
      call azavg3(vtc,vtca,mr,mt,mpl,nr,nt,np,rmiss)

cbbbbb    Begin vortex scale and ocean diagnostic calculations

c++       Find max wind, min sea level pressure, RMW

      call vorparm(usc,vsc,psc,r,srmax,mr,mt,nr,nt,rmiss,
     +             vmax,rmw,vmaxa,rmwa,pmina)


c++       Initialize SST, OHC, TPW to missing

      ssta  = rmiss
      sstaa = rmiss
      ohca  = rmiss
      tpwa  = rmiss

 
ceeeee    ** End vortex scale and ocean diagnostic calculations


cbbbbb    ** Begin large scale diagnostic calculations

c++       Area average sounding

      do k=1,np

c         wind

cccccccccccccccccccccccccccccccccccccccccccccccccc!!!!!!!!!!!!!!bugto use 1,1,k?
c changed to 0,0,k
c
         call caavg(uc(0,0,k),r1sw,r2sw,mr,mt,nr,nt,
     +              rmiss,r,theta,usnd(k),usndhemiR,usndhemiL)
         call caavg(vc(0,0,k),r1sw,r2sw,mr,mt,nr,nt,
     +              rmiss,r,theta,vsnd(k),usndhemiR,usndhemiL)

c         mass

         call caavg(tc(0,0,k),r1st,r2st,mr,mt,nr,nt,
     +              rmiss,r,theta,tsnd(k),usndhemiR,usndhemiL)
         call caavg(zc(0,0,k),r1st,r2st,mr,mt,nr,nt,
     +              rmiss,r,theta,zsnd(k),usndhemiR,usndhemiL)
         call caavg(rhc(0,0,k),r1st,r2st,mr,mt,nr,nt,
     +              rmiss,r,theta,rhsnd(k),usndhemiR,usndhemiL)
      enddo

cbbbbbbbbbbbbbbbbbbbbb user-defined parameters


cbbbb     total precip and asymmetric/total ratio
      call caavg(prc(1,1),r1sw,r2sw,mr,mt,nr,nt,
     +     rmiss,r,theta,totPrecip,totPrecipHemiR,totPrecipHemiL)

      prAsym=rmiss

c***      divide by 2*pr because area averaged (each hemi is 1/2)
c
      if(totPrecip .gt. 0.0) prAsym=((totPrecipHemiR-totPrecipHemiL)/(2.0*totPrecip))*100.0
      if(verb) print*,'totPrecip,prAsym: ',totPrecip,prAsym

ceeee     total precip


cbbbb     hart cyclone phase space
 
c++       min max z for hart cps vtl and vth

      do k=1,nkcps

        call cminmax(zcpsc(1,1,k),r1sw,r2sw,mr,mt,nr,nt,
     $       rmiss,r,theta,fmin,fmax)
        

        zdiff(k)=fmax-fmin
        lnp(k)=log(plevcps(k))

      enddo
 
      dz=0.0
      dlnp=0.0
      dzdlnp=0.0
      nkcpsH=nkcps/2
      nkcpsM=nkcpsH+1

c--       don't need for the linear regression
c      do k=2,nkcpsM
c        dz(k) = zdiff(k) - zdiff(k-1)
c        dlnp(k) = log(plevcps(k)) - log(plevcps(k-1))
c        dzdlnp(k) = dz(k) / dlnp(k)
c        print*,'lllll ',plevcps(k),plevcps(k-1),dz(k),dlnp(k),dzdlnp(k)
c      enddo

      call calccorr(lnp(1),zdiff(1),nkcpsM,R2,cps_VtL)

c      do k=nkcpsM+1,nkcps
c        dz(k) = zdiff(k) - zdiff(k-1)
c        dlnp(k) = log(plevcps(k)) - log(plevcps(k-1))
c        dzdlnp(k) = dz(k) / dlnp(k)
c        print*,'hhhhh ',plevcps(k),plevcps(k-1),dz(k),dlnp(k),dzdlnp(k)
c      enddo

      call calccorr(lnp(nkcpsM),zdiff(nkcpsM),nkcpsM,R2,cps_VtH)

c++       hart cps B = delta 900-600 thickness between hemisphere

      call caavg(zthkloc,r1sw,r2sw,mr,mt,nr,nt,
     +     rmiss,r,theta,bmean,bhemiR,bhemiL)

      
      cpsB=bhemiR-bhemiL

      if(verb) then
        print*
        print*,'cpsVtL: ',cps_VtL
        print*,'cpsVtH: ',cps_VtH
        print*,'  cpsB: ',cpsB
        print*
      endif

ceeee     hart cyclone phase space

cbbbbbbbbbbbbbbbbbbbbb user-defined parameters

c++       Surface area averages

      call caavg(usc,r1sw,r2sw,mr,mt,nr,nt,rmiss,r,theta,
     $     usnds,usndhemiR,usndhemiL)

      call caavg(vsc,r1sw,r2sw,mr,mt,nr,nt,rmiss,r,theta,
     $     vsnds,usndhemiR,usndhemiL)

      call caavg(tsc,r1st,r2st,mr,mt,nr,nt,rmiss,r,theta,
     $     tsnds,usndhemiR,usndhemiL)

      call caavg(psc,r1st,r2st,mr,mt,nr,nt,rmiss,r,theta,
     $     psnds,usndhemiR,usndhemiL)

      call caavg(rhsc,r1st,r2st,mr,mt,nr,nt,rmiss,r,theta,
     $     rhsnds,usndhemiR,usndhemiL)

c++       TPW, SST and OHC area averages

      call caavg(tpwc,0.0,radtpw,mr,mt,nr,nt,rmiss,r,theta,
     $     tpwa,usndhemiR,usndhemiL)

      call caavg(sstc,0.0,ssmax,mr,mt,nr,nt,rmiss,r,theta,
     $     ssta,usndhemiR,usndhemiL)

      call caavg(sstanomc,0.0,ssmax,mr,mt,nr,nt,rmiss,r,theta,
     $     sstaa,usndhemiR,usndhemiL)

      call caavg(ohcc,0.0,somax,mr,mt,nr,nt,rmiss,r,theta,
     $     ohca,usndhemiR,usndhemiL)

c++       Vertical shear and direction (heading)

      call shrcal(mp,np,plev,psbot,pstop,usnd,vsnd,rmiss,
     $     shrmag,shrhead,ierr)

cbbbb     total shear

      call shrTot(shrmag,
     $     uc,vc,r1sw,r2sw,
     $     mr,mt,mp,nr,nt,np,
     $     plev,psbot,pstop,
     $     rmiss,r,theta,
     $     totshrbar,ratioShr2Tot,totshrAsym)

      if (ierr .ne. 0)  then
        print*,' lllllllllllllllllllllllllllllllllllllllllllllllllllllll shear error'
        return
      endif

ceeee     total shear


cbbbb     roci/poci

      idoroci=1
      if(idoroci.eq.1) then
        call getRociPoci(psc,
     $       icurtau,
     $       mr,mt,
     $       rmiss,r,theta,
     $       finalPoci,finalRoci)
        
      endif

ceeee     roci/poci


      call getWindRadii(usc,vsc,
     $     icurtau,
     $     mr,mt,
     $     rmiss,r,theta,
     $     nRadii,wRadii,rRadii)

c++       Area average vorticity and divergence

      call aavd(urca,vtca,pva,rva,rmiss,r,plev,vavgpv,davgpv,
     +                               mr,mp,mpl,nr,np,ierr)

      if (ierr .ne. 0)  then
        print*,' lllllllllllllllllllllllllllllllllllllllllllllllllllllll area vort'
        return
      endif


      call aavd(urca,vtca,pda,rda,rmiss,r,plev,vavgpd,davgpd,
     +                               mr,mp,mpl,nr,np,ierr)

      if (ierr .ne. 0)  then
        print*,' lllllllllllllllllllllllllllllllllllllllllllllllllllllll area div'
        return
      endif

 
c++       Radially averaged tangential wind

      call ravt(urca,vtca,pta,rta,r,plev,vtbar,urbar,
     +          mr,mp,mpl,nr,np,ierr,rmiss)

      if (ierr .ne. 0)  then
        print*,' lllllllllllllllllllllllllllllllllllllllllllllllllllllll area tang wind'
        return
      endif


c++       Distance to nearest major landmass

      call gbland(clon,clat,dtl)

ceeeee    ** End large-scale diagnostic calculations


 900   continue

c         ** Begin unit conversions
c         
c         ++Convert max sfc wind from m/s to kt

       if (vmaxa .gt. rmiss) then
         vmaxa = cmtk*vmaxa
       endif
       
c         ++ Scale SST by 10, convert K to C

       if (sstaa .gt. rmiss) then
         sstaa = sstaa*10.0
       endif

       if (ssta .gt. rmiss .and. ((ssta-273.15) .gt. sstMinDegC) ) then
         ssta = (ssta-273.15)*10.0
       else
         ssta = rmiss
         sstaa = rmiss
       endif

c--       force climo
c         
c       if(itau.gt.1) then
c         ssta=rmiss
c         sstaa=rmiss
c       endif

c         ++Convert u,v soundings and surface from m/s to kt

       do k=1,np
         if (usnd(k) .gt. rmiss) then
           usnd(k) = cmtk*usnd(k)
         endif
         if (vsnd(k) .gt. rmiss) then
           vsnd(k) = cmtk*vsnd(k)
         endif
       enddo

       if (usnds .gt. rmiss) then
         usnds = cmtk*usnds
       endif

       if (vsnds .gt. rmiss) then
         vsnds = cmtk*vsnds
       endif

c++       Convert shr magnitude from m/s to kt

       if (shrmag .gt. rmiss) then
         shrmag = cmtk*shrmag
       endif

c++       Scale average vorticity and divergence by 10**7

       if (vavgpv .gt. rmiss) then
         vavgpv = vavgpv*(10.0**7)
       endif

       if (davgpv .gt. rmiss) then
         davgpv = davgpv*(10.0**7)
       endif

       if (vavgpd .gt. rmiss) then
         vavgpd = vavgpd*(10.0**7)
       endif

       if (davgpd .gt. rmiss) then
         davgpd = davgpd*(10.0**7)
       endif

c++       Scale radially averaged tangential wind by 10

       if (vtbar .gt. rmiss) then
         vtbar = 10.0*vtbar
       endif

       if (urbar .gt. rmiss) then
         urbar = 10.0*urbar
       endif


c--       End unit conversions

       if(verb) then

         write(6,600) clon,clat,dtl
         write(6,601) vmaxa,rmwa,pmina
         write(6,602) ssta,sstaa,ohca
         write(6,605) shrmag,shrhead
         write(6,606) vavgpv,davgpd
         write(6,607) vtbar,urbar

       endif

         
c     Choose diagnostic variables to send back to calling routine
c***  editted here to include 16 instead of 14 (str speed, heading)
      ns = 16
c
      diagvar( 1) = clat
      diagvar( 2) = clon
      diagvar( 3) = vmaxa
      diagvar( 4) = rmwa
      diagvar( 5) = pmina
      diagvar( 6) = shrmag
      diagvar( 7) = shrhead
      diagvar( 8) = cspeed
      diagvar( 9) = cbearing
      diagvar(10) = ssta
      diagvar(11) = ohca
      diagvar(12) = tpwa
      diagvar(13) = dtl
      diagvar(14) = vtbar
      diagvar(15) = vavgpv
      diagvar(16) = davgpd
      

      n=1
      if(cpmnTC(itau) .lt. 0.0) cpmnTC(itau)=rmiss
 
      udiagvar( n) = cvmxTC(itau)     ; n=n+1
      udiagvar( n) = vmaxa            ; n=n+1
      udiagvar( n) = cpmnTC(itau)     ; n=n+1
      udiagvar( n) = pmina            ; n=n+1
      udiagvar( n) = sstaa            ; n=n+1
      udiagvar( n) = totPrecip        ; n=n+1
      udiagvar( n) = prAsym           ; n=n+1
      udiagvar( n) = cmtk*totshrbar   ; n=n+1
      udiagvar( n) = ratioShr2Tot     ; n=n+1
      udiagvar( n) = totshrAsym       ; n=n+1
      udiagvar( n) = cpsB             ; n=n+1
      udiagvar( n) = cps_VtL          ; n=n+1
      udiagvar( n) = cps_VtH          ; n=n+1
      udiagvar( n) = finalPoci        ; n=n+1
      udiagvar( n) = finalRoci        ; n=n+1
      udiagvar( n) = rRadii(1,2)      ; n=n+1
      udiagvar( n) = rRadii(2,2)      ; n=n+1
      udiagvar( n) = rRadii(3,2)      ; n=n+1


 600  format(/,' clon,clat,dtl:  ',f7.2,1x,f7.2,1x,f8.1)
 601  format(  ' vmax,rmw,pmin:  ',f7.2,1x,f7.2,1x,f8.1)
 602  format(  ' ssta,sstaa,ohca:        ',f7.2,1x,f7.2,1x,f7.2)
 605  format(  ' shrmag,shrhead: ',f7.2,1x,f7.2)
 606  format(  ' v850,d200:      ',f7.2,1x,f7.2)
 607  format(  ' vtbar,urbar:    ',f7.2,1x,f7.2)

      return
      end




      subroutine lintcf(fxy,x1,dx,y1,dy,mx,my,nx,ny,xi,yi,rmiss,fxyii)

c     This routine bi-linearly interpolates fxy to the point             
c     (xi,yi) to give fxyii. Points with missing values (fxy .le. rmiss) 
c     are excluded from the interpolation. If all points are missing, 
c     fxyii is set to rmiss.                                            
c                                                                        
c     Input:   fxy(mx,my) - array to be interpolated                     
c              dx,dy      - spacing of evenly spaced x,y points          
c              x1,y1      - x,y coorindates of lower-left point          
c              mx,my      - max dimensions of fxy                        
c              nx,ny      - working dimensions of fxy                    
c              xi,yi      - coordinates of point to be interpolated      
c                                                                        
c     Output:  fxyii      - value of interpolated function at (xi,yi)    
c                                                                        
      dimension fxy(mx,my)                                               
c                                                                        
      data itemp /0/
c
c     Find the indices of the lower-left point of the                
c     grid box containing the point (xi,yi)                              
      i0 = 1 + int( (xi-x1)/dx )                                        
      j0 = 1 + int( (yi-y1)/dy )                                        
c                                                                        
      fxyii = rmiss
c 
c     Check index bounds                                                 
c      if (i0 .lt.    1) i0=   1                                          
c      if (i0 .gt. nx-1) i0=nx-1                                          
c      if (j0 .lt.    1) j0=   1                                          
c      if (j0 .gt. ny-1) j0=ny-1                                          
      if (i0 .lt.    1) return                                          
      if (i0 .gt. nx-1) return                                          
      if (j0 .lt.    1) return                                          
      if (j0 .gt. ny-1) return  
c                                                                        
      i1 = i0+1                                                          
      j1 = j0+1                                                          
c                                                                        
c     Calculate normalized x,y distances                                 
      xn = ( (xi-x1) - dx*float(i0-1) )/dx                               
      yn = ( (yi-y1) - dy*float(j0-1) )/dy                               
c                                                                        
      if (xn .lt. 0.0) xn = 0.0                                          
      if (xn .gt. 1.0) xn = 1.0                                          
      if (yn .lt. 0.0) yn = 0.0                                          
      if (yn .gt. 1.0) yn = 1.0                                          
c                                                                        
c     Calculate coefficients for interpolation function                  
      f00 = fxy(i0,j0)                                                   
      f10 = fxy(i1,j0)                                                   
      f01 = fxy(i0,j1)                                                   
      f11 = fxy(i1,j1)                                                   
c                                                                        
      w00 = 1.0 + xn*yn - xn - yn
      w10 = xn*(1.0-yn)
      w01 = yn*(1.0-xn)
      w11 = xn*yn
c
      if (f00 .le. rmiss) w00 = 0.0
      if (f01 .le. rmiss) w01 = 0.0
      if (f10 .le. rmiss) w10 = 0.0
      if (f11 .le. rmiss) w11 = 0.0
c
      wtsum = w00 + w01 + w10 + w11
      if (wtsum .le. 0.0) then
         fxyii = rmiss
      else
         fxyii = (w00*f00 + w10*f10 + w01*f01 + w11*f11)/wtsum
      endif

      return                                                             
      end    


      subroutine caavg(frt,r1,r2,mr,mt,nr,nt,rmiss,r,theta,
     $     fbar,fbarhemiR,fbarhemiL)

c     This routine calculates the area average of f(r,theta)
c     from r=r1 to r=r2. 

      dimension frt(0:mr,0:mt) 
      dimension r(0:mr),theta(0:mt)

c     Find indices corresponding to r1 and r2
      ir1 = 0
      ir2 = nt

      do i=nr,0,-1
        if (r(i) .le. r1) then
          ir1 = i
          exit
        endif
      enddo
      
      do i=1,nr
        if (r(i) .ge. r2) then
          ir2 = i
          exit
        endif
      enddo

      jb=0
      je=nt-1
      call doaavec(frt,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,fbar)


c***      don't  understand why, but this gives the Left hemi; thought
c         thought it would be right, but is consistent Tim's cpsB
c
      jb=0
      je=nt/2-1
      call doaavec(frt,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,fbarhemiL)

      jb=nt/2
      je=nt-1
      call doaavec(frt,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,fbarhemiR)

ccc      print*,'fbar ',fbar,fbarhemiR,fbarhemiL

      return
      end


      subroutine doaavec(frt,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,fbar)

      dimension frt(0:mr,0:mt) 
      dimension r(0:mr)

      if (ir1 .ge. ir2) then
         fbar = rmiss
         return
      endif

      fbar = 0.0
      abar = 0.0
      do i=ir1,ir2
        do j=jb,je
         if (frt(i,j) .gt. rmiss) then
            abar = abar + r(i)
            fbar = fbar + r(i)*frt(i,j)
         endif
      enddo
      enddo
           
      if (abar .gt. 0.0) then
         fbar = fbar/abar
      else
         fbar = rmiss
      endif

      return
      end 



      subroutine cminmax(frt,r1,r2,mr,mt,nr,nt,rmiss,r,theta,
     $     fmin0,fmax0)

c     This routine find max/min in f(r,theta)
c     from r=r1 to r=r2. 

      dimension frt(0:mr,0:mt) 
      dimension r(0:mr),theta(0:mt)

c     Find indices corresponding to r1 and r2
      ir1 = 0
      ir2 = nt

      do i=nr,0,-1
         if (r(i) .le. r1) then
            ir1 = i
            go to 1000
         endif
      enddo
 1000 continue

      do i=1,nr
         if (r(i) .ge. r2) then
            ir2 = i
            go to 1100
         endif
      enddo
 1100 continue
c         
      jb=0
      je=nt-1

      call dominmax(frt,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,fmin0,fmax0)

ccc      print*,'fmin0 ',fmin0,'fmax0 ',fmax0

      return
      end


      subroutine dominmax(frt,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,fmin0,fmax0)

      dimension frt(0:mr,0:mt) 
      dimension r(0:mr)


      if (ir1 .ge. ir2) then
        fmin=rmiss
        fmax=rmiss
        return
      endif

      fmin1=1e20
      fmax1=-1e20

      fmin0=fmin1
      fmax0=fmax1

      do i=ir1,ir2
        do j=jb,je
          if(frt(i,j).gt.fmax0 .and. frt(i,j) .ne. rmiss) fmax0=frt(i,j)
          if(frt(i,j).lt.fmin0 .and. frt(i,j) .ne. rmiss) fmin0=frt(i,j)
        enddo
      enddo

      if(fmax0.eq.fmax1) fmax0=rmiss
      if(fmin0.eq.fmin1) fmin0=rmiss

      return
      end 





      subroutine cgcal(mr,mt,nr,nt,dr,dt,r0,dtr,r,
     $     theta,theta0,
     $     xrt,yrt,
     +     sinth,costh)

c     This routine calculate the radial and azimuthal
c     points of the cylindrical grid. The x,y coordinates of the cg
c     and the sines and cosines of the azimuthals are also calculated. 


      dimension r(0:mr),theta(0:mt)
      dimension xrt(0:mr,0:mt),yrt(0:mr,0:mt)
      dimension sinth(0:mt),costh(0:mt)

      do ii=0,nr
         r(ii) = r0 + dr*float(ii)
      enddo

      do jj=0,nt
        theta(jj) = dt*float(jj) + theta0
ccc        if(theta(jj).gt.360.0) theta(jj)=theta(jj)-360.0
ccc        print*,'jj ',jj,theta(jj)
        
      enddo

      do jj=0,nt
         sinth(jj) = sin(dtr*theta(jj))
         costh(jj) = cos(dtr*theta(jj))
      enddo

      do ii=0,nr
        do jj=0,nt
          xrt(ii,jj) = r(ii)*costh(jj)
          yrt(ii,jj) = r(ii)*sinth(jj)
ccc          if(ii.eq.5) print*,ii,jj,r(ii),theta(jj),xrt(ii,jj),yrt(ii,jj)
        enddo
      enddo

      return
      end


      subroutine gridcon(mx,my,nx,ny,rlon,rlat,
     $     clon,clat,
     $     dtr,
     +     dlon,dlat,dx,dy,glon1,glat1,xg1,yg1)

c     This routine calculates variables needed to convert between
c     the lat/lon and cylindrical grids
c
      dimension rlon(mx),rlat(my)
c
c     Calcualte dx,dy of lat/lon grid at storm center location
      dlon = rlon(2)-rlon(1)
      dlat = rlat(2)-rlat(1)
c     
      dy = 111.1*dlat
      dx = 111.1*dlon*cos(dtr*clat)
c
c     Assuming storm center is origin, calculate x,y of lower left
c     model grid point
      glat1 = rlat(1)
      glon1 = rlon(1)
c     if (glon1 .lt. 0.0) glon1 = glon1 + 360.0
c
      xg1 = dx*(glon1-clon)/dlon
      yg1 = dy*(glat1-clat)/dlat
c
      return
      end

      subroutine lltocg3(f3,fc,mx,my,mp,mpl,
     $     nx,ny,np,mr,mt,nr,nt,
     $     dx,dy,xg1,yg1,xrt,yrt,rmiss)

c     This routine interpolotes the function f3 from an evenly spaced grid to a
c     cylindrical grid. This version is where f3 is a 3D function (lon,lat,P). All
c     pressure levels are interpolated.

      dimension f3(mx,my,mp)
      dimension fc(0:mr,0:mt,mpl)
      dimension xrt(0:mr,0:mt),yrt(0:mr,0:mt)

      do k=1,np
         do ii=0,nr
           do jj=0,nt
             call lintcf(f3(1,1,k),xg1,dx,yg1,dy,mx,my,nx,ny,
     +            xrt(ii,jj),yrt(ii,jj),rmiss,fxyii)
             fc(ii,jj,k) = fxyii
         enddo
       enddo
      enddo

      return
      end

      subroutine lltocg2(f2,fc,mx,my,nx,ny,mr,mt,nr,nt,
     +                   dx,dy,xg1,yg1,xrt,yrt,rmiss)

c     This routine interpolotes the function f2 from an evenly spaced grid to a
c     cylindrical grid. This version is where f2 is a 2D function (lon,lat).
c
      dimension f2(mx,my)
      dimension fc(0:mr,0:mt)
      dimension xrt(0:mr,0:mt),yrt(0:mr,0:mt)

      do ii=0,nr
        do jj=0,nt
          call lintcf(f2,xg1,dx,yg1,dy,mx,my,nx,ny,
     +         xrt(ii,jj),yrt(ii,jj),rmiss,fxyii)
          fc(ii,jj) = fxyii
        enddo
      enddo

      return
      end

      subroutine shrcal(mp,np,plev,pbot,ptop,usnd,vsnd,rmiss,
     $     shrmag,shrhead,ierr)

c     This routine calculates the vertical shear and direction
c 
!      use diag_util
c 
      dimension usnd(mp),vsnd(mp),plev(mp)
c
c     Find vertical indices and weights closest to requested 
c         pressure levels.

      call pfind(pbot,plev,mp,np,kb1,kb2,wb1,wb2,ierrb)
      call pfind(ptop,plev,mp,np,kt1,kt2,wt1,wt2,ierrt)

c
      if (ierrb .ne. 0 .or. ierrt .ne. 0) then
        print*,'shrcal ierrb: ',ierrb,' ierrt: ',ierrt
        ierr = 2
        return
      endif

cccc      print*,'plev ',plev,pbot,ptop,wb1,wb2,wt1,wt2

      ubot = wb1*usnd(kb1) + wb2*usnd(kb2)
      vbot = wb1*vsnd(kb1) + wb2*vsnd(kb2)
      utop = wt1*usnd(kt1) + wt2*usnd(kt2)
      vtop = wt1*vsnd(kt1) + wt2*vsnd(kt2)

      ushr = utop-ubot
      vshr = vtop-vbot

      call ctorh(ushr,vshr,shrmag,shrhead)

cccccccccccccccc      print*,'shrcal: ushr,vshr:',ushr,vshr,shrmag,shrhead

      if ((usnd(kb1) .le. rmiss) .or. (usnd(kb2) .le. rmiss) .or. 
     +    (usnd(kt1) .le. rmiss) .or. (usnd(kt2) .le. rmiss) .or.
     +    (vsnd(kb1) .le. rmiss) .or. (vsnd(kb2) .le. rmiss) .or. 
     +    (vsnd(kt1) .le. rmiss) .or. (vsnd(kt2) .le. rmiss)) then
         shrmag = rmiss
         shrhead = rmiss
      endif
c
      return
      end

      subroutine pfind(p,plev,mp,np,k1,k2,w1,w2,ierrp)

c     This routine searches for the two pressure levels in the vertical
c     pressure domain closest to p and calculates the weights for each. 
c     If the requested level is not in the domain, ierrp is set to 1. 

      dimension plev(mp)

      ierrp = 0

c     Make sure the requested p is in the domain

      if (plev(np) .gt. plev(1)) then
         pmax = plev(np)
         pmin = plev( 1)
      else
         pmax = plev( 1)
         pmin = plev(np) 
      endif

      if (p .gt. pmax .or. p .lt. pmin) then
         ierrp = 1
         k1 = -999
         k2 = -999
         w1 = -999.9
         w2 = -999.9
         return
      endif

      dpmin = 10000.0
      k1 = -999
      k2 = -999

      do k=1,np
         dp = abs(plev(k) - p)
         if (dp .lt. dpmin) then
            dpmin = dp
            k1  = k 
         endif
      enddo

      if (k1 .eq. 1) then
         k2 = 2
      elseif (k1 .eq. np) then
         k2 = np-1
      else
         dpp = abs(plev(k1+1)-p)
         dpm = abs(plev(k1-1)-p)
         if (dpp .lt. dpm) then
            k2 = k1 + 1
         else
            k2 = k1-1
         endif
      endif

      w1 = (p-plev(k2))/(plev(k1)-plev(k2))
      w2 = (plev(k1)-p)/(plev(k1)-plev(k2))

      return
      end



cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
c         ROCI/POCI
c
      subroutine getRociPoci(psc,
     $     icurtau,
     $     mr,mt,
     $     rmiss,r,theta,
     $     finalPoci,finalRoci)

c         calc roci/poci
c
      real psc(0:mr,0:mt),pscSym(0:mr),pscMin(0:mr),dpRmdr(0:mr),dpCntr(0:mr)
      real r(0:mr),theta(0:mt)
      real poci(0:mr),roci(0:mr)

      real, parameter :: MinRoci=100.0,MinRociP=100.0,MaxRociP=500.0,MaxPociP=1014.0,pCntr=2.0

      real pmin

      logical verb

      verb=.false.
ccc      verb=.true.

      undef=9999.
      poci(0)=undef
      roci(0)=poci(0)

      finalPoci=undef
      finalRoci=undef

      do i=0,mr
        pscMin(i)=1e10
        do j=0,mt
          if(psc(i,j).lt.pscMin(i)) pscMin(i)=psc(i,j)*0.01
        enddo
ccc        print*,'mmmmm ',i,r(i),pscMin(i)
      enddo

      pmin=1e10
      rmin=1e20

      do i=0,mr
        if(pscMin(i).lt.pmin) then
          pmin=pscMin(i)
          rmin=r(i)
          ipmin=i
        endif
      enddo

      if(rmin.le.MinRoci) then
        do i=ipmin,mr
          dpRmdr(i)=1e20
          dpCntr(i)=1e20
          if(i.le.mr-1) then
            dp=pscMin(i+1)-pscMin(i)
            if(dp.gt.0.0) then
              dpRmdr(i)=mod(pscMin(i),pCntr)
              dpCntr(i)=pscMin(i)-dpRmdr(i)+pCntr
cccc              print*,'BBB ',i+1,r(i),pscMin(i),dp,dpRmdr(i),dpCntr(i)
            else
              ipmax=i
              exit
            endif
          endif
        enddo

ccc        print*,'iiiiiiiiiiiiiiiiiiiiiii ipmin,ipmax: ',ipmin,ipmax

        np=0
        do i=ipmin,ipmax
          if(i.le.mr-1) then
            dpR=dpRmdr(i+1)-dpRmdr(i)
ccc       print*,'MMM ',i,r(i),pscMin(i),dpR
            if(dpR .lt. 0.0) then
              dp=pscMin(i+1)-pscMin(i)
              if(dp.gt.0) then

                dp1=(pscMin(i+1)-dpCntr(i))/dp
                dp2=(dpCntr(i)-pscMin(i))/dp
                rociP=dp2*r(i+1)+dp1*r(i)
                pociP=dpCntr(i)

c--       test for min roci
                if(rociP .lt. MinRociP) cycle
                if(rociP .gt. MaxRociP) cycle
                if(pociP .gt. MaxPociP) cycle

                np=np+1
                roci(np)=rociP
                poci(np)=pociP

ccc                print*,'HHHHHHHHHHHH ',pscMin(i+1),pscMin(i),dpCntr(i),dp,dp1,dp2,(dp1+dp2),r(i+1),roci,r(i)
                
              endif
            endif
          endif
        enddo


        if(np.gt.0) then

          do n=1,np

            if(pmin .lt. 1000.0)                        pminRoci=1004.0
            if(pmin .ge. 1000.0 .and. pmin .lt. 1006.0) pminRoci=1006.0
            if(pmin .ge. 1006.0 .and. pmin .lt. 1008.0) pminRoci=1010.0
            if(pmin .ge. 1008.0 .and. pmin .lt. 1010.0) pminRoci=1012.0
            if(verb) print*,'NNNN ',n,pmin,pminRoci,poci(n),roci(n)

            if(poci(n).eq.pminRoci) then
              finalPoci=poci(n)
              finalRoci=roci(n)
            endif

          enddo

          
          npdefault=np
          if(finalPoci.eq.9999.0 .and. poci(npdefault).gt.0.0) then
            finalPoci=poci(npdefault)
          endif

           if(finalRoci.eq.9999.0 .and. roci(npdefault).gt.0.0) then
             finalRoci=roci(npdefault)
           endif

c--       pick the biggest within MinRociP - MaxRociP
c
           finalPoci=poci(npdefault)
           finalRoci=roci(npdefault)
        else

          finalPoci=poci(0)
          finalRoci=roci(0)

        endif

        if(verb) print*,'FFFF  tau: ',icurtau,' pmin: ',pmin,' rmin: ',rmin,' np: ',np,
     $       ' finalPoci:',finalPoci,' finalRoci: ',finalRoci

      else
        finalPoci=poci(0)
        finalRoci=roci(0)
        if(verb) print*,'FFFF no roci/poci within MinRoci: ',MinRoci,' tau: ',icurtau,' pmin: ',pmin
      endif

      return
      end



cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
c         wind radii
c
      subroutine getWindRadii(usc,vsc,
     $     icurtau,
     $     mr,mt,
     $     rmiss,r,theta,
     $     nRadii,wRadii,rRadii)

      use const

c         find wind radii (34/50/64 kt)
c
      real usc(0:mr,0:mt),vsc(0:mr,0:mt),
     $     wsc(0:mr,0:mt),wbar(0:mr)

      real r(0:mr),theta(0:mt)

      real wRadii(nRadii),rRadii(nRadii,2)

      logical verb

      call initConst(ierr)

      undef=9999.


      verb=.false.
ccc      verb=.true.

      do i=0,mr
        wbar(i)=0.0
        nw=0
        do j=0,mt
          if(usc(i,j).gt.rmiss .and. vsc(i,j).gt.rmiss) then
            nw=nw+1
            wsc(i,j)=sqrt(usc(i,j)*usc(i,j) + vsc(i,j)*vsc(i,j))*rms2kt
            wbar(i)=wbar(i)+wsc(i,j)
ccc       print*,'nw...',i,j,nw,wbar(i),usc(i,j),vsc(i,j),rms2kt
          endif

        enddo

c--       make sure there are at least a full hemisphere of points at each radius
c
        if(nw.gt.0 .and. nw.gt.mt/2) then
          wbar(i)=wbar(i)/(1.*nw)
        else
          wbar(i)=rmiss
        endif

      enddo

      w34=34.0

      do k=1,nRadii
        
        rRadii(k,1)=undef
        rRadii(k,2)=undef

        do i=1,mr-1

c--       allow undef for when there is no data for missing TC taus
c         
c          if(wbar(i+1).eq.rmiss .or. wbar(i).eq.rmiss) then
c            print*,'EEEEEEEEEEEEEEEEEEE ',i,wbar(i+1),wbar(i)
c            stop 'qqq'
c          endif


          if(wbar(i+1).ge.wRadii(k) .and. wbar(i) .lt. wRadii(k) ) then
            dwbar=wbar(i+1)-wbar(i)
            if(dwbar .gt. 0.001) then
              dw1=(wbar(i+1)-wRadii(k))/dwbar
              dw2=(wRadii(k)-wbar(i))/dwbar
            else
              dw1=1.0
              dw2=0.0
            endif
            
            if(rRadii(k,1) .eq. undef) then
              rRadii(k,1)=r(i+1)*dw1 + r(i)*dw2
              if(verb) print*,'RRRR1111: ',wRadii(k),i+1,wbar(i+1),wbar(i),dw1,dw2,r(i+1),r(i),rRadii(k,1)
            endif

          elseif(wbar(i+1).lt.wRadii(k) .and. wbar(i) .ge. wRadii(k) ) then

            dwbar=wbar(i)-wbar(i+1)
            if(dwbar .gt. 0.001) then
              dw1=(wbar(i)-wRadii(k))/dwbar
              dw2=(wRadii(k)-wbar(i+1))/dwbar
            else
              dw1=1.0
              dw2=0.0
            endif
            
            if(rRadii(k,2) .eq. undef) then
              rRadii(k,2)=r(i+1)*dw1 + r(i)*dw2
              if(verb) print*,'RRRR2222: ',wRadii(k),i+1,wbar(i+1),wbar(i),dw1,dw2,r(i+1),r(i),rRadii(k,2)
            endif

          endif

        enddo

      enddo

      return

      end subroutine getWindRadii

      
cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
c         total shear fields
c
      subroutine shrTot(shrmag,
     $     uc,vc,r1,r2,
     $     mr,mt,mp,nr,nt,np,
     $     plev,pbot,ptop,
     $     rmiss,r,theta,
     $     totshrbar,ratioShr2Tot,totshrAsym)

c         calc mag of shear field
c
      dimension uc(0:mr,0:mt,mp),vc(0:mr,0:mt,mp) 
      dimension r(0:mr),theta(0:mt)

      real ubot(0:mr,0:mt),vbot(0:mr,0:mt),
     $     utop(0:mr,0:mt),vtop(0:mr,0:mt),
     $     ushr(0:mr,0:mt),vshr(0:mr,0:mt),totshr(0:mr,0:mt)

      real totshrbar,totshrhemiR,totshrhemiL

      dimension plev(mp)


      call pfind(pbot,plev,mp,np,kb1,kb2,wb1,wb2,ierrb)
      call pfind(ptop,plev,mp,np,kt1,kt2,wt1,wt2,ierrt)

      if (ierrb .ne. 0 .or. ierrt .ne. 0) then
        print*,'shrTot ierrb: ',ierrb,' ierrt: ',ierrt
        ierr = 2
        return
      endif

      do i=0,mr
        do j=0,mt
          ubot(i,j) = wb1*uc(i,j,kb1) + wb2*uc(i,j,kb2)
          utop(i,j) = wt1*uc(i,j,kt1) + wt2*uc(i,j,kt2)
          vbot(i,j) = wb1*vc(i,j,kb1) + wb2*vc(i,j,kb2)
          vtop(i,j) = wt1*vc(i,j,kt1) + wt2*vc(i,j,kt2)
        enddo
      enddo

      do i=0,mr
        do j=0,mt
          ushr(i,j)=utop(i,j)-ubot(i,j)
          vshr(i,j)=vtop(i,j)-vbot(i,j)
          totshr(i,j)=sqrt(ushr(i,j)*ushr(i,j) + vshr(i,j)*vshr(i,j))
        enddo
      enddo

      do i=nr,0,-1
        if (r(i) .le. r1) then
          ir1=i
          exit     
        endif
      enddo
      
      do i=1,nr
        if (r(i) .ge. r2) then
          ir2 = i
          exit
        endif
      enddo

      jb=0
      je=nt-1

ccc       -- used to check calc -- gives same answer as in shrcal
c
c      call doaavec(ubot,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,ubotbar)
c      call doaavec(utop,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,utopbar)
c      call doaavec(vbot,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,vbotbar)
c      call doaavec(vtop,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,vtopbar)
c      print*,'uuuuuuuuvvvvvvvvvvv 850',ubotbar,vbotbar
c      print*,'uuuuuuuuvvvvvvvvvvv 200',utopbar,vtopbar
c      ush=utopbar-ubotbar
c      vsh=vtopbar-vbotbar
c      call ctorh(ush,vsh,shrmag,shrhead)

      call doaavec(totshr,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,totshrbar)

      jb=0
      je=nt/2-1

c***      flip as in cpsB in caavg()
c
      call doaavec(totshr,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,totshrHemiL)

      jb=nt/2
      je=nt-1
      call doaavec(totshr,r,mr,mt,nr,nt,rmiss,ir1,ir2,jb,je,totshrHemiR)

      if(totshrbar .gt. 0.0) then

c***      area averaged hemis hemiR+hemiL = 2*total
c
        totshrAsym=((totshrHemiR-totshrHemiL)/(2.0*totshrbar))*100.0
        ratioShr2Tot=(shrmag/totshrbar)*100.0
      else
        totshrAsym=rmiss
        ratioShr2Tot=rmiss
        totshrbar=rmiss
      endif

cccc      print*,'totshrbar,ratioShr2Tot,totshrAsym: ',totshrbar,ratioShr2Tot,totshrAsym

      return
      end






      subroutine uvtort(uc,vc,sinth,costh,mr,mt,mp,nr,nt,np,urc,vtc,
     +                  rmiss)
c     This routine converts cartesian velocity components uc,vc on a cylindrical
c     grid to radial and tangential wind components on the same grid. 
c
      dimension uc(0:mr,0:mt,mp),vc(0:mr,0:mt,mp)
      dimension urc(0:mr,0:mt,mp),vtc(0:mr,0:mt,mp)
      dimension sinth(0:mt),costh(0:mt)
c
      do k=1,np
      do jj=0,nt
      do ii=0,nr
         urc(ii,jj,k) =  uc(ii,jj,k)*costh(jj) + vc(ii,jj,k)*sinth(jj)
         vtc(ii,jj,k) = -uc(ii,jj,k)*sinth(jj) + vc(ii,jj,k)*costh(jj)
         if ((uc(ii,jj,k) .le. rmiss) .or. 
     +       (vc(ii,jj,k) .le. rmiss)) then
            urc(ii,jj,k) = rmiss
            vtc(ii,jj,k) = rmiss
         endif
      enddo
      enddo
      enddo
c
      return
      end
      subroutine azavg3(frtp,frp,mr,mt,mp,nr,nt,np,rmiss)
c     The routine performs an azimuthal average of frtp to give frp.
c
      dimension frtp(0:mr,0:mt,mp),frp(0:mr,mp)
c
c      cf = 1.0/float(nt)
c
      do k=1,np
      do ii=0,nr
         icf=0
         frp(ii,k) = 0.0
         do jj = 0,nt-1
            if (frtp(ii,jj,k) .gt. rmiss) then
               icf=icf+1
               frp(ii,k) = frp(ii,k) + frtp(ii,jj,k)
            endif
         enddo
         if (icf .eq. nt) then
            cf = 1.0/float(icf)
            frp(ii,k) = cf*frp(ii,k)
         else
            frp(ii,k) = rmiss
         endif
      enddo
      enddo
c 
      return
      end


      subroutine aavd(urca,vtca,pvda,rvda,rmiss,r,plev,vavg,davg,
     +                mr,mp,mpl,nr,np,ierr)
c     This routine calculates the area averaged vorticity and divergence. The average
c     is from r=0 to r=rvda, so only the azmithally averaged ur and vt at r=rvda are needed.
c
      dimension urca(0:mr,mpl),vtca(0:mr,mpl)
      dimension r(0:mr),plev(mp)
c 
c     Find requested pressure level
      call pfind(pvda,plev,mp,np,k1,k2,w1,w2,ierrt)
      if (ierrt .ne. 0) then
         ierr = 3
         return
      endif
c
c     Make sure radial grid is large enough for requested radius
      if (rvda .gt. r(nr)) then
         ierr = 4
         return
      endif
c
c     Find index of nearest radial grid point
      drmin = 9999.9
      iim = -9
      rrm = -9999.9
      do ii=1,nr
            dr = abs(r(ii)-rvda)
            if (dr .lt. drmin) then
               drmin = dr
               iim = ii
            endif
      enddo
c 
      vavg = rmiss
      davg = rmiss
      rmm  = 1000.0*r(iim)
      if ((vtca(iim,k1) .gt. rmiss) .and. 
     +    (vtca(iim,k2) .gt. rmiss)) then
         vavg = 2.0*(w1*vtca(iim,k1) + w2*vtca(iim,k2))/rmm
      endif
      if ((urca(iim,k1) .gt. rmiss) .and. 
     +    (urca(iim,k2) .gt. rmiss)) then
         davg = 2.0*(w1*urca(iim,k1) + w2*urca(iim,k2))/rmm
      endif
c 
      return
      end

      subroutine ravt(urca,vtca,pta,rta,r,plev,vtbar,urbar,
     +                mr,mp,mpl,nr,np,ierr,rmiss)
c     This routine radially averages the tangential and radial wind.
c     The average is not radially weighted. 
c
      dimension urca(0:mr,mpl),vtca(0:mr,mpl)
      dimension r(0:mr),plev(mp)
c 
c     Find requested pressure level
      call pfind(pta,plev,mp,np,k1,k2,w1,w2,ierrt)
      if (ierrt .ne. 0) then
         ierr = 5
         return
      endif
c
c     Make sure radial grid is large enough for requested radius
      if (rta .gt. r(nr)) then
         ierr = 6
         return
      endif
c
c     Find index of nearest radial grid point
      drmin = 9999.9
      iim = -9
      do ii=1,nr
         dr = abs(r(ii)-rta)
         if (dr .lt. drmin) then
            drmin = dr
            iim = ii
         endif
      enddo
c
      vtbar = 0.0
      urbar = 0.0
      ifv = 0
      ifu = 0
      do ii=0,iim
         if ((vtca(ii,k1) .gt. rmiss) .and. 
     +       (vtca(ii,k2) .gt. rmiss)) then
            vtbar = vtbar + (w1*vtca(ii,k1) + w2*vtca(ii,k2))
            ifv = ifv + 1
         endif
         if ((urca(ii,k1) .gt. rmiss) .and. 
     +       (urca(ii,k2) .gt. rmiss)) then
            urbar = urbar + (w1*urca(ii,k1) + w2*urca(ii,k2))
            ifu = ifu + 1
         endif
      enddo
      if (ifv .ne. 0) then
         cfv = 1.0/float(ifv)
         vtbar = cfv*vtbar
      else
         vtbar = rmiss
      endif
      if (ifu .ne. 0) then
         cfu = 1.0/float(ifu)
         urbar = cfu*urbar
      else
         urbar = rmiss
      endif
c
      return
      end



      subroutine vorparm(usc,vsc,psc,r,srmax,mr,mt,nr,nt,rmiss,
     +     vmax,rmw,vmaxa,rmwa,pmin)

c     This routine finds the max wind, radius of max wind and 
c     minimum sea level pressure between r=0 and r=srmax.
c
      dimension usc(0:mr,0:mt),vsc(0:mr,0:mt),psc(0:mr,0:mt)
      dimension vmax(0:mt),rmw(0:mt)
      dimension r(0:mr)
c
      vmaxa = rmiss
      rmwa  = rmiss
      pmin = rmiss
c
c     Find vmax and rmw at each azimuth
      do jj=0,nt
         vmax(jj) = rmiss
         rmw(jj)  = rmiss
         uvmax    = -1.0
         rmax     = -1.0
         do ii=0,nr
            if (r(ii)      .gt. srmax) go to 1000
            if (usc(ii,jj) .le. rmiss) go to 1000
            if (vsc(ii,jj) .le. rmiss) go to 1000
c
            uv = sqrt(usc(ii,jj)**2 + vsc(ii,jj)**2)
            if (uv .gt. uvmax) then
               uvmax = uv
               rmax  = r(ii)
            endif
 1000       continue
         enddo
c
         vmax(jj) = uvmax
         rmw(jj)  = rmax
      enddo
c
c     Azimuthally average rmw and find max value of vmax
      vmaxa = rmiss
      rmwa  = 0.0
      count = 0.0
      do jj=0,nt-1
         if (vmax(jj) .gt. vmaxa) vmaxa = vmax(jj)
c
         if (rmw(jj) .gt. rmiss) then
            count = count + 1.0
            rmwa = rmwa + rmw(jj)
         endif
      enddo
c
      if (count .gt. 0.0) then
         rmwa = rmwa/count
      else
         rmwa = rmiss
      endif
c
c     Find minimum sea-level pressure
      pmin = 10000.0*100.0
      do jj=0,nt-1
      do ii=0,nr
         if (r(ii)      .gt. srmax) go to 2000
         if (psc(ii,jj) .le. rmiss) go to 2000
c
         if (psc(ii,jj) .lt. pmin) pmin = psc(ii,jj)
c
 2000    continue
      enddo
      enddo
c 
c     Convert pmin from Pa to hPa (mb)
      pmin = pmin/100.0
c 
      if (pmin .gt. 9999.0) pmin=rmiss
      if (vmaxa .le. 0.0) then
         vmaxa=rmiss
         rmwa=rmiss
      endif
c
c     do i=0,nr
c        write(6,888) r(i),(psc(i,j),j=0,nt,2)
c 888    format(f7.1,1x,16(f7.1,1x))
c     enddo
c
      return
      end


c
C----------------------------------------------------
C
C----------------------------------------------------
      subroutine calccorr(xdat,ydat,numpts,R2,slope)
c
c     This subroutine is the main driver for a series of
c     other subroutines below this that will calculate the
c     correlation between two input arrays, xdat and ydat.
c
c     INPUT:
c      xdat     array of x (independent) data points
c      ydat     array of y (dependent)   data points
c      numpts   number of elements in each of xdat and ydat
c
c     OUTPUT:
c      R2    R-squared, the coefficient of determination
c      slope Slope of regression line
c
c     xdiff   array of points for xdat - xmean
c     ydiff   array of points for ydat - ymean
c     yestim  array of regression-estimated points
c     yresid  array of residuals (ydat(i) - yestim(i))

      implicit none

      real    xdat(numpts),ydat(numpts)
      real    xdiff(numpts),ydiff(numpts)
      real    yestim(numpts),yresid(numpts)
      real    xmean,ymean,slope,yint,R2
      integer numpts,i

      integer verb
      
      verb=3
      verb=0

c
      call getmean(xdat,numpts,xmean)
      call getmean(ydat,numpts,ymean)
c
      call getdiff(xdat,numpts,xmean,xdiff)
      call getdiff(ydat,numpts,ymean,ydiff)
c
      call getslope(xdiff,ydiff,numpts,slope)
      yint = ymean - slope * xmean
c
      call getyestim(xdat,slope,yint,numpts,yestim)
      call getresid(ydat,yestim,numpts,yresid)
c
      if ( verb .ge. 3 ) then
        print *,' '
        print *,' *--------------------------------------------------* '
        print *,' * CPS Thermal wind regression details              * '
        print *,' *--------------------------------------------------* '
      endif

      call getcorr(yresid,ydiff,numpts,R2)
c
      if ( verb .ge. 3 ) then
        print *,'   i     ydat     xdat    ydiff    xdiff        e'
     &         ,'       e2   ydiff2'
        print *,' ----   -----    -----    -----    -----    -----   '
     &         ,' -----    -----'
        do i = 1,numpts
         write(6,'(2x,i3,2x,f7.2,2x,f7.4,2x,f7.2,2x,f7.4,3(2x,f7.2))') 
     &           i,ydat(i),xdat(i),ydiff(i)
     &           ,xdiff(i),yresid(i),yresid(i)*yresid(i)
     &           ,ydiff(i)*ydiff(i)
        enddo

        print *,' ----   -----    -----    -----    -----    -----   '
     &         ,' -----    -----'
        print *,' '
        write (6,'(1x,a13,f9.3,3x,a5,f7.2)') ' means:   y: ',ymean,'  x: '
     &       ,xmean

        write (6,*) ' '
        write (6,30) 'slope= ',slope,'         y-intercept = ',yint
  30    format (2x,a7,f10.3,a23,f10.3)
        if (slope .gt. 0.0) then
          write(6,40) 'Regression equation:   Y = ',yint,' + ',slope
        else
          write(6,40) 'Regression equation:   Y = ',yint,' - ',abs(slope)
        endif
  40    format (2x,a27,f8.2,a3,f8.2,'X')
c     
        print *,' '
        write (6,'(1x,a17,f6.4,5x,a7,f6.4)') ' R2(r_squared) = ',R2
     &        ,'   r = ',sqrt(R2)
        print *,' '
        print *,' *--------------------------------------------------* '
        print *,' *  End of regression details                       * '
        print *,' *--------------------------------------------------* '
      endif
c     
      return
      end

c-------------------------------------------c
c                                           c
c-------------------------------------------c
      subroutine getmean(xarr,inum,zmean)
c     
c     This subroutine is part of the correlation calculation,
c     and it simply returns the mean of the input array, xarr.
c     
c     INPUT:
c      xarr   input array of data points
c      inum   number of data points in xarr
c     
c     OUTPUT:
c      zmean  mean of data values in xarr

      implicit none
      
      real   xarr(inum)
      real   xsum,zmean
      integer i,inum
c     
      xsum = 0.0
      do i = 1,inum
        xsum = xsum + xarr(i)
      enddo
c     
      zmean = xsum / float(MAX(inum,1))
c     
      return
      end
      
c-------------------------------------------c
c                                           c
c-------------------------------------------c
      subroutine getdiff(xarr,inum,zmean,zdiff)
c     
c     This subroutine is part of the correlation calculation,
c     and it returns in the array zdiff the difference values
c     between each member of the input array xarr and the
c     mean value, zmean.
c     
c     INPUT:
c      xarr   input array of data points
c      inum   number of data points in xarr
c      zmean  mean of input array (xarr)
c     
c     OUTPUT:
c      zdiff  array containing xarr(i) - zmean

      implicit none
      
      real xarr(inum),zdiff(inum)
      real zmean
      integer i,inum
c     
      do i = 1,inum
        zdiff(i) = xarr(i) - zmean
      enddo
c     
      return
      end
      
c-------------------------------------------c
c                                           c
c-------------------------------------------c

      subroutine getslope(xarr,yarr,inum,slope)
c
c     This subroutine is part of the correlation calculation,
c     and it returns the slope of the regression line.
c
c     INPUT:
c      xarr   input array of xdiffs (x - xmean)
c      yarr   input array of ydiffs (y - ymean)
c      inum   number of points in x & y arrays
c
c     OUTPUT:
c      slope  slope of regression line

      real xarr(inum),yarr(inum)
      real slope,sumxy,sumx2
      integer i,inum

c     First sum up the xarr*yarr products....

      sumxy = 0.0
      do i = 1,inum
        sumxy = sumxy + xarr(i) * yarr(i)
      enddo

c     Now sum up the x-squared terms....

      sumx2 = 0.0
      do i = 1,inum
        sumx2 = sumx2 + xarr(i) * xarr(i)
      enddo

c     Now get the slope....

      slope = sumxy / sumx2

      return
      end

c-------------------------------------------c
c                                           c
c-------------------------------------------c
      subroutine getyestim(xarr,slope,yint,inum,yestim)
c
c     This subroutine is part of the correlation calculation,
c     and it calculates all the predicted y-values using the
c     regression equation that has been calculated.
c
c     INPUT:
c      xarr   array of x data points
c      slope  slope of the calculated regression line
c      yint   y-intercept of the calculated regression line
c      inum   number of input points
c
c     OUTPUT:
c      yestim array of y pts estimated from regression eqn.

      implicit none

      real xarr(inum),yestim(inum)
      real slope,yint
      integer i,inum
c
      do i = 1,inum
        yestim(i) = yint + xarr(i) * slope
      enddo
c
      return
      end

c-------------------------------------------c
c                                           c
c-------------------------------------------c
      subroutine getresid(yarr,yestim,inum,yresid)
c
c     This subroutine is part of the correlation calculation,
c     and it calculates all the residual values between the
c     input y data points and the y-estim predicted y values.
c
c     INPUT:
c      yarr   array of y data points
c      yestim array of y pts estimated from regression eqn.
c      inum   number of input points
c
c     OUTPUT:
c      yresid array of residuals (ydat(i) - yestim(i))

      implicit none

      real yarr(inum),yestim(inum),yresid(inum)
      integer i,inum
c
      do i = 1,inum
        yresid(i) = yarr(i) - yestim(i)
      enddo
c
      return
      end

c-------------------------------------------c
c                                           c
c-------------------------------------------c
      subroutine getcorr(yresid,ydiff,inum,R2)
c
c     This subroutine is part of the correlation calculation,
c     and it does the actual correlation calculation.
c
c     INPUT:
c      yresid array of residuals (ydat(i) - yestim(i))
c      ydiff  array of points for ydat - ymean
c      inum   number of points in the arrays
c
c     OUTPUT:
c      R2     R-squared, the coefficient of determination

      implicit none

      real yresid(inum),ydiff(inum)
      real R2,sumyresid,sumydiff
      integer i,inum

      integer verb

      verb=0

      sumyresid = 0.0
      sumydiff  = 0.0

      do i = 1,inum
        sumyresid = sumyresid + yresid(i) * yresid(i)
        sumydiff  = sumydiff  + ydiff(i) * ydiff(i)
      enddo

      if ( verb .ge. 3 ) then
        write (6,*)  ' '
        write (6,30) 'Sum of y-residuals squared (e2) = ',sumyresid
        write (6,30) 'Sum of y-diffs squared (ydiff2) = ',sumydiff
        write (6,*)  ' '
      endif

  30  format (1x,a35,f10.2)
      if (sumydiff == 0.0) then
       R2=1.0
       else
      R2 = 1 - sumyresid / sumydiff
      endif
c
      return
      end
c

