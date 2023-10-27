      subroutine bicub2(ikeep,ib,f,ix,jy,dout,mn,yr,xin,yin,
     $     ipt,jpt,pix,pjy,
     $     tensx,tensy,
     $     fxx,fyy,tp1,tp2,tp3)
c         
      dimension f(ix,jy),dout(mn),xin(mn)       
     1     ,yr(jy),yin(mn),ipt(mn),jpt(mn),pix(mn,4),pjy(mn,4)
c
      dimension fxx(ix,jy),fyy(ix,jy),tp1(mn,4),tp2(mn,4),tp3(ix,jy)
c         
c          subroutine bicub2  
c         
c          a bicubic spline interpolator to interpolate from a grid   
c          with constant grid spacing to a grid with constant or      
c          variable grid spacing. all grids are assumed to have point 
c          (1,1) in the lower left corner with i increasing to the right        
c          and j increasing upward.     
c         
c          arguments:         
c         
c          f(ix,jy): fwa of data array to be interpolated from (given 
c                    by user) 
c         
c          ix: first (i) dimension of f (given by user)     
c         
c          jy: second (j) dimension of f (given by user)    
c         
c          dout(mn): fwa of array of interpolated values (given on    
c                     output) 
c         
c         
c         mn: number of points (dimension) of output grid   
c         
c          xin(mn): x-coordinates of points in dout relative to the   
c                   x-coordinates of f. a "1" refers to the leftmost  
c                   boundary of f (given by user) 
c         
c          yin(mn): y-coordinates of points in dout relative to the   
c                   y-corrdinates of f. a "1" refers to the bottom    
c                   row of f (given by user)      
c         
c          pix(mn,4): array to hold coefficients for interpolation in 
c                     x-direction (computed internally if ikeep=0)    
c         
c          pjy(mn,4): array to hold coefficients for interpolation in 
c                     y-direction (computed internally if ikeep=0)    
c         
c          tp1(mn,4): work space        
c         
c          tp2(mn,4): work space        
c         
c          tp3(ix,jy): work space       
c         
c          fxx(ix,jy): array to hold cubic spline values (computed    
c                      internally)      
c         
c          fyy(ix,jy): array to hold cubic spline values (computed    
c                      internally)      
c         
c          ipt(mn): array that holds i coordinate, relative to f grid,
c                   of each point in dout (computed internally if     
c                   ikeep=0)  
c         
c          jpt(mn): array that holds j coordinate, relative to f grid,
c                   of each point in dout (computed internally if     
c                   ikeep=0)  
c         
c          ib: =1  second derivative of spline is zero on i=1 and     
c                   i=ix boundaries     
c               =2  spline is periodic in i dimension (i.e., f is     
c                   periodic) 
c               (given by user)         
c         
c          ikeep:  =0  ipt,jpt,pix,pjy,and work2 are computed         
c                  =1  ipt,jpt,pix,pjy and work2 are used from        
c                      a previous call (i.e., the co-ordinates of f   
c                      and dout are the same as in a previous call)   
c                  (computed internally if ikeep=0)         
c         
      parameter (zero= 0.0, one= 1.0, two= 2.0)   
c         
c          compute ipt,jpt,pix and pjy  
c         
      if(ikeep.eq.0)
     $     call stupiy(ib,yr,xin,yin,mn,ix,jy,pix,pjy,ipt,jpt,
     $ tp1,tp2)
      ixm1=ix-1     
      jym1=jy-1     
      jym2=jy-2     
      ijm2=ix*jy-2  
      ixjym2=ix*jym2
      ixjy= ix*jy   
c         
c          interpolate in x-direction   
c         
c          compute fyy        
c         
cmic$ parallel shared(jy,ix,ixjym2,yr,f,fxx,fyy,tp3) private(i,j)
cmic$ do parallel     
      do 100 j=2,jy
      do 100 i=1,ix 
      fxx(i,j)= yr(j)-yr(j-1)         
  100 continue      
c         
cmic$ do parallel vector         
cdir$ ivdep
      do  i=1,ixjym2
        fyy(i,2)= (fxx(i,3)*(f(i,1)-f(i,2))+
     $       fxx(i,2)*(f(i,3)-f(i,2)))
     *       /(fxx(i,3)*fxx(i,3)*fxx(i,2))
        tp3(i,2)= fxx(i,2)/fxx(i,3)
      end do
cmic$ end parallel
c         
      call trdivv(ix,jym2,tp3(1,2),fyy(1,2))   
c         
      call zilch(fyy,ix)      
      call zilch(fyy(1,jy),ix)
c         
c  apply tension    
      if(tensy.lt.one) then   
cmic$ do all vector autoscope
      do 130 i=1,ixjy         
      fyy(i,1)= fyy(i,1)*tensy
  130 continue      
      endif         
c         
c          compute fxxyy      
c         
cmic$ do all vector autoscope
      do 140 i=1,ijm2         
      fxx(i+1,1)=(fyy(i,1)-two*fyy(i+1,1)+fyy(i+2,1))       
  140 continue      
c
      if(ib.ne.2) then        
      call tpotri(ix,jy,fxx)      
c
      else
c
      do 110 j=1,jy 
      fxx(1,j)= fyy(ix,j)-two*fyy(1,j)+fyy(2,j)   
      fxx(ix,j)= fyy(ixm1,j)-two*fyy(ix,j)+fyy(1,j)         
  110 continue      
c
      call tpose(fxx,ix,jy,tp3)        
      call trdiph(jy,ix,tp3)      
      call tpose(tp3,jy,ix,fxx)        
      endif
c         
      if(tensx.lt.one) then   
      do 210 i=1,ixjy         
      fxx(i,1)= fxx(i,1)*tensx
  210 continue      
      endif         
c         
c          fxx holds fxxyy and fyy holds fyy      
c         
      call gathij(1,ib,mn,ix,jy,ipt,jpt,fxx,fyy,tp2)    
cmic$ do all vector autoscope
      do 150 i=1,mn
      tp2(i,1)=pix(i,1)*tp2(i,1)        
      tp2(i,2)=pix(i,2)*tp2(i,2)        
      tp2(i,3)=pix(i,3)*tp2(i,3)        
      tp2(i,4)=pix(i,4)*tp2(i,4)        
      tp1(i,1)=tp2(i,1)+tp2(i,2)+tp2(i,3)+tp2(i,4)
  150 continue      
c         
      call gathij(0,ib,mn,ix,jy,ipt,jpt,fxx,fyy,tp2)    
cmic$ do all vector autoscope
      do 170 i=1,mn 
      tp2(i,1)=pix(i,1)*tp2(i,1)        
      tp2(i,2)=pix(i,2)*tp2(i,2)        
      tp2(i,3)=pix(i,3)*tp2(i,3)        
      tp2(i,4)=pix(i,4)*tp2(i,4)        
      tp1(i,2)=tp2(i,1)+tp2(i,2)+tp2(i,3)+tp2(i,4)
  170 continue      
c         
c          compute fxx        
c         
cmic$ do all vector autoscope
      do 190 i=1,ijm2         
      fxx(i+1,1)= f(i,1)-two*f(i+1,1)+f(i+2,1)    
  190 continue      
c
      if(ib.ne.2) then        
      call tpotri(ix,jy,tp3,fxx)
c
      else
c
      do 155 j=1,jy 
      fxx(1,j)= f(ix,j)-two*f(1,j)+f(2,j)         
      fxx(ix,j)= f(ixm1,j)-two*f(ix,j)+f(1,j)     
  155 continue      
c
      call tpose(fxx,ix,jy,tp3)        
      call trdiph(jy,ix,tp3)
      call tpose(tp3,jy,ix,fxx)        
      endif
c         
c  apply tension    
c         
      if(tensx.lt.one) then   
cmic$ do all vector autoscope
      do 240 i=1,ixjy         
      fxx(i,1)= fxx(i,1)*tensx
  240 continue      
      endif         
c         
      call gathij(1,ib,mn,ix,jy,ipt,jpt,fxx,f,tp2)      
c
cmic$ do all vector autoscope
      do 250 i=1,mn
      tp2(i,1)=pix(i,1)*tp2(i,1)        
      tp2(i,2)=pix(i,2)*tp2(i,2)        
      tp2(i,3)=pix(i,3)*tp2(i,3)        
      tp2(i,4)=pix(i,4)*tp2(i,4)        
      tp1(i,3)=tp2(i,1)+tp2(i,2)+tp2(i,3)+tp2(i,4)
  250 continue      
c
      call gathij(0,ib,mn,ix,jy,ipt,jpt,fxx,f,tp2)      
c
cmic$ do all vector autoscope
      do 270 i=1,mn
      tp2(i,1)=pix(i,1)*tp2(i,1)        
      tp2(i,2)=pix(i,2)*tp2(i,2)        
      tp2(i,3)=pix(i,3)*tp2(i,3)        
      tp2(i,4)=pix(i,4)*tp2(i,4)        
      tp1(i,4)=tp2(i,1)+tp2(i,2)+tp2(i,3)+tp2(i,4)
c         
c          interpolate in y-direction   
c         
      tp1(i,1)=tp1(i,1)*pjy(i,1)        
      tp1(i,2)=tp1(i,2)*pjy(i,2)        
      tp1(i,3)=tp1(i,3)*pjy(i,3)        
      tp1(i,4)=tp1(i,4)*pjy(i,4)        
      dout(i)=tp1(i,1)+tp1(i,2)+tp1(i,3)+tp1(i,4) 
  270 continue      
      return        
      end 
