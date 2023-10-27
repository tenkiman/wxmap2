c
c  SCCS IDENTIFICATION:  @(#)omega_com.inc	1.1  01 Jun 1996
c
c     name          description
c   -----------    ---------------------------------------------
c    w10           1000 hPa vertical wind (m/s)
c    w70            700 hPa vertical wind (m/s)
c    w40            400 hPa vertical wind (m/s)
c    w00            100 hPa vertical wind (m/s)
c
      double precision w10(ixm,jym), w70(ixm,jym), w40(ixm,jym),
     &                 w00(ixm,jym)
      double precision www(ixm,jym,4)
c
      common/omega4/ w10, w70, w40, w00
c
      equivalence (w10(1,1),www(1,1,1))
c
