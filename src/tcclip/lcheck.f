      function lcheck (nsew)
      character nsew*1
c
c  this function checks the n/s and e/w indicator. it returns
c               0 - not n, s, e, or w
c               1 - n or s
c               2 - e or w
c

c     call prctrc('lcheck',.true.)

      lcheck = 0
      if (nsew .eq. 'N' .or. nsew .eq. 'n' .or. 
     &    nsew .eq. 'S' .or. nsew .eq. 's' ) lcheck = 1
      if (nsew .eq. 'E' .or. nsew .eq. 'e' .or. 
     &    nsew .eq. 'W' .or. nsew .eq. 'w' ) lcheck = 2

c     call prctrc('lcheck',.false.)

      return
      end
