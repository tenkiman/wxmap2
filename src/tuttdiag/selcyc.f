      subroutine selcyc (sgxx,sgyy,egxx,egyy,
     $     igrdx,jgrdy,
     $     blat,blon,dlat,dlon,
     $     cirdat,nccf,
     &     fffld,ixgd,jygd,konf,indx)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)selcyc.f	1.2 8/1/95
C                        16:16:16 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  selcyc
C
C  DESCRIPTION:  driver routine for finding which tropical cyclone
C                is best prospect
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
C  USAGE:  call selcyc (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,jygd,
C                       konf,indx)
C
C  PARAMETERS:
C     NAME      TYPE    USAGE           DESCRIPTION
C   --------   -------  -----   ------------------------------
C     sgxx      real     in     last known x-location of cyclone
C     sgyy      real     in     last known y-location of cyclone
C     egxx      real     in     extrapolated x-location of cyclone
C     egyy      real     in     extrapolated y-location of cyclone
C   cirdat      real     in     circulation data
C                                 (1, first  dimension location
C                                 (2, second dimension location
C                                 (3, wind support factor, 3 or 4
C                                 (4, intersection support, 2 - 8
C     nccf       int     in     number of cyclonic circulations
C    fffld      real     in     wind speed squared (m/s)**2
C     ixgd       int     in     first  dimension of fffld
C     jygd       int     in     second dimension of fffld
C     konf       int     out    confidence factor
C     indx       int     out    index to cirdat of selected cc
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
C        NAME           DESCRIPTION
C       -------     ----------------------
C       sortem2     sort prospective data based upon distance from last
C                   know location and from extrapolated location, and
C                   on maximum wind speed near each cyclonic center
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C          edist     real       distance from extrapolated position
C          jptsp      int       pointer array, last known location
C          kptep      int       pointer array, extrtapolated position
C          lptwd      int       pointer array, wind speed
C          sdist     real       distance from last known location
C          wind      real       maximum wind speed
C          wndmx     real       array of maximum wind speeds
C
C  METHOD:  1)  Load pointer arrays, calculate distance values, load
C               wind speed array and then sort distance arrays (least
C               to most) and wind speed array (most to least) by calling
C               sortem2.
C           2)  Based upon the information in these sorted arrays,
C               select the best index to the cyclones found to represent
C               the cyclone being tracked.  Set confidence factor to
C               represent the goodness of the selection.
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
C    Add wind speed as a selection parameter.
C
C...................END PROLOGUE.......................................
C
      implicit none

      integer maxptc
      parameter (maxptc = 27)
c
c         formal parameters
      integer nccf, ixgd, jygd, konf, indx

      integer i,j,k,n,ierr


      real slat,slon,flat,flon
      real shead,sspd,ehead,espd

      real sgxx, sgyy, egxx, egyy
      real cirdat(4,nccf), fffld(ixgd,jygd)
      real tmpcirdat(4,nccf)

      real curhead,curdist

      real latminspd,headminspd

      real tclat(maxptc),tclon(maxptc),
     $     tchead(maxptc),tcdist(maxptc),
     $     dtchead(maxptc),dtcdist(maxptc),
     $     dum(maxptc)

      integer igrdx,jgrdy
      real blat,blon,dlat,dlon

      integer ntcok,nok

      integer tccheck(maxptc)

      logical verb
c
c         local variables
c                   pointer arrays
      integer jptsp(nccf), kptep(nccf), lptwd(nccf)
c                   distance arrays (d squared)
      real sdist(nccf), edist(nccf)
c                   wind speed max at grid point near cc
      real wndmx(nccf)
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .


      verb=.true.
      verb=.false.


C         mf 20010920 -- 
C         preselect check for anamolous motion 
C         hard  turns > headminspd for lat > latminspd
C         

      latminspd=30.0
      headminspd=120.0

ccc      call cxytll (sgxx,sgyy,slat,slon,ierr)
      call cxytll (sgxx,sgyy,
     $     blat,blon,dlat,dlon,igrdx,jgrdy,
     $     slat,slon,
     $     ierr)


ccc      call cxytll (egxx,egyy,flat,flon,ierr)
      call cxytll (egxx,egyy,
     $     blat,blon,dlat,dlon,igrdx,jgrdy,
     $     flat,flon,
     $     ierr)


      call rcalhdst (slat,slon,flat,flon,curhead,curdist)

      if(verb)
     $     write(*,'(a,2x,2(f7.2,1x))') 
     $     'PREselcyc TC Cur Motion  :',curhead,curdist

      ntcok=0

      do n=1,nccf
        tccheck(n)=0

cccc        call cxytll (cirdat(1,n),cirdat(2,n),tclat(n),tclon(n),ierr)
        call cxytll (cirdat(1,n),cirdat(2,n),
     $     blat,blon,dlat,dlon,igrdx,jgrdy,
     $     tclat(n),tclon(n),
     $     ierr)


        call rcalhdst (slat,slon,tclat(n),tclon(n),tchead(n),tcdist(n))

        if( abs(curhead-tchead(n)).ge.180.0 ) then
          dtchead(n)=360.0-abs(curhead-tchead(n))
        else
          dtchead(n)=abs(curhead-tchead(n))
        endif
        if( (abs(slat).ge.latminspd) .and. 
     $       (dtchead(n).ge.headminspd) ) then
          tccheck(n)=1
        else
          ntcok=ntcok+1
        endif

        if(verb)
     $       write(*,'(a,2x,i2,2x,3(f7.2,1x),2x,i1)') 
     $       'PREselcyc heading check  :',
     $       n,dtchead(n),curhead,tchead(n),tccheck(n)

      end do

C         
C...      if one or more TCs pass the heading check then toss
C...      the questionable posits and reset the # of cyclones (nccf)
C...      otherwise, let the scheme operate
C

      if(ntcok.ge.1) then

        if(verb) then
          do n=1,nccf
            write(*,('(a,4(f7.2,1x))'))
     $           'BEFORE: ',(cirdat(i,n),i=1,4)
          end do
        endif

        nok=0
        do n=1,nccf
          if(tccheck(n).eq.0) then
            nok=nok+1
            do i=1,4
              tmpcirdat(i,nok)=cirdat(i,n)
            end do
          end if
        end do

        do n=1,ntcok
          do i=1,4
            cirdat(i,n)=tmpcirdat(i,n)
          end do
        end do

        nccf=ntcok

        if(verb) then
          do n=1,nccf
            write(*,('(a,4(f7.2,1x))'))
     $           'AFTER: ',(cirdat(i,n),i=1,4)
          end do
        endif

      endif

c
c                   load pointer, distance and wind speed arrays
c
      call sortem2 (sgxx,sgyy,egxx,egyy,cirdat,nccf,fffld,ixgd,jygd,
     &     jptsp,kptep,lptwd,sdist,edist,wndmx)

c
c                   select index to cyclone location
c
      if (jptsp(1).eq.kptep(1) .and. jptsp(1).eq.lptwd(1)) then
c
c                   pick cyclone which is minimum distance to both
c                   last known location and estimated position,
c                   and has max wind speed
c
        indx = jptsp(1)
        konf = 2
      elseif (sdist(jptsp(1)) .lt. edist(kptep(1)) .and.
     &        cirdat(3,jptsp(1)) .gt. 3.5 .and.
     &        cirdat(4,jptsp(1)) .gt. 4.5 .and.
     &        wndmx(jptsp(1)) .ge. wndmx(kptep(1))) then
c
c                  pick cyclone closer to last known position,
c                  if it has good wind support
c
        indx = jptsp(1)
        konf = 3
      elseif (edist(kptep(1)) .le. sdist(jptsp(1)) .and.
     &        cirdat(3,kptep(1)) .gt. 3.5 .and.
     &        cirdat(4,kptep(1)) .gt. 4.5 .and.
     &        wndmx(kptep(1)) .ge. wndmx(jptsp(1))) then
c
c                  pick cyclone closer to estimated position,
c                  if it has good wind support
c
        indx = kptep(1)
        konf = 3
      elseif (cirdat(3,jptsp(1)) .ge. cirdat(3,kptep(1)) .and.
     &        cirdat(4,jptsp(1)) .ge. cirdat(4,kptep(1)) .and.
     &        wndmx(jptsp(1)) .ge. wndmx(kptep(1))) then
c
c                   pick cyclone closest to the start position,
c                   if it has the best wind and intersection support
c
        indx = jptsp(1)
        konf = 4
        elseif (cirdat(3,kptep(1)) .ge. cirdat(3,jptsp(1)) .and.
     &          cirdat(4,kptep(1)) .ge. cirdat(4,jptsp(1)) .and.
     &          wndmx(kptep(1)) .ge. wndmx(jptsp(1))) then
c
c                   pick cyclone closest to estimated position,
c                   if it has the best wind and intersection support
c
        indx = kptep(1)
        konf = 4
      elseif (wndmx(jptsp(1)) .gt. wndmx(kptep(1))) then
c
c                  pick cyclone closest to last known position,
c                  if wind speed is greater
c
        indx = jptsp(1)
        konf = 5
      elseif (wndmx(kptep(1)) .gt. wndmx(jptsp(1))) then
c
c                  pick cyclone closest to estimated position,
c                  if wind speed is greater
c
        indx = kptep(1)
        konf = 5
      else
c
c                  pick cyclone with highest wind speed
c
        indx = lptwd(1)
        konf = 6
      endif

      return
c
      end
