      subroutine readtc(iunit,rlat,rlon,nf)
      include 'params.h'
      real rlat(nf),rlon(nf)
      character card*80
C         123456789+123456789+123456789+123456789+123456789+123456789+
C         WP, 22, 2001092112, 72, JAVN,  96, 359N, 1495E,   26
      character ihemns*1,ihemew*1
      nc=0
      do while(1) 
        read(iunit,('a'),end=100) card
        nc=nc+1
        read(card,('(34x,i4,a1,2x,i4,a1)')) ilat,ihemns,ilon,ihemew
        rlat(nc)=ilat*0.1
        rlon(nc)=ilon*0.1
        if(ihemew.eq.'W') rlon(nc)=360.0-rlon(nc)
        if(verb) then
          print*,'readtc: ',nc,rlat(nc),rlon(nc)
        endif
      end do
 100  continue
      return
      end
      
      
      

