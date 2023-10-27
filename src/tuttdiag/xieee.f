      subroutine xieee(kk,endian,iunfld,len,lvtitle,glob,istat)
C
C.............................START PROLOGUE............................
C
C  SCCS IDENTIFICATION:  %W% %G%
C                        %U% %P%
C
C  CONFIGURATION IDENTIFICATION:  NOGAPS
C
C  MODULE NAME:  xieee 
C
C  DESCRIPTION:  Module to read/write grids in IEEE format.
C
C  ORIGINAL PROGRAMMER: NRL/Monterey
C
C  COPYRIGHT:                  (c) 1996 FLENUMMETOCCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  n/a
C
C  REFERENCES:   None
C
C  CLASSIFICATION:  Unclassified
C
C  RESTRICTIONS:    None
C
C  COMPUTER/OPERATING SYSTEM
C               DEPENDENCIES:  None
C
C  LIBRARIES OF RESIDENCE:  /a/ops/lib/librt.a
C
C  USAGE:  call xieee(kk,endian,iunfld,len,lvtitle,glob,istat)
C       
C
C  PARAMETERS:
C       Name            Type         Usage            Description
C    ----------      ----------     -------  ----------------------------
C    n/a
C
C  COMMON BLOCKS:              Common Blocks are documented where they
C                              are defined in the code within include
C                              files.  This module uses the following
C                              Common Blocks:
C
C       Block      Name     Type    Usage              Notes
C      --------  --------   ----    ------   ----------------------------
C
C  FILES:
C       Name        Unit    Type    Attribute  Usage       Description
C    ----------     ----  --------  --------- -------  ------------------
C
C
C  DATA BASES:
C       Name             Table        Usage            Description
C    ----------     --------------  ---------   -------------------------
C    ISIS           various        input/output
C
C  NON-FILE INPUT/OUTPUT:
C     Name         Type        Usage             Description
C   --------      -------      ------   ---------------------------------
C   n/a
C
C  ERROR CONDITIONS:
C         CONDITION                 ACTION
C     -----------------        ----------------------------
C
C  ADDITIONAL COMMENTS:  None
C
C....................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          Name           Description
C         -------     ----------------------
C
C  LOCAL VARIABLES AND         Variables are documented in detail
C           STRUCTURES:        where they are defined in the code
C                              within include files.
C
C          Name      Type                 Description
C         ------     ----       -----------------------------------------
C         j          integer    do loop index
C         units      char*32    isis units 
C         lvltitl    char*80    isis grid title
C         fbuff      real       buffer array for reading isis grids
C
C  METHOD:                                                              
C 
C
C  INCLUDE FILES:
C       Name                           Description
C    ---------------    -------------------------------------------------
C
C  COMPILER DEPENDENCIES:  f90
C
C  COMPILE OPTIONS:
C
C  MAKEFILE:  rtlib.mak
C
C  RECORD OF CHANGES:
C  <<CHANGE NOTICE>> version 1.1 (Oct 1996) Pauley, R.
C    Initial installation under configuration management.
C
C..............................END PROLOGUE.............................
C
c
      implicit none
c
      integer kk,iunfld,len,istat
      character*8 endian
c
      real x((len+1)/2)
      real glob(len)
      character*80 lvtitle
c
      integer i,len2,ierr,cray2ieg,ieg2cray
c
      len2= (len+1)/2

      if(kk.gt.0) then
 
CCCCC     ierr= cray2ieg(2,len,x,0,glob)
        ierr=0

        if(ierr.eq.0) then
          write(iunfld,rec=1,iostat=istat) (x(i),i=1,len2)
        else
          print*,' cray2ieg pack error, ierr=', ierr
          istat= ierr
        endif

      else
c
        read(iunfld,rec=1,iostat=istat) (x(i),i=1,len2)
c
        if (istat.eq.0) then

CCCCC          ierr= ieg2cray(2,len,x,0,glob)

          ierr=0
          if(ierr.ne.0) then
            print*,' ieg2cray unpack error, ierr= ',ierr
            istat=ierr
          endif

        else
          print *,'xieee read error'
        endif
c
      endif
c
      return
      end
