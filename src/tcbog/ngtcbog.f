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
      parameter (mxobs=30, nstms=15, lb=9, lbm1=lb -1)
c
      include 'parmg.h'
      include 'cnstnt.h'
c
      character*1  iflg,ibsn,nobsn
      character*3  trec,stmid
      character*5  iblk
      character*8  jdtg
      character*40 irpt(2400),icard
      character*48 ngtfils, datfil, ngtrp, ngtrpo

      character stid*8
      logical verb
      
c
      integer ioe
      real cycspd
c
      dimension phi(imgaus,jmgp2,lb),u(imgaus,jmgp2,lb)
     x     ,    v(imgaus,jmgp2,lb)

      dimension phis(imgaus,jmgp2,lb),us(imgaus,jmgp2,lb)
     x     ,    vs(imgaus,jmgp2,lb)

      dimension phisav(imgaus,jmgp2,lb),usav(imgaus,jmgp2,lb)
     x     ,    vsav(imgaus,jmgp2,lb),

     $     dum1(ni,nj),dum2(ni,nj),dum3(ni,nj),anu(1)
      
      dimension phif(imgaus,jmgaus,lb),uf(imgaus,jmgaus,lb)
     x,      vf(imgaus,jmgaus,lb),dum(imgaus,jmgaus)

      dimension 

     $     fgu(mxobs,lb),fgv(mxobs,lb),
     $     fguc(mxobs,lb),fgvc(mxobs,lb),
     $     fgub(mxobs,lb),fgvb(mxobs,lb),

     $     tcum(mxobs,lb),tcvm(mxobs,lb),
     $     tcrd(mxobs,lb),tcrs(mxobs,lb),
     $     tcu(mxobs,lb),tcv(mxobs,lb),
     $     tcru(mxobs,lb),tcrv(mxobs,lb),

     $     tcz(mxobs,lb),

     $     zo(mxobs,lb),

     $     iob(mxobs),job(mxobs),xind(mxobs),yind(mxobs),
     $     xin(mxobs),yin(mxobs),
     $     pix(mxobs,4),pjy(mxobs,4),
     $     blat(mxobs),blon(mxobs),w1(10*mxobs),
     $     plat(mxobs),plon(mxobs),phiper(mxobs),
     $     ucorr(lb),vcorr(lb)

      dimension slat(nstms),slon(nstms),svmax(nstms),spmin(nstms),smr50(nstms),
     $     smr30(nstms),istmno(nstms),ibsn(nstms),
     $     vmean(nstms),umean(nstms),nstrm(nstms),nobsn(nstms),
     $     nobgob(nstms)

      dimension fxx(imgaus,jmgp2),fyy(imgaus,jmgp2),
     $     tp1(mxobs,4),tp2(mxobs,4),tp3(imgaus,jmgp2)

      dimension vinten(lb),sdeg(mxobs),sang(mxobs)
      dimension phiu(lb),phiuog(lb),zstd(lb),pres(lb)
      dimension w(12024)

      character pfile*120,ffile*120,ofiletxt*120,ofilefgge*120,obsfile*120,opt*3,copt*2

      logical smthtc,addinflow,domass,ukmobg,proxcheck

cccc      equivalence (w(25),irpt)

C**********************************************************************         
C         
C         setup constants and parameters of the bogus
C
C**********************************************************************         

      data irpt/2400*'                                        '/
      data nlvls/6/

CCCc        sdeg is the number of degrees away from the bogus center.
CCC      data sdeg/  0.0,  2.0,  2.0,  2.0,  2.0,  4.0,  4.0,  4.0,  4.0
CCC     1         ,  6.0,  6.0,  6.0,  6.0,17*0.0/
CCCc          sang is the angle of rotation from the bogus center.
CCC     data sang/  0.0,  0.0, 90.0,180.0,270.0, 45.0,135.0,225.0,315.0
CCC     1     ,  0.0, 90.0,180.0,270.0,17*0.0/


Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn         
C         
C         V32 of bogus - 5 point stencil; UKMO bg (motion)
C
Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn         

      data ntcobs/5/
      data ntcobs_mid/5/
      data ntcobs_inner/5/

C         
C 200908 -- 1.5 deg vice 2.0         
C
C      data sdeg/
C     $     0.0,
C     $     1.5, 1.5, 1.5, 1.5,
C     $     3.0, 3.0, 3.0, 3.0,
C     $     4.5, 4.5, 4.5, 4.5,
C     $     17*0.0/
C         
C 20090929 -- change back after talking with jeff whitaker         
C
      data sdeg/
     $     0.0,
     $     2.0, 2.0, 2.0, 2.0,
     $     4.0, 4.0, 4.0, 4.0,
     $     6.0, 6.0, 6.0, 6.0,
     $     17*0.0/

      data sang/
     $       0.0,
     $       0.0,  90.0, 180.0, 270.0,
     $      45.0, 135.0, 225.0, 315.0,
     $       0.0,  90.0, 180.0, 270.0,
     $     17*0.0/


c          vinten is the weight of the bogus wind intensity
c          in the vertical.

      data vinten/0.00,0.00,0.35,0.65,0.85,0.95,1.00,1.00,1.00/
C         
C  pressure levels of data; and standard heights         
C
      data pres/200.,250.,300.,400.,500.,700.,850.,925.,1000./
      data zstd/11784.,10363.,9164.,7185.,5574.,3012.,1457.,762.,111./

      data trec/'GTO'/
      data g/9.80665/
      data pi/3.14159/
      data radius/6371229.0/

Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss         
C         
C         new constraints
C
Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss         

      data rinflow_1000/20.0/
      data rinflow_925/10.0/
      data bdist_inner/2.5/

      data smthtc/.false./
      data addinflow/.true./
      data domass/.false./

C         
C  turn off proxmity check in case of dups         
C
      data proxcheck/.false./
C         
C  V32 - yes         
C
      data ukmobg/.true./

Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
C         
C         command line 
C
Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      iopt=999
      verb=.false.
      copt=''         

ccc      call getarg(1,ffile)
      call getarg(1,pfile)
      call getarg(2,ofilefgge)
      call getarg(3,ofiletxt)
      call getarg(4,obsfile)
      call getarg(5,copt) 

      narg=iargc()
      
ccc       if(narg.lt.4) then
      if(narg.lt.4) then

        print*,'Arguments to ngtbog:'
        print*,' '
        print*,'        pfile : position file'
        print*,'    ofilefgge : output FGGE obs file'
        print*,'     ofiletxt : output txt obs file'
        print*,'      obsfile : grads obs file'
        print*,' '
        print*,' [copt] : optional character option:'
        print*,' '
        print*,'          -v verbose'
        print*,' '
        print*,'Example'
        print*,' '
        print*,'ngtcbog.x tcbog.posits.txt tcbog.fgge.txt tcbog.txt tcbog.obs'
        print*,' '
        stop 

      endif

      if(copt.eq.'-v') verb=.true. 


C**********************************************************************         
C         
C         setup - options
C
C**********************************************************************

      nobs = min0 (ntcobs,mxobs)

      do i=1, nstms
        nobgob(i) = nobs
      end do

      ltop   = lb-nlvls +1
      d2r    = pi/180.0
      r2d    = 180.0/pi
      onedeg = 2*pi*radius/360.0
      omega4 = 4*pi/86400.0
      pid2=pi*0.5
c
      msg=2
      itype=0
      lenx=12024
      len=2400

      jdtg='87090700'
      nlrec=nlvls+1
      jrecmx=1800/nlrec


COOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
C         
C         open files
C
COOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

      if(.not.ukmobg) then
        open(10,file=ffile,
     $       form='unformatted',status='old',
     $       err=875)

      endif

      iunito=69
      open(iunito,file=obsfile,
     $     form='unformatted',status='unknown',
     $     err=862)

      open(unit=26,file=pfile,
     $     form='formatted',status='old',
     $     err=865)

      open(unit=70,file=ofilefgge,
     $     form='formatted',status='unknown',
     $     err=870)

      open(unit=71,file=ofiletxt,
     $     form='formatted',status='unknown',
     $     err=871)



CTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
C         
C  tc data       
C         
CTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

C
C         read tropical cyclone data from reanalysis best track files
C
      call gettrp (nstms,numbstm,noldstm,jdtg,slat,slon,svmax,spmin,
     &     smr50,smr30,istmno,ibsn,jdtgo,umean,vmean,nstrm,nobsn)
      
      do n=1,numbstm
        write(stmid,'(i02,a1)') istmno(n),ibsn(n)
        if(stmid(1:1).eq.' ') stmid(1:1)='0'
        iblk='TC'//stmid

Cbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb         
C txt form of the data         
C
        write(71,'(a,a,1x,2(f6.1,1x),1x,f6.2,1x,f6.0,1x,i3)') 'tcvitals: ',iblk,slat(n),slon(n),
     $       svmax(n),spmin(n),n

      enddo


CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
C         
C         field data and calculate gaussian grid
C
CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
        
        if(.not.ukmobg) then
          call getspc (phi,u,v,phif,uf,vf,
     $         zstd,pres,lb,jdtg,iflspc)
          call gausgr
        endif

Ctttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
C         
C  check for depressions; reduce bogus to 9
C         
Ctttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt

        rmw_min_crit=35.0
        rmw_min_crit=rmw_min_crit*0.5144
        dist_sep_min=20.0

        nob_mw_min=ntcobs_mid
        if (numbstm.gt.0) then
          do i=1,numbstm
            if (svmax(i).le.rmw_min_crit) then
              nobgob(i) = min0 (nob_mw_min,nobgob(i))
              print *,'!!!!!!! TS and below set threshold i=',i,' nob = ',nobgob(i)
            endif
          end do
        endif

c
c         check storms for proximity to each other and
c         adjust the number of synthetic observations to 
c         eliminate overlap
c
        
        if ((numbstm.gt.1).and.(proxcheck)) then

          nostm1 = numbstm -1
          do i=1,nostm1
            ip1=i+1
            do j=ip1, numbstm
              avlat = 0.5*(slat(i)+slat(j))*d2r
              dist  = sqrt((slat(i)-slat(j))**2
     x             +(cos(avlat)*(slon(i)-slon(j)))**2)
              print*,'distance check .... ',dist

              if (dist.lt.dist_sep_min) then

c         
c                 Adjust number of bogus points for one or more cyclones
c         
              if (dist .ge. 10.0) then

c         Give cyclone with highest wind speed more bogus

                if (svmax(i) .ge. svmax(j)) then
                  nobgob(i) = min0 (ntcobs,nobgob(i))
                  nobgob(j) = min0 (ntcobs_mid,nobgob(j))
                else
                  nobgob(i) = min0 (ntcobs_mid,nobgob(i))
                  nobgob(j) = min0 (ntcobs,nobgob(j))
                endif
              elseif (dist .ge. 8.0) then
                nobgob(i) = min0 (ntcobs_mid,nobgob(i))
                nobgob(j) = min0 (ntcobs_mid,nobgob(j))
              elseif (dist .ge. 6.0) then
c                     Give cyclone with highest wind speed more bogus
                if (svmax(i) .ge. svmax(j)) then
                  nobgob(i) = min0 (ntcobs_mid,nobgob(i))
                  nobgob(j) = min0 (ntcobs_inner,nobgob(j))
                else
                  nobgob(i) = min0 (ntcobs_inner,nobgob(i))
                  nobgob(j) = min0 (ntcobs_mid,nobgob(j))
                endif
              elseif (dist .ge. 4.0) then
                nobgob(i) = min0 (ntcobs_innner,nobgob(i))
                nobgob(j) = min0 (ntcobs_innner,nobgob(j))
c                    Give cyclone with heighest wind speed more bogus
              elseif (svmax(i) .ge. svmax(j)) then
                nobgob(i) = min0 (ntcobs_innner,nobgob(i))
                nobgob(j) = 0
              else
                nobgob(i) = 0
                nobgob(j) = min0 (ntcobs_innner,nobgob(j))
              endif
            endif
          end do
        end do

      endif

      if(smthtc) then

Cllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
C         
C         save original fields data
C         for smthing
C
Cllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
      
        call load33(u,usav,ni,nj,lb)
        call load33(v,vsav,ni,nj,lb)
        call load33(phi,phisav,ni,nj,lb)

        call load33(u,us,ni,nj,lb)
        call load33(v,vs,ni,nj,lb)
        call load33(phi,phis,ni,nj,lb)

        open(11,file='fld.smth.dat',
     $       form='unformatted',status='unknown')
        
      endif
      
cllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
C
c          cycle over all storms
C
cllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll

      do 105 na=1,numbstm

        write(stmid,'(i2,a1)') istmno(na),ibsn(na)
        if(stmid(1:1).eq.' ') stmid(1:1)='0'
        print 805,istmno(na),ibsn(na),stmid
 805    format(' ','processing tropical storm ',i2,a1,1x,a3)

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
      vm=svmax(na)
      radrat=1.0
      rm=165000.0
      alpha=0.9

c         cms50kt and cms30kt convert 50 and 30 kt to m/s.

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
      if(verb) then
        print 705,stmid,vm,alpha,rm,r50,r30
 705    format(2x,'stmid, vm, alpha, rmax, r50, r30: ',a,5e13.5)
      endif
c
c   determine lat and lon of synthetic observations
c
      do ll=1,nobs
        dlat= cos (sang(ll)*d2r)
        dlon= -sin (sang(ll)*d2r)
        blat(ll)=slat(na)+sdeg(ll)*dlat
        blon(ll)=slon(na)+sdeg(ll)*dlon
        
C         
C         use rhumb lines
C         

cccc        write(*,'(a,i6,4(f7.2,1x))') 'rrrrrrbbbbb ',ll,sang(ll),sdeg(ll),blat(ll),blon(ll)
        call rumlatlon ((sang(ll)+0.0),sdeg(ll)*60.0,slat(na),slon(na),blat(ll),blon(ll))
C         
C reverse dlon -- sang is NOT the bearing from center -> bogus point, but the direction of v component of wind!         
C
        dlon=slon(na)-blon(ll)
        blon(ll)=slon(na)+dlon
        
ccc        write(*,'(a,i6,4(f7.2,1x))') 'rrrrrraaaaa ',ll,sang(ll),sdeg(ll),blat(ll),blon(ll)
        if(verb) write(*,'(a,1x,3f6.1)') 
     $       'lat and lon sang',blat(ll),blon(ll),sang(ll)
      enddo

      cycspd = sqrt (umean(na)**2 +vmean(na)**2)
      print*,'cycspd = ',cycspd

      if (cycspd.gt.15.0) then
c
c         Speed too high to safely use storm motion
c
        print 9600, cycspd
 9600   format (2x,'BAD cyclone position? 12-hr speed= ',f10.1)
        write(*,*)
        write(*,*) 'PUNCH OUT PUNCH OUT PUNCH OUT PUNCH OUT PUNCH OUT PUNCH OUT '
        write(*,*) 'PUNCH OUT for storm ',stmid,' because of fast motion'
        write(*,*) 'PUNCH OUT PUNCH OUT PUNCH OUT PUNCH OUT PUNCH OUT PUNCH OUT '
        write(*,*)

C!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!         
C         
C         bail!
C
C!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        go to 105
        umean(na) = -999.9
        vmean(na) = -999.9

      end if

      print 667, umean(na),vmean(na)
 667  format (2x,' umean, vmean ',2f10.1)

      if(.not.ukmobg) then
        call glogau (blat,blon,xind,yind,nobs)
      endif

Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss         
C         
C         9905
C         tc area smoothing (doesn't work very well yet)
C
Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

      if(smthtc) then

        ximin=xind(1)
        ximax=xind(1)
        dy=float(jmgp2-1)/pi
        yjmin=jmgp2-(pid2-yind(1))*dy
        yjmax=yjmin

        do ll=1,nobs
          ygrid=jmgp2-(pid2-yind(ll))*dy
          if(verb) write(*,'(a,1x,3(f6.2,1x))') 
     $         'x and y ',xind(ll),blat(ll),ygrid

          if(xind(ll).gt.ximax) ximax=xind(ll)
          if(xind(ll).lt.ximin) ximin=xind(ll)

          if(ygrid.gt.yjmax) yjmax=ygrid 
          if(ygrid.lt.yjmin) yjmin=ygrid

        enddo

        ilim=2
        imin=nint(ximin)-ilim
        imax=nint(ximax)+ilim
        jmin=nint(yjmin)-ilim
        jmax=nint(yjmax)+ilim

        print*,'ximin = ',ximin,' ximax = ',ximax
        print*,'imin = ',imin,' imax = ',imax

        print*,'yjmin = ',yjmin,' yjmax = ',yjmax
        print*,'jmin = ',jmin,' jmax = ',jmax

        ricent=xind(1)
        rjcent=jmgp2-(pid2-yind(1))*dy

        rmax=(jmax-jmin)*0.5

        print*,'ricent = ',ricent,' rjcent = ',rjcent

        anu(1)=0.5
        npass=100
        numbnu=1
        io=0
        nrad=3
        brad=0.9
        drad=0.10

        do k=ltop,lb


Cuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
C         
Cuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu

          call load32(us,dum1,ni,nj,lb,k)
          do ismth=1,nrad
            r2=rmax*brad - (ismth-1)*rmax*drad
            r1=r2*0.8
            print*,'us  r1 = ',r1,' r2 = ',r2,'kkkkkk ',
     $           k,' sssss ',npass,brad,drad
            call smthrad(dum1,dum2,dum3,ni,nj,ricent,rjcent,
     $           imin,imax,jmin,jmax,r1,r2,
     $           anu,npass,numbnu,io) 
          end do
          call load23(dum1,us,ni,nj,lb,k)

Cvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
C         
Cvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
          
          call load32(vs,dum1,ni,nj,lb,k)

          do ismth=1,nrad
            r2=rmax*brad - (ismth-1)*rmax*drad
            r1=r2*0.8
            print*,'vs  r1 = ',r1,' r2 = ',r2,'kkkkkk ',k,
     $           ' sssss ',npass
            call smthrad(dum1,dum2,dum3,ni,nj,ricent,rjcent,
     $           imin,imax,jmin,jmax,r1,r2,
     $           anu,npass,numbnu,io) 
            
          end do
          call load23(dum1,vs,ni,nj,lb,k)
          
Cpppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
C         
Cpppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
          
          call load32(phis,dum1,ni,nj,lb,k)

          do ismth=1,nrad
            r2=rmax*brad - (ismth-1)*rmax*drad
            r1=r2*0.8
            print*,'phi   r1 = ',r1,' r2 = ',r2,'kkkkkk ',k,
     $           ' sssss ',npass
            
            call smthrad(dum1,dum2,dum3,ni,nj,ricent,rjcent,
     $           imin,imax,jmin,jmax,r1,r2,
     $           anu,npass,numbnu,io) 
            
          end do

          call load23(dum1,phis,ni,nj,lb,k)
          
        end do

      endif

      if(.not.ukmobg) then
C         
C         run gautrp to initialize arrays
C
        ikeep=0
        call gautrp (xind,yind,xin,yin,fgu(1,1),
     $       nobs,u(1,1,1),w1,ikeep,pix,pjy,
     $       fxx,fyy,tp1,tp2,tp3,imgaus,jmgp2)
c
c         get u and v at pseudo observation locations from the
c         t20 fields
c
      endif

      do k=ltop,lb

        if(.not.ukmobg) then

          call gautrp (xind,yind,xin,yin,fgu(1,k),
     $         nobs,u(1,1,k),w1,ikeep,pix,pjy,
     $         fxx,fyy,tp1,tp2,tp3,imgaus,jmgp2)

          ikeep=1
          call gautrp (xind,yind,xin,yin,fgv(1,k),
     $         nobs,v(1,1,k),w1,ikeep,pix,pjy,
     $         fxx,fyy,tp1,tp2,tp3,imgaus,jmgp2)
          

          print 950,pres(k),k
 950      format(2x,f5.0,' mb level k =',i2)
          sumu=0.0
          sumv=0.0

        end if

        do  n=1,nobs
          sumu=sumu+fgu(n,k)
          sumv=sumv+fgv(n,k)
        end do

        sumu=sumu/nobs
        sumv=sumv/nobs

        if(umean(na).ne.-999.9.and.vmean(na).ne.-999.9) then
          ucorr(k)=umean(na)-sumu
          vcorr(k)=vmean(na)-sumv
        else
          ucorr(k)=0.
          vcorr(k)=0.
        endif

        if(.not.ukmobg) then
          print 956,fgu(1,k),fgv(1,k),sumu,sumv,ucorr(k),vcorr(k)
 956      format(2x,' center u and v ',2f8.1,'  average u and v ',2f8.1
     x         , ' ucorr,vcorr ',2f8.1)
        endif

        do  n=1,nobs
          fgub(n,k)=ucorr(k)
          fgvb(n,k)=vcorr(k)
          fguc(n,k)=fgu(n,k)+ucorr(k)
          fgvc(n,k)=fgv(n,k)+vcorr(k)
          tcum(n,k)=umean(na)
          tcvm(n,k)=vmean(na)

Cuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu         
C         
C         ukmo bg = motion
C
Cuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu         

          if(ukmobg) then
            fguc(n,k)=umean(na)
            fgvc(n,k)=vmean(na)
          endif

        end do

      end do

c
c          compute average geopotential around perimeter
c          of storm (variable phiu) at radius of 6 degrees
c
      nperim=16
      rudeg=6.0
      ru=rudeg*onedeg
      print 825,vm,rm,ru
c
      do ll=1,nperim
        ang=(ll-1)*22.5
        plat(ll)=slat(na)+cos (ang*d2r)*rudeg
        plon(ll)=slon(na)+sin (ang*d2r)*rudeg
      end do


      if(.not.ukmobg) then

        call glogau (plat,plon,xind,yind,nperim)
        ikeep=0
        do k=ltop,lb
c
          phiu(k)=0.
c         
          call gautrp (xind,yind,xin,yin,phiper,nperim,
     $         phi(1,1,k),w1,ikeep,pix,pjy,
     $         fxx,fyy,tp1,tp2,tp3,imgaus,jmgp2)
          
          ikeep=0
          do  ll=1,nperim
            phiu(k)=phiu(k)+phiper(ll)
          end do
          
          phiu(k)=phiu(k)/float(nperim)
          phiu(k)=phiu(k)*g
          print 830,k,phiu(k)
        end do

      endif
c
c********************************************************************
c          use rankine vortex to generate pseudo-obs
c********************************************************************
c

C------------------------------------------------------------
C
C          make pseudo-observations for all storms
C
C          compute terms in constant c2 that do not include f
C
      a1=(ru/rm)
      a2=-2.0*alpha
      a1=a1**a2
      a3=vm*vm/a2
      a1=a1*a3
      c2=phiu(lb)-a1

c          loop over all points to get pseudo-observations

      do ll=1,nobs

c          compute coriolis force at observation point
         
        fcor=omega4*sin (blat(ll)*d2r)

c         take absolute value into account for the s.h.

        fcor=abs(fcor)

c          compute height and wind at observation point
        
        r1=(blat(ll)-slat(na))*onedeg
        avlat=0.5*(blat(ll)+slat(na))
        r2=(blon(ll)-slon(na))*cos (avlat*d2r)*onedeg
        r1=r1*r1+r2*r2
        r1=sqrt(r1)
        a4=((fcor*rm*vm)/(1.0-alpha))*(ru/rm)**(1.0-alpha)

c     check to see if inside radius of max winds

        if (r1.le.rm) then
          tcrs(ll,lb)=vm*(r1/rm)
          a1=(vm/2.0)*(fcor*rm+vm)*((r1/rm)**2.0)
          a2=(fcor*rm*vm/2.0)*(1.0+alpha)/(1.0-alpha)
          a3=vm*vm*(1.0+alpha)/(2.0*alpha)
          zo(ll,lb)=a1+a2-a3+c2-a4
        else
          tcrs(ll,lb)=vm*(r1/rm)**(-alpha)
          if(r1.gt.333000.) then
            tcrs(ll,lb)=tcrs(ll,lb)*(1.2-r1/1111200.)
          endif
          a1=((fcor*rm*vm)/(1.0-alpha))*(r1/rm)**(1.0-alpha)
          a2=(vm*vm/(-2.0*alpha))*(r1/rm)**(-2.0*alpha)
          zo(ll,lb)=a1+a2+c2-a4
        endif

        zo(ll,lb)=zo(ll,lb)/g

c          convert to direction and speed

        tcrd(ll,lb)=450.0-sang(ll)
C         
C  SHEM condition
C         
        if (blat(ll).lt.0.0) tcrd(ll,lb)=tcrd(ll,lb)+180.0

        if(tcrd(ll,lb).gt.360.0) tcrd(ll,lb)=tcrd(ll,lb)-360.0
        if(tcrd(ll,lb).eq.0.0) tcrd(ll,lb)=360.0

c          convert geopotentials to heights to conform to fgge standard
        
        if(verb) then
          print 835,ll,sang(ll),sdeg(ll),blat(ll),blon(ll)
          print 840,r1,tcrd(ll,lb),tcrs(ll,lb),zo(ll,lb),a4
        endif

c          spread obs to all level

        do  k=ltop,lbm1
          tcrd(ll,k)=tcrd(ll,lb)
          tcrs(ll,k)=tcrs(ll,lb)
        end do

Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C         
C         add inflow
C
Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

        if(addinflow) then

          do  k=ltop,lb
            if (blat(ll).lt.0.0) then

              if(pres(k).eq.1000.0) then
                tcrd(ll,k)=tcrd(ll,k)+rinflow_1000
              elseif(pres(k).eq.925.0) then
                tcrd(ll,k)=tcrd(ll,k)+rinflow_925
              endif

            else

              if(pres(k).eq.1000.0) then
                tcrd(ll,k)=tcrd(ll,k)-rinflow_1000
              elseif(pres(k).eq.925.0) then
                tcrd(ll,k)=tcrd(ll,k)-rinflow_925
              endif

            endif

            if(verb) then
              write(*,'(a,2(i3,1x),1x,4(f8.2,2x))') 
     $             'inflow: ',k,ll,blat(ll),blon(ll),pres(k),tcrd(ll,k)
            end if

          end do
        end if

      end do

c------------------------------------------------------------         
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
        if(nobs.eq.ntcobs) then
          zcen=zo(1,lb)
          z2deg=zo(2,lb)
          z4deg=zo(6,lb)
          z6deg=zo(10,lb)
          do ll=1,9
            if(ll.ge.6) then
              zo(ll,lb)=
     $             z6deg*.375+z4deg*.3125+z2deg*.25+zcen*.0625
            else
              if(ll.eq.1) then
                zo(ll,lb)=
     $               z4deg*.125+z2deg*.5+zcen*.375
              else
                zo(ll,lb)=
     $               z6deg*.0625+z4deg*.25+z2deg*.4375+zcen*.25
              endif
            endif
          end do
        endif
      endif


c********************************************************************
c          build the pseudo-observations
c********************************************************************

c          sort through all the observation points

      do 165 i=1,nobs

c          set up first card

        iflg='*'
        ids=11
        ids=15

        iblk='TC'//stmid
        
        ielev=0
        ilat=blat(i)*100.0
        ilon=blon(i)*100.0
        
        bdist=sqrt(
     $       (blat(1)-blat(i))*(blat(1)-blat(i)) + 
     $       (blon(1)-blon(i))*(blon(1)-blon(i)) 
     $       ) 

        imn=0
        irecn=irecn+1

Cbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb         
C txt form of the data         

        write(71,'(a,a,1x,2(f6.1,1x),1x,i3)') 'retrieval: ',iblk,blat(i),blon(i),i

        write (icard,810) 
     $       iflg,ids,iblk,ielev,ilat,ilon,inst,jdtg,
     1       imn,nlrec
 810    format(a1,i2,a5,i4,i5,i5,i2,a8,i2,i3,3x)


        irpt(irecn)=icard
        write(70,'(a)') icard

        print 821,irecn,icard
 821    format(2x,' rec no. ',i5,5x,a40)

c         set up pressure level data
        
        do ka=1,nlvls
          k=lb-ka+1
          ityp=10

c         set up the pressure
          
          ipre=pres(k)*10.0

c         set up the height
C
C  limit to to inner five obs
C         
         
          if (k.eq.lb.and.bdist.le.bdist_inner.and.domass) then
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
            call dftouv (tcrd(i,k),tcrs(i,k),uu,vv)
c
            uu=uu*vinten(k)
            vv=vv*vinten(k)
            tcru(i,k)=uu
            tcrv(i,k)=vv

            if(k.eq.lb) then
              print 911,i,tcrd(i,k),tcrs(i,k),uu,vv,fguc(i,k),fgvc(i,k)
 911          format(2x,'ob no. ',i3,' rankine u and v ',4f8.1,
     $             ' fg u and v',
     $             2x,2f8.1)
            endif
c
            uu=uu+fguc(i,k)
            vv=vv+fgvc(i,k)
c
            call uvtodf (uu,vv,tcrd(i,k),tcrs(i,k))

            tcu(i,k)=uu
            tcv(i,k)=vv
c
            idd=tcrd(i,k)
            iff=tcrs(i,k)
            iwqh=1
            iwqv=1

            oz1000=zo(i,k)
            if(abs(oz1000).le.0.01) oz1000=99999.9

Cbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb         
C txt form of the data         
            
            write(71,'(f6.0,1x,f6.2,1x,f6.2,1x,f7.1)') pres(k),uu,vv,oz1000

          else
            idd=-99
            iff=-99
            iwqh=9
            iwqv=9
          endif
c
c         compute the record number
c         
          irecn=irecn+1
          jrecn=ka+1
c
c          write out the pseudo-observation
c
          write (icard,815) 
     $         ityp,ipre,ihgt,ihqh,ihqv,
     $         itmp,itqh,itqv,
     $         idpd,idqh,idqv,idd,iff,iwqh,iwqv,jrecn

          irpt(irecn)=icard
          print 821,irecn,icard
          write(70,'(a)') icard
        end do
c
c         increment the number of obs on the current record
c
        jobs=jobs+1
        if(jobs.le.jrecmx) goto 165
c
c         output observations if buffer 'irpt' is full
c
        jobs=1
        irecn=0
c         
c         fill observation buffer with blanks
c         
        do ll=1,len
          irpt(ll)='                                        '
        end do

 165  continue

CGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
C         
C         write out obs in grads format
C
CGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

      rt=0.0
      nl=lb-ltop+1

      do ii=1,nobs
        iflag=0
        rlat=blat(ii)
        rlon=blon(ii)
        stid="bogustc\0"

        write(iunito,err=860) stid,rlat,rlon,rt,nl,iflag
        write(iunito,err=860)  (
     $       pres(l),zo(ii,l),
     $       fgu(ii,l),fgv(ii,l),
     $       fgub(ii,l),fgvb(ii,l),
     $       fguc(ii,l),fgvc(ii,l),
     $       tcum(ii,l),tcvm(ii,l),
     $       tcru(ii,l),tcrv(ii,l),
     $       tcu(ii,l),tcv(ii,l),
     $       l=ltop,lb)

      end do

c
c          finished processing data for storm na
c         


 105  continue

Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
C         
C         output smoothed fields for diagnostics
C
Cssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

      if(smthtc) then

        do k=ltop,lb
          call load32(u,dum1,ni,nj,lb,k)
          write(11) dum1
        end do

        do k=ltop,lb
          call load32(us,dum1,ni,nj,lb,k)
          write(11) dum1
        end do

        do k=ltop,lb
          call load32(v,dum1,ni,nj,lb,k)
          write(11) dum1
        end do

        do k=ltop,lb
          call load32(vs,dum1,ni,nj,lb,k)
          write(11) dum1
        end do

        do k=ltop,lb
          call load32(phi,dum1,ni,nj,lb,k)
          write(11) dum1
        end do

        do k=ltop,lb
          call load32(phis,dum1,ni,nj,lb,k)
          write(11) dum1
        enddo

      endif

c          fill observation buffer with blanks
c
      do ll=1,len
        irpt(ll)='                                        '
      end do

c
C         
C         write out end of time record
C         
      rlon=0.0
      rlat=0.0
      rt=0.0
      nlev=0
      print*,'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
      write(iunito,err=860) stid,rlat,rlon,rt,nlev,iflag
      close(10)

c
c          format statements
c
  815 format(i2,i5,i5,i1,i1,i4,i1,i1,i4,i1,i1,i3,i3,i1,i1,i3,3x)
  825 format(' vm=',f10.2,' rm=',f10.2,' ru=',f10.2)
  830 format(' k=',i4,' phiu=',f10.2)
  835 format(' ll=',i3,' sang=',f7.2,' sdeg=',f5.1,' blat=',f7.2
     1      ,' blon=',f7.2)
  840 format(' r1=',f10.2,' do=',f6.2,' fo=',f8.2,' zo=',f10.2
     1     ,' a4=',f10.2)
      go to 999
 860  continue
      print*,'unable to open obs file'
      go to 999
 862  continue
      print*,'unable to open obs file'
      print*,'file = ',obsfile
      go to 999
 865  continue
      print*,'unable to opening position file'
      print*,'file = ',pfile
      go to 999
 870  continue
      print*,'unable to opening fgge output file'
      print*,'file = ',ofilefgge
      go to 999
 871  continue
      print*,'unable to opening txt output file'
      print*,'file = ',ofiletxt
      go to 999
 875  continue
      print*,'unable to opening field data file'
      print*,'file = ',ffile
      go to 999
c         
 999  continue
      stop
      end


      subroutine load33(a,b,ni,nj,nk)
      dimension a(ni,nj,nk),b(ni,nj,nk)
      do k=1,nk
        do i=1,ni
          do j=1,nj
            b(i,j,k)=a(i,j,k)
          end do
        end do
      end do
      return
      end

      subroutine load32(a,b,ni,nj,nk,k)
      dimension a(ni,nj,nk),b(ni,nj)
      do i=1,ni
        do j=1,nj
          b(i,j)=a(i,j,k)
        end do
      end do
      return
      end

      subroutine load23(b,a,ni,nj,nk,k)
      dimension a(ni,nj,nk),b(ni,nj)
      do i=1,ni
        do j=1,nj
          a(i,j,k)=b(i,j)
        end do
      end do
      return
      end

