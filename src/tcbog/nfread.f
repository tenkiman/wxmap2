      subroutine nfread(fnam,msg,itype,istrt,nrec,len,x,itau,cdtg,istat)
c
c  subroutine to read NOGAPS history files (but can also be used for
c  general purpose IO).  file structure is FORTRAN direct access.  as an
c  option can retrieve data written in IEEE format (e.g. SUN format) and
c  convert it to CRAY 64 bit data.
c
c  formal parameters
c
c  INPUT:
c
c  fnam: character*48 path/filename to data to be read.  path can be
c    relative or absolute but must be pre-existing.  actual filename can  
c    have a indexing string appended depending of value of formal parameter 
c    'itau'.  see example below.           
c
c  msg: flag to control information prints about file activity
c        =0, no prints
c        =1, print info about read or write action
c        =2, print info about file opening, reading and writing action
c        = anything else, same as 2
c
c  itype:  data type
c        = 0, do not unpack data, used if file data is already CRAY format  
c        = 1 (or -1), unpack from IEEE integer to CRAY integer 
c        = 2 (or -2), unpack from IEEE float pt. to CRAY float pt.
c
c  istrt: beginning direct access index of records to be read from fnam
c
c  nrec: number of records (beginning at istrt) to be read from fnam
c
c  len:  number of data items read into array x. (note: since
c    file format is direct access, len must be the same for all records
c    on a given fnam)
c
c  itau: counter index.  if .GE. zero it is appended as a character*6
c    string to fnam, yielding a new filename which is the actual 
c    one opened for the requested data.  see example below.
c
c  OUTPUT:
c 
c  x: array that data is being read into. should have dimension at least
c    (nrec*len)
c
c  itau: counter index. integer item included with data read and returned to 
c  calling program.  the returned value of itau can be compared to the input
c    value to check data integrity.
c
c  cdtg: data-time-group character*8 item of data read and returned to calling
c    program.
c
c  istat: returned status code.
c       =0, no problems
c       =1, bad read, data not returned
c       =2  file missing, no data returned
c
c  EXAMPLE:
c 
c ********************************************************************
c
!     program test
c     
c     program to demonstrate use of subroutines nfread and nfwrits        
c     remove !'s from column 1 to get compilible code
c
!     parameter (len= 10001)
!     dimension x(len,5)
!     dimension xfull(len,5)
!     dimension ix(len,5)
!     character*48 ifile
!     character*8 cdtg
c
c  change the following path/filename to suit your interests
c
!     ifile='/a/yourname/datapath/dummy'
!     cdtg='92030412'
!     n=5
!     itau= 10
c
c  generate some test data
c
!     do 1 j=1,n
!     do 1 i=1,len
!     x(i,j)= (i+j)
!     x(i,j)=-x(i,j)**3.888
!     xfull(i,j)= x(i,j)
!     ix(i,j)= (i+j)**2
!   1 continue
c
c  this is the largest integer preserved when packed and
c  unpacked. put it at the end of the ix array.
c
!     ix(len,5)=( 2**31-1)
c
!     print*,' *** case 1 ***'
c
c  write some packed fl. pt. data and read it back in.
c  itau is .GE. 0, so it is appended to ifile, itype is
c  .GT. 0, so nfwrit returns 64 bit data with precision
c  truncated to 32 bits.
c
!     itype=  2
!     print*, ' x before packing= ',x(len,5)
!     call nfwrit(ifile,1,itype,1,n,len,x,itau,cdtg,istat)
!     print*, ' x returned from nfwrit=', x(len,5)
!     call nfread(ifile,1,itype,1,n,len,x,itau,cdtg,istat)
!     print*, ' x returned from nfread=', x(len,5)
c
!     print*,' *** case 2 ***'
c
c  write some packed integer data and read it back in
c  the data is added to ifile starting at record no. 6.
c
!     itype= 1
!     print*, ' ix before packing=', ix(len,5)
!     call nfwrit(ifile,1,itype,6,n,len,ix,itau,cdtg,istat)
!     call nfread(ifile,1,itype,6,n,len,ix,itau,cdtg,istat)
c
!     print*, ' ix after unpacking=',ix(len,5)
c
!     print*,' *** case 3 ***'
c
c  write some packed fl. pt. data and read it back in.
c  itau is .GE. 0, so it is appended to ifile, itype is
c  .LT. 0, so nfwrit returns full 64 bit data. data is
c  still written as 32 bit IEEE, however.
c
!     itype=  -2
!     print*, ' x before packing= ',x(len,5)
!     call nfwrit(ifile,1,itype,1,n,len,x,itau,cdtg,istat)
!     print*, ' x returned from nfwrit=', x(len,5)
!     call nfread(ifile,1,itype,1,n,len,x,itau,cdtg,istat)
!     print*, ' x returned from nfread=', x(len,5)
c
!     print*,' *** case 4 ***'
c
c  write some packed integer data to a file without the appended
c  counter and read it back in
c
!     itau= -1
!     itype= 1
!     print*, ' ix before packing=', ix(len,5)
!     call nfwrit(ifile,1,itype,1,n,len,ix,itau,cdtg,istat)
!     call nfread(ifile,1,itype,1,n,len,ix,itau,cdtg,istat)
c
!     print*, ' ix after unpacking=',ix(len,5)
c
!     print*,' *** case 5 ***'
c
c  write some unpacked fl. pt. data to a file and read it back in.
c  note that a different value of positive itau generates a new
c  filename which can have the different length records the full
c  precision array requires
c
!     itau= 20
!     itype= 0
!     print*, ' xfull before write= ',xfull(len,5)
!     call nfwrit(ifile,1,itype,1,n,len,xfull,itau,cdtg,istat)
!     print*, ' xfull returned from nfwrit=', xfull(len,5)
!     call nfread(ifile,1,itype,1,n,len,xfull,itau,cdtg,istat)
!     print*, ' xfull returned from nfread=', xfull(len,5)
c
c  after running this test example look at contents of your
c  target directory to verify filenames and sizes.
c
!     stop
!     end
c        
c ***END OF EXAMPLE*******************************************
c
      implicit none
c
      integer len,numrec,itype,istrt,itau,istat,msg
      real x(len,nrec)
      real xpack((len+1)/2)
c
      character*8 cdtg
      character*48 fnam,blk24
      character*54 file
c
      integer nf,icall
      parameter (nf=20)
      common/fncom/ cfiles(nf)
      common/fucom/ icall
      character*48 cfiles
      logical fcall,iread
      integer i,irec,k,kk,iun,j,ieg2cray,ierr,itp,lenx,nrec
c
      data blk24/'                                                '/
c
      fcall= icall.ne.-111
      icall= -111
      if(fcall) then
      do 5 i=1,nf
      cfiles(i)=blk24
    5 continue
      endif
c
      do 10 k=1,nf 
      kk= k
      if(cfiles(k).eq.blk24) cfiles(k)= fnam
      if(cfiles(k).eq.fnam) go to 20 
   10 continue
   20 iun= 10+kk   
c
c
      iread=.true.
      call nfopen(fnam,msg,iread,itau,itype,len,iun,file,istat)
c
      if(istat.eq.2) return
c
      if(itype.eq.0) then
c
c  no unpacking
c
      do 30 j=1,nrec
      irec= istrt+j-1
      read(iun,rec=irec,err=45) (x(i,j),i=1,len),itau,cdtg 
   30 continue
c
      else
c
c  data is packed, convert from ieee 32 bit to cray 64 bit
c
      itp= abs(itype)
      lenx= (len+1)/2
      do 40 j=1,nrec
      irec= istrt+j-1
      read(iun,rec=irec,err=45) (xpack(i),i=1,lenx),itau,cdtg
      ierr= ieg2cray(itp,len,xpack,0,x(1,j))
   40 continue
c
      endif
c 
      if(itau.ne.-2) close(unit=iun)
c
      istat= 0
      if(msg.eq.0) return
c
      print 100,file,nrec,istrt,len
  100 format(1x,a54,'read: ',i3,' records starting at rec=',i4
     *,' : len= ',i8)
c
      if(itype.eq.0) then
      print 200, itau,cdtg
  200 format(' data read for tau=',i6,' : dtg= ',a8)
      else
      print 300, itype,itau,cdtg
  300 format(' type',i2,' packed data read for tau=',i6,' : dtg= ',a8)
      endif
c
      return
c
   45 print 400, file,iun,irec
  400 format(' bad read on ',a54,' : unit=',i3,' : record= ',i4)
      istat= 1
      return
      end
