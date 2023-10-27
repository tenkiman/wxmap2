      subroutine uvtodf(uu,vv,dd,ff)
c
c          subroutine to convert earth-oriented u and v
c          components to direction and speed
c
      ff=sqrt(uu*uu+vv*vv)
      if (uu.eq.0.0) uu=1.0e-10
      chi=atan2(vv,uu)*57.29577951
      dd=270-chi
      if (dd.gt.360.0) dd=dd-360.0
      return
      end
