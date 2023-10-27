      subroutine dtgfix(cidtg,cndtg,ndif)         
c         
c         
c********************************************************** 
      character*8 cidtg, cndtg    
      dimension myc(4)        
      data myc/8784,3*8760/   
      call daynum(cidtg,my,mm,md,mh,mdy,mhy)       
c         
c  increment (decrement) hour of the year (mhy) by ndif,    
c   test for change of year, adjust if necessary, reform to ndtg      
c         
      if(my.eq.0) my= 100
      newmhy = mhy+ndif       
      if(newmhy.ge.0) go to 10
 1    my = my-1     
      idx = mod(my,4)+1       
      newmhy = myc(idx)+newmhy
      if(newmhy.ge.0) go to 20
      go to 1       
c         
 10   idd = mod(my,4)+1       
      if(newmhy.lt.myc(idd)) go to 20   
      newmhy = newmhy-myc(idd)
      my= my+1
      go to 10      
c         
   20 my= mod(my,100)           
      call noday(cndtg,my,newmhy)        
      return        
      end 
