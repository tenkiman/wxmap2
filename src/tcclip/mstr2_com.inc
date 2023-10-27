c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ----------     ------------------------------------------------
c    u285          second  850 hPa u-wind field (m/s)
c    v285          second  850 hPa v-wind field (m/s)
c    u255          second  550 hPa u-wind field (m/s)
c    v255          second  550 hPa v-wind field (m/s)
c    u225          second  250 hPa u-wind field (m/s)
c    v225          second  250 hPa v-wind field (m/s)
c    t210          second 1000 hPa potential temperature (K)
c    t285          second  850 hPa potential temperature (K)
c    t255          second  550 hPa potential temperature (K)
c    t225          second  250 hPa potential temperature (K)
c    z210          second 1000 hPa geopotential (m)
c    z285          second  850 hPa geopotential (m)
c    z255          second  550 hPa geopotential (m)
c    z225          second  250 hPa geopotential (m)
c
      double precision u285(ixm,jym), u255(ixm,jym), u225(ixm,jym),
     &                 v285(ixm,jym), v255(ixm,jym), v225(ixm,jym),
     &  t210(ixm,jym), t285(ixm,jym), t255(ixm,jym), t225(ixm,jym)
      double precision uu2(ixm,jym,3), vv2(ixm,jym,3)
      double precision pt2(ixm,jym,4)

      double precision z210(ixm,jym), z285(ixm,jym), z255(ixm,jym),
     &                 z225(ixm,jym)
      double precision gz2(ixm,jym,4)
c
      common/mstr2/     u285,u255,u225,      v285,v255,v225,
     &             t210,t285,t255,t225, z210,z285,z255,z225
c
      equivalence (u285(1,1),uu2(1,1,1)), (v285(1,1),vv2(1,1,1))
      equivalence (t210(1,1),pt2(1,1,1)), (z210(1,1),gz2(1,1,1))
