      program tctrack
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)tctrack.f	1.2 8/7/95
C                        16:28:41 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  tctrack
C
C  DESCRIPTION:  track tropical cyclones in NOGAPS 1000 mb wind fields
C
C  COPYRIGHT:                  (C) 1994 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  none
C
C  CLASSIFICATION:  unclassified
C
C  RESTRICTIONS:  none
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  Cray UNICOS
C
C  LIBRARIES OF RESIDENCE:
C
C  USAGE:
C
C  PARAMETERS:  none
C
C  COMMON BLOCKS:  none
C
C  FILES:  none
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C     i/o error                write diagnostic and exit
C
C  ADDITIONAL COMMENTS:
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         bogread     read NOGAPS tropical cyclone bogus file
C         fldread     read NOGAPS 1000 mb wind fields and produce
C                     and return direction field
C         outgdat     write tracking data to file
C         trackem     track all tropical cyclones in one forecast period
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------------
C           cdtg     char       synoptic date-time-group of initial
C                               cyclone position(s) and NOGAPS analysis
C          ddfld     real       global 1000 mb wind direction (toward)
C                               field, deg
C          fffld     real       global 1000 mb wind speed field (squared)
C          vvfld     real       global 1000 mb wind vorticity (1e-5 s-1)
C           gdat     real       tropical cyclone tracking data
C            igo      int       good/bad flag, 0 no error
C            ioe      int       i/o error flag
C          ni      int       first  dimension (lon) of global fields
C           itau      int       tau of forecast period being used
C           ni      int       first  dimension (lon) of global fields
C          nj      int       second dimension (lat) of global fields
C           nj      int       second dimension (lat) of global fields
C           ktau      int       exported itau value
C          maxtc      int       maximum number of tropical cyclones to
C                               track - maximum allowed in bogus
C          maxhr      int       index to maximum forecast period
C                                  21 = 120 hours
C           nbog      int       number of cyclones to track
C           ntrk      int       number of cyclones being tracked
C         numvar      int       number of variables carried in output
C                               array gdat - first dimension of gdat
C           nwrt      int       unit number of output file tctracks
C           rtau      int       real version of itau
C           tcyc     char       tropical cyclone data from bogus file
C
C  METHOD:
C    1.  Use past heading and speed of cylone to estimate expected
C        position.
C    2.  Use wind direction field to locate approximate location of
C        cyclonic circulations within window covering last known
C        position and the estimated position.
C    3.  If more than one circulation found within window, select the
C        best location for cyclone being tracked.
C    4.  Use isogons to locate the exact center of circulation.
C    5.  Track every six hours till ciculation lost, no more fields or
C        144 hours.
C    6.  Output latitude, longitude, heading, speed of movement,
C        confidence of location factor, wind support factor and
C        isogon intersection support factor for each tracked position.
C
C  INCLUDE FILES:  none
C
C  COMPILER DEPENDENCIES:  Fortran 77
C
C  COMPILE OPTIONS:
C
C  MAKEFILE:
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
C    Add processing of wind speed field, fffld, to improve cyclone selection
C    when more than one cyclone if found in the vicinity of the cyclone being
C    tracked.  Increase last forecast fields from 120 to 144 hours.
C
C...................END PROLOGUE.......................................
C

      
      use trkParams
      use f77OutputMeta
      use f77Output
      use mfutils

      implicit none

      integer iflg

      integer numv, mxhr, mxfct, mxtc, mxtau
      integer iunittco, iunittcm
      integer nbog, igo, ioe, ntrk, itau, ktau, ntau
      integer iunittci,iunittcf,iunittcd
      integer narg
      integer iargc

      character*28 tcyc(maxtc+1)
      character*16 cdtg
      character nlpath*128,tcipath*128,tcopath*128,tcdpath*128,
     $     metapath*128,tcmpath*128
c
      real*4 rtau

      real beglat,beglon
      
      integer istat,n,nwrt,iunit,ierr

c--       allocate the big tracker array in readFldMeta :: gdat




c----------------------------------------------------------------------------------------



Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
C         
C         command line processing
C
Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      call getarg(1,nlpath)
      call getarg(2,tcipath)
      call getarg(3,metapath)
      call getarg(4,tcopath)
      call getarg(5,tcdpath)
      call getarg(6,tcmpath)

      narg=iargc()
      
      if(narg.lt.5) then

        print*,'Arguments to ngtrk.x:'
        print*,' '
        print*,'         nlpath : path to input namelist file'
        print*,'        tcipath : path to input track data (ngtrp) file'
        print*,'       metapath : path to input field meta data file from grads with path to .dat'
        print*,'        tcopath : path to output track file'
        print*,'        tcdpath : path to output diagnostics file'
        print*,'        tcmpath : path to output mf track diagnostics'
        print*,' '
        print*,'now use a namelist...'
        print*,' '
        print*,'ngtrk.x'
        print*,' '
        stop 

      endif




Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C         
C         open files

      iunittci=10
      iunittcd=33
      iunittco=20
      iunittcm=21

ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
c         initialize trkParams

      call inittrkParams(nlpath)


Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C
C         input with positions (ngtrp)

      open(iunittci,file=tcipath(1:ichlen(tcipath,128)),
     $     status='old',err=810)

Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C
C         input meta file with path to .dat with sfc wind, 850 vort, psl

      call readFldMeta(metapath,ierr)

      maxhour=itaus(nt)
      if(nt > 1) dtau=itaus(2)-itaus(1)
      maxhr=((maxhour/dtau)+1)

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C
C         output diagnostics

      open(iunittcd,file=tcdpath(1:ichlen(tcdpath,128)),
     $     status='unknown')

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C
C         output track


      open(iunittco,file=tcopath(1:ichlen(tcopath,128)),
     $     status='unknown')

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C
C         output mf (my tracker) diagnostics

      open(iunittcm,file=tcmpath(1:ichlen(tcmpath,128)),
     $     status='unknown')


c--       set search radius in deg
c

c--       print parameters of the tracker
c         

      print*,'     doGdatCon: ',doGdatCon
      print*,'       rlatmax: ',rlatmax
      print*,'     forspdmax: ',forspdmax
      print*,'       dlonmax: ',dlonmax
      print*,'      sdistmin: ',sdistmin
      print*,'      vortcrit: ',vortcrit
      print*,'vortcritadjust: ',vortcritadjust
      print*,'      rfindGen: ',rfindGen
      print*,'      rfindPsl: ',rfindPsl
      print*,'   rfindVrt850: ',rfindVrt850

c--       print trkParams
c
      print*,'       dtau: ',dtau
      print*,'      maxtc: ',maxtc
      print*,'     numvar: ',numvar
      print*,'     maxfix: ',maxfix
      print*,'      itaus: ',itaus(nt)
      print*,'       gdat: ',gdat(1,0,1,0)

c--       initialize (allocate) the fields
c
      call initFlds()

c--       set passing variables
c

      mxhr=maxhr
      mxtc=maxtc
      nbog=maxtc
      numv=numvar

c--       read bogus file data
c         
C--       blat and blon are the lat,lon of 1,1 point of grid -- 
C         pass to bogread to get initial x,y of TC (in tcyc arra)

      beglat=blat
      beglon=blon
      call bogread (tcyc,
     $     beglat,beglon,dlat,dlon,ni,nj,
     $     gdat,numv,mxhr,mxtc,maxfix,cdtg,nbog,iunittci)


      if (nbog .gt. 0) then
c
c                 there are nbog cyclones to track
c
        write (*,9010) nbog, cdtg
 9010   format (' tctrack, tracking ',i1,' tropical cyclones for ',
     &          a10)
        write (iunittcd,9020) nbog, cdtg
        write (iunittco,9020) nbog, cdtg
 9020   format (1x,i3.3,1x,a10)
        do n=1, nbog
          write (*,9030) tcyc(n)
          write (iunittco,9030) tcyc(n)
          write (iunittcd,9030) tcyc(n)
        enddo
 9030   format (1x,a24)
        write (iunittco,*) ' '

c
c         read analysis sfc wind component fields
C         produce  wind direction and wind speed fields
c

        mxtau = dtau * (mxhr -1)
        itau=0
        rtau=0.0
        ktau=itau
        ntau=1
        igo=0

        call readFlds(ntau)

c--       convert u,v to spd,dir
c
        call calddto (ddfld,fffld,ni,nj) 


c--       cycle through the taus
c
        do while (igo.eq.0)

          ktau=itau

c--       always call the sfc wind 'trackem' routine
c         
          call trackem(ddfld,fffld,
     $         ni,nj,
     $         beglat,beglon,dlat,dlon,
     $         ktau,dtau,gdat,numv,
     &         mxhr,maxtc,nbog,maxfix,ntrk,iunit,
     $         verbTrackem)


c--       then call my tracker using the new extrema routines
c--       also does consensus and makes first guess motion
c
          call mftrackem(
     $         fffld,vvfld,pslfld,
     $         rtau,ktau,
     $         nwrt,tcyc,numv,
     $         mxhr,nbog,ntrk,igo)
          
c--      call old tracker for diagnostics
c
          call mftrack(fffld,vvfld,pslfld,
     $         rtau,ktau,
     $         iunittcm,tcyc,numv,
     &         mxhr,nbog,ntrk,igo)


          itau=itau+dtau
          ntau=ntau+1

          if (itau.le.mxtau) then

c--       read forecast fields; produce direction field for sfc tracking of ntrk cyclones and wind speed field
c         
            rtau = itau
            call readFlds(ntau)
            call calddto (ddfld,fffld,ni,nj) !calculate direction of wind, towards - ddfld

          else

c--       lost track of all cyclones, or reached last tau;  stop tracking
c         
            igo=-1

          endif
        enddo   ! tau loop

c--       set index to maximum data in gdat
c
        mxfct = min0 (mxhr,1+itau/dtau)

c--       output tracking data contained in gdat, output
c         
        call outgdat(iunittco,tcyc,gdat,
     $       numv,mxhr,nbog,maxfix,mxfct,ntrk,dtau)

      else

c--       there are no cyclones to track
c

        write (iunittco,9050)
 9050   format (' NO CYCLONES TO TRACK')
        write (*,9050)

      endif


      rewind (iunittco)
      close  (iunittco)
      rewind (iunittcd)
      close (iunittcd)

      stop

 810  continue
      print*,'error opening input posit file: '
      print*,tcipath
      stop 810

 814  continue
      print*,'error in allocate... '
      stop 814

      end

