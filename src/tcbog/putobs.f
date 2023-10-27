      subroutine putobs(len,inam,idtg,jtau,iflap,ichk)
      common/cran1/aid(61440)
      common/cran2/afile
      character*8 afile
      dimension bid(61440)
      character*8 iid(24)
      half precision bid
      equivalence (aid,bid,iid)
      dimension idtg(3),irec(2)
      character*1 iflap
      character*8 irec,idtg
      character*40 irpt(480)
      equivalence (aid(25),irpt)
c
      call syslblc(inam,idtg,jtau,iflap,irec)
      iid(1)=irec(1)
      iid(2)=irec(2)
      iid(4)='fp64'
      call cwriter(afile,irec,aid,len,istat)
      ichk=istat
c
      print 800,jtau
      do 100 k=1,480
      print 805,k,irpt(k)
  100 continue
c
c          format statements
c
  800 format(' ----------output for tau ',i3,'----------')
  805 format('      record number:',i3,':',a40)
c
      return
      end
