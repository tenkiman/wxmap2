      subroutine findmx2(d,rmax,rmin,ii,jj,ibig,jbig,ilit,jlit)
      real d(ii,jj)
      rmax = -9999.
      rmin = 9999.
      do i = 1,ii
        do j =1,jj
          if(d(i,j) .lt. rmin) then
            rmin = d(i,j)
            ilit = i
            jlit = j
          endif
          if(d(i,j) .gt. rmax) then
            rmax = d(i,j)
            ibig = i
            jbig = j
          endif
        end do
      end do
      
      return
      end
