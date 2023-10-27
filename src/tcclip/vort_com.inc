c  SCCS IDENTIFICATION: 
c
c  RECORD OF CHANGES:
c
c     name          description
c   ----------      -----------------------------------------
c    ijoff          integer "radius" of vortex
c    radmx          real "radius" of vortex
c    dnorm          radius normalize factor for 1-degree Mercator
c
      integer ijoff
      real    radmx, dnorm
c
      common/vort_c/ ijoff, radmx, dnorm
