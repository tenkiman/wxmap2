C     This file is autogenerated with f2py (version:2.317)
C     It contains Fortran wrappers to fortran functions.

      subroutine f2pywraplastch (lastchf2pywrap, string_v)
      external lastch
      integer lastch, lastchf2pywrap
      character*(*) string_v
      lastchf2pywrap = lastch(string_v)
      end


      subroutine f2pyinitextrap(setupfunc)
      external setupfunc
      integer ifpxtrp(3,11)
      common /extrap/ ifpxtrp
      call setupfunc(ifpxtrp)
      end

      subroutine f2pyinitcliper(setupfunc)
      external setupfunc
      integer ifpclip(3,11)
      real flat(7)
      real flon(7)
      common /cliper/ ifpclip,flat,flon
      call setupfunc(ifpclip,flat,flon)
      end

      subroutine f2pyinitshifor(setupfunc)
      external setupfunc
      integer ishifor(3,11)
      common /shifor/ ishifor
      call setupfunc(ishifor)
      end

      subroutine f2pyinitshifor5(setupfunc)
      external setupfunc
      integer ishifor5(3,11)
      common /shifor5/ ishifor5
      call setupfunc(ishifor5)
      end

      subroutine f2pyinital5coef(setupfunc)
      external setupfunc
      real scoef(36,10)
      real avg(36,10)
      real sdev(36,10)
      common /al5coef/ scoef,avg,sdev
      call setupfunc(scoef,avg,sdev)
      end

      subroutine f2pyinitcl84(setupfunc)
      external setupfunc
      real cdi(12)
      common /cl84/ cdi
      call setupfunc(cdi)
      end

      subroutine f2pyinitpp(setupfunc)
      external setupfunc
      real p(164)
      common /pp/ p
      call setupfunc(p)
      end

      subroutine f2pyinithgrprm(setupfunc)
      external setupfunc
      real a(3,3)
      real radpdg
      real rrthnm
      real dgridh
      real hgridx
      real hgridy
      common /hgrprm/ a,radpdg,rrthnm,dgridh,hgridx,hgridy
      call setupfunc(a,radpdg,rrthnm,dgridh,hgridx,hgridy)
      end

      subroutine f2pyinitep5coef(setupfunc)
      external setupfunc
      real scoef(36,10)
      real avg(36,10)
      real sdev(36,10)
      common /ep5coef/ scoef,avg,sdev
      call setupfunc(scoef,avg,sdev)
      end


