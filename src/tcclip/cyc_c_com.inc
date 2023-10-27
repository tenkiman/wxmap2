c
c  SCCS IDENTIFICATION:  @(#)cyc_c_com.inc	1.1  01 Jun 1996
c
c     name          description
c   ---------     ----------------------------------------------
c    cycid        cyclone identification, number and basin (04W)
c    cycdtg       dtg of starting position (YYYYMMDDHH)
c
      character cycid*3, cycdtg*10
c
      common/c_cyclone/ cycid,cycdtg
