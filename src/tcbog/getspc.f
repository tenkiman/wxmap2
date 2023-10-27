      subroutine getspc(phi,u,v,phif,uf,vf,
     $     phiadd,pres,lm,jdtanl,iflspc)

c **-neprf-** programmer jim goerss - date 19 sep 1989
      include 'parmg.h'

      dimension phi(imgaus,jmgp2,lm),u(imgaus,jmgp2,lm)
     x     ,    v(imgaus,jmgp2,lm),pres(lm)

      dimension phif(imgaus,jmgaus,lm),uf(imgaus,jmgaus,lm)
     x,      vf(imgaus,jmgaus,lm),dum(imgaus,jmgaus)

      dimension phiadd(lm)
      character*8 jdtanl
      character ffile*120
      data grav/9.81/
      data gravecmwf/9.80665/

      logical verb

      verb=.false.

      do l=1,lm
        read(10,err=802) dum
        do i=1,imgaus
          do j=1,jmgaus
            jj=jmgaus-j+1
            uf(i,jj,l)=dum(i,j)
          end do
        end do
        if(verb)
     $       print*,'  uf l = ',l,' uf(220,120) = ',uf(220,120,l)
      end do

      do l=1,lm
        read(10,err=802) dum
        do i=1,imgaus
          do j=1,jmgaus
            jj=jmgaus-j+1
            vf(i,jj,l)=dum(i,j)
          end do
        end do
        if(verb) 
     $       print*,'  vf l = ',l,' vf(220,120) = ',vf(220,120,l)
      end do

      do l=1,lm
        read(10,err=802) dum
        do i=1,imgaus
          do j=1,jmgaus
            jj=jmgaus-j+1
            phif(i,jj,l)=dum(i,j)
          end do
        end do
        if(verb) 
     $       print*,'phif l = ',l,' phif(220,120) = ',phif(220,120,l)
      end do

      do  l=1,lm
        do  i=1,imgaus
          do j=1,jmgaus
ccccc            phi(i,2,l)=phif(i,1,l)+phiadd(l)
            phi(i,j+1,l)=phif(i,j,l)/gravecmwf
            u(i,j+1,l)=uf(i,j,l)
            v(i,j+1,l)=vf(i,j,l)
          end do
        end do

        do i=1,imgaus
          phi(i,1,l)=0.
          u(i,1,l)=0.
          v(i,1,l)=0.
          phi(i,jmgp2,l)=0.
          u(i,jmgp2,l)=0.
          v(i,jmgp2,l)=0.
        end do

      end do

      go to 999
 802  print*,' error reading... '
      stop 'error reading fields'

      go to 999

 999  continue
      return
      end
