      subroutine tranuv(im,jm,mlmax,radsq,ocos,eps4,cim
     *, poly,dpoly,vor,div,ut,vt)
c
      dimension ocos(jm),eps4(mlmax),cim(mlmax),poly(mlmax,jm/2)
     *, dpoly(mlmax,jm/2),vor(mlmax,2)
     *, div(mlmax,2),ut(im,jm),vt(im,jm)
c
      dimension cu(im+3,jm),cv(im+3,jm),work(im*jm,2)
     *, cfac(mlmax),dfac(mlmax)
c
      include 'fftcom.h'
c
      jtrun= 2*((1+(im-1)/3)/2)
      mlx= (jtrun/2)*((jtrun+1)/2)
c
cdir$ ivdep
      do 10 ml=2,mlmax
      dfac(ml)= 1.0/(radsq*eps4(ml))
      cfac(ml)= cim(ml)*dfac(ml)
   10 continue
      dfac(1)= 0.0
      cfac(1)= 0.0
c
      do 55 m=1,(im+3)*jm/2
      cu(m,1)= 0.0
      cu(m,jm/2+1)= 0.0
      cv(m,1)= 0.0
      cv(m,jm/2+1)= 0.0
   55 continue
c
      do 20 j=1,jm/2
      rcos= 1.0/ocos(j)
      jj= jm+1-j
c
      ml= 2*mlx
cdir$ ivdep
      do 50 m=2,jtrun,2
      ml= ml+1
      mm= 2*m-1
      mp= mm+1
      cu(mm,j)=         +cfac(ml)*poly(ml,j)*div(ml,2)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*vor(ml,1)
c
      cu(mm,jj)=          +cfac(ml)*poly(ml,j)*div(ml,2)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*vor(ml,1)
c
      cu(mp,j)=         -cfac(ml)*poly(ml,j)*div(ml,1)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*vor(ml,2)
c
      cu(mp,jj)=          -cfac(ml)*poly(ml,j)*div(ml,1)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*vor(ml,2)
c
      cv(mm,j)=         +cfac(ml)*poly(ml,j)*vor(ml,2)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*div(ml,1)
c
      cv(mm,jj)=          +cfac(ml)*poly(ml,j)*vor(ml,2)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*div(ml,1)
c
      cv(mp,j)=         -cfac(ml)*poly(ml,j)*vor(ml,1)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*div(ml,2)
c
      cv(mp,jj)=          -cfac(ml)*poly(ml,j)*vor(ml,1)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*div(ml,2)
c
   50 continue
c
      m1= 0
      do 30 l=jtrun-1,1,-2
cdir$ ivdep
      do 40 m=1,l
      mm= 2*m-1
      mp= mm+1
      ml= m+m1
      mk= ml+mlx
c
      cu(mm,j)= cu(mm,j)+cfac(ml)*poly(ml,j)*div(ml,2)
     *                  +cfac(mk)*poly(mk,j)*div(mk,2)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*vor(ml,1)
     *                  +dfac(mk)*dpoly(mk,j)*rcos*vor(mk,1)
c
      cu(mm,jj)= cu(mm,jj)+cfac(ml)*poly(ml,j)*div(ml,2)
     *                  -cfac(mk)*poly(mk,j)*div(mk,2)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*vor(ml,1)
     *                  +dfac(mk)*dpoly(mk,j)*rcos*vor(mk,1)
c
      cu(mp,j)= cu(mp,j)-cfac(ml)*poly(ml,j)*div(ml,1)
     *                  -cfac(mk)*poly(mk,j)*div(mk,1)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*vor(ml,2)
     *                  +dfac(mk)*dpoly(mk,j)*rcos*vor(mk,2)
c
      cu(mp,jj)= cu(mp,jj)-cfac(ml)*poly(ml,j)*div(ml,1)
     *                  +cfac(mk)*poly(mk,j)*div(mk,1)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*vor(ml,2)
     *                  +dfac(mk)*dpoly(mk,j)*rcos*vor(mk,2)
c
      cv(mm,j)= cv(mm,j)+cfac(ml)*poly(ml,j)*vor(ml,2)
     *                  +cfac(mk)*poly(mk,j)*vor(mk,2)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*div(ml,1)
     *                  -dfac(mk)*dpoly(mk,j)*rcos*div(mk,1)
c
      cv(mm,jj)= cv(mm,jj)+cfac(ml)*poly(ml,j)*vor(ml,2)
     *                  -cfac(mk)*poly(mk,j)*vor(mk,2)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*div(ml,1)
     *                  -dfac(mk)*dpoly(mk,j)*rcos*div(mk,1)
c
      cv(mp,j)= cv(mp,j)-cfac(ml)*poly(ml,j)*vor(ml,1)
     *                  -cfac(mk)*poly(mk,j)*vor(mk,1)
     *                  -dfac(ml)*dpoly(ml,j)*rcos*div(ml,2)
     *                  -dfac(mk)*dpoly(mk,j)*rcos*div(mk,2)
c
      cv(mp,jj)= cv(mp,jj)-cfac(ml)*poly(ml,j)*vor(ml,1)
     *                  +cfac(mk)*poly(mk,j)*vor(mk,1)
     *                  +dfac(ml)*dpoly(ml,j)*rcos*div(ml,2)
     *                  -dfac(mk)*dpoly(mk,j)*rcos*div(mk,2)
c
   40 continue
c
      m1= m1+l
   30 continue
   20 continue
c
      call rfftmlt(cu,work,trigs,ifax,1,im+3,im,jm,1)
      call rfftmlt(cv,work,trigs,ifax,1,im+3,im,jm,1)
c
      do 22 j=1,jm
cdir$ ivdep
      do 22 i=1,im
      ut(i,j)= cu(i,j)
      vt(i,j)= cv(i,j)
   22 continue
c
      return
      end
