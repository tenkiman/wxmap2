      subroutine rumltlg(course,distance,rlat0,rlon0,rlat1,rlon1)
c
c****       routine to calculate lat,lon after traveling "dt" time
c****       along a rhumb line specifed by the course and speed
c****       of motion
c             
c*****************            longitude is in degree west
c      
CCCC input distance (nm)      distance=speed*dt
c
c...     now find the lat/long point dt hours away along
c...     this course and heading
c         
      logical degeast

      degeast=.true.

      rad=4.0*atan(1.0)/180.0
      radinv=1.0/rad
      icrse=ifix(course+0.01)
c
      if(icrse.eq.90.or.icrse.eq.270) then
c      
c*****            take care of due east and west motion
c
        dlon=distance/(60.0*cos(rlat0*rad))

        if(degeast) then
          if(icrse.eq.90) rlon1=rlon0+dlon
          if(icrse.eq.270) rlon1=rlon0-dlon
        else
          if(icrse.eq.90) rlon1=rlon0-dlon
          if(icrse.eq.270) rlon1=rlon0+dlon
        endif

        rlat1=rlat0
c
      else
c
        rlat1=rlat0+distance*cos(course*rad)/60.0
        d1=(45.0+0.5*rlat1)*rad
        d2=(45.0+0.5*rlat0)*rad
        td1=tan(d1)
        td2=tan(d2)
        rlogtd1=alog(td1)
        rlogtd2=alog(td2)
        rdenom=rlogtd1-rlogtd2 
        if(degeast) then
          rlon1=rlon0+(tan(course*rad)*rdenom)*radinv
        else
          rlon1=rlon0-(tan(course*rad)*rdenom)*radinv
        endif
c
      endif
c
      return
      end
