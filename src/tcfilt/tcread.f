      subroutine tcread (iunit,ntc,TCs,verb)

      include 'tctype.h'

      type (TC) , dimension(10) :: TCs

      logical verb,ngtrp
      character card*80
      character stmid*3

      ngtrp=.true.
      ngtrp=.false.

      if(ngtrp) read(iunit,'(a)',iostat=ioe) card

      ioe=0
      ntc=0
      do while (ioe .eq. 0)

        read(iunit,'(a)',iostat=ioe) card
        if(card(1:3).eq.'999'.or.ioe.eq.-1) then
          return
        endif

        if(ngtrp) then
          read(card(1:3),'(f3.1)') rlat
          read(card(6:9),'(f4.1)') rlon
          read(card(11:13),'(i3)') ivmax
          stmid(1:2)=card(16:17)
          stmid(3:3)=card(19:19)
          if(card(4:4).eq.'S') rlat=-rlat
          if(card(10:10).eq.'W') rlon=360.0-rlon
        else
C          stmid=card(12:14)
C          read(card(16:18),'(i3)') ivmax
C          read(card(25:29),'(f5.1)') rlat
C          read(card(31:35),'(f5.1)') rlon
C         
C new form         
C
          read(card(1:3),'(a)') stmid
          read(card(5:8),'(f4.1)') rlat
          read(card(10:14),'(f5.1)') rlon
          ivmax=999

        endif
        
        ntc=ntc+1

        TCs(ntc)%stmid=stmid
        TCs(ntc)%lat=rlat
        TCs(ntc)%lon=rlon
        TCs(ntc)%vmax=ivmax


        if(verb) then
          print*,'tc card ',ntc,card,ioe
          print*,'stmid ',stmid,ivmax,rlat,rlon
        endif

      end do

      return
      end
