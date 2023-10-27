      subroutine wpclip120 (ymdh,la0,lo0,int1,dir1,spd1,ltlnwnd)
cx    WESTERN NORTH PACIFIC 120 HOUR CLIPER
c     
c     derived from program written by Sim Aberson
c     NOAA/AOML/Hurricane Research Division
c     26-JAN-2000
cx
cx    modified subsantially to be a subroutine, run on ATCF3.4   
cx						sampson nrl, jan 00
cx
cx    Parameters Passed In
cx         ymdh = year month day hour in integer format
cx         la0  = current latitude (degrees) 
cx         lo0  = current longitude (degrees)  
cx         int1 = intensity (knots)
cx         dir1 = storm direction of motion (12 hour)
cx         spd1 = storm speed (knots)
cx    Parameters Passed Back 
cx         ltlnwnd = array of cliper forecast lats and lons
cx                  12,24,36,48,60,72,84,96,108,120
cx
      include 'dataioparms.inc'

cx    character*4 coma
cx    character*14 yymmddhh,yymmddhh2
      character*8 cmdh
      parameter(nvar=27)
      parameter(nva1=28)
      integer yy,mm,dd,hh,int1,dir1,spd1
      real rlat,rlon,wind,days,ucmp,vcmp,jday(12),
     1     x(nvar),coef(20,nva1),disp(20)
      integer ltlnwnd(numtau,llw)
cx
      integer ymdh
      real la0,lo0
      common/block120/acon(20),
     1          co1(nva1) ,co2(nva1) ,co3(nva1) ,co4(nva1) ,co5(nva1),
     2          co6(nva1) ,co7(nva1) ,co8(nva1) ,co9(nva1) ,co10(nva1),
     3          co11(nva1),co12(nva1),co13(nva1),co14(nva1),co15(nva1),
     4          co16(nva1),co17(nva1),co18(nva1),co19(nva1),co20(nva1)

cx      
      data jday /1.,32.,60.,91.,121.,152.,182.,213.,244.,274.,305.,335./


c100  format(2x,a4,4i2,2i4,16x,i3,3x,2i3)
c102  format(3i2,13(f8.2,1x))
c103  format(3i2,7(f8.2,1x))
cx    yymmddhh='90ALIP        '
cx    yymmddhh2='91ELIP        '
c1200 format(5(5(1x,f12.9)/),3(1x,f12.9))
cx
cx  split out year, month, day and hour
cx
      write (cmdh,'(i8)')ymdh
      read  (cmdh,'(4i2)')yy,mm,dd,hh
cx
cx  get the lat and lon in tenths of degrees
cx
      lat1=la0*10
      lon1=lo0*10

cx    do i=1,20
cx      read(9,1200)acon(i),(coef(i,j),j=1,nvar+1)
cx    end do
cx
cx  assign the big regression coefficients array ...
cx
      do j=1,nva1
	coef(1,j) =co1(j)
	coef(2,j) =co2(j)
	coef(3,j) =co3(j)
	coef(4,j) =co4(j)
	coef(5,j) =co5(j)
	coef(6,j) =co6(j)
	coef(7,j) =co7(j)
	coef(8,j) =co8(j)
	coef(9,j) =co9(j)
	coef(10,j)=co10(j)
	coef(11,j)=co11(j)
	coef(12,j)=co12(j)
	coef(13,j)=co13(j)
	coef(14,j)=co14(j)
	coef(15,j)=co15(j)
	coef(16,j)=co16(j)
	coef(17,j)=co17(j)
	coef(18,j)=co18(j)
	coef(19,j)=co19(j)
	coef(20,j)=co20(j)
      end do
c
c     input line -- use whatever format you like.  This is old atcf format
c       yy is two digit year
c       mm is two digit month
c       dd is two digit day
c       hh is two digit hour
c       lat1 is integer latitude*10, positive north
c       lon1 is integer longitude*10, positive east
c       int1 is integer maximum sustained wind speed in kn
c       dir1 is integer direction of motion in degrees
c       spd1 is integer speed of motion in knots
c
c10   read(11,100,err=11,end=99)coma,yy,mm,dd,hh,lat1,lon1,int1,
cx   1                          dir1,spd1
cx    if(coma.ne.'COMA')goto 10
      rlat=real(lat1)/10.
      rlon=real(lon1)/10.
      wind=int1*111.1*1000./(60.*3600.)
      days=jday(mm)+real(dd)+real(hh)/24.
      rdir=dir1+180.
      if(rdir.ge.360.)rdir=rdir-360.
      rspd=spd1*111.1*1000./(60.*3600.)
      call uvcomp(rdir,rspd,ucmp,vcmp)
c      ucmp=-ucmp
      x(1)=rlat
      x(2)=rlon
      x(3)=wind
      x(4)=days
      x(5)=vcmp
      x(6)=ucmp
      klij=6
      do ijkl=1,6
        do jkli=ijkl,6
          klij=klij+1
          x(klij)=x(ijkl)*x(jkli)
        end do
      end do
      do i=1,20
        disp(i)=acon(i)
      end do
      do i=1,20
        do j=1,nvar
          disp(i)=disp(i)+x(j)*coef(i,j)
        end do
      end do
cx    write(yymmddhh(7:8),'(i2)')yy
cx    write(yymmddhh(9:10),'(i2)')mm
cx    write(yymmddhh(11:12),'(i2)')dd
cx    write(yymmddhh(13:14),'(i2)')hh
cx    if(mm.lt.10)yymmddhh(9:9)='0'
cx    if(dd.lt.10)yymmddhh(11:11)='0'
cx    if(hh.lt.10)yymmddhh(13:13)='0'
cx    write(yymmddhh2(7:8),'(i2)')yy
cx    write(yymmddhh2(9:10),'(i2)')mm
cx    write(yymmddhh2(11:12),'(i2)')dd
cx    write(yymmddhh2(13:14),'(i2)')hh
cx    if(mm.lt.10)yymmddhh2(9:9)='0'
cx    if(dd.lt.10)yymmddhh2(11:11)='0'
cx    if(hh.lt.10)yymmddhh2(13:13)='0'
      lat12=lat1+int(disp(1)*10)
      lat24=lat12+int(disp(2)*10)
      lat36=lat24+int(disp(3)*10)
      lat48=lat36+int(disp(4)*10)
      lat60=lat48+int(disp(5)*10)
      lat72=lat60+int(disp(6)*10)
      lat84=lat72+int(disp(7)*10)
      lat96=lat84+int(disp(8)*10)
      lat108=lat96+int(disp(9)*10)
      lat120=lat108+int(disp(10)*10)
      disp(11)=disp(11)/cosd(real((lat1+lat12)/20.))
      disp(12)=disp(12)/cosd(real((lat12+lat24)/20.))
      disp(13)=disp(13)/cosd(real((lat24+lat36)/20.))
      disp(14)=disp(14)/cosd(real((lat36+lat48)/20.))
      disp(16)=disp(16)/cosd(real((lat60+lat72)/20.))
      disp(17)=disp(17)/cosd(real((lat72+lat84)/20.))
      disp(18)=disp(18)/cosd(real((lat84+lat96)/20.))
      disp(19)=disp(19)/cosd(real((lat96+lat108)/20.))
      disp(20)=disp(20)/cosd(real((lat108+lat120)/20.))
      lon12=lon1+int(disp(11)*10)
      lon24=lon12+int(disp(12)*10)
      lon36=lon24+int(disp(13)*10)
      lon48=lon36+int(disp(14)*10)
      lon60=lon48+int(disp(15)*10)
      lon72=lon60+int(disp(16)*10)
      lon84=lon72+int(disp(17)*10)
      lon96=lon84+int(disp(18)*10)
      lon108=lon96+int(disp(19)*10)
      lon120=lon108+int(disp(20)*10)
c
c     output in atcf-like line -- modify as needed
c
cx    write(*,101)yymmddhh,lat12,lon12,lat24,lon24,lat36,lon36,lat48,
cx   1            lon48,lat60,lon60
cx    write(*,101)yymmddhh2,lat72,lon72,lat84,lon84,lat96,lon96,lat108,
cx   1            lon108,lat120,lon120
c101  format(a14,10i4)
c11   goto 10
c99   stop
cx
cx  assign the ltlnwnd array
cx
      ltlnwnd(1,1) =lat12
      ltlnwnd(2,1) =lat24
      ltlnwnd(3,1) =lat36
      ltlnwnd(4,1) =lat48
      ltlnwnd(5,1) =lat60
      ltlnwnd(6,1) =lat72
      ltlnwnd(7,1) =lat84
      ltlnwnd(8,1) =lat96
      ltlnwnd(9,1) =lat108
      ltlnwnd(10,1)=lat120
      ltlnwnd(1,2) =lon12
      ltlnwnd(2,2) =lon24
      ltlnwnd(3,2) =lon36
      ltlnwnd(4,2) =lon48
      ltlnwnd(5,2) =lon60
      ltlnwnd(6,2) =lon72
      ltlnwnd(7,2) =lon84
      ltlnwnd(8,2) =lon96
      ltlnwnd(9,2) =lon108
      ltlnwnd(10,2)=lon120
      ltlnwnd(1,3) =0
      ltlnwnd(2,3) =0
      ltlnwnd(3,3) =0
      ltlnwnd(4,3) =0
      ltlnwnd(5,3) =0
      ltlnwnd(6,3) =0
      ltlnwnd(7,3) =0
      ltlnwnd(8,3) =0
      ltlnwnd(9,3) =0
      ltlnwnd(10,3)=0
      return
      end
cx******************************************************
cx
cx  computes u and v from speed and direction
cx
      subroutine uvcomp(dir,spd,u,v)
      degrad=atan(1.)/45.
      dirdg=270.-dir
      if(dirdg.lt.0.)then
        dirdg=dirdg+360.
      endif
      dirrd=dirdg*degrad
      u=spd*cos(dirrd)
      v=spd*sin(dirrd)
      return
      end
cx
cx*********************************************************************
cx
      block data blk120
cx
cx  block data contains regression coefficients for 120 hour cliper
cx
      parameter(nva1=28)
      common/block120/acon(20),
     1          co1(nva1) ,co2(nva1) ,co3(nva1) ,co4(nva1) ,co5(nva1),
     2          co6(nva1) ,co7(nva1) ,co8(nva1) ,co9(nva1) ,co10(nva1),
     3          co11(nva1),co12(nva1),co13(nva1),co14(nva1),co15(nva1),
     4          co16(nva1),co17(nva1),co18(nva1),co19(nva1),co20(nva1)
cx
cx    These are the ??? coefficients 
cx
      data acon /
     1  0.154036954,-1.888187408,-3.097655535, 0.237874597,-0.028722927,
     2 -3.956638575,-4.109622955,-3.894234896,-3.893000364,-3.683694839,
     3 -0.359974325,-0.838267028, 0.291460305, 0.350479245, 0.400820464,
     4 -1.842935801,-1.833651900,-1.812050819,-1.752319694,-0.164094508/
      data co1 /
     1               0.000000000, 0.000000000, 0.000000000, 0.000000000,
     2  0.299659699, 0.010402090, 0.000000000, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000006445, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.001322171, 0.000000000,-0.000002848, 0.000000000, 0.000000000,
     6  0.000000000, 0.002072340, 0.00000000,
     7  0.000000000/
      data co2 /
     1               0.000000000, 0.032345895, 0.000000000, 0.000000000,
     2  0.187385947, 0.000000000, 0.000000000, 0.000000000, 0.000180991,
     3  0.000000000, 0.000000000, 0.000000000,-0.000121482, 0.000000000,
     4  0.000016597, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.002435162, 0.000783775,-0.000006927, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co3 /
     1               0.000000000, 0.051695958, 0.000000000, 0.000000000,
     2  0.105390511, 0.022597207,-0.000460666, 0.000000000, 0.000854663,
     3  0.000000000, 0.000000000, 0.000000000,-0.000191097, 0.000000000,
     4  0.000025692, 0.000000000, 0.000000000,-0.000167834, 0.000000000,
     5  0.002782297, 0.000000000,-0.000010551, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co4 /
     1               0.000000000, 0.000000000, 0.000000000, 0.003313301,
     2  0.050760299, 0.048205744,-0.000608187, 0.000000000, 0.001034722,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000020217, 0.000000000, 0.000000000,-0.000158492, 0.000000000,
     5  0.002355158, 0.000000000,-0.000017052, 0.000000000, 0.000000000,
     6  0.000000000,-0.007194290, 0.002968729,
     7  0.000000000/
      data co5 /
     1               0.000000000, 0.000000000, 0.000000000, 0.006781749,
     2  0.000000000, 0.000000000,-0.001353879, 0.000280520, 0.000806417,
     3  0.000000000, 0.000000000, 0.002198229, 0.000000000, 0.000000000,
     4  0.000000000, 0.000000000, 0.000000000,-0.000112824, 0.000000000,
     5  0.002668055, 0.000000000,-0.000019116, 0.000000000, 0.000000000,
     6  0.000000000,-0.009762526, 0.000000000,
     7  0.000000000/
      data co6 /
     1               0.000000000, 0.068949744, 0.000000000, 0.000000000,
     2  0.000000000, 0.034633212, 0.000000000, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000,-0.000268106, 0.000052910,
     4  0.000047863, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.002332837, 0.000000000,-0.000019420, 0.000000000, 0.000000000,
     6  0.000000000,-0.006482060, 0.000000000,
     7  0.000000000/
      data co7 /
     1               0.000000000, 0.071424834, 0.000000000, 0.000000000,
     2  0.000000000, 0.021902628, 0.000000000, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000,-0.000278958, 0.000053609,
     4  0.000052553, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.002202633, 0.000000000,-0.000021362, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co8 /
     1               0.000000000, 0.068709709, 0.000000000, 0.000000000,
     2  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.001298790,-0.000273128, 0.000057786,
     4  0.000058188, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.001893963, 0.000000000,-0.000023576, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co9 /
     1               0.000000000, 0.068829373, 0.000000000, 0.000000000,
     2  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.001358749,-0.000273301, 0.000055144,
     4  0.000060852, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.001739874, 0.000000000,-0.000024755, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co10/
     1               0.000000000, 0.067046151, 0.000000000, 0.000000000,
     2  0.000000000, 0.000000000, 0.000000000, 0.000000000,-0.000519409,
     3  0.000000000, 0.000000000, 0.000000000,-0.000276842, 0.000138001,
     4  0.000067689, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.001868455, 0.001124266,-0.000027384, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co11/
     1               0.041687567, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.391013771, 0.000000000,-0.000187248, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000000000,-0.000134495,-0.000358266, 0.000000000, 0.000000000,
     5  0.001625416, 0.000926464, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.002153437,
     7  0.000000000/
      data co12/
     1               0.093471140, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.366746575, 0.000000000,-0.000423460, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000000000,-0.000231706,-0.000679689, 0.000000000, 0.000000000,
     5  0.003897411, 0.001832656, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.003734221,
     7  0.000000000/
      data co13/
     1               0.000000000, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.481332451, 0.001197655, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000,-0.000056334, 0.000000000,
     4  0.000000000, 0.000000000,-0.001932982, 0.000000000, 0.000000000,
     5  0.005049936, 0.001739235, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.002664932,
     7  0.000000000/
      data co14/
     1               0.000000000, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.488367707, 0.001541445, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000,-0.000068962, 0.000000000,
     4  0.000000000, 0.000000000,-0.002366217, 0.000000000, 0.000000000,
     5  0.006185836, 0.001289445, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co15/
     1               0.000000000, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.504965663, 0.001737921, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000,-0.000077014, 0.000000000,
     4  0.000000000, 0.000000000,-0.002572762, 0.000000000, 0.000000000,
     5  0.006700626, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co16/
     1               0.235681891, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.295948505, 0.000000000,-0.001138776, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000000000, 0.000000000,-0.001339637, 0.000000000, 0.000000000,
     5  0.006901512, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co17/
     1               0.219412148, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.078755677, 0.000000000,-0.001010515, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.006895849, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co18/
     1               0.234244242, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.052666880, 0.000000000,-0.001109461, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.006913775, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000, 0.000000000,
     7  0.000000000/
      data co19/
     1               0.244210362, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.000000000, 0.000000000,-0.001180397, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     4  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.006860228, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000,-0.005295991,
     7  0.000000000/
      data co20/
     1               0.066412561, 0.000000000, 0.000000000, 0.000000000,
     2  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     3  0.000000000, 0.000000000, 0.000000000,-0.000064242, 0.000000000,
     4  0.000000000, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     5  0.006721725, 0.000000000, 0.000000000, 0.000000000, 0.000000000,
     6  0.000000000, 0.000000000,-0.004445432,
     7  0.000000000/
      end
cx------------------------------------------------------------------------
