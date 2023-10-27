
CCS Keywords: @(#)isoc.inc	1.1 12/15/94
C	      22:57:38 /cm/library/tctrack/src/inc/SCCS/s.isoc.inc

      integer iter, nc1, nc2
      real rh
c
c
c                   common isoc variable definitions
c
c           rh - true value of isogon, in degrees
c         iter - iteration number, either 1 or 2
c          nc1 - number of isogon points for first  iteration
c          nc2 - number of isogon points for second iteration
c
      common/isoc/ rh,iter,nc1,nc2
