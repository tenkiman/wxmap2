      subroutine readtcstruct(iunit,tcstruct,ns)
      include 'params.h'

      real tcstruct(ns)
      character card*80 
      read(iunit,('(a)')) card
      read(iunit,('(4x,12(f4.0,1x))')) (tcstruct(i),i=1,ns)
      if(verb) then
        print*,'SSSSSSS: ',card
        print*,'SSSSSSS: ',tcstruct
      endif
      return
      end
      
      
      

