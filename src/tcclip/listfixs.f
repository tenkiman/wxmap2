      program lstfix
C      (listfixs.f)
 
c  this program reads the jtwc fixes and lists them
c  in the format found in the atcr annex
 
      dimension fixes(750)
 
      character fixrecd*82
      character fixes*80,fixtyp*1,eyeshp*10,dvorak*20,flag*1,fl*6,
     &   hgt*4,mslp*4,fix*4,temp*15,wind*28,radpos*12,radacr*4,
     &   strmid*6,stmpth*18
      character*100 jtwc,outfil
      integer iarg
c ******************************************************************

c  get i/o files from cmd line (or shell script)
c  arg0=executable, arg1=strmid, arg2=jtwc, arg3=outfil
cajs  Use the following starting arg # when compiling with f77
cajs      iarg = 1
cajs  Use the following starting arg # when compiling with f90
      iarg = 2
      call getarg(iarg,strmid)
      iarg = iarg + 1
      call getarg(iarg,jtwc)
      iarg = iarg + 1
      call getarg(iarg,outfil)
      iarg = iarg + 1
cx      print*,'The current storm is:',strmid
cx      print*,'The input file 2 is:',jtwc
cx      print*,'The output file 8 is:',outfil
 
c  define unit numbers-
c  unit2 = jtwc fixes (jtwc)
c  unit5 = FORTRAN standard input (keyboard)
c  unit6 (or *) = FORTRAN standard output (terminal screen)
c  unit7 (or *) = FORTRAN standard error (screen or file) 
c  unit8 = atcr listing (outfil)
 
c  The following line is required for SCO-XENIX (LPI)
c  Dont use it with the HP-Fortran;
c      open (7, file='stderr')
c      inquire (file='stderr',number=num)
c      print*,'number associated with stderr is:',num
      open (7,file='listfixs.dbg',status='unknown',err=9020)
 
c  open input and output files
      open (2,file=jtwc,status='old',iostat=ios,err=9021)
      call openfile( 8, outfil, 'unknown', ioerror )
cajs      open (8,file=outfil,status='unknown')
 
c write the storm id on the top of the listing
      write (8,'(45x,''FIX POSITIONS FOR '',a6)') strmid
 
      nfixes = 1
  100 continue
      read (2,'(a82)',end=200) fixrecd
cajs   Assign fixes to be the old style record format,
c      with 2 digit vs 4 digit year.  10/98  ajs 
      fixes(nfixes)(1:3) = fixrecd(1:3)
      fixes(nfixes)(4:80) = fixrecd(6:82)
      nfixes = nfixes + 1
      goto 100
 
  200 continue
      nfixes = nfixes - 1
 
c  list satellite fixes
 
      write (8,1000)
      do 300 i=1,nfixes
      fixtyp = fixes(i)(1:1)
      if (fixtyp .eq. '1' .or. fixtyp .eq. 'A' .or. 
     &  fixtyp .eq. 'I')  then
          flag = ' '
          if (fixtyp .eq. 'A') flag = '*'
          if (fixes(i)(25:25) .ne. ' ') then
          dvorak = 'T' // fixes(i)(25:25) // '.' // fixes(i)(26:26)
     &  // '/' // fixes(i)(27:27) // '.' // fixes(i)(28:29) //
     &  '/' // fixes(i)(30:31) // '.' // fixes(i)(32:32) // '/' //
     &  fixes(i)(33:34) // 'HRS'
          else
             dvorak = '                    '
          endif
      if (fixes(i)(23:23) .ne. ' ') then
          write (8,1100) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &  fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &  fixes(i)(23:23),dvorak,fixes(i)(37:42),fixes(i)(43:43),
     &  fixes(i)(44:75),fixes(i)(76:79)
          else
          write (8,1200) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &  fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &  fixes(i)(24:24),dvorak,fixes(i)(37:42),fixes(i)(43:43),
     &  fixes(i)(44:75),fixes(i)(76:79)
          endif
      endif
  300 continue
 
c  list aircraft fixes
 
      write (8,2000)
      do 400 i=1,nfixes
      fixtyp = fixes(i)(1:1)
      if (fixtyp .eq. '2' .or. fixtyp .eq. 'B' .or. 
     &  fixtyp .eq. 'J')  then
          flag = ' '
          if (fixtyp .eq. 'B') flag = '*'
          if (fixes(i)(23:24) .ne. '  ') then
             fl = fixes(i)(23:24) // '00FT'
             hgt = '    '
          else
             fl = ' ' // fixes(i)(25:27) // 'MB'
             hgt = fixes(i)(28:31)
          endif
          if (fixes(i)(50:50) .eq. '9' .or. fixes(i)(50:50) 
     &       .eq. '8') then
             mslp = ' ' // fixes(i)(50:52)
          elseif (fixes(i)(50:50) .ne. ' ') then
             mslp = '1' // fixes(i)(50:52)
          else
             mslp = '    '
          endif
          eyeshp = fixes(i)(66:67)
          if (eyeshp(1:2) .eq. 'CI') eyeshp = 'CIRCULAR  '
          if (eyeshp(1:2) .eq. 'EL') eyeshp = 'ELLIPTICAL'
          if (eyeshp(1:2) .eq. 'CO') eyeshp = 'CONCENTRIC'
 
          temp = fixes(i)(53:55) // ' ' // fixes(i)(56:58) // ' ' //
     &           fixes(i)(59:61) // '  ' // fixes(i)(62:63)
          wind = fixes(i)(32:34) // ' ' // fixes(i)(35:36) // '0 ' //
     &           fixes(i)(37:39) // '  ' // fixes(i)(40:41) // '0 '
     &        // fixes(i)(42:44) // ' ' // fixes(i)(45:46) // '0 ' //
     &           fixes(i)(47:49)
          write (8,2100) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &  fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &  fl,hgt,mslp,wind,fixes(i)(74:75),fixes(i)(76:77),
     &  eyeshp,fixes(i)(70:71),fixes(i)(72:73),fixes(i)(68:69),
     &  temp,fixes(i)(78:79)
      endif
  400 continue
 
c  list radar fixes
 
      write (8,3000)
      do 500 i=1,nfixes
      fixtyp = fixes(i)(1:1)
      if (fixtyp .eq. '3' .or. fixtyp .eq. 'C' .or. 
     &  fixtyp .eq. 'K')  then
          flag = ' '
          if (fixtyp .eq. 'C') flag = '*'
          fix = fixes(i)(23:23)
          if (fix(1:1) .eq. 'L') fix = 'LAND'
          if (fix(1:1) .eq. 'S') fix = 'SHIP'
          if (fix(1:1) .eq. 'A') fix = 'AIRC'
          radpos = fixes(i)(66:67) // '.' // fixes(i)(68:69) // ' '
     &          // fixes(i)(70:72) // '.' // fixes(i)(73:74)
          radacr = fixes(i)(24:24)
          if (radacr(1:1) .ne. 'G' .and. radacr(1:1) .ne. 'F' .and.
     &        radacr(1:1) .ne. 'P') then
             write (8,3100) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &          fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &          fix,fixes(i)(24:28),fixes(i)(29:33),fixes(i)(34:65),
     &          radpos,fixes(i)(75:79)
          else
             if (radacr(1:1) .eq. 'G') radacr = 'GOOD'
             if (radacr(1:1) .eq. 'F') radacr = 'FAIR'
             if (radacr(1:1) .eq. 'P') radacr = 'POOR'
             eyeshp = fixes(i)(25:26)
             if (eyeshp(1:2) .eq. 'CI') eyeshp = 'CIRCULAR  '
             if (eyeshp(1:2) .eq. 'EL') eyeshp = 'ELLIPTICAL'
             if (eyeshp(1:2) .eq. 'CO') eyeshp = 'CONCENTRIC'
 
             write (8,3200) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &             fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &             fix,radacr,eyeshp,fixes(i)(27:29),fixes(i)(34:65),
     &             radpos,fixes(i)(75:79)
          endif
      endif
  500 continue
 
c  list synoptic fixes
 
      write (8,4000)
      do 600 i=1,nfixes
      fixtyp = fixes(i)(1:1)
      if (fixtyp .eq. '4' .or. fixtyp .eq. 'D' .or. 
     &  fixtyp .eq. 'L')  then
          flag = ' '
          if (fixtyp .eq. 'D') flag = '*'
          write (8,4100) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &  fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &  fixes(i)(23:25),fixes(i)(26:28),fixes(i)(29:79)
      endif
  600 continue
 
c  list scatterometer fixes
 
      write (8,4005)
      do 700 i=1,nfixes
      fixtyp = fixes(i)(1:1)
      if (fixtyp .eq. '5' .or. fixtyp .eq. 'E' .or. 
     &  fixtyp .eq. 'M')  then
          flag = ' '
          if (fixtyp .eq. 'E') flag = '*'
          write (8,4100) flag,i,fixes(i)(8:13),fixes(i)(14:15),
     &  fixes(i)(16:17),fixes(i)(18:20),fixes(i)(21:22),
     &  fixes(i)(23:25),fixes(i)(26:28),fixes(i)(29:79)
      endif
  700 continue
 
 1000 format (//50x,'SATELLITE FIXES',//
     &        ' NO.  TIME    FIX POSITION  ACCRY  DVORAK CODE',
     &        11x,'BIRD',7x,'COMMENTS',25x,'SITE',/)  
 1100 format (a1,i3,2x,a6,2x,a2,'.',a2,1x,a3,'.',a2,'  PCN ',a1,
     &        2x,a20,2x,a6,1x,a1,2x,a32,2x,a4)
 1200 format (a1,i3,2x,a6,2x,a2,'.',a2,1x,a3,'.',a2,' CONF ',a1,
     &        2x,a20,2x,a6,1x,a1,2x,a32,2x,a4)
 
 2000 format (//50x,'AIRCRAFT FIXES',//
     &       31x,'FLT  700MB  OBS  MAX-SFC-WND  MAX-FLT-LVL-WND',
     &       '  ACCRY      EYE      EYE ORIEN-    EYE TEMP (C)   MSN',/
     &       ' NO.  TIME    FIX POSITION     LVL   HGT  MSLP  VEL',
     &       '/BRG/RNG  DIR/VEL/BRG/RNG NAV/MET    SHAPE    DIAM/',
     &       'TATION   OUT/ IN/ DP/SST  NO.',/)
 2100 format (a1,i3,2x,a6,2x,a2,'.',a2,1x,a3,'.',a2,2x,a6,2x,a4,2x,a4,
     &        2x,a28,2x,a2,1x,a2,3x,a10,2x,a2,1x,a2,2x,a2,'0   ',a15,
     &        2x,a2)
 
 3000 format (//50x,'RADAR FIXES',//
     &  46X,'EYE      EYE     RADOB-CODE',40X,'RADAR',6X,'SITE',/
     &  ' NO.  TIME    FIX POSITION  RADAR  ACCRY     SHAPE     DIAM',
     &  '    ASWAR TDDFF   ',10X,'COMMENTS',16X,'POSITION',4X,'WMO NO.'
     &  ,/)
 3100 format (a1,i3,2x,a6,2x,a2,'.',a2,1x,a3,'.',a2,2x,a4,31x,a5,1x,
     &        a5,2x,a32,2x,a12,2x,a5)
 3200 format (a1,i3,2x,a6,2x,a2,'.',a2,1x,a3,'.',a2,2x,a4,3x,a4,4x,a10,
     &        3x,a3,17x,a32,2x,a12,2x,a5)
 
 4000 format (//50x,'SYNOPTIC FIXES',//
     &  29x,'INTENSITY  NEAREST',/
     &  ' NO.  TIME    FIX POSITION   ESTIMATE   DATA (NM)',
     &  20X,'COMMENTS',/)
 4005 format (//50x,'SCATTEROMETER FIXES',//
     &  29x,'INTENSITY  NEAREST',/
     &  ' NO.  TIME    FIX POSITION   ESTIMATE   DATA (NM)',
     &  20X,'COMMENTS',/)
 4100 format (a1,i3,2x,a6,2x,a2,'.',a2,1x,a3,'.',a2,4x,a3,6x,a3,2x,a32)
 
c      close(1)
      close(2)
      close(8)
      stop
 9020 continue
      print *, ' Error opening listfixs.dbg'
      stop
 9021 write (7,'(''Error 9021 in LISTFIXS.F - '',
     &  '' cant open jtwc fixes file: '',/,2x,a)') jtwc
       write (*,'(''LISTFIXS.F: cant open jtwc file:'',/,2x,a)')jtwc
      stop 1

      end
