      program ngtrack
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  ngtrack
c
c  DESCRIPTION:  track tropical cyclones in NOGAPS 1000 hPa wind fields
c                and provide additional data at 850, 700 & 500 for use
c                in the Systematic Approach Expert System (SAES).
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:
c
c  PARAMETERS:  none
c
c  COMMON BLOCKS:  none
c
c  FILES:
c    NAME      UNIT  FILE TYPE  ATTRIBUTE   USAGE       DESCRIPTION
c   ---------  ----  ---------  ----------  -----   ---------------------
c  PATH/        10   permanent  sequential   in     working best track
c  PATH/        20   permanent  sequential   in     field data
c  PATH/        30   permanent  sequential   out    standard ATCF output
c  ngtrack.dbg  33   local      sequential   out    diagnostics
c  tctracks     40   local      sequential   out    1000 hPa tracking data
c  suainfo      50   local      sequential   out    surface & u/a support
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     i/o error                write diagnostic and exit
c
c  ADDITIONAL COMMENTS:
c   All tracking is performed with isogons.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         bogread     read NOGAPS tropical cyclone bogus file
c          cxytll     convert U/A locations from grid to lat/lon
c          cycsfc     obtain surface pressure at 1000 hPa cyclone location
c          dbstop     FNMOC ISIS closing routine
c         flduvrd     read NOGAPS wind fields, produce and return
c                     direction and wind-speed fields
c         lodtrkd     load data arrays for obtaining associated data
c         outgdat     write tracking data to file
c         sfcread     read surface pressure field
c         trackem     track all tropical cyclones in one forecast period
c         uatrack     locate U/A cyclone based upon 1000 hPa location
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------------
c           cdtg     char       synoptic date-time-group of initial
c                               cyclone position(s) and NOGAPS analysis
c          uufld     real       global wind direction (toward) field, deg
c          vvfld     real       global wind speed field (squared)
c           gdat     real       tropical cyclone tracking data @ 1000
c            igo      int       good/bad flag, 0 no error
c            ioe      int       i/o error flag
c          igrdx      int       first  dimension (lon) of global fields
c          issrd      int       return code from ISIS read of fields
c           itau      int       tau of forecast period being used
c           ixgd      int       first  dimension (lon) of global fields
c          jgrdy      int       second dimension (lat) of global fields
c           jygd      int       second dimension (lat) of global fields
c             j1      int       latitude  index for U/A location
c             j2      int       longitude index for U/A location
c             kf      int       running forecast hour_index
c           kont      int       array of tracking termination in hour_index
c             kt      int       maximum hour_index for U/A tracking
c           ktau      int       exported itau value
c            lev      int       level indicator in U/A
c          maxtc      int       maximum number of tropical cyclones to
c                               track - maximum allowed in bogus
c          maxhr      int       index to maximum forecast period
c                                  25 = 144 hours
c           ntrk      int       number of cyclones to track
c             nc      int       exported cyclone being processed in U/A
c           nogo      int       prcess continuation flag
c             nt      int       number of cyclones to track in U/A
c           itrk      int       number of cyclones being tracked
c         numvar      int       number of variables carried in output
c                               array gdat - first dimension of gdat
c           nout      int       unit number of output file tctracks
c           rtau      int       real version of itau
c         suadat     real       surface and U/A data for QC program
c           tcdat    real       grid coordinates of tropical cyclones @ 1000
c           tcyc     char       tropical cyclone data from bogus file
c
c  METHOD:
c    1.  Use past heading and speed of cylone to estimate expected
c        position.
c    2.  Use wind direction field to locate approximate location of
c        cyclonic circulations within window covering last known
c        position and the estimated position.
c    3.  If more than one circulation found within window, select the
c        best location for cyclone being tracked.
c    4.  Use isogons to locate the exact center of circulation.
c    5.  Track every six hours till ciculation lost, no more fields or
c        144 hours.
c    6.  Output latitude, longitude, heading, speed of movement,
c        confidence of location factor, wind support factor and
c        isogon intersection support factor for each tracked position
c        at the 1000 hPa level.
c    7.  Process surface pressure fields to obtain centrap pressure of cyclone
c        at the wind center point.
c    8.  Attempt to locate the cyclone with isogons at the 850, 700
c        levels based upon the 1000 hPa location for each time-period.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
c    Initial installation on OASIS
c
c  <<CHANGE NOTICE>>  Version 1.2  (14 MAY 1997) -- Hamilton, H.
c    Add surface pressure and U/A (850, 700
c    in the Systematic Approach Expert System (SAES) by JTWC.
c
c   Modified to run on ATCF 3.0  - Sampson Aug 97
c
c   Modified to use new data format,  6/98   A. Schrader
c   Modified to use bt posit century "cent", 11/98     Sampson 
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      integer igrdx, jgrdy, maxtc, numvar, maxhr
cx    parameter  (igrdx = 144, jgrdy = 73, maxtc = 9, numvar = 9)
      parameter  (igrdx = 360, jgrdy = 181, maxtc = 9, numvar = 9)
      parameter  (maxhr = 25)
c
      integer  numv, mxhr, mxfct, mxtc, ixgd, jygd, n, mxtau
      integer  ntrk, igo, ioe, itrk, itau, ktau, nogo
      integer  lev, kt, nt, kf, nc, j, k, l, issrd, ierr, j1, j2
      integer  lbp, ioer, nerr
      integer  kont(maxtc)
      integer  nuwbt, nufld, nuout, nutrk, nudbg, nusua
      integer  ibtwind, ios, iarg
c
      character*1   cdummy
      character*3   cyc_id, cycid(maxtc)
      character*6   strmid
      character*2   century
      character*2   cent
      character*8   cfdtg, cpdtg, crdtg
      character*8   tdtg
      character*8   btdtg
      character*24  tcyc(maxtc+1)
      character*100 storms
      character*132 filename
      character*1   btns, btew
c
      real  rlat, rlon
      real  uufld(igrdx,jgrdy), vvfld(igrdx,jgrdy)
      real  gdat(numvar,0:maxhr,maxtc)
      real  suadat(7,maxhr,maxtc)
      real  tcdat(2,maxhr,maxtc)
      real  btlat, btlon
c
      data nuwbt/10/, nufld/20/, nuout/30/, nutrk/40/, nusua/50/
      data nudbg/33/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c
c  write heading on output
c
      print *,'********************************************************'
      print *,' '
      print *,'          initial ngpr initial forecast for ',strmid
      print *,' '

      nogo = 0
      ntrk = 0
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
c                              get cyclone to forecast (WP0497)
      call getarg (iarg,strmid)
      iarg = iarg + 1
      call locase (strmid,6)
c
c                              get the first two digits of the year
c
      call getarg(iarg,century)
      iarg = iarg + 1
c                              get path to cyclone data
      call getenv ("ATCFSTRMS",storms)
c                              get length of base path to cyclone data
      lbp = index (storms," ") -1
c
c                   all filenames must be lower case,
c                   set the filenames and open the output and data files
c
c                   open standard ATCF output file
c
      filename = ' '
      filename = storms(1:lbp) // "/wptot.dat"
      open (nuout,file=filename,status='unknown',iostat=ioer)
      if (ioer .eq. 0) then
        rewind (nuout)
c
c                   go to the end of the output file
c
   20   continue
        read (nuout,'(a1)',end=25) cdummy
        goto 20
c
   25   continue
      else
	write (*,*) 'ngtrack, OPEN ERROR is ',ioer,' ',filename
        nogo = -1
	goto 399
c
      endif
c
      filename = storms(1:lbp) // "/" // strmid // ".tctracks"
      open (nutrk,file=filename,status='unknown',iostat=ioer)
      if (ioer .eq. 0) then
c
c                   open working best track file for requested cyclone
c
        filename = ' '
cajs    filename = storms(1:lbp) // "/b" // strmid // ".dat"
        write(filename,'(a,a,a,a,a,a)') storms(1:lbp), "/b", 
     1       strmid(1:4), century, strmid(5:6), ".dat"
        open (nuwbt,file=filename,status='old',iostat=ioer)
      else
	write (*,*) 'OPEN ERROR is ',ioer,' for file tctracks'
        nogo = -1
      endif
      if (ioer .eq. 0) then
        rewind (nuwbt)
c
c                   convert the 1st two characters of stormid to uppercase
c
        call upcase (strmid,6)
        cyc_id(1:2) = strmid(3:4)
        cyc_id(3:3) = strmid(1:1)
        if (cyc_id(3:3) .eq. 'I') cyc_id(3:3) = 'A'
c
c                   find the last dtg in the working best track file
c
caj30   continue
cajs    read (nuwbt,'(2x,a8)',end=35) tdtg
cajs    if (tdtg.ne.'        ') cpdtg=tdtg
cajs    goto 30
        ios = 0
        do while ( ios .eq. 0 )
           call readBT(nuwbt,cent,tdtg,btlat,btns,btlon,btew,ibtwind, 
     1          ios)
           if (tdtg.ne.'        ') cpdtg=tdtg
        enddo
c
   35   continue
	write(*,*) '35 cpdtg ',cpdtg
        rewind (nuwbt)
c
c                   obtain other parameters and initial conditions
c
        numv = numvar
        mxhr = maxhr
        mxtc = maxtc
        call wbtdat (nuwbt,cpdtg,cyc_id,ntrk,tcyc,gdat,numv,mxhr,
     &               mxtc,cfdtg,nerr)
        close (nuwbt)
	write(*,*) 'Back cpdtg ',cpdtg
	if (nerr .eq. 0 .and. ntrk .gt. 0) cycid(ntrk) = cyc_id
c
c                   right now only one cyclone is tracked at a time
c
	write (*,*) 'ntrk=',ntrk
        if (ntrk .gt. 0) then
c
c                   open diagnostic file
c
          open (nudbg,file='ngtrack.dbg',form='formatted',iostat=ioe)
          if (ioe .ne. 0) then
            write (*,*) 'OPEN diagnostic file error is ',ioe
            nogo = -77
          endif
        elseif (ntrk .eq. 0) then
          write (*,*) 'NO cyclones to track'
          nogo = -99
        endif
      else
	write (*,*) 'ngtrack, OPEN ERROR is ',ioer,' ',filename
	nogo = -77
      endif
      write(*,*) 'NOGO is ',nogo
      if (nogo .lt. 0) goto 399
c
c                   open file which has all the global fields
c
cx changed            (1.0 degree 360 by 181 - pt1 South pole, 0 Longitude)
cx changed         first  dimension (360) are longitude points with fixed lat
cx changed         second dimension (181) goes from South pole to North Pole
cx old                (2.5 degree 144 by 73 - pt1 South pole, 0 Longitude)
cx old       first  dimension (144) are longitude points with fixed lat
cx old       second dimension (73) goes from South pole to North Pole
c
      write(*,*) 'READing ',cpdtg
      filename = ' '
      filename = storms(1:lbp) // "/ngpl." // cpdtg
      open (nufld,file=filename,status='old',form='unformatted',
     &        access='sequential',err=744,iostat=ioe)
      if (ioe .eq. 0) read (nufld,err=745,iostat=ioe) crdtg
      if (ioe .eq. 0) then
        if (crdtg .ne. cfdtg) then
          write (*,*) 'NGPL FIELDS are for ',crdtg,' NEED ',cfdtg
          nogo = -77
        endif
      else
	write (*,*) 'BAD INITIAL READ dtg of fields, error ',ioe
	nogo = -77
      endif
      write(*,*) 'nogo=',nogo
      if (nogo .ne. 0) goto 399
c
c                   set passing variables
c
      ixgd = igrdx
      jygd = jgrdy
c
c                 there are ntrk cyclones to track
c
      write (*,9010) ntrk, cfdtg
 9010 format (' tctrack, tracking ',i1,' tropical cyclones from ',a8)
      write (nudbg,9020) ntrk, cfdtg
      write (nutrk,9020) ntrk, cfdtg
      do n=1, ntrk
        write (*,9030) tcyc(n)
        write (nutrk,9030) tcyc(n)
        write (nudbg,9030) tcyc(n)
      enddo
 9030 format (1x,a24)
      write (nutrk,*)
c
c               read 1000 hPa wind component fields
c
      mxtau = 12*(mxhr -1)
      itau  = 0
      lev   = 1
      write (*,*) 'READ FIRST FIELDS'
      call flduvrd (nufld,ixgd,jygd,uufld,vvfld,igo)
      if (igo .eq. 0) then
c
c               read and production OK
c
        do k=1, mxhr
          ktau = itau
          call trackem (uufld,vvfld,ixgd,jygd,ktau,gdat,numv,mxhr,
     &                  ntrk,itrk)
          write(nudbg,*) ' trackem tracked ',itrk,' for tau ',itau
          itau = itau +12
          if (itrk.gt.0 .and. itau.le.mxtau) then
c
c                read forecast wind fields and produce direction
c                field for tracking of ntrk cyclones and wind speed
c                field to assist in selection process, as required
c
	    write (*,*) 'READ next field....'
            call flduvrd (nufld,ixgd,jygd,uufld,vvfld,igo)
	    if (igo .ne. 0) then
	      write (nudbg,*) 'READ I/O error, ktau= ',ktau
	      goto 199
c
	    endif
          else
c
c                lost track of all cyclones, or reached 144 hours
c                stop tracking
c
           goto 199 
c
          endif
        enddo
  199   continue
c
c         set index to maximum data in gdat
c
        mxfct = min (mxhr, 1 +itau/12)
	write (*,*) 'mxfct= ',mxfct
c
c         output tracking data contained in gdat and
c         load arrays for gathering additional data
c
        call outgdat (nutrk,tcyc,gdat,numv,mxhr,ntrk,mxfct,itrk)
c
c          *****  OBTAIN SURFACE AND U/A DATA  *****
c
        write (*,*) 'Start processing additional data'
c
        filename = ' '
        filename = storms(1:lbp) // "/ngpu." // cpdtg
        open (nusua,file=filename,status='old',form='unformatted',
     &        access='sequential',err=744,iostat=ioe)
        read (nusua,err=745,iostat=ioe) crdtg
        if (crdtg .ne. cfdtg) then
          write (*,*) 'NGPU FIELDS are for ',crdtg,' NEED ',cfdtg
          goto 399
c
        endif
        call lodtrkd (numv,mxhr,ntrk,tcyc,gdat,tcdat,kont,cycid,ierr)
        if (ierr .eq. 0) then
          kt = 0
          do n=1, ntrk
            kt = max (kt,kont(n))
          enddo
          write (*,*) 'ngtrack, max tau for su/a data is ',12*(kt-1)
c
          suadat = 0.0
          nt     = ntrk
          do k=1, kt
            kf   = k
            itau = 12*(k -1)
            call sfcread (nusua,ixgd,jygd,uufld,issrd)
            if (issrd .ne. 0) then
              write (*,*) 'BAIL at tau ',itau
              nogo = -1
              exit
c
            endif
            write (*,*) 'HAVE SFC for tau ',itau
            do n=1, nt
              if (kont(n) .ge. k) then
c
c               obtain surface pressure for 1000 hPa cyclone location
c
                nc = n
                call cycsfc (tcdat,mxhr,ntrk,kf,nc,ixgd,jygd,uufld,
     &                       suadat)
              endif
            enddo
            do l=2, 4
              call flduvrd (nusua,ixgd,jygd,uufld,vvfld,igo)
              if (igo .eq. 0) then
		lev = l
                do n=1, nt
                  if (kont(n) .ge. k) then
c
c                     locate cyclone, if possible, near 1000 hPa position
c
                    nc = n
                    call uatrack (mxhr,ntrk,tcdat,ixgd,jygd,uufld,
     &                            vvfld,lev,kf,nc,suadat)
                  endif
                enddo
              else
                nogo = -1
                write (*,*) 'MISSING U/A for tau ',itau
                exit
c
              endif
            enddo
            write (*,*) 'ngtrack, finished su/a data for tau ',itau
          enddo
	  close (nusua)
        else
          write (*,*) 'INTERNAL PROBLEM WITH GDAT FILE'
          write (nudbg,*) ' INTERNAL PROBLEM WITH GDAT FILE'
          goto 399
c
        endif
c
c                ******  OUTPUT ADDITIONAL DATA  ******
c
        do n=1, nt
          write (*,*) 'additional data for cyclone ',cycid(n)
          do k=1, kont(n)
	    ktau = (k -1)*12
            do l=2, 6, 2
              j1 = l
              j2 = l +1
              if (suadat(l,k,n) .gt. 0.0) then
                call cxytll (suadat(j1,k,n),suadat(j2,k,n),rlat,rlon,
     &                       ierr)
                if (ierr .eq. 0) then
                  suadat(j1,k,n) = rlat
                  suadat(j2,k,n) = rlon
                else
		  write(*,*)'ierr=',ierr,' l=',l,' k=',k
                  suadat(j1,k,n) = 0.0
                  suadat(j2,k,n) = 0.0
                endif
              else
                suadat(j1,k,n) = 0.0
                suadat(j2,k,n) = 0.0
              endif
            enddo
            write (*,'(i4,2x,f6.1,2x,3(f5.1,1x,f5.1,3x))')
     &            ktau, (suadat(j,k,n),j=1,7)
          enddo
          write (*,*)
        enddo
        call locase (strmid,6)
        filename = storms(1:lbp) // "/" // strmid // ".suainfo"
        open (nusua,file=filename,iostat=ioe,access='sequential',
     &    form='unformatted',status='unknown')
        if (ioe .eq. 0) then
          write  (nusua) cycid
          write  (nusua) suadat
          rewind (nusua)
          close  (nusua)
c
          write (*,*) 'SURFACE & U/A data written for QC program'
          write (nutrk,*) 'SURFACE & U/A data written for QC program'
          write (nudbg,*) 'SURFACE & U/A data written for QC program'
	  nogo = 0
        else
          write (*,*) 'CANT OPEN suainfo file, no additional data'
          write (nutrk,*) 'CANT OPEN suainfo file, no additional data'
          write (nudbg,*) 'CANT OPEN suainfo file, no additional data'
        endif
      else
        write (*,9040)
        write (nutrk,9040)
        write (nudbg,9040)
 9040   format (' ngtrack FAILED, NO INITIAL FIELDS')
      endif
  399 continue
      if (nogo .ne. 0) then
c
c                   no cyclones were tracked
c
        write (nutrk,9020) ntrk, cpdtg
 9020   format (1x,i3.3,1x,a10)
        write (nutrk,9050)
 9050   format (' NO CYCLONES TO/WERE TRACKED')
        write (*,9020) ntrk, cpdtg
        write (*,9050)
      endif
      rewind (nutrk)
      close  (nutrk)
      rewind (nudbg)
      close  (nudbg)
      stop
c
  744 continue
      write (*,*) 'ngtrack, OPEN ERROR ',ioe,' file ',filename
      nogo = -77
      goto 399
c
  745 continue
      write (*,*) 'ngtrack, READ ERROR ',ioe,' file ',filename
      nogo = -77
      goto 399
c
      end
      real function avgddt (dd1,dd2,f1)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  avgddt
c
c  DESCRIPTION:  calculate weighted average wind direction
c
c  COPYRIGHT:                  (C) 1996 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  avgdd = avgddt (dd1,dd2,f1)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     dd1          real          in     wind direction at point 1, deg
c     dd2          real          in     wind direction at point 2, deg
c      f1          real          in     fraction of grid length from pt1
c                                       to "center-line", which is
c                                       between pt 1 and pt 2
c  avgddt          real         out     weighted average wind direction
c                                       on "center-line", degrees
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          dds       real       copy of dd1 or dd2
c          ddl       real       copy of dd2 or dd1
c           fs       real       fractional part of grid length
c           fl       real       fractional part of grid length
c
c  METHOD:  simple weighted average
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 77
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real dd1, dd2, f1
c
c         local variables
      real dds, ddl, fl, fs
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (dd1 .ne. dd2) then
        if (dd1 .lt. dd2) then
          dds = dd1
          ddl = dd2
           fl = f1
           fs = 1.0 -f1
        else
          dds = dd2
          ddl = dd1
          fs  = f1
          fl  = 1.0 -f1
        endif
        if (ddl -dds .gt. 180.0) dds = dds +360.0
        avgddt = amod ((fs*dds +fl*ddl), 360.0)
      else
        avgddt = dd1
      endif
      if (avgddt .eq. 0.0) avgddt = 360.0
c
      end
      subroutine calcntr (nc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calcntr
c
c  DESCRIPTION:  calculate centroid of intersections
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calcntr (nc)
c
c  PARAMETERS:
c     NAME        TYPE      USAGE             DESCRIPTION
c   --------     ------     ------   ------------------------------
c      nc         int         in     index to systems
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c      /BOX/      lbox      int      in     unit number for diagnostics
c                   xs     real      in     starting first dimension of
c                                           isogon box
c                   xl     real      in     ending first dimension of
c                                           isogon box
c                   ys     real      in     starting second dimension of
c                                           isogon box
c                   yl     real      in     ending second dimension of
c                                           isogon box
c                  nip      int      in     count of intersection points
c                   cx     real      in     array of first dimension
c                                           intersection points
c                   cy     real      in     array of second dimension
c                                           intersection points
c                  rxc     real      in     running average of first
c                                           dimension intersection point
c                  ryc     real      in     running average of second
c                                           dimension intersection point
c                  rxc     real     out     first dimension of cyclone
c                                           location
c                  ryc     real     out     second dimension of cyclone
c                                           location
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           diff     real       maximum x or y difference from estimated
c                               centroid
c             dr     real       radial distance from centroid
c         epslon     real       small number
c              k      int       number of iterations
c             rr     real       radial distance from centroid
c             sx     real       sum of x-coord of centroid
c             sy     real       sum of y-coord of centroid
c            ttt     real       temporary variable
c
c  METHOD:  calculate centroid based upon intersections closest to the
c           running centroid position, for index nc.
c           note: nip(nc) must be 3 or greater before calling calcntr
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          -----------    ---------------------------------------
c           box.inc       common block
c
c  COMPILER DEPENDENCIES:  Cray UNICOS
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameter
      integer nc
c
c         local variables
      integer k,m,n
      real diff,rxl,ryl,dx,dy,dr,rr,ttt,sx,sy,epslon
c
      INCLUDE 'box.inc'
c
      data epslon/1.0e-03/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (33,*) ' calcntr, running avg xc ',rxc(nc),' yc ',ryc(nc),
     &             ' with ',nip(nc),' intersections'
c
      k    = 0
      diff = 99.9
      do while (nip(nc) .gt. 2 .and. diff .gt. epslon)
        rxl = rxc(nc)
        ryl = ryc(nc)
c
c                   sort on difference from last estimate of location,
c                   least to most
c
        do m=1, nip(nc) -1
          dx = rxl -cx(nc,m)
          dy = ryl -cy(nc,m)
          dr = dx*dx +dy*dy
          do n=m+1, nip(nc)
            dx = rxl -cx(nc,n)
            dy = ryl -cy(nc,n)
            rr = dx*dx +dy*dy
            if (rr .lt. dr) then
              ttt      = cx(nc,n)
              cx(nc,n) = cx(nc,m)
              cx(nc,m) = ttt
              ttt      = cy(nc,n)
              cy(nc,n) = cy(nc,m)
              cy(nc,m) = ttt
              dr       = rr
            endif
          enddo
        enddo
c
c                   calculate new estimate, w/o worst case
c
        sx = 0.0
        sy = 0.0
        nip(nc) = nip(nc) -1
        do n=1, nip(nc)
          sx = sx +cx(nc,n)
          sy = sy +cy(nc,n)
        enddo
        rxc(nc) = sx/nip(nc)
        ryc(nc) = sy/nip(nc)
        k = k +1
        diff = amax1 (abs (rxl -rxc(nc)), abs (ryl -ryc(nc)))
      enddo
      write (33,*) ' calcntr, with ',k,' iterations: x= ',rxc(nc),
     &             ' y= ',ryc(nc),' with ',nip(nc),' intersections'
c
      end
      subroutine calddto (igrdx,jgrdy,ddfld,fffld)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calddto
c
c  DESCRIPTION:  calculate wind direction, towards, with u,v components
c                and wind speed
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calddto (ddfld,fffld,igrdx,jgrdy)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c    ddfld         real        in/out   u-component array, m/s
c                                       wind direction, deg (towards)
c    fffld         real         in      v-component array, m/s
c    igrdx          int         in      first  dimension of fields
c    jgrdy          int         in      second dimension of fields
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           ddto     real       grid point wind direction
c          epsln     real       small number
c           inil      int       flag for initial calculation
c            rtd     real       radian-to-degree conversion factor
c             uu     real       u-wnd at grid point
c             vv     real       v-wnd at grid point
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer igrdx, jgrdy
      real ddfld(igrdx*jgrdy,1), fffld(igrdx*jgrdy,1)
c
c         local variables
      integer inil, n
      real epsln, rtd, uu, vv, ddto
c
      save inil, rtd
c
      data epsln/0.0001/
      data inil/0/, rtd/57.2958279/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .eq. 0) then
        inil = -1
        rtd  = 180.0/acos (-1.0)
      endif
      do n=1, igrdx*jgrdy
        uu = ddfld(n,1)
        vv = fffld(n,1)
c                   note: wind speed is squared
        fffld(n,1) = uu*uu +vv*vv
        if (abs (uu) .lt. epsln) uu = 0.0
        if (abs (vv) .lt. epsln) vv = 0.0
        if (uu.ne.0.0 .or. vv.ne.0.0) then
          ddto = amod (450.0 -rtd*atan2 (vv,uu),360.0)
          if (ddto .lt. 0.0) ddto = 360.0 +ddto
          if (ddto .eq. 0.0) ddto = 360.0
        else
          ddto = 360.0
        endif
        ddfld(n,1) = ddto
      enddo
      return
c
      end
      subroutine calint
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  calint
c
c  DESCRIPTION:  calculate point(s) of intersection of two isogons
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call calint
c
c  PARAMETERS:  none
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c      box       cx        real     out     new x-intercept
c      box       cy        real     out     new y-intercept
c      box       lbox       int      in     diagnostic unit number
c      box       nip        int    in/out   count of intersections
c      box       rxc       real    in/out   running x-intercept
c      box       ryc       real    in/out   running y-intercept
c      box       xs        real      in     x-start of isogon box
c      box       xl        real      in     x-end of isogon box
c      box       ys        real      in     y-start of isogon box
c      box       yl        real      in     y-end of isogon box
c
c      isoxy     xx1       real      in     x-values of rh1
c      isoxy     yy1       real      in     y-values of rh1
c      isoxy     xx2       real      in     x-values of rh2
c      isoxy     yy2       real      in     y-values of rh2
c      isoxy     nxy1       int      in     number of rh1 points
c      isoxy     nxy2       int      in     number of rh2 points
c      isoxy     rh1       real      in     value of first  isogon
c      isoxy     rh2       real      in     value of second isogon
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c    1.  The old method of locating the system assumed that only a
c        cyclone or col would be located within each box.  However,
c        testing found that both the col and the cyclone may be found
c        within the box.  Since the old method allowed only one system
c        per box, if the col were found rather than the cyclone the
c        tracking would stop.  90+% of the time, the cyclone was found
c        rather than the col, so this oversite went undetected.
c    2.  During testing so far, the maximum number of systems found has
c        been 2, one col and one center; however this new design
c        accommodates up to 4 systems per box.
c    3.  Likewise, 10 segments is more than twice the number of segments
c        found thus far during testing.
c    4.  The method of finding the "second" point has also been revised
c        and improved.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c      name              description
c   ------------       --------------------------------------------
c     evaliso          evaluate possible intersection(s)
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c            a1      real       y-coefficient of rh1
c            a2      real       y-coefficient of rh2
c            b1      real       x-coefficient of rh1
c            b2      real       x-coefficient of rh2
c            c1      real       constant of rh1
c            c2      real       constant of rh2
c           cxl      real       array of last x-locations of cx
c           cyl      real       array of last y-locations of cy
c            dd      real       value of determinant
c            d1      real       value of determinant
c            d2      real       value of determinant
c           dx1      real       delta-x of rh1 near intersection
c           dx2      real       delta-x of rh2 near intersection
c           dy1      real       delta-y of rh1 near intersection
c           dy2      real       delta-y of rh2 near intersection
c          dydx      real       slope of rh1 or rh2 near intersection
c           jdd       int       direction of first isogon
c          jj11       int       primary index of rh1
c          jj12       int       secondary index of rh1
c          jj21       int       primary index of rh2
c          jj22       int       secondary index of rh2
c           kdd       int       direction of second isogon
c         maxpc       int       maximum number of prospective
c                               circulations for S/R evaliso
c           ms1       int       starting segmnet index, rh1
c           me1       int       ending segment index, rh1
c            nn       int       running index to system
c            np       int       index to prospective segments
c           npc       int       max allowed prospective systems (out)/
c                               number of prospective systems (in)
c           n1s       int       starting index to rh1 segment
c           n1e       int       ending index to rh1 segment
c           n2s       int       starting index to rh2 segment
c           n2e       int       ending index to rh2 segment
c           ns2       int       starting segment index, rh2
c           ne2       int       ending segment index, rh2
c             r      real       working distance between rh1
c          rmin      real       working minimum distance
c           rmm      real       distance between rh1
c           rmp      real       distance between rh1
c           rpm      real       distance between rh1
c           rpp      real       distance between rh1
c            x1      real       working x-point of rh1
c            xd      real       working x-distance between rh1
c         xx1mn      real       minimum x-distance of rh1 near
c                               intersection
c         xx2mn      real       minimum x-distance of rh2 near
c                               intersection
c            y1      real       working y-point of rh1
c            yd      real       working y-distance between rh1
c
c  METHOD:  1.  Call evaliso to establish the starting and ending
c               indecies to rh1 and rh2 of segments that may contain
c               intersections
c           2.  Evaluate each segment for an intersecion within the
c               regional area defined by the indicies
c           3.  For each intersection found, allowcate the intersection
c               to a system based upon the juxtaposition of the running
c               average location of the previously identified systems.
c               If none are found, start a new system.
c           4.  Maintain the count of intersections supporting each
c               system and the running average location of each system.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          -----------    ---------------------------------------
c           box.inc       common block
c           isoyx.inc     common block
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      integer maxpc
      parameter (maxpc = 10)
c
      integer jdd,jj11,jj12,jj21,jj22,j901,j902,j1801,j1802,kdd
      integer j1,j2,np,npc,n1s,n1e,n2s,n2e,nn
      integer ms1(maxpc), me1(maxpc), ns2(maxpc), ne2(maxpc)
c
      real a1,a2,b1,b2,c1,c2,c11,c12,c21,c22,dd,d1,d2,dx1,dx2,dy1,dy2
      real dydx,xc,x1,xd,xx1mn,xx2mn,yc,y1,yd,xxs,xxl,yys,yyl
      real r,rmin,rmm,rpm,rpp,rmp,cxl(4),cyl(4)
      real difx,dify,epsln
c
      INCLUDE 'box.inc'
      INCLUDE 'isoxy.inc'
c
      data epsln/0.1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (lbox,*) ' calint, nxy1 ',nxy1,' rh1 ',rh1,' nxy2 ',nxy2,
     &               ' rh2 ',rh2
c
      jdd = anint (rh1)
      kdd = anint (rh2)
      if (kdd -jdd .eq. 90) then
c
c                   isogons are for directions 90 degrees apart
c
c
c                      evaluate prospects for intersection(s)
c
        npc = maxpc
        call evaliso (nxy1,xx1,yy1, nxy2,xx2,yy2, ms1,me1,ns2,ne2,npc)
        if (npc .gt. 0) then
c
c                   set the last intersection points, for this call to
c                   the S/R, to zero
c
          do nn=1, 4
            cxl(nn) = 0.0
            cyl(nn) = 0.0
          enddo
c
          do np=1, npc
c
c                   extract prospective starting and ending points for
c                   rh1 and rh2 isogons
c
            n1s = ms1(np)
            n1e = me1(np)
            n2s = ns2(np)
            n2e = ne2(np)
c
            rmin = 99999.0
            jj11 = 0
            jj21 = 0
c
c                   locate the indicies to the nearest points of rh1
c                   and rh2 within the two segments defined above
c
            do j1=n1s, n1e
              x1 = xx1(j1)
              y1 = yy1(j1)
              do j2=n2s, n2e
                xd = x1 -xx2(j2)
                yd = y1 -yy2(j2)
                r  = xd*xd +yd*yd
                if (r .lt. rmin) then
c
c                        save the indicies
c
                  rmin = r
                  jj11 = j1
                  jj21 = j2
                endif
              enddo
            enddo
c
c                   the nearest point may not be the first or last point
c                   of the segments - if it is, there is not an
c                   intersection because of the way evaliso establishes
c                   these points
c
            if (jj11 .eq. nxy1) jj11 = -1
            if (jj21 .eq. nxy2) jj21 = -1
            if (jj11 .gt. 1 .and. jj21 .gt. 1) then
c
c                   find "second" point for rh1 and rh2
c                   by finding the next nearest point
c
              xd  = xx1(jj11-1) -xx2(jj21-1)
              yd  = yy1(jj11-1) -yy2(jj21-1)
              rmm = xd*xd +yd*yd
              xd  = xx1(jj11-1) -xx2(jj21+1)
              yd  = yy1(jj11-1) -yy2(jj21+1)
              rmp = xd*xd +yd*yd
              xd  = xx1(jj11+1) -xx2(jj21+1)
              yd  = yy1(jj11+1) -yy2(jj21+1)
              rpp = xd*xd +yd*yd
              xd  = xx1(jj11+1) -xx2(jj21-1)
              yd  = yy1(jj11+1) -yy2(jj21-1)
              rpm = xd*xd +yd*yd
              r   = amin1 (rmm,rmp,rpp,rpm)
              if (r .eq. rmm) then
                jj12 = jj11 -1
                jj22 = jj21 -1
              elseif (r .eq. rmp) then
                jj12 = jj11 -1
                jj22 = jj21 +1
              elseif (r .eq. rpp) then
                jj12 = jj11 +1
                jj22 = jj21 +1
              else
                jj12 = jj11 +1
                jj22 = jj21 -1
              endif
c
c                   assume isogons are straight lines at intersection,
c                   so calculate the a, b, c of equation ay +bx = c
c
c                     calculate for rh1
c
              xx1mn = amin1 (xx1(jj11),xx1(jj12))
              if (xx1mn .eq. xx1(jj11)) then
                j901 = jj11
                j902 = jj12
              else
                j901 = jj12
                j902 = jj11
              endif
              dx1 = xx1(j902) -xx1(j901)
              if (dx1 .ne. 0.0) then
                a1   = dx1
                dy1  = yy1(j902) -yy1(j901)
                b1   = -dy1
                dydx = dy1/dx1
                c11  = yy1(j901) -dydx*xx1(j901)
                c12  = yy1(j902) -dydx*xx1(j902)
                c1   = dx1*(0.5*(c11 +c12))
              else
                a1 = 1.0
                b1 = 0.0
                c1 = xx1(j901)
              endif
c
c                     calculate for rh2
c
              xx2mn = amin1 (xx2(jj21),xx2(jj22))
              if (xx2mn .eq. xx2(jj21)) then
                j1801 = jj21
                j1802 = jj22
              else
                j1801 = jj22
                j1802 = jj21
              endif
              dx2 = xx2(j1802) -xx2(j1801)
              if (dx2 .ne. 0.0) then
                a2   = dx2
                dy2  = yy2(j1802) -yy2(j1801)
                b2   = -dy2
                dydx = dy2/dx2
                c21  = yy2(j1801) -dydx*xx2(j1801)
                c22  = yy2(j1802) -dydx*xx2(j1802)
                c2   = dx2*(0.5*(c21 +c22))
              else
                a2 = 1.0
                b2 = 0.0
                c2 = xx2(j1801)
              endif
c
c                     check that lines intercept
c
              dd = a1*b2 -(b1*a2)
              if (dd .ne. 0.0) then
c
c                       calculate new intercept
c
                d1 = c1*b2 -(b1*c2)
                d2 = a1*c2 -(c1*a2)
                yc  = d1/dd
                xc  = d2/dd
c
c                        establish bounds of regional area
c
                xxs = amin1 (xx1(n1s),xx1(n1e),xx2(n2s),xx2(n2e))
                xxl = amax1 (xx1(n1s),xx1(n1e),xx2(n2s),xx2(n2e))
                yys = amin1 (yy1(n1s),yy1(n1e),yy2(n2s),yy2(n2e))
                yyl = amax1 (yy1(n1s),yy1(n1e),yy2(n2s),yy2(n2e))
c
                if (xc .ge. xxs .and. xc .le. xxl .and. yc .ge. yys
     &             .and. yc .le. yyl) then
c
c                          intercept is within regional area
c
                  if (nsys .eq. 0) then
c
c                          start first system for this box
c
                    nsys    = 1
                    nn      = 1
                    rxc(1)  = xc
                    ryc(1)  = yc
                    nip(1)  = 1
                    cx(1,1) = xc
                    cxl(1)  = xc
                    cy(1,1) = yc
                    cyl(1)  = yc
                  else
c
c                         load intersection in proper system
c
                    do nn=1, nsys
c
c                           ensure same position is not loaded again
c
                      difx = abs (cxl(nn) -xc)
                      dify = abs (cyl(nn) -yc)
                      if (difx .le. epsln .and. dify .le. epsln)
     &                    goto 220
c
                      difx = abs (rxc(nn) -xc)
                      dify = abs (ryc(nn) -yc)
                      if (difx .le. epsln .and. dify .le. epsln)
     &                    goto 210                                                              XXXXX
c
                    enddo
c
c                      start new system
c
                    nn = nsys +1
                    if (nn .gt. 4) then
                      write (*,*) ' $ $ calint, error more than 4 cc'
                      write (33,*) '$ $ calint, ERROR more than 4 cc'
                      goto 900
c
                    endif
 210               continue
                    if (nip(nn) .eq. nint) then
                      write (*,*) ' $ $ calint, error in allocations'
                      write (33,*) '$ $ calint, ERROR in allocations'
                      goto 220
c
                    endif
                    nip(nn) = nip(nn) +1
                    if (nip(nn) .gt. 1) then
c
c                           calculate running average location
c
                      rxc(nn) = (rxc(nn)*(nip(nn) -1) +xc)/nip(nn)
                      ryc(nn) = (ryc(nn)*(nip(nn) -1) +yc)/nip(nn)
                      cx(nn,nip(nn)) = xc
                      cy(nn,nip(nn)) = yc
                    else
c
c                           load inital position
c
                      rxc(nn) = xc
                      ryc(nn) = yc
                      cx(nn,nip(nn)) = xc
                      cy(nn,nip(nn)) = yc
                      nsys = nn
                    endif
c
c                             load last position to check for duplicates
c
                    cxl(nn) = xc
                    cyl(nn) = yc
                  endif
                  write (lbox,*) 'calint, ',nn,' ',nip(nn),
     &              ' intersection at ',xc,' ',yc,' for ',rh1,' ',rh2
                else
                  write (lbox,*) ' calint, intersection outside of',
     &                           ' local region'
                endif
              else
                write (lbox,*) ' calint, no intercept'
              endif
            else
              write (lbox,*) ' calint, no calculations'
            endif
 220       continue
          enddo
        else
          write (lbox,*) 'calint, NO PROSPECTIVE intersections'
        endif
      else
        write (lbox,9010) rh1, rh2
        write (33,9010) rh1, rh2
 9010   format (' rh"s not 90 degreees for ',f7.2,' ',f7.2)
      endif
 900  continue
      do nn=1, nsys
        write (33,*) 'CALINT, system ',nn,' intersections ',nip(nn)
      enddo
c
      end
      subroutine chkcir (dfld,igx,jgy,nc,isotyp)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  chkcir
c
c  DESCRIPTION:  determine type of circulation
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call chkcir (dfld,igx,jgy,nc,isotyp)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     dfld         real         in      wind direction (to) array
c      igx          int         in      first  dimension of dfld
c      jgy          int         in      second dimension of dfld
c       nc          int         in      index to intersection
c   isotyp         real         out     type of circulation found
c                                         4 - ccw flow 4 out of 4
c                                         3 - ccw flow 3 out of 4
c                                         0 - col or no evaluation
c                                        -4 - cw flow 4 out of 4
c                                        -3 - cw flow 3 out of 4
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c       box       rxc      real      in     x-location of intersection
c       box       ryc      real      in     y-location of intersection
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c    Name          Description
c   --------       -----------------------------------------------------
c   avgddt         calculate weighted average wind
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dde        real       wind direction at East-point
c         ddn        real       wind direction at North-point
c         dds        real       wind direction at South-point
c         ddw        real       wind direction at West-point
c         fi         real       fractional i grid-length to "center line"
c         fj         real       fractional j grid-length to "center line"
c         ichk        int       sum of winds within window
c         ixce        int       eastern-edge index
c         jycn        int       northern-edge index
c         jycs        int       southern-edge index
c         ixcw        int       western-edge index
c
c  METHOD:  1.  Check wind direction at cardinal points about
c               intersection.
c           2.  If 3 or 4 agree with cw or ccw flow
c               assign isotyp +sum for ccw and -sum for cw flow.
c           3.  Else, assign isotyp a 0 for a col.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------    ---------------------------------------
c           box.inc        common block
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (17 JUN 1996) -- Hamilton, H.
c    Initial installation on OASIS
c
c  <<CHANGE NOTICE>>  Version 1.2  (09 APR 1997) -- Hamilton, H.
c    Modify how representative winds are selected
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer igx, jgy, nc, isotyp
      real dfld(igx,jgy)
c
c         local variables
      integer ixcw, ixce, jycs, jycn, ichk
      real fi, fj, ddn,dds,dde,ddw, avgddt
c
      include 'box.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   obtain north, south, west and east indicies
c                   about isogon intersection
c
      isotyp = 1
      ixcw   = anint (rxc(nc))
      if (ixcw .gt. rxc(nc)) ixcw = ixcw -1
      ixce = ixcw +1
      if (ixcw .lt. 1 .or. ixce .gt. igx) isotyp = 0
      fi   = rxc(nc) -ixcw
      jycs = anint (ryc(nc))
      if (jycs .gt. ryc(nc)) jycs = jycs -1
      jycn = jycs +1
      fj   = ryc(nc) -jycs
      if (jycs .lt. 1 .or. jycn .gt. jgy) isotyp = 0
      if (isotyp .eq. 1) then
c
c                     obtain wind directions north, south, west and east
c                     of isogon intersection
c                     note, directions are toward not from.
c
        if (fi .ge. 0.2 .and. fi .le. 0.8 .and.
     &      fj .ge. 0.2 .and. fj .le. 0.8) then
          ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),fi)
          dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),fi)
          ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),fj)
          dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),fj)
        elseif (fj .ge. 0.2 .and. fj .le. 0.8) then
          if (fi .lt. 0.2) then
            ddn = dfld(ixcw,jycn)
            dds = dfld(ixcw,jycs)
            ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),fj)
            dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),fj)
          else
            ddn = dfld(ixce,jycn)
            dds = dfld(ixce,jycs)
            ddw = avgddt (dfld(ixcw,jycs),dfld(ixcw,jycn),fj)
            dde = avgddt (dfld(ixce,jycs),dfld(ixce,jycn),fj)
          endif
        elseif (fi .ge. 0.2 .and. fi .le. 0.8) then
          if (fj .lt. 0.2) then
            ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),fi)
            dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),fi)
            ddw = dfld(ixcw,jycs)
            dde = dfld(ixce,jycs)
          else
            ddn = avgddt (dfld(ixcw,jycn),dfld(ixce,jycn),fi)
            dds = avgddt (dfld(ixcw,jycs),dfld(ixce,jycs),fi)
            ddw = dfld(ixcw,jycn)
            dde = dfld(ixce,jycn)
          endif
        elseif (fi .lt. 0.2) then
          if ( fj .lt. 0.2) then
            if (jycs .gt. 1 .and. ixcw .gt. 1) then
              ddn = dfld(ixcw,jycn)
              dds = dfld(ixcw,jycs-1)
              ddw = dfld(ixcw-1,jycs)
              dde = dfld(ixce,jycs)
            else
              isotyp = 0
            endif
          else
            if (ixcw .gt. 1 .and. jycn .lt. jgy) then
              ddn = dfld(ixcw,jycn+1)
              dds = dfld(ixcw,jycs)
              ddw = dfld(ixcw-1,jycn)
              dde = dfld(ixce,jycn)
            else
              isotyp = 0
            endif
          endif
        elseif (fj .lt. 0.2) then
          if (jycs .gt. 1 .and. ixce .lt. igx) then
            ddn = dfld(ixce,jycn)
            dds = dfld(ixce,jycs-1)
            ddw = dfld(ixcw,jycs)
            dde = dfld(ixce+1,jycs)
          else
            isotyp = 0
          endif
        else
          if (ixce .lt. igx .and. jycn .lt. jgy) then
            ddn = dfld(ixce,jycn+1)
            dds = dfld(ixce,jycs)
            ddw = dfld(ixcw,jycn)
            dde = dfld(ixce+1,jycn)
          else
            isotyp = 0
          endif
        endif
      endif
      if (isotyp .eq. 1) then
c
c                     check the type of flow pattern associated with
c                     isogon intersection
c
c                       check for:  cyclonic circulation, nh
c                                   anticyclonic circulation, sh
c
        ichk = 0
        if (ddn  .ge. 210.0 .and. ddn .le. 315.0) ichk = ichk +1
        if (ddw  .ge. 120.0 .and. ddw .le. 225.0) ichk = ichk +1
        if (dds  .ge. 030.0 .and. dds .le. 135.0) ichk = ichk +1
        if ((dde .ge. 000.0 .and. dde .le. 045.0) .or.
     &      (dde .ge. 300.0 .and. dde .le. 360.0)) ichk = ichk +1
c
        if (ichk .ge. 3) then
c                     closed circulation found
          isotyp = ichk
        else
c
c                     check for anticyclonic circulation, nh
c                                   cyclonic circulation, sh
c
          ichk = 0
          if (ddn  .ge. 045.0 .and. ddn .le. 150.0) ichk = ichk +1
          if (dde  .ge. 135.0 .and. dde .le. 240.0) ichk = ichk +1
          if (dds  .ge. 225.0 .and. dds .le. 330.0) ichk = ichk +1
          if ((ddw .ge. 000.0 .and. ddw .le. 060.0) .or.
     &        (ddw .ge. 315.0 .and. ddw .le. 360.0)) ichk = ichk +1
          if (ichk .ge. 3) then
c                     closed circulation found
            isotyp = -ichk
          else
c
c                     flow appears to be a col
c
            isotyp = 0
          endif
        endif
      endif
c
      end
      subroutine chkfcir (ddfld,ixgrd,jygrd,mni,mxi,mnj,mxj,nhsh,mxcc
     &  ,cirdat,nccf)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  chkfcir
c
c  DESCRIPTION:  determine approximate location of cyclonic
c                circulation(s) in both NH and SH
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call chkfcir (ddfld,igrdx,jgrdy,mni,mxi,mnj,mxj,nhsh,mxcc,
c                        cirdat,nccf)
c
c  PARAMETERS:
c     NAME        TYPE        USAGE             DESCRIPTION
c   --------     -------      ------   ------------------------------
c    ddfld        real         in      global wind direction (to) field
c    igrdx         int         in      first  dimension of ddfld
c    jgrdy         int         in      second dimension of ddfld
c      mni         int         in      first  dimension start of window
c      mxi         int         in      first  dimension end of window
c      mnj         int         in      second dimension start of window
c      mxj         int         in      second dimension end of window
c     nhsh         int         in      north/south hemisphere indicator
c     mxcc         int         in      maximum number of cyclonic
c                                      circulations (cc) allowed
c   cirdat        real         out     array for circulation data
c                                        (1,  first  dimension estimate
c                                        (2,  second dimension estimate
c                                        (3,  wind support factor
c     nccf         int         out     number of cc found
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c    Name          Description
c   --------       -----------------------------------------------------
c   avgddt         calculate weighted average wind direction
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dde        real       wind direction at East-point
c         ddn        real       wind direction at North-point
c         dds        real       wind direction at South-point
c         ddw        real       wind direction at West-point
c         f1         real       fractional grid-length to "center line"
c         ichk        int       sum of winds within window
c         ixce        int       eastern-edge index
c         jycn        int       northern-edge index
c         jycs        int       southern-edge index
c         ixcw        int       western-edge index
c          rxc       real       approximate first  dimension location
c          ryc       real       approximate second dimension location
c
c  METHOD:  1.  Check wind direction at cardinal points about
c               central point.
c           2.  If 3 or 4 agree with cyclonic flow
c               assign cirdat sum of agreement.
c           3.  Replace duplicates when sum is 4.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
c    Increase allowed cross flow by 15 degrees to better accommodate
c    1000 mb boundary layer flow
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c      formal parameters
      integer ixgrd, jygrd, mni, mxi, mnj, mxj, nhsh, mxcc, nccf
      real ddfld(ixgrd,jygrd), cirdat(4,mxcc)
c
c      local variables
      integer i, ii, im1, ip1, j, n, ixcw, ixce, jycs, jycn, ichk
      real f1, ddn,dds,dde,ddw, rxc, ryc
c      real function
      real avgddt
c . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nccf = 0
      do j=mnj, mxj-1
        ryc  = j +0.5
        jycs = j
        jycn = j +1
        do ii=mni, mxi-1
c                assume field is cyclic in first dimension
          i = ii
          if (i .lt. 1) then
            i = ixgrd +i
          elseif (i .gt. ixgrd) then
            i = i -ixgrd
          endif
          rxc  = i +0.5
          ixcw = i
          ixce = i +1
          if (ixce .gt. ixgrd) ixce = ixce -ixgrd
c
c                obtain wind directions north, south, west and east
c                note, directions are to not from.
c
          f1  = rxc -i
          ddn = avgddt (ddfld(ixcw,jycn),ddfld(ixce,jycn),f1)
          dds = avgddt (ddfld(ixcw,jycs),ddfld(ixce,jycs),f1)
          f1  = ryc -j
          ddw = avgddt (ddfld(ixcw,jycs),ddfld(ixcw,jycn),f1)
          dde = avgddt (ddfld(ixce,jycs),ddfld(ixce,jycn),f1)
c
c                check the type of flow pattern associated with
c                this grid block
          ichk = 0
          if (nhsh .gt. 0) then
c
c                  check for:  cyclonic circulation, nh
c
            if (ddn .ge. 210.0 .and. ddn .le. 315.0) ichk = 1
            if (ddw .ge. 120.0 .and. ddw .le. 225.0) ichk = ichk +1
            if (dds .ge. 030.0 .and. dds .le. 135.0) ichk = ichk +1
            if ((dde .ge. 000.0 .and. dde .le. 045.0) .or.
     &          (dde .ge. 300.0 .and. dde .le. 360.0)) ichk = ichk +1
          else
c
c                              cyclonic circulation, sh
c
            if (ddn .ge. 045.0 .and. ddn .le. 150.0) ichk = 1
            if (dde .ge. 135.0 .and. dde .le. 240.0) ichk = ichk +1
            if (dds .ge. 225.0 .and. dds .le. 330.0) ichk = ichk +1
            if ((ddw .ge. 000.0 .and. ddw .le. 060.0) .or.
     &          (ddw .ge. 315.0 .and. ddw .le. 360.0)) ichk = ichk +1
          endif
          if (ichk .ge.  3) then
c
c                cyclonic circulation found, see if this is a
c                new or "duplicate" circulation
c
            if (nccf .gt. 0) then
              n = 0
              do while (ichk.gt.0 .and. n.lt.nccf)
                n = n +1
                if (abs (cirdat(1,n) -rxc) .lt. 1.8) then
                  if (abs (cirdat(2,n) -ryc) .lt. 1.8) then
c
c                    "duplicate" found, keep 4 over 3
c
                    if (ichk .gt. nint (cirdat(3,n))) then
c                      replace old with new location
                      cirdat(1,n) = rxc
                      cirdat(2,n) = ryc
                      cirdat(3,n) = 4.0
                    endif
                    ichk = 0
                  endif
                endif
              enddo
              if (ichk .gt. 0) then
c                new point was not absorbed above
                nccf = nccf +1
                if (nccf .lt. mxcc) then
c                    add new cyclonic circulation
                  cirdat(1,nccf) = rxc
                  cirdat(2,nccf) = ryc
                  cirdat(3,nccf) = ichk
                endif
              endif
            else
              nccf = 1
              cirdat(1,nccf) = rxc
              cirdat(2,nccf) = ryc
              cirdat(3,nccf) = ichk
            endif
          endif
        enddo
      enddo
      do j=mnj+1, mxj-1
        ryc = j
        do ii=mni+1, mxi-1
c                assume field is cyclic in first dimension
          i = ii
          if (i .lt. 1) then
            i = ixgrd +i
          elseif (i .gt. ixgrd) then
            i = i -ixgrd
          endif
          ip1 = i +1
          if (ip1 .gt. ixgrd) ip1 = ip1 -ixgrd
          im1 = i -1
          if (im1 .lt. 1) im1 = ixgrd
c
c                obtain wind directions north, south, west and east
c                note, directions are to not from.
c
          ddn = ddfld(i,j+1)
          dds = ddfld(i,j-1)
          ddw = ddfld(im1,j)
          dde = ddfld(ip1,j)
c
c                check the type of flow pattern associated with
c                this grid block
          ichk = 0
          if (nhsh .gt. 0) then
c
c                  check for:  cyclonic circulation, nh
c
            if (ddn .ge. 210.0 .and. ddn .le. 315.0) ichk = 1
            if (ddw .ge. 120.0 .and. ddw .le. 225.0) ichk = ichk +1
            if (dds .ge. 030.0 .and. dds .le. 135.0) ichk = ichk +1
            if ((dde .ge. 000.0 .and. dde .le. 045.0) .or.
     &          (dde .ge. 300.0 .and. dde .le. 360.0)) ichk = ichk +1
          else
c
c                              cyclonic circulation, sh
c
            if (ddn .ge. 045.0 .and. ddn .le. 150.0) ichk = 1
            if (dde .ge. 135.0 .and. dde .le. 240.0) ichk = ichk +1
            if (dds .ge. 225.0 .and. dds .le. 330.0) ichk = ichk +1
            if ((ddw .ge. 000.0 .and. ddw .le. 060.0) .or.
     &          (ddw .ge. 315.0 .and. ddw .le. 360.0)) ichk = ichk +1
          endif
          if (ichk .ge. 3) then
c
c                cyclonic circulation found, see if this is a
c                new or "duplicate" circulation
c
            rxc = i
            if (nccf .gt. 0) then
              n = 0
              do while (ichk.gt.0 .and. n.lt.nccf)
                n = n +1
                if (abs (cirdat(1,n) -rxc) .lt. 1.1) then
                  if (abs (cirdat(2,n) -ryc) .lt. 1.1) then
c
c                    "duplicate" found, keep 4 over 3
c
                    if (ichk .gt. nint (cirdat(3,n))) then
c                      replace old with new location
                      cirdat(1,n) = rxc
                      cirdat(2,n) = ryc
                      cirdat(3,n) = 4.0
                    endif
                    ichk = 0
                  endif
                endif
              enddo
              if (ichk .gt. 0) then
c                new point was not absorbed above
                nccf = nccf +1
                if (nccf .lt. mxcc) then
c                    add new cyclonic circulation
                  cirdat(1,nccf) = rxc
                  cirdat(2,nccf) = ryc
                  cirdat(3,nccf) = ichk
                endif
              endif
            else
              nccf = 1
              cirdat(1,nccf) = rxc
              cirdat(2,nccf) = ryc
              cirdat(3,nccf) = ichk
            endif
          endif
        enddo
      enddo
c
      end
      subroutine cirloc (dfld,ixgrd,jygrd,imin,jmin,imax,jmax,nhsh,
     &                   kccf,kuvs,kint,xc,yc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cirloc
c
c  DESCRIPTION:  driver routine for locating circulation with isogons
c
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call cirloc (dfld,ixgrd,jygrd,imin,jmin,imax,jmax,nhsh,
c                       kccf,kuvs,kint,xc,yc)
c
c  PARAMETERS:
c     NAME        TYPE      USAGE             DESCRIPTION
c   --------     ------     ------   ------------------------------
c      dfld       real        in     wind direction field, deg
c     ixgrd        int        in     first  dimension of field
c     jygrd        int        in     second dimension of field
c      imin        int        in     first  dimension start of window
c      jmin        int        in     second dimension start of window
c      imax        int        in     first  dimension end of window
c      jmax        int        in     second dimension end of window
c      kccf        int       out     number of cyclones found
c      kuvs        int       out     wind support factor
c                                      0 - no circulation, col
c                                      3 - three quads, cyclonic
c                                      4 - four quads, cyclonic
c      kint        int       out     number of isogons
c                                    1 - 9 - cyclone found
c                                      -77 - no intersection found
c                                      -88 - no isogons produced
c        xc       real       out     x-grid (lon) cyclone location
c        yc       real       out     y-grid (lat) cyclone location
c
c  COMMON BLOCKS:
c
c      BLOCK    NAME    TYPE   USAGE              NOTES
c     -------  ------   ----   ------   -------------------------------
c       box     lbox     int    out     output unit number
c                 xs    real    out     starting first dim of isogon box
c                 xl    real    out     ending first dim of isogon box
c                 ys    real    out     starting second dim isogon box
c                 yl    real    out     ending second dim of isogon box
c                rxc    real    out     running x-grid location
c                ryc    real    out     running y-grid location
c                nip     int    out     number of intersections
c      view     mini     int    out     starting first dim of isogon box
c               maxi     int    out     ending first dim of isogon box
c               minj     int    out     starting second dim isogon box
c               maxj     int    out     ending second dim of isogon box
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     bad  first dimension     write diagnostic, correct error
c     bad second dimension     write diagnostic, correct error
c     no isogons produced      set flag, write diagnostic and return
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c          isocnt     driver routine for producing isogons
c         calcntr     calculate centroid of isogon intersections
c          chkcir     check type of circulation found
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           ixg       int       first  dimension of windowed dd-field
c           jyg       int       second dimension of windowed dd-field
c           ncc       int       number of cyclonic circulations found
c
c  METHOD:  1) Establish size and location of local grid for
c              constructing isogons.
c           2) Load grid with wind direction values.
c           3) Load common blocks for constructing isogons.
c           4) Construct isogons and determine if there are
c              intersections within the box.
c           5) If one or more systems of intersections are found,
c              determine center of each and the synoptic system that
c              the center(s) represent.
c           6) For each, cyclonic center found load the following:
c              a.  wind support by quadrants (must be 3 or 4)
c              b.  number of intersections used to determine location
c              c.  global grid location of cyclone
c           7) Pass on the number of cyclones found.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          -----------    ---------------------------------------
c             box.inc     common block
c            view.inc     common block
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
c    Initial installation on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer ixgrd, jygrd, imin, jmin, imax, jmax, nhsh
      integer kccf, kuvs(4), kint(4)
      real dfld(ixgrd,jygrd), xc(4), yc(4)
c
c         local variables
      integer ixg, jyg
      parameter (ixg = 7, jyg = 7)
c
      integer is, ie, js, je, n, j, m, i, ii, ix, jy, ibyj, kntr
      integer ncc, nn, k
      integer ktyp(4), kcc(4)
      real ddgrd(ixg,jyg)
c
      INCLUDE 'view.inc'
      INCLUDE 'box.inc'
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   load local grid, ddgrd, with wind directions.
c                   allow for crossing 0 longitude, which will probably
c                   never happen, for software engineering's sake.
c
      is = imin -1
      if (is .lt. 1) is = ixgrd +is
      ie = imax +2
      if (ie .lt. is) ie = ixgrd +ie
      if (ie -is .gt. ixg -1) then
        ie = is +ixg -1
        write (33,*) ' CIRLOC, warning -- first dimension too big.'
      endif
      js = jmin -1
      je = jmax +2
      if (je -js .gt. jyg -1) then
        je = js +jyg -1
        write (33,*) ' CIRLOC, warning -- second dimension too big.'
      endif
c
      n = 0
      do j=js, je
        n = n +1
        m = 0
        do i=is, ie
          ii = i
          if (ii .gt. ixgrd) ii = ii -ixgrd
          m = m +1
          ddgrd(m,n) = dfld(ii,j)
        enddo
      enddo
c
c                   load isogon common blocks
c
      mini = 2
      xs   = 2.0
      maxi = 5
      xl   = 5.0
      minj = 2
      ys   = 2.0
      maxj = 5
      yl   = 5.0
      ix   = ixg
      jy   = jyg
      ibyj = ix*jy
      nsys = 0
      do n=1, 4
        rxc(n)  = 0.0
        ryc(n)  = 0.0
        nip(n)  = 0
        ktyp(n) = 0
        do m=1, 10
          cx(n,m) = 0.0
          cy(n,m) = 0.0
        enddo
      enddo
      lbox =  9
      open (lbox,file='xyboxd',form='formatted')
      write (9,*) ' cirloc, x-box, fm ',mini,' to ',maxi,' y-box, fm '
     &            ,minj,' to ',maxj,' for cntr near ',xc(1),' ',yc(1)
c
c                   calculate isogons and determine if there is an
c                   intersection(s) within the box, if there is an
c                   interection determine the type of flow depicted
c                   by the isogons for each.
c
      kntr = 0
      call isocnt (ddgrd,ix,jy,ibyj,kntr)
      if (kntr .gt. 0) then
c
c                   isogons were created
c
        if (nsys .gt. 0) then
c
c                     nsys isogon centers were found
c
          ncc = 0
          do n=1, nsys
            kcc(n) = 0
            if (rxc(n).gt.0.0 .and. ryc(n).gt.0.0) then
c
c                   running intersection is available, if there are
c                   more than 2 intersections, locate centroid
c
              nn = n
              if (nip(n) .gt. 2) call calcntr (nn)
              write (9,*) 'cirloc, intersection at ',rxc(n),' ',ryc(n)
c
c                   check type of circulation found with isogons
c
              call chkcir (ddgrd,ix,jy,nn,ktyp(n))
c
c                   evaluate output from isogons
c
              if (ktyp(n) .ne. 0)  then
                write (9,*) 'cirloc, found circulation, type ',ktyp(n)
                write(33,*) 'cirloc, found circulation, type ',ktyp(n)
              endif
              if (iabs (ktyp(n)) .ge. 3) then
                if (nhsh.gt.0 .and. ktyp(n).gt.0) then
c
c                   closed cyclonic circulation found in NH
c
                  ncc    = ncc +1
                  kcc(n) = -1
                elseif (nhsh.lt.0 .and. iabs (ktyp(n)).le.4) then
c
c                   closed cyclonic circulation found in SH
c
                  ncc    = ncc +1
                  kcc(n) = -1
                endif
              else
                write (9,*) 'cirloc, found a col for location ',n
                write(33,*) 'cirloc, found a col for location ',n
              endif
            endif
          enddo
          if (ncc .gt. 0) then
            k = 0
            do n=1, nsys
              if (kcc(n) .lt. 0) then
c
c                   good cyclonic circulation found
c
                k = k +1
                kuvs(k) = iabs (ktyp(n))
                kint(k) = nip(n)
                xc(k)   = float (is -1) +rxc(n)
                yc(k)   = float (js -1) +ryc(n)
                write(33,*) 'cirloc, ',k,' qds ',kuvs(k),' int ',kint(k)
              endif
            enddo
            kccf = k
          else
            kccf = -1
            write (9,*) 'circloc, no cyclones found near ',xc(1),' ',
     &                   yc(1)
          endif
        else
          kccf = -77
          write (9,*) 'cirloc, no intersection found near ',xc(1),' ',
     &                 yc(1)
        endif
      else
        kccf = -88
        write (9,*) 'cirloc, no isogons produced $$$$$'
      endif
      close (lbox)
c
      end
      subroutine clltxy (blat,blon,xgrd,ygrd,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  clltxy
c
c  DESCRIPTION:  convert lat,lon to x,y grid locations for FNMOC global
c                one-degree grid
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call clltxy (blat,blon,xgrd,ygrd,ierr)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     blat         real          in     latitude, deg  +NH, -SH
c     blon         real          in     longitude, deg (0 - 360E)
c     xgrd         real          out    first  dimension location
c     ygrd         real          out    second dimension location
c     ierr          int          out    error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c   invalid lat,lon point    set error flag to -1 and write diagnostic
c
c  ADDITIONAL COMMENTS:
c     Note: grid coordinates are traditional 1-based NOT 0-based
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          clon      real       working longitude
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer ierr
      real blat, blon, xgrd, ygrd
c
c         local variables
      real clon
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = 0
      clon = blon
      if (clon .eq. 360.0) clon = 0.0
      xgrd = 1.0 +clon
      if (xgrd .lt. 1.0 .or. xgrd .ge. 361.0) then
        write (*,*) 'clltxy, longitude error, lon = ',blon
        ierr = -1
      endif
      ygrd = 91.0 +blat
      if (ygrd .lt. 1.0 .or. ygrd .gt. 181.0) then
        write (*,*) 'clltxy, latitude error, lat = ',blat
        ierr = -1
      endif
c
      end
      subroutine cxytll (xgrd,ygrd,clat,clon,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cxytll
c
c  DESCRIPTION:  convert x,y grid locations of FNMOC global one-degree
c                grid to lat,lon
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call cxytll (xgrd,ygrd,clat,clon,ierr)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     clat         real          out    latitude, deg  +NH, -SH
c     clon         real          out    longitude, deg (0 - 360E)
c     xgrd         real          in     first  dimension location
c     ygrd         real          in     second dimension location
c     ierr          int          out    error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c   invalid x,y grid point    set error flag to -1 and write diagnostic
c
c  ADDITIONAL COMMENTS:
c     Note: grid coordinates are traditional 1-based NOT 0-based
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:  none
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer ierr
      real clat, clon, xgrd, ygrd
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = 0
      clon = xgrd  -1.0
      if (clon.lt.0.0 .or. clon.gt.360.0) then
        write (33,*) 'cxytll, x-grid error, x-grid = ',xgrd
        ierr = -1
      endif
      clat = ygrd -91.0
      if (clat.lt.-90.0 .or. clat.gt.90.0) then
        write (33,*) 'cxytll, y-grid error, y-grid = ',ygrd
        ierr = -1
      endif
c
      end
      REAL FUNCTION CYCIT1 (RML,RNL,BFLD,MGRD,NGRD)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)cycit1.f	1.1 12/22/93 
C                        23:21:46 /home/library/util/cycit1/src/SCCS/s.cycit1.f
C
C  CONFIGURATION IDENTIFICATION: NONE
C
C  MODULE NAME: CYCIT1
C
C  DESCRIPTION:  INTERPOLATE FIELD, BFLD, WHICH IS CYCLIC IN THE FIRST
C                DIMENSION, BASED UPON AYRES CENTRAL DIFFERENCE FORMULA
C                WHICH PRODUCES VALUES THAT ARE CONTINUOUS IN THE FIRST
C                DERIVATIVE, EXCEPT NEAR LIMITS OF SECOND DIMENSION,
C                WHERE BILINEAR INTERPOLATION IS USED.
C
C  COPYRIGHT:                  (C) 1993 FLENUMMETOCCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  NONE
C
C  REFERENCES: NONE
C  
C  CLASSIFICATION:  UNCLASSIFIED
C
C  RESTRICTIONS:  BFLD MUST BE 4 BY 4 OR LARGER FIELD AND CYCLIC IN
C                 FIRST DIMENSION
C
C  COMPUTER/OPERATING SYSTEM 
C               DEPENDENCIES:  UNIX Operating System
C
C  LIBRARIES OF RESIDENCE: /usr/local/fnoc/lib/libfnoc.a
C
C  USAGE:  VAL = CYCIT1 (RML,RNL,BFLD,MGRD,NGRD)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       RML         REAL         IN     FIRST  DIMENSION POINT LOCATION
C       RNL         REAL         IN     SECOND DIMENSION POINT LOCATION
C       BFLD        REAL         IN     FIELD  FOR INTERPOLATION
C       MGRD         INT         IN     FIRST  DIMENSION OF BFLD
C       NGRD         INT         IN     SECOND DIMENSION OF BFLD
C
C  COMMON BLOCKS:  NONE
C
C  FILES:  NONE
C
C  DATA BASES:  NONE
C
C  NON-FILE INPUT/OUTPUT:  
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C    NONE     
C
C  ERROR CONDITIONS:
C    Since cycit1 is a function, the out-of-bounds error condition re-
C    turns a large negative number (-999999999.00).
C
C  ADDITIONAL COMMENTS:
C           1.  IF SECOND DIMENSION LOCATION IS OUT-OF-BOUNDS,
C               IT'S REPRESENTATIVE IS MADE IN BOUNDS.
C           2.  NO CHECK IS MADE ON IN-BOUNDS FOR FIRST DIMENSION
C               LOCATION.  APPROX. RANGE: (-MGRD < RmL < 2*MGRD)
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  NONE
C
C  LOCAL VARIABLES:
C
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C             AA     REAL       INTERPOLATION FACTOR
C             BB     REAL       INTERPOLATION FACTOR
C             BV     REAL       Temporary store of array value
C             CC     REAL       INTERPOLATION FACTOR
C          EV3M1     REAL       INTERPOLATION FACTOR
C          EV3M2     REAL       INTERPOLATION FACTOR
C          EV4M2     REAL       INTERPOLATION FACTOR
C            ECV     REAL       INTERPOLATED ROW OR COLUMN VALUES
C                               FOR FINAL INTERPOLATION
C             M2      INT       TRUNCATED FIRST DIMENSION POINT LOCATION
C             M3      INT       M2 +1
C             N2      INT       TRUNCATED SECOND DIMENSION LOCATION
C             N3      INT       N2 +1
C              R     REAL       FRACTION OF FIRST DIMENSION OF GRID
C                               POINT IS LOCATED FROM M2
C             RN     REAL       REAL REPRESENTATIVE OF RNL
C             RM     REAL       REAL REPRESENTATIVE OF RML
C              S     REAL       FRACTION OF SECOND DIMENSION OF GRID
C                               POINT IS LOCATED FROM N2
C           VFLD     REAL       BLOCK OF VALUES USED FOR INTERPOLATION
C
C  METHOD:  AYRES CENTRAL DIFFERENCE FORMULA USED IN TWO DIMENSIONS
C
C  INCLUDE FILES: NONE
C
C  COMPILER DEPENDENCIES:  NONE
C
C  COMPILE OPTIONS:  NONE
C
C  MAKEFILE:  */cycit1/src/makefile
C
C  RECORD OF CHANGES: NONE
C
C
C...................END PROLOGUE.......................................
C
C         FORMAL PARAMETERS
C
      IMPLICIT NONE

      INTEGER MGRD,NGRD
      REAL RML, RNL, BFLD(MGRD,NGRD)
C
C         LOCAL VARIABLES
C
      INTEGER M2, N2, M3, N3, K, N, M, I
      REAL EV3M1, EV3M2, EV4M2, AA, BB, CC, RN, RM, R, S
      REAL ECV(4), VFLD(16), BV
C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C
C
      IF (MGRD.GE.4 .AND. NGRD.GE.4) THEN
C
        Rn = RnL
        n2 = Rnl
C                   MAKE second DIMENSION LOCATION IN BOUNDS
        IF (n2 .LT. 1) THEN
          n2 = 1
          Rn = 1.0
        ELSEIF (n2 .GT. nGRD) THEN
          n2 = nGRD
          Rn = nGRD
        ENDIF
C
        rm = rml
        m2 = rml
        R  = RM -M2
        S  = RN -N2
        IF (n2.GE.2 .AND. n2.LT.(nGRD -1)) THEN
C
C                   PERFORM INTERPOLATION BASED UPON AYRES
C
          K  = 0
C                   LOAD 4-BY-4 ARRAY, VFLD, FOR INTERPOLATION
          DO 120 n=n2-1, n2+2, 1
            DO 110 m=m2-1, m2+2, 1
              i = m
              IF (i .LE. 0) THEN
                i = mGRD +i
              ELSEIF (i .GT. mGRD) THEN
                i = i -mGRD
              ENDIF
              K = K +1
              VFLD(K) = BFLD(i,n)
  110       CONTINUE
  120     CONTINUE
C
C                   PERFORM AYRES CENTRAL DIFFERENCES AND INTERPOLATION,
C                   FOUR TIMES TO LOAD ECV
C
          DO 130 K=1, 4
            EV3M1  = VFLD(K+8) -VFLD(K)
            EV3M2  = VFLD(K+8) -VFLD(K+4)
            EV4M2  = 0.5*(VFLD(K+12) -VFLD(K+4))
            AA     = 0.5*EV3M1
            BB     = 3.0*EV3M2 -EV3M1 -EV4M2
            CC     = AA +EV4M2 -EV3M2 -EV3M2
            ECV(K) = VFLD(K+4) +S*(AA +S*(BB +S*CC))
  130     CONTINUE
C
C                   PERFORM AYRES CENTRAL DIFFERENCES WITH ECV
C
          EV3M1  = ECV(3) -ECV(1)
          EV3M2  = ECV(3) -ECV(2)
          EV4M2  = 0.5*(ECV(4) - ECV(2))
          AA     = 0.5*EV3M1
          BB     = 3.0*EV3M2 -EV3M1 -EV4M2
          CC     = AA +EV4M2 -EV3M2 -EV3M2
          CYCIT1 = ECV(2) +R*(AA +R*(BB +R*CC))
C
        ELSE
C
C                   PERFORM BILINEAR INTERPOLATION
C                   BUT USE CYCLIC CONDITIONS OF FIRST DIMENSION
C
          IF (m2 .LE. 0) THEN
            m2 = mGRD +m2
          ELSEIF (m2 .GT. mGRD) THEN
            m2 = m2 -mGRD
          ENDIF
          M3 = M2 +1
          IF (m3 .LE. 0) THEN
            m3 = mGRD +m3
          ELSEIF (m3 .GT. mGRD) THEN
            m3 = m3 -mGRD
          ENDIF
          BV = BFLD(M2,N2)
          IF (Rn.EQ.1.0 .OR. n2.EQ.nGRD) THEN
            CYCIT1 = BV +R*(BFLD(M3,N2) -BV)
          ELSE
            N3 = N2 +1
            CYCIT1 = BV +R*(BFLD(M3,N2) -BV) +S*(BFLD(M2,N3) -BV)
     .              +R*S*(BFLD(M3,N3) +BV -BFLD(M3,N2) -BFLD(M2,N3))
          ENDIF
        ENDIF
      ELSE
C
C                   ERROR VALUE RETURNED, BFLD MUST BE 4 BY 4 OR LARGER
C
        CYCIT1 = -999999999.0
      ENDIF
      RETURN
C
      END
      subroutine cycsfc (tcdat,mxf,mxc,kf,nc,ixg,jyg,sfcfld,suadat)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  cycsfc
c
c  DESCRIPTION:  obtain pressure at wind center
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:
c
c  CLASSIFICATION:  UNCLASSIFIED
c
c  RESTRICTIONS:
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call cycsfc (tcdat,mxf,mxc,kf,nc,ixg,jyg,suadat,sfcfld)
c
c  PARAMETERS:
c     NAME        TYPE     USAGE             DESCRIPTION
c   --------      ----     -----     ----------------------------------
c    tcdat        real      in       array of isogon locations at 1000 hPa
c      mxf         int      in       maximum forecasts, second dimension of tcda
c                                    and suadat
c      mxc         int      in       maximum cyclones, third dimension of tcdat
c                                    and suadat
c       kf         int      in       index to forecast
c       nc         int      in       index to cyclone
c      ixg         int      in       first  dimension of sfcfld
c      jyg         int      in       second dimension of sfcfld
c   sfcfld        real      in       surface pressure field, global
c   suadat        real     out       array of sfc
c
c  COMMON BLOCKS:  NONE
c
c  FILES:  NONE
c
c  DATA BASES:  NONE
c
c  NON-FILE INPUT/OUTPUT:  NONE
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     bad interpolation        set missing/bad data value and exit
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c      NAME           DESCRIPTION
c    -------     ----------------------
c    cycit1      FNMOC utility lib function for interpolation
c
c  LOCAL VARIABLES:
c        NAME      TYPE                 DESCRIPTION
c       ------     ----       ------------------------------------------
c      rixg        real       first dimension location in grid
c      rixg        real       first dimension location in grid
c      press       real       interpolated pressure value
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  NONE
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
c
c  MAKEFILE:  N/A
c
c  RECORD OF CHANGES:
c
c    <<change notice>>  V1.1  (14 MAY 1997)  Hamilton, H.
c      initial installation on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c     formal parameters
      integer  mxf, mxc, kf, nc, ixg, jyg
      real tcdat(2,mxf,mxc)
      real suadat(7,mxf,mxc)
      real sfcfld(ixg,jyg)
c
c     local variables
      real  rixg, rjyg, press, cycit1
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      rixg  = tcdat(1,kf,nc)
      rjyg  = tcdat(2,kf,nc)
      press = cycit1 (rixg,rjyg,sfcfld,ixg,jyg)
      if (press .gt. 0.0) then
        suadat(1,kf,nc) = press
      else
        suadat(1,kf,nc) = -99.9
      endif
c
      end
      subroutine evaliso (md1,fx1,fy1,nd2,fx2,fy2,m1s,m1e,n2s,n2e,npc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  evaliso
c
c  DESCRIPTION:  evaluate isogons for segments that may intersect
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-94-BHD-0107
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call evaliso (md1,fx1,fy1,nd2,fx2,fy2,m1s,m1e,n2s,n2e,npc)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      md1          int         in      dimension of fx1
c      fx1         real         in      array of x-values of isogon rh1
c      fy1         real         in      array of y-values of isogon rh1
c      nd2          int         in      dimension of fx2
c      fx2         real         in      array of x-values of isogon rh2
c      fy2         real         in      array of y-values of isogon rh2
c      m1s          int         out     array of rh1 start points
c      m1e          int         out     array of rh1 end points
c      n2s          int         out     array of rh2 start points
c      n2e          int         out     array of rh2 end points
c      npc          int        in/out   maximum size of m1s, m1e, n2s
c                                       n2e / count of segments that
c                                       contain potential centers
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dx         real       working difference in x
c         dy         real       working difference in x
c         epsilon    real       minimum value of distance
c         ddw        real       wind direction at West-point
c         mm          int       working index to rh1 values
c         mxpc        int       maximum number of segments
c         nn          int       working index to rh2 values
c         x1         real       working x location of rh1
c         y1         real       working y location of rh1
c
c  METHOD:  1.  Initialize starting and ending points to zero.
c           2.  Iteratively search rh1 and rh2 isogon locations for a
c               gap less than or equal to epsilon.  Mark the starting
c               indicies in m1s and n2s.
c           3.  Continue iterative search for a gap greater than
c               epsilon.  Mark the ending inicies in m1e and n2e.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (09 AUG 1995) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer md1, nd2, npc
      integer m1s(npc), m1e(npc), n2s(npc), n2e(npc)
      real fx1(md1), fy1(md1), fx2(nd2), fy2(nd2)
c
c         local variables
      integer m, mm, ms, mxpc, n, nn
      real x1, y1, dx, dy
      real epsilon
c
      data epsilon/0.1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   initialize prospective locations
c
      mxpc = npc
      do n=1, npc
        m1s(n) = 0
        m1e(n) = 0
        n2s(n) = 0
        n2e(n) = 0
      enddo
      npc = 0
c
c                   look for prospective starting and ending points
c
      ms = 1
 110  continue
      do m=ms, md1
        x1 = fx1(m)
        y1 = fy1(m)
        do n=1, nd2
          dx = abs (x1 -fx2(n))
          dy = abs (y1 -fy2(n))
          if (dx .le. epsilon .and. dy .le. epsilon) then
            npc = npc +1
            if (npc .le. mxpc) then
              m1s(npc) = m
              n2s(npc) = n
            else
              npc = mxpc
              goto 200
c
            endif
            mm   = m
            nn   = n
c
c                   top of internal loop to find ending point
c
 120        continue
            mm = mm +1
            nn = nn +1
            if (mm .le. md1 .and. nn .le. nd2) then
              dx = abs (fx1(mm) -fx2(nn))
              dy = abs (fy1(mm) -fy2(nn))
              if (dx .gt. epsilon .and. dy .gt. epsilon) then
c
c                     found ending point
c
                m1e(npc) = mm
                ms       = mm +1
                n2e(npc) = nn
                goto 110
c
              elseif (mm .lt. md1 .and. nn .lt. nd2) then
c
c                       jump to top of internal loop
c
                  goto 120
c
              else
                m1e(npc) = mm
                n2e(npc) = nn
                if (mm .lt. md1) then
                  ms = mm +1
                  goto 110
c
                else
c
c                       finished searches
c
                  goto 200
c
                endif
              endif
            else
              if (m1s(npc) .eq. m -1 .and. n2s(npc) .eq. n -1) then
c
c                   too close to the edge for find ending point
c
                npc = npc -1
              else
c
c                   at the edge, so assume this is the end
c
                m1e(npc) = mm -1
                n2e(npc) = nn -1
              endif
              goto 130
c
            endif
          endif
        enddo
 130    continue
      enddo
 200  continue
c
      end
      subroutine expand (uufld,vvfld,ixg,jyg,icyc,jcyc,ddfld,ssfld,ixe,
     &                   jye)
c
c
c
      integer ixg,jyg,icyc,jcyc,ixe,jye
      real    uufld(ixg,jyg), vvfld(ixg,jyg)
      real    ddfld(ixe,jye), ssfld(ixe,jye)
c
cx    ibc = icyc -6
      ibc = icyc -15
cx    jbc = jcyc -6
      jbc = jcyc -15
cx    rje = jbc -0.4
      rje = jbc -1
      do j=1, jye
cx      rje = rje +0.4
        rje = rje +1
cx      rie = ibc -0.4
        rie = ibc -1
        do i=1, ixe
cx        rie = rie +0.4
          rie = rie +1
cx        ddfld(i,j) = cycit1 (rie,rje,uufld,ixg,jyg)
          ddfld(i,j) = uufld(rie,rje)
cx        ssfld(i,j) = cycit1 (rie,rje,vvfld,ixg,jyg)
          ssfld(i,j) = vvfld(rie,rje)
        enddo
      enddo
      call calddto (ixe,jye,ddfld,ssfld)
c
      end
      subroutine flduvrd (nuinp,igrdx,jgrdy,uufld,vvfld,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  flduvrd
c
c  DESCRIPTION:  routine for reading u and v fields and producing
c                derived fields
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call flduvrd (nuinp,uufld,vvfld,ierr)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      nuinp        int          in     unit number to read fields
c      ddfld       real         out     wind direction field
c      fffld       real         out     wind speed field
c       ierr        int         out     error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:
c     NAME          TABLE      USAGE       DESCRIPTION
c    --------     -----------  ------  --------------------
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     missing field or         set error flag to non-zero
c        read error
c
c  ADDITIONAL COMMENTS:
c    Fields must be stacked in right order, for there is no checking
c    to see if they are right.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         calddto     calculates wind direction, towards (deg)
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dsetnam    char       data set name
c         dsets      char       data set names
c         geonam     char       geometry name
c         idgrid      int       internal dataset identifier number
c         igrdx       int       first  dimension of fields
c         irecnum     int       internal record sequence number
c         istatus     int       status of ISIS request
c         jgrdy       int       second dimension of fields
c         params     char       parameter names
c         rlvl1      real       level 1 value
c         rlvl2      real       level 2 value
c         seclvl     char       security level
c         title      char       title of field
c         typlvl     char       type of level
c         typmodl    char       type of model
c         units      char       units of fields
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer nuinp, igrdx, jgrdy, ierr
      real uufld(igrdx,jgrdy), vvfld(igrdx,jgrdy)
c
c         local variables
      integer ioe
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   read u-wind - into uufld
c
      read (nuinp,iostat=ioe) uufld
c
c                   read v-wind - into vvfld
c
      if (ioe .eq. 0) read (nuinp,iostat=ioe) vvfld
      if (ioe .eq. 0) then
        ierr = 0
      else
        ierr = -1
      endif
c
      end
      subroutine isocnt (dfld,mgrd,ngrd,mgbyng,kntr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isocnt
c
c  DESCRIPTION:  driver for producing isogons in pairs, 90 degrees
c                apart, and solving for the intersection of each pair
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:
c    CONTOURING AND HIDDEN-LINE ALGORITHMS FOR VECTOR GRAPHIC DISPLAYS.
c    AFAPL-TR-77-3, JANUARY 1977.                      DDC: AD A040530
c    AIR FORCE AERO-PROPULSION LABORATORY
c    AIR FORCE WRIGHT AERONAUTICAL LABORATORIES
c    AIR FORCE SYSTEMS COMMAND
c    WRIGHT-PATTERSON AIR FORCE BASE, OHIO 45433
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call isocnt (dfld,mgrd,ngrd,mgbyng,kntr)
c
c  PARAMETERS:
c     NAME         TYPE     USAGE             DESCRIPTION
c   --------      ------    -----    ------------------------------
c     dfld         real       in     wind direction field
c     mgrd          int       in     first  dimension of field
c     ngrd          int       in     second dimension of field
c   mgbyng          int       in     total length of field
c     kntr          int      out     number of isogons
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE   USAGE              NOTES
c     --------  --------   ----   -----   ------------------------
c       isoc        rh     real    out    real value of isogon, deg
c                 iter      int    out    iteration number
c                  nc1      int    out    isogon count first  iteration
c                  nc2      int    out    isogon count second iteration
c       isol     first      log    out    flag, true if start
c                 last      log    out    flag, true if end
c                 open      log    out    flag, true if open contour
c               backwd      log    out    flag, true if backward contour
c      mndir        ii      int    out    starting minimum first dim of
c                                         contouring block
c                   jj      int    out    starting minimum second dim of
c                                         contouring block
c                   iv      int    out    starting first dim contour
c                                         direction vector
c                   jv      int    out    starting second dim contour
c                                         direction vector
c       view      mini      int     in    starting first dim of box
c                 maxi      int     in    ending first dim of box
c                 minj      int     in    starting second dim of box
c                 maxj      int     in    ending second dim of box
c      zoomv      rint     real    out    first dim resolution of zoomed
c                                         block
c                 sint     real    out    second dim resolution of
c                                         zoomed block
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     wrong dimensions of      error diagnostics and exit
c     zoomed block
c
c  ADDITIONAL COMMENTS:
c     No closed contours are allowed, so this code has been removed.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         iostrc      traces isogons through field
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----    ----------------------------------
c            brh     real    base real "height" value
c           cint     real    contour interval
c           cntr     real    starting contour value
c            dtr     real    degree-to-radian conversion factor
c             hc     real    "height" value being contoured
c          ijtoi      int    double to single index function
c             jp      int    second index point
c           kzlk      int    first dimension of zoomed block
c           lzlk      int    secomd dimension of zoomed block
c           lfld      log    array for contour flags
c         maxim1      int    maxi -1
c         maxjm1      int    maxj -1
c         minip1      int    mini +1
c         minjp1      int    minj +1
c           mxnc      int    maximum number of contours
c            nij      int    single index for i,j location
c           nijp      int    nij of "upper" grid point
c             nr      int    number of contours
c           rdmn     real    minimum value of contour
c           rdmx     real    maximum value of contour
c             rh     real    real "height" value of contour
c             ru     real    "upper" value at grid point
c             rl     real    "lower" value at grid point
c           sfld     real    sine of (dd -rh)
c           zblk     real    zoomed block array
c
c  METHOD:
c    1.  Modification of contouring routines previously developed by
c        H. D. Hamilton for FNMOC graphics program CODEDEF.
c    2.  The trick in generating isogons is to trace the zero value of
c        sine (wind direction minus desired isogon direction).
c        Note that sine (0) equals sine (180).  Therefore, if the isogon
c        spacing is 10 degrees, only 10 through 180 degrees is required
c        to provide complete coverage.
c    3.  In order to improve the quality of the intersection point,
c        isogons are produced sequentially in pairs, 90 degrees apart.
c        Therefore, if the 10 degree isogon is not produced, the 100
c        degree isogon is not attempted.
c    4.  Since a complete field of isogons is not desired, only one
c        isogon is allowed for each direction.
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------     ----------------------------------------------
c           isoc.inc      common block
c           isol.inc      common block
c          mndir.inc      common block
c           view.inc      common block
c           zoom.inc      common block
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer mgrd, ngrd, mgbyng, kntr
      real dfld(mgrd,ngrd)
c
c         local variables
      integer kzlk,lzlk
      parameter (kzlk = 11,  lzlk = 11)
c
      logical lfld(mgbyng)
      integer ijtoi, i, j, minip1, minjp1, maxim1, maxjm1, nr
      integer mxnc, k, mn, nij, nijp, jp
      real hc, dtr, rdmn, rdmx, cint, cntr, brh, ru, rl
      real sfld(mgbyng), zblk(kzlk,lzlk)
c
      INCLUDE 'view.inc'
c
      INCLUDE 'isol.inc'
c
      INCLUDE 'isoc.inc'
c
      INCLUDE 'mndir.inc'
c
      INCLUDE 'zoomv.inc'
c
      data hc/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c         integer statement function:
      ijtoi(i,j) = (j-1)*mz +i
c
c - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
c
      dtr    = acos (-1.0)/180.0
      mz     = mgrd
      nz     = ngrd
      mbyn   = mgbyng
      kzlt   = kzlk
      lzlt   = lzlk
      rint   = 1.0/(kzlt -1)
      sint   = 1.0/(lzlt -1)
      minip1 = mini +1
      minjp1 = minj +1
      maxim1 = maxi -1
      maxjm1 = maxj -1
      nr     = 0
c
c           contouring is accomplished at one value, hc, at a time,
c           and one contour at a time.  true value of isogon is rh.
c
      rdmn =   1.0
      rdmx = 360.0
      cint =  10.0
      cntr = cint
      mxnc = anint (180.0/cint)
      brh  = cntr -cint
      do 490 k=1, mxnc
        if (mod (k,2) .ne. 0) then
          brh  = brh +cint
          rh   = brh
          iter = 1
          nc1  = 0
          nc2  = 0
        else
c                   check that first contour has more than one point
          if (nc1 .lt. 5) goto 490
c
          rh   = rh +90.0
          iter = 2
        endif
        write (9,*) ' isocnt, k ',k,' iter ',iter,' rh ',rh
        if (rh .lt. rdmn .or. rh .gt. rdmx) goto 490
c
        write (9,9010) rh
 9010   format (1x,'contouring all contours of value ',g11.5)
c
c                   field to be contoured, sfld, must be the sine of the
c                   difference between the true wind direction and the
c                   true value of the direction to be contoured, rh.
c                   note, the actual value of the contour being traced,
c                   hc, is always zero.
c
c                   initailize sfld and lfld
c
          do mn=1, mbyn
            lfld(mn) = .false.
            sfld(mn) = sin ((dfld(mn,1) -rh)*dtr)
          enddo
c
c               set edge bits for backward scan
c
c                        bottom row
        nij = ijtoi(mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          rl  = ru
          ru  = sfld(nij+1)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nij +1
        enddo
c                        right side
        nij = ijtoi (maxi,minj)
        ru  = sfld(nij)
        do j=minjp1, maxj
          rl   = ru
          nijp = ijtoi (maxi,j)
          ru   = sfld(nijp)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nijp
        enddo
c                        top row
        nij = ijtoi (maxi,maxj)
        ru  = sfld(nij)
        do i=maxim1, mini, -1
          rl  = ru
          ru  = sfld(nij-1)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nij -1
        enddo
c                        left side
        nij = ijtoi (mini,maxj)
        ru  = sfld(nij)
        do j=maxjm1, minj, -1
          rl   = ru
          nijp = ijtoi (mini,j)
          ru   = sfld(nijp)
          if (rl .ge. hc .and. ru .lt. hc) lfld(nij) = .true.
          nij = nijp
        enddo
c
        backwd = .false.
        open   = .true.
        first  = .true.
        last   = .false.
        kkk    = 0
c
c               the boundary of the array is scanned for the
c               beginning of any open contour of value hc, forward mode.
c
c                   scan bottom
        iv  = -1
        jv  =  0
        jj  = minj
        nij = ijtoi (mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          ii  = i
          rl  = ru
          nij = nij +1
          ru  = sfld(nij)
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c                   scan right side
        iv =  0
        jv = -1
        ii = maxi
        ru = sfld(ijtoi (maxi,minj))
        do j=minjp1, maxj
          rl = ru
          jj = j
          ru = sfld(ijtoi (maxi,j))
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   scan top
c
        iv  = 1
        jv  = 0
        jj  = maxj
        nij = ijtoi(maxi,jj)
        ru  = sfld(nij)
        do i=maxim1, mini, -1
          ii  = i
          rl  = ru
          nij = nij -1
          ru  = sfld(nij)
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   scan left side
c
        iv = 0
        jv = 1
        ii = mini
        j  = maxj
        ru = sfld(ijtoi(mini,j))
        do j=maxjm1, minj, -1
          rl = ru
          jj = j
          ru = sfld(ijtoi (mini,j))
          if (rl .lt. hc .and. ru .ge. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
        enddo
c
c                   rescan edges, using backward mode
c
        backwd = .true.
c
c                   scan bottom
c
        write(9,*) 'isocnt, starting open backwards'
        iv  = 1
        jv  = 0
        jj  = minj
        nij = ijtoi (mini,minj)
        ru  = sfld(nij)
        do i=minip1, maxi
          ii   = i -1
          rl   = ru
          ru   = sfld(nij+1)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          nij = nij +1
        enddo
c
c                    scan right side
c
        ii  = maxi
        iv  = 0
        jv  = 1
        nij = ijtoi (maxi,minj)
        ru  = sfld(nij)
        jj  = minj
        do j=minjp1, maxj
          rl   = ru
          jp   = j
          nijp = ijtoi (maxi,jp)
          ru   = sfld(nijp)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          jj  = jp
          nij = nijp
        enddo
c
c                   scan top
c
        iv  = -1
        jv  =  0
        jj  = maxj
        nij = ijtoi (maxi,jj)
        ru  =  sfld(nij)
        do i=maxim1, mini, -1
          ii  = i +1
          rl  = ru
          ru  = sfld(nij-1)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          nij = nij -1
        enddo
c
c                   scan left side
c
        ii  =  mini
        iv  =  0
        jv  = -1
        jj  = maxj
        nij = ijtoi (mini,jj)
        ru  = sfld(nij)
        do j=maxjm1, minj, -1
          rl   = ru
          jp   = j
          nijp = ijtoi (mini,jp)
          ru   = sfld(nijp)
          if (lfld(nij) .and. rl .ge. hc .and. ru .lt. hc) then
            call isotrc (sfld,lfld,zblk)
            if (last) then
              write(9,*) ' last for iter ',iter,' n1 ',nc1,' n2 ',nc2
              if (iter .eq. 1) then
                if (nc1 .gt. kzlt) goto 450
c
              else
                if (nc2 .gt. kzlt) goto 450
c
              endif
            endif
          endif
          jj  = jp
          nij = nijp
        enddo
 450   continue
        if (kkk .ne. 0) nr = nr +1
 490  continue
      if (nr .gt. 0) then
        write (9,9020) nr
      else
        write (9,9030)
      endif
 9020 format(' found about ',i3,' different valued contours')
 9030 format('   *** no contours ***')
      kntr = nr
c
      end
      subroutine isofnd (exc,eyc,nhsh,ddfld,igrdx,jgrdy,kccf,kuvs,kint,
     &                   xc,yc)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isofnd
c
c  DESCRIPTION:  driver routine to locate tropical cyclone with isogons
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  isofnd (exc,eyc,nhsh,ddfld,igrdx,jgrdy,kccf,kuvs,kint,xc,yc)
c
c  PARAMETERS:
c     NAME         TYPE      USAGE             DESCRIPTION
c   --------      -------    ------   ------------------------------
c       exc        real        in     x-location, estimated
c       eyc        real        in     y-location, estimated
c      nhsh         int        in     north/south indicator, +nh -sh
c     ddfld        real        in     wind direction global field, deg
c     igrdx         int        in     first  (x-lon) dimension of fields
c     jgrdy         int        in     second (y-lat) dimension of fields
c      kccf         int       out     cyclonic circulations found
c      kuvs         int       out     code of wind support
c                                          0 - no cyclone
c                                          3 - wind support in 3 quads
c                                          4 - wind support in 4 quads
c      kint         int       out     count of intersection support
c        xc        real       out     x-location of tropical cyclone
c        yc        real       out     y-location of tropical cyclone
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c          cirloc     driver routine to locate circulation center
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----     ----------------------------------
c           imax      int     maximum x-edge of isogon window
c           imin      int     minimum x-edge of isogon window
c           isx       int     x-truncated point of search
c           ixgd      int     first dimension of global fields
c           jmax      int     maximum y-edge of isogon window
c           jmin      int     minimum y-edge of isogon window
c           jsy       int     y-truncated point of search
c           jygd      int     second dimension of global fileds
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer nhsh, igrdx, jgrdy, kccf, kuvs(4), kint(4)
      real exc, eyc, xc(4), yc(4)
      real ddfld(igrdx,jgrdy)
c
c         local variables
      integer isx, jsy, imin, imax, jmin, jmax, ixgd, jygd
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      kccf  = 0
      xc(1) = exc
      isx   = exc
      yc(1) = eyc
      jsy   = eyc
      ixgd  = igrdx
      jygd  = jgrdy
c
c                   establish isogon window for search
c
      imin = isx  -1
      imax = imin +3
      jmin = jsy  -1
      jmax = jmin +3
c
c                   call driver for using isogon routines
c
      call cirloc (ddfld,ixgd,jygd,imin,jmin,imax,jmax,nhsh,kccf,kuvs,
     &             kint,xc,yc)
      if (kccf .le. 0) write (33,*) ' $ $ $ ISOFND, CYCLONE NOT FOUND ',
     &     '$ $'
c
      end
      subroutine isotrc (sfld,lfld,zblk)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isotrc
c
c  DESCRIPTION:  routine to trace isogons through field sfld via zoomed
c                grid blocks
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  see isocnt for references
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call isotrc (sfld,lfld,zblk)
c
c  PARAMETERS:
c     NAME         TYPE       USAGE             DESCRIPTION
c   --------      -------     ------   ------------------------------
c     sfld           real       in     field to be contoured
c     lfld        logical       in     field with contour flags set
c     zblk           real       in     working array for zooming
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c        box      lbox      int     in    unit number for diagnostics
c                   xs     real     in    starting first dimension of
c                                         isogon box
c                   xl     real     in    ending first dimension of
c                                         isogon box
c                   ys     real     in    starting second dimension of
c                                         isogon box
c                   yl     real     in    ending second dimension of
c                                         isogon box
c
c       view      mini      int     in    starting first dim of box
c                 maxi      int     in    ending first dim of box
c                 minj      int     in    starting second dim of box
c                 maxj      int     in    ending second dim of box
c
c       isoc        rh     real     in    real value of isogon, deg
c                 iter      int     in    iteration number
c                  nc1      int    out    isogon count first  iteration
c                  nc2      int    out    isogon count second iteration
c
c       isol     first      log    out    flag, true if start
c                 last      log    out    flag, true if end
c                 open      log     in    flag, true if open contour
c               backwd      log     in    flag, true if backward contour
c
c      mndir        ii      int     in    starting minimum first dim of
c                                         contouring block
c                   jj      int     in    starting minimum second dim of
c                                         contouring block
c                   iv      int     in    starting first dim contour
c                                         direction vector
c                   jv      int     in    starting second dim contour
c                                         direction vector
c                  kkk      int    out    contour generation indicator
c
c     zoomv       kzlt      int     in    first  dim of zoomed block
c                 lzlt      int     in    second dim of zoomed block
c                 mbyn      int     in    length of sfld
c                   mi      int    out    starting minimum first dim of
c                                         contouring block
c                   mz      int     in    first dimension of sfld
c                   nj      int    out    starting minimum second dim of
c                                         contouring block
c                   nz      int     in    second dimension of sfld
c                 rint     real     in    first dim resolution of zoomed
c                                         block
c                 sint     real     in    second dim resolution of
c                                         zoomed block
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                       ACTION
c     -----------------             ----------------------------
c     bad interpolation             error diagnostic and exit
c     no start-point in block       error diagnostic and exit
c     too many contour points       error diagnostic and exit
c
c  ADDITIONAL COMMENTS:
c     No closed contours are allowed - some code commented out
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         calint      calculate intersection of two isogons
c         isovzm      zoom grid square values into zblk
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c             hc     real       value of contour being contoured
c           ierr      int       interpolation flag, 0 no error
c          ijtoi      int       two dimension to one dimension function
c            ija      int       single index of point a
c            ijb      int       single index of point b
c            ijc      int       single index of point c
c            ijo      int       single index of point o
c             ka      int       first dim of point a in block
c             kb      int       first dim of point b in block
c             kc      int       first dim of point c in block
c             kf      int       first dim of point f in block
c            klt      int       temp storage
c             kv      int       first dim vector in block
c             la      int       second dim of point a in block
c             lb      int       second dim of point b in block
c             lc      int       second dim of point c in block
c             lf      int       second dim of point f in block
c             lv      int       second dim vector in block
c            mim      int       mi -1
c            mip      int       mi +1
c            njm      int       nj -1
c            njp      int       nj +1
c           nval      int       number of points in contour
c         nxylmt      int       error flag, 0 no error
c              t     real       grid length fraction
c            xus     real       x-grid point values of contour
c            yus     real       y-grid point values of contour
c             za     real       "height" value at point a
c             zb     real       "height" value at point b
c             zc     real       "height" value at point c
c             zf     real       "height" value at point f
c
c  METHOD:  see isocnt method and reference
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------     ----------------------------------------------
c            box.inc      common block
c           isoc.inc      common block
c           isol.inc      common block
c          isoxy.inc      common block
c          mndir.inc      common block
c           view.inc      common block
c          zoomv.inc      common block
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
c
      implicit none
c
      integer ncnt
      parameter (ncnt = 51)
c
      INCLUDE 'zoomv.inc'
c
      logical lfld(mbyn)
      real sfld(mz,nz), zblk(kzlt,lzlt)
c
      integer ijtoi, i, j, ka, la, ierr, kv, lv, nt, n, kf, lf, njp
      integer ija, ijo, ijb, ijc, nval, kb, lb, klt, kc, lc
      integer mim, njm, mip, nn, nxylmt
      real hc, zf, za, t, zb, zc
      real xus(ncnt), yus(ncnt)
c
      INCLUDE 'view.inc'
c
      INCLUDE 'box.inc'
c
      INCLUDE 'isol.inc'
c
      INCLUDE 'isoc.inc'
c
      INCLUDE 'mndir.inc'
c
      INCLUDE 'isoxy.inc'
c
      data hc/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c         integer function:
      ijtoi(i,j) = (j -1)*mz +i
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c              initialize conturing variables
c                     mi  i-value in sfld of lower left point
c                     nj  j-value in sfld of lower left point
c                     ka  k-value in grid point block of point a
c                     la  l-value in grid point block of point a
c
      mi = ii
      nj = jj
      if (.not. backwd) then
        if (iv .eq. -1) then
          mi = mi -1
          ka = 1
          la = 1
        elseif (jv .eq. -1) then
          mi = mi -1
          nj = nj -1
          ka = kzlt
          la = 1
        elseif (iv .eq. 1) then
          nj = nj -1
          ka = kzlt
          la = lzlt
        elseif (jv .eq. 1) then
          ka = 1
          la = lzlt
        endif
c
      else
        if (iv .eq. 1) then
          ka = kzlt
          la = 1
        elseif (jv .eq. 1) then
          mi = mi -1
          ka = kzlt
          la = lzlt
        elseif (iv .eq. -1) then
          mi = mi -1
          nj = nj -1
          ka = 1
          la = lzlt
        elseif (jv .eq. -1) then
          nj = nj -1
          ka = 1
          la = 1
        endif
      endif
c
c              remove flag set in subroutine isocnt
      lfld(ijtoi(ii,jj)) = .false.
c
c                   zoom grid into zblk
      call isovzm (sfld,zblk,ierr)
      if (ierr .ne. 0) then
        write (33,*) ' $$$ isotrc, initial mi ',mi,' nj ',nj,
     &               ' out of bounds'                                                          XXXXX
        goto 300
c
      endif
c
c              determine start point of contour in grid block
      kv = iv
      lv = jv
      nt = kzlt -1
      do n=1, nt
        kf = ka -kv
        lf = la -lv
        if (zblk(ka,la) .lt. hc  .and.  zblk(kf,lf) .ge. hc) goto 120
c
        ka = kf
        la = lf
      enddo
      write (33,9010) hc, kf, lf
      write (lbox,9010) hc, kf, lf
 9010 format (' $$$$$ no start point for contour ',g11.5,2(2x,i3))
      njp = nj +1
      write (33,9020) mi,njp, mi+1,njp, mi,nj, mi+1,nj
      write (lbox,9020) mi,njp, mi+1,njp, mi,nj, mi+1,nj
 9020 format (1x,'c ',i2,',',i3,5x,'b ',i2,',',i3,/,
     &        1x,'a ',i2,',',i3,5x,'o ',i2,',',i3)
      ija = ijtoi (mi,nj)
      ijo = ijtoi (mi+1,nj)
      ijb = ijtoi (mi+1,njp)
      ijc = ijtoi (mi,njp)
      write(33,9030) lfld(ijc),sfld(mi,njp), lfld(ijb),sfld(mi+1,njp)
      write(33,9030) lfld(ija),sfld(mi,nj),  lfld(ijo),sfld(mi+1,nj)
      write(lbox,9030) lfld(ijc),sfld(mi,njp), lfld(ijb),sfld(mi+1,njp)
      write(lbox,9030) lfld(ija),sfld(mi,nj),  lfld(ijo),sfld(mi+1,nj)
 9030 format (1x,l1,2x,g11.5,5x,l1,2x,g11.5)
      goto 300
c
 120  continue
c
c              initialize starting values
      first = .true.
      last  = .false.
      nval  = 1
      zf    = zblk(kf,lf)
      za    = zblk(ka,la)
c                   find first point of contour
      t = 0.0
      if (zf .ne. za) t = (zf -hc)/(zf -za)
      xus(1) = mi +rint*((kf -1) +t*kv)
      yus(1) = nj +sint*((lf -1) +t*lv)
ccc   if (.not. open) then
c                   save starting location
ccc     mif  = mi
ccc     njf  = nj
ccc     xusf = xus(1)
ccc     yusf = yus(1)
ccc   endif
c
 200  continue
      if (.not. backwd) then
c                   initialize values for forward trace
        kb = kf +lv
        lb = lf -kv
        zb = zblk(kb,lb)
        if (zb .lt. hc) then
c                      turn right
          za  =  zb
          klt =  kv
          kv  =  lv
          lv  = -klt
c
        else
          kc = kf +kv +lv
          lc = lf +lv -kv
          zc = zblk(kc,lc)
          if (zc .lt. hc) then
c                        go straight ahead
            zf = zb
            za = zc
            kf = kf +lv
            lf = lf -kv
          else
c                        turn left
            zf  =  zc
            kf  =  kc
            lf  =  lc
            klt =  lv
            lv  =  kv
            kv  = -klt
          endif
        endif
c
      else
c                   initialize values for backward trace
        kb = kf -lv
        lb = lf +kv
        zb = zblk(kb,lb)
        if (zb .lt. hc) then
c                      turn left
          za  =  zb
          klt =  kv
          kv  = -lv
          lv  = klt
c
        else
          kc = kf +kv -lv
          lc = lf +kv +lv
          zc = zblk(kc,lc)
          if (zc .lt. hc) then
c                        go straight
             zf = zb
             za = zc
             kf = kf -lv
             lf = lf +kv
c
          else
c                        turn right
            zf  =  zc
            kf  =  kc
            lf  =  lc
            klt =  lv
            lv  = -kv
            kv  =  klt
          endif
        endif
      endif
c
c             interpolate for next location of contour
      t = 0.0
      if (zf .ne. za)  t = (zf -hc)/(zf -za)
      nval = nval +1
      if (nval .gt. ncnt) then
        write (lbox,*) ' isotrc, aborting - too many one block points'
        nc1 = 0
        nc2 = 0
        goto 300
c
      endif
      xus(nval) = mi +rint*((kf -1) +t*kv)
      yus(nval) = nj +sint*((lf -1) +t*lv)
c
c              check to see if edge of zoomed block has been reached
c
      if (lv .eq. 0) then
        if (lf .gt. 1 .and. lf .lt. lzlt) goto 200
c
      else
        if (kf .gt. 1 .and. kf .lt. kzlt) goto 200
c
      endif
 210  continue
c
c                   determine if contour is finished and
c                   if contouring continuing,
c                   location of next block to be zoomed.
c
      if (.not.backwd) then
c
c                   setup forward contouring values
c
        if (kv .eq. -1) then
          njp = nj +1
          if (njp .ge. maxj) then
            last = .true.
          else
            nj = njp
            lf = 1
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi+1,nj)) = .false.
c
c                   determine if closed contour is finished
c
ccc         if (.not.open .and. mi.eq.mif .and. nj.eq.njf) then
ccc           last      = .true.
ccc           nval      = nval +1
ccc           xus(nval) = xusf
ccc           yus(nval) = yusf
ccc         endif
          endif
        elseif (lv .eq. -1) then
          mim = mi -1
          if (mim .lt. mini) then
            last = .true.
          else
            mi = mim
            kf = kzlt
          endif
        elseif (kv .eq. 1) then
          njm = nj -1
          if (njm .lt. minj) then
            last = .true.
          else
            lf = lzlt
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi,nj)) = .false.
            nj = njm
          endif
        elseif (lv .eq. 1) then
          mip = mi +1
          if (mip .ge. maxi) then
            last = .true.
          else
            mi = mip
            kf = 1
          endif
        endif
c
      else
c                   setup backward contouring values
        if (kv .eq. 1) then
          njp = nj +1
          if (njp .ge. maxj) then
            last = .true.
          else
            nj = njp
            lf = 1
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi,nj)) = .false.
c
c                   determine if closed contour is finished
c
ccc         if (.not.open .and. mi.eq.mif .and. nj.eq.njf) then
ccc           last      = .true.
ccc           nval      = nval +1
ccc           xus(nval) = xusf
ccc           yus(nval) = yusf
ccc         endif
          endif
        elseif (lv .eq. 1) then
          mim = mi -1
          if (mim .lt. mini) then
            last = .true.
          else
            mi = mim
            kf = kzlt
          endif
        elseif (kv .eq. -1) then
          njm = nj -1
          if (njm .lt. minj) then
            last = .true.
          else
            nj = njm
            lf = lzlt
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi+1,nj+1)) = .false.
          endif
        elseif (lv .eq. -1) then
          mip = mi +1
          if (mip .ge. maxi) then
            last = .true.
          else
            mi = mip
            kf = 1
          endif
        endif
      endif
c
c                   output contour points for one block
c
      write (lbox,*) 'isotrc, nval ',nval,' ncnt ',ncnt,' last ',last
      if (first) then
        nn     = 0
        nxylmt = 0
      endif
      do n=1, nval
        if (xus(n) .ge. xs .and. xus(n) .le. xl .and. yus(n) .ge. ys
     &     .and. yus(n).le.yl) then
          if (iter .eq. 1) then
            if (nn .eq. 0) then
              nn     = 1
              xx1(1) = xus(n)
              yy1(1) = yus(n)
            else
              if (xus(n) .ne. xx1(nn) .and. yus(n) .ne. yy1(nn)) then
                nn = nn +1
                if (nn .le. npts) then
                  xx1(nn) = xus(n)
                  yy1(nn) = yus(n)
                else
                  nxylmt = -1
                endif
              endif
            endif
          else
            if (nn .eq. 0) then
              nn     = 1
              xx2(1) = xus(n)
              yy2(1) = yus(n)
            else
              if (xus(n).ne.xx2(nn) .and. yus(n).ne.yy2(nn)) then
                nn = nn +1
                if (nn .le. npts) then
                  xx2(nn) = xus(n)
                  yy2(nn) = yus(n)
                else
                  nxylmt = -1
                endif
              endif
            endif
          endif
        endif
      enddo
      first = .false.
      nval  = 0
      if (nxylmt .lt. 0) then
        write (33,*) ' $$$$ isotrc, too many total pts ',nn
        last = .true.
      endif
 240  continue
      if (last) then
        if (iter .eq. 1) then
          nxy1 = min0 (nn,npts)
          nc1  = nxy1
          rh1  = rh
          kkk  = kkk +1
        else
          nxy2 = min0 (nn,npts)
          nc2  = nxy2
          rh2  = rh
          kkk  = kkk +1
          if (nxy1 .gt. 1 .and. nxy2 .gt. 1) then
            call calint
          else
            write (33,*) ' isotrc, no calint for ',rh1,'  ',rh2
            nc2 = 0
          endif
        endif
      else
c                   zoom grid into zblk
        call isovzm (sfld,zblk,ierr)
c                   jump to continue isogon
        if (ierr .eq. 0) goto 200
c
        write (33,*) ' $$$ isotrc, mi ',mi,' nj ',nj,
     &               ' driven out of bounds'                                                          XXXXX
        last = .true.
        goto 240
c
      endif
 300  continue
c
      end
      subroutine isovzm (bfld,zblk,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  isovzm
c
c  DESCRIPTION:  zoom grid square into block of interpoalted values,
c                no interpolation on edges (it is not required)
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call isovzm (bfld,zblk,ierr)
c
c  PARAMETERS:
c     NAME         TYPE      USAGE             DESCRIPTION
c   --------      ------     -----    ----------------------------------
c     bfld         real        in     base field
c     zblk         real       out     zoomed block of data
c     ierr          int       out     error flag, 0 no error
c
c  COMMON BLOCKS:
c
c      BLOCK      NAME     TYPE    USAGE              NOTES
c     --------  --------   ----    ------   ------------------------
c     zoomv       kzlt      int     in    first  dim of zoomed block
c                 lzlt      int     in    second dim of zoomed block
c                   mi      int     in    starting minimum first dim of
c                                         contouring block
c                   mz      int     in    first dimension of sfld
c                   nj      int     in    starting minimum second dim of
c                                         contouring block
c                   nz      int     in    second dimension of sfld
c                 rint     real     in    first dim resolution of zoomed
c                                         block
c                 sint     real     in    second dim resolution of
c                                         zoomed block
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     request interpolation    output diagnostic and return error flag
c     in edges of base field
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c              a     real       interpoation factors
c             ar     real       interpoation factor
c              b     real       interpolation factors
c             br     real       interpolation factor
c              c     real       interpolation factors
c             cr     real       interpolation factor
c            ecv     real       first set of interpolated values
c          ec3m1     real       interpolation factor
c          ec3m2     real       interpolation factor
c          ec4m2     real       interpolation factor
c           efld     real       environment base field values
c          er3m1     real       interpolation factor
c          er3m2     real       interpolation factor
c          er4m2     real       interpolation factor
c            im       int       starting first  dim grid point
c            jn       int       starting second dim grid point
c             r      real       first  dimension index of block
c             s      real       second dimension index of block
c
c  METHOD:  Apply Ayres' central difference formula in two dimensions
c
c  INCLUDE FILES:
c             NAME              DESCRIPTION
c          ----------     ----------------------------------------------
c          zoomv.inc      common block
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      include 'zoomv.inc'
c
c         formal parameters
      integer ierr
      real bfld(mz,nz), zblk(kzlt,lzlt)
c
c         local variables
      integer im, jn, k, n, m, i, l
      real ar, br, cr, r, s
      real er3m1, er3m2, er4m2, ec3m1, ec3m2, ec4m2
      real efld(16), a(4), b(4), c(4), ecv(4)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      im = mi
      jn = nj
c
c                  check that lower left hand point is an interior point
c
      if (im .ge. 2 .and. im .lt. mz-1 .and. jn .ge. 2 .and. jn .lt.
     &   nz-1) then
c
c                   load 4-by-4 array, efld, for interpolation
c
        k = 0
        do n=jn-1, jn+2, 1
          do m=im-1, im+2, 1
            k = k +1
            efld(k) = bfld(m,n)
          enddo
        enddo
c
c                   load four corners of zblk
c
          zblk(1,1)       = efld(6)
          zblk(kzlt,1)    = efld(7)
          zblk(1,lzlt)    = efld(10)
          zblk(kzlt,lzlt) = efld(11)
c
          if (kzlt .gt. 2 .or. lzlt .gt. 2) then
c
c                   perform interpolation of efld block to load zblk
c
            do i=1, 4
              er3m1 = efld(8+i) -efld(i)
              er3m2 = efld(8+i) -efld(4+i)
              er4m2 = 0.5*(efld(12+i) -efld(4+i))
              a(i)  = 0.5*er3m1
              b(i)  = 3.0*er3m2 -er3m1 -er4m2
              c(i)  = a(i) +er4m2 -er3m2 -er3m2
            enddo
c
            s = -sint
            do l=1, lzlt
              s = s +sint
              do i=1, 4
                ecv(i) = efld(4+i) +s*(a(i) +s*(b(i) +s*c(i)))
              enddo
c
              ec3m1 = ecv(3) -ecv(1)
              ec3m2 = ecv(3) -ecv(2)
              ec4m2 = 0.5*(ecv(4) -ecv(2))
              ar    = 0.5*ec3m1
              br    = 3.0*ec3m2 -ec3m1 -ec4m2
              cr    = ar +ec4m2 -ec3m2 -ec3m2
              r     = -rint
              do k=1, kzlt
                r = r +rint
c
c                   if (true) fill block with interpolated values
c
                if ((l.ne.1 .and. l.ne.lzlt) .or. (k.ne.1 .and.
     &            k.ne.kzlt)) zblk(k,l) = ecv(2) +r*(ar +r*(br +r*cr))
              enddo
            enddo
          endif
          ierr = 0
      else
c
c                   no edge interpolation allowed in this version,
c                   so set ierr to error value.
c
         ierr = -1
         write (*,*) '$$$$$ warning:  error return in isovzm  $$$$$'
      endif
c
      end
      subroutine lodtrkd (numv,mxf,ntc,tcyc,gdat,tcdat,kont,cycid,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  LODTRKD
c
c  DESCRIPTION:  PROCESS NOGAPS TROPICAL CYCLONE TRACKING DATA TO LOAD
c                DATA ARRAYS FOR OBTAINING ASSOCIATED DATA
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:
c
c  CLASSIFICATION:  UNCLASSIFIED
c
c  RESTRICTIONS:
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  CALL PRCTCTD (NUMV,MXF,NTC,TCYC,GDAT,TCDAT,KONT,CYCID,IERR)
c
c  PARAMETERS:
c     NAME        TYPE     USAGE             DESCRIPTION
c   --------      ----     -----     ----------------------------------
c     NUMV         INT      IN       FIRST  DIMENSION OF GDAT
c     MXF          INT      IN       SECOND DIMENSION OF GDAT
c     NTC          INT      IN       THIRD DIMENSION OF GDAT
c     TCYC        CHAR      IN       ORIGINAL BOGUS DATA
c     GDAT        REAL      IN       TRACKING DATA ARRAY
c    TCDAT        CHAR      OUT      ADDITIONAL TRACKING DATA ARRAY
c     KONT         INT      OUT      ARRAY OF MAXIMUM FORECASTS
c    CYCID        CHAR      OUT      T. C. NUMBER AND ORGIN BASIN FLAG
c     IERR         INT      OUT      ERROR FLAG, 0 - NO ERROR
c
c  COMMON BLOCKS:  NONE
c
c  FILES:  NONE
c
c  DATA BASES:  NONE
c
c  NON-FILE INPUT/OUTPUT:  NONE
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     BAD DATA                 DIAGNOSTIC, SET ERROR FLAG
c
c  ADDITIONAL COMMENTS:
c       FORMAT OF TROPICAL CYCLONE TRACKING DATA FILE
c         FIRST LINE
c                  1         2
c         12345678901234567890
c          NNN YYYYMMDDHH
c
c         BOGUS DATA
c                  1         2
c         1234567890123456789012345
c          NNB LAT   LON   HEAD SPD
c          37W 101N 1501E  2827 091
c
c         FORECAST DATA
c                  1         2         3         4
c         1234567890123456789012345678901234567890
c          TAU NNB -LATI  LONGI  HEAD   SPD  K J I                 lt,ln
c          *** 37W  10.1  150.1  282.7   9.1 0 0 0 - BOGUS LINE  (-SH,E)
c          000 37W  10.1  150.5  282.7   9.1 2 4 8 - TAU ZERO
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  NONE
c
c  LOCAL VARIABLES:
c        NAME      TYPE                 DESCRIPTION
c       ------     ----       ------------------------------------------
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  NONE
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:  STANDARD FNMOC OPERATIONAL
c
c  MAKEFILE:  N/A
c
c  RECORD OF CHANGES:
c
c    <<change notice>>  V1.1  (14 MAY 1997)  Hamilton, H.
c      initial installation on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         FORMAL PARAMETERS
      integer  numv, mxf, ntc, ierr
      integer  kont(ntc)
      character*3  cycid(9)
      character*24 tcyc(ntc)
      real tcdat(2,mxf,ntc)
      real gdat(numv,0:mxf,ntc)
c
c         LOCAL VARIABLES
      integer  n, k
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write(*,*) 'LODTRKD, numv ',numv,'  mxf ',mxf,'  ntc ',ntc
      cycid = ' '
      tcdat = 0.0
      ierr  = -1
      kont  =  0
      do n=1, ntc
        if (gdat(1,1,n) .lt. 90.0) cycid(n) = tcyc(n)(1:3)
        do k=1, mxf
          if (gdat(1,k,n) .lt. 90.0) then
            kont(n) = k                      ! max TAU index
            tcdat(1,k,n) = gdat(3,k,n)
            tcdat(2,k,n) = gdat(4,k,n)
          else
            tcdat(1,k,n) = -99.9
            tcdat(2,k,n) = -99.9
          endif
        enddo
        ierr = 0
        write (33,*) ' kont ',n,' is ',kont(n),' for ',cycid(n)
        write (*,*)  ' kont ',n,' is ',kont(n),' for ',cycid(n)
      enddo
c
      end
      subroutine numchk (card,ks,kt,nnum)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  numchk
c
c  DESCRIPTION:  check that characters between ks-1 and kt+1 are all
c                numbers or number(s) and blank(s)
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call numchk (card,ks,kt,nnum)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     card         char         in      character string
c     ks            int         in      starting character for checking
c     kt            int         in      ending character for checking
c     nnum          int         out     number of digits or number of
c                                       digits and blanks
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          cx        char       working character
c          nblk       int       count of blanks
c          js         int       starting character position
c          jt         int       ending character position
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer ks, kt, nnum
      character*24 card
c
c         local variables
      integer nblk, js, jt, j
      character*1 cx
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nnum = 0
      nblk = 0
c                   validate starting and ending positions
      js = max0 (ks,1)
      jt = min0 (kt,24)
      do j=js, jt
        cx = card(j:j)
        if (cx .ge. '0' .and. cx .le. '9') then
          nnum = nnum +1
        elseif (cx .eq. ' ') then
          nblk = nblk +1
        endif
      enddo
      if (nblk .gt. 0 .and. nnum .ge. 1) nnum = nnum +nblk
      return
c
      end
      subroutine outgdat (nwrt,tcyc,gdat,numv,mxhr,nbog,mxfct,ntrk)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  outgdat
c
c  DESCRIPTION:  output tracking data
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call outgdat (nwrt,tcyc,gdat,numv,mxhr,nbog,mxfct,ntrk)
c
c  PARAMETERS:
c     NAME        TYPE        USAGE             DESCRIPTION
c   --------     -------      ------   ------------------------------
c     nwrt        int           in     output unit number
c     tcyc        char          in     initial bogus values array
c     gdat        real          in     tracking data array
c     numv        int           in     first dimension of gdat,
c                                      number of values in each set
c     mxhr        int           in     second dimension of gdat,
c                                      number of tracking positions
c     nbog        int           in     third dimension of gdat,
c                                      number of cyclones tracked
c     mxfct       int           in     max forecast index in tracking
c     ntrk        int           in     number of cyclones being tracked
c                                      when tracking terminated
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c     contents of gdat array:
c        first index  1 - latitude, deg (+NH, -SH)
c                     2 - longitude, deg (0 - 360 EAST)
c                     3 - first  dimension grid location
c                     4 - second dimension grid location
c                     5 - heading, deg
c                     6 - distance traveled last 6 hours, nm
c                     7 - confidence factor
c                           0.0 - not rated
c                           1.0 - only one cyclone in area
c      ******  all the following have 2 or more cyclones in search area  *****
c                           2.0 - cyclone selected is closest to both ep
c                                 and has the higher wind speed
c                           3.0 - cyclone selected is closest to either ep or
c                                 lkl with good wind support and speed
c                           4.0 - cyclone selected is closest to either ep or
c                                 lkl with best wind and intersection support
c                           5.0 - cyclone selected is closest to either ep or
c                                 lkl with highest wind speed
c                           6.0 - cyclone selected has highest wind speed
c                     8 - wind support factor
c                           3.0 - three quadrants
c                           4.0 - all four quadrants
c                     9 - intersection support factor
c                           2.0 thru 8.0, the larger the better
c       second index  0 - bogus position
c                     1 - analysis position
c                     2 - 6-hr position
c                     3 - 12-hr position
c                    --   --------------
c                    25 - 144-hr position
c        third index  1 - first  cyclone in bogus data file
c                     2 - second cyclone in bogus data file
c
c     example and format of output:
c                  1         2         3         4         5
c         12345678901234567890123456789012345678901234567890
c          *** 36W  25.9  158.4  285.60  11.20 0 0 0
c          000 36W  25.5  158.5  285.60  11.20 1 4 8
c          012 36W  26.2  157.6  307.89  10.67 1 4 8
c
c          tau nnb  lat    lon    head   speed k j i
c
c       where:  tau - forecast period, *** - bogus
c               nnb - cyclone number and one letter original basin code
c               lat - latitude, -SH
c               lon - 0 - 360 deg EAST
c              head - heading in degrees, last six hours
c             speed - average speed during last six hours, kt
c                 k - confidence factor of location
c                 j - wind support factor
c                 i - intersection support factor
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           k         int       second index to gdat
c           kill      int       do while control variable
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (19 JUN 1996) -- Hamilton, H.
c    Initial installation on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer numv, mxhr, nwrt, nbog, mxfct, ntrk
      character*24 tcyc(nbog)
      real gdat(numv,0:mxhr,nbog)
c
c         local variables
      integer k, kill, n, ifac, jfac, kfac
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   output data cyclone by cyclone
c
      write (*,*) 'Output tracking data'
      do n=1, nbog
        kill = 0
        k    = -1
        do while (kill .eq. 0)
          k = k +1
          if (abs (gdat(1,k,n)) .gt. 90.0) then
            gdat(2,k,n) = 999.9
            gdat(5,k,n) = 999.99
            gdat(6,k,n) =  99.99*6.0
            gdat(7,k,n) =   0.0
            gdat(8,k,n) =   0.0
            gdat(9,k,n) =   0.0
            kill = -1
          endif
          kfac = nint (gdat(7,k,n))
          jfac = nint (gdat(8,k,n))
          ifac = nint (gdat(9,k,n))
          write (*,9010) (k-1)*12,tcyc(n),gdat(1,k,n),gdat(2,k,n),
     &            gdat(5,k,n),gdat(6,k,n)/6,kfac,jfac,ifac
          write (nwrt,9010) (k-1)*12,tcyc(n),gdat(1,k,n),gdat(2,k,n),
     &            gdat(5,k,n),gdat(6,k,n)/6,kfac,jfac,ifac
          if (kill .ne. 0) then
c
c                   terminate output of cyclone when track lost
c
            write (*,9020)
            write (nwrt,9020)
          endif
c
c                   if last position output, terminate output
c
          if (k .eq. mxfct) kill = -1
        enddo
      enddo
 9010 format (1x,i3.3,1x,a4,f5.1,1x,f6.1,2x,f5.1,2x,f4.1,3(1x,i1))
 9020 format (' LOST TRACK OF CYCLONE')
      if (ntrk .eq. 0) then
c
c                 tracking was terminated because all cyclones were lost
c
        write (*,9030)
        write (nwrt,9030)
 9030   format (' LOST TRACK OF ALL CYCLONES - ABORTING')
      elseif (ntrk .eq. nbog) then
c
c                   no cyclones were lost during tracking
c
        write (*,9040)
        write (nwrt,9040)
 9040   format (' FINISHED TRACKING ALL CYCLONES')
      else
c
c                 one or more cyclone tracks were lost, but at least one
c                 cyclone was still being tracked when field data ended
c
        write (*,9050)
        write (nwrt,9050)
 9050   format (' FINISHED TRACKING CYCLONES')
      endif
c
      end
      subroutine rcalhdst (slat,slon,elat,elon,head,dist)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  rcalhdst
c
c  DESCRIPTION:  use rhumb line to calculate heading and distance from
c                slat,slon to elat,elon
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call rcalhdst (slat,slon,elat,elon,head,dist)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      slat         real         in     initial latitude
c      slon         real         in     initial longitude
c      elat         real         in     final latitude
c      elon         real         in     final longitude
c      head         real         out    heading (deg)
c      dist         real         out    distance (nm)
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           a45r     real       radians per 45 degrees
c           eln1     real       intermediate calculation factor
c           eln2     real       intermediate calculation factor
c           inil      int       set-up caculation flag
c            rad     real       degrees per radian
c           radi     real       radians per degree
c           rai2     real       radians per two degrees
c           tiny     real       small real number, hardware dependent
c             xl     real       working initial latitude
c             xn     real       working initial longitude
c             xr     real       intermediate calculation factor
c             yl     real       working final latitude
c             yn     real       working final longitude
c             yr     real       intermediate calculation factor
c
c  METHOD:  standard calculations, with near pole point corrections
c           omitted - no tropical cyclones near the poles
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (05 JUN 1996)  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (04 SEP 1996)  Hamilton, H.
c    Adjust value of tiny for OASIS computer
c    Correct IF statement for proper setting of longitude in Atlantic
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real slat, slon, elat, elon, head, dist
c
c         local variables
      integer inil
c
      real rad, radi, rdi2, a45r, tiny, xl, xn, yl, yn
      real eln1, eln2, xr, yr
c
      save inil, rad, radi, rdi2, a45r
c
      data tiny/0.1e-4/
c                   maximum poleward latitude, hardware dependent
ccc   data plmx/89.99/
      data inil/-1/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .ne.  0) then
         inil = 0
         rad  = 180.0/acos (-1.0)
         radi = 1.0/rad
         rdi2 = 0.5*radi
         a45r = 45.0*radi
      endif
c                    same point returns 0.0 head and 0.0 dist
      head = 0.0
      dist = 0.0
c                   southern hemisphere latitude is negative
      xl = slat
      yl = elat
c                   longitude is 0 -360 in degrees East or
c                             negative for West longitude
      xn = slon
      yn = elon
      if (xl .ne. yl .or. xn .ne. yn) then
c                   if longitude is west, convert to 0-360 east
        if (xn .lt. 0.0) xn = xn +360.0
c                   if longitude is west, convert to 0-360 east
        if (yn .lt. 0.0) yn = yn +360.0
c                    check for shortest angular distance
        if (xn .gt. 270.0 .and. yn .lt. 90.0) then
          yn = yn +360.0
        elseif (yn .gt. 270.0 .and. xn .lt. 90.0) then
          xn = xn +360.0
        endif
        if (abs (xl -yl) .gt. tiny) then
c                   calculate initial distance
          dist = 60.0*(xl -yl)
          if (abs (xn -yn) .gt. tiny) then
c                   check for positions poleward of 89+ degrees latitude
ccc         if (abs (xl) > plmx .or. abs (yl) > plmx) then
c              (hardware dependent - not required for tropical cyclones)
ccc           xlt = xl
ccc           if (abs (xlt) > plmx) xlt = sign (plmx,xl)
ccc           ylt = yl
ccc           if (abs (ylt) > plmx) ylt = sign (plmx,yl)
ccc           xr   = tan (xlt*rdi2 +sign (a45r,xl))
ccc           yr   = tan (ylt*rdi2 +sign (a45r,yl))
ccc         else
              xr   = tan (xl*rdi2 +sign (a45r,xl))
              yr   = tan (yl*rdi2 +sign (a45r,yl))
ccc         endif
            eln1 = sign (alog (abs (xr)),xr)
            eln2 = sign (alog (abs (yr)),yr)
            head = rad*(atan ((xn -yn)/(rad*(eln1 -eln2))))
            if (yl   .lt.   xl) head = head +180.0
            if (head .le. 0.0) head = head +360.0
            head = mod (head,360.0)
c                   correct initial distance, based only on latitiude
            dist = dist/cos (head*radi)
          else
c                  resolve 0 or 180 heading, note head is preset to zero
            if (yl .lt. xl) head = 180.0
          endif
        else
c                    resolve 90 or 270 heading
          head = 90.0
          if (yn .lt. xn) head = 270.0
          dist = 60.0*(yn -xn)*cos (xl*radi)
        endif
        dist = abs (dist)
      endif
      write (*,*) 'in rcalhdst'
      write (*,*) 'slat,slon,elat,elon,head,dist'
      write (*,*) slat,slon,elat,elon,head,dist
      return
c
      end
      subroutine rcaltln (slat,slon,head,dist,elat,elon)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c
c  MODULE NAME:  rcalltln
c
c  DESCRIPTION:  use rhumb line to calculate ending lat,lon given
c                starting lat,lon, heading and distance
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call rcaltln (slat,slon,head,dist,elat,elon)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      slat         real         in     starting latitude
c      slon         real         in     starting longitude
c      head         real         in     heading (deg)
c      dist         real         in     distance (nm)
c      elat         real         out    ending latitude
c      elon         real         out    ending longitude
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                DESCRIPTION
c         ------     ----      ----------------------------------
c           crhd     real      heading converted to radians
c         degrad     real      conversion factor, deg to radians
c           dlat     real      distance in terms of latitude
c           dlon     real      distance in terms of longitude
c         hdgrad     real      half of degrad
c           icrs      int      integer value of heading
c           inil      int      initialization flag
c         raddeg     real      conversion factor, radian to degrees
c         rad045     real      radians in 45 degrees
c           rdst     real      absolute distance, nm
c           rhed     real      local copy of heading
c           tiny     real      small number
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      real slat, slon, head, dist, elat, elon
c
c         local variables
      integer icrs, inil
      real crhd, degrad, dlat, dlon, hdgrad, raddeg, rad045, rdst, rhed
      real tiny
c
      save raddeg, degrad, hdgrad, rad045, inil
      data inil/0/
      data tiny/1.0e-3/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      if (inil .eq. 0) then
        inil   = -1
        degrad = acos (-1.0)/180.0
        hdgrad = 0.5*degrad
        rad045 = 45.0*degrad
        raddeg = 1.0/degrad
      endif
c
      rdst = abs (dist)
      if (rdst .gt. tiny) then
        rhed = head
        if (rhed .lt. 0.0) then
          rhed = rhed +360.0
        elseif (rhed .gt. 360.0) then
          rhed = rhed -360.0
        endif
        if (abs (rhed -360.0) .le. tiny) rhed = 0.0
        icrs = nint (rhed)
        if (abs (head -270.0) .le. tiny .or. abs (head  -90.0) .le.
     &    tiny) then
          dlon = rdst/(60.0*cos (slat*degrad))
c                 longitude is in degrees east, 0.0 to 360.0
          if (icrs .eq. 270) then
            elon = slon -dlon
          else
            elon = slon +dlon
          endif
          elat = slat
        elseif (abs (rhed -360.0) .le. tiny .or. abs (head -180.0) .le.
     &    tiny) then
          dlat = rdst/60.0
          if (icrs .eq. 360) then
            elat = slat +dlat
          else
            elat = slat -dlat
          endif
          elon = slon
        else
          crhd = head*degrad
          elat = slat +(rdst*cos (crhd)/60.0)
          elon = slon +raddeg*(alog (tan (rad045 +hdgrad*elat))
     &          -alog (tan (rad045 +hdgrad*slat)))*tan (crhd)
        endif
      else
        elon = slon
        elat = slat
      endif
      return
c
      end
      subroutine selcyc (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,
     &                   jygd,konf,indx)                                                       XXXXX
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  selcyc
c
c  DESCRIPTION:  driver routine for finding which tropical cyclone
c                is best prospect
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call selcyc (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,jygd,
c                       konf,indx)
c
c  PARAMETERS:
c     NAME      TYPE    USAGE           DESCRIPTION
c   --------   -------  -----   ------------------------------
c     sgxx      real     in     last known x-location of cyclone
c     sgyy      real     in     last known y-location of cyclone
c     egxx      real     in     extrapolated x-location of cyclone
c     egyy      real     in     extrapolated y-location of cyclone
c   cirdat      real     in     circulation data
c                                 (1, first  dimension location
c                                 (2, second dimension location
c                                 (3, wind support factor, 3 or 4
c                                 (4, intersection support, 2 - 8
c     nccf       int     in     number of cyclonic circulations
c    fffld      real     in     wind speed squared (m/s)**2
c     ixgd       int     in     first  dimension of fffld
c     jygd       int     in     second dimension of fffld
c     konf       int     out    confidence factor
c     indx       int     out    index to cirdat of selected cc
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c        NAME           DESCRIPTION
c       -------     ----------------------
c       sortem2     sort prospective data based upon distance from last
c                   know location and from extrapolated location, and
c                   on maximum wind speed near each cyclonic center
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          edist     real       distance from extrapolated position
c          jptsp      int       pointer array, last known location
c          kptep      int       pointer array, extrtapolated position
c          lptwd      int       pointer array, wind speed
c          sdist     real       distance from last known location
c          wind      real       maximum wind speed
c          wndmx     real       array of maximum wind speeds
c
c  METHOD:  1)  Load pointer arrays, calculate distance values, load
c               wind speed array and then sort distance arrays (least
c               to most) and wind speed array (most to least) by calling
c               sortem2.
c           2)  Based upon the information in these sorted arrays,
c               select the best index to the cyclones found to represent
c               the cyclone being tracked.  Set confidence factor to
c               represent the goodness of the selection.
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
       implicit none
c
c         formal parameters
       integer nccf, ixgd, jygd, konf, indx
       real sgxx, sgyy, egxx, egyy
       real cirdat(4,nccf), fffld(ixgd,jygd)
c
c         local variables
c               pointer arrays
       integer jptsp(nccf), kptep(nccf), lptwd(nccf)
c               distance arrays (d squared)
       real sdist(nccf), edist(nccf)
c               wind speed max at grid point near cc
       real wndmx(nccf)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c               load pointer, distance and wind speed arrays
c
       call sortem2 (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,jygd,
     &               jptsp,kptep,lptwd,sdist,edist,wndmx)
c
c               select index to cyclone location
c
       if (jptsp(1) .eq. kptep(1) .and. jptsp(1) .eq. lptwd(1)) then
c
c               pick cyclone which is minimum distance to both
c               last known location and estimated position,
c               and has max wind speed
c
         indx = jptsp(1)
         konf = 2
       elseif (sdist(jptsp(1)) .lt. edist(kptep(1)) .and.
     &         cirdat(3,jptsp(1)) .gt. 3.5 .and.
     &         cirdat(4,jptsp(1)) .gt. 4.5 .and.
     &         wndmx(jptsp(1)) .ge. wndmx(kptep(1))) then
c
c              pick cyclone closer to last known position,
c              if it has good wind support
c
         indx = jptsp(1)
         konf = 3
       elseif (edist(kptep(1)) .le. sdist(jptsp(1)) .and.
     &         cirdat(3,kptep(1)) .gt. 3.5 .and.
     &         cirdat(4,kptep(1)) .gt. 4.5 .and.
     &         wndmx(kptep(1)) .ge. wndmx(jptsp(1))) then
c
c              pick cyclone closer to estimated position,
c              if it has good wind support
c
         indx = kptep(1)
         konf = 3
       elseif (cirdat(3,jptsp(1)) .ge. cirdat(3,kptep(1)) .and.
     &         cirdat(4,jptsp(1)) .ge. cirdat(4,kptep(1)) .and.
     &         wndmx(jptsp(1)) .ge. wndmx(kptep(1))) then
c
c               pick cyclone closest to the start position,
c               if it has the best wind and intersection support
c
         indx = jptsp(1)
         konf = 4
         elseif (cirdat(3,kptep(1)) .ge. cirdat(3,jptsp(1)) .and.
     &           cirdat(4,kptep(1)) .ge. cirdat(4,jptsp(1)) .and.
     &           wndmx(kptep(1)) .ge. wndmx(jptsp(1))) then
c
c               pick cyclone closest to estimated position,
c               if it has the best wind and intersection support
c
         indx = kptep(1)
         konf = 4
       elseif (wndmx(jptsp(1)) .gt. wndmx(kptep(1))) then
c
c              pick cyclone closest to last known position,
c              if wind speed is greater
c
         indx = jptsp(1)
         konf = 5
       elseif (wndmx(kptep(1)) .gt. wndmx(jptsp(1))) then
c
c              pick cyclone closest to estimated position,
c              if wind speed is greater
c
         indx = kptep(1)
         konf = 5
       else
c
c              pick cyclone with highest wind speed
c
         indx = lptwd(1)
         konf = 6
       endif
       return
c
       end
      subroutine sfcread (nuinp,igrdx,jgrdy,sfcfld,ierr)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  flduvrd
c
c  DESCRIPTION:  routine for reading surface pressure field
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call sfcread (nuinp,igrdx,jgrdy,sfcfld,ierr)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c      nuinp        int          in     unit number to read fields
c      igrdx        int          in     first  dimension of field
c      jgrdy        int          in     second dimension of field
c     sfcfld       real         out     pressure (hPa) field
c       ierr        int         out     error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:
c     NAME          TABLE      USAGE       DESCRIPTION
c    --------     -----------  ------  --------------------
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     missing field or         set error flag to non-zero
c        read error
c
c  ADDITIONAL COMMENTS:
c    Fields must be stacked in right order, for there is no checking
c    to see if they are right.
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         calddto     calculates wind direction, towards (deg)
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         dsetnam    char       data set name
c         dsets      char       data set names
c         geonam     char       geometry name
c         idgrid      int       internal dataset identifier number
c         igrdx       int       first  dimension of fields
c         irecnum     int       internal record sequence number
c         istatus     int       status of ISIS request
c         jgrdy       int       second dimension of fields
c         params     char       parameter names
c         rlvl1      real       level 1 value
c         rlvl2      real       level 2 value
c         seclvl     char       security level
c         title      char       title of field
c         typlvl     char       type of level
c         typmodl    char       type of model
c         units      char       units of fields
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:  Fortran 90
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer nuinp, igrdx, jgrdy, ierr
      real sfcfld(igrdx,jgrdy)
c
c         local variables
      integer ioe
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   read surface pressure field
c
      read (nuinp,iostat=ioe) sfcfld
      if (ioe .eq. 0) then
        ierr = 0
      else
        ierr = -1
      endif
c
      end
      subroutine sortem2 (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,
     &                    jygd,jptsp,kptep,lptwd,sdist,edist,wndmx)
c
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  sortem2
c
c  DESCRIPTION:  sort on: 1) distance from last know location
c                         2) distance from estimated position
c                         3) wind speed
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  sortem2 (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,
c                   jygd,jptsp,kptep,lptwd,sdist,edist,wndmx)
c
c  PARAMETERS:
c     NAME         TYPE     USAGE             DESCRIPTION
c   --------      ------    -----    ------------------------------
c     sgxx         real       in     last known x-grid location
c     sgyy         real       in     last known y-grid location
c     egxx         real       in     estimated  x-grid location
c     egyy         real       in     estimated  y-grid location
c     cirdat       real       in     array of cyclonic circulation data
c                                      (1,n) appx. x-grid location
c                                      (2,n) appx. y-grid location
c                                      (3,n) circulation factor
c                                      (4,n) intersection factor
c     nccf          int       in     number of circulations
c     fffld        real       in     wind speed squared
c     ixgd          int       in     first  dimension of fffld
c     jygd          int       in     second dimension of fffld
c     jptsp         int       out    pointers for min distance from
c                                    last known location
c     kptep         int       out    pointers for min distance from
c                                    estimated position
c     lptwd         int       out    pointers for max wind speed
c     sdist        real       out    distance from last known location
c     edist        real       out    distance from estimated position
c     wndmx        real       out    maximum wind speed near center
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:  none
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c         imn         int       truncated grid position, first dimension
c         itemp       int       working temporary storage
c         jmn         int       truncated grid position, second dimension
c         dist       real       working distance storage
c         vormx      real       working vorticity storage
c         wnd1       real       wind speed, lower left corner
c         wnd2       real       wind speed, lower right corner
c         wnd3       real       wind speed, upper right corner
c         wnd4       real       wind speed, upper left corner
c         wind       real       working wind speed value
c         xdst       real       working x-distance storage
c         ydst       real       working y-distance storage
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
c    Add processing of wind speed arrays
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c     formal parameters
      integer nccf, ixgd, jygd
      integer jptsp(nccf), kptep(nccf), lptwd(nccf)
      real sgxx, sgyy, egxx, egyy
      real cirdat(4,nccf), sdist(nccf), edist(nccf), wndmx(nccf)
      real fffld(ixgd,jygd)
c
c     local variables
      integer n, j, k, itemp, imn, jmn
      real dist, xdst, ydst, wnd1, wnd2, wnd3, wnd4, wind
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c               initialize arrays
c
c                     load pointer arrays
      do n=1, nccf
        jptsp(n) = n
        kptep(n) = n
        lptwd(n) = n
      enddo
c
c                     load distance and wind max arrays
c
      do j=1, nccf
c
c               load sdist based on last known location
c
        xdst = cirdat(1,j) -sgxx
        if (abs (xdst) .gt. 180.0) then
          if (xdst .lt. 0.0) then
            xdst = 360.0 +cirdat(1,j) -sgxx
          else
            xdst = cirdat(1,j) -(sgxx +360.0)
          endif
        endif
        ydst = cirdat(2,j) - sgyy
        sdist(j) = xdst*xdst +ydst*ydst
c
c               load edist based on estimated location
c
        xdst = cirdat(1,j) -egxx
        if (abs (xdst) .gt. 180.0) then
          if (xdst .lt. 0.0) then
            xdst = 360.0 +cirdat(2,j) -egxx
          else
            xdst = cirdat(2,j) -(egxx +360.0)
          endif
        endif
        ydst = cirdat(2,j) -egyy
        edist(j) = xdst*xdst +ydst*ydst
c
c              load wndmx array
c
        imn  = cirdat(1,j)
        jmn  = cirdat(2,j)
        wnd1 = fffld(imn,jmn)
        wnd2 = fffld(imn+1,jmn)
        wnd3 = fffld(imn+1,jmn+1)
        wnd4 = fffld(imn,jmn+1)
c
c               note: fffld values are squared (m/s)
c
        wndmx(j) = sqrt (amax1 (wnd1,wnd2,wnd3,wnd4))
      enddo
c
c           adjust pointer arrays, jptsp, kptep
c
c               sort on distance from past position, min to max
c               adjust jptsp pointers
c
      do j=1, nccf-1
        dist = sdist(jptsp(j))
        do k=j+1, nccf
          if (sdist(jptsp(k)) .lt. dist) then
            itemp    = jptsp(j)
            jptsp(j) = jptsp(k)
            jptsp(k) = itemp
            dist     = sdist(jptsp(j))
          endif
        enddo
      enddo
c
c               sort on distance from estimated position, min to max
c               adjust kptep pointers
c
      do j=1, nccf-1
        dist = edist(kptep(j))
        do k=j+1, nccf
          if (edist(kptep(k)) .lt. dist) then
            itemp    = kptep(j)
            kptep(j) = kptep(k)
            kptep(k) = itemp
            dist     = edist(kptep(j))
          endif
        enddo
      enddo
c
c               sort on maximum wind speed, max to min
c               adjust lptwd pointers
c
      do j=1, nccf-1
        wind = wndmx(lptwd(j))
        do k=j+1, nccf
          if (wndmx(lptwd(k)) .gt. wind) then
            itemp    = lptwd(j)
            lptwd(j) = lptwd(k)
            lptwd(k) = itemp
            wind     = wndmx(lptwd(j))
          endif
        enddo
      enddo
c
      end
      subroutine trackem (uufld,vvfld,ixgd,jygd,ktau,gdat,numv,mxhr,
     &                    nbog,ntrk)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  trackem
c
c  DESCRIPTION:  driver to track tropical cyclones
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call trackem (ddfld,fffld,ixgd,jygd,ktau,gdat,numv,
c                        mxhr,nbog,ntrk)
c
c  PARAMETERS:
c     NAME       TYPE     USAGE           DESCRIPTION
c   --------    ------    ------    ------------------------------
c    uufld       real       in      u-wind field (m/s)
c    vvfld       real       in      v-wind field (m/s)
c     ixgd        int       in      first  dimension of ddfld
c     jygd        int       in      second dimension of ddfld
c     ktau        int       in      forecast period index
c     gdat       real     in/out    bogus data in real form / new
c                                   position data
c    numv         int       in      first dimension of gdat, number of
c                                   variables
c    mxhr         int       in      second dimension of gdat, maximum
c                                   number of forecast periods
c    nbog         int       in      third diemsnsion of gdat, number of
c                                   valid bogus positions to track
c    ntrk         int       out     number of cyclones being tracked
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c
c
c  ADDITIONAL COMMENTS:
c         contents of gdat array
c           (1,n,m) - latitude of cyclone m, +NH -SH
c           (2,n,m) - longitude of cyclone m, 0 - 360 E
c           (3,n,m) - x-grid (lon) of cyclone m
c           (4,n,m) - y-grid (lat) of cyclone m
c           (5,n,m) - heading  from last location of cyclone m, deg
c           (6,n,m) - distance from last location of cyclone m, nm
c           (7,n,m) - confidence factor of location of cyclone m
c                        0 - cyclone lost or not rated
c                        1 - excellent
c                        2 - good
c                        3 - fair
c                        4 - poor
c                        5 - poorer
c                        6 - poorest
c           (8,n,m) - cyclonic wind support, 3 or 4
c           (9,n,m) - intersection support, 2 - 9
c
c           note: n goes from 0 to mxhr,  0   is bogus position
c                                         1   analysis position
c           forecast period = (n-1)*12    2  12-hr forecast period
c                                         3  24-hr forecast period
c                                        --  - - - - - - - - - - -
c                                        14 144-hr forecast period
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         chkfcir     locate initial potential areas for cyclones
c         clltxy      convert lat,lon to x,y grid location
c         cxytll      convert x,y grid location to lat,lon
c         expand      expand to local 1-degree direction & force fields
c         fndcyc      driver routine for finding which cyclone to locate
c         selcyc      select best cyclone for each one being tracked
c         rcalhdst    calculate heading and distance from old lat,lon to
c                     new lat,lon
c         rcalltln    calculate new lat,lon, given old lat, lon, heading
c                     and distance
c         verify      locate cyclones based upon isogons
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          cirdat    real       array of cyclone values
c                                 (1 - x-grid location
c                                 (2 - y-grid location
c                                 (3 - quadrant wind support
c                                 (4 - final intersection count
c          clat      real       cyclone latitude, deg (+NH, -SH)
c          clon      real       cyclone longitude, deg (0 - 360E)
c          dist      real       distance traveled between taus (nm)
c          egxx      real       estimated grid location, first dimension
c          egyy      real       estimated grid location, second dimension
c          elat      real       estimated future latitude (degrees)
c          elon      real       estimated future longitude (degrees)
c          head      real       cyclone heading betweeb taus, (degrees)
c          ierr       int       error flag, 0 no error
c          iloc       int       cyclone location flag, 0 not found
c          indx       int       index to selected cyclone data in cirdat
c          kc         int       present second index to gdat
c          kcl        int       last second index to gdat
c          kint       int       count of intersections used to produce location
c          konf       int       confidence factor of selected cyclone
c          ltrk       int       last number of cyclones being tracked
c          maxptc     int       maximum number of prospective cyclones
c                               to process
c          mbd        int       minimum/maximum boundary of search window
c          mni        int       minimum first dimension of search window
c          mnj        int       minimum second dimension of search window
c          mxi        int       maximum first dimension of search window
c          mxj        int       maximum second dimension of search window
c          mxptc      int       working number of maximum allowed
c                               prospective cyclones to process
c          nccf       int       number of closed circulations found
c          ndup       int       duplicate cyclone indicator
c          nhsh       int       north/south hemisphere indicator
c          sgxx      real       starting grid location, first dimension
c          sgyy      real       starting grid location, second dimension
c          slat      real       starting latitude, deg
c          slon      real       starting longitude, deg
c          xc        real       x-grid location of cyclone
c          yc        real       y-grid location of cyclone
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
c    Make changes for the use of wind speed field, fffld, and allow for up to
c    four centers of intersections to be found for each prospective area
c    selected for a cyclone search.
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      integer maxptc, ixe, jye
      parameter (maxptc = 27,  ixe = 31,  jye = 31)
c
c         formal parameters:
      integer ixgd, jygd, numv, mxhr, nbog, ktau, ntrk
      real uufld(ixgd,jygd), vvfld(ixgd,jygd)
      real gdat(numv,0:mxhr,nbog)
c
c         local variables
      integer n, j, iloc, kc, kcl, nhsh, ierr, ltrk, ndup, indx
      integer mni, mxi, mnj, mxj, mxptc, nccf, konf, kint
      integer icyce, jcyce
      real cirdat(4,maxptc), slat, slon, sgxx, sgyy, head, dist
      real elat, elon, egxx, egyy, xc, yc, clat, clon
      real sgex, sgey, egex, egey
      real ddfld(ixe,jye), fffld(ixe,jye)
      integer ii,jj
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
cx  assign clat, clon so that compile warning dissapears ... bs 9/29/97
      clat =  99.9
      clon = 999.9
      mxptc = maxptc
      ntrk  = 0
      kc    = 1 +ktau/12
      kcl   = kc -1
      do n=1, nbog
        iloc = 0
        if (abs (gdat(1,kcl,n)) .lt. 90.0) then
c
c               last position is valid, so calculate extrapolated
c               location for tracking
c
          slat = gdat(1,kcl,n)
          slon = gdat(2,kcl,n)
          sgxx = gdat(3,kcl,n)
          sgyy = gdat(4,kcl,n)
          head = gdat(5,kcl,n)
          dist = gdat(6,kcl,n)
       write(*,*) 'slat',slat,'  slon',slon,'  x',sgxx,'  y',sgyy
c               use rhumb line in calculations of elat,elon
          call rcaltln (slat,slon,head,dist,elat,elon)
       write(*,*) 'head',head,'  dist',dist,'  elt',elat,'  eln',elon
c               convert to grid co-ordinates
          call clltxy (elat,elon,egxx,egyy,ierr)
          if (ierr .eq. 0) then
            icyce = 0.5 * (sgxx +egxx)
            jcyce = 0.5 * (sgyy +egyy)
	    write(*,*) 'ixgd ',ixgd,'  jygd ',jygd
	    write(*,*) 'icyce ',icyce,'  jcyce ',jcyce
	    write(*,*) 'ixe ',ixe,'  jye ',jye
            call expand (uufld,vvfld,ixgd,jygd,icyce,jcyce,
     &                   ddfld,fffld,ixe,jye)
cx	    write(*,*)' ddfld'
cx	    write(*,'(31f5.0,/)')((ddfld(ii,jj),ii=1,ixe,1),jj=jye,1,-1)
cx	    write(*,*)' fffld'
cx	    write(*,'(31f5.0,/)')((fffld(ii,jj),ii=1,31,1),jj=31,1,-1)
c
c               set hemisphere flag nhsh, + for NH and - for SH
c
            if (slat .gt. 0.0) then
              nhsh =  1
            else
              nhsh = -1
            endif
c
c               set window dimensions for searching for cyclonic
c               circulations within ddfld
c
            mni = 1
            mxi = ixe
            mnj = 1
            mxj = jye

            call chkfcir (ddfld,ixe,jye,mni,mxi,mnj,mxj,nhsh,mxptc,
     &                    cirdat,nccf)
            write(33,*) 'CHKFCIR found ',nccf,' possible cyclonic',
     &                  ' centers'
c
c               verify that all prospective cc's are wind centers
c
            call verify (nhsh,ddfld,ixe,jye,mxptc,cirdat,nccf)
            if (nccf .gt. 1) then
c
c               select best cyclonic center for cyclone
c
cx  changed   sampson dec 98
cx            sgex = 1.0 +(sgxx -icyce -6)/0.4
cx            sgey = 1.0 +(sgyy -jcyce -6)/0.4
cx            egex = 1.0 +(egxx -icyce -6)/0.4
cx            egey = 1.0 +(egyy -jcyce -6)/0.4
	      sgex = float(16)
	      sgey = float(16)
              egex = egxx-sgxx +16.
              egey = egyy-sgyy +16.

	      write (*,*) " Before selcyc **************"   
	      write (*,*) "sgxx,sgyy,egxx,egyy"
	      write (*,*)  sgxx,sgyy,egxx,egyy 
	      write (*,*) "sgex,sgey,egex,egey"
	      write (*,*) sgex,sgey,egex,egey
	      write (*,*) "cirdat"
	      write (*,*) cirdat
	      write (*,*) "ixe,jye"   
	      write (*,*)  ixe,jye    

              call selcyc (sgex,sgey,egex,egey,cirdat,nccf,fffld,ixe,
     &                     jye,konf,indx)
	      write (*,*) " After selcyc **************"   
	      write (*,*) "konf,indx"   
	      write (*,*)  konf,indx    
            elseif (nccf .eq. 1) then
              konf = 1
              indx = 1
            else
              indx = 0
            endif
            if (indx .gt. 0) then
cx            xc   = float (icyce -6) +0.4*(cirdat(1,indx) -1.0)
cx            yc   = float (jcyce -6) +0.4*(cirdat(2,indx) -1.0)
              xc   = float (icyce -15) + (cirdat(1,indx) -1.0)
              yc   = float (jcyce -15) + (cirdat(2,indx) -1.0)
              iloc = nint (cirdat(3,indx))
              kint = nint (cirdat(4,indx))
            else
              iloc = 0
              konf = 0
            endif
            if (iloc .gt. 0) then
c
c               cyclone found, convert grid co-ordinates to lat,lon
c
              write (33,*) 'TRACKEM, center found at ',xc,'  ',yc
              if (konf .gt. 1) then
c
c               check for duplicate positions
c
                j    = 0
                ndup = 0
                do while (j.lt.n-1 .and. ndup.eq.0)
                  j = j +1
                  if (abs (gdat(1,kc,j)) .lt. 90.0) then
c                     valid values for comparision
                    if (abs (gdat(3,kc,j) -xc) .le. 1.0) then
                      if (abs (gdat(4,kc,j) -yc) .le. 1.0) then
c                           duplicate found
                        ndup = -1
                      endif
                    endif
                  endif
                enddo
                if (ndup .ne. 0) then
c
c                       duplicate found from above
c
                  write (33,*) ' trackem, duplicate position found!!!'
                  if (nint (gdat(7,kc,j)) .lt. konf) then
c                     this will drop this new position
                    iloc = 0
                  elseif (nint (gdat(7,kc,j)) .gt. konf) then
c                     replace old position with missing values
                    gdat(1,kc,j) =  99.9
                    gdat(2,kc,j) = 999.9
                    gdat(3,kc,j) = -99.9
                    gdat(4,kc,j) = -99.9
                    gdat(5,kc,j) = 999.99
                    gdat(6,kc,j) =  99.99*6.0
                    gdat(7,kc,j) =   0.0
                    gdat(8,kc,j) =   0.0
                    gdat(9,kc,j) =   0.0
                    ntrk         = ntrk -1
                  else
                    write (33,*) ' trackem, duplicate position not ',
     &                           'resolved'
                  endif
                endif
              endif
              if (iloc .gt. 0) then
c                 obtain latitude and longitude
                call cxytll (xc,yc,clat,clon,ierr)
                if (ierr .eq. 0) then
c                 sum cyclones to be tracked next
                  ntrk = ntrk +1
                else
c                 bad conversion, so indicate cyclone not found
c                       (this should not happen)
                  iloc = 0
                  write (33,*) 'BAD CONVERSION for ',xc,'  ',yc
                endif
              endif
            endif
          endif
        else
          mni = -1
          mxi =  0
          mnj = -1
          mxj =  0
        endif
        if (iloc .eq. 0) then
c
c               cyclone not found, so set values to missing
c
          clat =  99.9
          clon = 999.9
          xc   = -99.9
          yc   = -99.9
          write (33,*) 'NO CYCLONE ',mni,' to ',mxi,' fm ',mnj,' to ',
     &                  mxj
        endif
c
c               load new position values
c
        gdat(1,kc,n) = clat
        gdat(2,kc,n) = clon
        gdat(3,kc,n) = xc
        gdat(4,kc,n) = yc
        if (iloc .gt. 0) then
c               load confidence factor of cyclone location, 1 - 3
          gdat(7,kc,n) = konf
c               load wind support, 3 or 4
          gdat(8,kc,n) = iloc
c               load intersection support, 2 - 8
          gdat(9,kc,n) = kint
        else
          gdat(5,kc,n) = 999.99
          gdat(6,kc,n) =  99.99*6.0
          gdat(7,kc,n) = 0.0
          gdat(8,kc,n) = 0.0
          gdat(9,kc,n) = 0.0
        endif
        if (kcl .ne. 0 .and. clat .lt. 90.0) then
c
c               calculate heading and distance from last location
c               to new location, use rhumb line
c
          call rcalhdst (slat,slon,clat,clon,head,dist)
          gdat(5,kc,n) = head
          gdat(6,kc,n) = dist
        elseif (kcl .eq. 0) then
c
c               transfer initial heading and distance
c
          gdat(5,kc,n)  = gdat(5,kcl,n)
          gdat(6,kc,n)  = gdat(6,kcl,n)
          gdat(7,kcl,n) = 0.0
          gdat(8,kcl,n) = 0.0
          gdat(9,kcl,n) = 0.0
        endif
      enddo
c
c             load ltrk with number of cyclones still being tracked
c
      ltrk = ntrk
      return
c
      end
      subroutine uatrack (nf,nt,tcdat,ixg,jyg,uufld,vvfld,lev,kf,nc,
     &                    suadat)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  uatrack
c
c  DESCRIPTION:  driver to track tropical cyclone in U/A
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:  Sun/Solaris
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call uatrack (tcdat,nf,nt,ixg,jyg,uufld,vvfld,lev,kf,nc,suadat)
c
c  PARAMETERS:
c     NAME       TYPE     USAGE           DESCRIPTION
c   --------    ------    ------    ------------------------------
c    nf          int        in      max number of forecasts
c    nt          int        in      total number of cyclones
c    tcdat       real       in      tracking data for 1000 hPa
c    ixg         int        in      first  dimension of fields
c    jyg         int        in      second dimension of fields
c    uufld       real       in      u-wind field
c    vvfld       real       in      v-wind field
c    lev         int        in      level indicator
c                                   2 - 850,  3 - 700,  4 - 500
c    kf          int        in      index to tau being processed
c    nc          int        in      cyclone being processed
c    suadat      real       out     additional data, cycone positions at lev
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c
c
c
c
c  ADDITIONAL COMMENTS:
c         contents of suadat array
c           (1,k,n) - surface pressure (hPa)
c           (2,k,n) - x-grid (lon) of cyclone n, for time k, at 850
c           (3,k,n) - y-grid (lat) of cyclone n, for time k, at 850
c           (4,k,n) - x-grid (lon) of cyclone n, for time k, at 700
c           (5,k,n) - y-grid (lat) of cyclone n, for time k, at 700
c           (6,k,n) - x-grid (lon) of cyclone n, for time k, at 500
c           (7,k,n) - y-grid (lat) of cyclone n, for time k, at 500
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         chkfcir     locate initial potential areas for cyclones
c         clltxy      convert lat,lon to x,y grid location
c         cxytll      convert x,y grid location to lat,lon
c         expand      expand to local 1-degree direction & force fields
c         fndcyc      driver routine for finding which cyclone to locate
c         selcyc      select best cyclone for each one being tracked
c         verify      locate cyclones based upon isogons
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          cirdat    real       array of cyclone values
c                                 (1 - x-grid location
c                                 (2 - y-grid location
c                                 (3 - quadrant wind support
c                                 (4 - final intersection count
c          dist      real       distance traveled between taus (nm)
c          egxx      real       estimated grid location, first dimension
c          egyy      real       estimated grid location, second dimension
c          ierr       int       error flag, 0 no error
c          iloc       int       cyclone location flag, 0 not found
c          indx       int       index to selected cyclone data in cirdat
c          konf       int       confidence factor of selected cyclone
c          maxptc     int       maximum number of prospective cyclones
c                               to process
c          mbd        int       minimum/maximum boundary of search window
c          mni        int       minimum first dimension of search window
c          mnj        int       minimum second dimension of search window
c          mxi        int       maximum first dimension of search window
c          mxj        int       maximum second dimension of search window
c          mxptc      int       working number of maximum allowed
c                               prospective cyclones to process
c          nccf       int       number of closed circulations found
c          nhsh       int       north/south hemisphere indicator
c          sgxx      real       starting grid location, first dimension
c          sgyy      real       starting grid location, second dimension
c          xc        real       x-grid location of cyclone
c          yc        real       y-grid location of cyclone
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (14 MAY 1997) -- Hamilton, H.
c    Initial installation on OASIS
c
c...................END PROLOGUE.......................................
c
      implicit none
c
      integer maxptc, ixe, jye
      parameter  (maxptc = 27,  ixe = 31,  jye = 31)
c
c         formal parameters:
      integer nf, nt, ixg, jyg, lev, kf, nc
      real uufld(ixg,jyg), vvfld(ixg,jyg)
      real tcdat(2,nf,nt), suadat(7,nf,nt)
c
c         local variables
      integer  iloc, nhsh, indx
      integer  m, mni, mxi, mnj, mxj, mxptc, nccf, konf
      integer  j1, j2, x1, x2, y1, y2, d1, d2
      integer  icyce, jcyce
      real     sgxx, sgyy
      real     egxx, egyy, xc, yc
      real     sgex, sgey, egex, egey
      real     cirdat(4,maxptc)
      real     ddfld(ixe,jye), fffld(ixe,jye)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write (33,*) 'uatrck, mxf ',nf,'  mxt ',nt,'  kf ',kf,' lev ',lev
c
      cirdat =   0.0
      mxptc  = maxptc
      xc     = -99.9
      yc     = -99.9
      j1     = 2*lev -2
      j2     = j1 +1
      iloc   = 0
      if (tcdat(2,kf,nc) .gt. 0.0) then
c
c         1000 hPa position is valid, try to find cyclone for this level (lev)
c
        egxx = tcdat(1,kf,nc)
        egyy = tcdat(2,kf,nc)
        sgxx = egxx
        sgyy = egyy
        if (kf .gt. 1) then
c
c               load past position, if valid
c
          if (suadat(j1,kf-1,nc) .gt. 0.0) then
            sgxx = suadat(j1,kf-1,nc)
            sgyy = suadat(j2,kf-1,nc)
          endif
        endif
        write(33,*) 'ex ',egxx,' ey ',egyy,'  sx ',sgxx,' sy ',sgyy
        icyce = 0.5 * (sgxx +egxx)
        jcyce = 0.5 * (sgyy +egyy)
	write(33,*) 'icyce ',icyce,'  jcyce ',jcyce
        call expand (uufld,vvfld,ixg,jyg,icyce,jcyce,
     &               ddfld,fffld,ixe,jye)
c
c               set hemisphere flag nhsh, + for NH and - for SH
c
        nhsh = ifix (egyy) -jyg/2
        if (nhsh .gt. 0) then
          nhsh =  1
        else
          nhsh = -1
         endif
c
c               set window dimensions for searching for cyclonic
c               circulations within ddfld
c
        mni = 1
        mxi = ixe
        mnj = 1
        mxj = jye
c
c               locate possible cyclonic circulation(s) within window
c
        call chkfcir (ddfld,ixe,jye,mni,mxi,mnj,mxj,nhsh,mxptc,cirdat,
     &                nccf)
        write (33,*) 'uatrack, chkfcir found ',nccf,' possible ',
     &               'cyclonic centers'
c
c               verify which prospective cc's are wind centers
c
        write (33,*) 'CALL verify...'
        if (nccf .gt. 0) call verify (nhsh,ddfld,ixe,jye,mxptc,cirdat,
     &                                nccf)
        write (33,*) 'BACK verify...'
        write (*,*) 'uatrack, verified ',nccf,' circulations'
        if (nccf .eq. 1) then
          konf = 1
          indx = 1
        elseif (nccf .gt. 1) then
c
c                select best cyclonic center for cyclone
c
cx  changed   sampson dec 98
cx        sgex = 1.0 +(sgxx -icyce -6)/0.4
cx        sgey = 1.0 +(sgyy -jcyce -6)/0.4
cx        egex = 1.0 +(egxx -icyce -6)/0.4
cx        egey = 1.0 +(egyy -jcyce -6)/0.4
	  sgex = float(16)
	  sgey = float(16)
          egex = egxx-sgxx +16.
          egey = egyy-sgyy +16.
          call selcyc (sgex,sgey,egex,egey,cirdat,nccf,fffld,ixe,jye,
     &                 konf,indx)
        else
          indx = 0
        endif
        if (indx .gt. 0) then
cx        xc   = float (icyce -6) +0.4*(cirdat(1,indx) -1.0)
cx        yc   = float (jcyce -6) +0.4*(cirdat(2,indx) -1.0)
          xc   = float (icyce -15) +(cirdat(1,indx) -1.0)
          yc   = float (jcyce -15) +(cirdat(2,indx) -1.0)
          iloc = nint (cirdat(3,indx))
c         kint = nint (cirdat(4,indx))
        else
          iloc = 0
          konf = 0
        endif
        if (iloc .gt. 0) then
c
c               found a cyclone position
c
          if (konf .gt. 1) then
c
c               check for duplicate positions
c
            write (33,*) 'DUPLICATION found...'
            do m=1, nc-1
              if (suadat(j1,kf,m) .gt. 0.0) then
c                     have valid prior location for comparision
                if (abs (suadat(j1,kf,m) -xc) .le. 1.0) then
                  if (abs (suadat(j2,kf,m) -yc) .le. 1.0) then
c                           duplicate cyclone position found
                    x1 = suadat(j1,kf,m) -tcdat(1,kf,m)
                    y1 = suadat(j2,kf,m) -tcdat(2,kf,m)
                    d1 = x1*x1 +y1*y1
                    x2 = xc -tcdat(1,kf,nc)
                    y2 = yc -tcdat(2,kf,nc)
                    d2 = x2*x2 +y2*y2
                    if (d1 .le. d2) then
                      xc = -99.9
                      yc = -99.9
                    else
                      suadat(j1,kf,m) = -99.9
                      suadat(j2,kf,m) = -99.9
                    endif
                    exit
c
                  endif
                endif
              endif
            enddo
          endif
        endif
      endif
c
c               load new position values
c
      suadat(j1,kf,nc) = xc
      suadat(j2,kf,nc) = yc
      write(33,*) 'Cyclone ',nc,' for lev ',lev,' located at ',xc,'  ',
     &             yc
c
      end
      subroutine valinp (tcyc,nbog,iok)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  valinp
c
c  DESCRIPTION:  validate input in tcyc array
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call valinp (tcyc,nbog,iok)
c
c  PARAMETERS:
c     NAME        TYPE     USAGE           DESCRIPTION
c   --------     ------    -----    ------------------------------
c     tcyc        real    in/out   bogus data values
c     nbog         int    in/out   number of tropical cyclones
c     iok          int    out       "ok" value
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c     bad data                 mark, and then omit in count
c
c  ADDITIONAL COMMENTS:
c         contents of bogus data in tcyc:
c                  1         2
c         123456789012345678901234
c         12W 123N 1234E  1234 123
c          A   B     C      D   E
c         where:
c         A - cyclone number and original basin identification
c         B - latitude  times 10, with hemipshere indicator
c         C - longitude times 10, with hemipshere indicator
c         D - forecast direction times 10, degrees (toward)
c         E - forecast speed times 10, knots
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         numchk      validate digits are digits
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          ih         int       heading*10, deg
c          iok        int       good/bad flag
c          is         int       speed*10, kt
c          kg         int       count of good bogus
c          ks         int       starting character position
c          kt         int       ending character position
c          nnum       int       number of digits in number
c          no         int       cyclone number
c          ln         int       longitude*10, deg
c          lt         int       latitude*10,  deg
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<change notice>>  V1.1  (17 JUN 1996)  --  Hamilton, H.
c    initial installation on OASIS
c
c  <<change notice>>  V1.2  (09 APR 1997)  --  Hamilton, H.
c    increase allowed cyclones to 79 and add 90 series cyclones
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer nbog, iok
      character*24 tcyc(nbog)
c
c         local variables
      integer  n, ks, kt, nnum, no, lt, ln, ih, is
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      n   = nbog
      iok = 0
      if ((tcyc(n)(8:8) .eq. 'N'   .or. tcyc(n)(8:8) .eq. 'S') .and.
     &    (tcyc(n)(14:14) .eq. 'E' .or. tcyc(n)(14:14) .eq. 'W')) then
        ks = 1
        kt = 2
        call numchk (tcyc(n),ks,kt,nnum)
        if (nnum .eq. 2) then
          ks = 5
          kt = 7
          call numchk (tcyc(n),ks,kt,nnum)
          if (nnum .eq. 3) then
            ks = 10
            kt = 13
            call numchk (tcyc(n),ks,kt,nnum)
            if (nnum .eq. 4) then
              ks = 17
              kt = 20
              call numchk (tcyc(n),ks,kt,nnum)
              if (nnum .eq. 4) then
                ks = 22
                kt = 24
                call numchk (tcyc(n),ks,kt,nnum)
                if (nnum .eq. 3) then
                  iok = -1             ! set to good
                else
                  write (33,*) 'Bad bogus speed ',tcyc(n)(22:24)
                endif
              else
                write (33,*) 'Bad bogus heading ',tcyc(n)(17:20)
              endif
            else
              write (33,*) 'Bad bogus longitude ',tcyc(n)(10:13)
            endif
          else
            write (33,*) 'Bad bogus latitude ',tcyc(n)(5:7)
          endif
        else
          write (33,*) 'Bad bogus storm number ',tcyc(n)(1:2)
        endif
      else
        write (33,*) 'Bad bogus: ',tcyc(n)(1:24)
      endif
      if (iok .eq. -1) then
c
c                   check range of values
c
        read (tcyc(n),'(i2,2x,i3,2x,i4,3x,i4,1x,i3)') no,lt,ln,ih,is
        iok = 0
cx changed ... bs   cyclone number must be within 01 to 79 or 90 to 99
cx      if (no .gt.   0 .and. no .le. 79) iok = 1
c                   cyclone number must be within 01 to 99
        if (no .gt.   0 .and. no .le. 99) iok = 1
c                   latitude check (10*deg)
        if (lt .gt. 0 .and. lt .lt. 600)  iok = iok +1
c                   longitude check (10*deg)
        if (ln .ge. 0 .and. ln .le. 1800) iok = iok +1
c                   heading check (deg)
        if (ih .ge. 0 .and. ih .le. 3600) iok = iok +1
c                   speed check (kts)
        if (is .ge. 0 .and. is .le. 600)  iok = iok +1
        if (iok .eq. 5) then
c
c                   good data in tropical cyclone bogus
c
          iok = 0
        else
          write (33,*) 'Bad bogus: ',tcyc(n)
          tcyc(n) = ' '
	  iok = -1
        endif
      endif
      return
c
      end
      subroutine verify (nhsh,ddfld,ixgd,jygd,mxptc,cirdat,nccf)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  verify
c
c  DESCRIPTION:  driver to track tropical cyclones
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call verify (nhsh,ddfld,ixgd,jygd,mxptc,cirdat,nccf)
c
c  PARAMETERS:
c     NAME       TYPE     USAGE           DESCRIPTION
c   --------    ------    ------    ------------------------------
c     nhsh        int       in      hemisphere flag, +NH, - SH
c    ddfld       real       in      wind direction field, deg
c     ixgd        int       in      first  dimension of ddfld
c     jygd        int       in      second dimension of ddfld
c   cirdat       real     in/out    circulation data
c                                     (1, first  dimension location
c                                     (2, second dimension location
c                                     (3, wind support factor, 3 or 4
c                                     (4, intersection support, 2 - 8
c     nccf        int     in/out    number of prospective cc's/
c                                   number of verified cc's
c
c  COMMON BLOCKS:  none
c
c  FILES:  none
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:  none
c
c  ADDITIONAL COMMENTS:
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         isofnd      driver routine for locating cyclone with isogons
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c          ccvdat    real       working array of cirdat
c          exc       real       estimated first  dimension location
c          eyc       real       estimated second dimension location
c          iadd       int       flag for keeping cyclone
c          iloc       int       cyclone location flag, 0 not found
c          kc         int       total count of verified cyclones
c          kccf       int       count of verified cc's per area
c          kint       int       array of intersection counts
c          kuvs       int       array of quadrant wind support counts
c          xc        real       array of x-grid location of cyclone(s)
c          yc        real       array of y-grid location of cyclone(s)
c
c  METHOD:
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
c    Initial installation
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal argumnets
      integer nhsh, ixgd, jygd, mxptc, nccf
      real ddfld(ixgd,jygd), cirdat(4,mxptc)
c
c         local variables
      integer n, k, kk, kccf, kc, iadd
      integer kuvs(4), kint(4)
      real exc, eyc, xc(4), yc(4)
      real ccvdat(2,mxptc)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write(33,*) ' verify, processing ',nccf,' areas'
      do n=1, nccf
        ccvdat(1,n) = cirdat(1,n)
        ccvdat(2,n) = cirdat(2,n)
        cirdat(1,n) = 0.0
        cirdat(2,n) = 0.0
        cirdat(3,n) = 0.0
        cirdat(4,n) = 0.0
      enddo
c
c               search for cyclonic centers based upon isogons
c
      kc = 0
      do n=1, nccf
        exc = ccvdat(1,n)
        eyc = ccvdat(2,n)
        write (33,*) 'Verify, checking ',n,' at ',exc,'  ',eyc
        call isofnd (exc,eyc,nhsh,ddfld,ixgd,jygd,kccf,kuvs,kint,xc,yc)
        if (kccf .gt. 0) then
c
c                 circulation center found with isogons
c
          write(33,*) ' isofnd found ',kccf,' cyclones for area ',n
          do k=1, kccf
            write (33,*) 'cyclone ',k,' is at ',xc(k),'  ',yc(k)
            if (kc .eq. 0) then
              kc = 1
              cirdat(1,1) = xc(k)
              cirdat(2,1) = yc(k)
              cirdat(3,1) = kuvs(k)
              cirdat(4,1) = kint(k)
            else
c
c                 do not add duplicate position
c
              iadd = -1
              do kk=1, kc
                if (abs (cirdat(1,kk) -xc(k)) .le. 0.1) then
                  if (abs (cirdat(2,kk) -yc(k)) .le. 0.1) iadd = 0
                endif
              enddo
              if (iadd .eq. -1) then
c
c                 add new cyclone location to cirdat
c
                kc = kc +1
                if (kc .le. mxptc) then
                  cirdat(1,kc) = xc(k)
                  cirdat(2,kc) = yc(k)
                  cirdat(3,kc) = kuvs(k)
                  cirdat(4,kc) = kint(k)
                endif
              else
                write (33,*) ' verify, duplicate cyclone at ',xc(k),
     &                       '  ',yc(k)
              endif
            endif
          enddo
        endif
      enddo
      if (kc .gt. mxptc) then
        write (*,*) 'ERROR: verify, cirdat too small, needed = ',kc
        kc = mxptc
      endif
      nccf = kc
      write (33,*)'Verify, retained ',nccf,' cyclones'
c
      end
      subroutine wbtdat (ninp,cpdtg,cyc_id,ntrk,tcyc,gdat,
     &                   numv,mxhr,mxtc,cfdtg,nogo)
c
c..........................START PROLOGUE..............................
c
c  SCCS IDENTIFICATION:
c
c  CONFIGURATION IDENTIFICATION:
c
c  MODULE NAME:  wbtdat
c
c  DESCRIPTION:  process working best tarck data
c
c
c  COPYRIGHT:                  (C) 1997 FLENUMOCEANCEN
c                              U.S. GOVERNMENT DOMAIN
c                              ALL RIGHTS RESERVED
c
c  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
c                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
c                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
c
c  REFERENCES:  none
c
c  CLASSIFICATION:  unclassified
c
c  RESTRICTIONS:  none
c
c  COMPUTER/OPERATING SYSTEM
c               DEPENDENCIES:
c
c  LIBRARIES OF RESIDENCE:
c
c  USAGE:  call wbtdat (ninp,cpdtg,cyc_id,ntrk,tcyc,gdat,numv,mxhr,mxtc,cfdtg,
c                        nogo)
c
c  PARAMETERS:
c     NAME         TYPE        USAGE             DESCRIPTION
c   --------      -------      ------   ------------------------------
c     ninp          int          in     I/O unit number for input
c     cpdtg        char          in     requested starting dtg, in
c                                       YYMMDDHH format
c     cyc_id       char          in     cyclone ID (04W)
c     ntrk          int         out     number of cyclones to track
c     tcyc         char         out     cyclone data in character form
c     gdat         real         out     cyclone data in real form
c     numv          int          in     first dimension of gdat, number
c                                       of variables in gdat
c     mxhr          int          in     limit second dimension of gdat,
c                                       max number of tracking positions
c     mxtc          int          in     third dimension of gdat, max
c                                       number of cyclones to track
c     cfdtg        char         out     starting field dtg of tracking, in
c                                       YYYYMMDDHH format
c     nogo          int         out     error flag, 0 no error
c
c  COMMON BLOCKS:  none
c
c  FILES:
c    NAME     UNIT  FILE TYPE  ATTRIBUTE  USAGE         DESCRIPTION
c   -------  -----  ---------  ---------  ------   ---------------------
c    ngtrp    10    permanent  sequential   in     NOGAPS tropical
c                                                  cyclone bogus file
c
c  DATA BASES:  none
c
c  NON-FILE INPUT/OUTPUT:  none
c
c  ERROR CONDITIONS:
c         CONDITION                 ACTION
c     -----------------        ----------------------------
c    read error                diagnostic
c    bad bogus data            diagnostic
c    number of cyclones to     diagnostic
c      process does not
c      match number read
c
c  ADDITIONAL COMMENTS:
c
c    The format of the tcyc array is:
c                  1         2
c         123456789012345678901234
c         12W 123N 1234E  1234 123
c          A   B     C      D   E
c
c         where:
c         A - cyclone number and original basin identification
c         B - latitude  times 10, with hemipshere indicator
c         C - longitude times 10, with hemipshere indicator
c         D - forecast heading times 10, deg
c         E - forecast speed times 10, kts
c
c...................MAINTENANCE SECTION................................
c
c  MODULES CALLED:
c          NAME           DESCRIPTION
c         -------     ----------------------
c         bdtgchk     check that bogus dtg is the same as the computer's
c         valinp      validate input data
c         clltxy      convert from lat,lon to x,y grid co-ords
c
c  LOCAL VARIABLES:
c          NAME      TYPE                 DESCRIPTION
c         ------     ----       ----------------------------------
c           card     char       working string
c            cns     char       north/south hemisphere indicator
c            cew     char       east/west hemisphere indicator
c            ioe     int        I/O error flag
c            iok     int        good/bad dtg flag, -1 - good
c           ierr     int        conversion error flag, 0 - good
c              k     int        number of good cyclones
c            ntc     int        number of cyclone data to read
c            nrd     int        number of cyclones read
c           shed     real       heading of cyclone, deg
c           slat     real       latitude  of cyclone, deg
c           slon     real       longitude of cyclone, deg
c           sspd     real       speed of movement of cyclone, kts
c           xgrd     real       first x-dimension of grid (lon)
c                               location of cyclone
c           ygrd     real       second y-dimension of grid (lat)
c                               location of cyclone
c
c           Note, grid location 1,1 is 90.0S and 0.0 longitude
c
c  METHOD:  N/A
c
c  INCLUDE FILES:  none
c
c  COMPILER DEPENDENCIES:
c
c  COMPILE OPTIONS:
c
c  MAKEFILE:
c
c  RECORD OF CHANGES:
c
c
c...................END PROLOGUE.......................................
c
      implicit none
c
c         formal parameters
      integer       ninp, numv, mxhr, mxtc, ntrk, nogo
      character*8   cpdtg, cfdtg
      character*24  tcyc(mxtc+1)
      real          gdat(numv,0:mxhr,mxtc)
c
c         local variables
      integer       ndrop, iwndmxf, iwndmxr, ilat, ilon, ihead, isped
      integer       nrd, nval, ierr, n, j, iwnd
      integer       ibtwind, ios
      character*1   cnso, cnsp, cnsf, cnsr, cns
      character*1   cewo, cewp, cewf, cewr, cew
      character*2   cent
      character*3   cyc_id
      character*8   dtgm12, dtgm6
      character*8   btdtg
      character*32  cline
      character*1   btns, btew
      real          xgrd, ygrd, head, dist, spd_kt
      real          olat, plat, flat, rlat
      real          olon, plon, flon, rlon
      real          btlat, btlon
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   determine the field dtg from the initial position dtg
c
      ntrk  = 0
      nrd   = 0
      nogo  = 0
      ndrop = 0
      iwndmxf = 0
      cfdtg = cpdtg
      if (cfdtg(7:8) .eq. '06' .or. cfdtg(7:8) .eq. '18') then
        ndrop = -6
        if (cfdtg(7:8) .eq. '06') then
          cfdtg(7:8) = '00'
        else
          cfdtg(7:8) = '12'
        endif
      endif
      if (cfdtg(7:8) .eq. '00' .or. cfdtg(7:8) .eq. '12') then
c
c                   find the  -6 hr and -12 hr dtg's
c
        call icrdtg (cfdtg,dtgm6,-6)
        call icrdtg (cfdtg,dtgm12,-12)
c
c                   find positions which match dtg's
c
        rewind (ninp)
        olat = 0.0
        plat = 0.0
        flat = 0.0
        rlat = 0.0
caj50   continue
cajs    read (ninp,'(a25)',end=60) cline
cajs    if (cline(3:10) .eq. dtgm12) then
c                   12-hr old position
cajs      read (cline,'(10x,2(f4.1,a1))') olat,cnso,olon,cewo
cajs      if (cnso .eq. 'S') olat = -olat
cajs      if (cewo .eq. 'W') olon = 360.0 -olon
cajs    elseif (cline(3:10) .eq. dtgm6) then
c                   6-hr old position
cajs      read (cline,'(10x,2(f4.1,a1))') plat,cnsp,plon,cewp
cajs      if (cnsp .eq. 'S') plat = -plat
cajs      if (cewp .eq. 'W') plon = 360.0 -plon
cajs    elseif (cline(3:10) .eq. cfdtg) then
c                   field position and maximum sustained wind speed
cajs      read (cline,'(10x,2(f4.1,a1),1x,i3)') flat,cnsf,flon,cewf,iwndmxf
cajs      if (cnsf .eq. 'S') flat = -flat
cajs      if (cewf .eq. 'W') flon = 360.0 -flon
cajs      if (ndrop .eq. 0) then
cajs        rlat = flat
cajs        cnsr = cnsf
cajs        rlon = flon
cajs        cewr = cewf
cajs        iwndmxr = iwndmxf
cajs      endif
cajs    elseif (cline(3:10) .eq. cpdtg) then
c                   present position and maximum sustained wind speed
cajs      read (cline,'(10x,2(f4.1,a1),1x,i3)') rlat,cnsr,rlon,cewr,
cajs &          iwndmxr
cx        bug fix ... i hope .........bs 10/10/97
cx        if (cns .eq. 'S') rlat = -rlat
cx        if (cew .eq. 'W') rlon = 360.0 -rlon
cajs      if (cnsr .eq. 'S') rlat = -rlat
cajs      if (cewr .eq. 'W') rlon = 360.0 -rlon
cajs    endif
c
cajs    if (rlat.eq.0.0 .or. flat.eq.0.0 .or. plat.eq.0.0 .or.
cajs &      olat.eq.0.0) goto 50
c
caj60   continue
        ios = 0
        do while (ios .eq. 0)
           call readBT(ninp,cent,btdtg,btlat,btns,btlon,btew,ibtwind,
     1                ios)
           if( ios.eq.0 .and. btdtg.eq.dtgm12 ) then
c                   12-hr old position
              olat = btlat
              cnso = btns
              if (cnso .eq. 'S') olat = -olat
              olon = btlon
              cewo = btew
              if (cewo .eq. 'W') olon = 360.0 -olon
           else if( ios.eq.0 .and. btdtg.eq.dtgm6 ) then
c                   6-hr old position
              plat = btlat
              cnsp = btns
              if (cnsp .eq. 'S') plat = -plat
              plon = btlon
              cewp = btew
              if (cewp .eq. 'W') plon = 360.0 -plon
           else if( ios.eq.0 .and. btdtg.eq.cfdtg ) then
c                   field position and maximum sustained wind speed
              flat = btlat
              cnsf = btns
              if (cnsf .eq. 'S') flat = -flat
              flon = btlon
              cewf = btew
              if (cewf .eq. 'W') flon = 360.0 -flon
              if (ndrop .eq. 0) then
                 rlat = flat
                 cnsr = cnsf
                 rlon = flon
                 cewr = cewf
                 iwndmxr = iwndmxf
              endif
           else if( ios.eq.0 .and. btdtg.eq.cpdtg ) then
c                   present position and maximum sustained wind speed
              rlat = btlat
              cnsr = btns
              if (cnsr .eq. 'S') rlat = -rlat
              rlon = btlon
              cewr = btew
              if (cewr .eq. 'W') rlon = 360.0 -rlon
           endif
        enddo

        if (rlat .ne. 0.0) then
          if (ndrop .eq. 0) then
c                     flat = rlat
            if (plat .ne. 0.0) then
              call rcalhdst (plat,plon,rlat,rlon,head,dist)
              spd_kt  = dist/6.0
            elseif (olat .ne. 0.0) then
              call rcalhdst (olat,olon,rlat,rlon,head,dist)
              spd_kt  = dist/12.0
            else
              head   = 0.0
              spd_kt = 0.0
            endif
          else
            if (flat .ne. 0.0) then
              call rcalhdst (flat,flon,rlat,rlon,head,dist)
              spd_kt  = dist/6.0
            elseif (plat .ne. 0.0) then
              call rcalhdst (plat,plon,rlat,rlon,head,dist)
              spd_kt  = dist/12.0
            elseif (olat .ne. 0.0) then
              call rcalhdst (olat,olon,flat,flon,head,dist)
              spd_kt  = dist/12.0
            else
              head   = 0.0
              spd_kt = 0.0
            endif
          endif
        elseif (flat .ne. 0) then
          if (plat .ne. 0.0) then
            call rcalhdst (plat,plon,flat,flon,head,dist)
            spd_kt  = dist/6.0
          elseif (olat .ne. 0.0) then
            call rcalhdst (olat,olon,flat,flon,head,dist)
            spd_kt  = dist/12.0
          else
            head   = 0.0
            spd_kt = 0.0
          endif
        else
          head   = 0.0
          spd_kt = 0.0
        endif
          write(*,*)'olat,plat,rlat,flat'
          write(*,*)olat,plat,rlat,flat
          write(*,*)'olon,plon,rlon,flon'
          write(*,*)olon,plon,rlon,flon
        if (flat .ne. 0.0) then
          if (flat .lt. 0.0) flat = -flat
          ilat = nint (flat * 10.0)
          if (flon .gt. 180.0) flon = 360.0 -flon
          ilon  = nint (flon * 10.0)
          ihead = nint (head * 10.0)
          isped = nint (spd_kt * 10.0)

cx
cx  if speed out of range, change to 0   bs 10/10/97
cx
	  if (isped.gt.900) then
	       write(*,*) 'speed out of range:',isped
	       write(*,*) 'speed changed to 0:'
	       isped=0
          endif

          tcyc(1) = ' '
          write (tcyc(1),9040) cyc_id,ilat,cnsf,ilon,cewf,ihead,isped
 9040     format (a3,1x,i3.3,a1,1x,i4.4,a1,2x,i4.4,1x,i3.3)
	  write(*,*) 'found ',tcyc(1)
c
          nrd = nrd +1
c
c                   validate data with valinp
c
          call valinp (tcyc,nrd,nval)
          if (nval .eq. 0) then
c
c                   convert from character mode to real mode
c                   for latitude, longitude, heading and speed
c                   and load gdat array with starting values
c
	    write(*,*) 'ntrk=',ntrk,'  mxtc=',mxtc
            if (ntrk .lt. mxtc) then
	    write(*,*) 'tcyc(nrd)=',tcyc(nrd)
	      read (tcyc(nrd),'(4x,f3.1,a1,1x,f4.1,a1,2x,f4.1,1x,f3.1)')
     &              flat, cnsf, flon, cewf, head, spd_kt
              if (cnsf .eq. 'S') flat = -flat
c                   note: make longitude 0 - 360 EAST
              if (cewf .eq. 'W') flon = 360.0 -flon
c                   convert lat,lon to grid co-ordinates
              write (*,*) 'Calling clltxy, flat ',flat,' flon ',flon
              call clltxy (flat,flon,xgrd,ygrd,ierr)
              if (ierr .eq. 0) then
                ntrk = ntrk +1
                gdat(1,0,ntrk) = flat
                gdat(2,0,ntrk) = flon
                gdat(3,0,ntrk) = xgrd
                gdat(4,0,ntrk) = ygrd
c                   store heading (deg)
                gdat(5,0,ntrk) = head
c                   store distance (nm) in 12 hours vice speed (kt)
                gdat(6,0,ntrk) = 12.0*spd_kt
                gdat(7,0,ntrk) = 0.0
                gdat(8,0,ntrk) = 0.0
                gdat(9,0,ntrk) = 0.0
c                   put missing lat to all following positions
                do j=1, mxhr
                  gdat(1,j,ntrk) = 99.9
                enddo
              else
		write (*,*) 'BAD conversion for ',flat,'  &  ',flon
              endif
            else
	      write (*,*) 'ngtrack, TOO MANY cyclones, limit ',mxtc
	    endif
          else
            write (*,*) 'NO VALID wbt data'
            nogo = -99
          endif
        else
          write (*,*) 'NO position for dtg ',cfdtg
          nogo = -99
        endif
      else
        write (*,*) 'BAD initial dtg is ',cpdtg
        nogo = -99
      endif
c
      end
