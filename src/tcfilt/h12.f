      subroutine h12(mode,lpivot,l1,m,u,iue,up,c,ice,icv,ncv)
c***begin prologue  h12
c***refer to  hfti,lsei,wnnls
c
c     subroutine h12 (mode,lpivot,l1,m,u,iue,up,c,ice,icv,ncv)
c
c     c.l.lawson and r.j.hanson, jet propulsion laboratory, 1973 jun 12
c     to appear in 'solving least squares problems', prentice-hall, 1974
c
c     modified at sandia labs, may 1977, to --
c
c     1)  remove double precision accumulation, and
c     2)  include usage of the basic linear algebra package for
c         vectors longer than a particular threshold.
c
c     construction and/or application of a single
c     householder transformation..     q = i + u*(u**t)/b
c
c     mode    = 1 or 2   to select algorithm  h1  or  h2 .
c     lpivot is the index of the pivot element.
c     l1,m   if l1 .le. m   the transformation will be constructed to
c            zero elements indexed from l1 through m.   if l1 gt. m
c            the subroutine does an identity transformation.
c     u(),iue,up    on entry to h1 u() contains the pivot vector.
c                   iue is the storage increment between elements.
c                                       on exit from h1 u() and up
c                   contain quantities defining the vector u of the
c                   householder transformation.   on entry to h2 u()
c                   and up should contain quantities previously computed
c                   by h1.  these will not be modified by h2.
c     c()    on entry to h1 or h2 c() contains a matrix which will be
c            regarded as a set of vectors to which the householder
c            transformation is to be applied.  on exit c() contains the
c            set of transformed vectors.
c     ice    storage increment between elements of vectors in c().
c     icv    storage increment between vectors in c().
c     ncv    number of vectors in c() to be transformed. if ncv .le. 0
c            no operations will be done on c().
c***routines called  saxpy,sdot,sswap
c***end prologue  h12
      dimension u(iue,m), c(1)
c***first executable statement  h12
      one=1.
c
      if (0.ge.lpivot.or.lpivot.ge.l1.or.l1.gt.m) return
      cl=abs(u(1,lpivot))
      if (mode.eq.2) go to 60
c                            ****** construct the transformation. ******
          do 10 j=l1,m
   10     cl=amax1(abs(u(1,j)),cl)
      if (cl) 130,130,20
   20 clinv=one/cl
      sm=(u(1,lpivot)*clinv)**2
          do 30 j=l1,m
   30     sm=sm+(u(1,j)*clinv)**2
      cl=cl*sqrt(sm)
      if (u(1,lpivot)) 50,50,40
   40 cl=-cl
   50 up=u(1,lpivot)-cl
      u(1,lpivot)=cl
      go to 70
c            ****** apply the transformation  i+u*(u**t)/b  to c. ******
c
   60 if (cl) 130,130,70
   70 if (ncv.le.0) return
      b=up*u(1,lpivot)
c                       b  must be nonpositive here.  if b = 0., return.
c
      if (b) 80,130,130
   80 b=one/b
      mml1p2=m-l1+2
      if (mml1p2.gt.20) go to 140
      i2=1-icv+ice*(lpivot-1)
      incr=ice*(l1-lpivot)
          do 120 j=1,ncv
          i2=i2+icv
          i3=i2+incr
          i4=i3
          sm=c(i2)*up
              do 90 i=l1,m
              sm=sm+c(i3)*u(1,i)
   90         i3=i3+ice
          if (sm) 100,120,100
  100     sm=sm*b
          c(i2)=c(i2)+sm*up
              do 110 i=l1,m
              c(i4)=c(i4)+sm*u(1,i)
  110         i4=i4+ice
  120     continue
  130 return
  140 continue
      l1m1=l1-1
      kl1=1+(l1m1-1)*ice
      kl2=kl1
      klp=1+(lpivot-1)*ice
      ul1m1=u(1,l1m1)
      u(1,l1m1)=up
      if (lpivot.eq.l1m1) go to 150
      call sswap(ncv,c(kl1),icv,c(klp),icv)
  150 continue
          do 160 j=1,ncv
          sm=sdot(mml1p2,u(1,l1m1),iue,c(kl1),ice)
          sm=sm*b
          call saxpy (mml1p2,sm,u(1,l1m1),iue,c(kl1),ice)
          kl1=kl1+icv
  160 continue
      u(1,l1m1)=ul1m1
      if (lpivot.eq.l1m1) return
      kl1=kl2
      call sswap(ncv,c(kl1),icv,c(klp),icv)
      return
      end
