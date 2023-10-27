c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ----------     ------------------------------------------------
c    u185          first  850 hPa u-wind field (m/s)
c    v185          first  850 hPa v-wind field (m/s)
c    u155          first  550 hPa u-wind field (m/s)
c    v155          first  550 hPa v-wind field (m/s)
c    u125          first  250 hPa u-wind field (m/s)
c    v125          first  250 hPa v-wind field (m/s)
c    t110          first 1000 hPa potential temperature (K)
c    t185          first  850 hPa potential temperature (K)
c    t155          first  550 hPa potential temperature (K)
c    t125          first  250 hPa potential temperature (K)
c    z110          first 1000 hPa geopotential (m)
c    z185          first  850 hPa geopotential (m)
c    z155          first  550 hPa geopotential (m)
c    z125          first  250 hPa geopotential (m)
c
      double precision u185(ixm,jym), u155(ixm,jym), u125(ixm,jym),
     &                 v185(ixm,jym), v155(ixm,jym), v125(ixm,jym),
     &  t110(ixm,jym), t185(ixm,jym), t155(ixm,jym), t125(ixm,jym)
      double precision uu1(ixm,jym,3), vv1(ixm,jym,3)
      double precision pt1(ixm,jym,4)

      double precision z110(ixm,jym), z185(ixm,jym), z155(ixm,jym),
     &                 z125(ixm,jym)
      double precision gz1(ixm,jym,4)
c
      common/mstr1/     u185,u155,u125,      v185,v155,v125,
     &             t110,t185,t155,t125, z110,z185,z155,z125
c
      equivalence (u185(1,1),uu1(1,1,1)), (v185(1,1),vv1(1,1,1))
      equivalence (t110(1,1),pt1(1,1,1)), (z110(1,1),gz1(1,1,1))
