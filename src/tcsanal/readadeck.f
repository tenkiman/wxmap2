      subroutine readadeck(iunit,rlat,rlon,nf,nposits)
      include 'params.h'
      real rlat(nf),rlon(nf)
      character card*120
C         123456789+123456789+123456789+123456789+123456789+123456789+
C         WP, 22, 2001092112, 72, JAVN,  96, 359N, 1495E,   26
      character ihemns*1,ihemew*1
      nposits=0
      i=0
      do while(i.eq.0) 
        read(iunit,('(a)'),end=100) card
        print*,'card: ',card
        nposits=nposits+1
        read(card,('(34x,i4,a1,2x,i4,a1)'),end=100) ilat,ihemns,ilon,ihemew
        rlat(nposits)=ilat*0.1
        rlon(nposits)=ilon*0.1
        if(ihemew.eq.'W') rlon(nposits)=360.0-rlon(nposits)
        if(ihemns.eq.'S') rlat(nposits)=-rlat(nposits)
        if(verb) then
          print*,'readadeck: ',nposits,rlat(nposits),rlon(nposits)
        endif
      end do
 100  continue
      return
      end
      
      
      

