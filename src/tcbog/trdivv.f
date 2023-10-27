      subroutine trdivv (m,n,a,y)
c         
c  tri-diagonal gaussian elimination subroutine   
c         
      dimension       a(m,n)         ,y(m,n)    ,c(m,n-1)     
c         
      parameter (haf= 0.5, one= 1.0, two= 2.0)    
          
      nm = n-1      
      do 201 i=1,m  
      c(i,1)= haf/(one+a(i,1))       
      y(i,1) = y(i,1)*c(i,1)         
  201 continue      
c         
c         
c gaussian elimination        
c         
      do 101 j=2,nm 
CDIR$ IVDEP
      do 101 i=1,m  
      c(i,j)= one/(two+a(i,j)*(two-c(i,j-1)))        
      y(i,j) = (y(i,j)-a(i,j)*y(i,j-1))*c(i,j)        
  101 continue      
c
      do 202 i=1,m  
      y(i,n)= (y(i,n)-a(i,n)*y(i,nm))/(two+a(i,n)*(two-c(i,nm)))   
  202 continue      
c         
c backwards substitution      
c         
      do 104 k=nm,1,-1
CDIR$ IVDEP
      do 104 i=1,m  
      y(i,k)= y(i,k)-c(i,k)*y(i,k+1)
  104 continue      
      return        
      end 
