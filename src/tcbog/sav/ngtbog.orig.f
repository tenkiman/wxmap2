      program ngtbog
C
C.............................START PROLOGUE............................
C
C SCCS IDENTIFICATION:  @(#)ngtbog.f	1.8 1/16/97
C
C CONFIGURATION IDENTIFICATION:
C
C MODULE NAME:  ngtbog
C
C DESCRIPTION:  Main program for NOGAPS tropical bogus
C
C COPYRIGHT:  (c) 1994 FLENUMMETOCCEN
C             U.S. GOVERNMENT DOMAIN
C             ALL RIGHTS RESERVED
C
C CONTRACT NUMBER AND TITLE:
C
C REFERENCES:
C
C CLASSIFICATION:  Unclassified
C
C RESTRICTIONS:
C
C COMPUTER/OPERATING SYSTEM DEPENDENCIES:  C90/Unicos
C
C LIBRARIES OF RESIDENCE:
C
C USAGE:  see tbog.job
C
C PARAMETERS:  none
C
C COMMON BLOCKS:  none
C
C FILES:
C      Name        Unit    Type    Attribute  Usage       Description
C   ----------     ----  --------  --------- -------  ------------------
C
C
C DATA BASES:
C      Name             Table        Usage            Description
C   ----------     --------------  ---------   -------------------------
C
C NON-FILE INPUT/OUTPUT:  none
C
C ERROR CONDITIONS:
C        CONDITION                 ACTION
C    -----------------        ----------------------------
C
C
C
C ADDITIONAL COMMENTS:
C
C.................MAINTENANCE SECTION................................
C
C MODULES CALLED:
C         Name           Description
C        -------     ----------------------
C
C LOCAL VARIABLES AND
C          STRUCTURES:
C
C
C         Name      Type                 Description
C        ------     ----       ----------------------------------
C
C METHOD:
C
C INCLUDE FILES:
C      Name                           Description
C   ---------------    -------------------------------------------------
C
C COMPILER DEPENDENCIES: FORTRAN 77
C
C COMPILE OPTIONS:
C
C MAKEFILE: /a/ops/src/met/nogaps/src/main/tbog_t159l18.mak
C
C RECORD OF CHANGES:
C <<CHANGE NOTICE>> version 1.0 (12 Jan 1994) -- Pauley, R.
C   Initial installation under configuration management.
C
C <<CHANGE NOTICE>> version 1.1 (24 Aug 1994) -- Pauley, R.
C   Revise the tropical depression bogus from 5 to 13 point.
C
C <<CHANGE NOTICE>> version 1.3 (22 Mar 1995) -- Hamilton, H.
C   Add modification for past 12-hr direction and speed of cyclone.
C   (adjust version # to agree with cm)
C
C <<CHANGE NOTICE>> version 1.4 (28 Jun 1995) -- Hamilton, H.
C   Modify open statements so missing subdirectories from a previous
C   abbriviated OPS run will not crash program.
C
C <<CHANGE NOTICE>> version 1.5 (09 Aug 1995) -- Hamilton, H.   
C   Put upper limit on speed of motion to use 12-hr old position in
C   generating the bogus data.
C
C <<CHANGE NOTICE>> version 1.6 (20 Sep 1995) -- Hamilton, H.
C   Check proximity of tropical cyclones and adjust the lateral
C   extent of the bogus to prevent overlap.
C
C <<CHANGE NOTICE>> version 1.7 (09 Oct 1996) -- Hamilton, H.
C   change minimum radius from 50000 to 165000 to better describe 25kt
C   cyclones and correct maximum speed of motion from 30m/s to 15m/s
C   for motion adjustment of background winds.
C
c <<CHANGE NOTICE>> version 1.8 (22 Jan 1997) -- Hamilton, H.
c   add output file of synthetic obs for TX to ECMWF
c
C..............................END PROLOGUE.............................
C
      integer mxobs, nstms, lb, lbm1
      parameter (mxobs=30, nstms=9, lb=9, lbm1=lb -1)
c
      include 'parmg.h'
      include 'cnstnt.h'
c
      character*1  iflg,ibsn,nobsn
      character*3  trec
      character*5  iblk
      character*8  jdtg,idtgs,jdtgo
      character*10 adtg,adtgo
      character*40 irpt(2400),icard
      character*48 ifile, ngtfils, datfil, ngtrp, ngtrpo
c
      integer ioe
      real cycspd
c
      dimension phi(imgaus,jmgp2,lb),u(imgaus,jmgp2,lb)
     x,    v(imgaus,jmgp2,lb)
      dimension ufg(mxobs,lb),vfg(mxobs,lb),do(mxobs,lb)
     x            ,fo(mxobs,lb),zo(mxobs,lb)
     x            ,iob(mxobs),job(mxobs),xind(mxobs),yind(mxobs)
     x            ,blat(mxobs),blon(mxobs),w1(10*mxobs)
     x      ,plat(mxobs),plon(mxobs),phiper(mxobs)
     x,    ucorr(lb),vcorr(lb)
      dimension slat(nstms),slon(nstms),smxv(nstms),smr50(nstms)
     x     ,smr30(nstms),istmno(nstms),ibsn(nstms)
     x,     olat(nstms),olon(nstms),nstrm(nstms),nobsn(nstms)
     x,     nobgob(nstms)
      dimension vinten(lb),sdeg(mxobs),sang(mxobs)
      dimension phiu(lb),phiuog(lb),zstd(lb),pres(lb)
      dimension w(12024)
c
      equivalence (w(25),irpt)
c
      data irpt/2400*'                                        '/
      data nlvls/6/
c          sdeg is the number of degrees away from the bogus center.
      data sdeg/  0.0,  2.0,  2.0,  2.0,  2.0,  4.0,  4.0,  4.0,  4.0
     1         ,  6.0,  6.0,  6.0,  6.0,17*0.0/
c          sang is the angle of rotation from the bogus center.
      data sang/  0.0,  0.0, 90.0,180.0,270.0, 45.0,135.0,225.0,315.0
     1         ,  0.0, 90.0,180.0,270.0,17*0.0/
c          vinten is the weight of the bogus wind intensity
c          in the vertical.
      data vinten/0.00,0.00,0.35,0.65,0.85,0.95,1.00,1.00,1.00/
      data pres/200.,250.,300.,400.,500.,700.,850.,925.,1000./
      data zstd/11784.,10363.,9164.,7185.,5574.,3012.,1457.,762.,111./
      data trec/'GTO'/
      data g/9.80616/
      data pi/3.14159/
      data radius/6371229.0/
      data ngtfils/'ngtfils       '/
c
c                   obtain vlaues for variables thru namelist
c
      namelist/gtfiles/ datfil,ngtrp,ngtrpo,hstdir,pstdir1,pstdir2
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      open (unit=1,file=ngtfils,form='formatted',iostat=ioe)
      if (ioe .ne. 0) then
        print *, 'CANT OPEN ngtfils, abort'
        call exit (1)
c
      endif
      read (1,gtfiles,end=999)
  999 continue
      nobs = min0 (13,mxobs)
      do 20 i=1, nstms
       nobgob(i) = nobs
   20 continue
      ltop   = lb -nlvls +1
      d2r    = pi/180.0
      onedeg = 2*pi*radius/360.0
      omega4 = 4*pi/86400.0
c
      msg=2
      itype=0
      lenx=12024
      len=2400
      call dtgops (adtg,istat)
      idtgs=adtg(3:10)
      nlrec=nlvls+1
      jrecmx=1800/nlrec
c
c            Open ngtrp files, new and 12-hr old
c
      open (unit=26,file=ngtrp,form='formatted',iostat=ioe)
      if (ioe .ne. 0) then
        print *, 'MISSING ngtrp file, abort'
        call exit (1)
c
      endif
c
      open (unit=27,file=ngtrpo,form='formatted',iostat=ioe)
      if (ioe .ne. 0) print *, 'MISSING 12-hr old ngtrp file, continue'
c
c     open (65,file='ecmwf.dat',iostat=ioe)
c     if (ioe .ne. 0) print *, '**** OPEN ERROR on ecmwf.dat file'
c
c         Top of loop for now, +6 and +12 hr processing
c         from base time of ngtrp tropical cyclone data
c
      do 210 nk=1, 3
        jtau=0
        jobs=1
        irecn=0
        do 160 ll=1, len
          irpt(ll) = '                                        '
  160   continue
c
c          read tropical cyclone data from ngtrp file(s)
c
        call gettrp (nstms,numbstm,noldstm,jdtg,slat,slon,smxv,
     &     smr50,smr30,istmno,ibsn,jdtgo,olat,olon,nstrm,nobsn)
c
c           check for matching dtg's
c
        if (jdtg .ne. idtgs) goto 210
c
c          determine number of tropical cyclones
c
c       if (ioe .eq. 0) write (65,9060) numbstm, adtg, nk
c9060   format (i2,' tropical cyclones for ',a10,' nk=',i1)
c
        if (numbstm .le. 0) then
          if (nk .eq. 1) then
            stop 'no +0 hour tropical cyclones'
c
          elseif (nk .eq. 2) then
            stop 'no +6 hour forecast tropical cyclones'
c
          else
            stop 'no +12 hour forecast tropical cyclones'
c
          endif
        endif
        read(jdtg,961) ihour
  961   format(6x,i2)
c
c   get t20 fields
c
      call getspc (phi,u,v,zstd,pres,lb,jdtg,iflspc)
      print 100,iflspc
  100 format(2x,' iflspc = ',i3)
      if(iflspc.eq.99) then
        print *, 'no gaussian grid first guess fields'
        call exit (1)
c
      endif
      call chlen (datfil,lendir)
      ifile=datfil(1:lendir)//trec
      print 991,ifile
  991 format(2x,' ifile = ',a48)
      call gausgr
c
c               check storms for proximity to each other and
c               adjust the number of synthetic observations to 
c               eliminate overlap
c
      if (numbstm .gt. 1) then
        nostm1 = numbstm -1
        do 50 i=1, nostm1
          ip1 = i +1
          do 51 j=ip1, numbstm
            avlat = 0.5*(slat(i) +slat(j))*d2r
            dist  = sqrt ((slat(i) -slat(j))**2
     x             +(cos (avlat)*(slon(i) -slon(j)))**2)
            if (dist .lt. 12.0) then
c
c                 Adjust number of bogus points for one or more cyclones
c
              if (dist .ge. 10.0) then
c                     Give cyclone with highest wind speed more bogus
                if (smxv(i) .ge. smxv(j)) then
                  nobgob(i) = min0 (13,nobgob(i))
                  nobgob(j) = min0 (9,nobgob(j))
                else
                  nobgob(i) = min0 (9,nobgob(i))
                  nobgob(j) = min0 (13,nobgob(j))
                endif
              elseif (dist .ge. 8.0) then
                nobgob(i) = min0 (9,nobgob(i))
                nobgob(j) = min0 (9,nobgob(j))
              elseif (dist .ge. 6.0) then
c                     Give cyclone with highest wind speed more bogus
                if (smxv(i) .ge. smxv(j)) then
                  nobgob(i) = min0 (9,nobgob(i))
                  nobgob(j) = min0 (5,nobgob(j))
                else
                  nobgob(i) = min0 (5,nobgob(i))
                  nobgob(j) = min0 (9,nobgob(j))
                endif
              elseif (dist .ge. 4.0) then
                nobgob(i) = min0 (5,nobgob(i))
                nobgob(j) = min0 (5,nobgob(j))
c                    Give cyclone with heighest wind speed more bogus
              elseif (smxv(i) .ge. smxv(j)) then
                nobgob(i) = min0 (5,nobgob(i))
                nobgob(j) = 0
              else
                nobgob(i) = 0
                nobgob(j) = min0 (5,nobgob(j))
              endif
            endif
   51     continue
   50   continue
      endif
c
c          cycle over all storms
c
      do 105 na=1,numbstm
      print 805,istmno(na),ibsn(na)
c
c             set number of synthetic observations (nobs) for each cyclone
c             skip cyclone if it is too close to a stronger cyclone 
c
      if (nobgob(na) .gt. 0) then
        nobs = nobgob(na)
        print 23, nobs
   23   format (2x,i5,' synthetic obs for this cyclone')
      else
        print 22
   22   format (2x,' no synthetic obs for this cyclone')
        go to 105
c
      endif
c
c          compute initial position of the storm
c
      vm=smxv(na)
      radrat=1.0
      rm=165000.0
      alpha=0.9
c     cms50kt and cms30kt convert 50 and 30 kt to m/s.
      cms50kt = 50.0/1.94595
      cms30kt = 30.0/1.94595
      r50 = smr50(na)*radrat
      r30 = smr30(na)*radrat
c     convert n.mi.to meters
      r50 = 1852.0*r50
      r30 = 1852.0*r30
      if(r50.gt.0.0.and.r30.gt.0.0) then
      alpha = alog(30./50.)/alog(r50/r30)
      if(alpha.gt.0.9) alpha = 0.9
         rm = r50*(cms50kt/vm)**(1.0/alpha)
      else
         if(r50.gt.0.0) then
            rm = r50*(cms50kt/vm)**(1.0/alpha)
         else
            if(r30.gt.0.0) then
               rm = r30*(cms30kt/vm)**(1.0/alpha)
            endif
         endif
      endif
c
      print 705,alpha,rm,r50,r30
  705 format(2x,'alpha, rmax, r50, r30 ',4e13.5)
c
c   determine lat and lon of synthetic observations
c
      do 110 ll=1,nobs
      dlat= cos (sang(ll)*d2r)
      dlon= -sin (sang(ll)*d2r)
      blat(ll)=slat(na)+sdeg(ll)*dlat
      blon(ll)=slon(na)+sdeg(ll)*dlon
      print 970,blat(ll),blon(ll)
  110 continue
  970 format(2x,'lat and lon ',2f6.1)
c
c  determine storm motion from 12-hour old position, if possible
c
      if(noldstm.gt.0) then
        do 665 nold=1, noldstm
          if(nstrm(nold).eq.istmno(na).and.nobsn(nold).eq.ibsn(na)) then
c
c                   Found 12-hr old position
c                     (Note: speed in m/s NOT kts)
c
            vmean = onedeg*(slat(na)-olat(nold))/(12.0*3600.0)
            avlat = 0.5*(olat(nold) +slat(na))*d2r
            umean=onedeg*cos (avlat)*(slon(na)-olon(nold))/(12.0*3600.0)
            cycspd = sqrt (umean**2 +vmean**2)
            if (cycspd .le. 15.0) then
c
c                   Valid speed to use storm motion
c
              goto 668
c
            else
c
c                   Speed too high to safely use storm motion
c
              print 9600, cycspd
 9600         format (2x,'BAD cyclone position? 12-hr speed= ',f10.1)
              goto 666
c
            endif
          endif
  665   continue
  666   continue
        umean = -999.9
        vmean = -999.9
      else
        umean = -999.9
        vmean = -999.9
      endif
  668 continue
      print 667, umean,vmean
  667 format (2x,' umean, vmean ',2f10.1)
      call glogau (blat,blon,xind,yind,nobs)
      ikeep=0
c
c          get u and v at pseudo observation locations from the
c          t20 fields
c
      do 115 k=ltop,lb
      call gautrp (xind,yind,ufg(1,k),nobs,u(1,1,k),w1,ikeep)
      ikeep=1
      call gautrp (xind,yind,vfg(1,k),nobs,v(1,1,k),w1,ikeep)
      print 950,pres(k)
      sumu=0.0
      sumv=0.0
      do 1015 n=1,nobs
      sumu=sumu+ufg(n,k)
      sumv=sumv+vfg(n,k)
 1015 continue
      sumu=sumu/nobs
      sumv=sumv/nobs
      if(umean.ne.-999.9.and.vmean.ne.-999.9) then
      ucorr(k)=umean-sumu
      vcorr(k)=vmean-sumv
      else
      ucorr(k)=0.
      vcorr(k)=0.
      endif
      print 956,ufg(1,k),vfg(1,k),sumu,sumv,ucorr(k),vcorr(k)
  956 format(2x,' center u and v ',2f8.1,'  average u and v ',2f8.1
     x, ' ucorr,vcorr ',2f8.1)
      do 1115 n=1,nobs
      ufg(n,k)=ufg(n,k)+ucorr(k)
      vfg(n,k)=vfg(n,k)+vcorr(k)
 1115 continue
  115 continue
  950 format(2x,f5.0,' mb level')
c
c          compute average geopotential around perimeter
c          of storm (variable phiu) at radius of 6 degrees
c
      nperim=16
      rudeg=6.0
      ru=rudeg*onedeg
      print 825,vm,rm,ru
c
      do 125 ll=1,nperim
      ang=(ll-1)*22.5
      plat(ll)=slat(na)+cos (ang*d2r)*rudeg
      plon(ll)=slon(na)+sin (ang*d2r)*rudeg
  125 continue
      call glogau (plat,plon,xind,yind,nperim)
      ikeep=0
      do 190 k=ltop,lb
c
      phiu(k)=0.
c
      call gautrp (xind,yind,phiper,nperim,phi(1,1,k),w1,ikeep)
      ikeep=1
      do 126 ll=1,nperim
      phiu(k)=phiu(k)+phiper(ll)
  126 continue
c
      phiu(k)=phiu(k)/16.0
      phiu(k)=phiu(k)*g
      print 830,k,phiu(k)
c
  190 continue
c
c
c********************************************************************
c          use rankine vortex to generate pseudo-obs
c********************************************************************
c
c
c          make pseudo-observations for all storms
c
c          compute terms in constant c2 that do not include f
c
      a1=(ru/rm)
      a2=-2.0*alpha
      a1=a1**a2
      a3=vm*vm/a2
      a1=a1*a3
      c2=phiu(lb)-a1
c
c          loop over all points to get pseudo-observations
c
      do 155 ll=1,nobs
c
c          compute coriolis force at observation point
c
      fcor=omega4*sin (blat(ll)*d2r)
c          take absolute value into account for the s.h.
      fcor=abs(fcor)
c
c          compute height and wind at observation point
c
      r1=(blat(ll)-slat(na))*onedeg
      avlat=0.5*(blat(ll)+slat(na))
      r2=(blon(ll)-slon(na))*cos (avlat*d2r)*onedeg
      r1=r1*r1+r2*r2
      r1=sqrt(r1)
      a4=((fcor*rm*vm)/(1.0-alpha))*(ru/rm)**(1.0-alpha)
c
c     check to see if inside radius of max winds
c
      if (r1.le.rm) then
         fo(ll,lb)=vm*(r1/rm)
         a1=(vm/2.0)*(fcor*rm+vm)*((r1/rm)**2.0)
         a2=(fcor*rm*vm/2.0)*(1.0+alpha)/(1.0-alpha)
         a3=vm*vm*(1.0+alpha)/(2.0*alpha)
         zo(ll,lb)=a1+a2-a3+c2-a4
      else
         fo(ll,lb)=vm*(r1/rm)**(-alpha)
      if(r1.gt.333000.) then
      fo(ll,lb)=fo(ll,lb)*(1.2-r1/1111200.)
      endif
         a1=((fcor*rm*vm)/(1.0-alpha))*(r1/rm)**(1.0-alpha)
         a2=(vm*vm/(-2.0*alpha))*(r1/rm)**(-2.0*alpha)
         zo(ll,lb)=a1+a2+c2-a4
      endif
      zo(ll,lb)=zo(ll,lb)/g
c
c          convert to direction and speed
c
      do(ll,lb)=450.0-sang(ll)
      if (blat(ll).lt.0.0) do(ll,lb)=do(ll,lb)+180.0
      if(do(ll,lb).gt.360.0) do(ll,lb)=do(ll,lb)-360.0
      if(do(ll,lb).eq.0.0) do(ll,lb)=360.0
c
c          convert geopotentials to heights to conform to fgge standard
c
c
      print 835,ll,sang(ll),sdeg(ll),blat(ll),blon(ll)
      print 840,r1,do(ll,lb),fo(ll,lb),zo(ll,lb),a4
c
c          spread obs to all level
c
      do 150 k=ltop,lbm1
      do(ll,k)=do(ll,lb)
      fo(ll,k)=fo(ll,lb)
  150 continue
c
  155 continue
c
c
c  smooth synthetic 1000 mb height observations
c
c  set ismoo = 1 , if smoothing is desired
c  smoothing only performed when nobs = 13
c  ob at storm center - ll of 1
c  obs at 2 degree radius - ll from 2 to 5
c  obs at 4 degree radius - ll from 6 to 9
c  obs at 6 degree radius - ll from 10 to 13
c
c  obs at 6 degree radius are untouched by the smoother
c
      ismoo=0
      if(ismoo.eq.1) then
      if(nobs.eq.13) then
      zcen=zo(1,lb)
      z2deg=zo(2,lb)
      z4deg=zo(6,lb)
      z6deg=zo(10,lb)
      do 156 ll=1,9
      if(ll.ge.6) then
      zo(ll,lb)=z6deg*.375+z4deg*.3125+z2deg*.25+zcen*.0625
      else
        if(ll.eq.1) then
        zo(ll,lb)=z4deg*.125+z2deg*.5+zcen*.375
        else
        zo(ll,lb)=z6deg*.0625+z4deg*.25+z2deg*.4375+zcen*.25
        endif
      endif
  156 continue
      endif
      endif
c
c
c********************************************************************
c          build the pseudo-observations
c********************************************************************
c
c
c
c          sort through all the observation points
c
      do 165 i=1,nobs
c
c          set up first card
c
      iflg='*'
      ids=11
      iblk='BOGUS'
      ielev=0
      ilat=blat(i)*100.0
      ilon=blon(i)*100.0
      inst=99
      imn=0
      irecn=irecn+1
c
      write (icard,810) iflg,ids,iblk,ielev,ilat,ilon,inst,jdtg
     1                 ,imn,nlrec
      irpt(irecn)=icard
      print 821,irecn,icard
  821 format(2x,' rec no. ',i5,5x,a40)
c         
c                    write header line of data for TX to ECMWF
c
c     if (ioe .eq. 0) write (65,'(a40)') icard
c
c          set up pressure level data
c
      do 170 ka=1,nlvls
      k=lb-ka+1
      ityp=10
c
c          set up the pressure
c
      ipre=pres(k)*10.0
c
c          set up the height
c
      if (k.eq.lb) then
         ihgt=zo(i,k)
         ihqh=1
         ihqv=1
      else
         ihgt=-9999
         ihqh=9
         ihqv=9
      endif
c
c          set up the temperature
c
      itmp=-999
      itqh=9
      itqv=9
c
c          set up the moisture
c
      idpd=-999
      idqh=9
      idqv=9
c
c          set up the direction and speed - add in the background
c          wind from the first-guess field
c
      if (vinten(k).gt.0.0) then
        call dftouv (do(i,k),fo(i,k),uu,vv)
c
        uu=uu*vinten(k)
        vv=vv*vinten(k)
      if(k.eq.lb) then
c     print 911,i,uu,vv,ufg(i,k),vfg(i,k)
c 911 format(2x,'ob no. ',i3,' rankine u and v ',2f8.1,' fg u and v'
c    x,2x,2f8.1)
      endif
c
          uu=uu+ufg(i,k)
          vv=vv+vfg(i,k)
c
        call uvtodf (uu,vv,do(i,k),fo(i,k))
c
        idd=do(i,k)
        iff=fo(i,k)
        iwqh=1
        iwqv=1
      else
        idd=-99
        iff=-99
        iwqh=9
        iwqv=9
      endif
c
c          compute the record number
c
      irecn=irecn+1
      jrecn=ka+1
c
c          write out the pseudo-observation
c
      write (icard,815) ityp,ipre,ihgt,ihqh,ihqv,itmp,itqh,itqv
     1                 ,idpd,idqh,idqv,idd,iff,iwqh,iwqv,jrecn
      irpt(irecn)=icard
      print 821,irecn,icard
c         
c                    write sounding data for TX to ECMWF
c
c     if (ioe .eq. 0) write (65,'(a40)') icard
  170 continue
c
c          increment the number of obs on the current record
c
      jobs=jobs+1
      if(jobs.le.jrecmx) goto 165
c
c          output observations if buffer 'irpt' is full
c
      ktau=jtau+ihour*10000
      call nfwrit (ifile,msg,itype,1,1,lenx,w,ktau,jdtg,istat)
      jtau=jtau+1
      jobs=1
      irecn=0
c
c          fill observation buffer with blanks
c
      do 175 ll=1,len
      irpt(ll)='                                        '
  175 continue
c
  165 continue
c
c          finished processing data for storm na
c
  105 continue
c          output remaining observations
c
      ktau=jtau+ihour*10000
      call nfwrit (ifile,msg,itype,1,1,lenx,w,ktau,jdtg,istat)
      jtau=jtau+1
c
c          fill observation buffer with blanks
c
      do 180 ll=1,len
      irpt(ll)='                                        '
  180 continue
  210 continue
c
      if (ioe .eq. 0) then
c       rewind (65)
c       close (65)
      endif
c
c          format statements
c
  805 format(' ','processing tropical storm ',i2,a1)
  810 format(a1,i2,a5,i4,i5,i5,i2,a8,i2,i3,3x)
  815 format(i2,i5,i5,i1,i1,i4,i1,i1,i4,i1,i1,i3,i3,i1,i1,i3,3x)
  825 format(' vm=',f10.2,' rm=',f10.2,' ru=',f10.2)
  830 format(' k=',i4,' phiu=',f10.2)
  835 format(' ll=',i3,' sang=',f7.2,' sdeg=',f5.1,' blat=',f7.2
     1      ,' blon=',f7.2)
  840 format(' r1=',f10.2,' do=',f6.2,' fo=',f8.2,' zo=',f10.2
     1      ,' a4=',f10.2)
c
      stop
      end
