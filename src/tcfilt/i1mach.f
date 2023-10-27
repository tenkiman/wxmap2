      integer function i1mach(i)
c***begin prologue  i1mach
c***date written   750101   (yymmdd)
c***revision date  910131   (yymmdd)
c***category no.  r1
c***keywords  machine constants
c***author  fox, p. a., (bell labs)
c           hall, a. d., (bell labs)
c           schryer, n. l., (bell labs)
c***purpose  returns integer machine dependent constants
c***description
c
c     this is the cmlib version of i1mach, the integer machine
c     constants subroutine originally developed for the port library.
c
c     i1mach can be used to obtain machine-dependent parameters
c     for the local machine environment.  it is a function
c     subroutine with one (input) argument, and can be called
c     as follows, for example
c
c          k = i1mach(i)
c
c     where i=1,...,16.  the (output) value of k above is
c     determined by the (input) value of i.  the results for
c     various values of i are discussed below.
c
c  i/o unit numbers.
c    i1mach( 1) = the standard input unit.
c    i1mach( 2) = the standard output unit.
c    i1mach( 3) = the standard punch unit.
c    i1mach( 4) = the standard error message unit.
c
c  words.
c    i1mach( 5) = the number of bits per integer storage unit.
c    i1mach( 6) = the number of characters per integer storage unit.
c
c  integers.
c    assume integers are represented in the s-digit, base-a form
c
c               sign ( x(s-1)*a**(s-1) + ... + x(1)*a + x(0) )
c
c               where 0 .le. x(i) .lt. a for i=0,...,s-1.
c    i1mach( 7) = a, the base.
c    i1mach( 8) = s, the number of base-a digits.
c    i1mach( 9) = a**s - 1, the largest magnitude.
c
c  floating-point numbers.
c    assume floating-point numbers are represented in the t-digit,
c    base-b form
c               sign (b**e)*( (x(1)/b) + ... + (x(t)/b**t) )
c
c               where 0 .le. x(i) .lt. b for i=1,...,t,
c               0 .lt. x(1), and emin .le. e .le. emax.
c    i1mach(10) = b, the base.
c
c  single-precision
c    i1mach(11) = t, the number of base-b digits.
c    i1mach(12) = emin, the smallest exponent e.
c    i1mach(13) = emax, the largest exponent e.
c
c  double-precision
c    i1mach(14) = t, the number of base-b digits.
c    i1mach(15) = emin, the smallest exponent e.
c    i1mach(16) = emax, the largest exponent e.
c
c  to alter this function for a particular environment,
c  the desired set of data statements should be activated by
c  removing the c from column 1.  also, the values of
c  i1mach(1) - i1mach(4) should be checked for consistency
c  with the local operating system.
c***references  fox p.a., hall a.d., schryer n.l.,*framework for a
c                 portable library*, acm transactions on mathematical
c                 software, vol. 4, no. 2, june 1978, pp. 177-188.
c***routines called  (none)
c***end prologue  i1mach
c
      integer imach(16),output
      equivalence (imach(4),output)
c
c     machine constants for the cray 1, xmp, 2, and 3.
c     using the 64 bit integer compiler option
c
c === machine = cray.64-bit-integer
       data imach( 1) /     5 /
       data imach( 2) /     6 /
       data imach( 3) /   102 /
       data imach( 4) /     6 /
c      data imach( 5) /    64 /
c      data imach( 6) /     8 /
       data imach( 5) /    32 /
       data imach( 6) /     4 /
       data imach( 7) /     2 /
       data imach( 8) /    31 /
c      data imach( 8) /    63 /
       data imach( 9) /  2147483647 /
c      data imach( 9) /  777777777777777777777b /
       data imach(10) /     2 /
c      data imach(11) /    47 /
       data imach(11) /    15 /
cc     data imach(12) / -8189 /
cc     data imach(13) /  8190 /
       data imach(12) / -65   /
       data imach(13) /  63   /
       data imach(14) /    94 /
       data imach(15) / -8099 /
       data imach(16) /  8190 /
c
c***first executable statement  i1mach
      if (i .lt. 1  .or.  i .gt. 16)
     1   call xerror ( 'i1mach -- i out of bounds',25,1,2)
c
      i1mach=imach(i)
      return
c
      end
