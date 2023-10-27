      subroutine grhilo_proc(fld,
     $     ib,ie,jb,je,
     $     rlatc,rlonc,tough,
     $     iunit,oformat,pcntile)
c         
c         routine to find all critical points in a 2-d scalar grid (fld) 
c         
c         np is the max # of critical points
c         the i,j ; lat/lon ; and critical value are returned
c
c         
      use trkParams
      use f77OutputMeta
      use mfutils

      real*4 fld(ni,nj)

      logical verb,tough

      real        acl(np),xcl(np),ycl(np),gcl(np),lcl(np),dcl(np)
      integer     ndxl(np)
      character*1 chll(np)

      real        ach(np),xch(np),ych(np),gch(np),lch(np),dch(np)
      integer     ndxh(np)
      character*1 chlh(np)

      character oformat*24,cval*24

      verb=.false.
ccc      verb=.true.


c--       hhhhhhhhhhhhhh

      call findExtrema(fld,
     $     ib,ie,jb,je,'h',
     $     rfindGen,
     $     nh)

      do n=1,nh
        call getExtremaProps(fld,
     $       ihl(n),jhl(n),rlatc,rlonc,
     $       xch(n),ych(n),ach(n),gch(n),lch(n),dch(n))

        if(verb) print*,'HHHH ',n,xch(n),ych(n),ach(n),gch(n),lch(n),dch(n)
        chlh(n)='H'
      enddo

c--       lllllllllllllllll

      call findExtrema(fld,
     $     ib,ie,jb,je,'l',
     $     rfindGen,
     $     nl)

      do n=1,nl
        call getExtremaProps(fld,
     $       ihl(n),jhl(n),rlatc,rlonc,
     $       xcl(n),ycl(n),acl(n),gcl(n),lcl(n),dcl(n))
        chll(n)='L'
        if(verb) print*,'LLLL ',n,xcl(n),ycl(n),acl(n),gcl(n),lcl(n),dcl(n)

      enddo


CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
C         
C         output to the file
C         sort by lat
C         sort by distance (deg) from rlatc,rlonc
C
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
      
      iec=ichar_len(oformat,24)
      iec=iec+1

      write(iunit,'(i4,1x,i4)')  nh,nl
      
      if(nh.ge.1) then

        if(nh.gt.1) then
          call indexx(nh,dch,ndxh)
        else
          ndxh(1)=1
        endif
      
        do i=1,nh
          ii=nh-i+1
          cval='                        '
          val=ach(ndxh(ii))

          if((oformat(1:1).eq.'i').or.(oformat(1:1).eq.'I')) then
            ival=nint(val)
            write(cval,'('//oformat(1:iec)//')') ival
          else
            write(cval,'('//oformat(1:iec)//')') val
          endif

          write(iunit,
     $         '(a1,1x,3(f10.2,1x),g14.6,1x,2(g10.4,1x))') 
     $         chlh(ndxh(ii)),dch(ndxh(ii)),xch(ndxh(ii)),ych(ndxh(ii)),
     $         val,
     $         gch(ndxh(ii)),lch(ndxh(ii))
        end do
      endif

      if(nl.ge.1) then

        if(nl.gt.1) then
          call indexx(nl,dcl,ndxl)
        else
          ndxl(1)=1
        endif

        do i=1,nl
          ii=i
          val=acl(ndxl(ii))

          if((oformat(1:1).eq.'i').or.(oformat(1:1).eq.'I')) then
            ival=nint(val)
            write(cval,'('//oformat(1:iec)//')') ival
          else
            write(cval,'('//oformat(1:iec)//')') val
          endif

          write(iunit,
     $         '(a1,1x,3(f10.2,1x),g14.6,1x,2(g10.4,1x))') 
     $         chll(ndxl(ii)),dcl(ndxl(ii)),xcl(ndxl(ii)),ycl(ndxl(ii)),
     $         val,
     $         gcl(ndxl(ii)),lcl(ndxl(ii))

        end do
      endif

c         
      return
      end


