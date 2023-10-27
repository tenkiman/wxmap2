      subroutine qprntn(a,t1,t2,ibeg,jbeg,m,n)
c
c**********	may 17, 1988, this version outputs to unit 6
c**********	using write vice print
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
c t1,t2 = title (2 8-character words)
c ibeg,jbeg=lower left corner coords to be printed
c up to 43 x 83 points printed
c
      dimension a(m,n),ix(43)
      character*8 t1,t2
c
c  determine grid limits
c
      iend=min0(ibeg+42,m)
      jend=min0(jbeg+82,n)
c
   24 continue
c
c  index backwards checking for max
c
   11 xm=0.
      jendsc=min0(jend,n)
      do 14 j=jbeg,jendsc
      do 14 i=ibeg,iend
   14 xm=amax1(xm,abs(a(i,j)))
c
c  determine scaling factor limits
c
      if(xm.lt.1.e-38) xm=99.0
      xm=alog10(99.0/xm)
      kp=xm
      if(xm.lt.0.)kp=kp-1
c
c  print scaling constants
c
   12 write(6,1) t1,t2,kp,(i,i=ibeg,iend,2)
    1 format('0',a8,a8,'   k=',i3,
     2  /' ',22i6) 
      fk=10.0**kp
c
c  quickprint field
c
      do 2 j=jbeg,jend
      jli=jend-j+jbeg
      if(jli.gt.n) go to 2
      ii= 0
      if(kp.ne.0) go to 8
      do 9 i=ibeg,iend
      ii=ii+1
    9 ix(ii)=a(i,jli)+sign(.5,a(i,jli))
      go to 10
    8 do 7 i=ibeg,iend
      ii=ii+1
    7 ix(ii)=a(i,jli)*fk+sign(.5,a(i,jli))
   10 write(6,6) jli,(ix(i),i=1,ii),jli
    6 format(i4,44i3)
    2 continue
      return
      end
