C  SCCS IDENTIFICATION:  @(#)box.inc	1.2 8/1/95
C                        16:51:25 @(#)
C
C  RECORD OF CHANGES:
C
C  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
C    Increase dimension of rxc, ryc, nip, cx and cy by 4 to allow
C    more than one intersection to be located by S/R calint.
C
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
      integer nint
      parameter (nint = 9)
c
      integer lbox, nsys, nip
      real xs,xl, ys,yl, rxc,ryc, cx,cy
c
c                   common box variable definitions
c
c         lbox - unit number for diagnostics
c           xs - real starting first dimension of isogon box
c           xl - real ending first dimension of isogon box
c           ys - real starting second dimension of isogon box
c           yl - real ending second dimension of isogon box
c         nsys - number of systems being processed
c          rxc - array of running averages, first dimension intersection
c                points
c          ryc - array of running averages second dimension intersection
c                points
c          nip - array of number of intersection points
c           cx - array of first  dimension intersection points
c           cy - array of second dimension intersection points
c
      common/box/ lbox,xs,xl,ys,yl,nsys,rxc(4),ryc(4),nip(4),
     &            cx(4,nint),cy(4,nint)
