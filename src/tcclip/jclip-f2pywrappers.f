C     -*- fortran -*-
C     This file is autogenerated with f2py (version:2)
C     It contains Fortran 77 wrappers to fortran functions.

      subroutine f2pywrapf1 (f1f2pywrap, alon)
      external f1
      real alon
      real f1f2pywrap, f1
      f1f2pywrap = f1(alon)
      end


      subroutine f2pywrapf2 (f2f2pywrap, idatim)
      external f2
      integer idatim
      real f2f2pywrap, f2
      f2f2pywrap = f2(idatim)
      end


      subroutine f2pywrapnewcyc (newcycf2pywrap, nowcyc, n)
      external newcyc
      integer nowcyc
      integer n
      integer newcycf2pywrap, newcyc
      newcycf2pywrap = newcyc(nowcyc, n)
      end


      subroutine f2pyinitwpclpfcst(setupfunc)
      external setupfunc
      real cfcst(12)
      common /wpclpfcst/ cfcst
      call setupfunc(cfcst)
      end

      subroutine f2pyinitblock1(setupfunc)
      external setupfunc
      real rcm(90,6)
      real rcz(95,6)
      real cnstm(6)
      real cnstz(6)
      common /block1/ rcm,rcz,cnstm,cnstz
      call setupfunc(rcm,rcz,cnstm,cnstz)
      end

      subroutine f2pyinitblock2(setupfunc)
      external setupfunc
      integer*2 npm(90,6)
      integer*2 npz(95,6)
      common /block2/ npm,npz
      call setupfunc(npm,npz)
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

      subroutine f2pyinitblockse1(setupfunc)
      external setupfunc
      real rcm(16,6)
      real rcz(14,6)
      real cnstm(6)
      real cnstz(6)
      common /blockse1/ rcm,rcz,cnstm,cnstz
      call setupfunc(rcm,rcz,cnstm,cnstz)
      end

      subroutine f2pyinitblockse2(setupfunc)
      external setupfunc
      integer*2 npm(16,6)
      integer*2 npz(14,6)
      common /blockse2/ npm,npz
      call setupfunc(npm,npz)
      end

      subroutine f2pyinitseiclpfcst(setupfunc)
      external setupfunc
      real cfcst(12)
      common /seiclpfcst/ cfcst
      call setupfunc(cfcst)
      end

      subroutine f2pyinitblocksw2(setupfunc)
      external setupfunc
      integer*2 npm(31,6)
      integer*2 npz(31,6)
      common /blocksw2/ npm,npz
      call setupfunc(npm,npz)
      end

      subroutine f2pyinitblocksw1(setupfunc)
      external setupfunc
      real rcm(31,6)
      real rcz(31,6)
      real cnstm(6)
      real cnstz(6)
      common /blocksw1/ rcm,rcz,cnstm,cnstz
      call setupfunc(rcm,rcz,cnstm,cnstz)
      end

      subroutine f2pyinitswpclpfcst(setupfunc)
      external setupfunc
      real cfcst(12)
      common /swpclpfcst/ cfcst
      call setupfunc(cfcst)
      end

      subroutine f2pyinitoldclpfcst(setupfunc)
      external setupfunc
      real cfcst(12)
      common /oldclpfcst/ cfcst
      call setupfunc(cfcst)
      end


