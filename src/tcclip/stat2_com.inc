c
c  SCCS IDENTIFICATION:
c
c     name          discription
c   ---------    ----------------------------------------
c    dp          delta hPa between levels of the model
c    pilo        hydrostatic conversion factor
c    piup        hydrostatic conversion factor
c    pic         conversion factor, temperature to potential
c                temperature
c - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
c
      double precision dp(4), pilo(4), piup(4), pic(4)
c
      common/static2/ dp, pilo, piup, pic
c
