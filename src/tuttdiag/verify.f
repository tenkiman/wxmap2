      subroutine verify (nhsh,ddfld,ixgd,jygd,mxptc,cirdat,nccf,iunit)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)verify.f	1.2 8/1/95
C                        16:16:21 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  verify
C
C  DESCRIPTION:  driver to track tropical cyclones
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
C  USAGE:  call verify (nhsh,ddfld,ixgd,jygd,mxptc,cirdat,nccf)

C
C  PARAMETERS:
C     NAME       TYPE     USAGE           DESCRIPTION
C   --------    ------    ------    ------------------------------
C     nhsh        int       in      hemisphere flag, +NH, - SH
C    ddfld       real       in      wind direction field, deg
C     ixgd        int       in      first  dimension of ddfld
C     jygd        int       in      second dimension of ddfld
C   cirdat       real     in/out    circulation data
C                                     (1, first  dimension location
C                                     (2, second dimension location
C                                     (3, wind support factor, 3 or 4
C                                     (4, intersection support, 2 - 8
C     nccf        int     in/out    number of prospective cc's/
C                                   number of verified cc's
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
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         isofnd      driver routine for locating cyclone with isogons
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          ccvdat    real       working array of cirdat
C          exc       real       estimated first  dimension location
C          eyc       real       estimated second dimension location
C          iadd       int       flag for keeping cyclone
C          iloc       int       cyclone location flag, 0 not found
C          kc         int       total count of verified cyclones
C          kccf       int       count of verified cc's per area
C          kint       int       array of intersection counts
C          kuvs       int       array of quadrant wind support counts
C          xc        real       array of x-grid location of cyclone(s)
C          yc        real       array of y-grid location of cyclone(s)
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
C    Make changes to allow more than one intersection centers per area
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal argumnets
      integer nhsh, ixgd, jygd, mxptc, nccf
      integer iunit
      real ddfld(ixgd,jygd), cirdat(4,mxptc)
c
c         local variables
      integer n, k, kk, kccf, kc, iadd
      integer kuvs(4), kint(4)
      real exc, eyc, xc(4), yc(4)
      real ccvdat(2,mxptc)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      write(iunit,*) ' verify, processing ',nccf,' areas'
      do n=1, nccf
        ccvdat(1,n) = cirdat(1,n)
        ccvdat(2,n) = cirdat(2,n)
        cirdat(1,n) = 0.0
        cirdat(2,n) = 0.0
        cirdat(3,n) = 0.0
        cirdat(4,n) = 0.0
      enddo
c
c                   search for cyclonic centers based upon isogons
c
      kc = 0
      do n=1, nccf
        exc = ccvdat(1,n)
        eyc = ccvdat(2,n)
        write(iunit,*) 'Verify, checking ',n,' at ',exc,'  ',eyc
        call isofnd (exc,eyc,nhsh,ddfld,ixgd,jygd,kccf,kuvs,kint,xc,yc,iunit)
        if (kccf .gt. 0) then
c
c                     circulation center found with isogons
c
          write(iunit,*) ' isofnd found ',kccf,' cyclones for area ',n
          do k=1, kccf
            write(iunit,*) 'cyclone ',k,' is at ',xc(k),'  ',yc(k)
            if (kc .eq. 0) then
              kc = 1
              cirdat(1,1) = xc(k)
              cirdat(2,1) = yc(k)
              cirdat(3,1) = kuvs(k)
              cirdat(4,1) = kint(k)
            else
c
c                     do not add duplicate position
c
              iadd = -1
              do kk=1, kc
                if (abs (cirdat(1,kk) -xc(k)) .le. 0.1) then
                  if (abs (cirdat(2,kk) -yc(k)) .le. 0.1) iadd = 0
                endif
              enddo
              if (iadd .eq. -1) then
c
c                     add new cyclone location to cirdat
c
                kc = kc +1
                if (kc .le. mxptc) then
                  cirdat(1,kc) = xc(k)
                  cirdat(2,kc) = yc(k)
                  cirdat(3,kc) = kuvs(k)
                  cirdat(4,kc) = kint(k)
                endif
              else
                write(iunit,*) ' verify, duplicate cyclone at ',xc(k),
     &                       '  ',yc(k)
              endif
            endif
          enddo
        endif
      enddo
      if (kc .gt. mxptc) then
        write (*,*) 'ERROR: verify, cirdat too small, needed = ',kc
        kc = mxptc
      endif
      nccf = kc
      write(iunit,*)'Verify, retained ',nccf,' cyclones'
      return
c
      end
