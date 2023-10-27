c
c  SCCS IDENTIFICATION:
c
c     name          description
c   -----------   -------------------------------------------------
c    flat         (0) reported latitude of cyclone (-SH)
c    flat         (1) j-grid initial location of cyclone
c    flat         (X) j-grid forecast location of cyclone
c    flon         (0) reported longitude of cyclone (E)
c    flon         (1) i-grid initial location of cyclone
c    flon         (X) i-grid forecast location of cyclone
c           where: X = 1 to 13
c
      real flat(0:13), flon(0:13)
c
      common/latlon/ flat,flon
