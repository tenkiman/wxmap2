      program read
      parameter(ni=360,nj=180)
      dimension ia(ni,nj),a(ni,nj)
      open(10,file='veg_clss.vgc')
      open(12,file='veg_clss.dat',form='unformatted')
      do j=1,nj
        read(10,'(360i8)') (ia(i,j),i=1,ni)
        do i=1,ni
          a(i,j)=float(ia(i,j))
        end do
      end do

      write(12) a
      stop
      end
