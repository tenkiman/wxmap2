ckpd  tridecls.inc, used just to get all this trash off the top of
ckpd  the main routine!

ckpd  This program is extensively parameterized, with the parameters
ckpd  held in a separate file.  The whole separate file is included
ckpd  where any of its parameters are needed.  This is done to allow a
ckpd  unique location at which to maintain the parameter values.

ckpd  The last (output) parameter of dtgdif() needs 4 byte integer
ckpd  precision:

ckpd    tri       -- A working array of three parts into which instances of
ckpd                 errors are accumulated for self in the location
ckpd                 indexed where the last subscript has value "iself",
ckpd                 into which instances of errors are accumulated for an
ckpd                 "other" aid that forecasts for the same storm, tau
ckpd                 offset, and forecast synoptic time (to allow
ckpd                 comparisions of aids' forecasting quality, the whole
ckpd                 point of this program), where the last subscript has
ckpd                 value "iother", and into which the occurrences of
ckpd                 these matching errors is counted, where the last
ckpd                 subscript has value "koccur".  Where iself == iother,
ckpd                 the forecasting aid is being compared with itself; i.e.,
ckpd                 the measure of quality is absolute against the best
ckpd                 track as "truth", not comparitive against another aid.

      real*8           tri(naids,naids,ntau,ntdata)


      real*8           tri1(naids,naids,ntau,n1data)

ckpd  We need a place to look at the standard forecast offset hours,
ckpd  since they are neither any longer a) offset by 24 hours, nor b)
ckpd  offset by a fixed amount one from another:

      integer          stdtau(ntau)
      integer          error(naids,nerror,ntau)
      integer          ntot(ntau)
      integer          istat
      integer          iaid
      integer          kerr
      integer          ntused
      integer          ner

      integer          ktau

      logical*1        lstats(nstats)
      logical*1        ltechs(taids)
      logical*1        lerror(nkinds)
      logical*1        iodiag
      logical*1        indone
      logical*1        lposit


      character*4      atech(taids)
      character*4      ntech(naids,ntau)
      character*31     aerr(nkinds)
      character*38     astats(nstats)
      character*3      errin
      character*5      deck
      character*1      stat
      character*6      storm
      character*8      fstdy
      character*8      lstdy
      character*30     cfmt1
      character*30     cfmt2
      character*30     cfmt3
      character*2      cnaids


ckpd  MAINTENANCE WARNING:  The "data" statement for "stdtau" must be
ckpd                        modified to correspond to a change in
ckpd                        parameter "ntau", and vice versa.

ckpd FIXME                    MAINTENANCE WARNING:  This won't work and
ckpd FIXME                    is inappropriate if the ATCF storm and
ckpd FIXME                    aids data storage are ever revised to
ckpd FIXME                    capture the actual tau offset of a
ckpd FIXME                    non-standard last forecast position.
ckpd FIXME                    Right now they incorrectly treat a tau 66
ckpd FIXME                    forecast as a tau 72 forecast, so this
ckpd FIXME                    program follows that error in blind
ckpd FIXME                    ignorance.  See the knownbug.doc file for
ckpd FIXME                    more discussion about this.

ckpd FIXME CONTEXT       data stdtau /12,24,36,48,72/
ckpd FIXME CONTEXT       if (stdtau(ktau).eq.iabs(itau)) nowtau = ktau

      data stdtau
     & /12,24,36,48,72,96,120/

ckpd  This needs to have a value before the routine reading it is set,
ckpd  since it is passed to every subroutine!

      data iodiag /.false./

ckpd  MAINTENANCE WARNING:  The "data" statement for "aerr" must be
ckpd                        modified to correspond to a change in
ckpd                        parameter "nkinds", and vice versa.

      data aerr
     & /'FORECAST ERROR (NM)',
     &  'CROSS TRACK ERROR WRT CLIP (NM)',
     &  'ALONG TRACK ERROR WRT CLIP (NM)',
     &  'TRACK ERROR (NM)',
     &  'SPEED ERROR (KTS)',
     &  'TIMING ERROR (HRS)',
     &  'CROSS TRACK ERROR (NM)',
     &  'ALONG TRACK ERROR (NM)'/

ckpd  MAINTENANCE WARNING:  The "data" statement for astats must be
ckpd                        modified to correspond to a change in
ckpd                        parameter "nstats", and vice versa.

      data astats
     & /'Arithmetic Mean of |Errors|',
     &  'Student''s T and Std. Dev. of +- Errors',
     &  'Gamma Median of +- Errors',
     &  'Arithmetic Median of |Errors|',
     &  'Arithmetic Median of +- Errors'/
