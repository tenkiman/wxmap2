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

