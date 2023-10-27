      subroutine fldread (cdtg,rtau,ddfld,fffld,ierr)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)fldread.f	1.2 8/1/95
C                        16:16:11 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  fldread
C
C  DESCRIPTION:  driver routine for reading ISIS fields and producing
C                derived field
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
C  USAGE:  call fldread (cdtg,rtau,ddfld,fffld,ierr)
C
C  PARAMETERS:
C     NAME         TYPE        USAGE             DESCRIPTION
C   --------      -------      ------   ------------------------------
C       cdtg       char          in     date_time_group of fields
C       rtau       real          in     forecast period
C      ddfld       real         out     wind direction field
C      fffld       real         out     wind speed field
C       ierr        int         out     error flag, 0 no error
C
C  COMMON BLOCKS:  none
C
C  FILES:  none
C
C  DATA BASES:
C     NAME          TABLE      USAGE       DESCRIPTION
C    --------     -----------  ------  --------------------
C      ISIS         NOGAPS       in    analysis & forecast fields
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C     missing field or         set error flag to non-zero
C        read error
C
C  ADDITIONAL COMMENTS:
C    Tau 0 fields are read from anal_ops vice fcst_ops to see how close
C    the bogus position is to the initial analysis position w/o model
C    initialization.  As far as the tracking goes, it would make no
C    difference if all the fields were from fcst_ops.
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         calddto     calculates wind direction, towards (deg)
C             grd     reads requested ISIS field
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         dsetnam    char       data set name
C         dsets      char       data set names
C         geonam     char       geometry name
C         idgrid      int       internal dataset identifier number
C         igrdx       int       first  dimension of fields
C         irecnum     int       internal record sequence number
C         istatus     int       status of ISIS request
C         jgrdy       int       second dimension of fields
C         params     char       parameter names
C         rlvl1      real       level 1 value
C         rlvl2      real       level 2 value
C         seclvl     char       security level
C         title      char       title of field
C         typlvl     char       type of level
C         typmodl    char       type of model
C         units      char       units of fields
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
C  <<CHANGE NOTICE>>  Version 1.1  (15 DEC 1994) -- Hamilton, H.
C    Initial installation
C
C  <<CHANGE NOTICE>>  Version 1.2  (09 AUG 1995) -- Hamilton, H.
C    Add return of wind speed field by S/R calddto
C
C...................END PROLOGUE.......................................
C
      implicit none
c
      integer igrdx, jgrdy
      parameter (igrdx = 360,  jgrdy = 181)
c
c         formal parameters
      integer ierr
      character*16 cdtg
      real rtau,rlvl(2)
      real ddfld(igrdx,jgrdy), fffld(igrdx,jgrdy)
c
c         local variables
      integer idgrid, irecnum, istatus, len
c
      character*8  seclvl
      character*24 dsetnam, dsets(2), typlvl
      character*32 typmodl, geonam, params(2), units
      character*80 title
c
c
c                   ISIS parameters
      data typmodl/'/a/jgoerss/tropflds'/, geonam/'glob360x181'/
      data params/'uuwind', 'vvwind'/
      data dsets/'analfld', 'fcstfld'/
      data rlvl/1000.0,0.0/
      data units/'m/s'/
      data typlvl/'pre'/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
      ierr = -1
      len=360*181
c     if (rtau .lt. 6.0) then
c       dsetnam = dsets(1)
c     else
        dsetnam = dsets(2)
c     endif
c
c                   read 1000 mb u-wind - into ddfld
c
      write (*,*) 'Reading U-wind for ',cdtg,' tau ',rtau
      call glclrd(typmodl,geonam,dsetnam,params(1),typlvl,1,rlvl
     x,     cdtg,rtau,units,ddfld,title,seclvl,len,istatus)
      write (*,*) ' U-wind return code is ',istatus
      if (istatus.ge.0 .and. istatus.ne.100) then
c
c                     read 1000 mb v-wind - into htfld
c
        write (*,*) 'Reading V-wind for ',cdtg,' tau ',rtau
      call glclrd(typmodl,geonam,dsetnam,params(2),typlvl,1,rlvl
     x,     cdtg,rtau,units,fffld,title,seclvl,len,istatus)
        write (*,*) ' V-wind return code is ',istatus
        if (istatus.ge.0 .and. istatus.ne.100) then
c
c                   calcaulate direction of wind, towards - ddfld
c
          call calddto (ddfld,fffld,igrdx,jgrdy)
          ierr = 0
          write (*,*) ' Have dd-field for tau ',rtau
        endif
      endif
      return
c
      end
