      subroutine gausgr
c  **-neprf-** programmer jim goerss - date 5 feb 1988
      include 'parmg.h'
      include 'gridg.h'
      dimension sinl(jmgaus),work(jmgaus)
      dlngau=360./imgaus
      pi=4.*atan(1.)
      pimul=pi/180.
      do i=1,imgaus
        xlngau(i)=(i-1)*dlngau
        if(xlngau(i).gt.360.) xlngau(i)=xlngau(i)-360.
      end do

      call gausl3(jmgaus,-1.,1.,work,sinl)

      do j=1,jmgaus
        xltgau(j)=asin(sinl(j))
      end do

      tem=pi/2.+1.e-6

      yrgau(1)=-tem
      yrgau(jmgp2)=tem

      do j=1,jmgaus
        yrgau(j+1)=xltgau(j)
      end do

      return
      end
