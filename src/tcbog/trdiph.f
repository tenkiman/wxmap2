      subroutine trdiph (m,n,y)         
c         
c  vectorized periodic gaussian elimination solver
c         
      dimension y(m,n),work(m+3*n) 
c         
      parameter (one= 1.0, four= 4.0)   
c         
c gaussian elimination        
c         
      nt2= 2*n      
      work(n+1)= 0.25         
      v = one       
      work(1) = work(n+1)     
      work(nt2+1) = work(n+1) 
      bn = -v*work(nt2+1)+four
      do 101 j=2,n-2
         ne = j+n   
         work(ne) = one/(four-work(j-1))
         work(j) = work(ne)   
         nu = j+nt2 
         work(nu) = -work(nu-1)*work(ne)
         v = -v*work(j-1)     
         bn = bn-v*work(nu)   
  101 continue      
c
      v = one-v*work(n-2)     
      ne = nt2      
      work(ne-1) = one/(four-work(n-2)) 
      nu = nt2+n    
      work(n-1) = (one-work(nu-2))*work(ne-1)      
      work(ne) = one/(bn-v*work(n-1))    
c
      v= one        
CDIR$ IVDEP
      do 201 i=1,m  
      y(i,1)= y(i,1)*work(n+1)
      work(i+3*n)=y(i,n)-v*y(i,1)       
  201 continue      
c
      do 103 j=2,n-2
      v= -v*work(j-1)         
         ne = j+n   
CDIR$ IVDEP
      do 113 i=1,m  
      y(i,j)= (y(i,j)-y(i,j-1))*work(ne)
      work(i+3*n)= work(i+3*n)-v*y(i,j) 
  113 continue      
  103 continue      
      v = one-v*work(n-2)     
      ne = nt2      
CDIR$ IVDEP
      do 203 i=1,m  
      y(i,n-1)=(y(i,n-1)-y(i,n-2))*work(ne-1)       
      work(i+3*n)= work(i+3*n)-v*y(i,n-1)
c         
c backwards substitution      
c         
      y(i,n)= work(i+3*n)*work(ne)      
      y(i,n-1)= y(i,n-1)-work(n-1)*y(i,n)  
  203 continue      
c
      do 104 k=n-2,1,-1
         nu = k+nt2 
CDIR$ IVDEP
      do 104 i=1,m  
      y(i,k)= y(i,k)-work(k)*y(i,k+1)-work(nu)*y(i,n)       
  104 continue      
      return        
      end 
