      subroutine gathv(mn,ix,jy,ipt,jpt,fyy,f,tp1)      
c         
      dimension fyy(ix*jy),f(ix*jy),tp1(mn,4)     
      dimension ipt(mn),jpt(mn) 
c         
      do 10 i=1,mn  
      inx= ipt(i)+ix*jpt(i)
      inxp= inx-ix
c         
      tp1(i,1)= fyy(inx)         
      tp1(i,3)= f  (inx)         
c         
      tp1(i,2)= fyy(inxp)         
      tp1(i,4)= f  (inxp)         
   10 continue      
c         
      return        
      end 
