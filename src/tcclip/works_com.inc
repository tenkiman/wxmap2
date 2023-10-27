c
c  SCCS IDENTIFICATION:
c
c     working arrays for real and double precision values, Mercator grid
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      real              wrk41(ixm,jym), wrk42(ixm,jym), wrk43(ixm,jym),
     &  wrk44(ixm,jym), wrk45(ixm,jym), wrk46(ixm,jym), wrk47(ixm,jym)
c
      double precision  wrk81(ixm,jym), wrk82(ixm,jym), wrk83(ixm,jym),
     &  wrk84(ixm,jym), wrk85(ixm,jym), wrk86(ixm,jym), wrk87(ixm,jym)
c
      common/dumwrk/ wrk81, wrk82, wrk83, wrk84, wrk85, wrk46, wrk47
c
      equivalence (wrk81(1,1),wrk41(1,1)), (wrk82(1,1),wrk42(1,1))
      equivalence (wrk83(1,1),wrk43(1,1)), (wrk84(1,1),wrk44(1,1))
      equivalence (wrk85(1,1),wrk45(1,1)), (wrk86(1,1),wrk46(1,1))
      equivalence (wrk87(1,1),wrk47(1,1))
c
