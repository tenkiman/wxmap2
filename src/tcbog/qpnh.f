      subroutine qpnh(fld,title,i1,j1,im,jm)        
c
c  this is a vectorized version of qpn  
c         
      dimension fld(im,jm)    
      character*16 title
c
      xmin= 1.0e35  
      xmax= -1.0e35
      imin=1
      jmin=1
      imax=1
      imin=1
      ii= im-i1+1
c         
      do 10 j=j1,jm
      ix= ismin(ii,fld(i1,j),1)
      if(fld(ix,j).lt.xmin) then      
      xmin= fld(ix,j)
      jmin= j
      imin= ix      
      endif         
      ix= ismax(ii,fld(i1,j),1)
      if(fld(ix,j).gt.xmax) then      
      xmax= fld(ix,j)       
      jmax= j
      imax= ix       
      endif         
   10 continue      
      
c         
      print 8995, title,imax,jmax,xmax,imin,jmin,xmin   
 8995 format(1h0,a16,': imax=',i4,' jmax=',i4,' xlarg=',g15.8        
     *,' imin=',i4,' jmin=',i4,' xsmal=',g15.8)   
      return        
      end 
