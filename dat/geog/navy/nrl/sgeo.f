      program nogaps_geog

CLLLLLLLLLLLLLLLLLLLLLLL         
C         LATS include
CLLLLLLLLLLLLLLLLLLLLLLL         
ccc      include "/usr/local/lats/include/lats.inc"
      include "lats.inc"
CLLLLLLLLLLLLLLLLLLLLLLL         

ccc      parameter (im=192,jm=94,igridg=1)
ccc      parameter (im=144,jm=im/2,igridg=1)
ccc       parameter (im=144,jm=73,igridg=0)
      parameter (im=360,jm=181,igridg=0)
      parameter (jtrun= 2*((1+im/3)/2),mlmax=jtrun*(jtrun+1)/2)
      parameter (idim2= mlmax*2)
c
      common/terr/ xt(im,jm),xtm(im,jm)
      dimension ils(im,jm),rls(im,jm)
      dimension sgeo(mlmax,2,5)
c
      dimension weight(jm),sinl(jm)
c
      common/imptop/ itopo(2160,1080),ils1(2160,1080)
c
      parameter (imjm= im*jm)
c
      dimension mlsort(jtrun,jtrun),msort(mlmax),lsort(mlmax)
c         
      character*48 gsstfil,galbfil,gwetfil,glz0fil,tsstfil,tclimfil
     *, topofil,tdevfil,ilsfil,spgeo

      character*8 cdtg

CLLLLLLLLLLLLLLLLLLLLLLL         
C         LATS setup
CLLLLLLLLLLLLLLLLLLLLLLL         

      parameter(nv=3)

      character*20 center
      character*20 model
      character*9 var
      dimension var(nv),id_var(nv)
      double precision rlon(im),rlat(jm),slev

      data center/'PCMDI'/
      data model/'nrl'/

      data var/'orog','sftlf','sftlf'/ 
C         
C         constants
C
      pi= 4.0*atan(1.0)
      r2d=(180.0/pi)

CLLLLLLLLLLLLLLLLLLLLLLL         
C         LATS definition
CLLLLLLLLLLLLLLLLLLLLLLL         

      id_parmtab=
     $     latsparmtab("/usr/local/lats/table/amip2.lats.table")
      if(id_parmtab.eq.0) stop 'latsparmtab error'

      iconv=LATS_COARDS
      iconv=LATS_GRADS_GRIB

ccc      id_fil = latscreate('geo.t62.eqlonlat',
      id_fil = latscreate('geo.1deg',
     $     iconv,
     $     LATS_STANDARD,
     $     LATS_FIXED,1,center,
     $     model,'geog based on Navy 10 min'//
     $     ' using equal lon lat boxes')
      print*,'LATS grib file id = ',id_fil

      do i=1,im
        rlon(i)=0.0+(i-1)*360.0/im
      end do
      
      if(igridg.eq.1) then
C         
C         get gauss wieghts
C         
        call gausl3(jm,-1.0,1.0,weight,sinl)
        do j=1,jm
          rlat(j)=asin(sinl(j))*r2d
        end do
        igridconv=LATS_GAUSSIAN
      else
        do j=1,jm
          rlat(j)=-90.0+(j-1)*180.0/(jm-1)
        end do
        igridconv=LATS_LINEAR
      endif

      id_grd=latsgrid("navygeog",igridconv, im, rlon, jm, 
     $     rlat)

      print*,'LATS grid id = ',id_grd

      id_var(1)=latsvar(id_fil,var(1),
     $     LATS_FLOAT,LATS_INSTANT,id_grd,
     $     0, 'navy 10 min topo')

      print*,'LATS var id 1 = ',id_var(1)
      
      id_var(2)=latsvar(id_fil,var(2),
     $     LATS_FLOAT,LATS_INSTANT,id_grd,
     $     0, 'navy 10 min land sea')
	
      print*,'LATS var id 2 = ',id_var(2)

CLLLLLLLLLLLLLLLLLLLLLLL         

      open(69,file='geo.t62.dat',form='unformatted',
     $     status='unknown')
c
      gsstfil='gsstfil'
      galbfil='galbfil'
      gwetfil='gwetfil'
      glz0fil='glz0fil'
      tsstfil='tsstfil'
      tclimfil='tclimfil'
      topofil='topofil'
      tdevfil='tdevfil'
      ilsfil='ilsfil'
      spgeo= '/home/rosmond/spgeo                        '
      spgeo= 'mfgeo                                      '

      itestl=0
      if(itestl.ne.1) then
c
c  read in climo data
c
        len= 2160*1080
        call nfread(topofil,1,-1,1,1,len,
     $       itopo,-1,cdtg,istat)
        call nfread(ilsfil,1,-1,1,1,len,
     $       ils1,-1,cdtg,istat)
        call sortml(jtrun,mlmax,msort,lsort,mlsort)
        call topo(itopo,ils1,xt,xtm,ils,rls,
     $       sinl,weight,mlsort
     *       ,lsort,sgeo)
C         
C         mike output
C
        write(69) xt
        write(69) xtm
        do i=1,im
          do j=1,jm
            xtm(i,j)=float(ils(i,j))
            rls(i,j)=rls(i,j)*100.0
          end do
        end do

        write(69) xtm
        write(69) rls

      else
        
        read(69) xt
        read(69) xtm
        read(69) xtm
        read(69) rls

      endif


CLLLLLLLLLLLLLLLLLLLLLLL         
C         LATS write
CLLLLLLLLLLLLLLLLLLLLLLL         

      slev=0.0D0
      ierr=latswrite(id_fil,id_var(1),slev,
     $     iyr,imo,ida,ihr,xt)
      if(ierr.eq.0) stop 'latswrite error - var 1'

      ierr=latswrite(id_fil,id_var(2),slev,
     $     iyr,imo,ida,ihr,rls)
      if(ierr.eq.0) stop 'latswrite error - var 2'

CLLLLLLLLLLLLLLLLLLLLLLL         



CRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
C         Rosmond output

C         call nfwrit(spgeo,2,-2,1,5,idim2,sgeo,-1,cdtg,istat)
C         
CRRRRRRRRRRRRRRRRRRRRRRRRRRRRR

 999  continue

CLLLLLLLLLLLLLLLLLLLLLLL         
C         LATS close
CLLLLLLLLLLLLLLLLLLLLLLL
      ierr=latsclose(id_fil)
      print*,'ierr on close = ',ierr

      stop
      end

      subroutine topo(itopo,ils1,xt,xtm,ils,rls,sinl,weight
     *, mlsort,lsort,sgeo)
c
      parameter (im=360,jm=181,igridg=0)
      parameter (jtrun=2*((1+im/3)/2),mlmax=jtrun*(jtrun+1)/2)
      parameter (imjm=im*jm) 
C         
C         max number of point in lat
C         
      parameter (nlatm=24)
c
      dimension ils1(2160,1080)
      dimension ibits(2160,nlatm)
      logical bils(im,jm)
c
      dimension itopo(2160,1080)
      dimension x(2160,nlatm)
      dimension xt(im,jm),xtm(im,jm),ils(im,jm),rls(im,jm)
      dimension xtx(im,jm)
      dimension filt(mlmax), sgeo(mlmax,2,5)
      common/pol/ poly(mlmax,jm/2),dpoly(mlmax,jm/2)
      dimension sinl(jm),mlsort(jtrun,jtrun),lsort(mlmax)
      dimension alat(jm),weight(jm)
      dimension azero(100)
C         
C         do not filter the silloette topo
C
      ifilt=0

c
c  origin of data is 0 deg long, 90 deg s.
c  form land-sea bit mask
c
      pi= 4.0*atan(1.0)
C         
C         number of 10' points in the target grid box dlon
C         for a 2.5 deg grid this is 15
C
      iav= 2*((1+2160/im)/2) 
      if(iav.gt.nlatm) then 
        print*,'ERROR           !!!! iav = ',iav,
     $       ' but max point sin lat slab is ',nlatm
        stop 'nlatm bound'
      end if

C
C         iav= 8

      do jq=1,jm 

        if(igridg.eq.1) then
C         
C         gaussian grid
C         
          alat(jq)= asin(sinl(jq))
        else
C         
C         uniform lat grid
C         
          alat(jq)= -0.5*pi+(jq-1.)*pi/(jm-1.)
        endif
C         
C         location of the grid box center in grid units of the 10' data
C
        rjj= 1080.0*(alat(jq)/pi+0.5)+0.5
C         
C         starting south point
C
        jj= rjj-0.5*iav
C         
C         number of points in an equal area box, set max to 50 (~ 8 deg)
C         e.g, for 2.5 deg grid at 45 N = 15/.707 = 21
C         at 90 N = 15/0.001 = 15000
C
        iavi= iav/(cos(alat(jq))+0.001)
C         
C         equal lon/lat box
C
        iavi=iav
        iavi= 2*(iavi/2)
        iavi= min(50,iavi)
C        
C         scan from south-north in 10' grid boxes in the 
C         target grid box lat band (2160,iav)
C
        do j=1,iav
          jp= jj+j-1
          jp= max(1,jp)
          jp= min(1080,jp)
          do i=1,2160
            ibits(i,j)= ils1(i,jp)
            x(i,j)= itopo(i,jp)
            if(ibits(i,j).eq.0) x(i,j)= 0.0
          end do
        end do
C        
C         siloette topography
C
        call ciloet(jq,iav,iavi,im,x,
     $       ils(1,jq),rls(1,jq),
     $       xt(1,jq),xtm(1,jq),ibits)
c
        do i=1,im
          bils(i,jq)= ils(i,jq).eq.1 
        end do

      end do

C         
C         filtering for model applications
C
      if(ifilt.eq.1) then
c
      jm2= jm/2
      call lgndr(jm2,jtrun,mlmax,mlsort,poly,dpoly,sinl)
c
      do 251 i=1,imjm
      xt(i,1)= xt(i,1)*9.80616
      xtm(i,1)= xtm(i,1)*9.80616
      if(.not.bils(i,1)) xt(i,1)= 0.0
      if(.not.bils(i,1)) xtm(i,1)= 0.0
  251 continue
      call shft(im,jm,1,xtm)
      call shft(im,jm,1,xt)
c
      call tranrs(0,im,jm,mlmax,poly,weight,xtm,sgeo)
      call tranrs(0,im,jm,mlmax,poly,weight,xt,xtx)
c
c  filtered terrain
c
      azero(2)= 0.5
      azero(3)= 0.75
      azero(4)= 1.0
      azero(5)= 1.5
      call filter(azero(2),lsort,mlmax,jtrun,filt,xtx,sgeo(1,1,2))
      call filter(azero(3),lsort,mlmax,jtrun,filt,xtx,sgeo(1,1,3))
      call filter(azero(4),lsort,mlmax,jtrun,filt,xtx,sgeo(1,1,4))
      call filter(azero(5),lsort,mlmax,jtrun,filt,xtx,sgeo(1,1,5))
c
      iqp= 2
      call transr(im,jm,mlmax,poly,sgeo,xtx,iqp,'ichar','jchar')
      call transr(im,jm,mlmax,poly,sgeo(1,1,2),xtx,iqp,'ichar','jchar')
      call transr(im,jm,mlmax,poly,sgeo(1,1,3),xtx,iqp,'ichar','jchar')
      call transr(im,jm,mlmax,poly,sgeo(1,1,4),xtx,iqp,'ichar','jchar')
      call transr(im,jm,mlmax,poly,sgeo(1,1,5),xtx,iqp,'ichar','jchar')

      endif
c
      return
      end

      subroutine ciloet(jq,iav,iavi,lenv,x,ils,rls,xt,xtm,ibits)
      dimension x(2160,iav),xt(lenv),ils(lenv),xtm(lenv),rls(lenv)
      dimension ibits(2160,iav)
c
      iavh= iavi/2
      oiav2= 1.0/(iav*iavi)
C         
C         lenv is the number of grid points in x (lon)
C
      do ix=1,lenv
        ii= 0.5+(ix-1.)*2160./float(lenv)
        ii= ii-iavh
        sum= 0.0
        sumb= 0.0
        summ= 0.0
C         
C         sum up the highest point in each lat band
C         and the land/sea mask
C
        do j=1,iav
          xmax= 0.0
          do i=1,iavi
            il= i+ii
            if(il.lt.1) il= 2160+il
            if(il.gt.2160) il=il-2160
            sumb= sumb+ibits(il,j)
            xmax= max(xmax,x(il,j))
          end do
          sum= sum+xmax
        end do
C         
C         sum in x, the highest point in y
C
        do i=1,iavi
          ymax= 0.0
          il= i+ii
          if(il.lt.1) il= 2160+il
          if(il.gt.2160) il=il-2160
          do j=1,iav
            summ= summ+x(il,j)
            ymax= max(ymax,x(il,j))
          end do
          sum= sum+ymax
        end do
C         
C         30.48 must be a unit conversion (units of deg?)
C
        xt(ix)= sum*30.48/(iav+iavi)
        ils(ix)= 0.5001+sumb*oiav2
        rls(ix)=sumb*oiav2
        var= 0.0
        summ= summ*oiav2

        do  j=1,iav
          do  i=1,iavi
            il= i+ii
            if(il.lt.1) il= 2160+il
            if(il.gt.2160) il=il-2160
            var= var+(x(il,j)-summ)**2
          end do
        end do

        xtm(ix)= 30.48*sqrt(var*oiav2)
      end do

c
      return
      end

