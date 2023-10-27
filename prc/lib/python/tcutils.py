
def gc_dist(rlat0,rlon0,rlat1,rlon1):

    #
    # based on sherical law of cosines 
    #
    
    dlat=abs(rlat0-rlat1)
    dlon=abs(rlon0-rlon1)
    zerotest=(dlat<epsilon and dlon<epsilon)
    if(zerotest): return(0.0)
    
    f1=deg2rad*rlat0
    f2=deg2rad*rlat1
    rm=deg2rad*(rlon0-rlon1)
    finv=cos(f1)*cos(f2)*cos(rm)+sin(f1)*sin(f2)
    rr=rearth*acos(finv)
    if(tcunits =='english'): rr=rr*km2nm 

    return(rr)


def mercat(rlat,rlon):

    lat=rlat*deg2rad

    if(rlon < 0.0):
        lon=360.0+rlon
    else:
        lon=rlon
        
    x=lon*deg2rad
    y=log(tan(pi4+lat*0.5))

    return(x,y)

def gc_theta(blat1,blon1,flat1,flon1):

    verb=0
    (xa,ya)=mercat(flat1,flon1)
    (xr,yr)=mercat(blat1,blon1)

    difx=xa-xr
    dify=ya-yr

    difx=difx*rad2deg*deglat2nm
    dify=dify*rad2deg*deglat2nm

    if (difx == 0.0):

        if(dify >= 0.0): theta=pi2
        if(dify < 0.0): theta=3*pi/2.0 

    else:

        slope=dify/difx
        if (abs(slope) < 1e-10):
            if(dify >= 0.0): theta=pi2 
            if(dify <= 0.0): theta=pi
        else:
            theta=atan2(dify,difx)
            #if(theta < 0.0):
            #   theta=theta + 2.0*pi
            theta=theta*rad2deg
            return(difx,dify,theta)
        
            if (difx > 0.0):
                if(dify < 0.0): theta=pi-theta
            else:
                if (dify > 0.0):
                    theta=2*pi+theta
                    theta=theta
                else:
                    theta=pi+theta
                    theta=theta

    
    #if(theta < 0.0):
    #    theta=theta + 2.0*pi

    theta=theta*rad2deg
    return(difx,dify,theta)


def dist_err(blat,blon,blat1,blon1,flat,flon):

    verb=0
    (xa,ya)=mercat(flat,flon)
    (xb,yb)=mercat(blat,blon)
    (xr,yr)=mercat(blat1,blon1)

    difx=xb-xr
    dify=yb-yr

    if (difx == 0.0):

      if(dify >= 0.0): theta=0.0
      if(dify < 0.0): theta=pi 

    else:

      slope=dify/difx
      if (abs(slope) < 1e-10):
          if(difx > 0): theta=pi2 
          if(difx < 0): theta=3*pi/2.0
      else:
        theta=atan(1./slope)
        if (difx > 0.0):
          if(dify < 0.0): theta=pi-theta
        else:
           if (dify > 0.):
             theta=2*pi+theta
           else:
             theta=pi+theta

    biasx=cos(theta)*(xa-xb)-sin(theta)*(ya-yb)
    biasy=sin(theta)*(xa-xb)+cos(theta)*(ya-yb)
    factor=cos(deg2rad*(blat+flat)*0.5)
    biasx=biasx*rearth*factor
    biasy=biasy*rearth*factor

    biasew=(xa-xb)*rearth*factor
    biasns=(ya-yb)*rearth*factor
    rr=sqrt(biasx*biasx+biasy*biasy)
    #dist_x=abs(biasx)
    #dist_y=abs(biasy)

    if(tcunits =='english'):
        rr=rr*km2nm
        biasx=biasx*km2nm
        biasy=biasy*km2nm
        biasew=biasew*km2nm
        biasns=biasns*km2nm
        

    if(verb):
        print "mmm ",blat,blon,flat,flon,rr,biasx,biasy

    return(rr,biasx,biasy,biasew,biasns)


def rumltlg(course,speed,dt,rlat0,rlon0):

    ####  print "qqq course,speed,dt,rlat0,rlon0\n"
    #c****	    routine to calculate lat,lon after traveling "dt" time
    #c****	    along a rhumb line specifed by the course and speed
    #c****	    of motion
    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #  assume speed is in kts and dt is hours
    #
    #      
    distnce=speed*dt
    
    icrse=int(course+0.01)

    if(icrse == 90.0 or icrse == 270.0):

    #      
    #*****		  take care of due east and west motion
    #
        dlon=distnce/(60.0*cos(rlat0*deg2rad))
        if(icrse == 90.0): rlon1=rlon0+dlon
        if(icrse == 270.0): rlon1=rlon0-dlon 
        rlat1=rlat0
    else:
        rlat1=rlat0+distnce*cos(course*deg2rad)/60.0
        d1=(45.0+0.5*rlat1)*deg2rad
        d2=(45.0+0.5*rlat0)*deg2rad
        td1=tan(d1)
        td2=tan(d2)
        #
        # going over the poles!
        #
        if(abs(rlat0) >= 90.0 or abs(rlat1) >= 90.0):
            rlat1=rlon1=None
        else:
            rlogtd1=log(td1)
            rlogtd2=log(td2)
            rdenom=rlogtd1-rlogtd2 
            rlon1=rlon0+(tan(course*deg2rad)*rdenom)*rad2deg

    return(rlat1,rlon1)


def rumhdspi(rlat0,rlon0,rlat1,rlon1,dt):

    verb=0

    if(verb):
        print rlat0,rlon0,rlat1,rlon1,dt,units
        
    if(tcunits == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60
        spdfac=1.0
    
    rnumtor=(rlon0-rlon1)*deg2rad
    rnumtor=(rlon1-rlon0)*deg2rad
    
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom
    course=0.0
    
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):
        course=360.0+course

    icourse=int(course+0.1)
    
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))
        
    speed=distance/dt

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad
    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    if(verb): print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f"%(distance,icourse,spdmtn,angle,umotion,vmotion)
####    print "%5.2f %5.2f"%(icourse,spdmtn)

    return(course,speed,iumotion,ivmotion)


def rumhdsp(rlat0,rlon0,rlat1,rlon1,dt,units=tcunits,opt=0):

    verb=0

    if(verb):
        print "***** ",rlat0,rlon0,rlat1,rlon1,dt,units,opt

    if(units == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60.0
        spdfac=1.0


    #
    # assumes deg W
    #
    rnumtor=(rlon0-rlon1)*deg2rad

    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #

    rnumtor=(rlon1-rlon0)*deg2rad
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom

    course=0.0
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):  
        course=360.0+course

    #
    #...     now find distance
    #

    icourse=int(course+0.1)
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))

    #
    #...     now get speed
    #
    speed=distance/dt

    #
    #...      convert to u and v motion
    #

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad
    
    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    rumotion=float(iumotion)
    rvmotion=float(ivmotion)
    rcourse=float(course)
    rspeed=float(spdmtn)
    if(verb):
        print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n"%\
              (distance,icourse,spdmtn,angle,umotion,vmotion)
        
    return(rcourse,rspeed,umotion,vmotion)



