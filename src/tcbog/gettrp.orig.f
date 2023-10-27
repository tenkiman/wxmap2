      subroutine gettrp (nstms,numbstm,noldstm,idtg,slat,slon,smxv,
     &         smr50,smr30,istmno,ibsn, idtgo,olat,olon,nstrm,nobsn)
C
C.............................START PROLOGUE............................
C
C SCCS IDENTIFICATION:  @(#)gettrp.f	1.2 3/17/95
C                       17:25:29 /cm/library/nogaps/src/sub/tbog/SCCS/s.gettrp.f
C
C CONFIGURATION IDENTIFICATION:
C
C MODULE NAME:  gettrp
C
C DESCRIPTION:  read tropical cyclone data from ngtrp file
C
C COPYRIGHT:  (c) 1994 FLENUMMETOCCEN
C             U.S. GOVERNMENT DOMAIN
C             ALL RIGHTS RESERVED
C
C CONTRACT NUMBER AND TITLE:
C
C REFERENCES:
C
C CLASSIFICATION:  Unclassified
C
C RESTRICTIONS:
C
C COMPUTER/OPERATING SYSTEM DEPENDENCIES:
C
C LIBRARIES OF RESIDENCE: /a/ops/lib/libtbog159.a
C
C USAGE: call gettrp (nstms,numbstm,noldstm,idtg,slat,slon,smxv,smr50,
C                     smr30,istmno,ibsn, idtgo,olat,olon,nstrm,nobsn)
C
C PARAMETERS:
C      Name            Type         Usage            Description
C   ----------      ----------     -------  ----------------------------
C   nstms             int            in     maximum number of cyclones
C                                           to process
C   numbstm           int            out    number of now cyclones
C   noldstm           int            out    number of 12-hr old cyclones
C   idtg              int            out    dtg of cyclone data in "now"
C                                           ngtrp
C   slat              real           out    latitude of "now" cyclone
C   slon              real           out    longitude of "now" cyclone
C   smxv              real           out    maximum wind speed of "now"
C                                           cyclone
C   smr50             real           out    radius of 50 kt "now" winds
C   smr30             real           out    radius of 30 kt "now" winds
C   istmno            int            out    cyclone number of "now"
C                                           cyclone
C   ibsn              char           out    original basin of "now"
C                                           cyclone
C   idtgo             int            out    dtg of cyclone from 12-hr
C                                           old ngtrp file
C   olat              real           out    12-hr old cyclone latitude
C   olon              real           out    12-hr old cyclone longitude 
C   nstrm             int            out    12-hr old cyclone number
C   nobsn             char           out    original basin of 12-hr old
C                                           cyclone
C   
C COMMON BLOCKS:  none
C
C FILES:
C      Name        Unit    Type    Attribute  Usage       Description
C   ----------     ----  --------  --------- -------  ------------------
C    ngtrp         26     local    seq        in      "now" cyclone data
C    ngtrpo        27     local    seq        in      12-hr old cyclone
C                                                     data
C
C DATA BASES:  none
C
C NON-FILE INPUT/OUTPUT:  none
C
C ERROR CONDITIONS:  none
C
C ADDITIONAL COMMENTS:
C
C.................MAINTENANCE SECTION................................
C
C MODULES CALLED:  none
C
C LOCAL VARIABLES:
C         Name      Type                 Description
C        ------     ----       ----------------------------------
C
C METHOD:
C
C INCLUDE FILES:  none
C
C COMPILER DEPENDENCIES: FORTRAN 77
C
C COMPILE OPTIONS:
C
C MAKEFILE: /a/ops/met/nogaps/src/sub/tbog/tbog159lib.mak
C
C RECORD OF CHANGES:
C <<CHANGE NOTICE>> version 1.0 (12 Jan 1994) -- Pauley, R.
C   Initial installation under configuration management.
C
C <<CHANGE NOTICE>> version 1.3 (22 MAr 1995) -- Hamilton, H.
C   Add processing of 12-hr old ngtrp file data on unit 27
C   (adjust version # to agree with cm)
C
C..............................END PROLOGUE.............................
C
      dimension slat(nstms),slon(nstms),smxv(nstms),smr50(nstms)
     x ,smr30(nstms),istmno(nstms),ibsn(nstms)
     x, olat(nstms),olon(nstms),nstrm(nstms),nobsn(nstms)
c
c     character assignments
c
      character*1 ihemns,ihemew,ibsn,nobsn
      character*8 idtg,idtgo
c
c     read in the number of storms
c
      read(26,800,end=999) numbstm,idtg
c
c     if there are no storms, go to end
c
      if (numbstm.le.0) go to 999
c
c     if there are storms, make sure there are no more
c     than nstms and then input data
c
      if (numbstm .gt. nstms) numbstm = nstms
c
c     process data for all storms
c
      do 100 i=1,numbstm
      read(26,810) ilat,ihemns,ilon,ihemew,imaxv,istmno(i),ibsn(i)
     x  ,ir50,ir30
c
c     scale lat and lon
c
      slat(i)=float(ilat)*0.1
      slat(i)=abs(slat(i))
      slon(i)=float(ilon)*0.1
      if (ihemns.eq.'S') slat(i)=-slat(i)
      if (ihemew.eq.'W') slon(i)=360.0-slon(i)
c
c     convert max wind to m/s
c
      smxv(i)=float(imaxv)*0.5144
      smr50(i)=float(ir50)
      smr30(i)=float(ir30)
c
c     print storm position
c
      print 815,idtg
      print 820,istmno(i),ibsn(i),slat(i),slon(i),smxv(i),smr30(i)
  100 continue
c
c     read in the number of storms from 12-hour old ngtrp
c
      read(27,800,end=998) noldstm,idtgo
c
c     if there are no storms, go to end
c
      if (noldstm.le.0) go to 998
c
c     if there are storms, make sure there are no more
c     than nstms and then input data
c
      if (noldstm .gt. nstms) noldstm = nstms
c
c     process data for all storms
c
      do 200 i=1,noldstm
      read(27,810) ilat,ihemns,ilon,ihemew,imaxv,nstrm(i),nobsn(i)
c
c     scale lat and lon
c
      olat(i)=float(ilat)*0.1
      olat(i)=abs(olat(i))
      olon(i)=float(ilon)*0.1
      if (ihemns.eq.'S') olat(i)=-olat(i)
      if (ihemew.eq.'W') olon(i)=360.0-olon(i)
c
c     print storm position
c
      print 815,idtgo
      print 820,nstrm(i),nobsn(i),olat(i),olon(i)
  200 continue
c
c               NORMAL return
c
      return
c
c               ERROR returns follow
c
c
c     set noldstm to 0 if tape27 is blank
c
  998 continue
      noldstm = 0
      return
c
c     set numstm & noldstm to 0 if tape26 is blank
c
  999 continue
      numbstm = 0
      noldstm = 0
      return
c
c     format statements
c
  800 format(i1,2x,a8)
  810 format(i3,a1,1x,i4,a1,1x,i3,1x,i2,1x,a1,2x,i3,1x,i3)
  815 format(2x,' idtg is ',a8)
  820 format(' data for tropical storm ',i2,a1/
     1      ,' lat: ',f6.1,/
     2      ,' lon: ',f6.1,/
     3      ,' mxv: ',f6.1,' m/s'/
     4      ,' r30: ',f6.1,' nm')
      end
