      subroutine constants(iopt)

      common /const/pi,deg2rad,rad2deg,ms2kt,m2ft

      pi=4.0*atan(1.0)
      deg2rad=pi/180.0
      rad2deg=180.0/pi
      m2ft=3.2808
      ms2kt=1.944

      
      return
      end
