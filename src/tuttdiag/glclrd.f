      subroutine glclrd(mdltype,geomnm,dsetnm,parm,lvlt,nolev,rlvl
     *, dtgdb,rtau,units,glob,lvtitle,clastyp,len,istat)
C
C.............................START PROLOGUE............................
C
C  SCCS IDENTIFICATION:  %W% %G%
C                        %U% %P%
C
C  CONFIGURATION IDENTIFICATION:  NOGAPS
C
C  MODULE NAME:  glclrd
C
C  DESCRIPTION:  Clone glrd. 
C
C  ORIGINAL PROGRAMMER:  NRL/Monterey
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
C  USAGE:  call glclrd(mdltype,geomnm,dsetnm,parm,lvlt,nolev,rlvl
C    ,dtgdb,rtau,units,glob,lvtitle,clastyp,len,istat)
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
C         istat      integer    return status
C         errary     integer    error array returned by glclrd and glwr
C         units      char*32    isis units 
C         lvltitl    char*80    isis grid title
C         opsuser    logical    opsuser logical
C         fbuff      real       buffer array for reading isis grids
C
C  METHOD:  
C
C
C  INCLUDE FILES:
C       Name                           Description
C    ---------------    -------------------------------------------------
C
C  COMPILER DEPENDENCIES:  
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
      implicit none
c
      integer nolev,len,istat
c
      character*24 lvlt,dsetnm,parm
      character*80 mdltype
      character*32 geomnm,units
      character*16 dtgdb
      character*80 lvtitle(nolev)
      character*64 filnam
      character*120 fullpath
      character*3 clv3
      character*4 clv4
      character*5 clv5
      character*6 clv6,clv62
      character*8 clastyp
      character*8 ctau
c
      real glob(len,nolev),rtau,rlvl(2,nolev)
      integer ix(len)
c
      integer iunfld
      character*8 endian
c
      integer len1,itau,k,i,llen,kk
c
      iunfld=80
c
      call chlen(mdltype,len1)
c
      if(mdltype(len1:len1).eq.'/') len1= len1-1
c
      itau= rtau
c
      do 100 k=1,nolev
c
c first level parameter
c
        if(rlvl(1,k).ge.10000.0) then
          write(clv6,'(f6.0)') rlvl(1,k)
c
        else if(rlvl(1,k).ge.1000.0) then
          write(clv6,'(f6.1)') rlvl(1,k)
c
        else if(rlvl(1,k).ge.100.0) then
          write(clv5,'(f5.1)') rlvl(1,k)
          clv6='0'//clv5
c
        else if(rlvl(1,k).ge.10.0) then
          write(clv4,'(f4.1)') rlvl(1,k)
          clv6='00'//clv4
c
        else if(rlvl(1,k).ge.1.0) then
          write(clv3,'(f3.1)') rlvl(1,k)
          clv6='000'//clv3
c
        else
          write(clv3,'(f3.2)') rlvl(1,k)
          clv6='000'//clv3
          if(rlvl(1,k).eq.0.0) clv6='0000.0'
        endif
c
c second level parameter
c
        if(rlvl(2,k).ge.10000.0) then
          write(clv62,'(f6.0)') rlvl(2,k)
c
        else if(rlvl(2,k).ge.1000.0) then
          write(clv62,'(f6.1)') rlvl(2,k)
c
        else if(rlvl(2,k).ge.100.0) then
          write(clv5,'(f5.1)') rlvl(2,k)
          clv62='0'//clv5
c
        else if(rlvl(2,k).ge.10.0) then
          write(clv4,'(f4.1)') rlvl(2,k)
          clv62='00'//clv4
c
        else if(rlvl(2,k).ge.1.0) then
          write(clv3,'(f3.1)') rlvl(2,k)
          clv62='000'//clv3
c
        else
          write(clv3,'(f3.2)') rlvl(2,k)
          clv62='000'//clv3
          if(rlvl(2,k).eq.0.0) clv62='0000.0'
        endif
c
        write(ctau,'(i8.8)') itau*10000
c
        filnam= parm(1:6)//'_'//lvlt(1:3)//'_'//clv6//'_'//clv62//
     *  '_'//geomnm(1:11)//'_'//dtgdb(1:10)//'_'//ctau//
     *  '_'//dsetnm(1:7)
c
        fullpath= mdltype(1:len1)//'/'//filnam(1:64)
        print *,fullpath(1:len1+65)
c
c   read 32 bit IEEE
c
        llen= (len+1)/2
        llen= 8*llen
        open(unit=iunfld,file=fullpath,form='unformatted',status='old'
     *  , access='direct',recl=llen,iostat=istat)
c
        if(istat.eq.0) then
          kk= -1
          call xieee(kk,endian,iunfld,len,lvtitle(k),glob(1,k),istat)
          if(istat.ne.0) then
            print *,' error reading IEEE field'
            istat=1
          endif
        else
          print *,' field not found'
          istat=2
        endif
c
        close(iunfld)
        if (istat.ne.0) return
c
  100 continue
      return
      end
