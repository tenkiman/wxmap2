      subroutine qprnth(a,t1,ic,jc,m,n) 
c
      implicit real (a-h,o-z)
c
c         
c  qprnth prints an array a(m,n) starting at address a(1+ic,1+jc).    
c  values are automatically scaled to allow integer format printing.  
c         
c a= fwa of m x n array       
c t1 = title (16 character) 
c ic,jc=lower left corner coords to be printed    
c up to 43 x 83 points printed
      dimension ix(43)
      character*16 t1
      real a(m,n)   
      haf= 0.5
c  determine grid limits      
    3 ie=min0(ic+42,m)        
      jl= n         
c  index backwards checking for max     
c         
   11 xm=0.         
      do 14 j=jc,jl 
      do 14 i=ic,ie 
      af= (a(i,j))  
   14 xm=max(xm,abs(af))      
c  determine scaling factor limits      
      if(xm.lt.1.e-35) xm=99. 
      x99= 99.
      xm=log10(x99/xm)       
      kp=xm         
      if(xm.lt.0.)kp=kp-1     
c  print scaling constants    
   12 print 1,t1,kp,(i,i=ic,ie,2)        
    1 format(1h0,a16,'   k=',i3/1x,22i6)        
      fk=10.**kp    
c  quickprint field 
      jli= jl+1     
      do 2 j=jc,jl  
      jli= jli-1    
      ii= 0         
      if(kp.ne.0) go to 8     
      do 9 i=ic,ie  
      ii=ii+1       
      af= (a(i,jli))
    9 ix(ii)=af+sign(haf,af)   
      go to 10      
    8 do 7 i=ic,ie  
      ii=ii+1       
      af= (a(i,jli))
    7 ix(ii)=af*fk+sign(haf,af)
   10 print 6,jli,(ix(i),i=1,ii),jli    
    6 format(i4,44i3)         
    2 continue      
      return        
      end 
