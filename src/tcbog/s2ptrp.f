      subroutine s2ptrp(im,jm,lm,lpout,y,boty,pin,dout,pout,vten) 
c
c      
      dimension y(im,jm,lm+1),pout(lpout),boty(im,jm),dout(im,jm,lpout)         
     *, pin(im,jm,lm+1),vten(lm+1)       
c         
      dimension yh(im,lm+1),pinh(im,lm+1),doh(im,lpout),poh(im,lpout)
c         
      imlm= im*lpout
c
cmic$ do all 
cmic$1 shared(im,jm,lm,lpout,y,boty,pin,dout,pout,imlm,vten)
cmic$1 private(j,k,i,poh,yh,pinh,doh)
      do 1 j=1,jm   
c
      do 5 k=1,lpout
      do 5 i=1,im   
      poh(i,k)= pout(k)       
    5 continue      
c
      do 4 i=1,im   
      yh(i,lm+1)= boty(i,j)   
      pinh(i,lm+1)= pin(i,j,lm+1)
    4 continue      
c
      do 2 k=1,lm   
      do 2 i=1,im   
      yh(i,k)= y(i,j,k)       
      pinh(i,k)= pin(i,j,k)   
    2 continue      
c
      call bcubvs(0,yh,im,lm+1,doh,imlm,pinh,poh,vten)
c
      do 6 k=1,lpout
      do 6 i=1,im   
      dout(i,j,k)= doh(i,k)   
    6 continue      
c
    1 continue      
      return        
      end 
