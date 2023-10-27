      subroutine bcubvs(iderv,f,ix,jy,dout,mn,yr,yin,tensy) 
c
c  parameter list   
c         
c  f,ix,jy,dout,mn,xin,yin - see below  
c         
      dimension f(ix,jy),dout(mn),yr(ix,jy),yin(mn)         
      dimension tensy(jy)     
c         
      dimension fxx(ix,jy),fyy(ix,jy),pjy(mn,4),tp1(mn,4)    
      dimension ipt(mn),jpt(mn)
c         
c         
c          a bicubic spline interpolator to interpolate from a grid   
c          with constant i (first dimension) grid spacing and variable
c          j (second dimension) grid spacing t0 a grid with 
c          variable grid spacing. all grids are assumed to have point 
c          (i,1) in the lower left corner with i increasing to the right        
c          and j increasing upward.     
c         
      parameter (zero= 0.0, one=1.0)    
c         
c          compute ipt,jpt and pjy      
c         
      call setupv(iderv,yr,yin,mn,ix,jy,pjy,ipt,jpt,tp1)         
      jm= mn/ix     
      ixm1=ix-1     
      jym1=jy-1     
      jym2=jy-2     
      ijm2=ix*jy-2  
      ixjym2=ix*jym2
      mn4=mn*4      
c         
c         
c          compute fyy        
c         
      ll= ixjym2+ix 
      do 100 i=1,ll 
      fxx(i,2)= yr(i,2)-yr(i,1)         
  100 continue      
c         
      do 210 i=1,ixjym2       
      fyy(i,2)= (fxx(i,3)*(f(i,1)-f(i,2))+fxx(i,2)*(f(i,3)-f(i,2)))
     * /(fxx(i,3)*fxx(i,3)*fxx(i,2))
      fxx(i,2)= fxx(i,2)/fxx(i,3)
  210 continue      
c         
      call trdivv(ix,jym2,fxx(1,2),fyy(1,2))   
c         
      call zilch(fyy,ix)      
      call zilch(fyy(1,jy),ix)
c         
c  apply tension    
      do 5 j=1,jy   
      do 5 i=1,ix   
      fyy(i,j)= fyy(i,j)*tensy(j)       
    5 continue      
c         
      call gathv(mn,ix,jy,ipt,jpt,fyy,f,tp1)  
c         
      do 130 i=1,mn4
      tp1(i,1)=tp1(i,1)*pjy(i,1)        
  130 continue      
      do 140 i=1,mn 
      dout(i)=tp1(i,1)+tp1(i,2)+tp1(i,3)+tp1(i,4) 
  140 continue      
      return        
      end 
