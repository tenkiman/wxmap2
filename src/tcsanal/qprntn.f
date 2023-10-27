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
