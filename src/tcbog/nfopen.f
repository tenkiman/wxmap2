      subroutine nfopen(filnam,msg,iread,itau,itype,len,iun,file,istat) 
c
      implicit none
c
      character*54 file
      character*48 filnam
      character*8 status
      character*6 ctau
c
      logical lex,opn,iread
      integer lenr,len,itau,lenc,iun,itype,msg,istat
c
      lenr= 8*(2+len)
      if(itype.ne.0) lenr= 8*(2+(len+1)/2)
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
      if(opn) then
      istat= 0
      return
      endif
c
      if(lex) then 
      status='old' 
      istat= 0
      else
      status='new' 
c
      if(iread) then
      istat=2
      print 500, file,istat
  500 format(1x,a54,' missing, istat=',i1)
      return
      endif
c
      endif
c
      open(unit=iun,file=file,access='direct',form='unformatted'
     *, recl=lenr,status=status)
c
      if(msg.lt.2) return
c
      print 100, status(1:3),filnam,iun,lenr 
  100 format(1x,a3,1x,a54,' opened as unit=',i3,' : lenr=',i9,' bytes ')
      return 
      end
