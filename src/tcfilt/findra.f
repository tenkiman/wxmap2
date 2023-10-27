      subroutine findra(dxc,dyc,yc,rmxavg,rfind,tanuv)
      
      include 'params.h'
c
c  finds rfind from azimuthally averaged radial profile of tang. wind
c         

      dimension tanuv(ini)

      include 'const.h'

      dr=0.1

      dist= rmxavg*1.5
      x1 = 0.0
      rtan1 = 100000.
      r = 1.0
      r=dist
c         
c         only come back to 666 if rtan > 6m/s
c         

 666  continue

      rtan1=100000.
c
c  return to 777 if gradient, dist, or 3m/s are unmet
c

 777  continue

      r = r + dr
      irad= int(r/dr)
      rtan= tanuv(irad)
      
      rtan2 = rtan
      if(rtan.gt.3.) go to 666
c
      if(rtan2.ge.rtan1.and.r.gt.dist.and.x1.gt.0.5) go to 999

      if(rtan2.ge.rtan1.and.r.gt.dist) then
        x1 = 1.0
      endif

      if(rtan.lt.3..and.r.gt.dist) go to 999
      rtan1 = rtan - 4.0
      if(r.lt.10.8) go to 777

 999  continue
      
      rfind=r
      
      return
      end
