      subroutine gettrp (nstms,numbstm,noldstm,idtg,slat,slon,svmax,spmin,
     &         smr50,smr30,istmno,ibsn,idtgo,umean,vmean,nstrm,nobsn)
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
C USAGE: call gettrp (nstms,numbstm,noldstm,idtg,slat,slon,svmax,smr50,
C                     smr30,istmno,ibsn, idtgo,umean,vmean,nstrm,nobsn)
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
C   svmax              real           out    maximum wind speed of "now"
C                                           cyclone
C   smr50             real           out    radius of 50 kt "now" winds
C   smr30             real           out    radius of 30 kt "now" winds
C   istmno            int            out    cyclone number of "now"
C                                           cyclone
C   ibsn              char           out    original basin of "now"
C                                           cyclone
C   idtgo             int            out    dtg of cyclone from 12-hr
C                                           old ngtrp file
C   umean              real           out    12-hr old cyclone latitude
C   vmean              real           out    12-hr old cyclone longitude 
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
      dimension slat(nstms),slon(nstms),svmax(nstms),spmin(nstms),smr50(nstms)
     x ,smr30(nstms),istmno(nstms),ibsn(nstms)
     x, umean(nstms),vmean(nstms),nstrm(nstms),nobsn(nstms)
c
c     character assignments
c
      character*1 ihemns,ihemew,ibsn,nobsn
      character*3 istmid
      character*8 idtg,idtgo
      character*10 cdtg

C1987090700 04L 030 1009  21.3 322.2  -99  -99 032.0 08.87 004.79 007.46

      i=0
      do while(i<10000)

        i=i+1

        read(26,602,end=100)
     $       cdtg,istmno(i),ibsn(i),
     $       imaxv,ipmin,slat(i),slon(i),ir50,ir30,
     $       rdir,rspd,umean(i),vmean(i)
 602    format(a,1x,i2,a1,1x,
     $       i3,1x,i4,2(f6.1),2i5,1x,
     $       f5.1,1x,f5.2,2f7.2)

        
        print*
        write(*,'(a,1x,i1,1x,a,1x,i02,1x,a,2x,8(f8.2,1x))')
     $       'TC # ',i,cdtg,istmno(i),ibsn(i),
     $       slat(i),slon(i),vmax,pmin,
     $       rdir,rspd,umean(i),vmean(i)
        print*
c
c     convert max wind and motion to m/s
c
        svmax(i)=float(imaxv)*0.5144
        spmin(i)=float(ipmin)
        smr50(i)=float(ir50)
        smr30(i)=float(ir30)
        umean(i)=umean(i)*0.5144
        vmean(i)=vmean(i)*0.5144
c
c     print storm position
c
        print 815,cdtg
 815    format(2x,' idtg is ',a10)
        print 820,istmno(i),ibsn(i),slat(i),slon(i),
     $       svmax(i),spmin(i),umean(i),vmean(i),
     $       smr50(i),smr30(i)
 820    format(' data for tropical storm ',i2,a1/
     1       ,' lat:   ',f6.1,/
     2       ,' lon:   ',f6.1,/
     3       ,' vmax:  ',f6.2,' m/s'/
     3       ,' pmin:  ',f6.0,' mb'/
     3       ,' umean: ',f6.1,' m/s'/
     3       ,' vmean: ',f6.1,' m/s'/
     4       ,' r50:   ',f6.1,' nm'/
     5       ,' r30:   ',f6.1,' nm')

      enddo

 100  continue
      numbstm=i-1

      idtg=cdtg(3:10)

      return
      end
