      subroutine chkfcir (ddfld,fffld,ixgrd,jygrd,
     $     mni,mxi,mnj,mxj,nhsh,mxcc,
     &     cirdat,nccf)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)chkfcir.f	1.2 8/1/95
C                        16:16:06 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  chkfcir
C
C  DESCRIPTION:  determine approximate location of cyclonic
C                circulation(s) in both NH and SH
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
C  USAGE:  call chkfcir (ddfld,fffld,igrdx,jgrdy,mni,mxi,mnj,mxj,nhsh,mxcc,
C                        cirdat,nccf)
C
C  PARAMETERS:
C     NAME        TYPE        USAGE             DESCRIPTION
C   --------     -------      ------   ------------------------------
C    ddfld        real         in      global wind direction (to) field
C    fffld        real         in      global wind speed field
C    igrdx         int         in      first  dimension of ddfld
C    jgrdy         int         in      second dimension of ddfld
C      mni         int         in      first  dimension start of window
C      mxi         int         in      first  dimension end of window
C      mnj         int         in      second dimension start of window
C      mxj         int         in      second dimension end of window
C     nhsh         int         in      north/south hemisphere indicator
C     mxcc         int         in      maximum number of cyclonic
C                                      circulations (cc) allowed
C   cirdat        real         out     array for circulation data
C                                        (1,  first  dimension estimate
C                                        (2,  second dimension estimate
C                                        (3,  wind support factor
C     nccf         int         out     number of cc found
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
C    Name          Description
C   --------       -----------------------------------------------------
C   avgddt         calculate weighted average wind direction
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C         dde        real       wind direction at East-point
C         ddn        real       wind direction at North-point
C         dds        real       wind direction at South-point
C         ddw        real       wind direction at West-point
C         f1         real       fractional grid-length to "center line"
C         ichk        int       sum of winds within window
C         ixce        int       eastern-edge index
C         jycn        int       northern-edge index
C         jycs        int       southern-edge index
C         ixcw        int       western-edge index
C          rxc       real       approximate first  dimension location
C          ryc       real       approximate second dimension location
C
C  METHOD:  1.  Check wind direction at cardinal points about
C               central point.
C           2.  If 3 or 4 agree with cyclonic flow
C               assign cirdat sum of agreement.
C           3.  Replace duplicates when sum is 4.
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
C    Increase allowed cross flow by 15 degrees to better accommodate
C    1000 mb boundary layer flow
C
C...................END PROLOGUE.......................................
C
      implicit none
c
c         formal parameters
      integer ixgrd, jygrd, mni, mxi, mnj, mxj, nhsh, mxcc, nccf
      real ddfld(ixgrd,jygrd), fffld(ixgrd,jygrd), cirdat(4,mxcc)
c
c         local variables
      integer i, ii, im1, ip1, j, n, ixcw, ixce, jycs, jycn, ichk

      integer iskip

      logical verb

      logical warn

      real f1, ddn,dds,dde,ddw, rxc, ryc
c         real function
      real avgddt

      real diff1,diff2


      verb=.false.
      warn=.false.

      diff1=1.8
      diff2=1.1

ccc      diff1=diff1*0.5
ccc      diff2=diff2*0.5
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c         


      iskip=1
cc      iskip=2

      nccf = 0
      
      do j=mnj,mxj-iskip

        ryc =j+0.5
        jycs=j
        jycn=j+1

        jycs = j
        jycn = jycs + iskip
        ryc  = jycs*1.0 + (jycn-jycs)*0.5


        do ii=mni,mxi-iskip

c                   assume field is cyclic in first dimension
          i=ii
          if (i.lt.1) then
            i=ixgrd+i
          elseif (i.gt.ixgrd) then
            i=i-ixgrd
          endif

          ixcw = i
          ixce= ixcw + iskip

c--       bounds check, bail if outside the box


          if(  (ixcw.lt.1 .or. ixcw.gt.ixgrd) .or.
     $         (ixce.lt.1 .or. ixce.gt.ixgrd) ) then
            if(warn) print*,'EEEE search beyond grid in i...chkfcir...'
            nccf=0
            return
          endif

          if(  (jycs.lt.1 .or. jycs.gt.jygrd) .or.
     $         (jycs.lt.1 .or. jycn.gt.jygrd) ) then
            if(warn) print*,'EEEE search beyond grid in j...chkfcir...'
            nccf=0
            return
          endif


          rxc  = ixcw*1.0 + (ixce-ixcw)*0.5

          if (ixce.gt.ixgrd) ixce=ixce-ixgrd
c
c                   obtain wind directions north, south, west and east
c                   note, directions are to not from.
c
          f1 = rxc-i

c--       assume center halfway between corner points
          f1 = 0.5

          ddn = avgddt (ddfld(ixcw,jycn),ddfld(ixce,jycn),f1)
          dds = avgddt (ddfld(ixcw,jycs),ddfld(ixce,jycs),f1)
          f1 = ryc-j

c--       assume center halfway between corner points
          f1 = 0.5
          ddw = avgddt (ddfld(ixcw,jycs),ddfld(ixcw,jycn),f1)
          dde = avgddt (ddfld(ixce,jycs),ddfld(ixce,jycn),f1)

c                   check the type of flow pattern associated with
c                   this grid block

          ichk = 0
          if (nhsh .gt. 0) then

c         check for:  cyclonic circulation, nh

            if (ddn.ge.210.0 .and. ddn.le.315.0) ichk=1
            if (ddw.ge.120.0 .and. ddw.le.225.0) ichk=ichk+1
            if (dds.ge.030.0 .and. dds.le.135.0) ichk=ichk+1
            if ((dde.ge.000.0 .and. dde.le.045.0) .or.
     &          (dde.ge.300.0 .and. dde.le.360.0)) ichk=ichk+1

          else

c                                 cyclonic circulation, sh

            if (ddn.ge.045.0 .and. ddn.le.150.0) ichk=1
            if (dde.ge.135.0 .and. dde.le.240.0) ichk=ichk+1
            if (dds.ge.225.0 .and. dds.le.330.0) ichk=ichk+1
            if ((ddw.ge.000.0 .and. ddw.le.060.0) .or.
     &          (ddw.ge.315.0 .and. ddw.le.360.0)) ichk=ichk+1
          endif

          if(verb) then
            write(*,'(a,1x,6(i3,2x),2x,4(f8.2,1x),2x,a,i3)')
     $           'CCC: ddn dds dde ddw',
     $           ixcw,ixce,jycn,jycs,i,j,
     $           ddn,dds,dde,ddw,'ichk: ',ichk
            
          endif
          if (ichk.ge.3) then
c
c         cyclonic circulation found, see if this is a
c         new or "duplicate" circulation
c
            if (nccf.gt.0) then
              n = 0
              do while (ichk.gt.0.and.n.lt.nccf)
                n = n+1
                if (abs (cirdat(1,n)-rxc) .lt. diff1) then
                  if (abs (cirdat(2,n)-ryc) .lt. diff1) then
c
c                       "duplicate" found, keep 4 over 3
c
                    if (ichk.gt.nint(cirdat(3,n))) then
c                         replace old with new location
                      cirdat(1,n)=rxc
                      cirdat(2,n)=ryc
                      cirdat(3,n)=4.0
                    endif
                    ichk=0
                  endif
                endif
              enddo

              if (ichk.gt.0) then
c         new point was not absorbed above
                nccf=nccf +1
                if (nccf.lt.mxcc) then
c         add new cyclonic circulation
                  
                  cirdat(1,nccf)=rxc
                  cirdat(2,nccf)=ryc
                  cirdat(3,nccf)=ichk
                endif
              endif
            else
              nccf = 1
              cirdat(1,nccf)=rxc
              cirdat(2,nccf)=ryc
              cirdat(3,nccf)=ichk
            endif
          endif
        enddo
      enddo


      do j=mnj+1,mxj-1

        ryc=j

        do ii=mni+1,mxi-1

c                   assume field is cyclic in first dimension
          i = ii
          if (i .lt. 1) then
            i = ixgrd +i
          elseif (i .gt. ixgrd) then
            i = i -ixgrd
          endif

          ip1 = i + iskip
          if (ip1 .gt. ixgrd) ip1 = ip1 -ixgrd
          im1 = i - iskip
          if (im1 .lt. 1) im1 = ixgrd



c                   obtain wind directions north, south, west and east
c                   note, directions are to not from.

          ddn = ddfld(i,j+iskip)
          dds = ddfld(i,j-iskip)
          ddw = ddfld(im1,j)
          dde = ddfld(ip1,j)

c                   check the type of flow pattern associated with
c                   this grid block

          ichk = 0
          if (nhsh .gt. 0) then

c                     check for:  cyclonic circulation, nh

            if (ddn.ge.210.0 .and. ddn.le.315.0) ichk = 1
            if (ddw.ge.120.0 .and. ddw.le.225.0) ichk = ichk +1
            if (dds.ge.030.0 .and. dds.le.135.0) ichk = ichk +1
            if ((dde.ge.000.0 .and. dde.le.045.0) .or.
     &          (dde.ge.300.0 .and. dde.le.360.0)) ichk = ichk +1
          else

c                                 cyclonic circulation, sh

            if (ddn.ge.045.0 .and. ddn.le.150.0) ichk = 1
            if (dde.ge.135.0 .and. dde.le.240.0) ichk = ichk +1
            if (dds.ge.225.0 .and. dds.le.330.0) ichk = ichk +1
            if ((ddw.ge.000.0 .and. ddw.le.060.0) .or.
     &          (ddw.ge.315.0 .and. ddw.le.360.0)) ichk = ichk +1
          endif

          if (ichk .ge. 3) then

c                   cyclonic circulation found, see if this is a
c                   new or "duplicate" circulation

            rxc = i
            if (nccf .gt. 0) then
              n = 0
              do while (ichk.gt.0 .and. n.lt.nccf)
                n = n +1
                if (abs (cirdat(1,n) -rxc) .lt. diff2) then
                  if (abs (cirdat(2,n) -ryc) .lt. diff2) then
c
c                       "duplicate" found, keep 4 over 3
c
                    if (ichk .gt. nint (cirdat(3,n))) then
c                         replace old with new location
                      cirdat(1,n) = rxc
                      cirdat(2,n) = ryc
                      cirdat(3,n) = 4.0
                    endif
                    ichk = 0
                  endif
                endif
              enddo
              if (ichk .gt. 0) then
c                   new point was not absorbed above
                nccf = nccf +1
                if (nccf .lt. mxcc) then
c                       add new cyclonic circulation
                  cirdat(1,nccf) = rxc
                  cirdat(2,nccf) = ryc
                  cirdat(3,nccf) = ichk
                endif
              endif
            else
              nccf = 1
              cirdat(1,nccf) = rxc
              cirdat(2,nccf) = ryc
              cirdat(3,nccf) = ichk
            endif
          endif
        enddo
      enddo
      if (nccf .gt. 1) then
        write (33,*) 'CHKFCIR data check'
        do n=1, nccf
          write (33,*) n, cirdat(1,n), cirdat(2,n), cirdat(3,n)
        enddo
      endif
      return
c
      end
