      subroutine mftrackem(
     $     spd,vort,psl,
     $     rtau,ktau,
     $     nwrt,tcyc,numv,
     $     mxhr,nbog,ntrk,ierr)

      use trkParams
      use f77OutputMeta
      use mfutils

      logical verb,speedBrake

      integer numv, mxhr,  nbog, ktau, ntrk

      real*4 spd(ni,nj),vort(ni,nj),psl(ni,nj),rtau

      real fixlat(maxfix),fixlon(maxfix)

      real forspdMX

      character*28 tcyc(maxtc+1)


c***         local variables

      integer idgrid, irecnum, istatus, len, nwrt
      integer ib,ie,jb,je
      integer i,j,n,kc,kcl,ierr

      real pcntile

      real rlat,rlon

      character*8  seclvl
      character*24 dsetnam, dsets(2), typlvl
      character*32 typmodl, geonam, params(2), units
      character*80 title
      character*24 qtitle
      character oformat*24

      verb=verbMfTrackem

      oformat='g10.4'
      pcntile=0.7


         
C--       set search limit         
C
      
      kc=1+ktau/dtau
      kcl=kc-1
      if(kcl.lt.0) kcl=0

      if(nbog.gt.0) then

        do n=1,nbog
        
C--       get current and t-1 sfc wind tracker if a tc found, if not, then use
C         mine and put into the gdat array

          slatwkc=gdat(1,kc,n,0)
          slonwkc=gdat(2,kc,n,0)
          slatwkcl=gdat(1,kcl,n,0)
          slonwkcl=gdat(2,kcl,n,0)

          slatw=gdat(1,kcl,n,0)
          slonw=gdat(2,kcl,n,0)
          headw = gdat(5,kcl,n,0)
          distw = gdat(6,kcl,n,0)
          vmax0 = gdat(10,0,n,0)


C--       20080314 -- reduce critical vort for storms <= 30 kt by 25%         
C
          if(vortcritadjust.and.(vmax0.le.vmaxweak)) then
            vcrit=vortcrit*vortadjfact
          else
            vcrit=vortcrit
          endif
          
          if(verb) then
            print*,'mftrackem: vcrit: ',vcrit
            print*,'mftrackem: slatw, slonw: ',slatw,slonw,ktau,vmax0
            print*,'mftrackem: headw, distw: ',headw,distw
          endif
          
C--       20110829 -- allow storm to go faster initially for weak storms
c         

          if(doInitialSpdMaxAdj .and. (vmax0.le.vmaxweak) .and. rtau <= forspdMaxTau0) then
            forspdMX=forspdMax*forspdAdjfact
          else
            forspdMX=forspdMax
          endif

          dlonmax=forspdMX*(dtau/60.0)
          sdistmin=dlonmax*60.0

          if((slatw.lt.90.).and.(slonw.lt.900.)) then
            continue
          else
            cycle         
          endif

c--       make a first guess using the previous 6-h motion to flat,flon
c         
          call rcaltln (slatw,slonw,headw,distw,flat,flon)
          
          if(verb) then
            print*,'mftrackem: flat, flon: ',flat,flon,blat,blon
          endif
          
          call clltxy (flat,flon,
     $         blat,blon,dlat,dlon,ni,nj,
     $         egxx,egyy,
     $         ierr)


C 20000824 - use initial position vice interpolated for tau = 0         
C         
          if((slatw.lt.90.).and.(slonw.lt.900.).and.ktau.eq.0) then
            flat=slatw
            flon=slonw
          endif
          
          if(verb) then
            print*,'mftrackem: flat,flon: ',flat,flon
            print*,'mftrackem: egxx,egyy: ',egxx,egyy
          endif

c***      main if have an estimated posit to look around

          if((flat.lt.90).and.(flon.lt.900)) then
            
            call getIJrange(egyy,egxx,
     $           dlonmax,
     $           ib,ie,jb,je)

            
C         storm must be within sdistmin [nm]
C         of the first guess location and
C         greater than 'vcrit' (10-5 s-1) 
C         to be valid

            if(verb) then
              qtitle='spd in mftrack [kt]    '
              call qprntn(spd,qtitle,ib,jb,ni,nj,1,6)
              qtitle='vrt in mftrack [s-1]   '
              call qprntn(vort,qtitle,ib,jb,ni,nj,1,6)
            end if

            if(verb) write(*,
     $           '(a,i2,i4,2(f7.2,2x))')
     $           'WND: ',n,ktau,slatwkc,slonwkc
            

            call grhilo_proc_vrt925(
     $           vort,
     $           ib,ie,jb,je,
     $           flat,flon,vcrit,
     $           slatv,slonv,svort)

            if(verb)    write(*,
     $           '(a,i2,i4,3(f7.2,2x))')
     $           'VRT: ',n,ktau,slatv,slonv,svort
            
            slatp=slatv
            slonp=slonv
            
            call grhilo_proc_psl(
     $           psl,ktau,
     $           ib,ie,jb,je,
     $           flat,flon,vcrit,
     $           slatp,slonp,spsl,spsldef)
            
            if(verb) write(*,
     $           '(a,i2,i4,4(f7.2,2x))')
     $           'PSL: ',n,ktau,slatp,slonp,spsl,spsldef
            
            
c--       load vort fix if wind not found
c         
            
            iloc=0
            
            slat=slatwkc
            slon=slonwkc
            
            if(abs(slat).gt.90.0) iloc=1
            
            
C--       abslat bounds check, if > rlatmax then stop tracking, first for sfc wind center
            if(abs(slat).ge.rlatmax.and.abs(slat).lt.90.0) then 
              iloc=0
            endif
            
C--       abslat bounds check, if > rlatmax then stop tracking, second if using vort center
            if (iloc.gt.0 .and. abs(slatv).le.rlatmax) then 
              
              slat=slatv
              slon=slonv
              
              write(*,'(a,1x,a,2x,i03,2x,5(f8.2,1x))') 
     $             'BACKUP ',tcyc(n)(1:3),
     $             ktau,slon,slat,svort,flon,flat

              gdat(1,kc,n,0) = slat
              gdat(2,kc,n,0) = slon

              call clltxy (slat,slon,
     $             blat,blon,dlat,dlon,ni,nj,
     $             xc,yc,
     $             ierr)

              gdat(3,kc,n,0) = xc
              gdat(4,kc,n,0) = yc
C         
C         first confidence factor to -1 to indicate vorticity posit
C         
              gdat(7,kc,n,0) = -1
C         
C         second confidence fact to max cyclone vort (10**-5 s**-1)
C         
              gdat(8,kc,n,0) = abs(svort)
C         
C         third factor = 0
C         
              gdat(9,kc,n,0) = 0
              
            endif
              
c***      past initial position

            if (kcl.ne.0 .and. slat.lt.90.0) then

c--       calculate heading and distance from last location to new location, use rhumb line

              flat=gdat(1,kcl,n,0)
              flon=gdat(2,kcl,n,0)
              call rcalhdst (flat,flon,slatv,slonv,head,dist)
              gdat(5,kc,n,0) = head
              gdat(6,kc,n,0) = dist
              forspd=dist/dtau

c--       check forward speed, if > forspdMX, stop tracking
c
              speedBrake=.false.

              if(forspd.ge.forspdMX .and. doSpeedBrake) then
                speedBrake=.true.
                print*,'HHHHHHHHHHHHHHHHHHHHH hit the brakes!',rtau
                gdat(1,kc,n,0) = 99.9
                gdat(2,kc,n,0) = 999.9
                gdat(3,kc,n,0) = 999.9
                gdat(4,kc,n,0) = 999.9
                gdat(5,kc,n,0) = 999.99
                gdat(6,kc,n,0) =  99.99*dtau
                gdat(7,kc,n,0) = 0.0
                gdat(8,kc,n,0) = 0.0
                gdat(9,kc,n,0) = 0.0

              endif             ! -- speed brake
              
c--         transfer initial heading and distance
           elseif (kcl .eq. 0) then
              flat=gdat(1,kcl,n,0)
              flon=gdat(2,kcl,n,0)
              gdat(5,kc,n,0)  = gdat(5,kcl,n,0)
              gdat(6,kc,n,0)  = gdat(6,kcl,n,0)
              gdat(7,kcl,n,0) = 0.0
              gdat(8,kcl,n,0) = 0.0
              gdat(9,kcl,n,0) = 0.0
              
           endif               ! --kcl.ne.0 .and. slat.lt.90.0
           
c--       load vort tracker into ,1 and slp in ,2

            headv=999.9
            distv=999.9*dtau
            
            if(slatv.lt.90.0)   call rcalhdst (flat,flon,slatv,slonv,headv,distv)
            
            gdat(1,kc,n,1) = slatv
            gdat(2,kc,n,1) = slonv
            gdat(3,kc,n,1) = 999.9
            gdat(4,kc,n,1) = 999.9
            gdat(5,kc,n,1) = headv
            gdat(6,kc,n,1) = distv
            gdat(7,kc,n,1) = 0.0
            gdat(8,kc,n,1) = 0.0
            gdat(9,kc,n,1) = 0.0
            
            headp=999.9
            distp=999.9*dtau
            
            if(slatv.lt.90.0)   call rcalhdst (flat,flon,slatp,slonp,headp,distp)
            
            gdat(1,kc,n,2) = slatp
            gdat(2,kc,n,2) = slonp
            gdat(3,kc,n,2) = 999.9
            gdat(4,kc,n,2) = 999.9
            gdat(5,kc,n,2) = headp
            gdat(6,kc,n,2) = distp
            gdat(7,kc,n,2) = 0.0
            gdat(8,kc,n,2) = 0.0
            gdat(9,kc,n,2) = 0.0
            
            if(doGdatCon) then

              fixlat(1)=slatwkc
              fixlon(1)=slonwkc
              fixlat(2)=slatv
              fixlon(2)=slonv
              fixlat(3)=slatp
              fixlon(3)=slonp
              
              call conGdat(fixlat,fixlon,conLat,conLon,ifixbase,npcon)
              
c--       finalize the output posit

              if((npcon .gt. 0) .and. (gdat(1,kc,n,0) .lt. 90.0) ) then
                
                call rcalhdst (flat,flon,conLat,conLon,headf,distf)
                
                gdat(1,kc,n,0) = conLat
                gdat(2,kc,n,0) = conLon
                
c***      causes a seq fault if uncommented...  sheesh
cc        gdat(3,kc,n,0) = 0.0
cc        gdat(4,kc,n,0) = 0.0
                
                if (kcl .eq. 0) then
                  gdat(5,kc,n,0)  = gdat(5,kcl,n,0)
                  gdat(6,kc,n,0)  = gdat(6,kcl,n,0)
                else
                  gdat(5,kc,n,0) = headf
                  gdat(6,kc,n,0) = distf
                endif
                
                if(ifixbase.ne.1) then
                  gdat(7,kc,n,0) = -1.0*ifixbase
                  if(ifixbase.eq.2) then
                    gdat(8,kc,n,0) = abs(svort)
                  endif
                  if(ifixbase.eq.3) then
                    gdat(8,kc,n,0) = spsl
                  endif
                endif
                
c--       put # of fixes in the consensus here...
                gdat(9,kc,n,0)=npcon
                
              endif             ! if npcon > 0 and the tracker has not been terminated because of
                                ! either sfc wind shift or 925 vort has gone below thresholds

            endif               ! --- doGdatCon

          endif                 ! -- have a first guess for flat/flon

        end do                  ! -- n=1,nbog
        
      endif                     ! -- if nbog > 0
      
      ierr=0

      return

 810  continue

      print*, 'spd < 0 at i,j = ',i,j,' val = ',spd(i,j)
      stop 810
      
      end

