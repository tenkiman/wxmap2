      subroutine phase(ifl,u,v,us,vs)

      parameter  (nx=25)

      include 'params.h'

      logical verb

cc****************************************************************
cc        
cc        this subroutine creates  filtered  fields of (u,v) wind
cc        
cc        
cc****************************************************************
cc        
cc***************************************************************
cc        important!!!
cc        we assume that the spacing of all the points is one degree
cc        latitude and longitude.
cc        
cc        
cc        ifl = the strength of the filter varying from 1 (weak damping) to
cc        4 (very strong damping). we are currently using ifl=2.
cc        thus there are 4 choices for the type of filter desired,
cc        ifl = 1, 2, 3, or 4.
cc        
cc        
cc        u,v      =  input of the unsmoothed fields                      *
cc        
cc        ni = number of input and output points in x-direction
cc        nj = number of input and output points in y-direction
cc        
cc        us,vs   =  output of the smoothed fields                       *
cc        
cc**********************************************************************

      dimension  u(ni,nj), v(ni,nj)
      dimension  us(ni,nj),vs(ni,nj)

      dimension  tk(nx),ampf(100)

      dimension  xtu(ni,nx),xtv(ni,nx)
      dimension  ytu(nj,nx),ytv(nj,nx)

      verb=.false.
      
      nim  = ni-1
      njm  = nj-1

      tn = float(nx)

      pi = 4.*atan(1.0)
      cosf = cos(2.*pi/tn) - 1.0
cc        
cc        *************************************************************
cc        
cc        ...ifl...  will control the extent of damping requested
cc        
cc        ifl is determined in the program test at the beginning
cc        
cc        
cc        ...nty...  is the number of passes through the smoothing operator
cc        

      if(ifl.eq.1) nty = 8
      if(ifl.eq.2) nty = 11
      if(ifl.eq.3) nty = 17
      if(ifl.eq.4) nty = 24

cc**************************************************************
cc        
cc        ismth: is the parameter to turn on des-smoothing. we will always asssume
cc        desmoothing is unnecessary. however it is still in the code for
cc        the purpose of generalization.
cc        
      ismth = 0
cc        
cc**********************************************************************
cc        
cc        
cc        
cc        next we will determine the smoothing parameter k to be used
cc        during each of n passes through the smoothing operation.
cc        
cc        (see the appendix of kurihara et al., from the monthly weather
cc        review article, 1990 .....equation a2).
cc        
cc        
      chg = 0.0
      kt = 0
cc        
cc        
cc        
      do 802 kty = 1 , nty
cc        
cc        
ccxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cc        
cc        
cc        filter 1...weak filter.....
cc        
cc        n = 8 .... and m varies as 2,3,4,2,5,6,7,2
cc        
cc        
        if((kty.eq.4.or.kty.eq.8).and.ifl.eq.1)chg = 1.0
cc        
cc        
ccxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cc        
cc        filter 2....regular filter.....currently in use
cc        
cc        n = 11 .... and m varies as 2,3,4,2,5,6,7,2,8,9,2
cc        
cc        
        if((kty.eq.4.or.kty.eq.8.or.kty.ge.11)
     *       .and.ifl.eq.2)chg = 1.0
cc        
cc        
ccxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cc        
cc        filter 3....strong filter.....effective for hurricane gilbert
cc        
cc        n = 17 .... and m varies as 2,3,4,2,5,6,7,2,8,9,10,2,11,2,2,2,2
cc        
cc        
        if((kty.eq.4.or.kty.eq.8.or.kty.eq.12.or.kty.ge.14.)
     *       .and.ifl.eq.3)chg = 1.0
cc        
cc        
ccxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cc        
cc        
cc        filter 4.....very strong filter....the pattern will start to beco
cc        
cc        
cc        
cc        n = 24.......and m varies as :
cc        2,3,4,2,5,6,7,2,8,9,10,2,11,12,13,2,2,2,2,2,2,2,2,2
cc        
cc        
cc        
        if((kty.eq.4.or.kty.eq.8.or.kty.eq.12
     *       .or.kty.ge.16).and.ifl.eq.4)chg = 1.0
cc        
cc        
cc        
cc**********************************************************************
cc        
cc        
        if(chg.eq.0)kt = kt + 1
        if(chg.eq.1.0)tk(kty) = .25
        if(chg.eq.1.0)go to 801
        fact = 2.0*pi/(float(kt) + 1.0)
        tk(kty) = -.5/(cos(fact) - 1.0)

        if(verb)  write (6,'(2i5,3f7.2)') kty,kt,chg,fact,tk(kty)

        do 679 na = 2 , 25
          ampf(na) = 1 + 2.*tk(kty)*(cos(2.*pi/float(na)) - 1.0)
 679    continue
 801    continue
        chg = 0.0
 802  continue

      if(verb) then
        write(6,815) (tk(kk),kk = 1 , nty)
 815    format(2x,'this is tk:',e12.6)
      endif

cc        
cc**********desmoothingis set up if needed********************
cc        
      if(ismth.eq.1)then

        ntym = nty - 1
        tff = 1.0
        do 61 k = 1 , ntym
          tff = tff*(1. + 2.*tk(k)*cosf)
 61     continue
        tfr = 1./tff
        tk(nty) = (tfr - 1.0)/(2.*cosf)
        if(verb) then
          write(6,816) tk(nty)
 816      format(2x,'the desmoothing constant',e12.6)
        endif

      endif
cc        
c***********printout the damping characteristics***************

      irt = kt+1
      
      do nz=2,40

        amp = 1.0
        tnn = float(nz)
        ckg = 0.0
        if(nz.gt.irt) ckg=1.0

        do kt = 1 , nty
          amp1 = (1. + 2*tk(kt)*(cos(2.*pi/tnn)-1.0))
          if(ckg.eq.0.0) go to 619
          amp =  amp1*amp
 619      continue
          if(abs(amp1) .lt. 0.01) ckg = 1.0
        end do

        amm = amp
        if(nz.le.irt)amm=0.0

        zz = float(nz)

CC         write(11,455)zz,amm
CC 455    format(f8.3,f8.3)
cc        
cc        
cc        
cc        the following write statement will let you know the amount of the
cc        wave that has remained after the filtering,
cc        for the wave of a given length d (which is currently one degree)
cc        

        if(verb.and.(nz.eq.20.or.nz.eq.30.or.nz.eq.40)) then
          write(6,677) nz,amm
 677      format(2x,'wave number',i5,2x,'percent wave remaining: ',e12.6)
        endif
        
      end do
cc*******************************************************************
cc        
cc        do the smoothing in the latitudinal direction:
cc        (equation a1)
cc        

      do j=1,nj

        do nn = 1 , nty
          xtu(1,nn)   = u(1,j)
          xtu(ni,nn) = u(ni,j)
          xtv(1,nn)   = v(1,j)
          xtv(ni,nn) = v(ni,j)
        end do

        do i = 2 , nim
          xtu(i,1) = u(i,j)   + tk(1)*(u(i-1,j) +
     *         u(i+1,j) - 2.*u(i,j))
          xtv(i,1) = v(i,j)   + tk(1)*(v(i-1,j) +
     *         v(i+1,j) - 2.*v(i,j))
        end do

        do  nn=2,nty
          do  i=2,nim
            xtu(i,nn) = xtu(i,nn-1) + tk(nn)*(xtu(i-1,nn-1) +
     $           xtu(i+1,nn-1) - 2.*xtu(i,nn-1))
            xtv(i,nn) = xtv(i,nn-1) + tk(nn)*(xtv(i-1,nn-1) +
     $           xtv(i+1,nn-1) - 2.*xtv(i,nn-1))
          end do
        end do

        do i=1,ni
          us(i,j)=xtu(i,nty)
          vs(i,j)=xtv(i,nty)
        end do
      end do


cc********************************************************************
cc        
cc        now do the smoothing in the meridional direction:
cc        (equation a3)
cc        
cc        

      do i=1,ni

        do nn=1,nty
          ytu(1,nn)   = us(i,1)
          ytu(nj,nn) = us(i,nj)
          ytv(1,nn)   = vs(i,1)
          ytv(nj,nn) = vs(i,nj)
        end do
        
        do j=2,njm
          ytu(j,1) = us(i,j) + tk(1)*(us(i,j-1) + us(i,j+1)
     $         -2.*us(i,j))
          ytv(j,1) = vs(i,j) + tk(1)*(vs(i,j-1) + vs(i,j+1)
     $         -2.*vs(i,j))
        end do

        do nn=2,nty
          do j=2,njm
            ytu(j,nn) = ytu(j,nn-1) + tk(nn)*(ytu(j-1,nn-1) +
     $           ytu(j+1,nn-1) - 2.*ytu(j,nn-1))
            ytv(j,nn) = ytv(j,nn-1) + tk(nn)*(ytv(j-1,nn-1) +
     $           ytv(j+1,nn-1) - 2.*ytv(j,nn-1))
          end do
        end do

cc        store the filtered fields in us,vs and gs

          do j=1,nj
            us(i,j)=ytu(j,nty)
            vs(i,j)=ytv(j,nty)
          end do

        end do
        
        return
        end
