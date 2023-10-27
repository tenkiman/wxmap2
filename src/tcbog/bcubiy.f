      subroutine bcubiy(ikeep,ib,f,ix,jy,dout,mn,yr,xin,yin,v,
     $     tensx,tensy,
     $     pix,pjy,fxx,fyy,tp1,tp2,tp3)
c         
c  parameter list   
c         
c  ikeep= 0 - compute data in array v   
c       = 1 - assumes array v saved from previous call      
c         
c  ib= 1 - 2nd derivative=0 on i=1, i=ix boundaries         
c     = 2 - periodic boundaries in i direction    
c         
c  f,ix,jy,dout,mn,xin,yin - see below  
c         
c  v= save array ( must be saved if ikeep= 1 is used on subsequent call)        
c  length=10*mn words)  
c         
      dimension f(ix,jy),dout(mn),xin(mn),yr(jy),yin(mn),
     $     pix(mn,4),pjy(mn,4)    

      dimension fxx(ix,jy),fyy(ix,jy),tp1(mn,4),tp2(mn,4),tp3(ix,jy)

      real v(10*mn)      
      mn2= mn*4     
      ixj= (ix*jy+1)
c         
c  indexes for wsave (v) array
      j1=1
      j2=j1+mn      
      j3=j2+mn      
      j4=j3+mn2     
c
      call bicub2(ikeep,ib,f,ix,jy,dout,mn,yr,xin,yin,
     $     v(j1),v(j2),pix,pjy,
     $     tensx,tensy,
     $     fxx,fyy,tp1,tp2,tp3)

      return        
      end 
