c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ----------     ------------------------------------------------
c    uls85         starting  850 hPa u-wind field (m/s)
c    vls85         starting  850 hPa v-wind field (m/s)
c    uls55         starting  550 hPa u-wind field (m/s)
c    vls55         starting  550 hPa v-wind field (m/s)
c    uls25         starting  250 hPa u-wind field (m/s)
c    vls25         starting  250 hPa v-wind field (m/s)
c    tls10         starting 1000 hPa potential temperature (K)
c    tls85         starting  850 hPa potential temperature (K)
c    tls55         starting  550 hPa potential temperature (K)
c    tls25         starting  250 hPa potential temperature (K)
c    zls10         starting 1000 hPa geopotential (m)
c
      double precision uls85(ixm,jym), uls55(ixm,jym), uls25(ixm,jym),
     &                 vls85(ixm,jym), vls55(ixm,jym), vls25(ixm,jym),       
     & tls10(ixm,jym), tls85(ixm,jym), tls55(ixm,jym), tls25(ixm,jym)
      double precision uls(ixm,jym,3), vls(ixm,jym,3)
      double precision tls(ixm,jym,4)

      double precision zls10(ixm,jym)
c
      common/mstrls/ uls85,uls55,uls25,  vls85,vls55,vls25,
     &               tls10,tls85,tls55,tls25,
     &               zls10
c
      equivalence (uls85(1,1),uls(1,1,1)), (vls85(1,1),vls(1,1,1))
      equivalence (tls10(1,1),tls(1,1,1))
