
CCS Keywords: @(#)isoxy.inc	1.1 12/15/94
C	      22:40:12 /cm/library/tctrack/src/inc/SCCS/s.isoxy.inc

      integer npts
      parameter (npts = 151)
c
      integer nxy1, nxy2
      real rh1,xx1,yy1, rh2,xx2,yy2
c
c                   common isoxy variable definitions
c
c         nxy1 - number of x,y points in first isogon
c          rh1 - value of first isogon, degrees
c          xx1 - first  dimension first isogon location values
c          yy1 - second dimension first isogon location values
c         nxy2 - number of x,y points in second isogon
c          rh2 - value of second isogon, degrees
c          xx2 - first  dimension second isogon location values
c          yy2 - second dimension second isogon location values
c
      common/isoxy/ nxy1,rh1,xx1(npts),yy1(npts),
     .              nxy2,rh2,xx2(npts),yy2(npts)
