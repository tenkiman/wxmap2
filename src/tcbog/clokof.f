      subroutine clokof(time)
c
c  **-neprf-** programmer tom rosmond- date 24 jun 1987
      common/clok/ clkstk(20),jstk
      data jstk/0/
c
      time2= second()
      time= time+time2-clkstk(jstk)
      jstk= jstk-1
      return
      end
