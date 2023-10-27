      subroutine outgdat (nwrt,
     $     tcyc,gdat,numv,mxhr,nbog,maxfix,mxfct,ntrk,dtau)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)outgdat.f	1.2 8/1/95
C                        16:35:28 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  outgdat
C
C  DESCRIPTION:  output tracking data
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
C  USAGE:  call outgdat (nwrt,tcyc,gdat,numv,mxhr,nbog,mxfct,ntrk)
C
C  PARAMETERS:
C     NAME        TYPE        USAGE             DESCRIPTION
C   --------     -------      ------   ------------------------------
C     nwrt        int           in     output unit number
C     tcyc        char          in     initial bogus values array
C     gdat        real          in     tracking data array
C     numv        int           in     first dimension of gdat,
C                                      number of values in each set
C     mxhr        int           in     second dimension of gdat,
C                                      number of tracking positions
C     nbog        int           in     third dimension of gdat,
C                                      number of cyclones tracked
C     mxfct       int           in     max forecast index in tracking
C     ntrk        int           in     number of cyclones being tracked
C                                      when tracking terminated
C
C  COMMON BLOCKS:  none
C
C  FILES:  none
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:  none
C
C  ADDITIONAL COMMENTS:
C     contents of gdat array:
C        first index  1 - latitude, deg (+NH, -SH)
C                     2 - longitude, deg (0 - 360 EAST)
C                     3 - first  dimension grid location
C                     4 - second dimension grid location
C                     5 - heading, deg
C                     6 - distance traveled last 6 hours, nm
C                     7 - confidence factor
C                           0.0 - not rated
C                           1.0 - only one cyclone in area
C      ******  all the following have 2 or more cyclones in search area  *****
C                           2.0 - cyclone selected is closest to both ep & lkl
C                                 and has the higher wind speed
C                           3.0 - cyclone selected is closest to either ep or
C                                 lkl with good wind support and speed
C                           4.0 - cyclone selected is closest to either ep or
C                                 lkl with best wind and intersection support
C                           5.0 - cyclone selected is closest to either ep or
C                                 lkl with highest wind speed
C                           6.0 - cyclone selected has highest wind speed
C                     8 - wind support factor
C                           3.0 - three quadrants
C                           4.0 - all four quadrants
C                     9 - intersection support factor
C                           2.0 thru 8.0, the larger the better
C       second index  0 - bogus position
C                     1 - analysis position
C                     2 - 6-hr position
C                     3 - 12-hr position
C                    --   --------------
C                    25 - 144-hr position
C        third index  1 - first  cyclone in bogus data file
C                     2 - second cyclone in bogus data file
C
C     example and format of output:
C                  1         2         3         4         5
C         12345678901234567890123456789012345678901234567890
C          *** 36W  25.9  158.4  285.60  11.20 0 0 0
C          000 36W  25.5  158.5  285.60  11.20 1 4 8
C          006 36W  26.2  157.6  307.89  10.67 1 4 8
C
C          tau nnb  lat    lon    head   speed k j i
C
C       where:  tau - forecast period, *** - bogus
C               nnb - cyclone number and one letter original basin code
C               lat - latitude, -SH
C               lon - 0 - 360 deg EAST
C              head - heading in degrees, last six hours
C             speed - average speed during last six hours, kt
C                 k - confidence factor of location
C                 j - wind support factor
C                 i - intersection support factor
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:  none
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C           k         int       second index to gdat
C           kill      int       do while control variable
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
C  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
C    Modify documentation to agree with changes in other S/R
C
C...................END PROLOGUE.......................................
C
      implicit none
      integer maxtc
      parameter (maxtc=9)

c
c         formal parameters
      integer numv, mxhr, nwrt, nbog,maxfix, mxfct, ntrk, dtau
      character*28 tcyc(maxtc+1)
      real*4 gdat(numv,0:mxhr,nbog,0:maxfix)
c
c         local variables
      integer k, kill, n, ifac, jfac, kfac
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c                   output data cyclone by cyclone
c
      write (*,*) 'Output tracking data'
      do n=1, nbog
        kill = 0
        k    = -1
        do while (kill .eq. 0)
          k = k +1
          if (abs (gdat(1,k,n,0)) .gt. 90.0) then
            gdat(2,k,n,0) = 999.9
            gdat(5,k,n,0) = 999.99
            gdat(6,k,n,0) =  99.99*dtau
            gdat(7,k,n,0) =   0.0
            gdat(8,k,n,0) =   0.0
            gdat(9,k,n,0) =   0.0
            kill = -1
          endif
          kfac = nint (gdat(7,k,n,0))
          jfac = nint (gdat(8,k,n,0))
          ifac = nint (gdat(9,k,n,0))
          write (*,9008) (k-1)*dtau,tcyc(n),
     $         gdat(1,k,n,0),gdat(2,k,n,0),
     $         gdat(5,k,n,0),gdat(6,k,n,0)/dtau,kfac,jfac,ifac
          write (nwrt,9008) (k-1)*dtau,tcyc(n),
     $         gdat(1,k,n,0),gdat(2,k,n,0),
     $         gdat(5,k,n,0),gdat(6,k,n,0)/dtau,kfac,jfac,ifac
          if (kill .ne. 0) then
c
c                   terminate output of cyclone when track lost
c
            write (*,9020)
            write (nwrt,9020)
          endif
c
c                   if last position output, terminate output
c
          if (k .eq. mxfct) kill = -1
        enddo
      enddo
 9008 format (1x,i3.3,1x,a4,1(f5.1,1x,f6.1),2x,f5.1,2x,f4.1,
     &        3(1x,i4))
 9010 format (1x,i3.3,1x,a4,3(f5.1,1x,f6.1),2x,f5.1,2x,f4.1,
     &        3(1x,i4))
 9020 format (' LOST TRACK OF CYCLONE')
      if (ntrk .eq. 0) then
c
c                 tracking was terminated because all cyclones were lost
c
        write (*,9030)
        write (nwrt,9030)
 9030   format (' LOST TRACK OF ALL CYCLONES - ABORTING')
      elseif (ntrk .eq. nbog) then
c
c                   no cyclones were lost during tracking
c
        write (*,9040)
        write (nwrt,9040)
 9040   format (' FINISHED TRACKING ALL CYCLONES')
      else
c
c                 one or more cyclone tracks were lost, but at least one
c                 cyclone was still being tracked when field data ended
c
        write (*,9050)
        write (nwrt,9050)
 9050   format (' FINISHED TRACKING CYCLONES')
      endif
      return
c
      end
