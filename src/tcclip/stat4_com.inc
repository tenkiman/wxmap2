c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ----------   --------------------------------------------
c    y2eq        distance from initial position of tropical cyclone
c                (working best track) to the equator on the Mercator
c                grid (m)
c    re_tlat_i   inverse of the radius of the Earth where the map 
c                factor is 1.0 on the Mercator grid (22.5 deg lat) (m)
c
      double precision  y2eq, re_tlat_i
c
      common/static4/ y2eq,re_tlat_i
c
