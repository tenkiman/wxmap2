      subroutine dftouv(dd,ff,uu,vv)
c
c          subroutine to convert direction and speed to earth-
c          oriented u and v components
c
      phi=dd*0.017453292
      uu=-sin(phi)*ff
      vv=-cos(phi)*ff
c
      return
      end
