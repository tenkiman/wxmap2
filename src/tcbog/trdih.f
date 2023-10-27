      subroutine trdih (m,n,y)
c         
c  vectorized tri-diagonal gaussian elimintaion solver      
c         
      dimension y(m,n),c(n) 
c         
      parameter (one=1.0, four= 4.0)    
c         
c gaussian elimination        
c         
      c(1) = 0.25          
c
      do 201 i=1,m  
      y(i,1)= y(i,1)*c(1)  
  201 continue      
c
      do 103 j=2,n-1 
      c(j)= 1.0/(4.0-c(j-1))
CDIR$ IVDEP
      do 103 i=1,m  
      y(i,j)= (y(i,j)-y(i,j-1))*c(j) 
  103 continue      
c
CDIR$ IVDEP
      do 202 i=1,m  
      y(i,n)=(y(i,n)-y(i,n-1))/(four-c(n-1))     
  202 continue      
c         
c backwards substitution      
c         
      do 104 k=n-1,1,-1        
CDIR$ IVDEP
      do 104 i=1,m  
      y(i,k)= y(i,k)-c(k)*y(i,k+1)
  104 continue      
      return        
      end 
