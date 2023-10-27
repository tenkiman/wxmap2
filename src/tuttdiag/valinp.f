      subroutine valinp (tcyc,nbog)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)valinp.f	1.1 12/15/94
C                        22:45:14 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  valinp
C
C  DESCRIPTION:  validate input in tcyc array
C
C  COPYRIGHT:                  (C) 1994 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  none
C
C  CLASSIFICATION:  unclassified
C
C  RESTRICTIONS:  none
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  Cray UNICOS
C
C  LIBRARIES OF RESIDENCE:
C
C  USAGE:  call valinp (tcyc,nbog)
C
C  PARAMETERS:
C     NAME        TYPE     USAGE           DESCRIPTION
C   --------     ------    -----    ------------------------------
C     tcyc        real    in/out   bogus data values
C     nbog         int    in/out   number of tropical cyclones
C
C  COMMON BLOCKS:  none
C
C  FILES:  none
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C     bad data                 mark, and then omit in count
C
C  ADDITIONAL COMMENTS:
C         contents of bogus data in tcyc:
C                  1         2
C         123456789012345678901234
C         12W 123N 1234E  1234 123
C          A   B     C      D   E
C         where:
C         A - cyclone number and original basin identification
C         B - latitude  times 10, with hemipshere indicator
C         C - longitude times 10, with hemipshere indicator
C         D - forecast direction times 10, degrees (toward)
C         E - forecast speed times 10, knots
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         numchk      validate digits are digits
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          ih         int       heading*10, deg
C          iok        int       good/bad flag
C          is         int       speed*10, kt
C          kg         int       count of good bogus
C          ks         int       starting character position
C          kt         int       ending character position
C          nnum       int       number of digits in number
C          no         int       cyclone number
C          ln         int       longitude*10, deg
C          lt         int       latitude*10,  deg
C
C  METHOD:
C
C  INCLUDE FILES:  none
C
C  COMPILER DEPENDENCIES:  Fortran 77
C
C  COMPILE OPTIONS:
C
C  MAKEFILE:
C
C  RECORD OF CHANGES:
C
C
C...................END PROLOGUE.......................................
C
      implicit none
      integer maxtc
      parameter (maxtc=9)

c
c         formal parameters
      integer nbog
      character*28 tcyc(maxtc+1)
c
c         local variables
      integer kg, n, iok, ks, kt, nnum, no, lt, ln, ih, is
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      kg = 0
      do n=1, nbog
        iok = 0
        if ((tcyc(n)(8:8).eq.'N'   .or. tcyc(n)(8:8).eq.'S') .and.
     &      (tcyc(n)(14:14).eq.'E' .or. tcyc(n)(14:14).eq.'W')) then
          ks = 1
          kt = 2
          call numchk (tcyc(n),ks,kt,nnum)
          if (nnum .eq. 2) then
            ks = 5
            kt = 7
            call numchk (tcyc(n),ks,kt,nnum)
            if (nnum .eq. 3) then
              ks = 10
              kt = 13
              call numchk (tcyc(n),ks,kt,nnum)
              if (nnum .eq. 4) then
                ks = 17
                kt = 20
                call numchk (tcyc(n),ks,kt,nnum)
                if (nnum .eq. 4) then
                  ks = 22
                  kt = 24
                  call numchk (tcyc(n),ks,kt,nnum)
                  if (nnum .eq. 3) then
                    iok = -1
                  else
                    write (*,*) 'Bad bogus speed ',tcyc(n)(22:24)
                  endif
                else
                  write (*,*) 'Bad bogus heading ',tcyc(n)(17:20)
                endif
              else
                write (*,*) 'Bad bogus longitude ',tcyc(n)(10:13)
              endif
            else
              write (*,*) 'Bad bogus latitude ',tcyc(n)(5:7)
            endif
          else
            write (*,*) 'Bad bogus storm number ',tcyc(n)(1:2)
          endif
        else
          write (*,*) 'Bad bogus: ',tcyc(n)(1:24)
        endif
        if (iok .eq. -1) then
c
c                   check range of values
c
          read (tcyc(n),'(i2,2x,i3,2x,i4,3x,i4,1x,i3)') no,lt,ln,ih,is

          iok = 0
c         cyclone number must be within 01 to 50
C mf 20010427 -- eliminate storm # < 50
C
C          if (no.gt.0 .and. no.le.50)   iok = 1
          if (no.gt.0)   iok = 1
c                   latitude check (10*deg)
          if (lt.gt.0 .and. lt.lt.600)  iok = iok +1
c                   longitude check (10*deg)
          if (ln.ge.0 .and. ln.le.1800) iok = iok +1
c                   heading check (deg)
          if (ih.ge.0 .and. ih.le.3600) iok = iok +1
c                   speed check (kts)
          if (is.ge.0 .and. is.le.600)  iok = iok +1
          if (iok .eq. 5) then
c
c                   good data in tropical cyclone bogus
c
            kg = kg +1
c                   back load, as required
            if (kg .lt. n) tcyc(kg) = tcyc(n)
          else
            write (*,*) 'Bad data in bogus: ',tcyc(n)
            tcyc(n) = ' '
          endif
        else
          write (*,*) 'Bad bogus: ',tcyc(n)
          tcyc(n) = ' '
        endif
      enddo
      if (kg .lt. nbog) then
        write (*,*) ' $$$ tctrack, bad input data listed above'
        write (*,*) '     only found ',kg,' good out of ',nbog
        write (*,*)
        nbog = kg
      endif
      return
c
      end
