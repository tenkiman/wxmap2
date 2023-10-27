      subroutine tpotri(ix,jy,fxx) 
c         
      dimension tp3(jy,ix),fxx(ix,jy)    
c         
      call tpose(fxx,ix,jy,tp3)        
      call trdih(jy,ix-2,tp3(1,2))      
      do 10 j=1,jy  
      tp3(j,1)= 0.0
      tp3(j,ix)= 0.0         
   10 continue      
      call tpose(tp3,jy,ix,fxx)        
      return        
      end 
