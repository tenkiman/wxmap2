      subroutine noday(cidtg,my,mhy)         
c        
      character*8 cidtg
      dimension month(12,2)   
      data month/0,31,59,90,120,151,181,212,243,273,304,334,
     $           0,31,60,91,121,152,182,213,244,274,305,335/
c
c  given --         
c     my = last 2 digits of year        
c     mhy= hour of the year   
c         
c  return ascii dtg (yymmddhh) in idtg  
c         
      j = 1         
      mdy = mhy/24+1
      if(mod(my,4).eq.0) j = 2
      kk=0
      do 2 i = 2,12 
      kk=kk+1       
      if(mdy.le.month(i,j)) go to 3     
 2    continue      
      kk=kk+1       
 3    mm = kk       
      mh = mod(mhy,24)        
      md = mdy-month(mm,j)    
      write(cidtg,1)  my,mm,md,mh      
    1 format(4i2)
      do 5 i = 1,8  
      if(cidtg(i:i).eq.' ') cidtg(i:i)='0'    
 5    continue      
c         
      return        
      end 
