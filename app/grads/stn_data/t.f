	program test
	parameter(ni=100)
	dimension a(ni)
	open(10,file='test.dat',form='unformatted',status='unknown')
        icnt=1
        do i=1,ni
          a(i)=icnt
          icnt=icnt+1
        end do
	write(10) a
	write(10) (a(i),i=1,50)
        close(10)
	open(10,file='test.dat',form='unformatted',status='unknown')
        read(10) (a(i),i=1,50)
        print*,'i1 ',(a(i),i=1,50)
        read(10) (a(i),i=1,50)
        print*,'i2 ',(a(i),i=1,50)
	stop
	end
