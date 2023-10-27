      function ichlen(c,imax)
      character*1 c(imax)
      iend=-1
      ii=1
      do while (iend.eq.-1.and.ii.le.imax)
        if(c(ii).eq.' ') iend=ii
        ii=ii+1
      end do  
      if(ii.gt.imax) then
        ichlen=imax
      else
        ichlen=iend-1
      end if
      return
      end
