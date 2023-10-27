      program iships
c     This program reads in data from the istormcard.dat, itrack.dat and 
c     lsdiag.dat files which contain the information for the SHIPS
c     intensity forecast.  The forecast is written to the file
c     ships.dat for the new ATCF format, and to ships.tst in a modified
c     version of the old ATCF format. 
c
c     PARMOD
c     This is the version for parallel runs. Code mods are identified by PARMOD.
c
c     This version can be used in the Atlantic or Eastern Pacific
c
c     The over-ocean forecasts are modified to take into
c     account the effect of land. 
c
c     This version also includes forecasts out to 5 days,
c     and writes the output in the new ATCF format.
c
c     Modified: Jul 27, 2001 to add Atlantic rapid intensity index
c     Modified: Apr 10, 2002 to add new SHIPS predictors for 2002 season
c     Modified: Jul 16, 2002 to add new RII routine with 24-hr input parameters
c                             and for parallel forecast with OHC predictors
c     Modified: May  9, 2003 to add new SHIPS predictors for 2003 season
c     Modified: May 21, 2004 for 2004 season (new coefficients, RI index)
c     Modified: May 17, 2005 for 2005 season (new coefficients, RI index, 
c                                             6 hour data)
c     Modified: Jul 14, 2005 to correct persistence for storms moving
c                            back over water
c     Modified: May 15, 2006 for 2006 season 
c                          1) Speed adjusted MPI
c                          2) New T250 predictor
c                          3) Forecast lat/speed used in Cione SST cooling
c                          4) 36 N restriction removed in Cione cooling
c                          5) Forecast divergence field used
c                          6) Order of predictors adjusted
c                          7) New coefficients
c     Modified: May 19, 2006 to add Logistic Growth Equation (LGE) forecast
c     Modified: Jul  3, 2006 to add ATCF number to SHIPS output
c     Modified: Aug 17, 2006 to add additional GOES error checking
c     Modified: Aug 29, 2006 Still more GOES error checking (std check)
c     Modified: Sep 21, 2006 Experimental shear version and annular
c                            hurricane index added
c     Modified: Mar 30, 2007 for 2007 season
c                          1) SHRD replaced by SHDC
c                          2) New TWAC predictor added
c                          3) RHHI replaced by RHMD
c                          4) New coefficients (based on 1982-2006)
c                          5) VMAX added to LGEM forecast
c                          6) Experimental run turned off
c     Modified: May 22, 2008 for 2008 season
c                          1) Some variable names changes to avoid compiler warnings
c                          2) New RII routines
c                          3) New coefficients (based on 1982-2007)
c     Modified: May  15, 2009 for the 2009 season
c                          1) New coefficients (based on 1982-2008)
c                          2) Perturbation model eliminated 
c                             (satellite input included with main model)
c                          3) OHC added to east Pacific
c                          4) New quality control for GOES and OHC data
c                             (proxy or sample mean used when missing)
c                          5) New predictor based on shear direction 
c                             added to SHIPS and LGEM
c                          6) Satellite data added to LGEM (GOES and OHC)
c                          7) Code for "experimental" SHIPS removed
c     Modified: Mar 11, 2010 to add PrSEFoNe model (prob of secndry eywll frmtn)
c                          1) Small block of code to fill feature matrix required
c                             by model added to main program body.
c                          2) PrSEFoNe driver subroutine added below annular hurricane
c                             index code. All required subroutines and functions 
c                             (PrSEFoNe module) added below AHI module.
c     Modified: May 25,2010 for 2010 season
c                          1) New predictor SHGC - SHCGBAR(SHDC)
c 
      !ships_util includes subroutines tspdcal, stndz, patch, moment,
      !   ctorh, rhtoc, jdate, chartointmon, tdiff, and yr2to4
      use ships_util
      use ships_input
c 
c***      include 'dataformats.inc'
c
c-----7---------------------------------------------------------------72
c***********************************************************************
c     User-defined options
c***********************************************************************
      !Set ioper=1 for operational run where coefficient files 
      !            use the getenv command
      ! or ioper=0 for non-operational runs where coefficient files are
      !            copied to the local directory where the code is run
      integer, parameter :: ioper=0
c
      !Set run id number for test runs
      character(2), parameter :: runid='30'
c
      !Set flags for turning off RII, SEF, AHI routines, and SHIPS output
      integer, parameter :: irii=0
      integer, parameter :: isef=0
      integer, parameter :: iahi=0
      integer, parameter :: ishp=1

      !Set flag for SHIPS input type
      ! imodel=0 for normal input (lsdiag.dat, istormcard.dat, itrack.dat)
      ! imodel=1 for model input (imodel.dat, iadeck.dat)
      integer, parameter :: imodel=1
c 
      !Set iperts= 1 to add perturbation SHIPS forecasts (satellite input)
      ! or iperts= 0 to skip perturbation SHIPS
      integer, parameter :: iperts=0
c 
      !Set flag for using AMSR SST data
      integer, parameter :: iamsr=0
c 
c***********************************************************************
c     Set constants
c***********************************************************************
      !the integer and real versions of missing data
      integer, parameter :: imiss = 9999
      real, parameter :: rmiss = 9999.
c       
      !nvar is the number of parameters used in SHIPS
      integer, parameter :: nvar=23
c 
      !this parameter is defined in SHIPS in the same line as nvar
c***  check on this
      !it is never actually used in iships.f though, may be able to
      !dispose of it
      integer, parameter :: nvarp=3
c 
      !mft represents the maximum number of time periods
      !example: mft=20 -> 20*6=120hrs maximum time
      integer, parameter :: mft=20


C--mf     20101117 flag ivmx=vmx0
C--mf     20101117 flag for reading full adeck vice my reduced version
      ! set flag for initializing model Vmax with CARQ
      integer icarqvmax

      ! set flag for reading adeck or my carq
      integer ireadAdeck,do5charname

c 
c     Integer arrays for predictors
c 
      !LAT, LON, and DTL
      integer, dimension(-2:mft) :: ilat=imiss, ilon=imiss
      integer, dimension(0:mft) :: idist=imiss
      !VMAX
      integer, dimension(0:mft) :: ivmaxb=imiss
      integer :: ivmx   !VMAX(t=0)
      integer :: iper   !VMAX(t=0)-VMAX(t=-12)
      !SST
      integer, dimension(0:mft) :: isst=imiss, irsst=imiss
      integer :: irlag = imiss   !lag in hrs for RSST
      integer, dimension(0:mft) :: iasst=imiss
      !ocean heat content
      integer, dimension(0:mft) :: irhcn=imiss, iphcn=imiss
      !GOES IR
      integer, dimension(0:mft) :: igoes=imiss, igoesm3=imiss
      integer, dimension(0:mft) :: igoesxx=imiss
      !pressure level : U200, T200, T250
      integer, dimension(0:mft) :: iu200=imiss
      integer, dimension(0:mft) :: it200=imiss, it250=imiss
      !derived : Z850, D200, EPOS, REFC, PSLV, TWAC
      integer, dimension(0:mft) :: id200=imiss, iz850=imiss
      integer, dimension(0:mft) :: iepos=imiss, irefc=imiss
      integer, dimension(0:mft) :: ipslv=imiss, itwac=imiss
      !relative humidity RHLO, RHMD, RHHI
      integer, dimension(0:mft) :: irhlo=imiss, irhmd=imiss
      integer, dimension(0:mft) :: irhhi=imiss
      !wind shear : SHRD, SHDC, SDDC, SHTD, SHGC
      integer, dimension(0:mft) :: ishr=imiss, ishtd=imiss
      !modified wind shear
      integer, dimension(0:mft) :: ishdc=imiss, isddc=imiss
      integer, dimension(0:mft) :: ishgc=imiss
c***  read in from model but unused
      integer, dimension(0:mft) :: ishrs=imiss, ishts=imiss
      integer, dimension(0:mft) :: ishrg=imiss
c 
c     Real arrays for predictors
c 
      !TIME
      real, dimension(-2:mft) :: ftimec=rmiss
      !LAT, LON, and distance
      real, dimension(-2:mft) :: rlat=rmiss, rlon=rmiss
      real, dimension(-2:mft) :: cxt=rmiss, cyt=rmiss
      real, dimension(-2:mft) :: cmagt=rmiss
c 
c***  adjusting variable declarations
c 
      !VMAX
      dimension v(0:mft),delv(0:mft)
      dimension iv(0:mft)
      !SST
      dimension sst(0:mft),vsst(0:mft)
      dimension sstc(0:mft),vsstc(0:mft),vsstl(0:mft)
      !pressure level temperatures: T200, T250
      real, dimension(0:mft) :: t200=rmiss, t250=rmiss
      !derived : TWAC
      real, dimension(0:mft) :: twac=rmiss
      !wind shear : SHRD, SHDC, SDDC, SHGC, SHTD (?)
c***  there's a question here about which are being used
      !modified wind shear
      dimension shdc(0:mft),sdir(0:mft)
      dimension shdct(0:mft),shgc(0:mft)
c 
      dimension var(nvar),coef(nvar,mft),vart(nvar,mft)
      dimension xbar(nvar,mft),xsig(nvar,mft)
      dimension ybar(mft),ysig(mft)
c
c     Arrays for perturbation SHIPS forecast
      dimension coefp(nvar,mft)
      dimension xbarp(nvar,mft),xsigp(nvar,mft)
      dimension ybarp(mft),ysigp(mft)
      dimension delvp(0:mft),delvt(0:mft)
      dimension vpert(0:mft),vartp(nvar,mft)
c 
      dimension ilatt(0:mft),ilont(0:mft)
c
c     Arrays for printing intensity change per variable
      dimension dvvar(nvar,mft)
      character *20 cdvlab(nvar)
c 
c     Character arrays for printing predictors
      character *4  cv(0:mft),cshr(0:mft),csst(0:mft)
      character *4  cshtd(0:mft), cvmaxb(0:mft)
      character *4  cvsst(0:mft),cvsstc(0:mft)
      character *4  clat(0:mft),cdist(0:mft),crefc(0:mft)
      character *4  crhlo(0:mft),cu200(0:mft)
      character *4  cz850(0:mft),cd200(0:mft)
      character *4  crhhi(0:mft),cepos(0:mft)
      character *4  crhmd(0:mft)
      character *5  clon(0:mft),ct200(0:mft),ct250(0:mft)
      character *4  cmagc(0:mft)
c 
c     Storm names/designations
      character *4  sname4           !4-char storm designation: BB##
      character *4  tmname           !4-char model designation
      character *4  tem4             !altered model designation
      character *5  tem5             !altered model designation
      character *6  slab,natcf
      character *8  natcf8           !8-char ATCF ID: BB##YYYY
      character *10 sname            !10-char storm name
      character *5  varlab(0:nvar)   !Predictor names

c     I/O file names
      character *256 fnis,fnls,fnit,fnco,fnat,fnsh,fnlg,fnts
      character *256 fncop
c***  added model input files (fnmo,fnad)
      character *256 fnmo,fnad,fnadmf
      character *256 coef_location

c     temporary text lines
      character *80 iline80
      character *130 iline
c***  add line readin for model (16+6*(mft+1)) = 142
      character *142 ilinem
c***  add character strings for holding model read formats
      character *13 cfmtstri
      character *13 cfmtstrf
c
c     Arrays for decay program
      parameter(idmx=mft+1)
      dimension rlatd(idmx),rlond(idmx),ftime(idmx),vmaxo(idmx)
      dimension vmaxd(idmx),ddland(idmx)
      dimension ivd(0:mft)
      character *4 cvd(0:mft)
c
c     Variables for new ATCF output
      dimension ifship(11,3)
      character *8 strmid
      character *10 aymdh
c
c     Variables for LGE model
      parameter (ilmx=mft+1)
      dimension vmaxl(ilmx)
c***      dimension t200(0:mft),t250(0:mft)
      dimension ivl(0:mft)
      character *4 cvl(0:mft)
c
c     Variables for modified shear version
c***      dimension itwac(0:mft),ishdc(0:mft),isddc(0:mft)
c***      dimension  twac(0:mft), shdc(0:mft),sdir(0:mft)
c***      character*2 runid
      character*4 cshdc(0:mft),cshgc(0:mft)
      character*4 ctwac(0:mft)
c
c     Variables for SHGC and transformed shdc
c***      dimension ishgc(0:mft)
c***      dimension shdct(0:mft),shgc(0:mft)
c
c     Variables for annular hurricane index
      character *8 tcfid
      character *10 stname
      character *34 fn_ships
      character *34 fn_ird1
      character *34 fn_ird2
      character *34 fn_iri1
      character *34 fn_iri2

      character copt*2

c ************************************************************************
c  Variables for PrSEFoNe (probability of secondary eyewall formation) 
c    NATL: 11 features from lsdiag. Include DTL for 12. PC4 is 
c          calculated later. Data needed for 4 forecast times. 
      dimension psef_feat_vec(12,4) ! NATL feature set
      dimension iflag_feat(4)
      integer, dimension(0:mft) :: ipenc,ivmpi2 ! PrSEFoNe model needs these
      integer imiss_feat,iflag_feat_ir

c ************************************************************************
c
c     Array for climatological goes predictors
      parameter (ngoes=16)
      dimension igoessm(0:mft)
      data igoessm /0,-365,145,-266,191,
     +              71,65,58,50,40,25,
     +              -364,-402,15,
     +              -481,-405,56,
     +              9999,9999,9999,9999/

c     Max lon (deg W neg) for calling annular routine
      data rlonam /-35.0/

c     ++ Common blocks for main iships.f program for lgecal routine

      common /lgestr/ aday,spdx,pslv,per,vmx,pc20,rthresh
      common /lgetdi/ ishr,iepos,iz850,id200,ishdc,irhcn
      common /lgetdr/ sst,vsstl,rlat,rlon,t200,t250,twac,sdir,
     +                shdct,shgc
c***      common /lgepar/ rmiss,imiss,ioper
c
c     Initialize various arrays

      data delv  /21*0.0/
      data delvp /21*0.0/
      data v     /21*0.0/

      data dtr /0.017453/
 
      !I/O file unit numbers
      data luis,luls,luit,luco,luat,lush,lulg,luts 
     +     /30,31,32,33,34,35,36,37/
      data lucop /38/
c***  added model input file unit numbers lumo, luad
      data lumo, luad /41,42/

Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
C         
C         command line processing
C
Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      call getarg(1,copt) 

      narg=iargc()
      
      if(narg.eq.1 .and.copt.eq.'-h') then

        print*,'Arguments to ishipk.x:'
        print*,' '
        print*,'    copt : optional character option:'
        print*,' '
        print*,'          -i set initial Vmax to model; otherwise use CARQ'
        print*,'          -A use adeck vice icarq.dat'
        print*,"          -5 use 5-char techname otherwise use 1st 3 char from the techname"
        print*,"               append 'S' for SHIPS; 'D' for decay SHIPS; and 'G' for LGEM"
        print*,'          -h this help message'
        print*,' '
        print*,'Example'
        print*,' '
        print*,'iship.x -i'
        print*,' '
        stop 

      endif

      icarqvmax=1
      ireadAdeck=0

      do5charname=0
      if(copt.eq.'-i') icarqvmax=0
      if(copt.eq.'-A') ireadAdeck=1
      if(copt.eq.'-5') do5charname=1

c***      type ( AID_DATA ) comRcd, tauData
c 
c     ++ End declaration section
c 
      if (ioper .eq. 1) then
c        get COEF Env Variable
         call getenv( "SHIPS_COEF", coef_location )
      endif
c
c     Specify the maximum acceptable age (in hours) of the
c     Reynolds SST data
      irlagx = 440 
c
c     Specify intensity (kt) for which storm is considered dissipated
      vdiss  = 15.0
      ivdiss = ifix(vdiss)
c
c     Forecast time interval (hr)
      delt = 6.0
      idelt = ifix(delt)
c
c     Open the input and output files
      fnis = 'istormcard.dat'
      fnls = 'lsdiag.dat'
      fnit = 'itrack.dat'
c***  added model input files fnmo, fnad
      fnmo = 'modeldiag.dat'
      fnad = 'iadeck.dat'
      fnadmf = 'icarq.dat'   ! mf 20101015 different input of tcvitals
c 
      fnat = 'ships.dat'
      fnts = 'ships.tst'
      fnsh = 'ships.txt'
      fnlg = 'ships.log'
c 
c     Input files opened based on imodel flag
      if (imodel .eq. 0) then !opens lsdiag.dat and supporting files
         open(unit=luis,file=fnis,form='formatted',status='old',err=900)
         open(unit=luls,file=fnls,form='formatted',status='old',err=900)
         open(unit=luit,file=fnit,form='formatted',status='old',err=900)

       else                     !opens modeldiag.dat and supporting files
         
         if(ireadAdeck.eq.1) then
           open(unit=luad,file=fnad,form='formatted',status='old',err=900)
         else
           open(unit=luad,file=fnadmf,form='formatted',status='old',err=900)
         endif

         open(unit=lumo,file=fnmo,form='formatted',
     $        status='old',err=900)

      endif
c 
c         Open output files
      
      open(unit=lulg,file=fnlg,form='formatted',status='replace',
     +     err=900)
      open(unit=luat,file=fnat,form='formatted',status='replace',
     +     err=900)
      open(unit=luts,file=fnts,form='formatted',status='replace',
     +     err=900)
      open(unit=lush,file=fnsh,form='formatted',status='replace',
     +     err=900)
c
c     Read input files depending on type of input chosen (imodel flag)
      if (imodel .eq. 0) then   !read in lsdiag and supporting files
c 
c        Read the stormcard file
         call readSCard(luis,ierr,isyr,isyr4,ismon,isday,istime,
     +                  ilat0,ilatm12,ilon0,ilonm12,
     +                  ivmx0,ivmxm12,ihead,ispeed,
     +                  sname,natcf,natcf8)
         close(luis)
         print*,'read stmcard'
         if (ierr .ne. 0) go to 900
c
c        Read the track file (for the track model name)
         read(luit,'(24x,a4)') tmname
         close(luit)
c 
c        Read the lsdiag file
         call readLSDiag(luls,mft,ierr,
     +                   ilyr,ilyr4,ilmon,ilday,iltime,
     +                   sname4,ivmx,iper,irlag,
     +                   ilat,ilon,idist,ivmaxb,
     +                   iu200,it200,it250,
     +                   iz850,id200,itwac,iepos,ipslv,irefc,
     +                   irhhi,irhmd,irhlo,
     +                   ishr,ishtd,ishdc,isddc,ishgc,
     +                   isst,irsst,iasst,irhcn,iphcn,
     +                   igoes,igoesm3,igoesxx,
     +                   ipenc,ivmpi2)
         close(luls)
         if (ierr .ne. 0) go to 900
         write(aymdh,'(i4.4,3(i2.2))') ilyr4,ilmon,ilday,iltime

      else   !model input data
c 
c        Read the modeldiag file
         call readModel(lumo,mft,ierr,
     +                  ilyr,ilyr4,ilmon,ilday,iltime,
     +                  tmname,sname4,sname,natcf,natcf8,
     +                  ivmx,
     +                  ilat,ilon,idist,ivmaxb,
     +                  iu200,it200,it250,
     +                  iz850,id200,itwac,iepos,ipslv,
     +                  irhhi,irhmd,irhlo,
     +                  ishr,ishtd,ishrs,ishts,ishrg,
     +                  ishdc,isddc,ishgc,
     +                  isst,iphcn)
         close(lumo)
         print*,'readModel',ierr
         if (ierr .ne. 0) go to 900

c        Read the adeck data

         write(aymdh,'(i4.4,3(i2.2))') ilyr4,ilmon,ilday,iltime

         if(ireadAdeck.eq.1) then

           call readADeck(luad,aymdh,ierr,
     +          isyr,isyr4,ismon,isday,istime,
     +          ilat0,ilatm12,ilon0,ilonm12,
     +          ivmx0,ivmxm12,ihead,ispeed,iper)
           print*,'readAdeck',ierr
           
         else

C--mf     20101014 -- new routine in ships_input.f

           call readCARQ(luad,ierr,
     +          isyr,isyr4,ismon,isday,istime,
     +          ilat0,ilatm12,ilon0,ilonm12,
     +          ivmx0,ivmxm12,ihead,ispeed,iper)
           print*,'readCARQ',ierr
           
         endif

         print*,'  isyr,isyr4,ismon,isday,istime: ',isyr,isyr4,ismon,isday,istime
         print*,'    ilat0,ilatm12,ilon0,ilonm12: ',ilat0,ilatm12,ilon0,ilonm12
         print*,'ivmx0,ivmxm12,ihead,ispeed,iper: ',ivmx0,ivmxm12,ihead,ispeed,iper

         if(icarqvmax.eq.1) then
           print*, 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW set model vmax to carq ivmx0: ',ivmx0,' ivmx: ',ivmx
           ivmx=ivmx0
         endif
         
         close(luad)
         if (ierr .ne. 0) go to 900

       endif
c
c     Open the coefficient file, depending on the basin
      if (natcf(1:1) .eq. 'E' .or. natcf(1:1) .eq. 'C') then
         ibasin=2
      else
         ibasin=1
      endif
c
c     Set basin dependent parameters
c         fnco = Coefficient file name
c         jdmax = Julian Day of peak hurricane season
c         ishrx = The maximum no. of forcast times to use the
c                 shear (1=12 hr, 2=24 hr, 3=36 hr, etc)
c         irefcx= Similar to ishrx for refc
c         it200x= Similar to ishrx for t200
c         it250x= Similar to ishrx for t250
c         t250th= Threshold value for t250 predictor
c         icione= flag for Joe Cione SST cooling algorithm
c                 0 to skip cooling algorithm
c                 1 to include it with initial value of lat and storm speed
c                 2 to include it with forecast lat and storm speed values
c         mpispd= flag to adjust MPI for storm translational speed
c                 0 to use mean speed adjusted mpi routine (mpical)
c                 1 to use original mpi routine (mpicalo) and add
c                   fraction of storm speed from Schewerdt formula a = 1.5*c**0.63
c         iohcsm= Sample mean value of OHC
c         rthresh=OHC threshold
c         rsdir = Reference direction for shear direction predictor (sdp)
c         th1,th2,f1,f2 = factors for scaling sdp by latitude
c         sna,snb,snc,snd: Coefficients for log transformation of shear
c         ga0,ga1,ga2:     Coefficients for mean SHGC from SHDC
c
c
      if (ibasin .eq. 2) then
         if (ioper .eq. 1) then
            fnco = trim( coef_location ) // 'ships10_coef_epac.dat'
         else
            fnco = 'ships10_coef_epac.dat'
         endif
         jdmax =238
	 raefld = 30.0
         ishrx =mft
         irefcx=mft
         it200x=mft
         it250x=mft
         t250th= 0.0
         icione=0
         mpispd=1
         iohcsm=35
         rthresh=0.0
c 
         rsdir = 70.0
         th1   = 10.0
         th2   = 30.0
         f1    = 1.0
         f2    = -1.0
c 
         ga0 = 12.74
         ga1 = 0.6572
         ga2 = 0.0070
c 
         sna = 20.0
         snb = 0.5
         snc = 5.0
         snd = 33.5
      else
         if (ioper .eq. 1) then
            fnco = trim( coef_location ) // 'ships10_coef_atlc.dat'
         else
            fnco = 'ships10_coef_atlc.dat'
         endif
         jdmax =253
	 raefld = 30.0
         ishrx =mft
         irefcx=mft
         it200x=mft
         it250x=mft
         t250th= -44.0
         icione=2
         mpispd=1
         iohcsm=45
         rthresh=60.0
         rsdir = 55.0
	 th1   = 10.0
	 th2   = 40.0
	 f1    = 1.0
         f2    = -0.75
c 
         ga0 = 10.12
         ga1 = 0.8348
         ga2 = 0.0041
c 
         sna = 20.0
         snb = 0.5
         snc = 5.0
         snd = 33.5
      endif
c
c**   lsdiag read was moved to inside the input if construct
c**    (before the basin-dependent coefficients)
c 
c***
c***  Finished reading in files, begin data manipulation
c***  (coefficient file actually read in later?)
c***
c 
c     change some of the initializations from imiss to 0
      if (itwac(0) .eq. imiss) itwac(0) = 0
      if (ivmx .eq. imiss) ivmx = 0
      do k=0,mft
         if (ivmaxb(k) .ge. imiss) ivmaxb(k) = 0
      enddo
c
c     Check to make sure at least the initial value of each atmospheric
c     predictor is available
      istop=0
      if (ishdc(0) .eq. imiss) istop=1
      if (ishgc(0) .eq. imiss) istop=1
      if (isddc(0) .eq. imiss) istop=1
      if (it200(0) .eq. imiss) istop=1
      if (it250(0) .eq. imiss) istop=1
      if (iepos(0) .eq. imiss) istop=1
      if (irhmd(0) .eq. imiss) istop=1
      if (id200(0) .eq. imiss) istop=1
      if (iz850(0) .eq. imiss) istop=1
c 
      if (istop .eq. 1) then
         write(lulg,990)
  990    format(/' Some t=0 predictors missing')
         write(*,990)
         go to 900
      endif
c 
c     Choose SST
      if (iamsr .eq. 1) then
c        Replace RSST with AMSR SST if it is available
         do k=0,mft
            if (iasst(k) .lt. imiss) irsst(k)=iasst(k)
         enddo
      endif
c     Replace the climatological SST with the Reynolds SST
c     data if it is available
      do 4 k=0,mft
         if (irlag .gt. irlagx) go to 4
         if (irlag .lt.      0) go to 4
         if (irsst(k) .gt. 350) go to 4
         isst(k) = irsst(k)
    4 continue
c
c     Check OHC data. If missing, replace with PHCN. 
c     If that is missing, use sample mean OHC at t=0
      ipohc = 0
      do k=0,mft
         if (irhcn(k) .ge. imiss .and. iphcn(k) .lt. imiss) then
            irhcn(k) = iphcn(k)
            if (k .eq. 0) then
               ipohc=2
            else
               ipohc=1
            endif
         endif
      enddo
      if (irhcn(0) .ge. imiss) then
         irhcn(0) = iohcsm
         ipohc=3
      endif
c
c     ++ Begin GOES data quality control
c 
      vmx       = float(ivmx)
c 
      if (igoes(4) .lt. imiss) then
c        Check GOES00 standard deviation variable to see if 
c        it unreasonably large (+/- 3sigma)
         stdck = abs(vmx*0.1*float(igoes(4))-1000.0)/450.0
c 
         write(lulg,824) vmx,igoes(4),stdck
  824    format(/,' t=0  GOES std chk: vmx, igoes4, stdck=',
     +                               f5.0,1x,i4,1x,f6.2)
c 
         if (stdck .gt. 3.0) then
            do ii=0,mft
               igoes(ii) = imiss
            enddo
         endif
      endif
c 
      if (igoesm3(4) .lt. imiss) then
c        Check GOESM3 standard deviation variable to see if 
c        it unreasonably large (+/- 3sigma)
         stdck = abs(vmx*0.1*float(igoesm3(4))-1000.0)/450.0
c 
         write(lulg,825) vmx,igoes(4),stdck
  825    format(/,' t=-3 GOES std chk: vmx, igoes4, stdck=',
     +                               f5.0,1x,i4,1x,f6.2)
c 
         if (stdck .gt. 3.0) then
            do ii=0,mft
               igoes(ii) = imiss
            enddo
         endif
      endif
c
c     Perform buddy check of GOES data if possible
      it1 = igoes(1)
      is1 = igoes(2)
      it2 = igoesm3(1)
      is2 = igoesm3(2)
c 
      if (it1 .lt. imiss .and. it2 .lt. imiss .and.
     +    is1 .lt. imiss .and. is2 .lt. imiss       ) then
         adt = 0.1*abs(float(it2-it1))
         ads = 0.1*abs(float(is2-is1))
c 
         write(lulg,826) it1,it2,is1,is2,adt,ads
  826    format(/,' GOES buddy check input: ',4(i4,1x),2(f6.1,1x))
c
c        If dt or ds too large, one of the GOES profiles is bad
         if (adt .gt. 40.0 .or. ads .gt. 20.0) then
            do ii=0,mft
               igoes(ii) = imiss
            enddo
            go to 890
         endif
      endif
c
c     If t=0 GOES data missing, replace with t=-3 data.
c     If still missing, replace with proxy GOES.
c     If still missing, replace with sample mean values
      ipgoes = 0
      do k=0,ngoes
         if (igoes(k) .ge. imiss .and. igoesm3(k) .lt. imiss) then
            igoes(k) = igoesm3(k)
         endif
      enddo
c 
      do k=0,ngoes
         if (igoes(k) .ge. imiss .and. igoesxx(k) .lt. imiss) then
            igoes(k) = igoesxx(k)
            ipgoes=1
         endif
      enddo
c 
      do k=0,ngoes
         if (igoes(k) .ge. imiss) then
            igoes(k) = igoessm(k)
            ipgoes=2
         endif
      enddo
c
c     ++ End GOES data quality control
c
c     Convert t200 and t250 to real, and apply 250 threshold
      do k=0,mft
         if (it200(k) .lt. imiss) then
            t200(k) = 0.1*float(it200(k))
         else
            t200(k) = rmiss
         endif
c 
         if (it250(k) .lt. imiss) then
            t250t = 0.1*float(it250(k))
            t250t = t250t - t250th
            if (t250t .gt. 0.0) t250t = 0.0
            t250(k) = t250t
         else
            t250(k) = rmiss
         endif
      enddo
c
c     Convert twac to real and fill out array
      do k=0,mft
         if (itwac(k) .eq. imiss) then
            twac(k) = rmiss
         else
            twac(k) = 0.1*float(itwac(k))
         endif
      enddo
      call patch(twac,rmiss,mft)
c
c     Calculate shear direction predictor
      do k=0,mft
         if (ilat(k) .lt. imiss .and. isddc(k) .lt. imiss) then
            tlat = 0.1*float(ilat(k))
            sddct=     float(isddc(k))
c 
            adif = abs(rsdir-sddct)
            if (adif .gt. 180.0) adif = abs(360.0-adif)
            if (adif .gt. 180.0) adif = 0.0
            adif = adif - 90.0
c 
            if (tlat .le. th1) then
               fscale = f1
            elseif (tlat .ge. th2) then
               fscale = f2
            else
               z = (tlat-th1)/(th2-th1)
               fscale = f1 + 3.0*(f2-f1)*z*z - 2.0*(f2-f1)*z*z*z
            endif
c 
            sdir(k) = fscale*adif
         else
            sdir(k) = 9999.
         endif
c         write(6,731) k,tlat,rsdir,sddct,adif,sdir(k)
c  731    format('k,lat,rsdir,sddc,adif,sdir: ',i2,6(1x,f7.1))
      enddo
c
c     Convert shgc to a deviation from value based on shdc and calculate 
c     log-transformed shdc if ilogt=1 
      ilogt = 0
      do k=0,mft
         if (ishdc(k) .lt. imiss .and. ishgc(k) .lt. imiss) then
            sdtem = 0.1*float(ishdc(k))
            sgtem = 0.1*float(ishgc(k))
c 
            if (ilogt .eq. 1) then
               shdct(k) = sna*alog(snb*sdtem + snc) - snd
            else
               shdct(k) = sdtem
            endif
            sgbar    = ga0 + ga1*sdtem + ga2*sdtem*sdtem
            shgc(k)  = sgtem - sgbar
         else
            shdct(k) = rmiss
            shgc(k)  = rmiss
         endif
      enddo
c 
c     Read the coefficient file
      open(unit=luco,file=fnco,form='formatted',status='old',err=900)
c 
      do 5 k=1,mft
         read(luco,135) ybar(k),ysig(k)
  135    format(14x,e12.5,1x,e12.5)
c      
         do 6 n=1,nvar
            read(luco,136) coef(n,k),xbar(n,k),xsig(n,k)
  136       format(1x,3(e12.5,1x))
    6    continue
    5 continue
      close(luco)
c
c     Write basic storm information to the log file
      write(lulg,302) sname,isyr,ismon,isday,istime
  302 format(' SHIPS forecast for ',a10,3(i2.2),1x,i2.2)
c 
      write(lulg,303) irlag
  303 format(/,' Reynolds SST is ',i4,' hrs old')
c 
      do 12 k=-2,mft
         if (ilat(k) .ge. imiss) then
            rlat(k) = rmiss
         else
            rlat(k) = 0.1*float(ilat(k))
         endif
c 
         if (ilon(k) .ge. imiss) then
            rlon(k) = rmiss
         else
            rlon(k) = 0.1*float(ilon(k))
         endif
   12 continue
c 
c     Calculate the storm translational speed along the forecast track
      do k=-2,mft
         ftimec(k) = delt*float(k)
      enddo
      call tspdcal(rlat,rlon,ftimec,mft,rmiss,cxt,cyt,cmagt)
c
c     Calculate the mpi from the SST or the modified SST
      rlattm = rlat(0)
      ctm    = float(ispeed)/1.944
c 
      do 10 k=0,mft
         sstt = 0.1*float(isst(k))
c 
         if (icione .eq. 2) then
            rlattm = rlat(k)
            ctm    = cmagt(k)/1.944
            if (ctm .gt. 20.0) ctm = 20.0
         else
            rlattm = rlat(0)
            ctm    = float(ispeed)/1.944      
         endif
c
c        Calculate the SST cooling from J. Cione's equation
         ssttc = 1.1222793*sstt + 0.1425625*ctm - 0.0778590*rlattm
     +           -3.3705640
c 
         if (mpispd .eq. 0) then
            call mpical(sstt ,rmpi ,ibasin)
            call mpical(ssttc,rmpic,ibasin)
         else
            call mpicalo(sstt ,rmpi ,ibasin)
            call mpicalo(ssttc,rmpic,ibasin)
c 
            if (cmagt(k) .lt. rmiss .and. cmagt(k) .gt. 0.0) then
               ctemp = cmagt(k)
               if (ctemp .gt. 40.0) ctemp=40.0
               cadj = 1.5*(ctemp**0.63)
               rmpi = rmpi + cadj
               rmpic= rmpic+ cadj
            endif
         endif
c 
         vsst(k)  = rmpi
         vsstc(k) = rmpic
         sst(k)   = sstt
         sstc(k)  = ssttc
c
c        Save appropriate MPI for LGE model
         if (icione .eq. 0) then
            vsstl(k) = rmpi
         else
            vsstl(k) = rmpic
         endif
   10 continue
c
c     Calculate non-time dependent predictors and
c     other related variables 
      vmx       = float(ivmx)
      v(0)      = vmx
      vpert(0)  = vmx
c 
      if (iper .lt. 90) then
         per = float(iper)
      else
         per = 0.0
      endif
c
c     Check to see if storm is now over the ocean but was
c     recently over land. If so, modify the persistence
c     accordingly.
      call lcheck(ilat0,ilon0,ilatm12,ilonm12,12.0,tland,lmod)
      if (lmod .eq. 1 .and. per .lt. 0.0) per = 0.0
c 
      vper = per*vmx
      pslv = float(ipslv(0))
      d200 = float(id200(0))
c
c     Calculate the eastward component of the storm motion at t=0
      speed = float(ispeed)
      head  = float(ihead)
      call rhtoc(speed,head,spdx,spdy)
c
c     Calculate the Julian date
      call jdate(isyr,ismon,isday,jday)
      aday   = abs(float(jday-jdmax))
      if (aday .gt. 182.5) aday = 365.0-aday
c
c     Calculate new ADAY parameter
      raday = (aday/raefld)
      aday = exp(-raday*raday)
c
c     GOES predictors
      pc20    = float(igoes(6))
      pc20m   = float(igoessm(6))
      btstd   = 0.1*float(igoes(2))
      btstdm  = 0.1*float(igoessm(2))
      gstd    = vmx*btstd
c
c     ++ Begin variables for input to the rapid intensity index
      perri  = per
c 
      if (ipgoes .eq. 0) then
         pcri30 = float(igoes(7))
         sbtri  = 0.1*float(igoes(2))
      else
         pcri30 = 999.
         sbtri  = 999.
      endif
c 
      shdcri = 0.1*float(ishdc(0))
      rhlori = float(irhlo(0))
      d200ri = d200
c 
      if (icione .eq. 0) then
          vssttm = vsst(0)
      else
          vssttm = vsstc(0)
      endif
      potri = vssttm-vmx
      rhcri = float(irhcn(0))
c
c     Perform time average of RI variables if necessary
      ic2=1
      ic3=1
      ic4=1
      ic5=1
      ic6=1
      ic7=1
      ic8=1
      do i=1,4
         if (ishdc(i) .lt. 9999) then
            ic7 = ic7+1
            shdcri = shdcri + 0.1*float(ishdc(i))
         endif
c 
         if (icione .eq. 0) then
             vssttm = vsst(i)
         else
             vssttm = vsstc(i)
         endif
c 
         if (vssttm .lt. 200.0) then
            ic3 = ic3+1
            ic4 = ic4+1
            sstri = sstri + sst(i)
            potri = potri + (vssttm-vmx)
         endif
c 
         if (irhlo(i) .lt. 9999) then
            ic5 = ic5+1
            rhlori = rhlori + float(irhlo(i))
         endif
c 
         if (id200(i) .lt. 9999) then
            ic6 = ic6+1
            d200ri = d200ri + float(id200(i))
         endif
c 
         if (irhcn(i) .lt. 9999) then
            ic8 = ic8 + 1
            rhcri = rhcri + float(irhcn(i))
         endif
      enddo
c 
      irimin=1
      if (ic2 .ge. irimin) then
         shrdri = shrdri/float(ic2)
      else
         shrdri = 999.
      endif
c 
      if (ic7 .ge. irimin) then
         shdcri = shdcri/float(ic7)
      else
         shdcri = 999.
      endif
c 
      if (ic5 .ge. irimin) then
         rhlori= rhlori/float(ic5)
      else
         rhlori = 999.
      endif
c 
      if (ic6 .ge. irimin) then
          d200ri=d200ri/float(ic6)
      else
          d200ri = 999.
      endif
c 
      sstri = sstri/float(ic3)
      potri = potri/float(ic4)
      rhcri = rhcri/float(ic8)
c
c     ++ End RI variable input
c
c     Specify the independent variable names
      varlab(1)  = 'VMAX '
      varlab(2)  = 'PER  '
      varlab(3)  = 'ADAY '
      varlab(4)  = 'SPDX '
      varlab(5)  = 'PSLV '
      varlab(6)  = 'VPER '
      varlab(7)  = 'PC20 '
      varlab(8)  = 'GSTD '
      varlab(9)  = 'POT  '
      varlab(10) = 'SHDC '
      varlab(11) = 'T200 '
      varlab(12) = 'T250P'
      varlab(13) = 'EPOS '
      varlab(14) = 'RHMD '
      varlab(15) = 'TWAT '
      varlab(16) = 'Z850 '
      varlab(17) = 'D200 '
      varlab(18) = 'LSHDC'
      varlab(19) = 'VSHDC'
      varlab(20) = 'POT2 '
      varlab(21) = 'RHCN '
      varlab(22) = 'SDIR '
      varlab(23) = 'SHGC '
c
c     Start the forecast time loop
      do 99 kk=1,mft
c
c        Calculate the average mpi 
         vssta = 0.0
         ccount = 0.0
         do 20 k=0,kk
            if (icione .eq. 0) then
               vssttm = vsst(k)
            else
               vssttm = vsstc(k)
            endif
c 
            if (vssttm .lt. 200.0) then
               vssta = vssta + vssttm
               ccount = ccount + 1.0
            endif
   20    continue
c 
         if (ccount .gt. 0.9) then
            vssta = vssta/ccount
         else
            vssta = 100.0
         endif
         tapot = vssta-vmx
c
c        Calculate time averaged OHC
         taohc = 0.0
         ccount= 0.0
         do k=0,kk
            if (irhcn(k) .lt. imiss) then
               taohc = taohc + float(irhcn(k))
               ccount= ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            taohc = taohc/ccount
         else
            taohc = float(iohcsm)
         endif
c 
         taohc = taohc - rthresh
         if (taohc .lt. 0.0) taohc = 0.0
c
c        Calculate the time-averaged shear and talshr
         tashr  = 0.0
         talshr = 0.0
         ccount = 0.0
c 
         do 25 k=0,kk
            if (ishr(k) .lt. 9000 .and. rlat(k) .lt. 900.0) then
	       shrtem = 0.1*float(ishr(k))
c 
               tashr  = tashr  + shrtem
	       talshr = talshr + shrtem*sin(dtr*rlat(k))
               ccount = ccount + 1.0
            endif
   25    continue
c 
         if (ccount .gt. 0.9) then
            tashr  = tashr/ccount
	    talshr = talshr/ccount
         else
            tashr  = 18.0
	    talshr = 7.5
         endif
c
c        Calculate the time-averaged modified shear and lshr
         tashdc  = 0.0
         talshdc = 0.0
         ccount = 0.0
c 
         do k=0,kk
            if (ishdc(k) .lt. 9000 .and. rlat(k) .lt. 900.0) then
	       shrtem = 0.1*float(ishdc(k))
c 
               tashdc  = tashdc  + shrtem
	       talshdc = talshdc + shrtem*sin(dtr*rlat(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tashdc  = tashdc/ccount
	    talshdc = talshdc/ccount
         else
            tashdc  = 18.0
	    talshdc = 7.5
         endif
c
c        Calculate the time-averaged log-transformed shear and lshr
         tashdct  = 0.0
         talshdct = 0.0
         ccount = 0.0
c 
         do k=0,kk
            if (shdct(k) .lt. rmiss .and. rlat(k) .lt. 900.0) then
c 
               tashdct  = tashdct  + shdct(k)
	       talshdct = talshdct + shdct(k)*sin(dtr*rlat(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tashdct  = tashdct/ccount
	    talshdct = talshdct/ccount
         else
            tashdct  = 18.0
	    talshdct = 7.5
         endif
c
c        Calculate time-averaged shear direction variable
         tasdir = 0.0
         ccount = 0.0
c 
         do k=0,kk
            if (sdir(k) .lt. rmiss) then
               tasdir = tasdir + sdir(k)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tasdir = tasdir/ccount
         else
            tasdir = 0.0
         endif
c
c        Calculate time-averaged generalized shear
         tashgc = 0.0
         ccount = 0.0
c 
         do k=0,kk
            if (shgc(k) .lt. rmiss) then
               tashgc = tashgc + shgc(k)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tashgc = tashgc/ccount
         else
            tashgc = 0.0
         endif
c
c        Calculate the time-averaged eddy fluxes
         tarefc  = 0.0
         ccount   = 0.0
c 
         do 26 k=0,kk
            if (irefc(k) .lt. 9000) then
               tarefc = tarefc + float(irefc(k))
               ccount = ccount + 1.0
            endif
   26    continue
c 
         if (ccount .gt. 0.9) then
            tarefc = tarefc/ccount
         else
            tarefc = 0.0
         endif
c
c        Calculate the initial value of eddy fluxes
	 if (irefc(0) .lt. 9000) then
	    refc0 = float(irefc(0))
         else
	    refc0 = 0.0
         endif
c
c        Calculate the time-averaged t200
         tat200  = 0.0
         ccount  = 0.0
c 
         do k=0,kk
            if (it200(k) .lt. 9000) then
               tat200 = tat200 + 0.1*float(it200(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tat200 = tat200/ccount
         else
            tat200 = -53.2
         endif
c
c        Calculate the time-averaged t200 threshold variable
         tat250  = 0.0
         ccount   = 0.0
c 
         do 27 k=0,kk
            if (it250(k) .lt. 9000) then
               t250t = 0.1*float(it250(k))
               t250t = t250t - t250th
               if (t250t .gt. 0.0) t250t = 0.0
               tat250 = tat250 + t250t
               ccount = ccount + 1.0
            endif
   27    continue
c 
         if (ccount .gt. 0.9) then
            tat250 = tat250/ccount
         else
            tat250 = 0.0
         endif
c
c        Calculate the time-averaged u200
         tau200  = 0.0
         ccount   = 0.0
c 
         do 28 k=0,kk
            if (iu200(k) .lt. 9000) then
               tau200 = tau200 + 0.1*float(iu200(k))
               ccount = ccount + 1.0
            endif
   28    continue
c 
         if (ccount .gt. 0.9) then
            tau200 = tau200/ccount
         else
            tau200 = 8.0
         endif
c
c        Calculate the time-averaged z850
         taz850  = 0.0
         ccount   = 0.0
c 
         do k=0,kk
            if (iz850(k) .lt. 9000) then
               taz850 = taz850 + float(iz850(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            taz850 = taz850/ccount
         else
            taz850 = 25.0
         endif
c
c        Calculate the time-averaged d200 
         tad200  = 0.0
         ccount   = 0.0
c 
         do k=0,kk
            if (id200(k) .lt. 9000) then
               tad200 = tad200 + float(id200(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tad200 = tad200/ccount
         else
            tad200 = 0.0
         endif
c
c        Calculate the time-averaged rhlo,rhmd and rhhi
         tarhlo  = 0.0
         tarhmd  = 0.0
         tarhhi  = 0.0
         ccount   = 0.0
c 
         do k=0,kk
            if (irhlo(k) .lt. 9000 .and. irhhi(k) .lt. 9000 .and.
     +          irhmd(k) .lt. 9000) then
               tarhlo = tarhlo + float(irhlo(k))
               tarhmd = tarhmd + float(irhmd(k))
               tarhhi = tarhhi + float(irhhi(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            tarhlo = tarhlo/ccount
            tarhmd = tarhmd/ccount
            tarhhi = tarhhi/ccount
         else
            tarhlo = 65.0
            tarhmd = 53.0
            tarhhi = 45.0
         endif
c
c        Calculate the time-averaged thetae variable (epos)
         taepos  = 0.0
         ccount   = 0.0
c 
         do k=0,kk
            if (iepos(k) .lt. 9000) then
               taepos = taepos + 0.1*float(iepos(k))
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.9) then
            taepos = taepos/ccount
         else
            taepos = 12.0
         endif
c
c        Calculate time tendency of GFS mean tangential wind
         twat = twac(kk)-twac(0)
c
c        Specify the values of the independent variables
         var(1)  = vmx           
         var(2)  = per      
         var(3)  = aday  
         var(4)  = spdx 
         var(5)  = pslv
         var(6)  = vper
         var(7)  = pc20
         var(8)  = gstd
         var(9)  = tapot
         var(10) = tashdct
         var(11) = tat200
         var(12) = tat250
         var(13) = taepos
         var(14) = tarhmd
         var(15) = twat
         var(16) = taz850
         var(17) = tad200
         var(18) = talshdct
	 var(19) = vmx*tashdct
	 var(20) = tapot*tapot
	 var(21) = taohc
	 var(22) = tasdir
         var(23) = tashgc
c
c        Normalize the independent variables
         do 29 j=1,nvar
            var(j) = (var(j) - xbar(j,kk))/xsig(j,kk)
   29    continue
c
c        Save variable values for later output
	 do 31 j=1,nvar
            vart(j,kk) = var(j)
   31    continue
c
c        Calculate the intensity change
         delv(kk) = 0.0
         do 30 n=1,nvar
            delv(kk) = delv(kk) + var(n)*coef(n,kk)
   30    continue
         delv(kk) = ybar(kk) + delv(kk)*ysig(kk)
         v(kk) = vmx + delv(kk)
c
c        Initialze perturbation forecast with original forecast
	 vpert(kk) = v(kk)
c 
         write(lulg,300) kk*idelt,vmx,v(kk),delv(kk)
  300    format(//,1x,i3,' hr forecast, v(0)=',f5.1,'  v=',f6.1,
     +                                             ' dv=',f6.1,/)
         do 35 n=1,nvar
            write(lulg,305) n,varlab(n),var(n),coef(n,kk),
     +                                  var(n)*coef(n,kk),
     +                                  var(n)*coef(n,kk)*ysig(kk)
  305       format(1x,i2,1x,a5,' var=',f8.2,'  coef=',f9.4,
     +                           ' dvn=',f6.1,'  dv=',f6.1)
   35    continue
   99 continue      
c
c     Check the forecast for dissipation
      do 40 k=1,mft
         if (v(k) .lt. vdiss) then
	    do kk=k,mft
	       v(kk) = 0.0
            enddo
	    go to 2040
         endif
   40 continue
 2040 continue
c
c     Write the forecast to integer array for output
      iv(0) = ifix(v(0))
      do 45 k=1,mft
         iv(k)  = ifix(v(k)  + 0.49)
   45 continue
c
c     Write required predictors 
c     to character array for later output
      do 50 k=0,mft
         if (ishr(k) .lt. 0 .or. ishr(k) .gt. 9000
     +                      .or.       k .gt. ishrx)   then
            cshr(k) = ' N/A'
         else
            shrt  = 0.1*float(ishr(k))
            ishrt = ifix(shrt +0.49)
            write(cshr(k), 200) ishrt
  200       format(i4)
         endif
c 
         if (ishdc(k) .lt. 0 .or. ishdc(k) .gt. 9000
     +                      .or.       k .gt. ishrx)   then
            cshdc(k) = ' N/A'
         else
            shrt  = 0.1*float(ishdc(k))
            ishrt = ifix(shrt +0.49)
            write(cshdc(k), 200) ishrt
         endif
c 
         if (ishgc(k) .gt. 9000
     +                      .or.       k .gt. ishrx)   then
            cshgc(k) = ' N/A'
         else
            shrt  = shgc(k)
            ishrt = ifix(shrt +0.49)
            write(cshgc(k), 200) ishrt
         endif
c 
         if (ishtd(k) .gt. 9000) then
            cshtd(k) = ' N/A'
         else
            write(cshtd(k), 200) ishtd(k)
         endif
c 
         if (irefc(k) .gt. 9000 .or. k .gt. irefcx) then
            crefc(k)= ' N/A'
         else
            refct  = float(irefc(k))
            irefct = ifix(refct+0.49)
            write(crefc(k), 200) irefct
         endif
c 
         if (it200(k) .gt. 9000 .or. k .gt. it200x) then
            ct200(k)= '  N/A'
         else
            t200t  = 0.1*float(it200(k))
            write(ct200(k),210) t200t
         endif
c 
	 if (iu200(k) .gt. 9000) then
	    cu200(k) = ' N/A'
         else
	    iu200t = ifix(0.1*iu200(k))
	    write(cu200(k), 200) iu200t
         endif
c 
	 if (irhlo(k) .gt. 9000) then
	    crhlo(k) = ' N/A'
         else
	    write(crhlo(k), 200) irhlo(k)
         endif
c 
	 if (irhhi(k) .gt. 9000) then
	    crhhi(k) = ' N/A'
         else
	    write(crhhi(k), 200) irhhi(k)
         endif
c 
	 if (irhmd(k) .gt. 9000) then
	    crhmd(k) = ' N/A'
         else
	    write(crhmd(k), 200) irhmd(k)
         endif
c 
	 if (iepos(k) .gt. 9000) then
	    cepos(k) = ' N/A'
         else
	    iepost = ifix(0.1*iepos(k))
	    write(cepos(k), 200) iepost
         endif
c 
	 if (iz850(k) .gt. 9000) then
	    cz850(k) = ' N/A'
         else
	    write(cz850(k), 200) iz850(k)
         endif
c 
	 if (id200(k) .gt. 9000) then
	    cd200(k) = ' N/A'
         else
	    write(cd200(k), 200) id200(k)
         endif
c 
         if (ivmaxb(k) .gt. 9000) then
            cvmaxb(k) = ' N/A'
         else
            write(cvmaxb(k), 200) ivmaxb(k)
         endif
c 
   50 continue
c           
c     Write the sst and mpi to character arrays for output.
c     Similarly for dist,lat,lon
      do 55 k=0,mft
         if (sst(k) .gt. 50.0) then
            csst(k) = ' N/A'
         else
            write(csst(k),205) sst(k)
  205       format(f4.1)
         endif
c   
         if (vsst(k) .gt. 200.0) then
            cvsst(k) = ' N/A'
         else
            ivsst = ifix(0.49 + vsst(k))
            write(cvsst(k),200)  ivsst
         endif
c 
         if (vsstc(k) .gt. 200.0) then
            cvsstc(k) = ' N/A'
         else
            ivsstc = ifix(0.49 + vsstc(k))
            write(cvsstc(k),200)  ivsstc
         endif
c 
         if (idist(k) .gt. 9000) then
            cdist(k) = ' N/A'
         else
            write(cdist(k),200) idist(k)
         endif
c 
         if (rlat(k) .gt. 900.0 .or. rlon(k) .gt. 900.0) then
            clat(k) =  ' N/A'
            clon(k) = '  N/A'
         else
            write(clat(k),205) rlat(k)
            write(clon(k),210) rlon(k)
  210       format(f5.1)
         endif
c 
         if (cmagt(k) .ge. rmiss) then
            cmagc(k) = ' N/A'
         else
            icmag = ifix(cmagt(k)+0.49)
            write(cmagc(k),200) icmag
         endif
   55 continue
c
c     Put track in an array for inclusion in atcf file
      do 56 i=0,mft
         ilatt(i) = ifix(10.0*rlat(i))
         ilont(i) = ifix(10.0*rlon(i))
c 
         if (ilatt(i) .gt. 9000 .or. ilont(i) .gt. 9000) then
	    ilatt(i) = 0
	    ilont(i) = 0
         endif
   56 continue
c           
c     Run the decay model to include land effects
      do i=1,mft+1
	 ftime(i) = 0.0
	 rlatd(i) = 0.0
	 rlond(i) = 0.0
	 vmaxo(i) = 0.0
	 vmaxd(i) = 0.0
	 ddland(i) = 0.0
      enddo
c 
      do i=0,mft
         ftime(i+1) = delt*float(i)
c 
	 if (v(i) .ge. vdiss) then
	    vmaxo(i+1) = v(i)
         else
	    vmaxo(i+1) = 0.0
         endif
c 
         if (rlat(i) .lt. 999. .and. rlon(i) .lt. 999.) then
	    rlatd(i+1) = rlat(i)
            rlond(i+1) = rlon(i)
         else
	    rlatd(i+1) = 0.0
	    rlond(i+1) = 0.0
         endif
      enddo
c
c     Use persistence for cases with v, but with missing lat/lon
      do 72 k=2,mft+1
         if ( vmaxo(k) .gt. 0.0 .and.
     +       (rlatd(k) .le. 0.0 .or. rlond(k) .le. 0.0) ) then
             do 73 kk=k,mft+1
                rlatd(kk) = rlatd(k-1)
                rlond(kk) = rlond(k-1)
   73        continue
c 
             go to 2000
         endif
   72 continue
 2000 continue
c 
      call decay(ftime,rlatd,rlond,vmaxo,vmaxd,ddland,lulg)
c 
      do i=1,mft+1
	 ivd(i-1) = ifix(vmaxd(i) + 0.49)
	 if (i .ne. 1 .and. ivd(i-1) .lt. ivdiss) ivd(i-1)=0
      enddo
c 
c     Write no-perturbation SHIPS forecasts in a modified form of the old ATCF format
c     to ships.tst file
      if (ioper .eq. 1) then
         if (iperts .eq. 1) then
            slab = '98SHNS'
         else
            slab = '98SHIP'
         endif
      else
         if (iperts .eq. 1) then
            slab = '92SNxx'
         else
            slab = '92SHxx'
         endif
         slab(5:6) = runid
      endif
c 
      write(luts,400) slab,isyr,ismon,isday,istime,
     +                (ilatt(i),ilont(i),i=2,mft,2),
     +                (iv(k),k=2,mft,2),natcf
c 
      if (ioper .eq. 1) then
         if (iperts .eq. 1) then
            slab = '98DSNS'
         else
            slab = '98DSHP'
         endif
      else
         if (iperts .eq. 1) then
            slab = '92DNxx'
         else
            slab = '92DSxx'
         endif
         slab(5:6) = runid
      endif
c 
      write(luts,400) slab,isyr,ismon,isday,istime,
     +                (ilatt(i),ilont(i),i=2,mft,2),
     +                (ivd(k),k=2,mft,2),natcf
  400 format(a6,4(i2.2),20(i4),10(i3),1x,a6)
c     write(luts,401) slab,sname4,isyr,ismon,isday,istime,
c    +                (ilatt(i),ilont(i),i=2,mft,2),
c    +                (ivd(k),k=0,mft,2),(ivmaxb(k),k=0,mft,2)
c 401 format(a6,1x,a4,1x,4(i2.2),11(1x,i3),1x,'BEST',11(1x,i3))
c
c     close(luts)
c
c     Write no-perturbation SHIPS forecasts in the new ATCF format to ships.dat file
      if (isyr .lt. 50) then
	 isyr4 = isyr + 2000
      else
	 isyr4 = isyr + 1900
      endif
      write(aymdh,600) isyr4,ismon,isday,istime
  600 format(i4.4,3(i2.2))
c 
      strmid(1:4)=natcf(1:4)
      write(strmid(5:8),601) isyr4
  601 format(i4.4)
c
c     SHIPS (no perturbation)
      kkount=0
      do k=1,mft+1,2
         kkount=kkount+1
	 ifship(kkount,1) = ilatt(k-1)
	 ifship(kkount,2) = ilont(k-1)
	 ifship(kkount,3) = iv(k-1)
      enddo
c 
      if (iperts .eq. 1) then
         call newWriteAidRcd(luat,strmid,aymdh,"SHNS",ifship)
      else
         if (imodel .eq. 1) then
            !Change model name in output to xxxxS (SHIPS run on model xxx)

C mf option for 5-char techname

           if(do5charname.eq.1) then
             tem5(1:4) = tmname(1:4)
             tem5(5:5) = 'S'
             call newWriteAidRcd5(luat,strmid,aymdh,tem5,ifship)
           else
             tem4(1:3) = tmname(1:3)
             tem4(4:4) = 'S'
             call newWriteAidRcd(luat,strmid,aymdh,tem4,ifship)
           endif

         else
            call newWriteAidRcd(luat,strmid,aymdh,"SHIP",ifship)
         endif
      endif
c
c     Decay SHIPS (no perturbation)
      kkount=0
      do k=1,mft+1,2
         kkount=kkount+1
	 ifship(kkount,3) = ivd(k-1)
      enddo
      if (iperts .eq. 1) then
         call newWriteAidRcd(luat,strmid,aymdh,"DSNS",ifship)
      else
         if (imodel .eq. 1) then
            !Change model name in output to xxxD (decay SHIPS run on model xxx)


C         mf option for 5-char techname

           if(do5charname.eq.1) then
             tem5(1:4) = tmname(1:4)
             tem5(5:5) = 'D'
             call newWriteAidRcd5(luat,strmid,aymdh,tem5,ifship)
           else
             tem4(1:3) = tmname(1:3)
             tem4(4:4) = 'D'
             call newWriteAidRcd(luat,strmid,aymdh,tem4,ifship)
           endif

         else
            call newWriteAidRcd(luat,strmid,aymdh,"DSHP",ifship)
         endif
      endif
c
c     Write intensities to character array for later output
      write( cv(0),200)  iv(0)
      write(cvd(0),200) ivd(0)
c 
      do k=1,mft
         if (iv(k) .ge. ivdiss) then
            write(cv(k),200) iv(k)
         else
            cv(k) = ' DIS'
         endif
c 
         if (ivd(k) .ge. ivdiss) then
            write(cvd(k),200) ivd(k)
         else
            cvd(k) = ' DIS'
         endif
      enddo
c
c     **** End of no perturbation version of SHIPS ****
c
c     **** Start perturbation SHIPS forecast (satellite as corretion terms) ****
c
c     Initialize iperr error flag 
      iperr=1
c 
      if (iperts .eq. 1) then
c        Modify forecast based upon GOES data (EP)
c        or modify based upon GOES/OHC data (AL)
c 
         if (ibasin .eq. 1) then
            if (ioper .eq. 1) then
               fncop = trim( coef_location ) // 'shipp08_coef_atlc.dat'
            else
               fncop = 'shipp08_coef_atlc.dat'
            endif
            nvarpt = 3
         else
            if (ioper .eq. 1) then
               fncop = trim( coef_location ) // 'shipp08_coef_epac.dat'
            else
               fncop = 'shipp08_coef_epac.dat'
            endif
            nvarpt = 2
         endif
c   
         open(unit=lucop,file=fncop,form='formatted',status='old',
     +        err=890)
c
c        Read the coefficient file
         do k=1,mft
            read(lucop,135) ybarp(k),ysigp(k)
c      
            do n=1,nvarpt
               read(lucop,136,err=890) coefp(n,k),xbarp(n,k),xsigp(n,k)
            enddo
         enddo
c 
         if (ibasin .eq. 1) then
c           Check to make sure at least one OHC value is available
	    if (irhcn(0) .ge. imiss) go to 890 
         endif
c 
         if (igoes(2) .ge. imiss .or. igoes(4) .ge. imiss .or.
     +       igoes(6) .ge. imiss .or. igoes(7) .ge. imiss .or.
     +                               igoes(10) .ge. imiss      ) then
            igoes(2) = igoesm3(2)
            igoes(4) = igoesm3(4)
            igoes(6) = igoesm3(6)
            igoes(7) = igoesm3(7)
            igoes(10) = igoesm3(10)
            if (igoes(4) .ge. imiss .or. igoes(6) .ge. imiss) then
               do ii=0,mft
                  igoes(ii) = imiss
               enddo
               go to 890
            endif
         endif
c
c        Check GOES standard deviation variable to see if 
c        it unreasonably large (+/- 3sigma)
         stdck = abs(vmx*0.1*float(igoes(4))-1000.0)/450.0
c 
         write(lulg,814) vmx,igoes(4),stdck
  814    format(/,' GOES std chk: vmx, igoes4, stdck=',
     +                               f5.0,1x,i4,1x,f6.2)
c 
         if (stdck .gt. 3.0) then
            do ii=0,mft
               igoes(ii) = imiss
            enddo
            go to 890
         endif
c
c        Perform buddy check of GOES data if possible
         it1 = igoes(1)
         is1 = igoes(2)
         it2 = igoesm3(1)
         is2 = igoesm3(2)
c 
         if (it1 .lt. 9000 .and. it2 .lt. 9000 .and.
     +       is1 .lt. 9000 .and. is2 .lt. 9000       ) then
            adt = 0.1*abs(float(it2-it1))
            ads = 0.1*abs(float(is2-is1))
c 
            write(lulg,815) it1,it2,is1,is2,adt,ads
  815       format(/,' GOES buddy check input: ',4(i4,1x),2(f6.1,1x))
c
c           If dt or ds too large, one of the GOES profiles is bad
            if (adt .gt. 40.0 .or. ads .gt. 20.0) then
               do ii=0,mft
                  igoes(ii) = imiss
               enddo
               go to 890
            endif
         endif
c
c        Specify mean value of BT std dev and pixel count
         pc20m  = xbarp(2,1)
	 if (ibasin .eq. 1) then
             btstdm = 20.0
         else
	     btstdm = 18.0
         endif
c
c        Start perturbation forecast time loop
	 do 199 kk=1,mft
c
c            Get the GOES variables
	     if (igoes(4) .ge. imiss .or. igoes(6) .ge. imiss) then
		btstd = btstdm
	        vbtstd= xbarp(1,kk)
	        pc20  = xbarp(2,kk)
		pc20p = pc20m
             else
                btstd  =     0.1*float(igoes(4))
	        vbtstd = vmx*0.1*float(igoes(4))
	        pc20   =         float(igoes(6))
		pc20p  = pc20
             endif
c
c            Calculate the time-averaged rhcn (ocean heat content)
             tarhcn = 0.0
             ccount  = 0.0
c 
             do k=0,kk
                if (irhcn(k) .lt. 9000) then
	           rhcntem = float(irhcn(k))
                   tarhcn  = tarhcn  + rhcntem
                   ccount = ccount + 1.0
                endif
             enddo
c 
             if (ccount .gt. 0.9) tarhcn = tarhcn/ccount 
c
c            Apply threshold to time-averaged ocean heat content
	     tarhcn = tarhcn-rthresh
	     if (tarhcn .lt. 0.0) tarhcn = 0.0
c 
	     var(1) = vbtstd
	     var(2) = pc20
             var(3) = tarhcn
c 
c            Normalize the independent variables
c            and save the values for later output
             do j=1,nvarpt
                var(j) = (var(j) - xbarp(j,kk))/xsigp(j,kk)
                vartp(j,kk) = var(j)
	     enddo
c
c            var(1) = 0.0
c            var(2) = 0.0
c            vartp(1,kk) = 0.0
c            vartp(2,kk) = 0.0
c
c            var(3) = 0.0
c            vartp(3,kk) = 0.0
c
c            Calculate the intensity change
             delvp(kk) = 0.0
             do n=1,nvarpt
                delvp(kk) = delvp(kk) + var(n)*coefp(n,kk)
             enddo
             delvp(kk) = ybarp(kk) + delvp(kk)*ysigp(kk)
c 
c            write(6,888) kk*12,delvp(kk),tarhcn,(var(mm),mm=1,nvarpt)
c 888        format(i3,1x,6(f6.2,1x))
  199    continue
c
c        Add the perturbation intensity changes to the SHIPS forecast
         do k=1,mft
	    vpert(k) = vpert(k) + delvp(k)
         enddo
c 
         iperr=0
      endif
c
c     Jump to here is there is a problem with the forecasts mod section
  890 continue
c 
      if (iperts .ne. 1) then
c        Skip writing perturbation forecast if there is none
         go to 3000
      endif
c
c     Check perturbation forecast for dissipation
      do k=1,mft
	 if (vpert(k) .lt. vdiss) then
	    do kk=k,mft
	       vpert(k) = 0.0
            enddo
	    go to 2041
         endif
      enddo
 2041 continue
c
c     Copy perturbation forecast to output array whether the perturbation
c     model ran or not. If it did not run, the perturbation forecast will
c     equal the original forecast
c 
      do k=1,mft
         iv(k) = ifix(0.49 + vpert(k))
         if (vpert(k) .lt. vdiss) then
            iv(k) = 0
         endif
      enddo
c
c     Write the perturbation SHIPS forecast to the ATCF 
      kkount = 0
      do k=1,mft+1,2
         kkount = kkount + 1
         ifship(kkount,3) = iv(k-1)
      enddo
      call newWriteAidRcd(luat,strmid,aymdh,"SHIP",ifship)
c
c     Run the decay model to include land effects 
c     in the perturbation SHIPS forecast
      do i=1,mft+1
         vmaxo(i) = 0.0
         vmaxd(i) = 0.0
         rlatd(i) = 0.0
         rlond(i) = 0.0
         ddland(i) = 0.0
      enddo
c 
      do i=0,mft
         if (vpert(i) .ge. vdiss) then
            vmaxo(i+1) = vpert(i)
         else
            vmaxo(i+1) = 0.0
         endif
c 
         if (rlat(i) .lt. 999. .and. rlon(i) .lt. 999.) then
            rlatd(i+1) = rlat(i)
            rlond(i+1) = rlon(i)
         else
            rlatd(i+1) = 0.0
            rlond(i+1) = 0.0
         endif
      enddo
c
c     Use persistence for cases with v, but with missing lat/lon
      do 82 k=2,mft+1
         if ( vmaxo(k) .gt. 0.0 .and.
     +      (rlatd(k) .le. 0.0 .or. rlond(k) .le. 0.0) ) then
               do 83 kk=k,mft+1
                  rlatd(kk) = rlatd(k-1)
                  rlond(kk) = rlond(k-1)
   83          continue
c 
            go to 2002
         endif
   82 continue
 2002 continue
c 
      call decay(ftime,rlatd,rlond,vmaxo,vmaxd,ddland,lulg)
c 
      do i=1,mft+1
         ivd(i-1) = ifix(vmaxd(i) + 0.49)
         if (i .ne. 1 .and. ivd(i-1) .lt. ivdiss) ivd(i-1)=0
      enddo
c 
c     Write perturbation Decay SHIPS to the ATCF
      kkount=0
      do k=1,mft+1,2
         kkount=kkount+1
         ifship(kkount,3) = ivd(k-1)
      enddo
      call newWriteAidRcd(luat,strmid,aymdh,"DSHP",ifship)
c
c     Write perturbation forecasts in a modified form 
c     of the old ATCF format to the ships.tst file
      if (ioper .eq. 1) then
         slab = '98SHIP'
      else
         slab = '92SH05'
         slab(5:6) = runid
      endif
c 
      write(luts,400) slab,isyr,ismon,isday,istime,
     +                (ilatt(i),ilont(i),i=2,mft,2),
     +                (iv(k),k=2,mft,2),natcf
c 
      if (ioper .eq. 1) then
         slab = '98DSHP'
      else
         slab = '92DSxx'
         slab(5:6) = runid
      endif
c 
      write(luts,400) slab,isyr,ismon,isday,istime,
     +                (ilatt(i),ilont(i),i=2,mft,2),
     +                (ivd(k),k=2,mft,2),natcf
c
c     Write intensities to character array for later output
      write( cv(0),200)  iv(0)
      write(cvd(0),200) ivd(0)
c 
      do 75 k=1,mft
         if (iv(k) .ge. ivdiss) then
            write(cv(k),200) iv(k)
         else
            cv(k) = ' DIS'
         endif
c 
         if (ivd(k) .ge. ivdiss) then
            write(cvd(k),200) ivd(k)
         else
            cvd(k) = ' DIS'
         endif
   75 continue
c
c     **** End of perturbation SHIPS forecast ****
 3000 continue
c
c     **** LGE Model ****
c
c     Initialize LGE forecast to zero
      nftl = mft+1
      do k=1,nftl 
         vmaxl(k) = 0.0
      enddo
c 
      call lgecal(ibasin,nftl,ftime,vdiss,vmaxl,ierr,lulg,rmiss,
     +            imiss,ioper)
c
c     ++ LGE model output
      do i=1,mft+1
         ivl(i-1) = ifix(vmaxl(i) + 0.49)
      enddo
c 
c     Write LGE forecast to the ATCF
      kkount=0
      do k=1,mft+1,2
         kkount=kkount+1
         ifship(kkount,3) = ivl(k-1)
      enddo
      if (imodel .eq. 1) then
         !Change model name in output to xxxG (LGEM run on model xxx)

C         mf option for 5-char techname

        if(do5charname.eq.1) then
          tem5(1:4) = tmname(1:4)
          tem5(5:5) = 'G'
          call newWriteAidRcd5(luat,strmid,aymdh,tem5,ifship)
        else
          tem4(1:3) = tmname(1:3)
          tem4(4:4) = 'G'
          call newWriteAidRcd(luat,strmid,aymdh,tem4,ifship)
        endif

      else
         call newWriteAidRcd(luat,strmid,aymdh,"LGEM",ifship)
      endif
c
c     Write LGE forecast in a modified form 
c     of the old ATCF format to the ships.tst file
      if (ioper .eq. 1) then
         slab = '98LGEM'
      else
         slab = '92LGxx'
         slab(5:6) = runid
      endif
c 
      write(luts,400) slab,isyr,ismon,isday,istime,
     +                (ilatt(i),ilont(i),i=2,mft,2),
     +                (ivl(k),k=2,mft,2),natcf
c     write(luts,401) slab,sname4,isyr,ismon,isday,istime,
c    +                (ivl(k),k=0,mft,2),(ivmaxb(k),k=0,mft,2)
      close(luts)
c
c     Write intensities to character array for later output
      write(cvl(0),200) ivl(0)
c 
      do k=1,mft
c 
         if (ivl(k) .gt. 0) then
            write(cvl(k),200) ivl(k)
         else
            cvl(k) = ' DIS'
         endif
      enddo
c
c     **** End LGE Model ****
c
c     **** Begin SHIPS text file section ****
c
c     Write GFS Vortex mean tangential wind to an array for printing
      do k=0,mft
         if (itwac(k) .eq. imiss) then
            ctwac(k) = 'LOST'
         else
            ttem = 1.944*0.1*float(itwac(k))
            ittem= ifix(ttem)
            write(ctwac(k),701) ittem
  701       format(i4)
         endif
      enddo
c
c     write(lush,500) 
c 500 format(   20x,'*********************************************')
      if (ibasin .eq. 2) then
         write(lush,502)
c        PARMOD
  502    format(20x,'*   EAST PACIFIC SHIPS INTENSITY FORECAST   *' )
c  502    format(20x,'*   EPAC RAPID INTENSITY INDEX TESTS        *' )
c
c         if (iperr .eq. 0) then
c         write(lush,503)
c  503    format(20x,'*        GOES INPUT INCLUDED                *' )
c	 else
c         write(lush,504)
c  504    format(20x,'*        GOES INPUT MISSING                 *' )
c	 endif
      else
         write(lush,505)
c        PARMOD
  505    format(20x,'*   ATLANTIC SHIPS INTENSITY FORECAST       *' )
c  505    format(20x,'*   ATLC RAPID INTENSITY INDEX TESTS        *' )
c
c         if (iperr .eq. 0) then
c         write(lush,506)
c  506    format(20x,'*        GOES/OHC INPUT INCLUDED            *' )
c	 else
c         write(lush,507)
c  507    format(20x,'*     GOES AND/OR OHC INPUT MISSING         *' )
c	 endif
      endif 
c 
      if (ipgoes .eq. 0) then
         write(lush,503)
  503    format(20x,'*      GOES DATA AVAILABLE                  *' )
      else
         write(lush,504)
  504    format(20x,'*      GOES DATA MISSING, PROXY USED        *' )
      endif
c 
      if (ipohc .le. 1) then
         write(lush,506)
  506    format(20x,'*      OHC  DATA AVAILABLE                  *' )
      else
         write(lush,507)
  507    format(20x,'*      OHC  DATA MISSING, PROXY USED        *' )
      endif
c
c     write(lush,500)
c 
      write(lush,508) sname,natcf8,ismon,isday,isyr,istime
  508 format(20x,'*',2x,a10,2x,a8,2x,i2.2,'/',i2.2,'/',i2.2,2x,
     +                                        i2.2,' UTC   *')
c
c     PARMOD
      if (ishp .eq. 0) go to 7000
c 
      write(lush,510) (i*6,i=0,4),(i*6,i=6,mft,2)
  510 format(/,
     +       'TIME (HR)     ',21(3x,i3))
      write(lush,512) (cv(i),i=0,4),(cv(i),i=6,mft,2)
  512 format('V (KT) NO LAND',21(2x,a4))
      write(lush,514) (cvd(i),i=0,4),(cvd(i),i=6,mft,2)
  514 format('V (KT) LAND   ',21(2x,a4))
      write(lush,515) (cvl(i),i=0,4),(cvl(i),i=6,mft,2)
  515 format('V (KT) LGE mod',21(2x,a4))
      if (imodel .eq. 1) then
         write(lush,511) tmname,(cvmaxb(i),i=0,4),
     +                   (cvmaxb(i),i=6,mft,2)
  511    format('V (KT) ',a4,'   ',21(2x,a4))
      endif
c 
      write(lush,516) (cshdc(i),i=0,4),(cshdc(i),i=6,mft,2)
  516 format(/,
     +       'SHEAR (KT)    ',21(2x,a4))
      write(lush,519) (cshgc(i),i=0,4),(cshgc(i),i=6,mft,2)
  519 format('SHEAR ADJ (KT)',21(2x,a4))
      write(lush,517) (cshtd(i),i=0,4),(cshtd(i),i=6,mft,2)
  517 format('SHEAR DIR     ',21(2x,a4))
      write(lush,520) (csst(i),i=0,4),(csst(i),i=6,mft,2)
  520 format('SST (C)       ',21(2x,a4))
      write(lush,522) (cvsst(i),i=0,4),(cvsst(i),i=6,mft,2)
  522 format('POT. INT. (KT)',21(2x,a4))
      if (icione .ne. 0) then
         write(lush,523) (cvsstc(i),i=0,4),(cvsstc(i),i=6,mft,2)
  523    format('ADJ. POT. INT.',21(2x,a4))
      endif
      write(lush,524) (ct200(i),i=0,4),(ct200(i),i=6,mft,2)
  524 format('200 MB T (C)  ',21(1x,a5))
      write(lush,526) (cepos(i),i=0,4),(cepos(i),i=6,mft,2)
  526 format('TH_E DEV (C)  ',21(2x,a4))
      write(lush,528) (crhmd(i),i=0,4),(crhmd(i),i=6,mft,2)
  528 format('700-500 MB RH ',21(2x,a4))
c     write(lush,518) (crefc(i),i=0,4),(crefc(i),i=6,mft,2)
c 518 format('MO FLX (M/S/D)',21(2x,a4))
      write(lush,529) (ctwac(i),i=0,4),(ctwac(i),i=6,mft,2)
  529 format('GFS VTEX (KT) ',21(2x,a4))
      write(lush,533) (cz850(i),i=0,4),(cz850(i),i=6,mft,2)
  533 format('850 MB ENV VOR',21(2x,a4))
      write(lush,531) (cd200(i),i=0,4),(cd200(i),i=6,mft,2)
  531 format('200 MB DIV    ',21(2x,a4))
      write(lush,530) (cdist(i),i=0,4),(cdist(i),i=6,mft,2)
  530 format('LAND (KM)     ',21(2x,a4))
      write(lush,532) (clat(i),i=0,4),(clat(i),i=6,mft,2)
  532 format('LAT (DEG N)   ',21(2x,a4))
      write(lush,534) (clon(i),i=0,4),(clon(i),i=6,mft,2)
  534 format('LONG(DEG W)   ',21(1x,a5))
      write(lush,535) (cmagc(i),i=0,4),(cmagc(i),i=6,mft,2)
  535 format('STM SPEED (KT)',21(1x,a5))
      write(lush,716) (irhcn(i),i=0,4),(irhcn(i),i=6,mft,2)
  716 format('HEAT CONTENT  ',21(2x,i4))
c 
      ispdx = ifix(spdx+0.5)
      ispdy = ifix(spdy+0.5)
      ipslvm = ifix(xbar(5,1))
c 
      write(lush,536) tmname,ihead,ispeed,ispdx,ispdy
  536 format(/,'  FORECAST TRACK FROM ',a4,
     +         '      INITIAL HEADING/SPEED (DEG/KT):',I3,'/',I3,
     +       '      CX,CY: ',i3,'/',i3)
c 
      write(lush,542) ivmxm12,ipslv(0),ipslvm
  542 format('  T-12 MAX WIND: ',i3,
     +       '            PRESSURE OF STEERING LEVEL (MB): ',i4,
     +               '  (MEAN=',i3,')')
c 
      write(lush,718) btstd,btstdm
  718 format('  GOES IR BRIGHTNESS TEMP. STD DEV.  50-200 KM RAD: ',
     +                                      f5.1,' (MEAN=',f4.1,')')
      write(lush,720) pc20,pc20m
  720 format('  % GOES IR PIXELS WITH T < -20 C    50-200 KM RAD: ',
     +                                      f5.1,' (MEAN=',f4.1,')')
c
c     Set iarr=1 to print array showing contributions to
c     intensity change from individual variables, 
c     else set iarr=0
      iarr=1
c 
      if (iarr .eq. 1) then
c        Calculate contributions to intensity change from various variables
c        or groups of variables. 
c        Note: This section of code depends on specific order of 
c              independent variables
c
c        Specify labels for variables
         ngrp = 17 
         cdvlab(1) = 'SAMPLE MEAN CHANGE  '
         cdvlab(2) = 'SST POTENTIAL       '
         cdvlab(3) = 'VERTICAL SHEAR MAG  '
         cdvlab(4) = 'VERTICAL SHEAR ADJ  '
         cdvlab(5) = 'VERTICAL SHEAR DIR  '
         cdvlab(6) = 'PERSISTENCE         '
         cdvlab(7) = '200/250 MB TEMP.    '
         cdvlab(8) = 'THETA_E EXCESS      '
         cdvlab(9) = '700-500 MB RH       '
         cdvlab(10)= 'GFS VORTEX TENDENCY '
         cdvlab(11)= '850 MB ENV VORTICITY'
         cdvlab(12)= '200 MB DIVERGENCE   '
         cdvlab(13)= 'ZONAL STORM MOTION  '
         cdvlab(14)= 'STEERING LEVEL PRES '
         cdvlab(15)= 'DAYS FROM CLIM. PEAK'
         cdvlab(16)= 'GOES PREDICTORS     '
         cdvlab(17)= 'OCEAN HEAT CONTENT  '
c
c        Calculate intensity change contributions
         do 60 kk=1,mft
            dvvar( 1,kk) = ybar(kk)
            dvvar( 2,kk) = vart( 1,kk)*coef( 1,kk)*ysig(kk) +
     +                     vart( 9,kk)*coef( 9,kk)*ysig(kk) +
     +                     vart(20,kk)*coef(20,kk)*ysig(kk)
            dvvar( 3,kk) = vart(10,kk)*coef(10,kk)*ysig(kk) +
     +                     vart(18,kk)*coef(18,kk)*ysig(kk) +
     +                     vart(19,kk)*coef(19,kk)*ysig(kk)
            dvvar( 4,kk) = vart(23,kk)*coef(23,kk)*ysig(kk)
            dvvar( 5,kk) = vart(22,kk)*coef(22,kk)*ysig(kk)
            dvvar( 6,kk) = vart( 2,kk)*coef( 2,kk)*ysig(kk) +
     +                     vart( 6,kk)*coef( 6,kk)*ysig(kk)
            dvvar( 7,kk) = vart(11,kk)*coef(11,kk)*ysig(kk) +
     +                     vart(12,kk)*coef(12,kk)*ysig(kk)
            dvvar( 8,kk) = vart(13,kk)*coef(13,kk)*ysig(kk) 
            dvvar( 9,kk) = vart(14,kk)*coef(14,kk)*ysig(kk) 
            dvvar(10,kk) = vart(15,kk)*coef(15,kk)*ysig(kk) 
            dvvar(11,kk) = vart(16,kk)*coef(16,kk)*ysig(kk) 
            dvvar(12,kk) = vart(17,kk)*coef(17,kk)*ysig(kk) 
            dvvar(13,kk) = vart( 4,kk)*coef( 4,kk)*ysig(kk) 
            dvvar(14,kk) = vart( 5,kk)*coef( 5,kk)*ysig(kk) 
            dvvar(15,kk) = vart( 3,kk)*coef( 3,kk)*ysig(kk) 
            dvvar(16,kk) = vart( 7,kk)*coef( 7,kk)*ysig(kk)+
     +                     vart( 8,kk)*coef( 8,kk)*ysig(kk)
            dvvar(17,kk) = vart(21,kk)*coef(21,kk)*ysig(kk)
c
c           do n=1,nvar
c           write(lulg,305) n,varlab(n),var(n),coef(n,kk),
c    +                                  var(n)*coef(n,kk),
c    +                                  var(n)*coef(n,kk)*ysig(kk)
c           enddo
   60    continue
c
c        Print IC array
         write(lush,570)
  570    format(/,24x,'INDIVIDUAL CONTRIBUTIONS TO INTENSITY CHANGE')
c 
         write(lush,572) (kk*6,kk=1,4),(kk*6,kk=6,mft,2)
  572    format(22x,20(1x,i3,1x))
         write(lush,574)
  574    format(24x,
     +   '----------------------------------------------------------')
         do 62 i=1,ngrp
            write(lush,576) cdvlab(i),(dvvar(i,kk),kk=1,4),
     +                                (dvvar(i,kk),kk=6,mft,2)
  576       format(2x,a20,20(f5.0))
   62    continue
c 
         write(lush,574)
         if (iperts .eq. 1) then
            write(lush,578) (delv(kk),kk=1,4),(delv(kk),kk=6,mft,2)
  578       format(2x,'SUB-TOTAL CHANGE',4x,20(f5.0))
         else
            write(lush,579) (delv(kk),kk=1,4),(delv(kk),kk=6,mft,2)
  579       format(2x,'TOTAL CHANGE    ',4x,20(f5.0))
c 
         endif
         
c        write(lush,574)
c 
         if (iperts .eq. 1) then
c           Calculate contributions to perturbation intensity change 
c           from various variables or groups of variables
c
c           Note: This section of code depends on specific order of 
c                 independent variables
c
c           Specify labels for variables
            ngrp = nvarpt + 1 
            cdvlab(1) = 'MEAN ADJUSTMENT     '
            cdvlab(2) = 'GOES IR STD DEV     '
            cdvlab(3) = 'GOES IR PIXEL COUNT '
            cdvlab(4) = 'OCEAN HEAT CONTENT  '
c
c           Calculate intensity change contributions
            if (iperr .eq. 0) then
               do kk=1,mft
                  dvvar( 1,kk) = ybarp(kk)
                  do jj=1,nvarpt
                     dvvar(jj+1,kk) = vartp(jj,kk)*coefp(jj,kk)*
     +                                             ysigp(kk)  
                  enddo
               enddo
            else
               do kk=1,mft
	       do jj=0,nvarpt
                  dvvar(jj+1,kk) = 0.0
	       enddo
	       enddo
	    endif
c
c           Print IC array
c           write(lush,770)
c 770       format(/,24x,
c    +             'INTENSITY ADJUSTMENTS FROM SATELLITE INPUT')
c 
            write(lush,573)
  573       format(/,'  SATELLITE ADJUSTMENTS ',
     +   '----------------------------------------------------------')
c 
            do i=1,ngrp
               write(lush,576) cdvlab(i),(dvvar(i,kk),kk=1,4),
     +                                   (dvvar(i,kk),kk=6,mft,2)
            enddo
c 
            write(lush,574)
            write(lush,778) (delvp(kk),kk=1,4),(delvp(kk),kk=6,mft,2)
  778       format(2x,'TOTAL ADJUSTMENT',4x,20(f5.0))
            write(lush,574)
c
c           Calculate and print total intensity change
	    do k=1,mft
	       delvt(k) = delv(k) + delvp(k)
            enddo
c
c           write(lush,780)
c 780       format(/,24x,
c    +             'TOTAL INTENSITY CHANGE')
c           write(lush,572) (kk*12,kk=1,mft)
            write(lush,781) (delvt(kk),kk=1,4),(delvt(kk),kk=6,mft,2)
  781       format(2x,'TOTAL CHANGE (KT)',3x,20(f5.0))
c           write(lush,574)
         endif
      endif
c
c     PARMOD
 7000 continue
c     **** End of SHIPS text file section ****
c
c     **** Begin rapid intensity index ****
c
c     PARMOD
      if (irii .eq. 1) then
      if (ibasin .eq. 2) then
        write(lush,793)
  793   format(/,20x,'*   EPAC RAPID INTENSITY INDEX TESTS        *')
      else
        write(lush,794)
  794   format(/,20x,'*   ATLC RAPID INTENSITY INDEX TESTS        *')
      endif 
      write(lush,791) 
  791 format(/,'++++++++ SECTION 1, COPY OF OPERATIONAL RII ++++++++')
c 
      if (ibasin .eq. 1) then
         call rapidga_2010(perri,shdcri,d200ri,potri,rhlori,
     +                sbtri,pcri30,rhcri,sname,natcf8,ismon,isday,isyr,
     +                istime,lush)
      else
         call rapidge_2010(perri,shdcri,d200ri,potri,rhlori,
     +                sbtri,pcri30,rhcri,sname,natcf8,ismon,isday,isyr,
     +                istime,lush)
      endif
c
c     PARMOD
      write(lush,792) 
  792 format(/,'++++++++ SECTION 2, RII WITH LIGHTNING DATA ++++++++',
     +       /,'                    FOR GOES-R PROVING GROUND       ')
      endif
c
c     **** End rapid intensity index ****
c
c     **** Begin Annular hurricane index ****
c     PARMOD
      if (iahi .gt. 0) then
      luout = lush
      stname = sname
      tcfid  = natcf8
      fn_ships='lsdiag.dat'
      fn_ird1='IRRP1.dat'
      fn_ird2='IRRP2.dat'
      fn_iri1='IRRP1.inf'
      fn_iri2='IRRP2.inf'
c 
      rlon00 = -1.0*rlon(0)
      if (rlon00 .lt. rlonam) then
         call id_annular_op(luout,stname,tcfid,fn_ships,fn_ird1,
     +                      fn_ird2,fn_iri1,fn_iri2,ianmon,ianday,
     +                      ianyr,iantime,dfval,ann_prob)
      endif
c     PARMOD
      endif
c
c     **** End Annular hurricane index ****
c
c     PARMOD
      if (ibasin .eq. 1 .and. isef .gt. 0) then
c  **** Begin PrSEFoNe (probability of Secondary Eyewall Formation) model ****
c
c   At 4 forcast times 0,12,24,36h, 12 features are input into the model:
c     1.  Current intensity (kt)
c     2.  Latitude of center fix (degrees N)  [SHIPS -> LAT / 10]
c     3.  Climatological ocean heat content [SHIPS -> PHCN]
c     4.  200mb zonal wind (kt) [SHIPS -> U200 / 10]
c     5.  Relative humidity between 500-300mb (%) [SHIPS -> RHHI]
c     6.  Symmetric tangential wind (m/s) [SHIPS -> TWAC / 10]
c     7.  Surface pressure at outer vortex edge (mb - 1000) [SHIPS -> PENC / 10]
c     8.  Vertical shear (kt) [SHIPS -> SHRD / 10]
c     9.  Potential intensity (kt) [SHIPS -> VMPI]
c     10. Standard deviation of Tb between 100-300km (C) [SHIPS -> IR00-05 / 10]
c     11. Mean Tb between 20-120km (C) [SHIPS -> IR00-16 / 10]
c     12. IR Tb Principal component #4 (added within subroutine psef_driver)
c

c fill feature matrix for PrSEFoNe model. DTL is included to identify cases
c where storm center is over land, but it's not a feature of the model.
c
c If any one of the standard ships features are missing from lsdiag, 
c  then flag that fix.
c 
      imiss_feat=9999
      do i=1,4
         j=(i-1)*2
         iflag_feat(i)=0
         if (ivd(j).eq.imiss_feat) iflag_feat(i)=1
         if (ilat(j).eq.imiss_feat) iflag_feat(i)=1
         if (iphcn(j).eq.imiss_feat) iflag_feat(i)=1
         if (iu200(j).eq.imiss_feat) iflag_feat(i)=1
         if (irhhi(j).eq.imiss_feat) iflag_feat(i)=1
         if (itwac(j).eq.imiss_feat) iflag_feat(i)=1
         if (ipenc(j).eq.imiss_feat) iflag_feat(i)=1
         if (ishr(j).eq.imiss_feat) iflag_feat(i)=1
         if (ivmpi2(j).eq.imiss_feat) iflag_feat(i)=1
      enddo

c
c flag missing IR00 features
c 
      iflag_feat_ir=0
      if (igoes(4).eq.imiss_feat) iflag_feat_ir=1
      if (igoes(15).eq.imiss_feat) iflag_feat_ir=1

      do i=1,4
         j=(i-1)*2
         psef_feat_vec(1,i)=ivd(j)         ! vmx at 0,12,24,36h
         psef_feat_vec(2,i)=ilat(j)/10.    ! lat at 0,12,24,36h
         psef_feat_vec(3,i)=iphcn(j)       ! phcn at 0,12,24,36h
         psef_feat_vec(4,i)=iu200(j)/10.   ! u200 at 0,12,24,36h
         psef_feat_vec(5,i)=irhhi(j)       ! rhhi at 0,12,24,36h
         psef_feat_vec(6,i)=itwac(j)/10.   ! twac at 0,12,24,36h
         psef_feat_vec(7,i)=ipenc(j)/10.   ! penc at 0,12,24,36h
         psef_feat_vec(8,i)=ishr(j)/10.    ! shrd at 0,12,24,36h
         psef_feat_vec(9,i)=ivmpi2(j)      ! vmpi at 0,12,24,36h
         psef_feat_vec(10,i)=igoes(4)/10.  ! ir00-5 (fixed through all times)
         psef_feat_vec(11,i)=igoes(15)/10. ! ir00-16 (fixed through all times)
         psef_feat_vec(12,i)=idist(j)      ! dtl at 0,12,24,36h
      enddo

c call PrSEFoNe driver subroutine:
c   luout is for writing to ships output file (ships.txt)
c   stname, tcfid, iyear4, ilmon, ilday, itime is for output file header
c   psef_feat_vec, iflag_feat, iflag_feat_ir are needed to calculate PrSEFoNe

      call psef_driver(luout,stname,tcfid,ioper,iyear4,ilmon,ilday,
     .                iltime,psef_feat_vec,iflag_feat,iflag_feat_ir)

c  **** End PrSEFoNe (probability of Secondary Eyewall Formation) ****
      endif

      stop '***** SHIPS COMPLETED *****'
c 
  900 continue
      write(lulg,*) ' Error during file open: ',fnlg
      stop '***** SHIPS HALTED DUE TO FILE OPEN ERROR *****'
c 
      end
c+++
c+++  END MAIN PROGRAM, BEGIN SUBROUTINES
c+++
      subroutine mpical(sst,rmpi,ibasin)
c     This routine calculates the maximum potential intensity (kt)
c     from the sst (C) using empirical relationships.
c
c     ibasin=1 for Atlantic
c     ibasin=2 for East Pacific
c     ibasin=3 for West Pacific
c      
c     Check for illegal sst values 
      if (sst .gt. 35.0 .or. sst .lt. 0.0) then
         rmpi=999.9
         return
      endif
c 
      if (ibasin .eq. 1) then
c        Atlantic function (speed adjusted, DeMaria and Kaplan 1994)
         vcold = 34.2
         vadd  = 55.8
         a     = 0.1813
         tmax  = 30.00
c 
         rmpi = vcold + vadd*exp(-a*(tmax-sst))
         rmpi = rmpi*1.944
      elseif (ibasin .eq. 2) then
c        East Pacific function (speed adjusted, Whitney 1995)
         a = -79.2
         b = 5.362
         c = 4.7
C 
         tmin = 20.0
         sstt = sst
         if (sstt .lt. tmin) sstt=tmin
C 
         rmpi = a + b*sstt + c
         rmpi = rmpi*1.944
      elseif (ibasin .eq. 3) then
C        West Pacific function
         vcold = 19.7
         vadd  = 88.0
         a     = .1909
         tmax  = 30.00
C 
         rmpi  = vcold + vadd*exp(-a*(tmax-sst))
         rmpi  = rmpi*1.944
      else
         rmpi = 999.9
         return
      endif
C 
      if (rmpi .gt. 165.0) rmpi=165.0
c 
      return
      end
c 
      subroutine lcheck(ilat0,ilon0,ilatm,ilonm,dt,tland,lmod)
c     This routine checks to see if a storm is now over water,
c     but was recently over land. If so, lmod is set to 1.
c
c     Specify maximum allowable time over land (hr)
      tlmax = 2.0
c 
      lmod = 0
c
c     Check  and convert lat/lon values
      if (ilat0 .eq. 0 .or. ilatm .eq. 0) return
      if (ilon0 .eq. 0 .or. ilonm .eq. 0) return
c 
      rlat0 =  0.1*float(ilat0)
      rlatm =  0.1*float(ilatm)
      rlon0 = -0.1*float(ilon0)
      rlonm = -0.1*float(ilonm)
c 
      dlat  = rlat0-rlatm
      dlon  = rlon0-rlonm
c
c     Check to make sure lat/lon pair are physically close
      dmax = dt*50.0/60.0
c 
      if (abs(dlat) .gt. dmax .or.
     +    abs(dlon) .gt. dmax      ) return
c
c     If storm is currently over land, no adjustment is needed
      call aland(rlon0,rlat0,dland0)
      if (dland0 .lt. 0.0) return
c
c     Divide positions into smaller sub-intervals
      dts = 1.0
      nts = ifix(0.0001 + dt/dts)
c 
      dlati = dlat/float(nts)
      dloni = dlon/float(nts)
      tland = 0.0
      do k=0,nts
         if (k .eq. 0 .or. k .eq. nts) then
            wt = 0.5*dts
         else
            wt = dts
         endif
c 
         rlatt = rlatm + dlati*float(k)
         rlont = rlonm + dloni*float(k)
         call aland(rlont,rlatt,dlandt)
c 
         if (dlandt .lt. 0.0) tland = tland + wt
c        write(6,888) rlatt,rlont,dlandt,wt,tland
c 888    format(5(f8.1,1x))
      enddo
c 
      if (tland .ge. tlmax) lmod = 1
c 
      return
      end
c
c     ++++BEGIN LGEM MODULE++++
c 
      subroutine lgecal(ibasin,nft,ftime,vdiss,vmaxl,ierr,lulg,rmiss,
     +                  imiss,ioper)
c     This routine makes an intensity forecast using the 
c     Logistic Growth Equation. This routine constructs the cappa 
c     array using statistical relationship , and then calls routine 
c     lgeim for the numerical solution of the LGE equation. Most of the 
c     required input for this routine is passed through common blocks. 
c
c***  needs to use ships_util for patch
      use ships_util
c     ++ Calling argument variables
      dimension ftime(nft),vmaxl(nft)
c
c     ++ Common blocks from main iships.f for lgecal routine
      common /lgestr/ aday,spdx,pslv,per,vmx,pc20,rthresh
      common /lgetdi/ ishr,iepos,iz850,id200,ishdc,irhcn
      common /lgetdr/ sst,vsstl,rlat,rlon,t200,t250,twac,sdir,
     +                shdct,shgc
c***      common /lgepar/ rmiss,imiss,ioper
c 
      parameter (mft=20)
      dimension ishr(0:mft),iepos(0:mft),iz850(0:mft),id200(0:mft)
      dimension ishdc(0:mft),irhcn(0:mft)
      dimension twac(0:mft),sdir(0:mft)
      dimension shdct(0:mft),shgc(0:mft)
      dimension t200(0:mft),t250(0:mft)
      dimension sst(0:mft),vsstl(0:mft)
      dimension rlat(-2:mft),rlon(-2:mft)
c
c     ++ Local variables for variables derived from common variables
      dimension shr(0:mft),epos(0:mft),z850(0:mft),d200(0:mft)
      dimension shrl(0:mft),sstl(0:mft),rhcn(0:mft)
      dimension shdctl(0:mft)
c
c     ++ Local variables for coefficients
      parameter (nvar=18)
      dimension var(nvar),coef(nvar,0:mft)
      dimension xbar(nvar,0:mft),xsig(nvar,0:mft)
      dimension ybar(0:mft),ysig(0:mft)
c
c     ++ Local variables for lgeim call
      parameter (nmx=mft+1)
      dimension tlat(nmx),tlon(nmx),vmpi(nmx),cappa(nmx),dland(nmx)
      intrinsic trim
c 
      character *256 fncol
      character *256 coef_location
c 
      if (ioper .eq. 1) then
c        get SHIPS_COEF env variable
         call getenv( "SHIPS_COEF", coef_location )
      endif
c   
      dtr = 0.017453
c
c     **** Default forecast ****
      vmaxl(1) = vmx
      do k=2,nft
         vmaxl(k) = 0.0
      enddo
      ierr=1
c
c     **** Check of input variables ****
      if (nft  .lt. 2                         ) return
      if (vmx  .le. 0.0 .or. vmx .ge. rmiss   ) return
      if (aday .ge. rmiss .or. spdx .ge. rmiss) return
      if (pslv .ge. rmiss                     ) return
      if (per  .ge. rmiss                     ) return
      if (pc20 .ge. rmiss                     ) return
c     if (ishr(0) .ge. imiss                  ) return
      if (ishdc(0) .ge. imiss                 ) return
      if (iepos(0) .ge. imiss                 ) return
      if (iz850(0) .ge. imiss                 ) return
      if (id200(0) .ge. imiss                 ) return
      if (irhcn(0) .ge. imiss                 ) return
      if (t200(0) .ge. rmiss                  ) return
      if (t250(0) .ge. rmiss                  ) return
      if (rlat(0) .ge. rmiss                  ) return
      if (rlon(0) .ge. rmiss                  ) return
      if (vsstl(0) .ge. rmiss                 ) return
      if (sst(0) .ge. rmiss                   ) return
      if (sdir(0) .ge. rmiss                  ) return
      if (shdct(0) .ge. rmiss                 ) return
      if (shgc(0) .ge. rmiss                  ) return
c
c     **** Specify basin-specific variables ****
      if (ibasin .eq. 1) then
         if (ioper .eq. 1) then
            fncol=trim( coef_location )//'shipl10_coef_atlc.dat'
         else
            fncol='shipl10_coef_atlc.dat'
         endif
      else
         if (ioper .eq. 1) then
            fncol=trim( coef_location )//'shipl10_coef_epac.dat'
         else
            fncol='shipl10_coef_epac.dat'
         endif
      endif
c
c     Open and read coefficient file
      lucol=45
      open(file=fncol,unit=lucol,form='formatted',status='old',
     +     err=900)
c 
      ierr=2
      do 5 k=0,mft
         read(lucol,135,end=900,err=900) ybar(k),ysig(k)
  135    format(14x,e12.5,1x,e12.5)
c      
         do 6 n=1,nvar
            read(lucol,136,end=900,err=900) 
     +          coef(n,k),xbar(n,k),xsig(n,k)
  136       format(1x,3(e12.5,1x))
    6    continue
    5 continue
c 
      close(lucol)
            
c     **** Variable initialization and specification ****
c
c     ++Specify the beta (1/hr) and nn parameters for the MPI term
      beta = 1.0/24.0
      rnn   = 2.5
c
c     ++Convert common block variables to real
      do k=0,mft
         if (ishdc(k) .lt. imiss) then
            shr(k) = 0.1*float(ishdc(k))
            if (rlat(k) .lt. rmiss) then
               shrl(k) = shr(k)*sin(dtr*rlat(k))
            else
               shrl(k) = rmiss
            endif
         else
            shr(k)  = rmiss
            shrl(k) = rmiss
         endif
c 
         if (iepos(k) .lt. imiss) then
            epos(k) = 0.1*float(iepos(k))
         else
            epos(k) = rmiss
         endif
c 
         if (iz850(k) .lt. imiss) then
            z850(k) = float(iz850(k))
         else
            z850(k) = rmiss
         endif
c 
         if (id200(k) .lt. imiss) then
            d200(k) = 0.1*float(id200(k))
         else
            d200(k) = rmiss
         endif
c 
         if (irhcn(k) .lt. imiss) then
            rhcn(k) = float(irhcn(k))
         else
            rhcn(k) = rmiss
         endif
c 
         sstl(k) = sst(k)
      enddo
c
c     Calculate transformed shear times sin(lat)
      do k=0,mft
         if (shdct(k) .lt. rmiss .and. rlat(k) .lt. rmiss) then
            shdctl(k) = shdct(k)*sin(dtr*rlat(k))
         else
            shdctl(k) = rmiss
         endif
      enddo
c
c     ++ Fill in missing values in time arrays
      rmiss1 = rmiss/10.0
      call patch(shr ,rmiss,mft)
      call patch(shrl,rmiss,mft)
      call patch(shdct,rmiss,mft)
      call patch(shdctl,rmiss,mft)
      call patch(shgc,rmiss,mft)
      call patch(sdir,rmiss,mft)
      call patch(epos,rmiss,mft)
      call patch(z850,rmiss,mft)
      call patch(d200,rmiss,mft)
      call patch(t200,rmiss,mft)
      call patch(t250,rmiss,mft)
      call patch(sstl,rmiss1,mft)
      call patch(vsstl,rmiss1,mft)
      call patch(rhcn,rmiss,mft)
c
c     ++ Calculate initial value of cappa from previous 12 hour intensity change
      cappa00 = per/(12.0*vmx) + beta*(vmx/vsstl(0))**rnn
c
c     **** Calculate cappa ****
c
c     ++ Main time loop
      do 99 k=0,mft
         ktime = k*6
c
c        ++ GFS vortex time tendency
         klag  = 2
         klead = 2
         ks = k-klag
         ke = k-klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         deltg = float(ke-ks)
         if (deltg .le. 0.0) then
            twacten = 0.0
         else
            twacten = 4.0*(twac(ke)-twac(ks))/deltg
         endif
c
c        ++ time averaged shear and lshear
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tashr = 0.0
         tashrl= 0.0
         do kk=ks,ke
            if (shr(kk) .lt. rmiss .and. shrl(kk) .lt. rmiss) then
               tashr = tashr + shr(kk)
               tashrl= tashrl+ shrl(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tashr = tashr/ccount
            tashrl= tashrl/ccount
         else
            tashr = rmiss
            tashrl= rmiss
         endif
c 
c        ++ time averaged transformed shear, lshear
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tashdct = 0.0
         tashdctl= 0.0
         do kk=ks,ke
            if (shdct(kk) .lt. rmiss .and. shdctl(kk) .lt. rmiss) then
               tashdct = tashdct + shdct(kk)
               tashdctl= tashdctl+ shdctl(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tashdct = tashdct/ccount
            tashdctl= tashdctl/ccount
         else
            tashdct = rmiss
            tashdctl= rmiss
         endif
c 
c        ++ time averaged shear direction parameter
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tasdir = 0.0
         do kk=ks,ke
            if (sdir(kk) .lt. rmiss) then
               tasdir = tasdir + sdir(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tasdir = tasdir/ccount
         else
            tasdir = rmiss
         endif
c      
c        ++ time averaged generalized shear
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tashgc = 0.0
         do kk=ks,ke
            if (shgc(kk) .lt. rmiss) then
               tashgc = tashgc + shgc(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tashgc = tashgc/ccount
         else
            tashgc = rmiss
         endif
c      
c        ++ time averaged epos
         klag=1
         klead=1
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         taepos = 0.0
         do kk=ks,ke
            if (epos(kk) .lt. rmiss) then
               taepos = taepos + epos(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            taepos = taepos/ccount
         else
            taepos = rmiss
         endif
c
c        ++ time averaged d200 and z850
         klag=2
         klead=2
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tad200 = 0.0
         taz850 = 0.0
         do kk=ks,ke
            if (d200(kk) .lt. rmiss .and. z850(kk) .lt. rmiss) then
               tad200 = tad200 + d200(kk)
               taz850 = taz850 + z850(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tad200 = tad200/ccount
            taz850 = taz850/ccount
         else
            tad200 = rmiss
            taz850= rmiss
         endif
c
c        ++ time averaged t200 and t250
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tat200 = 0.0
         tat250 = 0.0
         do kk=ks,ke
            if (t200(kk) .lt. rmiss .and. t250(kk) .lt. rmiss) then
               tat200 = tat200 + t200(kk)
               tat250 = tat250 + t250(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tat200 = tat200/ccount
            tat250 = tat250/ccount
         else
            tat200 = rmiss
            tat250= rmiss
         endif
c
c        ++ time averaged sst
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         tarsst = 0.0
         do kk=ks,ke
            if (sstl(kk) .lt. 200.0) then
               tarsst = tarsst + sstl(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            tarsst = tarsst/ccount
         else
            tarsst = rmiss
         endif
c
c        ++ time averaged ohc
         klag=5
         klead=0
         ks = k-klag
         ke = k+klead
         if (ks .lt.   0) ks = 0
         if (ke .gt. mft) ke = mft
         if (ke .lt.  ks) ke = ks
         ccount = 0.0
         taohc = 0.0
         do kk=ks,ke
            if (rhcn(kk) .lt. rmiss) then
               taohc = taohc + rhcn(kk)
               ccount = ccount + 1.0
            endif
         enddo
c 
         if (ccount .gt. 0.0) then
            taohc = taohc/ccount
            taohc = taohc-rthresh
            if (taohc .lt. 0.0) taohc=0.0
         else
            taohc = rmiss
         endif
c
c        ++ Specify the values of the independent variables for cappa
         var( 1) = cappa00
         var( 2) = aday
         var( 3) = spdx
         var( 4) = pslv
         var( 5) = tashdct
         var( 6) = tashdctl
         var( 7) = taepos
         var( 8) = twacten
         var( 9) = taz850
         var(10) = tad200
         var(11) = tat200
         var(12) = tat250
         var(13) = tarsst
         var(14) = vmx
         var(15) = taohc
         var(16) = pc20
         var(17) = tasdir
         var(18) = tashgc
c       
c       ++ Normalize the independent variables
        do j=1,nvar
           var(j) = (var(j) - xbar(j,k))/xsig(j,k)
        enddo
c
c       ++ calculate cappa
        cappa(k+1) = 0.0
        do j=1,nvar
           cappa(k+1) = cappa(k+1) + var(j)*coef(j,k)
        enddo
        cappa(k+1) = ybar(k) + cappa(k+1)*ysig(k)
c 
        write(lulg,830) ktime,cappa(k+1)
  830   format('t= ',i4,' cappa=',f8.4)
c 
        do j=1,nvar
           write(lulg,831) j,var(j),coef(j,k),var(j)*coef(j,k)
  831      format(i3,1x,3(f8.4,1x))
        enddo
c
c       write(6,828) ktime,tashr,tashrl,tat200,tat250,tarsst,
c    +               tad200,taz850,taepos
c828    format('ktime,shr,l, t200,250, rsst,d200,z850,epos ',
c    +          i3,1x,10(f6.1,1x))
   99 continue
c
c     ++ Integrate LGE model ++
c
c     Copy rlat,rlon,vsstl to temporary arrays for the lgemi call
      do k=0,mft
         tlat(k+1) = rlat(k)
         tlon(k+1) = -rlon(k)
         vmpi(k+1) = vsstl(k)
      enddo
c 
      call lgeim(nft,ftime,tlat,tlon,vmpi,cappa,vmx,
     +           rnn,beta,lulg,vmaxl,dland,ierrl)
c
c     ++ Check integration error
      if (ierrl .ne. 0) then
         vmaxl(1) = vmx
         do i=2,nft
            vmaxl(i) = 0.0
         enddo
         ierr=3
      endif
c
c     ++ Check for dissipation
      do i=2,nft
         if (vmaxl(i) .lt. vdiss) then
            do ii=i,nft
               vmaxl(ii) = 0.0
            enddo
            go to 1100
         endif
      enddo
 1100 continue
c
c     write(6,599) cappa00,aday,spdx,pslv
c 599 format('cappa00,aday,spdx,pslv: ',e11.4,1x,3(f6.1,1x))
c
c     do i=1,nft
c        write(6,600) ftime(i),tlat(i),tlon(i),sstl(i-1),
c    +                vmpi(i),shr(i-1),cappa(i),dland(i),vmaxl(i)
c 600    format(f6.0,1x,f6.1,1x,f7.1,1x,f6.1,1x,
c    +          f6.1,1x,f6.1,1x,e11.4,1x,f6.0,1x,f6.1)
c     enddo
c
c     Normal exit
      write(lulg,400) 
  400 format(/,'LGE model completed normally')
      return
c
c     Error exit
  900 continue
      write(lulg,950) ierr
  950 format(/,'Error in LGE model, no forecast made, ierr=',i2)
c 
      return
      end
c 
      subroutine lgeim(nft,ftime,rlat,rlon,vmpi,cappa,v0,
     +                      rnn,beta,lulg,vmax,dland,ierr)
c
c     This code is for an intensity forecast model based upon
c     a simple two term logistical growth equation method. A separate procedure is
c     used if the storm is over land. 
c
c     ********** INPUT **********
c 
c       nft:         The number of forecast times 
c       ftime(nft ): The time in hours (for example, 0.,6.,12. ... 120.)
c                    The times need to sequential, but the time interval
c                    does not need to be even. 
c       rlat(nft):   The storm latitude (deg n) at the times in array ftime
c       rlon(nft):   The storm longitude (deg w negative) at the times in
c                    array ftime
c       vmpi(nft):   The maximum potential intensity (kt) versus time
c       cappa(nft):  The coefficient of the synoptic term (1/hr) in the simple two term model
c                    versus time
c       rnn:          The order of the SST term (integer, usually 2 or 4)
c       beta:        The time scale (1/hr) of the SST term
c       v0:          The initial maximum winds (kt)
c       lulg:        Unit number for write statements
c
c     ********** OUTPUT **********  
c
c       vmax(nft):  The forecast maximum wind (kt) versus time
c       dland(nft): The distance (km) from the storm center (rlat,rlon) to 
c                   the nearest major land mass. dland is negative if the 
c                   point is storm center is inland.
c       ierr:       Error flag (=0 for normal return, =1 for error)
c
c     ********** PARAMETER SPECIFICATION **********
c
c     Specify the time interval (hr) for numerical integration
      data dt /1.00/
c
c     Set interp=1,2 or 3 to print out (to unit lulg) intermediate 
c     intensity calculations or else set interp=0 for no print 
      data interp /0/ 
c
c     Inland decay model coefficients for east/gulf coast
      data rf1,a1,vb1,rclat1 /0.9,0.095,26.7,36.0/
c     
c     Inland decay model coefficients for New England
      data rf2,a2,vb2,rclat2 /0.9,0.183,29.6,40.0/
c
c     Specify radius of storm circulation (km) for fractional
c     decay option. Set rcrad to zero to eliminate this option. 
c
c     data rcrad /   0.0/
      data rcrad / 110.0/
c     data rcrad / 150.0/
c
c     ********** Passed arrays **********
c 
      dimension ftime(nft),rlat(nft),rlon(nft)
      dimension vmpi(nft),cappa(nft),dland(nft)
      dimension vmax(nft)
c
c     ********** Arrays for numerical integration **********
      parameter (imaxs=1000)
      dimension ftimes(imaxs),rlats(imaxs),rlons(imaxs)
      dimension vmpis(imaxs),cappas(imaxs)
      dimension vmaxs(imaxs)
      dimension redfacs(imaxs),vbs(imaxs),alphas(imaxs)
      dimension dlands(imaxs),flands(imaxs)
c 
c     ********** MODEL CODE *********
c
c     Initial intensity forecast
      vmax(1) = v0
      do i=2,nft
	 vmax(i) = 0.0
      enddo
c
c     Find the number of valid forecast times
      itimet = 0
      do 10 i=1,nft
         if (abs(rlat(i))  .lt.  0.5) go to 1000
         if (abs(rlat(i))  .gt. 90.0) go to 1000
	 if (vmpi(i)       .lt.  0.5) go to 1000
	 if (abs(cappa(i)) .gt.  5.0) go to 1000
         itimet=i 
   10 continue
c 
 1000 continue
c     There must be at least two valid forecast times
      if (itimet .lt. 2) then
	 ierr=1
	 return
      endif
c
c     Check to make sure times are sequential
      itime=0
      do 15 i=2,itimet
         if (ftime(i) .le. ftime(i-1)) go to 1100
         itime=i
   15 continue
c 
 1100 continue
      if (itime .lt. 2) then
	 ierr=1
	 return
      endif
c         
      if (interp .gt. 2) then
         do i=1,itime
            write(6,887) ftime(i),rlat(i),rlon(i),cappa(i),vmpi(i)
         enddo
      endif
c
c     Calcuate the time values at the small time interval points
      ntimes = 1 + (ftime(itime)-ftime(1))/dt
      do i=1,ntimes
	 ftimes(i) = ftime(1) + dt*float(i-1)
      enddo
c
c     Interpolate the input lat,lon,vmpi,cappa to the 
c     small time interval
c
c     ++ lat
      lflag=0
      iflag=1
      call xint(ftime,rlat,itime,iflag,lflag,xi,fi,ierrx)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,rlat,itime,iflag,lflag,
     +                  ftimes(i),rlats(i),ierrx)
      enddo
c
c     ++ lon
      iflag=1
      call xint(ftime,rlon,itime,iflag,lflag,xi,fi,ierrx)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,rlon,itime,iflag,lflag,
     +                  ftimes(i),rlons(i),ierrx)
      enddo
c
c     ++ vmpi
      iflag=1
      lflag=0
      xi = 0.0
c 
      call xint(ftime,vmpi,itime,iflag,lflag,xi,fi,ierrx)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,vmpi,itime,iflag,lflag,
     +                   ftimes(i),vmpis(i),ierrx)
      enddo
c
c     ++ cappa
      iflag=1
      lflag=0
      xi = 0.0
c 
      call xint(ftime,cappa,itime,iflag,lflag,xi,fi,ierrx)
c 
      iflag=0
      do i=1,ntimes
         call xint(ftime,cappa,itime,iflag,lflag,
     +                   ftimes(i),cappas(i),ierrx)
      enddo
c
c     Calcuate distance to land and fractional land at small time points
      do i=1,ntimes
         call aland(rlons(i),rlats(i),dlands(i))
	 call fland(rlons(i),rlats(i),rcrad,flands(i))
      enddo
c
c     Calculate decay model parameters at small time points
      do i=1,ntimes
	 rlatt = rlats(i)
         if     (rlatt .ge. rclat2) then
             redfacs(i) = rf2
             alphas(i)  = a2
             vbs(i)     = vb2
         elseif (rlatt .le. rclat1) then 
             redfacs(i) = rf1
             alphas(i)  = a1
             vbs(i)     = vb1
         else
             w1 = (rclat2-rlatt)/(rclat2-rclat1)
             w2 = (rlatt-rclat1)/(rclat2-rclat1)
c 
             redfacs(i) = w1*rf1 + w2*rf2
             alphas(i)  = w1*a1  + w2*a2
             vbs(i)     = w1*vb1 + w2*vb2
         endif
      enddo
c
c     Perform time integration
      vmaxs(1) = v0
c 
      do 99 i=1,ntimes-1
c        
         vnow = vmaxs(i)
c
c        Check to see if the storm is over water or land
	 if (dlands(i) .lt. 0.0) then
c            Over land case
c 
             if (i .gt. 1) then
c               Check to see if the storm just moved over land
c               If so, apply the sea/land reduction factor
                if (dlands(i-1) .gt. 0.0) then
		   vnow = vnow*redfacs(i)
                endif
             endif
c
c            Forward time step
             vmaxs(i+1) = vnow - alphas(i)*flands(i)*(vnow-vbs(i))*dt
	 else
c
c            Over water case
             if (i .gt. 1) then
c               Check to see if the storm just moved over water 
c               If so, apply the inverse sea/land reduction factor
                if (dlands(i-1) .le. 0.0) then
		   vnow = vnow/redfacs(i)
                endif
             endif
c
c           Forward time step
c
c           Calculate coefficient of MPI term
	    cmpi = beta*(vnow/vmpis(i))**rnn
	    vmaxs(i+1) = vnow + (cappas(i)*vnow - cmpi*vnow)*dt
	 endif
   99 continue
c
       
      if (interp .gt. 2) then
         do i=1,ntimes
	    write(6,887) ftimes(i),rlats(i),rlons(i),vmpis(i),cappas(i),
     +                   redfacs(i),vbs(i),alphas(i),dlands(i),
     +                   flands(i),vmaxs(i)
  887       format(4(f6.1,1x),1x,f8.4,1x,f6.1,1x,f6.1,1x,
     +                         f8.4,1x,f6.0,1x,f8.4,1x,f6.1)
         enddo
      endif
c
c     Interpolate decay vmaxs back to original forecast times
      iflag=1
c 
      call xint(ftimes,vmaxs,ntimes,iflag,lflag,xi,fi,ierrx)
c 
      iflag=0
      do i=2,itime
         call xint(ftimes,vmax,ntimes,iflag,lflag,
     +                  ftime(i),vmax(i),ierrx)
      enddo
c
c     Interpolate dlands back to original forecast times
      iflag=1
c 
      call xint(ftimes,dlands,ntimes,iflag,lflag,xi,fi,ierr)
c 
      iflag=0
      do i=1,itime
         call xint(ftimes,dlands,ntimes,iflag,lflag,
     +                  ftime(i),dland(i),ierrx)
      enddo
c 
      return
      end
c     ++++END LGEM MODULE++++
c 
      subroutine mpicalo(sst,rmpi,ibasin)
c     This routine calculates the maximum potential intensity (kt)
c     from the sst (C) using empirical relationships.
c
c     This version was modifed March 2006 to
c     use the original formulas from DK 1994 and
c     WH 1997, rather than the formulas adjusted
c     for the average storm translational speed.
c
c     Input: 
c       sst:    SST in deg C
c       tspeed: Storm translational speed in knots
c       ibasin: Basin indicator
c               ibasin=1 for Atlantic
c               ibasin=2 for East Pacific
c               ibasin=3 for West Pacific
c      
c     Output:
c       rmpi:  Maximum potential intensity (kt)
c              Note: rmpi is set to 999.9 for missing SST
c
c     Check for illegal sst values 
      if (sst .gt. 35.0 .or. sst .lt. 0.0) then
         rmpi=999.9
         return
      endif
c 
      if (ibasin .eq. 1) then
c        Atlantic function (DeMaria and Kaplan 1994)
c        vcold = 34.2
         vcold = 28.2
         vadd  = 55.8
         a     = 0.1813
         tmax  = 30.00
c 
         rmpi = vcold + vadd*exp(-a*(tmax-sst))
         rmpi = rmpi*1.944
      elseif (ibasin .eq. 2) then
c        East Pacific function (Whitney and Hobgood 1997)
         a = -79.2
         b = 5.362
c        c = 4.7
         c = 0.0
C 
         tmin = 20.0
         sstt = sst
         if (sstt .lt. tmin) sstt=tmin
C 
         rmpi = a + b*sstt + c
         rmpi = rmpi*1.944
      elseif (ibasin .eq. 3) then
C        West Pacific function
         vcold = 19.7
         vadd  = 88.0
         a     = .1909
         tmax  = 30.00
C 
         rmpi  = vcold + vadd*exp(-a*(tmax-sst))
         rmpi  = rmpi*1.944
      else
         rmpi = 999.9
         return
      endif
C 
      if (rmpi .gt. 165.0) rmpi=165.0
c 
      return
      end
c 
c ++++BEGIN ANNULAR HURRICANE INDEX MODULE++++
c
c This set of routines calculates the probability of a tropical
c cyclone becoming an annular cyclone in the next 24h.  They were 
c adapted to be cut and pasted into the SHIPS model and run in 
c realtime.



c-----7---------------------------------------------------------------72
      SUBROUTINE id_annular_op(luout,stname,tcfid,fn_ships,fn_ird1,
     .                   fn_ird2,fn_iri1,fn_iri2,ilmon,ilday,
     .                   iyr,iltime,dfval,ann_prob)
c-----7---------------------------------------------------------------72
c id_annular_op.f determines the probability of a tropical
c cyclone becoming an annular cyclone within 24 h.  It uses the most
c recent SHIPS run and requires at least 1 IR data file within 12h
c of the SHIPS data file, but ideally uses 2 IR data files.   
c 
c
c Operational version of id_annular.test3.f written by Thomas Cram, 
c CIRA/CSU, February 2006 
c
c Adapted from McIDAS GOES-IR AREA file reader program written
c by Jim Kossin, CIRA/CSU, Jan. 2002
c
c Input: 
c	luout = unit number for writing data output
c	stname = storm name, 10 character string
c	tcfid = ATCF storm id, 8 character string 
c	fn_ships = SHIPS data file name - eg. 'lsdiag.dat'
c	fn_ird1 = IR data file name - eg. 'IRRP1.dat'
c	fn_ird2 = IR data file name - eg. 'IRRP2.dat'
c	fn_iri1 = IR information file name - eg. 'IRRP1.inf'
c	fn_iri2 = IR information file name - eg. 'IRRP2.inf'
c
c Output:
c	ilmon = storm month from SHIPS file, eg. '09' for Sep
c	ilday = storm day from SHIPS file, eg. '23' for the 23rd
c	iyr = storm year from SHIPS file, eg. '2005'
c	iltime = storm time from SHIPS file, UTC, eg '0600'
c	dfval = discriminant function value normalized to 
c		vary between 0 and 1 = annular hurr index
c	ann_prob = probability of annular structure
c
c
c Should be machine independent (portable) assuming that: 
c    1) The RECL specifiers in the OPEN statements refer to bytes, 
c       not words.
c    2) The default size of integers is 4 bytes.
c
c REQUIRES SUBROUTINES:
c	read_ships
c	ir_prof_avg2
c	detend
c	read_radprof
c	moment
c	chartointmon
c	ahindex
c	tdiff
c
c     Modified by Andrea Schumacher for operational use, CIRA, July 2006
c
c     MODIFIED: February 16, 2007 - JAK
c     1) changed the number of disciminants used to 5
c     2) more changes to ahindex and block data.
c
c-----7---------------------------------------------------------------72
c 
c***  needs to use ships_util for: moment, chartointmon, tdiff
      use ships_util

      parameter(maxavg=1000)     ! max size of 1D radial profile arrays
      parameter(radmax=600.)    ! max radius of profile output files
      parameter(maxrad=radmax/4) ! max number of elements in profiles
      dimension raz(maxrad)
      character *10 stname
      character*9 stnm       ! storm name
      character*9 stnmabr       ! abbreviated storm name
      character*8 tcfid
      character*2 bas           ! ocean basin (AT,EP,WP,SP,CP,NI,SI)
      real xmsng
      character*3 irmonchar
      character*40 errmsg0,errmsg1,errmsg2,errmsg3,errmsg4,errmsg5


c Averaged IR data      
      real prof_avg(maxrad),std_avg(maxrad)
      integer irerr,irerr1,irerr2,irerrflg
      integer ibuff
      integer useir1,useir2

c Annular hurricane predictors
      real std_cpix,eye_diff
      real cpix,std,var,weye,shrd,shrs,shrg,u200,t200,vmax
      ! Other screening variables
      real sst
      real mmaxval

c SHIPS data
      parameter(mft=20)
      integer ilyr,ilmon,ilday,iltime,ivmx,iyr
      integer ishrd(0:mft),ishtd(0:mft),ishrs(0:mft),ishts(0:mft),
     .        ishrg(0:mft),irsst(0:mft),iu200(0:mft),it200(0:mft),
     .        irefc(0:mft),ivmax(0:mft)
      integer endoffile
      integer ludiag
      character*4 sname4
      character*34 fn_ships
      character*34 fn_ird1
      character*34 fn_ird2
      character*34 fn_iri1
      character*34 fn_iri2
      integer iphold,irhold
      real tbmin,tbmax
      integer smiss   ! SHIPS missing data value (=9999)

c Array counters
      integer sample_count
      integer luout
      real dv,dfval,ann_prob
      integer screen_fail
      logical radexist
      
c-----7---------------------------------------------------------------72      
      ! Standardized data
      real weye_s, var_s, std_s, sst_s, u200_s
      
c-----7---------------------------------------------------------------72
      ! Statistical moments and discriminant weights (block data)
      REAL sdev(5),means(5),dweights(5),idiv
      
      common /MOMENTS/ sdev,means
      common /DWEIGHTS/ dweights
      common /DIVIDER/ idiv
      
c     Set ishort=1 for short form of output for SHIPS text file
      ishort=1
      
c     Specify total number of screening variables for output
      nscreen=7
c 
      ludiag=50
           
      xmsng=-1.0

      endoffile=0
      sample_count=0
      
      ibuff=0
       
      ! SHIPS missing data value
      smiss=9999
      ! Discriminant value missing data
      dmiss=9999.

      ir1ex=0
      ir2ex=0
      irex=0
      ir1tg=0
      ir2tg=0
      irtg=0

      ivmx=0
      dv=0.0
      dfval=0.0
      ann_prob=0.0
      
c     write(errmsg0,631) 'NOTE:',', ANNULAR INDEX RAN NORMALLY'
      errmsg0=' ANNULAR INDEX RAN NORMALLY'
      write(errmsg1,632) 'ERR=1',', SHIPS FILE MISSING'
      write(errmsg2,633) 'ERR=2',', BOTH IR FILES BAD OR MISSING'
      write(errmsg3,634) 'ERR=3',', IR & SHIPS DATA > 12h APART'
      write(errmsg4,635) 'ERR=4',', SHIPS DATA MISSING'
      errmsg5='NOTE: 1 INSTEAD OF 2 GOES FILES USED'
c     write(errmsg5,636) 
c636  format(5x,'NOTE: 1 INSTEAD OF 2 GOES FILES USED   ')
      
c637  format(/,/,/,/,a40)
 637  format('   ##',4x,a40)
 638  format('   ##',4x,a40)
 639  format('   ##',4x,a40)
c639  format(/,13x,a40)
 
 631  format(5x,a5,a28,2x)
 632  format(5x,a5,a20,10x)
 633  format(5x,a5,a30)
 634  format(5x,a5,a29,1x)
 635  format(5x,a5,a20,10x)
      
      mmaxval=-3.105263
 
 
c-----7---------------------------------------------------------------72
c open data output file
c
c     open(unit=luout,file='./annout.dat',status='replace')
c
c
c open warning message file
c
c      open(unit=luwarn,file='./warning_msg2.out',status='unknown')
c
c
c determine endian-ness of host machine
c 
      call detend(indwrd)

  
c-----7---------------------------------------------------------------72      
c Verify that SHIPS data file exists. If not, fail. If so, read header.
c-----7---------------------------------------------------------------72


      ! Open SHIPS file on first pass


      open(unit=ludiag,file=fn_ships,status='old',err=901) 

      !Read the date and time info from SHIPS data file

c      read(ludiag,110,err=901,end=901) sname4,ilyr,ilmon,ilday,
c     .                    iltime,ivmx,iheader
c 110  format(1x,a4,1x,3(i2.2),1x,i2.2,1x,i4,a110)

      read(ludiag,110,err=901,end=901) sname4,ilyr,ilmon,ilday,
     .                    iltime,ivmx
 110  format(1x,a4,1x,3(i2.2),1x,i2.2,1x,i4)

      close(ludiag)
      
c-----7---------------------------------------------------------------72
c      
c Write header to output file, first calculating 4-digit year:
c
c-----7---------------------------------------------------------------72

      if (ilyr.lt.40) then
         iyr=2000+ilyr
	  write(stnm,25) sname4(1:3)
         write(stnmabr,26) ilyr,bas,sname4(1:3)
      else
         iyr=1900+ilyr
	  write(stnm,25) sname4(1:3)
         write(stnmabr,28) ilyr,bas,sname4(1:3)
      endif
 
 25   format(a3)
 26   format('20',i2.2,a2,a3)
 28   format('19',i2.2,a2,a3)     
c 
      write(luout,600) tcfid,stname,ilmon,ilday,
     +                 ilyr,iltime
  600 format(/,'   ##',9x,'ANNULAR HURRICANE INDEX (AHI) ',a8,1x,a10,
     +         1x,i2.2,'/',i2.2,'/',i2.2,2x,i2.2,' UTC         ##')


c-----7---------------------------------------------------------------72      
c Verify 1st .inf and .dat files both exist.  If so, read header and
c   determine if .dat file time is > 12h from SHIPS data file time.
c-----7---------------------------------------------------------------72

      ! Does IR radial profile file exist?
      inquire(file=fn_ird1,exist=radexist)
      if(.not.radexist) then
	  goto 902
      endif
  
      open(unit=ludiag+2,file=fn_iri1,status='old',err=902)
      read(unit=ludiag+2,fmt=111,err=902,end=902) irday,
     .               irmonchar,iryr,irtime

 111  format(/,/,/,/,1x,i2.2,2x,a3,4x,i2,1x,i2)
 
      ir1ex=1
      
      call chartointmon(irmonchar,irmon)         
      call tdiff(iryr,irmon,irday,irtime,ilyr,ilmon,ilday,iltime,idelt)      
      
      if (idelt.gt.12.or.idelt.lt.-12) then
           ir1tg=0
      else
	   ir1tg=1
      endif
      goto 904
      
 902  ir1ex=0
       
 904  continue
      close(ludiag+2)
       
c-----7---------------------------------------------------------------72      
c Verify 2nd .inf and .dat files both exist.  If so, read header and
c   determine if .dat file time is > 12h from SHIPS data file time.
c-----7---------------------------------------------------------------72

      ! Does IR radial profile file exist?
      inquire(file=fn_ird2,exist=radexist)
      if(.not.radexist) then
	  goto 903
      endif
 
      open(unit=ludiag+2,file=fn_iri2,status='old',err=903)
      read(unit=ludiag+2,fmt=112,err=903,end=903) irday,
     .              irmonchar,iryr,irtime

 112  format(/,/,/,/,1x,i2.2,2x,a3,4x,i2,1x,i2)
 
      ir2ex=1
      
      call chartointmon(irmonchar,irmon)      
      call tdiff(iryr,irmon,irday,irtime,ilyr,ilmon,ilday,iltime,idelt)
             
      if (idelt.gt.12.or.idelt.lt.-12) then
           ir2tg=0
      else
	   ir2tg=1
      endif
      goto 905
 
 903  ir2ex=0
 
 905  continue
      close(ludiag+2)
      
      
      irex = ir1ex+ir2ex     
      irtg = ir1tg+ir2tg
      
      ! If both IR files are missing, display error in data output
      ! file and skip to the end (ie, calculation fails)
      if (irex.eq.0) then
           write(luout,638) errmsg2
	   goto 1500
      endif

      ! If both IR files are more than 12h before or after the
      ! current SHIPS data, display error in data output file
      ! and skip to the end (ie, calcualtion fails)
      if (irtg.eq.0) then
	   write(luout,638) errmsg3
	   goto 1500
      endif
     
      
      if ((ir1ex.eq.1).and.(ir1tg.eq.1)) then
           useir1 = 1
      else 
           useir1 = 0
      endif
      if ((ir2ex.eq.1).and.(ir2tg.eq.1)) then
           useir2 = 1
      else
           useir2 = 0
      endif
	   

c-----7---------------------------------------------------------------72
c Open and Read in SHIPS data
c-----7---------------------------------------------------------------72    

         ! Open SHIPS file
           open(unit=ludiag,file=fn_ships,status='old',err=901)


 5    call read_ships(ludiag,sname4,ilyr,ilmon,ilday,iltime,ivmx,
     .                iu200,it200,irsst,irefc,ishrd,ishtd,ishrs,
     .                ishts,ishrg,endoffile)
     
c-----7---------------------------------------------------------------72
c Call routine 'ir_prof_avg2' to read in IR Tb radial profiles, 
c compute the Tb standard deviations, and then compute average radial
c profiles of each.
c-----7---------------------------------------------------------------72

       call ir_prof_avg2(fn_ird1,fn_ird2,fn_iri1,fn_iri2,        
     .                   iyr,useir1,useir2,prof_avg,std_avg,
     .			 raz,ibuff,irerr)
      
    
      if (sum(prof_avg).le.0) then
        dv=dmiss
        dfval=dmiss
	    ann_prob=0.0
	  write(luout,638) errmsg2
	  goto 1500
      endif

c-----7---------------------------------------------------------------72
c Screen SHIPS data -- skip if environmental conditions would not
c support an annular hurricane
c-----7---------------------------------------------------------------72

      screen_fail = 0
      ahi         = 0.0
c 
      vmxr = float(ivmx)
      if (ivmx .lt. 85) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,652) vmxr
  652      format(5x,'SCREENING STORM INTENSITY       = ',f6.1,
     +               ' kt      >    84 kt?       ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,653) vmxr
  653      format(5x,'SCREENING STORM INTENSITY       = ',f6.1,
     +               ' kt      >    84 kt?       ---> PASSED')
        endif
      endif
            
      rsstr = 0.1*float(irsst(0))
      if (rsstr .lt. 24.3)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,654) rsstr
  654      format(5x,'SCREENING SST                   = ',f6.1,
     +               ' C       >  24.3 C ?       ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,655) rsstr
  655      format(5x,'SCREENING SST                   = ',f6.1,
     +               ' C       >  24.3 C ?       ---> PASSED')
        endif
      endif
            
      if (rsstr .gt. 29.1)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,656) rsstr
  656      format(5x,'SCREENING SST                   = ',f6.1,
     +               ' C       <  29.1 C ?       ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,657) rsstr
  657      format(5x,'SCREENING SST                   = ',f6.1,
     +               ' C       <  29.1 C ?       ---> PASSED')
        endif
      endif
c 
      shrdr = 0.1*float(ishrd(0))
      if (shrdr .gt. 22.0)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,658) shrdr
  658      format(5x,'SCREENING VERT. SHR             = ',f6.1,
     +               ' kt      <  22.0 kt?       ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,659) shrdr
  659      format(5x,'SCREENING VERT. SHR             = ',f6.1,
     +               ' kt      <  22.0 kt?       ---> PASSED')
        endif
      endif
            
      u200r = 0.1*float(iu200(0))
      if (u200r .lt. -23.0)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,662) u200r
  662      format(5x,'SCREENING 200 hPa ZONAL WIND    = ',f6.1,
     +               ' kt      > -23.0 kt?       ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,663) u200r
  663      format(5x,'SCREENING 200 hPa ZONAL WIND    = ',f6.1,
     +               ' kt      > -23.0 kt?       ---> PASSED')
        endif
      endif
            
      if (u200r .gt. 3.0)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,664) u200r
  664      format(5x,'SCREENING 200 hPa ZONAL WIND    = ',f6.1,
     +               ' kt      <   3.0 kt?       ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,665) u200r
  665      format(5x,'SCREENING 200 hPa ZONAL WIND    = ',f6.1,
     +               ' kt      <   3.0 kt?       ---> PASSED')
        endif
      endif

      refcr = 0.1*float(irefc(0))
      if (refcr .lt. -9.0)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,666) refcr
  666      format(5x,'SCREENING 200 hPa MOM FLUX CONV = ',f6.1,
     +               ' m/s-day >  -9.0 m/s-day?  ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,667) refcr
  667      format(5x,'SCREENING 200 hPa MOM FLUX CONV = ',f6.1,
     +               ' m/s-day >  -9.0 m/s-day?  ---> PASSED')
        endif
      endif

      if (refcr .gt. 11.0)  then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        screen_fail=screen_fail+1
        if (ishort .ne. 1) then
           write(luout,668) refcr
  668      format(5x,'SCREENING 200 hPa MOM FLUX CONV = ',f6.1,
     +               ' m/s-day <  11.0 m/s-day?  ---> FAILED')
        endif
      else 
        if (ishort .ne. 1) then
           write(luout,669) refcr
  669      format(5x,'SCREENING 200 hPa MOM FLUX CONV = ',f6.1,
     +              ' m/s-day <  11.0 m/s-day?  ---> PASSED')
        endif
      endif

      

      

 702  format(5x,a27,i6,a13,13x,a11)
 703  format(5x,a15,f6.1,a14,24x,a11)
 704  format(5x,a21,f6.1,a16,16x,a11)
 705  format(5x,a25,f6.1,a17,11x,a11)
 706  format(5x,a26,f6.1,a25,2x,a11)
 707  format(5x,a29,f6.1,a16,8x,a11)

 
 712  format(19x,a35)
 713  format(19x,a28)
 714  format(19x,a44) 
 715  format(19x,a36) 
 716  format(19x,a41)
 
        
c-----7---------------------------------------------------------------72
c Skip if missing data

      missdata_fail=0

      if (irsst(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      if (ishrd(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      if (ishrs(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        missdata_fail=missdata_fail+1
      endif
      if (ishrg(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      if (iu200(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      if (it200(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      if (irefc(0).eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      if (ivmx.eq.smiss) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        missdata_fail=missdata_fail+1
      endif
      
      if (missdata_fail.gt.0)  then
        write(luout,638) errmsg4
        goto 1500
      endif
 
c-----7---------------------------------------------------------------72
c
c Find radius of coldest Tb pixel in averaged IR profile
c and grab standard deviation at that radius
c 
      tbmin=1.e3
      tbmax=-1.
      irhold=0
      iphold=0

      ! Determine size of prof_avg (i.e. where prof_avg does not
      !    contain missing data)
      do iprof=1,maxrad
	 if (prof_avg(iprof).ne.xmsng) then
	   iphold=iprof
         endif
      enddo

      ! Find radius of coldest pixel and std dev.
      do iprof=1,maxrad
	 if ((prof_avg(iprof).lt.tbmin).and.
     .      (prof_avg(iprof).ne.xmsng)) then
	      tbmin=prof_avg(iprof)
	      cpix=raz(iprof)
	      std_cpix=std_avg(iprof)
	      irhold=iprof
	 endif
      enddo
      
c-----7---------------------------------------------------------------72
c Skip if missing data
      if ((iphold.lt.2).or.(irhold.eq.0)) then
        dv=dmiss
        dfval=dmiss
	    ann_prob=0.0
	  goto 1500
      endif
      if (std_cpix.lt.0)  then
        dv=dmiss
        dfval=dmiss
	    ann_prob=0.0
	  goto 1500
      endif

c-----7---------------------------------------------------------------72
c Calculate variance of radial profile
c      
      call moment(prof_avg(1:iphold),iphold,ave_prof,adev_prof,
     .            sdev_prof,var_prof,skew_prof,curt_prof)
c
c Calculate warm eye - cold ring difference
c 
      do iprof=1,irhold
         if (prof_avg(iprof).gt.tbmax) then
	        tbmax=prof_avg(iprof)
	        eye_diff=tbmax-tbmin
	     endif
      enddo

c-----7---------------------------------------------------------------72
c Screen IR data -- skip if cold eye exists

      if (cpix .lt. 50.) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        if (ishort .ne. 1) then
           write(luout,670) cpix
  670      format(5x,'SCREENING GOES RAD COLD BR TEMP = ',f6.1,
     +               ' km      >  50.0 km?       ---> FAILED')
        endif
        screen_fail=screen_fail+1
      else
        if (ishort .ne. 1) then
           write(luout,671) cpix
  671      format(5x,'SCREENING GOES RAD COLD BR TEMP = ',f6.1,
     +               ' km      >  50.0 km?       ---> PASSED')
        endif
      endif
      
      if (eye_diff .lt. 15.) then
        dv=dmiss
        dfval=dmiss
        ann_prob=0.0
        if (ishort .ne. 1) then
           write(luout,672) eye_diff
  672      format(5x,'SCREENING GOES EYE-RING BR TEMP = ',f6.1,
     +               ' C       >  15.0 C ?       ---> FAILED')
        endif
        screen_fail=screen_fail+1
      else
        if (ishort .ne. 1) then
        write(luout,673) eye_diff
  673   format(5x,'SCREENING GOES EYE-RING BR TEMP = ',f6.1,
     +            ' C       >  15.0 C ?       ---> PASSED')
        endif
      endif
      
      if (screen_fail.gt.0)  then
        if (ishort .eq. 1) then
           nfail = screen_fail
           npass = nscreen-nfail
           write(luout,780) npass,nfail
  780      format('   ## STORM NOT ANNULAR, SCREENING STEP FAILED,',
     +            ' NPASS=',i1,' NFAIL=',i1,15x,
     +            '           ##') 
           go to 1501
        else
           write(luout,723) 
 723       format(25x,'STORM NOT ANNULAR, FAILED SCREENING',/) 
c 
	   write(luout,722) '******************************',
     .                      '***********************'
           write(luout,721) ahi
	   write(luout,722) '******************************',
     .                         '***********************'
        endif
        goto 1500
      else
        if (ishort .eq. 1) then
           write(luout,781)
  781      format('   ## PASSED SCREENING STEP, MIGHT BE ANNULAR,',
     +            ' CALCULATE AHI FROM DISCRIMINANT ANALYSIS  ##') 
        else
           write(luout,724) 
  724      format(25x,'STORM MAY BE ANNULAR, PASSED SCREENING',/,
     +            23x,'CALCULATE AHI FROM DISCRIMINANT ANALYSIS',/)
        endif
      endif
      
 701  format(25x,a31,/) 
 721  format(15x,'*    ANNULAR HURRICANE INDEX (AHI) VALUE = ',f5.0,
     +           '    *',/,15x,
     +       '*   (AHI=100. IS  BEST MATCH TO ANNULAR STRUCTURE)  *',
     + /,15x,'*   (AHI=  1. IS WORST MATCH TO ANNULAR STRUCTURE)  *',
     + /,15x,'*   (AHI=  0.            FOR NO ANNULAR STRUCTURE)  *')
 722  format(15x,a30,a23)
 
 708  format(5x,a33,f5.1,a13,8x,a11)
 709  format(5x,a31,f5.1,a10,13x,a11,/)
 
c-----7---------------------------------------------------------------72
c Standardize data
      sst  = real(irsst(0)) / 10.0
      u200 = real(iu200(0)) / 10.0


      weye_s = (eye_diff - means(1)) / sdev(1)
      var_s  = (var_prof - means(2)) / sdev(2)
      std_s  = (std_cpix - means(3)) / sdev(3)
      sst_s  = (sst      - means(4)) / sdev(4)
      u200_s = (u200     - means(5)) / sdev(5)

      

c Get annular hurricane index

      call ahindex(weye_s,var_s,std_s,sst_s,u200_s ,dv,dfval,ann_prob)


c     Calculate annular hurricane index (ahi) from the discriminant value
c      
c     Specific df scaling factors
c        ahi = ahmin at dfmin 
c        ahi = ahmax at dfmax
c
c     dfmin, dfmax based upon 1995-2006 developmental data and should 
c     result in a ~ 96% hit rate and ~4% false alarm rate - JAK
c     
      dfmin = -0.3
      dfmax =  2.3
      ahmin =  1.0
      ahmax = 100.0
c 
      ahslope = (ahmax-ahmin)/(dfmax-dfmin)
      ahyint  = ahmin - ahslope*dfmin
c 
      ahi   = dfval*ahslope + ahyint
c 
      if (ahi .lt.   1.0) ahi = 1.0
      if (ahi .gt. 100.0) ahi = 100.0
      
      sample_count=sample_count+1
            

c-----7---------------------------------------------------------------72
c Write data
 1501 continue
      if (ishort .eq. 1) then
         iahin = ifix(ahi+0.49)
         write(luout,782) iahin
  782    format('   ## AHI=',i3,'   (AHI OF 100 IS BEST FIT TO ANN.',
     +          ' STRUC., 1 IS MARGINAL, 0 IS NOT ANNULAR) ##') 
      else
         write(luout,722) '******************************',
     .                    '***********************'
         write(luout,721) ahi
         write(luout,722) '******************************',
     .                    '***********************'
      endif
c
c     iwcon = 0
      if (iwcon .eq. 1) then
c        write individual contributions to annular index
      write(luout,603) 'CONTRIBUTIONS TO ANNULAR INDEX'
c     write(luout,604) 'Vertical Shear',' ',dweights(5)*shrd_s + 
c    .                      dweights(6)*shrg_s
c     write(luout,605) 'Radius of Coldest Pixel',' ',
c    .                     dweights(1)*cpix_s
c     write(luout,606) 'GOES Core Symmetry Factor',' ',
c    .                     dweights(3)*var_s + dweights(4)*std_s
c     write(luout,607) 'GOES Eye Temperature',' ',dweights(2)*weye_s
c     write(luout,608) '200 hPa Eddy Fluxes',' ',dweights(8)*refc_s
c     write(luout,609) '200 hPa Zonal Wind',' ',dweights(7)*u200_s
c     write(luout,610) 'Storm Intensity',' ',dweights(9)*vmax_s 
c     write(luout,621) '_','_____________________________',
c    .                      '__________' 
c     write(luout,611) 'TOTAL',' ', dv
c     write(luout,622) 'TOTAL > ',idiv, ' ---->',
c    .                     ' ANNULAR STRUCTURE POSSIBLE'
c     write(luout,623) 'TOTAL < ',idiv, ' ---->',
c    .                     ' ANNULAR STRUCTURE VERY UNLIKELY'
      endif

                   
 602  format(a15,5x,a36,f4.1,a1,4x,a5)
 603  format(/,a56/)
 604  format(23x,a14,a16,f7.3)
 605  format(23x,a23,a7,f7.3)
 606  format(23x,a25,a5,f7.3)
 607  format(23x,a20,a10,f7.3)
 608  format(23x,a19,a11,f7.3)
 609  format(23x,a18,a12,f7.3)
 610  format(23x,a15,a15,f7.3)
 611  format(23x,a5,a25,f7.3,/)
 620  format(a15,a30,a25)
 621  format(a24,a29,a7)
 622  format(18x,a8,f3.1,a6,a27)
 623  format(18x,a8,f3.1,a6,a33) 
 
 

      ! If only 1 of the IR files is within 12h of SHIPS data,
      ! display a note in the data output file, proceed.

      if ((irtg.eq.1).or.(irerr.gt.0)) then
      	 write(luout,639) errmsg5
      else
         write(luout,639) errmsg0
      endif
      
      
      goto 1500
c-----7---------------------------------------------------------------72
 
 901  write(luout,637) errmsg1

1500  continue
      
c-----7---------------------------------------------------------------72      

      RETURN   
      END

c-----7---------------------------------------------------------------72
c--------------------------  SUBROUTINES  ------------------------------
c-----7---------------------------------------------------------------72

      SUBROUTINE ir_prof_avg2(fn_ird1,fn_ird2,fn_iri1,fn_iri2,        
     .                   iyr,useir1,useir2,prof_avg,std_avg,
     .			 raz,ibuff,irerr)
     
c-----7---------------------------------------------------------------72
c  Routine to read in 2 IR radial profile data and average
c  
c
c INPUT 
c    fn_ird1 = filename of 1st IR data file
c    fn_ird2 = filename of 2nd IR data file
c    fn_iri1 = filename of 1st IR information file
c    fn_iri2 = filename of 2nd IR information file
c    iyr = 4-digit storm year
c    useir1 = integer indicating validity of IRRP1.dat, 0=n, 1=y
c    useir2 = integer indicating validity of IRRP2.dat, 0=n, 1=y                    
c
c OUTPUT
c    prof_avg = time average of IR profile
c    std_avg = time average of IR standard deviations
c    raz = radii (km) of prof_avg and std_avg
c    ibuff = (integer) If equal to zero, then disregard prof_avg
c            and std_avg in main program.
c
c-----7---------------------------------------------------------------72

      parameter(maxbyt=1000000) ! max file size (bytes; multiple of 4)
      byte tot(maxbyt)          ! total data file (bytes)
      parameter(maxele=3000,maxlin=3000) ! max image size (elems,lines)
      dimension ximage(maxele,maxlin)
      
      parameter(maxavg=1000)     ! max size of 1D radial profile arrays
      parameter(radmax=600.)  ! max radius of profile output files (km)
      parameter(maxrad=radmax/4) ! max number of elements in profiles
      dimension azav(maxrad),raz(maxrad),std(maxrad) ! averaging arrays
      dimension specr(maxrad),speci(maxrad) ! spectral coefficient arrays
      
      parameter(maxtim=1000)    ! max number of data files
      dimension timarray(maxtim)
      parameter(maxwrd=maxbyt/4) ! max file size (words)
      integer navi(maxwrd)      ! navigation block (words)
      integer area(64)          ! area block (words)
      equivalence (tot(1),navi(1)) ! fills navigation from total
      character*80 fn           ! area file name
      character*80 fnout        ! generic output file name
      character*80 pthar        ! path to area file
      logical swap              ! little or big endian query
      logical fnxst             ! file name query
      integer LL(2)             ! (lat,lon) <---> (y,x) flag
      character*12 stnm         ! storm name
      character*9 stnmabr       ! abbreviated storm name
      character*2 bas           ! ocean basin (AT,EP,WP,SP,CP,NI,SI)
      character*11 lmstarr(maxtim) ! LMST in "MM/DD/hh/mm" format 
      parameter(pi=3.1415926535897932384626433832795) ! define pi
      integer tdiffmin,tdiff,irerr,irerr1,irerr2
      character*29 fnrad       ! Radial Tb profile data file
      integer lurad
      logical radexist
      real xmsng
      integer ir1ex,ir2ex,irex
      integer ir1tg,ir2tg,irtg
      integer useir1,useir2
      character*34 fn_ird1
      character*34 fn_ird2
      character*34 fn_iri1
      character*34 fn_iri2
      character*80 pthbt        ! path to best track file
      parameter(maxfix=200)     ! max no of best track fixes (per storm)
      dimension vnz(maxfix),pnz(maxfix)
      dimension xlanz(maxfix),xlonz(maxfix)
      dimension tnz(maxfix),sdla(maxfix),sdlo(maxfix)
      integer im(maxfix/4),id(maxfix/4)

c Start and end time of IR time averaging period    
      real bt_start,bt_end

c percent pixels along circles
      dimension pp00(maxrad),pp10(maxrad),pp20(maxrad),pp30(maxrad)
      dimension pp40(maxrad),pp50(maxrad),pp60(maxrad),pp70(maxrad)

      parameter(maxbuff=40)
      real buff_azav(maxrad,maxbuff),buff_std(maxrad,maxbuff),
     .     prof_avg(maxrad),std_avg(maxrad)
      integer ibuff,ip,ib
      integer iphold,irhold,iphold_min

c-----7---------------------------------------------------------------72

      xmsng=-1.0
      itim=0
      ibuff=0
      iphold_min=1000
      irnum=0
      
      lurad=46

c Zero out buffer and averaged IR arrays
      do 12 i=1,maxrad
        do 11 j=1,maxbuff
	   buff_azav(i,j)=0.0
	   buff_std(i,j)=0.0
 11	 continue
        prof_avg(i)=0.0
	 std_avg(i)=0.0
 12   continue


c-----7---------------------------------------------------------------72
c Read in 1st radial profile
c-----7---------------------------------------------------------------72


       if (useir1.eq.0) then
           goto 446
       else
       
        fnrad=fn_ird1
	irnum=irnum+1     

       open(unit=lurad,file=fnrad,status='old',err=446)
       call read_radprof(lurad,raz,azav,std,pp50,irerr1)
       close(lurad)

 
c-----7---------------------------------------------------------------72
c Find radius of coldest Tb pixel and grab standard deviation
c at that radius
c 
         tbmin=1.e3
	 irhold=0
	 iphold=0
	 
	do iprof=1,maxrad
	   if ((azav(iprof).ne.xmsng).and.(std(iprof).ne.xmsng)) then
	     iphold=iprof
	   endif
	enddo
	 
	do iprof=1,maxrad
	   if ((azav(iprof).lt.tbmin).and.(azav(iprof).ne.xmsng)) then
	      tbmin=azav(iprof)
	      cpix=raz(iprof)
	      std_cpix=std(iprof)
	      irhold=iprof
	   endif
	enddo
       
	! Check data -- skip if missing data
	if ((tbmin.eq.xmsng).or.(std_cpix.eq.xmsng)) then
	   tbmin=1.e3
	   goto 446
	endif
	
	if (irhold.eq.0) goto 446
	if (iphold.eq.0) goto 446
	if (iphold.lt.iphold_min) iphold_min=iphold


c-----7---------------------------------------------------------------72
c Store current IR data in buffer arrays for averaging 
c 
      
          
        do ip=1,maxrad	  
	   buff_azav(ip,irnum)=azav(ip)
	   buff_std(ip,irnum)=std(ip)
	enddo
	
	endif

c-----7---------------------------------------------------------------72
  446  continue
c-----7---------------------------------------------------------------72

c-----7---------------------------------------------------------------72
c Read in 2nd radial profile
c-----7---------------------------------------------------------------72
 

       if (useir2.eq.0) then
           goto 449
       else
       
        fnrad=fn_ird2
	irnum=irnum+1
       

       open(unit=lurad,file=fnrad,status='old',err=449)
       call read_radprof(lurad,raz,azav,std,pp50,irerr2)
       close(lurad)

 
c-----7---------------------------------------------------------------72
c Find radius of coldest Tb pixel and grab standard deviation
c at that radius
c 
         tbmin=1.e3
	 irhold=0
	 iphold=0
	 
	do iprof=1,maxrad
	   if ((azav(iprof).ne.xmsng).and.(std(iprof).ne.xmsng)) then
	     iphold=iprof
	   endif
	enddo
	 
	do iprof=1,maxrad
	   if ((azav(iprof).lt.tbmin).and.(azav(iprof).ne.xmsng)) then
	      tbmin=azav(iprof)
	      cpix=raz(iprof)
	      std_cpix=std(iprof)
	      irhold=iprof
	   endif
	enddo
       
	! Check data -- skip if missing data
	if ((tbmin.eq.xmsng).or.(std_cpix.eq.xmsng)) then
	   tbmin=1.e3
	   goto 449
	endif
	
	if (irhold.eq.0) goto 449
	if (iphold.eq.0) goto 449
	if (iphold.lt.iphold_min) iphold_min=iphold


c-----7---------------------------------------------------------------72
c Store current IR data in buffer arrays for averaging
c 
          
          
        do ip=1,maxrad	  
	   buff_azav(ip,irnum)=azav(ip)
	   buff_std(ip,irnum)=std(ip)
	enddo
	
	endif

c-----7---------------------------------------------------------------72
  449  continue
c-----7---------------------------------------------------------------72
        if (irnum.eq.0) then
	   goto 444
	endif   

        
	 ! Average IR data
	 do ip=1,iphold_min
           prof_avg(ip)=sum(buff_azav(ip,1:irnum))/2
           std_avg(ip)=sum(buff_std(ip,1:irnum))/2
	 enddo
	 
	 ! Fill out rest with missing value, if necessary
         if (iphold_min.lt.maxrad) then
	   do ip=iphold_min+1,maxrad
             prof_avg(ip)=xmsng
             std_avg(ip)=xmsng
	   enddo
	 endif
	         
        ! Zero out buffer arrays
	 do ip=1,maxrad
	   do ib=1,maxbuff
	     buff_azav(ip,ib)=0.0
	     buff_std(ip,ib)=0.0
	   enddo
	 enddo
       

c-----7---------------------------------------------------------------72
c 
444   continue
c
c-----7---------------------------------------------------------------72

      irerr = irerr1 + irerr2

ccccc output prof_avg and raz to file

      RETURN
      END

c-----7---------------------------------------------------------------72
c-----7---------------------------------------------------------------72

      subroutine read_ships(luls,sname4,ilyr,ilmon,ilday,iltime,ivmx,
     .                      iu200,it200,irsst,irefc,ishrd,ishtd,ishrs,
     .                      ishts,ishrg,endoffile)

c Thomas Cram, CIRA, November 2005
c
c Reads information from the SHIPS model reanalysis data files
c      (lsdiaga_1982_2004_rean.dat, lsdiage_1982_2004_rean.dat)
c
c INPUT
c   luls = SHIPS data file unit number
c
c OUTPUT
c   sname4 = First 4 letters of storm name
c   ilyr = 2-digit year
c   ilmon = UTC month
c   ilday = UTC day
c   iltime = UTC hour
c   ivmx = Maximum winds (kt)
c   iu200 = 200 mb zonal wind (kt)
c   it200 = 200 mb temperature (deg C)
c   irsst = Reynolds SST (deg C)
c   irefc = Relative eddy momentum flux convergence (m/s/day)
c   ishrd = 850-200 mb shear magnitude (kt)
c   ishtd = Heading (deg) of SHRD shear vector
c   ishrs = 850-500 mb shear magnitude (kt)
c   ishts = Heading (deg) of SHRS shear vector
c   ishrg = Generalized 850-200 mb shear magnitude (kt; takes into 
c             account all levels)
c   endoffile = Integer specifying if the end of the file has been 
c               reached (0 = no, 1 = yes)
c
c-----7---------------------------------------------------------------72

      parameter (mft=20)
      
      character*130 iline
      character*110 iheader
      integer ilyr,ilmon,ilday,iltime,ivmx
      integer iper,itime(0:mft),iincv(0:mft),ilat(0:mft),
     .        ilon(0:mft),isst(0:mft),id20c(0:mft),
     .        id26c(0:mft),ihcon(0:mft)
      
      integer idist(0:mft),irsst(0:mft),iu200(0:mft),it200(0:mft),
     .        ie000(0:mft),iepos(0:mft),ieneg(0:mft),iepss(0:mft),
     .        ienss(0:mft),irhlo(0:mft),irhmd(0:mft),irhhi(0:mft),
     .        ishrd(0:mft),ishtd(0:mft),ishrs(0:mft),ishts(0:mft),
     .        ishrg(0:mft),ipslv(0:mft),iz850(0:mft),id200(0:mft),
     .        irefc(0:mft),it000(0:mft),ir000(0:mft),iz000(0:mft),
     .        igoes(0:mft),igoesm3(0:mft),ird20(0:mft),ird26(0:mft),
     .        irhcn(0:mft)
           
      integer endoffile
      character*4 sname4

      endoffile=0

c     Read the SHIPS data file
      read(luls,110,end=1200,err=1200) sname4,ilyr,ilmon,ilday,
     .                                 iltime,ivmx,iheader
 110  format(1x,a4,1x,3(i2.2),1x,i2.2,1x,i4,a110)

 1100 continue

c-----7---------------------------------------------------------------72
      read(unit=luls,fmt=111,end=1200,err=1200) iline
 111  format(a130)

      if (iline(117:120).eq.'LAST') goto 1300

c Format read definitions 
 112       format(1x,23(i4,1x))
 114       format(11x,i4)
 116       format(11x,21(i4,1x))
 117       format(11x,21(i4,1x),5x,i4)

	! TIME
      if (iline(117:120).eq.'TIME') then
cc           read(iline,112) (itime(k),k=-2,mft)
           read(iline,116) (itime(k),k=0,mft)
      endif
      
	! DELV
      if (iline(117:120).eq.'DELV') then
           read(iline,114) iper
      endif
	
	! INCV
      if (iline(117:120).eq.'INCV') then
cc           read(iline,112) (iincv(k),k=-2,mft)
           read(iline,116) (iincv(k),k=0,mft)
      endif
	
	! LAT
      if (iline(117:120).eq.'LAT ') then
cc           read(iline,112) (ilat(k),k=-2,mft)
           read(iline,116) (ilat(k),k=0,mft)
      endif
	
	! LON
      if (iline(117:120).eq.'LON ') then
cc           read(iline,112) (ilon(k),k=-2,mft)
           read(iline,116) (ilon(k),k=0,mft)
      endif
	
	! CSST
      if (iline(117:120).eq.'CSST') then
cc           read(iline,112) (isst(k),k=-2,mft)
           read(iline,116) (isst(k),k=0,mft)
      endif
	
	! DTL
      if (iline(117:120).eq.'DTL') then
           read(iline,116) (idist(k),k= 0,mft)
      endif
      
	! D20C
      if (iline(117:120).eq.'D20C') then
cc           read(iline,112) (id20c(k),k=-2,mft)
           read(iline,116) (id20c(k),k=0,mft)
      endif
	
	!D26C
      if (iline(117:120).eq.'D26C') then
cc           read(iline,112) (id26c(k),k=-2,mft)
           read(iline,116) (id26c(k),k=0,mft)
      endif

	! HCON
      if (iline(117:120).eq.'HCON') then
cc           read(iline,112) (ihcon(k),k=-2,mft)
           read(iline,116) (ihcon(k),k=0,mft)
      endif


c-----7---------------------------------------------------------------72

	! RSST
      if (iline(117:120).eq.'RSST') then
           read(iline,117) (irsst(k),k= 0,mft),irlag
      endif
	  
	! U200
      if (iline(117:120).eq.'U200') then
            read(iline,116) (iu200(k),k= 0,mft)
      endif
	
	! T200
      if (iline(117:120).eq.'T200') then
            read(iline,116) (it200(k),k= 0,mft)
      endif
	
	! E000
      if (iline(117:120).eq.'E000') then
            read(iline,116) (ie000(k),k= 0,mft)
      endif

	! EPOS
      if (iline(117:120).eq.'EPOS') then
            read(iline,116) (iepos(k),k= 0,mft)
      endif

	! ENEG
      if (iline(117:120).eq.'ENEG') then
            read(iline,116) (ieneg(k),k= 0,mft)
      endif

	! EPSS
      if (iline(117:120).eq.'EPSS') then
            read(iline,116) (iepss(k),k= 0,mft)
      endif

	! ENSS
      if (iline(117:120).eq.'ENSS') then
            read(iline,116) (ienss(k),k= 0,mft)
      endif

	! RHLO
      if (iline(117:120).eq.'RHLO') then
            read(iline,116) (irhlo(k),k= 0,mft)
      endif

	! RHMD
      if (iline(117:120).eq.'RHMD') then
            read(iline,116) (irhmd(k),k= 0,mft)
      endif

	! RHHI
      if (iline(117:120).eq.'RHHI') then
            read(iline,116) (irhhi(k),k= 0,mft)
      endif

c-----7---------------------------------------------------------------72
	! SHRD
      if (iline(117:120).eq.'SHRD') then
         read(iline,116) (ishrd(k),k= 0,mft)
      endif

	! SHTD
      if (iline(117:120).eq.'SHTD') then
         read(iline,116) (ishtd(k),k= 0,mft)

c           Convert ishtd from heading to direction
            do k=0,mft
               if (ishtd(k) .lt. imiss) then
                  ishtd(k) = 180 + ishtd(k)
                  if (ishtd(k) .gt. 360) ishtd(k) = ishtd(k)-360
               endif
            enddo
      endif
         
      ! SHRS
      if (iline(117:120).eq.'SHRS') then
         read(iline,116) (ishrs(k),k= 0,mft)
      endif

       ! SHTS
      if (iline(117:120).eq.'SHTS') then
            read(iline,116) (ishts(k),k= 0,mft)

c           Convert ishts from heading to direction
            do k=0,mft
               if (ishts(k) .lt. imiss) then
                  ishts(k) = 180 + ishts(k)
                  if (ishts(k) .gt. 360) ishts(k) = ishts(k)-360
               endif
            enddo
      endif
         
	  ! SHRG
      if (iline(117:120).eq.'SHRG') then
         read(iline,116) (ishrg(k),k= 0,mft)
      endif
      
c-----7---------------------------------------------------------------72
      ! PSLV
      if (iline(117:120).eq.'PSLV') then
         read(iline,116) (ipslv(k),k= 0,mft)
      endif

      ! Z850
      if (iline(117:120).eq.'Z850') then
         read(iline,116) (iz850(k),k= 0,mft)
      endif

      ! D200
      if (iline(117:120).eq.'D200') then
         read(iline,116) (id200(k),k= 0,mft)
      endif

      ! REFC
      if (iline(117:120).eq.'REFC') then
         read(iline,116) (irefc(k),k= 0,mft)
      endif

      ! T000
      if (iline(117:120).eq.'T000') then
         read(iline,116) (it000(k),k= 0,mft)
      endif

      ! R000
      if (iline(117:120).eq.'R000') then
         read(iline,116) (ir000(k),k= 0,mft)
      endif

      ! Z000
      if (iline(117:120).eq.'Z000') then
         read(iline,116) (iz000(k),k= 0,mft)
      endif

      ! IR00
      if (iline(117:120).eq.'IR00') then
         read(iline,116) (igoes(k),k= 0,mft)
      endif

      ! IRM3
      if (iline(117:120).eq.'IRM3') then
         read(iline,116) (igoesm3(k),k= 0,mft)
      endif

      ! RD20
      if (iline(117:120).eq.'RD20') then
         read(iline,116) (ird20(k),k= 0,mft)
      endif

      ! RD26
      if (iline(117:120).eq.'RD26') then
         read(iline,116) (ird26(k),k= 0,mft)
      endif

      ! RHCN
      if (iline(117:120).eq.'RHCN') then
         read(iline,116) (irhcn(k),k= 0,mft)
      endif

      goto 1100

c-----7---------------------------------------------------------------72
 1200 continue
      endoffile=1
c-----7---------------------------------------------------------------72

 1300 continue

      RETURN
      END
      
c-----7---------------------------------------------------------------72
c-----7---------------------------------------------------------------72
c 
      subroutine read_radprof(lurad,raz,azav,std,pp50,irerrflg)
      

c Thomas Cram, May 2005
c
c Reads information from the IR brightness temperature radial
c profile data.
c
c INPUT
c   lurad = unit number for radial profile data file
c
c OUTPUT
c   raz = radii (km)
c   azav = Tb profile
c   std = standard deviation
c   pp50 = percentage of -50C pixels
c   irerrflg = 1.0 if error reading ir radial profile file
c
c-----7---------------------------------------------------------------72

      parameter(maxrad=150)
      
      real raz(maxrad),azav(maxrad),std(maxrad),
     .     pp00(maxrad),pp10(maxrad),pp20(maxrad),pp30(maxrad),
     .     pp40(maxrad),pp50(maxrad),pp60(maxrad),pp70(maxrad)
     
      integer irerrflg
      
      irerrflg=0.0
      radtot = 0.0
     
      do iprof=1,maxrad
         read(unit=lurad,fmt=100,end=567,err=567) 
     .                raz(iprof),azav(iprof),std(iprof),
     .                pp00(iprof),pp10(iprof),pp20(iprof),
     .                pp30(iprof),pp40(iprof),pp50(iprof),
     .                pp60(iprof),pp70(iprof)
         radtot = radtot + 1
      enddo     
 100  format(f6.1,1x,10(f6.2,1x))
       
 567  continue
 
      if (radtot.lt.maxrad) then
        irerrflg = 1.0
      endif 
      
      return
      end
c 
c-----7---------------------------------------------------------------72
c-----7---------------------------------------------------------------72

      BLOCK DATA
      
c***********************************************************************      
c Contains standard deviations, means, discriminant parameter
c weights, and discriminant function dividing value for use in the 
c annular hurricane linear discriminant analysis.  
c
c Order of array elements:
c weye, var, std, sst, u200
c
c Last Modified: Feb 16, 2007:  JAK
c
c 1) Reduced number of factors to 5 from 9
c 2) replaced the means and standard deviations to represent the screened
c    sample in the 1995-2006 developmental data
c************************************************************************
      REAL sdev(5),means(5),dweights(5),idiv
      
      common /MOMENTS/ sdev,means
      common /DWEIGHTS/ dweights
      common /DIVIDER/ div
      
      data means/ 56.73, 558.21, 4.23, 
     .            27.68, -8.09 /

      data sdev/  21.61, 218.52, 2.45,
     .           1.04, 5.62 /
       
      data dweights/ 0.80944,  0.61429,  -0.44537,
     .                -0.80173,   -0.14644/
      
      data div/0.75904/

      END

c-----7---------------------------------------------------------------72

      SUBROUTINE ahindex(weye,var,std,sst,u200,dv,val,prob)

c-----7---------------------------------------------------------------72
c     Subroutine to apply disciminant weights contained in the BLOCK
c     DATA routine to create discrimnant fucntion value (val) and
c     a probability associated with val.
c
c     Last Modified: Feburary 16, 2007 - JAK
c     1) now uses 5 predictors
c     2) new fit to the probability estimation
c***********************************************************************

      REAL weye,var,std,sst,u200
      REAL dv,val,prob
      
      ! Discriminant weights (block data)
      common /DWEIGHTS/ dweights(5)

      ! Discriminant function divider (block data)
      common /DIVIDER/ div

c-----7---------------------------------------------------------------72

      dv=0.0
      val=0.0

      dv=dweights(1)*weye + dweights(2)*var +
     .   dweights(3)*std  + dweights(4)*sst + dweights(5)*u200 
      
      val=dv-div
      
      ! Determine annular hurricane probability
      !
      ! quadratic function fits the observe PDF from the 1995-2006
      ! dependent data
      if (val.lt.-0.3)then
         prob=0.0
      else if (val .ge. -0.3 .and. val .lt. 1.929)then
         prob=-0.0183 * val**3 + 0.0689 * val**2
     1        +0.2483 * val    + 0.1347
      else if (val .ge. 1.929) then
         prob=1.0
      endif
      if (prob.gt.1.0) prob=1.0


      RETURN
      END

c-----7---------------------------------------------------------------72
c-----7---------------------------------------------------------------72
c 
      subroutine detend(idum)
c
c Jim Kossin
c Determines endian-ness of host machine. Returns index 1 for Little
c Endian, index 4 for Big Endian. The index specifies least significant
c byte position of 4-byte word.
c 
      integer i,j,idum
      byte word(4)
      equivalence(word(1),i)
      do j=1,4
         word(j)=0
      enddo
      i=1
      if(word(1).ne.0)then
         idum=1
      else
         idum=4
      endif
      return
      end
c
c-----7---------------------------------------------------------------72
c-----7---------------------------------------------------------------72
c 
      INTEGER*4 FUNCTION LIT(C)
      IMPLICIT NONE
      CHARACTER*4 C
C --- local variables
      INTEGER*4 L
      CHARACTER*4 C1
      EQUIVALENCE (C1,L)
C 
      C1=C
      LIT=L
      RETURN
      END
C 
      CHARACTER*4 FUNCTION CLIT(L)
      IMPLICIT NONE
      INTEGER L
C --- local variables
      CHARACTER*4 C
      INTEGER*4 L1
      EQUIVALENCE(L1,C)
      L1=L
      CLIT=C
      RETURN
      END
c
c ++++END ANNULAR HURRICANE INDEX MODULE++++
