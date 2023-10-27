c----------------------------------------------------------------------
      subroutine slop( y , x , t , m )
c----------------------------------------------------------------------

ctt   This routine 'slop' calculates the slopes t of y over x axis at
ctt   each of the m points.  Reference: Akima 1970, Journal of the
ctt   Association for Computing Machinery, 589-602.

ckpd      dimension y(200),x(200),t(200)
ckpd      dimension work(204)

ckpd                   Input four byte real two hundred element array
ckpd                   y() holds the latitude or longitude values
ckpd                   between which slopes with respect to time are to
ckpd                   be computed.

      real*4           y( 200 )

ckpd                   Input four byte real two hundred element array
ckpd                   x() holds the times (in steps of at least unity
ckpd                   between entries) with respect to which slopes
ckpd                   between latitude or longitude values are to be
ckpd                   computed.

      real*4           x( 200 )

ckpd                   Output four byte real two hundred element array
ckpd                   t() holds computed slopes of the latitude or
ckpd                   longitude values with respect to time.

      real*4           t( 200 )

ckpd                   Working four byte real two hundred and four
ckpd                   element array work() holds intermediate
ckpd                   unsmoothed entry to entry slopes used to compute
ckpd                   the final smoothed slopes.  The extra four
ckpd                   elements are used to insert parabolic
ckpd                   approximations at the extremes of the data before
ckpd                   doing the cubic slope approximations among the
ckpd                   inputs.

      real*4           work( 204 )

ckpd                   Input two byte integer m is the number of valid
ckpd                   entries in the input x() and y() arrays.

      integer*2        m

ckpd                   Working loop counter and array index i is used to
ckpd                   walk the computations through the input, working,
ckpd                   and output arrays in a systematic manner.

      integer*2        i

ckpd                   Working four byte real a holds the second
ckpd                   difference of the data for two intervals after
ckpd                   the current output entry.

      real*4           a

ckpd                   Working four byte real b holds the second
ckpd                   difference of the data for two intervals before
ckpd                   the current output entry.

      real*4           b


ckpd  Fill the working array positions corresponding to the inputs
ckpd  (offset by two to allow room for special case parabolic "seed"
ckpd  approximations before and after the data) with first difference
ckpd  delta y over delta x values.


c     call prctrc('slop',.true.)

      do 100 i = 2 , m

       work( i + 1 ) =   ( y( i ) - y( i - 1 ) )
     &                 / ( x( i ) - x( i - 1 ) )

100   continue

ckpd  Special case parabolic approximations before and after the live
ckpd  data, to make the more complex cubic interpolation special case
ckpd  free.

      work( 1 )     = 3.0 * work( 3 )     - 2.0 * work( 4 )

      work( 2 )     = 2.0 * work( 3 )     -       work( 4 )

      work( m + 2 ) = 2.0 * work( m + 1 ) -       work( m )

      work( m + 3 ) = 3.0 * work( m + 1 ) - 2.0 * work( m )

ckpd FIXED  Oops!  Notice what is going on here:
ckpd FIXED
ckpd FIXED  1) we take the differences of potentially large numbers,
ckpd FIXED     always a destroyer of significant digits,
ckpd FIXED
ckpd FIXED  2) we do a floating point compare of the floating point
ckpd FIXED     results to floating zero, never a safe operation, and
ckpd FIXED
ckpd FIXED  3) we decide based on those comparisions either
ckpd FIXED
ckpd FIXED     a) to divide by the sum of the few significant digit
ckpd FIXED        results, possibly using values that would be zero with
ckpd FIXED        infinite precision arithmetic, and giving potentially
ckpd FIXED        an explosively large and / or error prone result,
ckpd FIXED
ckpd FIXED     or else
ckpd FIXED
ckpd FIXED     b) not to do so, risking a less than exact computation
ckpd FIXED        when the floating values would be non-zero with
ckpd FIXED        infinite precision arithmetic but are zero computed
ckpd FIXED        with the available limited precision arithmetic.
ckpd FIXED
ckpd FIXED  As a result (discovered by actually paying attention to the
ckpd FIXED  output) this routine is unstable to extremely unstable when
ckpd FIXED  the data points are closely approximating an evenly spaced
ckpd FIXED  linear set of points, what should be the easiest case.

ckpd  Reformatted this to get rid of some unnecessary goto statements.

ckpd  Loop in units of the output array indices.

      do 200 i = 1 , m

ckpd    Take second differences of the first differences.

        a = abs( work( i + 3 ) - work( i + 2 ) )

        b = abs( work( i + 1 ) - work( i     ) )

ckpd    The ATCF data being calculated with slop() consists of latitudes
ckpd    and longitudes to precision 0.1 degree, and it is probably safe
ckpd    to say that insufficient significance remains for a safe
ckpd    division here when the storm motion, or the change in storm
ckpd    motion between sample times, is less than one least significant
ckpd    digit in at least one dimension per unit of time (i.e., is
ckpd    hidden in the roundoff noise).  We can test a simple sum here
ckpd    because we've already taken absolute values above.

ckpd        if ( a .ne. 0.0 .or. b .ne. 0.0 ) then

ckpd    If a quick check shows probable significance in the second
ckpd    difference method, do a cubic interpolation.  (Roughly, average
ckpd    the second differences to get a third difference and interpolate
ckpd    back out to get the smoothed slope, but it isn't that obvious
ckpd    what is going on from the calculation as shown.)

        if ( ( a + b ) .ge. 0.1 ) then

          t( i ) = ( a * work( i + 1 ) + b * work( i + 2 ) ) / ( a + b )

        else

ckpd      Otherwise, the data is too nearly linear in time and space for
ckpd      a useful cubic approximation, so just average the prior and
ckpd      next first differences to get the result.

          t( i ) = 0.5 * ( work( i + 1 ) + work( i + 2 ) )

        endif

  200 continue


c     call prctrc('slop',.false.)

      return

      end
