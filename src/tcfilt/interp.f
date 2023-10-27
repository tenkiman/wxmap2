       subroutine interp(uo,vo,sigp,ilev,un,vn)
c
       parameter ( kmax = 18, ilt=20 )
c
       dimension  uo(ilt),vo(ilt)
       dimension  sigp(ilt),q(kmax)
       dimension  un(kmax),vn(kmax)
       dimension  uf(kmax),vf(kmax)
c
       data q/ .9949968,.9814907,.9604809,.9204018,.8563145,.7772229,
     *           .6881255,.5935378,.4974484,.4248250,.3748014,.3247711,
     *           .2747291,.2246687,.1745733,.1244004,.0739862,.0207469/
c
       tmask = 1.0e20
c
       ilevm = ilev -1
       if(ilev.lt.2)then
       do kk = 1,kmax
          un(kk) = tmask
          vn(kk) = tmask
       end do
       return
       endif
       do 10 kk = 1 , ilevm
c
       sgo1 = sigp(kk)
       sg02 = sigp(kk+1)
c
       do 20 k  = 1 ,  kmax
c
       sgn = q(k)
       if(sgn.gt.sigp(1))then
       uf(k) = tmask
       vf(k) = tmask
       endif
       if(sgn.lt.sigp(ilev))then
       uf(k) = tmask
       vf(k) = tmask
       endif
c
       if(sgn.le.sgo1.and.sgn.ge.sg02)then
       dx  = sgo1  - sg02
       dx1 = sgo1  - sgn
       dx2 = sgn  - sgo2
       x1 = dx1/dx
       x2 = dx2/dx
       uf(k) = (1.-x1)*uo(kk) + x1*uo(kk+1)
       vf(k) = (1.-x1)*vo(kk) + x1*vo(kk+1)
       endif
c
20     continue
10     continue
       do 30 k = 1 , kmax
       kk = kmax + 1 - k
       un(k) = uf(kk)
       vn(k) = vf(kk)
30     continue
       return
       end
