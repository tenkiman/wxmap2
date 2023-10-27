
CCS Keywords: @(#)isol.inc	1.1 12/15/94
C	      22:40:06 /cm/library/tctrack/src/inc/SCCS/s.isol.inc

      logical first, last, open, backwd
c
c                   common isol variable definitions
c
c        first - logical flag indicating start of isogon, if true
c         last - logical flag indicating end of isogon, if true
c         open - logical flag indicating open isogon, if true
c       backwd - logical flag indicating trace direction, backward if
c                true
c
      common/isol/ first,last,open,backwd
