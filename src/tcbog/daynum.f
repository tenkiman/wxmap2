      subroutine daynum(cidtg,my,mm,md,mh,mdy,mhy)
c         
c***********************************************************
c         
      character*8 cidtg         
c         
      dimension month(12,2)   
      data month/0,31,59,90,120,151,181,212,243,273,304,334,
     $           0,31,60,91,121,152,182,213,244,274,305,335/
c         
      read(cidtg,1)  my,mm,md,mh      
 1    format(4i2)   
      j = 1         
      if(mod(my,4).eq.0) j = 2
      mdy = month(mm,j)+md    
      mhy = (mdy-1)*24+mh     
      return        
      end
