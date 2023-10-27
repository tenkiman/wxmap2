      subroutine gbland(clon,clat,dtl)
c     This program estimates the distance to the nearest land mass
c     using the aland, wland and shland programs. 
c
c     This version is global. 
c     Input:  
c       clon - Longitude in deg E. It can be in either 0 to 360 deg convention,
c              or 0 to 180 for deg E, and -180 to 0 for deg W.
c       clat - Latitude in deg N. clat is negative for southern hemisphere points.
c
c     Output:
c       dtl - Distance (km) to the nearest major landmass. dtl is negative for
c             inland points, and positive to over water points. 
c
c       Calculate clon where deg W is negative.
        clondwn = clon
        if (clon .gt. 180.0) then
           clondwn = clon - 360.0
        else
           clondwn = clon
        endif
c
        if (clat .lt. 0.0) then
           call shland(clondwn, clat, dtl)
        else
           if (clondwn .gt. 0.0) then
              call wland(clondwn, clat, dtl)
           else
              call aland(clondwn, clat, dtl)
           endif
        endif
c
        return
        end
