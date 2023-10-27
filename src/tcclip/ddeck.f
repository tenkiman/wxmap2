c ---------------------------------------------------------------------
      program ddeck
c ---------------------------------------------------------------------

ckpd  Comments installed by the anonymous original authors are marked
ckpd  "cxxx".  They, and the program, were originally all uppercase.

ckpd  This program computes the 8 forecast errors using the objective
ckpd  aids technique file "techlist.dat" and the best track file, whose
ckpd  name has format Bbbnnyy.DAT.

c  record of changes:
c
c     Modified to use new data format,  7/98   A. Schrader
c     Modified to figure errors for TAU's 96 and 120,  12/98  A. Schrader

ckpd  To avoid maintaining copies of the same code in multiple places,
ckpd  do common block declarations and declarations of the variables
ckpd  they contain from include files named after the common blocks.

ckpd  --------------------- parameterize program -----------------------

      include 'ddeckparms.inc'

      INCLUDE 'bestc.inc'
      INCLUDE 'bstchr.inc'
      INCLUDE 'fcstc.inc'
      INCLUDE 'techc.inc'
      INCLUDE 'posit.inc'
      INCLUDE 'mtechs.inc'
      INCLUDE 'requst.inc'

      character*30      techlst

      logical*1         endb

ckpd FIXME  The limits of arrays should be fully described parameters,
ckpd FIXME  not magic numbers.  Do this right, the way a good C
ckpd FIXME  programmer would do it.

ckpd                    Variable iclear is a  integer loop
ckpd                    counter with legal values 1 to naids used to clear
ckpd                    array mobj.

      integer           iclear

ckpd                    Variable ierrnm is a  integer loop
ckpd                    counter with legal values 1 to 8 used to read
ckpd                    data into elements of array errlst.


      integer           ierrnm

ckpd                    Variable ntech is a  integer that holds
ckpd                    the two digit decimal objective aid technique
ckpd                    number when read from the techlist.dat file.
ckpd                    Legal values are 0 - naids.

      integer           ntech

ckpd                    Variable irderr is a  integer that holds
ckpd                    the error return values from fnwc library
ckpd                    routine readb().  Legal values as returned by
ckpd                    readb() are 0 and -1, 0 indicates normal
ckpd                    completion, while -1 indicates an error.

      integer           irderr

ckpd                    Variable iflag is a  integer that holds
ckpd                    the "end of list" return value from subroutine
ckpd                    reada().  The expected values are 1 for "more
ckpd                    file left to read", and -1 for "end of file
ckpd                    seen".

      integer           iflag

      integer           iarg

cajs  ktauarr ( kmax )  Array of forecast periods (tau)

cx    filenames    
      character*120   tlist,decreq,btrk,objtec,outfil


cxxx  blat,blng      bstrk positions
cxxx  hlat,hlng      interpolated hourly positions
cxxx  dtgb           dtg for corresponding bstrk positions
cxxx  fstdy          first dtg
cxxx  n              total number of bstrk points

cxxx  idif           total number of interpolated points

cxxx  flat,flng      fcst positions
cxxx  error          jmax types & kmax fcst periods
cxxx  idtg           fcst dtg
cxxx  jmax           types of error
cxxx  kmax           fcst periods (number of tau's)
cxxx  kdel           tau interval (except for last tau)

      endb = .false.

      kdel = 12
      ktauarr(1) = 0
      ktauarr(2) = 12
      ktauarr(3) = 24
      ktauarr(4) = 36
      ktauarr(5) = 48
      ktauarr(6) = 72
      ktauarr(7) = 96
      ktauarr(8) = 120
      

cxxx  tech,gech      kmax fcst periods, nt techniques for lat & long,
ckpd                 respectively
cxxx  wlat,wlng      carq & wrng positions
cxxx  mobj           nt technique names
cxxx  nt             number of techniques

cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
cx    Get the filenames off the command line
      call getarg(iarg,tlist)
      iarg = iarg + 1
      call getarg(iarg,decreq)
      iarg = iarg + 1
      call getarg(iarg,btrk)
      iarg = iarg + 1
      call getarg(iarg,objtec)
      iarg = iarg + 1
      call getarg(iarg,outfil)
      iarg = iarg + 1

cxxx  Read the list of technique names and numbers.  Note that the first
cxxx  line in the data file is a header so skip it.  The next two lines
cxxx  must contain the position names and numbers.

      do 5 iclear = 1 , naids

        mobj( iclear ) = '    '
cajs  Added this line to initialize the ic array.  12/98
        ic( iclear ) = 0

    5 continue

ckpd  Open techlist.dat file.
cx    open ( 1 , file = ' ' , status = 'old' )
      open ( 1 , file = tlist , status = 'old' )

ckpd  Set up to find the high technique number in the file.

      nt = 0

      rewind 1

ckpd  Throw away the header line.

      read ( 1 , * )

ckpd  Read the CARQ and WRNG lines.

ckpd FIXME  Notice that reading the techlist.dat file expecting CARQ and
ckpd FIXME  WRNG to be the first two data lines after the header line
ckpd FIXME  may fail miserably if the techlist.dat file is out of sorted
ckpd FIXME  order due to editing errors.

      read ( 1 , '( i3 , 1x , a4 )' ) nposit(1) , iposit(1)

      read ( 1 , '( i3, 1x, a4 )' ) nposit(2) , iposit(2)

      ntech = 0

   10 continue

      read ( 1 , '( a30 )', end=20 ) techlst

cajs  read ( techlst , '( i3 , 1x , a4 )' ) ntech, mobj( ntech )

      ntech = ntech + 1

cajs  The ic array is read in from the STATS column of techlist.dat
cajs  here but this is ignored since later in reada all of the ic 
cajs  elements are arbitarily set to 1.  
cajs  This is to prevent confusion about having to turn on two
cajs  flags (ERRORS and STATS) in order to get an aid in the triangle
cajs  table output.
      read ( techlst , '( 4x , a4, 10x, i1 )' ) mobj( ntech ), 
     &      ic( ntech )

ckpd  Keep track of the highest technique number seen so far.
cajs  nt = max( nt , ntech )

cxxx  Save the CLIP technique number for the cross track / along track
cxxx  with respect to CLIP computation.

      if ( mobj( ntech ) .eq. 'CLIP' ) nclip = ntech

      if( ntech .lt. naids ) goto 10

   20 continue

cajs  Save the highest technique number      
      nt = ntech

      close( 1 )

cxxx  Read in the user's requests for number of errors and format of
cxxx  output.

cxxx  errlst(i)  =  .true.  (compute the error)
cxxx                .false.  (don't compute the errors)
cxxx  dbase      =  .true.   (write in dbase format)
cxxx                .false.  (write in jtwc ddeck format)

ckpd  This file is ddkrqst.cur or ddkrqst.fnl in 1992.11.09 ATCF.

cx    open ( 2 , file = ' ' , status = 'old' , err = 900 )
      open ( 2 , file = decreq , status = 'old' , err = 900 )

      read( 2, '(8(/,L7 ),/,/,L7)' ) 
     &     ( errlst(ierrnm), ierrnm = 1, 8 ), dbase

      close ( 2 )

cxxx  unit5 : bstrk file
cxxx  unit7 : objtech file
cxxx  unit8 : d-deck containing eight fcst errors

ckpd  Open best track (Bbbnnyy.DAT, where bb is basin id, nn is storm
ckpd  number, yy is forecast year) data file.

cx    open( 5 , file = ' ' , status = 'old' , err = 910 )
      open( 5 , file = btrk , status = 'old' , err = 910 )

ckpd  Open objective aids (Abbnnyy.DAT, bb, nn, yy as above) data file.

cx    open( 6 , file = ' ' , status = 'old' , err = 920 )
      open( 7 , file = objtec , status = 'old' , err = 920 )

ckpd  Open output (ddeck.txt) file.

cx    open( 7 , file = ' ' , status = 'unknown' , err = 930 )
      call openfile( 8, outfil, 'unknown', ioerror )
      if( ioerror .lt. 0 ) goto 930
cajs      open( 8 , file = outfil , status = 'unknown' , err = 930 )

      rewind 7

      rewind 8

cxxx  Read the first A-Deck line to get the storm id.
cajs  read ( 7 , '( t71 , a6 )' ) strmid
      read ( 7, '(a2,2x,a2,4x,a2)' ) strmid(1:2), strmid(3:4), 
     &     strmid(5:6)
      rewind 7

cxxx  Reads & interpolates bstrk file.

      call readb( 5 , irderr )

      if ( irderr .ne. 0 )
     &  stop 'Abnormal termination by readb() routine in ddeck().'

ckpd  Top of loop to read the objective aids forecast data file and
ckpd  process

  300 continue

cxxx    Reads objective aids file.

ckpd    Routine reada() has three possible return values in iflag:

ckpd    iflag =  1, Successfully loaded a DTG-full, more to read.
ckpd    iflag =  0, Successfully loaded a DTG-full, no more to read.
ckpd    iflag = -1, Saw EOF when trying to start reading a DTG.
ckpd                (This is an error return, normal "out of data"
ckpd                return value is 0.)

        call reada( iflag )

cxxx    Calculates error.
ckpd    We have data to process if we got back at least a zero in iflag.

200     if (iflag .ge. 0) call fill

cxxx  If iflag .le. 0, the end of the objective aids forecast data file
cxxx  was reached.

ckpd DEBUG      write(8,'('' ddeck(): aborting early!'')')

ckpd DEBUG      write(*,'('' ddeck(): aborting early!'')')

ckpd DEBUG      goto 400

      if ( iflag .gt. 0 ) go to 300

ckpd DEBUG  400 continue

      close( 5 )

      close( 7 )

      close( 8 )

      stop 'ddeck(): Normal run termination.'

  900 stop 'ddeck(): Error opening user request file.'

  910 stop 'ddeck(): Error opening best track file.'

  920 stop 'ddeck(): Error opening objective techniques file.'

  930 stop 'ddeck(): Error opening output file.'

      end
c ---------------------------------------------------------------------
      subroutine calerr( iaid )
c ---------------------------------------------------------------------

ckpd  To avoid maintaining copies of the same code in multiple places,
ckpd  do common block declarations and declarations of the variables
ckpd  they contain from include files named after the common blocks.

      include 'ddeckparms.inc'

      INCLUDE 'bestc.inc'
      INCLUDE 'bstchr.inc'
      INCLUDE 'fcstc.inc'
      INCLUDE 'techc.inc'
      INCLUDE 'posit.inc'
      INCLUDE 'mtechs.inc'
      INCLUDE 'requst.inc'

ckpd                   Debug variable tmpdtg is an eight byte character
ckpd                   string used to hold the returned date time group
ckpd                   when icrdtg() is used to fill it with the DTG of
ckpd                   the closest interpolated hour position of a best
ckpd                   track to a forecast aid position in computing
ckpd                   error TKE.

ckpd DEBUG      character*8      tmpdtg

ckpd                   Debug variable j1tmp is used to pass the value of
ckpd                   j1, but in a four byte integer as required by
ckpd                   icrdtg().

ckpd DEBUG      integer          j1tmp

ckpd                   Variable lastvp is a  integer used as a
ckpd                   last valid position index array when doing the
ckpd                   search described in the description of ktau,
ckpd                   below.  It has the same set of legal values as
ckpd                   ktau.

      integer        lastvp

ckpd                   Variable ktau is a  integer used as a
ckpd                   loop counter and array index, with values in the
ckpd                   range 1 to kmax, when searching through the
ckpd                   forecast taus prior to the one of current concern
ckpd                   to find one with a valid position, in the case
ckpd                   where some tau to tau delta is needed for a
ckpd                   computation.  Since the synoptic hour position
ckpd                   for the 00 hour of the forecast comes from the
ckpd                   CARQ or WRNG, or, last choice, from the
ckpd                   corresponding best track position, there is alway
ckpd                   a valid position for that tau, or things are too
ckpd                   broken to be fixed by software.  That is the ktau
ckpd                   = 1 arrays entry, and we search from the position
ckpd                   entry at that tau foreward to the one prior to
ckpd                   the currently being considered tau to find a most
ckpd                   recent second valid position for the delta
ckpd                   determination.

      integer          ktau

ckpd                   Function validpos() captures the concept of what
ckpd                   a valid (versus a "no value") latitude and
ckpd                   longitude pair looks like in the objective aids
ckpd                   data files.  It returns ".true." for a valid
ckpd                   position, and ".false." for a "no value" lat/long
ckpd                   datum.

      logical*1        validpos

ckpd                   Variable iaid is a  integer array index,
ckpd                   passing through this routine (otherwise unused)
ckpd                   to xtcatc(), with legal values 1 - naids and
ckpd                   semantics the chosen aid for which error
ckpd                   computations are currently in progress.

      integer          iaid

ckpd                   Variable ihour is a four byte integer.  That
ckpd                   precision is needed because ihour is returned
ckpd                   from the dtgdif() fnwc library routine which for
ckpd                   other uses sometimes returns large hour
ckpd                   quantities, not the case here.  Ihour's returned
ckpd                   computed value is the number of hours from the
ckpd                   storm data start to the currently considered DTG.

      integer          ihour

ckpd                   Variable kfcst is a  integer loop
ckpd                   counter with legal values 1 to kmax used as the
ckpd                   second array index in array error and indexes it
ckpd                   by the forecast tau number.

      integer          kfcst

ckpd                   Variable jerrtp is a  integer loop
ckpd                   counter with legal values 1 to 8 used as the
ckpd                   first array index in array error and indexes it
ckpd                   by the error type number.

      integer          jerrtp

ckpd                   Variable jjhour is a  integer array index
ckpd                   that holds as legal values the hour offset from
ckpd                   the beginning of the storm to the time of the
ckpd                   position forecast for which error calculations
ckpd                   are being done.  It is restricted in legal values
ckpd                   to 1 - 1201 by the limits of the arrays it
ckpd                   indexes.

      integer          jjhour

ckpd                   Variable jhour is a  integer used as a
ckpd                   loop counter where the count needs to be in
ckpd                   forecast hours; thus its legal values are
ckpd                   restricted to the hour array index limits of 1 -
ckpd                   1201.

      integer          jhour

ckpd                   Variable j1 is a  integer to which the
ckpd                   value of jjhour is copied in situations where it
ckpd                   might need changing due to being beyond the
ckpd                   beginning or end of the working dataset in the
ckpd                   hour arrays, but we don't want to clobber the
ckpd                   value of jjhour.  Its legal values are those of
ckpd                   jjhour.

      integer          j1

ckpd                   Variable j2 is a  integer used like j1,
ckpd                   but in situations where a pair of copies of
ckpd                   jjhour are needed for the same reasons.

      integer          j2

ckpd                   Variable hge is a four byte real used to pass a
ckpd                   control value to dirdst(), and to return the
ckpd                   direction between the two passed lat/longs. Its
ckpd                   legal values are the decimal directions in
ckpd                   degrees and tenths.  After some processing, the
ckpd                   final legal value is between 0.1 and 360.0, for
ckpd                   valid directions, and 0.0, for a "no valid
ckpd                   direction" return value.

      real             hge

ckpd                   Variable dir has the same type, legal values, and
ckpd                   use as variable hge.  They both exist because we
ckpd                   are frequently dealing with 1) the direction of
ckpd                   the best track storm motion vector, 2) the
ckpd                   direction of the forecast storm motion vector,
ckpd                   and 3) the direction of the error vector, and
ckpd                   need more than one place to store the values.

      real             dir

ckpd                   Variable smdir has the same type, legal values,
ckpd                   and content semantics as hge and dir.  It is used
ckpd                   to hold the matching angle to a distance in the
ckpd                   routines that seek the smallest distance between
ckpd                   a forecast and a best track over a forecast
ckpd                   period.

      real             smdir

ckpd                   Variable dis is a four byte real, with legal
ckpd                   values in signed nautical miles less than the
ckpd                   circumferance of the earth, and is used to store
ckpd                   the returned value of dirdst() calls, the
ckpd                   distance between two lat/long positions.

      real             dis

ckpd                   Variable small is a four byte real, with legal
ckpd                   values in signed nautical miles less than the
ckpd                   circumferance of the earth, and is used to store
ckpd                   the value of the smallest distance seen so far
ckpd                   between best track and forecast where that
ckpd                   distance is being sought.

      real             small

ckpd                   Variable cc is a four byte real, with legal
ckpd                   values from minus two pi to two pi, probably, and
ckpd                   holds error distance values expressed as radian
ckpd                   offsets along a great circle of the earth.  It is
ckpd                   used in trig calculations needed for error
ckpd                   statistics.

      real             cc

ckpd                   Variable pi is a four byte real, holds the math
ckpd                   constant pi, is used for angle to radian
ckpd                   calculations before using the FORTRAN intrinsic
ckpd                   trig routines, and the data statement below that
ckpd                   gives it a value has a ridiculous precision for a
ckpd                   data type that only holds about six decimal
ckpd                   digits of precision, just so you know that I
ckpd                   know.

      real             pi

      data pi / 3.1415926535898 /

cxxx  This routine calculates eight tropical cyclone forecast errors:

ckpd  Each of these error measures has been checked by a hand plot of a
ckpd  couple of the forecast aids plus CLIP and best track, to assure
ckpd  that the correct computations were being done or correct vector
ckpd  projections were being taken and both sensible and accurate
ckpd  results returned.  Lots of bugs were expunged in the process, both
ckpd  from these routines, and from the fnwc library routines they call.

cxxx    error(1,k) : FTE (n mi)    forecast error

ckpd                 FTE is the absolute distance in nautical miles
ckpd                 between the aid's forecast storm position, and the
ckpd                 best track's "best estimate" storm position, for
ckpd                 the same tau.

cxxx    error(2,k) : XTC (n mi)    cross track with respect to cliper

ckpd                 XTC is a measure of the forecasting aid's skill in
ckpd                 reproducing the CLIP climatological forecast.  It
ckpd                 measures the parallel component of the error vector
ckpd                 between the CLIP and forecast positions, projected
ckpd                 onto the CLIP "prior tau to current tau" motion
ckpd                 vector.  If the dropped perpendicular hits the
ckpd                 CLIP motion vector at a place corresponding to a
ckpd                 time earlier than the forecast tau, the error is
ckpd                 signed negative; after is signed positive.

cxxx    error(3,k) : ATC (n mi)    along track with respect to cliper

ckpd                 ATC is a measure of the forecasting aid's skill in
ckpd                 reproducing the CLIP climatological forecast.  It
ckpd                 measures the perpendicular component of the error
ckpd                 vector between the CLIP and forecast positions,
ckpd                 projected onto the CLIP "prior tau to current tau"
ckpd                 motion vector.  If the dropped perpendicular hits
ckpd                 the CLIP motion vector from the right side as seen
ckpd                 from the direction of CLIP motion, the error is
ckpd                 signed positive; from the left is signed negative.
ckpd                 That is, the error sign is with respect to the
ckpd                 mariner's compass, not the mathematician's compass.

ckpd                 The ATC error, because it is measured by dropping
ckpd                 perpendiculars rather than by swinging arcs, has an
ckpd                 inherent negative bias; a forecast with the same
ckpd                 speed as CLIP but a different heading will return a
ckpd                 negative ATC. Better would be an error measure that
ckpd                 returned zero in that case: i.e., a radial motion
ckpd                 error measure.

cxxx    error(4,k) : TKE (n mi)    track error

ckpd                 TKE is the distance measured from the forecast
ckpd                 position at a synoptic forecast time, and the
ckpd                 closest approach of the best track to that
ckpd                 position, measured by interpolating the best track
ckpd                 positions to have a position for each even hour,
ckpd                 and finding the smallest distance from the forecast
ckpd                 position to one of those best track positions.

cxxx    error(5,k) : SPD (kts*10)  speed error

ckpd                 SPD is the difference in the rate of storm travel
ckpd                 over the ground as predicted by the forecast aid,
ckpd                 and as estimated by the best track.  It is measured
ckpd                 by walking the interpolated best track positions,
ckpd                 measuring the distance from hour to hour, and by
ckpd                 walking the forecast positions, also accumulating
ckpd                 distances, and, at each forecast tau and position,
ckpd                 taking the distance difference since the initial
ckpd                 forecast DTG of the accumulated distances and
ckpd                 dividing by the time since the initial DTG in hour.
ckpd                 Lesser travel over the forecast gets a negative
ckpd                 signed error, greater gets positive.

ckpd                 Notice that the method of computation yields speed
ckpd                 errors over the cumulative time since the forecast
ckpd                 initial tau, not just between forecast taus.

cxxx    error(6,k) : TME (hr)      timing error

ckpd                 TME is the time difference in hours between the
ckpd                 date time group of the forecast position and of a
ckpd                 closest distance even hour position on a copy of
ckpd                 the best track which has been interpolated hour by
ckpd                 hour.  If the closest position on the best track is
ckpd                 prior to the forecast tau, the error is signed
ckpd                 negative (the forecast is arriving late); if the
ckpd                 closest position on the best track has a time after
ckpd                 the forecast tau,,the error is signed positive (the
ckpd                 forecast is arriving early).

cxxx    error(7,k) : XTE (n mi)    cross track error

ckpd                 XTE is a measure of the forecasting aid's skill in
ckpd                 reproducing the storm best track.  It measures the
ckpd                 parallel component of the error vector between the
ckpd                 best track and forecast positions, projected onto
ckpd                 the best track "prior hour to current tau"
ckpd                 interpolated motion vector.  If the dropped
ckpd                 perpendicular hits the best track motion vector at
ckpd                 a place corresponding to a time earlier than the
ckpd                 forecast tau, the error is signed negative; after
ckpd                 is signed positive.


cxxx    error(8,k) : ATE (n mi)    along track error

ckpd                 ATE is a measure of the forecasting aid's skill in
ckpd                 reproducing the storm's best track.  It measures
ckpd                 the perpendicular component of the error vector
ckpd                 between the best track and forecast positions,
ckpd                 projected onto the best track "prior hour to
ckpd                 current tau" interpolated motion vector.  If the
ckpd                 dropped perpendicular hits the best track storm
ckpd                 motion vector from the right side as seen from the
ckpd                 direction of best track storm motion, the error is
ckpd                 signed positive; from the left is signed negative.
ckpd                 That is, the error sign is with respect to the
ckpd                 mariner's compass, not the mathematician's compass.

ckpd                 The ATE error, because it is measured by dropping
ckpd                 perpendiculars rather than by swinging arcs, has an
ckpd                 inherent negative bias; a forecast with the same
ckpd                 speed as the storm best track but a different
ckpd                 heading will return a negative ATC. Better would be
ckpd                 an error measure that returned zero in that case:
ckpd                 i.e., a radial motion error measure.


cxxx  Note that logical array errlst is checked to see if the error is
cxxx  to be computed.  This is specified by a file read in the main
cxxx  program. This allows certain error types which take a long time to
cxxx  run (TKE) to be ignored, until the final stats for a storm are to
cxxx  be computed.

      do 100 kfcst = 1 , kmax

        do 95 jerrtp = 1 , jmax

          error( jerrtp , kfcst ) = -9999.

   95   continue

  100 continue

cxxx  ihour:      idtg     index sequential number
cxxx  jjhour:     idtg+tau index sequential number

ckpd  Find out how many hours are between the beginning of the storm
ckpd  data and the tau for which we are currently involved in doing
ckpd  error calculations.

      call dtgdif( fstdy , idtg , ihour )

ckpd  Bump it by one, since we are using an array for the hourly
ckpd  interpolations whose first array has index number 1.

      ihour = ihour + 1

ckpd  If we've somehow gotten past the DTG for which we are computing
ckpd  errors, give up.

      if ( ihour .gt. idif ) return

      if ( ihour .lt. 1 ) ihour = 1

cxxx  Loop 150 for all tau periods.

      do 150 kfcst = 2 , kmax

cxxx  Calculate forecast errors: FTE -- error(1,kfcst),
cxxx                             XTC -- error(2,kfcst),
cxxx                             ATC -- error(3,kfcst).

ckpd    With ihour set to be an index into the hour by hour arrays for the
ckpd    forecast's base DTG, make jjhour the hour index to the same arrays
ckpd    for the (offset from that base) time of the current future
ckpd    position forecast.

cajs        jjhour = ihour + ( kfcst - 1 ) * kdel

ckpd    Fudge in for the fact that we don't make a forecast at tau 60
ckpd    hours, but do make one at 72 hours, so our even 12 hour
ckpd    forecasting steps have a gap in them.

cajs        if ( kfcst .eq. kmax ) jjhour = jjhour + kdel
         jjhour = ihour + ktauarr( kfcst )

ckpd      Guaranteeing a valid position is much more complex than this,
ckpd      due to poorly followed specification of what a "no valid data"
ckpd      entry for a latitude, longitude pair should be encoded as in
ckpd      MS-DOS ATCF; hide all the grunge in a function, validpos().

ckpd        if ( ( jjhour        .ge. ihour    ) .and.
ckpd     &       ( jjhour        .le. idif     ) .and.
ckpd     &       ( flat( kfcst ) .ge. -90.0 )          ) then

ckpd FIXME  Why are we checking something we just assured, in the first
ckpd FIXME  clause of the test for process / don't process this aid at
ckpd FIXME  this forecast plus hour tau?

        if ( ( jjhour        .ge. ihour    ) .and.
     &       ( jjhour        .le. idif     ) .and.
     &       validpos( flat( kfcst ) , flng( kfcst ) ) ) then

ckpd      Since, given a valid forecast position we compute an entire
ckpd      output record of different forecast errors based on that
ckpd      position, there is no need for an "else" clause for the above
ckpd      "if ... then"; its only purpose would be to emit a line of all
ckpd      "-9999" error entries, a waste of space and time.

ckpd      If the FTE error has been requested to be computed ...

          if ( errlst( 1 ) ) then

ckpd        Set the direction  holder to a flag value consulted by
ckpd        dirdst on input to control whether the subroutine bothers to
ckpd        do the trig for the direction calculation.  Here, we want
ckpd        it.

            hge = 1.0

ckpd        FTE is just the unsigned distance between the forecast
ckpd        position and the best track position for the same time, so
ckpd        let dirdst() fill it in directly.
cx
cx  compute the fte distance and direction from concurrent best track posit 
cx

            call dirdst( hlat( jjhour ) , hlng(  jjhour   ) ,
     &                   flat( kfcst  ) , flng(  kfcst    ) ,
     &                   hge ,            error( 1 , kfcst )  )

          endif

cxxx    xtcatc() computes XTC and ATC

          if ( errlst( 2 ) .or. errlst( 3 ) )
     &      call xtcatc( iaid ,
     &                   kfcst ,
     &                   error( 2 , kfcst ) ,
     &                   error( 3 , kfcst )   )

cxxx    Calculate cross and along track errors: XTE -- error(7,kfcst),
cxxx                                            ATE -- error(8,kfcst)

          if ( errlst( 7 ) .or. errlst( 8 ) ) then

            j1 = jjhour - 1

            j2 = jjhour

            if ( j1 .lt. 1 ) then

              j1 = 1

              j2 = 2

            endif

            dir = 1.0
cx
cx call dirdst to calculate the tangent to best track
cx
            call dirdst( hlat( j1 ) , hlng( j1 ) ,
     &                   hlat( j2 ) , hlng( j2 ) ,
     &                   dir        , dis          )

ckpd            dir = amod( ( hge - dir + 359.0 ) , 360.0 ) + 1.0
cx
cx  angle between the tangent to best track and the fte direction
cx
            dir = amod( ( hge - dir + 359.9 ) , 360.0 ) + 0.1

            dis = 1.0

            if ( ( dir .gt. 180.0 ) .and. (dir .lt. 360.0 ) ) then

              dis = -1

              dir = 360.0 - dir

            endif
cx
cx  convert fte to radians
cx
            cc = ( error( 1 , kfcst ) / 60.0 ) * ( pi / 180.0 )
cx
cx  calculate sin(xte) - this is the law of sines on a sphere
cx                  sina/sinA=sinb/sinB   (A = cc, a = xte, b = 90, B = fte)
cx
            error( 7 , kfcst ) = sin( cc ) * sin( dir * pi / 180.0 )
cx
cx  cos(xte)
            error( 7 , kfcst ) =
     &        sqrt( 1.0 - error( 7 , kfcst ) * error( 7 , kfcst ) )

cx  check for possible zero in denom  ... bs 1/8/96
            if ( error(7,kfcst) .eq. 0.0) error(7,kfcst)=0.0000001

cx
cx  calculate cos(ate) (law of cosines on a sphere, modified)
cx  cosa = cosb*cosc + sinb*sinc*cosA
cx  where a=fte, b=xte, c=ate, A is a 90 degree angle
cx
            error( 8 , kfcst ) = cos( cc ) / error( 7 , kfcst )

cx  concurrent problem with undefined in acos, asin  ... bs 1/8/96
            error( 7, kfcst ) = min ( 1.0, error( 7, kfcst))
            error( 7, kfcst ) = max (-1.0, error( 7, kfcst))
            error( 8, kfcst ) = min ( 1.0, error( 8, kfcst))
            error( 8, kfcst ) = max (-1.0, error( 8, kfcst))
cx
cx  convert xte, ate  back to nautical miles from cos of angle
cx
            error( 7 , kfcst ) =   ( acos( error( 7 , kfcst ) ) * 60.0 )
     &                           * ( 180.0 / pi )
     &                           * dis

            error( 8 , kfcst ) =   ( acos( error( 8 , kfcst ) ) * 60.0 )
     &                           * ( 180.0 / pi )

            if ( dir .gt. 90.0 )
     &        error( 8 , kfcst ) = - error( 8 , kfcst )

          endif

cxxx      Calculate track and timing errors: TKE -- error(4,kfcst),
cxxx                                         TME -- error(6,kfcst)

          if ( errlst( 4 ) .or. errlst( 6 ) ) then

            small = 9999.0

ckpd        Make sure _all the variables modified in the "if (dis .le.
ckpd        small) then" block below have initial values, in case the
ckpd        condition is never satisfied.

            smdir = 0.0

            j1 = 0

ckpd FIXME  These ihour, idif loop limits assume that the smoothed best
ckpd FIXME  track is never so severely modified from the CARQ position
ckpd FIXME  as to move the ihour position past the current forecast tau
ckpd FIXME  position, not a safe assumption for a slow moving storm.
ckpd FIXME  The synoptic CARQ +00hr position, not the best track +00hr
ckpd FIXME  position, should be the starting position for measuring this
ckpd FIXME  skill, with the subsequent positive tau positions taken from
ckpd FIXME  the smooth best track.

ckpd FIXME  This calls into question the entire existance of this error
ckpd FIXME  measure, which should measure storm motion relative to the
ckpd FIXME  then estimated position of the storm, compared to aid
ckpd FIXME  forecast relative to the same starting place, not aid skill
ckpd FIXME  relative to information ( the smooth best track forecast
ckpd FIXME  initial time position, possibly developed long afterwards )
ckpd FIXME  nowhere available at the time of the forecast.  Skill should
ckpd FIXME  be measured modulo information available at forecast time,
ckpd FIXME  not with respect to information unavailable to _any_
ckpd FIXME  forecast technique at forecast time.

            do 200 jhour = ihour , idif

              dir = 1.0

ckpd FIXME  Notice that the TKE and TME calculations work only with the
ckpd FIXME  closest _even_hour_ point of the interpolated best track to
ckpd FIXME  the forecast position.  For just a little more effort, the
ckpd FIXME  next closer of either the prior or else the subsequent
ckpd FIXME  hourly interpolated best track position (relative to the
ckpd FIXME  closest one) to the forecast position could be found, and
ckpd FIXME  then the closest approach of the line between them to the
ckpd FIXME  forecast position could be found, giving error estimates
ckpd FIXME  with considerably more fidelity to reality.

              call dirdst( hlat( jhour ) , hlng( jhour ) ,
     &                     flat( kfcst ) , flng( kfcst ) ,
     &                     dir           , dis             )

            if ( dis .le. small ) then

              small = dis

              smdir = dir

              j1 = jhour

            endif

200         continue

            if ( j1 .gt. 1 ) then

              dir = 1.0

              call dirdst( hlat( j1 - 1 ) , hlng( j1 - 1 ) ,
     &                     hlat( j1     ) , hlng( j1     ) ,
     &                     dir,            dis               )

ckpd          Protect against losing track of a "no interesting
ckpd          direction" result returned in dir from dirdst().

              if ( abs ( dir ) .ge. 0.1 ) then

ckpd          Find the error direction relative to the direction of the
ckpd          storm's prior hour interpolated direction of motion.

ckpd          Surely that isn't what was intended!

ckpd              dir = amod( ( smdir - dir + 359.0 ) , 360.0 ) + 1.0

ckpd          Set the direction to a value from 0.1 to 360.0.  Value
ckpd          0.0 is reserved for a "no interesting direction" value,
ckpd          usually used when the corresponding distance is zero.

                dir = amod( ( smdir - dir + 359.9 ) , 360.0 ) + 0.1

              endif

              error( 4 , kfcst ) = small

              if ( dir .gt. 180.0 ) error( 4 , kfcst ) = - small

ckpd          If the forecast position is nearest a storm best track
ckpd          position for a time earlier in the best track than the
ckpd          time of the current forecast tau, then the aid is running
ckpd          slow (the storm is outrunning the aid) and a negative
ckpd          timing error is stored.  Conversely, if we are nearest a
ckpd          best track position later in the best track than the
ckpd          forecast position's tau, then the aid is running fast (the
ckpd          aid is outrunning the storm), and a positive timing error
ckpd          is stored.

              if ( j1  .lt. idif  ) error( 6 , kfcst ) = j1 - jjhour

ckpd DEBUG              if (       ( mobj( iaid ) .eq. 'OTCM'     )
ckpd DEBUG     &             .and. ( kfcst        .eq. 5          )
ckpd DEBUG     &             .and. ( idtg         .eq. '91090200' ) ) then

ckpd DEBUG                call dirdst( hlat( j1    ) , hlng( j1    ),
ckpd DEBUG     &                       flat( kfcst ) , flng( kfcst ),
ckpd DEBUG     &                       dir           , dis            )

ckpd DEBUG                j1tmp = j1

ckpd DEBUG                call icrdtg( fstdy , tmpdtg , ( j1tmp - 1 ) )

ckpd DEBUG                write
ckpd DEBUG     &            (
ckpd DEBUG     &              8 ,
ckpd DEBUG     &              '(
ckpd DEBUG     &                    '' best track DTG    = '' , a8 ,
ckpd DEBUG     &                / , '' j1                = '' , i8 ,
ckpd DEBUG     &                / , '' hlat( j1 )        = '' , f12.3 ,
ckpd DEBUG     &                / , '' hlng( j1 )        = '' , f12.3 ,
ckpd DEBUG     &                / , '' forecast base DTG = '' , a8 ,
ckpd DEBUG     &                / , '' kfcst             = '' , i8 ,
ckpd DEBUG     &                / , '' flat( kfcst )     = '' , f12.3 ,
ckpd DEBUG     &                / , '' flng( kfcst )     = '' , f12.3 ,
ckpd DEBUG     &                / , '' dir               = '' , f12.3 ,
ckpd DEBUG     &                / , '' dis               = '' , f12.3
ckpd DEBUG     &              )'
ckpd DEBUG     &            )
ckpd DEBUG     &            tmpdtg,
ckpd DEBUG     &            j1 ,
ckpd DEBUG     &            hlat( j1 ) ,
ckpd DEBUG     &            hlng( j1 ) ,
ckpd DEBUG     &            idtg,
ckpd DEBUG     &            kfcst ,
ckpd DEBUG     &            flat( kfcst ),
ckpd DEBUG     &            flng( kfcst ),
ckpd DEBUG     &            dir ,
ckpd DEBUG     &            dis

ckpd DEBUG                do 700 j1tmp = j1 - 72 , j1 + 72 , 1

ckpd DEBUG                  call icrdtg( fstdy, tmpdtg, ( j1tmp - 1 ) )

ckpd DEBUG                  if ( mod( ( j1tmp - 1 ) , 6 ) .eq. 0 ) then

ckpd DEBUG                    write( 8 , '(1x,a8,1x,2f12.3,2x,2f12.3)' )
ckpd DEBUG     &                tmpdtg ,
ckpd DEBUG     &                hlat( j1tmp ) ,
ckpd DEBUG     &                hlng( j1tmp ) ,
ckpd DEBUG     &                blat( ( ( j1tmp - 1 ) / 6 ) + 1 ) ,
ckpd DEBUG     &                blng( ( ( j1tmp - 1 ) / 6 ) + 1 )

ckpd DEBUG                  else

ckpd DEBUG                    write( 8 , '(1x,a8,1x,2f12.3)' )
ckpd DEBUG     &                tmpdtg ,
ckpd DEBUG     &                hlat( j1tmp ) ,
ckpd DEBUG     &                hlng( j1tmp )

ckpd DEBUG                  endif

ckpd DEBUG  700           continue

ckpd DEBUG              endif

            endif

          endif

ckpd      The computation as found did not provide for the possibility
ckpd      of missing forecast data, because, while flat(kfcst) and
ckpd      flng(kfcst) were checked to be a valid position pair, the same
ckpd      was not true here of flat(kfcst-1) and flng(kfcst-1), which
ckpd      were used unchecked.  The resulting failure was that the
ckpd      historical aids, converted from three tau to five tau format,
ckpd      were filled in with zeros for the missing positions, and this
ckpd      code happily ran the speed error computations to and from the
ckpd      Greenwich meridian at the equator and the real forecast
ckpd      positions.  Sigh.  Fix it up by making the code flow of
ckpd      control much more complicated and opaque. What else is new?

ckpd FIXME  Notice that this functionality of finding the most recent
ckpd FIXME  prior valid position is done various places in ddeck() with
ckpd FIXME  one dimensional and two dimensional arrays as source data
ckpd FIXME  for positions.  If this code were ported to Fortran-90,
ckpd FIXME  which gives the programmer the capability to take a "slice"
ckpd FIXME  of an array and pass it to a subroutine, the finding of the
ckpd FIXME  next prior valid position, and its return and use, could be
ckpd FIXME  accomplished by a call to a subroutine, hiding this absurd
ckpd FIXME  complexity, rather than by a complicated set of special case
ckpd FIXME  code at each site where this information is needed.

cxxx      Calculate speed error.

          if ( errlst( 5 ) ) then

            error( 5 , kfcst ) = 0.0

ckpd        Set the last valid positon indicator to a known valid
ckpd        position index.

            lastvp = 1

ckpd        Walk down the position arrays to the tau before kfcst,
ckpd        looking for the last valid position, which may well be the
ckpd        first one.

            do 225 ktau = 1 , kfcst - 1

              if ( validpos( flat( ktau ) , flng ( ktau ) ) )
     &          lastvp = ktau

  225       continue

ckpd        Now make use of what we've learned to set up our best track
ckpd        walk to cover the same time interval as that between our
ckpd        prior and current forecast valid positions.

ckpd            j1 = jjhour - kdel + 1

cajs            j1 = jjhour - ( ( kfcst - lastvp ) * kdel ) + 1

ckpd        Once again, fudge for the fact that we don't have a +60hr
ckpd        forecast.  If we're at the last forecast interval, we've
ckpd        jumped _two_ kdel intervals.

cajs            if ( kfcst .eq. kmax ) j1 = j1 - kdel

            j1 = jjhour - (ktauarr(kfcst) - ktauarr(lastvp)) + 1

ckpd        Check to make sure there _is_ a best track position before
ckpd        the current one, before trying to use it.

            if ( j1 .ge. 2 ) then

ckpd          Add up the little hour to hour distances along the best
ckpd          track to get a grand total storm motion distance
ckpd          corresponding to the time between forecast positions.

              do 250 jhour = j1 , jjhour

                dir = 0.0

                call dirdst( hlat( jhour - 1 ) , hlng( jhour - 1 ) ,
     &                       hlat( jhour     ) , hlng( jhour     ) ,
     &                       dir               , dis                 )

                error( 5 , kfcst ) = error( 5 , kfcst ) + dis

250           continue

              dir = 0.0

ckpd          Use our new knowledge of the last prior valid position
ckpd          forecast to choose between which two points we determine
ckpd          the storm motion as depicted by the forecast, to determine
ckpd          the forecast speed, implicitly.

ckpd              call dirdst( flat( kfcst - 1 ) , flng( kfcst - 1 ) ,
ckpd     &                     flat( kfcst     ) , flng( kfcst     ) ,
ckpd     &                     dir               , dis                 )

              call dirdst( flat( lastvp ) , flng( lastvp ) ,
     &                     flat( kfcst     ) , flng( kfcst     ) ,
     &                     dir               , dis                 )

ckpd          We now have both the best track "actual" storm motion
ckpd          distance, and the storm motion distance as forecast; the
ckpd          forecast distance error (on the way to the forecast speed
ckpd          error) is the signed difference, in the appropriate order,
ckpd          of the two.

              error( 5 , kfcst ) = dis - error( 5 , kfcst )

            endif

          endif

        endif

  150 continue

cxxx  Adjust speed error; error(5,kfcst) contains the distance
cxxx  difference in that tau period only.

      if ( errlst( 5 ) ) then

ckpd    Again, we have to take into account that if a forecast position
ckpd    is invalid, we have to reach back further in time (ktau steps)
ckpd    to find valid information with which to work, we can't just pick
ckpd    up the previous tau's position unchecked.

        do 275 kfcst = 3 , kmax

ckpd      Because we can't just stick the zero we want in error(5,1),
ckpd      we have to special case the lastvp for the first tau.

          lastvp = 1

          do 260 ktau = 1 , kfcst - 1

            if ( error ( 5 , ktau ) .ge. -9000.0 ) lastvp = ktau

  260     continue

          if ( error( 5 , kfcst ) .ge. -9000.0 ) then

ckpd            error( 5 , kfcst ) =
ckpd     &        error( 5 , kfcst ) + error( 5 , kfcst - 1 )

            if ( lastvp .gt. 1 ) then

              error( 5 , kfcst ) =
     &          error( 5 , kfcst ) + error( 5 , lastvp )

ckpd        The "else" condition is that lastvp _is_ 1, in which case we
ckpd        would want to be adding zero, so skip that part.'

            endif

          endif

275     continue

ckpd    Here, at last, we convert to speed errors.  No special
ckpd    processing for the interval between valid errors should be
ckpd    needed, because we're dividing by the total time offset from tau
ckpd    00, not the incremental time offset from the last valid
ckpd    position.

        do 280 kfcst = 2 , kmax

          if ( error( 5 , kfcst ) .ge. -9000.0 ) then

cajs            if ( kfcst .ne. kmax ) then

ckpd          Another special case for the missing +60 hour forecast tau.

cajs              error( 5 , kfcst ) =
cajs     &         ( error( 5 , kfcst ) * 10.0 )     /
cajs     &         float( ( kfcst * kdel ) - kdel )

cajs            else

cajs              error( 5 , kfcst ) =
cajs     &          error( 5 , kfcst ) * 10.0 / float( kfcst * kdel )

cajs            endif

             error( 5 , kfcst ) = 
     &            error( 5 , kfcst ) * 10.0 / float( ktauarr(kfcst) )

          endif

280      continue

      endif

      return

      end
c ---------------------------------------------------------------------
      subroutine fill
c ---------------------------------------------------------------------

cxxx  This routine fills flat,flng array for error calculations and
cxxx  writes:

cxxx   error(1,k) : FTE (n mi)
cxxx   error(2,k) : XTC (n mi)
cxxx   error(3,k) : ATC (n mi)
cxxx   error(4,k) : TKE (n mi)
cxxx   error(5,k) : SPE (kts)
cxxx   error(6,k) : TME (hr)
cxxx   error(7,k) : XTE (n mi)
cxxx   error(8,k) : ATE (n mi)

ckpd  To avoid maintaining copies of the same code in multiple places,
ckpd  do common block declarations and declarations of the variables
ckpd  they contain from include files named after the common blocks.

      include 'ddeckparms.inc'

       INCLUDE 'bestc.inc'
       INCLUDE 'bstchr.inc'
       INCLUDE 'fcstc.inc'
       INCLUDE 'techc.inc'
       INCLUDE 'posit.inc'
       INCLUDE 'mtechs.inc'
       INCLUDE 'requst.inc'

ckpd                   Function validpos() captures the concept of what
ckpd                   a valid (versus a "no value") latitude and
ckpd                   longitude pair looks like in the objective aids
ckpd                   data files.  It returns ".true." for a valid
ckpd                   position, and ".false." for a "no value" lat/long
ckpd                   datum.

      logical*1        validpos

ckpd                   Variable ihour needs 4 byte precision as the
ckpd                   third parameter of dtgdif().

      integer          ihour

ckpd                   Variable icw is a  integer used as an
ckpd                   array index and at the same time as a counter in
ckpd                   a loop from 1 to 2, with the semantics of
ckpd                   choosing either CARQ or WRNG for position
ckpd                   forecast error computations.

      integer          icw

ckpd                   Variable ltau is a  integer used as a
ckpd                   loop counter and index witht he semantics of
ckpd                   choosing one of the five forecast taus (+12, +24,
ckpd                   +36, +48, or +72 hours from the forecast synoptic
ckpd                   time).

      integer          ltau

ckpd                   Variable iaid is a  integer used as a
ckpd                   loop counter and array index.  It has the
ckpd                   semantics of identifying one of the objective aid
ckpd                   techniques by the technique number, from 1 - naids.
ckpd                   Notice tht this leaves out CARQ and WRNG, which
ckpd                   are really records of positions forecast, not
ckpd                   objective aids, and which share the aid number 0.

      integer          iaid

ckpd FIXME  Again, this is unnecessarily complex.  It would be far
ckpd FIXME  better to make arrays with common dimension sizes, and just
ckpd FIXME  leave the unwanted ones unused, instead of having this
ckpd FIXME  proliferation of nearly semantically identical variables.
ckpd FIXME  The latter leads quite promptly to program maintainer
ckpd FIXME  confusion and added maintenance expense.

ckpd                   Variable kfcst is a  integer used as a
ckpd                   loop counter and array index with the semantics
ckpd                   of choosing one of the six forecast taus (+00,
ckpd                   +12, +24, +36, +48, or +72 hours from the
ckpd                   forecast synoptic time).  Contrast to ltau.

      integer          kfcst

ckpd                   Variable jerrtp is a  integer used as a
ckpd                   loop counter and array index with the semantics
ckpd                   of choosing one of the eight error types.

      integer          jerrtp

ckpd                   Variable lhour is a  integer used as a
ckpd                   computational variable and array index.  It has
ckpd                   the semantics of a number of hours from the start
ckpd                   of a set of storm data, plus one to make it a one
ckpd                   based index.

      integer          lhour

ckpd                   Variable hge is a  real used to control
ckpd                   subroutine dirdst at calling time and to hold the
ckpd                   returned direction component.  It has the
ckpd                   semantics of degrees and tenths, and the desired
ckpd                   range is 0.1 to 360.0 for situations where the
ckpd                   direction is valid, and 0.0 for situations where
ckpd                   there is not a valid direction, such as with a
ckpd                   zero distance.

      real             hge

cxxx  Calculates idtg index in hourly best track positions.

      call dtgdif( fstdy , idtg , ihour )

      ihour = ihour + 1

      if ( ( ihour .lt. 1 ) .or. ( ihour .gt. idif ) ) return

      iclip = 0

cxxx  Forecast errors for position cards ( CARQ and WRNG ).
cxxx  Note that FTE is the only error calculated.

      do 125 icw = 1 , 2

        do 100 kfcst = 1 , kmax

          do 95 jerrtp = 1 , jmax

            error( jerrtp , kfcst ) = -9999.

   95     continue

  100   continue

ckpd    We are counting backwards in time through the values stored on
ckpd    the CARQ or WRNG line, whose entries are at 00hr, -6hr, -12hr,
ckpd    -18hr and -24hr from the forecast synoptic hour in the order
ckpd    ltau indexes them.

        do 110 ltau = 1 , 5

ckpd      Guaranteeing a valid position is much more complex than this,
ckpd      due to poorly followed specification of what a "no valid data"
ckpd      entry for a latitude, longitude pair should be encoded as in
ckpd      MS-DOS ATCF; hide all the grunge in a function, validpos().

ckpd          if ( poslat( ltau , icw ) .ge. -90.0 ) then

          if (
     &         validpos( poslat( ltau , icw ) ,
     &                   poslng( ltau , icw )   )
     &       ) then

            hge = 1.0

            lhour = ihour - ( ( ltau - 1 ) * 6 )

            if ( lhour .gt. 0 ) then

              call dirdst( hlat(   lhour       ) ,
     &                     hlng(   lhour       ) ,
     &                     poslat( ltau , icw  ) ,
     &                     poslng( ltau , icw  ) ,
     &                     hge ,
     &                     error( 1     , ltau ) )

ckpd DEBUG              write ( 8,
ckpd DEBUG     &          '(
ckpd DEBUG     &          / , '' fill():  ihour............= '' , i8 ,
ckpd DEBUG     &          / , '' fill():  lhour............= '' , i8 ,
ckpd DEBUG     &          / , '' fill():  ltau.............= '' , i8 ,
ckpd DEBUG     &          / , '' fill():  icw..............= '' , i8 ,
ckpd DEBUG     &          / , '' fill():  hlat(lhour)......= '' , f10.1 ,
ckpd DEBUG     &          / , '' fill():  hlng(lhour)......= '' , f10.1 ,
ckpd DEBUG     &          / , '' fill():  poslat(ltau,icw).= '' , f10.1 ,
ckpd DEBUG     &          / , '' fill():  poslng(ltau,icw).= '' , f10.1 ,
ckpd DEBUG     &          / , '' fill():  hge..............= '' , f10.1 ,
ckpd DEBUG     &          / , '' fill():  error(1,ltau)....= '' , f10.1
ckpd DEBUG     &          )' )
ckpd DEBUG     &          ihour ,
ckpd DEBUG     &          lhour ,
ckpd DEBUG     &          ltau ,
ckpd DEBUG     &          icw ,
ckpd DEBUG     &          hlat(lhour) ,
ckpd DEBUG     &          hlng(lhour) ,
ckpd DEBUG     &          poslat(ltau,icw) ,
ckpd DEBUG     &          poslng(ltau,icw) ,
ckpd DEBUG     &          hge ,
ckpd DEBUG     &          error(1,ltau)

            endif

          endif

  110   continue

        maxv( 1 ) = poswnd( icw )

cxxx  Output the errors.

        call out7( ( -1 * icw ) , iposit( icw ) )

  125 continue

cxxx  Fill flat,flng array for obj tech's, call calerr, and write to
cxxx  tape7. Compute the errors and print them only if the technique
cxxx  made a forecast for this dtg unless dbase = true. Then print them
cxxx  regardless.

  150 continue

      do 200  iaid = 1 , nt

        if ( ( iaid         .ne. nposit( 1 ) ) .and.
     &       ( iaid         .ne. nposit( 2 ) ) .and.
     &       ( mobj( iaid ) .ne. '    '      )       ) then

          if ( ic( iaid ) .eq. 1 .or. dbase) then

            do 210 kfcst = 1 , kmax

              flat( kfcst ) = tech( kfcst , iaid )

              flng( kfcst ) = gech( kfcst , iaid )

              maxv( kfcst ) = vmax( kfcst , iaid )

              if ( maxv( kfcst ) .le. 0 ) maxv( kfcst ) = -99

  210       continue

            call calerr( iaid )

            call out7( iaid , mobj( iaid ) )

          endif

        endif

200   continue

      return

      end
c ---------------------------------------------------------------------
      subroutine out7( itech , name )
c ---------------------------------------------------------------------

cxxx  This routine converts error array to integers and writes these
cxxx  integers on unit8.

ckpd  To avoid maintaining copies of the same code in multiple places,
ckpd  do common block declarations and declarations of the variables
ckpd  they contain from include files named after the common blocks.

      include 'ddeckparms.inc'

      INCLUDE 'fcstc.inc'
      INCLUDE 'techc.inc'
      INCLUDE 'posit.inc'
      INCLUDE 'mtechs.inc'
      INCLUDE 'requst.inc'

ckpd                   Function validpos() captures the concept of what
ckpd                   a valid (versus a "no value") latitude and
ckpd                   longitude pair looks like in the objective aids
ckpd                   data files.  It returns ".true." for a valid
ckpd                   position, and ".false." for a "no value" lat/long
ckpd                   datum.

      logical*1        validpos

ckpd These gave an integer overflow, probably due to default short
ckpd integers.

      integer*4        ix
      integer*4        iy

ckpd                   Variable kfcst is a two byte integer used for a
ckpd                   loop counter in the main subroutine loop, and for
ckpd                   an array index many places within that loop.  It
ckpd                   counts through the forecast position numbers (tau
ckpd                   numbers) 1 - kmax.

      integer*2        kfcst

ckpd                   Variable jerrtp is a two byte integer used as a
ckpd                   loop counter and array index taking as values
ckpd                   the (currently 8) possible forecast error types,
ckpd                   errors 1 - 8.

      integer*2        jerrtp

ckpd                   Variable name is a four byte character string,
ckpd                   passed to this subprogram as an input variable.
ckpd                   If this set of errors is based off a CARQ or WRNG
ckpd                   card's set of positions, that aid's ASCII name
ckpd                   will be in variable name.

      character        name*4

ckpd                   Variable iout is a two dimensional array of two
ckpd                   byte integers, with dimensions number of forecast
ckpd                   error types by number of standard forecast
ckpd                   synoptic times (taus).  It is used as a place in
ckpd                   which to build up the error values as integers to
ckpd                   achieve compact display formats, and as a place
ckpd                   from which the error data is written to the
ckpd                   output (d-deck) file on logical unit 7.

      integer*2        iout( 8 , 8 )

ckpd                   Variable ktau is a two byte integer into which
ckpd                   the offset times in hours from the forecast time
ckpd                   for both position errors and forecast errors is
ckpd                   built, and from which it is printed to the output
ckpd                   d-deck file to time stamp the errors relative to
ckpd                   the forecast time (position errors at negative
ckpd                   time offsets, forecast errors at positive time
ckpd                   offsets).


      integer*2        ktau

ckpd FIXME  This next, iaidnm situation is much more complicated than
ckpd FIXME  necessary!  There is a "belt and suspenders" look about the
ckpd FIXME  code, since the needed information is pulled out from
ckpd FIXME  variable name, rather than variable iaidnm, in most of the
ckpd FIXME  code below.

ckpd                   Variable iaidnm is a two byte integer whose value
ckpd                   is passed into this routine as parameter itech
ckpd                   with a (possibly) negative value, and taken as
ckpd                   the absolute value of itech.  While lots of aid
ckpd                   numbers are passed in via itech, iaidnm is only
ckpd                   interesting when the aids are CARQ or WRNG, the
ckpd                   value of itech is then negative, and a position
ckpd                   error forecast print operation is being
ckpd                   requested.  For all other aids, the value of
ckpd                   itech is positive, and itech is used as the index
ckpd                   instead of iaidnm.

      integer*2        iaidnm

      logical*1        nofcst

      do 100 kfcst = 1 , kmax

cxxx  Check all errors to see if they exist. If at least one error
cxxx  exists ( i.e. it is > -9000 ) then set nofcst to false.

        nofcst = .true.

        do 110 jerrtp = 1 , jmax

          if ( error( jerrtp , kfcst ) .gt. -9000.0 ) nofcst = .false.

  110   continue

cxxx  Write the errors unless there is no forecast (all errors = -9999)
cxxx  and the jtwc d-deck format was selected (dbase = .false.).

ckpd FIXME  Notice that this "nofcst" check is how we avoid writing an
ckpd FIXME  error line for the 00hr array entries (those with array time
ckpd FIXME  slot index = 1).  Those entries are otherwise unused.
ckpd FIXME  Question is, why do we look at them at all, here?  I could
ckpd FIXME  make use of them to simplify code elsewhere if they weren't
ckpd FIXME  walked by in this loop!

        if ( dbase .or. (.not. nofcst ) ) then

          do 150 jerrtp = 1 , jmax

            iout( jerrtp , kfcst ) = -9999

            if ( error( jerrtp , kfcst ) .ge. -9000.0 ) then

              ix = abs( error( jerrtp , kfcst ) ) + 0.5

              iy = error( jerrtp , kfcst ) * 10.0

              iout( jerrtp , kfcst ) = isign( ix , iy )

            endif

150       continue

cxxx  Write the position errors.

          if ( ( name .eq. iposit(1) ) .or.
     &         ( name .eq. iposit(2) )      ) then

            ktau = ( -6 ) * ( kfcst - 1 )

            iaidnm = iabs( itech )

ckpd        Guaranteeing a valid position is much more complex than
ckpd        this, due to poorly followed specification of what a "no
ckpd        valid data" entry for a latitude, longitude pair should be
ckpd        encoded as in MS-DOS ATCF; hide all the grunge in a
ckpd        function, validpos().

ckpd            if ( ( ktau                     .ge. -24   ) .and.
ckpd     &           ( poslat( kfcst , iaidnm ) .ge. -90.0 ) .and.
ckpd     &           ( poslng( kfcst , iaidnm ) .ge. -90.0 )       ) then

            if ( ( ktau .ge. -24 ) .and.
     &             validpos( poslat( kfcst , iaidnm ) ,
     &                       poslng( kfcst , iaidnm )   )
     &         ) then

              if ( dbase ) then

                write
     &            ( 8 ,
     &              '(
     &                a6 , a8 , i2.2 , i3.2 , a4 , 2( f5.1 ) , i3 ,
     &                8( i5 )
     &              )'
     &            )
     &            strmid ,
     &            idtg ,
     &            nposit( iaidnm ) ,
     &            ktau ,
     &            name ,
     &            poslat( kfcst , iaidnm ) ,
     &            poslng( kfcst , iaidnm ) ,
     &            maxv( kfcst ) ,
     &            ( iout( jerrtp , kfcst ) , jerrtp = 1 , jmax )

              else

                write
     &            ( 8 ,
     &              '(
     &                i2.2 , a4 , i3.2 , a8 , 8( i5 ) , 1x , a6
     &              )'
     &            )
     &            nposit( iaidnm ) ,
     &            name ,
     &            ktau ,
     &            idtg ,
     &            ( iout( jerrtp , kfcst ) , jerrtp = 1 , jmax ) ,
     &            strmid

              endif

            endif

          else

cxxx  Write the forecast errors.

cajs            ktau = ( kfcst - 1 ) * kdel
cajs            if ( kfcst .eq. kmax ) ktau = ktau + kdel
             ktau = ktauarr( kfcst )


ckpd        Guaranteeing a valid position is much more complex than
ckpd        this, due to poorly followed specification of what a "no
ckpd        valid data" entry for a latitude, longitude pair should be
ckpd        encoded as in MS-DOS ATCF; hide all the grunge in a
ckpd        function, validpos().


ckpd           if ( ( ktau          .ne.   0   ) .and.
ckpd     &           ( flat( kfcst ) .ge. -90.0 ) .and.
ckpd     &           ( flng( kfcst ) .ge. -90.0 )       ) then
            if (
     &           ( ktau .ne. 0 ) .and.
     &           validpos( flat( kfcst ) , flng( kfcst ) )
     &         ) then

              if ( dbase ) then

                write
     &            ( 8 ,
     &              '(
     &                 a6 , a8 , i2.2 , i3.2 , a4 , 2( f5.1 ) , i3,
     &                 8( i5 )
     &              )'
     &            )
     &            strmid ,
     &            idtg ,
     &            itech ,
     &            ktau ,
     &            mobj( itech ) ,
     &            flat( kfcst ) ,
     &            flng( kfcst ) ,
     &            maxv( kfcst ) ,
     &            ( iout( jerrtp , kfcst ) , jerrtp = 1 , jmax )

              else

                write
     &            ( 8 ,
     &              '(
     &                i2.2 , a4 , i3.2 , a8 , 8( i5 ) , 1x , a6
     &              )'
     &            )
     &            itech ,
     &            mobj( itech ) ,
     &            ktau ,
     &            idtg ,
     &            ( iout( jerrtp , kfcst ) , jerrtp = 1 , jmax) ,
     &            strmid

              endif

            endif

          endif

        endif

  100 continue

      return

      end
c ---------------------------------------------------------------------
      subroutine reada( iflag )
c ---------------------------------------------------------------------

ckpd  This routine reads the objective aids forecast data file until a
ckpd  date time group with at least one valid forecast is found, and
ckpd  then fills the tech and gech arrays for further computations.

ckpd  To avoid maintaining copies of the same code in multiple places,
ckpd  do common block declarations and declarations of the variables
ckpd  they contain from include files named after the common blocks.

      include 'ddeckparms.inc'

      INCLUDE 'bestc.inc'
      INCLUDE 'bstchr.inc'
      INCLUDE 'fcstc.inc'
      INCLUDE 'techc.inc'
      INCLUDE 'posit.inc'
      INCLUDE 'mtechs.inc'

cajs  Include file containing record formats for the a and b decks.
      INCLUDE 'dataformats.inc'

ckpd                   Function validpos() captures the concept of what
ckpd                   a valid (versus a "no value") latitude and
ckpd                   longitude pair looks like in the objective aids
ckpd                   data files.  It returns ".true." for a valid
ckpd                   position, and ".false." for a "no value" lat/long
ckpd                   datum.

      logical*1        validpos

ckpd                   Variable kdif holds the  integer value
ckpd                   of delta hours returned from fnwc library
ckpd                   subroutine dtgdif.  Useful values in this routine
ckpd                   are limited by the index limits 1 - 1201 of the
ckpd                   hourly interpolated position arrays.

      integer          kdif

ckpd                   Variable ia is an 80 character string variable
ckpd                   that holds a line of data read in from the
ckpd                   forecast file for further buffer oriented I/O.

cajs  character*80     ia

ckpd                   Variable ndtg is an eight character string
ckpd                   variable that holds the "now" date time group
ckpd                   read from the forecast file; global variable idtg
ckpd                   is used for reads after the first so ndtg won't
ckpd                   be clobbered when the DTG changes, and so that
ckpd                   the two can be compared to detect a DTG change.
ckpd                   Legal values are legal DTG values in format
ckpd                   yymmddhh.

      character*8      ndtg

ckpd                   Variable itech is a  character string
ckpd                   variable that holds the objective aids technique
ckpd                   ASCII name as read from the forecast file.

      character*4      itech

ckpd                   Variable test is a  character string
ckpd                   variable that holds the objective aids technique
ckpd                   ASCII name as read from the forecast file.

      character*4      test

ckpd                   Variable ktau is a  integer that holds
ckpd                   value from 1 to 6, some places 2 to 6, some
ckpd                   places 1 to 5, of the offset in six hour synoptic
ckpd                   period units, of a forecast position (looking
ckpd                   foreward) or a recorded best track position
ckpd                   (looking backward) from the synoptic time of the
ckpd                   currently considered forecast position.

      integer          ktau

ckpd                   Variable jtech is a  integer used as a
ckpd                   loop counter and array index that holds the index
ckpd                   corresponding to the currently considered
ckpd                   objective aids technique number.

      integer          jtech

ckpd                   Variable iaid is a  integer that also
ckpd                   holds an objective aids technique number, but
ckpd                   this time one read from the objective aids
ckpd                   technique list file, and used as a program
ckpd                   control variable.

      integer          iaid

ckpd                   Variable icw is a  integer that is used
ckpd                   an index, either 1 or 2, according as the
ckpd                   position being considered corresponds to CARQ
ckpd                   appropriate data or WRNG appropriate data.

      integer          icw

ckpd                   Variable iflag is a  integer which is a
ckpd                   parameter to this program.  Since this subprogram
ckpd                   returns its results through common blocks, a flag
ckpd                   of satisfactory performance is needed; iflag is
ckpd                   used to return a 1 for normal termination, and a
ckpd                   -1 for failed termination.

      integer          iflag

ckpd                   Variable nseen is a  integer which is
ckpd                   used to count the aids both for which forecasts
ckpd                   exist and also for which error computation has
ckpd                   been requested, separately in each DTG for which
ckpd                   data exists in the forecast data file.   If the
ckpd                   count is zero, the rest of the calculations are
ckpd                   bypassed.

      integer          nseen

ckpd                   Variable domore is a one byte logical used to
ckpd                   provide a record of the fact that the end of the
ckpd                   input file has been seen, to control whether a
ckpd                   branch is taken backwards to process more data.

      logical*1        domore

      integer           istat
      type (AID_DATA) aidRcd
      type (A_RECORD) aRecord


ckpd  Top of loop to read and process the objective aids forecast data
ckpd  cards until either a DTG with a valid forecast is found, or else
ckpd  the aids file is exhausted.
210   continue
cajs        Clearing the ic array is done at the beginning of the program
cajs        do jtech = 1 , nt
cajs           ic( jtech ) = 0
cajs        enddo
        nseen = 0
cxxx  Read a line from the forecast file.
cajs    read ( 7 , '( a80 )' , end = 125 ) ia
cajs    read ( ia , '( i2 , a4 , a8 )' ) iaid , itech , ndtg
        call readARecord( 7, aidRcd, istat )
        if( istat .ne. 1 ) goto 125
        iaid = aidRcd%aRecord(1)%technum
        itech = aidRcd%aRecord(1)%tech
        ndtg = aidRcd%aRecord(1)%DTG(3:10)

cxxx  Fill arrays with null data.
        do icw = 1 , 2
           do ktau = 1 , 5
              poslat( ktau , icw ) = -99.9

ckpd FIXME  Here and elsewhere, this "-99.9" is the "wrong" "no valid
ckpd FIXME  data" value for longitudes.  ATCF _really_ needs one and
ckpd FIXME  only one standard way of saying this, applicable to _any_
ckpd FIXME  longitude value, not merely one associated with a storm
ckpd FIXME  position.  That lets out "0.0" and "-99.9", both of which
ckpd FIXME  can be valid values in particular circumstances, and cries
ckpd FIXME  for "999.9".

              poslng( ktau , icw ) = -99.9
              poswnd( icw )    = -99.0
           enddo
        enddo
        do jtech = 1 , nt
           do ktau = 1 , kmax
              tech( ktau , jtech ) = -99.9
              gech( ktau , jtech ) = -99.9
              vmax( ktau , jtech ) = -99.0
           enddo
        enddo

ckpd    Top of loop to process the forecast cards for a single DTG.
 200    continue
c     reassign index (iaid) to technique using techlist.dat
          iaid = -1
          do ii=1,nt
             test=mobj(ii)
             if(itech(1:4).eq.test(1:4)) then
		iaid=ii
             endif
          enddo
          
cxxx  Check the technique name to see if it is one of the two
cxxx  position cards (i.e. WRNG or CARQ). If it is, save its data
cxxx  in poslat and poslng ...
          if ( ( itech .eq. iposit( 1 ) ) .or.
     &         ( itech .eq. iposit( 2 ) )      ) then
             if ( itech .eq. iposit(1) ) icw = 1
             if ( itech .eq. iposit(2) ) icw = 2
cajs         read ( ia , '( 14x , 10( f4.1 ) , f3.0 )' )
cajs &            ( poslat(ktau, icw), poslng(ktau, icw), ktau= 1,5 ),
cajs &            poswnd( icw )
             do ktau = 1, 5
                call getAidTAU(aidRcd,-((ktau-1)*6),aRecord,istat)
                if( istat .eq. 1 ) then
                   poslat(ktau, icw) = aRecord%lat
                   if( aRecord%NS .eq. 'S' ) then
                      poslat(ktau,icw) = -poslat(ktau,icw)
                   endif
                   poslng(ktau, icw) = aRecord%lon
                   if( aRecord%EW .eq. 'E' ) then
                      poslng(ktau,icw) = 360.0 - poslng(ktau,icw)
                   endif
                   poswnd(icw) = aRecord%vmax
                else
                   poslat(ktau,icw) = -99.9
                   poslng(ktau,icw) = -99.9
                   poswnd(icw) = -99.0
                endif
             enddo
             do ktau = 1 , 5
                if ( ( abs( poslat( ktau , icw ) ) .lt. 0.1 ) .or.
     &               ( abs( poslng( ktau , icw ) ) .lt. 0.1 )      )
     &               then
                   poslat( ktau , icw ) = -99.9
                   poslng( ktau , icw ) = -99.9
                   poswnd( icw )    = -99.0
                endif
             enddo

cxxx      ... Otherwise, save the forecast in tech and gech.
          else
cxxx        If a technique number is .le. 0, ignore it.
ckpd        Since the CARQ and WRNG techniques are both numbered 0,
ckpd        this means we're skipping them here.

cajs             To allow ddeck aids selection in the techlist.dat 
cajs             STATS column simply, uncomment the next line and 
cajs             comment out the two lines following that.
cajs             if( iaid .gt. 0 .and. ic( iaid ) .eq. 1 ) then
             if ( iaid .gt. 0 ) then
                ic( iaid ) = 1
                nseen = nseen + 1
cajs            read( ia, '(14x,10(f4.1),5(f3.0))' )
cajs &               (tech(ktau, iaid), gech(ktau, iaid), ktau = 2, 6),
cajs &               (vmax(ktau, iaid), ktau=2,6)
                do ktau = 2, kmax
cajs                   if( ktau .lt. kmax ) then
cajs                      call getAidTAU(aidRcd,(ktau-1)*12,aRecord,istat)
cajs                   else
cajs                      call getAidTAU( aidRcd, 72, aRecord, istat )
cajs                   endif
                   call getAidTAU(aidRcd, ktauarr(ktau), aRecord, istat)
                   if( istat .eq. 1 ) then
                      tech(ktau, iaid) = aRecord%lat
                      if( aRecord%NS .eq. 'S' ) then
                         tech(ktau,iaid) = -tech(ktau,iaid)
                      endif
                      gech(ktau, iaid) = aRecord%lon
                      if( aRecord%EW .eq. 'E' ) then
                         gech(ktau,iaid) = 360.0 - gech(ktau,iaid)
                      endif
                      vmax(ktau,iaid) = aRecord%vmax
                   else
                      tech(ktau,iaid) = -99.9
                      gech(ktau,iaid) = -99.9
                      vmax(ktau,iaid) = -99.0
                   endif
                enddo
                do ktau = 2 , kmax
                   if ( abs( tech( ktau , iaid ) ) .lt. 0.1 ) then
                      tech( ktau , iaid ) = -99.9
                      gech( ktau , iaid ) = -99.9
                      vmax( ktau , iaid ) = -99.0
                   endif
                enddo
             endif
          endif
          
cxxx  Now read the next line of data.  If the dtg is different than
cxxx  the previous line, it's time to compute the errors.  Otherwise,
cxxx  go back and process it.
          domore = .false.
cajs      read ( 7 , '( a80 )' , end = 175 ) ia
cajs      domore = .true.
cajs      read ( ia , '( i2 , a4 , a8 )' ) iaid , itech , idtg
          call readARecord( 7, aidRcd, istat )
          if( istat .ne. 1 ) goto 175
          domore = .true.
          iaid = aidRcd%aRecord(1)%technum
          itech = aidRcd%aRecord(1)%tech
          idtg = aidRcd%aRecord(1)%DTG(3:10)
          if ( idtg .ne. ndtg ) then
             do ii=1,aidRcd%numrcrds
                backspace 7
             enddo
             goto 175
          endif
          ndtg = idtg
        goto 200

cxxx    We have now read all the forecasts for 1 DTG.

 175    continue

ckpd    Did we find any aids for which we should develop error
ckpd    statistics in this DTG?

        if ( nseen .gt. 0 ) then
           idtg = ndtg
           
ckpd DEBUG          write ( 8 , '( '' DTG = '' , a8 )' ) ndtg

cxxx      Now insert the intial position into the first word of
cxxx      the array of each forecast (tech and gech).  Thus, the data
cxxx      is stored as follows:

cxxx        tech(ktau,jtech), or gech(ktau,jtech),

cxxx          ktau = 1 to kmax  where

cxxx            1 = tau 00, values from CARQ, WRNG, or best track
cxxx            2 = tau 12, values from objective forecast aid 1st loc.
cxxx            3 = tau 24, values from objective forecast aid 2nd loc.
cxxx            4 = tau 36, values from objective forecast aid 3rd loc.
cxxx            5 = tau 48, values from objective forecast aid 4th loc.
cxxx            6 = tau 72, values from objective forecast aid 5th loc.
cxxx            7 = tau 96, values from objective forecast aid 6th loc.
cxxx            8 = tau 120, values from objective forecast aid 7th loc.

cxxx          jtech = 1 to 50 , one for each objective aid
cxxx                            forecast technique.

cxxx      Note that we use the CARQ position as the initial position
cxxx      (tau 00). If it wasn't found, use the WRNG.

           do icw = 1 , 2
              if ( validpos( poslat( 1 , icw ) ,
     &             poslng( 1 , icw )   ) ) then

ckpd DEBUG      if (icw .eq. 1) then
ckpd DEBUG         write( 8 , '('' Going with CARQ tau 00 of '',2f7.1)')
ckpd DEBUG     &         poslat( 1 , icw ) , poslng( 1 , icw )
ckpd DEBUG      else
ckpd DEBUG         write( 8 , '('' Going with WRNG tau 00 of '',2f7.1)')
ckpd DEBUG     &          poslat( 1 , icw ) , poslng( 1 , icw )
ckpd DEBUG       endif

                 do jtech = 1 , nt
                    if ( ic( jtech ) .gt. 0 ) then
                       tech( 1 , jtech ) = poslat( 1 , icw )
                       gech( 1 , jtech ) = poslng( 1 , icw )
                    endif
                 enddo
                 go to 250
              endif
           enddo

cxxx      If both the CARQ and WRNG positions weren't found, use the
cxxx      corresponding best track position.

           call dtgdif( fstdy , idtg , kdif )
           kdif = kdif + 1
           if ( ( kdif .ge. 0 ) .and. ( kdif .le. idif ) ) then

ckpd FIXME  Why nt - 2?  Document or revise.  This should break
ckpd FIXME  something, if it means what it seems to mean.  There are in
ckpd FIXME  fact objective forecast aids numbered 48 and 49 in
ckpd FIXME  techlist.dat.

              do jtech = 1 , nt - 2
                 if ( ic( jtech ) .gt. 0 ) then
                    tech( 1 , jtech ) = hlat( kdif )
                    gech( 1 , jtech ) = hlng( kdif )
                 endif
              enddo

ckpd DEBUG         write( 8 , '('' Going with BSTT tau 00 of '',2f7.1)')
ckpd DEBUG     &        hlat( kdif ) , hlng( kdif )

              goto 250
           endif
           write( * ,
     &          '('' reada() in ddeck(): ''
     &          '' Found no starting position for DTG '' , a8 ,
     &          /,'' CARQ was  '', 2f7.1,
     &          /,'' WRNG was  '', 2f7.1,
     &          /,'' and best track hour (+1) index '' , i10 ,
     &          /,'' was outside limits of '',i10,'' and '',i10)' )
     &          idtg,
     &          poslat(1,1) , poslng(1,1),
     &          poslat(1,2) , poslng(1,2),
     &          kdif,0,idif
        endif
        if (domore) then
           goto 210
        else
           
ckpd  iflag =  1, read a DTG, more to read
ckpd  iflag =  0, read a DTG, no more to read
cxxx  iflag = -1, error
           
           iflag = 0
           return
        endif
 250  continue
      if (domore) then
         iflag = 1
      else
         iflag = 0
      endif
      return
 125  continue
      iflag = -1
      return
      end

c-----------------------------------------------------------------------
      subroutine readb( ilu , ierr )
c-----------------------------------------------------------------------

cx  sampson, nrl Nov 98   added cent to read

      include 'ddeckparms.inc'
      INCLUDE 'bestc.inc'
      INCLUDE 'bstchr.inc'

      real             x( 200 )
      real             vmax
      integer          i
      integer          iwind
      integer          ios
      character*11     fnam
      character*1      l
      character*1      g
      character*2      cent
      logical*1        exst

cxxx  This routine reads and interpolates the bstrk lat,lng to hourly
cxxx  positions.

cxxx    blat,blng  - 6-hourly lat/long
cxxx    hlat,hlng  - 1-hourly lat/long
cxxx    fstdy      - first dtg of best track
cxxx    numpos     - number of 6 hourly best track points
cxxx    idif       - difference in hrs between 1st and last dtg's
cxxx    ierr       - 0 = normal return
cxxx                 0 <> abnormal return

cxxx  Reading bstrk file

      numpos = 0
 150  continue
         numpos = numpos + 1
cajs     read( ilu, '(2x, a8, f4.1, a1, f4.1, a1, f4.0)', end = 200 )
cajs &        dtgb( numpos ), blat( numpos ), l, blng( numpos ), g, vmax
         call readBT( ilu, cent, dtgb(numpos), blat(numpos), l, 
     &        blng(numpos), g, iwind, ios )
         if( ios .ne. 0 ) goto 200
         vmax = iwind
         if ( l .eq. 'S' ) blat( numpos ) = -blat( numpos )
         if ( g .eq. 'E' ) blng( numpos ) = 360.0 - blng( numpos )
      go to 150
 200  continue
      
cxxx  Interpolating bstrk file
      
ckpd  Fill in the time array x(), checking for out of order times along
ckpd  the way.
      
      numpos = numpos - 1
      if ( numpos .gt. 1 ) then
         fstdy = dtgb( 1 )
         do 300 i = 1 , numpos
            call dtgdif( fstdy , dtgb( i ) , idif )
            if ( idif .lt. 0 ) then
               write( * ,
     &        '(  '' Subroutine readb() in program ddeck() found the'' ,
     &        / , '' best track file to be not in sorted order.'' ,
     &        / , '' Please correct the problem and try again.'' )' )
               ierr = -1
               return
            endif
            x( i ) = float( idif )
 300     continue
         call hour( x , blat , hlat , numpos )
         call hour( x , blng , hlng , numpos )
         idif = idif + 1
         
ckpd    Found the next two lines out of order, reversed them.
ckpd    1992.03.19.
         
         ierr = 0
         return
      else
         write( *  ,
     &        '(  '' Subroutine readb() in program ddeck() found no'' ,
     &        / , '' best track positions when attempting to read'' ,
     &        / , '' the best track file. '' ,
     &        '' Please correct the problem and try again.'' )' )
         ierr = -1
         return
      endif
      end

c ---------------------------------------------------------------------
      function validpos(lat,lng)
c ---------------------------------------------------------------------

ckpd  Purpose:

ckpd    Function validpos() captures the concept of what a valid (versus
ckpd    a "no valid data" placeholder) latitude and longitude pair looks
ckpd    like in the objective aids data files, into a single software
ckpd    location for the MS-DOS ATCF 2.7x software.

ckpd    It returns a one byte logical value ".true." for a valid
ckpd    position, and ".false." for a "no valid data" lat/long datum.

ckpd  Author:

ckpd    Kent Paul Dolan, LCDR, USNOAA Corps, Retired
ckpd    Computer Science Corporation contractor to
ckpd    Fleet Numerical Oceanography Center
ckpd    Monterey, California, USA,  93940-5005
ckpd    (408) 656-4363

ckpd  Maintenance History:

ckpd  1993.03.23: First written.

c ----------------------------------------------------------------------

      real             lat

      real             lng

      logical*1        validpos

ckpd FIXME  ATCF should have exactly one "no valid data" format and
ckpd FIXME  value pair for a ( latitude , longitude ) paired datum, in
ckpd FIXME  the stored data display integer format, ( "-999" , "9999" ),
ckpd FIXME  representing respectively ( signed, unsigned) integer counts
ckpd FIXME  of tenths of degrees, or in the internal format, ( -99.9 ,
ckpd FIXME  999.9 ), representing floating point numbers of degrees.

ckpd FIXME  Instead, there are (at least) four; in display -- internal
ckpd FIXME  forms respectively:

ckpd FIXME     display / storage              internal / computational
ckpd FIXME    -------------------             ------------------------

ckpd FIXME    ( "    " , "    " )      <-->      (  00.0 , 000.0 )

ckpd FIXME    ( "   0" , "   0" )      <-->      (  00.0 , 000.0 )

ckpd FIXME    ( "-999" , "-999" )      <-->      ( -99.9 , -99.9 )

ckpd FIXME    ( "-999" , "9999" )      <-->      ( -99.9 , 999.9 )

ckpd FIXME  This is a raging software maintenance disaster, to say the
ckpd FIXME  least, because:

ckpd FIXME    first, since no standard for this data construct exists of
ckpd FIXME    which the software authors or maintainers were aware, each
ckpd FIXME    software author or maintainer has tested only for the
ckpd FIXME    case(s) of which s/he was aware, and the tests are
ckpd FIXME    different and incompatible throughout ATCF, and

ckpd FIXME    second, some routines (e.g., the fnwc library routine
ckpd FIXME    hour()) receive the latitudes and longitudes in separate
ckpd FIXME    calls, and, for instance, the longitude in the third
ckpd FIXME    option is completely valid, and both the latitude and
ckpd FIXME    longitude in the first two computational options are in
ckpd FIXME    the domain of real ( latitude , longitude ) pairs (though
ckpd FIXME    in terms of tropical cyclones probably both impossible or
ckpd FIXME    vanishingly unlikely), and only together do they make a
ckpd FIXME    "no valid data" token, prohibiting implementation of
ckpd FIXME    checks for invalid data in the called routine.

ckpd FIXME  The end result in the case of the ddeck() suite of software
ckpd FIXME  is that invalid data went unrecognized by the "no valid
ckpd FIXME  data" checking code, was passed to the interpolation routine
ckpd FIXME  as if it were valid, and and resulted in the completely
ckpd FIXME  bogus finding that objective aids were making forecast
ckpd FIXME  errors compared to the climatological aid CLIP of a third
ckpd FIXME  the circumferance of the planet.

ckpd FIXME  Thus, the maintainer chose to change all of the ddeck()
ckpd FIXME  tests for valid positions versus "no valid data" positions
ckpd FIXME  to use this little routine instead.

ckpd FIXME  This is because the archival three tau format storm data
ckpd FIXME  from before the three tau to five tau upgrade (ATCF 2.6 ->
ckpd FIXME  ATCF 2.7x) was improperly reformatted to five tau format
ckpd FIXME  with zeros filling the missing position data fields, to five
ckpd FIXME  tau format, instead of -99.9 and 999.9 as the "no valid
ckpd FIXME  data" values.

ckpd FIXME  This broke every test for valid data that used the "is
ckpd FIXME  latitude of datum < -90.0" construct in ATCF.

ckpd FIXME  Naturally letting this use of zeros as lat long "no valid
ckpd FIXME  data" entries breaks other potential uses for that value
ckpd FIXME  pair.  An Atlantic storm that actually passes through the
ckpd FIXME  Greenwich meridian at the equator is supposedly physically
ckpd FIXME  impossible (though nature is full of surprises), so probably
ckpd FIXME  best track data couldn't land there, though forecast data
ckpd FIXME  from a misbehaving model might well do so.

ckpd FIXME  However, there is other data with which ATCF is concerned (a
ckpd FIXME  ship location when it provides a meteorological observation,
ckpd FIXME  perhaps) that are examples of a now or future valid ( 00.0 ,
ckpd FIXME  00.0 ) ATCF position datum.

ckpd FIXME  When time is available, reformat the archival data to use
ckpd FIXME  the correct lat-long "no valid data" tokens, find and change
ckpd FIXME  all instances in the ATCF software that look for the several
ckpd FIXME  different "no valid data" tokens to look for only the proper
ckpd FIXME  ones by calling this routine, coordinate with the mainframe
ckpd FIXME  software maintainers to make sure only the proper ones are
ckpd FIXME  produced there, and pull the extra garbage out of this
ckpd FIXME  routine.

ckpd FIXME  To make a neater solution than patching the reality of the
ckpd FIXME  poorly formatted archival data into every routine where
ckpd FIXME  checks for valid position information exist, make this
ckpd FIXME  little software "object" that captures the test for the
ckpd FIXME  existing but errant cases in a single place, so that when
ckpd FIXME  the data is cleaned up to use only the correct fourth case,
ckpd FIXME  an easy one place fix can be done here, and in the meantime,
ckpd FIXME  the checks rife in ATCF can be changed to use this routine
ckpd FIXME  to make the whole software suite more robust about this one
ckpd FIXME  issue.

ckpd  I'll bet you thought you'd never find the code in here.

ckpd  Do a one place test for a valid lat/lng pair:

      if ( ( lat .ge. -90.0) .and.
     &     ( ( lat .ne. 0.0 ) .or. ( lng .ne. 0.0 ) ) ) then

        validpos = .true.

      else

        validpos = .false.

      endif

      return

      end

c ---------------------------------------------------------------------
      subroutine xtcatc( itech , itau , err2 , err3 )
c ---------------------------------------------------------------------

cxxx  Interpolate CLIP to hourly positions / calculate XTC and ATC
cxxx  errors.

ckpd  To avoid maintaining copies of the same code in multiple places,
ckpd  do common block declarations and declarations of the variables
ckpd  they contain from include files named after the common blocks.

      include 'ddeckparms.inc'

       INCLUDE 'bestc.inc'
       INCLUDE 'bstchr.inc'

ckpd  By a blunder, this common statement was omitted from the original
ckpd  form of this subprogram.  As a result, variables kmax and kdel,
ckpd  used in the error computation part of this routine, were never
ckpd  initialized, leaving them either zero valued or garbage valued,
ckpd  depending on whether the compiler sets the code up to clear the
ckpd  data space before beginning, or not.  This problem was discovered
ckpd  1993.03.19, after taking the trouble to completely reformat this
ckpd  code for maintainability, including declaring all variables and
ckpd  turning on the compiler warning for undeclared variables. Another
ckpd  victory for software engineering over software hacking.  The
ckpd  program has been in production use with the above error since at
ckpd  least 1991.11.10, making any calculations of error with respect
ckpd  to CLIP unreliable over that timespan.

      INCLUDE 'fcstc.inc'

      INCLUDE 'techc.inc'
      INCLUDE 'posit.inc'
      INCLUDE 'mtechs.inc'

ckpd                   Function validpos() captures the concept of what
ckpd                   a valid (versus a "no value") latitude and
ckpd                   longitude pair looks like in the objective aids
ckpd                   data files.  It returns ".true." for a valid
ckpd                   position, and ".false." for a "no value" lat/long
ckpd                   datum.

      logical*1        validpos

ckpd                   Variable lcopynm is a  integer store,
ckpd                   loop limit, and index that holds the y() array
ckpd                   index number of the hour value corresponding to
ckpd                   the last valid position enountered when copying
ckpd                   valid values to the hour() interpolation input
ckpd                   position arrays clat() and clng().  It is used to
ckpd                   control clearing of subsequent array locations to
ckpd                   "no valid data" values.

      integer          lcopynm

ckpd                   Variable icopynm is a  integer counter
ckpd                   and index that counts the data values copied from
ckpd                   the best track or CLIP forecast positions to the
ckpd                   clat() and clng() arrays for feeding to
ckpd                   interpolation routine hour().  It is used to
ckpd                   accomodate the fact that data values may be
ckpd                   missing, with "no valid data" tokens in their
ckpd                   place, and we certainly don't want hour()
ckpd                   interpolating the rest of the valid data smoothly
ckpd                   through these tokens!  The legal values for
ckpd                   icopynm are zero through ten, the largest number
ckpd                   of positions that will be copied in this routine
ckpd                   for a single hour() call.

      integer          icopynm

ckpd                   Variable nodata is a loop counter and array index
ckpd                   used to fill unused positions of the x() array
ckpd                   before the hour() call, and the hhlat() and
ckpd                   hhlng() arrays after the hour() call, with
ckpd                   invalid data markers of appropriate sorts.

      integer          nodata

ckpd                   Variable itech is a  integer passed as an
ckpd                   input parameter to this routine with the
ckpd                   semantics of an objective aid technique number,
ckpd                   from 1 to naids.

      integer          itech

ckpd                   Variable itau is a  integer passed as an
ckpd                   input parameter to this routine  with the
ckpd                   semantics of a forecast synoptic interval index
ckpd                   from 1 to kmax for the standard forecast synoptic
ckpd                   times.

      integer          itau

ckpd                   Variable err2 is a  real passed as an
ckpd                   input parameter to this routine with the
ckpd                   semantics of an error value. (It is actually, two
ckpd                   calling routines above, an element of common
ckpd                   fcstc's array error() corresponding to error type
ckpd                   2, XTC error.)

      real             err2

ckpd                   Variable err3 is a  real passed as an
ckpd                   input parameter to this routine with the
ckpd                   semantics of an error value. (It is actually, two
ckpd                   calling routines above, an element of common
ckpd                   fcstc's array error() corresponding to error type
ckpd                   3, ATC error.)

      real             err3

ckpd  Need 4 byte precision for third parameter of dtgdif().

      integer          idiff

ckpd                   Variable cc is a  real, with legal
ckpd                   values from minus two pi to two pi, probably, and
ckpd                   holds error distance values expressed as radian
ckpd                   offsets along a great circle of the earth.  It is
ckpd                   used in trig calculations needed for error
ckpd                   statistics.

      real             cc

ckpd                   Variable dir1 is a  real used to pass a
ckpd                   control value to dirdst(), and to return the
ckpd                   direction between the two passed lat/longs. Its
ckpd                   legal values are the decimal directions in
ckpd                   degrees and tenths.  After some processing, the
ckpd                   final legal value is between 0.1 and 360.0, for
ckpd                   valid directions, and 0.0, for a "no valid
ckpd                   direction" return value.

      real             dir1

ckpd                   Variable dir has the same type, legal values, and
ckpd                   use as variable dir1.  They both exist because we
ckpd                   are frequently dealing with 1) the direction of
ckpd                   the best track storm motion vector, 2) the
ckpd                   direction of the forecast storm motion vector,
ckpd                   and 3) the direction of the error vector, and
ckpd                   need more than one place to store the values.

      real             dir

ckpd                   Variable dis is a  real, with legal
ckpd                   values in signed nautical miles less than the
ckpd                   circumferance of the earth, and is used to store
ckpd                   the returned value of dirdst() calls, the
ckpd                   distance between two lat/long positions.

      real             dis

ckpd                   Variable dis1 is pair with variable dir1, and has
ckpd                   the same characteristics and use as variable dis.

      real             dis1

ckpd                   Variable y is a  real array of 10
ckpd                   elements used to store the standard interpolation
ckpd                   times for copying to array x iff they are
ckpd                   actually used in an interpolation pass because
ckpd                   there is valid data corresponding to those times.

      real             y( 12 )

ckpd                   Variable x is a four btye real array of 200
ckpd                   elements used to store the offset times for which
ckpd                   interpolations should be done by routine hour(),
ckpd                   to which it is passed.

      real             x( 200 )

ckpd                   Variable clat is a  real array of 200
ckpd                   elements used to store the forecast position
ckpd                   latitudes as aid CLIP forecast them.

      real             clat( 200 )

ckpd                   Variable clng is a  real array of 200
ckpd                   elements used to store the forecast position
ckpd                   latitudes as aid CLIP forecast them.

      real             clng( 200 )

ckpd                   Variable hhlat is a  real array of 1201
ckpd                   elements used to return the hourly interpolated
ckpd                   positions for the clat synoptic hour positions
ckpd                   from fnwc library routine hour().

      real             hhlat( 1201 )

ckpd                   Variable hhlng is a  real array of 1201
ckpd                   elements used to return the hourly interpolated
ckpd                   positions for the clng synoptic hour positions
ckpd                   from fnwc library routine hour().

      real             hhlng( 1201 )

ckpd                   Variable indx is a  integer that is used
ckpd                   as an index of the best track position arrays
ckpd                   corresponding to the forecast synoptic tau of the
ckpd                   currently considered forecasts.  Offsets to indx
ckpd                   are used to pull data into arrays prior to
ckpd                   calling the interpolating routine hour().

      integer          indx

ckpd                   Variable indxhr is a  integer that is
ckpd                   used as an array index into the hourly
ckpd                   interpolated position arrays while passing data
ckpd                   to fnwc library routine dirdst().

      integer          indxhr

ckpd                   Variable pi is a  real, holds the math
ckpd                   constant pi, is used for angle to radian
ckpd                   calculations before using the FORTRAN intrinsic
ckpd                   trig routines, and the data statement below that
ckpd                   gives it a value has a ridiculous precision for a
ckpd                   data type that only holds about six decimal
ckpd                   digits of precision, just so you know that I
ckpd                   know.

      real             pi

ckpd  The strange looking set of numbers here are the hours to which the
ckpd  latitude and longitude data loaded into the clat and clng files
ckpd  correspond, relative to the first of them.  The current time of
ckpd  the forecast is the 24.0 hour entry, and the 48.0, 72.0, and 96.0
ckpd  entries are the forecast times for position forecasts +24, +48,
ckpd  and +72 hours from then, respectively. The earlier entries are the
ckpd  best track data points, in order backwards from the 24.0 entry the
ckpd  -6, -12, -18, and -24 hour positions correspond to the 18.0, 12.0,
ckpd  6.0, and 0.0 entries here, respectively.  These time offsets are
ckpd  used by the fnwc library routine hour(), in its interpolation of
ckpd  positions at all the intermediate even hours for this routine.

ckpd      data x / 0.0 , 6.0 , 12.0 , 18.0 , 24.0 , 48.0 , 72.0 , 96.0 ,
ckpd     &         192*0.0 /

ckpd  Sigh again.  No one bothered to update the code here when the
ckpd  three tau to five tau data format change happened, and the wrong
ckpd  stuff is being copied out of tech() and gech() arrays to be passed
ckpd  to hour().  Doing the job "right" in hour is not possible, because
ckpd  only one of the lat, lng data sets is interpolated at a time, so
ckpd  hour() can't check that the lat and lng are simultaneously zero,
ckpd  one of the now three possible "no valid data" lat/lng entries.
ckpd  Guess I get to make this a lot more complex, instead.


ckpd  Now, as opposed to above for array x(), the data declaration lines
ckpd  for array y() represent in turn:

ckpd    first, the best track positions in minus time offsets from the
ckpd    forecast's synoptic time: -24 hours, -18 hours, -12 hours, and
ckpd    -06 hours, since best track positions are captured every six
ckpd    hours;

ckpd    second, the (best track) position at the forecast's synoptic
ckpd    time: 00 hours;

ckpd    third, the five forecast taus in plus time: +12 hours, +24
ckpd    hours, +36 hours, +48 hours, and +72 hours after the forecast's
ckpd    synoptic time (notice that +60 hours is not a standard forecast
ckpd    time, breaking the even 12 hour intervals among the other
ckpd    forecast times, and causing lots of extra coding throughout ATCF
ckpd    to make up for the irregularity);

ckpd  with all times shifted by 24 hours to make the first one 00.0 for
ckpd  the sake of the hour() interpolation routine.

      data y / 00.0 , 06.0 , 12.0 , 18.0 ,
     &         24.0 ,
     &         36.0 , 48.0 , 60.0 , 72.0 , 96.0, 120, 144 /

      data pi / 3.1415926535898 /

cxxx  Return if 24 hours of best track previous to forecast position
cxxx  unavailable.

      call dtgdif( fstdy , idtg , idiff )

      if ( idiff .lt. 24 ) return

cxxx  Interpolate CLIP to hourly positions if this is the first
cxxx  technique of this forecast DTG.

      if ( iclip .ne. 1 ) then

        iclip = 1

cxxx  Load CLIP positions + 24 hours of previous best track positions to
cxxx  arrays.

ckpd FIXME  Notice that this method of matching up forecast times to
ckpd FIXME  best track position array values is not robust in the face
ckpd FIXME  of a missing best track position for any included hour, and
ckpd FIXME  is pure garbage in the case of a missing forecast position.
ckpd FIXME  Is it made to work by putting in dummy values elsewhere, and
ckpd FIXME  then respecting them in hour()? No, it doesn't work at all!

ckpd    We have copied no values yet.

        icopynm = 0

ckpd    We want to index the best track position array in synoptic
ckpd    periods, not hours, and the array index is one-based.

        indx    = idiff / 6 + 1

ckpd    The following ten if ... then blocks all perform about the same
ckpd    function, the first five copy from the best track data, where
ckpd    valid, the last five copy from the CLIP forecast position array,
ckpd    where valid.  One set of comments will suffice for all.


ckpd    Check that the source of the copy has a valid position in it;
ckpd    if so ...

        if ( validpos( blat( indx - 4 ) , blng( indx - 4 ) ) ) then

ckpd      ... bump the copy counter to point to the next available
ckpd      clat(), clng(), and x() array locations ...

          icopynm = icopynm + 1

ckpd      ... copy from the source latitude component of the position
ckpd      to the clat() array ...

          clat( icopynm ) = blat( indx - 4 )

ckpd      ... copy from the source longitude component of the position
ckpd      to the clng() array ...

          clng( icopynm ) = blng( indx - 4 )

ckpd      ... fill in the time array x() with the corresponding time for
ckpd      the copied position in the source array (laid out in comments,
ckpd      above) ...

          x( icopynm ) = y( 1 )

ckpd      ... and capture, in ascending order, the y() array index of the
ckpd      hour value corresponding to the last of these if ... then
ckpd      statements with which we find a valid position associated.

          lcopynm = 1

        endif

        if ( validpos( blat( indx - 3 ) , blng( indx - 3 ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = blat( indx - 3 )

          clng( icopynm ) = blng( indx - 3 )

          x( icopynm ) = y( 2 )

          lcopynm = 2

        endif

        if ( validpos( blat( indx - 2 ) , blng( indx - 2 ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = blat( indx - 2 )

          clng( icopynm ) = blng( indx - 2 )

          x( icopynm ) = y( 3 )

          lcopynm = 3

        endif

        if ( validpos( blat( indx - 1 ) , blng( indx - 1 ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = blat( indx - 1 )

          clng( icopynm ) = blng( indx - 1 )

          x( icopynm ) = y( 4 )

          lcopynm = 4

        endif

        if ( validpos( blat( indx     ) , blng( indx     ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = blat( indx     )

          clng( icopynm ) = blng( indx     )

          x( icopynm ) = y( 5 )

          lcopynm = 5

        endif

        if ( validpos( tech( 2 , nclip ) , gech( 2 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 2 , nclip )

          clng( icopynm ) = gech( 2 , nclip )

          x( icopynm ) = y( 6 )

          lcopynm =  6

        endif

        if ( validpos( tech( 3 , nclip ) , gech( 3 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 3 , nclip )

          clng( icopynm ) = gech( 3 , nclip )

          x( icopynm ) = y( 7 )

          lcopynm = 7

        endif

        if ( validpos( tech( 4 , nclip ) , gech( 4 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 4 , nclip )

          clng( icopynm ) = gech( 4 , nclip )

          x( icopynm ) = y( 8 )

          lcopynm = 8

        endif

        if ( validpos( tech( 5 , nclip ) , gech( 5 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 5 , nclip )

          clng( icopynm ) = gech( 5 , nclip )

          x( icopynm ) = y( 9 )

          lcopynm = 9

        endif

        if ( validpos( tech( 6 , nclip ) , gech( 6 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 6 , nclip )

          clng( icopynm ) = gech( 6 , nclip )

          x( icopynm ) = y( 10 )

          lcopynm = 10

        endif

        if ( validpos( tech( 7 , nclip ) , gech( 7 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 7 , nclip )

          clng( icopynm ) = gech( 7 , nclip )

          x( icopynm ) = y( 11 )

          lcopynm = 11

        endif

        if ( validpos( tech( 8 , nclip ) , gech( 8 , nclip ) ) ) then

          icopynm = icopynm + 1

          clat( icopynm ) = tech( 8 , nclip )

          clng( icopynm ) = gech( 8 , nclip )

          x( icopynm ) = y( 12 )

          lcopynm = 12

        endif

ckpd    All available valid positions are copied to slots; zero out the
ckpd    rest of the hour array for no perceptable reason except that the
ckpd    original code given me to maintain had set it that way; in case
ckpd    someone maintains hour() to make it expect zero times in the
ckpd    unused slots.

        do 100 nodata = ( icopynm + 1 ) , 200

          x( nodata ) = 0.0

  100   continue

cxxx    Interpolate.

        call hour( x , clat , hhlat , icopynm )

        call hour( x , clng , hhlng , icopynm )

        do 200 nodata = ( ifix( y( lcopynm ) + 2 ) ) , 1201

          hhlat( nodata ) = -99.9

          hhlng( nodata ) = 999.9

  200   continue

ckpd DEBUG        write( 8 ,'( / , '' index, hhlat, and hlong triplets:'' )' )

ckpd DEBUG        write( 8 , '( 1x , 4(i5,2f7.1) )' )
ckpd DEBUG     &    ( nodata , hhlat( nodata ) , hhlng( nodata ),
ckpd DEBUG     &    nodata = 1 , ( ifix( y( lcopynm ) ) + 1 ) )

ckpd  It's been a long time; this endif is the other end of the check
ckpd  that the interpolation has been run once for this DTG to fill in
ckpd  the hhlat() and hhlng() arrays for the rest of the work done
ckpd  hereafter in this routine.

      endif

cxxx  Compute XTC (error2) , ATC (error3).

      dir = 1.0

      dir1 = 1.0

ckpd  The magic number 25 here is the 24 hours of interpolated best
ckpd  track position array hours for the four previous best track
ckpd  positions used to initialize the clat() and clng() arrays above,
ckpd  plus one hour to put us on the currently being considered forecast
ckpd  synoptic time.  Then kdel and itau step us down to the plus time
ckpd  forecast under consideration.

cajs      indxhr = 25 + ( ( itau - 1 ) * kdel )

cajs      if ( itau .eq. kmax ) indxhr = indxhr + kdel
      indxhr = 25 + ktauarr( itau )

ckpd DEBUG      write( 8 ,
ckpd DEBUG     &  '( /, '' iaid,aid,itau,indxhr,kdel,kmax:  '' ,
ckpd DEBUG     &  i8, 1x, a4, 1x, 4i8 )'
ckpd DEBUG     &  ) itech , mobj(itech) , itau , indxhr , kdel , kmax

ckpd  Guaranteeing a valid position is much more complex than this, due
ckpd  to poorly followed specification of what a "no valid data" entry
ckpd  for a latitude, longitude pair should be encoded as in MS-DOS
ckpd  ATCF; hide all the grunge in a function, validpos().

ckpd FIXME CONTEXT      if( tech( itau , 4 ) .eq. -99.9 ) return

ckpd FIXME  The "4" above was probably never right, but in particular,
ckpd FIXME  it is not the fourth position in the two arrays, but the
ckpd FIXME  "itech"th position that is being used in the succeeding
ckpd FIXME  code, and surely that should be the one being checked here.
ckpd FIXME  In any case, position 4 is no longer the +72 hour position,
ckpd FIXME  it is the +36 hour position. Try this fix, substituting
ckpd FIXME  "itech" for "4" in the valid position check, and see if it
ckpd FIXME  breaks anything.

      if ( .not. validpos( tech( itau , itech ) ,
     &                     gech( itau , itech )   )
     &   ) then

ckpd DEBUG        write( 8 , '( / , '' Bouncing, because itau,itech,'',
ckpd DEBUG     &    ''mobj(itech),tech(itau,itech),gech(itau,itech) are:'', / ,
ckpd DEBUG     &    2i8,1x,a4,1x,2f7.1)' )
ckpd DEBUG     &    itau,itech,mobj(itech),tech(itau,itech),gech(itau,itech)

        return

      endif

      call dirdst( hhlat( indxhr - 1 ) , hhlng( indxhr - 1 ) ,
     &             hhlat( indxhr     ) , hhlng( indxhr     ) ,
     &             dir                 , dis                   )

ckpd DEBUG      write( 8 ,
ckpd DEBUG     &  '( '' xtcatc: '' , i8 , 6f7.1 )' )
ckpd DEBUG     &  indxhr,
ckpd DEBUG     &  hhlat(indxhr-1),hhlng(indxhr-1),
ckpd DEBUG     &  hhlat(indxhr),hhlng(indxhr),
ckpd DEBUG     &  dir, dis

      call dirdst( hhlat( indxhr       ) , hhlng( indxhr      ) ,
     &             tech(  itau , itech ) , gech( itau , itech ) ,
     &             dir1                  , dis1                   )

ckpd DEBUG      write( 8 ,
ckpd DEBUG     &  '( '' xtcatc: '' , i8 , 6f7.1 )' )
ckpd DEBUG     &  indxhr,
ckpd DEBUG     &  hhlat(indxhr),hhlng(indxhr),
ckpd DEBUG     &  tech(itau,itech),gech(itau,itech),
ckpd DEBUG     &  dir1, dis1

ckpd FIXED  Surely this isn't what was intended!

ckpd      dir = amod( dir1 - dir + 359.0 , 360.0 ) + 1.0

ckpd FIXME  It is almost certain that the projection for computing the
ckpd FIXME  XTC and ATC errors is being done to the wrong vector, just
ckpd FIXME  like the error in the XTE and ATE calculations, but it will
ckpd FIXME  take a lot of pencil and paper noodling to prove that and
ckpd FIXME  to figure out how to make it right.

ckpd  Make dir the angle _from_ the direction of the interpolated last
ckpd  hour of the CLIP forecast _to_ the error vector from the same-tau
ckpd  CLIP forecast position to the current aid's forecast position.

      dir = amod( dir1 - dir + 359.9 , 360.0 ) + 0.1

      dis = 1.0

      if ( ( dir .gt. 180.0 ) .and. ( dir .lt. 360.0 ) ) then

        dis = -1.0

        dir = 360.0 - dir

      endif

ckpd  Convert the error distance to radians along a great circle
ckpd  following the error vector direction.

      cc   = ( dis1 / 60.0 ) * ( pi / 180.0 )

ckpd  The sin(cc) here pulls the problem down from a problem on the
ckpd  spherical cap defined by radial distance cc along the sphere, in
ckpd  spherical trig, to a more tractible problem on the disk defined by
ckpd  a plane through the base of that same spherical cap, now in plane
ckpd  trig.

      err2 = sin( cc ) * sin( dir * ( pi / 180.0 ) )

      err2 = sqrt( 1.0 - ( err2 * err2 ) )

cx  check for possible zero in denom  ... bs 1/8/96
      if ( err2 .eq. 0.0 ) err2 = 0.0000001

      err3 = cos( cc ) / err2

cx  concurrent problem with undefined in acos ... bs 1/8/96
      err2 = min ( 1.0, err2)
      err2 = max (-1.0, err2)

      err2 = ( acos( err2 ) * 60.0 ) * ( 180.0 / pi ) * dis

cx  concurrent problem with undefined in acos ... bs 1/8/96
      err2 = min ( 1.0, err2)
      err2 = max (-1.0, err2)

      err3 = ( acos( err3 ) * 60.0 ) * ( 180.0 / pi )

      if ( dir .gt. 90.0 ) err3 = -err3

      return

      end
