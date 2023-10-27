      subroutine load32(a,b,k,ni,nj,nk)
      dimension a(ni,nj,nk),b(ni,nj)
      do i=1,ni
        do j=1,nj
          b(i,j)=a(i,j,k)
        end do
      end do
      return
      end

