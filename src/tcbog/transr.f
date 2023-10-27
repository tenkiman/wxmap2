      subroutine transr(im,jm,mlmax,poly,s,r,iqp,ichar,jchar)
c
      dimension poly(mlmax,jm/2),s(mlmax,2),r(im,jm)
      dimension cc(im+3,jm),work(im*jm,2)
c
      include 'fftcom.h'
c
      character*8 ichar,jchar
c
c
      jtrun= 2*((1+(im-1)/3)/2)
      mlx= (jtrun/2)*((jtrun+1)/2)
c
cmic$ do all
cmic$1 shared (im,jm,mlx,jtrun,poly,s,cc)
cmic$1 private (l,j,jj,m,ml,mm,mp,mk,m1)
c
      do 5 j=1,jm/2
      jj= jm+1-j
cdir$ ivdep
      do 55 m=1,im+3
      cc(m,j)= 0.0
      cc(m,jj)= 0.0
   55 continue
      ml= 2*mlx
CDIR@ IVDEP
      do 3 m=2,jtrun,2
      ml= ml+1
      mm= 2*m-1
      mp= mm+1
      cc(mm,j)= poly(ml,j)*s(ml,1)
      cc(mp,j)= poly(ml,j)*s(ml,2)
      cc(mm,jj)= cc(mm,j)
      cc(mp,jj)= cc(mp,j)
    3 continue
c
      m1= 0
      do 5 l=jtrun-1,1,-2
CDIR@ IVDEP
      do 6 m=1,l
      mm= 2*m-1
      mp= mm+1
      ml= m+m1
      mk= ml+mlx
      cc(mm,j)= cc(mm,j)+poly(ml,j)*s(ml,1)+poly(mk,j)*s(mk,1)
      cc(mm,jj)=cc(mm,jj)+poly(ml,j)*s(ml,1)-poly(mk,j)*s(mk,1)
      cc(mp,j)= cc(mp,j)+poly(ml,j)*s(ml,2)+poly(mk,j)*s(mk,2)
      cc(mp,jj)=cc(mp,jj)+poly(ml,j)*s(ml,2)-poly(mk,j)*s(mk,2)
    6 continue
      m1= m1+l
    5 continue
c
      call rfftmlt(cc,work,trigs,ifax,1,im+3,im,jm,1)
c
cmic$ do all autoscope
      do 22 j=1,jm
      do 22 i=1,im
      r(i,j)= cc(i,j)
   22 continue
c
      if(iqp.gt.0) then    
      if(iqp.ge.2) call qprnth(r(1,1),ichar//jchar,1,1,im,jm)
      if(iqp.ge.1)call qpnh(r(1,1),ichar//jchar,1,1,im,jm)
      endif
c
      return
      end
