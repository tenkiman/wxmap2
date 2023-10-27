      subroutine stupiy(ib,yr,xin,yin,mn,ix,jy,pix,pjy,ipt,jpt    
     *, tp1,bitx)   
c         
      implicit real (a-h,o-z) 
c         
      dimension yin(mn),xin(mn),pix(mn,4),pjy(mn,4),tp1(mn,4)         
      dimension yr(jy)        
      dimension ipt(mn),jpt(mn) 
      logical bitx(mn,2)      
c         
      parameter (one= 1.0)    
c         
c  if non-periodic in i-direction, force all interpolation pts to     
c  be inside left boundary to avoid indexing beyond limits of arrays. 
c         
      if(ib.eq.1) then        
      tem1=ix-0.00001         
cmic$ do all vector autoscope
      do 10 i=1,mn  
      xin(i)= min(tem1,xin(i))
   10 continue      
      endif         
c         
c         
c  find x-index of box containing each interpolation point  
c  and compute coefficients for spline interpolation        
c         
cmic$ do all vector autoscope
      do 20 i=1,mn  
      ipt(i)= xin(i)
      pix(i,3)= ipt(i)        
      pix(i,3)= xin(i)-pix(i,3)         
      pix(i,4)= one-pix(i,3)  
c         
      pix(i,1)= pix(i,3)*(pix(i,3)*pix(i,3)-one)   
      pix(i,2)= pix(i,4)*(pix(i,4)*pix(i,4)-one)   
   20 continue      
c         
c  find y-index of box containing each interpolation point and compute
c  coefficients for spline interplation 
c         
      do 45 i=1,mn  
      bitx(i,1)= .false.      
   45 continue      
      num= 0        
      do 5 j=2,jy   
      if(j.lt.jy) then        
      do 55 i=1,mn  
      bitx(i,2)= .not.bitx(i,1).and.(yin(i).lt.yr(j))       
   55 continue      
      else
      do 65 i=1,mn  
      bitx(i,2)= .not.bitx(i,1)         
   65 continue      
      endif         
      ic= ilsum(mn,bitx(1,2),1)
      if(ic.eq.0) go to 5     
      do 75 i=1,mn  
      if(bitx(i,2)) then      
      jpt(i)= j-1
      tp1(i,1)= yin(i)-yr(j-1)
      tp1(i,2)= yr(j)-yr(j-1) 
      endif         
   75 continue      
      num= num+ic   
      if(num.eq.mn) go to 6   
      do 85 i=1,mn  
      bitx(i,1)= bitx(i,1).or.bitx(i,2) 
   85 continue      
    5 continue      
    6 continue      
c         
cmic$ do all vector autoscope
      do 95 i=1,mn  
      pjy(i,3)= tp1(i,1)/tp1(i,2)       
      pjy(i,4)= one-pjy(i,3)  
c         
      pjy(i,1)= pjy(i,3)*pjy(i,3)-one   
      pjy(i,2)= pjy(i,4)*pjy(i,4)-one   
c         
      pjy(i,1)= pjy(i,1)*tp1(i,1)*tp1(i,2)        
      pjy(i,2)= pjy(i,2)*tp1(i,2)*(tp1(i,2)-tp1(i,1))       
   95 continue      
      return        
      end 
