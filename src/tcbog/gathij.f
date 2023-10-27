      subroutine gathij(kp,ib,mn,ix,jy,ipt,jpt,fxx,f,tp2)         
c         
      dimension fxx(ix*jy),f(ix*jy),tp2(mn,4)     
      dimension ipt(mn),jpt(mn) 
c         
cmic$ parallel 
cmic$1 shared(ib,kp,ipt,jpt,ix,mn,f,fxx,tp2) private(i,inx,inxp)
      if(ib.eq.1) then
c
      if(kp.eq.0) then
c
c  ib=1, kp=0
c
cmic$ do parallel vector
cdir$ ivdep
      do 10 i=1,mn  
      inx= ipt(i)+ix*jpt(i)-ix
      inxp= inx+1
c         
      tp2(i,2)= fxx(inx)         
      tp2(i,4)= f  (inx)         
c         
      tp2(i,1)= fxx(inxp)         
      tp2(i,3)= f  (inxp)         
   10 continue      
c
      else
c
c  ib=1 kp=1
c
cmic$ do parallel vector
cdir$ ivdep
      do 20 i=1,mn  
      inx= ipt(i)+ix*jpt(i)
      inxp= inx+1
c         
      tp2(i,2)= fxx(inx)         
      tp2(i,4)= f  (inx)         
c         
      tp2(i,1)= fxx(inxp)         
      tp2(i,3)= f  (inxp)         
   20 continue      
c
      endif
c
      else
c         
      if(kp.eq.0) then
c
c  ib=2, kp=0
c
cmic$ do parallel vector
cdir$ ivdep
      do 30 i=1,mn  
      inxp= 1+mod(ipt(i),ix)
      inx= ix*jpt(i)-ix
      inxp= inx+inxp
      inx= inx+ipt(i) 
c         
      tp2(i,2)= fxx(inx)         
      tp2(i,4)= f  (inx)         
c         
      tp2(i,1)= fxx(inxp)         
      tp2(i,3)= f  (inxp)         
   30 continue      
c
      else
c
c  ib=2, kp=1
c
cmic$ do parallel vector
cdir$ ivdep
      do 40 i=1,mn  
      inxp= 1+mod(ipt(i),ix)
      inx= ix*jpt(i)
      inxp= inx+inxp
      inx= inx+ipt(i) 
c         
      tp2(i,2)= fxx(inx)         
      tp2(i,4)= f  (inx)         
c         
      tp2(i,1)= fxx(inxp)         
      tp2(i,3)= f  (inxp)         
   40 continue      
c
      endif
c
      endif
cmic$ end parallel
c
      return
      end
