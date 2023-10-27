c
c  SCCS IDENTIFICATION: 
c
c     name          description
c   ----------- -------------------------------------------
c    rlat         latitude of initial cyclone location (-SH)
c    rlon         longitude of initial cyclone location (E)
c    head         last known heading of cyclone (deg)
c    speed        last known speed of cyclone (kt)
c    ricyc        initial i-grid location of cyclone
c    rjcyc        initial j-grid location of cyclone
c
      real rlat, rlon, head, speed, ricyc, rjcyc
c
      common/r_cyclone/ rlat,rlon,head,speed,ricyc,rjcyc
