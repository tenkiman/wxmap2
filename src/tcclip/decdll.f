      subroutine decdll (ltln,latlon,nsew)
      character ltln*10,nsew*1,fmt*6

      real latlon

c  this subroutine extracts the latitude/longitude from the input string
c  ltln.  it accomplishes this by reading each character until an error
c  occurs or the end of the string is reached.  if an error occurs, a 
c  non-numeric character (other than a decimal) exits. save it to the
c  nsew indicator and read the entire number before it. 
c    by doing this, the lat/long entry is not a fixed format.

c     call prctrc('decdll',.true.)


      i = 1
  100 read (ltln(i:i),'(i1)',err=200) itest
      i = i + 1
      if (i .lt. 10) then
         goto 100
      else

c  if the whole string was searched and no non-numeric character was found
c  (other than a decimal), store a blank in nsew.

         nsew = ' '
         goto 900
      endif
  200 continue

c  to get to here, you need at least 2 characters. otherwise, exit.

      if (i .le. 1) then
         nsew = ' '
         goto 900
      endif

c  ignore decimals

      if (ltln(i:i) .eq. '.') then
         i = i + 1
         goto 100
      endif

c  store the non-numeric character into nsew 

      nsew = ltln(i:i)

c  must create a format to read the real variable because the length
c  can change. although the format specifies no decimal places, a
c  decimal in the input will overide this

      write (fmt,'(''(f'',i1,''.0)'')') i-1

c  store the value preceeding the non-numeric character into latlon

      read (ltln(1:i-1),fmt) latlon
  900 continue

c     call prctrc('decdll',.false.)

      return
      end
