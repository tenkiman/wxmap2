      subroutine locase (string,nchar)
 
c  this routine converts all upper case characters (ascii 65 - 90)
c  in the variable string to lower case characters (ascii 97 - 122).
 
      character string*(*)
 
c  loop thru each character in the string
 
      do 100 i=1,nchar
 
c  if it is upper case, add 32 from it to make it lower case.
 
      ich = ichar(string(i:i))
      if ((ich .gt. 64) .and. (ich .lt. 91)) string(i:i) = 
     &         char(ichar(string(i:i))+32)
  100 continue
      return
      end
 
