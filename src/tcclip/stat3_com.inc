c
c  SCCS IDENTIFICATION:
c
c     name          description
c   ----------   ------------------------------------------------
c    heat        weighting function for the amount of heat to be
c                applied to the hPa levels of the model
c    tend        modified Perkey-Kreitzberg weighting function for
c                the time-dependent boundary conditions
c
      real             heat(4)
      double precision tend(ixm,jym) 
c
      common/static3/ heat, tend
c
