      program newice

ccc      parameter (im=144,jm=im/2,igauss=1)

ccc      parameter (im=144,jm=73,
ccc     $     igauss=0,rlat0=-90.0,dlat=2.5)

ccc      parameter (im=144,jm=72,
ccc     $     igauss=0,rlat0=-88.75,dlat=2.5,
ccc     $     rlon0=0,dlon=2.5)

C         
C         the AMIP II BCS grid
C
ccc      parameter (im=360,jm=180,
ccc     $     igauss=0,rlat0=-89.5,dlat=1.0,
ccc     $     rlon0=0.5,dlon=1.0)

ccc      parameter (im=288,jm=145)
ccc      parameter (im=360,jm=181)
C         
C ncep 0.5 global grid         
C
      parameter (im=720,jm=361,
     $     igauss=0,rlat0=-90.0,dlat=0.5,
     $     rlon0=0.0,dlon=0.5)


      parameter (jtrun= 2*((1+im/3)/2),mlmax=jtrun*(jtrun+1)/2)
      parameter (idim2= mlmax*2)
c
      dimension xt(im,jm),xtm(im,jm)
      dimension ils(im,jm),rls(im,jm)
      dimension sgeo(mlmax,2,5)
c
      dimension weight(jm),sinl(jm),alat(jm)
      dimension mlsort(jtrun,jtrun),lsort(mlmax)

      dimension ils1(2160,1080)
      dimension itopo(2160,1080)
      logical bils(im,jm)
c
      parameter (imjm= im*jm)
c
      dimension msort(mlmax)
c
      character*48 gsstfil,galbfil,gwetfil,glz0fil,tsstfil,tclimfil
     *, topofil,tdevfil,ilsfil,uaclim,climof,spgeo,lsice
      character*8 cdtg

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

      pi= 4.0*atan(1.0)
      iunit_ctl=99
      iunit_dat=98


C         
C...         define the latitudes
C

      do j=1,jm
ccc        alat(j)= -0.5*pi+(j-1.0)*pi/(jm-1.0)
        alat(j)= (rlat0*pi/180.0)+(j-1)*dlat*(pi/180.0)
ccc        print*,j,alat(j)*(180.0/pi)
      end do

      if(igauss.eq.1) then
        call gausl3(jm,-1.0,1.0,weight,sinl)
        do j=1,jm
          alat(j)= asin(sinl(j))
        end do
      endif

C         
C...      read in 10 min land-sea mask
C         

      len= 2160*1080
      call nfread(ilsfil,1,-1,1,1,len,ils1,-1,cdtg,istat)
      call nfread(topofil,1,-1,1,1,len,itopo,-1,cdtg,istat)

C         
C...         interpolate
C
      call topo(itopo,ils1,xt,xtm,ils,sinl,weight,
     $     mlsort,lsort,sgeo,
     $     alat,im,jm,jtrun,mlmax,
     $     bils,rlon0)
      
C         
C...       convert to floats
C
      do i=1,im
        do j=1,jm
          rls(i,j)=float(ils(i,j))
        end do
      end do

C         
C...      output the data
C
      open(iunit_dat,file='ls.dat',access='direct',form='unformatted',
     $     recl=im*jm*4,status='unknown')

      write(iunit_dat,rec=1) rls

C         
C...      output the .ctl file
C
      open(iunit_ctl,file='ls.ctl',form='formatted',status='unknown')

      write(iunit_ctl,'(a)') 'dset ^ls.dat'
      write(iunit_ctl,'(a)') 'title land (1) sea (0) masks'
      write(iunit_ctl,'(a)') 'undef 1e20'
      write(iunit_ctl,'(a,i3,a,f8.3,1x,f8.3)')
     $     'xdef ',im,' linear ',rlon0,dlon

      if(igauss.eq.1) then
        do j=1,jm
          alat(j)= asin(sinl(j))*(180.0/pi)
        end do
        write(iunit_ctl,'(a,1x,i3,a)') 
     $       'ydef ',jm,' levels '
        write(iunit_ctl,'(10f8.3,1x)') 
     $       (alat(j),j=1,jm)
      else
        write(iunit_ctl,'(a,i3,a,f8.3,1x,f8.3)')
     $       'ydef ',jm,' linear ',rlat0,dlat
      endif

      write(iunit_ctl,'(a)') 'zdef   1 levels 1013.0'
      write(iunit_ctl,'(a)') 'tdef   1 linear 0z1jan1990 1mo'
      write(iunit_ctl,'(a)') 'vars   1'
      write(iunit_ctl,'(a)') 'w 0 0 ls mask'
      write(iunit_ctl,'(a)') 'endvars'

c
      stop
      end


      subroutine topo(itopo,ils1,xt,xtm,ils,sinl,weight,
     $     mlsort,lsort,sgeo,
     $     alat,imm,jmm,jtrun,mlmax,
     $     bils,rlon0)
c
      dimension ils1(2160,1080)
c     dimension ibits(2160,16)
      dimension ibits(2160,24)
      logical bils(imm,jmm)
c
      dimension itopo(2160,1080)
      dimension x(2160,16)
      dimension xt(imm,jmm),xtm(imm,jmm),ils(imm,jmm)
      dimension sgeo(mlmax,2,5)
      dimension sinl(jmm),mlsort(jtrun,jtrun),lsort(mlmax)
      dimension alat(jmm),weight(jmm)

c
c  origin of data is 0 deg long, 90 deg s.
c  form land-sea bit mask
c         

C         
C         iav controls the smoothness as iav dec the more the output grid
C         depends in the nears point in the mask
C         
      pi= 4.0*atan(1.0)
      iav= 2*((1+2160/imm)/2) 
ccc      iav= 8
C         
C         calculate offset in X for non 0 starting grids
C
      roff=rlon0*((2160.0+1.0)/360.0)
      ioff=roff+0.5
      print*,'qqqq ioff = ',ioff,' iav = ',iav

      do jq=1,jmm 

        rjj= 1080.0*(alat(jq)/pi+0.5)+0.5
        jj= rjj-0.5*iav
C         
C         change the # of points in x to approximate equal area grid cells
C
        iavi= iav/(cos(alat(jq))+0.001)
        iavi= 2*(iavi/2)
        iavi= min(50,iavi)
c
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
        call ciloet(jq,iav,iavi,imm,
     $       x,ils(1,jq),xt(1,jq),xtm(1,jq),ibits,ioff)
c
        do i=1,imm
          bils(i,jq)= ils(i,jq).eq.1 
        end do

      end do

      print 888,((ils(i,j),j=1,jmm),i=1,imm)
 888  format(1x,145i1)

      return
      end

      subroutine ciloet(jq,iav,iavi,lenv,
     $     x,ils,xt,xtm,ibits,ioff)
      dimension xt(lenv),ils(lenv),xtm(lenv)
      dimension ibits(2160,iav)
c
      iavh= iavi/2
      oiav2= 1.0/(iav*iavi)
      do 10 ix=1,lenv
      ii= 0.5+(ix-1.)*2160./float(lenv) + ioff
      ii= ii-iavh
      sum= 0.0
      sumb= 0.0
      summ= 0.0
      do 11 j=1,iav
      xmax= 0.0
      do 13 i=1,iavi
      il= i+ii
      if(il.lt.1) il= 2160+il
      if(il.gt.2160) il=il-2160
      sumb= sumb+ibits(il,j)
 13   continue
   11 sum= sum+xmax

      ils(ix)= 0.5001+sumb*oiav2
   10 continue
c
      return
      end

      subroutine nfread(filnam,msg,itype,istrt,numrec,len,x,itau,
     $     cdtg,istat)
c
      dimension x(len,numrec)
c
      character*8 cdtg
      character*48 filnam,blk24
      character*54 file
c
      parameter (nf=20)
      common/fncom/ cfiles(nf)
      common/fucom/ fcall
      character*48 cfiles
      logical fcall
      dimension itau2(2)
c
      data blk24/'                                                '/
      if(fcall) then
      fcall=.false.
      do 5 i=1,nf
      cfiles(i)=blk24
    5 continue
      endif
c
      do 10 k=1,nf 
      kk= k
      if(cfiles(k).eq.blk24) cfiles(k)= filnam
      if(cfiles(k).eq.filnam) go to 20 
   10 continue
   20 iun= 10+kk   
c
      call nfopen(filnam,itau,len,iun,file)
c
      do 30 j=1,numrec
      irec= istrt+j-1
      read(iun,rec=irec,err=45) (x(i,j),i=1,len),itau2,cdtg 
   30 continue
      if(itau.ge.0) close(unit=iun)
c
      if(msg.eq.0) return

ccc      print 100,file,numrec,istrt,len
ccc  100 format(1x,a54,'read: ',i3,' records starting at rec=',i4
ccc     *     ,' : len= ',i8)
ccc      print 200, itau2,cdtg
ccc       200 format(' data read for tau=',2i6,' : dtg= ',a8)

      istat= 0

      return
c
   45 print 400, file,iun,irec
  400 format(' bad read on ',a54,' : unit=',i3,' : record= ',i4)
      istat= 1
      return
      end
      subroutine nfopen(filnam,itau,len,iun,file) 
c
      character*54 file
      character*48 filnam
      character*8 status
      character*6 ctau
      common/fucom/ fcall
      logical fcall
c
      logical lex,opn
      data fcall/.true./
c
      lenr= 4*(4+len)
c
      call chlen(filnam,lenc)
      write(ctau,'(i6.6)') itau
c
      if(itau.lt.0) then
      file= filnam(1:lenc)
      else
      file= filnam(1:lenc)//ctau
      endif
c
      inquire(file=file,exist=lex,opened=opn)
      if(opn) return
c
      if(lex) then 
      status='old' 
      else
      status='new' 
      endif
      print*, file,'status=',status
c
      open(unit=iun,file=file,access='direct',form='unformatted'
     *, recl=lenr,status=status)
c
      print 100, filnam,iun,lenr 
  100 format(1x,a54,' opened as unit=',i3,' : lenr=',i9,' bytes ')
      return 
      end

      subroutine chlen(file,lenc)
      character*1 file(*)
      character*1 blnk1
      data blnk1/' '/
      lenc= 0
      do 1 i=1,100
      if(file(i).eq.blnk1) return  
      lenc= i
    1 continue
      return
      end

      subroutine gausl3 (n,xa,xb,wt,ab) 
c         
c weights and abscissas for nth order gaussian quadrature on (xa,xb). 
c input arguments   
c n  -the order desired       
c xa -the left endpoint of the interval of integration      
c xb -the right endpoint of the interval of integration     
c output arguments  
c ab -the n calculated abscissas        
c wt -the n calculated weights
c         
      implicit double precision (a-h,o-z)
c
      real  ab(n) ,wt(n),xa,xb     
c         
c machine dependent constants---        
c  tol - convergence criterion for double precision iteration         
c  pi  - given to 15 significant digits 
c  c1  -  1/8                     these are coefficients in mcmahon"s 
c  c2  -  -31/(2*3*8**2)          expansions of the kth zero of the   
c  c3  -  3779/(2*3*5*8**3)       bessel function j0(x) (cf. abramowitz,        
c  c4  -  -6277237/(3*5*7*8**5)   handbook of mathematical functions).
c  u   -  (1-(2/pi)**2)/4     
c         
      data tol/1.d-14/,pi/3.14159265358979/,u/.148678816357662/       
      data c1,c2,c3,c4/.125,-.080729166666667,.246028645833333,       
     1                 -1.82443876720609 /        
c         
c maximum number of iterations before giving up on convergence        
c         
      data maxit /5/
c         
c arithmetic statement function for converting integer to double      
c         
      dbli(i) = dble(float(i))
c         
      ddif = .5d0*(dble(xb)-dble(xa))   
      dsum = .5d0*(dble(xb)+dble(xa))   
      if (n .gt. 1) go to 101 
      ab(1) = 0.    
      wt(1) = 2.*ddif         
      go to 107     
  101 continue      
      nnp1 = n*(n+1)
      cond = 1./sqrt((.5+float(n))**2+u)
      lim = n/2     
c         
      do 105 k=1,lim
         b = (float(k)-.25)*pi
         bisq = 1./(b*b)      
c         
c rootbf approximates the kth zero of the bessel function j0(x)       
c         
         rootbf = b*(1.+bisq*(c1+bisq*(c2+bisq*(c3+bisq*c4))))        
c         
c      initial guess for kth root of legendre poly p-sub-n(x)         
c         
         dzero = cos(rootbf*cond)       
         do 103 i=1,maxit     
c         
            dpm2 = 1.d0       
            dpm1 = dzero      
c         
c       recursion relation for legendre polynomials         
c         
            do 102 nn=2,n     
               dp = (dbli(2*nn-1)*dzero*dpm1-dbli(nn-1)*dpm2)/dbli(nn)
               dpm2 = dpm1    
               dpm1 = dp      
  102       continue
            dtmp = 1.d0/(1.d0-dzero*dzero)        
            dppr = dbli(n)*(dpm2-dzero*dp)*dtmp   
            dp2pri = (2.d0*dzero*dppr-dbli(nnp1)*dp)*dtmp   
            drat = dp/dppr    
c         
c       cubically-convergent iterative improvement of root  
c         
            dzeri = dzero-drat*(1.d0+drat*dp2pri/(2.d0*dppr))         
            ddum= dabs(dzeri-dzero)
         if (ddum .le. tol) go to 104  
            dzero = dzeri     
  103    continue   
         print 504
  504    format(1x,' in gausl3, convergence failed')         
  104    continue   
         ddifx = ddif*dzero   
         ab(k) = dsum-ddifx   
         wt(k) = 2.d0*(1.d0-dzero*dzero)/(dbli(n)*dpm2)**2*ddif       
         i = n-k+1  
         ab(i) = dsum+ddifx   
         wt(i) = wt(k)        
  105 continue      
c         
      if (mod(n,2) .eq. 0) go to 107    
      ab(lim+1) = dsum        
      nm1 = n-1     
      dprod = n     
      do 106 k=1,nm1,2        
         dprod = dbli(nm1-k)*dprod/dbli(n-k)      
  106 continue      
      wt(lim+1) = 2.d0/dprod**2*ddif    
  107 return        
      end

