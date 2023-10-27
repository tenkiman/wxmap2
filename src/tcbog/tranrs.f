      subroutine tranrs(istrt,im,jm,mlmax,poly,w,r,s)
c
      dimension poly(mlmax,jm/2),s(mlmax,2),r(im,jm),w(jm)
      dimension cc(im+3,jm),work(im*jm,2)
c
      include 'fftcom.h'
c
c
      jtrun= 2*((1+(im-1)/3)/2)
      mlx= (jtrun/2)*((jtrun+1)/2)
c
      jstrt= 1
      if(istrt.eq.0) jstrt= 2
c
      do 23 j=1,jm
      do 23 i=1,im
      cc(i,j)= r(i,j)
   23 continue
c
      call rfftmlt(cc,work,trigs,ifax,1,im+3,im,jm,-1)
c
c  if istrt .eq. zero, the quadrature integral is initialized from zero,
c  otherwise the sum is added to initial 's' array passed with call.
c
      if(istrt.eq.0) then
c
      m1= 0
      do 62 l=jtrun-1,1,-2
cdir$ ivdep     
         do 63 m = 1, l
         mm= 2*m-1
         mp= mm+1
         ml= m+m1
         mk= ml+mlx
            s(ml,1) = w(1)*poly(ml,1)*(cc(mm,1)+cc(mm,jm))
            s(ml,2) = w(1)*poly(ml,1)*(cc(mp,1)+cc(mp,jm))
            s(mk,1) = w(1)*poly(mk,1)*(cc(mm,1)-cc(mm,jm))
            s(mk,2) = w(1)*poly(mk,1)*(cc(mp,1)-cc(mp,jm))
   63    continue
      m1= m1+l
   62 continue
c
      ml= mlx*2
cdir$ ivdep     
      do 64 m=2,jtrun,2
      ml=ml+1
      mm= 2*m-1
      mp= mm+1
      s(ml,1)= w(1)*poly(ml,1)*(cc(mm,1)+cc(mm,jm))
      s(ml,2)= w(1)*poly(ml,1)*(cc(mp,1)+cc(mp,jm))
   64 continue
      endif
c
      do 70 j=jstrt,jm/2
      jj= jm-j+1
      m1= 0
      do 72 l=jtrun-1,1,-2
cdir$ ivdep     
         do 73 m = 1, l
         mm= 2*m-1
         mp= mm+1
         ml= m+m1
         mk= ml+mlx
            s(ml,1) = s(ml,1)+w(j)*poly(ml,j)*(cc(mm,j)+cc(mm,jj))
            s(ml,2) = s(ml,2)+w(j)*poly(ml,j)*(cc(mp,j)+cc(mp,jj))
            s(mk,1) = s(mk,1)+w(j)*poly(mk,j)*(cc(mm,j)-cc(mm,jj))
            s(mk,2) = s(mk,2)+w(j)*poly(mk,j)*(cc(mp,j)-cc(mp,jj))
   73    continue
      m1= m1+l
   72 continue
c
      ml= mlx*2
cdir$ ivdep     
      do 65 m=2,jtrun,2
      ml=ml+1
      mm= 2*m-1
      mp= mm+1
      s(ml,1)= s(ml,1)+w(j)*poly(ml,j)*(cc(mm,j)+cc(mm,jj))
      s(ml,2)= s(ml,2)+w(j)*poly(ml,j)*(cc(mp,j)+cc(mp,jj))
   65 continue
   70 continue
c
      return
      end
