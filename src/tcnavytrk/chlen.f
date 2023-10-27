      subroutine chlen(file,lenc)
      character*1 file(*)
      character*1 blnk1
      data blnk1/' '/
      lenc= 0
      do 1 i=1,100
      if(file(i).eq.blnk1) return  
      lenc= i
    1 continue
      return
      end
