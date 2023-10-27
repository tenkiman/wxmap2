      subroutine glogau(xlat,xlon,xind,yind,ntot)
c  **-neprf-** programmer jim goerss - date 5 feb 1988
      include 'parmg.h'
      include 'gridg.h'
      dimension xlat(ntot),xlon(ntot),xind(ntot),yind(ntot)
      zimgau=imgaus
      do  n=1,ntot
        xind(n)=xlon(n)/dlngau
        xind(n)=amod(xind(n),zimgau)+1.
        yind(n)=xlat(n)*pimul
      end do

      return
      end
