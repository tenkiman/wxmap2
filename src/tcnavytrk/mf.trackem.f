      subroutine mftrackem(
     $     spd,vort,psl,
     $     rtau,ktau,
     $     nwrt,tcyc,numv,
     $     mxhr,nbog,ntrk,ierr)

      use trkParams
      use f77OutputMeta
      use mfutils

      logical verb,speedBrake,realverb

      logical testTR,testET,testAC

      integer numv, mxhr,  nbog, ktau, ntrk

      real*4 spd(ni,nj),vort(ni,nj),psl(ni,nj),rtau

      real fixlat(maxfix),fixlon(maxfix)

      real forspdMX

      character*28 tcyc(maxtc+1),curstm


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
      realverb=.false.
ccc      verb=.true.

      oformat='g10.4'
      pcntile=0.7


         
C--       set search limit         
C
      
      kc=1+ktau/dtau
      kcl=kc-1
      if(kcl.lt.0) kcl=0

      if(nbog.gt.0) then

        do n=1,nbog
          
          curstm=tcyc(n)(1:3)

          if(verb) then
            print*
            print*,'MFT mftrackem --- nbog loop',n,tcyc(n)(1:3),' kc,kcl: ',kc,kcl,
     $           'ktau: ',ktau,
     $           ' *******************************************'
          endif

C--       get current and t-1 sfc wind tracker if a tc found, if not, then use
C         mine and put into the gdat array

          slatwkc=gdat(1,kc,n,0)
          slonwkc=gdat(2,kc,n,0)

          slatwkcl=gdat(1,kcl,n,0)
          slonwkcl=gdat(2,kcl,n,0)

          slatwkcl=gdat(1,kcl,n,0)
          slonwkcl=gdat(2,kcl,n,0)

          headwkcl = gdat(5,kcl,n,0)
          distwkcl = gdat(6,kcl,n,0)

          slat0=gdat(1,0,n,0)
          slon0=gdat(2,0,n,0)
          head0=gdat(5,0,n,0)
          dist0=gdat(6,0,n,0)
          vmax0=gdat(10,0,n,0)



C--       20080314 -- reduce critical vort for storms <= 30 kt by 25%         
C
          if(vortcritadjust.and.(vmax0.le.vmaxweak)) then
            vcrit=vortcrit*vortadjfact
          else
            vcrit=vortcrit
          endif
          
          if(verb) then
            print*,'MFT mftrackem(initial): slatwkcl, slonwkcl, vmax0: ',slatwkcl,slonwkcl,vmax0
            print*,'MFT mftrackem(initial): headwkcl, distwkcl: ',headwkcl,distwkcl
          endif
          
C--       20110829 -- allow storm to go faster initially for weak storms
c         

          if(doInitialSpdMaxAdj .and. (vmax0.le.vmaxweak) .and. rtau <= forspdMaxTau0) then
            forspdMX=forspdMax*forspdAdjfact
            rmaxConSepMX=rmaxConSep*forspdAdjfact
            if(verb) print*,'MFT mftrackem(forspd): forspdMX adjusted: ',forspdMX,' forspdAdjfact: '
     $           ,forspdAdjfact,'rmaxConSep: ',rmaxConSep,' FFF'
          else
            forspdMX=forspdMax
            rmaxConSepMX=rmaxConSep
          endif

          testET=( (abs(slatwkcl) .ge. forspdLatET) )

          if(testET) then
            forspdMX=forspdMaxET
          endif

c--       sdistmin is the var trkParams module
c
          dlonmax=forspdMX*(dtau/60.0)
          sdistmin=dlonmax*60.0

          if(verb) print*,'MFT mftrackem(dlonmax): dtau: ',dtau,' dlonmax: ',dlonmax,
     $         ' sdistmin: ',sdistmin

          if(slatwkcl.gt.90.) then
            if(verb) print*,'MFT mftrackem(WWW--cycling): dtau: ',dtau,' dlonmax: ',dlonmax,
     $           ' sdistmin: ',sdistmin,'slatwkcl: ',slatwkcl
            cycle

          endif


c--       set the initial motion to input for taus = 0 -> ktauMaxInitialMotion (12 in mf.modules.f)
c         

          slatfg=slatwkcl
          slonfg=slonwkcl
          headfg=headwkcl
          distfg=distwkcl

ccc          print*,'BBB ',kc,slatfg,slonfg,headfg,distfg,n,tcyc(n)(1:3),ktau,'kk',ktauMaxInitialMotion

          if(ktau.le.ktauMaxInitialMotion) then
            slatfg=slat0
            slonfg=slon0
            headfg=head0
            distfg=dist0*float(kc-1)

          elseif(dosmthMotion .and. (ktau.gt.ktauMaxInitialMotion) ) then

            ntau=nint(smthMotionTauPeriod/dtau)+1

            headmean=0.0
            distmean=0.0
            nmean=0

            if(verb) print*,'MSM mf.trackem.dosmthMotion rtau: ',rtau
            do k=1,ntau
              kcmk=kc-k
              if(kcmk.ge.1) then

                headkc=gdat(5,kcmk,n,0)

                if(verb) print*,'MSM NN(mf.trackem.dosmthMotion): ',kc,k,kcmk,headkc,gdat(6,kcmk,n,0)
c--       headkc > 360 is undef
c
                if(headkc.gt.360.0) cycle

c--       take away -180 so head ranges from -180 180
c
                headkc=headkc-180.0
                headmean=headmean+headkc
                distmean=distmean+gdat(6,kcmk,n,0)
                nmean=nmean+1
              endif

            enddo
              
            if(nmean.gt.0) then
              headmean=headmean/nmean
              distmean=distmean/nmean
c--       add back in 180 deg
              headmean=headmean+180.0

              headfg=headmean
              distfg=distmean

            endif
            
            if(verb) print*,'MSM mf.trackem.dosmthMotion ----',kc,nmean,headfg,distfg,n,tcyc(n)(1:3)
            
          endif

ccc          print*,'AAA ',kc,slatfg,slonfg,headfg,distfg,n,tcyc(n)(1:3)

c--       make a first guess using the previous 6-h motion to flat,flon
c         
          call rcaltln (slatfg,slonfg,headfg,distfg,flat,flon)
          
C 20000824 - use initial position vice interpolated for tau = 0         
C         
          if((slatwkcl.lt.90.).and.(slonwkcl.lt.900.).and.ktau.eq.0) then
            flat=slatwkcl
            flon=slonwkcl
          endif
          
          if(verb) then
            print*,'MFT mftrackem(1st guess): flat, flon: ',flat,flon
          endif

c***      main if have an estimated posit to look around

          if((flat.lt.90).and.(flon.lt.900)) then
            
            call clltxy (flat,flon,
     $           blat,blon,dlat,dlon,ni,nj,
     $           egxx,egyy,
     $           ierr)

            call getIJrange(egyy,egxx,
     $           dlonmax,
     $           ib,ie,jb,je)

C         storm must be within sdistmin [nm]
C         of the first guess location and
C         greater than 'vcrit' (10-5 s-1) 
C         to be valid

            if(realverb) then
              qtitle='spd in mftrack [kt]    '
              call qprntn(spd,qtitle,ib,jb,ni,nj,1,6)
              qtitle='vrt in mftrack [s-1]   '
              call qprntn(vort,qtitle,ib,jb,ni,nj,1,6)
            end if

            if(verb) write(*,
     $           '(a,i2,i4,2(f7.2,2x))')
     $           'MFT mftrackem(WND): ',n,ktau,slatwkc,slonwkc
            

            slatv=slatwkcl
            slonv=slonwkcl

            call grhilo_proc_vrt850(
     $           vort,rtau,curstm,
     $           ib,ie,jb,je,
     $           flat,flon,vcrit,
     $           slatv,slonv,svort)

            if(verb)    write(*,
     $           '(a,i2,i4,5(f7.2,2x))')
     $           'MFT mftrackem(VRT): ',n,ktau,flat,flon,slatv,slonv,svort
            
            slatp=slatv
            slonp=slonv
            
            call grhilo_proc_psl(
     $           psl,ktau,
     $           ib,ie,jb,je,
     $           flat,flon,vcrit,
     $           slatp,slonp,spsl,spsldef)
            
            if(verb) write(*,
     $           '(a,i2,i4,7(f7.2,2x))')
     $           'MFT mftrackem(PSL): ',n,ktau,flat,flon,slatp,slonp,spsl,spsldef,rminPsldef

c-------------------------do fix consensus
c            
            if(doGdatCon) then

              fixlat(1)=slatwkc
              fixlon(1)=slonwkc
              fixlat(2)=slatv
              fixlon(2)=slonv
              fixlat(3)=slatp
              fixlon(3)=slonp
              
              call conGdat(fixlat,fixlon,flat,flon,rmaxConSepMX,
     $             conLat,conLon,ifixbase,npcon)
              
c------------------------finalize the con output posit

              if( (npcon .gt. 0) .and. (conLat .lt. 90.0 .and. conLat.lt.rlatmax) ) then
                
c--       heading/distance from previous position
c         
                call rcalhdst (slatwkcl,slonwkcl,conLat,conLon,headf,distf)
                
                gdat(1,kc,n,0) = conLat
                gdat(2,kc,n,0) = conLon
                gdat(3,kc,n,0) = 0.0
                gdat(4,kc,n,0) = 0.0
                
                if (kc .eq. 0) then
                  gdat(5,kc,n,0)  = gdat(5,kcl,n,0)
                  gdat(6,kc,n,0)  = gdat(6,kcl,n,0)
                else
                  gdat(5,kc,n,0) = headf
                  gdat(6,kc,n,0) = distf
                endif
                
                if(verb) write(*,'(a,i2,4x,2(f7.2,2x),a,2(f7.2,2x))') 
     $               'MFT mftrackem(CON): ',kc,gdat(1,kc,n,0),gdat(2,kc,n,0),
     $               ' head/dist: ',gdat(5,kc,n,0),gdat(6,kc,n,0)

                if(npcon > 0) then

                  gdat(7,kc,n,0) = -1.0*ifixbase

                  if(npcon.eq.2 .or. npcon .eq. 12 .or. npcon .eq. 14) then
                    gdat(8,kc,n,0) = abs(svort)
                  endif

                  if(npcon.eq.3 .or. npcon .eq. 13 .or. npcon .eq. 15) then
                    gdat(8,kc,n,0) = spsl
                  endif

                endif
                
c--       put # of fixes in the consensus here...
c
                gdat(9,kc,n,0)=npcon
                
              endif             ! if npcon > 0 and the tracker has not been terminated because of
                                ! either sfc wind shift or 850 vort has gone below thresholds

c--       put con posit in the final slat/slon
c
              slat=conLat
              slon=conLon

            else

c----------------------use wind posit if not doing con
c
              slat=slatwkc
              slon=slonwkc

            endif               ! --- doGdatCon
            


c------------------------------------finalize posit
c         

c-----------------------------ifnot doing con use original check of wind fix and if not there use vort fix
c         
            if(.not.doGdatCon) then
              iloc=0
              if(abs(slatwkc).gt.90.0  ) iloc=1

c--       abslat bounds check, if > rlatmax then stop tracking, first for sfc wind center
c
              if(abs(slatwkc).ge.rlatmax.and.abs(slatwkc).lt.90.0) then 
                iloc=0
              endif
              
c--       abslat bounds check, if > rlatmax then stop tracking, second if using vort center
c--       99999. is the default -- in case can't find one in grhilo_vrt850

              if ( (iloc.gt.0 .and. abs(slatv).le.rlatmax) .and. (.not.doGdatCon) )  then 
              
                write(*,'(a,1x,a,2x,i03,2x,5(f8.2,1x))') 
     $               'BACKUP ',curstm(1:3),
     $               ktau,slatv,slonv,svort,flat,flon
                
                gdat(1,kc,n,0) = slatv
                gdat(2,kc,n,0) = slonv
                
                call clltxy (slatv,slonv,
     $               blat,blon,dlat,dlon,ni,nj,
     $               xc,yc,
     $               ierr)
                
                gdat(3,kc,n,0) = xc
                gdat(4,kc,n,0) = yc
                
C         first confidence factor to -1 to indicate non wind fix
C         
                gdat(7,kc,n,0) = -1
                
C         second confidence fact to max cyclone vort (10**-5 s**-1)
C         
                gdat(8,kc,n,0) = abs(svort)
                
C         third factor = 0
C         
                gdat(9,kc,n,0) = 0
              
              endif

            endif               ! original wind fix + vort fix check
c
c-----------------------------ifnot doing con use original check of wind fix and if not there use vort fix
              
c--       pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp past initial position

            if (kcl.ne.0 .and. slat.lt.90.0) then

c--       calculate heading and distance from last location to new location, use rhumb line

              flat=gdat(1,kcl,n,0)
              flon=gdat(2,kcl,n,0)
              call rcalhdst (flat,flon,slat,slon,head,dist)

              distm1=gdat(6,kcl,n,0)
              forspdm1=distm1/dtau

              gdat(5,kc,n,0) = head
              gdat(6,kc,n,0) = dist
              forspd=dist/dtau

              accel=abs(forspd-forspdm1)

c--       check forward speed, if > forspdMX, stop tracking
c
              testTR=( (forspd.ge.forspdMX)    .and. (abs(slat) .lt. forspdLatET) .and. doSpeedBrake)
              testET=( (forspd.ge.forspdMaxET) .and. (abs(slat) .ge. forspdLatET) .and. doSpeedBrake)

              testAC=( accel .ge. accelMax .and. doAccelBrake)
              if(verb) print*,'AAAcell forspdm1: ',forspdm1,'forspd: ',forspd,' accel: ',accel,accelMax
              
              if(testTR .or. testET) then
                if(testTR) print*,'HHH hit the brakes(TROPICS)  rtau:',rtau,' TC: ',curstm(1:3),'      slat: ',slat,
     $               ' forspd: ',forspd,' forspdMX:   ',forspdMX

                if(testET) print*,'HHH hit the brakes(MID-LATS) rtau:',rtau,' TC: ',curstm(1:3),' abs(slat): ',abs(slat),
     $               ' forspd: ',forspd,' forspdMaxET: ',forspdMaxET

              endif

              if(testAC) then
                print*,'AAA rapid accel  s(TROPICS)  rtau:',rtau,' TC: ',curstm(1:3),'      flat: ',flat,
     $               '  acell: ',accel,' acellMax:   ',accelMax
              endif

              if(testTR .or. testET .or. testAC) then
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
              
c--       transfer initial heading and distance
c
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
           
           if(slatp.lt.90.0)   call rcalhdst (flat,flon,slatp,slonp,headp,distp)
           
           gdat(1,kc,n,2) = slatp
           gdat(2,kc,n,2) = slonp
           gdat(3,kc,n,2) = 999.9
           gdat(4,kc,n,2) = 999.9
           gdat(5,kc,n,2) = headp
           gdat(6,kc,n,2) = distp
           gdat(7,kc,n,2) = 0.0
           gdat(8,kc,n,2) = 0.0
           gdat(9,kc,n,2) = 0.0
           
           
         endif                  ! -- have a first guess for flat/flon

c-------------------------------check of vort and/or psl ok
c         

         if(verb) print*,'MFT mftrackem(Vort/Psl check): ',svort,vcrit,'psl',spsldef,rminPsldef

         if( (svort .gt.  9000.) .and. (spsldef.gt.rminPsldef) ) then
           print*,'BBB bailing !!!! svort: ',svort,'spsldef > rminPsldef: ',spsldef,' tau: ',int(rtau),' stm: ',curstm(1:3)
           gdat(1,kc,n,0) = 99.9
           gdat(2,kc,n,0) = 999.9
           gdat(3,kc,n,0) = 999.9
           gdat(4,kc,n,0) = 999.9
           gdat(5,kc,n,0) = 999.99
           gdat(6,kc,n,0) =  99.99*dtau
           gdat(7,kc,n,0) = 0.0
           gdat(8,kc,n,0) = 0.0
           gdat(9,kc,n,0) = 0.0
         endif
         
         if(verb) print*,'MFT mftrackem(FINAL): ',kc,gdat(1,kc,n,0),gdat(2,kc,n,0),
     $        'head/dist: ',gdat(5,kc,n,0),gdat(6,kc,n,0),svort
         
       end do                   ! -- n=1,nbog
       
      endif                     ! -- if nbog > 0
      
      ierr=0

      return

 810  continue

      print*, 'spd < 0 at i,j = ',i,j,' val = ',spd(i,j)
      stop 810
      
      end

