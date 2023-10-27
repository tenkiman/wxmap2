      program test
      parameter (ni=360,nj=181)
      real*4 u(ni,nj),v(ni,nj)
      open(10,file='uv.dat',status='old',access='direct',recl=ni*nj*4)

      read(10,rec=1) u
      read(10,rec=2) v

      close(10)

      print*,u(180,90)
      stop
      end
