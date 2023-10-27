      subroutine icrdtg ( idtg1, idtg2, incr )

      integer*2 inid(12)

ckpd      dimension inid(12)

      integer*4 id, julda, julhr, newhr, nda

ckpd It doesn't work very well to have the last parameter of icrdtg be of
ckpd default integer type, defined either by the compile time switches _or_
ckpd by the $STORAGE metacommand, and then pass it integer constants whose
ckpd size is determined by the $STORAGE command but _not_ by the compile
ckpd time flags.  Worse yet, the last parameter is often shared with the
ckpd one used to call dtgdif(), which _must_ be a four byte integer, and
ckpd called in juda(), also expecting a four byte integer.  1992.12.24.

      integer*4 incr

      character idtg1*8, idtg2*8, yy*2, mm*2, dd*2, hh*2

      data inid /   0,  31,  59,  90, 120, 151,
     &            181, 212, 243, 273, 304, 334 /


c     call prctrc('icrdtg',.true.)

      read (idtg1,'(4i2)') iyr, imo, ida, ihr

 1000 format (4i2)

      leap = mod( iyr, 4 )

      id = iyr * 365.25 + 1

      if (leap .eq. 0) id = id - 1

      iadd = 0

      if (leap .eq. 0 .and. imo .gt. 2) iadd = 1

      julda = inid(imo) + ida + iadd

ckpd FIXME  This calculation is obviously not doing what the original
ckpd FIXME  author intended, because the "0.5" added for rounding makes
ckpd FIXME  no sense when all of the variables are of integer type and
ckpd FIXME  the rest of the calculation is all whole numbers.
ckpd FIXME CONTEXT  julhr = 24.0 * (id + julda) + ihr + 0.5

      julhr = 24.0 * (id + julda) + ihr + 0.5

      newhr = julhr + incr

      nda = float(newhr)/24.

      ihr = newhr - nda*24.

      iyr = float(nda - 1) / 365.25

      nda = float(nda) - iyr * (365.25)

      do 100 i = 2, 12

        iadd = 0

        leap = mod( iyr, 4 )

        if ( leap .eq. 0 .and. i .gt. 2 ) iadd = 1

        if ( nda .le. ( inid(i) + iadd ) ) go to 200

  100 continue

      imo = 12

      go to 300

  200 imo = i - 1

  300 continue

      ida = nda - inid(imo)

      if ( leap .eq. 0 .and. imo .gt. 2 ) ida = ida - 1

      write (idtg2, '(4i2.2)' ) iyr, imo, ida, ihr


c     call prctrc('icrdtg',.false.)

      return

      end
