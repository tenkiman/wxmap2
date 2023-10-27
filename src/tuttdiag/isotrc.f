      subroutine isotrc (sfld,lfld,zblk)
C
C..........................START PROLOGUE..............................
C
C  SCCS IDENTIFICATION:  @(#)isotrc.f	1.1 12/15/94
C                        22:44:03 @(#)
C
C  CONFIGURATION IDENTIFICATION:
C
C  MODULE NAME:  isotrc
C
C  DESCRIPTION:  routine to trace isogons through field sfld via zoomed
C                grid blocks
C
C  COPYRIGHT:                  (C) 1994 FLENUMOCEANCEN
C                              U.S. GOVERNMENT DOMAIN
C                              ALL RIGHTS RESERVED
C
C  CONTRACT NUMBER AND TITLE:  GS-09K-90-BHD0001
C                              ADP SUPPORT FOR HIGHLY TECHNICAL SOFTWARE
C                              DEVELOPMENT FOR SCIENTIFIC APPLICATIONS
C
C  REFERENCES:  see isocnt for references
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
C  USAGE:  call isotrc (sfld,lfld,zblk)
C
C  PARAMETERS:
C     NAME         TYPE       USAGE             DESCRIPTION
C   --------      -------     ------   ------------------------------
C     sfld           real       in     field to be contoured
C     lfld        logical       in     field with contour flags set
C     zblk           real       in     working array for zooming
C
C  COMMON BLOCKS:              COMMON BLOCKS ARE DOCUMENTED WHERE THEY
C                              ARE DEFINED IN THE CODE WITHIN INCLUDE
C                              FILES.  THIS MODULE USES THE FOLLOWING
C                              VARIABLES IN NAMED BLOCKS:
C
C      BLOCK      NAME     TYPE    USAGE              NOTES
C     --------  --------   ----    ------   ------------------------
C        box      lbox      int     in    unit number for diagnostics
C                   xs     real     in    starting first dimension of
C                                         isogon box
C                   xl     real     in    ending first dimension of
C                                         isogon box
C                   ys     real     in    starting second dimension of
C                                         isogon box
C                   yl     real     in    ending second dimension of
C                                         isogon box
C
C       view      mini      int     in    starting first dim of box
C                 maxi      int     in    ending first dim of box
C                 minj      int     in    starting second dim of box
C                 maxj      int     in    ending second dim of box
C
C       isoc        rh     real     in    real value of isogon, deg
C                 iter      int     in    iteration number
C                  nc1      int    out    isogon count first  iteration
C                  nc2      int    out    isogon count second iteration
C
C       isol     first      log    out    flag, true if start
C                 last      log    out    flag, true if end
C                 open      log     in    flag, true if open contour
C               backwd      log     in    flag, true if backward contour
C
C      mndir        ii      int     in    starting minimum first dim of
C                                         contouring block
C                   jj      int     in    starting minimum second dim of
C                                         contouring block
C                   iv      int     in    starting first dim contour
C                                         direction vector
C                   jv      int     in    starting second dim contour
C                                         direction vector
C                  kkk      int    out    contour generation indicator
C
C     zoomv       kzlt      int     in    first  dim of zoomed block
C                 lzlt      int     in    second dim of zoomed block
C                 mbyn      int     in    length of sfld & lfld
C                   mi      int    out    starting minimum first dim of
C                                         contouring block
C                   mz      int     in    first dimension of sfld
C                   nj      int    out    starting minimum second dim of
C                                         contouring block
C                   nz      int     in    second dimension of sfld
C                 rint     real     in    first dim resolution of zoomed
C                                         block
C                 sint     real     in    second dim resolution of
C                                         zoomed block
C
C  FILES:  none
C
C  DATA BASES:  none
C
C  NON-FILE INPUT/OUTPUT:  none
C
C  ERROR CONDITIONS:
C         CONDITION                       ACTION
C     -----------------             ----------------------------
C     bad interpolation             error diagnostic and exit
C     no start-point in block       error diagnostic and exit
C     too many contour points       error diagnostic and exit
C
C  ADDITIONAL COMMENTS:
C     No closed contours are allowed - some code commented out
C
C...................MAINTENANCE SECTION................................
C
C  MODULES CALLED:
C          NAME           DESCRIPTION
C         -------     ----------------------
C         calint      calculate intersection of two isogons
C         isovzm      zoom grid square values into zblk
C
C  LOCAL VARIABLES:
C          NAME      TYPE                 DESCRIPTION
C         ------     ----       ----------------------------------
C             hc     real       value of contour being contoured
C           ierr      int       interpolation flag, 0 no error
C          ijtoi      int       two dimension to one dimension function
C            ija      int       single index of point a
C            ijb      int       single index of point b
C            ijc      int       single index of point c
C            ijo      int       single index of point o
C             ka      int       first dim of point a in block
C             kb      int       first dim of point b in block
C             kc      int       first dim of point c in block
C             kf      int       first dim of point f in block
C            klt      int       temp storage
C             kv      int       first dim vector in block
C             la      int       second dim of point a in block
C             lb      int       second dim of point b in block
C             lc      int       second dim of point c in block
C             lf      int       second dim of point f in block
C             lv      int       second dim vector in block
C            mim      int       mi -1
C            mip      int       mi +1
C            njm      int       nj -1
C            njp      int       nj +1
C           nval      int       number of points in contour
C         nxylmt      int       error flag, 0 no error
C              t     real       grid length fraction
C            xus     real       x-grid point values of contour
C            yus     real       y-grid point values of contour
C             za     real       "height" value at point a
C             zb     real       "height" value at point b
C             zc     real       "height" value at point c
C             zf     real       "height" value at point f
C
C  METHOD:  see isocnt method and reference
C
C  INCLUDE FILES:
C             NAME              DESCRIPTION
C          ----------     ----------------------------------------------
C            box.inc      common block
C           isoc.inc      common block
C           isol.inc      common block
C          isoxy.inc      common block
C          mndir.inc      common block
C           view.inc      common block
C          zoomv.inc      common block
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
c
      implicit none
c
      integer ncnt
      parameter (ncnt = 51)
c
      INCLUDE 'zoomv.inc'
c
      logical lfld(mbyn)
      real sfld(mz,nz), zblk(kzlt,lzlt)
c
      integer ijtoi, i, j, ka, la, ierr, kv, lv, nt, n, kf, lf, njp
      integer ija, ijo, ijb, ijc, nval, kb, lb, klt, kc, lc
      integer mim, njm, mip, nn, nxylmt
      real hc, zf, za, t, zb, zc
      real xus(ncnt), yus(ncnt)
c
      INCLUDE 'view.inc'
c
      INCLUDE 'box.inc'
c
      INCLUDE 'isol.inc'
c
      INCLUDE 'isoc.inc'
c
      INCLUDE 'mndir.inc'
c
      INCLUDE 'isoxy.inc'
c
      data hc/0.0/
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c         integer function:
      ijtoi(i,j) = (j -1)*mz +i
c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
c
c              initialize conturing variables
c                     mi  i-value in sfld of lower left point
c                     nj  j-value in sfld of lower left point
c                     ka  k-value in grid point block of point a
c                     la  l-value in grid point block of point a
c
      mi = ii
      nj = jj
      if (.not. backwd) then
        if (iv .eq. -1) then
          mi = mi -1
          ka = 1
          la = 1
        elseif (jv .eq. -1) then
          mi = mi -1
          nj = nj -1
          ka = kzlt
          la = 1
        elseif (iv .eq. 1) then
          nj = nj -1
          ka = kzlt
          la = lzlt
        elseif (jv .eq. 1) then
          ka = 1
          la = lzlt
        endif
c
      else
        if (iv .eq. 1) then
          ka = kzlt
          la = 1
        elseif (jv .eq. 1) then
          mi = mi -1
          ka = kzlt
          la = lzlt
        elseif (iv .eq. -1) then
          mi = mi -1
          nj = nj -1
          ka = 1
          la = lzlt
        elseif (jv .eq. -1) then
          nj = nj -1
          ka = 1
          la = 1
        endif
      endif
c
c              remove flag set in subroutine isocnt
      lfld(ijtoi(ii,jj)) = .false.
c
c                   zoom grid into zblk
      call isovzm (sfld,zblk,ierr)
      if (ierr .ne. 0) then
        write (33,*) ' $$$ isotrc, initial mi ',mi,' nj ',nj,
     .                 ' out of bounds'
        goto 300
c
      endif
c
c              determine start point of contour in grid block
      kv = iv
      lv = jv
      nt = kzlt -1
      do n=1, nt
        kf = ka -kv
        lf = la -lv
        if (zblk(ka,la).lt.hc  .and.  zblk(kf,lf).ge.hc) goto 120
c
        ka = kf
        la = lf
      enddo
      write (33,9010) hc, kf, lf
 9010 format (' $$$$$ no start point for contour ',g11.5,2(2x,i3))
      njp = nj +1
      write (33,9020) mi,njp, mi+1,njp, mi,nj, mi+1,nj
 9020 format (1x,'c ',i2,',',i3,5x,'b ',i2,',',i3,/,
     .        1x,'a ',i2,',',i3,5x,'o ',i2,',',i3)
      ija = ijtoi (mi,nj)
      ijo = ijtoi (mi+1,nj)
      ijb = ijtoi (mi+1,njp)
      ijc = ijtoi (mi,njp)
      write(33,9030) lfld(ijc),sfld(mi,njp), lfld(ijb),sfld(mi+1,njp)
      write(33,9030) lfld(ija),sfld(mi,nj),  lfld(ijo),sfld(mi+1,nj)
 9030 format (1x,l1,2x,g11.5,5x,l1,2x,g11.5)
      goto 300
c
  120 continue
c
c              initialize starting values
      first = .true.
      last  = .false.
      nval  = 1
      zf    = zblk(kf,lf)
      za    = zblk(ka,la)
c                   find first point of contour
      t = 0.0
      if (zf .ne. za) t = (zf -hc)/(zf -za)
      xus(1) = mi +rint*((kf -1) +t*kv)
      yus(1) = nj +sint*((lf -1) +t*lv)
ccc   if (.not. open) then
c                   save starting location
ccc     mif  = mi
ccc     njf  = nj
ccc     xusf = xus(1)
ccc     yusf = yus(1)
ccc   endif
c
  200 continue
      if (.not. backwd) then
c                   initialize values for forward trace
        kb = kf +lv
        lb = lf -kv
        zb = zblk(kb,lb)
        if (zb .lt. hc) then
c                      turn right
          za  =  zb
          klt =  kv
          kv  =  lv
          lv  = -klt
c
        else
          kc = kf +kv +lv
          lc = lf +lv -kv
          zc = zblk(kc,lc)
          if (zc .lt. hc) then
c                        go straight ahead
            zf = zb
            za = zc
            kf = kf +lv
            lf = lf -kv
          else
c                        turn left
            zf  =  zc
            kf  =  kc
            lf  =  lc
            klt =  lv
            lv  =  kv
            kv  = -klt
          endif
        endif
c
      else
c                   initialize values for backward trace
        kb = kf -lv
        lb = lf +kv
        zb = zblk(kb,lb)
        if (zb .lt. hc) then
c                      turn left
          za  =  zb
          klt =  kv
          kv  = -lv
          lv  = klt
c
        else
          kc = kf +kv -lv
          lc = lf +kv +lv
          zc = zblk(kc,lc)
          if (zc .lt. hc) then
c                        go straight
             zf = zb
             za = zc
             kf = kf -lv
             lf = lf +kv
c
          else
c                        turn right
            zf  =  zc
            kf  =  kc
            lf  =  lc
            klt =  lv
            lv  = -kv
            kv  =  klt
          endif
        endif
      endif
c
c             interpolate for next location of contour
      t = 0.0
      if (zf .ne. za)  t = (zf -hc)/(zf -za)
      nval = nval +1
      if (nval .gt. ncnt) then
        write (33,*) ' isotrc, aborting - too many one block points'
        nc1 = 0
        nc2 = 0
        goto 300
c
      endif
      xus(nval) = mi +rint*((kf -1) +t*kv)
      yus(nval) = nj +sint*((lf -1) +t*lv)
c
c              check to see if edge of zoomed block has been reached
c
      if (lv .eq. 0) then
        if (lf.gt.1 .and. lf.lt.lzlt) goto 200
c
      else
        if (kf.gt.1 .and. kf.lt.kzlt) goto 200
c
      endif
  210 continue
c
c                   determine if contour is finished and
c                   if contouring continuing,
c                   location of next block to be zoomed.
c
      if (.not.backwd) then
c
c                   setup forward contouring values
c
        if (kv .eq. -1) then
          njp = nj +1
          if (njp .ge. maxj) then
            last = .true.
          else
            nj = njp
            lf = 1
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi+1,nj)) = .false.
c
c                   determine if closed contour is finished
c
ccc         if (.not.open .and. mi.eq.mif .and. nj.eq.njf) then
ccc           last      = .true.
ccc           nval      = nval +1
ccc           xus(nval) = xusf
ccc           yus(nval) = yusf
ccc         endif
          endif
        elseif (lv .eq. -1) then
          mim = mi -1
          if (mim .lt. mini) then
            last = .true.
          else
            mi = mim
            kf = kzlt
          endif
        elseif (kv .eq. 1) then
          njm = nj -1
          if (njm .lt. minj) then
            last = .true.
          else
            lf = lzlt
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi,nj)) = .false.
            nj = njm
          endif
        elseif (lv .eq. 1) then
          mip = mi +1
          if (mip .ge. maxi) then
            last = .true.
          else
            mi = mip
            kf = 1
          endif
        endif
c
      else
c                   setup backward contouring values
        if (kv .eq. 1) then
          njp = nj +1
          if (njp .ge. maxj) then
            last = .true.
          else
            nj = njp
            lf = 1
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi,nj)) = .false.
c
c                   determine if closed contour is finished
c
ccc         if (.not.open .and. mi.eq.mif .and. nj.eq.njf) then
ccc           last      = .true.
ccc           nval      = nval +1
ccc           xus(nval) = xusf
ccc           yus(nval) = yusf
ccc         endif
          endif
        elseif (lv .eq. 1) then
          mim = mi -1
          if (mim .lt. mini) then
            last = .true.
          else
            mi = mim
            kf = kzlt
          endif
        elseif (kv .eq. -1) then
          njm = nj -1
          if (njm .lt. minj) then
            last = .true.
          else
            nj = njm
            lf = lzlt
c                   remove flag set in subroutine isocnt
            lfld(ijtoi(mi+1,nj+1)) = .false.
          endif
        elseif (lv .eq. -1) then
          mip = mi +1
          if (mip .ge. maxi) then
            last = .true.
          else
            mi = mip
            kf = 1
          endif
        endif
      endif
c
c                   output contour points for one block
c
      write (33,*) 'isotrc, nval ',nval,' ncnt ',ncnt,' last ',last
      if (first) then
        nn     = 0
        nxylmt = 0
      endif
      do n=1, nval
        if (xus(n).ge.xs .and. xus(n).le.xl .and. yus(n).ge.ys .and.
     .      yus(n).le.yl) then
          if (iter .eq. 1) then
            if (nn .eq. 0) then
              nn     = 1
              xx1(1) = xus(n)
              yy1(1) = yus(n)
            else
              if (xus(n).ne.xx1(nn) .and. yus(n).ne.yy1(nn)) then
                nn = nn +1
                if (nn .le. npts) then
                  xx1(nn) = xus(n)
                  yy1(nn) = yus(n)
                else
                  nxylmt = -1
                endif
              endif
            endif
          else
            if (nn .eq. 0) then
              nn     = 1
              xx2(1) = xus(n)
              yy2(1) = yus(n)
            else
              if (xus(n).ne.xx2(nn) .and. yus(n).ne.yy2(nn)) then
                nn = nn +1
                if (nn .le. npts) then
                  xx2(nn) = xus(n)
                  yy2(nn) = yus(n)
                else
                  nxylmt = -1
                endif
              endif
            endif
          endif
        endif
      enddo
      first = .false.
      nval  = 0
      if (nxylmt .lt. 0) then
        write (33,*) ' $$$$ isotrc, too many total pts ',nn
        last = .true.
      endif
  240 continue
      if (last) then
        if (iter .eq. 1) then
          nxy1 = min0 (nn,npts)
          nc1  = nxy1
          rh1  = rh
          kkk  = kkk +1
        else
          nxy2 = min0 (nn,npts)
          nc2  = nxy2
          rh2  = rh
          kkk  = kkk +1
          if (nxy1.gt.1 .and. nxy2.gt.1) then
            call calint
          else
            write (33,*) ' isotrc, no calint for ',rh1,'  ',rh2
            nc2 = 0
          endif
        endif
      else
c                   zoom grid into zblk
        call isovzm (sfld,zblk,ierr)
c                   jump to continue isogon
        if (ierr .eq. 0) goto 200
c
        write (33,*) ' $$$ isotrc, mi ',mi,' nj ',nj,
     .                 ' driven out of bounds'
        last = .true.
        goto 240
c
      endif
  300 continue
      return
c
      end
