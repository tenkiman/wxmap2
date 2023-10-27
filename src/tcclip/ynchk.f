      function ynchck (answer)
      logical ynchck
      character answer*1 
c
c  this logical function returns true if answer is a y or n and false
c  if it is not
c
      ynchck = .false.
      if (answer .eq. 'Y' .or. answer .eq. 'y' .or. 
     &    answer .eq. 'N' .or. answer .eq. 'n') ynchck = .true.
      return
      end
