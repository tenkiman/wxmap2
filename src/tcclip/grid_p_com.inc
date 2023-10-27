c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ---------    -----------------------------------------------
c    del         Mercator grid length at 22.5 deg (m)
c    twodel      twice del
c    f           Coriolis parameter, as a function of j
c    em          map factor, as a function of j
c    emi         inverse of em
c    gdlon       longitude of grid points
c    ring        global i-grid extraction points
c    gdlat       latitude of grid points
c    rjng        global j-grid extraction points
c
      double precision del, twodel
      double precision f(jym), em(jym), emi(jym)
      real   gdlon(ixm), ring(ixm)
      real   gdlat(jym), rjng(jym)
c
      common/grid_par/ del,twodel,f,em,emi,gdlat,gdlon,ring,rjng
c
