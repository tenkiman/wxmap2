      subroutine clokon(time)
c
      common/clok/ clkstk(20),jstk
      jstk= jstk+1
      clkstk(jstk)= second()
      return
      end
