      subroutine qprntn(a,qtitle,ibeg,jbeg,m,n,iskip,iunit)
c
c**********	12 APR 91 this version outputs to iunit 
c**********	using write on the Cray Y/MP 
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****       qprint output routine (corrected 4/26/86)     *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
c a= fwa of m x n array
c qtitle - title
c ibeg,jbeg=lower left corner coords to be printed
c up to 43 x 83 points printed
c         
      dimension a(m,n),ix(81)
      character qtitle*24
c
c  determine grid limits
c
      if(iskip.eq.0) iskip=1
      iend=min0(ibeg+79*iskip,m)
      jend=min0(jbeg+79*iskip,n)
c
   24 continue
c
c  index backwards checking for max
c
   11 xm=0.
      jendsc=min0(jend,n)
      do j=jbeg,jendsc,iskip
      jend_qp = j
      do i=ibeg,iend,iskip
        xm=amax1(xm,abs(a(i,j)))
      end do
      end do
c
c  determine scaling factor limits
c
      if(xm.lt.1.0e-32.or.xm.eq.0.0) xm=99.0
      xm=alog10(99.0/xm)
      kp=xm
      if(xm.lt.0.0)kp=kp-1
c
c  print scaling constants
c
   12 write(iunit,1) qtitle,kp,iskip,(i,i=ibeg,iend,2*iskip)

    1 format('0',a,'   k=',i3,' iskip=',i2,/,' ',41i6) 
      fk=10.0**kp
c
c  quickprint field
c
      do 2 jli=jend_qp,jbeg,-iskip
        ii= 0
        if(kp.eq.0) then 
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)+sign(.5,a(i,jli))
          end do
        else
          do i=ibeg,iend,iskip
            ii=ii+1
            ix(ii)=a(i,jli)*fk+sign(.5,a(i,jli))
          end do
        end if
        write(iunit,'(i4,81i3)') jli,(ix(i),i=1,ii),jli
2     continue
      return
      end
      function qsatw(t,p)
c
c     t is temperature of air in deg celcius.
c     ta is temperature in deg kelvin
c     p is pressure in mb
c     qsatw is saturation specific humidity in g/g (over water)
c
      data ps/1013.246/,ts/373.16/
c
      ta = t
      if(t .lt. 100.0) then
         ta = t + 273.16
      end if
      e1=11.344*(1.0-ta/ts)
      e2=-3.49149*(ts/ta-1.0)
      f1=-7.90298*(ts/ta-1.0)
      f2=5.02808*alog10(ts/ta)
      f3=-1.3816*(10.0**e1-1.0)*1.e-7
      f4=8.1328*(10.0**e2-1.0)*1.e-3
      f5=alog10(ps)
      f=f1+f2+f3+f4+f5
      es=10.0**f
      qsatw=.62197*es/(p-0.378*es)
      return
      end


      subroutine load2(a,b,ni,nj)
      dimension a(ni,nj),b(ni,nj)
      do i=1,ni
        do j=1,nj
          b(i,j)=a(i,j)
        end do
      end do
      return
      end


      subroutine bssl5(xi,xj,f,m,n,res)
c
c  general purpose two dimensional bessel interpolation
c
c  d. henson  --  april, 1987
c
c  arguments --
c
c   xi  -- i coordinate (real) 1.le.i.le.m
c   xj  -- j coordinate (real) 1.le.j.le.n
c   f   -- array to be interpolated
c   m   -- number of columns in f
c   n   -- number of rows in f
c   res -- returned interpolated value at f(xi,xj)
c
c   note----xi and xj are not tested for legal range
c
      dimension f(m,n)
      dimension fr(4)
c
      mm1 = m-1
      nm1 = n-1
      ii = xi
      j = xj
      r = xi-ii
      s = xj-j
c
c   r and s are the fractional parts of xi and xj respectively
c
c   test for top/right edge, border, or interior 
c
      if(ii.ge.2 .and. j.ge.2 .and. ii.lt.mm1 .and. j.lt.nm1)
     $  go to 10
c
      if(ii.lt.m .and. j.lt.n) go to 5 
c
c   top or right edge
c
      if(ii.eq.m .and. j.eq.n) then
        res = f(m,n)
      else if(ii.eq.m) then
        res = (1.-s)*f(ii,j)+s*f(ii,j+1)
      else if(j.eq.n) then
        res = (1.-r)*f(ii,j)+r*f(ii+1,j)
      endif
      return
c
 5    continue
c
c   border zone -- use bilinear interpolation
c
      res = (1.-s)*((1.-r)*f(ii,j)+r*f(ii+1,j))
     $  +s*((1.-r)*f(ii,j+1)+r*f(ii+1,j+1))
      return
c
 10   continue
c   interior zone
c
c   interpolate 4 columns (i-1,i,i+1,i+2) to j+s and store in fr(1)
c   through fr(4)
c
      r1 = r-0.5
      r2 = r*(r-1.)*0.5
      r3 = r1*r2*0.3333333333334
      s1 = s-0.5
      s2 = s*(s-1.)*0.5
      s3 = s1*s2*0.3333333333334
c
      k = 0
      im1 = ii-1
      ip2 = ii+2
c
      do 20 i = im1,ip2
      k = k+1
      u = (f(i,j)+f(i,j+1))*0.5
      del = f(i,j+1)-f(i,j)
      udel2 = (f(i,j+2)-f(i,j+1)+f(i,j-1)-f(i,j))*0.5
      del3 = f(i,j+2)-f(i,j+1)-2.*del+f(i,j)-f(i,j-1)
      fr(k) = u+s1*del+s2*udel2+s3*del3
 20   continue
c
c   interpolate the fr row to ii+r
c
      u = (fr(2)+fr(3))*0.5
      del = fr(3)-fr(2)
      udel2 = (fr(4)-fr(3)+fr(1)-fr(2))*0.5
      del3 = fr(4)-fr(3)-2.*del+fr(2)-fr(1)
c
      res = u+r1*del+r2*udel2+r3*del3
c
      return
      end

      subroutine indexx(n,arrin,indx)
      dimension arrin(n),indx(n)
      do 11 j=1,n
        indx(j)=j
 11   continue
      l=n/2+1
      ir=n
10    continue
        if(l.gt.1)then
          l=l-1
          indxt=indx(l)
          q=arrin(indxt)
        else
          indxt=indx(ir)
          q=arrin(indxt)
          indx(ir)=indx(1)
          ir=ir-1
          if(ir.eq.1)then
            indx(1)=indxt
            return
          endif
        endif
        i=l
        j=l+l
20      if(j.le.ir)then
          if(j.lt.ir)then
            if(arrin(indx(j)).lt.arrin(indx(j+1)))j=j+1
          endif
          if(q.lt.arrin(indx(j)))then
            indx(i)=indx(j)
            i=j
            j=j+j
          else
            j=ir+1
          endif
        go to 20
        endif
        indx(i)=indxt
      go to 10
      end

      function ichar_len(c,imax)
      character*1 c(imax)
      iend=-1
      ii=imax
      do while (iend.eq.-1.and.ii.le.imax)
        if(c(ii).ne.' ') iend=ii
        ii=ii-1
      end do  
      if(ii.gt.imax) then
        ichar_len=imax
      else
        ichar_len=iend-1
      end if
      return
      end




       


