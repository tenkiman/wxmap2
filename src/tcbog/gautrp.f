      subroutine gautrp(xind,yind,xin,yin,est,ntot,
     $     fld,v,ikeep,pix,pjy,
     $     fxx,fyy,tp1,tp2,tp3,ix,jy)

c         **-neprf-** programmer jim goerss - date 5 feb 1988

      include 'parmg.h'
      include 'gridg.h'

      dimension xind(ntot),yind(ntot),est(ntot),
     $     xin(ntot),yin(ntot),fld(imgaus,jmgp2),v(10*ntot),
     $     pix(ntot,4),pjy(ntot,4)

      dimension fxx(ix,jy),fyy(ix,jy),
     $     tp1(ntot,4),tp2(ntot,4),tp3(ix,jy)

      data ibd/2/
      one=1.
      do n=1,ntot
        xin(n)=xind(n)
        yin(n)=yind(n)
      end do

      call bcubiy(ikeep,ibd,fld,imgaus,jmgp2,est,ntot,yrgau,
     $     xin,yin,v,one,one,
     $     pix,pjy,fxx,fyy,tp1,tp2,tp3)


      return
      end
