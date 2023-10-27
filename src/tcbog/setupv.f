      subroutine setupv(iderv,yr,yin,mn,ix,jy,pjy,ipt,jpt,tp1)   
c         
      implicit real (a-h,o-z) 
c         
      dimension yin(mn),yr(ix,jy),pjy(mn,4),tp1(mn,4)       
      dimension ipt(mn),jpt(mn)         
      logical bitx(ix,2)      
c         
      parameter (one= 1.0, three= 3.0)  
c         
      mn2=mn*2      
c         
      n= mn/ix      
      ii= -ix       
      do 10 j=1,n   
      ii= ii+ix     
      do 10 i=1,ix  
   10 ipt(i+ii)= i 
c         
      kt= 1         
      do 5 j=1,n    
      do 55 i=1,ix  
      bitx(i,1)= .false.      
   55 continue      
      k= kt         
      num= 0        
      ii= ix*(j-1)  
    6 k= k+1        
      do 66 i=1,ix  
      bitx(i,2)= .not.bitx(i,1).and.(yin(i+ii).le.yr(i,k))  
   66 continue      
      ic= ilsum(ix,bitx(1,2),1)
      if(ic.eq.0) then        
      if(num.eq.0) kt= kt+1   
      go to 6       
      endif         
      do 76 i=1,ix  
      bitx(i,1)= bitx(i,1).or.bitx(i,2) 
   76 continue      
      num= num+ic   
      do 86 i=1,ix  
      if(bitx(i,2)) then      
      jpt(i+ii)= k-1
      tp1(i+ii,1)= yin(i+ii)-yr(i,k-1)  
      tp1(i+ii,2)= yr(i,k)-yr(i,k-1)    
      endif         
   86 continue      
      if(num.lt.ix) go to 6   
    5 continue      
c         
      if(iderv.eq.0) then     
      do 90 i=1,mn  
      pjy(i,3)= tp1(i,1)/tp1(i,2)       
      pjy(i,4)= one-pjy(i,3)  
   90 continue      
c         
      do 100 i=1,mn2
      pjy(i,1)= pjy(i,3)*pjy(i,3)-one   
  100 continue      
c         
      do 110 i=1,mn 
      pjy(i,1)= pjy(i,1)*tp1(i,1)*tp1(i,2)        
      tp1(i,1)= tp1(i,2)-tp1(i,1)       
      pjy(i,2)= pjy(i,2)*tp1(i,1)*tp1(i,2)        
  110 continue      
      else
      do 120 i=1,mn 
      pjy(i,3)= one/tp1(i,2)  
      pjy(i,4)= -pjy(i,3)     
      pjy(i,1)= three*(pjy(i,3)*tp1(i,1)*tp1(i,1))-tp1(i,2) 
      pjy(i,2)= three*(pjy(i,4)*(tp1(i,2)-tp1(i,1))**2)+tp1(i,2)      
  120 continue      
      endif         
      return        
      end 
