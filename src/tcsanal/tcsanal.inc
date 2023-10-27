      parameter (ni=360,nj=181,nk=2,ntcf=13,ntcs=5)
      parameter(dlat=1.0,dlon=1.0,rearth=6363*1e3)

      parameter(dphi=10.0,nphi=nint(360.0/dphi))
      parameter(dr=10.0,rmax=1000.0,nr=nint(rmax/dr)+1,dt=12.0,speed=dr/dt)
      parameter(nq=5)

      real tclat,tclon,tcstruct,
     $     ur,vr,lat,lon,ucb,vcb,scb,dum1,dum2
      integer nb

      common /struct/ 
     $     tclat(ntcf),tclon(ntcf),tcstruct(ntcs),
     $     ur(nr,nphi),vr(nr,nphi),lat(nphi),lon(nphi),
     $     ucb(nr,nq),vcb(nr,nq),scb(nr,nq),
     $     dum1(ni,nj),dum2(ni,nj),
     $     nb(nq)

