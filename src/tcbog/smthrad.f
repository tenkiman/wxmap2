      subroutine smthrad(a,b,rmask,id,jd,ricent,rjcent,
     $     ib,ie,jb,je,r1,r2,
     $     anu,npass,numbnu,io) 
c
c***************************************************************
c***************************************************************
c*****                                                     *****
c*****         routine to smooth a cartesian field         *****
c*****           in an annulus centered about an           *****
c*****             interior point (icent,jcent)            *****
c*****                                                     *****
c***************************************************************
c***************************************************************
c
      dimension a(id,jd),b(id,jd),rmask(id,jd),anu(numbnu) 
      dr=r2-r1
      pi=3.141592654
c
c....       create the mask
c
      do  i=ib,ie
        do  j=jb,je
          rmask(i,j)=0.0
          rad=sqrt((i-ricent)**2+(j-rjcent)**2)
          if(rad.lt.r1) rmask(i,j)=1.0
          if(rad.ge.r1.and.rad.le.r2) 
     $         rmask(i,j)=1.0-((rad-r1)/dr)
          rmask(i,j)=1.0
        end do
      end do


c
c...     output unsmoothed field if io.ne.0
c         
      if(io.ne.0) call qprntn(rmask,'rmask   ','        ',ib,jb,id,jd)
      if(io.ne.0) call qprntn(a,'unsmthd ','        ',ib,jb,id,jd)
      do i=ib,ie
        do j=jb,je
          b(i,j)=a(i,j)
        end do
      end do

      do nn=1,npass
        do  l=1,numbnu
          do i=ib,ie
            do  j=jb,je
c
c...        bypass smoothing if outside the annulus
c
              b(i,j)=b(i,j)*(1.0-anu(l))**2
     $             +0.5*anu(l)*(1.0-anu(l))*(b(i+1,j)+b(i-1,j)+b(i,j+1)+b(i,j-1))
     $             +0.25*(anu(l)**2)*(b(i-1,j-1)+b(i-1,j+1)+b(i+1,j-1)+b(i+1,j+1))
            end do
          end do

      do  i=ib,ie
        do  j=jb,je
          a(i,j)=b(i,j)*rmask(i,j)
     $         +a(i,j)*(1.0-rmask(i,j))
        end do
      end do

        end do
      end do


c
c...     calculate response function assuming fourier basis
c
      iresp=0
      if(iresp.eq.0) go to 300
      print 200,npass,numbnu 
200   format(' ','smoothing function analysis'/
     1  ' ',5x,'number of passes = ',i2/
     2  ' ',5x,'number of elements per pass = ',i2)
      do 202 k=1,numbnu
      print 201,k,anu(k)
201   format(' ',7x,'k = ',i2,'  smoothing coefficient nu = ',f6.3)
202   continue
      do 210 i=2,id
      b(i,1)=float(i)
      b(i,2)=1.0
      do 215 mm=1,numbnu
      b(i,2)=b(i,2)*(1.0-anu(m)*(1.0-cos(2.0*pi/float(i))))
215   continue
      b(i,2)=b(i,2)**npass
210   continue
      print 222
222   format('0','response function as a function of wavelength ',
     1  ' in grid units'//)
      do 224 i=2,id
      print 225,i,b(i,2)
225   format(' ',10x,'i = ',i2,'  r = ',f10.5)
224   continue
300   continue
c
c...     output smoothed field if io ne 0
c
      if(io.ne.0) call qprntn(a,'smthed  ',' rad fld',ib,jb,id,jd)
      return
      end
