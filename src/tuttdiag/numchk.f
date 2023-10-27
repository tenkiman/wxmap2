      subroutine numchk (card,ks,kt,nnum)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)numchk.f	1.1 12/15/94
C                        22:44:09 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  numchk
C
C  DESCRIPTION:  check that characters between ks-1 and kt+1 are all
C                numbers or number(s) and blank(s)
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
C  USAGE:  call numchk (card,ks,kt,nnum)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C     card         char         in      character string
C     ks            int         in      starting character for checking
C     kt            int         in      ending character for checking
C     nnum          int         out     number of digits or number of
C                                       digits and blanks
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
C  MODULES CALLED:  none
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          cx        char       working character
C          nblk       int       count of blanks
C          js         int       starting character position
C          jt         int       ending character position
C
C  METHOD:  N/A
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
c
c         formal parameters
      integer ks, kt, nnum
      character*24 card
c
c         local variables
      integer nblk, js, jt, j
      character*1 cx
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      nnum = 0
      nblk = 0
c                   validate starting and ending positions
      js = max0 (ks,1)
      jt = min0 (kt,24)
      do j=js, jt
        cx = card(j:j)
        if (cx.ge.'0' .and. cx.le.'9') then
          nnum = nnum +1
        elseif (cx .eq. ' ') then
          nblk = nblk +1
        endif
      enddo
      if (nblk.gt.0 .and. nnum.ge.1) nnum = nnum +nblk
      return
c
      end
