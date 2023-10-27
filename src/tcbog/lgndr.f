      subroutine lgndr(jtrun,mlmax,mlsort,poly,dpoly,sinl)
c
c  ** neprf ***, programmer tom rosmond, august 3, 1987
c
c  generate legendre polynomials and their derivatives on the
c  gaussian latitudes
c
c
c ref= belousov, s. l., 1962= tables of normalized associated
c        legendre polynomials. pergamon press, new york
c
      dimension poly(mlmax),dpoly(mlmax)
     *, mlsort(jtrun,jtrun)
c
      dimension pnm(jtrun+1,jtrun+1),dpnm(jtrun+1,jtrun+1)
c
c sinl is sin(latitude) = cos(colatitude)
c pnm(np,mp) is legendre polynomial p(n,m) with np=n+1, mp=m+1
c pnm(mp,np+1) is x derivative of p(n,m) with np=n+1, mp=m+1
c
      jtrunp= jtrun+1
c
      sn= sqrt(1.0-sinl*sinl)
       sn2i = 1.0/(1.0 - sinl*sinl)
       c1 = sqrt(2.0)
c
       pnm(1,1) = 1.0/sqrt(2.0)
      theta=-atan(sinl/sqrt(1.0-sinl*sinl))+2.0*atan(1.0)
c
      do 20 n=1,jtrun
       np = n + 1
      fn=n
       fn2 = fn + fn
       fn2s = fn2*fn2
c eq 22
      c1= c1*sqrt(1.0-1.0/fn2s)
      c3= c1/sqrt(fn*(fn+1.0))
       ang = fn*theta
       s1 = 0.0
       s2 = 0.0
       c4 = 1.0
       c5 = fn
       a = -1.0
       b = 0.0
c
      do 27 kp=1,np,2
       k = kp - 1
      s2= s2+c5*sin(ang)*c4
      if (k.eq.n) c4 = 0.5*c4
      s1= s1+c4*cos(ang)
       a = a + 2.0
       b = b + 1.0
      fk=k
       ang = theta*(fn - fk - 2.0)
       c4 = (a*(fn - b + 1.0)/(b*(fn2 - a)))*c4
       c5 = c5 - 2.0
   27 continue
c eq 19
       pnm(np,1) = s1*c1
c eq 21
       pnm(np,2) = s2*c3
   20 continue
c
      do 4 mp=3,jtrunp
       m = mp - 1
      fm= m
       fm1 = fm - 1.0
       fm2 = fm - 2.0
       fm3 = fm - 3.0
      c6= sqrt(1.0+1.0/(fm+fm))
c eq 23
       pnm(mp,mp) = c6*sn*pnm(m,m)
      if (mp - jtrunp) 3,4,4
    3 continue
       nps = mp + 1
c
      do 41 np=nps,jtrunp
       n = np - 1
      fn= n
       fn2 = fn + fn
       c7 = (fn2 + 1.0)/(fn2 - 1.0)
       c8 = (fm1 + fn)/((fm + fn)*(fm2 + fn))
      c= sqrt((fn2+1.0)*c8*(fm3+fn)/(fn2-3.0))
      d= -sqrt(c7*c8*(fn-fm1))
      e= sqrt(c7*(fn-fm)/(fn+fm))
c eq 17
       pnm(np,mp) = c*pnm(np-2,mp-2)
     1 + sinl*(d*pnm(np-1,mp-2) + e*pnm(np - 1,mp))
   41 continue
    4 continue
c
      do 50 mp=1,jtrun
      mpm= mp-1
      do 50 np=mp,jtrun
       cf= sqrt(float((np*np-mpm*mpm)*(2*np-1))/float(2*np+1))
c der
      dpnm(np,mp)= -sn2i*(cf*pnm(np+1,mp)-float(np)*sinl*pnm(np,mp))
   50 continue
c
      do 71 m=1,jtrun
      do 71 l=m,jtrun
      ml= mlsort(m,l)
      poly(ml)= pnm(l,m)
      dpoly(ml)=dpnm(l,m)
   71 continue
      dpoly(1)= 0.0
      return
      end
