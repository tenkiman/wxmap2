
CCS Keywords: @(#)zoomv.inc	1.1 12/15/94
C	      22:40:59 /cm/library/tctrack/src/inc/SCCS/s.zoomv.inc

      integer mi, nj, kzlt, lzlt, mz, nz, mbyn
      real rint, sint
c
c
c                   common zoomv variable definitions
c
c           mi - starting minimum first  dimension of contouring block
c           nj - starting minimum second dimension of contouring block
c         rint - first  dimension resolution of zoomed block
c         sint - second dimension resolution of zoomed block
c         kzlt - first  dimension of zoomed block
c         lzlt - second dimension of zoomed block
c           mz - first  dimension of field being contoured
c           nz - second dimension of field being contoured
c         mbyn - total size of field being contoured (mz*nz)
c
      common/zoomv/ mi,nj,rint,sint,kzlt,lzlt,mz,nz,mbyn
