      subroutine sortml(jtrun,mlmax,msort,lsort,mlsort)
c
      dimension msort(mlmax),lsort(mlmax),mlsort(jtrun,jtrun)
c
      mlx= (jtrun/2)*((jtrun+1)/2)
      ml= 0
      do 1 k=1,jtrun-1,2
      do 1 m=1,jtrun-k  
      ml= ml+1
      mlp= ml+mlx
      mlsort(m,m+k)= mlp
      mlsort(m,m+k-1)= ml
      msort(ml)= m
      lsort(ml)= m+k-1
      msort(mlp)= m
      lsort(mlp)= m+k
    1 continue
c
      ml= mlp
      do 2 m=2,jtrun,2
      ml= ml+1
      mlsort(m,jtrun)= ml
      msort(ml)= m
      lsort(ml)= jtrun
    2 continue
      return
      end
