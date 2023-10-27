      subroutine tpose(x,im,jm,y)       
      dimension x(im,jm),y(jm,im)       
      do 1 i=1,im   
      do 1 j=1,jm   
    1 y(j,i)= x(i,j)
      return        
      end 
