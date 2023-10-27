&trkParamsNL
  vortcrit=7.5,
  vmaxweak=45.0,
  vortadjfact=0.60,
  doGdatCon=.true.,
  vortcritadjust=.true.,
! -- a bug in the speed brake?  for 01e.2012? 2012051512

!  doSpeedBrake=.false.,
!  doAccelBrake=.false.,

  doSpeedBrake=.true.,
  doAccelBrake=.true.,

!  forspdMax=45.0,
  forspdMax=30.0,
  accelMax=30.0,
  
  forspdLatET=40.0,
  forspdMaxET=45.0,

  forspdAdjfact=1.25,
  forspdMaxTau0=12,
  
!  rfindPsl=1.0,
!  rfindVrt850=1.0,
  rfindPsl=0.5,
  rfindVrt850=0.5,
  rfindGen=0.5,
  
! set the scale and min slp deficit for turning off the tracker
!
  sdistpsl=120,
  rminPsldef=-0.5,

  rlatmax=60.0,
  rmaxConSep=180.0,
  undef=1e20,

! time period to set the motion to the input/obs for making the first guess
!
  ktauMaxInitialMotion=12,

! smooth the motion from previous smthMotionTauPeriod motions
!
!  dosmthMotion=.true.,
  dosmthMotion=.false.,
  smthMotionTauPeriod=18.0,

/

&verbOse
  verbConGdat=.false.
!  verbMfTrackem=.true.
  verbGrhiloPsl=.false.	
!  verbGrhiloVrt850=.true.
!  verbMftrack=.true.
!  verbTrackem=.true.
/
        
