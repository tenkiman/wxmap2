c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ----------    ----------------------------------------------------
c    ixm          number of grid points, first  dimension of Mercator
c    jym          number of grid points, second dimension of Mercator
c    mg_deg       number of degrees of logitude between grid points
c    deg2m        conversion factor, meters per degree at latitude 22.5
c
      integer    ixm, jym, mg_deg
      parameter (ixm = 62, jym = 46, mg_deg = 1)
c              NOTE:  the Mercator grid is true at 22.5 degrees latitude
c                     1 deg = 111,137m x COS (22.5) = 102,677.2m
      double precision  deg2m
      parameter        (deg2m = 102677.2d0)
c
